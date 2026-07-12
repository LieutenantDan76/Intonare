//
//  IntonareAudioSession.swift
//
//  Configures the iOS audio session for Intonare.
//
//  WHY THIS EXISTS
//  ---------------
//  The moment WKWebView calls getUserMedia, iOS switches the app's audio session
//  to playAndRecord. That category routes output through the RECEIVER — the
//  earpiece you hold to your face on a call — not the loudspeaker. The OS assumes
//  an app that records and plays at the same time is a phone call.
//
//  So every sound Intonare makes goes quiet the moment the microphone is touched.
//  WebKit exposes no way to change this: no JS API, no AudioContext property.
//  AVAudioSession is the only lever, and it is native-only.
//
//  `.defaultToSpeaker` is the single option that overrides the receiver routing.
//  That is the entire fix. One flag on one call.
//
//
//  WHAT THIS FILE DELIBERATELY DOES NOT DO — READ THIS BEFORE ADDING ANYTHING
//  -------------------------------------------------------------------------
//  An earlier version made the app unusable and left the microphone reading pure
//  silence. Every item below was in it. None come back without a measurement on a
//  real device.
//
//  1. NO OBSERVER ON routeChangeNotification.
//     This is the one that broke the app. The observer called a helper that called
//     setCategory() — but setCategory() can ITSELF post a route change. So:
//     observer → setCategory → route change → observer → forever. An infinite loop
//     on the main thread, running from launch. The app was unusably laggy and the
//     mic read zeroes, because the session was thrashing its own category
//     thousands of times a second.
//
//     If route changes ever genuinely need handling, the handler must not call
//     setCategory, or must guard against re-entry. Better still: handle it from JS
//     on an explicit user action, where it can be seen.
//
//  2. NO setPreferredIOBufferDuration.
//     A 5 ms buffer asks iOS to wake the audio thread 200 times a second and cross
//     into WKWebView's Web Audio graph on every callback. It buys nothing here:
//     detection latency is bounded by rAF and the FFT window, not the hardware
//     buffer.
//
//  3. NO setPreferredSampleRate.
//     iOS picks a rate per route. Nothing downstream should assume one, and the
//     AudioContext reports the real value anyway.
//
//  4. NO setActive(true).
//     Configuring the category at launch is correct. Making the session ACTIVE at
//     launch is not — it claims the audio hardware the moment the app opens,
//     whether the mic is ever used or not. WKWebView activates the session itself
//     when Web Audio or getUserMedia needs it, and inherits the category set here.
//
//  What remains is one setCategory call, once, at launch. That is the whole job.
//
//
//  WHY .allowBluetoothA2DP AND NOT .allowBluetooth
//  -----------------------------------------------
//  Bluetooth audio has two profiles, and they are not a spectrum:
//
//    A2DP — stereo, high bitrate, OUTPUT ONLY. No microphone in this profile.
//           What AirPods use for music.
//
//    HFP  — the headset profile. It has a mic, but carrying a bidirectional link
//           collapses the ENTIRE session, both directions, to 8 or 16 kHz mono.
//           Telephone quality.
//
//  .allowBluetooth enables HFP. With AirPods connected, the tuner would silently
//  start reading an 8 kHz mic feed — Nyquist caps that at 4 kHz, gutting the
//  harmonic content the FFT pitch detector needs. All seven mic surfaces would
//  degrade, with no error and no warning.
//
//  .allowBluetoothA2DP gives users what they actually want — playback through
//  their headphones at full quality — while the mic stays on the phone's own
//  hardware at the full rate.
//

import Foundation
import AVFoundation

enum IntonareAudioSession {

    static func configure() {
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
            print("[Intonare] AVAudioSession category set — defaultToSpeaker.")
        } catch {
            // A failure here means the app is quiet, not broken. Every surface
            // still works. Do not take the app down over it.
            print("[Intonare] AVAudioSession configuration failed: \(error)")
        }

        // Nothing else. No observers, no activation, no buffer or rate hints.
        // See the header for why each was removed.
    }
}
