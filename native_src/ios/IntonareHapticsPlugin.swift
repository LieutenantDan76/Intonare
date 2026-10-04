//
//  IntonareHapticsPlugin.swift
//
//  Custom haptic patterns for iOS, through Core Haptics.
//
//  WHY THIS EXISTS
//  ---------------
//  Capacitor's Haptics plugin fires fixed presets (light, medium, heavy). Every
//  multi-tap feel in the app (success, level up, achievement) was a chain of those
//  presets with a JS timer between them, so the spacing wobbled with bridge and
//  main-thread load. Core Haptics takes the whole pattern in one call and the
//  hardware plays it on its own clock. It also lets each tap have its own
//  intensity and sharpness instead of three fixed strengths.
//
//  THE CONTRACT WITH JS (same on Android, see IntonareHapticsPlugin.java)
//    isSupported()            -> { supported: Bool }
//    play({ events: [...] })  -> { ok: Bool }
//    cancel()                 -> { ok: true }
//  Each event: { t: ms from now, i: intensity 0..1, s: sharpness 0..1, d: ms }
//  d == 0 is a single tap (transient). d > 0 is a sustained buzz of that length.
//  The patterns themselves live in JS (HD_PATTERNS), so both platforms feel the
//  same and a pattern is tuned in one place.
//
//  DESIGN NOTES
//  ------------
//  - playsHapticsOnly = true. Without it the haptic engine can open its own audio
//    session and fight the app's carefully managed AVAudioSession (see
//    IntonareAudioSession.swift for what that fight looks like). With it, this
//    plugin never touches the session at all.
//  - isAutoShutdownEnabled = true. The engine idles itself off to save power. The
//    next play() starts it again, which costs a few milliseconds the first time.
//  - When the system stops or resets the engine (a phone call, Siri, a media
//    server reset) the handlers drop it, and the next play() builds a fresh one.
//    An idle shutdown is the one stop that keeps the engine: start() wakes it.
//    Nothing here calls into the audio session or restarts in a loop.
//  - isSupported() also warms the engine, so the first real pattern does not pay
//    the engine start-up time.
//  - Failure is quiet. If anything throws, play() resolves ok:false and JS falls
//    back to the old Capacitor taps.
//

import Foundation
import Capacitor
import CoreHaptics

@objc(IntonareHapticsPlugin)
public class IntonareHapticsPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IntonareHapticsPlugin"
    public let jsName = "IntonareHaptics"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "isSupported", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "play", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "cancel", returnType: CAPPluginReturnPromise)
    ]

    private static let maxEvents = 64
    private static let maxSpanMs = 4000.0

    private let queue = DispatchQueue(label: "com.lieutenantdan.intonare.haptics")
    private var engine: CHHapticEngine?

    @objc func isSupported(_ call: CAPPluginCall) {
        let ok = CHHapticEngine.capabilitiesForHardware().supportsHaptics
        call.resolve(["supported": ok])
        if ok {
            queue.async {
                if let e = self.ensureEngine() { try? e.start() }
            }
        }
    }

    @objc func play(_ call: CAPPluginCall) {
        guard let raw = call.getArray("events", JSObject.self), !raw.isEmpty else {
            call.resolve(["ok": false, "error": "no events"])
            return
        }
        queue.async {
            self.playOnQueue(call, raw: raw)
        }
    }

    @objc func cancel(_ call: CAPPluginCall) {
        queue.async {
            if let e = self.engine {
                e.stop(completionHandler: { _ in })
                self.engine = nil
            }
            call.resolve(["ok": true])
        }
    }

    private func number(_ v: Any?) -> Double {
        if let n = v as? NSNumber { return n.doubleValue }
        if let d = v as? Double { return d }
        if let i = v as? Int { return Double(i) }
        return 0
    }

    private func ensureEngine() -> CHHapticEngine? {
        if !CHHapticEngine.capabilitiesForHardware().supportsHaptics { return nil }
        if let e = engine { return e }
        do {
            let e = try CHHapticEngine()
            e.playsHapticsOnly = true
            e.isAutoShutdownEnabled = true
            e.stoppedHandler = { [weak self] reason in
                if reason == .idleTimeout { return }
                self?.queue.async { self?.engine = nil }
            }
            e.resetHandler = { [weak self] in
                self?.queue.async { self?.engine = nil }
            }
            engine = e
            return e
        } catch {
            print("[Intonare] haptics: engine create failed: \(error)")
            return nil
        }
    }

    private func playOnQueue(_ call: CAPPluginCall, raw: [JSObject]) {
        guard let eng = ensureEngine() else {
            call.resolve(["ok": false, "error": "unsupported"])
            return
        }

        var events = [CHHapticEvent]()
        for ev in raw.prefix(IntonareHapticsPlugin.maxEvents) {
            let t = max(0.0, min(IntonareHapticsPlugin.maxSpanMs, number(ev["t"])))
            let i = Float(max(0.0, min(1.0, number(ev["i"]))))
            let s = Float(max(0.0, min(1.0, number(ev["s"]))))
            let d = max(0.0, min(IntonareHapticsPlugin.maxSpanMs, number(ev["d"])))
            let params = [
                CHHapticEventParameter(parameterID: .hapticIntensity, value: i),
                CHHapticEventParameter(parameterID: .hapticSharpness, value: s)
            ]
            if d > 0 {
                events.append(CHHapticEvent(eventType: .hapticContinuous, parameters: params,
                                            relativeTime: t / 1000.0, duration: d / 1000.0))
            } else {
                events.append(CHHapticEvent(eventType: .hapticTransient, parameters: params,
                                            relativeTime: t / 1000.0))
            }
        }

        do {
            // start() is safe to call on a running engine. After a stop or reset it
            // brings the engine back; that is the only restart logic there is.
            try eng.start()
            let pattern = try CHHapticPattern(events: events, parameters: [])
            let player = try eng.makePlayer(with: pattern)
            try player.start(atTime: CHHapticTimeImmediate)
            call.resolve(["ok": true])
        } catch {
            print("[Intonare] haptics: play failed: \(error)")
            // Stop and drop the engine so the next call builds a fresh one. Dropping it
            // without stopping would leave the old one running in the background.
            eng.stop(completionHandler: { _ in })
            engine = nil
            call.resolve(["ok": false, "error": String(describing: error)])
        }
    }
}
