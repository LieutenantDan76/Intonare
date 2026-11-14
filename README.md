# Intonare

Intonare is a music education app for singers and instrumentalists, in English and Italian. It has a tuner, a metronome with a drum machine, ear training games, chord and scale charts, a vocal range test, a piano song bank, and a Survival Guide with playable diagrams for many instruments. It runs on Android and iOS, and in any modern browser.

I am a music teacher, and I built it for my students and for myself. It has no server of its own. Your progress, settings and backups stay on your device.

## How it is built

The whole app is one file, `Intonare.html`: HTML, CSS and plain JavaScript with no framework. All sound comes from the Web Audio API, so the tuner, the tones, the drums and the instrument models are synthesized or played from samples in the browser.

[Capacitor](https://capacitorjs.com) wraps that file for Android and iOS. Native code is small and lives in `native_src/` (microphone, haptics, file saving, home screen shortcuts). In-app purchases go through RevenueCat. The online Music Quiz categories fetch questions from the [Open Trivia Database](https://opentdb.com) at run time.

I chose the single file on purpose. It deploys by copying one file, it works offline, and the browser version is the same code as the phone version. The cost is size: the file is about 15 MB.

## Run it

Open `Intonare.html` in Chrome, Firefox or Safari. Browsers need a tap or click before they allow sound, and the microphone tools ask for permission.

## Build for a phone

You need Node, the Android SDK and Android Studio for Android, and a Mac or the Codemagic cloud build for iOS.

1. `go.bat` asks for a commit message, pushes to GitHub, copies the app into `www/`, runs `npm install` and `cap sync`, and puts the native sources from `native_src/` back into the generated Android project.
2. Press Run in Android Studio.
3. `release.bat` builds the signed bundle for Google Play. iOS builds start by hand in Codemagic (`codemagic.yaml`).

`go.bat` and `release.bat` are Windows scripts, because that is the machine I develop on.

## Checks

```
tools\ship_check.bat
```

This runs the checks that gate every release: HTML integrity, the regression sentinel (it pins every past fix so it cannot quietly come back), the changelog match, and audits for backup coverage, drum presets, American spelling and search. The last step opens every tool, exercise and game in a headless browser and fails if any of them throws an error. It needs Python 3 and `pip install playwright`. More about each script is in `tools/README.md`.

## Folders

| Path | What is in it |
|---|---|
| `Intonare.html` | The app |
| `CHANGELOG.md` | Every release, in plain language |
| `native_src/` | Android and iOS native code and resources, the source of truth |
| `audio_assets/` | Instrument sample sets bundled into the phone builds |
| `icon_res/`, `ios_icon/` | App icons |
| `credits/` | Sources and licenses for third-party material |
| `tools/` | The audits behind the ship check and the pitch detection benchmark |

## License and credits

The code and original content are all rights reserved. You can read the source and test it for personal use, but you cannot reuse it commercially without permission. See `License`.

Third-party material keeps its own license: piano performance data from piano-midi.de (CC BY-SA 3.0), bassoon diagrams by Bret Pimentel (CC BY-NC-SA 4.0, used with permission), sheet music from OpenScore, Mutopia and others, quiz questions from the Open Trivia Database (CC BY-SA 4.0), and instrument samples from the gleitz MIDI.js soundfonts. The full list is in `License` and on the Credits screen inside the app.

## Contact

Support and privacy policy: `support.html` and `privacy.html`.
