//
//  IntonareMicPlugin.swift
//
//  Native microphone capture for iOS. The Swift twin of IntonareMicPlugin.java.
//
//  WHY THIS EXISTS
//  ---------------
//  On iOS the mic used to come from WKWebView's getUserMedia. WebKit answers that
//  by putting the audio session into a voice-chat flavour with Voice Processing IO
//  switched on. Voice processing is built for phone calls: it ducks everything the
//  app plays, and it colours the signal the pitch detector reads. Nothing in JS can
//  turn that off. IntonarePlugin.setAudioMode() only wins part of the level back.
//
//  Capturing with AVAudioEngine instead means WebKit never touches the mic. The
//  session stays in playAndRecord with mode .measurement, which asks iOS for the
//  least processed signal and does not duck output.
//
//  THE CONTRACT WITH JS (do not change one side without the other)
//  ---------------------------------------------------------------
//  Same as Android. JS finds the plugin through Capacitor.isPluginAvailable
//  ('IntonareMic'), so registering this class is the only switch.
//    start({ aec, ns, agc, sendPcm }) -> { started, sampleRate, frameSamples, ... }
//    stop()                           -> { stopped: true }
//    event "micFrame" { pcm, samples, sampleRate }
//      pcm is base64 of little-endian int16, mono, `samples` long.
//  sampleRate is whatever the hardware runs at (often 48000). JS rebuilds its
//  filters for it, so nothing here resamples.
//
//  PERMISSION
//  ----------
//  Android asks in MainActivity. iOS has no Capacitor Permissions plugin, so start()
//  asks for itself. A denial rejects with a message containing "denied", which is
//  the exact word _requestMicPermission() in JS looks for.
//
//  AEC
//  ---
//  aec:true (surfaces that play a reference and listen at the same time) turns on
//  Voice Processing IO for the input node. That brings echo cancellation back and
//  also brings the quieter output back, so those surfaces sound the way they did
//  before. aec:false surfaces get the clean .measurement path. ns and agc are
//  accepted and ignored: iOS has no separate switch for them, and JS keeps both off
//  everywhere anyway.
//
//  DELIBERATELY NOT HERE (read IntonareAudioSession.swift first)
//  -------------------------------------------------------------
//  - No NotificationCenter observers. A route-change observer that calls
//    setCategory once looped forever on the main thread. Everything below is
//    one-shot and JS-triggered.
//  - No setPreferredIOBufferDuration or setPreferredSampleRate.
//  KNOWN GAP: if headphones are plugged in or pulled out while the mic is live,
//  the engine stops and the tuner goes quiet until the mic is toggled. Handle that
//  from a device measurement, with a guard against re-entry, not before.
//
//  CONCURRENCY
//  -----------
//  Start, stop and IntonarePlugin.setAudioMode all run on IntonarePlugin
//  .sessionQueue, so the session category can never be changed by two callers at
//  once. The tap runs on a real-time audio thread: it only converts samples and
//  hands them to emitQueue. It never touches the session or the bridge.
//

import Foundation
import Capacitor
import AVFoundation

@objc(IntonareMicPlugin)
public class IntonareMicPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IntonareMicPlugin"
    public let jsName = "IntonareMic"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "ping", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "start", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "stop", returnType: CAPPluginReturnPromise)
    ]

    // True while the engine is capturing. IntonarePlugin.setAudioMode reads it so
    // it does not flip the session back to mode .default under a live capture.
    static var running = false

    // Size the tap is asked for. iOS may hand over a different count per callback,
    // so every micFrame event carries its own `samples`. JS accepts any length.
    private static let tapSamples = 2048

    private var engine: AVAudioEngine?
    private var voiceProcessingOn = false
    private var currentRate = 0

    // Bumped on every start and stop. A frame queued by an old engine carries the old
    // number and is dropped, so a quick stop then start never leaks stale audio.
    private let genLock = NSLock()
    private var genValue = 0
    private func bumpGeneration() -> Int {
        genLock.lock(); defer { genLock.unlock() }
        genValue += 1
        return genValue
    }
    private func currentGeneration() -> Int {
        genLock.lock(); defer { genLock.unlock() }
        return genValue
    }

    private let emitQueue = DispatchQueue(label: "com.lieutenantdan.intonare.micemit")

    @objc func ping(_ call: CAPPluginCall) {
        call.resolve(["ok": true, "msg": "native alive", "platform": "ios"])
    }

    @objc func start(_ call: CAPPluginCall) {
        let wantAec = call.getBool("aec") ?? false
        let sendPcm = call.getBool("sendPcm") ?? false

        askForPermission { granted in
            if !granted {
                call.reject("Microphone permission denied by user")
                return
            }
            IntonarePlugin.sessionQueue.async {
                self.startOnQueue(call, wantAec: wantAec, sendPcm: sendPcm)
            }
        }
    }

    @objc func stop(_ call: CAPPluginCall) {
        IntonarePlugin.sessionQueue.async {
            self.teardown()
            call.resolve(["stopped": true])
        }
    }

    // MARK: - Permission

    // Asks only when the answer is still unknown. A settled answer returns at once,
    // so a restart does not wait on a system callback.
    private func askForPermission(_ done: @escaping (Bool) -> Void) {
        if #available(iOS 17.0, *) {
            switch AVAudioApplication.shared.recordPermission {
            case .granted: done(true)
            case .denied: done(false)
            default: AVAudioApplication.requestRecordPermission(completionHandler: done)
            }
        } else {
            let session = AVAudioSession.sharedInstance()
            switch session.recordPermission {
            case .granted: done(true)
            case .denied: done(false)
            default: session.requestRecordPermission(done)
            }
        }
    }

    // MARK: - Start / stop (sessionQueue only)

    private func startOnQueue(_ call: CAPPluginCall, wantAec: Bool, sendPcm: Bool) {
        if IntonareMicPlugin.running {
            if let eng = engine, eng.isRunning {
                call.resolve([
                    "started": true,
                    "alreadyRunning": true,
                    "sampleRate": currentRate,
                    "frameSamples": IntonareMicPlugin.tapSamples,
                    "source": voiceProcessingOn ? "voice_processing" : "measurement",
                    "sendPcm": sendPcm
                ])
                return
            }
            // The flag says running but the engine is gone (a phone call, Siri, or an
            // unplugged route stopped it). Clean up and start again.
            print("[Intonare] mic: stale running flag, restarting.")
            teardown()
        }

        // First try as requested. If voice processing makes the engine refuse to
        // start, try once more without it, so the surface still works.
        var result = bringUp(aec: wantAec, sendPcm: sendPcm)
        if result == nil && wantAec {
            print("[Intonare] mic: voice processing start failed, retrying raw.")
            result = bringUp(aec: false, sendPcm: sendPcm)
        }

        guard let up = result else {
            call.reject("native mic failed to start (mic busy, or no input available)")
            return
        }

        IntonareMicPlugin.running = true
        // Whatever setAudioMode cached is stale now. Clear it so the next call
        // after stop re-applies the session instead of trusting old state.
        IntonarePlugin.lastMicLive = nil

        print("[Intonare] native mic up: \(up.rate) Hz, aec \(up.aecApplied)")
        call.resolve([
            "started": true,
            "sampleRate": up.rate,
            "frameSamples": IntonareMicPlugin.tapSamples,
            "source": up.aecApplied ? "voice_processing" : "measurement",
            "sendPcm": sendPcm,
            "aecRequested": wantAec,
            "aecApplied": up.aecApplied,
            "aecAvailable": true,
            "aecNote": up.aecApplied ? "" : (wantAec ? "voice processing unavailable, running raw" : ""),
            "nsRequested": false, "nsApplied": false,
            "agcRequested": false, "agcApplied": false
        ])
    }

    private struct Up {
        let rate: Int
        let aecApplied: Bool
    }

    // Sets the category, builds the engine, installs the tap and starts it.
    // Returns nil on any failure, with everything it touched undone.
    private func bringUp(aec: Bool, sendPcm: Bool) -> Up? {
        let session = AVAudioSession.sharedInstance()
        do {
            // .measurement turns off the system's input processing and does not
            // duck output. With voice processing wanted, the default mode is the
            // one Voice Processing IO expects.
            try session.setCategory(
                .playAndRecord,
                mode: aec ? .default : .measurement,
                options: [.defaultToSpeaker, .allowBluetoothA2DP, .mixWithOthers]
            )
            // iOS silences the Taptic Engine and system sounds while an app records.
            // Without this, every haptic in the app goes quiet whenever the mic is on.
            if #available(iOS 13.0, *) {
                try? session.setAllowHapticsAndSystemSoundsDuringRecording(true)
            }
            try session.setActive(true)
        } catch {
            print("[Intonare] mic: session setup failed: \(error)")
            return nil
        }

        let eng = AVAudioEngine()
        let input = eng.inputNode

        var vpOn = false
        if aec {
            do {
                try input.setVoiceProcessingEnabled(true)
                vpOn = true
            } catch {
                print("[Intonare] mic: setVoiceProcessingEnabled failed: \(error)")
                return nil
            }
        }

        // Read the format AFTER voice processing is decided: turning it on can
        // change the rate and the channel count.
        let format = input.outputFormat(forBus: 0)
        if format.sampleRate <= 0 || format.channelCount == 0 {
            print("[Intonare] mic: input format invalid: \(format)")
            if vpOn { try? input.setVoiceProcessingEnabled(false) }
            return nil
        }
        let rate = Int(format.sampleRate.rounded())
        let gen = bumpGeneration()

        // format nil: the tap takes the node's own format, so it can never disagree
        // with what the hardware really delivers. Rate is read from each buffer.
        input.installTap(onBus: 0, bufferSize: AVAudioFrameCount(IntonareMicPlugin.tapSamples), format: nil) { [weak self] buffer, _ in
            self?.consume(buffer, gen: gen, sendPcm: sendPcm)
        }

        eng.prepare()
        do {
            try eng.start()
        } catch {
            print("[Intonare] mic: engine start failed: \(error)")
            input.removeTap(onBus: 0)
            if vpOn { try? input.setVoiceProcessingEnabled(false) }
            return nil
        }

        engine = eng
        voiceProcessingOn = vpOn
        currentRate = rate
        return Up(rate: rate, aecApplied: vpOn)
    }

    private func teardown() {
        if let eng = engine {
            eng.inputNode.removeTap(onBus: 0)
            eng.stop()
            if voiceProcessingOn {
                try? eng.inputNode.setVoiceProcessingEnabled(false)
            }
        }
        engine = nil
        voiceProcessingOn = false
        currentRate = 0
        _ = bumpGeneration()
        IntonareMicPlugin.running = false
        // Forget the session state. JS follows a mic stop with setAudioMode(false),
        // and that must re-apply .playback rather than trust a stale cache. If audio
        // is busy JS defers it, which is what keeps the metronome alive.
        IntonarePlugin.lastMicLive = nil
    }

    // MARK: - Audio thread

    // Runs on the real-time audio thread. Convert, hand off, return.
    private func consume(_ buffer: AVAudioPCMBuffer, gen: Int, sendPcm: Bool) {
        if !sendPcm { return }
        let n = Int(buffer.frameLength)
        if n == 0 { return }
        let rate = Int(buffer.format.sampleRate.rounded())

        var samples = [Int16](repeating: 0, count: n)
        if let ch = buffer.floatChannelData {
            let p = ch[0]
            for i in 0..<n {
                let v = p[i]
                if v.isNaN { continue }
                samples[i] = Int16(max(-1.0, min(1.0, v)) * 32767.0)
            }
        } else if let ch = buffer.int16ChannelData {
            let p = ch[0]
            for i in 0..<n { samples[i] = p[i] }
        } else {
            return
        }

        emitQueue.async { [weak self] in
            guard let self = self,
                  IntonareMicPlugin.running,
                  gen == self.currentGeneration() else { return }
            let data = samples.withUnsafeBufferPointer { Data(buffer: $0) }
            self.notifyListeners("micFrame", data: [
                "pcm": data.base64EncodedString(),
                "samples": n,
                "sampleRate": rate
            ])
        }
    }
}
