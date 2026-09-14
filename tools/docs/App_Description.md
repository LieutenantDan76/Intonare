# Intonare — App Description

## ⚠️ CLAUDE WORKING FILE RULE — READ THIS FIRST

**Always use the uploaded `Intonare.html` from the conversation as the working base.
Never use `/mnt/project/Intonare.html` as a starting point — it may be behind.**

Correct workflow every session:
1. User uploads `Intonare.html` at the start of the conversation
2. `cp /mnt/user-data/uploads/Intonare.html /home/claude/Intonare.html`
3. Apply all fixes to `/home/claude/Intonare.html`
4. Output to `/mnt/user-data/outputs/Intonare.html`

If no file is uploaded at session start, **ask for one** before doing any work.

The audit scripts at `/mnt/project/intonare_i18n_audit.py` and `/mnt/project/intonare_teaching_audit.py` are fine to use directly — they don't change often and are safe to pull from project files.

---

## Project File
`Intonare.html` — single-file HTML/CSS/JS web app (~42,000+ lines). Mobile-first, PWA-ready. No build system — everything inline. Always work from the uploaded `Intonare.html`; it is the source of truth and contains all current fixes.

---

## Architecture

**4 modes** (tab-switched, each with its own theme color):
- **Tuner** (cyan) — chromatic pitch detection via mic, cents meter, chroma strip, note/octave display, instrument presets, ref tone playback, strobe meter, vibrato meter, pitch history graph, teaching mode, guided tour
- **Tools** (green) — sub-hub with folders: Piano, Tonal Center (drone + scale), Chord Reference, Circle of Fifths, Guitar Scale Fretboard, Guitar Chord Library, Volume/dB meter, Transposer, Vocal Range assessment, Charts/Reference tool, Survival Guide (textbook-style instrument reference — full coverage across bass, uke, mandolin/banjo/harp, bowed strings, woodwinds, brass, free-reed, voice; interactive photos, note-player buttons, playable range charts, tappable audio demo terms, floating "← Back to Guide" pill that restores exact position)
- **Metro** (yellow/amber) — metronome with groove mode (16-step pattern sequencer with preset library), tap tempo, custom time signature picker, subdivision, swing, beat flash overlay, pulse dots, haptic feedback, integrated drum kit sequencer
- **Train** (purple) — practice hub with ear training (intervals, chords, sight singing), rhythm exercises (tempo lock, tempo guess, polyrhythm), scales

**Tech:**
- Fonts: Bebas Neue, Fraunces, JetBrains Mono
- CSS `@property` registered custom properties for smooth theme crossfades
- Web Audio API for all sound
- `localStorage` for settings persistence
- Bilingual: English + Italian (`applyLang()` / `t()` i18n system)
- Haptics via `@capacitor/haptics` — fully native, working on Android
- Audio cues via Web Audio API — synthesized sounds paired with haptic events

---

## ⚠️ Ground Rules for All Sessions

1. **Always work from the uploaded `Intonare.html`** — never from memory, never from `/mnt/project/Intonare.html`. It may be behind.
2. **Never regress existing behavior.** Before changing anything, check the surrounding code for context.
3. **Carry all changes forward** — always output a complete updated `Intonare.html`, not a diff or patch.
4. **Save output as `Intonare.html`** every session so the next session has a clean starting point.
5. **Always upload `Intonare.html` directly in chat** — not via project files. Project files update separately and may lag behind.
6. **Syntax-check after every change.** Run `node --check` (or equivalent parse) on the output before declaring done. A file this size hides syntax errors expensively. Watch especially for unescaped apostrophes in JS strings and copy-paste typos in render switches (the legendary `break;reak;`).

---

## Adding a New Instrument — 12-Point Registration Checklist

Adding an instrument means hitting **every** one of these touch points. Missing one = silent breakage (blank render or wrong/no audio). Walk this list before debugging anything fancier:

1. `CS_INSTRUMENTS`
2. Picker
3. `gccGetOpenMidi`
4. String names
5. MIDI values
6. `capoApplies`
7. Voicings
8. Unavailable qualities
9. Inlay markers
10. `getFrettedTone`
11. `REF_TONES`
12. `stopAllAudio`

**Instruments added so far beyond the originals:** 5-string banjo (full voicing generator, `banjoSynth` with pitch-warp attack + roll playback engine with 7 patterns), mandocello, uke bass, baritone guitar, tenor guitar, mandola.

**Family sub-tab groupings** in the Charts tool: Uke Bass under Uke, Mandola/Mandocello under Mandolin, Baritone/Tenor Guitar under Guitar.

## Hard-Won Rules (each one is a scar — don't undo)

- **Single-mechanism capo.** Capo is applied in exactly ONE place: `gccVoicings()` does the root-shift before all lookups; audio adds the capo offset explicitly. Never add a second mechanism (shifting open MIDI *and* root-shifting in lookup) — that double-counts. One place, before branching, forever.
- **Sub-oscillators are a trap.** Two independent oscillators at the same frequency drift in phase and cause a beating buzz. Don't add one for low end — use a `PeriodicWave` with a strong fundamental coefficient.
- **Verify functions exist before shipping.** Ghost references (`ukeBassVoicings`, mandolin-family constants never defined) have bitten before. Grep for every called function/constant; don't assume.
- **Cache key collisions.** Instruments in the same family sharing a voicing cache need **distinct prefixes**, or one stomps another.
- **`gccInit` resets state.** Init hard-resets state. Restore logic must run AFTER init, or use a `keepState` flag, or init quietly stomps the restore.
- **Scale note collection: clamp the top.** Clamp to `midi <= hiRoot` when collecting scale notes, or compressed-range instruments bleed into a second octave.
- **Envelope shaping must be organic.** Jarring dynamic demo terms (sfz, fp, subito) need exponential curves (`setTargetAtTime` / exponential ramps), not abrupt gain jumps.
- **DOM insertion depth + ID-prefix matching.** Panels nested in the wrong container render blank; CSS scoping with a mismatched ID prefix silently breaks everything. Check that insertion point and ID prefix line up. (See also the `settingsModal` note below.)

## Saved Chart Views

Slide-up confirmation bar, smart auto-generated names, loose restore logic, dedup with toast notifications, amber-tinted tiles in Quick Access. Sub-tabs must appear on cold open — they didn't once, due to init ordering.

---

## Current Design Decisions (don't undo these)

- **tsBottom** (time signature denominator) is display-only — it does not affect playback or auto-switch subdivisions. Reserved for future notation generation.
- **Vibrato meter** uses a two-stage chained hold: dim after a short gap, clear after a longer one. The timers must be nested (clear starts inside dim's callback), not parallel.
- **Hub icons** are uniform 30px across folders and modules — no size distinction.
- **Drumkit back button** uses the standard `train-back` class, not the old `dk-back-btn`.
- **BPM cap** is 300 (not 240). Time signature top goes up to 24.
- **Language flags** use inline SVG (not emoji) — Capacitor WebView on Android cannot render regional indicator emoji sequences (🇬🇧 shows as "GB"). Do not revert to emoji flags.

### Header State Machine (3 levels — do not flatten or simplify)

The app header has three distinct states controlled by `setHeaderModule()` and `setHeaderSection()`:

1. **INTONARE** — tuner/metro tabs. Logo = "INTONARE", tagline = "suona in sintonia · play in tune". No back button. No header class.
2. **Section** — tab hubs and folders (TOOLS, TRAIN, EAR TRAINING, PITCH & SOUND, etc.). Logo = section name, subtitle from `_subs` map inside `setHeaderSection`. Optional back button via `body.in-section-back` class. Header gets `header--section` class.
3. **Module** — specific tool or exercise. Logo = module name, subtitle from `TOOL_SUBS` / `EXERCISE_SUBS`. Back button always shown. Header gets `header--module` class. Body gets `in-module` class.

**Key rules:**
- `in-section-back` and `header--section/module` class changes happen INSIDE the 60ms timeout (while fading) — never synchronously, or the back button snaps visibly.
- `in-module` body class is added synchronously before the fade so teach-hint hiding takes effect immediately.
- `_pendingHeaderTimeout` + `clearTimeout` prevents stale updates on fast navigation.
- `_headerBackFn` is set before the fade so `headerBack()` works if tapped mid-transition.

**Font size buckets** (applied via `logo.dataset.len`):
- Short (≤8 chars): 32px, nowrap — set by `.header--module #appLogo` / `.header--section #appLogo` base rules
- Medium (9–13): 20px, white-space: normal, line-height: 1.1, overflow: visible
- Long (≥14): 18px, same as medium

**Subtitle alignment:** Both `.header--module #headerSub` and `body.in-section-back #headerSub` get `padding-left: 24px` to align subtitle under the title (past the back button).

**Module name maps** live in `TOOL_NAMES`, `TOOL_SUBS`, `EXERCISE_NAMES`, `EXERCISE_SUBS` near the bottom of the script. They match the card titles shown in the hub views exactly — don't rename independently.

### CSS Transition Architecture (do not revert)

**Theme color transitions** use `@property`-registered CSS custom variables on `body`:
```css
body { transition: --theme 0.06s ease, --surface 0.06s ease, --bg-0 0.06s ease, ... }
```
Since all vars have `inherits: true`, every descendant reads the interpolated value each frame. No class toggling, no reflow tricks.

**Global transition sync rule** — required to prevent color flickering/jitter:
```css
*, *::before, *::after {
  transition: background 0.06s ease, background-color 0.06s ease,
              border-color 0.06s ease, color 0.06s ease, fill 0.06s ease,
              box-shadow 0.2s ease, transform 0.2s ease,
              opacity 0.2s ease, filter 0.2s ease !important;
}
```
**Why this exists:** buttons have `transition: all 0.2s` which catches CSS-variable-induced color changes and animates them at 0.2s while the body `@property` transition finishes at 0.06s — the background snaps fast while buttons slowly catch up, causing visible jitter. This rule forces all color properties to 0.06s globally so everything is synchronized. `box-shadow` and `transform` stay at 0.2s for hover feel. The `!important` is required to beat existing `transition: all` rules.

**`#logoArea` and `#headerSub` are exempt** via their own `!important` rules for the header fade animation — don't remove those.

**`body::before` has no `transition` rule on it** — it inherits `--theme` from body via `@property inherits:true`. Adding a separate `transition: background` on `body::before` will cause it to animate at a different speed than the body vars, creating visible desync. Don't add one.

#### Full history of what was tried and failed (don't repeat these):

**`theme-changing` CSS class approach (abandoned):**
Adding a `theme-changing` class to body and changing the theme class in the same JS tick → browser batches both into one style recalculation → no "before" state to diff against → transitions never fire → colors snap. Adding `void document.body.offsetHeight` between the two changes forces a reflow and makes transitions fire, but then having both `--surface` AND `background` in `transition-property` simultaneously creates a double-animation where both compete at different speeds → flicker. Tried many times in different forms. Abandoned entirely.

**`transition-property: background, --surface` conflict:**
When a CSS custom property (`--surface`) transitions on body AND an element also has `background` in its `transition-property`, the browser fires two competing animations on the same visual output at different rates. The element's own `transition: background 0.2s` beats the 0.06s var transition and wins at 0.2s speed → buttons lag behind. The global `*` sync rule (above) is the fix.

**View Transitions API (tried, rejected for header fade):**
`document.startViewTransition()` hides the real DOM and composites pseudo-elements over the browser's default white canvas. The `::view-transition` pseudo-element can't read `body`-scoped CSS variables for its background color → full-page white flash on every navigation. `mix-blend-mode: normal` on root pseudo-elements doesn't fix it. Do not attempt again.

**Header fade** uses 0.15s `ease-out` opacity transition with a 60ms swap timeout. The swap fires before the fade-out completes (~33% opacity remaining at 60ms), so CSS starts the fade-in from 33% opacity rather than 0% — old fades halfway out, new fades in from halfway, creating a dissolve overlap without needing two DOM elements. The `ease-out` curve is important: it front-loads the fade so the element is visually dim quickly (drops to ~33% in 60ms of a 150ms curve).

---

### Additional Structural Notes

**`settingsModal` must be a direct child of `body` (or at least outside `progressModal`):**
A missing `</div>` closing tag on `progressModal` previously caused `settingsModal` to be nested 6 levels deep inside a hidden element, rendering it at 0×0. The fix is in the HTML — `progressModal`'s closing tag must come before `settingsModal` opens. There's also a DOMContentLoaded re-attachment that moves all modals to body root as a safety net.

**`#headerBackBtn` has `align-self: center`** explicitly set. Do not remove it — some module contexts create layout situations where the parent's `align-items: center` alone isn't reliable.

**All header subtitles use `var(--text-dim)`** — uniform brightness. There was previously an override in `.header--module #headerTagline { color: var(--muted) }` which made module subtitles dimmer than section subtitles. It has been removed. Do not re-add it.

**Module name maps — canonical names (match card titles exactly):**
```
TOOL_NAMES:     piano→PIANO, tonal→TONAL CENTER, chords→CHORDS,
                guitarchords→CHARTS, progression→PROGRESSION, drumkit→DRUMKIT,
                cof→CIRCLE OF FIFTHS, volume→VOLUME METER, transpose→TRANSPOSER,
                vocalrange→VOCAL RANGE
EXERCISE_NAMES: interval→INTERVAL, chords→CHORDS, singsing→SIGHT SINGING,
                scales→SCALES, tempo→TEMPO LOCK, tempoguess→TEMPO GUESS,
                poly→POLYRHYTHM, chordle→CHORDLE
```

---

## Native App Infrastructure (Capacitor + Vite)

Intonare runs as a native Android app via **Capacitor**. The repo lives at `https://github.com/LieutenantDan76/Intonare.git` on the developer's Windows machine at `C:\Users\citti\Desktop\Intonare\`.

### Repo Structure
```
Intonare/
├── Intonare.html          ← the app — always the source of truth
├── index.html           ← 5-line redirect for GitHub Pages (do not delete)
├── main.js              ← Capacitor plugin imports, exposed to window globals
├── vite.config.js       ← Vite config, builds main.js → www/main.iife.js (lib/iife mode)
├── capacitor.config.json
├── package.json
├── manifest.json        ← PWA manifest
├── sw.js                ← PWA service worker
├── go.bat              ← one-command full deploy (Downloads → GitHub → Capacitor → Android assets)
├── .gitignore           ← excludes node_modules/, android/, www/
├── android/             ← generated Capacitor Android project (not in git)
├── www/                 ← Vite build output (not in git)
│   ├── index.html       ← copy of Intonare.html (generated by go.bat)
│   └── main.iife.js     ← built Capacitor plugin bundle
└── node_modules/        ← npm packages (not in git)
```

### Haptics Implementation
Search `// ─── HAPTICS ───` in `Intonare.html`. Uses `@capacitor/haptics` via `window` globals injected by `main.js`:
- `window.Haptics` — the Haptics plugin
- `window.ImpactStyle` — Light / Medium / Heavy
- `window.NotificationType` — Success / Warning / Error (currently unused, all haptics use impact())

**Do not revert to `navigator.vibrate`** — Samsung One UI 7 blocks it for web content entirely.

All haptic functions use `async/await` with silent `try/catch` so PWA doesn't break:

```javascript
// In-tune ping — double Light tap
async function hapticSuccess() { ... Light → 30ms → Light }

// Correct answer — quick da-Dink
async function hapticCorrect() { ... Light → 30ms → Medium }

// Wrong answer — slow BZZ...BZZ
async function hapticWrong() { ... Heavy → 150ms → Heavy }

// Level up — fireworks cascade
async function hapticLevelUp() { ... Heavy → 100ms → Light → 50ms → Light → 120ms → Heavy → 100ms → Medium → 60ms → Light → 40ms → Light }

// Streak milestone — ceremonial build
async function hapticMilestone() { ... Light → 120ms → Medium → 120ms → Heavy → 120ms → Heavy }

// Beat (metronome) — pocket mode bumps up when audio is muted
async function hapticBeat(isAccent) {
  // if !metroAudioOn: accent=Heavy, regular=Medium
  // if metroAudioOn:  accent=Heavy, regular=Light
}
```

**Haptic call sites** — these events fire haptics (and paired audio cues where noted):
- Metro beat → `hapticBeat(isAccent)`
- Mic toggle → `hapticSelect()`
- Note in tune → `hapticSuccess()`
- Piano key tap → `hapticLight()`
- Piano octave shift → `hapticMedium()`
- BPM nudge +/− → `hapticLight()`
- Drone toggle → `hapticSelect()`
- Circle of Fifths tap → `hapticLight()`
- Transposer key select → `hapticLight()`
- Tempo lock tap → `hapticLight()`
- Correct answer (all exercises) → `hapticCorrect()` + `playCueCorrect()`
- Wrong answer → `hapticWrong()` + `playCueWrong()`
- Streak milestone → `hapticMilestone()` + `playCueMilestone()`
- Level up → `hapticLevelUp()` + `playCueLevelUp()`
- Settings haptics toggle ON → `hapticSuccess()` (test pulse)
- Vocal range step locked → `hapticSuccess()`
- Vocal range save → `hapticSuccess()`

**Intentionally removed haptics** (too noisy): guitar tool navigation arrows, slider collapse toggles, chord zoom open/navigate, play/strum buttons, mode switches between chords/scales, progression chord add/delete.

---

## Audio Cues System

Search `// ─── AUDIO CUES ───` in `Intonare.html`.

### Critical rule: always use `getAudio()` — never create a separate AudioContext
The shared `_sharedAudio` context is already unlocked by user interaction. A new `AudioContext` will be blocked by Capacitor WebView and produce silence. All cue functions must call `getAudio()` and `buildLimiterChain()`.

### Key infrastructure functions:
- `_cueNote(freq, type, when, dur, vol)` — single oscillator note through limiter chain
- `_cueSweep(freqStart, freqEnd, type, when, dur, vol)` — pitch-ramped oscillator through limiter chain
- `playCueCorrect()`, `playCueWrong()`, `playCueMilestone()`, `playCueLevelUp()` — dispatchers that read `progState.audioCues` and call the right named function
- `setCueChoice(event, key)` — saves choice to `progState.audioCues`, re-renders UI, previews sound+haptic
- `renderCueDropdowns()` — renders the 2×2 grid picker in settings; called from `openSettings()`

### Sound library (21 sounds + silent options):

**Correct** (default: chime): chime · blip · piano · marimba · harp pluck · silent

**Wrong** (default: buzz): buzz · thud · clunk · trombone · glass knock · silent

**Milestone** (default: fanfare): fanfare · coin shimmer · brass stab · bell chord · drum roll · silent

**Level Up** (default: gameboy): gameboy · orchestral · chime swell · power up · harp cascade · treasure! · silent

### User preferences stored in `progState.audioCues`:
```javascript
audioCues: { correct:'chime', wrong:'buzz', milestone:'fanfare', levelup:'gameboy' }
```

### Settings UI:
2×2 grid of cards in settings under "Audio Cues". Tapping a card cycles through options and previews the sound + haptic. Rendered by `renderCueDropdowns()` which is called from `openSettings()`.

### Notable sound implementations (don't simplify these):

**Drum Roll** (`_cueMilestoneDrumroll`):
- Each `hit()` call fires `singleHit()` 10 times with staggered timing (0-28ms offsets), pitch variation (±8% freqMult), and volume taper — creates "whole drum section in unison" effect
- Pre-roll: two bandpass layers (300Hz Q=2.5 and 600Hz Q=3.0) building over 220ms, bleeds into first hit
- Pattern: SHHHUH (220ms pre-roll) → TA (0.22s) TA (0.37s) TA (0.52s) ... pause ... TA! (0.74s) + bass boom

**Treasure!** (`_cueLevelUpZelda`):
- F major 2nd inversion: C F A ratios (1 : 4/3 : 5/3) from bass note
- Bass on C5 (523.25Hz), chromatic ascent: C5→C#5→D5→D#5 (held)
- Pure square waves (8-bit sound)
- Three staccato stabs (0.00, 0.16, 0.32s) then held chord at 0.50s
- Shimmer sine overtones on final chord, fade over ~700ms

**Trombone Wah** (`_cueWrongTrombone`):
- Each slide goes UP briefly first then DOWN (cartoon arc, not just descending)
- Two detuned oscillators per slide (0 and +12 cents) for thickness
- Two slides: first WOM (A3→up→low), second WOMP (lower start, even lower end)

**Marimba** (`_cueCorrectMarimba`):
- Double strike: C5 first, then E5 at +180ms (game show bell bounce)
- Inharmonic partials at 3.78× (click transient) for woody mallet character

**Drum Roll pre-roll audio chain** — uses two separate `buildLimiterChain` instances and `createBufferSource` from a single pre-generated noise buffer. Both sources play from the same buffer simultaneously through different filters.

---

## Developer Workflow

### Full deploy process (every update):
1. Save new `Intonare.html` to Downloads
2. Run `go.bat` — single unified script, handles the whole chain (see below)
3. Hit **Run** in Android Studio
4. On phone: Settings → Apps → Intonare → Storage → **Clear Cache + Clear Data**

`go.bat` replaced the old `push.bat` + `sync.bat` pair. There is **no `npm run build` / Vite step** in the current pipeline — `go.bat` does `npm install` + `npx cap sync`, not a build. (If `vite.config.js` / `main.iife.js` still exist in the repo, they are vestigial to this workflow.)

### go.bat — what it does, in order:
1. Copy latest `Intonare.html` from `C:\Users\citti\Downloads\` (aborts if not found)
2. `git add -A` + commit + push to GitHub
3. Copy `Intonare.html` → `www\index.html`
4. `npm install` + `npx cap sync`
5. **Restore files cap sync overwrites** (see below)
6. Copy `www\index.html` → `android\app\src\main\assets\public\index.html` + verify with `findstr`

### ⚠️ Capacitor sync overwrites generated files — go.bat restores them:
`npx cap sync` (and `cap add android`) stomp generated Android files back to defaults. `go.bat` has a restore block re-copying:
- `AndroidManifest.xml`
- `MainActivity.java`
- `styles.xml`, `colors.xml`
- app icons (`icon_res` → res via `xcopy`)
- **`build.gradle` proguard patch**: rewrites `proguard-android.txt` → `proguard-android-optimize.txt` (required by current AGP — the non-optimizing file is no longer supported). PowerShell in-place replace, safe to run every time since it won't match an already-patched line.

If you regenerate the Android project, re-verify this restore block still covers everything that needs it.

### ⚠️ Critical: android assets often don't sync automatically
`npx cap sync` alone does NOT reliably update `android\app\src\main\assets\public\index.html`. The manual `copy /Y` step at the end of `go.bat` is essential. Always verify with:
```bash
findstr "some_unique_string" android\app\src\main\assets\public\index.html
```

### Android rebuild after an appId change:
`rmdir /S /Q android` → `npx cap add android` → `go.bat`. The old app must be **manually uninstalled** from the device since the `appId` changed (`com.lieutenantdan.intonare`).

### Adding new Capacitor plugins:
1. `npm install @capacitor/plugin-name`
2. Add import + `window.X = X` exposure to `main.js`
3. Run `go.bat`
4. Run in Android Studio + clear cache on phone

---

## What Still Needs Capacitor (not yet implemented)
- **Splash sound** — Web Audio autoplay policy blocks sound on page load in PWA/browser. Capacitor fixes this — native audio plays on app open without a user gesture. Pending.
- **iOS haptics** — not tested; needs Xcode + Apple Developer account.
- **Play Store submission** — pending when feature-complete. Will need Capgo for live OTA updates.

## Easter Egg Ideas (not yet implemented)
- **"Secret Found"** — Zelda secret discovered stinger, to be hidden somewhere in the app.

## GitHub Pages (PWA)
Still live at `https://lieutenantdan76.github.io/Intonare/` via GitHub Pages. Root `index.html` redirects to `Intonare.html`. Haptics silently fail in PWA (expected — Samsung One UI 7 blocks navigator.vibrate). Audio cues work fine in PWA since they're triggered by user interaction.
