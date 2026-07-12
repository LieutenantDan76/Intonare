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
//  setAudioMode(micLive:) re-sets the category AFTER the WebView has done its
//  thing. JS reports what the app IS; native decides what the session should BE.
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
        CAPPluginMethod(name: "setAudioMode", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "playSplashSound", returnType: CAPPluginReturnPromise)
    ]

    // Held for the lifetime of playback. A local AVAudioPlayer would be
    // deallocated the instant the method returns and you would hear nothing —
    // a classic, and a silent one.
    private var splashPlayer: AVAudioPlayer?

    // ── The audio session, single owner ──────────────────────────────────────
    //
    // THE BUG THIS REPLACES
    // There used to be two methods — assertAudioMode() and releaseAudioMode() —
    // called from three places: first audio, mic start, mic stop. Each is an async
    // bridge round-trip, and nothing sequenced them. Start and stop the metronome
    // quickly and you would get:
    //
    //     call A fires  → sets .playback
    //     call B fires  → sets .playAndRecord   (before A has landed)
    //     A resolves    → .playback wins, wrongly, because it finished last
    //     throttle      → blocks the corrective call
    //     result        → stuck quiet until something else happened to nudge it
    //
    // Symptom: "sometimes it works, sometimes it takes a second, sometimes I have
    // to hit the mic." A race, and an unreproducible one.
    //
    // THE FIX
    // One method. JS says what the app IS ("mic live" or not); native decides what
    // the session should therefore BE. All work runs on a serial queue, so two
    // calls can never interleave. And the last-applied state is remembered, so a
    // redundant call — which rapid start/stop produces constantly — costs nothing
    // and touches no hardware.
    //
    // Ordering is now deterministic by construction, not by timing.

    private static let sessionQueue = DispatchQueue(label: "com.lieutenantdan.intonare.audiosession")
    private static var lastMicLive: Bool?     // nil = nothing applied yet

    @objc func setAudioMode(_ call: CAPPluginCall) {
        let micLive = call.getBool("micLive") ?? false
        // force: apply even if the state matches what we last set.
        //
        // The cache is right in principle and wrong at startup. The app auto-starts
        // the mic at launch (deliberately — quick-access tuner), which fires a
        // session change BEFORE WKWebView has built its audio engine. We configure
        // a session nothing is attached to; WebKit then comes up with its own
        // defaults; and because the state was cached as applied, no later call ever
        // re-applies it. The audio sits quieter than either normal level until a
        // mic toggle changes micLive and happens to bypass the cache.
        //
        // JS passes force=true until it has applied at least once with a live
        // AudioContext. After that the cache is trustworthy and rapid start/stop
        // stays free.
        let force = call.getBool("force") ?? false

        IntonarePlugin.sessionQueue.async {
            // Idempotent. Rapid start/stop hits this constantly; make it free.
            if !force && IntonarePlugin.lastMicLive == micLive {
                call.resolve(["ok": true, "changed": false,
                              "mode": micLive ? "playAndRecord" : "playback"])
                return
            }

            let session = AVAudioSession.sharedInstance()
            do {
                if micLive {
                    // iOS requires playAndRecord to record. It is inherently
                    // quieter — output runs through a voice-processing path built
                    // for phone calls. mode .default keeps that as light as it
                    // goes; the port override snaps the level back after WebKit's
                    // getUserMedia has engaged Voice Processing IO.
                    try session.setCategory(
                        .playAndRecord,
                        mode: .default,
                        options: [.defaultToSpeaker, .allowBluetoothA2DP, .mixWithOthers]
                    )
                    try session.setActive(true)
                    try? session.overrideOutputAudioPort(.speaker)
                } else {
                    // No mic: plain playback. No voice processing anywhere near the
                    // output, full volume. This is the app's normal state, and it
                    // is where it should sit whenever the mic is not in use.
                    try session.setCategory(
                        .playback,
                        mode: .default,
                        options: [.mixWithOthers]
                    )
                    try session.setActive(true)
                }

                IntonarePlugin.lastMicLive = micLive
                print("[Intonare] session → \(micLive ? "playAndRecord" : "playback")")
                call.resolve(["ok": true, "changed": true,
                              "mode": micLive ? "playAndRecord" : "playback"])
            } catch {
                // A failure here means the app is quieter than ideal, not broken.
                // Do not poison lastMicLive: leaving it unchanged means the next
                // call will retry rather than assume this state was reached.
                print("[Intonare] session change failed: \(error)")
                call.resolve(["ok": false, "error": String(describing: error)])
            }
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

}
