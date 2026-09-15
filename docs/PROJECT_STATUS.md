# Intonare project status

Last updated: September 2026. Verify against the CHANGELOG.md and the
actual codebase before relying on any status line here.


## What it is

Intonare is a bilingual English/Italian music education app. It ships
as a single HTML file (~131,000+ lines of vanilla JS, CSS, and HTML),
Capacitor-wrapped for Android and iOS. Sole developer: Daniele
(LieutenantDan76 on GitHub). Primary tester: his mother, Linda.

The app covers: chromatic tuner with pitch history and vibrato
detection, metronome with groove sequencer and drum machine, ear
training exercises (intervals, chords, scales, Chordle, Tonale,
Diadle, Road Trip, Polyrhythm, Rhythm Reading, Tempo Guess, Music
Quiz), chord and scale reference charts, vocal range assessment, piano
song bank with playback, and a Survival Guide with interactive
instrument anatomy diagrams.


## Platform status

- Android: Play Store closed testing. Cleared for production access
  (questionnaire approved). Still shipping through closed testing until
  the production launch cutover.
- iOS: live on TestFlight via Codemagic cloud Mac build. Automatic
  builds are OFF; start a build manually in Codemagic when you want an
  IPA. CHANGELOG.md top entry must match INTONARE_VERSION or the build
  fails.
- Web: GitHub Pages at lieutenantdan76.github.io.
- IAP: RevenueCat built and shipping.
- Backup/restore: built, shipped, verified on-device.


## Version

Check CHANGELOG.md for the current version. As of this writing it is
v0.210.66. The marketing version lives in two declarations in the HTML
file that must stay in sync: an HTML comment near the top (grep
`INTONARE_VERSION:`) and a JS const. The Settings footer reads the
const; it is not a third literal. Android Play versionCode / versionName
are separate: go.bat for day-to-day, release.bat only on upload day.
version.txt must match android/app/build.gradle versionCode.


## Architecture

- Single-file HTML/CSS/JS, no build system for the app itself.
- Web Audio API for all sound (pitch detection, tone generation, drum
  synthesis, audio cues).
- One shared AudioContext via `getAudio()`. Do not create a second
  one; iOS Safari caps at ~6 and the Capacitor WebView hits silence.
- CSS custom properties with `@property` registration for animated
  theme transitions. Six color modes (one per tab/tool family) plus
  a light mode system using OKLCH-based saturated grounds.
- Capacitor 8.3.4 + Vite for native wrapping. go.bat handles the
  full pipeline: git push, npm build, cap sync, native file
  restoration, gradle clean when native sources change.
- Codemagic for iOS CI. RevenueCat for IAP. gleitz MP3 soundfonts
  for instrument samples. Bravura/SMuFL for notation rendering.
- Fonts: Fraunces (app name, flavor quotes), Bebas Neue (module/tool
  headers), JetBrains Mono (code-style readouts).
- i18n: a `STRINGS` object holds all EN/IT pairs. `t('key')` returns
  the active language string. `setLang()` persists to localStorage and
  calls every module's init so UI updates live. `applyLang()` pushes
  strings into the DOM. When editing i18n strings, watch for triplicates:
  the STRINGS value, a hardcoded DOM default, and a JS fallback can all
  carry the same text.
- Voice picker UI: the 4x2 grid is for tone banks with 8 options.
  Tighter contexts (chord/scale/exercise selectors) use the chip scroll
  strip. Don't put a grid where a strip belongs or vice versa.
- Reference sources: ABRSM standards for piano scale fingerings;
  tombatossals chord DB structure for guitar voicing reference.


## Active focus (verify against changelog before assuming)

As of the Claude handoff (Sep 2026), recent focus areas were:
- Drum engine (cymbal/brush synthesis, BPM per-step nudge)
- Drumkit UI layout (grid-first + dock panel)
- Light mode color system (OKLCH, per-theme saturated grounds)

Also shipped / settled:
- Krueger MIDI CC BY-SA publish: `credits/midi-sources/` live + linked
- Staff Notes shipped; Melody Dictation and Score Reader still deferred
- Android native mic is app-wide for pitch surfaces; WebView is fallback
  on native failure and the only mic path on iOS. Do not reintroduce a
  "half-native" capture+JS detection path.


## Quiz pack triage status

Daniele hand-triages each pack in English first; Italian only after
his pass. Voice reference packs: beatles and guitar_technique only.

Triaged and done: beatles, eighties, guitar_technique,
theory_fundamentals, advanced_theory, guitar_gods (90q), seventies
(113q).

Bass (104q): was partially triaged earlier (54% kept rate). Daniele
believes the full triage may now be done. Verify by checking the
changelog or asking before acting on the assumption it's incomplete.

Ignore any old `QUIZ_TRIAGE_HANDOFF.md` if it reappears; it was wrong
about advanced_theory / theory_fundamentals status.


## Known pending items

Verify each of these against the codebase before starting work. Some
may already be done.

- Dormant grid deletion: 7 converted piano songs (liebestraum,
  clair_de_lune, moonlight, prelude_c, moonlight_3, prelude_em,
  fuer_elise), ~157KB. Daniele approved the deletion but it may
  already have been carried out.
- Survival Guide reference images: guitar/bass/amp anatomy sections
  still need photos.
- Bret Pimentel SVG woodwind diagrams: bassoon/contrabassoon done.
  Remaining exports need donor authorization plus desktop work.
- Real drum samples: the current drum engine is synthesized. Pure
  synthesis cannot match acoustic drums (structural limit). Apps that
  sound acoustic use samples. Intonare's synthesis aims at electronic
  timbres by design.
- Cloud save / optional account: deliberate v1.1 feature. Local stays
  canonical, cloud is a mirror.
- Auto-start tuner mic on Android: post-launch. It races the
  MainActivity RECORD_AUDIO grant.
- iOS native mic plugin: Swift, from scratch. The Android-only Java
  plugin gives iOS nothing. Currently iOS uses WebView mic only.
- Melody Dictation and Score Reader: deferred WIP. Coming Soon cards
  were removed pre-launch but the features are not cancelled.
- Groove audit: 60 grooves, 57/60 vetted. Three are CEILING REACHED
  (montuno, samba tamborim, New Orleans). Ciftetelli is a guess.
  On-device listen list still outstanding.


## Build pipeline

The go.bat file in the repo root handles the full deploy:

1. Verify Intonare.html is in the project folder
2. git add, commit, push (updates GitHub Pages)
3. Copy to www/ for Capacitor
4. npm install, Vite build (main.iife.js haptics bridge), cap sync
5. Restore native files from native_src/ (AndroidManifest, Java
   plugins, styles, colors, icons, audio samples, splash sound)
6. Gradle clean if native sources changed

After go.bat completes, open Android Studio and hit Run. Clear cache
on the phone after install. The script does NOT build the APK.

For iOS: start a Codemagic build manually (auto-trigger is OFF).
Push alone does not build an IPA. Top CHANGELOG version must match
INTONARE_VERSION or the build fails.

## Claude tooling (imported Sep 2026)

High-value audits live under `tools/` (see `tools/README.md`). Python 3.12
is installed. Daily ship gate: `tools\ship_check.bat` (sentinel + changelog).
Do not treat the old August inventory as current for every script; area
audits are on-demand. Daily edit safety still uses `.cursor/rules` preflight.



## How Daniele works

- Direct, dry communication. Swearing is fine. No em-dashes (use
  semicolons). Short by default; longer only for analysis, decisions,
  or risk flagging.
- Feedback is perceptual: "too electronic," "jittery," "almost
  imperceptible but premium." Translate perception into parameters.
- Prototype-first for visual/audio changes: build a standalone HTML
  mockup and review on-device before touching the main file.
- On-device screenshots are the reliable verification. Headless
  renders miss real-device behavior.
- Triage style: fix everything in a session, audit at the end. Don't
  stop for confirmation mid-run unless a decision is actually needed.
- Engineering standard: professional team, not a garage. Correct over
  quick, with a working stopgap while the real fix is built.
- Read before touching: trace bugs fully before writing code. Never
  ship blind on performance or quality-tradeoff work.
- Any audit of the app must be a real read of the actual content, not
  a regex count presented as a finding.


## Recurring bug classes

These have bitten before. Keep them in mind.

- The `t` variable shadowing: forEach loop variables or function
  parameters named `t` conflict with the global `t()` translation
  function. Name loop vars `tone`, `trk`, `tick`, `mode`, etc.
- CSS brace balance: stray braces silently break large CSS sections.
  Maintain zero diff on brace count.
- Web Audio scheduler: parameter changes during playback require a
  bus-swap pattern (fade old buses, create fresh ones, reset
  scheduler), not just gain muting.
- Capacitor sync: `npx cap sync` alone doesn't reliably update assets.
  go.bat uses manual `copy /Y` commands for this reason. Cache must be
  cleared on device after each Android Studio run.
- Dead code purge: static analysis can't see onclick, querySelector,
  or IIFE invocations. A function that looks uncalled might be called
  from a string or an event attribute. Always do a full-file sweep
  before deleting anything.
- Tone bank skins: `.piano-overlay-voice-btn` defaults to piano
  console black; non-piano surfaces must explicitly opt out.
  `buildChordToneBank` defaults to `chd-tonepop`; pass a skin
  explicitly. `closeTonePopup()` must strip every skin class. New
  skins use theme vars only, never hardcoded hex.
- DOTALL regex: never run one on a ~12MB file. Use str.replace with
  an exact unique match instead.
- Giant-file truncate hangup: editor/tools can report success while
  `Intonare.html` silently shrinks (~12MB → ~8MB). Always re-check
  byte size and trailing `</html>` after every edit. If collapsed:
  stop, `git checkout -- Intonare.html`, re-apply with a unique exact
  replace (prefer a short Python patch under `tools/`; avoid PowerShell
  inline Python). Full rules in `.cursor/rules/intonare.mdc`.


## IP and licensing

- No triforce imagery (use triangle-with-sword). "Chiptune" not
  "Gameboy." All Zelda-derived audio was replaced with original
  compositions.
- Images require Wikimedia Commons with explicit CC BY or CC BY-SA.
  Google Images is not acceptable.
- Composition copyright applies regardless of synthesis method or
  instrumentation. All audio cues are original.
- Third-party licenses are listed in the License file and the app's
  Credits screen.
