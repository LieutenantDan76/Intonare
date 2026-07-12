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
import AudioToolbox

@objc(IntonarePlugin)
public class IntonarePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "IntonarePlugin"
    public let jsName = "IntonareIOS"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "assertAudioMode", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "releaseAudioMode", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "playSplashSound", returnType: CAPPluginReturnPromise)
    ]

    // Held for the lifetime of playback. A local AVAudioPlayer would be
    // deallocated the instant the method returns and you would hear nothing —
    // a classic, and a silent one.
    private var splashPlayer: AVAudioPlayer?

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
            // Same reasoning as releaseAudioMode: a configured session that is not
            // active has not actually taken effect.
            try? session.setActive(true)
            print("[Intonare] assertAudioMode: playAndRecord/.default + speaker, active")
            call.resolve(["ok": true])
        } catch {
            print("[Intonare] assertAudioMode failed: \(error)")
            call.resolve(["ok": false, "error": String(describing: error)])
        }
    }

    // The launch sound.
    //
    // WHY THIS IS NATIVE AND NOT WEB AUDIO
    // The splash fires at cold launch, before the user has touched anything.
    // WebKit refuses to play audio without a user gesture, so Web Audio cannot do
    // this at any price — the JS comment at the call site has said so all along:
    // "Native playback isn't gesture-gated, so this keeps true autoplay while
    // syncing exactly."
    //
    // WHERE THE FILE LIVES, AND WHY THERE
    // In www/, which Capacitor copies into the app bundle as `public/`. That
    // folder is ALREADY a registered Xcode resource — it is how the entire app
    // loads — so the sound ships without touching project.pbxproj, which
    // `cap add ios` regenerates every build anyway.
    //
    // The source is Vorbis (.ogg) for Android. iOS cannot decode Vorbis at all,
    // so CI transcodes it to AAC (.m4a) alongside the original.
    @objc func playSplashSound(_ call: CAPPluginCall) {
        guard let url = Bundle.main.url(
            forResource: "intonare_splash",
            withExtension: "m4a",
            subdirectory: "public/audio"
        ) else {
            print("[Intonare] splash sound not found in bundle at public/audio/")
            call.resolve(["ok": false, "error": "not found"])
            return
        }

        do {
            // The splash plays before any mic use, so the session is .playback:
            // full volume, no voice processing. Exactly what we want here.
            let player = try AVAudioPlayer(contentsOf: url)
            player.prepareToPlay()
            player.play()
            splashPlayer = player      // retain, or it dies on return
            print("[Intonare] splash sound playing.")
            call.resolve(["ok": true])
        } catch {
            print("[Intonare] splash sound failed: \(error)")
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
            // ACTIVATE. This is the difference between configuring a session and
            // having one.
            //
            // iOS does not apply a category until the session is active, and it
            // does not activate one until something needs audio. WKWebView gets
            // there first and activates with ITS defaults — which is why the first
            // sounds of a session came out quiet even though .playback had been
            // set at launch, and only corrected once the mic was touched.
            //
            // This is NOT the launch-time setActive(true) that was removed
            // earlier. That one claimed the audio hardware from app open, before
            // any user action, for a session nobody was using. This runs on demand
            // — first audio, or mic stop — after the user has already gestured.
            try? session.setActive(true)
            print("[Intonare] releaseAudioMode: playback/.default, session active")
            call.resolve(["ok": true])
        } catch {
            print("[Intonare] releaseAudioMode failed: \(error)")
            call.resolve(["ok": false, "error": String(describing: error)])
        }
    }
}
