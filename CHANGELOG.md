# Intonare — Changelog

A human-readable record of what changed, when, and to what specific value. This
is the companion to `intonare_regression_sentinel.py`: the sentinel proves a fix
is *present*; this log tells you what the fix *was* and what exact value it used.

**How to use:** newest at top. When something feels off, scan here first — you're
looking for "when did this value last change, and to what?" rather than digging
through old chats. Each entry: version · area · what changed · (old → new) where a
value moved. Values marked 📌 are exact-pinned in the sentinel — changing them
deliberately means telling Claude so the pin updates too.

> Entries before v0.20.36 were reconstructed from chat history and are
> approximate on dates/versions; values were verified against the file where
> still present. From v0.20.36 on, entries are recorded live as work happens.

---

## v0.81.13 — the volume race, and the splash was frame-rate coupled

### The splash animation had less travel on iOS
Not lag — the frames were smooth. The wave simply covered less horizontal ground.

Everything driven by `gatherEl` (the gather, the easing curves, the timing of every
beat) reads `performance.now()` and was already correct on any device. But the
wave's horizontal travel advanced by a **fixed amount per frame**:

    wavePhase += _spd;

which makes its speed directly proportional to frame rate. Every constant was tuned
by eye on Android; on a device rendering at a different rate the wave covers less
distance per second and the whole thing reads as sluggish **without ever dropping a
frame**. Which is exactly what it looked like. The colour, glow and pulse eases had
the same bug, so on iOS the palette was also arriving out of step with the motion it
is meant to be lighting.

- Now normalised by `dt60` — how many 60 fps frames this frame actually took. **At a
  true 60 fps `dt60` is 1.0 and every constant behaves exactly as tuned**, so Android
  is unchanged; at 30 fps it is 2.0 and each frame advances twice as far, covering
  the same ground per second.
- Clamped to 3 frames, so a stall (backgrounded tab, GC pause) cannot produce one
  enormous jump and tear the wave.
- The frame clock resets when the animation starts, or a stale timestamp from a
  previous run would hand frame 1 an enormous `dt`.

### The volume race

"Sometimes it works, sometimes it takes a second, sometimes I have to hit the mic,
and start/stopping the metronome sometimes gets stuck." Unreproducible, because it
was a **race**.

Three call sites (first audio, mic start, mic stop) each fired an async bridge call
that set the audio session, with a one-second throttle on top and no sequencing
between them. Start and stop the metronome quickly and:

    call A fires  → sets .playback
    call B fires  → sets .playAndRecord   (before A has landed)
    A resolves    → .playback wins, wrongly, because it finished last
    throttle      → blocks the corrective call
    result        → stuck quiet until something else happened to nudge it

### Fixed
- **One method, one owner.** `assertAudioMode()` / `releaseAudioMode()` are gone,
  replaced by `setAudioMode(micLive:)`. JS reports what the app **is**; native
  decides what the session should therefore **be**.
- **Serialised natively.** All session work runs on a dedicated serial
  `DispatchQueue`, so two calls cannot interleave. Ordering is deterministic by
  construction rather than by timing.
- **Idempotent.** Native remembers the last state it applied; a redundant call —
  which rapid start/stop produces constantly — returns immediately and touches no
  hardware. **The throttle is gone**, because it is no longer needed: repeat calls
  are already free.
- On failure the remembered state is deliberately *not* updated, so the next call
  retries rather than assuming a state that was never reached.
- All five JS call sites now use the one function, with no guards (the call is free
  when nothing changed). The mic-start call was also **moved to after
  `isListening = true`** — it had been firing while the flag was still false, which
  asked for `.playback` at the exact moment the mic was coming up.

### Caught by the sentinel, not by me
The JS rework accidentally deleted `_PITCH_HIST_N`, `_pitchHist`, `_pitchSort` and
`_pitchHistIdx` — a slice-based edit whose end index overshot into the pitch-median
declarations sitting just past it. `node --check` passed cleanly, because a missing
`const` is a runtime `ReferenceError`, not a syntax error; the tuner would have
thrown on every detected pitch. The regression sentinel flagged the drifted pin.
Restored, verified, and a good argument for the ship gate existing.

## v0.81.12 — Italian permission prompt, and the launch sound on iOS

### The iOS launch sound
It never played on iOS, and it was never going to: the JS called
`window.IntonareNative` — the Android `@JavascriptInterface` bridge, which does not
exist on iOS. Absence by construction, and completely silent about it.

The obvious shortcut (just play it from Web Audio) is dead on arrival, and the
comment at the call site has said why all along: *"Native playback isn't
gesture-gated, so this keeps true autoplay while syncing exactly."* The splash
fires at cold launch, before any user gesture, and **WebKit will not autoplay Web
Audio without one**. Native or nothing.

- **`IntonarePlugin.playSplashSound()`** — `AVAudioPlayer`, holding a reference for
  the lifetime of playback (a local player is deallocated the instant the method
  returns, and you hear nothing; a classic, and a silent one).
- **The file ships in `www/audio/`**, which Capacitor copies into the bundle as
  `public/audio/`. That folder is *already* a registered Xcode resource — it is how
  the entire app loads — so the sound needs **no `project.pbxproj` surgery**, which
  matters because `cap add ios` regenerates the project file every build.
- **CI transcodes it.** The Android source is Vorbis (`.ogg`); iOS cannot decode
  Vorbis at all. Now converted to AAC alongside the original, with ffmpeg installed
  on the fly if the build image lacks it.
- JS falls through: Android bridge if present, else the iOS plugin.

### The Italian microphone prompt
The permission dialog was English-only, on an app whose primary market is Italy.

- `en.lproj` / `it.lproj` `InfoPlist.strings`, plus `CFBundleLocalizations` in the
  plist (without which iOS does not even look for a localized string and uses the
  plist value verbatim regardless of device language).
- Written by Python rather than shell, because the Italian needs a real **né** and
  typographic apostrophes, and pushing UTF-8 accents through bash quoting inside an
  indented YAML block is a fight not worth having. (An earlier pass wrote "ne" to
  dodge the escaping. Not shipping that.)

**One open bet.** Strictly, a `.lproj` must be registered in the Xcode project to
be copied into the bundle. The bet is that `cap add ios` registers the contents of
`App/App/`, so a `.lproj` dropped inside gets copied for free. **If the Italian
prompt does not appear on an Italian device, that bet was wrong** and the fix is a
pbxproj patch or an `InfoPlist.xcstrings` catalogue. Flagged rather than assumed.

## v0.81.11 — quiet until the mic was touched; and the fader's dead top half

Two separate volume bugs, both now fixed. Neither was iOS-only in cause, though
only one showed up on iOS.

### Fixed: the app was quiet until you touched the mic
v0.81.10 set `.playback` at launch, which is the right category — but **iOS does
not apply a category until the session is ACTIVE**, and it does not activate one
until something needs audio. WKWebView gets there first and activates the session
with *its* defaults. So the first sounds of a session played under WebKit's
config, not ours; only touching the mic ran the plugin and made it stick.

- Both plugin methods now call `setActive(true)`.
- `getAudio()` asserts the session when the shared AudioContext is first created —
  before the first note, rather than after the first mic tap.
- It asserts the category matching the **current mic state**: `releaseAudioMode()`
  (`.playback`) when the mic is off, `assertAudioMode()` (`.playAndRecord`) when
  it is live. Calling the latter unconditionally would have claimed the microphone
  for nothing and dragged the app back into the attenuated category it is trying
  to escape.

This is **not** the launch-time `setActive(true)` removed in v0.81.3. That one
claimed the audio hardware from app open, before any user action, for a session
nobody was using. This runs on demand, after a gesture.

### Fixed: the master fader's top half did nothing
At 100% a typical chain computes `0.8 × 0.9 = 0.72`, and the limiter threshold is
`-3 dB` (≈0.708) — the signal **sits on the threshold at normal volume**. That is
where it should sit; it is what all the clipping and chord-pumping work converged
on, and it is not being touched.

But it means the fader's upper half was dead. At 200% the gain becomes 1.44 —
about 6 dB over the threshold, into a 20:1 ratio. The limiter handed back roughly
**a third of a decibel**. The fader raised the gain and the limiter immediately
took it away, so "louder" only ever meant "more compressed".

- **Above 100%, the limiter ceiling now rises with the gain**
  (`threshold = -3 + 20·log₁₀(scale)`, capped at 0 dBFS), so the added gain passes
  instead of being squashed.
- **At and below 100% the threshold is exactly the -3 dB it has always been.**
  Identical maths, identical sound, none of the existing tuning disturbed. Only
  the currently-dead range changes.
- Limiters are now registered alongside their gain nodes, because chains are
  cached and reused — without this, a limiter built at 100% would keep its old
  ceiling forever and the fader would move the gain into a fixed wall.

### And then: gain alone cannot reach 200%
Raising the ceiling helped, but exposed the real wall. **Digital audio stops at
1.0.** At 100% a chain sits at 0.72; a gain of 1.0 — reached around **139%** — is
the format's hard maximum. 200% asks for 1.44, which is 44% more than exists. No
threshold, no fader, no code can produce it; ask anyway and the peaks get sliced
flat, which the ear hears as buzz rather than volume.

So above 100%, the compressor **morphs from limiter into loudness processor.**

The ear judges loudness by *average* energy, not peak. A signal that touches 1.0
once and sits at 0.2 sounds quiet; one that never exceeds 0.9 but *lives* at 0.7
sounds far louder. So rather than push the peaks up (impossible), pull the quiet
parts up: compress harder, then make up the gain. Average level climbs toward the
ceiling without crossing it. This is what mastering does, and it is why modern
records sound loud on phone speakers.

| fader | gain | threshold | ratio | makeup | |
|---|---|---|---|---|---|
| **≤100%** | 0.72 | **-3 dB** | **20:1** | **1.00×** | **pure limiter — untouched** |
| 120% | 0.86 | -6 dB | 16.8:1 | 1.71× | loudness 19% |
| 139% | **1.00** | -8.8 dB | 13.8:1 | 2.29× | gain hits full scale |
| 175% | 1.00 | -14.2 dB | 8:1 | 3.74× | loudness 75% |
| 200% | 1.00 | **-18 dB** | **4:1** | **4.22×** | full loudness mode |

**At and below 100% the chain is electrically identical to what it always was.**
Same gain, same threshold, same ratio, unity makeup. Every hour of clipping and
chord-pumping work is untouched, and anyone who never moves the fader never
encounters any of this.

The price above 100% is dynamic range: a piano's decay flattens, attack and tail
move closer. For a metronome click that is ideal. For a sampled instrument you are
listening to musically, it costs life. **The user chooses** — which is the point.

All sixteen manually-created master gains (drums, theremin, Road Trip) were also
switched to the capped scale, so they cannot be driven past full scale either.

### Known gap
Five hand-rolled limiter chains (Road Trip, drum kit) build their own compressors
outside `buildLimiterChain` and connect straight to the destination. Their gains
are now capped so they will not clip, but they receive **no loudness processing** —
at 200% they will be full-scale-but-not-louder while the main surfaces get the
boost. Scoped follow-up, not a mystery.

## v0.81.10 — black screen: the storyboard needs the module

v0.81.9 built green and launched to a **black screen**. Nothing loaded.

`Main.storyboard` names the root view controller by class. The patcher swapped
`CAPBridgeViewController` for `IntonareViewController` — and **stripped the
`customModule` / `customModuleProvider` attributes** along with it, on the theory
that a class in the app target needs no module qualifier.

Wrong. UIKit resolves a storyboard's `customClass` **through its module**. With
the attributes gone it could not find the class, instantiated nothing, and the app
came up black. It compiled; the build was green; the failure is entirely at
runtime. (Xcode's own message for this is "Unknown class X in Interface Builder
file" — invisible without a Mac to read the device console.)

### Fixed
- The storyboard now reads
  `customClass="IntonareViewController" customModule="App" customModuleProvider="target"`.
  `CAPBridgeViewController` lives in the Capacitor module; ours lives in the app
  target, whose module is `App`. **Both** attributes had to change, not just the
  class.
- `@objc(IntonareViewController)` on the class, so the Objective-C runtime that
  storyboards actually use can see it.
- The patcher now **fails the build** if `customModule="App"` is absent after
  patching, or if any `CAPBridgeViewController` reference survives — and prints
  the resulting `viewController` line to the log. This class of bug will not ship
  green twice.

## v0.81.9 — the volume design: full loudness except while the mic is live

**Why iOS is quieter than Android even with routing fixed:** the `playAndRecord`
category runs output through a voice-processing chain that attenuates it — the
category is built for phone calls, where a loud speaker feeds back into the mic.
Apple's developer forums confirm it plainly ("when using .playAndRecord, all
sounds will be played with a low volume"), and WKWebView makes it worse: when
`getUserMedia` starts, WebKit reconfigures the session itself, flipping the mode
toward voice chat, which engages **Voice Processing IO**. Output ducks. No JS API
can undo it.

Note what this rules out: removing `.mixWithOthers` — the prior suspect — would
NOT have fixed this (multiple reports confirm `.defaultToSpeaker` +
`overrideOutputAudioPort(.speaker)` still cannot reach 100% on this category).
It would only have made Intonare pause everyone's Spotify for nothing.

### The design
Can the ducking be bypassed outright? Almost. The literal off-switch exists —
`kAUVoiceIOProperty_BypassVoiceProcessing` — but it lives on the VoiceProcessingIO
audio unit, and on iOS that unit belongs to **WKWebView's internal audio engine**,
which no API lets us touch. What IS available, per the Apple dev forums thread on
VPIO volume (721535): once VPIO has ducked the output, **re-calling `setCategory`
or `overrideOutputAudioPort(.speaker)` restores the level** — and any audio source
started afterwards may duck again and need another nudge. So:

- **Launch / mic off: `.playback`, mode `.default`.** No mic claim, no voice
  processing anywhere near the output, full volume. This is the app's resting
  state. (Previously `playAndRecord` was set at launch, which parked the whole app
  in the attenuated state before the mic was ever touched.)
- **Mic starts: `assertAudioMode()`** — `playAndRecord`, `.defaultToSpeaker`, mode
  `.default`, then `overrideOutputAudioPort(.speaker)` — the snap-back call.
- **New audio source while mic is live** (reference tone, drone, metronome):
  throttled re-nudge, max one per second, gated on `isListening`.
- **Mic stops: `releaseAudioMode()`** — back to `.playback`. Full volume returns.

The residual truth: while actually recording, iOS never grants quite the full
playback level on this category. Everything outside mic-time is now full volume,
and mic-time is as loud as the platform allows.

### Added
- **`IntonarePlugin.swift`** — Intonare's first real iOS Capacitor plugin. Two
  methods, `assertAudioMode()` / `releaseAudioMode()`, both one-shot,
  JS-triggered, **zero observers** (the observer-based ancestor of this idea
  looped `setCategory` against its own route-change notification and hung the
  app; the design constraint is written into the file header). Failure resolves
  `ok:false` rather than rejecting — a volume nudge must never break mic setup.
- **JS call site** right after `micStream` is set, iOS-gated, wrapped so no
  failure can propagate. Silently a no-op on Android/web/older builds.
- **Registration via `bridge.registerPluginInstance()`** from an
  `IntonareViewController: CAPBridgeViewController` subclass. Capacitor 8's
  config-based discovery (`packageClassList`) does not see local app plugins
  (capacitor#7409); instance registration from `capacitorDidLoad()` is the
  documented route. `patch_ios_appdelegate.py` now appends the plugin + subclass
  to AppDelegate.swift (same no-pbxproj-surgery reasoning as ever) and repoints
  `Main.storyboard` at the subclass, with hard verification and a printout of the
  storyboard if the anchor is missing. Dry-run tested against a faithful mock of
  the Capacitor 8 template, including idempotency on re-run.
- Panel now shows `audioMode: asserted / assert failed / plugin absent / not
  attempted`.

### Also fixed: haptics — and no Swift was needed
The plan was to add a haptic method to the new plugin. Reading the code first
made that unnecessary. The haptic functions call `window.Haptics` — the official
`@capacitor/haptics` plugin, which is installed, has an iOS implementation, and
is exposed by `main.iife.js`. The chain was correct end to end. Except:

    if (/^https?:/.test(location.protocol)) { ...load main.iife.js... }

**The loader's protocol guard only allowed http/https.** On iOS the protocol is
`capacitor:`, so the regex failed, `main.iife.js` never loaded, `window.Haptics`
never existed — and since every haptic function is try/catch'd by design, there
was no error anywhere. The buttons just didn't buzz. (The guard exists so nothing
is fetched when the raw HTML is opened from `file://` on desktop; it accidentally
excluded iOS.)

Fix: allow `capacitor:` in the guard. One regex. The panel now also reports
`Haptics bridge present/absent`.

### Why the plugin still matters
`IntonarePlugin` is the registration scaffolding the splash sound (and any future
native work) was waiting for. Adding a method to a registered plugin is trivial;
registering the first one was the wall.

## v0.81.7 — XHR fallback; the fetch scheme problem, actually fixed this time

Two prior attempts at the sample-loading bug did not survive contact:

- **v0.81.5** set `server.iosScheme: "https"`. Invalid — Capacitor's docs on
  `iosScheme`: *"Can't be set to schemes that the WKWebView already handles, such
  as http or https."* Silently ignored; origin stayed `capacitor://localhost`.
- **v0.81.6** enabled `CapacitorHttp` to patch `fetch` through native HTTP. On
  double-checking before shipping: native HTTP is URLSession, and **URLSession has
  no idea what `capacitor://` is** — it is a WKWebView scheme, registered inside
  the WebView. Whether the patched fetch handles local asset URLs is stated
  nowhere. It also has documented fallthrough cases (Request-object calls silently
  revert to browser fetch). A global fetch patch on both platforms for an
  unverified maybe is risk without proven reward. **Not shipped.**

### Fixed
- **`_fetchBuffer` now falls back to `XMLHttpRequest`** when `fetch` returns
  status 0 or throws. XHR goes through WKWebView's ordinary resource-loading path —
  the same one `<script>` tags and images use — which **can** read the
  `capacitor://` scheme. Old API, boring, works. Note: local-scheme XHR responses
  report status 0 *on success*, so the success test is "got bytes", not "2xx".
- Normal platforms are untouched: fetch succeeds, XHR never runs.
- The diagnostics panel now shows which transport loaded the samples
  (`via fetch` / `via xhr`).
- CI cleans any lingering invalid `iosScheme` from `capacitor.config.json` so it
  does not sit there looking intentional.

## v0.81.5 — fetch() cannot read the capacitor:// scheme

**Every sample on iOS was failing. All of them.** The diagnostics panel from
v0.81.4 gave the answer in two lines:

    origin       capacitor://localhost
    last error   HTTP 0
    ok / fail    0 / 294

**294 fetches, zero successes.** Not the piano — *everything*.

iOS Capacitor serves `www/` from the custom scheme `capacitor://localhost` by
default. WKWebView will load that scheme for `<script>`, `<img>`, `<link>` — but
**`fetch()` against it returns a response with status 0.** A custom scheme is not
treated as a normal HTTP origin, so the request never really happens.

Every audio sample is loaded with `fetch()`. Hence: synth, everywhere, silently.

### Fixed
- **`server.iosScheme` is now forced to `"https"` by CI**, before `cap add ios`
  runs. Capacitor then serves from `https://localhost`, which *is* a normal origin,
  and `fetch()` works.

  Patched in the pipeline rather than trusted to the file in the repo: `cap add
  ios` regenerates platform config every build, and a value this load-bearing
  should not depend on anyone remembering it. The step fails the build if
  `capacitor.config.json` is missing.

### Note on v0.81.4
The `document.baseURI` fix from v0.81.4 was correct and stays. It just resolved to
an origin that `fetch()` refuses — right instinct, wrong layer. The URI-encoding fix
(for filenames with spaces, like `Rdcus 024 060.mp3`) also stays; that bug is real
and would have surfaced the moment the scheme was fixed.

### Still open
- **Volume lower than Android**, though audio now comes from both speakers, so the
  routing fix worked. Next suspect is `.mixWithOthers`, which asks iOS to duck the
  app so it can share the output with other apps.
- **Haptics and splash audio**: `IntonareNative` reports absent. The bridge was
  never written for iOS. Both need real Capacitor plugins.
- **Top padding** still feels heavy under the notch.

## v0.81.4 — samples were never loading on iOS

The piano was still playing synth on iOS. The files are correct (30 mp3s, tracked
in git, copied into `www/audio/` by CI, no FATAL from the guard), so the failure is
between the file and the fetch.

### Fixed
- **`_capacitorAssetUrl` built a root-relative path.** It returned `/audio/<folder>/
  <file>`, and its own comment said why: *"Android assets under public/ are served
  directly from localhost/"*. That is an Android assumption, written when Android
  was the only target. iOS serves `www/` through a local server on a different
  scheme (`iosScheme: "https"`), so a root-relative path is not guaranteed to
  resolve the same way. Now built from `document.baseURI`, which is correct on
  every platform by construction and assumes nothing.
- **Filenames are now URI-encoded.** Some sample sets have **spaces** in their
  names — `Rdcus 024 060.mp3`. An unencoded space in a fetch URL is a silent
  failure, and it would have hit the Rhodes while sparing the piano, which is
  exactly the kind of half-working bug that wastes a day.
- **`grand_piano` had its own inline `assetUrl`** duplicating the shared helper.
  Routed through `_capacitorAssetUrl` so there is one implementation to fix.

### Added
- **Sample diagnostics in the audio panel** (seven taps on the version stamp):
  load state, ok/fail counts, the last URL actually fetched, the specific error
  (HTTP status, fetch throw, or decode failure with byte count), and
  `location.origin`. `_fetchBuffer` already threw a precise error; it was being
  swallowed into a `console.warn` that nobody can read on iOS without a Mac.

### Confirmed working (from the v0.81.3 panel)
AudioContext `running` at 48 kHz; mic track `live`, hardware rate 48 kHz matching;
`aec false`; peak reading real room noise. **The iOS audio path is healthy.**

`IntonareMic` and `IntonareNative` both report **absent** — neither native bridge
was ever written for iOS. So haptics and the splash sound are not broken; they were
never implemented on this platform. Both need real Capacitor plugins. The mic does
not: WebView capture at 48 kHz is working.

## v0.81.3 — the audio session was looping on itself

**The iOS lag was mine.** `IntonareAudioSession.swift` registered an observer on
`routeChangeNotification` whose handler called `setCategory()`. But `setCategory()`
can itself post a route change. Observer → setCategory → route change → observer,
on the main thread, from launch, forever.

That explains both symptoms together, which no other theory did: the app was
unusably laggy **from the splash screen**, before any user action; and the volume
meter read **silence**, because the session was thrashing its own category
thousands of times a second and the microphone never got a stable configuration.

### Fixed
- **Observer removed.** `IntonareAudioSession` is now one `setCategory` call, once,
  at launch. `.defaultToSpeaker` — the actual volume fix — is kept, because it is a
  flag on a category, not a thread or a callback, and it costs nothing.
- Also gone (all shipped in the same bad version, all removed):
  `setPreferredIOBufferDuration(0.005)` — asked iOS to wake the audio thread 200×/s
  and cross into WKWebView on each callback, for no gain, since detection latency
  is bounded by rAF and the FFT window. `setPreferredSampleRate(48000)` — iOS picks
  per route and the AudioContext reports the real value anyway. `setActive(true)` at
  launch — claimed the audio hardware from app open whether the mic was used or not;
  WKWebView activates the session itself when it needs one.
- The file now carries a header listing each of these and why it must not come back.

### Added
- **Audio diagnostics panel.** Seven rapid taps on the version stamp. (The
  long-press on the same element still opens the unlock-code entry; separate
  gestures, no collision.) Shows live: AudioContext state and real sample rate,
  whether a mic stream and track exist and what the OS reports for them, and the
  **raw peak amplitude off the analyser** — the number that distinguishes a dead
  microphone from a quiet one. Inert until opened: no DOM, no listeners, no polling.

  It exists because iOS audio fails silently. WKWebView refuses `getUserMedia`
  without saying so, an AudioContext can report `running` while producing nothing,
  and a broken `AVAudioSession` yields zeroes with no error. Without a Mac there is
  no console to read, so the app has to report on itself. Three wrong diagnoses
  tonight came from guessing at state we could simply have measured.

### Note on v0.81.2
The piano sample conversion (51 MB of WAV → 10.8 MB of mp3) was shipped as a fix
for this lag. It was not the cause — the app lagged before any sample loaded. The
conversion was worth doing anyway: 40 MB off the Android download, and no reason to
ship uncompressed PCM in a mobile bundle. But it did not fix what it was shipped to
fix, and that should be recorded honestly.

## v0.81.2 — piano samples were 51 MB of uncompressed WAV

**The app became unusable on iOS.** Cause: `grand_piano` shipped as **29.8 MB in
30 uncompressed WAVs**; `electric_piano` as **21.5 MB in 13**. Every other
instrument in the library is mp3 at 15–25 KB per note. These two were outliers by
roughly a factor of eighty.

`SampleEngine.load('grand_piano')` fires shortly after launch and fetches all 30
notes with `Promise.all` — thirty simultaneous requests, then thirty
`decodeAudioData` calls on raw PCM. Android serves those from the APK's local
assets and absorbs it. **iOS serves `www/` over a localhost HTTP server inside the
app**, so the same load is thirty HTTP round trips plus thirty decodes on a phone.

Before v0.81.1 the files were not bundled at all, every fetch 404'd instantly, and
the synth fallback ran. Bundling them is what exposed the weight.

### Fixed
- **`grand_piano`: 29.8 MB → 7.9 MB.** Source is already mono 16-bit/44.1k, so
  transcoding to 192 kbps mp3 loses nothing.
- **`electric_piano`: 21.5 MB → 2.9 MB.** Source is **stereo**; kept stereo at
  192 kbps. (An earlier pass folded it to mono to save 0.5 MB. Reverted — a Rhodes
  has real stereo width and a musician on headphones would hear it flatten. Not
  worth half a megabyte.)
- **Net: 51 MB → 10.8 MB.** The Android download shrinks by the same 40 MB.
- Both `noteToFile` maps repointed `.wav` → `.mp3` (59 references), plus the
  shared `_salamanderNoteToFile` helper. No other instrument touched: the other
  36 route through `_gleitzNoteToFile` and were always mp3.

### Note
This is the second time this bug has been fixed. The comment above the preload
(`removeSplash`) records the first: eager-loading *every* registered instrument at
launch made the tuner feel laggy, and the fix was to warm only the grand piano.
Correct as far as it went — but the grand piano was itself 15× heavier than any
other instrument, and that part survived. Android tolerated it. iOS did not.

### Known open
- **`audio_assets/mandolin/` is empty.** Zero files. It has been failing to load
  and falling back to synth silently. Unrelated to the above; needs sourcing.
- **The iOS audio session (`IntonareAudioSession.swift`) is still untested.** It
  shipped in a build that TestFlight buried below the old `1.0` version group, so
  no tester has ever run it. Whether `.defaultToSpeaker` actually fixes the
  earpiece-routing problem is still unknown.

## v0.81.1 — iOS build pipeline

> **Changelog gap:** entries between v0.73.37 and v0.81.1 (the audio detection
> overhaul, Road Trip journey slices, FFT pitch detector, Leg Tuner) are not in
> this file. They were shipped and sentinel-verified but the log was not kept.
> Reconstruct from chat history when there is time.

**iOS shipped to TestFlight for the first time.** Signed build, three internal
testers, microphone confirmed working on WebKit. No native audio plugin needed:
the same web code drives all seven mic surfaces on iOS.

### For testers
> TestFlight "What to Test" notes are written by hand in App Store Connect
> (TestFlight → Builds → the build → What to Test). Not automated: a build that
> refuses to run because the release notes were not written is a build that gets
> the check deleted. Copy from here if useful.

Fixed: the piano and other sampled instruments now play real samples rather than
falling back to synth; audio should be much louder once the microphone is on (it
was going to the earpiece speaker instead of the loudspeaker); the header no
longer sits under the notch; buttons buzz again (haptics were missing entirely);
real app icon.

To test: turn the microphone on, then play a reference tone or start the
metronome — is it loud enough now? Start a drone and sing over it: does the tuner
still track your voice, or does the drone coming out of the speaker confuse it?
If you have Bluetooth headphones, does the audio play through them?

### Web (`Intonare.html`)
- **iOS safe-area padding fixed.** `body { padding-top: min(8px, max(2px,
  env(safe-area-inset-top))) }` caps the top inset at **8px**. That cap exists for
  Android sticky-immersive, which zeroes the reported inset. On iPhone the inset
  is the real notch (**47–59px**), so the cap threw it away and the header sat
  under the Dynamic Island. Added `html.ios body { padding-top:
  env(safe-area-inset-top) }` — full inset on iOS, cap retained on Android.
- **Platform class set on `<html>` from JS** in `DOMContentLoaded`
  (`documentElement.classList.add(Capacitor.getPlatform())`). Capacitor may do
  this itself; doing it here means the CSS rule above does not depend on that
  behaviour holding.

### Build pipeline (`codemagic.yaml`)
Codemagic builds and signs iOS on every push; `ios/` is **not committed** and is
regenerated each build, so all native customisation happens as CI steps. This is
the same pattern as `go.bat [4b]–[4c2]` restoring `MainActivity.java` after
`cap sync` overwrites it.

- **Audio samples were missing → every sampled instrument fell back to synth.**
  The app fetches from `/audio/<instrument>/`, but they live in
  `audio_assets/<instrument>/`; `go.bat [4g]` does that rename and the CI step
  did not. Now mirrored, and the step **fails the build** if `audio_assets/` is
  absent rather than silently shipping a synth-only app.
- **`main.iife.js` was never built → haptics silently dead on iOS.** `go.bat [4a]`
  runs `npm run build` (Vite compiles `main.js` into the Capacitor haptics
  bridge); the CI step skipped it. Its absence produces no error anywhere. Now
  built and guarded.
- **App icon.** `cap add ios` writes a placeholder `AppIcon.appiconset` fresh
  every build. Real icon injected from `ios_icon/AppIcon-1024.png`. Rebuilt as
  **SVG** (`intonare_icon.svg`) traced from the 512 raster, so it renders at any
  size — the largest Android asset was 192px, and a 5× upscale to Apple's required
  1024 would have been mush. **Flat RGB, no alpha:** Apple rejects transparency in
  app icons at *upload*, not at review.
- **`Info.plist` patched** via PlistBuddy: `NSMicrophoneUsageDescription` (without
  it iOS *terminates* the app the instant `getUserMedia` fires — not a permission
  denial, an immediate crash), `UIBackgroundModes: audio`,
  `UISupportedInterfaceOrientations: portrait`, and
  `ITSAppUsesNonExemptEncryption: false` (pre-answers the export-compliance
  question App Store Connect otherwise asks on every upload).
- **`capacitor.config.json` · `server.iosScheme: "https"`** — iOS Capacitor
  defaults to the `capacitor://` scheme, which WebKit does not reliably treat as a
  secure context. Without this, `getUserMedia` and Web Audio are blocked outright
  and all seven mic surfaces fail silently.
- **Signing.** Certificate + provisioning profile are generated in the Codemagic
  UI, not at build time. `fetch-signing-files --create` cannot work alone: Apple
  only ever holds the *public* half of a certificate, so it can issue one but
  cannot return a private key to pair with it. Build is flagged
  `testFlightInternalTestingOnly` — internal testers need no Beta App Review.
- **`.gitignore` patterns anchored to root** (`ios/` → `/ios/`). Without the
  leading slash, git matches the pattern **at any depth**, so `ios/` was silently
  ignoring `native_src/ios/` too.

### Native (`native_src/ios/`)
- **`IntonareAudioSession.swift` + `patch_ios_appdelegate.py`.** When WKWebView
  calls `getUserMedia`, iOS switches the audio session to `playAndRecord`, which
  routes output through the **earpiece receiver** rather than the loudspeaker — the
  OS assumes an app that records and plays at once is a phone call. Everything the
  app plays goes quiet the moment the mic is touched. **WebKit exposes no way to
  change this**; there is no JS API. `AVAudioSession` is the only lever and it is
  native-only.
  - `.defaultToSpeaker` — the fix.
  - **`.allowBluetoothA2DP`, deliberately NOT `.allowBluetooth`.** A2DP is
    high-quality, output-only, no microphone. `.allowBluetooth` enables the HFP
    headset profile, which collapses the **entire session, both directions**, to
    **8–16 kHz mono**. With AirPods connected the tuner would silently start
    reading an 8 kHz mic feed (Nyquist ceiling 4 kHz), gutting the harmonic content
    the FFT detector depends on. No error, no warning. 📌
  - `.mixWithOthers`; preferred sample rate **48 kHz**; IO buffer **5 ms**.
  - Category is **re-asserted** on `routeChangeNotification` and after
    `interruptionNotification` ends — plugging in headphones or taking a call
    resets it, and without this the app returns quiet.
  - Applied by appending to the generated `AppDelegate.swift` rather than adding a
    new source file: Xcode tracks sources in `project.pbxproj`, and scripted
    surgery on pbxproj is exactly the kind of thing that breaks quietly later.

### Known open
- **`_iosBetaUnlock()` still grants Pro to every iOS user with no purchase path.**
  This gates everything: no external testing, no public TestFlight link, no App
  Store, under Guideline 3.1.1. Needs the RevenueCat iOS key, an IAP product in
  App Store Connect, StoreKit wired, Restore Purchases verified.
- **Microphone permission string is English-only.** Needs `InfoPlist.strings` in
  `it.lproj`/`en.lproj`, registered as Xcode resources.
- **Loudspeaker now fires next to the microphone.** The drone notch measures
  **−38 dB** on the drone with voice at −0.1 dB, so the detector should stay clean —
  but the mic's input stage now sees a much hotter signal, and any AGC iOS applies
  could duck the voice to compensate. Unverified on hardware.
- **Version string pinned at `1.0`** in TestFlight (comes from the regenerated
  Xcode project, not `INTONARE_VERSION`). Cosmetic until public release.

## v0.73.37
- **TONAL · temperament toggle restyled into the CRT language.** The old
  `ref-toggle` pill (last thing breaking the retro illusion) rebuilt as a keycap
  segment (`.tc-temp-seg` / `.tc-temp-key`) in matching dark housing — lit label
  only on the active key, same look as the root/octave keys. Explanatory hint line
  kept (teaching-app: the toggle is contextual, beginners need it explained). `?`
  help moved into a `.tc-strip-lab-row`.
- **TONAL · HUD mode mirror added.** Display-only `◈ EQ` / `◈ JUST` tag
  (`#tcTempMirror`) inside the CRT HUD shows the current temperament like real
  hardware; the keycap below controls, the tag reflects. Plain 7px pixel text (NOT
  a bordered box — the HUD is pinned `height:10px; overflow:hidden` for layout
  stability, a box would clip).
- **`toggleTemperament()` rewired** to drive both keycaps + mirror; hidden
  `#tempLabel` span kept so legacy reads don't crash. `temperament` still the only
  consumer of the value (feeds the just-intonation cents target in
  `updateIntervalDisplay`); it lives ONLY in tonal-centre, nowhere else in the app.
- **i18n:** new `tuner_tuning_system`, plus short keycap labels `tc_temp_equal` /
  `tc_temp_just` (so the key reads "JUST" not "JUST INTON."; the longer
  `tuner_just_inton` is untouched for the main tuner). EN + IT.

## v0.73.36
- **TONAL · CRT screen height reduced** `412px → 348px` (felt too tall on-device,
  ~half the viewport). Internal spacing tightened to match: `.tc-hud` margin-bottom
  `18→14px`, `.tc-iv-stage` margin-top `18→12px`, `.tc-reticle` margin `20→14px`,
  `.tc-crt` padding `22px 18px 22px → 18px`. Layout-stability invariants intact
  (fixed height + `.tc-screen-body` flex:1 + tabular-nums → no reflow on drone
  on/off).

## v0.73.35
- **TONAL · tour repointed at the CRT.** The `tonal` module tour still pointed at
  the now-hidden `#tcToggleBtn` (preview rendered blank). Repointed at visible
  elements: `#tcCrt` (readout) → `#tcRootGrid` (root/scale/octave + scale map) →
  `#tcStartBtn` (power-on + blue/red/green colour meaning) → `#micBtn`. EN + IT.
- **TONAL · `tonal_center` help rewritten** for the CRT layout (was describing the
  removed "What Am I Singing?" panel). Added `?` help button in the ROOT NOTE
  strip-label row (`.tc-help` pixel-chrome style, carries `help-btn` class so it
  respects the global hide-help-tips toggle).

## v0.73.34
- **TONAL · CRT/retro redesign ported into the app** (from `tonal_redesign_v6.html`
  preview). Full markup swap: cabinet + fixed-height CRT screen, DRONE↔YOU note
  pair, interval-name hero, lock-on reticle tuning bar, control strip with keycap
  root grid + custom (non-native) scale dropdown + octave keycaps + second SCALE
  MAP screen with live scale-degree highlight. Volume slider dropped per design.
- **Removed elements kept as hidden legacy hooks** (`#pianoIntervalName`,
  `#pianoCentsBadge`, `#tcDroneState`, `#tcScaleType` native select, etc.) inside a
  `display:none` div so `updateIntervalDisplay()` keeps writing them without crashing.
- **JS wiring:** `tcInit` builds keycaps + dropdown; `tcUpdateScale` builds the
  root-anchored scale map w/ degree numbers; `tcDroneStart`/`tcToggleDrone` drive
  power-on/standby (preserved the critical `droneRoot`/`droneOctaveIdx`/`_dronePureSine`
  sync before `droneStart()`). Live readout EXTENDS `updateIntervalDisplay` via a
  `tcRenderCRT(mode,data)` hook at its 3 exit points — all existing hold/temperament/
  JI/highlightPiano logic untouched.
- **Colour is meaningful 📌:** flat=blue, sharp=red, in-tune=lime/green; the hero,
  YOU note, reticle marker, and cents all tint by tuning direction.
- **Press Start 2P font self-hosted** as base64 (12.5KB woff2 from npm fontsource;
  Google Fonts CDN forbidden by sentinel pin). Used for HUD/chrome labels ONLY;
  Bebas for big content, JetBrains Mono for Hz.
- **i18n:** tc_drone_off, tc_listening, tc_drone_lab, tc_you_lab, tc_scale_map,
  tc_flat, tc_sharp, tc_iv_start, tc_standby, tc_matching_root/above_root/below_root,
  drone_stop — EN + IT. Orphaned (harmless): tc_what_singing, tc_set_root_hint.

---

## Gap reconstruction: v0.20.43 → v0.73.33 (~June 6–30)

> ⚠️ **Reconstructed from chat history, NOT live-logged.** Live logging lapsed
> after v0.20.43 and didn't resume until the CRT work (v0.73.34+). This block
> covers ~53 version bumps across ~15 chats. It is grouped by feature area, not
> per-version — individual version numbers below are anchors I could verify, not a
> complete bump-by-bump record. Exact values were not re-verified against the file.
> Treat as "what shipped in this window," not as precise as the live entries.

### Instruments · woodwind fingering charts (the dominant work of this window)
- **Oboe + cor anglais fingerings finalized** (~v0.43.2–0.43.4). Main fingerings
  verified vs wfg.woodwind.org; full alternate-fingering sets added across both
  octave registers (Side Bb, Fork Eb/F/G#/A, Oct I alts, etc.); fixed a bug where
  second-octave alts weren't surfaced to the UI alt-cycle buttons. Oboe altissimo
  added (MIDI 85–93, C#6–A6); range bumped high:93, octave 6. Cor anglais fully
  synced to oboe (no altissimo — non-standard).
- **Woodwind chart visuals normalized.** All renderers (oboe, recorder, whistle,
  clarinet, sax) unified to open-key GREY `#8a99a6` matching flute; closed ACCENT
  hardcoded `#2ec78f` (SVG can't resolve CSS vars). Clarinet/sax maxWidth caps
  added to stop sprawl.
- **Bassoon + contrabassoon FDB import** (v0.58.5–0.59.3). First instrument built
  from Bret Pimentel Fingering Diagram Builder SVG exports (CC BY-NC-SA 4.0, Bret
  emailed + granted permission; credit added to Credits modal). Verbatim path data
  wrapped in the original transform `matrix(.75 0 0 .75 3.718 2.395)`; `bodyPath()`
  grey-stroke structure + `keyPath(d,slot)` interactive keys (ACCENT fill closed,
  GREY stroke open, fill-rule evenodd). Quadrant labels only (LT/RT/LH/RH) — in-key
  labels abandoned as un-centerable. Sub-tab switching needs 4 synced sites
  (WW_SUBS, CS_INSTRUMENTS, switchSubType, _buildSubRow ternary) — pinned learning.
- **`BRET_SVG_IMPORT_GUIDE.md` written** — Claude-targeted process doc for importing
  the remaining 9 woodwind families. Clarinet identified as next (Standard Boehm
  Bb/A/Eb + Bass clarinet pro), parked on Daniele needing desktop FDB donor auth.
- **Flute trills + clarinet** (earlier in window, ~v0.38–0.39). Flute renderer
  traced via potrace (18 toggleable key slots); TRILLS subtab infrastructure built
  for woodwinds from scratch; trill audio via alternating pitches. Clarinet got
  MIDI-direct fingering lookup (register-break accuracy) + trills. Flute collapsed
  to one `ww_flute` with Flute/Piccolo/Alto sub-types (piccolo 8va up, alto P4 down).

### Charts · audit pass (fretted + brass + woodwind ledger)
- **`INSTRUMENT_AUDIT_LEDGER.md`** built — full tier'd status of every instrument's
  chart/fingering correctness with sources + open questions.
- **Bass trombone low register fixed** (v0.67.0–0.67.1): notes below ~E2 all
  defaulted to Position 1; replaced with full sourced F/D chart (Doug Yeo / Waage).
- **Mandola tuning fixed** GDAE → CGDA (viola pitches; code comment said "fifth
  below mandolin" but MIDI didn't match).

### Tools · new + finalized
- **Rhythm Flash Cards** built and finalized (v0.53.0–0.54.2). 29-card deck
  (whole→sixteenth, dotted, ties, triplets, syncopation, RESTS), onset-distinctness
  validator to kill tap-identical collisions, multi-select category Set, Fisher-Yates
  shuffle on open, full-screen `position:fixed; inset:0` overlay, drill-to-mastery
  mode (3 consecutive passes at ≤0.10 bar, neutral stats by design), tap-only
  haptics. Uneven-tuplet bracket rendering fixed (group by whole-beat sum).
- **Polyrhythm** finalized (through v0.68.83): tempo-leak fixes (constants not
  inherited prBpm), downbeat-drop scheduler fix (late clicks clamp to currentTime,
  only >20ms dropped), end chimes, help modal.
- **Metronome grooves** expanded earlier in window: +27 patterns across odd meters
  (3/4–11/8) → 51 grooves, +18 chord presets → 37, preset pairings audited,
  suggestedBpm hints.

### Train · interval / ear-training
- **Interval Training + Flash Cards** work (v0.66.50–0.66.57). Mic-powered; share
  helper `intonareNativeShare()` confirmed as 3-tier (native → web → clipboard).

### Launch prep (the pre-Play-Store push)
- **Privacy policy** drafted + shipped (`privacy.html`, github.io/Intonare/privacy),
  styled to app; covers mic, local storage, gleitz soundfont fetches, children's
  privacy, GDPR, Italian jurisdiction.
- **App icon + notification icon** built: `intonare_icon_512.png` + adaptive
  launcher set (`icon_res.zip`, mdpi→xxxhdpi, mask-verified circle+squircle);
  `ic_stat_intonare` notification icon (5 densities).
- **Splash audio sync fix** in `MainActivity.java` (native): removed `runOnUiThread`
  from `playSplashSound()` so `MediaPlayer.start()` fires on the binder thread; added
  audio pipeline pre-warm in `prepareSplashSound()`.
- **RevenueCat / IAP Pro unlock (Layer 1) — DONE** (built June 24 splash session).
  One-time-purchase model, integrated + shipping. Public RevenueCat SDK key ships by
  design (`goog_rbcoHGgwLmrhKklhmYPGFtvsSKL`); security scan clean (no secrets/
  keystore/service-account in repo).
- **Play Console submission published to CLOSED TESTING** (resolved an Advertising-ID
  declaration blocker → answered No).
- **DYK / fact-bank copy pass** (v ~0.73.x, late June): tone/AI-speak cleanup across
  the fact bank; flagged-not-fixed content dups (two Wes Montgomery near-dups, a
  Beatles/Decca pair, a `},,` double-comma at the Leo Fender entry).

### Native groundwork (scaffolding, not user-facing)
- **Web AEC stopgap** shipped v0.73.13: `_ECHO_TOOLS=['tonal']`,
  `_ECHO_EXERCISES=['interval','singsing']` → `_wantEcho` requests
  `echoCancellation:{ideal:true}` for reference-tone modes; tuner stays raw. Marked
  scaffolding for removal when native lands.
- **`NATIVE_AUDIO_ENGINE_PLAN.md`** written; **Phase 0 native mic plugin**
  (`IntonareMicPlugin.java`, `ping()`) placed. Key learning pinned: Capacitor 8 does
  NOT auto-discover app-embedded plugins — explicit `registerPlugin(...)` before
  `super.onCreate()` required. go.bat got a `[4c2]` native-restore line.

### Tooling
- Sentinel grew **85 → 97 tracked fixes** (9 new from Flash Cards) + pins 21 → 27.
- `intonare_quiz_audit.py` regex repaired (over-escaped raw string crashed
  `re.compile`); now parses cleanly.

---

## v0.20.43
- **NAV · folder reorg (per Daniele).** (1) Train "Rhythm" renamed → "RHYTHM
  TRAINING" (EN) / "ALLENAMENTO RITMICO" (IT) to end the clash with the Tools
  "Rhythm" (drumkit) folder; also fixed the JS routing key for the tools folder
  (`folder_rhythm_title` → `folder_rhythm_tools_title`) so the tools folder header
  still reads just "Rhythm". (2) "Analysis & Reference" (5 items) split into
  **Reference** (Circle of Fifths, Vocal Range, Survival Guide) + **Utilities**
  (Volume Meter, Transposer). New folder ids `toolFolderReference` /
  `toolFolderUtilities`, routing map + IDs updated, two new hub entry cards, full
  EN/IT i18n. Old `folder_analysis_*` keys now orphaned (harmless). (3) Drumkit
  folder left as-is per Daniele.
- **i18n · all 6 flagged hardcoded strings fixed** + the Diadle guess counter:
  PLAYING/PAUSE/RESUME (rhythm-reading), ALL chip, TAP AGAIN TO CONFIRM (×2),
  GUESS N OF M. New keys rr_*, chip_all, confirm_tap[_warn], diadle_guess_of
  (placeholder-interpolated). Strings audit now 0 hardcoded.
- **FAV · Diadle can now be favorited** — added `exercise:diadle` FAV_META entry.
- **QUIZ · 2 criticals fixed** (Music History): lengthened the distractors on #61
  Philly Soul and #24 outlaw country so the correct answer is no longer a
  length-giveaway. Quiz audit: no criticals.
- **TOOLING · both audit scripts repaired this session** (strings key-extraction
  regex; quiz filepath arg) — re-shipped.

## v0.20.42
- **UI · stale folder counts fixed.** Games badge 3→4 (Diadle was added but the
  count + sub-string never updated); now uses its own `folder_badge_games4` key
  instead of sharing Ear Training's `folder_badge_ex3`. Analysis & Reference
  badge 4→5 (has cof, volume, transpose, vocalrange, survivalguide); new
  `folder_badge_5` key. `folder_games_sub` now lists Diadle (EN + IT).
- **Tooling · strings audit repaired.** Its key extractor matched only
  one-per-line keys (`\n    key:`), missing all multi-per-line keys → 372 FALSE
  "key not in STRINGS" errors. Fixed regex to catch keys after `,` too;
  extraction 542→933 keys, false errors gone.
- **Tooling · quiz audit repaired.** Had a hardcoded input path; now takes a
  filepath argument like the others.
- **Audit findings logged (NOT yet fixed — Daniele to action):**
  FAV_META missing for `exercise:diadle` (can't be favorited); 6 hardcoded UI
  strings (ALL, PLAYING, RESUME, PAUSE, GUESS, TAP AGAIN TO CONFIRM); 2 quiz
  criticals in Music History (correct answer ~2.7× longer than wrong: #61 Philly
  Soul, #24 outlaw country) + 89 milder length warnings.
- **Pending (waiting on Daniele's spec):** folder module moves + renames.

---

## v0.20.41
- **UI · long-press text-selection guard restored** (regression). Global
  `user-select:none` + `-webkit-touch-callout:none` re-added on
  `html, body, button, .practice-card-btn, [onclick]`; re-enabled
  `user-select:text` on inputs/textareas/select/contenteditable so typing & paste
  still work. Had silently vanished from the global rule.

## v0.20.40
- **UI · games folder extra header fixed.** Added `#gamesHub .train-header` to the
  in-section header-hiding CSS rule — it was the only sibling hub left off the
  list, so Games showed a redundant second header.

## v0.20.39
- **Tónale · score decimals unified.** Final count-up + share now whole-number to
  match the live header (`N / 50`). Was: header whole, count-up `.toFixed(1)`,
  share `.toFixed(0)` — three representations of one score.
- **Tónale · per-round breakdown** added to final screen (`tonaleRenderBreakdown`):
  per-round colored dot + cents-off + points. New i18n key `tonale_round_abbr` ('R'/'R').
- **Tónale · guess wave tints to score color on reveal.** Wave uses
  `tonaleCmp.colorResolved` (concrete color from `tonaleResolveColor`, since canvas
  can't read CSS `var()`); only overrides during `revealed` state.

## v0.20.38
- **Audit · Pass 19** added to instrument audit: flags any woodwind pitch class
  in-range but missing from its fingering table (silent home-fingering fallback).
  Hardened `parse_ranges` to handle nested `subRanges`.
- **UI · embouchure card min-height 📌** set to `78px` with flex-centering on
  `#trpCardEmbouchure` and `#trpEmbouchure`, so variable-length embouchure text
  never resizes the note card. (was: no min-height → card grew/shrank per note)

## v0.20.37
- **WIND · ocarina C4 bug — real fix.** Wind note grid offered any octave×pitch-class
  with no range check, so out-of-range notes (e.g. C4, below ocarina A4 floor)
  showed the same fingering as the in-range octave. Now: octave selector only
  offers octaves containing in-range notes; out-of-range pitch buttons are
  disabled/greyed ("Out of range for this instrument"); selection snaps to lowest
  in-range note. General fix — applies to all wind instruments.
- **WIND · ocarina range 📌** `octaves:[4,5]` → `[4,5,6]` so high C6–F6 are reachable
  (12-hole high `89`/F6; 7-hole capped `84`/C6).

## v0.20.36
- **WIND · ocarina fingerings rebuilt from source** (pureocarinas.com / Hickman).
  Old data was invented (fake octave-register split). Now one continuous
  hole-opening sequence; diatonic naturals verified, accidentals = labeled
  cross-fingerings. C5 home 📌 = `[1,1,1,1,0,0,1,1,1,1,1,1]`.
- **Audit · Pass 18** added: asserts the 6 verified ocarina diatonic naturals
  against expected values (catches invented/regressed fingerings).
- **Breath hints** corrected (no "register/overblow" language — ocarina has no
  octave registers).

---

## Earlier (reconstructed from history, pre-live-logging)

### Tónale (added ~v0.20.x, "Adding Tonale" chat)
- Pitch-memory game modeled on dialed.gg/sound. 5 rounds, scored /50, easy/hard
  modes + daily challenge with mid-game resume (`dailyInProgress`).
- Reveal color thresholds 📌: `pts>=9.5` green, `pts>=7` amber, else red.
- Positive-cue (haptic/sound) threshold 📌: `pts >= 6.5`.
- Frequency skew biases targets higher (`Math.pow(r, skew)`); per-mode ceilings
  raised (easy E5, medium C6, hard A7, insane G8).
- Wave visualizer: crest speed made constant across pitch (phaseStep scales with
  cycle count). Slider reskinned to "wide pitch-field" with frequency ladder.

### Diadle (scale-degree ear-training game)
- Wordle-style; name each note's scale degree. Difficulties 📌: all three
  `maxGuesses:5` (easy len 3/drone, medium 4/button, hard 5/once).
- Locked-slot carryover between guesses; loss screen reveals each degree + note;
  daily mode w/ shareable emoji grid; first-try firework.
- Piano-timbre voice through reverb bus; click fixed with 18ms attack +
  asymptotic release.

### Quiz (19 packs, 1153 questions)
- **Major regression repaired:** ~116 `opts` arrays were scrambled onto wrong
  questions (truss-rod Q had amplifier options, etc.). Re-paired across 8 packs;
  spot-checked. The clean June-3 474Q build had never merged in.
- Beatles rooftop/George-Martin question swap fixed.
- 14 compound questions trimmed to just the "what".
- Background scroll/bounce lock (`body.sg-open`); two-tap reset stats;
  missed-questions scroll + centered title; game-over redesign.
- Daily streak toast opacity 📌: solid base layer on all tiers (`opacity:1`),
  regression-proofed.

### Metronome / Progression
- BPM scrub wheel: flywheel inertia, windowed velocity (fixed direction-flip from
  ghost mouse events + sign error in `_bpmFrac`), `_computeReleaseVel` ignores
  stale samples.
- Tick sound 📌: two detuned sines `3100Hz + 4700Hz`, 12ms exp decay; Hann-windowed
  prebaked buffers (no GC pops); 38ms rate limiter.
- Groove mode: dynamic `groovePattern.length` (not hardcoded 16); 51 grooves,
  37 chord presets; mute syncs across views (`metroMuteBtnGroove`); long-press
  sort needs 10px threshold + `touch-action:pan-y`.
- Shared `getAudio()` context to kill clock drift; `startMetroAt` for bar-boundary
  alignment; time sigs 2/4–11/8.

### Charts / instruments
- Capo root-shift moved to top of `gccVoicings()` (universal across instruments).
- Added banjo (roll engine), mandolin, mandocello, uke bass, baritone/tenor guitar.
- Mandocello cache-prefix fix (was returning mandolin shapes); sub-tab cold-open
  fix (`_buildSubRow` called directly); save-chart `keepState` (root restores).
- Bass synth click 📌: 3ms (`0.003`) linear ramp from zero; removed redundant
  sub-oscillator (phase-beating buzz).
- Harmonica pathMap keyed by MIDI not pitch-class (wrong-C highlight fix).
- Ocarina diagram: traced geometry from PDF; rule = change labels, never positions.

### System / layout / i18n
- Lang switch no longer false-fires drumkit achievement (`fromLangSwitch` guard).
- Haptic feedback default-ON with `progLoad` migration.
- Permission flow split: notifications immediate on splash removal, mic on first
  touch (`_reqMicPerm`).
- Survival Guide: in-flow layout w/ measured `--sg-h`; dynamic `--nav-bar-h` /
  `--header-h` from live DOM; tools tab exits folder.
- Version lives in 3 synced spots (top comment, JS const, `#smVersionStamp`).
- Renamed Sonoro → Intonare; appId `com.lieutenantdan.intonare`.
