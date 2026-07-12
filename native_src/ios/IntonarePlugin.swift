//
//  IntonarePlugin.swift
//
//  Intonare's native bridge for iOS. One plugin, deliberately tiny.
//
//  WHY THIS EXISTS
//  ---------------
//  iOS output is quieter than Android even with routing fixed (.defaultToSpeaker
//  works; sound comes from the loudspeaker). The mechanism, per Apple's own
//  developer forums and multiple engine bug trackers (Godot #88893 among them):
//  the playAndRecord category runs output through a voice-processing chain that
//  attenuates it — the category is built for phone calls, where a loud speaker
//  feeds back into the microphone.
//
//  WKWebView makes it worse: when getUserMedia starts, WebKit reconfigures the
//  session itself, typically flipping the MODE toward voice chat, which engages
//  Voice Processing IO. Output ducks. There is no JS API to undo it.
//
//  assertAudioMode() re-sets the category with mode .default AFTER the WebView
//  has done its thing. Called from JS, once, when mic setup completes.
//
//  DESIGN CONSTRAINTS — LEARNED THE HARD WAY
//  -----------------------------------------
//  - NO NotificationCenter observers. A previous audio-session file observed
//    routeChangeNotification and called setCategory from the handler; but
//    setCategory can itself post a route change. The result was an infinite loop
//    on the main thread from launch: the app unusably laggy, the mic reading
//    zeroes. Everything here is one-shot and JS-triggered. Nothing reacts to
//    anything.
//
//  - Failure is quiet, not fatal. If the assert fails, the app is quieter than
//    ideal; every surface still works. call.resolve() with ok:false, never
//    reject, so no JS path starts throwing because of a volume nudge.
//
//  REGISTRATION
//  ------------
//  Capacitor 8's config-based plugin discovery (packageClassList) does not pick
//  up local app plugins — the generated list comes out empty (capacitor#7409).
//  The supported route for custom in-app code is bridge.registerPluginInstance()
//  from a CAPBridgeViewController subclass's capacitorDidLoad() override. The CI
//  patcher (patch_ios_appdelegate.py) appends that subclass and points the
//  storyboard at it.
//

import Foundation
import Capacitor
import AVFoundation

@objc(IntonarePlugin)
public class IntonarePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IntonarePlugin"
    public let jsName = "IntonareIOS"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "assertAudioMode", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "releaseAudioMode", returnType: CAPPluginReturnPromise)
    ]

    // Mic is (or is about to be) live: playAndRecord with the least-attenuating
    // mode, then snap the output level back.
    //
    // The snap-back matters. Per the Apple Developer Forums thread on Voice
    // Processing volume (thread 721535): once VPIO has ducked the output,
    // re-calling setCategory or overrideOutputAudioPort(.speaker) RESTORES the
    // volume — and any audio source started after that may duck again and need
    // another nudge. So JS calls this not only at mic start, but (throttled)
    // after starting a drone / reference tone / metronome while the mic is live.
    @objc func assertAudioMode(_ call: CAPPluginCall) {
        let session = AVAudioSession.sharedInstance()
        do {
            try session.setCategory(
                .playAndRecord,
                mode: .default,
                options: [
                    .defaultToSpeaker,
                    .allowBluetoothA2DP,
                    .mixWithOthers
                ]
            )
            // The snap-back. Redundant with .defaultToSpeaker for ROUTING, but it
            // is the call the forum thread confirms restores LEVEL after VPIO has
            // ducked it. Best-effort: failure is not worth reporting.
            try? session.overrideOutputAudioPort(.speaker)
            print("[Intonare] assertAudioMode: playAndRecord/.default + speaker override")
            call.resolve(["ok": true])
        } catch {
            print("[Intonare] assertAudioMode failed: \(error)")
            call.resolve(["ok": false, "error": String(describing: error)])
        }
    }

    // Mic fully stopped: drop back to plain playback. No mic claim, no voice
    // processing chain anywhere near the output, full volume. This is the app's
    // resting state; the launch-time AppDelegate configuration matches it.
    @objc func releaseAudioMode(_ call: CAPPluginCall) {
        let session = AVAudioSession.sharedInstance()
        do {
            try session.setCategory(
                .playback,
                mode: .default,
                options: [
                    .mixWithOthers
                ]
            )
            print("[Intonare] releaseAudioMode: back to playback/.default")
            call.resolve(["ok": true])
        } catch {
            print("[Intonare] releaseAudioMode failed: \(error)")
            call.resolve(["ok": false, "error": String(describing: error)])
        }
    }
}
