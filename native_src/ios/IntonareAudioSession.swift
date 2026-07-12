//
//  IntonareAudioSession.swift
//
//  Configures the iOS audio session for Intonare.
//
//  WHY THIS EXISTS
//  ---------------
//  The moment WKWebView calls getUserMedia, iOS switches the app's audio
//  session to AVAudioSessionCategoryPlayAndRecord. That category defaults to
//  routing output through the RECEIVER — the earpiece speaker you hold to your
//  face on a call — not the loudspeaker. The OS assumes that an app which
//  records and plays simultaneously is a phone call.
//
//  The result is that every sound Intonare makes is dramatically quieter than
//  it should be, the moment the microphone is touched.
//
//  WebKit exposes no way to change this. There is no JS API, no AudioContext
//  property, nothing. It cannot be fixed in the web layer at any price. The
//  only lever is AVAudioSession, and that is native-only.
//
//  WHY .defaultToSpeaker
//  ---------------------
//  This is the single option that overrides the receiver routing and sends
//  output to the loudspeaker while recording is active.
//
//  WHY .allowBluetoothA2DP AND NOT .allowBluetooth
//  -----------------------------------------------
//  Bluetooth audio has two profiles and they are not a spectrum:
//
//    A2DP  — stereo, high bitrate, OUTPUT ONLY. No microphone exists in this
//            profile. This is what AirPods use for music.
//
//    HFP   — the headset profile. It has a microphone, but to carry a
//            bidirectional link it collapses the ENTIRE session, both
//            directions, to 8 or 16 kHz mono. Telephone quality.
//
//  .allowBluetooth enables HFP. If a user has AirPods connected, the tuner
//  would silently start reading an 8 kHz mic feed: Nyquist caps that at 4 kHz,
//  which guts the harmonic content the FFT pitch detector depends on. It would
//  degrade every one of the seven mic surfaces, with no error and no warning.
//
//  .allowBluetoothA2DP gives users what they actually want — game and playback
//  audio through their headphones, in full quality — while the microphone stays
//  on the phone's own hardware at the full sample rate.
//
//  WHY 48 kHz
//  ----------
//  iOS picks a sample rate based on device and route, and it varies. Pinning it
//  removes a whole class of bug: code that assumes a rate and gets another one
//  produces detection errors that look like tuning errors.
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

            // Ask for 48 kHz. iOS may not honour this on every route, so nothing
            // downstream should assume it succeeded; read the actual rate from
            // the AudioContext rather than hardcoding one.
            try session.setPreferredSampleRate(48000.0)

            // A short IO buffer keeps the tuner responsive. iOS treats this as a
            // hint and may round it to whatever the hardware supports.
            try session.setPreferredIOBufferDuration(0.005)

            try session.setActive(true)

        } catch {
            // A failure here means the app is quiet, not broken. Every surface
            // still functions; do not take the app down over it.
            print("[Intonare] AVAudioSession configuration failed: \(error)")
        }

        // The route can change under us at any time: headphones plugged in or
        // pulled out, a Bluetooth device connecting, a call arriving. iOS may
        // reset the category when that happens, so reassert it.
        NotificationCenter.default.addObserver(
            forName: AVAudioSession.routeChangeNotification,
            object: nil,
            queue: .main
        ) { _ in
            reassert()
        }

        // An interruption (a phone call, Siri) deactivates the session. When it
        // ends, the category has to be set up again or the app comes back quiet.
        NotificationCenter.default.addObserver(
            forName: AVAudioSession.interruptionNotification,
            object: nil,
            queue: .main
        ) { note in
            guard
                let info = note.userInfo,
                let raw = info[AVAudioSessionInterruptionTypeKey] as? UInt,
                let type = AVAudioSession.InterruptionType(rawValue: raw)
            else { return }

            if type == .ended {
                reassert()
            }
        }
    }

    private static func reassert() {
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
            try session.setActive(true)
        } catch {
            print("[Intonare] AVAudioSession reassert failed: \(error)")
        }
    }
}
