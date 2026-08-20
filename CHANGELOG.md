# Intonare — Changelog

A human-readable record of what changed, when,

---

## OPEN ITEMS (as of v0.150.72)

**Device state: v0.150.65 is built and running.** Only .66 to .72 are untested,
which is the update card being tappable, the download size readout, and the
backup work. Everything else — the Italian sweep, the 60 help translations, chord
quality names, solfège on the bowed charts, the relabel registry — shipped at or
before .65 and has been in use.

**Backup is the one that matters.** The round trip (back up, restore, Reset All
Progress, confirm Pro and settings survive) has still never been run end to end.
It is the only remaining bug class that costs someone their data rather than
annoying them.

**Tooling to re-upload to project knowledge**, none of which survives a session:
`intonare_regression_sentinel.py` (247 pins), `intonare_i18n_audit.py` (seven
categories, A/E/F/G are the unambiguous ones) and `intonare_lang_sweep.py`
(drives a browser through 35 screens and reports only strings identical in both
languages).

**Deferred with measurements, so they can be picked up cold:**
- First module open compiles the module-building JS. Repeated reloads go smooth
  because of V8's bytecode cache. Needs the file split; v1.1.
- `setLang` leaks ~2,679 DOM nodes over 20 language switches, in the legacy
  builder list rather than the relabel registry. Fix is migrating those calls
  into `registerRelabel`, which puts them behind its leak check.
- Relative Pitch tone overlap. Two attempts tracked the delayed-tone timers in
  both the climb and practice mode; it still overlaps, so a second voice comes
  from somewhere not yet found. Needs a trace, not another guess.
- Drum samples: all five kits sourceable under CC0 (Versilian Virtuosity for
  standard/jazz/brushes/latin, tidalcycles/sounds-tr808-fischer for electronic).
  ~70 samples, ~2MB, lives in assets rather than the HTML. All five or none.

---

## OPEN ITEMS (superseded — as of v0.150.42)

Not a release entry. A standing list so these survive outside anyone's memory.

**Road Trip leg tuning: DONE.** All 39 legs are tuned and signed off; `RT_TUNED`
holds 21 entries, which is every perf leg, and no leg still carries the
converter's default hook spacing. Completed across v0.150.18 to v0.150.27. The
earlier version of this section said 21 songs still needed tuning and that
`RT_TUNED` was empty; that has not been true since v0.150.27.

**Housekeeping — audit scripts must be re-uploaded to project knowledge.**
`/mnt/project/` does not persist edits made during a session. The regression
sentinel has been changed several times since (Relative Pitch band-change pin,
plus pins for the six legs tuned in v0.150.21) and now holds 247 pins. If the
copy in project knowledge is not replaced, a fresh session runs an older sentinel
and either misses pins or reports drift on values that are correct.
`intonare_groove_audit.py` has the same problem and has already had to be rebuilt
from scratch once for exactly this reason.

**Relative Pitch tone overlap.** Parked, not fixed. The delayed question tone is
tracked and cancelled in both the climb and practice mode, and tones still
overlap on rapid next, so a second voice comes from somewhere not yet found.
Needs a trace rather than another guess.

**Charts Italian sweep.** Instrument picker (39 strings) and piano console done.
A few interval-reference labels remain, several of which are JS-filled
placeholders rather than static text and so cannot simply be tagged.

**On-device listening, from the v0.102.x groove work — LARGELY SETTLED.**
`intonare_groove_audit.py` now vets 57 of 60 grooves and the patterns are pinned
in the sentinel, so the "did this silently revert" worry is handled. The list
below is kept because the musical judgements in it are still open questions, not
because the code is unverified.


- JOROPO — accents moved so the three-against-two hemiola is audible. Should read
  as a cross-rhythm, not as lopsided.
- TUMBAO — new preset, two strokes, empty downbeat. Suspended or broken?
- AFROBEAT — Tony Allen's first pattern. Nothing lands on any of the four beats.
  The extreme version of the same question.
- JAZZ SWING — was genuinely broken and never struck beat 2. Should now sound like
  a swing ride.
- BOOM BAP — had no bap. Now has one.
- SHIKO, SOUKOUS, GAHU — will sound close to son clave. That is correct; the six
  distinguished timelines differ from each other by one or two sixteenths.
- ÇİFTETELLİ — the one place three sources disagreed and a choice was made. Most
  likely of any entry to be wrong.
- BULERÍA — should now open on an accent where Soleá does not. That is the audible
  difference between the pair.

Everything else in v0.102.x was citations only and will not sound different.

**Three grooves are finished in the sense of "as good as desk research gets"**

Montuno's piano guajeo, Samba's tamborim, and New Orleans. Each carries a CEILING
REACHED note naming what would settle it: a Cuban piano method, a bateria chart,
or Antoon Aukes' "Second Line: 100 Years of New Orleans Drumming" — failing those,
a player. Bhangra is technically sourced but sits on the wrong grid for a triplet
feel and its sources contradict each other on accents.

---

---

---

---

---

---

---

---

---

## v0.150.72 — A partial backup has to say it is partial

v0.150.71 recorded skipped fields inside the file and said nothing on screen.
That was the wrong call, and it was pointed out immediately: someone would
believe they had a complete backup and discover otherwise at restore time, which
is the one moment they cannot afford it. Quiet data loss is worse than loud
failure.

Both ends now speak up:

- **On export**, if anything was dropped the toast says so and calls it a bug
  rather than a normal outcome.
- **On restore**, an incomplete file warns BEFORE it is applied. The export
  warning is not enough on its own — the file may have been made months ago on
  another device by someone who never saw it. Restore is where the gap costs
  something, so restore mentions it.

Worth being clear about why anything would ever be skipped: **nothing should be.**
`JSON.stringify` throws on exactly two things, a circular reference and a BigInt,
and neither occurs through normal use. Both mean the app wrote something
malformed into saved state. So a skipped field is an alarm, not a footnote, and
the wording says so instead of hiding behind "some items".

With dev tools unlocked both messages name the fields outright.

## v0.150.71 — One bad field can no longer take the whole backup down

`backupBuild()` did `JSON.parse(JSON.stringify(prog))` in a single shot, so one
unserialisable value threw and the caller reported total failure. Someone with
years of progress got NOTHING because of one bad field. Losing a setting is
survivable; losing the backup is not.

Each field is now serialised on its own. Anything that throws is skipped, logged,
and listed in a `skipped` array that travels inside the backup file, so the file
explains itself rather than leaving a support conversation to guesswork.

Tested by poisoning `progState.stats` with a circular reference: the old path
threw, the new one produces a backup with 36 of 37 fields and
`skipped: ["stats"]`.

Restore ignores the field, so an older build reading a newer file is unaffected.

Static analysis of the live app could not find the offending value — nothing in
progState holds a DOM node, an audio node or a self-reference, and a clean state
serialises fine. So the failure depends on real saved data. This change means
that no longer matters: whatever it is, the backup now completes and names it.

## v0.150.70 — The backup error was never about the plugin

Chased this properly instead of waiting on a build.

**Verified the native side against the real Capacitor 8 source**, pulled from the
npm tarball: the `String` overload of `startActivityForResult` exists,
`@ActivityCallback` registers launchers by method NAME, and the invoker calls
`setAccessible(true)` so a private callback is fine. `FileSaverPlugin.java` is
correct as written.

**And the plugin must be installed anyway.** `MainActivity.java` references
`FileSaverPlugin.class` directly, so if that class were missing the build would
FAIL rather than quietly succeed. A successful build means it is registered.

**The real culprit is the first three lines of `backupExport()`:**

```js
try { txt = JSON.stringify(backupBuild(), null, 2); }
catch (e) { svcToast(t('backup_err_writefail')); return; }
```

That catch fires BEFORE any plugin is touched, and it was showing
`backup_err_writefail` — restore wording about running out of disk space. So a
failure to BUILD the backup object presented as a storage problem, which sent us
looking at free space and native plugins for something neither had caused.

`backupBuild()` runs clean here — 6 keys, 2.6KB — so the failure is
data-dependent: something in a real saved state that will not serialise, most
likely a circular reference or a value that became undefined.

All three failure paths now say different things, so the next build names the
culprit rather than pointing at the phone:
- **build failed** — the object could not be created (a bug, and it says so)
- **FileSaver rejected** — falls back to sharing, and logs why
- **share failed** — its own message, no disk-space claim

With dev tools unlocked each one shows the underlying exception text.

## v0.150.69 — Make the plugin tell us why it refused

The FileSaver rejection was being swallowed, so a build where the save dialog
never appears looks identical to one where it failed for an unrelated reason.
The message is now logged always, and shown on screen when dev tools are
unlocked.

It distinguishes two cases that need opposite fixes:

- **"not implemented on android"** or **"does not have web implementation"** —
  the plugin is not in the APK. Either the .java never landed in
  `android/app/src/main/java/com/lieutenantdan/intonare/`, its `package` line
  does not match that path, or the build reused a cached APK.
- **anything else** (ActivityNotFoundException, an IO error, a permission
  refusal) — the plugin IS there and the save itself failed, which is a
  different problem entirely.

Normal users are unaffected: they still just get the share sheet.

## v0.150.68 — Backup reported a disk-space failure on a phone with 30GB free

Two of my own bugs stacked, both introduced in v0.150.52.

**The fallback stopped falling back.** `Capacitor.registerPlugin()` returns a
proxy whether or not the native plugin exists — it only rejects when you CALL it.
So adding that fallback silently broke the "plugin missing, use the share sheet"
check: the FileSaver path is now ALWAYS taken, and a build without
FileSaver.java installed reached the catch and reported failure instead of
sharing. The catch now calls the share path rather than giving up, so a missing
plugin degrades exactly as it did before.

**And it reported the wrong failure.** The catch used `backup_err_writefail`,
which is RESTORE wording about running out of space. Telling someone with 30GB
free to clear room, for a backup that failed because a plugin was not installed,
is wrong twice in one sentence. Backup now has its own message, and it describes
what actually happened.

The share tiers are split into `_backupShareFallback()` so both entry points use
one path instead of the FileSaver branch having nowhere to go.

Worth remembering about Capacitor: a registered plugin proxy is never falsy.
Feature-detecting one by truthiness always passes. The only way to know it is
really there is to call it and handle the rejection.

## v0.150.67 — Download size on the update card

Play hands over `bytesDownloaded` and `totalBytesToDownload` with every progress
event, so showing them costs nothing. The subtitle now reads "12.4 / 40 MB" while
downloading.

Worth having: on a slow connection a bar that moves a pixel a second is hard to
tell apart from a bar that has stopped. A number that keeps climbing is not.

MB rather than MiB (dividing by 1,000,000, not 1,048,576) because that is what
the Play listing quotes, and the two disagreeing by 5% reads as a bug rather than
a unit convention. One decimal below 10MB, whole numbers above, so it does not
jitter through four digits as it climbs.

Confirmed while checking: every string on this card already had an Italian twin —
available, downloading, ready, restart and retry. The card did not escape the
translation work, only the pointer-events bug.

## v0.150.66 — The update card could not be tapped

It sits inside `#achToastStack`, which is `pointer-events: none` so achievement
toasts never block a tap on the app underneath them. The card inherited that. It
appeared, looked correct, and swallowed every press — DOWNLOAD, LATER and the
close X alike.

`pointer-events: auto` on `.iu-card` re-enables the card without re-enabling the
stack around it, which is the whole reason the stack is transparent.

Verified: both buttons reachable by hit test, and a click fires the handler.

Worth recording for anyone adding to that stack later: it is a TOAST layer.
Anything interactive placed in it has to opt back in, or it is decoration.

Also worth being clear about how these updates work, since the card looking
in-app is confusing: Play's in-app update API has two modes. **Immediate** hands
over a full-screen Play-owned screen. **Flexible**, which this uses, downloads in
the background through Play while the app stays usable, then leaves the prompt
and the restart to the app. So Play does the downloading and this card is
correctly ours.

## v0.150.65 — The help popups now exist in Italian

All 60 entries. `showHelp()` looks up `STRINGS[lang].help[key]` and falls back to
the English table when it misses; `STRINGS.it.help` did not exist, so every help
popup had always been English regardless of the setting.

Terminology follows Italian teaching rather than literal translation. The
distinctions that matter, checked against Italian sources rather than assumed:

- **calante / crescente** for flat and sharp when talking about TUNING. A written
  accidental is a *diesis* or a *bemolle*, but a note sounding too high is
  *crescente*. English blurs these; Italian does not, and using the notation word
  for the pitch would read as a mistake.
- **battere** for the downbeat, **pulsazione** for the underlying pulse.
- **semiminima / croma / semicroma / terzina** for the note values, rather than
  "quarto" and "ottavo" which read as arithmetic.
- **bordone** for drone, **tonica** for root, **grado** for scale degree,
  **armatura di chiave** for key signature, **rivolto** for inversion.
- **rullante / cassa / charleston** for the kit. Italian drummers say charleston,
  not hi-hat.
- **capotasto** for the nut, **capotasto mobile** for the capo, **corda a vuoto**
  for an open string, **tasto** for a fret.
- Left as-is because Italian players use them unchanged: swing, groove, step,
  ghost note, flam, shuffle, rimshot, clave, XP.

The markup is preserved exactly — same `<strong>`, `<br>` and entities — because
the popup renders it and the layout depends on it.

Verified live: 60 of 60 present, popups render Italian with the app in Italian
and English with it in English, no page errors.

## v0.150.64 — What the last dangling strings actually were

Chased the Circle of Fifths and Polyrhythm reports to the bottom. The header was
never the problem: verified live, `TOOL_NAME('cof')` returns CERCHIO DELLE QUINTE
with Italian set and CIRCLE OF FIFTHS with English, and `EXERCISE_NAME('poly')`
returns POLIRITMO. The re-render added in v0.150.63 works.

The giveaway was the CASING. The sweep reported "Circle of Fifths" in title case;
the header renders caps. Different element entirely.

It is the **help popups**. `HELP_CONTENT` holds 60 entries, `showHelp()` looks up
`STRINGS[lang].help[key]` and falls back to the English table when it misses —
and `STRINGS.it.help` does not exist at all. So every help popup in the app has
always been English, in both languages, and it looked like a header bug because
the panel sits on the screen it describes.

Not fixed here, and deliberately not started: 60 titles and 172 body fields, most
a paragraph of teaching prose with markup embedded. That is a translation job of
real size, and doing it badly would be worse than leaving it — these are the
explanations someone reads when they do not understand something, which is
exactly where clumsy Italian does damage.

The lookup already prefers the Italian table, so it needs only content. Logged
with the numbers.

**Everything else is clean:** 0 mismatched across all 35 screens, and the strings
the sweep still reports (SOLO A, SOLO B, hemiola) are identical in Italian by
nature.

## v0.150.63 — Hub titles, and two bugs the sweep exposed in my own fixes

**The TOOLS and TRAIN hub titles now follow the language.** Same root cause as
the module header: `setHeaderSection` is handed `t('mode_tools')`, already
resolved, so the title froze in whatever language was live when the tab opened.
Re-derived from `mode` instead.

**Caught before shipping: I guarded on a variable that does not exist.** The
first version tested `typeof currentMode`, but the variable is `mode`. A typeof
guard on a wrong name fails SILENTLY — no error, just a function that quietly
never does anything, which is the worst kind of wrong and precisely the class of
bug this whole exercise is meant to eliminate.

**The sweep was reporting a bug that was not there.** `setHeaderModule` fades the
old text out and writes the new one on a timer, so probing immediately after a
language change caught the PREVIOUS language. The sweep now waits past that
animation. Worth knowing for anyone reading its output: it measures what is on
screen, so anything animated needs settling time or it lies.

Down to 31 strings across 4 screens, 0 mismatched.

**Still open, and honestly not understood yet:** with the timing corrected, the
Circle of Fifths and Polyrhythm module headers show ENGLISH in both languages.
So `_rerenderHeader` is running and re-deriving, but landing on English even with
Italian set. That is a different bug from the one it replaced, and it is being
left for fresh eyes rather than guessed at. Everything else on those screens
translates; it is the title and subtitle only.

## v0.150.62 — Exercise headers and the Polyrhythm labels

**Four exercise folder names were hardcoded English** in `_exBackLabels`, so
Polyrhythm read "back to Rhythm" above a title reading POLIRITMO. Now
folder_rhythm / folder_ear / folder_games / folder_reading: torna a Ritmo,
Orecchio, Giochi, Lettura.

**`PR_MODES` had labelIt on some rows and not others** — TAP BOTH had one, BOTH
and the SOLO and TAP rows did not. All five filled: ENTRAMBI, BATTI A, BATTI B.
SOLO A and SOLO B keep their text because *solo* is an Italian word; the sweep
still reports them as identical in both languages, which for those two is the
correct answer rather than a finding.

**Correction to v0.150.61's header fix.** It stored setHeaderModule's arguments
and replayed them, which achieved nothing: those arguments arrive already
translated, because enterTool calls `setHeaderModule(TOOL_NAME(name), ...)` and
TOOL_NAME resolves at call time. Replaying them redrew the same Italian. It now
re-derives from `currentTool` / `currentExercise`, which are already tracked, so
the label functions run again and pick up the new language.

That is the same class of mistake as the original bug — assuming a stored value
is a key when it is actually a resolved string — and it is worth noting that the
live sweep caught it immediately, while reading the code twice did not.

## v0.150.61 — A sweep that proves it, instead of me claiming it

`intonare_lang_sweep.py` drives a real browser into all 35 screens, renders each
in English AND in Italian, and reports any visible string that is IDENTICAL in
both. That last part is what makes it usable: reporting every untagged string
buried the real findings under correctly-translated Italian. A string that does
not change between languages is either a proper noun or genuinely untranslated,
and that is a list short enough to read.

It also checks every tagged element's text against its key, catching the case a
file-reading audit cannot see: something rebuilt the element after the language
changed and lost the translation.

It found three real bugs on its first run:

**A key collision I introduced in v0.150.59.** `ui_key` was tagged onto the
tuner's reference-pitch label, which JS overwrites with "TONO". applyLang and the
live value then fought each other. Tag removed.

**The module header never re-rendered.** `setHeaderModule` draws the title,
subtitle and back label once when a screen opens, so it kept whatever language it
was drawn in. Category G had missed it because the function is not named
build*/render*. It now remembers its last arguments and a registered relabeler
redraws it.

Mismatches went from 3 to 0.

**38 untagged strings remain across 5 screens**, and they are listed by screen
rather than by line number: the Tools and Exercises hub titles and subtitles, the
Circle of Fifths header, and Polyrhythm's BOTH / SOLO A / SOLO B and its
dropdowns. Named, located, and no longer something to hunt for.

## v0.150.60 — Relabel registry: making the omission detectable instead of invisible

`setLang()` carried a hand-written list of ~30 builders to re-run on a language
change. Anything not on it kept the old language until its screen was rebuilt
some other way. That list failed twice in one session — the drum preset list was
missing, the chart buttons had no builder on it at all — and it fails SILENTLY,
which is the worst property such a list can have.

**Why not just re-enter the current screen?** Because `enterTool()` and
`enterExercise()` run each module's init, and init resets state: a vocal range
test in progress, a quiz mid-question. Losing someone's work to relabel a button
is worse than the stale label.

**What was built instead.** Screens register a RELABEL function — cheap,
idempotent, text-only. `runRelabelers()` executes the ones whose element is
actually on screen; off-screen ones are skipped because they re-render when
opened anyway. 21 registered, covering everything category G found.

**The audit now catches omissions.** New category G lists any builder that emits
translated text and is covered by neither `setLang` nor a registration. It found
27. Six remain, each a documented decision rather than an oversight: `render` is
the tuner's per-frame draw and re-runs constantly; the photo-zone builders fetch
over the network and a language toggle must not start downloads; the tone bank is
rebuilt by its own open handler; the pips carry no text.

**The registry defends itself.** Blanket-registering builders surfaced that
several APPEND rather than replace — `buildSequencer` adds ~846 nodes per call.
Those are latent bugs regardless of language, since calling them twice leaks.
Rather than trusting each to be idempotent, the first run of every relabeler is
measured; if the document grew, that relabeler is disabled permanently and
recorded in `_RELABEL_LEAKS`. A non-idempotent builder can therefore leak at most
once ever, and future registrations are protected without anyone remembering the
rule.

**Found while testing: setLang has been leaking all along.** With the registry
fully disabled, 20 language switches still add 2,679 nodes. `applyLang()` alone
is clean. So the leak is in the ORIGINAL builder list and predates all of
tonight's work. Not fixed here — migrating those calls into the registry would
put them behind the same leak check, and that is the right next step, but it is a
larger change than belongs at the end of a long session. Recorded with the
measurement so it can be picked up cold.

## v0.150.59 — Finishing the sweep, and a bug in my own audit

**Category B was inflated nine-fold by a bug in the audit itself.** It looked
back 3000 characters to decide whether a match was inside a `<script>` block.
That window is far too small in a file with script blocks tens of thousands of
lines long, so HTML built inside JS template strings — organ drawbars, Leslie
controls, chart internals around line 110k — was being counted as static markup.
It is not: `applyLang()` can never reach it, because it is regenerated on every
render. Those need `_tf()` at the point of construction instead.

Searching the whole preceding text rather than a window: **B drops from 1362 to
137**, which is a list someone can actually work through.

Translated in this pass: the vocal range panel (Mappa Estensione, Estensione
comoda, Centro di tessitura, Cantanti nella tua estensione), the Theremin's grid
and snap controls, the strings-grid hints, the difficulty ladder wherever it
appears (FACILE / MEDIO / DIFFICILE), INDIETRO, SERIE, IMPOSTA, TONALITÀ, STROBO,
ACCORDATORE and the tuner's "suona intonato".

**What the remaining 137 are, so nobody chases them again:**
- Product and brand names: Intonare, Rhodes, moog, ETHERWAVE THEREMIN, Grand
  Piano, Chordle.
- Terms identical in Italian or printed on real gear: SOST, SUST, TREM, VIBE,
  VOLUME, CLICK, TAP, AUTO, Allegro.
- Licences and credits: CC BY 4.0, CC0 1.0, Mutopia Project, Bret Pimentel.
- JS-filled placeholders: A MAJOR, PERFECT 5TH, SON CLAVE 3-2, OCT 4. Tagging
  these would let applyLang overwrite live content with the placeholder — a worse
  bug than the English it fixes.

Verified in a running browser, both languages: **1010 elements, 829 unique keys,
zero unresolved in either direction.**

## v0.150.58 — Rhythm Cards, Rhodes, Sound Bank, Theremin, Interval Reference

Twelve more keys across five modules: CARTE RITMICHE, MODO TOCCO, the Rhodes
voice controls (DOLCE / PROFONDO / BRILLANTE / CALDO), the Sound Bank editor
(piano / accento / pulisci), the Theremin's volume state, RIFERIMENTO INTERVALLI
and ASCOLTA, and the drumkit's long-press hint.

Deliberately skipped, so a later pass does not "fix" them:
- **Rhodes** and **ETHERWAVE THEREMIN** are product names.
- **TREM, SUST, PRESET, VOLUME, CLICK, TAP** are identical in Italian or are what
  is printed on real gear.
- **CC BY 4.0, CC0 1.0, Mutopia Project, Bret Pimentel** are licences and credits.
  Translating a licence name would be wrong.
- **PERFECT 5TH, C MAJOR, OCT 4** are JS-filled placeholders. Tagging those would
  let `applyLang()` overwrite live content with the placeholder text — a worse
  bug than the English it would fix.

Verified in a running browser: **819 unique keys across 986 elements, zero
unresolved.** That check is worth keeping, since it catches a key that exists in
markup but in neither table, which is how a raw key name ends up on screen.

## v0.150.57 — The Music Quiz was almost entirely untranslated

Grouping category B by screen showed the Music Quiz as by far the biggest
cluster: its landing, custom setup, in-quiz, results, win and review screens were
almost all raw English markup with no data-i18n anywhere.

43 keys added across 52 elements, covering the whole flow — PARTITA VELOCE,
SOPRAVVIVENZA, SENZA FINE, LE TUE REGOLE, the difficulty ladder (Familiari, Un
po' di ricerca, Per intenditori), the results screen (PUNTEGGIO, SERIE MIGLIORE,
PRECISIONE, DOMANDE SBAGLIATE) and the stats panel.

Some judgement in the wording rather than literal translation:
- "Deep cuts" is idiomatic English, not a difficulty level. "Per intenditori" is
  what an Italian would actually call the hardest tier.
- "Timer" and "XP" stay: both are used unchanged in Italian.
- CASUAL became LIBERA rather than a false friend — "casuale" means RANDOM in
  Italian, which would have described the wrong thing entirely.

## v0.150.56 — Chord quality names, all 55

Filtering the audit's category D by which table each entry lives in turned 860
findings into something reviewable. Most are correctly untranslatable — Chordle's
roman numerals (I - IV - V - I), the vocal range artist references (Johnny Cash,
Tom Waits), city names. `CHORD_DICT` was the real gap.

**It had no Italian at all.** Two of its four display sites already checked for
`nameIt` and fell back to English because there was none to find; the Chord Ear
pool chips and buttons used `def.name` raw on top of that. So chord qualities
read English on every screen regardless.

All 55 now have Italian: Minore, Diminuito, Aumentato, Semidiminuito, Settima di
Dominante, Sospeso 4ª, Terza Maggiore, Quarta Giusta and so on. Italian names
sevenths and ninths by degree — "Settima di Dominante" rather than a literal
"Dominante 7", which is how the theory is taught there.

Power Chord keeps its name: Italian guitarists say it unchanged, and Quartal
becomes Quartale, which is the real term rather than a coinage.

Added `_cdName(def)` so the four display sites share one path instead of two
checking and two not.

## v0.150.55 — Working through the audit's category C

Nineteen JS-built labels were writing English straight to the DOM, invisible to
`applyLang()` because they never touch a data-i18n attribute.

Translated: OTHER, OPTIONS, CLOSE, BASS, "to:", "tap a key to start",
"Sounds:" / "Written:" on the wind transposition card, and both photo states
(LOADING PHOTO, PHOTO UNAVAILABLE — NEEDS INTERNET).

**The octave abbreviation, at seven separate sites.** `'OCT '` was concatenated
inline in the Rhodes keyboard, the piano keyboard, the scale tool and the harp
octave tabs. All seven now go through one key, so Italian reads OTT (ottava) and
a future language needs one string rather than seven edits.

Added `_tf(key, fallback)` for JS-built labels. It exists because `t()` returns
the KEY when a string is missing, so a typo prints itself on screen — the bug
that put the literal text "gcc_play_note" on a chart button in v0.150.38. `_tf`
treats result-equals-key as a miss and uses the fallback, so the worst case is
English rather than gibberish.

Deliberately left in English: the leg tuner's "Show untuned only" and bar count.
Those are the dev-only tuning panel, reached by long-pressing a title, and are
not part of the app anyone else sees.

## v0.150.54 — Built an audit instead of chasing strings

Stopped fixing untranslated text one screenshot at a time and wrote
`intonare_i18n_audit.py`, which checks all six places a string can hide:
A) data-i18n keys missing from a table, B) markup text with no data-i18n,
C) JS writing English literals to the DOM, D) content tables with `name` but no
`nameIt`, E) `t()` keys in neither table, F) note names bypassing
`getDisplayNote`.

**A: 0. E: 0. F: 0** after this build — those three are unambiguous and now
clean. B and C are large but mostly dev surfaces and symbols; they need
judgement per item rather than a sweep.

What it caught:

**The drum preset list ignored `nameIt` entirely.** `name.textContent = p.name`,
raw. Twenty-four presets already HAD Italian names that were never being shown.
Every other preset surface in the app picks the twin; this one did not.

**`setLang` rebuilt the preset category tabs but not the preset list.** So
switching language relabelled the tabs and left the beat names in the old
language — exactly the "nothing updated when I switched to English" report.

**Eleven presets genuinely needed Italian names:** 8th Rock, the 5/4, 7/8 and 9/8
grooves, Trap 32nds, Bossa (Alt), Funky Drummer Fill, Copeland and Beauford
Style. The other 28 without a twin are proper nouns and genre names — Motown,
Bebop, Trap, Amen Break, Bonham, Porcaro. Translating those would be wrong, not
thorough, so they stay.

**Last Solfège gap closed.** `_bowedRenderNote` wrote `_BN[pc]` straight to the
chord label. Category F now reads zero.

**Regression fixed from v0.150.53:** moving the groove name out of the BPM pill
put a 100%-wide block inside `.prog-transport-strip`, a horizontal flex row,
which shoved the KIT button out of shape. The name is back inside the pill, and
the pill is now a column with `min-width: 0` so the name gets the pill's full
width and the ellipsis actually engages instead of forcing the pill wider.

## v0.150.53 — Solfège on the bowed charts, and the groove name given room

**Solfège stopped at the guitar-chord charts.** Only the `gcc*` functions routed
note names through `getDisplayNote()`. The bowed charts wrote `_BN[pc]` straight
into their note pills, so those stayed in letter names while the rest of the app
followed the setting. Three sites, now all going through one `_bnDisp()` helper
placed next to the `_BN` table so the next person writing a bowed pill finds it
first.

Worth noting the scale, plucked and wind charts show fret positions rather than
note names in their pills, so they were never affected — the gap was specific to
bowed.

**The groove name was ellipsised to nothing.** It lived INSIDE the BPM pill,
sharing a small fixed-width box with the number and the BPM unit, so on a phone
anything longer than a word or two vanished. It now sits on its own full-width
line under the row, centred, with the ellipsis kept only as a backstop for an
unusually long custom kit name.

## v0.150.52 — FileSaver was never actually called

The plugin installed correctly. The JS never asked for it.

`Capacitor.Plugins.X` is only auto-populated for plugins that also have a
JS-side definition. A native-only plugin registered in `MainActivity` needs
`Capacitor.registerPlugin('Name')` to build the bridge proxy. The check was
`P.FileSaver && P.FileSaver.save`, which is always undefined for a native-only
plugin, so export fell silently through to tier 1 and showed the share sheet —
looking exactly like the plugin had failed to install.

The mic plugin in this same file already does it correctly, a few hundred lines
up:

```js
let p = Capacitor.Plugins.IntonareMic;
if (!p && Capacitor.registerPlugin) p = Capacitor.registerPlugin('IntonareMic');
```

That pattern is now used for FileSaver too. No Java change; the Android side was
right the whole time.

## v0.150.51 — Backup export gets a real Save dialog

A backup you cannot retrieve is not a backup, which the share-sheet approach
proved in practice.

New native plugin, `FileSaverPlugin.java`, wrapping `ACTION_CREATE_DOCUMENT`.
The system file picker opens, the person chooses folder and filename, and the
app writes through the returned URI. No storage permission is needed, because
picking the location IS the grant. This is the sanctioned Android route and
nothing in the Capacitor ecosystem wraps it, hence writing it.

Export is now four tiers, each a fallback for the one above:
0. FileSaver — a real Save dialog, visible storage, survives uninstall
1. Filesystem + Share — writes a file, hands it to the share sheet
2. Share with the JSON as text
3. Browser download

The copy goes back to "Backup saved" from "Backup ready to send", because with
tier 0 it genuinely is saved rather than handed off.

Backing out of the picker resolves `saved: false` rather than rejecting — that
is a deliberate choice by the person, not a failure, and it should not raise an
error toast.

**Needs installing before it does anything**: drop the .java into
`android/app/src/main/java/com/lieutenantdan/intonare/`, add
`registerPlugin(FileSaverPlugin.class);` to MainActivity BEFORE `super.onCreate`,
then `npx cap sync android`. Until then the app falls through to tier 1 exactly
as before, so this build is safe to ship either way.

## v0.150.50 — Pre-decoding the fonts

Testing the same file in Chrome ON the phone was the breakthrough: jittery for
the first few loads, then smooth on every card once repeated reloads had warmed
the caches. That rules out the app, the WebView and the hardware, and points at
work that only happens the first time.

Two things reloading warms: V8's bytecode cache, and the font cache. Ten font
families ship embedded in this file, and a font is only decoded when something
first RENDERS text in it — so opening a module that uses a face nothing has used
yet pays a synchronous decode that blocks layout, mid-animation.

`warmFirstOpen()` now calls `document.fonts.load()` for all eleven families at
idle, doing deliberately what those reloads were doing by accident.

Worth recording what this session ruled OUT, so nobody re-treads it:
- **Not `overflow: hidden` on the morph.** A single run said otherwise; five runs
  said identical with and without.
- **Not module construction timing.** Deferring the build until after the
  animation changed 22 slow frames to 23.
- **Not document size.** 6,459 nodes exist but only 551 are rendered; the other
  5,908 are already skipped by `display: none`, so `content-visibility` would add
  risk for no gain — and it breaks size measurement of hidden elements, which
  this app does in several places including the overlay detector.
- **Not the hardware.** An S25 Ultra.

Also worth recording: frame timings measured in this headless container swing
between 15 and 43 slow frames on identical runs. They are not trustworthy for
anything this size. The Chrome-on-device comparison was worth more than every
measurement taken here.

## v0.150.49 — Warming the first module open

Your report that tapping anywhere BEFORE picking a card makes Tuner and Metro
better was the clue: that first gesture is what lets the audio context start.

Measured cold from a fresh load, with the launcher up: Tuner 33 of 70 frames
over 20ms, Tools 35, Train 43 — and only 2-16ms of synchronous work at the tap.
So it is neither the animation nor script at the moment of the tap. It is
first-layout of the module's own DOM plus first-touch audio setup, both landing
underneath the morph.

`warmFirstOpen()` pays that cost on idle after boot. Result:

| module | cold | warmed |
|---|---|---|
| Tuner | 33/70 | 23/70 |
| Tools | 35/70 | 23/70 |
| Train | 43/70 | 31/70 |

**Not tied to the splash or the launcher.** `lnchShouldShow()` returns false for
a pinned module or a deep link, so both are skippable — and those users need this
most, since their module opens immediately. It runs on `requestIdleCallback`
after boot regardless of path, with a timeout fallback for Safari.

**Deliberately does not navigate.** An earlier version called `setMode()` for each
hub, which warms considerably better (Train 43 → 8) but genuinely changes the
current view; doing that behind a launcher risks leaving the app somewhere nobody
asked for. This forces style and layout on the hidden hub subtrees instead, which
is the expensive half, and restores the inline styles it touched.

Honest about the size of it: this is a real, measured improvement of roughly a
quarter to a third of the dropped frames, not a fix. Train remains the worst
because it builds the most. Closing the rest means either accepting the
navigating warm-up or splitting the hub construction so it does not all land in
one frame.

## v0.150.48 — Morph timings, measured against the spec

The card morph is a "container transform" in Material terms — a card expanding
into a full screen. M3 specifies **long1 (450ms)** for exactly that, with the
corner radius animating alongside the movement.

Transform was 420ms and border-radius 340ms, so the corners finished settling
while the card was still travelling. Two halves of one gesture resolving 80ms
apart is the kind of thing that reads as unfinished rather than wrong. Both are
now 450ms and land together.

**Deliberately NOT adopted: M3's `emphasized` curve (0.2, 0.0, 0, 1.0).** Its
`y1` is 0, so it genuinely sits still at the start — which is the dead ~110ms
after the tap already diagnosed and commented on in this file. Motion a finger
started should move when the finger moves. The ease-out stays.

**Two timing contracts nearly broken while doing this**, both caught by reading
the surrounding comments rather than by any test:

- The morph's `opacity` is not part of the arrival. It drives the EXIT fade, and
  `CARD_FADE_MS` in `lnchGo` is documented as having to match it. Raising it to
  450ms would have scheduled the teardown before the fade finished — precisely
  the bug the comment there describes. Left at 300ms.
- The sibling cards' 300ms opacity is matched to `T_LAUNCHER_FADE`, so they stop
  fading at the same instant the launcher clears. Stretching them to 450ms left
  them mid-fade over an empty screen. Left at 380/300.

So the change is narrow on purpose: only the two properties that genuinely belong
to the same movement were touched.

Also of note for later: M3 replaced easing-and-duration with a spring system in
May 2025 (spatial springs overshoot slightly and settle). That is the current
standard, but it needs a physics implementation rather than CSS transitions, so
it is a post-1.0 consideration rather than a tweak.

## v0.150.47 — Module picker morph: what is actually slow

Promoted `#lnchMorph` to its own compositor layer (`will-change`, `contain`,
`backface-visibility`), which improved the median frame from 23ms to ~17ms.

The more useful result is the diagnosis, and it corrects two wrong turns taken
on the way:

**Measured across 5 runs each, the morph holds 60fps — 0 frames over 20ms,
worst 18ms — with or without `overflow: hidden`.** An earlier single-run sample
showed 19 slow frames with it and 0 without, which looked conclusive and was
noise. `overflow: hidden` is restored; removing it bought nothing and it was
there for a reason.

**Only the FIRST morph of a session stalls.** Subsequent ones are clean. That is
one-time lazy initialisation elsewhere in the app warming up under the
animation, not the animation itself — the same pattern already seen in
`chordScaleStopAllAudio`, which costs 42ms on its first call and 8ms after.

So the fix, when it is worth doing, is pre-warming that work during the splash
or the launcher, before anything is tapped, rather than optimising the morph.
Noted rather than done: it means moving initialisation earlier in the boot
sequence, which is not a change to make immediately before a device test pass.

A note is left in the CSS warning that single-run frame timings here are
extremely noisy, so the next person does not repeat the same wrong turn.

## v0.150.46 — Selected-instrument pill and tone bank categories

**The picker pill stayed English while the menu behind it was Italian.** It used
`meta.label`, the English roster name, so it read VIOLIN over a list reading
VIOLINO. It now reuses the `inst_<id>` keys added in v0.150.40, falling back to
the roster name only for an instrument with no key.

**Tone bank category tabs were English literals** — KEYBOARD / WAVES / PLUCKED /
BRASS / WOODWIND — built inline rather than through `t()`. Now TASTIERE / ONDE /
PIZZICATE / OTTONI / LEGNI.

**PENNATA confirmed correct** rather than assumed. Italian guitar teaching
material titles the technique "Strumming (o «pennata»)", and *strimpellare*, the
literal translation, carries a sense of playing badly — which is why the earlier
RASCHIA ACCORDO was wrong in a different way. The only other thing Italian
guitarists actually say is the English loanword, which would read as unfinished
in an Italian interface.

## v0.150.45 — Charts Italian pass, part 3

From the device screenshots:

**"back to ARMONIA"** — `'back to '` was concatenated in English against a
translated folder name, so the header was half and half. Now `hdr_back_to`, used
by both the tool header and the exercise header.

**Bowed sub-mode pills** NOTES / SCALES had no keys at all → NOTE / SCALE.

**Three bowed EXPAND buttons** were untagged; they reuse the existing
`gtool_expand` key, so they read ESPANDI like every other expand button.

**Two chart hint lines** were English: "Tap dot to hear · use arrows to browse ·
EXPAND shows all" and "Tap dot to hear · root orange · grayed = outside
position". Both translated, matching the phrasing of the six hint lines that
were already Italian.

Verified in a running browser: sub-pills, hints and expand buttons all render
Italian, and `hdr_back_to` resolves in both languages.

Note for the next pass: the ordinal position labels on the fingerboard (1st,
2nd, 3rd, 6th) and the "fr" fret abbreviation are still English. They are
generated, not static markup, so they need locating in the drawing code rather
than tagging.

## v0.150.44 — Language switching now refreshes the chart buttons, and an early return that ate half of setLang

**Chart buttons kept their English labels after switching to Italian.** Their
text is set programmatically, not through `data-i18n`, so `applyLang()` cannot
see them; they only corrected themselves when pressed or when the instrument was
swapped. `setLang()` rebuilds 35 surfaces by hand, and the wind and bowed charts
have no init function in that list. Added `_chartBtnsRelabel()`, which relabels
all 13 from `CHART_BTNS` in one pass. A button currently reading STOP keeps it,
so a language change cannot interrupt playback feedback.

**`setLang()` had an early `return` in the middle of it.**

```js
const vrModal = document.getElementById('vrArtistModal');
if (!vrModal) return;
```

On any screen where that element is absent, `setLang` bailed there and never
reached `vrRenderReference()` or the tooltip relabel. The same pattern sat at the
end for `#tooltipText`. Both are now guarded conditions rather than returns, so
nothing downstream can be skipped by an element simply not existing.

**Translation fix: `gcc_strum` read "RASCHIA ACCORDO".** *Raschiare* is to scrape
or scratch; no guitarist would read that as strumming. Now `PENNATA`, the
standard Italian term for a plectrum stroke across the strings, which also keeps
it distinct from `gcc_play_chord` ("SUONA ACCORDO") next to it.

Verified by switching languages in a running browser with the charts loaded: all
13 buttons flip immediately, none stay English, no page errors.

## v0.150.43 — Fast path for the known full-screen overlays

The launcher's entrance is driven by class changes on `#lnch` itself — 13 call
sites toggling lnch-gone / lnch-entering / lnch-in / lnch-nosplash-in. `#lnch` is
also an overlay candidate, so every one of those woke the scroll-lock observer,
and the answer was a 97-node walk calling `getBoundingClientRect`,
`getComputedStyle` and `elementFromPoint` — to answer a question a single display
check on `#lnch` already settles.

`_anyOverlayOpen()` now checks the launcher, the tour overlay and the module
picker first. Measured in a browser: 2.7ms against 10.1ms per 50 calls, and the
97-node walk is skipped entirely while one of them is up. The full scan still
runs when none is, so nothing stops being detected.

Honest caveat: those absolute numbers are small in desktop Chrome. This is a real
saving and it is the right shape, but it may not be the whole cause of the
launcher feeling slower in the built app than in a preview. WebView also
composites gradients, shadows and staggered opacity transitions more slowly than
Chrome, and the launcher has four large cards doing all three at once.

## v0.150.42 — Guarding the Italian labels against overflow

Could not render the piano console in the headless harness to measure it, so the
risk was removed rather than assumed away.

`SMORZATORE` is ten characters in a box built for `DAMPER`'s six. Shortened to
`SMORZ.`, which matches the English width exactly. `UNA CORDA` stays — it is the
correct name for that pedal — but it contains a space that could wrap onto two
lines and reflow the pedal row, so `.ppc-name` now holds one line and shrinks
with an ellipsis instead of overflowing or wrapping.

Still worth a glance on device: the pedal row and the lid segments are the two
places where a longer Italian word could look cramped even without overflowing.

## v0.150.41 — Charts Italian pass, part 2: the piano console

Translated what genuinely differs and deliberately left what an Italian musician
would already see in English or in Italian:

**Translated:** LID → COPERCHIO, CLOSED/STICK/OPEN → CHIUSO/ASTA/APERTO,
DAMPER → SMORZATORE, HOLD → TIENI, and the soft pedal → UNA CORDA, which is the
standard Italian name for that pedal rather than a literal rendering of "soft".

**Left alone on purpose**, so a future pass does not "fix" them back:
- `SOST` is already Italian — sostenuto.
- `TREM` is already Italian — tremolo. Same for VIBE/vibrato.
- `PIANO` is the Italian word.
- `SUST`, `VOL` and `OFF` are the abbreviations Italian players read on real gear.
- `RHODES` is a brand. `Grand Piano` is lettering on the instrument graphic, a
  prop rather than interface text; real pianos carry it in English everywhere.

Both instances of the console (the tuner's and the Tools one) are covered —
tagging was done by attribute rather than by position, so neither was missed.
Verified by switching to Italian in a running browser and reading both back.

## v0.150.40 — Charts Italian pass, part 1: the instrument picker

The whole instrument picker drawer was English. 33 instrument buttons and 6
family tabs, all static markup with no `data-i18n` at all, so `applyLang()` never
touched them.

All 39 now carry keys generated from their existing `data-inst` / `data-fam`
values, with Italian for each: CHITARRA, BASSO, UKULELE, MANDOLINO, LIUTO,
PIANOFORTE, ORGANO, ARPA, PERCUSSIONI, TROMBA, FLICORNO, CORNO, EUFONIO,
FLAUTO, CLARINETTO, FAGOTTO, FLAUTO DOLCE, ARMONICA, ARMONICA CROM., VIOLINO,
VIOLONCELLO, CONTRABBASSO, and family tabs Corde / Crom. / Ottoni / Legni /
Ance libere / Arco. Names that are the same in both languages (BANJO, TUBA,
TROMBONE, OBOE, SAX, OCARINA, VIOLA, MELODICA, BOUZOUKI, DIDGERIDOO, TIN
WHISTLE) keep their spelling rather than being forced.

Verified by switching the app to Italian in a running browser and reading every
button back: zero remain English.

**Still to do in this pass:** the piano console (LID, TONE, VIBE, DAMPER, SUST,
SOST, VOL, TREM and their values) has 22 untranslated strings, and the interval
reference has a handful. Counted, not yet done.

## v0.150.39 — A missing i18n key printed itself on a button

**Stopping a bowed note showed a raw text string.** `t()` returns the KEY ITSELF
when a string is missing, so the two bowed buttons pointing at the non-existent
`gcc_play_note` had `_chartBtnIdle` write the literal text "gcc_play_note" onto
them. The keys were fixed in v0.150.38; `_chartBtnIdle` now also treats a result
identical to the key as a miss and uses the fallback, so no future bad key can
print itself on a button.

**Module card titles were 30px off-centre.** `.lnch-txt` is padded 42px on the
left to clear the pin button against 12px on the right, so its box never sat
centred in the card. Short English names hid it; ACCORDATORE and STRUMENTI did
not, sitting right and running past the edge. The title now pulls that 30px back
and centres on the card, while the sub-line keeps the padding it needs.

**Streak milestone cues guarded.** `hapticMilestone()` and `playCueMilestone()`
run before the toast is built, so a throw in either — a missing haptics plugin, a
suspended audio context — would kill the toast on device while working in a
browser. Both wrapped.

On Interval Training's missing toast: verified the whole path in a running
browser — `enterExercise('interval')` resets the guard, five correct taps reach
`checkStreakMilestone(5)`, and the toast renders "STREAK 5!". The wiring landed
in v0.150.38, which is AFTER the build that test ran against.

## v0.150.38 — Interval Training's streak toast, and two dead bowed labels

**Interval Training never showed a streak toast in Tap or Test mode.** Only Sing
mode called `checkStreakMilestone()`. The other two incremented `ivStreak` and
stopped, so the mode most people use counted a streak it never celebrated. Both
now fire it.

**Two bowed chart buttons pointed at an i18n key that does not exist.**
`bowedNotePlayBtn` and `bowedDsPlayBtn` both used `gcc_play_note`, which is in
neither language, so `t()` returned nothing and they fell through to the English
fallback permanently — the placeholder seen on device. The note button now uses
`trp_play_note`, which already has its Italian twin; the double-stop gets its own
key, `bowed_play_ds` (SUONA BICORDO).

**Confirmed the new scales reach every instrument.** Measured in a running
browser across fretted, plucked and bowed families plus a wind and a re-entrant
instrument: all 35 scales and 9 groups on each. `gssGroupsForInstrument()` also
has a safety net that appends any group missing from the per-instrument config,
so a future group cannot be silently dropped from one chart.

Relative Pitch tone overlap remains. Two attempts fixed the delayed-tone timers
in both the climb and practice mode, and it still overlaps, so something else is
producing the second voice. Parked deliberately rather than guessed at again.

## v0.150.37 — Changing scale mid-loop kept playing the old one

Reported as two things — the new scales all sounding alike, and the loop not
updating when the scale changed. They are one bug.

`playScale()` snapshots `scaleTapeData()` once when it starts. Changing the
scale or root while it was running redrew the tape and the name but never
touched the audio, so the OLD sequence kept looping under the NEW label. Every
scale picked while a loop was running therefore sounded identical, because it
was: you were hearing whatever started first.

`updateScale()` now restarts playback in the same direction when a change lands
mid-loop. Root changes route through the same function, so they are covered too.

**Verified the data was never wrong.** Measured in a running browser at every
layer: `scaleDefIntervals`, `GSS_SCALE_TYPES.intervals` and the scales tool's own
`getScaleData` each return distinct, correct pitches for all eight new scales.
Also confirmed all eight are present in every registry that matters —
`SCALE_DEFS`, `GSS_SCALE_TYPES`, `GSS_SCALE_GROUPS`, `TC_SCALE_GROUPS`,
`SCALE_SHORT_NAMES` and `SCALE_GHOST_OVERRIDE` — with English and Italian names
on each.

## v0.150.36 — The fifth scale list, tempo graded on tempo, and long Italian labels

**The scales tool still showed 28.** There is a FIFTH place a scale must be
listed. `SCALE_DEFS` holds the data; `TC_SCALE_GROUPS`, `GSS_SCALE_TYPES` and
`GSS_SCALE_GROUPS` each drive a different surface; and `buildScaleTypePicker`
holds its own local array — twice, once per view — which is what actually
renders. All updated, with Japanese and Indian Thaat groups and both EN/IT
labels. Adding a scale touches five lists; that is worth knowing before the
next one.

**Tempo Lock graded distance from a grid, not tempo.** Every tap was compared to
its nearest expected beat, so a steady tempo error compounds: hold a rock-solid
123 against a target of 120 and each tap lands further ahead than the last. +3bpm
measured 43ms average and graded red while sounding fine. It now derives BPM from
the gaps between taps and grades the difference: LOCKED IN under 2bpm, CLOSE
under 5, NEEDS WORK under 10. A steady +3 now reads as 3bpm out whatever the
round length. Drift within a round still shows, because an unsteady pulse gives
an unstable average interval. Falls back to the old metric on a single tap, since
one tap gives no interval to measure.

**Relative Pitch still stacked tones on rapid next.** v0.150.30 tracked the
climb's delayed tone and missed that practice mode has its own, so each tap
queued another 350ms tone with nothing cancelling the previous. Both use the same
handle now.

**Italian launcher cards clipped mid-word.** ACCORDATORE is eleven characters
against TUNER's five, at a font size tuned for the English labels. Names over
eight characters now step down a size and tighten their tracking. Length-driven
rather than language-driven, so future translations are covered.

## v0.150.35 — A third scale list, and empty symbol popups

**The scales module showed 28 of 36.** There is a THIRD list of scales:
`SCALE_DEFS` holds the data, `TC_SCALE_GROUPS` drives the tonal-centre picker,
and `GSS_SCALE_GROUPS` drives the scales module and the chart menus. v0.150.22
updated the first two. Anything absent from the third simply never appears in
the module, which is why the count sat at 28.

Added `yo` to Pentatonic, `ukrdorian` to World, and two new groups — Japanese
(hirajoshi, iwato, kumoi, insen) and Indian Thaats (purvi, marwa, todi). Both
also registered in `GSS_INSTRUMENT_SCALE_ORDER`, without which a group exists
but is never rendered. Module now lists 35; `chromatic` stays out on purpose.

**Survival Guide symbol popups were empty.** They showed the label and nothing
else. The glyph rules are scoped to `#toolSurvivalGuide`, but the zoom sheet is
appended to `<body>` to avoid being clipped by the card — so it sat outside that
scope with no Bravura face and no sizing box, rendering an invisible glyph.
Added unscoped copies for the sheet.

## v0.150.34 — Backup copy stops promising a download

Decided for 1.0: backup export stays share-sheet only. Android has no guaranteed
"save to device" share target — the sheet lists whatever apps accept a .json, so
Drive or email is the realistic destination. Both are legitimate backups, and
arguably better than a local file that dies with the phone.

The copy said "Backup saved", which implied a file had landed somewhere on the
device. It now reads "Backup ready to send", and the sheet title asks you to send
it somewhere safe. EN and IT both.

A true local "Save as…" needs the Storage Access Framework. No Capacitor plugin
exposes `ACTION_CREATE_DOCUMENT`, so it means a small custom native plugin per
platform. Recorded as post-1.0 rather than left as an unexplained gap.

## v0.150.33 — Scale lists sorted by family, daily badge no longer overlaps

**Scales looked incomplete because they were unsorted, not missing.** Both lists
were verified complete: all 36 in the tonal-centre picker, 35 in the instrument
charts (`chromatic` is deliberately absent there — every note on a fingering
chart is not a scale). The eight world scales added in v0.150.22 were appended
to the END of the chart list, so they read as a random tail and were easy to
scroll past.

Both lists are now ordered by family, and the families match each other:
Major / Minor / Pentatonic & Blues / Japanese / Jazz · Melodic Modes / World /
Indian Thaats / Symmetric. The chart list also drives next/prev cycling, so this
makes stepping through scales follow a musical order instead of an
edit-history one.

**The Music Quiz daily badge overlapped in Italian.** GIORNALIERA is eleven
characters against DAILY's five, in an absolutely-positioned badge with fixed
padding. Added `mq_daily_badge` — OGGI in Italian, which reads naturally on a
once-a-day challenge and fits the same box. The badge also has a `max-width`
with ellipsis now, so no future translation can grow into the card beside it.

## v0.150.32 — Chart button parity pass

Went through all 13 buttons in `CHART_BTNS` rather than fixing the one that was
reported, since the same patterns were repeated across the charts.

**Four charts had a hand-rolled copy of `_chartBtnIdle`.** Guitar strum, guitar
scale, plucked scale and plucked chord each reset their own label with
`if (btn.textContent === '■ STOP')` — comparing against the English literal, so
in Italian the check never matched and the button stayed reading STOP after
playback finished. All four now call the shared helper, which reads its idle
label from the registry and is locale-aware.

**Two bowed buttons had untracked label timers.** Bowed note and double-stop
both set a bare 1900ms `setTimeout` to restore their label. Stopping early and
replaying left the old timer running, so it could reset the label of the note
started afterwards. Both tracked and cleared now, same as the wind Notes button
in v0.150.31.

Renamed `_chartBtnStopLabel` to `_chartBtnHaltText`: the stopAll audit matches
function names containing "Stop" and was flagging a label getter as an unwired
stop function.

Final state, all 13 buttons: every one has an idle path, every timer that
restores a label is tracked, and there are no hardcoded '■ STOP' comparisons
left anywhere in the file.

## v0.150.31 — The STOP button that played, and Tempo Lock's unreachable streak

**Wind Notes button said STOP and did PLAY, in a loop.** `_chartBtnPlay()` flips
the label to "■ STOP", but `trpPlayCardNote()` had no stop branch. Tapping it
again just replayed the note and restarted the 1500ms label timer, so the label
bounced between STOP and PLAY while the note fired every tap. It now stops the
ringing note, cancels the timer and restores the label. The timer is tracked too,
so a stale one cannot reset the label of a note started after it.

**Same helpers had a locale bug.** `_chartBtnPlay` wrote the literal string
'■ STOP' and `_chartBtnIdle` compared against that literal. In Italian the
button showed English AND the equality check never matched, so it silently
refused to restore any chart button's label. Both go through `t('btn_stop')`
now, still accepting the English literal for older code paths that write it
directly.

**Tempo Lock: 25/50ms to 40/75ms.** A streak needs LOCKED IN or CLOSE, and 50ms
is inside normal touchscreen jitter, so holding a streak on a phone was close to
impossible and the grade stopped carrying information. 40/75 still rewards
accuracy without being unreachable.

## v0.150.30 — Test-pass fixes: symbols, feedback box, overlapping tones, toast opacity

**Survival Guide showed one symbol on a three-symbol page.** The glyph map was
built from `SG_TERM_DEMOS` (the audio demos) instead of from the `data-term`
values actually in the Guide copy, so it covered 8 of the 17 terms in use. The
DYNAMICS page carries crescendo/decrescendo/diminuendo and only decrescendo was
mapped — exactly the one badge that appeared, and the fp/sforzando/subito page
got none at all. Added crescendo, diminuendo, piano, fp, sforzando, accent,
staccato and tenuto. `subito` stays unmapped on purpose: it is a direction, not
a mark. Coverage is now 16 of 17.

**Symbols are tappable for a large view.** They have to stay small to sit on one
row without pushing the body copy down, and some marks are tiny by nature (a
staccato dot is 4px tall in Bravura's own metrics). Tapping one opens it at 3.4x
using the same glyph data and the same scaling maths, so the two views cannot
disagree.

**Interval Training's feedback box still appeared only after answering.**
v0.150.9 fixed the markup default and the round reset, but missed a third place:
the manual/sing mode switch hid it again on every entry. That is why the layout
still shifted. All three now agree.

**Relative Pitch tones overlapped.** The question tone is deliberately delayed
350–620ms so it does not land on the rung transition, but the timer was
untracked. `chordPlayMidi` stops what is currently ringing; it cannot stop a
note that has not started yet, so tapping A440 during the window let both
sound. The handle is kept now and cleared by `rlpSound`.

**The streak toast let the screen read through it.** Its background was a single
`linear-gradient` starting from a translucent milestone tint, so whatever sat
behind the toast bled into the text. Split into `background-color: var(--panel)`
plus the same gradient as `background-image`: same tint, opaque base.

**Wind chart button flipped back to PLAY early.** The reset timer allowed 400ms
after the LAST note STARTS, but each note runs `dur` seconds, so on slower
instruments the button reverted while the final note still sounded. It now waits
for the note plus a short tail.

Chart button audit: all 13 buttons in `CHART_BTNS` have a registry entry and a
matching element, and none plays without a reset path.

## v0.150.29 — The alarms screen, found in the plugin source

Read the installed plugin's code instead of guessing a fourth time.

`@capacitor/local-notifications` **8.3.0** is a Kotlin rewrite, and it changed
behaviour. `schedule()` now does this:

```kotlin
val honorExact = notifications.any { it.isExactNotification }   // default: true
if (honorExact && SDK >= S && !canScheduleExactAlarms()) {
    startActivityForResult(... ACTION_REQUEST_SCHEDULE_EXACT_ALARM ...)
    return
}
```

`schedule()` opens the "Alarms & reminders" screen itself. The older Java
version silently fell back to an inexact alarm and logged a warning; the new
one prompts. `isExactNotification` is documented `@default true`, `@since
8.3.0`.

That explains everything that did not add up:
- **Why it appeared from nowhere.** Nothing in this app changed. A plain
  `npm install` pulled 8.3.0 through the `^8.2.0` caret in package.json.
- **Why two manifest fixes failed.** No manifest edit could work — removing the
  permission makes `canScheduleExactAlarms()` return false, which *guarantees*
  the prompt.
- **Why the toggle on that screen was inert.** It was `SCHEDULE_EXACT_ALARM`
  denied by default at targetSdk 36, exactly as Android intends.

Both reminders now set `isExactNotification: false`. A daily practice nudge does
not need second-accurate delivery. The notification still fires, just inexactly,
and Android is never asked for special access.

The v0.150.28 deferral of scheduling to first module entry is kept. It was not
the fix, but it is still correct: nothing system-level should run before someone
has seen the app.

## v0.150.28 — The alarms screen, actually diagnosed

Two manifest fixes failed before this one. The merge report settled it: the
permission was never the mechanism.

`scheduleNotifications()` ran 2 seconds after load. Scheduling a calendar-based
reminder makes the plugin call `canScheduleExactAlarms()`; on Android 13+ that
is denied by default, and Android's own documentation then prescribes firing an
intent to the "Alarms & reminders" special-access screen. So the plugin was
behaving correctly and the app was asking at the worst possible moment: a brand
new user met a system permission screen on their first tap, before seeing
anything.

Stripping the permission could not fix that, and made it worse in principle:
removing it guarantees `canScheduleExactAlarms()` returns false, which
guarantees the redirect.

**Reminders stay ON by default.** The practice nudge is most of their value and
most people never go looking for a notifications screen to switch one on. Per
Capacitor's own docs, without `SCHEDULE_EXACT_ALARM` notifications still fire —
they are just inexact, which is right for a 7pm nudge and easier on the battery.

What changed is only WHEN scheduling runs. It now waits for first module entry,
riding the same launcher gate as the update check, and is guarded so it can only
run once per session. The boot-time `requestPermissions()` call went too: it
fired on every first launch for the same reason.

Net effect: nothing system-level is requested until the person has actually
entered a module.

## v0.150.27 — Road Trip leg tuning complete: 39 of 39

`to_spring`, `traumerei`, `troika`, `waldstein_1` and `wedding_day` applied and
signed off. `RT_TUNED` 16 to 21, which is every perf leg.

Both checks now read zero: no leg is badged NEEDS TUNING, and no leg still
carries the converter's default hook spacing of 5/7/10/14/17. Every hook in
Road Trip has been heard by a person and placed by hand.

`waldstein_1` is the outlier worth noting: its final hook sits at beat 1553.96
(about 9m43s in), the longest leg in the set by a wide margin.

## v0.150.26 — Five more Road Trip legs tuned

`fantaisie_impromptu`, `prelude_csharp`, `prelude_op23`, `raindrop` and
`sonata_facile` applied from device and signed off in `RT_TUNED` (11 to 16).

34 of 39 legs tuned. Five remain on converter defaults: to_spring, traumerei,
troika, waldstein_1, wedding_day. The badge list and the hook data agree on the
same five.

## v0.150.25 — Tuned legs stopped claiming they need tuning

`RT_TUNED` is the sign-off list the leg tuner reads: a perf song is badged
NEEDS TUNING until its id appears there. Six legs tuned on device across the
last two passes were never added, so the tuner kept flagging work that was
already done.

Added `moonlight_3`, `prelude_c`, `alla_turca`, `barcarolle`, `butterfly` and
`moonlight_2`. Five entries to eleven.

Cross-check: the ten perf songs still badged are exactly the ten whose hook
spacing is still the converter's default (5/7/10/14/17). The badge list and the
data now agree, which was the point.

## v0.150.24 — Two untranslated strings, and duplicate keys in the chart labels

**Polyrhythm graded in English for Italian users.** Its four grade labels
(LOCKED IN / CLOSE / NEEDS WORK / OFF) were hardcoded, while Tempo Lock right
next door used `tl_grade_*` keys that already carry Italian twins and cover the
same four bands. Reused those rather than duplicating under a `pr_` prefix.

**Music Quiz's daily badge said DAILY in Italian.** The RESUME branch two lines
above it in the same function had already been fixed for exactly this and
carries a comment saying so; the DAILY branch was missed at the time. Now uses
`chordle_daily`, which already has its twin (GIORNALIERA).

**`SUB_LABELS` had duplicate keys.** `standard` was declared twice ('STANDARD'
for strings, then 'STD' for woodwinds) and `tenor` twice with the same value. In
an object literal the last wins silently, so every instrument was already
rendering 'STD' and the 'STANDARD' entry was dead. Removed the dead entries and
kept 'STD' to preserve exactly what shipped — changing the label is a separate
decision, not a side effect of a cleanup.

Also added the oboe family: `oboe` and `coranglais` were missing, so cor anglais
rendered as its raw key, 'CORANGLAIS' with no space.

Two strings the audit flags are deliberately left in English: the leg tuner's
untuned filter and the `audioPathStatus` debug overlay are both dev-only
surfaces.

Note on the instrument audit: it reads a fixed 600-character window after
`SUB_LABELS`, so the comment added above the map pushes later entries out of its
view. It will report `coranglais` as missing even though it resolves correctly
at runtime. Verified by evaluating the object directly.

## v0.150.23 — Vocal range reference copy, and a broken string that was shipping

**The Coloratura Soprano description was corrupted.** An unescaped apostrophe in
"Mozart's" ended the string early, so the Italian text and the `descIt:` key
itself were swallowed into the English string. The app was rendering literal
code to users:

> ...as much as by range. Mozart', descIt:'Un sottotipo di soprano...

Coloratura also had no working Italian description at all as a result. Both
rewritten and separated properly.

**Basso Profondo had a duplicate `nameIt` key** in the same object literal. The
second silently won. Harmless, but it was one typo away from mattering.

**Tenor and Countertenor both claimed to be "the highest standard male voice."**
Countertenor now describes what it actually is: a male voice sung mainly in
falsetto, reaching higher than a tenor.

Copy pass on all nine voice types: opinions dropped ("arguably the rarest voice
type of all", "rarer than most think", "territory only coloraturas can inhabit
reliably"), em-dashes replaced, scare quotes around choral "altos" removed.
Verified all nine now carry both EN and IT text with no leaked code.

**Dormant grid deletion: nothing to delete.** Checked the whole file — no song
carries both perf data and a legacy lh/rh grid. The 33 remaining `lh:` arrays
all belong to songs with no perf data, so they are live. Either the deletion
happened and was not recorded, or the perf conversion replaced them outright.
Removing this from the backlog.

## v0.150.22 — Eight world scales added: 28 to 36

Audited the scale bank against Western, Eastern European, Middle Eastern,
Indian and East Asian practice. Western coverage was already complete. Three
real gaps existed, and two things were deliberately left out.

**Japanese — was 2 of 6.** The app had Hirajoshi and In. Added **Yo, Iwato,
Kumoi and Insen**. Yo matters most: it is the bright, semitone-free counterpart
to In, and the two are the standard contrasting pair in Japanese folk music, so
shipping In without Yo was like shipping minor without major. Sources genuinely
disagree on these names — the intervals given here for Iwato are what Slonimsky
calls Hirajoshi — so the code follows one convention consistently and says so,
since mixing sources is what produces two scales with the same name and
different notes.

**Eastern European — one clear miss.** Added **Ukrainian Dorian** (Dorian ♯4),
also known as Mi Sheberakh, Altered Dorian, Romanian and Hutsul. It carries
that many names because Ukrainian, Romanian, Greek, Balkan and Jewish
traditions all use it; it is the standard klezmer minor and was the only one of
klezmer's four modes missing.

**Indian — completes the thaat system.** Seven of the ten Hindustani thaats
already existed under Western names (Bilawal=Major, Kalyan=Lydian,
Khamaj=Mixolydian, Kafi=Dorian, Asavari=Natural Minor, Bhairavi=Phrygian,
Bhairav=Double Harmonic). Added **Purvi, Marwa and Todi**, so the app now covers
all ten parent scales of Hindustani classical music.

**Deliberately NOT added.** Rast, Bayati, Saba and Sikah — four of the most
important maqamat, and Rast is called the mother of them all — are defined by
quarter tones. Rast's third sits between a major and minor third. There is no
honest 12-TET representation: an approximation is not a simplified version of
the scale, it is a different scale that a listener from that tradition hears as
wrong. Same reasoning for Indonesian slendro and pelog, which are not equal
tempered and vary between individual gamelan sets. Chinese gōng/shāng/jué/zhǐ/yǔ
are rotations of the major pentatonic, whose pitches the app already has, so
adding them would be five near-duplicates.

All eight go into `SCALE_DEFS`, which is the single source of truth: the
instrument charts derive their intervals from it via `scaleDefIntervals()`
rather than keeping a second table, so each scale reaches the Scales module,
tonal centre, drone and every chart at once. Each also gets a ghost-parent
mapping, without which the fingering charts render the scale with no positions.

Verified: all eight interval sets checked against expected pitch sets at root C,
all 8 present in the chart table and resolving to a definition, all 8 with a
ghost parent, and `intonare_scale_audit.py` passes all 36 scales for both pitch
content and spelling.

## v0.150.21 — Six more Road Trip legs tuned, and all six pinned

Applied from device: `moonlight_3` refined again (third hook moved to b:76 /
s:18.52), and five legs taken off the converter's default spacing entirely —
`prelude_c`, `alla_turca`, `barcarolle`, `butterfly`, `moonlight_2`.

`prelude_c` is the notable one: it had real values but no `ms` fields at all,
and is now fully specified with them.

**All six added to the sentinel as pins**, which is the part that actually
matters. A hand-tuned leg with no pin can be silently overwritten by a
converter re-run and nothing would report it — the previous six tuned legs sat
unprotected for exactly that reason. 241 pins to 247. Tamper-tested one of the
new pins by reverting `butterfly` to its old values; the sentinel caught it.

Tuning status: **29 of 39 legs tuned, 10 still on converter defaults** —
fantaisie_impromptu, prelude_csharp, prelude_op23, raindrop, sonata_facile,
to_spring, traumerei, troika, waldstein_1, wedding_day. Detection is a leg whose
five `s` values are exactly 5/7/10/14/17.

(Worth recording: the first version of that detection reported zero untuned,
because `s:([\d.]+)` also matches the `s:` inside `ms:`, so every leg looked
hand-tuned. Anchored to `,s:` now.)

## v0.150.20 — Tapping TRAIN inside a folder left both hubs on screen

Exact repro from device: open the Reading folder, tap the TRAIN tab. The main
Train hub appeared and the Reading sub-hub stayed rendered underneath it, so the
READING folder card and the loose STAFF NOTES / NOTATION CARDS cards were all on
screen together.

Three bugs behind it, all now fixed at the source rather than patched:

**1. The reset only fired when LEAVING practice.** The condition was
`mode === 'practice' && m !== 'practice'`. Tapping TRAIN while already in
practice is `m === 'practice'`, so it was skipped: the main hub was revealed by
the `.train-only` toggle while the sub-hub was never hidden. Tapping the tab you
are already on is a normal way to ask for the top level of that tab, and now
behaves like one.

**2. The list of sub-hubs was copied in three places and was one short
everywhere.** `earTrainingHub`, `rhythmHub` and `gamesHub` were listed at all
three reset sites; `readingHub` was added later, with Staff Notes, and none of
the three copies were updated. That is why this was Reading-only. Replaced with
a single `PRACTICE_SUBHUBS` list and a `closeAllSubHubs()` helper, so a fifth
folder cannot repeat it.

**3. Found while testing: folders never hid each other.** Each `enterX()` hid
only `practiceHub` and showed its own hub, so opening Games while Reading was up
left both rendered. Not previously reported because leaving a folder normally
goes through `exitX()` first. Added `openSubHub(id)`, which shows one and hides
the rest.

Verified in a mobile-viewport browser across all four folders: exactly one hub
visible at every step, and TRAIN from inside any folder returns to the main hub.

## v0.150.19 — Nothing scrolled anywhere, because the scroll lock was guessing

Reported as the Tools tab not scrolling. It was not the Tools tab: a single
false positive in the overlay detector locks the WHOLE app, because
`body.scroll-locked` sets `position: fixed`.

Measured in a real browser rather than reasoned about. Two findings:

**The candidate scan was 409 nodes, not the ~130 the code comment claims.** The
substring selectors match an overlay's own children — `[class*="-sheet"]` alone
hits 116, because `mq-sheet-title`, `mq-sheet-handle` and `fav-sheet-body` all
contain "-sheet". Now filtered to outermost matches only: a child cannot be open
unless its parent is, and the parent is already in the list. **409 → 97.** That
is also a straight win for the Road Trip lag fixed in v0.150.17.

**Geometry alone is a guess, and the guess is now confirmed by hit-testing.**
Width, height, opacity and position can all say "overlay" about something that
is not actually covering the page. If something genuinely covers the page, then
the element at the centre of the viewport IS that element or lives inside it, so
`elementFromPoint` at the viewport centre settles it in one cheap call.

The failure here is asymmetric, which is why the stricter test is the right
trade: a false negative means a page scrolls behind an overlay (cosmetic), a
false positive means nothing scrolls anywhere and the app appears broken.

Verified in a mobile-viewport browser: unlocked on Tools, Train, Tuner and
Metro; locks correctly when the module picker opens; unlocks when it closes.
One deliberate behaviour change — the tour overlay no longer locks, because it
is a `pointer-events: none` backdrop and the hit test correctly reports it is
not blocking the page.

This detector has now caused three incidents (a 411-node scan, the Road Trip
lag, and this). If there is a fourth, it should stop inferring state from the
DOM and have overlays declare themselves on open and close, the way `rt-open`,
`mq-open` and `sg-open` already do.

## v0.150.18 — Three hand-tuned Road Trip legs applied

`maple_rag`, `entertainer` and `moonlight_3` were tuned on device but never
made it into the file — they had been pasted as reference in conversation and
read, not written. Diffed all 39 legs field by field to find exactly which
differed rather than trusting either copy; those three, and only those three.

`moonlight_3` changed substantially (every hook moved, e.g. the final hook from
b:40.99/s:5.92 to b:214.99/s:33.46). `maple_rag` and `entertainer` were smaller
adjustments to their opening hooks.

Sentinel pins for `maple_rag` and `entertainer` updated to match; both are
pinned legs and correctly flagged the change as drift.

Remaining untuned: 14 legs still carry the converter's default hook spacing
(s values of exactly 5/7/10/14/17) — alla_turca, barcarolle, butterfly,
fantaisie_impromptu, moonlight_2, prelude_csharp, prelude_op23, raindrop,
sonata_facile, to_spring, traumerei, troika, waldstein_1, wedding_day.

## v0.150.17 — Road Trip was crawling because of the scroll-lock observer

Reported as Road Trip being laggy, glitchy and hard to use in the first build
since v0.148.3. That is also the first build carrying the generic scroll lock,
and the lock was the cause.

The MutationObserver watches `class` and `style` across the whole body subtree,
so **every animated element in the app woke it up**. The work it wakes up to is
`_anyOverlayOpen()`, which calls `getBoundingClientRect()` and
`getComputedStyle()` on up to 133 nodes — both force synchronous layout. An
animation-dense screen was therefore paying on the order of 266 forced reflows
per frame. Road Trip, with constant map, marker and progress animation, was the
worst-hit screen in the app.

Two fixes:

**Ignore mutations that cannot change overlay state.** An attribute change only
matters if the element that changed is itself an overlay candidate. A progress
bar restyling itself cannot open or close an overlay, so it is now skipped
without touching layout at all. `childList` still invalidates the cached node
list, since a genuinely new overlay may have appeared.

**Bail entirely for modules that run their own lock.** Road Trip, Music Quiz and
Survival Guide each manage a full-screen lock (`rt-open` / `mq-open` /
`sg-open`) and their own internal scrolling. Scanning 133 nodes to decide
something they have already decided is pure cost. The generic lock now hands
over to them and returns immediately — clearing any stale `scroll-locked` and
restoring the saved scroll position on the way out, so the two systems cannot
fight.

Verified: zero overlay scans while `rt-open` is set, stale lock cleared, scroll
position preserved rather than lost on entry, and normal overlay locking
unaffected on every other screen.

## v0.150.16 — Backup export saves a real file you can actually find

v0.150.6 removed the share sheet and wrote straight to `Directory.DOCUMENTS`.
The write succeeded and the toast was honest, but on Android 11+ scoped storage
that path resolves INSIDE the app sandbox
(`/Android/data/com.lieutenantdan.intonare/files/Documents`), not the Documents
folder visible in a file manager. Reported as "toasts backup saved but no file".

Worse for this feature specifically: that directory is deleted on uninstall. A
backup whose entire job is surviving a phone change would have evaporated at
exactly the moment it was needed.

Android has no API for silently writing a non-media file to a public folder.
The sanctioned routes are the Storage Access Framework — no Capacitor plugin
exposes `ACTION_CREATE_DOCUMENT`, so that means a hand-written native plugin per
platform — or handing the file to the system sheet, which offers "Save to Files"
and lands it in real, visible, uninstall-proof storage.

Tier 1 now writes to CACHE and shares the file's URI. The original complaint was
a sheet full of raw JSON *text*, which is a message-sharing sheet with nothing
useful in it; attaching a real file changes what the sheet offers, so it reads
as a save dialog. Same tap count, a genuine file at the end.

A dismissed sheet no longer reports an error — cancelling rejects the same as a
failure, and only a failed write is worth shouting about.

Verified across seven branches: writes to CACHE not DOCUMENTS, hands over a file
URI, no raw text in the sheet, one success toast, silent on dismissal, text-share
fallback on write failure, tier 2 fallback with no Filesystem plugin.

### Full session re-verification
Every change from v0.150.3 onward re-checked in one pass: syntax across all 9
script blocks, version synced in all three spots, no duplicate IDs among the
elements touched, all 17 session fixes still present, all 11 new strings present
in both EN and IT, and every audit green — sentinel (97 fixes + 241 pins),
backup (50 keys + 43 fields), stopAll, audio handles, and state leak.

Note for future reads of the state-leak report: `_scrollLockRAF` now appears in
every action's changed-state list. That is the v0.150.3 scroll-lock coalescer, a
transient rAF handle rather than module state. Benign.

## v0.150.15 — A net under uncaught errors

The app had no `window.onerror` and no `unhandledrejection` handling at all.
For one 10 MB file with ~118k lines of JS and no framework error boundary,
that means a single uncaught throw inside a render or audio path leaves the
screen half-drawn: overlays stuck open, body still scroll-locked, notes still
ringing, no message. The person force-quits and the report reads "it froze",
which is unactionable.

Both handlers now recover instead. Order matters: audio first (the most
intrusive symptom), then the scroll lock (which otherwise leaves the page
unscrollable with nothing on screen explaining why), then one plain message.

Deliberately NOT crash reporting. Nothing is transmitted; there is no analytics
SDK in this app and adding one at 1.0 would mean a new Data Safety disclosure
for data that would not get acted on by a solo developer at launch. This only
makes one error survivable.

Details that matter:
- Every recovery step is independently guarded. The handler must never itself
  throw, or it becomes the thing that breaks the app. Verified by testing with
  a `stopAllAudio` that throws.
- A throw inside a rAF loop or audio callback can fire hundreds of times a
  second, so a burst collapses into a single recovery on a 4-second window.
  Verified with 200 consecutive errors producing one recovery.
- Resource load failures (a missing image also fires `error`) are ignored;
  only events carrying an Error object trigger recovery.

EN and IT strings both added.

## v0.150.14 — The dev-tools switch could ride a backup onto someone else's phone

`intonare_dev` was the last unclassified key in the backup audit, warning on
every run this session. It is the developer-tools switch: per-device on
purpose, set from a console, and deliberately granting no Pro. But it was
never told whether to travel, so it defaulted to travelling — meaning an
export shared by a tester would silently enable dev tools for whoever restored
it. Classified as skip.

The backup audit now passes clean for the first time in this session: all 50
persisted keys and 43 progState fields classified. That matters beyond the bug
itself — a gate that always warns is a gate that stops being read.

## v0.150.13 — In-app update card, with a real download-and-install flow on Android

Uses Google Play In-App Updates through `@capawesome/capacitor-app-update`.
Play is asked directly whether a newer build of the app exists, so there is no
version manifest to host anywhere and nothing to remember to bump at release
time — the store already knows. An earlier plan in this project's notes called
for a JSON file on GitHub Pages; that was the wrong approach and is dropped.

**Android gets the flexible flow.** Tapping DOWNLOAD pulls the new build in the
background with a live progress bar while the app stays fully usable, then the
button becomes RESTART and `completeFlexibleUpdate()` restarts and installs it.
The person never leaves for the Play listing.

**iOS cannot do this** — Apple does not permit in-app update flows — so there
the plugin only reports the store version and the button reads OPEN STORE. The
card's wording switches accordingly rather than promising an in-app install
that cannot happen. Same fallback if Play itself declines the flexible flow.

A dismissible card above the tab bar, not a launch modal: the entire point of
the flexible flow is that it does not interrupt, so a blocking overlay would
defeat it. It cannot nag — LATER snoozes for three days, and the snooze is
recorded per version, so declining once never hides a *later* release. The
check is also deferred behind the same launcher gate the daily streak toast
uses, plus its own delay, so it can never land on the splash or the chooser.

Feature-detected end to end: with the plugin absent (a browser, or any build
made before `npx cap sync`), every entry point no-ops silently.

`iu_snooze` is classified as backup-skip. It is a per-device "do not re-ask
about this version" note; restoring it onto a new phone could silence a
legitimate prompt there, and it rebuilds itself the moment one is dismissed.
The backup audit caught it unclassified before this shipped.

**Requires `npm install @capawesome/capacitor-app-update` + `npx cap sync`.**
Until then the card simply never appears. Note also that in-app updates only
report correctly for builds *installed from Play* — a sideloaded `go.bat` build
returns UNKNOWN forever, so this can only be verified through Play internal app
sharing, not the normal dev loop.

Verified across six branches: no update, update available, Android flexible
start, iOS store fallback, snooze suppressing the same version while still
showing a newer one, and silent no-op with no plugin.

## v0.150.12 — Notation symbols beside the Survival Guide's interactive terms

The Guide's tappable terms now carry their written symbol. Eight of the nine
have one: forte, marcato, fermata, decrescendo, tremolo, legato, glissando and
vibrato. `subito` does not and never will, since it is a direction rather than
a mark on the page.

No new assets were needed. `NC_CARDS` (the Notation Cards deck) already holds
181 symbols with Bravura codepoints and per-glyph sizing, and the embedded
Bravura subset already ships these glyphs. The codes and metrics are lifted
verbatim so weight and baseline match that deck instead of being re-guessed;
legato, glissando and vibrato are drawn SVG there rather than font glyphs, and
stay that way here.

**Badge strip, not inline glyphs.** Both were prototyped and reviewed on
device. Bravura's em-boxes vary enormously — a staccato dot is 4px tall, a
quarter rest 37px — so inline glyphs shove line-height around inside a
paragraph. The strip leaves the body typography completely untouched.

**Built at render time from the DOM**, not written into the page copy. The
body strings are duplicated across ten render branches, and `body`/`body_it`
are twins that drift when edited separately; reading `data-term` out of the
rendered card means the Italian page gets its strip for free and neither copy
carries markup for it. Hooked into `sgAttachTermListeners()`, which already
runs once per card, so there was one insertion point rather than ten.

Verified it dedupes repeated terms, skips terms with no symbol, sits above the
first body block, and does not duplicate the strip when a card re-renders.
Styled with theme vars only, so light mode needs no parallel block.

## v0.150.11 — A sound at launch with no toast behind it

Reported as the streak audio cue firing for the daily streak. Traced every
caller of `playCueMilestone()` first — the nine game-streak sites, the ×40
mythic card, Relative Pitch's bank/start, Music Quiz at 5/10/20, and the
settings preview. None of them is the daily streak, and the daily toast path
(`dtFireDailyToast` → `dtBuildInner` → `dtAnimToast`) plays no audio at all.
So the cue was not the streak cue.

The actual bug: achievement toasts were not queued at launch while the daily
streak toast was. `checkDailyStreak()` calls `checkAchievements()` directly,
and `_achShowNextToast()` fired immediately, sound included — but at boot
that lands on the splash or the launcher, where the toast itself is not
visible. The daily toast two lines below it already defers through
`_queueLaunchCelebration()` for exactly this reason, which is why it waited
and the achievement did not. The audible half of the achievement arrived
alone, near the daily toast, and read as the streak cue misfiring.

`_achShowNextToast()` now checks the same launch gate and re-queues itself if
celebrations have not drained yet, so the toast and its sound arrive together
once the person is actually in a module. Mid-session unlocks are unaffected —
the gate is only closed during launch. Verified the queued case does not
strand or double-fire toasts when several unlock at once.

The `typeof` guard normally used for this kind of check does not work on a
`let` in its temporal dead zone (it throws rather than returning
'undefined'), so the read is wrapped in try/catch instead.

## v0.150.10 — Tier toast shows the current multiplier

The toast now reads "OPEN reached! At least 200 points, ×2.0 multiplier."

Deliberately two separate numbers rather than one combined figure.
`rlpHavenValue()` returns a RAW value and the multiplier is only applied
later in `rlpSettle()`, so the honest reading of "at least 200 points" is a
floor that can only ever go up. `rlpMult()` moves the other way — it drops a
quarter every time a lifeline is spent. Multiplying them into a single
"at least 400 points" would have been a promise the game breaks the moment
the player uses 50/50 on the next rung.

Known display quirk, left as-is for consistency: `toFixed(1)` renders ×1.75
as "×1.8" and ×1.25 as "×1.3". The multiplier readout already in the climb
HUD rounds identically, so the toast matches what's on screen; the
underlying math is unaffected. Worth fixing in both places together if it
ever matters.

## v0.150.9 — A440 corrected to a one-time free start, tier toast now shows guaranteed points, feedback box no longer pops in and out

**v0.150.8 overshot on the A440 fix.** Made it free and unlimited for the
entire climb, when the actual ask was a single free A440 as an optional
start-screen option, with the in-game lifeline behaving exactly as before —
one-shot, costs a slice of the multiplier, same as 50/50 and Black/White.
Reverted the in-game lifeline back to its original behavior byte-for-byte,
and added a genuinely separate button on the climb's intro screen — "HEAR
A440 FIRST" — that plays the tone before the run starts and has zero
interaction with `rlpLives`/`rlpLivesUsed`, since it fires before either
exists for that run.

**The tier toast now says what it actually means.** Was "New tier: OPEN,"
which doesn't tell you anything useful mid-climb. Now reads "OPEN reached!
You've got at least 200 points" — the exact payout `rlpHavenValue()` already
computes for the safe haven you just passed, the same number the app already
shows if you choose to bank there. Verified the three tier boundaries resolve
to 200 / 1,600 / 11,000, matching `RLP_VALUES`.

**Interval Training's feedback box popped in and out of the layout every
round.** It was the only piece of the exercise screen doing that — Chord Ear
and Sing Sing's equivalent boxes are visible-but-empty from the start.
`ivFeedback` had `display:none` baked into its markup and got re-hidden on
every round reset; both removed, replaced with a plain class-and-text reset
so the box keeps its reserved space and just goes blank between rounds.

## v0.150.8 — A440 is free in Relative Pitch, a toast on each new tier, and Interval Training finally says "got it"

**Relative Pitch's A440 reference tone was costing you a lifeline.** The
climb has three lifelines — A440, 50/50, Black/White — and using any of them
dents your score multiplier, since 50/50 and B/W actually remove information
from the question. A440 doesn't; it's just a reference pitch, the same kind
of thing you can tap anywhere else in the app for free. It was still wired
into the same one-shot, multiplier-costing lifeline system as the other two.
Pulled it out: free, unlimited, no multiplier hit, replayable as many times
as you want per rung.

**Relative Pitch now toasts when you cross into a new difficulty band.**
WIDE → OPEN → CLOSE → ADJACENT, the four named tiers the climb steps
through. Fires exactly on the transition, using the same names already in
both languages.

**Interval Training's manual mode never actually said you got it right.**
The feedback box already existed and already had a `.got` (green, correct)
CSS style defined — Sing mode was already using it. Manual/tap mode's wrong
path filled the same box with retry text and a hint; the correct path just
marked the button green and left the box empty. Wired the correct path to
use the box too, with the same "★ GOT IT!" text Sing mode shows.

`intonare_regression_sentinel.py` needed a pin update for the Relative Pitch
band-change block — the toast call changed the exact code shape the pin was
watching. Updated pin ships alongside this build; needs re-uploading to
project knowledge since `/mnt/project/` doesn't save back automatically.

## v0.150.7 — Streak toast under the camera cutout, Chords defaulting to whatever tone you last touched

**The milestone streak toast (5/10/15…40) was never actually moved off the
camera cutout.** There are two different streak toasts: `dailyStreakToast`
("day streak at risk") sits at `bottom:90px` and was already clear.
`streakMilestoneToast` — the one wired into four more exercises in
v0.150.5 — was hardcoded to `top:20px`, a bare pixel value with no
relationship to the safe area, landing right where an Android punch-hole
camera commonly sits. Changed to `calc(20px + env(safe-area-inset-top))`,
matching the pattern used elsewhere in the file.

**The Chords tool showed and played whatever tone was last picked anywhere
else in the app, not piano.** Root cause: its tone bank read and wrote the
same app-wide `selectedRefTone` that Interval Training, Sing Sing, Chord Ear
and Charts all share — so browsing a saxophone voice in an ear-training
exercise, then opening Chords, left Chords sounding like sax too, with no way
to tell it apart from a deliberate choice.

Found a half-built fix already sitting in the file: `_rememberChordToolTone()`
persisted a `chordToolTone` preference whenever you changed Chords' voice,
with a comment saying it was meant to restore your choice on return "rather
than the charts' last instrument." Nothing ever read that preference back —
not the tone bank button, not actual chord playback — so the write was
completely dead. Wired it up for real: `chordInit()` now passes explicit
`get`/`set` hooks pointing at `chordToolTone` (default `grand_piano`) instead
of the shared fallback, `chordPlayMidi()` takes an optional tone override so
Chords' actual playback matches what the button shows, and the old
no-hooks refresh of Chords' buttons was removed from `pickTonePopup` — it
was overwriting the correct scoped display with the shared tone every time
you picked a voice anywhere else. Interval Training, Sing Sing and Chord Ear
still intentionally share `selectedRefTone` with each other; only Chords was
decoupled.

## v0.150.6 — Backup export stopped popping a share sheet

The Tier 1 export path (native platform, `@capacitor/filesystem` present) wrote
the backup file to CACHE and then handed it straight to the Share plugin, so
saving a backup always meant an extra manual step: pick where to send it. That
was the actual complaint, not the file format.

It now writes directly to `Directory.DOCUMENTS` and stops there. A toast
confirms the save; no picker. On iOS that lands in the Files app under "On My
iPhone" once file sharing is enabled in the native project; on Android it's
the app's own document storage. Same shape Tier 3 (plain browser) already had —
Tier 1 just wasn't taking it.

Falls back to the share sheet only if the direct write itself fails, same as
before.

## v0.150.5 — Streak toasts wired into four more exercises, a sax note leak, and a duplicate button id

**Streak milestones only fired in three of eight exercises that track one.**
`checkStreakMilestone()` — the 5/10/15…40 toast — was wired into Interval
Training, Sing Sing and Chord Ear Training. Tempo Lock, Tempo Guess,
Polyrhythm and Rhythm Reading all keep their own streak counters and none of
them called it. Added the call at each exercise's streak-update site, same
pattern as the three that already had it. Left Music Quiz alone; it already
has its own streak-aware celebration (XP toast text + haptics at 5/10/20) and
wiring the shared toast in too would have doubled up.

Second bug behind the same symptom: `_lastMilestone`, which stops a milestone
firing twice, only reset on entering six specific exercises. None of the four
above were on that list, so even with the wiring in place, hitting milestone
10 in one exercise and then 5 in another would not have fired — 5 is not
greater than the leftover 10. Added `rhythmread`, `tempo`, `tempoguess` and
`poly` to the reset list.

**Sax (and every wind instrument) kept a tapped note ringing through a
subfamily switch, while the scale run stopped correctly.** Two separate audio
paths: the scale run plays through `trpPlayNodes`, which `trpStop()` clears —
that's why switching subfamily killed it. A single note tapped on the
fingering chart plays through a different variable, `trpLastTapNode`, which
was only ever stopped by the *next* tap. `trpStop()` never touched it, so it
was never included when `chordScaleStopAllAudio()` runs on a subfamily
switch. Added the cleanup to `trpStop()`.

**The wind "Notes" screen showed "PLAY ASCENDING."** Root cause: the Notes
screen's single-note button and the Scale screen's run button shared the
literal same DOM id, `trpPlayBtn`. `getElementById` always resolves the first
match regardless of which screen is visible, so every scale function
(`trpPlay`, `trpStop`, `trpToggleDirection`, the chart-button registry reset)
was silently overwriting the Notes button's "PLAY NOTE" label with scale
text, while the actual Scale button on screen never updated at all. Not a
leak from a previous chart — a standing cross-wire that fired the same way
every time. Gave the Notes button its own id, `trpCardPlayBtn`, and a
registry entry, matching the existing `bowedNotePlayBtn` / `bowedScalePlayBtn`
split for the equivalent bowed-strings screen.

## v0.150.4 — Rhythm Reading never had a streak toast to lose

Reported as "no streak toast at 5 in Rhythm Reading." Turned out the toast had
never been wired up for this exercise at all — `checkStreakMilestone()` was
only called from Interval Training, Sing Sing and Chord Ear Training. Added
the call to Rhythm Reading's streak update. (v0.150.5 found and fixed the
same gap in three more exercises, plus a second bug in the milestone-reset
logic that would have kept blocking this even after the wiring landed.)

## v0.150.3 — Overlays could still be scrolled behind, on-device only

Reported as scrolling behind the module picker; confirmed to be every overlay,
not just the picker, and confirmed to only happen on-device, never in a
desktop HTML preview.

Cause: `body.scroll-locked` (added v0.149.0, the generic MutationObserver-
driven lock covering all 133 overlay-shaped elements) only set
`overflow: hidden`. That blocks mouse-wheel and click-drag scrolling on
desktop, which is why every preview looked correct. It does not reliably
block touch-drag in mobile WebViews — touch gestures can still drag body
content through `overflow: hidden` via momentum scrolling. The three other
full-screen locks already in the file (`mq-open`, `rt-open`, `sg-open`) knew
this and use `position: fixed` too; the newer generic lock, written after
those, missed it.

Added `position: fixed` (plus `left`/`right`/`width`/`height`) to
`scroll-locked`. Fixed positioning drops the body's current scroll offset, so
`_scrollLockSync` now saves `scrollY` before locking, applies it as an inline
`top`, and restores it via `scrollTo` on unlock — otherwise every overlay
open/close would have jumped the page back to the top.

## v0.150.2 — Opening the Transpose tool buzzed, and a spacing audit

**The Transpose tool vibrated when you launched it.** Not the launcher, and
not a card handler — every module card goes through the same `lnchGo()`,
which fires no haptic at all. The cause was inside the tool: `tpInit()`
calls `tpSemiStep(0)` to paint the initial semitone display, and
`tpSemiStep` fired `hapticLight()` unconditionally. One function doing
double duty as a setup call and a user action, so opening the tool felt
like pressing a button.

Now conditional on `delta`, so it buzzes when the value actually moves and
stays quiet during setup. Confirmed by counting haptic calls while opening
each of the fifteen tools in turn: previously Transpose was the only one
that fired, now none do.

**Added `intonare_spacing_audit.py`**, prompted by the chord tabs feeling
close to the card. The finding is that spacing is not unstandardised
randomly — it is CONTINUOUS. Every integer from 1px to 14px is in use, with
no gaps, plus 347 distinct padding values. A design system uses a scale;
this is per-component tuning by eye, which is why "does this gap feel
right" has no answer anyone can apply twice.

Against a 4px scale, 37% of values already fit. The biggest offenders are
6px (189 uses), 10px (149) and 5px (141), and there are one-offs at 26, 34,
38, 44, 72 and 76px that look accidental rather than chosen.

Nothing was changed. Snapping around 900 values to a scale would alter
every screen in the app, which is a design pass rather than a cleanup, and
not something to do before a release.

The audit is static rather than a runtime measurement, and that was a
deliberate second attempt. Measuring rendered gaps needs a reliable answer
to "is this element visible to the user right now", and getting it wrong
silently pulls in elements from hidden panels — the runtime version
confidently reported that all fourteen tools had identical 5px and 20px
gaps, which was nonsense produced by exactly that mistake.

Also measured haptic coverage while looking into this: 47 of 465 inline
handlers fire one, so about 10%. Not recorded as a fault, just a fact worth
having before deciding whether haptics should be everywhere or nowhere.

## v0.150.1 — The enharmonic toggle worked in the Player tab and not the Builder

Reproduced by reading the labels out of both grids in each mode: the
Player switches C sharp to D flat correctly, the Builder stayed on sharps
in all three.

The cause is one missing call. `chdSetSpelling` refreshes the Player's
root grid, then calls `chordBuilderUpdate()` for the Builder — but that
function refreshes the chord name, the staff and the selected note set,
and never touches the grid. Both grids label their buttons with the same
`gccRootDisplayName()`, which reads the same `gRootFlatOverride` set, so
the Builder's labels were correct code that simply never re-rendered after
the set changed. `chordBuilderUpdateGrid()` is now called alongside.

For the record, since it was asked: the toggle DOES force a spelling
rather than suggest one. Sharp and flat write every accidental semitone
into `gRootFlatOverride`, not just the selected root, so the whole grid
reads consistently. Auto does something different — it spells only the
current root, chosen by `chdPreferFlatRoot` from the chord context, which
is why it currently shows one label rather than both.

## v0.150.0 — Streak toast moved to the bottom, and the Chords tool stops inheriting the charts' voice

**The toast sat under the pinhole camera.** It was anchored to
`.session-bar`, the 4px hairline at the top of the screen, which put it
around y47 — directly under the cutout on most phones, where it was half
covered. It now anchors to the mode bar at the bottom, landing at roughly
y810 with the bar at 862, and the entrance animation already rises from
below so it reads correctly down there.

Worth recording why a CSS fix alone did nothing: `showMiniNotif` sets an
inline `bottom` every time it runs, and an inline value beats any
stylesheet rule. Adding `bottom` to `.mini-notif` computed correctly and
was then overwritten on show. The anchor itself had to change.

**Choosing a chart instrument changed the Chords tool's sound bank.**
`switchChordScaleInstrument` writes `selectedRefTone` on purpose, so a sax
chart plays with a sax voice — correct for charts. But the Chords tool
plays through that same shared variable, so it inherited whatever the
charts last selected.

The Chords tool now remembers its own voice and restores it on entry,
which keeps both behaviors right without the charts needing to know this
tool exists. Verified: pick marimba in Chords, switch a chart to sax, come
back, and it is marimba again while the chart keeps alto sax.

Checked whether the same leak exists elsewhere by snapshotting fifteen
tone and voice variables around a chart instrument switch. Only
`chordScaleInstrument` and `selectedRefTone` move; no other module's voice
is touched.

Three failed edits are worth noting rather than hiding: I assumed the
indentation of the line I was replacing and got it wrong twice, and the
assertion caught it both times so nothing was written — but the test then
ran against an unmodified file and reported failure as though the fix were
broken. Reading the exact line before editing would have been faster than
guessing three times.

## v0.149.2 — Two regressions from the scroll rule: touch scrolling and the launcher morph

Both reported, both mine, both from the same build.

**Modules could not be scrolled.** `body.scroll-locked` carried
`touch-action: none`. That does not merely stop the page scrolling behind
an overlay — it stops touch scrolling ANYWHERE, including inside the
overlay that is open, so the moment anything locked, the app went rigid.
It passed testing because a test sets `scrollTop` directly and never
produces a touch gesture, and the property has no effect on programmatic
scrolling. Removed; `overscroll-behavior: contain` already prevents scroll
chaining, which was the actual goal.

**The module picker's animation was cut short.** `lnchGo()` deliberately
keeps the launcher on screen while the chosen module builds behind it, and
calls `setMode()` during that hold — where the new `closeAllOverlays()`
force-hid it. The app appeared before the morph had finished. The launcher
is now excluded alongside the tour and splash, all three of which manage
their own dismissal.

Verified by sampling the morph frame by frame: the launcher holds solid
through 180ms, fades between 240 and 360, and is gone by 420. Through the
real dismissal path the lock releases afterwards, body overflow returns to
`hidden auto` and touch-action to `auto`.

Worth noting for future testing here: driving `enterTool()` directly
leaves the launcher up, because only `lnchGo()` dismisses it. That made
the harness report a stuck scroll lock in every tool, which looked exactly
like the reported bug and was not it.

## v0.149.1 — Checked the scroll rule for collateral damage, and found a real cost

Asked whether the new rule affects anything unintentionally. It did, in a
way that would not have shown up as a bug report until someone complained
the app felt sluggish.

**The observer was costing a third of a frame.** Each pass ran
`querySelectorAll` afresh and scanned 411 elements at roughly 5ms — on
desktop. On a phone that is a dropped frame every time a class changes,
which during any animation is constantly. Two causes:

The id patterns were loose substrings. `[id*="ray" i]` matches "grayscale"
and anything else containing those three letters, so the selector was
pulling in three times the elements that exist. They are now anchored to
the capitalised form the app's ids actually use.

And the candidate list was rebuilt on every mutation, when it only changes
if nodes are added or removed — which attribute edits, the overwhelming
majority, never do. It is cached and invalidated only on childList
changes. 5ms became 0.006ms.

**Everything else checked out.** Toasts and mini-notifications do not match
the overlay selector and do not lock anything. All 15 tools scroll normally
with nothing open. Overlays that need to scroll internally still do —
settings and progress both confirmed with the body locked.

One earlier result that looked alarming was my test's fault rather than the
rule's: walking every tool in sequence showed the paywall "open"
everywhere, because entering a Pro tool legitimately opens it and the loop
kept entering tools underneath it. With Pro granted and overlays closed
between each, no tool locks scroll.

## v0.149.0 — One rule for scroll locking, and tabs now close what's open

Two related requests, both handled at the app level rather than by fixing
the two instances reported.

**Background scrolling behind overlays.** The count explains why it kept
coming back: 133 overlay-shaped elements in the app, nine of which locked
body scroll by hand. Locking was a per-overlay responsibility that most
overlays never took, and there is no single show/hide mechanism to hook
either — `.active` (80 uses), `.show` (28), `.open` (17) and direct
`style.display` (54) are all in play.

So the page state decides instead of the call sites. A MutationObserver
watches for anything becoming visible and toggles one body class. Any
overlay added later is covered without touching this code. `overscroll-
behavior: contain` also stops a scroll gesture that reaches the end of a
scrollable overlay from chaining through to the page underneath.

**Tabs leaving drawers on screen.** Nothing tied overlay lifetime to
navigation, so a drawer open when a tab was tapped simply stayed there
over the new tab. `setMode()` now calls `closeAllOverlays()` first. The
tour and splash are excluded, since they manage their own lifecycle.

Three faults in my own rule, each found by testing rather than reasoning:

The first version locked scroll at rest. Four bottom sheets are parked
off-canvas with a transform while still `display:flex` and `opacity:1`, so
by every measure except position they looked open. Visibility now checks
the element is actually within the viewport.

The second version missed the exact two things reported. The module picker
is `#lnch` with class `lnch-entering`, and the progression drawer is
`#progSyncTray` — neither carries a keyword anywhere in its class list, and
the selector was class-only. It now matches on id as well.

And the observer clears a stale inline `overflow: hidden` when nothing is
open, because not all nine of the old manual locks restore it, which can
leave the page unscrollable with nothing on screen.

## v0.148.5 — Survival Guide term demos play through a different synth entirely

"It's synth audio" was the detail that solved this. Three earlier fixes and
the one before this all targeted the Guide's own `tone()` oscillators. The
term demos never touch them.

`sgPlayTermDemo` plays through `REF_TONES` — the app's reference-tone
synths, the same ones the tuner uses — via `tone.synth()`, `_org.synth()`,
`_piano.synth()` and `_guitar.synth()`. A completely separate subsystem
from anything `stopAllSounds` knew about. Legato in particular uses the
`seq` branch, which calls `tone.synth()` for each note of the sequence, and
none of the demo's branches appear in the oscillator scan that found the
last four sources, because they create no oscillators of their own.

**Six `.synth()` calls, zero captured returns.** Eleventh instance of the
fire-and-forget pattern in this app, and the one actually being heard.
`REF_TONES` synths return `{gain, stop}` and every call site was discarding
it, so nothing could stop a demo once it started.

All six now register with `_sgTrackHandle`, and `stopAllSounds` stops them
alongside the oscillators. Verified that the handle's `stop` takes no
arguments before calling it bare — the same assumption, made without
checking, is what caused the sampled-guitar bug in v0.145.0, where an
absolute time was passed to a function expecting a duration.

Worth recording why this took five attempts. Each fix was verified against
the thing it changed and never against the thing being reported. The
oscillator scan that found `toneSoft` and `playTempo` was thorough and
still missed these, because it searched for `createOscillator` and these
call a function that creates them somewhere else entirely. Searching for
what makes sound is not the same as searching for what plays sound.

## v0.148.4 — Survival Guide audio, fourth attempt: four more sound sources nobody had tracked

Still not stopping on backout. The first three fixes were each real and each
insufficient, so this time the module was enumerated rather than reasoned
about.

The plumbing was never the problem, and that is worth stating because it
absorbed two of the previous attempts. `stopAllSounds` is called by the
Guide's own `render()`, exported as `window.sgStopAllSounds`, and listed in
`stopAllAudio`, which `exitTool` calls. All verified at runtime. The chain
has been intact since v0.136.11.

**The tracking was incomplete.** v0.145.0 added node tracking to `tone()` and
stopped there. Scanning every function in the module for `createOscillator`,
`createBufferSource` and `SampleEngine.play` found four more:

    playTempo       the tempo-row click
    clk             its inner tick
    toneSoft        a THREE SECOND note, the worst offender
    sgPlayTermDemo  eight separate sources: two 3-oscillator voices,
                    an LFO, and an accent blip

Eleven sound calls in total that nothing could stop. `toneSoft` alone runs
for three seconds, so backing out during one guaranteed audio survived the
screen.

All of them now register with `_sgTrack`, a single helper next to the
registry, so any future sound source in this module has one obvious place
to hand its nodes.

One flaw in the stop loop found while wiring it: the term demo's LFO has no
gain of its own, and the loop read `rec.g.gain` inside the same try block as
the oscillator stop — so the throw on the missing gain skipped `.stop()`
entirely and the LFO would have kept running. Gain handling and stopping are
now separate.

Cannot be verified headlessly: these functions live inside an IIFE and are
not reachable from a test harness, which is also how the original gap went
unnoticed. Needs a device check.

## v0.148.3 — Five rhythm hints described the wrong beats

Questioning the backbeat wording turned up something worse than prose.
Checking the hints against the actual note arrays found five that name
the wrong positions. `n.p` is measured in beats from the bar, so p:1 is
beat 2, and that made the claims checkable:

    five_four_groove  rest is on BEAT 2          hint said "the and-of-2"
    cascara           rests on and-of-1, and-of-3 hint said "the and of 2 and 4"
    mozambique        rest is on BEAT 2           hint said "an offbeat rest"
    guajeo            rests on 1, 2, and-of-3     hint said "1 and the and-of-2"

Someone tapping along and trusting the hint was being told the wrong
thing, which matters more in a rhythm trainer than any amount of cadence.
All four corrected against the data.

The fifth, `eighth_rest`, was accurate but read as a contradiction: the
rests really are on 2 and 4, and calling that "silence on the backbeat"
invites the obvious objection, since backbeat means those beats
accented. Rewritten to say what actually happens, that the rests land
where the accent is expected.

Swept every card with a verifiable rest claim afterwards; no others
disagree with their note data.

Worth recording the sequence: a question about a word led to checking a
musical claim, which led to finding four false ones. The copy pass was
looking at rhythm and cadence while the sentences were wrong about the
rhythm.

## v0.148.2 — Rewrote the "house style" hints too, because the consistency was the tell

Correct pushback: I wrote most of this text, so "house style" is really
"my style", which is the thing being removed. Preserving it was preserving
the problem.

The dash was never the real fingerprint. **334 blurbs sharing one
construction** was. Every rhythm hint ran [label] — [gloss]. [extra
sentence], with no exceptions across dozens of entries. A person writing
sixty-five of these drifts: some open with the count, some with the
instruction, some with what it sounds like, some are blunt because by the
fortieth one you get terse. Perfect uniformity is what reads as generated.

Twenty-two rewritten so that no two share a shape:

    The cornerstone of all rhythm — four even quarter notes per bar.
    Four even quarter notes per bar. Everything else is built on this.

    Beats 1 and 3 — the downbeat. Your feet would land here in a march.
    Beats 1 and 3, where your feet land in a march.

    Almost nothing — two hits, lots of silence. The rests are the challenge.
    Two hits and a lot of silence. The rests are the hard part.

    Syncopation inside 5/4 — already asymmetric, now off-beats too.
    5/4 is lopsided enough before you add off-beats.

Sentence lengths vary deliberately, several lose a sentence entirely, and
contractions are in where a person would use one — "you'll lose it" rather
than "you will lose it". That last one cost two syntax breaks: apostrophes
inside single-quoted strings. The stiff workaround was written first, then
replaced with proper escaping, because avoiding contractions to dodge an
escaping problem is how prose ends up sounding like a manual.

43 hints still carry a dash and the remaining content areas are untouched.
This is a reading job, not a pass; it goes at the speed of actually
reading each line.

## v0.148.1 — Read the rhythm-card hints properly, which the automated pass could not

Fair correction: cadence is not something a rule can see, and the previous
build proved it. 205 of 237 replacements landing on a colon is itself the
tell — no editor's mix looks like that.

The classifier's specific blind spot, now demonstrable: it treated
"Downbeat is a rest — your first hit is the and-of-1" as house style,
because the text before the dash is short. But that is two clauses, not a
label and its gloss. Length is not the distinction; grammar is, and
telling them apart means reading the sentence.

Read all 83 hint fields containing a dash. Most really are house style and
were left exactly as they are: "The cornerstone of all rhythm — four even
quarter notes per bar", "3+3+2 eighth-note grouping — three uneven hits
that underpin reggaeton". Eighteen were genuine AI cadence and are
rewritten by hand, individually:

    Beat 1 is silence — feel the empty downbeat
    Beat 1 is silence. Feel the empty downbeat

    Rest on 1 then an eighth — the first hit is pushed off the beat
    Rest on 1 then an eighth, so the first hit is pushed off the beat

    Hemiola in both bars — three-against-four feel sustained across two bars
    Hemiola in both bars, three-against-four sustained across the pair

Several were recast rather than repunctuated, which is the part no rule
reaches: "so the first hit is pushed off the beat" says the same thing
with a joint instead of a hinge, and "sustained across the pair" drops a
repetition the dash was hiding.

Also swept the previous build's colons for ones sitting in front of a full
clause, which is the damage that pass was most likely to have done. Two
turned up; one was a legitimate list, the other is fixed.

The remaining areas — Survival Guide prose, vocal range references, tool
blurbs — need the same treatment: read, not matched.

## v0.148.0 — Em-dash copy pass: 237 AI-cadence dashes rewritten, house style kept

Scanned every user-facing string for AI-speak. The result was lopsided:
576 em-dashes across 364 fields, and almost nothing else — four
"powerful/amazing", three "simply", one "seamless", one "not just X but
Y". The prose is in decent shape; the punctuation was the tell.

**Not every em-dash is AI cadence, so they were classified rather than
stripped.** The app's voice uses a label followed by its gloss, which is a
deliberate house pattern: "SAFE (under 70 dB) — no risk at any duration",
"Dotted quarter into eighth — the classic waltz lilt". 334 of those were
left alone. The other 237 are mid-sentence appositives, the rhythm that
reads as machine-written, and those are rewritten.

Replacement chosen by what actually follows the dash rather than a single
substitution: a full independent clause takes a semicolon, an imperative
becomes its own sentence with a capital, a participial phrase takes a
comma, and a noun-phrase gloss takes a colon. Final mix was 205 colons,
16 semicolons, 12 commas and 4 new sentences.

Also fixed `dt_streak_generic`, which read "days. keep going." in English
and "giorni. continua così." in Italian — lowercase after a full stop in
both.

Two things worth recording about how this went. The first classifier
called 219 of 237 semicolons, which would have been ungrammatical
wherever a fragment followed; semicolons need an independent clause on
both sides. And a capitalisation sweep run as a separate step duplicated
words ("Keepkeep") because of nested capture groups — that build was
discarded and the whole pass redone as a single operation with
capitalisation handled at the point of replacement. Nothing shipped in
between.

`COPY_PASS_REPORT.md` lists all 237 changes with their context for review.

## v0.147.1 — Dev code gets its own confirmation, and a way out that doesn't need the code

The developer code was reusing the Pro unlock modal, which congratulates
you on a purchase — the wrong message when what actually happened is that
six testing tools appeared. It now grants Pro quietly and shows a "DEV
TOOLS ON" notification instead, saying what turned on rather than
celebrating a transaction.

Added an **"Exit developer mode"** button at the bottom of Settings,
rendered only while dev mode is on. Entering the code again already
toggled it off, but that requires remembering the code; a visible way out
is better. It leaves Pro alone deliberately — the code granted it, and
silently revoking it on the way out would be a surprise — and confirms
with "DEV TOOLS OFF".

Two ordering faults found by testing rather than reasoning, both mine:

The Reset Pro button's visibility was only recomputed when the Settings
panel refreshed, so enabling dev mode left it hidden until Settings was
reopened. It is now updated by the dev toggle itself.

And even after that, it still didn't appear: `setDevMode(true)` ran BEFORE
Pro was granted, and the button's condition is "dev mode AND Pro", so the
check ran while Pro was still false. Granting Pro first fixes it. Worth
recording because the symptom — a dev code that looks like it half worked
— had two independent causes and fixing the first one changed nothing
visible.

Verified: the exit button is hidden before the code and visible after,
both dev buttons appear together, the purchase modal does not fire, the
notification reads DEV TOOLS ON, exiting hides both buttons again, and Pro
survives the exit.

## v0.147.0 — Every developer tool behind one code, and the iOS bypass restored

**The iOS beta bypass is back.** Removing it was premature: iOS is still
on TestFlight, it has no StoreKit IAP wired, and Apple rejects builds that
gate features behind a purchase path that does not work. It is scoped to
`isIOS() && isCapacitor()` so Android, desktop and the iOS PWA are
untouched, with the submission constraint recorded beside it.

**All six developer tools are now behind a single code.** Found by
searching rather than listing from memory, which turned up two nobody had
mentioned:

  · the Reset Pro button, which revokes a purchase
  · CALIBRATE on Survival Guide photos
  · UNLOCK ALL, the bulk achievement unlocker
  · long-press on an achievement to unlock just that one
  · the Road Trip leg tuner, on a long-press of the brand pill
  · `injectMockData`, which overwrites real progress with a fabricated save

Each function guards itself rather than relying only on its button being
hidden, because they are all reachable as globals.

**The dev code is deliberately NOT the tester code.** `INTONARE_AMICI` is
already the friends-and-family Pro unlock, so reusing it would hand every
tester a button that revokes their own Pro and a tool that overwrites
their progress. Developer tools use `DEV_CODE` — currently
`INTONARE_OFFICINA` — entered in the same Settings field, case
insensitive. It grants Pro as well, since every tool assumes access.
Entering it again turns the tools back off, so there is a way out that
isn't clearing site data.

The mode persists in localStorage rather than living in source, because
the build output is always plain `Intonare.html` and a source flag would
be overwritten by the next download.

Verified in both states. With no code: every tool is a no-op, the UNLOCK
ALL button is hidden, and entering the TESTER code grants Pro while
leaving dev mode off. With the dev code: it is accepted case-insensitively,
Pro is granted, the flag persists, all tools work, and entering it again
turns them off.

`intonare_dev_flag_audit.py` now checks all six gates and fails if the two
codes are ever made identical.

## v0.146.1 — Dev tools become a runtime toggle, and the iOS unlock is deleted rather than gated

v0.146.0 put three testing affordances behind a build-time constant. Two
things about that were wrong.

**A build-time flag is the wrong shape here.** Android is in production
while iOS is still on TestFlight, and both ship from ONE file. A source
constant would have to be edited per build and would be overwritten by the
next download. `INTONARE_DEV` is now read at runtime from a localStorage
key, so it ships off and is enabled per-device:

    localStorage.setItem('intonare_dev', '1'); location.reload();

Nothing behind it grants Pro, deliberately — so even if someone finds the
switch, the only things exposed are the Reset Pro button and the
Survival Guide CALIBRATE tool.

**_iosBetaUnlock is deleted, not gated.** It returned true for any native
iOS build and `isPro()` consulted it, so a public iOS release would have
handed Pro to every customer. Gating left that one boolean away from
happening. `tryUnlockCode()` with `UNLOCK_CODE` already lets a TestFlight
tester grant themselves Pro, so it was redundant as well as dangerous.
`isPro()` now depends on purchase state alone.

**Its original comment recorded a real App Store constraint, which is kept
in place rather than deleted with the code:** iOS has no StoreKit IAP
wired (the RevenueCat key is Android-only), and Apple rejects builds that
gate features behind a purchase path that does not work. That bypass
existed so review never met a dead purchase button. Before an iOS
submission, either StoreKit IAP must actually work or Pro must not be
gated on iOS for that build. Android is unaffected — RevenueCat works
there and this removal is what makes the Play Store build correct.

Verified both states: with no key the flag is false, a fresh install is
not Pro, the Reset button computes to display none even with Pro active,
calling `resetProTesting()` is a no-op, and the unlock code path still
exists. With the key set, the flag is true and the reset works.

`intonare_dev_flag_audit.py` updated to match — it now also fails if
`_iosBetaUnlock` reappears or if `isPro()` starts consulting anything
besides purchase state.

## v0.146.0 — Development hooks gated behind a single flag, with an audit that refuses to ship them live

Three testing affordances were sitting in the shipping file, each a real
problem in front of a paying customer rather than merely untidy.

`_iosBetaUnlock()` returned true for any iOS Capacitor build, and `isPro()`
consults it — so a public iOS release would have handed Pro to every
customer for free. The "Reset Pro (testing)" button appears in Settings
whenever Pro is active and REVOKES it; a customer could have tapped it and
destroyed what they bought. And the CALIBRATE button on Survival Guide
photos is a label-positioning tool with no meaning to a user.

All three are now gated on one `INTONARE_DEV` constant, declared beside
the version string where it can't be missed, and set to false. Gated
rather than deleted so the tooling still exists for development —
switching it on restores all three at once.

`resetProTesting()` also refuses to run outside a dev build regardless of
the button. It is a global function that destroys a purchase, and hiding
its button is not the same as making it safe.

Verified against a production build: the flag is false, the iOS unlock
returns false, `isPro()` is no longer true merely from running on iOS,
the reset button computes to `display: none` even with Pro active, and
calling `resetProTesting()` directly is a no-op.

**Added `intonare_dev_flag_audit.py`**, which exits non-zero if the flag
is true or if any of the four gates is missing, so it can gate a release
script. The point of the flag is that shipping is now exactly one boolean
away from unsafe; that is worth a machine check rather than a memory.

One consequence worth being explicit about: **TestFlight builds will no
longer grant Pro automatically** unless INTONARE_DEV is set true for those
builds. That is the correct behavior for a production binary, but it will
change what iOS testers see.

## v0.145.4 — Checked subdivisions, not just tempo numbers; bossa was still playing at double

Asked whether the subdivisions had been verified — whether a tempo that
reads correctly might still be playing in double or half time. It had
not been checked, and the question found something.

**Meter is sound: zero mismatches.** Every progression's time signature
matches its groove's beat count, so nothing is structurally stretched or
compressed.

**But several grooves declare a TWO-BAR cycle written into 16 steps,
while the engine plays those 16 steps across 4 beats — so the tempo a
listener hears is double the number in the preset.** Comparing tempo
figures cannot reveal that; it only shows up by computing the real
duration of one cycle and asking what style tempo it corresponds to.

Effective tempos, computed rather than assumed:

    salsa          app  90  ->  180   salsa runs 160-220        ok
    salsa_ii_v     app  95  ->  190   salsa runs 160-220        ok
    samba          app 130  ->  260   samba runs 130-320        ok
    bossa_251      app  88  ->  176   bossa runs 70-120         TOO FAST
    bossa_tritone  app  88  ->  176   bossa runs 70-120         TOO FAST

So the salsa correction in v0.145.2 was right, and the bossa correction
in v0.145.3 was not enough — 88 sounded like samba rather than bossa.
Both bossa progressions are now 60, an effective 120 and the top of the
typical range. Documented in place so the next person doesn't "fix" them
back up.

The general point, worth keeping: a tempo number is meaningless without
knowing how many bars the pattern spans and how many beats the engine
gives it. Two of the last three tempo passes compared numbers and drew
the wrong conclusion; the one that computed cycle durations found the
real answer.

## v0.145.3 — Researched the remaining tempo outliers; most were already right

The ratio table in v0.145.2 flagged six progressions whose tempo differed
sharply from their groove's suggested figure. Researched each rather than
assuming the same units mismatch applied, and the answer for four of them
is that nothing was wrong.

**Soleá (108) and bulerías (200) are correct.** Flamenco sources put
soleá at roughly 70-120bpm and bulerías at 160-275 counting compás beats,
which is exactly what the progression tempo represents. The compás
groove's `suggestedBpm` uses a different reference; the progressions are
right and were left alone.

**The waltzes are correct.** Waltz sits around 114-130 in practice, which
is where `country_waltz` (132) and `folk_waltz` (116) already are.
`ballad_34` at 72 and `minor_waltz` at 84 are deliberately slow jazz
waltzes, a real thing rather than a units error.

**Rhythm changes at 180 is correct.** Sources describe it being called at
200-340 at jam sessions with 144 as a learning tempo, so 180 is a
sensible practice speed rather than a mistake.

**Compound Jazz at 160 is correct, and the ratio explains itself.**
160 ÷ 3 = 53.3, which is the nine_eight groove's suggested 53. Nine-eight
groups into three dotted quarters, so the groove quotes the compound
pulse and the progression quotes the eighth-note pulse. Identical tempo,
two units — the same class of confusion as salsa, but harmless here
because both figures describe the same speed.

**One genuine correction: Bossa (tritone sub) was 128, now 88.** Bossa
nova runs roughly 70-120bpm, with teaching guides giving slow 56, medium
72 and fast 96, and the pattern is a two-bar cycle. 128 ran it fast and
out of style, and its sibling `bossa_251` was already at 88.

Worth recording the general lesson: a tempo that looks wrong against a
groove's suggested figure is usually a units difference, not an error.
Salsa was a real fault because the two figures described genuinely
different speeds; the rest describe the same speed counted differently.

## v0.145.2 — The preset chip leak was in the DOM, and salsa was running at double speed

**The drum module's preset chip still showed the progression's beat.** The
state was being handed back correctly — the variable restored, verified —
but `_rcApply` assigned `dk_loadedPresetName` directly while
`dkUpdatePresetLabel()` is what writes both the variable AND the visible
`#dkPresetLabel` element. So the chip kept displaying whatever
`loadPreset` last wrote. The leak was in the DOM, not the data, which is
why every state-level check said it was fixed. Restore now goes through
the updater.

**Clicking the Custom category didn't reset like CLEAR did.**
`_applySnapshot` handles patterns, kit, swing and bars but never touched
the preset label, so switching to Custom left the chip naming the preset
you had just come from. Both paths now behave identically.

**Salsa was running at double speed, and the cause is a units mismatch
that affects more than salsa.** Dance sources quote salsa at 160-220bpm
while DJs call the same records 89-100 — the same music described two
ways, differing by exactly 2x. The montuno and clave grooves are TWO-BAR
cycles written into 16 steps and authored at `suggestedBpm: 90`, the
half-time figure. The salsa progressions carried 180 and 190, so the
montuno played at literally twice the tempo it was written for. Now 90
and 95, with the convention documented on the groove so it doesn't get
"corrected" back.

Checking every progression against its groove's suggested tempo rather
than just this one found five more at roughly 2x, all of them grooves
with a two-bar cycle in 16 steps: compound_jazz (3.0x), solea (2.25x),
bossa_tritone (1.97x), bulerias (1.82x), and two waltzes at roughly half.
Those are left alone for now — each groove's cycle note needs reading
before assuming the same fix applies, and guessing at five more tempos
after this session is exactly the wrong instinct. The ratio table is
reproducible.

## v0.145.1 — Three device findings, traced rather than guessed

Taken one at a time, each verified before moving to the next.

**The flamenco beat sounded like twelve hits in a row.** In this engine a
step value of 1 is a GHOST NOTE, not silence — the scheduler passes
`val === 1` as the ghost flag and still triggers the voice. The preset
put a 1 on every non-accent step, so the clave fired on all twelve, seven
quiet and five loud, which on a sharp percussive voice reads as a stream
rather than a compás. The compás IS the accent figure, so only the five
accents sound now: 3, 6, 8, 10, 12, with kick on the two structural
pillars.

**The drum module's preset chip showed the progression's beat name, and
progression presets changed names without changing audio.** Both are the
same root cause, found by tracing the state through the whole flow rather
than reasoning about it.

`progLoadPreset` had TWO captures. The first is correct: borrow the
engine, apply the preset's beat, save the result as Progression's setup,
hand the drum module back. The second — added in v0.137.8 to store an
explicit choice — then ran unconditionally, and by that point the globals
had already been restored to the DRUM MODULE's state. So it captured the
drum module's pattern and label and saved them over the beat that had just
been stored. The progression ended up holding the drum module's pattern
under the preset's name: names changed, audio did not. That second capture
now only runs when the preset brings no beat of its own.

The Progression tray's beat cards had a related fault: they called
`loadPreset(p)` directly with no borrow at all, writing the drum module's
live pattern, kit and preset label. That is why the chip named the
progression's beat. They now borrow first, exactly as the preset path
does, and use `progSetBpm` rather than `setBPM` so no re-anchor fires.

Verified as a full sequence rather than in pieces: with the drum module
on Basic Rock at 96bpm, loading a progression preset leaves its pattern,
label and tempo untouched; the progression stores the flamenco beat;
playback runs that beat at ts 6; and after handback the drum module is
bit-for-bit as it was. The tray card path passes the same test. The state
leak audit now shows "PROGRESSION loads a preset" touching only `prog*`
variables, with the `dk_*` writes gone.

## v0.145.0 — Device testing round: a self-inflicted regression, and the sampled-note stop bug behind it all

Five findings from testing on hardware. One is a regression I introduced,
one is a bug that has been in the app the whole time, and it explains a
symptom that looked instrument-specific.

**Progressions skipped their first bar.** Mine, from v0.139.0. Giving
Progression its own tempo meant calling `setBPM(progBpm)` as it started,
and `setBPM` debounces a `_scheduleRetime()` which — by its own comment —
cancels pending audio and restarts every track's pattern from phase zero.
Correct when someone drags the tempo slider; catastrophic when the
progression is mid-launch, because the retime fires a moment later and
restarts what had just been aligned. Added `_setBpmNoRetime`, used
wherever tempo is loaded into or restored from the engine rather than
changed by a user. Also removes the same hazard from the context restore
on stop and from live tempo changes during playback.

**Fretted guitar kept playing through a subfamily switch while 12-string
stopped.** That asymmetry was the clue. `SampleEngine.play` returns a
handle whose `stop(releaseSec)` takes a DURATION; `gccStop` was calling
`n.stop(t + 0.12)` with `t = ctx.currentTime`, an absolute audio time.
So tau became the current clock value — thousands of seconds — meaning
the gain decayed over roughly twenty minutes and the buffer source was
scheduled to stop about ninety minutes out. The note never stopped. Only
sampled voices were affected, which is exactly why 12-string behaved: it
returns a composite handle that calls `stop()` with no argument and gets
the 0.04 default. Every other chart stop passes `stop()` or `stop(0)` and
was already correct; this was the single site.

**Survival Guide audio still didn't stop.** Third time, and the previous
two fixes were both real but neither was sufficient: the function is
exported and correctly listed, and `exitTool` does call `stopAllAudio`.
The remaining problem was the tenth instance of the fire-and-forget
pattern — the Guide's `tone()` created an oscillator, started it and
returned nothing, so `stopAllSounds` could only clear pending timers
while anything already sounding ran to full length. Tones are now tracked
and faded out, with self-pruning so a long session doesn't accumulate
finished oscillators.

**The new Flamenco Compás beat never appeared in the Progression tray.**
The tray filters its beat list by time signature, and the flamenco
progressions are `timeSig: [6, 8]` while the preset was `ts:12` — the
most literal reading of a twelve-beat cycle, and silently excluded.
Re-expressed as `ts:6` with `globalSub:2`: identical twelve-step array,
same accents, now matching the meter the progressions are actually
written in. It appears in the tray and shows as selected.

**CLEAR left the preset pill naming a preset that was no longer loaded.**
It reset the kit, swing, category and pattern but never the label.

Still outstanding from this round and not addressed here: the drum kit
module reportedly still being overridden by a progression. The state leak
audit reports clean, so whatever is happening is outside what that
instrument can see, and it needs its own pass rather than a guess.

## v0.144.1 — Sanity sweep after the compás work, which found two drum presets that never loaded at all

Re-ran everything after the content change: all seven project audits pass,
all 15 tools open, the audio path still installs its lookahead limiter at
0.7 headroom, both global stops are clean and the rhythm context is
released. Every progression preset resolves its drum preset by name and
every groove id it names exists.

The sweep did turn up two failures, and checking the pre-session build
confirmed they are not from this work: **2/4 Polka and 2/4 March threw on
load and always have.** `TIME_SIGS` had entries for 3, 4, 5, 6, 7, 9, 11
and 12 but not 2, so `loadPreset` read `.label` off undefined and gave up.
Those two presets have been unloadable rather than merely mis-tuned.

Added the missing 2/4 entry, shaped like the 3/4 and 4/4 rows: four
sixteenths per beat, eight at 32nd resolution, fill rows naming the
sixteenth positions. Both presets now load with their tracks populated
and the sequencer UI builds for them. 63 of 63 drum presets load, up from
61.

Worth noting how it surfaced. The check that found it was "load every
preset and see what throws", which is not something any existing audit
does — the groove audit checks musical content and the sentinel checks
that known fixes survive, but nothing tried to actually use each preset.
A whole time signature was missing from a lookup table and nothing
noticed.

## v0.144.0 — A real flamenco compás drum preset, and a correction to my own reading of the pairings

Asked to check the progression preset pairings against what the styles
actually do. Two findings, and one of them is me being wrong.

**The grooves themselves are well researched and correct.** Checked
against sources rather than assumed. `compas` (Soleá) accents steps 3, 6,
8, 10 and 12, which is exactly what the flamenco literature gives.
`flamenco` (Bulería) accents 1, 4, 7, 9 and 11, which looks wrong until
you account for bulerías starting its cycle on beat 12 — rotate so 12 is
step one and it becomes 12, 3, 6, 8, 10. Correct, including the
rotation. `son32` is a textbook 3-2 son clave. Whoever built this library
did the work.

**Salsa was fine.** The suspicion that the salsa progression doesn't use a
salsa beat was reasonable but wrong: it pairs `montuno` with `Son Clave`,
and those ARE salsa — montuno is the piano guajeo, son clave the
underlying clave. There is no groove named "salsa" because salsa is built
from those parts.

**I was also wrong about `funkback`.** I flagged it as a lazy catch-all
used by thirteen presets including Pachelbel's Canon and the cadence
demos. Its id misled me: the preset is `name: 'BACKBEAT'`, accents on 2
and 4, with a cited source, and it is the fundamental rock and pop
backbeat. Pairing it with three-chord pop, the Axis progression and
cadence demonstrations is correct. I judged it by its identifier instead
of its contents, which is the same mistake this session has caught
elsewhere. No change made.

**The one real defect: flamenco had no correct drum pairing.** Both
`bulerias` and `solea` used "6/8 Feel", and the compás is not 6/8 — it is
a 12-beat cycle grouped 3+3+2+2+2, usually notated in 3/4. "12/8 Blues"
would be no better, being four groups of three. Nothing in the library
fit, so this adds one.

`Flamenco Compás` is `ts:12` with `globalSub:1`, so one step is one
compás beat, which is how flamenco is actually counted rather than
burying the cycle inside a subdivision. Written on `clave` because the
real timekeeper is palmas and clave is the closest voice in the kit, with
kick marking the structural pillars at 12 and 6 the way a cajón bass tone
does. One preset serves both palos, since soleá and bulerías share the
accent pattern and differ in tempo and feel — soleá around 70-120bpm,
bulerías 160-275, and the progressions already carry their own tempos of
108 and 200 respectively.

Verified the accents land on exactly 3, 6, 8, 10, 12, that the preset
resolves by name, and that both progressions now point at it.

## v0.143.1 — The Interval Reference tour named controls that don't exist

Asked to check the tour actually reads correctly rather than merely
existing, which was the right question. It exists, its five selectors all
resolve, and its claims about the card check out — short name, full name
and semitone count are each real elements. But its third step described
buttons by names the app never uses.

The direction row's buttons read **Up**, **Down** and **TOGETHER**. The
tour body said "**Ascending** and **descending** play the notes one after
the other; **harmonic** plays them at once" — three bolded words, none of
which appear on any button. Bolding in these tours means "this is the
control you are looking at", so it was pointing at things that weren't
there. The step's own title had it right, "Up, Down or Together", while
its body invented different vocabulary. Italian had the identical
mismatch: buttons say Su, Giù and INSIEME, the body said Ascendente,
discendente and armonico.

Reworded so the bold names match the buttons while the musical terms stay
as explanation: "**Up** and **Down** play the notes one after the other,
ascending or descending; **Together** sounds them at once."

Swept every other tour for the same fault by collecting each bolded word
and checking it against the app's visible UI strings. That produced 53
hits and almost all are false positives — bolded phrases like "press and
hold the title" or "rushing" are ordinary emphasis, not control names.
The handful that did look like labels (the sing-sing modes, HEAR AGAIN,
NEW ROUND, TAP MODE, Strum) all resolve to real UI text. So the interval
reference was the outlier, and it was found by reading the tour against
the module rather than by any pattern match — worth recording, because
the automated version of this check is too noisy to gate on.

## v0.143.0 — Interval Reference gets its own tour; it was the only module without one

Reported as the interval reference showing the main tour. Auditing every
module against `TOURS` found the cause: `intervalref` was the only tool
or exercise in the app with no tour of its own. All fourteen exercises
have one and every other tool has one.

So the fallback was working exactly as designed — `startTour()` drops to
the overview when a module has no entry, deliberately, because a
section-level tour would target elements hidden behind the open tool and
close instantly. Nothing was mis-mapped; the tour simply didn't exist.
Confirmed by resolving the key with and without the new entry: with it,
`intervalref`; without, `overview`, which reproduces the report exactly.

Written to match the existing tool tours in structure and voice, five
steps in both languages: the card and what it shows, HEAR IT, the
up/down/harmonic row (the same interval sounds different depending on how
it's played, and harmonic is how you meet it inside a chord), the jump
row, and the voice picker.

Two mistakes in my own new copy were caught by running the audits rather
than by review: an HTML entity in an Italian title — `Su, Gi&ugrave; o
Insieme` — which is precisely the fault fixed one build ago in v0.142.2,
and it would have rendered literally for the same reason. Plus a British
spelling and an em dash the tone audit flags. All three corrected, and
both audits are back at their baselines.

Verified: five steps, every selector and preview selector resolves inside
the open tool, both languages complete on every step, and no entity
remains in any title.

## v0.142.2 — Tour titles showing raw HTML entities, in English and worse in Italian

Chased the "tour ampersands" report and it turned out to be the reverse
of missing: two English titles were showing a literal `&amp;`.

Tour titles render through `textContent`, not `innerHTML`. A bare `&` is
therefore correct and displays as an ampersand, while `&amp;` displays as
the five characters `&amp;`. Twelve titles used a bare `&` and were fine;
`rhythmcards` step 2 read "Pick &amp; Blend Categories" and `cof` step 3
read "Sharps &amp; Flats". Both had been HTML-escaped for a context that
never parses HTML.

**Checking the rest surfaced a worse version of the same fault in
Italian.** Four Italian titles carried entities that were rendering
literally: `L&rsquo;Accordo`, and `Modalit&agrave;` in three places, so
Italian users were reading "Modalit&agrave; Giornaliera" rather than
"Modalità Giornaliera". Replaced with the actual characters. The English
`&amp;` cases at least stayed readable; these did not.

Swept every title in both languages afterwards — no entity of any kind
remains in a field that renders as text. The one other `&amp;` found in
i18n strings, `hint_tools_main`, is bound with `data-i18n-html` and is
correctly escaped for that path, so it was left alone.

Worth noting the tour audit passes this file clean and always did: it
checks for missing tours, broken steps and tone, and has no concept of a
string that renders differently from how it reads in source. The check
that found this was rendering each title through the real path and
comparing.

## v0.142.1 — XP toast: lower, correct in light mode, and stacking updates in place

Three corrections from the first pass.

**It sat too high and clipped the level chip.** The toast was placed 2px
below the chip and then rises 3px as it fades in, so it overlapped the
chip's lower edge. Now 8px below, leaving a 5px gap at rest.

**The colour was right, the shadow wasn't.** `--in-tune` is properly
themed and matches the chip it sits under — #b6f25b in dark, #224700 in
light — with contrast against the page background of 14.6 and 4.9
respectively, so both are legible. But the text-shadow was a dark drop
shadow in both modes, and in light mode the text is dark, so the shadow
did nothing except muddy it. Light mode now uses a white halo instead.

**Stacking now updates in place rather than re-animating.** The number
changes on the toast that is already there and it does not replay its
entrance — no dropping back down and lifting again. If an award arrives
while the toast has already begun fading, it returns to full opacity from
wherever it had reached and holds its position, so the effect reads as
the total ticking up rather than a new toast arriving. The scale pulse
from the first version is gone; it was fighting the same idea.

Verified against the described scenario: three answers worth 2 XP each
show +2, +4, +6 on a single toast, and an award landing mid-fade updates
to +8 on the same element with the fade cancelled and the position held.

## v0.142.0 — "+N XP" toast under the level chip, with rapid awards stacking

A small monospace "+N XP" that fades in, rises slightly and fades out
beneath the level chip, showing the actual amount earned.

**Rapid awards stack rather than queue or replace.** If more XP lands
while a toast is still visible, the number adds to the running total, the
toast pulses and its timer restarts. Several quick answers in a test
therefore read as one climbing total — +12, then +20, then +50 — instead
of a stutter of overlapping toasts. It's calmer to watch and more honest
about what was earned in that burst. Once it fades, the next award starts
a fresh total rather than continuing the old one.

Positioned `fixed` against the chip's measured rect rather than absolute
inside the header. `.header-top-right` isn't a positioned ancestor, and
making it one would have shifted the buttons already laid out inside it.
The position is re-measured on every award, since the chip moves between
layouts and a stacked award can arrive after a reflow, and it's clamped
to the viewport so a wide total can't run off the edge.

Hooked into `progAddXp`, which every grant in the app already routes
through, so it needs exactly one call site and cannot miss a source.

Verified: appears below the chip and roughly centred on it, stacks three
awards into a single toast, clears itself after the timeout, starts a
fresh total afterwards, ignores zero and negative amounts, stays on
screen, and fires from the real `progAddXp` path rather than only when
called directly. It also no-ops when the chip is hidden, which is the
case behind the fullscreen instrument overlays.

## v0.141.1 — Level curve reshaped: two years now reaches the 100s rather than 47

Two years of daily practice reaching only level 47 was too harsh, and
modelling the curve against the actual earning rate showed why.

**The mismatch is between curve shape and income.** Standard RPG curves
are quadratic or exponential because in an RPG the player's income grows
with level — tougher enemies pay more, so the rate rises alongside the
requirement. Intonare's income is flat: a rhythm test pays the same at
level 40 as at level 4. A quadratic requirement against constant income
means time-per-level grows linearly and never stops. Level 20 cost about
13 days of typical practice, level 50 about 33, level 100 about 66.

`25n(n+1)` is replaced with `50 * n^1.5`, which keeps the early game
identical while flattening the long tail — quick progression first,
slowing afterwards, without slowing forever. Later levels settle around
7 to 14 days each instead of growing without bound.

    old: 1wk L5 · 1mo L10 · 3mo L17 · 6mo L23 · 1yr L33 · 2yr L47
    new: 1wk L5 · 1mo L13 · 3mo L27 · 6mo L43 · 1yr L68 · 2yr L108

**Tuned so it can never demote anyone.** The coefficient was chosen so
the new requirement never exceeds the old one at any level — verified
across 300 levels, maximum excess exactly 0. A curve that asked for more
XP anywhere would have dropped a level from any user sitting just above
that threshold, which is a bad thing to do to someone silently on
update. Existing levels can only stay the same or go up, and most will
go up substantially.

Also verified the curve is strictly increasing, that level boundaries are
exact in both directions (one XP below a threshold gives the lower level,
exactly on it gives the higher), and that `progLevelFromXp` still
resolves instantly at five million XP — it's a `while` loop, so an
ill-shaped curve could have hung it.

Rate assumptions come from the grants added in v0.141.0: roughly 76 XP a
day for a user completing a 20-minute session plus a few exercise rounds.

## v0.141.0 — XP for completing a practice session, and for the two rhythm-card modes that were missing it

Before adding anything, checked what the research actually says, because
this is a decision that can backfire rather than just be suboptimal.

**The risk is the overjustification effect**: attaching expected rewards
to an activity someone already finds intrinsically rewarding reduces
their motivation for it, and engagement can end up below where it
started once the reward is removed. That is a direct argument against
paying XP for time spent in the piano, drums or progression tools —
somebody playing piano for an hour is already motivated, and points would
risk turning "I enjoy this" into "I want the points". Reviews of gamified
music apps say exactly this, that gamification can reward repetition
rather than skill.

**But it isn't binary.** Recent work finds it is not the presence of
rewards that determines the outcome so much as how they are interpreted:
informational feedback on progress behaves very differently from pressure
to act. And rewards are most useful precisely for the tasks people
otherwise avoid.

**So the rule this build adopts: XP rewards effortful assessment, not
time spent or content viewed.** That keeps levels meaning something
rather than measuring how long the app was open.

**Added:**

- **Session completion**, scaled as `8 * sqrt(goalMin)`. This is the only
  time-based award and it qualifies because the goal is set BY the user,
  so it reads as feedback on a target they chose. Square root rather than
  linear so a 60-minute goal is worth more than a 20-minute one without
  being three times more — linear scaling quietly pressures people into
  longer goals than suit them, which defeats the point of letting them
  choose. 5 min earns 18, 20 min earns 36, 60 min earns 62, 120 min earns
  88, against 50 XP for level 2 and 150 for level 3.
- **Rhythm card test** (`rctFinish`), 2 XP per card passed, minimum 3. It
  was the only graded test in the app awarding nothing.
- **Rhythm card drill** (`rcdFinish`), 2 XP per card mastered. Skipped
  cards earn nothing. Drilling what you failed is the clearest case for a
  reward there is.

**Deliberately not added**, both suggested and both declined on the
evidence: XP for flipping through Survival Guide pages, since reading
reference material isn't practice and rewarding it makes XP purchasable
by scrolling; and timed XP drops while sitting in a learning tool, since
that rewards presence rather than effort and is where the
overjustification risk is highest.

Also checked every other test-completion path for a missed hookup.
`ivtFinish` is cleanup only, with the award already in `ivtShowResults`.
`vrShowResults` is vocal range measurement — a calibration, not a test —
so it stays unrewarded. The music quiz keeps its own separate `MQ.xp`
economy feeding `totalXP`; merging that with the main XP pool is a design
question rather than a missing wire, so it was left alone.

## v0.140.2 — "First Light" fired on any XP rather than a completed session, and a map of what grants XP

The achievement's condition reads "complete your first session" and its
check was `s => (s.xp||0) > 0` — so it unlocked the instant any XP was
earned anywhere, which is why opening a single training module triggered
it.

Fixing it needed a new field rather than a different comparison.
`sessionCompleted` is a per-DAY flag, set when the daily practice goal is
reached and reset every night, so it can never answer "have you ever
finished one". There is now a cumulative `sessionsCompleted`, incremented
where a session genuinely completes, and the achievement keys off that.
`checkAchievements()` is called at that point too — it was previously only
invoked there for a different achievement, so nothing re-evaluated the
session achievements at the moment one finished.

Existing installs that already completed a session today are credited on
migration rather than being made to wait until tomorrow. The backup audit
picked the new field up automatically: 43 progState fields, all
classified.

**Also mapped every XP grant, since "work out what grants XP" was the
next item.** There are 16, and every one of them is in a training or
exercise module: note cards, interval training, interval pitch, tone
listen, tone generator, staff reading, relative pitch, rhythm reading,
perfect pitch, sight singing, chord ear training, Tonale, Chordle,
Diadle.

Nothing else grants XP at all. Not practice time, not completing a
session, not any of the tools — the piano, drums, progression, charts,
tuner, metronome and Survival Guide award nothing. That is worth stating
plainly because it explains the bug above: XP was the only signal
available to that achievement, and it means "did an exercise", not "put
in a practice session". Whether the tools and session time should award
XP is a design decision rather than a bug, so it's left for a call rather
than guessed at.

## v0.140.1 — Dead code swept after the SVG conversion, including a cluster propping itself up

Checked for leftovers from the piano conversion and from the earlier
attempts at other bugs this session. Most of it was already clean: the
reverted organ fixes, the trill's oscillator fallback, the abandoned
bar-alignment helpers and the deferred-restart flag are all fully gone,
leaving only comments recording why.

**The DOM piano keyboard's touch chain was still there** —
`_buildPianoKeyboardRows`, `_initPianoMultiTouch`,
`_initPianoFullMultiTouch`, `_pianoPointerDown/Move/Up`,
`_pianoMidiFromPoint` and the `_pianoPointers` map. All of it bound to
`#pianoKeyboard`, an id that appears nowhere in the markup, so the chain
had been attaching listeners to an element that doesn't exist. Both piano
keyboards are SVG now and get their touch handling from
`_initSvgMultiTouch`.

**Deleting it exposed a second dead cluster that had been hiding behind
the first.** The Rhodes handlers — `_rhodesPointerDown/Move/Up`,
`_initRhodesMultiTouch`, `_rhodesPointers` — call the piano's
`_pianoMidiFromPoint`, and they bind to `#rhodesKeyboard`, which also
doesn't exist. Two unreachable systems calling into each other, so each
looked referenced while neither could ever run. Only removing one made
the other visible, which is a good argument for doing this sweep at all
rather than trusting a reference count.

Both clusters removed after checking for string and inline-handler
references, not just direct calls — the failure mode that made a previous
dead-code cull unsafe. The file is about 4.5KB smaller.

Verified after deletion rather than before: all 15 tools open, all four
keyboards render (piano card 24 keys, piano fullscreen 48, Rhodes card
24, Rhodes fullscreen 36), no page errors, and the regression sentinel,
backup audit, stop-all audit and spelling audit all pass.

## v0.140.0 — Fullscreen piano rebuilt on the shared SVG keyboard, removing the app's last DOM keyboard

Asked whether there was a real reason the expanded piano wasn't SVG like
everything else. There wasn't. Every other keyboard in the app — the
piano card, both Rhodes keyboards, the organ overlay, every chart
keyboard — goes through `csDrawChromPerc`. The fullscreen piano was the
only one built from DOM divs, with no comment anywhere explaining why. It
reads as the original implementation that never got migrated.

Being the odd one out was expensive, and the last few builds were paying
for it. The held-key highlight had to be written twice in two unrelated
ways, so fixing one left the other broken — which is exactly how it was
reported. The keys looked wrong beside the Rhodes and Hammond because
their bottom-edge rounding was designed at card size and the fullscreen
keyboard is rotated 90 degrees, landing that rounding on the key ENDS.
And a trail of dead code led back to the same place.

Now rendered through the shared renderer with `preserveAspectRatio="none"`
to fill the height, matching the Rhodes and organ overlays. Appearance,
touch handling, held-key behavior and riff flash all come from one
implementation instead of two kept in sync by hand.

**Every reader of the old keyboard was followed**, which is the lesson
this session kept teaching. `highlightPianoFull` looked up `pwkf-`/`pbkf-`
ids and now queries `data-midi`. `_riffFlashPianoFullKey` had its own
div-based flash and now defers to `_riffFlashSvgKey`, the same path
Rhodes and organ use. `_pianoKeyEls` was returning an empty list — one
prefix belonged to a DOM card keyboard whose builder has no callers at
all, the other to this keyboard — so the decay styling it feeds was
silently doing nothing; it now finds SVG keys on both.

`_pianoIsHeld` needed the same treatment and is worth calling out: it
walked `_pianoPointers`, which belongs to DOM touch handlers bound to
`#pianoKeyboard`, an element that does not exist. The map was always
empty, so it always answered false and the held-key decay skip added in
v0.139.3 never actually engaged. The SVG keyboards now publish their held
notes on the element and it reads those.

Verified: 48 keys render, touch is wired, the old div rows and their ids
are gone, highlight applies and clears, decay styling finds keys, held
state reports correctly, and octave shifting rebuilds properly (the first
shift test showed no movement, which turned out to be a correct clamp at
the top of the range rather than a fault).

## v0.139.5 — The held-key fix reached only the fullscreen keyboard

Reported that touch-and-hold works in expand but not compact, which is
correct: the two keyboards are entirely separate implementations and
v0.139.3 only fixed one of them.

The fullscreen keyboard is DOM divs with a `pressed` class. The compact
one is SVG — keys are `<g data-midi>` wrapping a `<rect>` — with its own
touch system in `_initSvgMultiTouch` and its own pointer map, so neither
`_pianoSetPressed` nor `_pianoPointers` reached it. Its highlight came
from `_flashKey`, which appended an overlay rect and removed it on a
150ms timer: the same shape of bug, in a second place, with no shared
code between them.

`_flashKey` is replaced by `_holdKey` / `_unholdKey`, which tag the
overlay with `data-hold-midi` so it can be found and removed by note on
release rather than by timer. Pressing lights the key, sliding onto
another moves the light, and releasing clears it. Pressing the same key
twice can't stack two overlays, and `_clearHeldKeys` sweeps everything if
a gesture is cancelled without reporting its pointers — better to clear a
key still held than strand one lit under no finger.

Verification is honest here: the compact keyboard's SVG has zero layout
size headlessly, so `elementFromPoint` can't hit it and synthetic
pointer events don't register. The wiring is confirmed by reading, and
`_flashKey` no longer exists anywhere in the file, but whether it feels
right needs a device. The fullscreen equivalent was fully driven in the
harness and passed.

Also corrected two British spellings in comments added this session
("cancelled", "relabelled"), keeping the spelling audit at its 59
baseline.

## v0.139.4 — Fullscreen piano keys squared off to match the Rhodes and Hammond

Screenshots side by side made this obvious: the Rhodes and the Hammond
both have square-ended keys and the piano's end in heavy rounded tabs,
which is why it looked awkward next to them.

The cause is a rotation. Both key styles carry `border-radius: 0 0 7px
7px` — rounding on the BOTTOM edge — and the fullscreen keyboard is
displayed rotated 90 degrees, so that rounding lands on the right-hand
ENDS of the keys. At the card's size it reads as a normal rounded key
edge. Blown up to fullscreen it reads as a row of rounded tabs.

The black keys had a second problem in the same place. Their gradient
lightened toward the end (#242433 at 100%) and they carried a white inset
shadow along that edge; rotated, both become a soft fade at the key tip,
which is what let the white keys' seams show through underneath. They now
stay dark to the end.

Scoped to `#pianoOverlay` so the piano card is untouched. The Rhodes
keyboard is unaffected regardless — it has its own overlay and draws its
keys as SVG rather than using these classes — and the Hammond likewise.

Verified the rules resolve on the real fullscreen keys rather than
assuming the selector matched.

## v0.139.3 — Held keys stay lit through a song, and a correction to yesterday's diagnosis

Two clarifications from device testing pinned this down: the fading only
happens while a song is playing, and a key held by a finger should stay
highlighted for the whole press regardless of what the audio is doing.

**First, a correction.** v0.139.2 said `_pianoKeyEls` was dead. It is
half dead. Its `pwk-`/`pbk-` lookup finds nothing, because the piano CARD
is drawn as SVG and `_buildPianoKeyboardRows`, which would have created
those ids, has no callers at all. But its `pwkf-`/`pbkf-` lookup works,
because `buildPianoFull` does assign those to the fullscreen keyboard. So
the decay styling is live in fullscreen, which is where the fading was
seen and where it was reported.

**The fade is `_applyPianoDecayStyle`.** It repaints each key as its note
decays, lerping the background from the lit color back toward resting —
which is what reads as fading out and showing the seams underneath. That
is correct and intended for notes a song is playing. What it had no way
of knowing is whether a key is currently under a finger, so during
playback it repainted held keys back to resting while they were still
being held.

Holding is a user action and outranks the audio, so `_pianoIsHeld` now
checks the live pointer map and both `_applyPianoDecayStyle` and
`_clearPianoDecayStyle` skip keys being held. Release clears what the
hold was protecting, and the pointer entry is deleted BEFORE that clear
runs — clearing first would have been a no-op against its own guard and
left the key painted after the finger lifted. Sliding off a key mid
gesture clears it the same way.

Verified against the real fullscreen keyboard rather than by reading:
with a finger simulated on a key, it stays lit through a decay repaint,
through an explicit decay clear, and past the old 120ms timer; it clears
when the finger lifts; and the decay styling still paints and clears
normally when nothing is held.

## v0.139.2 — Piano keys never showed a pressed state at all

Reported as held keys not visually holding. The cause turned out to be
one step further back: they were never highlighted in the first place.

`pianoKeyClick` looked up `'pwk-' + midi` or `'pbk-' + midi` and added a
`pressed` class to the result. Nothing in the app assigns those ids. The
card keyboard builds its keys with a variable prefix plus `'w'`/`'b'` and
the midi number, and the fullscreen keyboard sets no id at all, only
`data-midi`. So `getElementById` returned null every time and the class
was never applied to anything.

What made it look like a hold problem rather than a missing highlight is
that `.pressed` is styled alongside `:active`, and on desktop `:active`
supplies the pressed look for as long as the pointer is down. The touch
handlers call `preventDefault()`, which suppresses `:active` in the
Android WebView — so on device there was no highlight from either source.

Keys are now selected by `data-midi`, which is what both keyboards
actually set. A second problem was real as well: the class was removed on
a fixed 120ms timer regardless of whether the key was still held.
`pianoKeyClick` now takes a `hold` flag, set by the touch handlers, and
the timer only runs for callers that fire a note with no release to
follow — playback, previews, chord cards. Sliding off a key un-lights it,
and release clears it.

Noted, not fixed: `_pianoKeyEls` uses the same dead `pwk-`/`pbk-`
prefixes and the decay styling depends on it, so that is very likely
inert too. It is a different behavior and wants its own look rather than
being changed blind alongside this.

Honest about verification: the piano keyboard isn't built by `enterTool`
in the headless harness, so this is confirmed by reading how the keys are
constructed rather than by driving them. It needs a device check.

## v0.139.1 — Full verification pass against the pre-session build

Ran every audit in the project against v0.139.0 and, where a script
reported anything, ran it again against the build this session started
from (v0.134.11) to establish whether the finding was ours or
pre-existing.

**Identical before and after, so pre-existing and untouched by this
work:** the quiz audit's 129 critical items, the tour audit's 13
tone flags, and the groove audit's meter conflicts. Those are real
findings and worth their own pass, but none were introduced here.

**One regression found and fixed:** the British/US spelling audit went
from 59 to 62. All four were mine, in comments written during this
session — "analysing", "behaviour" twice, and "Parameterising". The
codebase standardises on US spelling and I default to British, so these
would have kept accumulating unnoticed. Corrected, and the count is back
to the 59 baseline exactly.

**Everything else clean:** regression sentinel (97 fixes, 241 pins),
backup audit (48 keys, 42 progState fields), stop-all audit, audio handle
audit, changelog gate, and a syntax check across all script blocks.

**Runtime smoke test:** all 15 tools open without error, the lookahead
limiter is installed with headroom at 0.7, `stopAllAudio` and
`chordScaleStopAllAudio` are both safe to call after visiting everything,
the rhythm context is released rather than left borrowed, and there are
no page errors.

**State leak audit clean:** every action writes only its own module's
state. Progression touches `prog*`, the metronome touches `bpm`,
`groovePattern` and `groovePresetId`, the drum kit touches
`dk_currentKit`. Nothing crosses.

## v0.139.0 — Tempo separated too, and the leak audit now comes back clean

Tempo was the last value the rhythm modules shared, deferred twice as
"its own pass". Asked for a third time, so it's done.

**Progression owns `progBpm`.** Its chord scheduler reads it, its
displays show it, its sliders and adjust buttons set it, and it persists.
The metronome's own screen controls are untouched and still drive the
metronome's tempo.

The engine still has to run at one tempo during playback, or the click
and the kit would drift against the chords. So tempo travels in the
rhythm context: while Progression holds the engine, the globals are set
to `progBpm` and the metronome's value is stashed, then handed back on
release. Changing tempo mid-playback retimes the click and kit live
rather than waiting for a restart.

**Two more leaks the audit caught while finishing this.**
`progLoadPreset` called `setBPM(p.bpm)`, so opening a progression preset
retuned the metronome and the drum kit. And `dk_loadedPresetName` wasn't
in the context, so a progression preset relabelled which preset the Drums
module showed as loaded.

**The groove selector now shows its selection after a preset load**, on
the category tab that holds it, without playing anything first.

**The leak audit now comes back clean.** Every action touches only its
own module: Progression writes `prog*` variables, the metronome writes
`bpm`, `groovePattern` and `groovePresetId`, the drum kit writes
`dk_currentKit`. No value crosses between modules any more, which is what
was asked for: a tool should behave the same way every time it's opened
regardless of what was done somewhere else earlier.

Verified end to end: with the metronome at 90 and Progression at 140,
each keeps its own, the engine runs at 140 while Progression plays, and
the metronome is back at 90 afterwards.

## v0.138.2 — Every cross-module write found by audit instead of by report

Five bugs in a row had the same root and each was fixed the same way: wait
for it to be noticed, trace that one value, patch it. That was never
going to converge, so this build audits the whole thing.

**Two real leaks found, both fixed.**

`grooveLoadPreset` is not a pure loader. Alongside setting the preset id
and pattern it calls `setTS()` to move the metronome's time signature to
the groove's native meter, calls `setBPM()` with the groove's suggested
tempo, sets `grooveCategory`, and rewrites the metronome's on-screen name
and meta text. `progSetGrooveChoice` was calling it purely to resolve a
pattern and then restoring the handful of fields the rhythm context
captures — so every one of those other changes stayed. That is
Progression moving the metronome. Presets are plain data, so the pattern
is now read directly from `GROOVE_PRESETS` and that path touches no
global at all.

`progLoadPreset` called `loadPreset()` directly to apply a preset's drum
beat, and that writes the Drums module's live state — patterns, steps,
subdivisions, the loaded-preset label. Opening a progression preset
therefore replaced whatever the user had built in Drums. It now borrows
the engine first, applies the beat, captures the result as Progression's
setup, and hands Drums back untouched. `dk_loadedPresetName` was also
missing from the context, so it is captured now too.

**Added `intonare_state_leak_audit.py`.** It extracts every top-level
state variable from the source, snapshots all of them, performs a user
action, snapshots again, and reports everything that moved.

The first version of it enumerated `window` and reported a perfectly
clean app while all of the above was live — top-level `let` and `const`
in a classic script live in script scope, not on `window`, so only `var`
and function declarations were visible. Reading names individually
through eval raised coverage from a handful to 1,180 variables, and the
leaks appeared immediately. Worth recording, because a clean result from
the wrong instrument is more dangerous than no result.

After the fixes, every change is either the acting module's own state or
tempo. `bpm` / `dk_bpm` remains genuinely shared app-wide, which is the
one known and documented exception: separating it means moving
Progression's scheduler and every BPM display onto their own value.

## v0.138.1 — The metronome's groove was overwriting a progression preset's

Same class as the drum module case, and caused by the capture added in
v0.137.8 reading the wrong copy.

`progSetGrooveChoice` records the preset's groove into Progression's
saved setup and then deliberately puts the live globals back, so choosing
a groove in Progression doesn't move the metronome. `progLoadPreset` then
called `_rcCapture()` a few lines later, which reads those same live
globals — the metronome's, by design — and wrote them over the groove
that had just been stored. So setting a groove on the metronome and then
loading a progression preset handed the progression the metronome's
groove instead of the preset's.

The drum-side fields still come from the capture, since those are live
and correct at that moment. The groove-side fields now come from
`progRhythmState`, which is already right either way: updated by
`progSetGrooveChoice` when the preset declares a groove, and holding the
previous choice when it doesn't, since a preset with no groove has
expressed no opinion about one.

The reverse direction was checked and is already correct: the
metronome's own groove picker writes the global, which is its own state
when it holds the engine, and Progression's saved setup is untouched by
it.

Verified as the full sequence: with the metronome on one groove, loading
a progression preset carrying a different one keeps the preset's for
Progression and leaves the metronome's alone; changing the metronome
again afterwards doesn't move Progression; and at playback the engine
receives Progression's groove and the metronome's is restored after.

## v0.138.0 — The BPM pill now names the beat or groove you picked

Requested as a small quality-of-life addition, and the element for it
already existed: `#progBpmGroove`, inside the pill that opens the sync
tray. It was being filled, just not with anything useful.

**In kit mode it showed the drum CATEGORY** — "Rock" rather than "Basic
Rock" — and read it from `dk_activeCat`, which is the Drums module's
current category and has nothing to do with what Progression selected.
**In metro mode it was gated on `grooveModeActive`**, the live global that
gets restored to the metronome's value whenever Progression isn't holding
the engine, so the name only appeared during playback and was blank
exactly when you'd want to check what was loaded.

Both are the same mistake found repeatedly today: reading a shared global
instead of the module's own selection. It now uses
`progCurrentGrooveId()` and `progDkSelectedName`, so the name is correct
while stopped, and blank in silent mode where there's nothing to name.

Coloured with `--metro`, the same yellow the groove and beat cards use
when selected, so the name reads as the thing you picked in the tray
rather than as more tempo text beside the BPM number (which is
`--accent-warm`). Being theme tokens, light mode follows automatically —
though it's worth recording that neither keeps its dark-mode hue there:
`--metro` is #ffd166 dark and #503600 light, and `--accent-warm` is green
dark but burnt orange light. The "green like the BPM" from the request
only reads green in dark mode.

Verified in both modes: the beat name shows in kit mode, the groove name
in metro mode, both while stopped, blank in silent, and the colour
resolves to the theme's value for each appearance.

## v0.137.10 — Swap restarts pause briefly instead of trying to thread a gap

The instant restart in v0.137.9 still glitched: with a chord change
imminent, the new pass appeared to skip straight to the next chord. The
cause is the chord scheduler's 0.2s lookahead. A pass beginning 0.16s out
has its first chord and the queueing of its second happen in the same
tick, so the first chord is immediately followed by the next. Pushing the
lead further doesn't help, because the lookahead window travels with it —
every value that clears one collision creates another.

Given a short pause was acceptable, the restart now stops, waits 250ms,
and starts clean. That sidesteps the whole class of problem rather than
picking a number that happens to work: everything from the old pass —
chords, and drum hits already scheduled inside `SCHEDULE_AHEAD` — has
finished before the new one begins, so there is nothing to overlap with
and no timing left to get right. It also reads as a deliberate reset
rather than a stutter.

Two edge cases came with it, both guarded and tested. Swapping twice in
quick succession cancels the pending restart rather than stacking a
second one. And stopping during the pause cancels it too, which matters
because `progStop` sets `progPlaying` false and the pause's own guard
checks that flag — without the cancel, a swap followed by pressing stop
would have restarted playback a quarter second after being told to stop.

`progStart`'s lead parameter is kept but nothing passes one now; the
comment explaining it has been corrected rather than left describing an
approach that no longer exists.

Verified: playback stops immediately on swap, stays silent through the
pause, resumes from the top afterwards, a double swap produces one
restart, and stop during the pause stays stopped.

## v0.137.9 — Swaps take effect immediately, and stop double-hitting the drums

Two complaints about the swap restart, both fair, and both consequences
of choices made in the last two builds.

**It waited for the current chord to finish.** v0.137.5 deferred the
restart to the next bar line to avoid racing the scheduler. That fixed
the race and introduced a worse problem: a swap could sit doing nothing
for most of a bar, which reads as the app having ignored the tap.
Swapping a beat is a direct instruction, so it now takes effect
immediately.

**It double-hit the drums when swapping near a chord change.** Stopping
clears the drum scheduler so no new hits are queued, but hits already
scheduled within `SCHEDULE_AHEAD` (0.12s) are created nodes with future
start times and will sound regardless. The new pass began at
`ctx.currentTime + 0.05`, which is inside that window, so fresh hits
landed underneath the leftovers. `progStart` now takes an optional lead
and the restart passes 0.16s — past the window, so the old pattern's tail
finishes before the new one starts. The only existing caller uses the
default and is unaffected.

The deferred-restart flag and its bar-line handling in the scheduler tick
are removed rather than left dead.

Worth noting what this build is not: a measurement. The restart being
synchronous, playback continuing and the kit still running are all
verified, but the lead itself can't be read back at runtime — `progStart`
runs a scheduler tick immediately, so both `progNextAudioTime` and
`progCurrentBarStartTime` have already advanced by the time anything can
observe them. The lead is verified as a property of the code rather than
of a running system, and whether the swap actually sounds clean is a
listening test.

## v0.137.8 — One rule for whose setup wins, which is what the last four builds were missing

The half-time report came with the detail that settled it: selecting a
preset played its drums at half time, swapping to groove was correct, and
swapping back was also correct. Swapping back re-runs `loadPreset`, which
sets the timing fresh — so the preset's beat was never wrong, something
was overwriting it afterwards.

**Progression had two sources of truth with no precedence between them:**
the preset, which declares a beat and groove, and the persisted
`progRhythmState`, which remembers what was last used. Whichever got
applied second won, and which one that was kept changing build to build.
Every symptom reported over the last four builds was an instance of that
one ambiguity, and each was fixed by patching whichever side had lost
that week.

**The rule, now stated in the code so it stops being re-decided:** an
explicit selection wins immediately and is written to the saved setup.
The persisted setup applies only when nothing more explicit has happened.
Loading a progression preset and picking a beat in the tray both count as
explicit, and both now capture the resulting state at the moment of
selection.

Concretely, that kills the half time: the preset loaded its beat
correctly and then playback applied the persisted setup over it, whose
`dk_timeSigKey`, `dk_numSteps` and `dk_globalSub` were left over from
whatever ran before. With the setup captured at selection there is
nothing stale left to win.

A preset that declares no groove keeps whichever groove was already
chosen, since it has expressed no opinion about it.

`progDkSelectedName` is also set from the preset's `drumPreset`, so the
beat shows as chosen without opening the tray or starting playback —
the selection existed all along and nothing recorded it.

Verified as the sequence rather than the parts, which is the change in
method this needed: the saved setup was deliberately poisoned with
conflicting timing, a preset carrying a drum beat was loaded, and then
playback was simulated. The stale values are gone from the saved setup,
the beat is highlighted, and loading the setup at playback no longer
alters the live timing at all. Testing each piece in isolation is what
let this survive three previous attempts.

## v0.137.7 — Half time, and the beat still not showing as chosen

**Everything played at half time.** v0.137.6 made the rhythm context load
for both sync sources, on the reasoning that applying fields the current
mode doesn't use is harmless. That reasoning was wrong, and it was
asserted rather than checked. `dk_timeSigKey`, `dk_numSteps` and
`dk_globalSub` feed step timing, and the METRO sync source runs the
groove without the kit — so loading a saved setup's values over the
metronome's changed the rate the groove was clocked at.

`_rcLoad` and `_rcApply` now take a scope. Metro sync loads only the
groove selection and leaves every drum-engine field alone; kit sync still
loads the whole setup, since there the kit genuinely is playing and those
fields are its own.

**The beat still didn't show as chosen on open**, and the value was never
the problem — it was stored correctly the whole time. The card's
highlight also required `progGrooveEnabled`, which is false when you open
a progression whose groove hasn't been switched on yet, so a correctly
stored selection simply never rendered as selected. Whether a groove is
currently sounding is a different question from which one is chosen, and
the card answers the second, so the highlight now turns on identity
alone.

Verified with the timing fields deliberately set to conflicting values:
metro sync loads the groove and leaves timeSigKey, numSteps and globalSub
exactly as the metronome had them; kit sync does load them; restore puts
them back; and the selected card highlights with groove output off.

Worth recording as a pattern, since it has now happened twice in this
run: both of these came from reasoning about what a change would do
instead of measuring it. The half-time bug was introduced by an explicit
"this is harmless" claim in a code comment, and the highlight was chased
through three builds at the wrong layer because the stored value looked
suspect and was never actually checked.

## v0.137.6 — Progression presets get their beats back: the context was only loading for one sync mode

Reported that presets stopped calling their own beats. `_rcLoad` sat
inside the `kit` branch of `progStartSyncSource` and nowhere else.
Grooves play through the METRO sync source, so a progression's groove was
being written into its own saved setup by `progSetGrooveChoice` and then
never loaded back into the engine when playback started. The preset asked
for a beat and the beat never arrived.

The context now loads for either sync source. Applying fields the current
mode doesn't use costs nothing, since `_rcApply` only writes what the
saved setup actually contains.

This is the third consequence of the same root change and worth naming
plainly: separating module state moved where the truth lives, and each of
these bugs has been a place that was still looking at the old location or
never told to read the new one. The separation itself is right, but it
had more reach than the initial audit showed, and the failures have been
silent ones — nothing throws, the value is simply stale or absent.

Verified as a full round trip, which is what the earlier fixes were
missing: with the metronome on its own groove and mode off, a progression
preset's groove is stored in Progression's setup without touching the
metronome's pattern; on playback the engine actually receives that groove,
groove mode comes on and the pattern genuinely changes; and after
handback the metronome's groove, pattern and mode are all exactly as they
were while Progression still remembers its own choice.

## v0.137.5 — Swap restart no longer races the scheduler, and Progression's groove shows as selected again

**Swapping near a chord change started the progression on its second
beat.** v0.137.4 restarted by calling progStop and then progStart behind
a short timeout. The scheduler runs a lookahead window, so chords were
already queued at future audio times when the restart began — swap close
to a chord change and that queued chord played over the top of the new
pass, which is what came out as starting on the second beat. The timeout
made it worse by widening the window.

Restart is now a flag the scheduler acts on at the next bar line:
sequence index and bar counter rewind, and when the kit is the sync
source its scheduler is re-initialised to that same bar time. Nothing is
torn down mid-flight and nothing is left in the queue behind it, because
the restart never leaves the clock it was already running on.

**A progression preset's groove stopped showing as selected.** This one
was a regression from the module separation in v0.137.0 and had been
reported before, in a form I fixed the wrong layer of. Progression's
groove choice now lives in its own saved setup, and the global
`groovePresetId` is restored to the METRONOME's groove the moment
Progression isn't holding the engine. The drawer, the tray's category
sync and the drawer label were all still reading that global, so they
were highlighting against the metronome's value and finding no match.

Added `progCurrentGrooveId()`, which returns the live global while
Progression holds the engine (it is Progression's state at that point)
and its saved choice otherwise, and pointed all three readers at it. This
is the same class of mistake as the Survival Guide stop earlier in the
session: separating state without following every reader of the thing
that was separated.

Verified: with the metronome on one groove and Progression on another,
the metronome's stays untouched, Progression's choice is stored and
returned, exactly one card highlights in the drawer, and the tray opens
on the category holding it.

## v0.137.4 — Beat and groove swaps restart the progression, which makes alignment a fact rather than a calculation

Third attempt at this, and the first one that doesn't depend on getting
arithmetic right at the instant of a swap.

The first attempt restarted the pattern at the next bar boundary, which
restarts it at ITS bar one — so a four-bar loop's variation bar landed
wherever you happened to tap. The second computed the loop's position
from an absolute bar counter so the pattern would sit where it would have
been had it played from the start. That arithmetic was verified correct
in isolation (bar 3 to step 48, bar 6 wrapping to bar 2, single-bar
patterns untouched) and it still came out of phase on device, because it
depends on every track's phase, the progression's bar counter and the
audio clock all agreeing at the moment of the swap.

Swapping now restarts the progression from the top. Both parts begin
together from a known state, so there is nothing left to compute or get
wrong. The cost is that a swap returns you to bar one rather than
continuing, which is a fair trade for a beat that is reliably in phase,
and it's what a drum machine does when you change pattern anyway.

The same applies to groove swaps, which previously queued to the next bar
boundary via `progPendingGrooveId` and had exactly the same
within-pattern problem. They now apply immediately and restart.

`progDkPhaseForBar` and `progDkInitAligned` from v0.137.3 are removed
rather than left dead, with a note recording what they did and why the
approach was abandoned — the arithmetic wasn't wrong, the assumption
behind it was.

Verified: the restart helper is safe to call when nothing is playing,
leaves a stopped progression stopped, and resets both the sequence index
and the bar counter.

## v0.137.3 — Multi-bar drum loops now land on the progression's bar, not their own bar one

v0.137.2 concluded the drumbeat swap was already handled because it
restarts cleanly on the next bar line. That was true and still missed the
point, which device testing with the Amen break made obvious: restarting
cleanly is not the same as restarting in the right place.

`_initTrackScheduler` zeroes every track's phase, so a swap always
restarted the pattern from its own first bar. For a one-bar pattern
that's invisible. For a four-bar pattern whose entire character is the
variation in its last bar, that bar then lands wherever you happened to
tap, and moves again on every swap — which is exactly the "tricky to see
where the odd 4th measure lands" that was reported.

Added `progBarsElapsed`, an absolute count of bars played since the
progression started. Unlike the existing `barIdx` it doesn't cycle with
the progression's own length, which is what a multi-bar loop needs in
order to work out which of ITS bars should be sounding. `progDkPhaseForBar`
turns that into a step offset, and `progDkInitAligned` starts each track
there instead of at zero, so a swapped-in pattern sits exactly where it
would have been had it been playing from the start.

Phase is computed per track because tracks can carry different
subdivisions and therefore different steps-per-bar; using one figure for
all of them would misplace any track running triplets.

Verified against a four-bar loop of 64 steps: bar 3 lands at step 48, bar
6 wraps to bar 2 at step 32, bar 4 returns to step 0, negative input is
clamped rather than producing a negative index, and single-bar patterns
are untouched at phase 0 for every bar.

This is measure-position alignment, which earlier in the session was
scoped as the larger follow-up to the quick reset-to-downbeat fix. It
turned out to be small once there was a bar counter to hang it on.

## v0.137.2 — Tempo taken back out of the rhythm contexts: v0.137.0 could desync chords from drums

Checking the drumbeat-swap item found that both swap paths were already
correct — the kit preset resets `dk_currentStep` and restarts at the next
bar boundary, and a groove swap during playback is queued via
`progPendingGrooveId` and applied exactly on the bar line. Nothing needed
doing there.

What it did find was a fault introduced by v0.137.0. That build gave
Progression its own `dk_bpm` inside its rhythm context, but Progression's
CHORD scheduler reads the global `bpm`, and its BPM sliders call `setBPM`
directly. So a progression whose saved setup carried 140 would have
played its chords at the global tempo and its drums at 140 — the two
drifting apart within the same progression. The separation work created
this; it wasn't pre-existing.

Tempo is therefore no longer part of a context, and the kit explicitly
follows the shared `bpm` when Progression borrows the engine, as it did
before. Everything else from v0.137.0 stands: kit, swing, bars,
subdivisions, per-track overrides and volumes, mutes, patterns and groove
selection remain per-module, and the Drums module still restores
bit-for-bit after Progression has played.

Verified: with Drums on brush/37% swing and a specific pattern, and the
shared tempo at 96, Progression loads its own kit and swing, the kit
tempo matches what the chords are using, the saved setup carries no
tempo, and after restore the Drums module and the tempo are both
untouched.

Separating tempo properly remains worth doing, and is now the last real
crossing between these modules. It means moving Progression's scheduler
and all of its BPM displays and sliders onto their own value, which is a
change to the most timing-sensitive path in the app. That deserves its
own pass with room to test, not being tacked onto the end of a long
session days from release.

## v0.137.1 — Trills sounded like a different instrument than the notes view

Reported from device testing: trill sounds don't match their note
sounds. The comment sitting above the trill audio code claims it uses
"the SAME engine the flute NOTES view uses... so the trill always matches
the rest of the flute's timbre". The code underneath it did not.

There were two paths. With samples loaded it called `windSynth`, which
matches. Without them it fell through to a hand-rolled square-plus-sine
oscillator pair through a 1kHz lowpass — an approximation that sounds
nothing like the app's wind synth. So whenever samples weren't ready, a
trill played a noticeably different instrument from the notes view of the
very same instrument.

That fallback existed to avoid per-note node churn, described in the
original comment as "that was the crackle". The crackle it was working
around has since been diagnosed properly and fixed at the source: there
was no master bus, and every synth voice was running over full scale into
a waveshaper that was permanently squashing it. With a real lookahead
limiter on the master bus, the reason for the workaround no longer holds,
so the trill now takes one path through `windSynth` and simply sounds
correct — samples when they're loaded, the app's own wind synth when
they're not, which is what the comment always described.

Two things followed from the change. The `windSynth` return value was
being discarded, one of the outstanding items the audio-handle audit had
been listing, so trill notes are now tracked and stopped properly (capped
at 24, since anything older has long finished). And `_trillEnsureOsc`
became genuinely dead — verified by full-file sweep for dynamic and
string references before deleting, not by static analysis alone, which is
how a previous cull removed things that were still reachable via onclick.
`_trillTeardown` and its variables are deliberately kept: the stop path
still calls the teardown, and with nothing creating those nodes it is a
guarded no-op.

Verified: the trill schedules through `windSynth`, tracks its notes,
clears them on stop, the button label round-trips through STOP and back,
and both stop functions are safe to call with nothing playing.

## v0.137.0 — Modules stop moving each other: Progression gets its own rhythm setup

The goal set for this: a tool should behave the same way every time you
open it, regardless of what you did somewhere else earlier. Nothing
should quietly reconfigure another part of the app.

**What was actually happening.** The drum engine reads its setup from
module-level globals, and Progression drives that same engine directly —
setting `dk_bpm`, flipping `dk_playing`, running `dk_scheduler`. Because
those globals are the only copy that exists, building a custom kit in
Drums and then playing a progression played your custom kit. There was no
such thing as "the progression's beat"; there was only THE beat, and
whichever module touched it last won. The same applied to tempo, time
signature and groove mode, which Progression wrote straight into the
metronome's globals — so choosing a groove in Progression flipped the
metronome out of METRO into GROOVE mode.

An audit of the four rhythm modules found exactly four variables written
by more than one module — `dk_bpm`, `bpm`, `grooveModeActive` and `tsKey`
— plus `dk_playing`, which Progression writes and Drums reads. Everything
else (`dk_patterns`, `dk_currentKit`, `dk_swingPct`, `dk_barCount`,
`dk_trackSub`, `dk_humanizeSnapshot`, `dk_viewBar`) was already properly
owned. So the fix is contained rather than a rewrite of four modules.

**Rhythm contexts.** Each module now owns a named context holding its
whole setup — tempo, kit, swing, bars, subdivisions, per-track
overrides and volumes, mutes, patterns, and groove selection. The
engine's globals become a scratch area that whoever is currently playing
loads into. `_rcLoad` borrows the engine with a module's setup,
`_rcRestore` hands it back and returns what the borrower ended with.

Restore is the part that has to be right, so it is idempotent, safe to
call when nothing was borrowed, called unconditionally rather than only
when playback ended tidily, and additionally called from `stopAllAudio`
as a safety net. If it were ever skipped, the Drums module would silently
show Progression's kit.

**Groove selection needed separate handling** because it happens at
selection time rather than play time, so the swap alone wouldn't have
covered it. `progSetGrooveChoice` writes the live globals when
Progression currently holds the engine (they ARE its state at that
moment) and otherwise records the choice into its saved setup, restoring
the metronome's state exactly. Progression also no longer calls
`grooveUpdateScreen`, which was repainting another module's UI.

**Persistence follows the distinction asked for:** builder-type tools
keep their work, so Progression's rhythm setup is saved and reloaded —
backing out to check something else shouldn't cost you the beat you built.
Training and reference modules deliberately don't persist and start fresh.

**On the choice of approach.** Parameterising the scheduler to read from
a passed-in state object is the tidier architecture and was considered.
It was rejected for now: the scheduler is the most timing-sensitive code
in the app, and swapping a known-good component for an untested one to
gain a structural nicety, days from release, is the wrong trade. Loading
and restoring around playback achieves the required behaviour with a much
smaller surface and is explicit rather than hidden. The parameterised
version remains the better long-term shape.

Verified end to end: with Drums set to 92bpm, brush kit, 37% swing and a
specific step pattern, Progression plays its own setup (140bpm,
electronic, no swing), and after it stops the Drums module is bit-for-bit
intact — tempo, kit, swing, pattern, groove and mode all unchanged.
Progression remembers what it ended with. Choosing a groove in
Progression leaves the metronome's groove and mode untouched. Restore is
safe called twice or with nothing borrowed.

Not changed, and worth being explicit about: Progression borrows the drum
engine rather than running its own, so Drums and Progression still cannot
play simultaneously. Separating their setups doesn't change that, and
making both playable at once would mean two independent schedulers, which
is a materially larger piece of work.

## v0.136.11 — Survival Guide audio: the fix in v0.136.2 was a silent no-op

Device testing found Survival Guide audio still playing after backing
out, despite v0.136.2 claiming to have fixed exactly that. It hadn't.

`stopAllAudio()` resolves its entries with `window[fn]`. Everything in
the Survival Guide block lives inside an IIFE, so none of its functions
are reachable from `window` — including `stopAllSounds`, which v0.136.2
added to the list. The name resolved to `undefined`, the surrounding
try/catch swallowed it without complaint, and the audit reported full
coverage the whole time because it only checks that a name is listed, not
that the name resolves to anything.

Worse, this was the exact failure mode already identified in that build:
`sgStopCadence` was rejected for not being reachable on `window` and
`stopAllSounds` was chosen instead — without checking whether that one
was reachable either. It wasn't.

Fixed by explicitly exporting the function from inside the IIFE
(`window.sgStopAllSounds`) and pointing the list at the exported name.
Verified by resolving every one of the 50 names `stopAllAudio` calls
against `window` at runtime: all reachable.

The lesson generalises past this one function. A name in a
hand-maintained list can fail in two independent ways — being absent, or
being present but resolving to nothing — and only the first was being
checked. Any future stop function added inside that block needs the same
export, which is noted in a comment beside it.

## v0.136.10 — The limiter wasn't loading on device; added a second URL scheme and real error reporting

On-device `audioPathStatus()` came back with `synthHeadroom: 0.32` and
`isPrimaryLimited: false` — meaning the AudioWorklet never installed and
the app was running the fallback shaper. The fail-safe added in v0.136.1
did exactly its job here: the level stayed at the conservative value, so
the failure was quiet rather than distorted, and nothing shipped louder
than its protection. But it also means the true limiter has not actually
been heard yet.

The page carries no Content-Security-Policy, so the refusal is coming
from the WebView itself rather than from anything in the app. Desktop
Chrome loads a worklet module from a `blob:` URL without complaint;
Android WebView and WKWebView do not reliably allow it, and which schemes
are permitted varies by version.

Rather than pick a scheme and hope, both are now tried in order: `blob:`
first, then a `data:` URL built from the same source. Verified by
simulating a WebView that refuses `blob:` outright — the attempt is
recorded as refused, the `data:` attempt succeeds, and the worklet
installs and swaps in normally.

Each attempt's exact error text is now recorded on the bus and reported
by `audioPathStatus()`, so if both schemes are refused on real hardware
the actual error can be read off the device instead of reasoned about
from here. Four builds were spent this session inferring audio state from
how things sounded; this is the same lesson applied to a failure that
only happens on hardware this environment can't reach.

## v0.136.9 — Verification sweep: every fix confirmed, and six more instances of the same hole

Asked for a full check of everything worked on this session plus a hunt
for similar holes. Built a static sweep that does both, and it earned its
keep immediately.

**Part one: all 22 structural fixes from this session verified present**
— master bus, worklet limiter with its sliding-window detector,
per-context bus and promise maps, exactly two raw destination
connections, fail-safe adaptive headroom, the diagnostic, organ stagger
and teardown, harmonic handles, chart button registry, harp chord
tracking, interval node tracking, the data-kit lookup, clearAll, tray
category sync. Runtime check confirms the worklet attaches, headroom
reaches 0.7, and every stop function is safe to call cold.

**Part two found six more instances of the fire-and-forget pattern**,
the same one that has now appeared nine times: start a note, discard the
handle, leave nothing for any stop function to act on.

- The **Interval Reference tool** discarded every note. `ivrStop` cleared
  its timers and bumped its session, which only blocks notes that haven't
  fired — anything already sounding played on.
- The **interval peek** had the identical fault.
- **Both chart dot-taps** — `gccPlayString` and `gssPlayNote`, the "tap a
  dot to hear that string" notes — discarded their handles, so a tapped
  string survived instrument and subfamily switches.
- **12-string guitar** sounds two notes per string and its `synth`
  returned only the first, so every caller tracking "the note" was
  tracking half of it and the doubled course rang on after a stop.
- **`ssPlayNoteEnhanced` returned nothing at all**, the same shape as
  `addLowFreqHarmonics` before this session. Sight singing and Road Trip
  both play their reference notes through it.

All six now return or record stoppable handles.

**Saved `intonare_audio_handle_audit.py`.** The first version of the
sweep missed the chart taps because it only matched the wrapper players
and not bare `.synth()` calls — which is exactly how these survive
review. The saved version matches both, and also reports partial stop
lists, textContent-based DOM lookups that break under translation, and
synth voices that create nodes without disconnecting them.

**Known and deliberately not fixed in this build**, listed so they aren't
lost: roughly ten remaining discarded returns, mostly Survival Guide
playback (its own AudioContext, reached via `stopAllSounds`), the flute
trill's wind synth, and a handful of theory-tool preview notes. Several
are legitimately fire-and-forget. They want a decision each rather than a
blanket change, and the audit now lists them every run.

## v0.136.8 — The Progression tray never showed you what was selected

Two separate gaps, both making the tray feel like it had forgotten what
you chose.

**The groove side highlighted the active card but never followed it.**
`progBuildDrawerGrooveCards` marks the selected groove active correctly,
but nothing ever pointed the category tabs at the category that groove
lives in. Pick a latin groove, close the tray, reopen it, and you land
back on whichever tab you last browsed with the active card sitting on a
tab you can't see — so the selection was effectively invisible.

**The drum kit side had no selection at all.** Every card rendered as
`'groove-card'` with no active state, and nothing anywhere recorded which
preset had been loaded. There was no state to highlight even if the
markup had allowed for it.

Fixed by adding `progDkSelectedName` (by name, since drum presets carry
no id), highlighting the matching card, repainting the list on selection
so the highlight lands immediately, and adding
`progSyncTrayCategories()` which runs on every tray open and points both
sets of category tabs at whatever is currently selected.

Verified: with a latin groove selected and the browse tab forced to funk,
opening the tray lands on latin with exactly one visible active card; the
same holds on the kit side for a preset in a non-default category.

Note on scope: this makes the tray honest about the selection it already
had. It does NOT separate that selection from the metronome and drum kit
modules — choosing a groove here still writes the same global those tools
read. That separation is a larger piece of work and is being scoped on
its own.

## v0.136.7 — Brush presets never applied their kit, and CLEAR left the old one standing

**The preset kit lookup matched on the button's visible label.** Loading a
preset ran `.find(b => b.textContent.toLowerCase() === p.kit)` against the
kit chips. The brush chip reads "Brushes" while the preset's kit id is
"brush", so it never matched, `setKit` never ran, and no brush preset
ever applied its kit.

It was worse than the report, because the bug is locale-dependent. In
Italian the chips read "Elettronico", "Latino" and "Spazzole", so
electronic, latin and brush all failed there too — only English standard
and jazz ever worked, and only by the coincidence of their label being
identical to their id. Every chip already carries a `data-kit` attribute
holding the real id, so the lookup now uses that. Verified directly: the
old comparison returns false for brush, the new one returns true.

Two other `textContent` lookups nearby were checked and left alone; they
match time signature labels like "4/4", which aren't translated.

**CLEAR wiped the grid and left everything else standing.** The loaded
preset stayed selected and highlighted, its kit stayed active (so
clearing a brush preset left you writing new patterns into brushes), and
its swing stayed applied. It now returns to the custom default the way
the Custom tab's own reset does: steps cleared, kit back to standard with
the chip re-highlighted, swing back to zero with its slider and hint
updated, and the category switched to Custom.

BPM is deliberately NOT reset, even though `_applySnapshot`'s blank path
sets it to 90. The drum BPM is shared with the main metronome, so
clearing a drum pattern must not pull the metronome's tempo out from
under whatever else is using it.

Also confirmed while in here, and left for a decision rather than
changed: the Progression tool's groove drawer and the metronome's groove
panel are not merely displaying the same highlight, they share one piece
of state. Progression's card click calls `grooveLoadPreset`, which writes
the global `groovePresetId`, and also forces `grooveModeActive = true` —
so choosing a groove in Progression flips the metronome out of METRO into
GROOVE mode as a side effect. The highlight is therefore accurate rather
than stale; what's questionable is the two tools sharing one selection at
all. Unpairing them is a design change, not a bug fix.

## v0.136.6 — The bass layer nothing could stop: addLowFreqHarmonics returned no handle

Reported that subfamily tabs still didn't stop playback. Tested directly
by clicking the real tab in the DOM after starting a strum, and the
switch itself was correct: nodes went 5 to 0, subtype changed, button
restored. So the switch was doing its job and something it couldn't see
was still sounding.

**`addLowFreqHarmonics` returned nothing.** It creates a gain node and
three oscillators and handed back no reference of any kind, so this
entire layer was unreachable by every stop function in the app. Callers
tracked the note they got from the tone player and had no way to know
this existed alongside it.

It only runs below 200Hz, which is why it hid for so long and why it was
worst in the reported case. Standard guitar's low E is 82Hz; baritone
guitar is tuned B1 to B3, so nearly every note of a chord triggers it.
Measured on a baritone strum: eleven nodes, five of them harmonic
handles. Before this build those five kept ringing through the switch
while the six tone nodes stopped correctly — which is exactly the
"tracked notes stop, something still sounds" behaviour described.

Now returns a handle that ramps its gain down and stops its oscillators,
and every call site tracks it. That covers the guitar strum, the piano
chord chart, both single-note chart taps, the chord tool's sample path
and the progression bus.

`practicePlayNote` got a slightly different treatment: it returns a
single combined handle stopping both the tone and its harmonic layer,
because its callers reasonably track one node per note. Interval training
is the main one, so the overlap fix in v0.136.3 was silencing the tone
and leaving the bass layer underneath it on low notes — a real remaining
hole in a fix that had been reported as working.

## v0.136.5 — All thirteen chart play buttons, done properly this time

v0.136.4 fixed the piano chord chart because that was the one reported,
and stopped there. Pushed to check the whole tool, the count was thirteen
play buttons, not four, and an audit of every play/stop pair found only
four handled their state correctly.

**What was wrong, per button.** Two had no `id` at all and so could never
show anything: the didgeridoo drone and the fretboard-overlay strum (a
second `gccPlayChord` button, distinct from the one in the main panel).
`hpPlayChord`, `trpPlayCardNote`, `bowedNotePlayCurrent`,
`bowedDsPlayCurrent` and `fluteTrillTogglePlay` never showed STOP. And
`trpPlay`, `bowedScalePlay` and `didiPlay` set STOP and never restored
it, so those buttons sat reading "■ STOP" over silence until something
else happened to redraw them.

**Rather than nine more bespoke label lines**, which is precisely how
this drifted in the first place, there is now a single `CHART_BTNS`
registry naming each button once with its i18n key, plus `_chartBtnPlay`,
`_chartBtnIdle` and `_chartBtnsResetAll`. `chordScaleStopAllAudio` calls
the reset as a backstop, so no instrument switch, subfamily switch or tab
switch can strand a button reading STOP regardless of which chart was
playing. `fluteTrillStop` was also added to that stop list, having been
missing from it.

**Two real bugs surfaced while wiring this, neither of them cosmetic.**
The harp had no chord node list at all — `hpPlayChord` discarded every
node it created and the only list that existed was `hpScaleNodes`, so
nothing anywhere could stop a ringing harp chord, not `hpStop` and not
the global stop. It played straight through instrument switches. Same
fire-and-forget shape as the interval training bug two builds ago. And
`hpPlayScale` never called `hpUpdatePlayBtn`, which is why the harp scale
run was the one chart that stayed reading PLAY for its whole duration;
the restore side was already correct, only the set side was missing.

**One deliberate exception.** `hpPlayBtn` is excluded from the registry
and delegates to `hpUpdatePlayBtn`, because that function picks its label
from `hpScaleDir` — ascending versus descending. Resetting it generically
would have silently relabelled a descending run as ascending, which is
the kind of regression this sweep was supposed to prevent rather than
introduce.

Single-note buttons (wind card note, bowed note, bowed double stop) now
show STOP for the note's actual duration, 1.8s in the bowed case, and
toggle to stop on a second press.

Verified at runtime: every registry id resolves to a real element, no
button remains on STOP after a global stop even when all are forced into
that state first, and the helpers are safe when handed an id that doesn't
exist.

## v0.136.4 — The chart stop button that only worked on fretted, and two more partial copies of the same stop list

**The piano chord chart's play button had no `id`.** That's the whole
reason it was the one instrument that never showed a stop state:
`pccPlay` and `pccStop` had nothing to address, so neither ever tried.
The fretted equivalent has `id="gccStrumBtn"` and works, and the piano
scale chart has `id="pssPlayBtn"` and works. Given an id, `pccPlay` now
shows STOP while the chord rings and `pccStop` restores the label, both
matching what the other three charts already did. Also removed a
duplicated STOP assignment in `pssPlay`, which set the same label twice
in consecutive lines.

**Swapping subfamily or chart tab left audio playing, for the same
reason `stopAllAudio` did: rival partial lists.** There are ten chart
voices and `chordScaleStopAllAudio()` stops all of them.
`switchChordScaleInstrument` correctly called it. But `switchSubType`
called only `gccStop(); gssStop();` — the two FRETTED stops — so
swapping subtype on mallet, sax, harmonica, organ, bowed, harp or
didgeridoo left it ringing through the swap, while guitar behaved. And
`switchGuitarChordMode` (the CHORDS/SCALES tabs) called four of the ten,
missing harp, wind, bowed, organ and didgeridoo.

Both now defer to `chordScaleStopAllAudio()`, so there is one list to
keep correct rather than three that drift apart. This is the third time
in three builds that a hand-maintained partial stop list has been the
bug; the pattern is now consistent enough to be worth watching for
directly.

Verified: the button exists and its label round-trips through
STOP and back, all ten chart stops are safe to call cold with nothing
playing, and none throw.

## v0.136.3 — Interval training notes overlapping between questions: nothing was holding the handles

`ivStop()` looked like it stopped playback and effectively stopped
nothing. `ivPlayReference` calls `practicePlayNote` through `playOne` and
`playBoth` and discarded every return value; only the sing-mode reference
kept a handle, in `ivRefNode`. So the melodic and harmonic notes — the
ones every manual and test round is built from — were fire-and-forget,
with no reference anywhere for `ivStop` to act on.

The session token (`ivSession`) hid how bad this was, because it does
prevent notes that haven't started yet from firing. Notes already
sounding, though, simply ran to their full length: 0.58s melodic, 1.4s
harmonic, 2.7s end to end for mel_harm, with the sample's own release
tail on top of that. Test mode advances on every answer, so the previous
question was still ringing underneath the next one — which is exactly how
it was reported.

Fixed by tracking every node started during playback in `ivNodes` and
having `ivStop()` stop them all. `practicePlayNote` already returns a
stoppable node on both the sampled and the synth path, so the handles
were there to be kept the whole time.

`ivReplay()` had the same fault by a different route: it calls
`ivPlayReference` directly rather than going through `ivStop`, so hitting
replay stacked a fresh playback on top of whatever was still sounding.
Rather than patch that one call site, playback now silences any tracked
notes at the top of `ivPlayReference`, which covers advancing, replaying,
and any future caller that reaches playback another way.

Verified that stopping is robust rather than merely present: tracked
nodes are stopped and the list cleared, `ivStop()` is safe to call cold
with nothing playing, and a node whose `stop()` throws does not prevent
the nodes after it from being stopped.

## v0.136.2 — Module audio that kept playing after you left: stopAllAudio had never heard of the drones

`stopAllAudio()` is the single source of truth for "make it quiet", and it
is a hand-maintained list of function names. Its own comment records that
it drifted once before, when `exitTool` and `exitExercise` kept two rival
lists with different holes. An audit diffing every stop-style function
defined in the file against the ones the list actually calls found it had
drifted again, and considerably further: 43 were missing.

Most of those are missing correctly — per-note and per-voice stops
covered by their module's own stop, animation and timer stops that make
no sound, and mic teardown that must not run on every exit. But the ones
that mattered were the worst possible category: **every drone**.
`stopAllRhodesDrones`, `stopAllPianoDrones`, `stopAllRef`,
`_organStopAll` and `diadleStopDrone` all ring indefinitely by design, so
nothing else was ever going to stop them, and the global "make it quiet"
had never heard of any of them. Alongside those, `riffStop` (20 call
sites), `mqAmbStop`, `hpStop`, `fluteTrillStop`, `tpStopAudio`,
`rcStopPlayback`, `thmnStopDemo`, `tonaleStopCompare`, `tonaleStopWave`,
`rtDistractStop`, `rcdStop`, `_bowedStopAll` and `bowedScaleStop` were
all leaking through every exit.

The Survival Guide turned out to be entirely outside the system. It runs
its own separate `AudioContext` in a later script block, and its
module-level stop, `stopAllSounds`, was not in the list — so backing out
mid-cadence left it playing. `sgStopCadence` isn't reachable on `window`,
so wiring that directly would have been a silent no-op; the fix calls
`stopAllSounds`, which is global and stops the cadence internally.

Every newly wired function was verified callable cold, with no module
open, since `stopAllAudio` fires on every module exit and on
backgrounding: none throw, and calling `stopAllAudio()` twice from a
standing start is clean. Coverage goes from 32 functions to 52.

**Added `intonare_stopall_audit.py`.** A list that has now drifted twice
will drift a third time, so this diffs defined stop functions against
called ones and fails on anything that is neither wired in nor named in
an exemption table with a stated reason. Adding a new stop function now
forces a decision instead of allowing silence.

Deliberately left alone pending a decision: `stopMic`, `_nativeMicStop`
and `vrStopDetect` are mic-side, and wiring them here would tear down the
mic stream on every module exit and every backgrounding, which would
break tuner resume. They are exempt with that reason recorded rather than
quietly omitted.

## v0.136.1 — Duplicate master buses, and making the loud setting conditional on the limiter actually existing

Reported still clipping, with the right question attached: are the sounds
routed correctly? They weren't.

**The master bus cache was a single slot, and this app runs several audio
contexts** — the main one plus dedicated contexts for the tuner, tone
generator, practice, drum kit and latency probing. A second context
overwrote the slot; when the first context asked for its bus again the
stored one no longer matched, so a SECOND bus was built for a context
that already had one, with both still connected to the destination.
Every sound on that context then ran through two parallel paths summing
into the same output, which clips harder than having no limiter at all.
The worklet promise was a single slot for the same reason, so only the
first context could ever receive a real limiter and the rest silently
stayed on the fallback shaper. Both are now keyed per context, verified
by interleaving `_getMasterOut` calls across three contexts and checking
each one gets exactly one stable bus.

**Second, and more likely what was actually audible: the loud setting was
unconditional.** v0.136.0 raised SYNTH_HEADROOM from 0.32 to 0.7 and
removed the per-chain ceiling shapers in the same build. Both are correct
when the lookahead limiter is running. If the worklet fails to load on a
given device, though, that combination is the worst of all worlds — a
level raised on the assumption of protection that isn't there, with the
old protection already removed. The worklet loads fine in Chrome over
http, and fails on file:// where blob module loading is blocked, which is
exactly the kind of environment-specific difference that shouldn't be
assumed away for a device that can't be inspected from here.

So the headroom is now adaptive: it starts at the conservative 0.32 and
is raised to 0.7 only once the limiter is confirmed installed and running
on the app's primary context. A worklet failure can now only ever sound
quiet, never distorted.

**Added `audioPathStatus()`**, callable from a device console, reporting
per context whether the true lookahead limiter or the fallback shaper is
carrying the ceiling, the install state, and the headroom currently in
force. Four builds were spent inferring the state of the audio path from
how it sounded; this makes it readable on the hardware it actually
matters on.

## v0.136.0 — One master bus, one true lookahead brickwall limiter, and the app can finally be loud

The question that produced this build was the right one: other music apps are
loud and don't clip, so what's the professional version of this? The answer
turned out to be architectural, not a tuning value.

**The structural problem: there was no master bus.** Around 30 separate places
connected straight to `ctx.destination`, each carrying its own
`DynamicsCompressor`, each limiting as though it were the only thing playing.
Organ plus metronome plus drum kit plus an achievement cue is four independent,
near-full-scale signals summing at the output with nothing supervising the
total. No per-chain limiter can fix that, because none of them can see each
other. That is the real reason the app couldn't be loud without distorting, and
it's why professional audio software routes everything through a single master
bus with one limiter at the end.

**Why `DynamicsCompressor` was never going to do this job.** It has no
lookahead. It reacts only after a peak has arrived, and its detector is
RMS-like, so coherent transients are out the door before gain reduction starts.
The standard approach — what every mastering limiter does — is to delay the
audio a few milliseconds while analysing the undelayed copy, so the reduction is
already in place when the peak lands, and to ramp the gain rather than step it,
since an abrupt gain change generates harmonics that weren't in the source. The
ceiling waveshaper in this file existed purely as cleanup for that leakage, and
a shaper doing heavy continuous work is itself distortion — which is exactly
what v0.135.5 measured happening on every synth voice.

**Built: a real lookahead brickwall limiter as an AudioWorklet**, 5 ms
lookahead, ceiling at -1 dBFS (industry practice is -1.0 to -0.1, the margin
being for intersample peaks that only appear after reconstruction in the DAC),
80 ms release. The worklet source lives in a template string and loads from a
Blob URL, so the single-file build is preserved.

The detector is the part that matters, and the first attempt got it wrong: it
took the instantaneous sample peak and ramped toward the required gain with a
one-pole attack, which lags the very peak it exists to catch. Measured, that
version let an 8x-full-scale input out at 3.07 — reducing, but nowhere near
brickwalling. The correct design takes a sliding maximum over the entire
lookahead buffer (every sample still queued for output), computed with a
monotonic deque for O(1) per sample. Because the detector sees every sample
before it's heard, the required reduction is always already applied, and the
ceiling becomes a guarantee rather than an approximation. Attack is therefore
structural, not a time constant; only release needs smoothing. Re-measured:
inputs from 0.9 to 8.0 all emerge at exactly 0.891 with zero samples over, and
anything already under the ceiling passes through completely untouched.

**Per-chain ceiling shapers removed**, from both `buildLimiterChain` and the
organ chain. With a real limiter at the end they were actively harmful: they
squash at 0.9 before the limiter ever sees the signal, turning clean gain
reduction back into the continuous waveshaping the whole exercise set out to
remove. The master bus keeps an identical shaper as its fallback, so protection
is never absent — just applied once, in the right place.

**Loudness restored: `SYNTH_HEADROOM` back up from 0.32 to 0.7.** The 0.32
value existed only because a waveshaper had to be kept out of its squashing
range. Measured, 0.7 is where usefulness tops out: a single note peaks at 0.828,
just under the ceiling, so solo notes pass with no gain reduction at all, while
chords are caught cleanly. Beyond that it's gain reduction without loudness —
three-note chord RMS is 0.420 at headroom 0.7 and 0.421 at 0.9, the point where
a limiter stops making things louder and only makes them flatter. Solo-note RMS
more than doubles against 0.32.

**Fallback behaviour.** `AudioWorkletProcessor` has been available across
browsers since April 2021, so both Android WebView and WKWebView support it on
any version this app targets. It's still loaded defensively: the master bus
works from the moment it's created using the shaper, and the worklet is swapped
in only once it has actually compiled, connecting the new path before tearing
down the old one so no buffer renders into silence. If it never loads,
behaviour is what shipped before. Both paths were verified — worklet attached
and every chain building on the real app context, and a clean load with the
worklet blocked.

Two bugs were caught by testing rather than review while building this: the
install returned an already-resolved promise to concurrent callers instead of
the in-flight one, and the async swap read the bus from a global at completion
time, so a context created during the load window left it silently targeting a
stale object while still reporting success.

Everything routes through this now — synths, samples, metronome, drums, cues,
Road Trip, every module. That was the ask.

## v0.135.5 — Every synth voice was over full scale on a single note; one global headroom factor fixes all of them

v0.135.4 fixed the organ's missing ceiling shaper, which was real, but
the report that piano still crackled meant the organ was never the whole
story. So the same offline-render harness was pointed at every synth
voice in REF_TONES, twice: once through the real `buildLimiterChain` to
see what reaches the DAC, and once through a bare gain to see what the
voices actually generate.

**Nothing hard-clips anywhere — and that was hiding the problem.** Almost
every voice sat at exactly 0.959 in the first sweep, including a bare
sine on a single note. That number is the ceiling shaper's asymptote, so
what looked like "no clipping" was actually the shaper pinned flat out
on essentially every note.

**The bare-gain sweep showed why.** Every synth voice generates over full
scale on a SINGLE note — sine 1.18, tuba 1.16, brass 1.32, harmonica
1.38, trumpet 1.41 — and 2.4x to 3.5x over on a three-note chord. The
ceiling was squashing a 3.5x overshoot continuously. That isn't
protection, it's permanent waveshaping distortion on every note, and it
is the crackle that has been audible across all synth voices from the
start. It also explains the clue that turning an instrument's volume to
soft nearly cured it: dropping the level was the only thing that got the
signal back under the shaper's 0.9 identity threshold.

**Fix: a global `SYNTH_HEADROOM` of 0.32 folded into `_synthTrim`.** That
function already existed as the per-tone loudness calibration applied by
the wrapper around every synth, so this scales all voices together and
leaves the relative balance that sweep established untouched. It lives
inside `_synthTrim` rather than in the wrapper because several
`addLowFreqHarmonics` call sites read the trim directly — putting it here
means the harmonics layer scales with its voice instead of overpowering
it once the voice got quieter. Sampled voices don't route through
`REF_TONES.synth` and are unaffected, which is correct, since samples
were never the ones crackling.

After: single notes land at 0.22-0.67 with the shaper fully out of the
way, and three-note chords touch it lightly instead of being crushed.

**The organ's local makeup cut from v0.135.4 is reverted to 4.0.** It was
a local answer to what turned out to be a global problem, and with
SYNTH_HEADROOM in place the two stacked and left the organ at a 0.19 peak
on a single note. Its ceiling shaper — the genuinely missing piece —
stays. Organ now measures 0.35 on one note up to 0.96 on six, reaching
the ceiling only on dense chords.

0.32 is a starting value chosen to put chords near the threshold rather
than a derived constant. If everything now sounds clean but too quiet,
that one number is the dial, and master volume compensates in the
meantime.

## v0.135.4 — The organ was clipping the DAC on a single note, found by rendering the actual code instead of reasoning about it

Four builds of hypotheses went nowhere, so this one started by rendering
the app's real organ synth through an `OfflineAudioContext` in a headless
browser and reading the output samples directly. The answer was
immediate and not subtle.

**A three-note chord peaked at 1.59 with 7,265 of 96,000 samples pinned
over full scale** — 7.6% of the output hard-clipping at the DAC. A single
note peaked at 1.05, already over. That is the crackle, and it explains
every symptom that made no sense before: it never tracked note count,
register or registration because it was clipping in all of them, and
drawbar changes only altered which harmonics were clipping, not whether
clipping happened. It also explains why the previous three fixes did
nothing — they were tuning stages upstream of a problem at the output.

Worth being blunt about the earlier Python simulation of this chain: it
predicted a 0.59 peak and it was wrong, because it modelled the gain
stages but not the `DynamicsCompressor`'s actual behaviour. Simulating a
chain from its component values is not the same as measuring it, and the
measurement was available the whole time.

**Root cause: `_getOrganChain` had no true-peak ceiling.** Every chain
built by `buildLimiterChain` ends with a ceiling WaveShaper after the
makeup gain, and the comment there already spells out why: a compressor's
attack lets coherent onsets through uncompressed, and no compressor
setting fixes peak leakage — a shaper after the makeup does. The organ
chain ended at a bare `DynamicsCompressor`, which detects on something
RMS-like and therefore waves through exactly the kind of signal an organ
produces: nine phase-locked harmonics per voice, several voices summing
coherently.

**Two changes.** The ceiling shaper is now in the organ chain, matching
every other chain in the app. And the makeup gain drops from 4.0 to 2.2,
because with the ceiling alone the shaper would have been working
constantly rather than catching occasional peaks. Measured after:
single note 0.59, three notes 0.96, six notes 0.96, zero clipped samples
at any polyphony. The registry entry feeding live master-volume updates
was moved to the new base too — left at 4.0 it would have restored the
clipping level the moment the volume slider moved.

The organ is quieter than it was. That is the correct trade: the old
level was never reaching the speaker intact. Chords still ride the
ceiling's asymptote at 0.96, so if it now sounds clean but too quiet
there is a further loudness-versus-headroom adjustment available.

## v0.135.3 — Audio graph node leak in the organ voice, and the same pattern found across 11 synth voices

New information reframed the whole investigation: the crackle is not
organ-specific. Every synthesized voice tends toward it, while sampled
voices don't. That rules out the organ's own chain (which is where the
last three builds were digging) and points at something shared by
synthesis but not playback.

**Found: synth voices leak audio graph nodes.** `voice.stop()`
disconnected `toneBus` and nothing else. The per-voice output gain `g`
stays wired to the organ bus permanently, and the key-click filter and
gain connect straight to the bus on every single note-on and are never
disconnected at all. Stopping an oscillator releases the oscillator;
GainNodes and BiquadFilters attached to the bus are not released by
that. Fixed by tracking every output-facing node in a `_toDisconnect`
list and tearing all of them down together.

**Second, worse leak: finite-duration voices never called `stop()` at
all.** Chart and scale taps pass a `dur`, so their oscillators self-stop
via `o.stop(when+dur)`, but nothing ever ran the teardown — so those
voices leaked their nodes AND their `_organActiveVoices` entry forever,
meaning the voice list itself grew without bound for the whole session.
Only the manual keyboard (which passes `dur: null` and releases on
key-up) was being cleaned up. Now a matching teardown is scheduled when
`dur` is set.

**The pattern is not confined to the organ.** A sweep of `REF_TONES`
found 11 synth voices — sine, piano, flute, bell, marimba, xylophone,
vibraphone, pad, guitar, brass, melodica — that create GainNodes and
BiquadFilters per note and contain zero `.disconnect()` calls anywhere.
The organ was the only voice doing even partial cleanup, and it was the
one being investigated purely by coincidence.

Deliberately not overclaiming this as the fix: Chrome can reclaim some
orphaned nodes once their inputs finish, so whether this fully accounts
for the audible crackle is an on-device question, not something the code
alone settles. The decisive test is whether crackle worsens across a long
session and clears after an app restart — that signature would confirm
accumulation. Sweeping the remaining 10 voices is queued behind that
answer rather than done blind.

## v0.135.2 — Two speculative organ fixes reverted, and the one real gain-staging flaw found by measurement

**Reverted v0.135.0's phase-decorrelation drift LFOs and v0.135.1's
polyphony bus rebalance.** Neither changed anything on-device, and a
numeric simulation of the whole organ chain explained why: nothing in the
signal path was clipping in the first place. Measured across every
polyphony and registration, the signal reaching the WaveShaper sits at
0.03-0.11 — deep in the tanh curve's linear region — and output peaks at
0.59 against a 0.84 limiter threshold, with master volume capped by
`_getEffectiveScale` at an effective peak of 0.82 even at maximum. Both
fixes were solving a problem that didn't exist. The drift LFOs also cost
two extra oscillators per voice, so leaving them in was a real expense
for no benefit. The v0.135.0 mass-release stagger stays — that one
addressed a genuine mechanical issue (every held voice's oscillators
being truncated on the identical sample when the pedal releases them all
in one tick) independent of any clipping question.

**The one thing measurement did find: chorus adds amplitude with no
compensation anywhere.** The `isChorus` branch creates a second
oscillator per active drawbar at 0.5x that bar's gain, so a chorus voice
carries roughly 1.5x the amplitude of the same voice with chorus off, and
nothing downstream accounted for it. On a low five-note chord that's
0.586 peak with V/C off versus 0.871 with chorus — the only configuration
in the entire sweep that crossed the limiter threshold. Vibrato is
unaffected since it only modulates detune and adds no layer. Fixed with a
chorus-only trim on the per-voice gain target, applied to `_gTarget`
rather than the bar gains because `_organUpdateLive` recomputes barGains
from `bars` on every live drawbar move (which would undo it) while
deliberately preserving `v.gTarget`.

Worth being straight about scope: this is a real flaw and it is the
correct fix, but the measured overshoot is small and it may not be the
whole of the reported crackle. The headphone/high-chord/no-16' tests are
still the thing that will say whether the remainder is digital or the
phone speaker giving up on sub-bass.

## v0.135.1 — Organ crackle, take two: the real culprit was fixed headroom, not phase drift

v0.135.0's phase-decorrelation fix didn't move the needle on-device — right
instinct (static detune re-locking is real) but not the dominant cause.
Correct diagnosis: `_getOrganChain`'s `drive` gain is a FIXED value sized
for "about 5 voices." Actual playing swings from one held note to a full
chord across both manuals — with fixed headroom, more simultaneous voices
just means a bigger combined signal driving deeper into the tanh
saturation curve. Tanh never hard-clips, but deep in the curve it
compresses hard and throws heavy intermodulation distortion across every
stacked sine partial — that's the buzz, and it scales with polyphony, not
with detune phase.

Fix: `_organRebalanceBus()` now scales the organ bus gain down as active
voice count rises (gentle curve, not 1/N — full chords should sound
fuller, not just quieter) and back up as notes release, so the combined
signal hitting the drive stage stays roughly constant regardless of how
many notes are stacked. Hooked into every voice add/remove path: the
synth's own internal push/removal, the chart-tool push, and (via
`voice.stop()`) every note-off route including the pedal's mass-release.

Also noted in passing, not touched: `pssPlayNote` (scale-chart organ
voices) pushes the voice returned by `synth()` a second time — `synth()`
already pushes it internally, so that path double-counts in
`_organActiveVoices`. Pre-existing, out of scope for this fix, flagged
for its own pass.

## v0.135.0 — Two organ crackle bugs, both root-caused instead of patched over

**Held-chord buzz that shows up a little after the note is pressed, then
clears — worst on bass, worst with Leslie off.** The per-bar drawbar
detune (`_BAR_DETUNE`, added earlier to stop the attack-instant coherent
peak) is a fixed cents offset per bar. That's fine at the moment of
attack, but on a HELD note those fixed offsets keep drifting in and out
of phase alignment forever — every time they drift back into alignment
the summed peak spikes and overdrives the saturation curve. A fixed
cents gap is a smaller absolute Hz separation down in the bass, so the
drift cycle runs slower there, which is exactly why the bug reads as
"worse on lows." And Leslie's own vibrato LFO already scrambles phase
continuously, which is why the whole thing nearly vanished whenever
Leslie was on — turn it off and the static detune has nothing left
disrupting it. Fix: two ultra-slow, ultra-shallow LFOs (10-20s period,
well under audible-vibrato depth) now run continuously on alternating
bars, independent of the Leslie setting, so harmonics never resettle
into a fixed relationship long enough to spike. Applied to both the main
bar oscillators and the chorus dry-copy oscillator.

**Pedal press crackle/buzz burst with multiple notes held.** Separate
bug, same neighborhood. `voice.stop()` schedules every oscillator's hard
`.stop()` at an identical `ctx.currentTime`-derived sample — fine for a
single note release. But `_organStopAll()` (what the hold pedal calls)
stops every active voice in the same JS tick, so with several notes
held, every oscillator across every one of those voices got truncated on
the exact same sample. `.stop()` chops mid-waveform, not at a zero
crossing, and the gain is still mid-fade at that point (`setTargetAtTime`
approaches zero but never truly hits it) — so several simultaneous
truncations stacked into one audible crackle. Fixed by giving
`voice.stop()` an optional stagger offset and having `_organStopAll()`
space each voice's stop a few ms apart, so the truncations land on
different samples instead of colliding.

Both awaiting an on-device listen to confirm — this is a "does it
actually sound fixed" call, not something a syntax check settles.

## v0.134.11 — Drumkit preset panel two-tone split, and every remaining instance of the gradient-flip bug found in one pass

**Drumkit preset panel: two sibling panes on two unrelated background
tokens.** Reported with a screenshot — the category rail (left) and the
preset list (right) read as two different brightness levels sitting side
by side. Cause: the rail used `var(--surface)` (near-white in light mode,
`#ececf6`) and the list used `var(--bg-1)` (`#b0b0d9`, a medium lavender)
— fine as two points on the same ramp in the abstract, but never
designed to sit edge-to-edge as siblings, and the gap between them is
small in dark mode and enormous in light mode. Unified both panes onto
`--surface`.

**Then the real question: how many more of these are there, and is there
a faster way than finding them one screenshot at a time?** Every color
bug this week — achievement categories, Chordle/Diadle/Tonale pickers,
the daily buttons, the chord/progression play buttons — turned out to be
the same mechanical shape: a CSS variable that deliberately flips
brightness direction between themes (`--accent`, `--accent-warm`,
`--accent-soft`, `--grad-*`), paired with a hardcoded literal text color
that assumed one direction. That shape is fully greppable. Wrote a script
that finds every gradient-background CSS rule built from one of those
theme-flipping variables, checks whether it hardcodes a literal color
instead of a theme-aware one, and reports every hit in the file at once
rather than waiting for the next screenshot to find the next instance.

**Result: five total matches file-wide. Two were already fixed
(v0.134.10's chord/progression play buttons). Three more found and fixed
in this build:**
- `.mq-daily-pop-start` (Music Quiz daily result popup)
- `.prog-sheet-confirm-btn` (Progression tool's save-sheet confirm)
- `#exIntervals .iv-mode-btn.active` (interval training mode toggle)

All three turned out to be a variant one step worse than the play
buttons: each gradient mixes a theme-flipping variable with a *second,
hardcoded* stop that never flips, so in light mode the gradient itself
spans dark-to-light internally — computed contrast confirmed neither
black nor white text can clear 4.5:1 against both ends of a gradient
shaped like that. Fixing the text color alone couldn't have worked here;
each got its own light-mode gradient instead, built from two stops in the
same dark family (matching the palette already established for
`--accent-warm`/`--accent-soft` light-mode ink elsewhere), so one white
ink now reads cleanly across the whole button.

**Five for five, file-wide, in one pass — this is the shape of thing that
should stop recurring, not the last instance of it.** Which is the honest
answer to "isn't there a better way than finding these one at a time":
for this ONE specific pattern, yes, and it's done. It doesn't generalize
automatically to the other three patterns behind this week's bugs
(bright accent colors used as ink with no light variant; glow/blur
effects that are a dark-UI-only idiom; sibling elements pulled from
different points on the color ramp, exactly like today's preset panel) —
those aren't mechanically greppable the same way, and finding the rest of
them needs either the wider audit sweep or a real token-level redesign,
not a bigger regex.

## v0.134.10 — chord/progression play buttons, and three near-misses investigated and left alone

Continuing the v3 audit's list. This batch turned up two more real hits
of the same `--grad-*` direction-flip bug as v0.134.9's daily buttons,
and — just as important — three flagged items checked and confirmed
fine, not fixed, because they weren't actually broken.

**Two real bugs, same root cause as last build.** `.chord-play-btn`
("PLAY" in the Chords tool) and `.prog-play-btn` ("PLAY" in Progression)
both pair `background: var(--grad-warm)` with hardcoded `color: #000`.
`--grad-warm` is a light salmon-to-pink gradient in dark mode (black
text correct) and a dark burnt-orange-to-maroon one in light mode (black
text nearly invisible) — identical shape to v0.134.9's fix, different
buttons. Measured 1.31:1; now white text in light mode, confirmed
cleared by the audit and by a fresh screenshot.

**Three flagged items checked, not touched:**
- `.iv-btn.primary` ("START" in ear training) — measures ~3.86:1 by hand
  calculation against the audit's 1.32:1, and reads clearly in a real
  screenshot. Already uses `color: var(--bg-0)`, which is the correct
  theme-aware approach; this is a near-miss, not a break, in the same
  category v2 already allowlists elsewhere. Left alone rather than
  fixing a number instead of a problem.
- `.tc-start-btn` ("START DRONE" in Tonal Center) — already has a
  deliberate, carefully-reasoned `body.light` override (bright DMG-green
  background, near-black text, part of that tool's considered retro
  aesthetic). The audit's 1.46:1 reading almost certainly caught a
  transitional render state, not the real one. Trusted the existing,
  documented design decision over one unverified number.
- `.gss-play-btn` ("STRUM CHORD" in Guitar Chords) — already uses
  `color: var(--accent)`, which is theme-aware and resolves to a dark
  legible teal in light mode. Screenshot confirms it reads fine. Another
  false positive.

Three checks, three real saves from "fixing" things that already work —
the same discipline as v0.134.8's false-positive cleanup, just applied
per-item instead of to a whole batch at once. An audit is a lead to
verify, not a queue to clear blindly.

## v0.134.9 — Chordle/Diadle/Tonale picker colors, daily-button text, chevron

Continuing the v3 audit's severity-ranked list, working top to bottom.

**Difficulty/mode picker colors were half-fixed already, just not wired
up.** `diffColorFor()` and a `DIFF_COLOR_LIGHT` mapping table already
existed in the file — built for exactly this problem, deepening each
difficulty's bright dark-mode color to an AA-legible equivalent in light
mode. `chordlePickerCard()`, the shared renderer behind Chordle's,
Diadle's, and Tonale's difficulty/mode cards, was passing `color`
straight through instead of calling it. One function was the actual fix;
finding it was the work. Also extended the table itself — Tonale runs
its own distinct four-color palette (`#54d18a`/`#f2c14e`/`#e8743b`/
`#d6455d`) that was never in there, so Tonale's cards weren't improving
even after the wiring fix until this got added too.

**"PLAY THE DAILY" and five other buttons were invisible, not just dim.**
Seven buttons across Chordle/Diadle/Tonale share one gradient background
built from `--accent`/`--accent-soft`, paired with hardcoded `color:#000`.
Correct in dark mode, where those two variables are light colors and
black text reads fine. Wrong in light mode, where the same two variables
are deliberately *dark* (legible-ink versions, same reasoning as
everywhere else) — meaning the gradient itself goes dark and the black
text nearly disappears into it. Same category of bug as the achievement
category colors (v0.134.3): a variable's brightness direction assumed
constant across themes when the theme system deliberately flips it.
Fixed with one attribute-selector CSS rule matching the shared inline
style, rather than touching seven separate button literals scattered
across three files' worth of game logic.

**Chevron arrow (`›`)** on the same picker cards — 0.4 opacity on an
already-modest `var(--muted)`, measuring ~2.06:1. Raised to 0.82;
confirmed clearing 4.5:1 afterward rather than guessing at a number that
looked reasonable.

**Net for this cluster:** 105 audit failures \u2192 11 across Chordle, Diadle,
and Tonale combined, verified by re-running the audit and by a fresh
rendered screenshot (not just trusting the numbers). The 11 remaining are
lower-severity near-misses — an attribution line, nav-label edge cases —
left for a later pass rather than chased for diminishing returns here.

Working the rest of the v3 audit's list top-to-bottom continues next
build; this is one batch of it, not the finish.

## v0.134.8 — a contrast audit that can actually reach the tools, and the three bugs it was built to catch

**Built `intonare_light_contrast_audit_v3.py`.** The standing audit
(`intonare_light_contrast_audit.py`) only ever visits 4 surfaces — the top
screen of each launcher tab, once. Every tool and every exercise —
Drumkit, Volume Meter, Rhythm Cards, Chordle, Road Trip, ~29 of them —
sat behind that top screen and had never been machine-checked once.
Reported with three screenshots this time: Drumkit's preset pills, Volume
Meter's SAFE/CAUTION/WARN/DANGER labels, both genuinely broken.

v3 reaches all of it by calling the app's own screen routers directly —
`enterTool('drumkit')`, `enterExercise('roadtrip')` — the same functions
a real tap ultimately calls, pulled straight out of `enterTool`/
`enterExercise`'s own hidden-class toggle lists so the surface list can't
drift out of sync with what the app can actually show. 4 hub screens + 15
tools + 14 exercises = 33 surfaces per run, up from 4. Same measurement
core as v2 (rendered-pixel percentile sampling — proven more trustworthy
than reading CSS declarations, see v2's own docstring for why).

**The first raw run came back with 278 "failures." Most were noise, not
bugs — caught before treating any of it as a finding:**
- Elements scrolled off-screen in horizontal strips were still being
  measured against whatever sat behind them. Fixed: added a right-edge
  bound to the existing viewport check.
- A meaningful chunk were genuinely tiny glyphs (a single digit, a
  bullet) inside generously-padded containers, where the percentile
  sampler's dark/light picks can both land on background pixels and
  report a false ~1:1. Fixed the common case: measure the text's own
  `Range` bounding box instead of the element's full padded box.
- The rest — Drumkit's category counts and names inside the collapsed
  `PRESETS ▾` panel — are clipped via `max-height:0`, not `display:none`,
  so the hidden-content walk doesn't catch them and they get measured
  as if visible. Not fixed this pass; noted in the script's own output
  rather than silently dropped, since it needs a real visibility check
  (actual rendered pixel area), not another special case.

An audit that reports noise as signal is worse than no audit — v2's own
docstring says exactly that, and v3 nearly repeated the mistake at 70x
the scale on its first run. Every fix here came from checking a raw
result against the real rendered screenshot before believing it, not
from trusting the number.

**Three bugs, confirmed and fixed:**
- **Drumkit preset pills** (Jazz/Latin/Standard/Electronic/Brushes) — the
  pill was fully transparent, relying on the app's carefully-pinned
  `--muted` ink token for contrast. That token is pinned against
  `--bg-0`/a card, not against this tool's own colored wash, and fell
  short here specifically: measured 3.29–3.81:1. Gave the pills their
  own light backing tint so their contrast doesn't depend on guessing
  what's behind them.
- **Drumkit's *active* preset color** — found while fixing the pills
  above: the selected chip's ink was hardcoded bright saturated RGB
  (the same bug shape as the achievement category colors, v0.134.3),
  measured 1.45–2.36:1 across the five kit colors. Added light-mode
  darkened variants for all five, each confirmed 4.65:1 or better.
- **Volume Meter's SAFE/CAUTION/WARN/DANGER labels** — black ink at 55%
  opacity wasn't dark enough against the light pastel band tints.
  Computed the actual contrast needed against all four bands and raised
  to 78%, with margin on every band.

All three verified two ways: the audit's own re-measurement, and a fresh
rendered screenshot checked by eye — the same discipline the audit itself
demands of its own results.

**Rhythm Cards' subtitle, investigated, not reproduced.** Screenshotted
as looking pale near the TEST button. Rendered it fresh, ran it through
the new audit: reads clearly, measures well clear of 4.5:1, not flagged.
Couldn't find a bug here to fix — noting that honestly rather than
inventing a change for something that isn't actually broken.

**Still not covered by v3:** the ~90 modals/overlays/sheets/popups (a
running list of their IDs is in a comment at the bottom of the script,
collected while investigating this so the next pass doesn't start from
zero). Those aren't behind a uniform router the way tools/exercises are;
each opens its own way, which is real additional harness work, not a
config change.

## v0.134.7 — grep sweep for the hardcoded-white-text pattern app-wide

Searched the whole file for the exact bug shape that hit achievements three
times running: `color: rgba(255,255,255,...)` used as ink with no
light-mode counterpart. 61 raw hits. Most were not bugs:

- A meaningful chunk already had light-mode coverage I'd missed on first
  pass — scoped as `body.light #containerID .class` rather than
  `body.light .class`, which a naive check for "does this class have a
  light override" walks right past. The whole piano overlay (~15 of the
  61 hits) falls in this bucket: fully handled already, just not
  adjacent to the rule in the file.
- A larger chunk are deliberately, permanently dark regardless of theme:
  the piano's mode-selector chrome, the drone mute button, the flash
  metronome's fullscreen strobe, the theremin's play pad and volume
  track. There's an explicit comment on the theremin block stating the
  reasoning: instrument "screens" (a play pad, an LED-style readout, a
  strobe display) stay dark on light the way a real piano's key-bed or a
  real synth's LCD would, and that's a considered design choice already
  applied consistently, not an oversight repeated 61 times.

Filtering those out left two genuine, confirmed bugs — same shape as
achievements, different screens: the groove editor's subdivision step
numbers (`.groove-step-num.subdiv`), and the drum kit precision-mode
step numbers and cursor ring (`#toolDrumkit .dk-prec-step-num`, `.cursor`
ring). Both sit on containers that already go theme-adaptive in light
mode (`.groove-step-nums` background, `.dk-prec-step`'s `var(--surface)`)
while the mark on top of them stayed hardcoded near-invisible white.
Fixed both the same way as achievements: a `body.light` override with a
dark low-opacity ink instead of the light one.

This was one grep sweep, not the audit rewrite — it only catches this one
specific anti-pattern (hardcoded white-as-ink) and only where the string
`rgba(255,255,255` appears literally in the CSS. It doesn't catch a wrong
color chosen some other way, and it doesn't touch the ~90 unaudited
modals/overlays/sheets/popups that still have zero machine coverage.
Cheap, fast, and it found two real bugs beyond achievements; the actual
audit-widening work is still open.

## v0.134.6 — seven achievements had no icon at all, silently showing the padlock

**"Some are the same lock icon" — because they were.** `ACH_ICONS[a.id] ||
ACH_ICONS.locked` was doing exactly what it says: any achievement with no
entry in `ACH_ICONS` fell back to the padlock glyph, even when unlocked.
Seven had no entry: The Force Is With You, I Got a Fever, Hard Day's
Night, First Blood, Boom, Giant Steps, Dead Composer. An earned
achievement showing a padlock isn't just uninspired, it reads as broken —
this was a real bug wearing a design complaint's clothes.

Drew all seven to match the existing hand-crafted convention exactly
(24x24, stroke-width 1.5, round caps/joins, main shape drawn twice — once
as a soft low-opacity fill, once as a crisp outline) rather than pulling
from an icon library and hoping it blended in:
- **The Force Is With You** (turn off the targeting computer) → a scope
  reticle with a slash through it, switched off
- **I Got a Fever** (more cowbell) → an actual cowbell
- **Hard Day's Night** (60-minute session, working like a dog) → a hard hat
- **First Blood** (first Chordle solved) → a puzzle grid with a checkmark
  in the first row
- **Boom** (Chordle solved first try — "headshot") → a bullseye, dead
  center
- **Giant Steps** (5 V.Hard Chordles, "living on the edge") → literal
  ascending stairs
- **Dead Composer** (Chordle solved without pressing play — deaf,
  composing anyway) → an ear with a slash through it

Verified two things, not just one: every one of the 40 achievements now
resolves to a real, unique icon (checked programmatically — zero missing,
zero byte-identical duplicates among the dedicated set), and separately
rendered all 40 on one sheet to eyeball the set as a whole rather than
trusting the count alone. Everything else in `ACH_ICONS` held up on
inspection — a couple (Master, Practitioner) lean more abstract than the
rest, but they're not broken or duplicated, so left alone rather than
redrawing icons nobody flagged as a problem.

## v0.134.5 — light mode achievement design, rethought rather than re-tinted; another run at the disappearing-content bug

**The glow fix from last build wasn't enough, and it couldn't have been.**
Screenshots still showed a hazy smudge behind unlocked icons. The actual
problem was never the specific blur radius or opacity — it's that glow is a
*dark-UI idiom*. A blurred color only reads as light bleeding into its
surround when the color is brighter than the surround. That's true of the
old bright saturated colors against near-black. It's structurally never
true in light mode: the color has to stay dark enough to work as legible
ink (v0.134.3's fix), and a dark color blurred onto a light panel is a
stain at any radius, any opacity. No amount of retuning the same recipe
was going to fix that — needed a different technique, not a better number.

Replaced glow with what flat/paper-style UI actually uses for this job —
Apple HIG, Material's light theme, Notion, Linear all do the same thing:
a solid tinted chip behind the icon, no blur, color communicated by fill
instead of luminosity. No filter, no drop-shadow. Common and rare are now
fully static in light mode, which is a better match for this file's own
stated design intent ("cards are the calm part, not the colorful part")
than the previous constant pulsing glow ever was; legendary and secret
keep a small amount of motion (a scale pulse, not a color blur) since
those tiers should still feel like a bit of an event. Same swap applied
to the achievement toast: flat tinted circle behind the icon instead of
the double drop-shadow, and the radial glow wash across the toast
background cut down to a faint corner tint instead of a full wash. Dark
mode is untouched — the original glow techniques are correct there, this
was never a dark-mode problem.

**Disappearing content, third attempt — different theory this time.** The
last two fixes (parent layer promotion, then pausing off-screen
animations) both assumed the trigger was specifically about elements
animating while scrolled off-screen. New screenshots broke that theory:
blank and fully-rendered cards showed up *side by side in the same
viewport at the same time*, which an off-screen-specific bug can't
produce. Also caught the same row flip from blank to fully-rendered
between two screenshots taken moments apart — consistent with the
WebView compositor genuinely falling behind on paint during a fast
scroll and catching up shortly after, not a permanently broken tile.

Removed both previous mitigations (layer promotion stays, harmless;
the custom IntersectionObserver pause/resume hack is gone) and replaced
them with `content-visibility: auto` on `.pm-ach-card`, with
`contain-intrinsic-size` to keep scroll position stable as cards enter
and exit rendering. This is the platform's own answer to "too much
off-screen content for the renderer to keep up with" — it skips layout
and paint work for content nowhere near the viewport, which cuts the
total paint burden during a scroll instead of trying to out-guess
WebView's tile scheduling with more CSS hints. Given two narrower,
targeted theories already came back wrong on-device, this cuts the
actual variable in play (total concurrent paint work) rather than
guessing at a third specific mechanism. Whether it holds still needs
your device, same as the last two rounds — this sandbox has never been
able to reproduce the bug itself, only reason about likely causes and
verify that nothing else broke.

## v0.134.4 — icon glow was a smudge in light mode, disappearing achievements: round two

**Icon glow, light mode.** Reported with screenshots: the icon halo behind
unlocked achievements looked like a hazy colored blob, not a glow. Root
cause was the previous build's own contrast fix: `--cat-c` now holds a
darkened, WCAG-legible color in light mode (needed for the rarity pill and
border text), and that same variable feeds the icon's `drop-shadow` glow.
A drop-shadow blur only reads as *emitted light* when the color is
brighter than its surround — true of the old bright dark-mode colors
against near-black, false of a dark burnt-orange or deep green blurred
onto a near-white panel. That's a stain, not a glow, however you tune it,
and no shared color token can be both a legible dark ink and a convincing
bright bloom at once. Gave light mode its own glow recipe instead of
reusing dark mode's with a swapped color: half the blur radius, every
stop routed through `color-mix()` at 35–60% so the halo stays a light
tint, and dropped the stacked double-`drop-shadow` on rare+ that was
making the smudge worse rather than richer. Applies to both the animated
breathing glow and the static base glow on every unlocked icon.

**Disappearing achievement content — still happening, tried a different
angle.** The `translateZ(0)` layer-promotion fix from two builds ago
didn't hold; screenshots showed the same failure, still isolated to
`rarity-secret` cards (the only rarity, along with legendary, that runs
the animated `@property`-driven conic-gradient border trace). Promoting
the parent card to its own compositing layer clearly wasn't sufficient —
it doesn't necessarily carry down to guarantee the animated pseudo-element
inside it gets the same treatment.

Two changes this time, aimed more at the actual trigger than another
layer-promotion guess: promoted the `::after` trace pseudo-element itself
to its own layer (not just its parent), and — the more likely real fix —
added an `IntersectionObserver` that pauses the border-trace and icon-
breathe animations on legendary/secret cards while they're off-screen,
resuming on scroll-back. These animations previously ran continuously and
indefinitely regardless of visibility. The failure mode this whole time
was plausibly: a card mid-animation scrolls off-screen, WebView's tile
cache discards or reuses that paint, and it comes back mis-composited.
A paused animation has no in-flight paint state for that to happen to —
this removes the precondition rather than hoping a layer hint changes how
Chromium schedules around it. Verified the observer itself works exactly
as intended (23 legendary/secret cards tracked, correctly toggling
between paused/running as the grid scrolls), which is as far as this
environment can confirm; the compositing bug itself is a device-specific
WebView quirk this sandbox has never been able to reproduce, so whether
it's actually gone still needs your eyes on the device, not mine on a
screenshot.

## v0.134.3 — achievement category colors in light mode, toast bleed-through behind open modals

**Achievement category colors were unreadable in light mode too, not just
the text.** `ACH_CATS` — the five accent colors for consistency/accuracy/
exploration/milestones/secrets — were hardcoded `rgba(...)` values shared
between both themes, tuned to glow on near-black. Measured their actual
rendered contrast against the light panel background: as low as 1.17:1 for
milestones (lime), none of the five cleared WCAG AA's 4.5:1 floor. This is
why the rarity pills, category dots, and section headers all read as faint
pastel smudges in the screenshots — same root cause as the text-color bug
from the last build, just on the accent colors instead of the ink.

Gave each category a light-mode-specific darker, more saturated version of
its own hue, chosen by reusing existing app tokens where the hue already
matched rather than inventing new colors: consistency → `--accent-warm`,
exploration → `--accent-soft`, milestones → `--in-tune`, secrets →
`--accent-rose`. Accuracy didn't have an existing match so it got one
custom deep teal. All five now measure 4.5:1 to 9.65:1. Also extended the
existing rare/legendary/secret background tint down to common-rarity cards
(previously flat `--panel` with zero tint) — a small thing, but it's a
chunk of why the achievement list read as a wall of plain white rather
than a set of grounded, categorized cards. Verified both changes rendered,
light and dark, not just computed.

**Audit coverage gap, confirmed and scoped.** `intonare_light_contrast_
audit.py` only opens the four launcher cells (tuner/metro/tools/train) and
screenshots once each — it never opens Profile, Settings, or any modal or
toast, which is exactly where both of the last two contrast bugs were
hiding. Not touched this build; flagging the real size of the gap so it
doesn't get treated as fixed: Road Trip, Rhythm Runner, Music Quiz,
Ladder Climb, and Chordle all sit deeper than the audit's one-tap reach
too.

**Toast rendering corrupted behind an open modal.** While testing the
light-mode fixes above, firing an achievement toast with Profile open
showed the modal's "No practice recorded" text visibly bled through the
toast's background — not a color problem, a compositing one. Confirmed
by disabling Profile's `backdrop-filter: blur(8px)`, which made the
artifact disappear; layer-promoting the toast stack instead (`transform:
translateZ(0)` + `backface-visibility: hidden` on `.ach-toast-stack`) is
the equivalent fix without touching the modal. Same family of bug as the
achievement-card scroll flicker from two builds ago — a Chromium/WebView
sibling failing to composite correctly against a neighboring layer — just
a different trigger: an animated `@property` there, a `backdrop-filter`
neighbor here.

This almost certainly wasn't visible before now: real achievement unlocks
fire during a practice session, when no modal is open behind them. The
long-press test-unlock feature (previous build) made "toast fires while
Profile is open" the normal case for the first time, which is exactly
what surfaced it. Not a regression of the scroll-flicker fix — that one's
still in place and unrelated — but a genuine bug found using the very
feature built to make bugs like this easier to catch.

## v0.134.2 — long-press to test-unlock, achievement panel unreadable in light mode

**Light mode contrast, Profile > Achievements.** Reported with screenshots:
unlocked achievement cards were unreadable — title, italic flavor line, and
condition text all washed out to the point of invisibility. Cause was three
hardcoded `rgba(255,255,255,...)` text colors on `.pm-ach-name` (unlocked),
`.pm-ach-desc`, and `.pm-ach-cond` — literal near-white text that assumed a
dark background and had no light-mode counterpart, plus the same problem on
the locked-card icon color and the progress-bar track background. All five
now resolve through theme variables (`var(--text)`, `var(--muted)`,
`var(--border-soft)`) instead of a fixed color, so they invert correctly
with the theme like everything else on the card already did. Verified
rendered, not just read — headless light-mode and dark-mode screenshots of
the actual expanded card grid, before assuming the CSS change was enough.

This slipped through because `intonare_light_contrast_audit.py` only walks
the four main module screens (tuner/metro/tools/train); the Profile modal's
Achievements panel isn't part of its sweep. Noting it here since the audit
itself wasn't touched this build — a real gap, not a false negative.

**Long-press a locked achievement card to test-unlock it.** Testing the new
sound-unlock toast (v0.134.1) meant resetting all progress and re-earning
achievements by hand to see one fire. Holding a locked card for 650ms now
unlocks that one achievement and runs it through the exact same pipeline as
a genuine unlock — toast, haptic, sound, and the sound-unlock toast above it
if that achievement carries one — instead of `devUnlockAll`'s silent
bulk-unlock. A short tap does nothing; verified the 650ms threshold actually
holds (a 200ms press left the card locked, a 750ms hold fired the toast).

## v0.134.1 — a toast for the sound you just unlocked

**Nothing told you a new cue option existed.** Six achievements unlock a
custom sound (Secret Found, Beethoven's Fifth, Adventurer, Hallelujah, The
Mountain King, Mythic Fanfare) and the achievement toast plays it once at
unlock, but nothing pointed at Settings afterward — the sound just became
selectable and sat there until someone happened to go looking.

Added a second, smaller toast that appears stacked above the achievement
toast exactly when (and only when) the achievement being unlocked also
unlocks a sound: name of the sound, plus which cue categories it's now
available for ("Achievement, Streak" for The Mountain King, "Achievement,
Level Up" for the others). Deliberately kept quiet — no glow, no shimmer,
no bounce, roughly a third the visual weight of the main toast — so it
reads as a bonus detail riding along, not a second achievement competing
for attention. It fades in a beat after the main toast rather than with
it, and both dismiss together.

Built as a stack (`achToastStack`, flex column-reverse) rather than two
independently-positioned fixed elements, so the sound toast's position
above the achievement toast is automatic and survives either toast's
height changing — no offset math to keep in sync by hand. That stack also
had to replace `achToast` in the DOMContentLoaded re-parenting fixup (the
one that rescues modals from the file's deeply-nested broken HTML
upstream); leaving the old id there would have yanked the achievement
toast back out to `body` on load and separated it from the sound toast
sitting above it.

## v0.134.0 — missing haptics on achievement/win/game-over, achievement card scroll flicker

**Haptics gap, four spots.** The seven audio-cue events (correct, wrong,
milestone, level up, achievement, game over, win) all funnel through
individual dispatch functions, but only four of them had a haptic paired
to the sound — correct, wrong, milestone, and level up. Achievement,
game over, and win never got one; there was no `hapticAchievement`,
`hapticGameOver`, or `hapticWin` function to begin with. Every place those
three fire — the achievement toast, the summit-climb win in the ladder
challenge, Rhythm Runner survival's end screen, and Music Quiz survival's
end screen — was sound-only.

Found a fourth, separate spot with the exact same shape: the ladder-climb
game's own terminal-sound dispatcher (`rlpCue`) mapped win/gameover/
milestone to sound at all three of its call sites with zero haptics,
independent of the main event system.

Added the three missing haptic functions (`hapticAchievement` — bright
Light-Light-Medium; `hapticWin` — a bigger build than Milestone, Medium-
Light-Heavy-Heavy; `hapticGameOver` — a fade-out distinct from Wrong's
sharp double-Heavy, Heavy-Medium-Light) and wired them into every real
trigger plus the settings preview, then fixed `rlpCue` centrally so its
three call sites inherit the fix without touching each one.

**Achievement card scroll flicker.** Reported as achievements "losing
visual data" and reappearing after scrolling off and back on. Not a data
bug — `renderAchievements()` builds the DOM once and nothing rebuilds it
on scroll. The likely cause is the legendary/secret rarity cards: they
animate a custom `@property --pm-trace-a` angle driving a `conic-gradient`
border trace on a masked `::after`, on top of `color-mix()` gradient
backgrounds — a combination WebView is known to mis-repaint when the
element scrolls offscreen and the layer gets discarded or reused instead
of re-rasterized. Forced `.pm-ach-card` onto its own stable compositing
layer (`transform: translateZ(0)` + `backface-visibility: hidden`) so the
browser stops trying to reuse the paint mid-scroll.

## v0.133.18 — the unlockable-sound registry refactor

**The architecture cleanup from tonight's design conversation.** Every
secret/achievement-tied cue (Secret Found, Beethoven's Fifth, Mythic
Fanfare, Adventurer, Hallelujah, The Mountain King) used to need edits in
~10-13 places to wire up: an entry in each eligible pool's `_CUE_DEFS.opts`,
a branch in each pool's dispatch function, a line in `_sndKey`, two i18n
lines, a line in the gate filter, plus `PROG_DEFAULTS`/`progMigrate`/
`devUnlockAll` for the unlock flag. That's exactly the surface where
tonight's wrong-achievement mistake happened — no single source of truth
for "what unlocks what, and where can it play."

Added one `UNLOCKABLE_SOUNDS` registry — a single array, one entry per
sound, declaring its play function, its unlock flag, which pools it's
eligible for, and (where relevant) which achievement id triggers it.
Everything downstream now reads from it instead of repeating itself:
`_CUE_DEFS` pool opts, all three dispatch functions (`playCueAchievement`,
`playCueLevelUp`, `playCueMilestone`), the picker's gate filter, `_sndKey`,
`devUnlockAll`, `progMigrate`, and the achievement-toast override all
collapsed from ~40 hand-written lines total down to a handful of generic
lookups. Adding the next unlockable sound is one registry entry, not a
hunt through ten places.

`PROG_DEFAULTS` and `checkAchievements()`'s 3-line flag-set were
deliberately left alone — the former for six flat lines not worth
restructuring, the latter because zelda and adventurer set their flags
through separate bespoke trigger paths (Road Trip completion) that don't
flow through the same loop as the other three, and generalizing it would
have silently widened scope.

**Verified with an actual behavioral diff, not just review.** Built an
offline spy harness (same `node-web-audio-api` tooling as the volume
measurements) that snapshotted every pool/key dispatch resolution and
every gate-filter visibility state *before* touching any code, then
re-ran the identical driver against the refactored code and diffed:
41 test cases, zero differences. The one real behavior change — Level
Up's Secret Found/Beethoven's Fifth/Hallelujah cues now respect the cue
volume slider, which they silently ignored before — doesn't show up in
that diff since it only checks which function fires, not its arguments;
confirmed safe separately since all three already handle that parameter
correctly in their other call sites.

## v0.133.17 — Mountain King moved to Streak

Swapped Mountain King's second pool from Level Up to Milestone/Streak —
perseverance fits a streak better than a level-up moment. Out of
`_CUE_DEFS.levelup.opts` and `playCueLevelUp()`, into `_CUE_DEFS.milestone.opts`
and `playCueMilestone()`. Gate filter needed no change — it already checks
`mountainking_unlocked` generically regardless of which pool's rendering it.

## v0.133.16 — Mountain King moved to the right Summit

**Wrong achievement.** Last release wired the Mountain King chime to
`clean_summit` ("The Force Is With You") based on how it had been tagged
through the prototyping conversation — should have been `the_summit` ("The
Summit," the Hardcore Polyrhythm climb specifically). Moved everything:
the achievement-unlock override, the `mountainking_unlocked` flag-set in
`checkAchievements()`, and the doc comment. `clean_summit` is back to
exactly what it was before — the plain achievement cue, no override,
nothing left behind.

**The Summit is now named The Mountain King.** Renamed the achievement
itself (`name:` field) since Hardcore-specific felt like it earned the more
evocative name over the general Climb.

## v0.133.15 — The Mountain King joins the achievement chimes

**Grieg's In the Hall of the Mountain King is now the clean_summit ("The
Force Is With You") achievement chime.** The lighter version from the last
prototyping round — dropped the sustained drone, quieted the octave doubling
— wired in following the exact same pattern as the other four special
achievement chimes: dedicated override at unlock time, its own
`mountainking_unlocked` flag (PROG_DEFAULTS, migrate, devUnlockAll,
checkAchievements, and the picker's gate filter all touched), selectable in
both the Achievement and Level Up pools once earned.

Measured it against its achievement-pool siblings before shipping this
time — landed 6.5dB hot on the first pass, corrected with a measured 0.473
gain factor, re-verified at dead-even with the pool average. Given what the
last release found, checking before shipping instead of after seemed like
the actual lesson to take from it.

One assumption worth flagging: there are two "summit" achievements —
`clean_summit` ("The Force Is With You", the regular Climb) and
`the_summit` ("The Summit", Hardcore-specific). Wired to `clean_summit`
based on how this had been tagged throughout the prototyping conversation;
straightforward to move if that's not the one intended.

## v0.133.14 — actually measured the volumes instead of guessing

**Funiculì's stutter, fixed.** The first note was a leftover from an earlier
"shorten it" pass and read as an awkward stutter against the rest of the
phrase. Dropped it, re-timed everything after to fill the gap.

**Built a real offline measurement harness** (`node-web-audio-api`, an actual
OfflineAudioContext implementation) to check whether the three new cues from
recent releases were louder than their pool-mates — not by ear, by rendering
each cue's real audio graph and comparing RMS. They were, badly:

| Cue | vs. pool average |
|---|---|
| Hallelujah (Completionist) | +22.3 dB |
| Press F (Game Over) | +16.5 dB |
| Funiculì (Win) | +14.3 dB |
| Valkyries (Mythic Fanfare) | +0.7 dB — already fine |

Root cause: these three route through the shared `_es*` primitives, where
several simultaneous voices (chord tones × doubling × sparkle layers) each
get their own independent limiter chain during cue playback rather than a
shared bus, so nothing was compressing the sum — the individually-reasonable
per-voice gains just added up. Valkyries used the older hand-rolled
`playAdventurerChime`-style pattern instead (single voice at a time, no
stacking), which is why it was never off in the first place.

Applied measured correction factors (0.077 / 0.15 / 0.193) directly to each
cue's gain values, then re-measured against the corrected production code to
confirm convergence — all four now sit within 4 dB of their siblings, game
over and win essentially exact.

**Mountain King's "too thick" preview is being reworked** — prototyping in
the standalone mockup first, not in this build yet.

## v0.133.13 — Mythic Fanfare is Ride of the Valkyries now

**Replaced the chiptune square-wave Mythic Fanfare with real Wagner.** Went
through a real prototyping pass first: full phrase felt too long/insistent
against the Mythic card's 3.6-second display window, a tag+payoff hybrid
landed better, a "filled out" version with timpani/octave-doubling/a
sustained pad sounded worse (the static pad fought the actively-moving
melody — lesson: a drone only works when it tracks the harmony, not just
sits under it). Ended up on the plain second half of the real phrase — the
turn into the big A4 leap, landing on a held F#4. Real notes from an actual
trumpet transcript, confirmed B minor, 9/8 meter.

Matches the same pattern `playAdventurerChime` already established: local
`brass()` helper with a proper sustain hold, a short convolver room (a
fanfare with no tail sounds like a doorbell), direct destination connection.
No dispatch changes — same function name, same two call sites as before.

## v0.133.12 — the staccato bug, and some housekeeping

**Found the actual cause of the new cues sounding clipped in-app versus the
mockups: `_esSaw` and `_esTone` never had a sustain phase.** They ramp up on
attack, then immediately start decaying — an AD envelope, not ADSR. My
mockup's custom voices held a real plateau before releasing; porting to the
app's shared primitives silently dropped that. Added an optional `sustain`
param to both (backward compatible — existing callers untouched, only cues
that pass it get the hold), and wired it into the Hallelujah and Funiculì
cues. The limiter chain was a red herring: it builds a fresh instance per
note during cue playback rather than a shared one, so it wasn't compounding
across notes the way it looked like it might.

**Hallelujah, trimmed.** Was playing both "Hallelujah" statements (measures
4 and 5); cut to just the first — it was running long next to the other
achievement chimes.

**Sad Trombone → Press F.** Better reference for the joke.

**Level Up can now play Secret Found, Beethoven's Fifth, or Hallelujah.**
Turned out `playCueLevelUp()` already had dead branches for `secret_chime`
and `beethoven_chime` — dispatchable but never exposed in the options list.
Finished that and added Hallelujah alongside them, so the achievement pool
isn't the only place these live once you've earned them.

## v0.133.11 — three real songs join the cue pool

**Three new audio cues, built from real MIDI transcriptions instead of guessed
melodies.** All three went through an extended prototyping pass in a standalone
mockup before landing here — real notes verified against source files, tempo
and voicing dialed in against feedback, then ported into the app's own synth
primitives (`_esSaw`, `_esBell`, `_esTone`, `_esSub`) so they inherit the
shared limiter chain like every other end-state cue.

**Hallelujah — new Completionist achievement chime.** Real chords from a
piano-solo arrangement of Handel's Hallelujah Chorus, measures 4-5: F#4-A4-D5,
D4-A4, D4-G4-B4, D4-F#4-A4, repeating, over the real walking bass line. Follows
the same pattern as the Zelda/Beethoven/Adventurer chimes — a dedicated
override at achievement-unlock time, plus a `completionist_unlocked` flag so
it's selectable in the achievement sound picker once actually earned. (Also
added to `devUnlockAll()` this time, learned that lesson already this
release.)

**Sad Trombone — new Game Over option.** Real first six notes of Taps, cut at
"gone the—": F4-F4-Bb4-F4-Bb4-D5, confirmed Bb major bugle triad. Cartoon/sad
character from a wobbly vibrato and a muting lowpass, not a big pitch-bend
slide — that read as too much. One low "womp" under the final note only.

**Funiculì — new New Record option.** Real notes from measures 68-71 of an
actual Funiculì Funiculà MIDI — the "Funiculì, funiculà!" tagline hook, choir
line rendered as a light flute tone, piano kept as piano. Compressed well
under the source tempo for a frantic, comedic-urgency win moment.

## v0.133.10 — the preview button only unlocked half the secrets

**Adventurer wasn't broken where it looked broken.** The achievement badge
unlocks fine from UNLOCK ALL (PREVIEW) — `devUnlockAll()` force-sets every
entry in `ACHIEVEMENTS` directly, no condition check involved. What's actually
gated separately is the *sound*: four flags control which secret chimes appear
in the audio cue pickers (`secret_chime_unlocked`, `beethoven_unlocked`,
`mythic_unlocked`, `rt_parchment_done`), and the preview button only ever set
two of them. Adventurer's chime and Mythic Fanfare stayed hidden in the
picker no matter how "unlocked" the trophy looked. Both flags now get set
alongside the other two.

Reset was already correct — none of the four flags live in
`PROG_KEEP_ON_RESET`, so a reset wipes them properly. But `beethoven_unlocked`
and `rt_parchment_done` weren't literal keys in `PROG_DEFAULTS`, only
backfilled through `progMigrate()`. Worked by accident. Both are now explicit
defaults, and `rt_parchment_done` picked up the same migrate-backfill line
its three siblings already had.

## v0.133.9 — softer selection, and the editor gets a floor

**The selection was tuned against a background that no longer exists.** A 2px dark
gold frame reads as definition on khaki and as harshness on cream, so removing the
slab in v0.133.8 changed what the frame had to fight without changing the frame. Now
a mid-gold frame instead of dark, a paler wash, a gentler glow, and the bright cap
line dropped entirely — on a pale card that line was the loudest part of the whole
treatment. Still outline and box-shadow only, so selection still cannot reflow the
grid. Name contrast holds at 4.62:1.

**The lower half of the panel had no depth at all.** Header, step grid and the
button were cream on cream separated by hairlines, so everything below the grooves
read as one undifferentiated field. The header and step grid now share a single
recessed slate — the surface you work on — with the button raised above it. Three
depths where there was one, and the inset shadow says "manipulate this" in the same
language the selected card uses.

Done without adding a wrapper to the markup: the slate is drawn on the pattern
header with square bottom corners and no bottom border, and the step grid continues
it with square top corners, so two adjacent elements share one well.

BAND FLASH gains a little saturation to sit clearly above that well as the action
rather than another panel.

All `body.light` scoped; dark mode confirmed unchanged by reading computed values
back in both schemes.

## v0.133.8 — the khaki slab goes, and the rest of the panel gets a light mode

**The slab was mine and it was wrong.** Giving the card grid a filled khaki ground
made sense on paper: pale cards need something to read against. On a device it is a
hard-edged tan block dropped into a cream page, and it looks like a rendering fault
rather than a surface. Gone. The cards separate on their own instead — pushed
slightly whiter than the page, given a warmer border, and lifted with a soft shadow.
Paper on paper, no slab required.

Which exposed that the rest of the panel had never been converted either, and two of
those were unreadable rather than merely dim:

**The selected-groove header.** Its subtitle measured `#c3b17b` on a `#c3b27b` bar —
the same colour as its own background, near enough 1:1. "tap steps to edit" is an
instruction, and nobody could read it. Now 5.08:1, with the title at 6.15.

**The step pips**, which is the worst of the lot. On measured 1.05:1 against off, so
you could see sixteen squares but not which ones were lit: the pattern you are
editing was invisible while you edited it. Three states need three separated steps
of lightness rather than three tints of one, and a first pass at this only reached
2.12 and 1.29 — better than what it replaced and still not enough to read a rhythm
from. Tuned until every neighbouring pair separates: **off to soft 2.19, soft to
accent 3.04, off to accent 6.66.**

**BAND FLASH** read flat because it was a single cream fill with no edge and no
ground. It now carries a warm vertical gradient, a defined border and a lift, with a
pressed state to match — the same weight START already has, which is right, since
these are the two primary actions on the panel.

All `body.light` scoped; dark mode untouched throughout.

## v0.133.7 — the groove picker gets a light mode

It never had one. The cards were running dark-mode values on a cream sheet, which
put filled khaki tiles on pale ground and made the eleven grooves you did not choose
heavier than the one you did. The step preview was worse: khaki dots on a khaki
card, measured at **1.37:1**, which means the one thing that tells son clave from
rumba clave at a glance was effectively invisible and people were picking grooves by
reading names.

The grid now takes the khaki and each card becomes pale paper on it — the same
construction as the metro screen itself, so it borrows an idiom the app already owns
rather than inventing one. Palette sampled off a device screenshot rather than
guessed, after two earlier attempts at light-mode colour went wrong by guessing.

**Selected reads as pressed in**, not lifted out: a warm wash, a gold frame, and an
inset glow along the top edge. Three cues on three different channels — hue, weight
and light — because on a grid of near-identical pale tiles any one alone is too
quiet, which four separate single-cue attempts demonstrated.

Nothing touches layout. The frame is an outline, which paints outside the box, and
the glow is an inset shadow, which never affects flow; there are no padding or
margin changes. Selected and unselected cards measure identically, so the grid
cannot reflow when the choice moves. An earlier cut of this did shift the rows, and
the cause was a single stray `margin-top` — grid rows size to their tallest cell, so
five pixels on one card dragged everything below it down.

Measured after merging: unselected name 13.19:1, origin 4.63:1, pattern 3.62:1;
selected 4.44, 6.08, 3.62. The pattern went from 1.37 to 3.62.

Dark mode is untouched — every rule is `body.light` scoped, confirmed by reading the
computed values back in both schemes.

## v0.133.6 — the third one in the same family

The groove screen has its own BPM readout, separate from the click screen's. Its
number had been given a light-mode value; the "BPM" caption inside it had not, and
was still on `rgba(255,209,102,.28)` — dark-mode amber at 28% alpha, **1.14:1**
against the cream screen, which is fainter than either of the icons fixed in
v0.133.5. Now `#523700`, the same 4.85:1 as its neighbours.

That is three in a row with an identical shape: a child element left behind when its
parent was converted to light mode. The BPM caption inside a converted number, the
icons inside a converted top row. Worth remembering as a place to look rather than a
coincidence — when a light override exists for a container, check what is nested
inside it.

## v0.133.5 — the screen icons had no light mode at all

The BPM label took the v0.133.4 fix; the mute and setlist icons did not, and the
reason is worse than a wrong colour. They had never been given a light-mode value:
both were still carrying the dark-mode `rgba(255,209,102,.4)`, pale amber at 40%
alpha, which resolves to **1.21:1** against the cream screen. That is the lowest
figure anything in the app has measured, and it is why they looked like ghosts.

The previous pass aimed at `.metro-screen-top` and `.screen-bpm-row` and hit
nothing, because the real containers are `#screenTopRow` and
`.groove-screen-bpm-row`. Found by walking up from the icons themselves rather than
by searching the stylesheet for a plausible-looking selector. Both now resolve to
`#523700`, **4.85:1**, verified by reading the computed colour back off all three
icons in the running app.

Stroke and fill are stated explicitly alongside the colour even though both resolve
from `currentColor`, because the paths carry `fill="currentColor"` as an attribute
and an attribute is an easy thing to lose track of later.

## v0.133.4 — the metro screen was hiding text inside its own background

The light-mode contrast audit reports 22 failures. On device, most of them are
fine: the chromatic strip's unlit note names are dim on purpose, the metro subtabs
read clearly, and the bottom-nav labels are flat but legible. Two were real, and
they turned out to share one cause.

The BPM label and the metronome screen's top icons were both a translucent amber
drawn on an amber screen, so the alpha blended them halfway into their own
background: `rgba(122,84,16,.7)` over `rgb(189,171,117)` resolves to roughly 2:1.
Solid `#523700` measures about 4.9:1 on the same ground, keeps the brass identity,
and still reads as secondary to the big BPM number because that number is far
larger.

**An earlier attempt at this made things worse and was reverted**, which is worth
recording. Guessing at what sat behind each element took the failure count from 22
to 39. The reason the guesses were bad is that light mode was being forced by adding
a class after load, while the audit sets a stored preference before it — two
different states, so every measurement disagreed with the last. Reading the same
state the audit reads gave numbers that matched, and the fix landed first time.

The remaining 21 are being left alone rather than silenced. Several are measurement
artifacts of the audit's own method — it samples the 2nd and 90th percentile pixels
of a text node's box, which under-reports contrast badly when a few small glyphs sit
in a wide button. The active metro subtab reporting 1.48:1 while looking perfectly
clear on a real screen is that. The audit is advisory and not one of the seven ship
gates, so a known-noisy signal is better left honest than allowlisted into silence.

## v0.133.3 — the tab fade is gone

Three attempts at a tab crossfade, from 0, then 0.4, then 0.72, each reduced the
flash on the Metro tab without removing it. So this time the fade went instead of
the number.

It was never reproducible here, and that turned out to be the useful fact. Sampled
on every animation frame, the region's opacity rises cleanly from 0.72 with no
bright frame anywhere; scanned across the whole Metro subtree, nothing inside it
animates or transitions during the switch. The most likely explanation is layer
promotion: animating opacity on a 772px subtree hands it to the compositor as its
own layer, and creating that layer can show a frame of unpainted content on some
hardware. The Tuner region is 317px and never showed it, which fits, and it also
explains why a headless desktop browser sees nothing.

Guessing at a fix for a device artifact that cannot be reproduced is how you end up
with four more versions of the same number. The effect was marginal by admission;
the artifact was not. Tab switches return to instant, which is what they were before
any of this and what nobody ever complained about. Folders and modules keep their
shared axis Z, where the motion means something and the regions are smaller.

**Removing it immediately brought back a bug**, which is worth recording. Unwrapping
`setMode` made its internal `exitTool` the outermost navigation call, so tabbing out
of a module fired a Z scale-out: the exact Metro-scales symptom from v0.133.1. It
stays wrapped with a null kind, taking part in the depth guard while animating
nothing.

If tab feedback is wanted later, the nav indicator is the place for it. Animating a
3px bar promotes a 3px layer.

## v0.133.2 — on a dark theme, a crossfade is a dip to black

The remaining blackout on the Metro card had nothing to do with a second animation;
a sweep of every animating element during a tab switch found exactly one, as
intended. It was the fade itself. Fading opacity on a dark theme fades toward a
near-black ground, so what reads as a crossfade on paper is really a dip to black on
screen, and how badly it shows scales with how much lit surface is dipping. The
Metro region is 772px tall against the Tuner's 317, which is why one looked wrong
and the other looked fine at the same setting.

The floor went 0, then 0.4, now 0.72, and the last move is the one that fixes it:
above roughly 0.7 the dip stops registering as darkness and just softens the swap.
Duration trimmed to 130ms to match.

**Full re-check while in here.** Twenty-six navigations driven in a real browser
covering every tab, every Tools folder and tool, every Train hub and exercise, both
directions, plus tabbing out from inside a folder and from inside a module. Each was
checked for exactly one animation, the right kind for the relationship, no animation
on the header, and nothing stale left behind afterwards. Then the whole run again
with the reduced-motion preference set, confirming every path dissolves instead.
Fifty-two navigations, no failures, no console errors.

## v0.133.1 — the Metro scale was a module closing, and the blink was a blackout

Two reports, one shared cause and one of its own.

**Metro appeared to scale where the Tuner did not.** The tab was never the
difference; whether a module was open was. `setMode` calls `exitExercise` on its
way to a new tab, and the train hubs call their own exits, so a single tap ran two
wrapped navigation functions. The inner exit fired a Z scale-out on the region
being left, and the tab's own fade landed on top of it. Leave Metro from a bare hub
and you saw a clean fade; leave it from inside the piano and you saw the scale
first. A depth counter now means only the outermost navigation animates, which is
also just the correct rule: one gesture, one transition.

**Titles blinking out on a tab switch** was the fade starting from fully
transparent. The header sits above the content and never moves, so it gives the eye
a fixed reference against which the content below going to zero reads as a blackout
rather than a crossfade. It now starts at 0.4 and runs 150ms instead of 190ms.

The 8px lift is gone from tab switches too. On a short hub it read as a lift; on a
full-height screen like the Tuner or the Metro, shifting that much content is a
lurch. Folders and modules keep their shared axis Z, which is where a depth cue
actually means something.

## v0.133.0 — the app moves between screens now

Navigation was instant everywhere. The palette crossfaded on a tab switch, over
0.06s, which is fast enough to read as a snap; the content itself teleported,
because panels are toggled with `.hidden`, and `display` cannot be transitioned.
The app had 133 keyframe animations and used none of them to get from one screen
to another.

Two patterns, picked to match what they mean rather than to look busy. **Tabs fade
through**, which Material names for elements with no strong relationship and
illustrates with bottom-navigation destinations; tabs are peers, so nothing there
implies a direction. **Folders and modules use shared axis Z**, which Material
names for parent-child navigation: scale and fade, no travel.

The no-travel part was learned the hard way. An earlier cut grew the new screen
out of the card you tapped, which sounds like Material's container transform and
is not one: that pattern morphs the card's own bounds into the screen's, keeping
the container visible throughout. Scaling a whole new screen up from a point where
a card happened to be is the same idea with the container missing, and it read as
the module scooting in from nowhere. Deleting the translate fixed the feel and
deleted the origin-rect bookkeeping with it.

**Cards cascade on the way down only**, forty milliseconds apart. Never on the way
back, because returning should feel quicker than descending, and never on a tab
switch: Apple's guidance is to avoid decorating interactions that happen often,
and switching tabs is the most repeated gesture in the app.

**Reduced motion dissolves rather than snapping.** The previous convention here was
a 0.01ms duration, which deletes the animation; Apple's position is that removing
animation outright can hurt understandability and that the replacement should be a
fade, and iOS 18's own zoom transition degrades to a standard transition rather
than to nothing. So travel and scale go, a 120ms dissolve stays, and the stagger
is dropped.

**The header does not animate**, by design. It is persistent chrome, and a still
frame is what makes movement inside it legible. It also must never be scaled:
`_fitModuleTagline` measures text width with a Range, and an ancestor transform
would corrupt that measurement.

Implemented as one hook that wraps the fifteen navigation functions after they
run, rather than an edit at every call site. The animation applies to whichever
mode region is showing, since only one panel inside a region is ever visible. It
is enter-only: a true cross-dissolve needs both panels mounted at once and
`display:none` has already removed the outgoing one. Every path was driven in a
real browser, with and without the reduced-motion preference, and checked for
stale animation classes left behind.

## v0.132.16 — the tumbao in octaves

The source line is an acoustic-bass patch, so it is one note per attack, and a bare
single note down at D2 is thin and woolly on a piano. A pianist plays the tumbao in
octaves, so it does now, on both montunos and the Rhodes twin.

The added octave sits ABOVE the source note rather than below. That keeps the
written bass as the floor and puts the definition where it can actually be heard;
doubling downward would have reached D1, which on this instrument is mud. Range is
now D2 to B3, all eighteen events doubled, and still no gaps between a note and the
next attack.

## v0.132.15 — Waldstein and Liebestraum lost their descriptions, and it was my regex

Both rendered as bare cards: title, no composer, no year, no note. The cause was in
v0.132.13, where the montuno metadata was replaced with a DOTALL `.*?\},\n` pattern.
The metadata entries on that line end with `}, ` and a space, not a newline, so the
first `},\n` the pattern could find was two entries further along, and the
replacement quietly took Waldstein and Liebestraum with it. Restored verbatim from
the last upload and pinned, since nothing in the gate set notices a missing
description.

This is the second failure today from a loose pattern on this file, and the
file's own rule covers it: never DOTALL `.*?` here, use bracket matching and assert
what you matched. Both restores were done that way.

**The montuno import itself is clean.** Checked by extracting the note events back
out of the running app and comparing them against the MIDI: 36 events in the 2-3 and
34 in the 3-2, identical to the source in both position and pitch. Whatever is wrong
with the 3-2 is not a transcription error.

**The left-hand durations are also fine, and measurably so.** Each tumbao note
sustains exactly to the next attack, with no gap anywhere: 0 to 1.5, 1.5 to 3, 3 to
5.5, and so on. It is already legato rather than clipped.

## v0.132.14 — accents from the clave track, and twice through

**Accents.** The source is flat at velocity 49 on every note, so dynamics had to be
added; the question was whether to invent them. They are not invented. A note takes
the accent when it lands on a stroke of the file's own clave track, which is data
already in the file rather than a judgement about style, and everything else sits
back at 0.7. In the left hand the beat-4 anticipation takes the weight, since that
is the gesture the tumbao exists for.

It stays a two-level scheme on purpose. The guajeo mostly falls BETWEEN clave
strokes, and how much it does is the actual difference between the two patterns:
4 of 18 notes coincide in the 2-3, 7 of 17 in the 3-2. That tension is the thing
being taught, and heavy accenting would bury it.

**Length.** Both are written out twice, eight bars, which is 16.8 seconds instead of
8.4. Four bars was barely long enough to hear the pattern, let alone play over it,
and repetition is what an ostinato does. Written out rather than looped because the
transport reports a real length and a real end.

**Pedals need nothing.** Both already carry `_riffPiano('pedal',0)` at bar zero and
that is correct and complete: son montuno is played dry, the articulation is the
point, and a wash glues the offbeats onto the downbeats. With the damper model in
place, pedal-up means each note stops at its finger-lift, which is what the written
durations now actually control.

## v0.132.13 — the montuno is a transcription now, and there are two of them

The old Salsa Montuno was an original pattern written to the documented conventions
rather than transcribed from anything, and it did not sound right. It is gone,
replaced by two transcriptions from a public-domain Basic Montunos MIDI, one per
clave direction.

**The clave direction is measured, not asserted.** The source carries a clave track,
and reading it settles which is which: the first pattern strikes 2 and 3 in its
opening bar, then 1, the "and of 2" and 4 in the next, so the two side leads and it
is 2-3. The second reverses. They ship as separate pieces rather than one piece with
a switch, because playing a 2-3 guajeo over 3-2 clave is the crossed-clave mistake
every salsa pianist learns to hear first, and hearing the two back to back is the
lesson.

**Only the piano parts came across.** The file also carries clave and cascara on
percussion channels; those are excluded, because a piano playing its own clave
teaches the wrong thing. The bass tumbao does come across, into the left hand, since
that is what a solo pianist plays: its chord lands on beat 4 of the bar before, which
is where the forward lean lives.

Two things were adjusted rather than copied. Note durations arrived as 0.948 and
0.473 of a beat, a sequencer's gate setting rather than anyone's intent, and are
snapped to the grid the part was obviously written on. Velocity is flat at 49 across
every note in the source, so it is left to the engine default rather than having
accents invented for it; if the guajeo wants accenting later, that is a musical
decision to make with ears.

Tempo stays at the source's 120, which is slower than a dance floor because the file
was written to be followed rather than danced.

The Rhodes twin was cloned from the deleted invention, so it has been rebuilt from
the 2-3 transcription, keeping its tremolo-off and bright-tine voicing.

## v0.132.12 — a song can exist and still not be in the list

Salsa Montuno was missing from the piano picker, and the cause is one the code
made easy. `_riffBuildList` groups piano songs by era, then filters that grouping
against `RIFF_ERAS` to fix the running order, and renders only what survives the
filter. Anything in a group the list has never heard of is dropped without a word.
Montuno was tagged `era:'Afro-Cuban'`, which is not one of the five, so the piece
loaded, held its metadata, sorted correctly, could be launched from a favourite,
and simply never appeared in the bank.

Fixed on both sides. Unknown groups are now appended after the known order instead
of being filtered away, so a typo or a new genre costs a group in an odd position
rather than a song nobody can find. Montuno itself moves to `Other`, an era the
list already renders, keeping its Latin style tag on the Rhodes twin where organ
and Rhodes group by style rather than era.

Checked the rest of the shelf while there, by building each picker for real and
looking for defined songs absent from the rendered HTML: 41 piano, 5 organ and 16
Rhodes, all present, and metadata coverage complete in both directions for all
three. Montuno was the only one hiding.

## v0.132.11 — two strings that never went through the translator

Ran the eleven audit scripts that sit outside the seven-gate set. Nine passed.
The strings audit found nine hardcoded literals, of which seven were false
positives (the literal appears inside the string table itself, or in a comment) and
two were real, both user-facing and both English-only in every language:

The **sustain pedal cap** on the piano and Rhodes wrote `'SUST'` directly.
Now `lbl_sust`, SUST in English and SOST in Italian; both abbreviated because the
cap is narrow, and sostenuto is the word the abbreviation comes from either way.

The **Music Quiz daily badge** wrote `'RESUME'` directly, so an Italian user with a
half-finished daily saw an English word on it. `rr_resume` already existed with its
twin, RIPRENDI, so it reuses that rather than adding a key.

A third hit, the leg tuner's "Show untuned only", is dev-only: it opens from the
console or a long-press on the brand pill and is not on any user path. Left in
English deliberately.

Key parity holds at 1,804 each side with no orphans in either direction.

The contrast audit reports 22 light-mode failures, mostly small uppercase labels in
the tuner and metro at 2:1 against a 4.5:1 requirement. Not touched here: that is a
palette decision across four modules, not a typo, and it wants its own pass.

## v0.132.10 — cleaning up after myself

Adding the Rhodes all-off call to every place the piano voices are cleared was
done with a blanket string replace, and the six-space indented occurrences contain
the four-space string as a substring, so two of them got the line inserted twice at
the wrong indent. Harmless to run and sloppy to read. Removed.

Also went back over two things from this run that were never actually verified
rather than assumed.

**The two-track Rhodes songs were already fine.** They schedule a finger-lift
through `rhodesCardRelease`, which checks the sustain mode and lets the note ring
if the pedal is down. Only the performance path had no note-off, which is the one
that was fixed. The two paths reach the same behaviour by different routes, worth
knowing but not worth merging today.

**The overlay seek lines are correct.** Measured in portrait they came back 12px
wide by 184 tall, which looked like a broken layout until the cause turned up:
`body.ov-portrait-rotate` rotates the whole overlay -90 degrees, and
getBoundingClientRect reports the transformed box. Re-measured at a landscape
viewport where no rotation applies, both read 184 by 12 inside a 200 by 50 screen,
and both render properly: transport and title on top, seek line and times beneath.

## v0.132.9 — the Rhodes had no note-off at all

The pedal moved correctly after v0.132.8 and still changed nothing you could hear,
and the reason turned out to be bigger than the pedal. A Rhodes performance fired
each note and walked away. There was no finger-lift event anywhere in the path, so
every note ran to the end of its sample regardless of what the score said, and the
entire piece sounded as though the pedal had been nailed down in bar one. That is
also why restoring the pedalling in v0.132.6 was inaudible: a damper needs
something to damp, and nothing was ever being held back.

The piano riffs have had a proper damper model for a while. The Rhodes now uses the
same one, which is the right shape for it: a felt pad landing on a tine is the same
mechanism as one landing on a string. A note rings for its written duration, the
finger lifts, and what happens next depends on the pedal. Down, it keeps ringing.
Up, it stops, and everything still sounding only because the pedal was down stops
with it. Release is the sample engine's own recorded release sample rather than a
gain ramp, so damping is click-free without any per-note shaping.

Verified against Clair de Lune with the state sampled twice a second: notes ring on
past their finger-lift while the pedal is down, the count of those collapses to
zero the instant it lifts, and after a stop nothing is left tracked or sounding.

Two smaller things fixed while in there. `riffStop` silenced Rhodes audio through
`stopAllRhodesDrones`, which knows nothing about the new voice map, so the
bookkeeping survived the song; and `rhodesPlayNote` sets its own teardown timer at
the end of a sample, so a note could already be gone by the time its finger-lift
arrived and left a stale entry behind. Both now clear.

## v0.132.8 — nothing was delivering the Rhodes pedal data

Restoring the pedalling in v0.132.6 was necessary and not sufficient. The
performance scheduler built its pedal events with `_riffPiano('pedal', pv)`
hardcoded, whatever instrument was playing, so a Rhodes performance spent four
minutes moving the PIANO's pedal on a tab nobody was looking at while its own sat
still. The arrays were loaded, timed and correct; nothing carried them anywhere.
Pedal events now dispatch on `inst`.

**Which exposed a second thing, worse than the first.** `_riffRhodes('pedal', 0)`
called `stopAllRhodesDrones()`, and that function silences every ringing note. It
is the right behaviour when a person leaves drone mode by hand, and ruinous inside
a performance: Clair de Lune lifts the pedal 163 times, so every one of those would
have chopped the whole texture dead. The hard stop now only fires when leaving
drone mode, which a performance never enters.

Verified by playing Clair de Lune on the Rhodes and sampling: the sustain state
changes four times in the first thirteen seconds, the card pedal toggles its
engaged class with it, the voice count keeps climbing and falling naturally
through pedal lifts instead of collapsing to zero, and the piano's pedal stays out
of it entirely.

**Worth knowing, and not fixed here:** on the sample path the Rhodes pedal is
visual only. `rhodesPlayNote` plays the sample to its natural end regardless of
sustain state; only the synth fallback lengthens its decay. So the pedal now moves
correctly and truthfully reflects the performance, but it will not sound different
while the electric piano samples are loaded.

## v0.132.7 — the organ console had twelve controls and songs could reach five

Before authoring any organ automation, the plumbing needed checking, and it was
worse than the earlier note suggested. `_riffOrgan` routed drawbars for both
manuals, Leslie, percussion on/off, percussion harmonic and the vibrato/chorus
selector. Percussion decay, percussion volume, the VIB UPPER and VIB LOWER
rockers, the VOL rocker and the HOLD latch all had working setters, and
`_riffRestoreState` was already saving and restoring their state around a song,
but nothing connected song data to them. Six controls sat there unreachable.

The volume rocker is the one that matters. On a real console the swell pedal is
how an organist phrases a line, and NORM/SOFT is the two-step version of that;
without it a song can change its registration but not its dynamics.

All six are routed now, HOLD refreshing both its pedals for the same reason the
Rhodes fix did. Verified by driving each control through `_riffOrgan` in the
running app and reading the state back: twelve for twelve, including both
nine-drawbar manuals.

No song data changed. The five organ pieces still set their registration at bar 0
and never move, which is the next job and the one that needs ears.

## v0.132.6 — the Rhodes gets its pedal back, and three songs that suit it

**Pedal.** Seven Rhodes performances shipped with `ped: []` because an earlier pass
decided a Rhodes has its own sustain and stripped it. It does have its own sustain,
and it also has a damper: felts lifting off tines, the same job a piano's lift off
strings. Stripped, the pedal sat frozen on screen through an entire performance and
the sustain stayed flat.

The seven are the same captured performance as their piano twins, note arrays
identical byte for byte at the same tempo and bpm, so the pedalling transferred
exactly rather than being invented: 1,706 events across Clair de Lune, Moonlight,
Barcarolle, Träumerei, To Spring, the E minor Prelude and Liebestraum. Checked in
the running app, every array spans its piece and lifts after the final note.

**Three songs for the Rhodes bank**, taking it from 13 to 16, all converted from the
piano bank and voiced for tines rather than hammers:

- **Salsa Montuno.** Tremolo off, bright. A wobble fights the clave and the guajeo
  needs its edges; the pattern is percussive, not sung. The electric piano is the
  standard salsa comping voice, so this is the one that most belonged here already.
- **St. Louis Blues.** Soft tremolo, warm tine. The Stage sound from soul records.
- **Blues Lick.** Soft tremolo, bright. A twelve-bar lick wants the attack to define
  each note.

All three keep their pianos' pedal-up marking, which was a deliberate call there and
is the same call here: blues and montuno piano is played essentially senza pedale,
and a wash glues the offbeats back onto the downbeats.

Organ control automation is still untouched and remains the biggest audible gap: all
five organ songs set their registration at bar 0 and never change Leslie speed again.

## v0.132.5 — the seek line only ever knew about the piano

Organ and Rhodes had a play/pause and a stop and nothing else: no seek line on the
card, none in the expand overlay. The transport was never instrument-aware.
`_riffScrubEls()` returned a hardcoded pair of piano element ids, so the render
loop and the drag handler had two surfaces to talk to and the other four did not
exist as far as the player was concerned. It now queries `.np-scrub` and finds
whatever the markup actually contains, because a hardcoded list is a list that
forgets the next instrument.

Both instruments gained a seek row under their riff bar, copied from the piano's,
and their overlay screens changed from the single-line compact panel to the same
stacked LCD the piano overlay uses: transport and title on top, seek line
underneath, inside the one panel. Only the playing instrument's line lights up.
Measured in the running app: all three read 346px wide by 14px tall with the
correct totals (organ 2:33, Rhodes 4:07, piano 2:45), fills advancing, no errors.

**The Rhodes sustain pedal had two separate problems and only one of them was a
bug.** `_riffRhodes('pedal')` and `_riffRestoreState('rhodes')` both refreshed
`rhodesPedal` and never `rhodesFullPedal`, so in full screen the pedal sat still
no matter what the song did. The piano has always refreshed both. There is now one
`_rhodesRefreshPedals()` and both call sites use it.

The second is not a bug and has not been touched. All seven Rhodes performance
songs carry `ped: []`, and the file says why: "Pedal stripped (Rhodes has its own
sustain)." Their piano twins carry 103 to 391 pedal events over byte-identical
note arrays at the same tempo and bpm, so the data could be restored exactly, but
that changes how those seven pieces sound and is a decision rather than a repair.

## v0.132.4 — the scale name never fitted its own box

The card did not shrink in the move. Measured both builds side by side and the
name box is 350px wide and 75px tall in each, character for character; the
clipping was already there and Scales moving into Reference just put it in front
of someone.

`.scale-name-big` was declared twice. The real rule sets 36px on a 1.04 line
height, which is the pair that makes the pinned 75px box hold exactly two lines,
and its comment says as much. A second copy sat further down in the leftover
Scale Reference block — `.scale-display`, `.scale-notes`, `.scale-select`, none of
which appear in the markup any more — setting 40px on a line height of 1. Being
later in the file, it won. At 40/1 two lines want 80px, so even a short name was
five pixels over its own box before anything wrapped to three, and
"E NATURAL MINOR · AEOLIAN" wrapped to three and got sliced through the middle,
top and bottom at once, because the text is flex-centred in a fixed height inside
a card that clips its overflow.

The duplicate is gone. That alone is not enough: three lines at 36px still want
112px, and a name like that genuinely needs three. Growing the box is the wrong
trade, since the pin is what stops the tape below jumping every time the scale
changes, so long names shrink to fit instead, down to a 20px floor.

Checked across every scale in the library at three roots, at 320, 360 and 412, in
both languages: 84 names each pass, none clipped, and the smallest any name had to
go was 24px, so the floor is not doing any work yet. The longest strings are
"F♯ NATURAL MINOR · AEOLIAN" in English and "F♯ DOPPIO ARMONICO MAGGIORE" in
Italian.

## v0.132.3 — Scales was never a Train module

It sat alone on the Train hub, full width, under a section label called "Explore"
that existed for nothing else. The case for moving it was already written into the
file: it never calls `progUpdate`, so unlike the thirteen exercises that do it
earns no XP, keeps no stats and reaches no achievement; its own subtitle reads
"look it up · hear it · play along"; and a comment beside the removed IMPROV tab
already refers to it as "the Scales tool". It is now the fourth card in
Tools > Reference, beside Circle of Fifths, Interval Reference and Vocal Range,
which is the company it was always keeping.

Not a merge with Tonal Center, before anyone asks. They share the drone engine
and nothing else: Tonal Center listens to you sing against the drone, Scales just
plays.

**The screen had to physically move.** `#exScales` lived inside `.train-only`,
which CSS hides outside the Train tab, so re-pointing the card without moving the
markup would have opened a blank tool. The id keeps its `ex` prefix on purpose:
about twenty-five CSS rules key off `#exScales` for its drone-mode skin, and a
cosmetic rename across all of them buys nothing anyone can see.

Rewired throughout: out of EXERCISE_NAME_KEYS, EXERCISE_SUB_KEYS, EXERCISE_PANELS,
MIC_EXERCISES and the exercise back-label map; into TOOL_NAME_KEYS, TOOL_SUB_KEYS,
TOOL_FOLDER_MAP and MIC_TOOLS, with `scalesInit` on the enterTool path and
`scaleStop`/`droneStop` on the exitTool path. The in-page back button was still
calling `exitExercise`. Reference went from four tools to five, badge included.

**Two things that would have quietly cost people something.** The favourite pin
key stays `exercise:scales` rather than becoming `tool:scales` — the registry is
keyed by string and `tool:musicquiz` already lives in the Games hub, so the prefix
and the placement never had to agree, and renaming it would have dropped the pin
of anyone who had starred it. And the Everything In Its Right Place achievement
tracks visits by key, which went `e:scales` to `t:scales`; an old `e:scales` still
counts, so nobody has to walk back and re-earn it.

Pro gating is unchanged, since Scales was in neither FREE_TRAIN nor FREE_TOOLS
before or after.

**Two stale strings on the way past.** The Train tour still told people scales was
on its own card. And the Tools hub tagline claimed "six utilities in three groups"
when there are fifteen in five; a tagline that counts things is a tagline that
goes stale, so it describes instead.

## v0.132.2 — the green subtitle was Chordle, three screens ago

A screenshot of RHYTHM TRAINING came in with its subtitle rendered in lime.
Sampling the pixels off it gave #c1e095, which is `--in-tune` (#b6f25b) with a
JPEG's opinion applied; the TUNER tab label in the same shot sampled #a4a5b9,
exactly `--text-dim`, so the palette was fine and the tagline alone was wrong.

`#headerTagline` is a single element shared by every screen, and modules write
inline styles onto it directly. Solve a Chordle and it fades out, swaps to the
progression's name and sets `tag.style.color = 'var(--in-tune)'` as a small
flourish. The only code that ever clears that again is Chordle's and Diadle's own
daily-reset paths. Leave the game any other way and the green leaves with you,
through folder headers and into other modules, since inline styles outrank every
rule in the stylesheet.

`_resetTaglineInline` wipes colour, opacity, transform, transition, font-size and
the length bucket, and both owners of the element call it before they write:
setHeaderModule, setHeaderSection, and the root branch that restores the INTONARE
tagline. Blunt on purpose. The alternative is chasing each new inline style to its
own cleanup site, which is the race that was already lost once here.

Reproduced against the previous build first, which reported rgb(182, 242, 91) on
the Rhythm folder header after a simulated win, then confirmed back to
rgb(163, 165, 184) on this one. Not a regression from the subtitle work; it has
been reachable for as long as Chordle has had the flourish.

## v0.132.1 — the module header was sizing the title as if it owned the row

A screenshot of Notation Cards showed its tagline reading "know the marks on the
pa...". Chasing that turned up something larger sitting underneath it.

Module headers put the title and its italic subtitle on one flex row and called
`_fitHeaderTitle` on the title. That function finds available width by walking up
to the first ancestor WIDER than the element it is fitting, which is right for a
shrink-wrapped inline box and wrong here: when the title overflowed its row, the
walk stepped straight past the row to the header and reported a width the title
never had. Italian RICONOSCIMENTO ACCORDI rendered 283px inside a 264px row and
the fitter called it comfortable, so the TITLE was being clipped, not merely the
subtitle. It also never subtracted the subtitle's width, so every title was sized
as though it had the whole row, and the subtitle got whatever fell off the end.

`_fitModuleTagline` replaces that call and measures against the row itself, which
is known at the call site. Title first, since the title is content: it shrinks to
its 15px floor only if it does not fit alone. The subtitle then takes what is
left, shrinks to its 9px legibility floor, and if it still does not fit it is
removed rather than ellipsed. A half word trailing three dots reads as breakage;
an absent flourish reads as a decision, and the module's full description is on
its card regardless.

Measured, not counted. The device font-scale setting changes rendered width, so
no character-count rule survives contact with a real phone; the fitter asks the
browser at runtime instead.

**Seventeen subtitles were also simply too long for a header.** The file's own
rule, written when Staff Notes and Relative Pitch were fixed, is three or four
words, and a good few had drifted well past it. Trimmed in both languages, which
took the subtitles dropped at 320px from ten to one in English and twelve to five
in Italian. The stragglers all sit behind titles long enough that no subtitle
would fit beside them: INTERVAL REFERENCE in English, and in Italian CERCHIO
DELLE QUINTE, NOTE SUL PENTAGRAMMA, INTONAZIONE RELATIVA and RICONOSCIMENTO
ACCORDI. Those hide cleanly now instead of showing a fragment. Nothing is clipped
at 320, 360, 390 or 412 in either language.

## v0.132.0 — the folder subtitles were answering the same question twice

Every folder carried a subtitle, and no two of them agreed on what a subtitle was
for. Eight named their contents; Reading described itself. Underneath that sat a
second, entirely separate family of subtitle strings, `folder_X_subtitle`, fully
written and fully translated, that nobody had seen in months: it lives in the
in-page `train-header`, and CSS hides that header whenever `body.in-section` is
on, which is always, once you have opened a folder.

The visible string was doing two jobs at once. On the hub card it is the only
preview of what is inside, so naming the tools earns its place. In the folder
header it sat directly above cards reading CIRCLE OF FIFTHS, VOCAL RANGE and
SURVIVAL GUIDE while itself reading "Circle of Fifths · Vocal Range · Survival
Guide". A label that repeats the labels below it is not telling you anything.

Split by surface. The card names the contents; the header describes the folder.
That put the dead `_subtitle` family back on screen, where four of the nine were
already written in the right voice. The other four were lowercase echoes of the
tool names and have been rewritten, Tools > Rhythm never had one at all and now
does, and all nine were measured in the running app at 320, 360, 390, 412 and
768 in both languages: single line everywhere, worst case the Italian Reference
string at 185px in a 264px box.

**Three things that were simply wrong, found on the way through.** The Reference
folder holds four tools and its card claimed three, omitting Interval Reference
from both the subtitle and the badge. The Games card had a hardcoded fallback
predating Road Trip, so it listed four of five whenever the string table was not
consulted. The Reading card's fallback still read "Staff Notes" alone, from
before Notation Cards shipped.

## v0.131.7 — the mega pass, and the deck was in the wrong order

Chord symbols were the one pack that had never been source-checked. All five
qualities confirmed: the triangle is major seventh, the circle diminished, the
slashed circle half-diminished (minor seventh flat five, 1-b3-b5-b7), the plus
augmented, and the letter after a slash is the bass note.

**A contradiction scan across all 138 glyph cards with a SMuFL description:**
zero conflicts. Up against down, above against below, open against closed, sharp
against flat, first against second. Nothing in a definition contradicts what the
spec says the glyph is.

**Then the visual pass found a real one, and it was structural.** The cards are
authored in two blocks — font glyphs, then the drawn ones — so each pack's drawn
cards landed after its glyph cards and split nine confusion groups into two
separate runs. Whole rest and half rest sat 120 cards away from the other rests.

Worse, the contents list emits a group header only the FIRST time it meets a
group, so that second run appeared with no header of its own, filed silently
under whichever group happened to come before it. Anyone opening the index
looking for the whole rest would have found it listed under something else.

Sorted once at load, by pack and then by the order each group first appears. All
nine groups are single runs now, the seven rests are contiguous, the index has 36
headers and no duplicates, and every card still renders at one height with its
distractors intact.

That is the fourth time this session the fix was ordering or registration rather
than the thing itself — panels, back-map, folder list, favourites, and now the
deck's own sequence.

---

## v0.131.6 — cards that describe instead of instruct

Daniele caught staccato reading shaky, and the bass clef saying "the left hand"
of nothing. Both right, and scanning for the same shapes found two more.

**Staccato hedged so hard it never said what to do.** "Detached from the note
that follows; how short depends on context." Every word is defensible — strictly,
the only thing you can infer from a staccato dot is that the note is not legato —
but a card that qualifies before it instructs teaches nobody. It now says to
shorten the note and leave a gap, and keeps the qualification after.

**Staccatissimo had the same problem** and only made sense read directly after
staccato: "Always very short, regardless of context" never mentions shortening.

**Bass clef said "the left hand"** with no instrument attached. The treble card
says "the right hand at the piano"; this one had lost the referent, so it read as
the left hand of whatever you happened to play.

**Tenuto-staccato** said "slightly separated but held", which specifies neither
how long nor how separated.

All four fixed in English and Italian, and every card still measures 348px with
nothing clipped in either language.

The scan also flagged a dozen cards for stating what something is NOT — laissez
vibrer, harmonic, let ring, arpeggio, the tab staff. Those are left alone: each
contrasts against the default behaviour, which is the informative part. A
harmonic really is defined by touching the string instead of pressing it.

---

## v0.131.5 — full pass over the session

Everything built since v0.120.0, re-verified in the final file rather than
trusted from when it was written.

**One real find: "centre" in the C clef definition.** The US spelling sweep at
v0.117.0 corrected 772 instances across the app; I then wrote 181 new cards and
put a British spelling straight back in. It was the only one — every other card
is clean — but it is a good illustration of why a sweep is not a permanent state.

Everything else held:

  Version synced across all three spots. All seven gates pass, read individually.
  Folders each render exactly their own modules, Games included.
  Zero leaks across 24 exercise-to-folder jumps.
  All six modules back out to their own folder, Music Quiz included.
  181 cards in both languages: one card height, no missing ink, no missing text,
  nothing clipped.
  A full English test scores 10/10, 100%, +20 XP, drill hidden on a clean run.
  A quit run changes XP by zero.
  Shuffle stays on the card, is fresh each time, resumes in place, leaves the
  deck alone.
  Index: 181 rows, none broken, exact deck order with shuffle both on and off.
  Casual counters never unlock Flawless Victory; a completed run does.
  Removing a pin removes it and launches nothing.
  No page errors anywhere in the sweep.

One check reported a false failure again — the index order looked wrong because
the row's textContent includes the SVG label text on drawn cards, so "P.M." was
being read as part of the name. Comparing the name element directly: all 181 in
exact order. Third time this session a test has been wrong rather than the code,
which cuts both ways and is worth remembering.

---

## v0.131.4 — Daniele's tour copy

His wording, applied. Better than mine in the place that matters: "bowing,
blowing, or bending" does in three words what my version explained in a clause,
and naming the three kinds of set up front is clearer than leading with the
instrument case.

Two changes to what he sent. The shuffle button is on the CARD, not inside the
index, and the sentence as written put them together — that would send people
looking in the wrong place. And XP is capitalised everywhere else in the app.

Italian written to match rather than translated literally: "arco, fiati o
bending" keeps the same three-beat shape, and bending stays in English because
that is what Italian players say.

All three steps fire, selectors resolve, and each body fits its card without
scrolling.

---

## v0.131.3 — the tour, held to the standard the sweep set

The rewrite an hour ago failed the rules the v0.118.0 tour sweep was written to
enforce. Written in the same session as everything else, and never read back
cold against them.

What was wrong with it:

  "These are the marks that sit around the notes rather than the notes
  themselves" — the not-X-but-Y construction, explicitly banned.

  "when you want the deck to stop being predictable" — quippy.

  "the wrong answers are always things you could plausibly have picked rather
  than something obviously unrelated", and "so reading through the deck can
  never be mistaken for practice" — explaining our own design reasoning to the
  person using it. They do not care why the distractors are chosen that way;
  they care that the wrong answers are hard.

  "the card teaches on the way out" — a flourish.

Five steps for a module whose card, deck size and TEST button are all on screen
and labelled. The sweep collapsed the two hub tours to one step each on exactly
this reasoning: only say the thing that is hidden.

Three steps now, 46 / 24 / 32 words. Picking a set, because the instrument pools
are worth choosing and the reason is not visible. Browsing, because tapping the
counter opening an index is not discoverable and neither is the shuffle button.
And the test, because only it earns XP. The deck itself needed no step; it is on
the screen behind the card.

---

## v0.131.2 — the tour catches up with the module

The Notation Cards tour was written at v0.121.1, when the module was browse-only
with 17 dynamics cards and a button that cycled between two packs. Everything it
described has since changed and it had never been revisited.

It never mentioned TEST at all — the primary action, and the only thing that
earns anything. It described packs as a cycle when the picker is now a grid with
curated instrument pools. And it predated both shuffle and the contents list, so
two features had no explanation anywhere in the app.

Five steps now: the deck, choosing a set, browsing, the test, and what counts.
The pools step leads with the reason they exist rather than the mechanism — a
guitarist gets bar lines and repeats and never bowing — because that is the part
worth knowing. The last step keeps the design decision out loud: only the test
earns XP, browsing earns nothing, and an abandoned run scores nothing at all.

Verified in the app: all five steps fire in order, every selector resolves at the
moment the tour runs, and Italian is twinned throughout.

This is the same failure mode as the tour sweep back in v0.118.0 — tours drift
silently because nothing checks whether what they describe still exists. The tour
audit confirms a tour is PRESENT and its selectors resolve; it cannot know the
words are describing a button that was replaced three builds ago.

---

## v0.131.1 — removal removes, and a perfect score means something

**Removing a pinned module also launched it.** The long-press timer fired the
removal but never cleared its own handle, so lifting the finger ran the tap path
too: it saw a live timer and no movement, closed the sheet and opened the module
it had just deleted. The press now marks itself as spent. Verified: the item is
removed, the sheet stays open, and nothing launches.

**Flawless Victory was unlocking off casual play.** It fires when an exercise
reports correct equal to total over at least ten attempts — but Chord Ear, Pitch
Match, Staff Notes and Relative Pitch all report RUNNING session counters that
tick upward while you are still playing, so ten right in a row during practice
unlocked a legendary. A perfect score now requires `runComplete`: a scored run
with a defined start and end. Verified both ways — twelve of twelve on running
counters does not unlock; a completed ten-question test does.

Notation Cards' test mode sets that flag. The other exercises need their own pass
to decide which of them have a real completed run; until then they no longer
award it by accident. Anyone who already has the achievement keeps it.

**The pool and contents sheets scrolled the page behind them** once their own
content reached the end. Both now contain their scroll.

**The tap lag is NOT the JavaScript, and I have not blind-fixed it.** Measured:
entering a module costs 3ms for Notation Cards, 7ms for Staff Notes, 8ms for
Intervals, 35ms for Road Trip. None of that is perceptible. The delay is paint or
transition, and the fix would mean restructuring `enterExercise`, which is shared
by fifteen modules and is exactly where the panel-list and back-map misses have
happened. Not something to reorganise speculatively on the way into a build.

---

## v0.131.0 — shuffle, and the contents list stops saying undefined

**43 rows in the contents list were broken.** Every row built a font glyph from
the card's codepoint, but a drawn card has no codepoint and no font metrics
either, so those rows rendered "&#xundefined;" at a NaN size. They now render
their SVG. Checked: 181 rows, 0 containing undefined or NaN, 43 carrying a
drawing.

**Shuffle.** Top left of the card, crossed arrows when on and parallel when off.

It is an ORDER over the deck rather than a reordering of it, which is what keeps
the contents list alone: the deck stays in its natural sequence and only the path
the arrows walk changes. Verified against each thing you asked for — toggling
leaves you on the card you were already looking at, the walk is not sequential,
each switch-on builds a fresh order, turning it off resumes the natural order
from wherever you are rather than jumping, the deck order is untouched, and the
contents list reads in deck order regardless.

Changing pool or preset rebuilds the order, so a shuffle never outlives the deck
it was built for.

One note on the verification: my first check of the contents order failed, and
the code was right — the test selector was picking a nested span inside a drawn
card's artwork rather than the name. Compared directly, the two orders are
identical.

---

## v0.130.3 — everything in its right place

Staff Notes was appearing in Games. It is not in Games: the folder registries and
the hub markup are both correct, and every folder renders exactly the modules it
should. What was happening is a leak.

**Opening a folder never closed the module already open.** `exitExercise()` hides
the panels, but changing folder is a second way out of an exercise and nothing
called it — so going Reading, into Staff Notes, then straight to Games left Staff
Notes sitting on top of the Games hub. It looked like a misplaced module and was
a stale one.

All four folder entry points now close any open exercise first. Tested as a
matrix, six exercises against four folders, 24 combinations: no panel survives
the jump.

**Two registry gaps found by the same scan.** Music Quiz was never added to
`GAMES_EXERCISES`, so backing out of it landed on TRAIN rather than GAMES — the
identical miss notationcards had, sitting there since Music Quiz shipped. And
Notation Cards had no entry in the favourites registry, so pinning it would have
produced a tile with no label and no icon. Both fixed, and the favourites entry
follows the `launch:` convention its neighbours use rather than the shape I first
wrote.

That is now four separate hand-maintained lists a new module has to join: the
panel list, the back-map, its folder list, and the favourites registry. Nothing
checks them against each other, and something has been missed in every one.

---

## v0.130.2 — third sweep, on the dimensions never looked at

The first two sweeps kept finding things, so the question was whether a third was
worth it. Repeating a check that already came back clean finds nothing; each
sweep had paid because it looked at a different dimension. So this one went at
the four that had never been examined at all.

**Switching language mid-test broke the answer marking.** The option buttons are
built once per question and carry no i18n key, so they kept their old-language
text while `ncName()` switched under them — and the right answer was found by
comparing button text to the card name, which then matched nothing. The green
highlight landed on no button at all.

Two fixes. The right answer is now identified by card ID rather than by text,
which cannot drift. And `applyLang` calls a relabel hook, so a live question, its
prompt, its reveal and the missed chips all follow the language. Verified in both
directions, including switching while a reveal is on screen: options follow,
the right answer stays marked, and the marked one is the correct one.

**Edge cases hold.** Every pack off falls back to the whole deck rather than an
empty one. A six-card pack builds a six-question test rather than padding to ten
or crashing. A confusion group with only two members still yields three
distractors through the widening fallback.

**The pool choice survives leaving and re-entering** the module.

**And light mode, which this module had never once been seen in.** Glyphs, drawn
cards and the stand-in notes all measure 10.7:1 against the stage; the name
11.9:1 and the definition 10.2:1 against the card. Nothing washes out, no
hardcoded colour leaked in — every surface uses theme variables, which is what
the light-mode remediation established and what the tone-bank rule exists to
protect.

---

## v0.130.1 — second pass, including the Italian

**Italian terminology checked against Italian sources**, not written from memory:
legatura di valore for the tie (same pitch, sums the duration) against legatura
di portamento for the slur (different pitches, articulation) — a pair that is
easy to swap and that the cards get right; punto di valore, which lengthens the
note by half its value; corona, stanghetta, bequadro, pentagramma; and the
semibreve / minima / semiminima / croma / semicroma chain. All confirmed.

**Functional sweep across both languages.** Every one of the 181 cards stepped
through in EN and IT: all render ink, all have a name and a definition, none
empty. Distractors drawn 60 times per language: always exactly three, never the
answer itself, never a duplicate label. A full ten-question run in Italian scores
10 / 10 and awards its XP, which matters because the correct-answer check
compares button text to the card name — if any site had missed the language
accessor, Italian would have scored zero.

**And the sweep found what eyeballing had not.** The reveal box in test mode
clips longer definitions: 8 in English and 14 in Italian. Browse gives the
definition 70px to itself with a group line beneath; the reveal has to fit the
name as well, so it needed that height back. Harp harmonic's English definition
was 144 characters and too long for any box; trimmed without losing the
instruction, since the bracketed fret is already drawn on the card.

Both cards now measure 348px in both modes and both languages, and nothing clips
anywhere.

---

## v0.130.0 — Italian for all 181 cards

Names and definitions, every card, using the `nameIt` convention the instrument,
interval and tuning tables already use. Verified 181 of 181 have both fields and
none is empty.

**The dynamics cards are not translations.** "Piano means quiet" teaches an
English speaker something and an Italian speaker nothing, because the vocabulary
IS Italian. Those seventeen teach the convention instead: that the mark means
volume and not touch, that it is always relative, where it sits on the ladder,
that the gap between mp and mf is the narrowest on the scale. Same card,
different lesson.

**Note values use the Italian names**, which follow the British system rather
than the American: semibreve, minima, semiminima, croma, semicroma — not
"nota intera". Rests likewise, and the clefs are chiave di violino and chiave di
basso.

Guitar keeps the English technique names players actually read — bend, tapping,
slide, palm mute — while using the real Italian where one is in normal use:
barre, capotasto, pizzicato alla Bartok.

**Every place card text is shown now goes through one accessor.** Browse, the
test reveal, the answer buttons, the contents list, the missed chips. Checked
that no site still reads `.name` or `.def` directly, because missing one leaves
the module half-Italian — and the answer buttons in particular would have scored
wrong, since the correct-answer check compares button text to the card name.

**Two layout fixes the Italian forced.** Italian names run longer and wrap to two
lines, so the name slot needed a fixed height like the definition slot already
had; without it the card grew and the layout jumped between languages as well as
between cards. Card heights now measure a single value, 326px, in both modes and
both languages, with no clipped text anywhere.

---

## v0.129.4 — the drawn cards checked against engraving rules

The last unverified set: the 43 drawn cards, which have no SMuFL glyph to check
against. The guitar ones were already drawn to the Hal Leonard legend and the
bend descriptions; this covers the standard-notation ones.

**Rest positions were right, proportions were not.** A whole rest hangs BELOW the
fourth line and a half rest sits ON the third — both correct, and both land in
the third space, one filling its upper half and one its lower. But the height
should be half the distance between staff lines, and mine was 7px against a 9px
space, near enough a full space. Both rects are now half a space tall and about
1.6 spaces wide, which is what makes the hanging and sitting legible rather than
the block simply filling the gap.

Checked and correct as drawn: the multi-bar rest (thick bar centred on the staff,
vertical caps at each end, count above), first and second endings, slur and tie
curves, the ottava and trill and pedal lines, the tuplet bracket, the glissando
line and the courtesy accidental.

That closes the accuracy pass. Every card in the module has now been checked
against something outside my own memory: 140 glyph cards against the SMuFL
codepoint tables and classification, 181 definitions against published sources,
and 43 drawings against Hal Leonard's legend or standard engraving practice.

Still open: Italian for all 181 cards.

---

## v0.129.3 — the strum arrows were backwards

Went back over how much of the module had actually been verified and the honest
number was worse than I had been saying: 65 of 181 definitions source-checked,
116 not.

**All 116 names cross-checked against SMuFL's own glyph descriptions first** —
free, and it proves no card points at the wrong symbol. All 116 match. So the
glyphs are right and only the explanations were in question.

**Then the explanations, and the strum pair was reversed.** A downstroke moves
toward the floor and sounds the LOWEST string first; an upstroke moves toward the
ceiling and sounds the HIGHEST first. Both cards said the opposite. This is the
error most likely to have actually taught someone something false, because a
beginner has no way to catch it and the two cards sit side by side confirming
each other.

**"Indicio" is not the Spanish for index finger.** The right-hand fingering card
glossed p-i-m-a as pulgar, indicio, medio, anular. Indicio means a clue. It is
indice. That has been wrong since the very first draft of the deck and survived
every pass, including one where I read the card aloud in a changelog.

Everything else in accidentals, note values, rests, navigation, pauses, chord
symbols and the staff pack checked out: accidental duration to the end of the
bar, the note-value chain, whole and half rest positions, the barlines, the
octave and pedal marks, the clefs, the chord-symbol qualities and the slash
chord.

Running total on definition errors found by checking rather than assuming: 5 in
dynamics and ornaments, 8 in strings and winds, 3 here. All 16 were in cards
that read perfectly plausibly.

---

## v0.129.2 — strings and winds get their source pass

The 26 cards that had never been checked against anything. Eight were wrong.

**Sul ponticello was the wrong technique entirely.** Sul ponticello is bowing
NEAR the bridge; this glyph is `stringsBowBehindBridge`, which is bowing BEHIND
it, on the short length between bridge and tailpiece — a different technique with
a different sound. SMuFL's own description reads "Bow behind bridge (sul
ponticello)" and I inherited the spec's looseness. Checked: there is no SMuFL
glyph for sul ponticello at all, because it is written as text. The card is now
"Behind the bridge".

**Buzz pizzicato buzzes against the FINGERNAIL**, not the fingerboard. Snapping
against the fingerboard is Bartok pizzicato, which is the card directly beside
it — so the two cards described the same thing and one of them was wrong.

**Fouetté arrives from the air.** Mine said it "starts from the string", which is
the one thing a fouetté is not: the bow is lifted and whipped back down onto the
string, usually up-bow near the tip.

Also corrected: bowing ON the bridge keeps the hair on the strings, hence quiet
and squeaky rather than a scrape; a flip is a turn off the note; scoop is
specifically a lip slur from about a semitone below; plop is a rapid descent onto
the note.

Half harmonic now says what the mark asks for — press only partway, between a
stopped note and a harmonic — rather than describing a tone I could not source.

**Verified correct and left alone:** down and up bow, harmonic, snap pizzicato,
left-hand pizzicato, thumb position (the thumb works like a capo, which is the
movable-nut framing the card already used), doit, the three falls, brass bend,
the three tone-hole cards, multiphonic and mouthpiece pop.

---

## v0.129.1 — an audit against the spec's own data

Daniele asked whether there is a repository or database for this rather than me
fixing one card at a time. There is, and I should have gone looking before the
fourth alignment pass.

**The W3C publishes SMuFL's own classification** — `classes.json`, 85 classes
over the whole font — and it settles by data what I had been assigning by hand:
which glyphs are articulations, which are ornaments, which are rests or clefs or
barlines. Checked against every card: 96 carry a class, and all 96 agree with the
attachment mode I had given them. That is the first accuracy claim on this module
that is not me marking my own homework.

**Bravura's own metadata is the bigger prize and I could not reach it.** SMuFL
fonts ship a metadata file carrying `glyphsWithAnchors` — `stemUpSE` gives the
exact point where a stem meets a notehead, in staff spaces — and
`engravingDefaults` for stem and staff-line thickness. Those are precisely the
numbers I derived by hand from outlines over the last four builds. Steinberg's
copy is not at any path reachable from here; MuseScore's Leland metadata came
down and confirms the schema, but its values describe Leland, not Bravura, so
they cannot be used. Worth another look from a machine with wider network access.

**New gate: `intonare_notation_audit.py`.** Checks that every codepoint resolves
and matches the id claiming it, that attachment agrees with SMuFL, that no two
cards share a codepoint, and that every confusion group has something to confuse
with. Needs `glyphnames.json` and `classes.json` beside it.

**It found a real bug on its first run.** Trill and Arpeggio each existed twice —
once in Ornaments, once added again during the guitar rewrite — so two cards
pointed at one codepoint. In a test that is a question with two correct answers,
the sf/sfz trap I had explicitly designed against. Merged: packs are a list, so
the surviving card simply belongs to both. 181 cards, and Guitar still counts 47
because nothing was lost.

---

## v0.129.0 — bends drawn from the sources, not from memory

Daniele called out that I was chasing fixes rather than checking against real
notation, and he was right: every previous pass redrew these from memory and then
verified geometry I had chosen myself. This one starts from published
descriptions.

**Bend arrows were the wrong shape.** A bend is a CURVED arrow leaving the note
and turning upward, with the interval label at the PEAK of the arrow. Mine were
straight vertical arrows with the label off to one side. All eight redrawn:
half-step, whole-step, slight, bend and release, unison and grace-note bend now
bow out of the fret number and turn up under their label.

The one that was already right turns out to have been right by accident: a
pre-bend genuinely is a straight vertical line, because the string is bent before
it is struck. That is now deliberate rather than lucky.

**Grace-note bend was greying its fret number.** MuseScore's convention is that
grace-note bend fret numbers are CUE SIZED. It is small now, not faded.

**Rake now runs into the note.** Practically you drag across the muted strings
and land on the target, so the Xs sit directly under the fretted note on the
strings you cross, not floating above it on a separate part of the staff.

**And the whammy text is w/bar**, no space, which is the default MuseScore uses.

183 cards, 43 drawn, every card 296px, nothing overflows, no page errors.

---

## v0.128.1 — guitar cards get their tab

Daniele's on-device pass found things a contact sheet at desk size did not.

**Rake was pointing the wrong way.** You rake INTO a target note, and dragging
from low strings to high puts the muted strings BELOW the fretted note. Mine had
the Xs above and the note on the bottom string, which is a rake nobody plays. The
target note is on an upper string now with the muted strings under it.

**Three cards were a bare symbol where the technique is the point.** A lone C
tells a learner nothing about a barré; it now shows one fret stopped across all
six strings with the bracket that marks it, and half barré across three. A T over
a notehead does not show that tapping is a two-hand move; it is tab with the
tapped fret, a slur, and the fretted note it pulls off to. Muffled strings and
the rhythm slash likewise needed strings to sit on.

**Text was overlapping its own dashes.** "let ring" ran into its extension line,
"P.M." into its dashes, "w/ bar" into the -1, and "full" into the pre-bend hold.
All given clearance.

**And one conversion I got wrong.** I put the string number on tab, where the
line the number sits on already tells you the string — the mark only means
anything on a staff. Reverted to a staff note.

183 cards, 43 drawn, every card 296px, nothing overflows.

---

## v0.128.0 — the drawn cards land

**183 cards.** The 38 that SMuFL cannot represent are in: slur, tie, the eight
bends, both slides, hammer-on, pull-off, all four harmonics, the tab conventions,
the ottava and trill and pedal lines, the tuplet bracket, first and second
endings, the multi-bar rest, the courtesy accidental, and the two rests that need
a staff line to be told apart. Drawn to the Hal Leonard legend where one exists.

The card list carries the SVG directly, so a drawn card is data like any other
and the pools pick them up: Guitar goes from 74 to 109, Staff from 19 to 27,
Beginner from 30 to 35.

Swept all 38 rendered through the app's own renderer, as before. Three wrong.

**Tremolo picking was the wrong concept, not a wrong drawing.** It showed two
fret numbers with strokes between them, which is a fingered tremolo — alternating
between two pitches. Tremolo picking is one note picked as fast as possible. It
is a single fret number with strokes on it now.

The **tie** curve dipped to y 50 inside a 48-tall viewBox and was being clipped;
both tie and slur are rebalanced within their box. And **wide vibrato** was
barely deeper than plain vibrato, which is the entire distinction between them.

Verified in the app: all 183 render, every card still 296px, no drawn card
overflows its stage, no page errors.

---

## v0.127.3 — flags push the head sideways

Last build anchored the plain note cards vertically on the notehead and left the
horizontal axis alone. A flag hangs off the right of an eighth or sixteenth note
and widens the bounding box that way, so centring on the box puts the NOTEHEAD
6.8px left of centre on the eighth and 7.1px on the sixteenth — visible against
the quarter note, which has no flag and sits nearly true.

The renderer only ever applied a vertical shift. It takes a horizontal one now,
and the six note glyphs with a stem or flag carry a `dx` computed from the font:
the distance between the glyph's bbox centre and its notehead's centre.

Measured across whole, breve, half, quarter, eighth and sixteenth: every notehead
is 0 from the stage centre, matching a composed card's head exactly.

---

## v0.127.2 — plain notes anchor on the notehead too

**The tremolo fix in the last build was wrong.** I moved the strokes with
`translate(9px, calc(50% + 4px))`, and a percentage translate resolves against
the element being moved — the 30px slot — not against the stem. That pushed them
19px down, straight onto the notehead. The vertical translate is gone entirely:
the slot already bottoms out just above the head, which puts the strokes across
the stem without being told to. Measured: on the stem to within 1px horizontally,
inside the stem's span vertically, 4px clear of the head, on all three cards.

**Plain note cards were anchored differently from composed ones.** A composed
card centres the notehead on the stage; a bare quarter or eighth note centred its
whole glyph, which puts the head below centre by half a stem. Flipping between
them moved the head. The eight note glyphs — half, quarter, eighth, sixteenth,
both grace notes, whole and breve — now carry a notehead-anchored offset computed
from the font rather than their bounding box. Measured: every one sits at 0 from
the stage centre, the same as a composed card's head.

---

## v0.127.1 — looking at all 145

Rendered every card through the module's own renderer into contact sheets and
read them, rather than measuring. Measurement can prove a thing is where I put
it; it cannot say the thing is wrong. Three problems, and the third is a notation
error rather than a layout one.

**Marks were touching the notehead.** The gap measured a consistent 0, which I
had recorded as a pass. Consistent, but wrong: notation leaves roughly half a
staff space, or the mark reads as part of the head. 5px clearance.

**Tremolo strokes sat at the far end of the stem** instead of crossing its
middle, which is where they belong.

**Eight brass articulations had no direction.** A scoop or plop leads INTO a note
and a doit, fall, flip or bend leaves it — they attach to the notehead on the
correct side. All eight were rendering above the head, which made a fall look
like it rises. Scoop and plop are now `before`, the five falls and bend are
`after`.

The rest checked out against convention: articulations on the notehead side with
the stem turned away, accidentals at head height, grace notes visibly smaller
than the note they lean on, the arpeggio spanning its chord, rests and clefs and
barlines all correct.

---

## v0.127.0 — the notehead is the anchor

Four rounds of nudging the composition and the augmentation dot still was not
beside the fat part of the note. Measuring the font explains why: in
`noteQuarterUp` the notehead centre sits at y -16 while the glyph's bounding box
centre is y 367. Anything aligned to that glyph lands 22px above the head. Every
fix so far had been aligning to the wrong point.

The stand-in note is no longer the composite glyph. It is a `noteheadBlack` with
an absolutely-positioned CSS stem, so the element's box IS the notehead and every
alignment is exact by construction rather than by offset. The stem adds no height
and cannot shift anything.

Full sweep over all 71 composed cards, measuring the gap between mark and
notehead rather than centre to centre — centre distance is SUPPOSED to vary with
the mark's height, which is why the earlier checks looked wrong when they were
not:

    before   7px, one value        after   7px, one value
    grace    7px, one value        above   0px, one value
    stem     0px, one value

Row modes align dead on the notehead's centre line (dy 0 across every card).
Tremolo strokes are offset 9px onto the stem, which runs from the right edge of
the head, instead of being centred over the head.

---

## v0.126.4 — the note is the centred thing

The last two fixes stopped the note moving between cards but left it off-centre
on the stage, because the symbol and note were still being balanced as a PAIR:
centring the group puts the note off to one side by half the symbol's width. On a
sharp it leaned right, on the augmentation dot it leaned left.

The composition is a three-track grid now, with the note in the middle track and
the symbol hanging off whichever side it belongs on. Measured across all 71
composed cards: the note's centre is offset from the stage's centre by 0 in every
one of the six modes.

Getting there took one wrong turn worth recording. In column mode I first put the
mark in grid column 1 and the note in column 2, which gives the grid two columns
and centres the note inside ITS column rather than on the stage — the offsets came
back scattered from 3 to 26px. Both live in column 2 now, different rows.

---

## v0.126.3 — and stops wandering vertically

The same bug on the other axis, which the last fix did not touch. A column sized
to its contents moves the note up or down depending on how tall the mark is: a
staccato dot is 4px of ink and a staccatissimo wedge is 14px, so the note sat in
a different place on each.

The mark now gets a fixed 30px slot, bottom-aligned. Bottom rather than centre
because that is also what the notation asks for — an articulation sits a constant
distance from the notehead whatever its own height, rather than being centred in
whatever space it happens to need.

Verified across all six composition modes: each one resolves to exactly one note
position, x and y. Above 197,267 across all 57 cards; grace, beside, stem, before
and after each a single pair of their own. Nothing overflows the stage.

---

## v0.126.2 — the note stops wandering

Three complaints, one cause. The symbol and its stand-in note were laid out as a
plain centred flex row, which centres the PAIR — so the note slid left or right
depending on how wide the symbol happened to be. A flat and a natural are
different widths, so the notehead landed somewhere different on each card, and
flipping between them looked like the note was drifting.

Each side now gets a fixed 54px slot: the symbol moves within its own half and
the note lands on the same pixel every time. Measured across sharp, flat,
natural, double sharp and double flat: identical x and identical baseline.

**The augmentation dot sits beside the notehead now**, not floating at the
vertical centre of the whole glyph. On a stem-up note the head is at the bottom,
so the accidental and dot slots align to the bottom rather than the middle —
which is also where an accidental belongs.

**And every card is the same height.** The definition was a minimum rather than a
fixed height, so a three-line definition (treble clef) made that card taller than
a one-line one and the whole layout jumped as you flipped. All 145 now measure
296px, verified by stepping through the deck and collecting the distinct heights:
one value.

---

## v0.126.1 — scale, after the scale changed

`NC_SCALE` was 1.65, tuned when every glyph was normalised to roughly the same
ink height. Switching to one uniform font-size made the tallest glyph 99px of ink
BEFORE scaling, so a treble clef was rendering at 163px inside a 104px stage. Now
1.15, with the stage at 124px, and every one of the 145 verified to fit.

**My overflow check could not have caught that**, which is the part worth
recording. It measured `.nc-g`, the span that carries `line-height: 0` and
therefore reports zero height no matter how much ink spills out of it. It
returned "none" on a build where clefs were half again taller than their
container. It now measures the `.nc-gb` wrappers, which carry the real ink
height. Third time this session a check has measured the wrapper instead of the
thing.

Composed cards were oversized for the same reason and now sit correctly: the
stand-in note is 59px against a 6px staccato dot, which is the true ratio.

**The contents list drew every symbol at full card size**, so a treble clef ran
down across five rows. Each row now scales its glyph to fit its slot on BOTH
axes — height alone still clipped the wide dynamics like pppp against the side —
and the slot clips anything left over. Cards carry a width for this.

The counter gave no sign it opened anything. It has a list icon now.

---

## v0.126.0 — one font size, and the notes that were missing

**The sizing approach was wrong from the start.** I was normalising every
glyph's ink height, which meant computing a different font-size per glyph — a 41
to 1 spread across this set, since a treble clef is 1.98em tall and a tenuto line
is 0.05em. Stroke weight scales with font-size, so normalising height necessarily
distorts weight. That is the "some feel thin, some feel stretched" exactly.

SMuFL is designed the other way round: every glyph works at ONE size, 1 em to 4
staff spaces, and ink height is meant to vary. Every card now renders at 50px.
Stroke weight is identical everywhere and relative sizes are the ones the font
was drawn for.

**Which exposed a thing I had never ported.** At true scale a staccato dot is 4px
of ink, and on its own that is not a card, it is a speck. The stand-in note
composition existed in the review sheet and never made it into the app — the
`mode` field was sitting in the card data doing nothing. All six modes are in
now: 57 cards above a stem-down note so the mark is on the notehead side, 5
accidentals before a notehead, the augmentation dot after one, 3 tremolos on the
stem, 2 grace notes leaning on a full note, 3 arpeggios beside a chord. 74 cards
stand alone and should.

A bug caught while porting: dimming the stand-in with `:not(:first-child)` would
have dimmed the augmentation dot instead, because in `after` mode the note comes
first. The note pieces carry their own class now.

**Curated pools are pruned rather than blanket.** Pulling in a whole pack drags
along cards the player never meets: Guitar was including the C clef, the
percussion clef and all three piano pedal marks. Pools take a `drop` list, by
card name or confusion group, and a card in the pool's own instrument pack is
never dropped. Guitar is 74 cards and no longer contains a sustain pedal.

**Presets show their state.** They highlight when the selection matches them, and
Everything now switches every pack on rather than clearing the grid, so the
selection always shows what it includes. Hand-toggling any pack drops back to
Custom.

**And a contents sheet.** Flipping one card at a time through 145 to reach the
one you want was the wrong interaction for a deck this size. The counter is now a
button: grouped list, each row showing the symbol and its name, tap to jump.

---

## v0.125.0 — all thirteen packs

**145 cards, up from 17.** Generated straight from SYMBOL_DECK.md, so the deck
document is the source and the app is the build product rather than a second copy
to keep in sync. Dynamics 17, Guitar 21, Staff 19, Winds & brass 15, Ornaments
12, Strings 11, Articulation 10, Chord symbols 9, Pauses 7, Note values 7,
Navigation 7, Accidentals 5, Rests 5.

Every glyph verified to render real ink: stepped through all 145 with the font
loaded and checked none came back empty. The Bravura subset already covered them,
so no font work was needed.

The curated pools have something to curate now. Guitar draws 74 cards, Woodwind
73, Strings 69 — each their own pack plus the general notation that instrument
actually meets on a page.

**38 drawn cards are deferred.** Slur, tie, the bend family, the tab conventions
and the rest have no SMuFL codepoint and exist only as SVGs in the review sheet;
porting those is its own pass.

**Two layout fixes.** The test card measured 274px against browse's 266 because
the reveal slot and the prompt slot did not match the definition and name they
replace; both are pinned now and measure identical. And the counter read "1 /
100" — the score was butted straight onto the question count with nothing between
them. It now reads "1 / 10 · 0 right".

---

## v0.124.0 — one bar, and the name where it belongs

**The bar was the thing that moved.** Browse and test had separate bars of
different heights, so starting a test shifted everything below them. There is now
one bar that never moves and only swaps its contents: pool chip and TEST on the
left and right in browse, progress and QUIT in test. Measured: bar height delta
0, card top delta 0.

**Rhythm Cards looks better and I finally rendered it side by side instead of
guessing.** Three concrete differences, all now matched:

The name sits ABOVE the figure. Burying it underneath made the card read as an
image with a caption rather than a card about a thing. TEST is a solid filled
accent button, not another outline chip in a row of outline chips — it is the
primary action and now looks like one. And the pool chip is small and
left-aligned rather than a full-width block, so the bar has a shape instead of
being two equal slabs.

Navigation is circular prev/next flanking the counter, same as Rhythm Cards,
rather than three equal full-width blocks.

The test card gains a WHAT IS THIS? prompt in the same slot the name occupies in
browse, so the card body does not reflow between modes either.

---

## v0.123.1 — the glyph was eating the taps

**QUIT did nothing, and the reason is worth writing down.** The glyph span
carries `line-height: 0` so its box collapses to zero height while the ink spills
far outside it. At the sizes this module uses, that invisible zero-height span
was lying on top of the progress row and swallowing every tap aimed at QUIT.
`elementFromPoint` on the button's own centre returned `nc-g`. It now has
`pointer-events: none` — it is decoration, nothing about it should be a hit
target — and the stage clips its overflow. Verified with a real tap rather than
a scripted click, which is what hid this the first time.

**A third hand-maintained registry.** `READING_EXERCISES` decides which hub the
back button returns to, and an unregistered exercise falls through to TRAIN. That
is now three lists a new module must join — panels, back-map, and this — none of
which any audit knows about, and I have missed a different one in each of the
last three builds.

**The pool picker is a grid now**, matching how Rhythm Cards does categories:
packs toggle on and off, and presets overwrite the selection rather than sitting
beside it as a parallel list. That is what stops a pack appearing under two
names. The label reads Everything with nothing filtered, the pack's own name for
one, the preset's name when the selection matches it exactly, and Custom
otherwise.

Two duplication bugs came out of that. Single-pack presets repeated the grid
directly beneath them, so Dynamics is a pack tile only. And Beginner is a
curation rather than a subject, so it is a preset only. Separately, a preset
whose other packs do not exist yet collapsed to the same selection as a single
pack — with only dynamics live, turning dynamics on reported itself as "Guitar".
Only live presets are matched now.

**The card no longer jumps** between browse and test; both are pinned to the same
minimum height, measured identical at 266px.

---

## v0.123.0 — pools, an exit, and a result worth reading

**The leak was mine and my last fix was wrong.** `exitExercise()` hides
everything in `EXERCISE_PANELS`, a hand-maintained list, and I wired the module
into `enterExercise` without ever registering it there. So it was shown on the
way in and never hidden on the way out, by any route. What I patched in v0.122.1
was `exitReading()` — one exit path out of several — which fixed the symptom on
the route I happened to test and left every other one leaking. The panel is now
in the list and the patch is reverted.

**Pool selection replaces the cycling button.** Three kinds, and the curated ones
are the reason to bother: a guitarist needs bar lines and repeats as much as
bends and gets nothing from bowing, so Guitar pulls in dynamics, articulation,
staff and navigation alongside the guitar pack. Woodwind and Strings do the same
with ornaments. Presets are Beginner and Everything; By subject is the raw packs
for drilling one thing.

Curated pools carry a `req` — the pack that makes them worth existing. Without it
all three instrument pools would show the same count while claiming to be
different things, since today only dynamics has cards. They stay hidden until
their own pack lands. Verified by injecting a guitar card: Guitar appears
immediately at 18, correctly pulling dynamics in with it.

**There was no way out of a test but to finish it**, which is a trap rather than
a design. QUIT sits in the progress row. An abandoned run scores nothing and
awards nothing, because it is not a result.

**The finish screen was a number in a box.** Now a ring that fills to the score,
the percentage, the XP earned, and — the part that matters — the names of what
you missed. "8 to work on" tells you nothing; eight names tell you whether you
are confusing a whole family or just guessed badly once.

---

## v0.122.1 — chimes, a still layout, and the folder bug

**Answer cues were never wired.** Both branches called `hapticLight()`, a
placeholder, so a wrong answer felt exactly like a right one and neither made a
sound. Now `hapticCorrect()` + `playCueCorrect()` and `hapticWrong()` +
`playCueWrong()`, which respect the cue choices in Settings like every other
exercise.

**The layout shifted on answer.** The reveal appeared out of nothing and pushed
the option grid down the screen at the exact moment your finger was on it. The
reveal now reserves its height and fades in; measured, the option row's top is
identical before and after answering.

**The classic folder bug.** `exitReading()` swapped the hubs and never hid the
open exercise, so backing out left the module sitting behind the hub. It now
hides both Reading modules first. Worth noting this is a shape the app has hit
before, and nothing checks for it: no audit knows that leaving a folder should
close what was open inside it.

Reading's folder badge still read "1 exercise". Now 2, both languages.

**Visual polish.** The symbol floated in a large empty panel; Rhythm Cards works
because the figure sits ON something. The glyph now has its own inset stage with
a hairline and a subtle inner highlight, the card tightened around it, the
progress counters became pills, and the options got a real press state. Same
type scale as Rhythm Cards so the two decks read as one family.

---

## v0.122.0 — Notation Cards test mode

Ten questions, four options, reveal on answer, drill your misses. Notation Cards
is an exercise now rather than a reference.

**The distractors are the whole design.** They come from the card's confusion
GROUP intersected with the active PACK, which is why `grp` has been a field on
every card since the data was written. Four random wrong answers would make every
question free, because nobody confuses a segno with a fortissimo; the drill only
teaches anything when the wrong answers are things you could plausibly have
picked. Loudness cards draw from the loudness ladder, sudden accents from each
other. Verified over 40 draws: always exactly four options, and the only
off-group cases are crescendo and diminuendo, whose group has just two members,
so the widening fallback fires as designed.

**XP is test-only, by decision.** Two per correct answer, awarded once at the
end. Verified that twenty browse flips move XP by zero, so the deck cannot be
farmed by flipping cards. A drill run pays the same per answer as a clean one,
because replaying your worst cards should not be worth less than a lucky first
pass.

The definition lands on the ANSWER, not the question — that is the teaching
moment, and putting it on the card would give the answer away. Right answers
advance after 900ms, wrong ones hold for 2100ms so the reveal is actually read.

Entering the module always lands on browse, so a half-finished test cannot be
walked back into from the hub.

Verified end to end: a ten-question run scores, awards XP, offers the drill and
hides it on a clean sweep; a deliberately perfect run reads 10 / 10, "Every one."
and no drill button. No page errors.

---

## v0.121.2 — sizing, icon, and the copy Reading had outgrown

Glyphs were scaled 2.2x, a number carried over from the standalone review sheet
where cards sit in a narrow list. On a full-width card it overshoots. Now 1.65
and behind a single `NC_SCALE` constant, so it can be nudged on device without
hunting through the render function. Card height 293px to 259px.

The module icon was a bordered rectangle with a plus in it, indistinguishable
from any other card-shaped icon in the app. It is now a two-card deck with a
fermata on the face: reads as notation at 24px and does not collide with Staff
Notes' stave-and-note beside it.

**And two strings that had quietly gone stale.** Reading's subtitle read "Staff
Notes · treble & bass" and the hub hint described only Staff Notes, both written
when Reading had exactly one module in it. The subtitle is now "notes on the
stave · marks on the page" and the hint covers both, in both languages. Neither
was flagged by any audit, because nothing checks whether a folder's description
still matches its contents; it only showed up in a screenshot.

---

## v0.121.1 — Notation Cards tour

Three steps, closing the gap the tour audit flagged the moment the module
landed: an exercise with no tour at all, which also breaks the welcome tour's
promise that picking a module gets you one.

The deck itself, the packs, and browsing. The third step carries the design
decision out loud — reading cards costs nothing and earns nothing, the scoring
lives in the test — so nobody spends an evening flipping cards expecting XP.

Tour audit back to 0 missing and 0 broken. All three selectors verified present
at the moment the tour fires, and the tour confirmed auto-firing on first entry
rather than only on a title-hold.

---

## v0.121.0 — Notation Cards, first slice

Reading's second module. Browse only, dynamics only: 17 cards, every one read
line by line before a keystroke of this went in.

**Bravura is now embedded.** A 149-glyph subset of Steinberg's SMuFL font
(SIL OFL 1.1), 19KB, base64 inlined as an @font-face. The app previously named
Bravura in a few font-family rules with no font behind it; notation was drawn
from hand-extracted SVG path constants. Reserved Font Name, so the subset keeps
the name and Steinberg needs a line in Credits & Thanks before this ships
publicly. The same subset covers all 183 cards in the full deck, so no further
font work is needed as packs land.

**Each card carries its own font-size and baseline shift**, computed from the
glyph's real bounding box. This is the part that is not obvious: Bravura em-boxes
vary enormously, a treble clef being four staff spaces tall and a staccato dot a
speck, so one font-size makes clefs overflow and dots vanish. Displayed ink is
clamped by a power law instead. Flat normalisation is equally wrong: it makes a
clef and a dot the same height. The glyph also needs a fixed-height wrapper or
its translateY leaks into the layout.

Packs are a LIST on each card rather than a category, so Beginner is a curation
of 8 of these 17 and nothing is written twice. The pack button cycles for now; a
picker comes with the second pack.

**Two bugs found in testing, both in the wiring rather than the module.** With no
entry in `EXERCISE_NAME_KEYS` the header fell back to `k.toUpperCase()` and read
NOTATIONCARDS. And the pack label was set by textContent alone, so switching
language mid-session left it in English; it now carries the i18n key on the
element and `applyLang` picks it up like everything else.

Not in yet: test mode, XP (test only, by decision), the distractor logic, the
drawn cards, the other 166 cards, and Italian for any card text. Module chrome is
EN/IT twinned; card definitions are English until the twins are written.

**A sentinel pin drifted and I shipped anyway before catching it.** The pin
asserted that `staffread` and `relpitch` were ADJACENT lines in
EXERCISE_SUB_KEYS; inserting `notationcards` between them broke the literal
string while leaving the guarded behaviour completely intact. Adjacency was
never the fix being protected — having a tagline entry each was — so the pin has
been split into two that assert exactly that, and the count moves 190 to 191.
The sentinel is green. The process failure is the point worth recording: the
gate said do not ship and the build shipped in the same command, because the
copy step was chained onto the gate with && rather than gated on reading it.

---

## v0.120.1 — Rhythm Cards

The rhythm deck was called FLASH CARDS, which names its format rather than its
contents. A notation symbol deck is coming to the Reading folder on the same
chassis, and two cards both labelled FLASH CARDS would have been
indistinguishable in the two places the app shows a module name with no folder
around it: the launcher's pinned row and the header star sheet. Both are now
named for their subject. Rhythm Cards in Tools, Notation Cards in Reading when
it lands.

Nine live strings, not one. The i18n value in both languages, the hardcoded DOM
default beside it, the folder subtitle in both languages and its DOM default, the
tool's own help text (which already called it "RHYTHM FLASH CARDS", so the card
label was the odd one out), the tools-hub hint in both languages, the launcher
tour's Italian body, the module tour's step title, and the favourites registry
entry. That last one supplies the label for the pinned row, which is exactly
where the collision would have been invisible.

Italian is Carte Ritmiche throughout. Only the section banners and code comments
still say FLASH CARDS, and those are internal.

---

## v0.120.0 — Coming Soon goes away

The Train hub's Coming Soon section and its two cards, MELODY DICTATION and
SCORE READER, are removed. Neither is cancelled and neither has been superseded;
a first public release that advertises two unbuilt exercises just reads badly.

Worth recording accurately, because the reason given was not quite the reason:
Relative Pitch was NOT one of the cards still sitting there. It and Chord
Progressions were pulled back in July as genuinely obsolete, since the shipped
Relative Pitch module and Chordle cover them. What remained were the two that are
still real gaps.

The i18n strings, the `wip_toast` and the `.practice-card-btn.wip` / `.wip-badge`
CSS all stay. Restoring a card is markup only, and the strings are already
twinned EN/IT.

Train now reads: four folders (Ear Training, Rhythm Training, Games, Reading),
then Explore with Scales. Nothing else on the hub referenced the removed cards;
the practice tour dropped to one step in v0.118.0 and never pointed at them.

The build path is unchanged and still one path with something shippable at each
rung: staff renderer, then staff note ID (shipped as Staff Notes), then melody
dictation, then score reader. Dictation needs the renderer plus sequence
playback; score reader needs both of those plus the mic scoring Road Trip already
proves works. Score Reader is still the differentiator nobody else has, in that
none of musictheory.net, tonedear, tonesavvy or teoria listens while you read.

---

## v0.119.2 — copy stops being a secret

The two support rows carried a chevron, which promises a sub-screen. Contact
opens a mail composer and Share opens the system sheet, so neither earns one, and
the rows read as inert. They now carry a COPY chip instead.

That does more than relabel. Copying was the silent fallback from v0.119.1, the
thing that happened only when the mail client or share sheet failed, and a device
with no mail app configured fails with no error at all. Promoting it to a visible
control means the reliable route is the one you can see. Text rather than a glyph
because the app's vocabulary is mono and letterspaced, and the slot one section
up already holds "38 MS".

The parent Support row keeps its chevron. Disclosure is the one thing a chevron
honestly means, and that one already rotates to show state.

Feedback moved from the sub-line to the chip. The sub-line carries the row's
description, and swapping it made the row flicker between two meanings; the chip
just reads "Copied" in --in-tune for 1.6s. Share text is now built by one
function so the chip and the row cannot drift apart.

**Two faults in my first pass at this.** The chip came out 26px tall, which is
not a touch target; it is now 40px, which fits inside the existing ~66px two-line
row without changing the row's height. And my test for whether tapping the chip
also fired the row used a capture-phase listener, which runs *before* the target
handler can call stopPropagation, so it reported a leak that was not there and
would equally have missed a real one. Re-tested by wrapping the row's actual
function: it does not fire.

---

## v0.119.1 — both support rows were no-ops

Shipped two buttons that did nothing. Both my fault, and both fail silently,
which is why the gates and the headless check waved them through: the functions
ran, threw nothing, and produced no effect.

**Share.** Every tier of `intonareNativeShare` ends at `copyFn`, and I passed
`null`. With the Capacitor Share plugin present that does not matter, but opening
`Intonare.html` directly rather than through the installed app means no plugins
at all, and `file://` is not a secure context so `navigator.share` is undefined
too. Tier 1 skipped, tier 2 skipped, tier 3 called a null. A guaranteed no-op in
exactly the way the file gets tested. It now passes a real clipboard ladder
(Capacitor Clipboard, async API, execCommand textarea) and confirms on the row.

**Contact.** `window.location.href = 'mailto:'` is not reliable inside a WebView:
a non-http scheme is resolved in `shouldOverrideUrlLoading`, and a scripted
navigation does not always reach it, so the tap is swallowed with no error and no
mail app. Now built as a real anchor and clicked, which goes through the normal
link path that Capacitor and Android both handle, and the element is removed on
the next tick. A device with no mail client still fails silently and cannot be
detected, so after 900ms — unless `document.hidden` says the mail app took over —
the address is copied to the clipboard and shown on the row.

Feedback goes on the row rather than swapping button text the way the daily
puzzles do, because these rows carry a two-line label and swapping the text would
eat the description. The chevron becomes a tick and the sub-line carries the
message for 1.8s.

**A race in the first version of that fix:** the address line and the "Link
copied" confirmation both wrote `.sm-link-sub`, so which one you saw depended on
whether the clipboard promise had resolved. `supportCopy` now takes the message
as an argument and there is one writer.

Verified with clipboard permissions granted: share copies the full text and
restores the description after the timeout, contact copies the address and leaves
it on the row, no stray mailto anchors left in the DOM, no page errors.

---

## v0.119.0 — settings stops being a pile

The tail of Settings had grown to five identical full-width boxes, and adding a
sixth for the support sheet was what made it obvious. The problem was never the
count; it was that the boxes were the same weight while doing different kinds of
thing. Re-run Welcome Tour and Calibration act on the app. Privacy, Credits and
now Support only open something else. Identical slabs for both meant nothing
grouped and nothing receded.

Actions stay buttons. Openers became one bordered group with hairline dividers
and a right chevron, under a new ABOUT heading. Six boxes down to three, and the
new row cost no visual weight at all because it joined a group instead of
extending a stack. The chevron reuses the slot where Calibration puts its "38 ms",
which was already the best-reading row down there.

**The support sheet.** Two rows for now. Get in touch opens a mail composer to
intonare.dev@gmail.com with version, platform, language and viewport prefilled in
the body, so a bug report arrives with a build number instead of "it doesn't
work"; platform comes from `Capacitor.getPlatform()` with a web fallback, and a
missing mail client falls back to showing the address rather than failing on a
tap. Share reuses `intonareNativeShare`, the same helper the daily puzzles use.

No Rate row yet: it needs a listing that is not live, and a button pointing at a
dead URL is worse than no button. No donation row either. Google's position on
developer tip jars is genuinely unclear (their documented policy covers charity
donations, and the Play community threads asking about BuyMeACoffee have no
public resolution), but the deciding factor is that the Pro unlock already runs
through store billing, and an external payment link beside an existing IAP is
exactly what anti-steering rules are written to catch. Not worth the risk on the
build that goes in for its first production review.

Also checked and worth writing down, because it is the opposite of what the
tester report suggested: the "are you enjoying this app?" pre-prompt is
prohibited. Google's Developer Program Policies name it directly, and Apple
treats routing happy users to the store and unhappy ones to a form as review
manipulation. The sanctioned version of that instinct is Apple's own advice to
keep support contact easy to find, which is what this build adds.

**One flaw the first render caught.** The support panel was appended after the
group, so tapping row one opened a panel below row three. It reads as a different
control opening. The rows are now nested directly beneath their own trigger with
a 28px inset and a `--surface` fill, and the trigger's chevron rotates to show
state.

Strings are EN/IT twinned and verified at two definitions each. Gates: syntax
clean, sentinel at 97 + 190, backup audit at 48 keys, no page errors, both themes
rendered at 412x915.

Still sitting in the file for launch: `smResetProBtn` carries a comment reading
"Strip this button + resetProTesting() before production launch." It is hidden
unless Pro is active, so it is invisible today, but it ships.

---

## v0.118.0 — the tours stop lying

A systematic pass over all 34 tours against what their modules actually contain
now. Tours were written when each module shipped and several never kept up.

**The hub tours were the worst, and the fix was deletion.** TOOLS ran five steps
and TRAIN ran six. Between them they listed every folder's contents by name,
which is text the hubs already print on screen in their own card subtitles, and
those subtitles were current while the tours were not. `folder_ear_sub` reads
"Intervals · Chords · Pitch Match · Relative Pitch"; the tour listed three.
`folder_games_sub` reads "Chordle · Diadle · Tónale · Road Trip · Music Quiz";
the tour listed four. `folder_reading_sub` exists at all; the tour had no Reading
folder. TOOLS opened "Thirteen tools in five folders" and then correctly listed
fourteen across the next two steps. TRAIN's mic step named Chord Ear Training,
which is not in MIC_EXERCISES, while omitting Scales and Road Trip, which are.

Both are now one card. They are menus, not modules, and everything a tour could
say about them is already on the screen behind it, printed correctly. What is
left in each card is the one genuinely hidden thing: pinning is a 500ms
press-and-hold on a hub card, with no affordance anywhere. The old TOOLS step
told people to "tap the ★ button in any tool", which does not exist for this
purpose; that star is `svc-save-star` in Charts and it saves diagram views.
Eleven steps became two, and neither can go stale again, because neither counts
anything or names a module.

**Survival Guide was described as the wrong tool.** Its sections are DYNAMICS,
THEORY, GUITAR, BASS, PLUCKED, STRINGS, WINDS, BRASS, FREE REED, PERCUSSION,
PIANO, VOICE, THEREMIN and PEDALS. The tour called it "a quick-reference music
theory guide" and listed intervals, chords, scales and notation, describing one
section of fourteen as though it were the whole thing.

**Progression and Chord Player were rewritten.** Both were label narration: "Set
the key and scale here", "Plays the selected chord". Chord Player's first two
steps were one idea on two cards. Progression's first step talked about key and
scale while spotlighting `#progAddBarBtn`, the wrong control entirely.

**Three features got a clause each** where the feature changes what you are
practicing rather than just doing a thing: rhythm reading's LISTEN FIRST versus
SIGHT READ, the tonal centre's EQUAL TEMP versus JUST, and the polyrhythm
challenge modes. Drumkit's presets and kits were deliberately left out; they are
labelled buttons on screen and exploring answers them.

Smaller: music quiz dropped two hard counts ("over a thousand questions across
nineteen packs"). Three steps stopped opening by restating their own title.
Verb agreement in the metronome RAMP step, a dangling clause in the piano
keyboard step, a missing conjunction in the tone bank list, and a comma in the
Charts quality step that read as a list of three things. The "handy for" tic
appeared five times across the tours and is down to zero; four
superlative-shortcut constructions went with it. And the three newest tours
(relpitch, roadtrip, staffread) were the only ones in the app written without a
single contraction, which made the warmest writing also the stiffest; they now
match everything else.

**Two mistakes worth recording, both mine, both caught before shipping.**

I deleted the metronome tour. The TOOLS rewrite sliced from `"  tools: ["` to
`"  practice: ["`, and `metronome:` sits between them in the object, so the slice
swallowed all six of its steps. Nothing caught it: syntax passed, the sentinel
passed, the tour audit reported 0 missing and 0 broken because it only checks the
tours that exist. It surfaced only because a later `str.replace` on the RAMP step
asserted count==0. Restored from the shipped baseline and verified at 34 tours
with all six steps and every selector resolving. Index-pair slicing across a
sorted object is not safe when the endpoints are not adjacent; a diff of every
tour's step count against the previous build now runs as part of this work.

I also invented two facts in new copy. I wrote that Music Quiz survival ramps
difficulty as the run gets longer; `mqStartSurvival` sets `qCount=50` with no
escalation, and what it actually offers is pack selection. And I wrote that the
polyrhythm challenge gets harder as you go; `prOpenChallenge` builds a picker
with per-card locks (`prHardcoreUnlocked`, `prEndlessUnlocked`), so the truth is
harder modes that unlock. Both were plausible, both were fabricated, and the only
reason they did not ship is that I went back to read the functions. Separately, I
typed British spellings into new copy twice within an hour of sweeping them out
of the file, and named an Italian button "LETTURA A PRIMA VISTA" when the label
reads "LETTURA VISTA".

Gates: syntax clean across 9 blocks, sentinel at 97 fixes + 190 pins, backup
audit at 48 keys, tour audit 0 missing and 0 broken, US sweep reports nothing
left, and every rewritten tour verified rendering at 412x915 with no page errors.
Tour count 34 before and after; step count 137 to 128.

Three audit tools added: `tour_weight.py` (step counts and body lengths),
`tour_tone.py` (hand-holding tells and title echoes) and `tour_drift.py` (each
module's control labels beside its tour's step titles).

---

## v0.117.0 — one dialect

The app was already inconsistent with itself: identifiers American
(`practiceHub`, `mode:'practice'`, every CSS `color:`), visible copy drifted
British. Daniele is US-based, so the copy moves rather than the code.

772 replacements across 58 distinct forms. The big ones are colour (185), centre
(105), grey (88) and centred (66); the long tail runs through theatre, programme,
equaliser, organise, recognise, memorise, prioritise, labelled, modelling,
cancelling, travelling, neighbour, behaviour, catalogue and favourite. Comments
were swept too, not just user-visible strings: leaving them would have meant
building perfect comment detection purely to preserve a second dialect nobody
reads, and the classification is the risky part, not the replacement.

**What was protected, and why.** A blind find-and-replace on this file eats
`AudioContext`, `createAnalyser` and every design note we have. So the identifier
collisions were enumerated first by scanning every `class=`/`id=`/`data-*`
attribute, every CSS selector, every `function`/`const`/`let`/`var` declaration
and every object key in the file. The full set turned out to be small: the
element ids `mst-analyse` and `mp-analyse`, the i18n KEY `metro_tab_analyse`, the
mode string `'analyse'` the metro subnav switches on, `analyser` and
`analyseVibrato`, a local `centre` in the capo solver, and the `underCentre`
property in a layout diagnostic. Those are masked. `GREY` in the woodwind diagram
renderers is handled by case: lower and Title case sweep, ALL CAPS does not.
Verified after writing that all ten survive at their exact original counts.

The i18n key `metro_tab_analyse` keeps its name while its value became ANALYZE,
which is the split that matters: the label on the button is what people read, the
string the handler switches on is not.

**Two bugs in the audit tooling itself, caught before they did damage.** The
first classifier called `'ANALYSE'` and `'Favourites'` identifiers purely for
being one word long inside quotes, which would have left two visible strings
British; case turned out to separate wiring from display labels cleanly.
`programme(d)` was a false positive throughout, since "programmed" is spelled the
same in both dialects, as are "specialist", "analysis" and "emphasis" without a
verb suffix. And the sweep's first pass silently dropped every pattern carrying a
lookahead (practis, analys, emphasis) because it re-matched the captured text
against a pattern whose lookahead context was outside the capture. Named groups
now carry the dispatch. That one is worth remembering: it failed by doing
nothing, and the only tell was four expected words missing from a summary count.

Gates: syntax clean across 9 blocks, sentinel at 97 fixes + 190 pins, backup
audit at 48 keys and 38 progState fields, tour audit 0 missing and 0 broken. The
quiz audit's 129 criticals are pre-existing and unrelated; identical count on the
pre-sweep baseline.

`intonare_us_spelling_audit.py` is in the toolkit now, so a future drift back is
one command away from being visible.

---

## v0.116.1 — dealing the cards back in

Two device bugs from the v0.116.0 re-run path, both mine, both invisible to the
way I tested it.

**The reopened chooser had no cards.** `lnchGo()` marks every cell `lnch-picked`
or `lnch-other` to fling them off screen behind the morph card, and nothing ever
cleared those classes; both rules set opacity 0, and `lnch-other` adds a
translate of around 125% with a rotation. `lnchReopen()` restored the container
and its classes, so the hint line and the pinned row came back correctly around
an empty space where the grid should be. Measured after re-run: all four cells at
opacity 0 with zero-size rects. Now stripped on reopen, and verified back at
opacity 1 in a 2x2 with real rects.

The reason this shipped is worth writing down: I verified the reopen by reading
classes and computed style on `#lnch` itself, which reported display flex,
opacity 1 and `lnch-gone` cleared. Every one of those was true. The state that
was wrong lived one level down on the children, and a container-level check
cannot see it. Same family as the original bug this release fixed, where the tour
overlay was genuinely active and genuinely visible while everything it pointed at
was not.

**The last card told people to hold a title that isn't there.** `showStep()`
appends the replay note to the final step of every tour, and it names the header
title as the replay gesture. That is correct in every tour but this one: the
chooser has no header, because `body.lnch-open` hides it. So the welcome tour
ended by naming a control that was not on screen and describing a gesture that
could not be performed. The launcher tour now points at Settings then Re-run
Welcome Tour instead, in both languages; every other tour keeps the hold-the-title
note unchanged, verified side by side.

---

## v0.116.0 — the tour that pointed at nothing

A paid tester report came back saying the app had no onboarding for new users.
It does. It has had one the whole time. It just fired at a moment when nothing
it described was on screen.

**What was actually happening.** On first launch, `startTour('overview')` ran on
a flat 600ms timer from the bottom of the main script. The splash runs about
three and a half seconds plus a 1.3s dissolve, so the tour opened underneath it;
the card's entrance animation played in full behind an opaque overlay and the
tour was already sitting there mid-flow when the splash finally cleared. What it
cleared to was the chooser, and the overview is anchored to the app proper.
Measured on a 412x915 viewport with the launcher up: `.logo`, `#micBtn` and
`#levelChip` all sit behind the opaque grid, so their spotlights cut a hole onto
a blank frosted rectangle. `.mode-toggle` measured at y=915 and `#mode-settings`
at y=916, which on a 915px viewport is a full bar-height below the fold, so the
caret on steps 2 and 5 pointed off the bottom edge at nothing at all. Six steps,
zero visible targets. The same anchors measure y=862 and y=863 once a module is
open, so the tour was never broken, only homeless.

**The new shape.** Onboarding is two halves handed to each other. A three-step
`launcher` tour runs on the chooser, about the chooser, and ends on a START
button that gives the person the grid instead of dismissing a document. Whichever
module they pick then introduces itself on arrival via `maybeSectionTour()`. The
four section tours (tuner, metronome, tools, practice) existed but had never been
wired to auto-fire; `maybeAutoTour` only ever covered tools and exercises, and it
keys off `currentTool`/`currentExercise`, both null at section level.

Three steps rather than six by choice. Each card already carries its name, a
subtitle and a static miniature of the real module surface, so a step per card
narrates what the person is reading at that moment. Pinning stayed out of the
walkthrough as its own card and became a clause in step 3: nobody knows their
favourite module before they have opened one, and following that instruction
sets `LNCH_PIN`, which makes `lnchShouldShow()` false and removes the chooser
permanently. Teaching it forty seconds in is teaching someone to delete the
screen they are standing on.

**Fixed card without the preview pane.** Module tours get a centred card and a
scaled DOM clone, because their subject is often on another screen. The launcher
tour wants the first and not the second: a near-fullscreen grid spotlit would
darken four thin margins and leave the card nowhere to sit, and a clone would
show a small copy of what is already behind the card. New `dataset.fixed` flag
rather than a fifth branch in the module list; `showStep` and `positionTour` now
read `_isFixedCard` for scroll-skip and positioning while `_isModuleTour` keeps
owning the preview.

**Triggering.** The boot-time timer is gone. `maybeWelcomeTour()` is called from
`lnchInit()` on both shown paths, hung off the launcher actually being visible
rather than off a duration the splash does not honour, and from the no-chooser
branch for pinned or deep-linked launches, where the in-module overview is the
tour that matches what is on screen.

**Re-running.** The Settings button ran `startTour('overview')` in place, which
from inside a module would have reproduced the original fault in mirror image.
`rerunWelcomeTour()` calls the new `lnchReopen()` to bring the chooser back
first, then runs the launcher tour against it, falling back to the overview only
if there is no launcher to restore. The auto-tour opt-in prompt deliberately does
not fire after the welcome tour on a first launch: it would cover the grid at the
exact moment step 3 says to pick a card. It arrives after the first section tour
instead, and a manual re-run still gets it via `_welcomeTourManual`.

Verified on a genuinely empty profile: tour appears after the splash with the
launcher in, three steps, no spotlight, no preview, START on the last card,
`tune_tour_done` and `intonare_tours_seen` both written, METRO picked afterwards
fires the metronome tour at 1/6 with a real spotlight. Returning users get no
welcome tour and still get unseen section tours. No page errors on any path.

Copy is US English throughout, which the rest of the app is not; a spelling
sweep is queued as its own build. 728 British spellings in the file, 461 of them
in comments, the rest split between user-visible strings and identifiers that
should stay exactly where they are.

---

## v0.115.3 — the targeting computer

Better than mine, and it is the closer mapping. Luke switches off the instrument
and hits the shot on feel alone, which is precisely what the climb asks: no
reference tone, no lifelines, twenty-four notes named on nothing but what you
carry in your head. Mallory was about doing a hard thing for its own sake; this
is about doing it without help, which is the actual condition.

The Force Is With You, described by the line that names the feat rather than the
one everyone quotes: "You switched off your targeting computer." Italian: "Hai
spento il computer di mira." The name is longer than most, and short of the
longest already in the set, so nothing about it is unusual for the card.

One thing to weigh rather than a problem: that makes three Star Wars references
across thirty-six achievements, alongside I Have You Now and Maestro. Still a
minority, and the other thirty-three range across Tolkien, Rowling, the Princess
Bride, Gladiator and Back to the Future — but it is now the most-quoted single
source, which is worth knowing before a fourth.

---

## v0.115.2 — Free Solo

The clean-summit achievement was written in the wrong shape. Looking at the
other thirty-five, the pattern is consistent: the NAME is plain and short, and
the DESCRIPTION is a quotation. Impressive. Most impressive. Inconceivable! A
day may come when your strength would fail, but it is not this day. It's
leviOsa, not levioSA. Mine had a plain name and prose where the quote goes,
which is why it read as written rather than found.

It is Free Solo now, and the description is Mallory on Everest: "Because it's
there." A real line, the most famous thing anyone has said about climbing
something for no reason other than that it can be done, and the right register
for an ascent made without touching a single lifeline. Italian: "Perché è lì."

Worth noting the neighbours, since the module borrowed their vocabulary: The
Climb and The Summit already exist as achievements. No collision — all
thirty-six names are still unique — but the words are spoken for.

---

## v0.115.1 — release check, and a backup that was a live view

Full pass over everything since 0.108.29 before this goes out: forty-seven
releases, the Relative Pitch module start to finish, the light-mode rebuild, the
tour work and the leg tuner. Every screen and every exercise opened in both
themes with no overflow and no console errors, the whole climb played end to end
to a clean 200,000 summit, and every gate green.

One real thing turned up, in the backup. backupBuild copied progState shallowly,
so the object it handed back shared every nested value with the live state — the
"backup" was a window onto the present, not a snapshot of the moment. In the
export path it never mattered, because the object is serialised to JSON on the
next line and the file is a true copy. Anywhere else it would matter a lot: hold
a payload, change something, apply it, and you restore what you have now rather
than what you had then. The tell was a round-trip test restoring zeros.

One JSON round trip at build time cuts it loose, and the round trip now behaves:
build with a score, wipe it, apply, and the score comes back in memory and on
disk. Pro entitlement still excluded, leg tuner state still excluded.

Also worth recording from the same pass: the ink audit sits at 41 and the
project light audit at 29, both steady and mostly sub-12px type where heavy ink
is correct. Neither is a gate.

---

## v0.115.0 — your tuning is in, and five songs are signed off

Sixty-six hand-tuned leg values across five songs, written in from the export:
clair_de_lune, prelude_em, moonlight, liebestraum and fuer_elise, all five legs
on each. Every one of those ids is now in RT_TUNED, so the tuner stops badging
them and the list is the record — the panel's own "changed" highlight only
remembers as far back as the last time it opened, which is what RT_TUNED exists
to fix. Sixteen perf songs still untuned.

**And fourteen stale bpm values, which were nothing to do with the tuning.**
Every song's tempo lives in two places: with the song, and again in RT_JOURNEY.
Fourteen of the newer entries had a placeholder 100 sitting in the second copy —
alla_turca reading 100 against a real 120, troika 100 against 92, waldstein_1 100
against 160. Harmless, because every reader prefers the song's own value and only
falls back to this one, and invisible for exactly the same reason. They now
agree. bella_ciao is genuinely 100 and was left alone.

There is a note on the object saying to treat that field as a fallback for
entries with no song data rather than as a second source of truth, since one
number kept in two places is how it drifted for months without anyone noticing.

Verified in the running app: the five report as tuned, their hooks match the
export leg for leg, the bpm copies agree with the songs, and a trip still picks
a song and builds.

---

## v0.114.9 — the rest of the holes in the leg tuner, found before you spend another hour

You asked whether anything else was waiting to eat an evening. Three things were.

**The save ran before the ms recompute.** Perf songs seek by absolute ms, and the
nudge buttons update ms straight after b and s. I put the save between those two
steps, so the stored snapshot had the new position and the old ms. It would have
survived the reload perfectly and then played the wrong spot — visibly correct in
the panel, audibly wrong on the road. Worse than losing the work, because you
would have tuned against it. Save moved after the recompute and pinned there,
with the reason written down.

**The key was invisible to the backup audit.** It was passed as a const, and the
audit finds keys by matching literals in setItem, so a newly persisted key went
unnoticed by the one check whose job is noticing exactly that. Literal now, and
the audit immediately flagged it as unclassified, which is the tool working.

**And it needed classifying rather than just silencing.** It goes in
BACKUP_KEYS_SKIP on purpose: the tuner is a scratchpad whose output belongs in
the source, and carrying it in a backup would drop a half-finished session onto
another device and silently override that device's hooks. Reasoning is in the
file next to the entry. 48 keys classified now, up from 47.

Verified end to end on the real button path rather than by calling the functions
directly: nudge a perf leg, b and s and ms all change together, all three land in
storage, all three come back after a full reload, backup skips the key, and
FORGET removes it.

---

## v0.114.8 — the leg tuner never saved anything, and now it does

Checking rather than guessing: the tuner edited RT_JOURNEY in memory and wrote
nothing anywhere. No localStorage, no progState, no prompt on close. A reload, a
crash, a fresh build — the whole session gone, silently. So yes, an evening of
tuning is gone, and it was never anywhere to lose: it would have gone the same
way on any reload, with or without a new build.

Nothing I changed took it. The export fix touched only the copy path, and the
hook values in the file are exactly what they were. But that is a small comfort
against a tool that quietly discards work, so it does not do that any more.

Every edit is written to localStorage as it is made. The saved set is applied
back over RT_JOURNEY at module load rather than when the panel opens, which
matters: it means a tuned leg actually PLAYS tuned instead of only reading tuned
inside the tuner. Verified across a full page reload — edit a hook, reload,
values still there and in effect.

A FORGET SAVED TUNING button sits beside the others for when a session needs
throwing away, behind a confirm, since it cannot be undone.

The one thing worth saying plainly: this was the second silent-loss bug in the
same panel in one day. The export looked like it worked and copied nothing; the
editor looked like it worked and saved nothing. Both were quiet in exactly the
same way, and both only surfaced because you asked a direct question about
something that should not have needed asking.

---

## v0.114.7 — the leg tuner's EXPORT was copying nothing

Three empty pastes in a row is not three accidents. The export ran
document.execCommand('copy') inside a try/catch that swallowed the failure, on a
textarea marked readonly — which the Android WebView will not select, so there
was nothing on the clipboard to copy in the first place. Every part of that
fails quietly: the button gave no feedback, the catch ate the error, and the
textarea appeared with the right text in it, so from the outside it looked like
it had worked. It had never worked on the device.

navigator.clipboard.writeText now, with execCommand as a fallback that lifts the
readonly attribute for exactly as long as it needs the selection and puts it
straight back. The button reports which one happened — COPIED, or SELECT AND
COPY BELOW — rather than assuming, and a line under it explains what to do if
the WebView blocked the clipboard entirely. The textarea grew to 300px and has
user-select forced on, so selecting it by hand is a real option rather than a
theoretical one.

Verified end to end with clipboard permissions granted: 5,451 characters, 39
songs, and the clipboard contents match the textarea byte for byte.

**Also struck from the open list: the dormant grid deletion.** It has been
sitting there as a pending cleanup for the seven converted piano songs. Checking
the actual entries, all seven carry only duckV, meter, label, tempo, bpm, perf
and tempoMap — no grid arrays at all. The data went out with the perf conversion
rather than needing a separate pass. Nothing to delete, and nothing about tuning
those songs removes anything.

---

## v0.114.6 — one press was firing two gestures

Both, yes. The leg tuner has been on a 600ms long-press of the ROADTRIP title
since it was built, and yesterday I bound the tour replay to the same element at
500ms. One press fired both: the tour opened at 500, the tuner opened on top of
it at 600. Verified before the fix rather than reasoned about.

Nothing in the code looks wrong. Two handlers on one element, each correct on
its own, added eight months apart, and the only way to notice is to know the
older gesture is there and try it.

The tour keeps the title, because it is the user-facing feature and the title is
where every other tour replays from. The tuner moves to the INTONARE brand pill
at 900ms — 84 by 18, so it is reachable on a phone, and not a thing anyone
presses on the way to something else. window.rtTuner() is unchanged. Verified:
the title now opens only the tour, the pill only the tuner, and a short press on
the pill opens neither.

**The audit gained a collision check.** It cannot find every clash — nothing can
enumerate listeners after the fact — but the leg tuner leaves a dataset marker
behind, so it can at least say whether something else has claimed the element a
tour hold is bound to. That is the one clash that exists today, and it is the
shape of the next one.

---

## v0.114.5 — Road Trip's tour could fire once and never again

Good question, and the answer was worse than it looked.

Every tour in the app replays the same way: press and hold the title. The gesture
is bound to #appLogo and #headerTagline so it works on whichever one is showing.
Road Trip draws its own full-screen chrome over the header — and the trap is that
the tagline is still in the DOM, still reports as visible, and still has pointer
events enabled. Nothing about it looks broken from the code. It is simply
covered: elementFromPoint at the middle of the tagline lands on a difficulty
chip. So the Road Trip tour could auto-fire once, on first open, and then be
unreachable forever.

Music Quiz had exactly this problem and already had the fix, because it is a
modal with no header at all and the failure was obvious there. Road Trip's
failure was not obvious, because it has a header — just not one you can touch.
Same fix, same shape: press-and-hold bound to the module's own ROADTRIP title,
with the movement threshold the Android WebView needs so its constant pointermove
jitter does not cancel every hold.

**The audit now checks this,** which it could not before. Coverage and selectors
were never going to catch it: the tour existed, every step resolved, and it
worked perfectly the one time it ran. The new check asks whether the tour can be
reached a second time, and it asks with elementFromPoint rather than by looking
at visibility, because visibility was the thing that lied.

Both full-screen modules now report bound and reachable.

---

## v0.114.4 — the switch went missing inside its own mode, and a tour audit

**Moving the switch into the card head stranded people in the climb.** It
landed on the practice card and on the climb's GAME card, and nowhere else —
the intro and the result screen have no head, so once you were on either of them
there was no way back to practice. That is worse than the row of slabs it
replaced, and it is exactly the failure that only shows up when someone uses the
thing rather than looks at it. Both screens carry it now, and it is pinned.

**The rules went back behind their toggle.** Unfolded they are three paragraphs
sitting between the record and the button, on a screen whose entire shape is
built to end on START. Behind a link they cost one dim line and are one tap away
for anyone who wants them, which was the right answer the first time.

**And a tour audit, because tours rot silently.** Nothing breaks when a module
ships without one, since the prompt simply never fires. Nothing breaks when a
step points at an element that has been renamed, since the tour skips it. Both
failures are invisible from inside the app, which is why they accumulate.

intonare_tour_audit.py checks three things: coverage against the app's own
module roster, every step opened against the live DOM, and a scan for the
writing tells this project keeps having to strip.

It found Road Trip with no tour — the last one — and it caught a broken selector
in the Road Trip tour I had just written, within a minute of writing it: I had
pointed at #rtDiffstrip and the element carries that as a class, not an id. That
is the whole argument for the tool in one example.

The tone scan flags thirteen. Two were the real thing and are rewritten: the
overview's "TUNER tunes any instrument by mic. METRO is a full metronome." and
the piano's "Fully multi-touch, so chords work. Glide across keys." Both are the
stacked-declarative rhythm rather than anything wrong with the content. The
other eleven are colons doing their proper job in front of a list, or a short
sentence that earns its length; the scan cannot tell those apart and is not
meant to. It says where to look.

Coverage is complete for the first time: every exercise in the roster has a
tour, and every step in all thirty-three resolves.

---

## v0.114.3 — the switch moves into the card, and the tour stops sounding like a tagline

**The switch replaces the title it was duplicating.** It sat in a row of its own
above the card, and the card's first line said PRACTICE — which the switch had
just said, one row up. It lives in the head now, where the title was, with the
settings line underneath it. The climb head does the same, folding the band name
and its gap onto one line. The practice card drops from 519px to 488.

**The rules come out from behind the toggle.** With the tour covering the module
itself, what is left is the terms of the bet, and those have no element to point
at until you are already climbing. Three lines, on the intro, where someone
deciding whether to press START can read them without going looking. The
one-wrong-ends-it rule went, because the intro line already says it and saying
it twice on one screen is worse than not saying it at all. The toggle, its
handler, its two labels and its link style are all gone rather than left
dangling.

**And the tour copy was written in the voice you keep catching.** A colon before
a punchline, "not a skill, it is a crutch", short declaratives stacked three
deep — a tour is somebody showing you round, and it should read like someone
talking rather than like a tagline. All six steps rewritten in both languages,
with the sentences let out to their natural length and the aphorisms taken out.
The fork step now explains why it costs you instead of scoring a point off it.

---

## v0.114.2 — the tour gap, and a mode switch that stops shouting

**No, tours have not been kept up, and asking found it.** Thirty tours exist.
Five exercises have none: Road Trip, Pitch Match, Chord Ear, and both modules
shipped this month, Staff Notes and Relative Pitch. The reason it stayed
invisible is that maybeAutoTour keys off the TOURS object, so a module without
an entry simply never prompts — nothing breaks, nothing warns, the module just
quietly has no first-run explanation while every older one does.

Relative Pitch gets four steps: the two modes, hearing a note with nothing to
compare it to, the screen, and why the fork costs you a run. Staff Notes gets
two. Both in English and Italian, both with every selector verified to resolve
against the live DOM rather than assumed. Road Trip, Pitch Match and Chord Ear
are still open and now written down rather than merely absent.

**The mode switch was this module inventing a control the app already has.**
Two full-width slabs, 358px across, the loudest thing on the screen — for a
choice between two things. .app-seg is what everything else uses for a small
either/or: an inline pill sized to its labels, sitting left. 181px now, and it
reads as a switch rather than as navigation.

Two things that fix took. The pill kept filling the row despite align-self,
because the parent is a GRID and align-self is the wrong axis there —
justify-self is what a grid item needs. And the state class changed from .on to
.active, since the shared control has its own convention and the point of using
it is to stop having two.

**On whether the rules should just be the tour:** mostly yes, and they now
overlap. But they are not the same job. A tour points at elements and runs once;
the rules are the terms of a game with stakes, and a rung-eighteen decision is
exactly when someone wants to re-read what a haven is worth. The tour explains
the module, the rules link explains the bet. Worth revisiting once the tour has
been on a device.

---

## v0.114.1 — you were right about the lifelines

**They were refreshing at every band edge,** which meant twelve across a climb
at 0.08 of the multiplier each. Spend every single one and you still settled at
x1.04. That is not a cost, it is paperwork. And a resource that refills cannot
be hoarded, so the one decision the multiplier was supposed to create — burn
this now, or keep the number — never actually came up, because there was always
another one along in six rungs.

Three for the whole climb now, at a quarter of the multiplier each. Spend all
three and you finish on x1.25 against x2.00 clean, so the full set is worth
three quarters of your score. Only the replays refresh at a band edge, which is
what your rewritten rule text already said before the code agreed with it.

Verified: a lifeline spent in the first band is still spent in the second, a
clean summit pays 200,000 and unlocks No Hands, and a summit with all three
spent pays 125,000.

**The eight rewritten strings are in, with Italian twins.** Two small
corrections inside them. The havens sit at rungs 6, 12 and 18, so "every five
steps" became "every sixth step" in both languages. And the lifeline rule still
said twelve, which was true this morning and is not any more — it says three.

The result captions are noticeably warmer than what they replaced, and losing
now says so plainly rather than describing the mechanics of where you landed.

---

## v0.114.0 — No Hands, a lighter ladder, and an editor for the climb's copy

**An achievement for the clean summit.** Twenty-four rungs with the wrong
answers closing in the whole way, not one lifeline taken, so the multiplier is
still on 2.0 at the top and the payout settles at 200,000. There is exactly one
way to earn it. It is called No Hands and it is legendary, which for once is
literal rather than a rarity tier: nothing else in the app asks for two dozen
correct answers in a row with no help available except the ones you are choosing
not to spend.

The condition checks the multiplier as well as the figure. Checking the payout
alone would let a helped run that happened to bank 200,000 some other way slip
through, and the whole point is the absence of help.

**The ladder was the last thing wearing floor-pinned ink.** A haven at 2.5:1
against the card is not gold, it is brown, and the cleared rungs behind it were
the accent at 42% opacity — which on a dark lamp bed is a lit rung and on a pale
one is a smear. Both are fills rather than text: they have to be findable, not
legible. The golds come up to 1.5 and 1.9 against a plain segment, still a clear
step either way, and a cleared rung is now an opaque lifted accent rather than a
wash of one.

**And an editor for the climb's copy.** ClimbCopy_Editor.html: every string the
CHALLENGE mode shows, English beside Italian, forty-five of them, each with the
place it appears and the width it has to live in. The character counts and
ceilings are measured off the app rather than guessed, so a label that will
ellipsise says so before it ships rather than after.

EXPORT prints only the lines that actually changed, was and now, both languages
— which means a rewrite comes back as a patch I can apply verbatim with no risk
of a stray edit riding along unnoticed. Nothing in the file touches the app.

---

## v0.113.9 — the app has more than one word for "a raised surface"

Read the residue rather than the headline, and it says something structural
about light mode that had gone unnoticed for the whole of this work.

**The card-scoped fix assumed there was one kind of card.** There is not. The
tuner's instrument card is .tuner-bpm-card, the interval card is .iv-card-v2,
the tour is .tour-card, the hub buttons are .practice-card-btn, the chooser
faces are .lnch-face — five raised surfaces holding text, none of them .card. So
the hierarchy fix reached the module cards and nothing else, and every one of
those five kept the ground-pinned ink it should not have had. That is why the
tuner and metro screens between them accounted for twenty-six of the forty-two
remaining findings while the module screens had almost none.

Extending the scope to all five overshot immediately, and the other audit caught
it: the practice hub buttons and the interval card carry sub-9px labels that the
lighter secondary drops below AA, and the tuner card's pill labels are 8px. So
the rule is not "is it raised" but "is its secondary text at label size", which
is not something a selector can ask. The scope now holds the surfaces that pass
that test — the module cards, the sheets, the tour and the chooser faces — and
the ones that failed it are deliberately outside, documented as such.

**Two things worth saying plainly about what this means.** The first is that the
residue is dominated by small type: of the elements still over ceiling, thirty
of forty-two are under 12px, where heavy ink is arguably correct and lightening
it is what breaks AA. The second is that four of the remaining findings are in
dark mode and all four are dark ink on a bright accent fill — a primary button —
which is right by design. The tool has no way to know that, so those stay.

Ends at 39 by the ink audit with the other two audits at zero new failures and
none made worse. That number is not going to zero, and it should not: it is a
hunting tool with a deliberately conservative ceiling, not a gate.

---

## v0.113.8 — what the ink audit actually found

Ran it properly and read the whole list rather than the top of it. Eighty-seven
pairings, and grouping them by the colour rather than by the element turned most
of the list into one fault.

**The hierarchy had collapsed.** Measured on a card: text 11.9:1, dim 10.2,
muted 9.6. Three levels that are supposed to be obviously different, sitting
barely two points apart. Nothing was individually wrong, which is why no
contrast audit ever mentioned it — and it is exactly what "muddy" turns out to
mean. Everything on a card weighed the same, so nothing led.

They cannot simply be lightened, because the same two tokens also carry text on
the GROUND where they are already near the AA floor. So they are redeclared
inside .card and inherited from there: the ground keeps its legal values, the
card gets values pinned for a card. Text stays, dim goes to 7.2:1, muted to 5.0.
The steps are visible again and both still clear AA on the surface they are
actually read on.

That one change cleared twenty pairings. Three more went with the tokens the
audit named individually — the ladder's gold and multiplier, the screen's rung
figure, and the tuner's face-swap control, all still using raw floor-pinned
values where a lifted variant already existed for exactly this.

**The tool needed two fixes of its own to be trustworthy.** It was flagging
primary body ink, which is supposed to be high contrast — black on white is 21:1
and nobody calls that a fault — and that noise was burying the real findings. It
reads the theme's own --text off the root and skips it now. The first attempt at
that silently did nothing, because a custom property comes back as the author
wrote it, and here that is a bare hex the parser did not know.

**And one thing the fix broke, which the other audit caught.** A card-scoped
secondary is right for a label at 10-12px and a step too far below that: the 9px
hint and the inactive instrument tabs lost their footing. --ink-tight keeps the
ground-pinned value reachable inside a card for those, and the card scope
deliberately leaves it alone.

Eighty-seven down to forty-two. The remainder is mostly small and several of
them are deliberate.

---

## v0.113.7 — a tool that finds the fault instead of hunting it

You should not have to hunt these down one screenshot at a time, and the reason
you have been is that a contrast audit can only ask one question: is this dark
enough? Every light-mode fault in this app has been the opposite — a colour
pinned dark enough to clear 4.5:1 on the FLOOR, then used on a CARD two steps
lighter, where the same value lands near 10:1 and reads as ink rather than as
colour. A contrast audit passes that every single time, because more contrast is
never a failure by its rules.

**intonare_ink_audit.py** asks the inverse. It walks twelve screens in both
themes and reports every element whose contrast is far HIGHER than its role
needs: over 9:1 for small text, over 7:1 for large text and graphical fills.
Those ceilings are not standards — nothing forbids high contrast — they are the
line past which, in this app, a colour has reliably turned out to be pinned
against the wrong ground. It prints the ink, the ground, the class and the
screen, so a colour can be found rather than searched for.

It found 87 pairings on its first run, and the single largest was systemic:
**the body ink itself.** Pinned at 7:1 against the floor, it lands at 13.8 to
14.6:1 on a card. That is well past AAA, and since almost everything in this app
is read on a card, it is what made light mode feel heavy element by element
rather than in any one place. The trio is pinned at 5.6 / 4.8 / 4.55 on the
floor now — still clearing AA there — and lands at 11.4 / 9.9 / 9.5 on a card.
Ink rather than tar.

**And the answer keys, which is where you noticed it.** Right and wrong are the
two states you look straight at, and both were wearing floor-pinned status ink
on a near-white card: 8.8:1 for a letter that is supposed to read as green,
which is how it ends up looking like moss. Both take the lifted status colours
in light now, along with the big note reading on the screen.

The audit still reports 81 pairings, most of them minor and several of them
deliberate. It is a hunting tool, not a gate; nothing about it blocks a build.

---

## v0.113.6 — the emboss was eating the letterforms

**Three shadows around a glyph, two of them white, is an outline.** That is what
the title treatment had become: a white pass above at 92% and another below at
55%, with the dark one underneath. Around type rather than around a box, the
white bleeds inward at the stroke edges and eats the contrast of the very thing
it is supposed to be lifting — the letters get a halo and lose their weight, and
at header size that reads as softness rather than as depth.

A raised object needs one highlight and one shadow. The white is a single
hairline on the lit side at 45%, and the dark does the lifting. Same modelling,
nothing eroding the stroke.

**And the paper is a nudge cooler.** Same lightness, chroma pulled back a third
and the hue eased off yellow toward neutral: 82 degrees at C .013 becomes the
same lightness at C .009. Still warm enough not to read as overcast, cool enough
to be paper rather than parchment. The top bloom went with it.

No new contrast failures, project audit steady at 26, module audit zero.

---

## v0.113.5 — paper

The chooser ground is paper. Warm off-white, a shade deeper toward the foot,
with a wide bloom across the top.

**Value stops holding the grid together at this lightness,** and that is the
whole consequence of the choice rather than a side effect of it. The ground sits
1.05:1 from a card's lit top edge and 1.16 from its foot, so the cards are held
entirely by their rim, their contact shadow and their own pool. All three were
tuned against a mid-tone ground and had to be stepped up: a firmer rim carrying
more of the module's own colour, a tighter and darker contact shadow so the card
meets the page somewhere definite, and a longer ambient so it still lifts off a
field this light. Sentinel-pinned, both the ground and the rim, because
softening any one of them now dissolves the grid into the page.

The pools read at their strongest here. On a mid grey they were fighting the
ground for the same territory; on paper they are the only colour in the field
outside the cards themselves.

**Two things the change broke and put back.** The pinned chips were white on a
near-white ground at 1.27:1, a chip with no edges — they carry more of their tool
colour and a firmer rim now. And the hint under the grid was pinned against a
mid ground; on paper it landed at 4.17:1, which is the AA floor with no headroom
at 7.5px. It is pinned against the darkest ground it can land on rather than the
lightest, since it sits over the lower pools and not over bare paper.

No new contrast failures, project audit steady at 26, module audit zero.

---

## v0.113.4 — the dark faces were fighting their own glow

**The vignette on the dark cards had to come down.** The face fell to 22% black
at its foot, which was right when the card had nothing behind it: the falloff
was doing the job a shadow does, and dark shadows are nearly invisible on
near-black. With a pool underneath, the same gradient stops reading as depth and
starts reading as a hard vignette — lit at the top, blackened at the bottom —
and the glow makes the swing worse rather than better, because now there is
light immediately outside the darkest part of the card.

Ten percent instead of twenty-two. The fall is still there, the light gets
through, and the 3D work stays exactly as it was: rim, inset highlight, layered
shadow, and now the pool.

**The mock could not be judged, and that was a fair criticism.** A ground shown
in a box the grid fills is a swatch, not a screen. In the app the field runs the
whole viewport with large empty regions above and below the grid, and those
regions are most of what you actually see. The stage is a phone now — 814px
tall against a 499px grid, so roughly forty percent of it is the dead space the
decision actually turns on — with the nav bar in place so the ground is judged
under the chrome that sits on it.

PAPER and LIFTED WARM are the two you picked out; they are next to each other in
the picker for a straight comparison.

---

## v0.113.3 — dark gets the glows, and the ground goes to a vote

**Yes, dark should have them, and it needed them more.** The whole language of
the dark theme is emission — every card has a lit rim, the page carries pools,
the icons glow — and the chooser was the one screen not speaking it. The same
card-attached pool is there now, weaker and tighter: a glow on near-black reads
at much lower alpha and turns to fog with far less spread, so it runs at 34%
against light's 70% and blurs 20px against 22.

**On the ground: you are not crazy, and the reason is structural.** A mid
neutral is being asked to do two incompatible jobs at once. It has to be dark
enough that pale cards read against it and light enough that it does not feel
like weather, and the value that satisfies both is the value that satisfies
neither. Measured, the cards all sit at OKLCH L .90 at the top and .966 at the
foot — they are very light and very close together, so anything in the middle
distance from them reads as a compromise.

That is a taste call with real trade-offs on each side, and it has now cycled
four times on my judgement, so it goes to a file rather than another guess:
ChooserGround_Mock.html, six grounds on the real components and the real glows,
with the measured value gap under each. WARM MID is what ships today at 1.29:1
to a card top. LIFTED WARM is the smallest possible answer if the complaint is
weight rather than hue. PAPER removes the gap almost entirely and lets border
and shadow hold the cards. DEEP and COOL DEEP go the other way at 2.65 and 2.74,
which is where the glows have something to fall on. INK is a dark chooser inside
a light app at 10:1 — the most striking and the biggest question, since one
screen breaking the theme is either a signature or a mistake.

---

## v0.113.2 — an overcast sky is a cool grey, and the four cards were not equals

Two faults, both measurable, and the reading around colour theory named them
before the eye could.

**The four cards were not the same weight.** Mixing a fixed percentage of each
module colour into white looks even on paper and is not, because the four
sources are not equals to begin with: measured in OKLCH they run C .121 to .154
and L .769 to .880. Tools' mint is the most chromatic and one of the darkest,
metro's gold the lightest, so the grid came out with tools heaviest and metro
faintest. This is the standard failure — two hues at matching perceptual chroma
feel balanced, the same hues at different chroma feel unbalanced with the more
saturated one dominating, and the traditional harmony rules all assume equal
saturation as a baseline.

Faces are built at matched lightness and matched chroma per stop now,
inheriting only the hue. A set of colours reads as a family when each sits at
the same perceptual distance from neutral; it reads as four swatches when they
do not.

**And the overcast feeling was literal.** An overcast sky is a cool grey — that
is the whole description — and the ground was sitting at hue 260 with a chroma
of .005. That value is the dead zone: enough tint to be felt, not enough to
register as a decision, which is exactly the "accidentally off-neutral" trap.
Pure greyscale also does not occur in nature and tends to read as unnatural, and
a neutral surrounded by saturated colour takes on the opponent cast of whatever
is nearest it, so a grey among four hues gets pushed four ways at once.

The ground is a warm neutral now: hue 76, chroma .013 so the tint is a decision
rather than an accident, and lifted. Same value structure, and it stops being
weather and starts being paper in daylight.

Contrast unchanged: no new failures, module audit zero in both themes.

---

## v0.113.1 — the light belongs to the card

The four pools worked, and they only worked at the aspect ratio they were
measured on. Anchoring them to percentages of the viewport meant a shorter
screen, a tablet or a rotation slid every one of them off the card it was
supposed to sit under. Checked at 360x640, 390x844, 430x932 and 768x1024: the
card centres move by up to 190px horizontally between them.

So the pool is attached to the cell. It goes wherever the card goes, at any
size, with no measurement to keep in sync — and it puts the physics the right
way round, which is the better half of the change. The cards emit onto the
ground rather than the ground happening to be tinted underneath them. Move a
card, add a fifth, change the grid, and the light follows on its own.

With the light coming off the cards, the ground goes flat and gets out of the
way: one near-neutral tone with a hair of fall so it is not a dead field.

**The stops are weighted outward,** which looks wrong written down and is the
only thing that works here. A card covers the middle of its own pool, so a
conventional falloff puts all the colour exactly where nothing can see it. The
visible part is the band in the gutters, so that is where the alpha sits: 70% at
the centre, still 62% at the halfway mark, 34% at 78%.

**And they breathe,** nine seconds, out of phase by a quarter cycle each. In
phase they read as the page flickering rather than as four lights. Reduced
motion holds them still at a fixed opacity.

Contrast unchanged: no new failures, module audit zero in both themes.

---

## v0.113.0 — the chooser ground is the four modules, out of focus

Every single-hue version of this failed the same way, and it took four attempts
to see it as one problem. A violet-grey clashed with the mint and the cream. A
neutral grey fixed the clash and read bland. The splash's blue brought the clash
back in a different key. The fault was never which colour — it was that one
colour has to sit behind four cards in four other colours, and there is no
single hue that agrees with all of them.

So the ground carries all four. A soft pool of each module's colour, centred on
the card that owns it: cyan top left, gold top right, mint bottom left, lavender
bottom right, over a near-neutral base. The centres are measured against the
real card positions rather than guessed, so each pool actually sits under its
own module. Nothing on the screen is foreign to what is behind it.

They are wide and shallow on purpose — 84% by 40% each, fading out by three
quarters — so the effect reads as a tint the whole field shares rather than four
blocks. Because the cards cover most of their own pool, what you actually see is
the spill in the gutters and margins, which is why they are stronger than they
look in the numbers.

Contrast unchanged: no new failures, module audit zero, project audit steady.

---

## v0.112.10 — the black flash, the bare top, and titles with a lift

**The challenge screen was flashing black in light mode,** and it was carried
straight over from dark. The entrance dims the display to brightness(.25) before
it stutters on, which on a near-black panel is an unlit screen and on a
near-white one is a black rectangle. Light gets its own range now: the unlit
state is a dim, slightly desaturated panel at .965, and the flicker moves
between .97 and 1.04 rather than a quarter to one and a half. Same stutter, in
the right key.

**The field started too high and fell too far.** Beginning at --surface put a
near-white band across the top of the screen with nothing in it, which is the
bare feeling. It starts one step down and spends more of its height near the
floor, so light still comes from above without giving a third of the screen away
to it. Splash and chooser share the change, since they share the recipe.

**The pinned chips got their colour back.** Rebuilding them as white with a 7%
tint fixed their invisibility and left them anaemic; the tool colour runs at
13-24% through the face now, the border carries nearly half of it, and the icon
is 78% of the tool colour rather than being mixed most of the way to ink.

**And the titles are lifted.** Dark uses a glow, which does not transfer. The
paper equivalent is an emboss: a white pass above, a soft dark one below, the
same modelling the cards get, at type scale. It has to be drop-shadow rather
than text-shadow — the titles are painted with background-clip:text, and a
text-shadow paints beneath a transparent fill and shows straight through it.

Contrast: no new failures, project audit steady at 26, module audit zero.

---

## v0.112.9 — the tagline audit, the chooser, and the last of the muddy darks

**The subtitle was never a header line.** Truncating it was treating the
symptom. Relative Pitch had no header tagline of its own — it was borrowing its
CARD subtitle, which is written for a card and roughly twice what the header can
hold. Staff Notes had no entry in the map at all, so it showed nothing.

Audited all thirteen exercises in both languages: they now all have a tagline,
none clips, and every header sits on one line. Relative Pitch gets "name it
cold" and Staff Notes "read it, name it", which is the register the rest of the
set already uses. The Italian for Staff Notes needed to be shorter than the
English, since NOTE SUL PENTAGRAMMA is the longest title in the app and leaves
its tagline the least room.

**The chooser follows the splash now.** Flat mid-tone read muddy behind pastel
cards, flat neutral read bland — both were flat, which was the actual problem.
The splash already solves the same brief, a field that has to hold anything in
no particular theme, and it does it with a fall from near-white down into the
floor. Sharing the recipe also means the app opens on one surface and stays on
it: splash into chooser, no cut.

**The last two muddy darks.** The fork button and the havens were the remaining
places a warm ink pinned against the floor was sitting on a near-white card,
where it reads brown rather than warm. Both lifted. The havens took a second
pass: gold reads instantly by hue, but hue alone strands anyone who cannot use
it, and at the first value the luminance step off a plain segment was 1.09. The
shipped gold is 1.8, and a cleared haven 2.5, so it is findable either way.

**Two more audit blind spots, both found by this pass.** It could not read
color-mix output, so any gradient starting with one made the backdrop walk fall
through to the page ground. And it treated background-clip:text elements as
having a painted box — those paint into the glyphs and nothing else, and since
the gradient is always an accent, it invented a failure every time. Fixed both:
thirty-one failures cleared, none introduced.

---

## v0.112.8 — the header wrap, the bland ground, and an audit that could not see color-mix

**The header tagline.** The subtitle was shortened once, but that fixed the hub
card, not the header — a different layout with a fixed-height box that the title
scales to fit. The base rule sets nowrap with an ellipsis, which works on the
title alone; with a subtitle appended inline, the SPAN inside still wrapped,
because the ellipsis belongs to the block and not to its inline child. So the
second line ran into the rule underneath. The row is a flex line now with the
ellipsis on the subtitle itself, where the overflow actually is. Header height
goes from 38px back to 19 on the longest one, and the shorter modules are
untouched.

**The chooser ground was bland because neutralising it took its modelling too.**
Fixing the muddiness left a flat field with two pools at 3 to 9 percent. It gets
what the module pages got: a warm key from above, a cool fill at the lower
right, a cool lift at the left, and a real top-to-bottom fall. Neutral in hue,
not neutral in modelling — those are separate decisions and only the first one
was wanted.

**The picker cards were pale because five sixths of each was neutral.** They
mixed 10% of the module colour into white at the top and then ran to the
un-themed surface for the rest of the height, so only the lid carried any
identity. The colour runs through the whole face now, 26% down to 9% and back up
at the foot, with the same four-layer shadow and rim the module cards got.

**And the audit could not see color-mix.** Both its colour parser and its
gradient extractor only knew rgba(). A gradient whose first stop is a color-mix
serialises as color(srgb ...), so the backdrop walk fell straight past the card
to the page ground and reported failures for text that is comfortably legible on
a pale face. Fixed in both places. With honest backdrops it found something
real: the peek labels mix 52% of the module colour into ink, which was tuned
against a nearly white face and lands at 3.5-4.0:1 against a tinted one. 34%
now. Thirty-one failures cleared, none introduced.

---

## v0.112.7 — the status colours had the same two-grounds problem

**The stats chart was a row of near-black bars.** in-tune, sharp, flat and metro
are pinned dark enough to clear 4.5:1 as small text on the floor, same as the
accent was. Used as a filled bar on a near-white card they measure 9.4 to
10.5:1 — and a filled shape is a graphical object, which needs 3:1, not 4.5.
So the chart was reading correct and heavy at the same time. A lifted set now
exists for fills and lands at 5.2 to 5.8:1 on a card: still comfortably above
the graphical floor, and green again rather than nearly black.

**The stats sheet was still wearing the page floor,** the same fault the
settings sheet had: a raised panel that fades to --bg-1 ends up with the page's
own colour along its bottom edge. Paint only — the geometry stays in the base
rule, which is the mistake that made settings unusable two versions ago.

**And the module picker was muddy for a reason.** Its ground carried real chroma
at hue 293, a violet-grey, and four cards in four other hues sat on it — one of
them lavender, right next to it. Four hues on a fifth hue is what makes a screen
look dirty rather than colourful; the ground was competing with everything it
was supposed to hold. Near-neutral now, a touch warm, at the same depth: the
seamless-backdrop trick a product photographer uses so that objects in different
colours can share a frame. The chooser stops being a colour and goes back to
being a surface.

Contrast: no new failures, project audit steady at 26, module audit zero.

---

## v0.112.6 — one accent was doing two jobs, and off did not look off

**Why the dark colours read harsh.** --accent is pinned at OKLCH L .36 because
it has to clear 4.5:1 as small text on the FLOOR, which is the hardest ground in
the app. But almost everywhere you actually see it — chip borders, labels,
controls — it is sitting on a CARD, two full steps lighter, where that same
value measures 9.5 to 10.9:1. That is not colour, it is ink, and ink on a pale
card looks severe.

One token cannot serve both grounds. --accent-lift sits at L .46 for card-borne
use and clears 6.2 to 7.1:1 there, which is comfortably above AA while reading
as a colour again. The floor keeps the darker value, because on the floor it is
genuinely needed. Settings chips take the lifted one for their border and label.

**The havens were the hardest thing to find on the ladder,** which is backwards
for the one mark that tells you where you can fall back to. In dark a gold rim
glows against near-black and reads instantly; on a light card the same rim is a
thin line on a pale ground. Filled in light now, with the rim kept as the edge
rather than as the whole signal. A haven segment measures 7.4:1 against a plain
one, where before it was a hairline.

**An unlit lamp was a white box on a white card.** In dark it is dark glass,
which explains itself. On paper the equivalent of off is recessed, so an unlit
lamp is pressed into the card: the token drops a step, and it takes the standard
soft-UI inset pairing — a dark shadow at the top edge where the surface falls
away and a light one along the lower lip where it catches the ambient. Same
technique as a raised chip, run in reverse. It now sits 1.36:1 below the card
instead of level with it.

That inset pairing is the one genuinely new idea from reading around the current
material on depth-driven UI, and it is the piece light was missing: raised
elements were getting the four-layer treatment while recessed ones were getting
nothing at all, so half the vocabulary was mute.

Contrast: no new failures, project audit steady at 26, module audit zero.

---

## v0.112.5 — light gets volume the way paper does

Side by side, dark reads three-dimensional and light reads fat. The reason is
that dark's depth is all emission: every card has a lit rim, the page carries a
theme-tinted bloom from above and two smaller pools, icons glow. None of that
transfers — a glow on a light ground is a smear, which is why it was stripped in
the first place. But nothing was put back in its place, so light had the geometry
of a design with no lighting model at all.

What does the same job on paper is edge and shadow. Cards now get all four
things that describe a real object on a lit page: a defined rim, a crisp
highlight along the top where the light strikes, a contact shadow directly under
the edge with a wide far falloff behind it, and a diagonal fall inside the card
so it is a surface rather than one flat tint. It is the same information dark
gets from a glowing border, said the other way round.

**The page field got dark's structure too.** Dark paints three theme-tinted
pools; light had a single top-down ramp and a 7% tint, so there was nothing to
read across the screen. Same three-pool geometry now, opposite physics: a warm
daylight bloom from above, a cooler accent lift at bottom right, a faint accent
pool at left. A warm key with a cool fill is what stops a light field reading as
one wash — it is how a real room looks and it is why the flat version felt
synthetic.

**And the selected chips had gone dark in every theme.** They mixed 70% of
--theme over white, which was right when --theme was a mid-tone. The light ramp
took the accent to OKLCH L .36, so the same mix landed at 3.0-3.9:1 against its
own label: a dark slab sitting in a pale sheet, in all four themes. A selected
chip in light should be a tinted LIGHT chip with a firm edge, not an inverted
one. It is 16-26% over white now with the accent as the border and the label,
which is legible and still unmistakably ON.

Contrast unchanged: no new failures, project audit steady at 26.

---

## v0.112.4 — the settings panel was unusable, and it was my fault

Adding the light-mode background override in v0.112.2 split the base rule. I
closed `.settings-modal-content` after its first property and opened
`body.light .settings-modal-content` before the rest, which handed max-width,
padding, max-height and overflow-y to the light selector alone. In dark the
panel had no width limit, no padding and no scrolling, so it rendered oversized
and immovable — and since the theme switch lives inside it, there was no way to
get to light mode and out of the problem.

The base rule owns geometry again; the theme rule may only repaint. Verified in
both themes: 366px wide inside a 420 max, correct padding, scrolls, sits inside
the viewport.

Sentinel-pinned, because the shape of this mistake is not specific to one
selector. Any theme override that reaches past paint into layout can strand a
control that only exists inside the thing it broke.

The lesson for the audits: everything I checked after that change was a
full-screen module view, and every one of them passed. A modal that only opens
on a tap was never in the frame. Screens behind an interaction need opening.

---

## v0.112.3 — light was flat because I had taken the depth out of it

The complaint that dark looks alive and light looks flat turned out to be
measurable rather than a matter of taste. Compared side by side:

    dark   card chroma .037-.042   fall inside one card .029
    light  card chroma .011-.015   fall inside one card .019

A third of the colour and two thirds of the modelling. On top of that light has
no glows, which were removed on purpose because a drop-shadow on a light ground
smears rather than emits. Three of the devices that give dark its depth were
missing from light, and two of them were mine.

Cards carry their hue again, chroma .038 falling to .026 across the card, with
the internal fall widened to match dark's. Every card is now a surface with a
top and a bottom rather than a flat rectangle, and each one wears its module's
colour instead of being white with a rumour of it. Floor-to-card separation is
unchanged at 1.84-1.89.

**The launcher's quick-access chips were wearing the dark palette.** Their
colour comes from --pc, which falls back to the dark theme's cyan, so in light
they were a 9% tint of a colour that does not exist in the light palette, on a
light ground: effectively invisible, which is exactly how they looked in the
module picker. They are small raised chips now, white with a tint of the tool's
own colour, a real border and a contact shadow, and an icon dark enough to read.

**The splash has moved with all of this** — it builds from --surface, --bg-1 and
--bg-0, so it followed the ramp, the chroma equalisation and this pass without
being touched directly. Checked: it runs light at the top into the floor at the
bottom, which is the direction it was fixed to in v0.112.1.

No new contrast failures; the project audit stays at 26 with none introduced.

---

## v0.112.2 — why light mode read washed out and heavy at the same time

Two faults, and between them they explain a complaint that sounded like it
contradicted itself.

**The four floors were not the same weight.** The ramp set every floor to the
same OKLCH lightness and then multiplied each hue's existing chroma by the same
factor — which preserved the inequality it was supposed to remove. Measured:
metro's gold sat at C .137 and tools' mint at C .128, while tuner's blue sat at
C .054 and train's lavender at C .066. Two and a half times the colour at
identical lightness. Perceived weight is lightness AND chroma, so two modes read
heavy and two read washed, from what was meant to be one recipe.

Chroma is absolute now, .075 on every floor. Gold and mint come down a long way,
blue and lavender come up slightly, and all four sit at the same weight with
their hue intact. Separation holds at 1.87 to 1.98.

**The daylight wash was repainting the top of the screen.** A white overlay at
62% at the top falling to 3% at the bottom, tuned when the floor was pale. On a
deeper floor it means the top third is nearly white and the bottom is the raw
floor colour: washed out up there, heavy down here, on every screen. Measured
down the left gutter the swing was about 90 points of luminance top to bottom.
It is 20% to 5% now, and the swing is 18 to 19 points, the same on all four
modes. A light field should be felt, not seen.

**And the sheets were dissolving into the page.** Settings, the favourites
sheet, the launcher sheet and the quiz sheet all ran from the card colour at the
top down to the page floor at the bottom. That reads as depth in dark, where the
floor is the darker end and a panel fading toward it looks like it is receding.
In light the floor is the darker end too, so a raised sheet ended up wearing the
page's own colour along its bottom edge and stopped looking raised at all. They
stay on raised colours now.

Contrast: no new failures, nine fixed, none made worse; the project audit goes
42 to 26 with none introduced. Two per-theme inks and the launcher hint needed
re-pinning by a hair as the floors moved.

**The audit was also measuring elements mid-fade,** which is why the launcher
hint kept reporting a different failing ratio on every run. It now skips
anything with an opacity transition in flight, and three consecutive runs agree.

---

## v0.112.1 — the light gradient ran the wrong way, and the climb got twice as long

**Light was coming from under the floor.** The splash gradient ran from a pale
top, down through the ground colour in the middle, and back up to near-white at
the bottom. That put the brightest band of the screen underneath everything,
which is why cards looked weakest exactly where they sit and the whole thing read
bottom-heavy. It runs one way now: lit at the top, settling into the floor and a
shade below it at the bottom.

The launcher had the opposite problem and the same cause. Its ground is a literal
rather than a token, deliberately, so the chooser does not change colour with
whichever module you last used — but that meant the ramp could not reach it, and
at OKLCH L .787 it stayed lighter than every module floor once those dropped to
.745. On the one screen that is nothing but cards, the cards had the least to sit
against. Re-pinned to ramp depth, still less chromatic than any module so it
reads as a null state. The lower radial pool is softened and lifted off the
bottom edge as well; anchored at 104% it pooled light under the content. The
crossfade veil tracks it exactly, or the background appears to change colour
mid-fade.

**The climb is twenty-four rungs.** Twelve was too short to be hard — two warm-up
rungs, four in the middle, six that could bite, and a clean run only had to
survive six real questions.

Four distance bands now instead of three, because doubling the length without
adding a step would just have meant more of the same: WIDE at a fourth or more,
OPEN at a third to a fourth, CLOSE at a tone to a minor third, ADJACENT within a
tone. Six rungs each. Havens sit on the first three band edges, at 6, 12 and 18,
so there are three places to fall back to rather than two, and each still means
what a haven has always meant here: the value is yours, and the lifelines and
replays refresh.

Values run 25 to 100,000, so a clean summit pays 200,000. The multiplier step
drops from a tenth to 0.08 because there are now twelve lifelines to spend across
four bands rather than nine across three; spend them all and you settle at ×1.04,
which is close enough to the floor that the difference between a careful climb
and a helped one is the whole score. Verified: clean summit 200,000, every
lifeline spent 104,000, a fall at rung 20 leaves 22,000, banking at 15 with two
lifelines gone pays 5,888.

All twenty-four rungs verified to deal four distinct options with the answer
present and every distractor inside its band's distance range.

---

## v0.112.0 — light mode gets a floor

Testers said light mode was washed out across the whole app. Measuring it agreed
and gave the reason: floor-to-card contrast was 1.16:1 in every one of the four
mode palettes. That identical figure across four independently chosen palettes is
the giveaway that it was a systematic architecture choice rather than four
decisions, and at that ratio nothing on screen reads as raised. Everything looks
like haze because everything is the same brightness.

**Generated from one ramp instead of picked by hand.** The four light palettes,
plus the un-themed fallback, now come from a single OKLCH ramp: floor at L .745
with chroma held high, card at L .965 with chroma pulled back, borders at L .52,
accent at L .36. OKLCH rather than HSL because equal perceptual lightness looks
equally deep across hues and equal HSL lightness does not, and because chroma
has to be gamut-aware — the earlier attempt in HSL multiplied saturation, which
did nothing at all for metro's gold and tools' mint since both were already at
the edge of what sRGB can show.

Separation now measures 1.84 to 1.96 across the four, with a spread of 0.12
between best and worst. The mode hue survives in the card as a whisper, which is
what keeps the four modes telling each other apart.

**Dropping the floor broke everything that was pinned to it,** and that was most
of the work. A before-and-after diff across twelve screens in all four modes
found 119 newly failing elements, every one of them text sitting directly on the
background rather than on a card. All resolved:

- The per-theme ink trio had been pinned against the card. The card is no longer
  the hard case, so the trio is pinned to the ground instead, at 7.0 / 5.5 /
  4.6:1. On the card, which got lighter, they now land 13.7 to 14.7.
- `--tab-accent` carries the bottom-nav labels and the session stamp, both drawn
  straight on the ground. Re-pinned with headroom, since the two contrast audits
  resolve the nav bar's backdrop differently and 5.3:1 clears both.
- The shared status colours — in-tune, sharp, flat, metro — had all fallen to
  around 2.6:1. Re-pinned to clear 4.6 on every ground and 8:1 on every card.
- Level chip and phase pills, deepened for the second time; the previous fix was
  measured against the old floor.
- The help button stopped being thinned to 90 percent opacity.
- The accent deepened with the floor, because it had to: at the old value it
  would have dropped from 5.24:1 to 3.66:1 on the new ground.

**Two long-standing failures fixed on the way past.** The session stamp's goal
text was half-opacity ink that never cleared AA even before this, and the panel
badge sat on a translucent wash so its contrast moved with whatever ground it
happened to land on. Both are real colours on real fills now.

**Seven hardcoded copies of the old tuner accent** were sitting in the string
face, the capo popup and the instrument pills, frozen at the old value while the
token moved. They read from the token now. The tonal-centre panel's greys were
left alone deliberately: that is an instrument face, not themed chrome.

Light failures across twelve screens: 150 down to 138, with none introduced.
The project's own light audit: 42 down to 25, none introduced. Dark mode
unchanged at 65, which is the point — nothing outside the light blocks moved.

---

## v0.111.4 — light-mode sweep of the module

A full pass over every Relative Pitch screen in light mode: practice, answered,
chromatic, the entrance settled, mid-game, the result, settings and stats, all
screenshotted and inspected rather than trusted to the contrast numbers.

The module holds up. Lamps, glows, ladder, hearts, the screen panel, the boot
sequence, the transport row and the utility row all read correctly on the light
surfaces, and the automated audit stays at zero failures in both themes.

One inconsistency found and fixed: on an unanswered card the big note reading
dimmed to placeholder grey while the Hz line under it stayed lit in the hit
colour, so half the display looked switched off and half looked on. Both dim
together now and both light together on the reveal.

The wider question — testers finding light mode across the whole app too light —
is a palette decision, not a bug, and it gets its own mockup file rather than a
quiet change: LightMode_Palettes.html, four palettes on the same components.

---

## v0.111.3 — four things on the intro that were not behaving

**THE RULES was restarting the entrance.** The toggle went through rlpRender,
which rebuilds the intro card, which replays the whole boot sequence from the
flicker. Opening a paragraph should not restart the machine. It edits the DOM in
place now; the card node survives, the ladder stays built, and the title does
not blink.

**A ghost B-flat was showing through the placeholder.** The unlit segment behind
the reading is what makes a lit one look lit, but that only works behind a real
value. Behind a two-dash placeholder it reads as a stray letter someone forgot
to clear. The ghosts appear once there is something to read and not before.

**THE CLIMB was sitting on the screen.** 22px above it now.

**START cut rather than handed over.** The intro vanished mid-word and the game
appeared fully formed, which is a page swap, not a machine changing state. The
intro lifts away over 220ms and the first rung arrives from below over 340ms.
The first note was also scheduled 350ms after the card was built, which put it
right in the middle of that; on rung one it waits 620ms instead, so it lands on
a settled screen. Measured at 854ms after the tap, with the transition classes
cleaned up behind it.

Reduced motion skips the hand-off.

---

## v0.111.2 — the intro stopped explaining itself

The second card described the three distractor bands and how close the wrong
answers sit in each one, and it did that before you had heard a single note.
Nobody can use that information at that point; it only becomes real once you are
in ADJACENT and everything on screen is within a tone. The game already prints
the band and its gap in the card head at the moment it matters, so the chips
were a manual for something that explains itself two seconds in.

Gone, along with the card holding them. The intro is one card ending on START,
which is also what the entrance animation was already driving at — the sequence
used to keep going for another half second after the button, fading in a second
card that pulled attention back off it.

The rules survive, because two things genuinely are not discoverable from play:
that lifelines cost multiplier, and that unspent ones expire at the band edge.
They live under a plain text link below the best line now. Closed it is one dim
line; open it is the four rules in place, no second card, and it collapses back.

519px settled instead of two cards and a scroll. The entrance now ends: START at
2.0s, best line at 2.1, rules link at 2.2, and the button starts breathing at
2.3.

---

## v0.111.1 — the intro ladder was showing somebody else's run

**The bars on the start screen were arbitrary, and worse than arbitrary.** They
lit rungs one to eight with nine standing tall, which was a number carried over
from the design mock and had nothing to do with the person looking at it. The
ladder sits on the intro to be the machine's memory of you, so it reads your
furthest rung now: cleared rungs dim, the one you reached standing tall, and a
caption saying FURTHEST 9/12 beside the multiplier you start on. A first-time
player gets twelve dark bars and NO RUNS YET, which still shows the shape of the
climb without pretending to a history.

**START makes no sound of its own.** The entrance is built so the chime belongs
to the build and the next thing you hear is the question; a cue on the button
sat between the two and blurred exactly the line it was meant to draw. Verified
silent at the tap, with the first note arriving on its own.

---

## v0.111.0 — the climb has an entrance

Arriving on the CHALLENGE tab used to look like a different page from the game:
a title, one line, a START button, and a stack of bars looping an attract
pattern. None of the machine you were about to use was on screen.

It is the same machine at rest now. The ladder, the twelve lamps and the
instrument screen are all present before you press anything, and they build
themselves once on arrival while a welcome chime plays over the top.

**The sequence,** five phases with one focal point each, measured in the app:

    0.12  the card lands and the screen stutters to life with its readings on it
    0.64  the ladder climbs a rung per tick, the record rolling up beside it
    1.32  ladder tops out; the lamps sweep once
    1.37  the record lands
    1.82  the title arrives on the chord, then the line and START
    2.42  the bands card follows, chips after it
    2.84  settled, and silent

The screen readings snap on inside the flicker rather than fading in afterwards,
because a display shows its content as it finds mains. Segments land with a
touch of overshoot instead of sliding to a stop, the rung you reached last time
gets a brighter pop as it grows tall, and once everything settles START takes a
slow three-and-a-half second breath.

**The chime lives entirely inside the build, and that is the point.** Once the
intro settles on your records nothing sounds again until you press START, so the
first note after that is unambiguously the question rather than a leftover
flourish. Verified: twenty-two sounds during the build, zero between settling
and START. It is bespoke rather than a cue-bank event, because it is tied frame
by frame to this animation and a user-swappable cue set would break the sync. It
still respects the module's own sound switch.

The idle sweep is one slow pass every two and a half seconds while you decide,
rather than the continuous chase the old attract loop ran.

**Two things the port needed that the mock did not.** The card's fade-in and the
staged reveal of its contents were sharing one class, so the moment the card
appeared everything inside it appeared with it; hiding is now a class on each
element, applied before the first paint. And the boot's timers are on their own
list that gets cleared by teardown and by START, so leaving mid-animation or
starting early cannot leave anything running — verified zero timers after exit.

Reduced motion skips the whole thing and renders the settled state.

---

## v0.110.9 — the chimes were scrubbing the note, and lifelines were free

**The chime after every correct rung had to go, and not for taste.** It fired a
pitched fifth immediately after the target note, in a drill whose whole job is
holding a pitch in your head. It was rinsing the thing you were being asked to
carry. What is left is the shape of a game show: a flourish when you press
START, then nothing but the notes until the run ends one way or the other.

The three remaining sounds — summit, loss, bank — go through the app's own cue
bank rather than being hard-coded arpeggios. That means they follow whichever
cue set the person picked and their per-event volumes, instead of ignoring every
audio setting in Settings.

**Lifelines were free, which made them admin rather than a decision.** Three a
band, expiring at the edge, so the only wrong move was leaving one unspent. They
cost something now: each one takes a tenth off the multiplier the final payout
is settled at. Start at double, drop a tenth per lifeline, floor at level. A
summit reached without asking for help pays 50,000 against 25,000 for the same
climb with help.

The multiplier sits under the ladder while you play, lime while it is still
clean, so the cost is in front of you at the moment you are deciding whether to
take the fork. The result screen shows the working — 25000 × 2.0, no help taken
— and the best take carries its multiplier into the intro and the stats sheet,
since a best score is now a settled figure rather than a rung value.

**The writing.** Every line in the challenge was a run of short declaratives,
which is the tell. "Twelve notes. Four answers each. One wrong and you leave with
your last haven." Three fragments where one sentence would do the work. All of
it rewritten in both languages to breathe: the intro line, the four rules, the
four result captions. The rules also stopped repeating the same
bold-lead-then-fragment shape four times in a row, and one of them now explains
the multiplier, which is new information rather than a restatement of the
replay budget.

---

## v0.110.8 — a voice for the drill, and the climb stopped being a list of lists

**Tone bank in settings.** The drill sounded on grand piano because that is what
the app's reference tone happened to be. It picks its own voice now, from the
same bank every other module uses, and swaps it in for the length of one note
before putting the app's setting back, so choosing a nylon guitar here does not
change what the Chords tool sounds like.

Both halves of the skin opt-out are in, because a tone row that does not ask for
one inherits the piano console's near-black button and the Chords tool's green
popup, and then ships looking broken on a Train card. The button override is
keyed on the modal id and the builder is handed ex-tonepop explicitly. Pinned,
since this is the third time that trap has come up.

**The climb was eleven stacked blocks.** A card of twelve ladder rows, then a
card carrying a header, the lamps, the screen, a replay button, a row of replay
pips, a caption under the pips, a caption over the lifelines, the lifelines, the
options, the verdict and the actions. Almost half of it was labelling the other
half.

Now it is one card of six blocks. The ladder is a horizontal strip of twelve
segments at the top, cleared rungs dim, the one you are on standing taller,
havens in gold, with a line underneath giving the rung and what is already
banked — the same information as twelve labelled rows in a fifth of the height.
The replay budget moved onto the screen as pips, where the hearts sit in
practice, so the two modes read the same way. Replay itself joined the lifelines
as one utility row of four, which is what it always was: something you spend.
And the screen's right-hand reading is what is on the line right now rather than
a lifetime best you cannot act on mid-climb.

The card is 624px, where the two cards together were closer to 930. Identical
across the reveal at rungs 1, 5 and 12, in both languages.

Lifeline labels lost a word each to fit four across — FORK, DROP 2, B OR W.

---

## v0.110.7 — the accidental toggle was rewriting your answers

In chromatic mode the answer input was seven letters and a flat/natural/sharp
toggle. Tap D-sharp, get it wrong, switch the toggle to flats, and the red mark
jumps to E. It is the same pitch class and the app is not lying, but it reads as
your own history moving under you. Worse on natural: the mark disappeared
altogether while the spent try stayed spent, so the card looked like it had
forgotten a guess it was still counting.

The toggle was the problem, not the marking. It was a mode you had to hold in
your head, it cost two taps per accidental, and it meant one button could mean
three different notes depending on state you could not see from the button.

**Twelve buttons instead, laid out as a keyboard.** Five accidentals on an upper
row, shifted half a column so each straddles the two naturals it sits between —
C-sharp between C and D, nothing between E and F, exactly where the gaps fall on
a real keyboard. Seven naturals below. Every note is one tap, every button means
one thing, and a wrong answer stays where you put it because the mark is keyed
to the pitch class rather than to a letter plus a mode.

Names come from the app's existing noteNaming preference, so solfège users get
Do-sharp and Mi-flat without the module needing its own setting. White-key mode
is unchanged, a single row of seven.

Verified all twelve reachable in one tap, marks stable across re-renders, both
pools and both input styles still answer correctly, and the card holds its
height through the cycle at 468 white and 513 chromatic.

---

## v0.110.6 — the free reference tone had to go, and the card lost a third of itself

**HEAR IT AGAINST A was a hole in the design.** Striking the fork costs you your
run; that button handed you the same A440 for nothing, and it arrived at exactly
the moment you would want it, right before the next note. The fork is supposed
to be the resource the whole module is built around. Removed, and pinned, so it
cannot come back as a convenience.

**The hearts now do what they do everywhere else.** The px-heart sprite has a
loss animation — a dark damage flash, then the heart drains and falls away
leaving a pip — and the module was using only its resting states. It fires now
on the try you just spent, and only that one: the flag clears on the next render
so a re-draw does not replay every heart you have already lost.

**The card was loaded, and three things were doing nothing.** The verdict line
under the answers said "it was E flat" while the screen two rows up already
printed the note and its frequency, so it was the same fact twice; mid-card the
key going red and the heart falling say "not that one" better than a caption
does. Gone. The fork was the biggest button on the card despite being the rarest
action, and it sat between the transport and the thing you actually tap — it is
one line now, below the answers, where a rarely-used destructive action belongs.
It also stopped announcing A440, since the button is the fork.

The practice card is 468px, down from 582 two versions ago. Still identical at
every step of the cycle, in both languages, in every input mode: 468 with letter
keys, 511 with the accidental row, 426 with the lamps.

---

## v0.110.5 — one transport row, and a screen that looks like a screen

**The buttons were in three places.** Replay sat on its own above the fork, and
the two reveal actions were stranded at the bottom of the card under the answer
grid. They are the same kind of thing — what you do with the note in front of
you — so they are one row of three now, where replay already was: AGAIN, NEXT,
AGAINST A, each with a small icon, all three the same width. Next and the A
reference are dashed and dimmed until there is an answer to use them on, so the
row never changes shape. Replay carries the accent, since it is the one you
reach for while you are still working.

That also took 69px off the card, because the reserved space at the bottom is no
longer needed. The card is 513px through the whole cycle now, down from 582, and
still identical at every step.

The climb keeps its single wide replay. It has no next and no reference tone, so
a three-up row there would have been two thirds empty.

**The screen.** It had the right shape but was still reading as a box with
numbers in it. Three things fixed that. Scanlines, one pixel on and two off,
multiplied over at low opacity. A corner vignette, so the middle sits brighter
than the edges the way a lit panel does. And the values glow rather than just
being coloured — the note carries a two-stop halo in the lit colour, the streak
gets a smaller one once it is above zero, while the labels take a downward
shadow so they read as etched into the bezel instead of printed on the glass.

All of it is off or inverted in light mode, where a glow washes out and an
etched label wants a highlight above it rather than a shadow below. Contrast
holds at zero failures in both themes.

---

## v0.110.4 — one screen instead of four scattered readouts

The card was telling you four things in four places. The note and its frequency
sat in a thin strip, the tries were two grey dots below the answer buttons where
nobody looked, and the streak was in a card of its own, a scroll further down,
rendered as twelve pips and a caption. Meanwhile the whole thing jumped when you
answered, because NEXT and HEAR IT AGAINST A only existed after a reveal.

**The screen.** All four readings live in one panel now, laid out the way a
tuner front panel would be: the run on the left, the note and its frequency in
the middle, the record on the right, and the tries on a strip underneath. It has
a proper inset and a glass highlight along the top edge so it reads as a panel
let into the card rather than a box drawn on it. The ghost segments behind the
note and the Hz stay — an unlit segment is what makes a lit one look lit.

The tries are the pixel hearts from Music Quiz and Rhythm Survival, the shared
px-heart sprite, so spending one looks the same here as it does there. Two grey
dots said nothing; a heart going out says it without a label.

The climb uses the same screen with the same geometry: rung on the left, best
take on the right, and the strip underneath carries what is on the line. That
also cleared a duplication, since the card header was printing the rung and the
value as well; it now says which band you are in and how close the wrong answers
sit, which is the thing you actually want to know at a glance.

**No more jumping.** Both action buttons are always mounted and simply disabled
until there is an answer to move on from, and the climb reserves the height of
its taller state so the bank row and the CLIMB button swap in place. Measured
across a full card cycle — fresh, one wrong, answered, next — the card is 582px
at every step, and the buttons do not move by a pixel. The climb holds at 663px
across the reveal at rungs 1, 5 and 12.

A disabled control still has to be readable, so it is a dashed outline in muted
rather than the 34%-opacity smudge it started as.

**Contrast, and an audit that was lying.** The app paints cards with a gradient,
and getComputedStyle reports gradient-painted elements as having a transparent
background, so the audit had been resolving text against the body colour two
levels up. Taught it to read the gradient's first colour stop, and to ignore
stops that are themselves translucent, which is what made the fork button look
like a 1:1 failure when it is fine.

With honest backdrops it found three real ones, all in light mode or in states
built from opacity: ruled-out letter keys at 2.08:1, dimmed to the point of
being unreadable by a .5 opacity that a real colour replaces; the lifeline
numerals at 4.36:1; and the option letters at 4.27:1. Both themes are at zero
across eight screens now.

---

## v0.110.3 — reset was disarming itself, and the drill opened mute

Three from on-device, and one more the fix uncovered.

**Reset never fired.** Arm-then-confirm, and the arming tap re-rendered the
stats sheet through rlpOpenStats — whose first line clears the armed flag,
because opening the sheet fresh should never inherit an armed reset. So tap one
armed it, the re-render disarmed it, and every tap was a first tap. The button
never even said TAP AGAIN. Split into rlpOpenStats, which opens fresh and
disarms, and rlpRenderStats, which redraws in place and touches nothing.
Verified: first tap arms and relabels, second tap zeroes the tab you are on and
leaves the other alone.

**The drill opened mute.** rlpInit dealt the first card with silent=true, a
leftover from the prototype where init ran before any user gesture. In the app
you arrive by tapping the card, so the module whose whole point is "hear a note,
name it" opened with nothing to name. It deals live now; the autoplay switch
still decides.

Fixing that exposed a ghost: the note rides a 350ms timeout, and leaving the
module inside that window sounded a note on a hidden panel. Both deferred sounds
— practice card and climb card — now check the panel is still visible before
playing, same guard as every other deferred callback in the module.

**NATURAL and CHROMATIC, not 7 and 12.** The pool picker was labelled with
counts. Counts are what the code sees; names are what a musician reads. Settings
buttons, the card-head summary and the stats sheet subtitle all say the words
now, in both languages — naturali · media · 2 tentativi reads like the app,
7 · mid · 2 read like a debug string.

Also swept content and flow end to end while in there: dirty cards do not extend
the run, the fork zeroes it, 50/50 never eliminates the answer and eliminated
options ignore taps, banking pays the rung below, the SUMMITED badge shows on
the intro, and the lamps input answers by pitch class so it works in any octave.
All held.

---

## v0.110.2 — the module survey: a leak, a lost chime, and the favourites hole

Asked to go back over the whole build with fresh eyes. Three real findings.

**The comet outlived the module.** exitExercise stops every exercise from a
hand-maintained list — ivStop, ceStop, roadtripStop and eleven friends — and
Relative Pitch was not on it. Worse, switching bottom tabs does not call
exitExercise at all, so the comet's requestAnimationFrame loop kept running at
60fps on a hidden panel while the user sat on the Tuner. On a phone that is
compositor work and battery for nothing, invisibly.

Fixed both ways. rlpTeardown is on the stop list now, and every frame loop —
comet, landing, intro attract — bails the moment its own panel is hidden, which
covers any path that hides it without asking. The auto-advance timer got the
same guard, since it could fire after exit and render a hidden panel back to
life, restarting the comet with it. Verified: RAF alive in the module, dead
after back, dead after a tab switch, alive again on re-entry. Both guards are
sentinel-pinned, because the stop list is exactly the kind of thing a refactor
tidies away.

**The favourites hole, and it was not ours.** The hub cards carry data-fav-id
and the star pin works, but the favourites sheet renders from FAV_META, a
separate hand-built registry — and neither Relative Pitch nor Staff Notes was in
it. Pin either module and it silently never appeared in the sheet. So Staff
Notes has been half-favouritable since it shipped and nobody noticed, which is
what happens when the same fact lives in two places. Both entries added, with
icons and launch handlers.

**Small ones.** The START chime on the climb got lost in the port; restored.
Checked the rest of the assumptions while in there: progUpdate is a shallow
merge onto the live object so nothing clobbers the nested challenge stats, and
it feeds the perfect-session and achievement bookkeeping for free; progAddXp
exists; every colour var the module leans on is defined app-wide; all 88 t()
keys and 6 data-i18n keys exist in both languages; per-module settings not
surviving Reset All Progress matches how every other module behaves.

---

## v0.110.1 — the ghost glow, and copy that did not sound like the app

Three things from the first look at v0.110.0.

**The ghost glow.** A soft blob was drifting across the card, out of step with
the lamps. It was the ambient bleed: a 132x150 radial gradient tracking the
comet head, standing 26px above the lamp row and 48px below it, so it swept over
the card header and the readout as a second light that never lined up with the
first. At the end of each pass it snapped back to the left edge, which is what
read as something moving the wrong way.

It was there to give the row some spill back when the glows were clipped. They
are not clipped any more, and the three-stop shadows do that job properly, so
the bleed is gone rather than tamed. Verified: every lit thing on screen is now
an actual lamp, and the overlay sits on its housing to the pixel.

**The subtitle.** Fifty-one characters and it ended on "the fork is a resource",
which is a thing written about a design, not a thing said to a person. Now "Hear
a note alone · name it · no reference first", 48 characters, which sits between
Chord Ear at 42 and Pitch Match at 56. Fixed in all three places the same string
lives: the i18n value, the hardcoded DOM default, and the Italian twin.

The rules card had the same problem in longer form. Each line lost a clause and
a piece of documentation grammar — "Each band is a stage. Clear one and its
value is yours whatever happens after, and you get fresh lifelines and a fresh
set of replays" became "Clear a band and its value is yours for good. Fresh
lifelines and fresh replays with it." Italian rewritten alongside, not
translated after.

**The folder.** EAR TRAINING still said three exercises and listed three. Now
four, with Relative Pitch named, and the folder subtitle leads with pitch.

---

## v0.110.0 — Relative Pitch

The Coming Soon card said "name notes by ear, sing any degree from a given
root". Half of that was already Interval Training's SING mode wearing a
different name, so the module that got built is only the first half: hear a note
cold, name it. No reference before the card, no key established. The only tools
are a note you carry in your head and an A440 fork, which is what the skill
actually is outside an app.

That framing decided the shape. The fork is a RESOURCE, not a difficulty slider,
so there is no anchor setting and no in-app note picker — picking your own
reference lets you cheese it. Drift is not a mode either; it is a number on the
practice screen, notes named since you last reached for the fork, because the
run falls out of the drill for free.

**PRACTICE.** A note sounds, you name it. Letter buttons, or the twelve lamps
themselves if you would rather tap a keyboard. Two tries by default. After a
reveal there is HEAR IT AGAINST A, which plays the fork and then the note, so
you hear the interval you should have been computing.

**CHALLENGE.** Twelve rungs, four answers a rung. The ladder escalates on ONE
axis: how close the wrong answers sit to the right one. Rungs 1-2 offer nothing
closer than a major third, 3-6 a tone to a third, 7-12 everything within a tone.
Same note pool throughout, same tone length, same everything else. Two rungs of
warmup, four in the middle, six where you can actually lose.

Havens at 2 and 6, which are the band edges, and lifelines and replays refresh
on the same edge. One boundary, three meanings: clear a band and its value is
yours, and you get three fresh lifelines and six fresh replays. Anything unspent
is gone. Six replays a band rather than three a note, so where you spend them is
a decision instead of a formality.

One wrong answer ends the run and you leave with your last haven, or nothing if
you never cleared one. Falling back to a haven and continuing, which is what the
first draft did, made banking pointless: a run you cannot lose is not worth
walking away from.

**What the design pass caught, in the order it hurt.**

BLACK-OR-WHITE was dead for a third of the game. The first band had been
white-keys-only, so "is it a black key" always answered no. That was a second
difficulty axis bolted onto the distance one, and removing it fixed the lifeline
and simplified the ladder at the same time. Sentinel-pinned, because a pool
creeping back into a band would bring the bug with it.

A miss taught you nothing. It named the answer and stopped, in a module whose
entire subject is how far apart two notes are. It now says "it was E-flat, you
were a semitone high", on the card and on the result screen.

The distractor fallback filled with random notes when a band could not produce
three, so the band that exists to guarantee distance occasionally served a
semitone. It sorts by distance now. Also pinned.

**The lamps.** The play surface is twelve lamps with a comet running left to
right while you listen, then the answer lands. Getting them to look like lights
rather than coloured boxes took three things: a housing with an inset shadow and
a lens gradient so an unlit lamp reads as dark glass, a three-stop glow so the
falloff is not a hard halo, and a white core above three-quarters brightness,
because a real emitter goes white at full output rather than more violet. Attack
is one frame, release is exponential on a 135ms constant; the first pass used a
linear tail and read flat.

Two bugs there. The glow was clipped by two `overflow:hidden` ancestors, and
even unclipped it sat inside each lamp, where the next lamp's opaque housing
painted over it. Glows now live in one overlay above every housing. That in turn
erased the key letters in keyboard input, so the captions moved into the overlay
too, above the light.

Only opacity and transform are animated. The glow shadows are painted once and
never touched, because animating box-shadow repaints a blurred area every frame.

**Colour.** The palette was already sitting on a complementary pair without
anyone deciding it: the Train violet measures 254 degrees, its true complement
is 74, and the in-tune lime is 84. Ten degrees off opposite is why the reveal
reads before you have read the label. Amber at 17 completes a rough
split-complementary, which is where the fork sits. 60/30/10, one accent lit at a
time.

Every lamp colour is a variable, so light mode is an override rather than a
parallel stylesheet — tighter bloom, denser fill, darker accents, because a glow
that reads on black washes out on white. Pinned, since hard-coded glows are
exactly what shipped the tone banks black twice.

**Contrast and type.** A pass with element opacity counted, not just colour,
found 124 failures across ten screens in the two themes. Nearly all of them were
labels dimmed with `opacity:.55`, which looks fine on black and disappears on
white. Those are real colours now. Type floor is 9px; there were 39 elements
below it, six at 7px, which had crept in card by card. Both themes are at zero
failures.

**Housekeeping.** Settings and stats use the app's own shells: `iv-cog-btn`,
`ce-stats-modal`, `progress-modal-close`, and the `iv-stats-hdr-btn` pattern
where STATS lives in the settings header, the way Staff Notes, Interval, Pitch
Match and Chord Ear all already do. Settings and stats persist inside progState,
so they ride the existing backup instead of adding a forty-eighth standalone
key. Audio goes through chordPlayMidi and inherits the soundfont and the master
volume. Seven sentinel pins added.

Stats are one window with two tabs rather than two windows. The per-note
accuracy stays separate between them on purpose: Challenge gives you four
options and Practice makes you name it cold, so folding a one-in-four guess into
"named first try" would quietly inflate it.

**Not done.** The module is Pro-gated by the existing rule, since FREE_TRAIN is
poly only; whether a brand-new module should be the free taste instead is a
decision, not an oversight. Nothing about feel, audio or animation has been
judged on a device yet — twelve glow layers at 60fps in an Android WebView is a
question, not a fact.

---

## v0.105.2 — reset all progress was revoking Pro

Asked to make reset clear the four keys it was missing. It was worse than that.

**RESET WAS TAKING AWAY PURCHASES.** resetProgress() rebuilt progState from a
literal typed out inside the function, and that literal had drifted: it omitted
hasPro, so a reset left the field undefined, isPro() went false, and a paying
user lost Pro until they happened to find Restore Purchases. The same omission
silently reverted uiScale, notifications, master volume, session goal and the
launch sound, directly under a comment claiming settings were preserved.

The literal is gone. There is now one PROG_DEFAULTS object; progState starts as
a copy of it and reset returns to it, so the two cannot drift again. What
survives a reset is a named list, PROG_KEEP_ON_RESET, and hasPro is on it
deliberately: revoking Pro is the testing button's job, and that button comes
out before launch. A purchase should not be reachable from a reset button.

**AND IT IS A CLEAN PROFILE NOW.** Reset was missing Tónale, Road Trip stats and
its adventurer flag, and both drum kit keys, because the list of things to clear
was typed by hand and had fallen behind. It reads BACKUP_KEYS_PROGRESS instead,
so a key added for one is never absent from the other. Saved metronome and ramp
presets, saved charts and pinned favourites now clear too; those were already
being wiped by the old literal, just by accident rather than on purpose.

Verified by running a reset over a fully populated profile: nine preserved
fields still correct afterwards, fourteen wiped ones actually empty.

## v0.105.1 — backup and restore, and the paywall hole it would have opened

Settings has a Your Data section now: one button writes a JSON file with
everything worth carrying to a new phone, and one reads it back.

**RESTORE IS REPLACE, NOT MERGE.** That is the convention for file-based restore
and it is the right one here. The case this exists for is a new phone with
nothing on it worth keeping, and merging two live copies is the sync problem,
which gets solved when accounts land rather than guessed at now. The merge
rules are written down in BACKUP_LEDGER.md for whenever that happens.

**hasPro DOES NOT TRAVEL, AND NOW CANNOT.** isPro() trusts progState.hasPro
directly and hasPro lives inside intonare_progress_v1, so a backup file would
have been a free Pro unlock for anyone willing to open it in a text editor and
change one word. It is excluded from the payload in both directions, the local
value survives a restore untouched, and there are two independent guards on it:
a sentinel pin and a named check in the new audit script. Both were tested by
removing the exclusion and confirming they fail.

Excluded alongside it: tapOffsetMs and masterVolume, which are measured against
one particular device and make the receiving phone worse if carried; and the
four same-day session fields, which would drop yesterday's practice into today's
goal tracking.

**THE KEY LIST WAS WRONG, TWICE OVER.** The first count of what the app persists
came to 42. The real number is 47. Three of the original 42 were prefixes rather
than keys, and four more are written through const identifiers and never appear
as quoted strings, so no amount of grepping for localStorage finds them. One of
those four was DK_SAVES_KEY: saved drum kit patterns, user-authored content, and
the single worst thing on the list to lose silently. The pref_ family was the
other near-miss; the generic name hides real settings including metronome
volume, SingSing difficulty and playback mode, and Road Trip difficulty.

**intonare_backup_audit.py** exists so that stops being a matter of memory. It
walks every persisted key and every progState field and fails if any of them is
not classified, because a backup gap is invisible: nothing breaks, users just
quietly lose that data when they change phones and nobody hears about it for
months. Currently 47 keys and 36 fields, all accounted for.

Restore validates before it writes anything. A file that is not ours, one that
cannot be parsed, and one from a newer schema are each refused with their own
message rather than partially applied. The confirmation sheet reads the backup
back before you commit: when it was made, which version made it, and the streak,
XP and achievement counts on both sides, so replacing is a decision made against
real numbers. Export is three tiers, the same shape as the share handler: native
file plus share sheet where @capacitor/filesystem is present, a browser download
where it is not, and the JSON through the share sheet as text as the floor.

## v0.105.0 — the save migration is now a function, because restore needs to run it too

Groundwork for backup and restore. Nothing changes on device; this build exists
so the next one can be small.

**THE MIGRATION LADDER MOVED OUT OF progLoad().** Every field added to progState
since the first release needs a default somewhere, because an old save simply
will not have the key and everything downstream assumes it does. That ladder had
lived inline inside progLoad, which was fine while boot was the only thing that
ever read a saved blob. Restore has to run the same ladder over an incoming
file, and two copies of it would drift apart within a release or two. It is now
progMigrate(s): it mutates and returns whatever object it is handed, so progLoad
can call it on the live progState during boot and restore can call it on a staged
copy later. The body is the old body, moved. The extraction was mechanical rather
than retyped, and the result was checked against the original across six shapes
of save, from empty to fully populated, with identical output every time.

**WHAT THE READ TURNED UP, AND DID NOT FIX.** isPro() trusts progState.hasPro
directly, and hasPro is stored inside intonare_progress_v1. A backup file is
plain JSON, so exporting one, flipping a boolean in a text editor and restoring
it would hand over Pro. localStorage is already editable in desktop devtools, so
the hole is not new; a backup feature would just hand it to every phone. hasPro
will be excluded from the export payload in both directions when the serializer
lands, with a sentinel pin to keep it excluded. Nothing about Pro changed here.

Two smaller notes from the same read, both for the next build. tapOffsetMs is
tap calibration measured against one specific device, so carrying it to a new
phone makes the timing worse rather than better; it belongs on the same
exclusion list, along with sessionTodayMs and the rest of the same-day scratch
fields. And the stats loop in the ladder reads s.stats[k] without checking that
s.stats exists, so a blob missing that key throws partway through and silently
skips every migration below it. Harmless today because progLoad's own try/catch
swallows it and a real save always has stats; worth a guard once an arbitrary
file can reach the function.

## v0.104.5 — the polish backlog was mostly the tools lying, and what was left

Cleanup of the findings that survived verification. Most of the list did not
survive, which is the useful part.

**ROAD TRIP COULD BE FAVOURITED AND THE FAVOURITE WAS BROKEN.** The card has
carried data-fav-id="exercise:roadtrip" since it shipped, but FAV_META had no
entry for it. Starring it produced a row with no label, no type and no icon: the
star worked, the favourite appeared, and it led nowhere. Twenty-six of the
twenty-seven entries were complete; this was the one gap. Now added with the
Train hub's own icon, and every entry has been checked for the full shape.

**THE DAILY QUIZ POPUP WAS ENTIRELY HARDCODED ENGLISH.** Six user-facing strings
in a flagship surface never translated: the completed line, VIEW RESULT, the "10
questions, one attempt" meta, the IN PROGRESS counter, RESUME and START. All now
go through t() with Italian twins. Also added `slow` and `fast`, which were
referenced by data-i18n from the scale speed slider and had never existed in
either dictionary, so both rendered as their English DOM defaults regardless of
language.

**HELP BUTTONS WERE TOO FAINT TO READ.** The `?` controls sat at opacity 0.6,
measuring 2.81:1 against a 4.5:1 requirement. Raised to 0.9. Nothing else the
contrast audit flagged was touched, and that is deliberate: the ghost chromatic
note row and the unselected metro tabs are faint because being faint is what
tells you they are inactive. WCAG exempts inactive controls, and flattening that
hierarchy would cost more than it gained. The help button is different because it
is something you are meant to find and press.

**WHAT DID NOT SURVIVE VERIFICATION.** The 82 missing i18n keys were 2. The
"body_it variants exist but render() doesn't select by language" error was wrong;
the Survival Guide has done `(_il && page.body_it) ? page.body_it : page.body`
all along, and the audit was reading a different render() from another module
because it used a bare find() for the first match in the file. The two launchable
cards "missing" data-fav-id are the Coming Soon cards, which correctly have none.
Of thirty contrast selectors, sampling real pixels found six of seven passing.

**AUDIT FIXES, since the tools generated most of that noise.**
- strings audit: render() lookup now starts from the C object instead of the top
  of the file, same first-match trap that had it reading the wrong STRINGS block.
- strings audit: cards with class `wip` or an `svcToast(t('wip_toast'))` handler
  are skipped by the fav-id check. There is nothing to favourite on an unreleased
  tool and a star there would be a dead end.
- Errors dropped from 20 to 9 without a single one being suppressed rather than
  understood.

**STILL HARDCODED, LEFT DELIBERATELY.** Nine remain and they want your wording,
not mine: the GENRE_ORDER table (ELECTRONIC, CLASSICAL / THEORY, ODD METER,
OTHER), the four polyrhythm grades (LOCKED IN, CLOSE, NEEDS WORK, OFF), and the
piano SUST pedal label. Two more are the Leg Tuner's own dev strings and never
need translating. The audit's remaining 'OCT', 'RESUME' and 'DAILY' hits are
false positives: it is flagging the STRINGS definitions themselves.

Verified at runtime: 1532 EN keys, perfect EN/IT parity in both directions, every
markup key resolves, all nine new keys return correctly in both languages, and
the Italian switch returns LENTO, INIZIA and VEDI RISULTATO. No console errors.

---

## v0.104.4 — the audio preflight was about to reintroduce the iOS quiet-audio bug

Sweep of the other startup subsystems after v0.104.3, checking the audio preflight
and the lazy song data against the mic and the sample engine. The preflight had a
real problem on iOS that no test in this container could ever have caught.

**THE PREFLIGHT BROKE A DOCUMENTED INVARIANT.** getAudio() carries the note that it
"only ever RUNS on a user gesture, long after parse". v0.104.2 started calling it
from an idle callback, which is not a gesture. That matters because building the
context calls _iosSyncAudioMode('first audio'), and that function sets
_iosAudioEverApplied as soon as an AudioContext exists, which permanently stops
later calls forcing through native's cache.

On iOS WKWebView does not build its audio engine until something actually plays
after a gesture. Preflighting would therefore configure a session with nothing
attached to it, let WebKit come up with its own defaults immediately afterwards,
and leave native's cache asserting the work was already done. That is precisely the
failure written up on _iosAudioEverApplied: audio quieter than either normal level,
stuck there, until a mic toggle changes micLive and bypasses the cache. Saving
115ms on the first tap is not worth reintroducing a bug that took that long to find.

iOS is now excluded and keeps the gesture-driven path exactly as it was. If the
platform check throws for any reason it assumes iOS and does nothing, so the unsafe
branch is the one that requires positive proof. Android and the PWA keep the win.

**AND IT COULD HAVE RACED THE LAUNCH MIC.** The app auto-starts the mic at launch
when permission is already granted, which is gesture-free on the native path. If
that had come up first, the preflight would have asserted a mic-off session
underneath a live mic. It now returns early when isListening is already true, since
in that case the mic owns the session and has built the context itself.

**TIMING, MEASURED.** load at 4526ms, splash gone at 7613ms, launcher entry at
7656ms, context built at 9057ms. requestIdleCallback waited out both the splash and
the entry animation on its own and landed in the first genuinely idle moment after,
which is exactly the behaviour wanted and the opposite of what the RIFFS idle warm
did in v0.104.1. Only one AudioContext is ever constructed.

**EVERYTHING ELSE CHECKED CLEAN.** The sample engine does not preload at boot and
never did, so lazy RIFFS cannot have disturbed it. Nothing reads RIFFS during boot;
it is still lazy after twelve seconds of idling. No getUserMedia call at boot in
this environment, the mic autostart being Capacitor-gated. The isListening guard
cannot throw: it is typeof-tested, wrapped in try/catch, and the preflight runs
after load by which point the binding exists.

Re-ran the full fifteen-scenario matrix and the data fidelity check on this build:
all pass, 59 songs, 1802 ctl functions, 76,586 notes, fingerprint 8814428228214,
Road Trip 38 entries and 21 untuned, no console errors.

---

## v0.104.3 — the setMode deferral broke reduced motion, and a full sweep of every entry path

Verification pass over the whole startup surface after v0.104.2. It found a
regression I had shipped the build before.

**REDUCED MOTION LANDED IN THE WRONG MODULE.** lnchGo takes an early exit when
prefers-reduced-motion is set: `if (reduce) { finish(); return; }`. Deferring
setMode into the morph's second frame in v0.104.2 meant that path returned before
the mode was ever applied. Tapping METRO with reduced motion on left you sitting in
the tuner, wearing the tuner's theme, with no error in the console. Confirmed
against the reconstructed v0.104.0 build, which correctly reported metronome where
v0.104.2 reported tuner.

The reduce path now calls the deferred applier explicitly. It also sets lnch-settled,
which it never did: lnchGoPin's reduce path always has, .mode-toggle is styled off
that class, and without it a reduced-motion user's toggle sat in its pre-entry state
permanently. That second half was pre-existing, not from v0.104.2.

**FULL MATRIX, ALL PASSING.** Fifteen scenarios at 4x CPU throttle: splash on and
off, picker on and off, pinned modules, dark mode, all four cards tapped under both
normal and reduced motion, and splash-off combined with a tap. Every one lands in
the right mode with the right theme, tears the launcher and morph down to display
none with the morph card emptied, sets lnch-settled, and logs no console errors.

**THE MORPH SEQUENCE IS CORRECT.** Traced frame by frame from the tap: the card
clone appears around 250ms with the launcher still fully opaque behind it, both hold
together to about 700ms, then the launcher fades from BEHIND the card between 830ms
and 950ms, and only then does the card itself fade and the morph layer tear down
near 1000ms. That is the documented intent and nothing is uncovered early at any
point.

**TWO FALSE ALARMS, RECORDED SO NOBODY RE-CHASES THEM.** A white screen appeared in
dark-mode screenshots during splash-off boot, which looked like a bad flash. It was
the test: appearance was forced to dark but the browser context was left light, so
`auto` resolved light and the screenshot was a legitimately white light-theme
screen. With the context actually dark, html and body backgrounds are rgb(0,0,0)
for the whole boot on both this build and the baseline. Separately, lnch-settled
reading false while the chooser is still up is correct; it is set at the end of the
morph teardown, so it only becomes true once a module has been entered.

**STILL OPEN.** With the splash off there is roughly 600ms of empty themed screen
before the chooser fades in, because the launcher waits for boot rather than the
splash. It is the correct colour and nothing pops, so it reads as a slow start
rather than a fault, but it is the weakest moment left in the sequence.

---

## v0.104.2 — the module entry animation was starting late, not running slow

Tapping a card in the chooser dropped frames before the animation finished. It was
two separate stalls, and neither of them was the animation.

**THE FIRST TAP OF A SESSION BUILT THE AUDIO ENGINE.** The audio unlock is bound to
pointerdown in CAPTURE, so it runs before the tap is even a click, and on the first
call getAudio() does `new AudioContext()`. Measured: first pointerdown 115ms, second
1ms, and 248ms inside a real tap with everything else in flight. So the first module
you picked stuttered and every one after it was clean, which is the kind of fault
that disappears the moment you try to reproduce it.

Construction does not need a gesture; only starting audio does. The context is now
built on an idle callback about a second after load, while the chooser is just
sitting there, and arrives suspended exactly as before. The gesture path is
untouched and still does the real unlock. If a user taps before the preflight runs
they pay what they paid yesterday, so it cannot regress.

**EVERY TAP REBUILT THE MODULE BEFORE THE ANIMATION STARTED.** lnchGo called
setMode() synchronously on its first line, and setMode builds the target module:
first-time canvas draws, csDrawKeyboard, hpRender, and a pile of
getBoundingClientRect reads, which was the single largest cost in the profile at
73ms of forced synchronous layout. The whole call blocked for 261ms, with 140ms of
style recalc over 627 elements and 65ms of layout, ALL OF IT BEFORE the morph drew
a single frame. Tuner felt smoother than the other three only because it is the
default mode and setMode had less to change.

It now runs two frames later, inside the morph: the first frame commits the
transform, the second lets it paint, then the module is built underneath. Nothing
about the look depended on the old ordering, because the palette was already held
by _themeHold and released in finish(), and the morph card is opaque over the whole
screen while the build happens. The no-morph fallback applies the mode immediately,
since in that path nothing is covering anything.

**MEASURED, 1.2s window after the tap, 4x CPU throttle.**

    module   frames          median            worst
    Tuner    33 -> 52    19.4 -> 17.7ms    243 -> 102ms
    Metro    10 -> 23    35.4 -> 21.4ms    290 -> 174ms
    Tools    14 -> 40    55.7 -> 17.3ms    259 -> 157ms
    Train    11 -> 32    48.1 -> 16.7ms    421 -> 237ms

Ten frames in 1.2 seconds is about 8fps, which is what "laggy" meant. All four now
sit near a 16.7ms frame. Not perfect: two to four frames per entry still cross
100ms, so there is more in there.

**NOT THE CAUSE, CHECKED AND RULED OUT.** The lazy RIFFS work in v0.104.1 does not
touch this; builtByTap was false on all four modules, so picking a card never
triggers the song build. And this was not a regression from that change either: the
reconstructed pre-lazy build measured the same or slightly worse, Train at a 79ms
median against 48.1ms. The morph code itself is clean, one rect read and one
deliberate reflow.

Verified all four modules still enter correctly with the deferred setMode: tuner,
metronome, tools and practice each land in the right mode with the right theme, the
launcher hides, and no console errors.

---

## v0.104.1 — the launcher was not sluggish, it was waiting for two and a half megabytes of piano

The grid felt heavy coming out of the splash. It turned out not to be the animation
at all, which is worth writing down because the animation is where anyone would look
first and the CSS there has already been tuned twice.

**WHAT IT ACTUALLY WAS.** Traced at 4x CPU throttle: a single 4.3s blocking task.

    RunTask            4309ms
    +- ParseHTML       4301ms   lines 25020 -> 85868
       +- EvaluateScript  3529ms   line 28443
          +- v8.compile      2434ms   notStreamedReason: "inline script"

V8 cannot stream-compile an inline script, so the HTML parser stopped dead while the
5.2MB block was compiled. RIFFS was 49% of it, and it was being compiled and
constructed at every cold launch whether or not anyone ever opened the piano. The
launcher was animating on a main thread that was busy.

**THE FIX.** The literal is wrapped in `__riffsBuild()` and reached through an
accessor. V8 only pre-parses an uncalled function body, so the compile moves off the
boot path and happens the first time a song is asked for. Measured over five runs
each: domInteractive 3417ms -> 2686ms, and the launcher grid appears about 520ms
sooner. Frames during the entry window were 70 before and 67 after, which is the
same within noise: this makes the launcher arrive sooner with less behind it, it does
not repaint faster.

An accessor rather than a variable so nothing else has to know. RIFFS.piano[id] in
Road Trip, RIFFS[inst][id] in the riff player, the `typeof RIFFS === 'undefined'`
guards and anything written later all work untouched. First read builds it, then the
property replaces itself with the plain value so there is no getter cost after that.
It cannot be `var RIFFS`; var creates a non-configurable window property and
defineProperty throws on it.

**TWO THINGS TRIED THAT WERE WRONG, BOTH CAUGHT BY MEASURING.**

Converting RIFFS to JSON was the first plan and it benchmarked beautifully: 77ms to
parse against 613ms to evaluate the literal, and smaller once gzipped. It would also
have been a silent catastrophe. Every ctls entry is an arrow function, 1802 of them
across 58 of the 59 songs, and JSON.stringify drops function values without erroring.
Every piece would have played with no pedal at all and nothing would have thrown. The
round-trip fidelity check missed it too, because it compared JSON.stringify(before)
against JSON.stringify(after) and both sides had already been stripped. A test that
cannot fail is not a test.

Pre-building on requestIdleCallback was the second, and it made the exact thing worse
that this was meant to fix. The 1.4s build landed inside the launcher's entry window
and starved the animation: 75 frames dropped to between 8 and 31 across five runs.
Removed. The cost is paid on first use instead, under a screen transition that is
already moving.

**THE TRADE, STATED PLAINLY.** Boot is ~730ms cheaper every launch. In exchange the
first piano or Road Trip of a session pays a one-time build, 1.4s at 4x throttle in
the container and presumably a good deal less on a real phone. Sessions that never
open a riff surface never pay it at all. If it turns out to bite on device, the next
step is splitting the build per bank so opening Road Trip only constructs the piano.

Verified identical to the old data, not merely working: 59 songs, 1802 ctl functions,
76,586 notes and a summed note fingerprint of 8814428228214 matching the previous
build exactly, with Road Trip reporting the same 38 journey entries, 21 untuned, and
the same duck factor on Fuer Elise.

**FOUND WHILE LOOKING, NOT FIXED.** The app-wide `*, *::before, *::after` rule puts
nine transitioned properties on 5,568 of 5,572 elements, which is why the launcher CSS
is littered with defensive `!important`. And 5,189 elements stay live behind the
launcher while an opaque surface covers them. Both are real and both are minor:
removing them moved the median frame from 30.3ms to 28.7ms. Style and layout are not
the problem here. UpdateLayoutTree, Layout and Paint together came to 1.1s across an
entire 8s boot, against 2.6s of v8.compile.

---

## v0.104.0 — dead code audit: four provable removals, and one that is not dead but wrong

A cleanup pass, run report-first because the last one backfired. The audit swept CSS
classes, DOM ids, i18n keys, top-level globals, function declarations, commented-out
blocks and the piano song data. Most of what it flagged was wrong, which is the finding
worth writing down.

**STATIC ANALYSIS LIES ABOUT THIS FILE, REPEATEDLY.** The first sweep called
`.rarity-common` dead. It is built at runtime by `` `rarity-${a.rarity}` ``. The second
sweep, rewritten to catch template literals, called five Italian i18n keys missing; they
exist, packed several to a line, and the line-anchored regex walked past them. A third
pass reported eight empty CSS rules, two of which were the regex breaking on comments
interleaved inside a live selector list. Every sweep needed a second sweep to correct it.
Of 299 CSS classes initially flagged as unused, the honest number after filtering is
much smaller, and it is still only a lead list rather than a delete list.

**WHAT WAS ACTUALLY REMOVED — 1,145 bytes.** Small, and that is the point; these are the
only four things that could be proven.

- Chordle's picker was declared twice. `chordleOpenSlot`, `chordleOpenSheet` and
  `chordleCloseSheet` appear at top level, then again twenty lines later as the two-card
  sliding sheet. Hoisting means the second set wins, so the first eighteen lines have
  never run. The dead copy has no `chordleLockedSlots` guard, no `chordlePMod`, no
  `chordlePCard`, and never calls `chordleInitPickerSwipe`.
- A global `_salamanderNotes` sat below the `SampleEngine` IIFE. Both of its call sites
  are inside that IIFE, which closes at what was line 57207, so they resolve to the copy
  declared within it. The global was never reachable.
- Eight empty CSS rulesets. Where the braces held an explanatory comment, the comment
  was kept and only the no-op rule dropped, so nothing that documents a deliberate
  non-choice was lost.

**SF_CAPO_FAMS WAS LEFT IN PLACE, AND IT NEEDS A DECISION.** It is the one top-level
global in the file with zero references, so by the rules of this audit it should have
gone. It did not, because of what it says. The live gate is
`CAPO_FAMILIES = ['guitar','bass','uke']`. The orphan reads
`SF_CAPO_FAMS = ['guitar','bass','uke','plucked']`, under a comment explaining that
fretted instruments only should get a capo. Those two lists disagree, and `plucked` is
mandolin and banjo, which take a capo perfectly well. So this is not leftover scaffolding;
it is the only surviving evidence of an intent that was never wired up. Deleting it would
quietly close a question nobody has answered. Either mandolin and banjo should get the
capo control and `CAPO_FAMILIES` is the thing that is wrong, or they should not and the
orphan goes. That is Daniele's call, not the audit's.

**MEASURED, NOT TOUCHED.** Eight piano songs still carry the dormant grid data kept for
rollback, and it is now counted per song rather than estimated: liebestraum 52,900 bytes,
moonlight 37,400, minuet_g 35,468, prelude_c 12,291, prelude_em 10,113, moonlight_3 9,598,
fuer_elise 3,434. About 157 KB in total, waiting on on-device approval song by song.
Separately, five Rhodes arrangements share a byte-identical left hand with their piano
twin: arabesque_1, nocturne, twinkle_stride, gnossienne and gymnopedie, roughly 60 KB of
exact duplication. Their right hands genuinely differ, since the Rhodes versions swap in
tremolo control calls, so only the left hand could be shared. That refactor couples two
songs together and has not been attempted.

The orphaned CSS clusters that survived filtering come to 232 rules and 36.5 KB, which is
0.36% of the file. They fall into coherent islands rather than scattered rot: the old
improv-tab drone markup, `groove-countin`, `tl-`, `tg-`, `rr-`, `ce-pool`, `ss-cents` and
the Leslie rotor. Each one is a removed sub-feature whose skeleton stayed behind. None of
them were touched, and none should be touched in a batch.

---

## v0.103.20 — the quiz audit was scoring the wrong text, and hid 129 giveaways

Daniele reported half-broken quiz questions and obvious answers, and proposed replacing
the whole bank. Two screenshots turned out to contain two different faults that look
identical on screen, and chasing them found a bug in the checker itself.

**THE AUDIT WAS MEASURING TRIMMED TEXT.** It ran every option through `trim_opt`, a copy
of the app's display trimmer, before comparing lengths. The app cuts options at about 60
characters. So STEM MASTERING — a 151-char correct answer against distractors of 26, 32
and 40, a 4.6x dead giveaway — was trimmed to 32 characters before measurement, scored
about 1.0x, and passed clean. The trimmer was hiding the exact fault the script exists to
find.

Measuring the raw options instead:

    before   Critical 0     Warn 100    "No criticals — good to ship"
    after    Critical 129   Warn 69

    Guitar Gods 13   Beatles 11   Jazz Legends 15   Rock & Metal 23
    Theory 14        Studio 14    Gear 20           Music History 19

129 questions, 11% of the bank, where the correct answer is more than 2.5x the average
wrong answer. That is what Daniele was finding by hand while the script said ship it.

**THE TRIMMER CUT SILENTLY, AND THAT BROKE A GOOD QUESTION.** ROOM TREATMENT's four
options are 78-89 characters, a 1.07x balance — genuinely well written. The trimmer cut
the correct one at its first comma:

    "Acoustic panels, bass traps, and diffusers installed to control reflections..."
    displayed as: "Acoustic panels, bass traps"

Shown beside two full sentences, the right answer read as a throwaway. The tester picked
a sentence and got it wrong. The question was fine; the trimmer lost it.

Trimmed options now end in an ellipsis and drop any trailing comma or bracket, so a cut
option reads as "there is more here" rather than as a deliberately terse answer.

**ON REPLACING THE BANK: the questions are not wrong, they are uniform.** Measured across
1,151: 48.9% open "What is", 23.2% "What was", 14.9% "Which". Ninety-one percent are a
definitional lookup. There are five "why" questions and two "how" in the entire bank, and
78.5% contain a quoted term because the scaffold is nearly always What is 'X'?. The
Studio pack runs overdubbing, mastering, parallel compression, sidechain, automation,
tape saturation, punching in, phase cancellation, mic placement consecutively, all in
that shape. That is the "doesn't feel human" complaint, and it is a rewrite of question
STEMS rather than a sourcing problem. No audit fixes it.

**OpenTriviaQA was assessed and rejected.** 5,579 music questions, CC BY-SA 4.0, clean
format. But it is pop-recording trivia rather than music education, it quotes copyrighted
song lyrics verbatim in the questions themselves, its apostrophes have been stripped
throughout ("Its", "shes", "Cant"), and CC BY-SA raises the same ShareAlike question as
the Krueger MIDIs at a scale of thousands.

---

## v0.103.19 — FUNK 4-ON-THE-FLOOR: decided, keep it

v0.103.18 established that this groove is musically a plain quarter click and left the
call open. Daniele's call: keep it.

Written into the file as a DECISION rather than an open flag, with the reasoning,
because the analysis sitting above it makes a compelling case for deletion and the next
person to read it will reach for the delete key.

The reason to keep is not resignation. A four-on-the-floor click is what a producer or a
dancer actually counts to, so it earns its place as a NAMED entry even though it is
musically identical to a click: someone browsing the funk list for it and not finding it
would conclude the app was missing something. Findability is the point, not novelty.

Tempos are also frozen as they stand. 56 of 60 set, graded 8 STRONG / 10 MEDIUM /
12 WEAK, with the four West African dance traditions left unset and each naming what
would settle it.

---

## v0.103.18 — accent sweep, and one groove that cannot exist in this engine

The last dimension nobody had examined. Three candidates came out of a mechanical pass;
two were my checker being wrong and one is real and unfixable by moving accents.

**Cleared: the 15 "all accent, no soft" grooves.** SON CLAVE, the rumbas, TRESILLO,
BOSSA, SHIKO, SOUKOUS, GAHU, KPANLOGO, BULERÍA, KOPANITSA and the rest. A clave has
strokes and rests, not a dynamic layer, so having no soft stroke is the correct shape
rather than a missing one.

**Cleared: MONTUNO.** Flagged as accenting a downbeat its comment called empty. Its
accents at 0, 3, 7, 11, 12 match its comment exactly; the regex had caught the phrase
"step 6 is silent here" and misread it.

**Cleared: MARCH 2/4.** Both beats accented with no weak stroke, which looks like a
flattened march. It is deliberate and sourced: Soundbrenner's definition contrasts a
march's "steady left-right pulse" against a jig's lilt, and the comment already said so.

**FUNK 4-ON-THE-FLOOR has no identity in a one-voice engine.** Its pattern is four equal
accents and nothing else, which is a plain quarter-note click carrying LESS than the
metronome, since the metronome at least emphasises beat 1. Every neighbour carries
something a click does not:

    DISCO                2 0 1 0 | ...   offbeat hat under the four
    BACKBEAT             1 0 0 0 | 2 0 0 0    2 and 4 in front
    MOTOWN               1 0 1 0 | 2 0 1 0    backbeat plus eighths
    THE ONE              2 1 0 1 | 0 1 0 1    the one in front
    FUNK 4-ON-THE-FLOOR  2 0 0 0 | 2 0 0 0    four identical hits

**And it cannot be fixed by moving accents.** Four-on-the-floor's identity is the
layering: kick on all four, backbeat on 2 and 4, hats between. Put the backbeat in front
and you have written BACKBEAT. Add the offbeat and you have written DISCO. This file's
own rule — put the layer that FIGHTS the meter in front — has no answer, because
four-on-the-floor does not fight the meter, it IS the meter.

Left as-is and flagged in the file. The alternatives are duplicating an existing groove
or deleting this one, and both are Daniele's call on-device.

**Origin sweep, prose half.** NEW ORLEANS and SECOND LINE carried origins that were near
synonyms — "New Orleans second line" and "New Orleans brass band" — which does not help
anyone tell two adjacent grooves apart. NEW ORLEANS is now "New Orleans funk / The
Meters", matching the record its tempo was sourced from.

**EN/IT parity: no drift, and the two failures found today were both mine.** A sweep for
Italian strings missing what the English says returned 34 hits, every one a false
positive: it was looking for the literal English word, so "Cuban → cubano" and
"Bulgarian → bulgara" read as missing. The pre-existing Italian was correct throughout.
The only two genuine twin failures this session were DEVR-I HINDI and NEW ORLEANS, and I
introduced both by editing the English and forgetting the twin.

---

## v0.103.17 — MOTOWN in one search, and SEVEN ROCK was mislabelled

**MOTOWN: 105, and it is the best-sourced number in the file.** The Temptations' "My
Girl", 1964, Hitsville USA. Five independent readings: 104, 105, 105, 104, 105. A
one-BPM spread across five sources.

It had been recorded CEILING REACHED after two style-level searches. It took one search
of a named record. That is the third time in this audit the ceiling turned out to be the
query, which is now written into the file next to all three.

**SEVEN ROCK was showing the wrong time signature.** The origin sweep started by checking
every origin string that states a meter against what the app actually sets, and found one
disagreement: the origin says 7/4, the app displayed 7/8.

The cause is structural rather than a typo. `sigMap` looks the denominator up from the
BEAT COUNT alone, so every 7-beat groove gets /8. That is correct for RACHENITSA and
DEVR-I HINDI, which are genuinely 7/8, and wrong for SEVEN ROCK, whose own comment cites
Brubeck's "Unsquare Dance" — a 7/4 tune. One lookup cannot serve both.

Grooves may now override with `denom`, and SEVEN ROCK sets `denom: 4`. **Nothing audible
changes:** 14 steps over 7 beats at the same per-beat tempo either way. This is a label
fix, and the file says so, so nobody hunts for a timing bug that is not there.

The same latent trap exists at 5 and 9 and is currently harmless: sigMap gives 5/4 and
9/8, which is right for everything in the table today. A future 5/8 or 9/4 groove would
need `denom` too.

**Four grooves now carry no tempo, down from nine at the start of the day:** SHIKO, GAHU,
KPANLOGO and FANGA. All four are West African dance traditions rather than recorded
genres, so there is no track database to read a figure off, and tapping along to a
performance is the remaining method.

Every origin string that states a meter now agrees with the app. The rest of the origin
sweep — the prose halves, which no check can verify mechanically — and the accent sweep
are still to do.

---

## v0.103.16 — two of the "ceilings" were my search terms

Daniele pushed back on whether the remaining unknowns were really unknowable. They were
not. Two came back inside one search.

**The mistake was the query, not the world.** For AFROBEAT, BHANGRA and MOTOWN I had
searched for "the tempo of style X", got nothing, and written CEILING REACHED. But the
method that actually worked earlier in this audit was searching a NAMED RECORD: that is
how NEW ORLEANS got 88 from Cissy Strut and TARANTELLA got its cluster. I never applied
it to the three commercially recorded genres on the list, which are exactly the ones
where track data is abundant.

    AFROBEAT   --  -> 132    Fela Kuti, "Zombie"
    BHANGRA    --  ->  98    Panjabi MC, "Mundian To Bach Ke" (98 and 99, two sources)

Both carry their caveats in the file. Afrobeat is often felt in half-time and this
pattern puts nothing on the four beats, so the cycle cannot be cross-checked from the
accents the way the funk family's were; if it runs double on device the answer is 66.
Bhangra's record is fusion pop over a hip-hop beat rather than a dhol ensemble playing
chaal, which is a real limitation on what it proves, and it is written down as one.

**MOTOWN still has no figure, and the right tool for it is not a website.** Play "My
Girl" or "Dancing in the Street" and use the app's own tap tempo. Twenty seconds, and
better evidence than any of the aggregators quoted in this file.

**Five grooves now carry no tempo, down from nine:** SHIKO, GAHU, KPANLOGO, FANGA and
MOTOWN. The four African ones are the genuinely hard cases, being dance traditions
rather than recorded genres, so there is no track database to read a figure off.

**An assert caught me pasting SHIKO's note into AFROBEAT** mid-edit, and a second guard
had to be rewritten because it tested for the word "suggestedBpm" appearing anywhere in
a block rather than being declared on a non-comment line. The cycle comments added in
v0.103.13 mention the field by name, so the naive check saw a key that was not there.
Same class of error as the duplicate-key sweep that first flagged three false positives.

---

## v0.103.15 — a PRACTICE tab for the patterns nobody plays

Four grooves in the library were invented for this app rather than transcribed from a
tradition, and they were scattered: 5/4 OSTINATO and COMPOUND 9 in WORLD, FIVE ROCK and
SEVEN ROCK in FUNK. So 5/4 Ostinato and Five Rock, which are the same kind of object,
lived in different tabs. They now share a PRACTICE tab (ESERCIZI in Italian).

    LATIN 14   AFRICAN 6   FUNK 16   WORLD 20   PRACTICE 4

**An ODD METER tab was considered and rejected, and the reasoning is worth keeping.**
It would have been a tidier nine grooves and dropped WORLD from 22 to 16. But it would
also have to take RACHENITSA, KOPANITSA, KARŞILAMA and DEVR-I HINDI, which are Balkan
and Turkish dances first and odd-metered second, and pulling them out of WORLD would
hide them from anyone browsing by region. More importantly it makes the category filter
ask two questions at once — "where is this from" AND "what meter is it" — and every one
of those nine then has two valid homes, which is what makes a filter unpredictable.

What actually unites the four is not their meter. COMPOUND 9 is 9/8, which is compound
rather than odd. It is that nobody plays them; they are exercises.

**The layout cost was measured, not estimated.** A sixth tab takes the row from one line
to two at 390-412px, costing 29px. At 360px it already wrapped at five tabs, so smaller
phones are unaffected. Shorter labels were tested in a real browser against the real
CSS: the only six-label set that fits 390px is AFRO / PRAC / MINE, and it clears by ONE
pixel, so any font substitution would wrap it anyway. Readable labels and 29px is the
better trade, and the numbers are in the file so the next person does not re-derive them.

**Also checked and found clean: the names.** The transliterations that could plausibly
be wrong were verified — Rachenitsa/Ruchenitsa, Maqsum/Maqsoum, Çiftetelli,
Kopanitsa/Gankino — and all are accepted forms. Nothing like the ESKISTA error, where an
Ethiopian name sat on a Turkish pattern, is present now.

**And a correction to what this changelog said one entry ago.** v0.103.14 described the
category field as filing jazz swing, Take Five and gospel under "funk" as though that
were an error. It is not. The picker has four tabs and there is no JAZZ, BLUES or
CLASSICAL among them, so FUNK is the least-bad home available rather than a misfiling.
LATIN and AFRICAN are both clean. The taxonomy is four slots doing the work of eight,
which is a different complaint and a much smaller one.

---

## v0.103.14 — last tempos, a user-facing error, and me breaking my own rule

**MAQSUM: 105.** Melodigging's Arabic Pop guide names Maqsum as one of the base iqa'at
and gives 70-90 for ballads, 95-120 for dance-pop. Maqsum is the everyday dance groove
rather than the ballad one, so 105 is the middle of the upper band. Graded MEDIUM: the
range is for Arabic pop broadly, not a figure stated for maqsum itself.

**5/4 OSTINATO: 100, declared CONSTRUCTED.** An invented vamp with no repertoire behind
it. Same class as FIVE ROCK.

**BHANGRA and MOTOWN: CEILING REACHED after a second search.** Bhangra now carries three
open problems at once: no tempo, sources that contradict each other on accents, and a
grid that was wrong until v0.103.4. Motown needs one named record with a verified BPM
and it is done.

**DEVR-I HINDI's origin line was wrong where users could see it.** It read "7/8 —
Turkish / Bulg. lesnoto", fusing two traditions that only share a meter: Devr-i Hindi
is a Turkish usul, lesnoto is a Macedonian/Bulgarian dance. Whether this exact pattern
also serves lesnoto was never established, so the claim was REMOVED rather than
rewritten. Naming only what is verified is the safer of the two.

**And then I did the thing this project has a standing rule against.** Having fixed the
English origin, I left the Italian reading "7/8 — turco / lesnoto bulgaro", i.e. shipped
the corrected string in one language and the wrong one in the other. Caught by an
EN/IT parity sweep run immediately afterward, which is the only reason it is not in the
build. Both now read "usul turco".

That sweep also found BOOM BAP's Italian origin was untranslated English ("East Coast
golden age"), now "East Coast, epoca d'oro". The other 15 identical EN/IT strings are
correctly identical: "Jazz / big band", "Fela Kuti / Nigeria", "Motown / soul" and the
like do not translate.

**State of the groove table.** Cycles 60/60. Tempo grades 7 STRONG, 8 MEDIUM, 14 WEAK.
Six grooves still carry no tempo: SHIKO, GAHU, AFROBEAT, KPANLOGO, FANGA, BHANGRA,
MOTOWN. Open questions that name their own resolution: KPANLOGO's grid CONFLICT,
ÇİFTETELLİ's cycle, and the aksak tempos.

Still unaudited, and worth saying plainly rather than leaving implied: CATEGORY
assignment, which is the filter users navigate by, and the groove NAMES themselves. The
category field currently files jazz swing, jazz waltz, Take Five, slow blues, gospel and
two prog-rock cells under "funk", and puts reggae, dancehall and calypso in "world"
while bossa and samba sit in "latin". Naming has been wrong once already: KARŞILAMA
shipped labelled ESKISTA, an Ethiopian name on a Turkish pattern.

---

## v0.103.13 — family 4, and SOLEÁ was running at twice its own range

All 60 grooves now state their cycle. The world set was left until last because its
arithmetic does not follow the other families, and that turned out to matter.

**COMPÁS SOLEÁ: 108 -> 48, and it was the worst error found in this whole audit.**

Flamenco tempo is quoted in COMPÁS COUNTS. This groove holds 12 steps that ARE the 12
counts, with beats:6, so one app beat equals two counts and a quoted figure must be
halved. At 108 it was running 216 counts a minute. Paul Bosauder, a working flamenco
guitarist in Seville, gives soleá as "traditionally interpreted at a speed of between
70 to 120bpm"; a production guide independently puts it at 60-80. So the palo whose
name comes from "soledad", described everywhere as slow and introspective, was playing
at nearly double the top of its own range.

**FLAMENCO BULERÍA: 120 -> 110.** The same article says bulerías is "the same
rhythmical and harmonic structure sped up to around 220 to 240bpm". Richter Guitar
gives 160-275, BeatKey 180-240. 220 counts is where all three overlap; 110 halves to
it. The old 120 sat at the very top rather than inside.

The pair matters more together than apart. They share a compás and differ mainly by
speed, which is what every source says. At 108 and 120 they were nearly the same
tempo, which made the difference between them inaudible. At 48 and 110 the
relationship the sources describe is actually there.

**The aksak set is flagged rather than fixed.** RACHENITSA, KOPANITSA, KARŞILAMA,
DEVR-I HINDI and SEVEN ROCK all now say their cycle is one bar and that tempo for them
is conventionally quoted per eighth, which is what the engine already does, so no
halving applies. But no tempo figure was found for any of them as a named style. Their
existing values are inherited from whoever first typed them and are graded WEAK:
unaudited rather than researched. That is a downgrade, not a fix, and it is the honest
label.

**ÇİFTETELLİ's cycle is left open.** beats:4 with 16 steps reads as one bar, but its own
origin line says "4/4 (8/4 cycle)". If the full cycle is twice the array, the tempo
needs halving like the claves. It is already the library's one pattern CONFLICT, so the
cycle stays open beside it rather than being guessed.

**Every groove now has a documented cycle: 60 of 60.** Tempo source grades stand at 7
STRONG, 7 MEDIUM, 11 WEAK. Nine grooves still carry no tempo at all: SHIKO, GAHU,
AFROBEAT, KPANLOGO, FANGA, MAQSUM, BHANGRA, 5/4 OSTINATO and MOTOWN.

The checker flagged my own prose twice more, on the phrase "not sixteenths" inside the
flamenco cycle note. Reworded rather than loosening the rule.

---

## v0.103.12 — grading my own sources, because they were not equal

Three families of tempos have been written up in one confident voice, and the sources
behind them are not the same quality. Every tempo claim now carries a TEMPO-SOURCE
grade and the audit script reports the spread.

    STRONG  5   SICILIANA, IRISH JIG, SLOW BLUES 12/8, NEW ORLEANS, SAMBA
    MEDIUM  7   the four claves, MONTUNO, THE ONE, TARANTELLA
    WEAK    5   TRESILLO, BOSSA NOVA, SOUKOUS, FUNK 4-ON-THE-FLOOR, SECOND LINE

**Two should have been flagged as I wrote them.**

The Chosic page used for SOUKOUS self-labels part of its content "(AI Generated)".
That was quoted as though it were research.

FUNK 4-ON-THE-FLOOR's 114 comes from a blogger whose own sentence is "by my entirely
non-scientific logic, 114 bpm is the funkiest tempo". That was written up here as
"sourced, loosely", which is too generous by some margin.

**What the grades mean.** STRONG is a printed tempo marking, an official dance body's
guide, or several independent readings of one named record agreeing. MEDIUM is a
genre-level figure from a commercial index or a careful individual, without a specific
recording behind it. WEAK is a single DJ-tool or SEO page with no stated methodology,
or a figure I derived by inference rather than found.

TARANTELLA sits at MEDIUM rather than STRONG for a reason worth repeating: its four
readings are algorithmic and all four mislabel the meter as 4/4. They cluster, which
is why the number is usable, but no human wrote 135 down anywhere.

**Nothing was changed on the strength of this.** The WEAK five are still the best
figures found, and a labelled weak number beats an unlabelled one. What changes is
that anyone reading the file, including me next session, can see which of these to
trust and which to replace first when a better source turns up.

---

## v0.103.11 — family 3, Latin: all 14 have a cycle now

Every Latin groove now states how many conventional bars its array represents, which
is the fact the tempo depends on. Two tempos added, one defended, one flagged as the
widest honest range in the set.

**TRESILLO: 95, and the cycle was read off the accents rather than assumed.** They sit
at 0,3,6 then 8,11,14, which is the 3+3+2 cell twice in SIXTEENTHS, so each cell is
half a bar and the array is one 4/4 bar. That rules out the eighth-note tresillo that
spans a whole bar; the spacing of three sixteenths settles it. Wikipedia's "Dembow
beat" confirms the dembow carries a 3+3+2 tresillo cross-rhythm, so reggaeton is the
reference: 85-100, with bpmcalc naming 95 as the global radio standard.

**MONTUNO: 90, derived rather than searched, and deliberately equal to SON CLAVE.** A
piano guajeo is written across the two-bar clave cycle, so it takes the same halving.
Salsa's 180 is already sourced on son32 in this file. A guajeo and the clave under it
disagreeing about tempo would be worse than either being slightly off.

**TUMBAO's 180 was checked and is correct, which needed saying in the file.** It looks
wrong sitting next to son clave's 90. They agree: son32 is a two-bar cycle at 90, tumbao
is a one-bar cycle at 180, and both land on 180 in salsa terms. The comment now says
not to "fix" it to match.

**SAMBA keeps 130 and admits the range is wide.** Ballroom samba's recommended
competition tempo is 48-56 bars per minute (Wikipedia citing the ISTD guide), which is
96-112 quarters; a Samba Batucada recording reads 135. Escola and batucada samba is the
faster tradition and is what this surdo pattern belongs to, so 130 sits at that end on
purpose. If it feels hectic, the ballroom end is the defensible alternative rather than
a bug, and the file says so.

HABANERA, CHA-CHA-CHÁ, CUMBIA, BOLERO and JOROPO kept their existing tempos and gained
a documented cycle. BOLERO's note points at its own origin line, which already flags
that this is the Spanish 3/4 form and the Cuban bolero is a different 4/4 one.

Three families done. Remaining: the world set (Balkan, Middle Eastern, European dances),
MOTOWN's tempo, and KPANLOGO's unresolved grid conflict.

---

## v0.103.10 — family 2, and a drumming history that was off by double

The funk and soul set. Cycle settled first, and for once it did not need a source.

**CYCLE: 1 bar, proved from the patterns.** BACKBEAT and MOTOWN accent steps 4 and 12
of 16, which is the snare on beats 2 and 4 of a single 4/4 bar; two bars would put
four backbeats in the array. Every other groove in the family accents quarter
positions of one bar the same way. So genre BPM goes in as written, no halving, and
the 2x ambiguity that stalled this twice does not apply here.

    NEW ORLEANS      --  ->  88    Cissy Strut
    THE ONE          --  -> 101    Funky Drummer
    SECOND LINE      --  -> 100    between two anchors, 88 and 112
    FUNK 4-ON-FLOOR  --  -> 114    break-tempo cluster
    BACKBEAT         --  -> 100    constructed default, labelled as one
    FIVE ROCK        --  -> 100    constructed default, labelled as one
    MOTOWN           --      --    searched, not found, still on the dial

**NEW ORLEANS overturns a source rather than agreeing with one.** A drumming history
puts New Orleans funk at "quarter note = 152-208" while also saying the style is
"easily interpreted in double time". Cissy Strut, the canonical record, is 88 BPM on
getsongbpm and sfrbeats, and songbpm's 176 is itself flagged there as half-time 88.
The 152-208 is the double-time count. Taken literally it would have run this groove at
twice the speed of the records it comes from, and it would have looked properly
sourced doing it.

**Two are labelled CONSTRUCTED rather than given a fake citation.** BACKBEAT is not a
style with a tempo; it is the snare-on-2-and-4 cell under most Anglo-American popular
music, played at any speed from a ballad to a punk record. FIVE ROCK is an invented
5/4 cell. Both get a neutral 100 and say plainly that it is a default.

**MOTOWN is still on the dial.** Searched in this pass, nothing found; the break-tempo
analysis covers funk rather than Motown. A named Motown record with a verified BPM
settles it.

**The checker caught me twice more, both times on my own prose.** Writing "swung-bossa
count" flagged BOSSA, and naming COMPOUND 9 inside FIVE ROCK's note flagged FIVE ROCK,
because "compound" is triplet vocabulary. First resolved with an acknowledgement
marker, second by rewording, since the reference was incidental. A checker that only
ever agrees with you is not doing anything.

---

## v0.103.9 — family 1 closed, and KPANLOGO turns out to be a real dispute

Going back for the four grooves left inheriting the dial found one tempo, three dead
ends, and a grid disagreement that matters more than any of them.

**SOUKOUS: 62.** Chosic gives soukous a typical range of 115-130 from artist tempo
data, with individual tracks reading 106, 130 and 144. 125 as the middle, halved for
the two-bar cycle, is 62.

**SHIKO, GAHU and KPANLOGO: CEILING REACHED on tempo,** and each says what would end
it. Shiko is filed under highlife, which sources describe only as "fast" with no
figure. Gahu is an Ewe dance rather than a recorded genre, so there is no track
database to read a number off. Kpanlogo is described as "a street party rhythm from
the Ga tribe" and nothing more. All three keep inheriting the dial, which is the
honest state rather than a number that looks researched.

**KPANLOGO's subdivision is downgraded from INFERRED to CONFLICT, and it is a dispute
about the GRID, not about accents.** globalmusictheory.com states the foundational
Kpanlogo rhythm is "often structured around 6/8 or 12/8 time signatures, which feature
groups of three pulses per beat". If that is right, a straight 16-pulse grid is the
wrong SHAPE for it, in the same way JAZZ SWING was before v0.103.4, and not merely a
quantisation of it.

Against that reading: Wikipedia's Kpanlogo article says the nono bell "plays the key
pattern or timeline of the music" and that the main bell part "is one of the most
common and oldest key patterns found in sub-Saharan Africa", which is the 16-pulse
family. And our array is byte-identical to SON CLAVE 3-2, a 16-pulse timeline, which
the groove audit already examined and accepted.

Two credible sources, opposite answers, on the thing this whole audit is about. It is
recorded rather than resolved, because picking one would be a guess dressed as a
finding. A Ga drumming method or a transcription of the nono part settles it.

Family 1 ledger: 1 SOURCED, 1 CONFLICT, 4 CEILING REACHED, 9 cycles established,
6 tempos set.

---

## v0.103.8 — family 1 tempos, halved for the cycle

First tempos set with the cycle length known, so they are right in genre terms rather
than right in app terms and wrong to a musician.

    SON CLAVE 3-2   110 ->  90     reads as 180 salsa (was 220)
    SON CLAVE 2-3    --  ->  90     had no tempo
    RUMBA CLAVE 3-2  --  -> 112     reads as 224 (was inheriting the dial)
    RUMBA CLAVE 2-3  --  -> 112
    BOSSA NOVA       96  ->  65     reads as 130 (was 192)

**SON CLAVE** now sits at the middle of the form. Salsa runs around 180 BPM across a
150-250 range, most social dancing 160-220. The old 110 read as 220, which is salsa
dura and timba territory, not a neutral reference for a clave.

**BOSSA NOVA was the worst of the five.** Its own defining description is the relaxed,
slower cousin of samba, and at 96 it read as 192 genre BPM, faster than the samba it
is defined as slower than. Reference points cluster near 130: Drumgenius has a plain
bossa phrase at 111 and "The Girl from Ipanema" at 180 in its swung count, and a Blue
Bossa backing track is 140. 130 halves to 65.

**RUMBA CLAVE is referenced to guaguanco,** which is the rumba style that actually
carries rumba clave. Drumgenius lists basic Havana-style guaguanco at 231 and a Robby
Ameen version at 217; halved that is 115 and 108, so 112 sits between them.

**The four African timelines got a cycle and no tempo, on purpose.** SHIKO, SOUKOUS,
GAHU and KPANLOGO have their two-bar cycle written down, but no tempo source was found
for any of them as a style. Halving an invented genre figure would produce something
that looks as researched as the five above and is not. They keep inheriting the dial
and each says so in the file.

Every one of these carries its source and its arithmetic in the comment, so the next
person can check the halving rather than trust it.

---

## v0.103.7 — cycle length declared, and a pin that was anchored to the wrong thing

**Method change first, because it is the point.** Cycle length, subdivision, tempo and
the user-facing origin line are all answered by the same paragraph of the same source.
Auditing them as four separate sweeps means opening sixty comment blocks four times,
which is how SICILIANA sat at more than double its tempo while three other audits
passed it. From here it is one pass per family that resolves everything about a groove
at once, and then that groove is not opened again.

**CYCLE is now written down for the timeline family.** Nine grooves, the four claves
plus BOSSA, SHIKO, SOUKOUS, GAHU and KPANLOGO, each carry a note saying the pattern
spans TWO conventional bars. This was never a new discovery; the CLAVE FAMILY encoding
note at the top of the list already said 16 steps is one app bar of sixteenths holding
a two-bar timeline in cut time. It had just never been written where a tempo decision
would trip over it.

The consequence is stated in each one: one app beat equals two beats of the style, so a
genre tempo must be HALVED before it goes in `suggestedBpm`. Son clave's 110 reads as
220 in salsa terms, against a genre that sits around 180. That is not corrected yet;
the tempo pass for this family comes next, and now it has the fact it needs.

**The SON CLAVE pin drifted, and it was the pin's fault.** It was anchored to the
`name:` line plus the steps line, because the array is not unique (KPANLOGO is
byte-identical, which the groove audit accepts as correct). Inserting a comment between
those two lines broke it, without a single value changing.

A pin that fires on edits which changed nothing trains everyone to ignore it, so it has
been rebuilt as the bare array plus an EXACT-COUNT guard: the pattern must appear
exactly twice, son32 and kpanlogo. Fewer means one of the twins was edited; more means
a third groove drifted into the same pattern, which is also worth knowing.

Verified by sabotage rather than by reading: altering son32's copy while leaving
kpanlogo's alone now reports "found 1, expected exactly 2" and fails the build. The
old pin would have caught that too; the difference is that this one no longer fails
when nothing is wrong.

---

## v0.103.6 — subdivision audit, family 1 of 4: the timelines

First real pass. The script in v0.103.5 could only check a grid against its own
comment, which is circular; this is the start of putting external sources behind the
claims so the check has something true to compare against. Same statuses the pattern
audit uses, and the script now reads them and reports a ledger.

**The research did not come back tidy, which is the useful part.** Three sources,
pulling different ways:

Magill (quoted in Riddim, arXiv:1705.04792) gives the general rule: West African bell
patterns "can nearly always be subdivided into a number of regular pulses (usually 8,
12, or 16)". That is what these arrays are and why they are straight.

Polak's "Rhythmic feel as meter" (2010) then complicates it. Uneven beat subdivision
"play[s] a substantial role in genres from Mali (Mande) and northern Ghana
(Dagbamba) but not in southern and central Ghana (Ewe, Asante)", explicitly against
"the widespread assumption that, in African rhythmic systems, the fast pulse in
general is structurally isochronous". So a straight grid is not universally right or
wrong; it depends on where the groove comes from.

And the quantitative study of Cuban guaguanco measured 186 clave cycles and found the
strokes are not deadpan even where the framework is isochronous: note 2 short, note 3
long, note 4 late, with the deviations "more or less cancel[ling]" so the final
stroke lands where the grid says. A step sequencer has no microtiming, so this is a
CEILING and is written up as one, specifically so nobody later "fixes" it by nudging
a stroke to a neighbouring slot, which would make the pattern wrong rather than
merely quantised.

**Ledger for this family, 6 grooves:**

    SOURCED          GAHU        Ewe; Polak names Ewe as isochronous, so this is the
                                 one groove the study settles outright
    INFERRED         KPANLOGO    Ga, Accra; same region, not one of the two peoples
                                 Polak names. Regional inference, not a citation
    CEILING REACHED  SHIKO       region not pinned by any source found
                     SOUKOUS     Congolese; outside the material studied
                     AFROBEAT    Nigerian; borrowing the Ewe result would be exactly
                                 the overgeneralisation Polak argues against
                     FANGA       Liberian; same

Four CEILING REACHED out of six is not a failure to research. It is what the sources
actually support, and each one names what would settle it.

**Still 32 grooves with no subdivision claim at all.** Three families to go: funk and
soul, the Latin dances, the Balkan and Middle Eastern set.

---

## v0.103.5 — subdivisions checked, and the checker made honest

New audit script, `intonare_subdiv_audit.py`. The pattern audit checked WHICH steps
are struck; this checks whether a groove's grid can express what its own comment says
is being played. It exists because the v0.103.4 bug was three grooves describing a
triplet feel on a duple grid while asserting that was unavoidable, and the wrong
claim had been copied between them.

**Result: no further wrong grids.** The first run flagged five, and all five were
false. MARCH 2/4 and KARSILAMA say "compound" only to contrast themselves with a jig
and with COMPOUND 9. FUNK 4-ON-THE-FLOOR had the word "swing" inside a URL. THE ONE
states outright that swing is a performance property and deliberately not encoded as
a grid position. TRAP's triplets are ornaments over a correct sixteenth base.

**A check that fires on things which are not wrong is worse than no check.** A second
version added GRID-FINER-THAN-USED, which flagged 31 of 61 grooves for using only
even sixteenths on a sixteenth grid. That is not an error; the spare resolution is
what makes a pattern editable. Demoted to an informational column rather than left
as a flag that would train everyone to ignore the script.

**Compromises are acknowledged in the file, not pattern-matched around.** Rather than
keep making the regex cleverer, a groove whose subdivision is knowingly a compromise
now carries a `SUBDIV-AUDIT: ok - reason` marker the script reads. Three do: TRAP,
plus BLUES SHUFFLE and BHANGRA, which were flagging on their own corrective text
describing the sixteenth positions they used to sit on. The reason is required, so
the marker cannot become a silencer someone pastes in to quiet the checker.

The script reports **FLAGGED: 0, acknowledged: 3.**

**What it does NOT prove.** 38 of 61 grooves make no subdivision claim in their
comments, so there is nothing to check them against and the script says so rather
than passing them silently. Their grids may be right; nobody has established it.
Closing that gap means writing a subdivision claim for each, which is research, not
tooling.

---

## v0.103.4 — three grooves were on the wrong grid, and the file said it was unavoidable

JAZZ SWING, BLUES SHUFFLE and BHANGRA are triplet feels. All three were written on a
sixteenth grid, and all three carried a comment saying a sixteenth grid could only
approximate a triplet, so the second stroke sat on the "a" as the nearest available
slot. GOSPEL 6/8 and the 12/8 pair pointed at those notes as precedent.

**That premise was wrong.** The grid is not fixed at sixteenths. `stepsPerBar` is
just the array length, so 12 steps over 4 beats ARE triplet eighths. The scheduler
divides cleanly, the beat markers land at 3 per beat, the pulse dots agree, and the
counting labels already carry a "1 + a" entry for that exact case. Nothing needed
building. The three grooves were simply written on the wrong grid, and the note
explaining why it could not be fixed had been copied between them.

    JAZZ SWING     [1,0,0,0, 2,0,0,1, ...]  ->  [1,0,0, 2,0,1, 1,0,0, 2,0,1]
    BLUES SHUFFLE  [2,0,0,1, x4]            ->  [2,0,1, 2,0,1, 2,0,1, 2,0,1]
    BHANGRA        [2,0,1,0,1,0,0,0, ...]   ->  [2,0,1, 1,0,1, 2,0,1, 1,0,1]

JAZZ SWING's two swung skips now sit on the LAST TRIPLET of beats 2 and 4, steps 5
and 11, which is literally where BYU Percussion and ArtistWorks put them. BLUES
SHUFFLE plays a real shuffle instead of a dotted-sixteenth impression of one; its
accents were not touched, only the grid. BHANGRA's chaal is now the four swung pairs
its own GCSE source vocalises as "dum-di, dum-di, dum-di, dum-di", which is what that
source's "4/4 (12/8)" meter meant all along.

These are the first three grooves in the library on a triplet grid.

**BHANGRA also had a duplicate `steps:` key,** the same array declared twice in one
object. JavaScript takes the last one so nothing ever misbehaved, which is why it
survived. Pre-existing, present in the file before any of this session's edits, and
found only because an assert expecting a unique match got two. A sweep of all 60
grooves for repeated `steps`, `beats`, `name`, `pulse` and `suggestedBpm`
declarations found no others.

**BHANGRA's accents are still contested and still flagged.** Its sources disagree in
opposite directions and this change keeps the old reading (strong on 1 and 3). Only
the grid moved.

**Still open: the swing control does nothing in groove mode.** `advanceNote()`
returns early in the groove branch, before the swing block runs, so the slider only
affects the plain metronome click. Arguably correct now that grooves can carry a real
triplet grid, but it is a silent no-op and the help text does not say so.

---

## v0.103.3 — the dots were lying about the pulse

Moving the audio to the felt pulse in v0.103.1 left the display behind. Three places
compute the beat grouping and after that change they disagreed.

**The pulse dots drew six under a groove you could hear pulsing twice.** They read
`pulseBeats || tsTop` and never learned about `pulse`, so a 6/8 groove clicked on
its two foot-taps while six dots animated underneath. Those dots are the picture of
that click; they now read the same felt pulse the scheduler does.

**The step grid and its counting syllables still use the notated beat, deliberately.**
That is the notation view: for a 6/8 groove it shows the six eighths, which is what
you want when editing a pattern and reading its structure. The pulse dots show what
you hear; the grid shows what is written. Those are different jobs and it is correct
for them to differ. Worth stating outright because it looks like the same
inconsistency that was just fixed and is not.

Caught by Daniele asking whether subdivisions had been checked, which they had not
been; the tempo work had taken all the attention.

---

## v0.103.2 — tempos taken from recordings, not from theory

v0.103.1 fixed the unit and left the numbers where they were, on the assumption that
a value written as a felt pulse was the right value. Checking each against what the
music actually gets played at says otherwise for three of them.

    IRISH JIG        --  -> 100    had no tempo at all; inherited the dial
    GOSPEL 6/8       --  ->  66    had no tempo at all; inherited the dial
    SICILIANA        96  ->  42    was too FAST, not too slow
    TARANTELLA      160  -> 135    above every recording found
    COMPOUND 9      160  ->  53    same sound as before, corrected unit
    SLOW BLUES 12/8  60      kept  52-60 is where the form sits
    GOSPEL 12/8      72      kept

**SICILIANA was wrong in the other direction.** The Clarinet Institute edition of
Bach's Siciliano BWV 1031 prints dotted quarter = 42, and both Wikipedia and San
Francisco Classical Voice describe the form as slow and melancholy. At 96 it was
more than twice that. It is the only value in this whole pass that was playing too
fast rather than too slow, which is a good argument for checking numbers against
recordings instead of reasoning about them.

**TARANTELLA came down.** Four recordings of Tarantella Napoletana read 127, 134,
136 and 149 foot-taps a minute. These are algorithmic readings and all four mislabel
the meter as 4/4, so they are a cluster and not a figure; 135 is the middle of it.
The old 160 sat above all four.

**IRISH JIG had no tempo at all,** so it inherited whatever was on the dial. Tom
Hanway gives the standard metronome setting for jigs as dotted crotchet = 100, Bill
Troxler gives 80-100, and Fiddle Hangout puts the range at 84-120 with dancers
preferring 110-120. 100 is where the session and dance readings overlap.

**COMPOUND 9 was deliberately held at the speed it already had.** It is a
constructed teaching cell with no recording behind it, so there is nothing to check
it against. Its old 160 was almost certainly entered as eighths, and it produced a
3.4-second bar that worked; 53 reproduces that same bar under the corrected unit.
Left at 160 it would have run to eight eighths a second. The comment says not to
restore the old number.

**GOSPEL 6/8's 66 is the weakest claim in the groove table and says so in the
file.** No recording or marking was found for that feel specifically. 66 sits just
above SLOW BLUES 12/8 at 60 and below GOSPEL 12/8 at 72, which is where the form
lives, but it is a considered default and not a citation.

Patterns untouched again; 48 pins held.

---

## v0.103.1 — BPM meant the wrong note

TARANTELLA felt slow because it was slow. It plays at 53 foot-taps a minute and its
own comment cites Wikipedia's "fast upbeat tempo."

**The groove patterns were never the problem.** Not one step array changed in this
entry, and all 48 sentinel pins held throughout. What was wrong is the unit the
tempo number was read in.

**`bpm` was being applied to the notated beat, not the felt one.** Selecting a
groove calls `setTS(preset.beats, ...)`, so a 6/8 groove sets `tsTop` to 6, and the
scheduler computed a bar as `secondsPerBeat * tsTop`. That makes BPM count EIGHTHS.
But a 6/8 bar has two beats, not six: ONE-two-three FOUR-five-six. Every value in
the file was written as the felt pulse, the way a tempo marking on a score is, so
each one played three times too slow. SLOW BLUES 12/8 had a twelve-second bar,
which is five bars a minute.

**Grooves can now declare `pulse`,** the number of felt beats in a bar, and the
scheduler uses that instead of `tsTop`. Anything that does not declare it falls
back to `tsTop`, so all the simple-meter grooves behave exactly as before and the
change cannot reach them. Seven declared it:

    TARANTELLA       2    2.25s bar -> 0.75s     53 -> 160 /min
    SICILIANA        2    3.75s bar -> 1.25s     32 ->  96 /min
    IRISH JIG        2    3.00s bar -> 1.00s
    GOSPEL 6/8       2    3.00s bar -> 1.00s
    SLOW BLUES 12/8  4   12.00s bar -> 4.00s     20 ->  60 /min
    GOSPEL 12/8      4   10.00s bar -> 3.33s     24 ->  72 /min
    COMPOUND 9       3    3.38s bar -> 1.12s     53 -> 160 /min

**Fixing `bpm` rather than the display was the smaller change, not the lazier one.**
`bpm` is read by tap tempo, the drum kit, progressions, the timeline and
`getTempoName`, and rendered in eight places. Leaving it meaning eighths and
correcting only what is shown would have meant patching all of those; `getTempoName`
was already naming compound tempos off the eighth rate and was wrong today. Making
`bpm` mean what a musician means by BPM fixes every one of them at once.

**Two shortcuts rejected, both of which look right until you check.**

Multiplying the seven values by three does not work: `setBPM` clamps at 300, and
five of them need more. TARANTELLA would want 480 and silently clamp to 300,
landing at 100 foot-taps rather than 160. It would have looked fixed and been wrong.

Inferring the grouping from the meter does not work either. "Divisible by three
means compound" gets 6/8 and 12/8 right and then mangles KARŞILAMA, whose 9/8 is
2+2+2+3, four beats of unequal length rather than three even ones. Every grouping
here is declared and taken from the sources already in the file.

**Deliberately left alone, and why.** The flamenco pair is not a compound-meter
case at all: their twelve steps are the twelve counts of the compás, not sixteenths,
so the arithmetic that applies to TARANTELLA does not apply to them. The aksak
meters (RACHENITSA 2+2+3, KOPANITSA 2+2+3+2+2, KARŞILAMA 2+2+2+3, DEVR-I HINDI,
SEVEN ROCK) have UNEVEN pulses, which a single `pulse` count cannot describe, and
their tempo is conventionally given per eighth, which is what they already do.
Whether they are individually too slow is a separate question and still open.

**The background click layer follows the felt pulse now.** In 6/8 it hits the two
foot-taps instead of all six eighths. It is off by default and has its own volume,
so it never touched the groove's own hits either way.

**Listen list.** Every one of the seven is now roughly three times faster, so all of
them want a hearing. TARANTELLA at 160 foot-taps and COMPOUND 9 at 160 are the two
to judge hardest: both are now genuinely quick, TARANTELLA's number is unsourced
beyond "fast upbeat tempo," and COMPOUND 9 is a constructed teaching cell that never
had a source to begin with. If either feels frantic the number is the thing to move,
not the pattern. IRISH JIG and GOSPEL 6/8 still carry no `suggestedBpm` and inherit
whatever is on the dial, which now means foot-taps rather than eighths.

---

## v0.103.0 — the ShareAlike debt, paid

Performance mode plays twenty-one recordings by Bernd Krüger, taken from
piano-midi.de under CC BY-SA 3.0 Germany. ShareAlike means an adaptation has to go
back out under the same licence, and until now the source comments in the file
claimed the adapted MIDIs were "published in repo" when nothing had been published
at all. That is now true instead of aspirational.

**Twenty-one MIDI files, exported back out of the app's own note data.** Not
re-downloaded from piano-midi.de and re-uploaded; exported from the exact
`perf:{notes,ped}` blocks the app plays, so what is published is what ships. All
twenty-one parse clean with balanced note-on and note-off, 423 KB total, from
Träumerei at 2:16 up to the Waldstein first movement at 10:18.

**The seven Rhodes variants are not published separately.** Their note data is
byte-identical to the piano version; the only difference is an empty pedal array,
because a Rhodes has no sustain pedal. Same adaptation, one file.

**The changes are named honestly.** Tempo map flattened to a fixed 120 BPM with the
rubato baked into absolute note positions, hands merged onto one track, velocities
round-tripped through a 0-to-1 float, pedal reduced to CC64 on and off, nothing
trimmed. Everything audible is still his playing.

**Credits now link to the adapted files.** Attribution without access is only half
of ShareAlike; the credits line points at the published folder.

**Two group titles were never translated.** "Performance sequences" and "Fingering
diagrams" sat as hardcoded English inside a bilingual credits screen. Both now have
`data-i18n` keys and Italian twins: Sequenze di esecuzione, Diagrammi di
diteggiatura.

Repo folder to push before this build ships publicly:
`credits/midi-sources/` with the twenty-one `.mid` files, a `README.md`, and an
`index.html` for GitHub Pages. Until that is pushed the in-app link is a 404.

---

## v0.102.24 — closing out: nothing left unexamined

Every groove in the table now has a status and a reason. DESCRIBED is empty. NONE
is empty. There is no entry left that asserts something without saying on what
authority.

**GOSPEL 6/8's frame is sourced and its decoration is flagged.** Practito on the
meter: 6/8 has two main beats, compound duple, each dividing in three, counted
ONE-two-three-FOUR-five-six with the emphasis on 1 and 4. Drumscore is specific
about the backbeat once you are in compound time: where a 4/4 backbeat sits on 2
and 4, the 6/8 equivalent goes on the fourth quaver. Drumhelper gives the same
skeleton as a starting groove, bass drum on count 1 and snare on count 4. So our
accents are the frame plus the backbeat, both verified. The four pushes on the
"and" of 2, 3, 5 and 6 are the gospel ornament on top, and nothing read pins them
there. Frame verified, decoration asserted, and the comment says which is which.

**The last three are marked CEILING REACHED, which is a finished state and not an
open task.** Each says what desk research established, what it could not, and
specifically what would settle it.

MONTUNO: the tumbao is sourceable because the bass has two named landmarks every
source repeats. The piano guajeo has no equivalent; it varies by tune, by pianist,
and by which side of the clave the bar sits on. What would settle it is a Cuban
piano method or a salsa pianist. What ships is one player's ear, which for this
preset is a better authority than another lesson blog.

SAMBA: the surdo half is solid, strong 1 and backbeat on 3. The tamborim carries
samba's identity and is exactly the part no general-audience source notates. What
would settle it is a bateria chart or a percussionist.

NEW ORLEANS: this one has a second problem underneath the disagreement. Second-line
drumming is explicitly not a fixed pattern; the Drummer Cafe notes that every
player has their own way of playing these grooves. So there is no single right
answer to converge on, only a well-chosen example, and this preset should be a
different well-chosen example from Second Line rather than a worse version of it.
What would settle it is Antoon Aukes' "Second Line: 100 Years of New Orleans
Drumming" or a New Orleans drummer.

**Final ledger: 57 of 60 vetted.** 49 sourced, 1 judgement call on conflicting
sources, 5 constructed teaching cells with their claims checked, 2 derived from
their parents by a stated rule, and 3 flagged with the reason and the remedy
written down.

That last number is the honest one. Three grooves in this library are as good as
research without a musician can make them, and they say so on their own faces
rather than in anyone's memory.


## v0.102.23 — the ledger was under-reporting itself

**FUNK 4-ON-THE-FLOOR was the last groove in the table with no comment at all.** It
is also the simplest thing in it, and the definition is the pattern: a bass drum
strike on each of the four quarter notes, creating a steady pulsating foundation.
Soundbrenner adds why nothing else is played, the kick marking every main beat so
the listener never has to guess where the downbeat is. Four accents, no weak
strokes, nothing between. It shares onsets with Backbeat on purpose, and the file
now says the accent weights are the entire difference.

**The bigger fix is to the audit script, which had been grading honest work as
unfinished.** It only recognised a URL as proof, so two whole categories of entry
could never pass no matter how correct they were.

Some presets are invented teaching cells. There is no village that plays "5/4
Ostinato" and no citation will ever exist for it. What CAN be true is that its
comment describes its own notes, and that has been checked. Others are derived from
a neighbour by a rule written in the comment, the way a 2-3 clave is its 3-2 parent
with the halves swapped; the parent carries the citation and repeating it would be
noise.

Two new statuses, CONSTRUCTED and BY-CONSTRUCTION, both counting as done and both
saying plainly that they are done in a different sense from SOURCED. The check
order matters and is commented: constructed cells are classified before the URL
test, so one that mentions a source in passing does not get mislabelled as
transcribed.

The honest count moves from 49 of 60 to **56 of 60**, and none of that jump is new
work. It is the same file, described accurately for the first time. A ledger that
calls correct work unfinished is as wrong as one that calls unfinished work
correct, and the second kind is only more obvious.

What is genuinely left is four entries: Gospel 6/8 and Montuno still want a source,
and Samba and New Orleans are flagged pending a real transcription.


## v0.102.22 — disco, and knowing when NOT to move an accent

**DISCO verified, and its comment's claim holds up unanimously.** MusicRadar says
disco's drums exist to stomp out the four-to-the-floor kick and fill the space
between with the characteristic hiss of the offbeat open hi-hat, calling the hats
the most important ingredient in any disco beat. DRUM! Magazine and Soundbrenner
say the same from their own angles: kick on all four, backbeat on 2 and 4, hats
accented or opened on the offbeat "ands".

**The origin ties two presets in this file together.** Earl Young invented this at
Philadelphia International in the early 70s, on Harold Melvin & the Blue Notes'
"The Love I Lost" in 1973, by turning the Motown beat upside down: he took the
quarter notes Motown put on the SNARE and moved them to the KICK, which freed the
hi-hat hand to do the opening. Disco and Motown are the same idea inverted, and
both have been sitting in this library the whole time without saying so. Now they
point at each other.

**The interesting decision was not moving anything.** Two builds ago Joropo's
accents were moved precisely because the sources called the cross-rhythm the
defining feature and it was inaudible. Disco looks like the same case and is not.

The open hat's distinguishing quality is timbral, not dynamic. Open versus closed,
not loud versus quiet. This engine's two weights mean loud and quiet. Accenting the
"ands" would assert they hit harder than the four-on-the-floor kick, which is
false. Unrenderable is not the same as unimportant, and faking a timbre with a
dynamic accent would be a worse lie than leaving the offbeats light.

Both entries now carry a note pointing at the other, because the difference between
those two situations is subtle and the wrong call in either direction produces a
groove that misrepresents its own genre.

Vetted count is 49 of 60.


## v0.102.21 — trap, and a contradiction that dissolved

**TRAP verified, and one source hands over our exact pattern as a numbered
instruction:** drop the kick on beat 1, add an off-beat kick on the "and" of beat
3, place the snare firmly on beats 2 and 4. Our accents are 1, 2, the "&" of 3, and
4. Kick, clap, kick, clap.

The same source explains why the kick stays thin, and in doing so explains why Boom
Bap and Trap belong at opposite ends of this library rather than next to each
other: in boom-bap the kick is busy and syncopated, in trap it is sparse and
deliberate, leaving room for the 808 to sustain and breathe.

**The apparent contradiction between sources turned out not to be one.** Some say
the snare sits on 2 and 4. Others say that in half-time trap the snare hits on beat
3 of every bar, and call that the defining characteristic of the genre. Both are
true and they describe the same groove counted at two different speeds: trap is
written near 140 BPM but is often felt as a half-time groove around 65 to 85, and
beat 3 of the fast bar is the backbeat of the slow one.

This preset counts at the written rate, so the backbeat lands on 2 and 4. Halve the
BPM and it becomes the other description with no step moving. That is written into
the file, because "the sources disagree" would have been the lazy read and it would
have been wrong.

One thing is deliberately out of scope and labelled as such. Every source agrees
the hi-hats are trap's signature, and they are 32nd rolls and triplet bursts. A
one-voice sixteenth grid can render neither. What ships is the kick-and-clap
skeleton, which is the part a metronome can usefully be.

Vetted count is 48 of 60.


## v0.102.20 — bhangra, where the honest answer is "not from a desk"

**BHANGRA researched properly and left alone, with both reasons written down.** This
is the first entry where the research argued for changing something and the right
call was still to change nothing.

The rhythm is the chaal, and that much is solid. Every source agrees it is the dhol
pattern under all bhangra; musicgcse.co.uk calls it a traditional rhythm featuring
in ALL bhangra music. Two problems sit underneath that, and neither is solvable
here.

**The grid is wrong for it.** The chaal is a triplet feel. A GCSE revision page
gives the meter as "4/4 (12/8)" and vocalises the pattern as "dum-di, dum-di,
dum-di, dum-di", which is four swung pairs, not four straight beats. Our sixteenth
grid cannot place a triplet. This is the same structural limitation already
documented on Blues Shuffle and Jazz Swing, and bhangra now points at those notes
rather than repeating them.

**The sources disagree about the accents, in opposite directions.** The same GCSE
page says "strong accents on first beat of bar", which is what we play. Wikipedia's
Bhangra (dance) article says the dhol gives the music a "syncopated (accents on the
weak beats), swinging rhythmic character" that is the hallmark of the genre. Those
are close to contradictory and both are reputable enough to take seriously.

Nothing moved on that basis. Flipping the accents on a coin toss would be guessing,
and guessing is what put most of the errors in this file to begin with.

The comment now ends with what would actually settle it: a dhol player, or a
transcription of the chaal on a compound grid. Not another search. That is the
ceiling for desk research on this one, and saying so is more useful than another
paragraph of hedging.

Vetted count is 47 of 60.


## v0.102.19 — polka, and a source that disagrees with itself

**POLKA sourced, and the wording correction from two builds ago is vindicated.**
Grokipedia's Oom-pah article states it flatly: in 2/4 time, prevalent in dances
like the polka, the oom falls squarely on beat 1 with the pah occurring on beat 2.
That is exactly what this preset plays, and it is what the old comment had garbled
into an accent on an "and".

Melodigging supplies the origin: polka emerged in early-1830s Bohemia, its hallmark
oom-pah feel being bass on the downbeat and chords on the offbeat.

**One disagreement, and it is inside the same source family.** The Oom-pah article
calls the pattern "a binary strong-weak alternation", which would make beat 2
quieter than beat 1. The Polka article calls the same thing "an accented upbeat
that imparts a buoyant, forward-driving feel", which makes it loud. Those cannot
both be encoded.

Both accents are kept, for two reasons written into the file. The polka-specific
description should win over the general one for a polka preset. And a weak beat 2
would leave this nearly indistinguishable from March 2/4 with a couple of lighter
"ands" added, which defeats the point of having both.

The reversal is a one-character edit and the comment says which character, so if it
reads flat on device it is thirty seconds to change rather than a re-derivation.

Vetted count is 46 of 60.


## v0.102.18 — cumbia, and a deliberate deviation admitted

**CUMBIA's meter and its cell are sourced; the stroke placement is labelled a
reading.** Third entry in the Calypso tier and the pattern is becoming familiar.

Wikipedia states both halves of what the comment already claimed: cumbia "has a 2/2
or 2/4 meter", and "the sound of cumbia can be characterized as having a simple
'chu-chucu-chu' rhythm created by the guacharaca". So the duple claim is right, the
guacharaca really is the instrument responsible, and "chu-chucu" is the source's own
word rather than ours. RF Dance says the same independently.

**One deviation is now admitted rather than glossed.** Traditional cumbia is 2/2 or
2/4 and this preset is 4/4. That is a deliberate choice, not a mistake: 4/4 is
where the rest of the app's cumbia material already lives, and two bars of 2/4 sit
inside one bar of 4/4 without changing a single stroke. Worth writing down because
a Colombian player looking at "4/4 — Colombian" on the card has a fair reason to
raise an eyebrow, and the file should be able to answer that rather than shrug.

What remains a reading is where the guacharaca's strokes land. "Chu-chucu" is
onomatopoeia. Rendering it as a stroke on the beat plus two quick ones on the "and"
and the "a" is a plausible mapping of that sound and is what ships; nothing read
pins the scraper to specific sixteenths.

Vetted count is 45 of 60.


## v0.102.17 — bolero, where the label matters more than the notes

**BOLERO's meter and lineage are now sourced, and its stroke placement is flagged.**
This is the second Calypso-shaped entry: solid on what it is, honest about where
the hits fall.

Wikipedia describes the Spanish bolero as a dance in 3/4 popular in the late 18th
and early 19th centuries, descended from the seguidilla between 1750 and 1772,
accompanied by guitar and castanets. MasterClass draws the split cleanly: the
Spanish bolero of around 1780 was performed in 3/4, while the Cuban bolero is
danced in 2/4 or 4/4.

Which makes the parenthetical in the origin label the important part of this entry
rather than a footnote. Two different dances share the name, they are in different
meters, and the Cuban one is far better known. Anyone reaching for "bolero"
expecting the Cuban ballad will find the meter wrong and reasonably assume we made
a mistake. The label already said so on the card; now the reason is written down
underneath it.

What is not sourced is where the guitar and castanets actually land inside the bar.
The 3/4 is beyond dispute. Accent 1, pickup on the "and" of 2, accent 3 is a
plausible and self-consistent reading, and it is now labelled as exactly that
rather than presented as transcribed.

Vetted count is 44 of 60.


## v0.102.16 — joropo, where the defining feature was inaudible

**JOROPO sourced properly, and then its accents moved.** The onsets were already
right and the problem was one level up.

Sesquiáltera is not a flourish in this music, it is what the genre is for. Pedroza,
writing on the joropo in Venezuela's musical modernity, describes the llanera harp
playing its treble strings "in 6/8 against the 3/4 of the bordones (a vertical
sesquiáltera)", the two producing "a rich array of polyrhythmic encounters".
Melodigging puts it plainly: joropo is famous for the overlay of 3/4 and 6/8,
creating the hemiolas that drive the dance.

Our steps already had both layers in them. Steps 0, 4 and 8 are the 3/4 quarters
and step 6 is the 6/8 midpoint, so nothing was missing. But only step 0 was
accented, which meant the preset played as a light 3/4 with a stray extra stroke
and the cross-rhythm was present in the data and inaudible. Same class of fault as
Boom Bap having no bap: the notes were there, the emphasis was not, and emphasis is
the entire content of the claim.

The 6/8 layer now carries the accents, on steps 0 and 6, with the 3/4-only quarters
weak on 4 and 8. Two against three, which is the hemiola.

Worth stating what this cannot do. A one-voice, two-weight engine cannot sound both
layers of a polyrhythm at once. The choice is which layer to put in front, and the
right answer is the one that fights the meter, because the other one is what the
listener supplies for themselves. That is the same reasoning behind Reggae
One-Drop's empty beat 1 and Tumbao's empty downbeat, and it is now written down in
three places rather than being rediscovered each time.

Vetted count is 43 of 60.


## v0.102.15 — the shuffle, and admitting the grid cannot do triplets

**BLUES SHUFFLE verified.** Every source states the same rule: play the first and
third notes of each triplet and leave the middle one out, giving the long-short
pattern that repeats on every beat. Total Drummer adds the rest of the kit, bass
drum on 1 and 3 and snare backbeat on 2 and 4, which is why all four beats sound in
this preset rather than only two. ArtistWorks supplies the counting our encoding
already uses: straight eighths are "1-and-2-and", shuffle is "1-a-2-a", long-short.
Beat plus its "a" is exactly what these steps play.

**The more useful part of this build is an admission, written into two presets.**

A shuffle's second note is the third triplet of the beat. A sixteenth grid has no
slot there. The "a" is the nearest available position and it sits slightly late. So
Blues Shuffle and Jazz Swing are both approximations, not because anyone got them
wrong but because the grid cannot represent a triplet subdivision at all.

That is now stated in both entries, with a source that acknowledges the same
problem from the notation side: Rhythm Notes points out that the shuffle feel "is
sometimes more of a triplet feel than sixteenth notes" and that written versions
are "open to interpretations". Each entry also points at the other, so anyone
looking at one finds the explanation for both.

This matters beyond these two. Anyone auditing this file later will eventually
notice that the swung presets do not line up with a triplet and may try to "fix"
them. There is no fix available at this resolution. The honest options are to leave
them approximate and labelled, or to give the engine a triplet grid, and that is a
much larger decision than a groove edit.

Vetted count is 42 of 60.


## v0.102.14 — maqsum, matched character by character

**MAQSUM got the tightest confirmation in the whole audit.** Wikipedia's Maqsoum
article prints the basic structure as a 16-slot grid, D-T---T-D---T---, which reads
as dum on 0, tek on 2, tek on 6, dum on 8, tek on 12. Ours sit on exactly those
five and nowhere else. Not a description in words that I then had to translate into
steps; the same grid, the same slots.

The source's own D and T split is doing the same job as this engine's accent and
weak split, since dum is the deep stroke and tek the bright one. So the dums carry
the accents and the teks do not, and that mapping is the source's rather than mine.

One thing written into the file for whoever looks at this next: maqsoum is a
derivative of baladi and the two differ by exactly one stroke. Baladi is
D-D---T-D---T---, meaning step 2 is a dum instead of a tek, and Wikipedia says
outright that the only difference is the accent on the second beat. Change step 2
and this preset silently stops being maqsum and becomes baladi. That is precisely
the kind of one-pulse edit that has gone wrong repeatedly in this file, so it is
now labelled as a tripwire rather than left to be rediscovered.

**KARŞILAMA sourced with a reference that was already in the file.** The Wikipedia
Aksak article that Devr-i Hindi leans on names this grouping specifically: in
Turkish music theory the term refers only to the grouping of nine pulses into
2+2+2+3. Group starts fall on pulses 1, 3, 5 and 7, and the accents are on exactly
those four with pulse 9 weak. Checked rather than assumed, since that is how the
five-four presets got caught out.

Also noted there: the other nine in the library is Compound 9, which is 3+3+3 and
constructed rather than transcribed. Two nines, two different things, and the file
now says which is which.

Vetted count is 41 of 60.


## v0.102.13 — splitting the bass off the piano

**New preset: TUMBAO.** The bass line that MONTUNO had been quietly describing
itself with, now shipping as its own entry and cited on day one.

It is deliberately sparse: two strokes, bombo on the "and" of 2 and ponche on beat
4, with beat 1 left empty. That emptiness is the whole figure. Wikipedia's Tumbao
article explains why: the last note of the measure is held over the downbeat of the
next, so only the two offbeats of tresillo are actually sounded, the first called
bombo and the second ponche. Piano With Jonny puts the same thing in playing terms,
noting beat 4 is tied across the bar line such that beat 1 is rarely played. A salsa
bassist on TalkBass arrives at the identical pair from experience rather than
theory. Three sources, one answer, given by name rather than by inference.

Adding a stroke on beat 1 fills in the gap that makes it work, which is the same
mistake as putting a kick on Reggae One-Drop's beat 1. Noted in the file next to
the pattern.

**MONTUNO's notes are unchanged; its explanation was the thing that was wrong.** It
had been justifying a piano guajeo using the bass tumbao's landmarks and claiming
to land both of them. It lands one. Ponche sits squarely on step 12. Bombo is step
6, and step 6 is silent, with the nearest stroke a sixteenth later on step 7.

That is not a fault in the pattern. The piano montuno leans offbeat and runs against
the clave; marking bombo is the bass's job, and the bass now has somewhere to do it.
The pattern was built by ear by the app's author and is kept exactly as built. The
false claim is gone and the reason it was false is written down.

The two are meant to be heard together, the way Backbeat and The One are, or Soleá
and Bulería. Separately each says one true thing; together they say what the
rhythm section actually does.

Sixty grooves now. Vetted count is 39 of 60, not 40: Tumbao lands vetted, but
Montuno stays unvetted because rewriting its comment removed the only source names
it had and they were never links anyway. It needs a real piano-guajeo transcription,
which is now on the same list as Samba's tamborim and New Orleans.


## v0.102.12 — the Jamaican pair, both clean

Two verifications, no notes moved, and one of them is the tightest source match in
the whole audit so far.

**REGGAE ONE-DROP verified beat by beat.** Tunable spells out all four: nothing on
beat 1, hi-hat or rimclick on beat 2, kick and snare together on beat 3, hi-hat or
rimclick on beat 4. That is this preset exactly, with nothing left over and nothing
missing. MusicRadar says why the empty beat 1 carries the whole idea: the one drop
is defined by the absence of the always-expected kick there, with the emphasis
moving to beat 3. Bass Culture calls beat 3 the single dominant accent of the bar,
which is precisely why it is the only accent we play. Carlton Barrett of the
Wailers is credited with popularising it, and that is now in the file too.

**DANCEHALL matched a source at step-number level**, which has not happened before.
Nearly every rhythm source describes placement in words and leaves the encoding as
an act of translation. This one uses the same 16-step grid the engine does and says
the dembow "places the snare on syncopated 16th-note positions — specifically step
4 and step 7 of a 16-step bar". Ours are on 4 and 7, with their repeats at 12 and
15. No interpretation required, which is the rarest and most reassuring kind of
confirmation available here. Wikipedia covers the kick side: the riddim employs the
tresillo pattern, and takes its name from Shabba Ranks' 1990 track "Dem Bow".

That also explains the last of the tresillo-family overlaps. Dancehall shares a
kick cell with Tresillo by descent, the same way Calypso does. The snare on 4 and 7
is what makes it dancehall rather than the bare cell, and the file says so.

Vetted count is 38 of 59.


## v0.102.11 — calypso, and admitting what a source does not say

**HABANERA verified, and the relationship it claimed turns out to be the textbook
one.** Its comment already said the habanera cell is the tresillo's first half plus
beats 3 and 4. Wikipedia's tresillo article says the same thing from the other
side: tresillo "is a more basic form of the rhythmic figure known as the habanera".
So habanera is tresillo with the back half filled in by two plain quarters, which
is exactly what these steps play. The Puget Sound theory text lands in the same
place independently, listing Bizet's Habanera among its 3+3+2 examples.

**CALYPSO is the first entry where I went looking and came back with less than I
wanted, so the comment says so.** What is properly sourced now is the meter, the
origin and the character of the bass: Trinidad and Tobago, Afro-Trinidadian,
early-to-mid 19th century, rhythms traceable to West African Kaiso, and a bass drum
that plays more syncopated than soca's with a less prominent snare.

What is not sourced is the exact sixteenths. No transcription has been read that
pins calypso to these specific strokes. The cell we play is the tresillo, inherited
rather than independently attested, and the file now states that plainly instead of
implying more confidence than exists.

That also settles the shared-onsets flag the audit has been raising, and settles it
honestly. Calypso and Tresillo land on the same six onsets because calypso's cell
IS the tresillo. What differs is weight: tresillo accents all six evenly, calypso
accents the first two of each half-bar and lightens the third, which is the
boom-boom-CHICK. Written into the file, along with a note that if a real calypso
transcription ever surfaces and disagrees, Calypso is the entry that moves and
Tresillo is not.

Vetted count is 36 of 59.


## v0.102.10 — the 6/8 pair, and the march

Citations only again. All three were already playing the right notes.

**IRISH JIG** verified against four sources that independently name the same two
beats. Six eighth notes felt as two groups of three, emphasis on 1 and 4, which is
what our accents on steps 0 and 6 already were. Soundbrenner happens to describe
our exact encoding for a percussion part: a stronger stroke on 1 and 4 with lighter
taps filling the subdivision.

**SICILIANA** verified too. Slow 6/8 or 12/8, compound dotted rhythm, pastoral and
usually minor. The strokes at 0, 3 and 4 of each group are the dotted-eighth,
sixteenth, eighth figure the comment always claimed.

The interesting part is why those two sound like cousins. It is not an accident and
it is not a duplicate: the sources describe the siciliana as somewhat resembling a
slow jig or tarantella, so they share the two dotted-quarter pulses by definition.
The jig fills them evenly and the siciliana dots them. Both ship, they do not share
onsets, and the file now explains the relationship instead of leaving it looking
like an oversight.

**MARCH 2/4** accents both beats and weakens neither, which is the point. The
left-right pulse of a march is a steady simple-meter tread, set against the
compound lilt of a jig. A march that leans hard on beat one is doing a waltz's job.

One process note. Two edits bounced off the assertion guard this build because my
copy of the existing comment had the line wraps in the wrong places. That is the
guard doing its job on a 10MB file rather than a problem: nothing was written
either time, and the fix was to read the exact bytes back before retrying.

Vetted count is 34 of 59. POLKA 2/4 still needs a citation; its wording was fixed
two builds ago but nothing is linked yet.


## v0.102.9 — the three-four family, verified without moving a note

All three 3/4 presets were already correct. This build is citations only, plus one
recorded disagreement.

**WALTZ** accents beat 1 and softens 2 and 3, which is the whole definition. The
Berliner Philharmoniker describes the waltz, while contrasting it with the mazurka,
as the one "whose rhythm always accentuates the beginning of the bar". TalkClassical
puts it physically: waltzes have a strong down on the first beat that mirrors the
swooping downward step in the dance.

**MAZURKA** accents beat 2, and Grove backs it. Wikipedia quotes the New Grove
Dictionary on the mazur's "strong accents unsystematically placed on the second or
third beat", and the Polish Music Center at USC says the same independently. The
sources say second OR third; a fixed preset has to pick one, and beat 2 is the
commoner reading and the one that contrasts most audibly with Waltz. Noted in the
file so the choice is visible rather than implied.

**VIENNESE WALTZ** got the best find of the three, a source that draws the exact
line between it and Mazurka: the Viennese waltz has "a slight anticipation of the
second beat; this is different from the second-beat accent of a mazurka and gives
the rhythm an exhilarating lift".

That sentence makes the trio coherent for the first time. Waltz accents 1. Mazurka
accents 2. Viennese accents 1 and moves beat 2 early without accenting it. Three
genuinely different things rather than three shades of the same one, which is what
they had been reading as.

One disagreement is written into the file rather than smoothed over. A discussion on
The Session describes the Viennese second beat as slightly delayed rather than
early, though the poster hedges. Anticipation is the commoner account and is what
ships; if better evidence turns up, only that one step moves.

Vetted count is 31 of 59.


## v0.102.8 — the 12/8 family, and a claim that made two presets lie together

**SLOW BLUES 12/8 sourced.** Tunable on the meter: twelve eighth notes grouped into
four beats of three, the compound quadruple feel that is essential to blues,
gospel, doo-wop and slow rock ballads. Beta Monkey's blues drumming guide on where
the snare goes, and it confirms the backbeat correction from the previous build:
play it with a lazier feel, slightly behind, on the 2 and 4 backbeat.

Worth writing down because it will come up again: some 12/8 sources put the snare
on the 7th eighth instead, which is beat 3 of the four. That is the half-time
slow-rock ballad feel and it is a genuinely different groove that happens to share
a time signature. This preset is the blues one, and the file now says which is
which so nobody "fixes" it into the other.

**GOSPEL 12/8's notes moved so its own comment stops being false.** It claimed the
"same four dotted-quarter frame" as slow blues, and then accented beats 1 and 3
while slow blues accented 2 and 4. The two presets did not share a frame at all,
which meant the sentence was describing a relationship that was not in the data.
Backbeat now matches, and the pair differ by density instead, which is the real
distinction and the one the rest of the comment already described: same four beats,
same backbeat, gospel fills every third partial and blues leaves it empty.

**GOSPEL 6/8's claim was under-describing its own notes.** It listed the pushes on
the "and" of 2 and 5 and said nothing about the ones on the "and" of 3 and 6, which
are also played. Four pushes, not two. Notes unchanged, comment corrected, plus a
line on what actually separates it from the 12/8 entry: compound duple, two
dotted-quarter beats, same lilt at half the frame.

Vetted count is 28 of 59.


## v0.102.7 — three comments that named their sources but never linked them

No pattern changes. Three grooves already quoted real sources in prose and cited no
URL, so the audit graded them as unsupported assertions. They are now verified and
linked, which is the cheapest kind of progress available and worth doing before any
more research.

**BACKBEAT and THE ONE** both leaned on PBS Sound Field's "How James Brown Invented
Funk" without a link. Located the episode and checked the transcript: the quotes
already in the file are accurate word for word, including the contrast the two
presets exist to demonstrate. Most music of that era leaned on the back beat, on
the two and the four; Brown moved the emphasis to the one. Both patterns already
played exactly that, so only the citations moved.

**MOTOWN** claimed the snare lands on every quarter note and vaguely gestured at
"Drumeo, Drumhelper, et al". Four sources now sit in the file, and one of them
names the man responsible. Loudlands credits Richard "Pistol" Allen with
popularising the snare on all four beats instead of only 2 and 4, "which gave a
much more driving feel to the music". A Belmont University thesis on Motown
drumming calls the groove Four-On-The-Snare and spells it out as eighth notes on
the hi-hat, quarter notes on the snare, bass drum following the bass guitar. Drumeo
and eMastered agree independently. Our accents on 2 and 4 with the other two
quarters weak is exactly that shape.

Vetted count is up to 26 of 59.


## v0.102.6 — the flamenco pair, and a regression caught

**COMPÁS SOLEÁ verified and left alone.** Four independent sources give the same
five accents on the twelve-count compás: beats 3, 6, 8, 10 and 12, counted from
one. Studio-flamenco, flamencometronome.com, chromatone, and Paul Bosauder writing
for NZ Musician from Seville all say it identically. Our steps 2, 5, 7, 9 and 11
are exactly those counts. Nothing moved.

**FLAMENCO BULERÍA had the right idea and the wrong arithmetic.** Its comment said
"accents on 12, 3, 6, 8, 10 → steps 0, 2, 5, 7, 9". If step 0 is count 12 then
count 3 is step 3, not step 2, so every accent after the first was landing a step
early. The mapping is now 12→0, 3→3, 6→6, 8→8, 10→10.

Worth understanding rather than just patching, because it explains the pair.
Bulería carries the same five accents as soleá. The only difference is where the
counting starts, and NZ Musician says why that is deliberate: flamenco musicians
count bulerías from beat 12 "to keep things consistent between the soleá and
bulerías styles so that internal accents, harmonic changes and closes happen in
the same place". In a looping metronome that shared accent set with a shifted
start is exactly what makes them feel different. Bulería opens on an accent. Soleá
does not.

**This one was a regression, not a fresh mistake.** Steps 0, 3, 6, 8, 10 were
correct in this file at one point and were changed to 0, 2, 5, 7, 9 later. Noted in
the comment so nobody re-derives the wrong version a third time.


## v0.102.5 — checking every claim against its own notes

Ran one mechanical sweep comparing what each remaining groove's comment asserts
against what its steps actually play. Eight mismatches, found in a single pass.
That is more bugs than three rounds of searching turned up, and it cost nothing.

**JAZZ SWING was the bad one.** The comment described the swing ride correctly and
the notes played something else entirely: accents landed on the "a" of 1 and the
"e" of 3, and beat 2 was never struck. Anyone who reached for a swing click got
something that was not swing and was not a click either.

Rebuilt to the actual pattern. BYU Percussion describes it as even quarter notes
with swung eighths on the "and" of beats two and four, plus a hi-hat chick on two
and four. ArtistWorks describes the same figure as spang-a-lang, quarter notes
with a triplet skip between beats 2 and 3 and between 4 and 1. So quarters on all
four, the swung skip after 2 and after 4, hi-hat backbeats as the accents. The
skip is the last note of a triplet and a sixteenth grid cannot place it exactly,
so it sits on the nearest slot, the "a". Kenny Clarke invented the figure, which
is why every source describes the same one.

**BOLERO** promised accents on 1 and 3 and delivered one; beat 3 was weak. Fixed.

**SLOW BLUES 12/8** called the backbeat essential in its own comment and then
accented beats 1 and 3, burying it. Now accented on 2 and 4, which is how the
Backbeat preset already treats the same idea in simple time.

**BHANGRA and VIENNESE WALTZ had labelling errors, not note errors.** Both comments
named the wrong subdivision, calling a stroke on the "a" an "and". The notes were
right in both cases; the words were one sixteenth out. Words fixed.

**POLKA's wording contradicted its own data.** It said the chord fell on "the
offbeat" and produced "the accented upbeat", which reads as an accent on an "and".
Nothing on an "and" is accented and nothing should be. In 2/4 the pah is beat 2.

**SAMBA and NEW ORLEANS are flagged rather than fixed.** Samba's comment listed
tamborim pushes on the "and" of 1, 2 and 4 while the data plays the "and" of 1, 3
and 4. New Orleans says the bass sits on 1 and 3 while beat 3 carries no accent. In
both cases one of the two is wrong and no source has been read that settles it, so
picking would have been guessing. Samba's comment was corrected to describe the
data honestly and marked unsourced. New Orleans is marked as a disagreement, with
a note that Second Line above is already the sourced New Orleans entry and this one
should end up being a genuinely different part rather than a second attempt at the
same one.


## v0.102.4 — the invented ones were lying too

New rule for the library, and it is a good one: a preset does not have to be
transcribed from anywhere, but if it asserts something it had better do it. Four
of the six constructed presets asserted a grouping their notes did not play.

**5/4 OSTINATO** claimed a 2+3 grouping and accented beats 1, 2 and 3. A 2+3 has
group starts on 1 and 3, so that is not a 2+3, it is three loud beats followed by
two quiet ones. Accents on 1 and 3 now.

**FIVE ROCK** claimed "4+1: driving four then an extra beat" and accented 1, 3 and
5, which is a 2+2+1 feel. Group starts for 4+1 are 1 and 5, so that is where the
accents sit now, and it finally sounds like the thing it is named after.

**TAKE FIVE** contradicted itself in a single line: it said "3+2 grouping" and
then listed accents on 1, 3 and 4. A 3+2 has group starts on 1 and 4 only, and the
accent on 3 belonged to no group at all, which made the whole thing read as
2+1+2. Take Five exists to teach the 3+2 division, so it now plays one.

**SEVEN ROCK lost its Brubeck reference, because the reference was wrong.** The
comment claimed "4+3 grouping, Unsquare Dance feel". Unsquare Dance is not 4+3. E.
Michael Harrington puts it plainly: in Unsquare Dance, 7 = 2+2+3. Jazz Backstory
describes the parts and lands in the same place, with the bass tapping 1, 3 and 5
against claps on 2, 4, 6 and 7, and 1-3-5 is exactly the 2+2+3 group start. That
rhythm was already in the library, correctly, as Rachenitsa. So the preset was
duplicating an existing groove and misattributing it at the same time. It is now
an honest 4+3 with no Brubeck claim attached, which means three genuinely distinct
sevens ship: 2+2+3, 3+2+2, and 4+3.

**JAZZ WALTZ's claim was rewritten** rather than its notes. It promised a strong 1,
a brushed 2 and a "medium" 3, but steps carry two weights and there is no medium,
so beats 2 and 3 were identical in the data while the comment insisted they were
not. The comment now describes what plays.

**COMPOUND 9 was checked and is fine.** Three groups of three, group starts on 1, 4
and 7, accents on exactly those. Left alone and marked verified.

All six now say CONSTRUCTED where that is the truth, so nobody later mistakes a
teaching cell for a transcription.


## v0.102.3 — the audit was lying to us

**The audit script had a parsing bug and it flattered the numbers.** It only read
comments sitting above a groove's `id:` line, so anything documented below its id
came back as undocumented. That is what produced the "20 unverifiable" figure and
sent a whole session chasing grooves that were already fine.

Rebuilt, and it now grades on a harder curve. A groove counts as done only if its
comment contains an actual URL. Five classes: SOURCED has a citation, CONFLICT
means the sources disagree and a reversible judgement was made, FLAGGED means
known-unresolved with the reason written down, DESCRIBED means someone asserted
something and cited nothing, NONE means silence. DESCRIBED is the honest new
category and it is not a pass, however confident the sentence sounds.

The real number is 18 of 59 vetted. That is worse than the old count claimed and
it is the number to work from.

**TARANTELLA verified, not changed.** Compound duple with the accents on the 1
and the 4 of the six eighths, gallop stroke on the third eighth of each group.
Melodigging is explicit: two strong pulses per bar, tamburello accents on 1 and 4.
Naples LDM describes the same thing from the listener's side, a very fast
ONE-two-three ONE-two-three.

**CHA-CHA-CHÁ: beat 3 promoted from weak to accent.** Jorrín simplified mambo's
syncopation on purpose, and part of that simplification was keeping a strong
metric accent on beats 1 and 3 in the cowbell. Our beat 3 was weak, which
contradicted the one thing the composer was deliberately doing. All four quarters
still sound; the triple still lands on 4, the "&" of 4, and 1; beat 2 is now the
only weak stroke.

**ÇİFTETELLİ is the one where sources genuinely disagree.** Three written readings
were found, all calling themselves çiftetelli, and no two match. The old pattern
matched none of them and cited nothing. Adopted the Darbuka Ritim Solo table
because it is the only version written at sixteenth resolution, which is what this
engine stores, so encoding it takes no interpretation. Dums on 1 and 3, teks and
kas filling the rest. All three readings are written into the file so this can be
reversed on better evidence.

**New check: shared onsets.** Same hits, different accent weights, which the old
duplicate check could not see. It found five clusters straight away. Tresillo and
Calypso land identically. So do Disco and Motown, and Funk 4-on-the-Floor and
Backbeat. Take Five, 5/4 Ostinato and Five Rock are all the same five-beat cell,
and Rachenitsa, Devr-i Hindi and Seven Rock are all the same seven. Some of those
are probably fine and some are three presets wearing one rhythm. Next job.

Grooves vetted: 18 of 59, honestly counted for the first time.


## v0.102.2 — Allen's first pattern, and fanga found

Both grooves I was ready to write off turned out to have real transcriptions
behind them. Neither is guesswork now.

**AFROBEAT is Tony Allen's first pattern.** Allen picked this one out himself; per
Rolling Stone he said the most important thing an aspiring afrobeat drummer needs
to learn is the first of the five patterns he demonstrates in "Birth of Afrobeat".
Joe Ospalla's transcription PDF builds it up one instruction at a time, and the
captions fix every stroke: bass on 1e and 3e, snare on 1a, snare on the "e" and
"&" of 2, snare on 4e, snare on the "&" of 4. Kick takes the accents, the snare
figures sit weak underneath, and the hi-hat layer is dropped because one voice
cannot carry three.

Fair warning before you hear it: nothing lands on 1, 2, 3 or 4. That is not a bug
and it is not a rounding error, it is the entire reason Allen sounds like Allen.
He pushes the kick off the downbeat onto its "e", so the groove floats over the
pulse rather than stamping it. Reggae One-Drop already drops beat 1, so an empty
step 0 is not new here, but four empty downbeats is. If it reads as broken rather
than as floating on device, say so and we will decide what to do about it.

**FANGA is the Djembe 1 accompaniment.** Two independent transcriptions give a
byte-identical sound row, which is the cross-check that made it shippable: the
Server Hosted African Rhythm Exchange and Kresimir Oreski's "15 Essential
Rhythms" both write it B--T -TT- B-B- TT--. Bass strokes at 0, 8 and 10 become
the accents; tones at 3, 5, 6, 12 and 13 become the weak strokes, which is the
same distinction the source notation already makes. The sparser dunun bass part is
noted in the file in case this ever wants simplifying.

The context stays written down rather than buried. Fanga as the world plays it is
partly a mid-century staging: Pearl Primus choreographed her version in 1959 and
LaRocque Bey wrote the "Fanga alafia" chant in New York in the late 50s. The drum
part is still the drum part that gets played, and it is now the one we play.

The two presets also no longer share onsets, which they never should have.

Grooves with no source behind them: down from 13 to 11.


## v0.102.1 — boom bap had no bap

**BOOM BAP corrected.** The preset accented beats 1 and 3 and put nothing at all
on 2 and 4. The name is onomatopoeia, per Wikipedia, for the kick drum and the
snare drum in that order, so the entire second half of the name was missing from
the pattern.

Every source gives the same skeleton. Hip Hop Music History: "The one and three
count on the beat would typically have a kick drum and the two and four count of
the beat would have a snare." Native Instruments goes further and supplies the
syncopation: snares on beats 2 and 4, kicks on the first, fourth and sixth 8th
notes. That works out to accents on all four beats with weak ghost kicks on the
"&" of 2 and the "&" of 3.

Its origin label said "Hip-hop / trap", which is backwards. Boom bap is the
late-80s and early-90s East Coast golden age, and trap is the thing that departed
from it. Trap is its own preset a few rows up. Label now reads East Coast golden
age.

**SECOND LINE verified, not changed.** It was already right and simply had nothing
written down. The accents sit on 1, the "&" of 2, and 4, which is the 3-side of
the son clave exactly as second-line players count it, and the accent on beat 4 is
the big four that the whole phrase leads to. Four independent sources now sit in
the file next to it, including the Ethnomusicology Review transcription that
identifies the weak stroke on the "and of 3" as the anticipation into that big
four.

**FANGA's origin corrected.** It said Mandinka. Fanga is from the Vai people of
Liberia. The pattern itself is still not signed off, and the comment now explains
why rather than pretending otherwise: fanga as the world plays it is largely a
mid-century American concert-dance construction, choreographed by Pearl Primus in
1959 with a song written by LaRocque Bey in the early 60s, set to a melody
popularised by minstrels. There is no single village transcription to be accurate
to, and the rhythm is an ensemble part in any case.

**AFROBEAT flagged, with the reason.** There is no one afrobeat timeline. Tony
Allen, who invented the drumming, said it plainly: "Afrobeat has different
varieties of rhythm... all what I'm doing is on 4/4 time signature, so it's just a
question of the composition of the patterns." In the same clip he demonstrates
five of them. The features that are citable are two-voice, an eighth-plus-two-
sixteenths figure on the ride against kicks on 1, 1e, 3 and 3e, and this engine
plays one voice. What ships is a plausible afrobeat-flavoured cell rather than a
cited one, and the file now says so out loud.

Grooves with no source behind them: down from 15 to 13.


## v0.102.0 — the six distinguished timelines

**SHIKO, SOUKOUS and GAHU corrected.** All three were undocumented and matched no
source. All three now sit on the canonical pattern, and the two long-standing
UNRESOLVED flags in the groove table are closed.

The thing that cracked it: shiko, son, rumba, soukous, bossa-nova and gahu are not
six unrelated grooves. They are one family. Toussaint's "The Geometry of Musical
Rhythm" (ch. 7) calls them the six distinguished timelines: six rhythms of five
strokes across sixteen pulses, each differing from the others by one or two
pulses. Diaz-Banez et al., "Measuring Musical Rhythm Similarity", prints the box
notation for all six in a single table.

Three of ours already sat exactly on it. Son, rumba and bossa-nova were correct
and are now annotated to say so. The other three were not:

    shiko     was 0,4,7,10,14   now 0,4,6,10,12
    soukous   was 0,3,6,8,11,14 now 0,3,6,10,11
    gahu      was 0,3,5,8,11,13 now 0,3,6,10,14

Each fix has a second source behind it, not just Toussaint.

**Shiko** cross-checks against Cuba. The shiko necklace is the same one Cuban
players call the cinquillo, and cinquillo doubled from eighths into sixteenths is
0, 4, 6, 10, 12. Two traditions, one answer.

**Gahu** is confirmed by Locke's own transcription. Johnston, citing Locke 1998
"Drum Gahu" p.124, describes a five-stroke timeline with inter-onset intervals of
3-4-4-2-3, beginning on an anacrusis, with the final onset landing on the
downbeat. Count 3-4-4-2-3 backwards from that downbeat and you land on 0, 3, 6,
10, 14. Identical to Toussaint, arrived at from the opposite direction. Gahu had
been carrying six strokes in two identical halves, which a five-stroke timeline
cannot be.

**Soukous** was byte-identical to tresillo, which cannot be right for two
differently named styles. It is now the soukous timeline: the son clave with its
last stroke pulled one sixteenth earlier. One caveat is written into the file
rather than hidden. Soukous's ensemble signature is really the cavacha, a
two-voice hi-hat and kick figure, and this engine plays one voice. It cannot
render a cavacha, so what ships is the timeline the literature files under the
name.

**SON CLAVE 2-3 and RUMBA CLAVE 2-3 documented.** Neither needs its own citation.
Each is its 3-2 parent with the two halves swapped, which is exactly what the
sources say a 2-3 form is, and the swap is now verified in the data and written
down.

Grooves with no source behind them: down from 20 to 15.

## v0.101.24 — THE ONE was not on the one

**THE ONE — corrected.** The preset accented beats 1 AND 3 equally, in two
identical halves. That is a half-bar pulse, and it gives beat 3 the same weight
as beat 1 - which loses the exact contrast the groove is named for.

Sources are unanimous and specific. PBS Sound Field: "most music of that era gave
heavy emphasis to the back beat, on the two and the four... What James Brown did
was he put the emphasis on the one, on the downbeat of the measure." Wikipedia's
Funk article: "a heavy emphasis on the first beat of every measure ('The One'),
and the application of swung 16th notes and syncopation".

Beat 1 is now the only accent. The surrounding sixteenths stay as weak strokes,
which is the other half of what the sources describe: "emphasizing the one
created space in the groove, so that the band could add syncopation to the other
beats."

**BACKBEAT annotated** rather than changed - it is correct at 2 and 4, and it is
the pattern THE ONE was invented against, so the two presets only make sense next
to each other. Said so in the source.

**TRESILLO and HABANERA verified.** Tresillo's onsets sit at steps 0, 3, 6, 8,
11, 14 - exactly 3+3+2 twice, matching Puget Sound's music theory text ("the
sixteenth-note version is known as tresillo"). Habanera hits 1, the "&" of 2, 3,
4, exactly as its own comment claims.

Unverified count is down from 23 to 20.

## v0.101.23 — Clave family verified; the bossa clave had six strokes

**BOSSA NOVA — corrected.** Wikipedia's Clave article gives the rule exactly: the
bossa nova clave "has a similar rhythm to that of the son clave, but the second
note on the two-side is delayed by one pulse." Applying that to our son clave
(1, the "a" of 1, the "&" of 2 | the "&" of 3, 4) delays beat 4 to the "e" of 4,
giving five strokes: **1, 1a, 2&, 3&, 4e**. That matches The Signal Beat's
transcription of the 3-2 bossa nova clave.

Ours had **six** strokes: an extra one on the "e" of 3 that son clave does not
have, beat 4 left undelayed, and an added "&" of 4. Every clave has five strokes,
so the count alone was a tell.

**The four claves verified and annotated.** Son 3-2, son 2-3, rumba 3-2, rumba
2-3 all check out:

- The son/rumba difference is the third stroke of the 3-side moving one sixteenth
  later - ours has son on the "&" of 2 and rumba on the "a" of 2, which is
  precisely what LANDR describes.
- Both 2-3 forms are exact half-swaps of their 3-2 forms, which is what the
  sources require: "3-2 and 2-3 are not two different rhythms... they are two
  directions of the same two-bar pattern."

A note on the ENCODING is now in the source above the clave block, because
misreading it is what caused the montuno to be "corrected" in the wrong direction
earlier in this session: 16 steps is ONE bar of sixteenths, with the two-bar
clave written in cut time across it.

**CUMBIA checked and left alone.** It looked wrong in the audit summary - a hit
on every eighth - but it is the guacharaca "chu-chucu" cell: accents on the
beats, weak strokes on the "&" and "a". The audit line does not distinguish
accent from weak stroke, which is a limitation of the summary, not a fault in the
pattern.

Unverified count is down from 26 to 23.

## v0.101.22 — Turkish and Balkan set: one misnamed groove, three verified

Wikipedia's "Aksak" article carries a table of pulse-counts, subdivisions and
names that makes this whole family checkable, and it settled four entries at
once. https://en.wikipedia.org/wiki/Aksak

**AKSAK → DEVR-I HINDI.** The article is explicit: "Strictly speaking, in Turkish
music theory the term refers only to the grouping of NINE pulses into a pattern
of 2+2+2+3." Our AKSAK was a SEVEN-pulse 3+2+2, which the same table names
Devr-i Hindi (Bulg. lesnoto / četvorno). The nine-pulse 2+2+2+3 that Turkish
theory actually calls aksak is already in the app - as KARŞILAMA, which is a
real Turkish 9/8 dance in that meter, so that entry stands. Renamed, with the
Italian origin string synced.

The pattern itself was already right: its accents land exactly on the 3+2+2
group starts. This was a label on the wrong rhythm, not a wrong rhythm.

**Verified and left alone, with sources now in the code:**

- RACHENITSA — 7-pulse 2+2+3. Wikipedia's table gives Bulg. Račenica as 2+2+3;
  the Bulgarian dances article agrees. Accents sit on the group starts.
- KOPANITSA — 11-pulse 2+2+3+2+2, accents at steps 0, 4, 8, 14, 18. Confirmed by
  the same table (Bulg. Gankino) and by Melodigging's "11/16 (2+2+3+2+2, e.g.,
  kopanitsa)".
- KARŞILAMA — 9-pulse 2+2+2+3, accents on every group start.

**ÇİFTETELLİ — flagged.** The D-K-T-K-T-D-D-T cell is the standard darbuka
teaching pattern, but I could not find a citable transcription fixing it to
specific sixteenths, and the rhythm differs between the Turkish and Greek
traditions that share the name. Recorded as unverified rather than asserted.

## v0.101.21 — African grooves: two errors found, two flagged, sources in the code

Started the source audit with the African set, where the risk of being visibly
wrong to a native player is highest.

**KPANLOGO — corrected.** Wikipedia's Kpanlogo article states the bell pattern
"is the same as the son clave pattern heard in Cuban music". Ours had a stroke on
the "e" of 3 where son clave has the "&" - one sixteenth early - so it was
neither the clave nor kpanlogo's bell. Now byte-identical to this file's own SON
CLAVE 3-2, which makes it self-checking.

**SOUKOUS — flagged, not guessed.** The audit found it byte-identical to
TRESILLO, which cannot be right for two differently-named styles. Sources agree
soukous's percussion signature is the *cavacha*: Wikipedia calls it "an
unyielding, fast-paced beat, most commonly referred to as cavacha", and World
Music Method describes cavacha as "a fast sixteenth-note hi-hat groove with
syncopated bass drum accents". That is a two-voice figure and this engine plays
one voice, so the honest options are a cavacha kick pattern or dropping the
preset. Recorded in the source rather than replaced with a guess.

**GAHU — flagged.** Two sources say the gahu timeline has FIVE strokes (Johnston,
citing Locke 1998; and a Grokipedia figure). Ours has six, arranged as two
identical halves, which a five-stroke timeline cannot be. Not rewritten: Locke's
transcription is the authority and I have not read it directly, and the
Grokipedia figure is AI-generated and hedged.

Every claim above is now a comment beside the pattern with its URL, so the next
person can check the source rather than trust the code.

**The audit script gained a duplicate check** (`intonare_groove_audit.py`), which
is what found the soukous error. It distinguishes documented matches - kpanlogo
genuinely should equal son clave - from unsourced ones.

## v0.101.20 — The montuno, corrected by ear and then checked

Daniele built the pattern he expected to hear on the custom grid. It differs from
the stored one at 10 of 16 steps, and the sources back it.

  his:     accents on 1, the "a" of 1, the "a" of 2, the "a" of 3, and beat 4
  stored:  accents on 1, 2e, 3, 4e

Two independent checks favour his:

- The tumbao a montuno locks to accents **"the and of 2 and the downbeat of beat
  4"** (Rhythm Notes; Piano With Jonny). His pattern hits beat 4. The stored one
  hits 4e and never beat 4 at all.
- The two sounded offbeats of tresillo are **bombo** (the "a" of 1 in cut time)
  and **ponche** (beat 4), and Wikipedia's Tumbao article identifies their
  consistent accentuation as what "gave the son montuno texture its unique
  groove". His lands both. The stored pattern landed neither.

It also shares three of five accents with the app's own SON CLAVE 3-2 and pushes
the other two a sixteenth later, which is the guajeo-against-clave relationship.

The reasoning is now recorded in a comment beside the pattern, because I have
already "corrected" this groove once this session in the wrong direction and a
future pass should not repeat that.

## v0.101.19 — The playhead outline stops lingering after stop

`grooveUpdateCursor()` writes `.gs-cursor` to three grids: the CLICK panel's
`.groove-step` cells, the VISUAL panel's `gvs-*` cells, and the main screen's
`gs-step-*` cells. `stopMetro()` cleared the first two and not the third - so the
one grid actually on screen kept its outline on whichever step happened to be
playing when you hit stop.

Cleared now, and cleared across every `gs-step-*` in the DOM rather than looping
to `groovePattern.length`, so switching to a shorter pattern cannot strand a
cursor on a cell past the new end.

## v0.101.18 — Groove names: stop splitting words, let the fitter do its job

The names were breaking mid-word - "MONTUN / O", "HABANE / RA" - and my previous
two attempts made it worse by treating it as a measurement problem. It is not.

Calibrated off the device screenshot ("MONTUN" spans 157px at 36px, so 0.727px
per character per font-px) against the real 172px column, the arithmetic is
unambiguous: **with wrapping between words only, all 60 names fit at 16.9px or
above**, and only FUNK 4-ON-THE-FLOOR reaches that. MONTUNO needs 24.4px on a
single line; HABANERA needs 21.5px. Both had enormous headroom.

So a word split was never necessary, and permitting it was the whole fault: the
browser resolved the overflow by breaking the word, which meant the fitter saw
text that already "fit" and had no reason to shrink. `overflow-wrap: anywhere`
did it, `break-word` still did it.

- `overflow-wrap: normal` and `word-break: keep-all`. Overflow is now resolved by
  shrinking, which is what the fitter was written to do.
- Floor lowered 17px to 16px. The worst case needs 16.9px for its longest word,
  so a 17px floor left it 0.1px short - and the only way the browser could
  resolve that was by breaking the word again.
- Verified arithmetically across all 60 names: none require a size below the
  floor, and none require a word split.

## v0.101.17 — The name fitter was measuring the wrong element

Measured from the device screenshot rather than guessed: "MONTUN" renders at
~36px - the fitter's MAXIMUM - across ~157 CSS px, in a name column that computes
to ~172px. Full "MONTUNO" needs ~183px, so it wraps. Two steps down to 32px would
fit it on one line. The fitter had stepped down zero times, which means its
measurement was never seeing the real constraint.

`#gsName` is `display: -webkit-box` with `-webkit-line-clamp` and
`background-clip: text`, and its own `clientWidth` does not report the limit
reliably through that combination. The fitter now measures the parent column,
which is a plain block and is the actual constraint.

The previous attempt - swapping `overflow-wrap: anywhere` for `break-word` -
addressed the symptom and not the cause, and on its own would not have fixed
this. It stays, because a mid-word break is still the wrong failure mode here,
but the sizing is what was broken.

## v0.101.16 — Groove audit: the name fitter, and a montuno correction I got wrong

**The name overflow.** MONTUNO rendered as "MONTUN / O" - a 7-character name in a
168px column that it fits at any size the fitter can choose. The cause was
`overflow-wrap: anywhere`, which splits inside a word as soon as the measured
column looks too narrow, combined with `_fitGrooveName()` running in the same
frame the groove screen becomes visible, when that column can still be resolving.
It guards against a zero width but not a stale one.

- `overflow-wrap: break-word` instead of `anywhere`. Every preset name fits the
  column at the fitter's 17px floor, so a mid-word break is always the wrong
  answer; shrinking is the right one.
- The fit runs again after two frames, so a measurement taken mid-layout cannot
  stick.
- The fitter always restarts from 36px. It set the size on every call but began
  from whatever was left over, so a name could stay smaller than necessary once
  the column widened.

**A structural audit of all 59 grooves.** Step counts divide evenly into beats
for 57 of them at 2, 3 or 4 steps per beat. The two exceptions - KARŞILAMA and
COMPOUND 9, both 9 steps over 9 beats - are correct: they are counted in nine,
not subdivided.

**And a correction to my own earlier change.** I rewrote the montuno pattern
this session on the reading that 16 steps meant two bars of eighths. The engine's
own comment settles it the other way: "Step duration = one bar duration / pattern
length - e.g. 16 steps in 4/4 = 16th notes." So SON CLAVE 3-2 is stored in cut
time, one bar of sixteenths, and decodes correctly as 1, 1a, 2&, 3&, 4. Under
that reading the original montuno accents 1, 2e, 3 and 4e - the "e" positions are
offbeat pushes, not downbeats, and the pattern was fine as written. Reverted.

## v0.101.15 — Share links stop showing the chooser first

Opening a shared daily flashed the module picker before the daily loaded.
Measured on a simulated cold-start deep link: the launcher was visible at full
opacity from 547ms to 1681ms - **1134ms of chooser** before the module took the
screen.

The logic was already correct and in the wrong place. `lnchShouldShow()` checks
`_intonareWantSkipSplash` and returns false for a deep link, and `lnchInit()`
hides the launcher when it does, with a comment naming this exact case. But the
flag is raised at ~116ms while `lnchInit` does not run until ~1020ms, so the
launcher had already built and painted; all `lnchInit` could do was hide
something the user had been looking at for 200ms.

- **The check moved to the pre-paint script**, where the pinned case is already
  decided. A deep link now means the chooser never paints at all, rather than
  painting and being taken away. The launcher is never visible on that path.
- Both arrival shapes are covered: the flag when Capacitor has already resolved
  the launch URL, and the URL itself read straight off `location` when it has
  not.

Normal launches are untouched: the launcher still appears on both non-pinned
paths, still stays hidden when a module is pinned, and the boot guard still
reports zero app-before-launcher frames across all five paths.

## v0.101.14 — SOSTENUTO stops running into DAMPER

The pedal column is 46px wide and "SOSTENUTO" needs about 47px at 10px Bebas with
1px tracking - sitting exactly on the boundary, so any font substitution or
rounding tips it over and it runs into the label beside it. That is the collision
on the piano's pedal row.

- The label is **SOST** now, matching the legend on the pad directly above it,
  which is what a player reads first anyway. It leaves margin rather than
  balancing on the limit.
- `white-space: nowrap` and `overflow: hidden` added to `.ppc-name`, so a long
  label can never bleed into its neighbour again.
- Both piano instances updated - the inline one and the full-screen one.

Left alone deliberately: DAMPER measures ~31px in the same 46px column, so it had
room and was not part of the fault. The pedal diagram elsewhere also says
SOSTENUTO, but its boxes are 64px with the text centred and the size already
tuned to fit, so it is a different situation.

## v0.101.13 — The tab bar was arriving after the module

The jar at the end of the handover was not the animation - it was the navigation
turning up late.

The tab bar carried a `.30s` transition delay, added so it would not start moving
mid-handover. With the faster morph that delay now landed AFTER the module was
already on screen: measured the launcher gone at 715ms, the morph gone at 788ms,
and the bar only beginning to move at 821ms. So the module appeared complete, and
then its navigation slid up as a separate event about a tenth of a second later.

- **The delay is gone.** The bar now leads the uncover rather than trailing it:
  on a card launch it starts at 508ms and lands at 788ms against a cover that
  clears at 712ms; on a pin launch it lands at 692ms against a cover clearing at
  692ms - exactly together.
- **Zero frames on either path** where the module is on screen without its tab
  bar, down from 6 on the card path.
- It also picked up the same ease-out curve as the rest of the entry, instead of
  the springy `cubic-bezier(.22,1,.36,1)` it was using.

Checked and found correct: the palette swap happens at 409ms with the launcher
still at full opacity, so the module is already wearing its own colours before
anything uncovers. That was not the cause.

## v0.101.12 — Motion polish on the first thing anyone does

The launch sequence was running on three different easing families at once. This
standardises the whole path on one idea: anything ARRIVING uses ease-out, so it
enters at speed and settles, which is what iOS does for touch-triggered motion.

- **The picked card was on an ease-IN-out curve.** `cubic-bezier(.36,0,.28,1)`
  ramps up from a standstill, so the first ~110ms after a tap produced no visible
  movement - measured 0px across three frames, then 10px/frame once the curve got
  going. That stall before the card commits is what read as jitter. Now
  ease-out: motion starts at 12.6px/frame and decelerates.
- **The launcher entry used Material's `.4,0,.2,1`**, which also accelerates into
  the motion. The launcher surface, the module cards, the quick pins and the hint
  all now share `cubic-bezier(.22,.61,.36,1)`, close to UIView's curveEaseOut.
- The hint was on a bare `ease`, which is symmetric and ramps both ends - on an
  arrival that reads as hesitant.
- Durations nudged from .34s to .38s on the surfaces that carry the entry, since
  an ease-out spends less of its time visibly moving than a symmetric curve.

Checked and left alone: `setMode()` costs 1-2ms for every module, so it is not
what delays the morph. The residual gap before motion in the container is the
headless harness's frame scheduling, not the app - worth stating because it looks
like a stall in the trace and is not one.

Boot, note fit and launch all re-verified: five boot paths with zero leak frames,
combined coverage never below 99%, every note inside the ring, and the pin launch
still uncovering a finished module.

## v0.101.11 — The skip-splash boot stops flashing, and the note fits its circle

A 120fps screen recording made the boot problem measurable: five distinct visual
states across ~1.7s before the module picker, including ~200ms of pure black.
Decoded from the frames - 16,000 colours at full brightness, then 3,500, then 11
colours at 79% flat, then two more states - which matches "three or four quick
card flashes, a background, something else, the tuner" exactly.

- **The boot guard was released 1.4 seconds too early.** `boot-ready` fired at
  263ms while the launcher did not reach full opacity until 1670ms, so the app sat
  uncovered underneath while the launcher slowly faded in over it. The reveal now
  waits for the launcher to be doing the covering on that path; the veil covers
  the gap, and combined coverage never drops below 99% at any frame.
- **The veil was lifting ahead of the launcher.** Both fades are .34s, but the
  launcher's starts a frame or two later - measured the veil at 0 with the
  launcher still at 0.82, a ~170ms window with nothing covering. The veil is held
  260ms so the two overlap instead of racing.
- **The launcher is covered by the boot guard too.** It ships visible so the
  pre-paint script can decide synchronously whether to keep it, which also meant
  it painted its own ground before that script ran.
- **The module-select morph was three events, not one.** ~105ms of nothing, a
  burst of 10px/frame, then a 270ms crawl at 0.1px/frame where it looks stopped,
  and only then the fade. Shortened .58s to .42s on a curve without the dead tail,
  dropped the .04s start delay, and moved the fade from 420ms to 300ms so it
  overlaps the travel rather than following it.
- **The note letter overflowed the ring.** 68px type in a circle of radius 45.3px:
  the glyph's corner reached 47px, outside the ring. The strip below gave up 6px
  of padding so the circle grows to 112.5px (R 47.3), and the note comes down to
  60px - corner now 42.5px, clearing with margin at every note including the
  sharps. Ring still square, face still 194px, meter still exact.

## v0.101.10 — Clipped on the other axis too, and the grow was overdoing it

v0.101.9 gave the launch grow vertical headroom and left the horizontal alone, so
the leftmost chip was still cut 6px on its left edge - the same bug, the other
axis. Padding on both sides now, pulled back by matching negative margins so the
row's position and scroll origin are unchanged: the first pin still starts at
x=29, and the grid, hint and row all hold their positions.

Checked every position rather than just the one reported: leftmost, middle and
last, in a 3-pin row and an 8-pin row, and at three scroll positions in the
scrolling case. All clear by 5px or more on every side.

**The grow is smaller.** 1.18 was sized when it had to carry the cover on its
own; the three-phase timing is really doing that work, so it comes down to 1.09
with a 3px lift instead of 6px. The unpicked chips also step back less - .3
opacity rather than .18, which was reading as a separate effect rather than the
row deferring to one of its own.

## v0.101.9 — The grow had nowhere to grow

The launch grow was clipped 10px at the top. The chip lifts -6px and scales to
1.18, but the pins row is a horizontal scroll container, and `overflow-x: auto`
forces overflow-y into a scrollport too - so `overflow-y: visible` is ignored by
spec and there was nothing to do but clip.

Fixed with 12px of top padding for the grow to expand into, pulled back by an
equal negative margin so nothing below moves. Measured after: the grown chip sits
2px INSIDE the row's bounds with 6px spare below, and the grid, hint and row all
hold their positions at both 915px and 800px viewports.

**On whether the card path loads under cover too - it does, and with more room
than the pins:**

| | module built | cover after build |
|---|---|---|
| card | 43ms (`setMode` runs before the morph starts) | ~530ms |
| pin | ~205ms (during the chip grow) | ~140ms |

The card gets the whole morph as post-build cover because `setMode` is called
first, then the clone grows for ~500ms on top of an already-finished module. The
pin's cover is shorter but still comfortably clear of the worst measured build
(81ms). Verified by sampling `elementFromPoint` every frame on both paths:
neither shows the app before the module.

## v0.101.8 — A pin grows, the module loads behind it, then the launcher fades

The pin launch is three phases now, and the middle one is the point.

1. The tapped chip grows in place - larger and slower than a press nudge, so it
   reads as the chip becoming the module rather than acknowledging a tap. The
   rest of the row steps back.
2. **The module is built while that grow is on screen**, with the launcher still
   fully opaque. Measured launch cost across all 26 favourites: 4ms median, 81ms
   worst - the exercises, which build more UI, not the tools as expected. Piano
   and Charts are 2-4ms. A 150ms grow covers the worst case comfortably.
3. Only then does the launcher fade, so it uncovers a module that is already
   finished instead of one assembling itself in view.

Verified with `elementFromPoint` sampled every frame through the handover: by the
time the fade starts, the module's own content is what is painted at screen
centre, and there are **zero frames where the app shows before the module** -
including on the slowest entry in the roster.

The first attempt left a 330ms hold on a static grown chip: two
requestAnimationFrames were waiting for a build that takes 4ms, and the outer
timeout did the rest. Trimmed to one frame, and the total is ~580ms with nothing
sitting still in the middle.

## v0.101.7 — The launcher never actually faded out

Tracing the exit the same way as the entry found a bug older than the pins: the
launcher's fade-out has never run. `.lnch-gone` sets `opacity: 0`, but the entry
state `.lnch-nosplash-in` sets `opacity: 1` at the same specificity and LATER in
the sheet, so the exit lost on source order. Isolated test - add the class with
nothing else running, sample for 600ms - opacity held at 1 and then the element
was displayed none. Confirmed with reduced motion both on and off.

A card launch hides this completely: its morph clone grows 164x268 to 278x456 and
carries the eye while the chooser cuts underneath. A pin launch has no morph, so
it showed the cut plainly - which is why it looked abrupt next to a card.

- **`.lnch-gone` is `!important` now.** It is the exit and has to beat every
  entry state. Measured afterwards: 20 distinct opacity values over ~330ms, a
  real ramp, on both paths.
- **A second bug found on the way.** The rule that cancels colour cross-fades
  inside the chooser included `body #lnch` itself, which restricted the
  launcher's own `transition-property` to a colour list and made opacity
  untransitionable regardless. Scoped to descendants, which is what its own
  comment describes.
- **Pins get a launch acknowledgement.** The tapped chip lifts and lights while
  the rest of the row steps back, so the module reads as coming from the thing
  you touched. Deliberately not a morph: growing a 72px chip to fill the screen
  would be a different gesture rather than a matching one.
- The pin path also now holds the palette swap under cover and releases it the
  way `lnchGo` does, so the module's colours no longer flash in around the
  chooser during the handover.

## v0.101.6 — The entry plays in the right order, and during the dissolve

Asked to state exactly what should be visible, the trace answered instead - and
showed the sequence was wrong in three ways.

- **The hint arrived FIRST, alone.** It had its own .72s delay, so a line of
  small grey text faded up on an empty launcher roughly 200ms before the four
  cards it describes. It now rides the same class as everything else and trails
  them.
- **The cards arrived AFTER the splash had fully gone** - 167ms of empty launcher,
  then a grid appearing on top of nothing. They now start while the splash is
  still fading (measured 66ms before it clears), so it hands over to a grid that
  is already forming. That is what the entry was designed to do and had stopped
  doing.
- **It was slow.** 767ms of arrival on every single launch, now 599ms, with each
  element's fade trimmed from .42s to .34s.

Measured sequence, splash-on path: splash begins fading 5693ms, cards 5793-5959
(overlapping the dissolve), pins 5959-6192, hint 6026-6292. Cards, then pins,
then the hint - reading order, with the modules first because they are what the
screen is for.

The hint's delay needed !important for the same reason the pins' did: the
app-wide `*` transition rule replaces the whole shorthand, so without it the
delay is dropped and the hint fades in lockstep with the cards rather than after
them.

## v0.101.5 — One fade, and it happens after the handover

Three passes at re-timing the stagger never helped because the stagger was never
the problem. The measurement that found it: the veil fades OUT in lockstep with
the launcher fading IN - veil .93 against card .07, veil .42 against card .58,
veil .07 against card .93. They cancel each other, the screen's net brightness
barely moves, and the eye reads one soft reveal rather than anything arriving.

That crossfade is deliberate and stays - it is what keeps the app underneath from
ever being uncovered. What changed is WHEN the contents arrive.

- **The launcher surface still covers immediately**, doing its half of the
  handover exactly as before. Only the cards and pins wait, on a new `lnch-in`
  class set a beat after the veil is gone - so the fade has a settled background
  to be seen against instead of a disappearing overlay.
- **Every stagger is gone**, on both entry paths and on the pins. Staggering
  inside a crossfade only smears it, and the delays were tuned for a rise that
  no longer exists.
- **The rise is gone too.** One calm opacity fade, which is what was asked for
  and what is actually perceivable here.
- Measured: the veil completes 1 to 0 by 1531ms with the cards still at 0, and
  they fade from 1704ms afterwards. Boot guard still reports zero
  app-before-launcher frames across all five paths, and both cards and pins are
  visible on every path where the launcher is shown.

## v0.101.4 — The launcher entry finally happens where you can see it

Both symptoms had one cause, and it was older than the pins.

The module cards' stagger was written against "the splash's 1.3s dissolve", but
the splash actually runs about three and a half seconds - its own comment says
so, and the two numbers never agreed. Traced frame by frame, the cards rose and
settled at **1457ms with splash opacity still 1**. Verified in a control build
with the pins stripped out entirely, so this predates them: the grid has been
finishing its arrival behind an opaque overlay and then simply being uncovered.
That is the jank - not motion, but the absence of it where motion was expected.

v0.101.3 fixed the pins by hanging them off the splash's real dissolve event, and
that left the cards on the old assumption - so the two halves of the launcher
arrived four seconds apart.

- **One gate for both.** `_lnchWhenVisible()` runs its callback when the splash is
  dissolving, has finished, or never ran, with an unconditional 4.2s fallback.
  `lnch-entering` now comes off through it, and the pins release through it.
  Nothing is timed against an assumed duration any more.
- **The designed effect works now.** Measured: the cards rise from 5305ms as the
  splash passes 0.08 to 0, the pins follow from 5338ms, and the whole entry plays
  THROUGH the fade - which is what the original comment describes and what was
  never actually visible.
- Verified across all four entry paths, plus the boot guard's five: cards and
  pins both arrive on the two paths where the launcher is shown, both correctly
  untouched on the pinned paths where it is not, and zero app-before-launcher
  leak frames throughout.

## v0.101.3 — The pin animation was running where nobody could see it

You were right that there was no animation, and v0.101.2's verification was
wrong. The transitions were firing correctly - they were just finishing
underneath the splash.

Measured with the browser's own `transitionstart` events: all four pins animated
at **1610-1720ms while the splash was still at full opacity**. By the time it
dissolved the row had long since settled, so it appeared fully formed. The module
cards do not have this problem because their stagger is deliberately timed to be
watched THROUGH the dissolve; the pins, added later on a copied delay, landed
before it.

- **The release is now an event, not a delay.** A fixed number cannot work here:
  the splash waits on fonts, sample preload and the viewport settle, so its real
  length is not a constant - measured well past 2.2s in the container against the
  1.3s the design assumed. The row is held hidden until `.lnch-qa-in` is set,
  which hangs off the splash's own dissolve, its completion, and the no-splash
  path's viewport settle.
- **A hard 4.2s fallback fires first and unconditionally**, so a missed event can
  never leave the row invisible.
- Verified across all four entry paths. The first attempt broke the skipped-splash
  case - that path returns early from `lnchInit` and never reached the release, so
  the row stayed hidden - caught by testing every path rather than only the one
  being fixed.
- With the splash on, the pins now animate as its opacity passes 0.08 to 0. With
  it skipped, they animate during the veil crossfade. Both are the moment the
  launcher becomes visible.

On the verification itself: v0.101.2 claimed the animation worked because
computed styles and `transitionstart` both reported it running. They were telling
the truth about the transition and nothing about whether it was on screen. A
control build with the change removed behaved identically, which is what showed
the measurement rather than the code was the problem.

## v0.101.2 — The pins arrive like the cards do

The quick-access row faded in as one block while the four module cards above it
rose and staggered. Same screen, same arrival, so it now uses the same gesture -
rise and fade - scaled to the object.

- **A smaller lift and a tighter step.** The cards travel 14px on an 80ms stagger;
  the pins travel 8px on 40ms, because they are smaller buttons and there can be
  eight of them - 80ms each would have run the entry on far too long. Capped at
  six: past that the remainder arrives with the sixth, since a stagger nobody can
  follow is just latency.
- **The delays needed `!important`.** All nine computed to 0s without it and every
  button arrived at once: the app-wide `*` transition rule replaces the whole
  shorthand, which is the same trap that flattened the launcher entry in v0.99.32
  and the tab bar's slide. Measured 0.70 / 0.74 / 0.78s afterwards, and traced in
  motion to confirm they actually cascade rather than merely computing correctly.
- **Press feedback survives it.** The entry rule gives transform a .46s duration
  so the buttons can rise, and a tap inheriting that would take half a second to
  respond. `:active` re-states .09s and, at ID specificity, wins - verified at
  `scale(0.96)` and `0.09s`.

Worth recording: the press appeared broken through several rounds of testing
because a synthetic mouse-down does not hold `:active` on a button that has a
click handler. Forcing the pseudo-state through CDP showed the CSS had been
correct for some time. The harness was wrong, not the app.

## v0.101.1 — The launcher hint mentions quick access

With no pins the row hides itself, so nothing on the launcher suggested the
feature existed. The hint line now carries it:

> Pin a module here · star tools for quick access

Deliberately NOT an empty-state row. The hint above it is always on screen in
both states, so an empty shelf saying "star tools to pin them here" would put two
different meanings of "pin" side by side on the one screen where a new user is
already working out what pinning does - pinning a MODULE skips the grid, starring
a TOOL adds it to a row. One clause on the existing line teaches the second
without competing with the first, and the star sheet still does the real teaching
at the moment you can act on it.

- The Italian is not a literal translation: "stella gli strumenti per l'accesso
  rapido" wraps to two lines at 320px, and a wrapped hint reads worse than no
  nudge, so the shorter "stella per l'accesso rapido" ships instead. Both
  measured at one line at 320 and 393px.

## v0.101.0 — Quick access on the launcher

The launcher asks "which module". Quick access already knows what you actually
do. So the pinned list now sits under the module grid: open the app, tap DROP D,
land on the chart.

- **Built from the same `progState.favorites` the star sheet manages**, so there
  is one place to pin things and two places to reach them - the launcher never
  becomes a second inventory to keep in sync.
- **Saved chart views come first**, ahead of tools and exercises. "Open the app
  and go straight back to my Drop D chart" is the case this exists for, and a
  saved view carries more context than a bare tool.
- **Colour carries the type**, reusing the fav sheet's own vocabulary: cyan
  tools, purple exercises, green saved views. No new language to learn.
- **It scrolls rather than wrapping.** Measured 292-312px of usable width, so
  three fit without scrolling and five sit at 54-58px each; beyond that the row
  scrolls. A wrapping list would change the launcher's height as the pin list
  grew, pushing the four module cards - the thing the eye lands on first - down
  the screen. The launcher being the same shape every time is what makes it fast.
- **No pins, no row.** It is `hidden` entirely rather than showing an empty
  shelf.
- Stale keys are skipped quietly, so a favourite left over from a removed tool
  cannot take the row down with it.

Two things worth recording. `.lnch-pin` was already taken - it is the
absolutely-positioned pin badge on each module card - and reusing it stacked all
eight buttons at the same coordinates; the row is `.lnch-qa` now. And the
document-level `touchmove` blocker that would have killed the horizontal scroll
on device turned out to be correctly scoped to the Survival Guide, so it does not
reach the launcher; checked rather than assumed, since it would have looked fine
in a desktop browser either way.

## v0.100.17 — Picking an instrument lights the panel too

Choosing an instrument and going back to the picker both snapped: the change is a
plain `display` toggle on the setup strip, with nothing between the two states.
They are the same event as a face swap - the glass showing something different -
so they now use the panel's own re-light rather than a separate effect. One
visual language for "the screen changed", not three.

- `_sfRelight()` replays the same `sfScreenOn` glow the face swap uses: opacity
  0 -> 1 with brightness settling 1.55 -> 1.06, no transform. Traced on both
  legs; picking and clearing ramp identically.
- Retrigger-safe by the same means as the face swap - the class is removed and a
  reflow forced before re-adding, since an animation will not restart while its
  class is already present. Verified firing across five consecutive transitions
  (pick, clear, pick, clear, chromatic) with state intact each time: pips, the
  tuning list and the strip label all correct.
- The face swap, the guide's independence from Simple, and the meter geometry are
  all unaffected.

## v0.100.16 — Less cathode ray, more lit segments

The squash-and-overshoot read as a glitch, and it was the wrong reference. A tube
collapses its beam vertically because there is a physical thing bouncing; this
glass is a lit segment display in a bezel - amber and cyan glyphs on dark glass -
and segments have no inertia and no geometry. Any transform on them is a jump,
not a screen.

- **The transform is gone entirely.** Verified across four consecutive swaps:
  peak scaleY deviation is now exactly 0, where the CRT version measured 0.14.
- **All the character is in the glow ramp now**, which is what a VFD actually
  does: the segments strike over-bright and settle. Traced frame by frame,
  brightness 1.55 -> 1.31 -> 1.12 -> 1 with a matching saturation lift, while
  opacity rises 0 -> 0.54 -> 0.9 -> 1.
- Slightly gentler than the CRT version too: the brightness peak drops from 1.9
  to 1.55 and the duration from .34s to .30s, since without the geometry move the
  bloom is doing all the work and does not need to shout.

**On the transport bar:** it was genuinely left out, and it stays out - but not
for want of trying. The row sits inside `#tunerReadout`, and that subtree is
`display: none` during the swap itself, so an animation started on it never gets
a start time and freezes on its first keyframe. Two attempts to drive it
separately both stuck: once at `opacity: 0` for the entire ramp, once at
`brightness(1.5)`. Since the readout it belongs to already re-lights as one
object, the row travels with its parent, which is the correct behaviour anyway -
the chrome and the numbers are the same panel.

## v0.100.15 — The glass re-lights instead of cross-fading

The face swap dissolved its contents: 100ms out, 300ms in, pure opacity. That is
a slideshow gesture. A real display does not dissolve between two pictures - it
blanks and re-lights, and the character comes from how the panel responds, not
from the content's opacity.

The app already had that vocabulary: the tonal-centre CRT's `tcPowerOn` does a
brightness overshoot with a vertical squash that settles. The face swap now
borrows the same grammar rather than inventing a second visual language for the
same idea.

- **`sfScreenOn`**: the arriving face starts blanked and squashed to 0.86 on Y at
  brightness 1.9, snaps past 1.0 to a 1.03 overshoot, then settles. Traced frame
  by frame: 0.86 -> 1.03 -> 0.995 -> 1.0, brightness 1.9 -> 1.35 -> 1.06 -> 1.
- **Y only, never both axes.** A display's image collapses vertically; scaling
  both reads as a zoom, which is the PowerPoint move being replaced.
- The out-leg is a blank rather than a fade (60ms linear, and the dark gap
  shortened from 90ms to 70ms), so the panel cuts and comes back rather than the
  two faces overlapping.
- Retrigger-safe: the class is removed and the reflow forced before it is
  re-added, so the animation replays on every swap. Verified firing in both
  directions across four consecutive swaps with identical amplitude, and it
  respects `prefers-reduced-motion`.
- The surrounding choreography is untouched: the screen still never resizes, the
  card still sheds its 149px on the .42s curve, and the card sheen still holds
  still.

## v0.100.14 — The sheen that actually moved

v0.100.13 fixed the wrong reflection. There are two: the glass shine on the
screen, and a second sheen on the CARD behind it - and the card one was the one
being pushed around.

`.tuner-bpm-card::after` was sized as a percentage of the card (`top: -60%;
height: 200%`). The card's height animates on a face swap - traced frame by
frame, 481px down to 332px over .42s - so that highlight's height ran 962px to
664px and its anchor slid the whole way with it. Anchored in px now (`top:
-180px; height: 620px`), it holds still at exactly those values across the entire
transition while the card resizes underneath.

The same block appears **three** times - the tuner card declares it twice,
identically, and the metro card is built the same way. All three are fixed, since
the later declaration would otherwise win and undo the earlier one. The
`assert count == 1` in the edit script is what caught this; the first attempt
would have patched one copy and left two.

**On the swap feeling like a bigger change than a readout:** it is, and it is
deliberate. Measured across a swap, the screen holds perfectly still (256px, same
y) while the card sheds 149px and the guide below it moves up 149px and shrinks
139px. The existing design note is explicit that this is intentional - the glass
never resizes because that would be "animating a lie", and the card and guide
carry the sense of the layout rearranging. An attempt to also collapse the bottom
section on the same curve made it worse, not better: the section animated first
and the card only snapped afterwards, turning one movement into two. Reverted.

## v0.100.13 — The glass reflection sits on the front in both faces

The glare was never moving. The housing, the bezel, the glass and the gradient
itself measure pixel-identical between the two faces - same box, same 443.78 x
238px pseudo-element, same peak column. What differed was which SIDE of the
content it was drawn on.

`.tuner-screen-inner::before` carried `z-index: 1`, but `#simpleFace` is
`z-index: 2`. So the simple face had its highlight painted BEHIND the setup
buttons and the pips, while the full face - whose readout has no stacking context
- had it in front of the readout. One gradient, opposite sides of the content,
which is what read as the light having moved when you swapped.

- The shine is now `z-index: 3`, in front of the content in both faces. A
  reflection is on the front of the glass either way.
- Verified the highlight peaks at the same column and the same brightness in the
  full face, the simple setup screen and the simple readout, and that the
  content underneath is unaffected: the setup buttons measure 10.17:1 with the
  shine over them, since it peaks at 0.07 alpha.

## v0.100.12 — "PLAY A STRING" stops showing before there is a string

A regression from v0.100.9, and the rule that should have caught it was already
there: `body.sf-needs-pick` stands the readout down while you are choosing,
because there is nothing to read yet. The state line used to live inside
`.sf-core` and was hidden with it. Moving it out of the ring - so it would stop
crossing the dial - quietly took it out of that rule's reach, so the setup screen
told you to play a string before you had said what you were tuning.

- `.sf-state` joins `.sf-core`, `.sf-pips` and `.sf-chosen` in the needs-pick
  rule. The setup screen is now just the question.
- Checked all four states rather than only the one reported: while choosing, only
  "WHAT ARE YOU TUNING?" shows; after picking, the ring, pips and state line all
  return; chromatic keeps the ring and the state line but has no pips, which is
  correct; and clearing the instrument goes back to the bare question. The face
  still holds its 194px with 22px of clearance in every one.

## v0.100.11 — Each face gets its own tuning list

v0.100.10 stopped Simple from overwriting the guide, but it took Simple's own
tuning list with it. The card under the glass rendered from the guide's
`selectedFamily`, so once Simple stopped setting that, the list came up empty:
picking a family gave you pips and nothing to change the tuning with.

The card is shared markup serving two independent selections, so it now renders
for whichever face is showing.

- **Simple has its own family** (`sfFamily`) alongside its own instrument, and
  `buildInstList` reads Simple's pair in the simple face and the guide's in the
  full one. Its pills call `sfPickInstrument` rather than the guide's
  `selectInstrument`, which was the coupling this whole change existed to remove.
  The Reference tool keeps using the guide's selection.
- **The card is rebuilt on every face swap.** One list serving two selections
  otherwise keeps whichever face built it last.
- **Two leftovers from the split, both caught by testing rather than reading.**
  `_sfSyncChosen` still read `selectedInstrument`, so the strip on the glass
  showed "—" instead of the instrument Simple was actually tuning. And the entry
  path still built the pips from `selectedInstrument`, so the row could show the
  guide's tuning while detection measured against Simple's.
- Verified end to end: the guide holds drop D on the guitar tab with 12 pills and
  its chip, while Simple independently holds a 5-string bass with 4 pills, its own
  chip and 5 pips; changing the tuning inside Simple's list moves only Simple;
  swapping faces changes neither; and detection targets the right instrument on
  each face.

## v0.100.10 — Light-mode chips, matching pips, and two pickers that stop fighting

- **The selected tuning was the hardest thing to read in light mode.**
  `.inst-pill.active` hardcoded the dark-mode cyan for its text, fill and
  sub-label with no light override, so on the light panel the chip telling you
  what you are tuning measured **1.29:1**. It now uses the light palette's own
  accent: 5.80:1 for the label, 4.69:1 for the sub.
- **The string pips did not match the picker beside them.** They carried their own
  light override at 5% fill / 13% border, which sat under the v0.100.9 base fix
  and left them far fainter than the family buttons on the same glass. Both are
  now #00536c at 14% fill / 40% border - two controls doing the same job on one
  screen should not be two different weights.
- **Simple and the string guide are independent now.** Simple's picker called
  `selectInstrument()` and `selectFamily()` - the guide's own setters - so
  answering "what are you tuning?" on the glass silently replaced a specific
  tuning chosen in the guide, swapped its family tab and dropped its active chip.
  Entering Simple did it again on every swap, which is why the guide always came
  back showing Simple's choice. Simple now holds its own `sfInstrument`.
- The coupling is kept in the direction that was always deliberate: the guide is
  where a specific tuning is chosen, so it still pushes down to the glass. That
  push is now unconditional - while it was gated on the simple face being
  visible, changing the tuning from the guide left Simple's target stale, and the
  next swap rebuilt the pips from one instrument while detection measured against
  another. Verified: guide set to drop D survives a bass pick in Simple with its
  tab, all 12 pills, active chip and 6-string grid intact, while Simple
  independently holds bass4 - and a tuning chosen in the guide still reaches the
  glass with pips, saved state and detection target all in agreement.

## v0.100.9 — The state line leaves the dial, and the readout gets a body

**The meter works and is correctly aligned.** Driven with simulated pitch rather
than the mic: the dot at 0 cents lands exactly on top of the circle (0.00px error
on both axes), note detection and closest-pip highlighting track correctly, and
the per-pip bar fills to exactly 25% at 25 cents and 50% at 50. The small values
seen on the first frame are the smoothing filter ramping, not a bug.

- **"PLAY A STRING" has left the ring.** It sat below the note, which put it
  32.8px below centre and 28.4px from the bottom arc - crossing it. Moving it
  above the note failed the same geometry in mirror image. The real constraint:
  the longest state, "TOO HIGH - LOOSEN", is 117.6px wide and the widest chord the
  circle offers is 104.5px, so NO position inside the ring works. It now has its
  own row between the dial and the pips, where it reads as a status line for the
  readout rather than a label painted on the dial. The ring pays 14px for it
  (108.5px with pips, still a perfect circle).
- **The readout's own elements got the treatment the picker got in v0.100.6.**
  The pips were `accent 4%` fill on `12%` border - the same colour as the glass,
  so the string buttons had no body, only a hairline. Now 12% fill and a 38%
  border. The note letters went 55% to 88%, their octave numbers 30% to 62%, and
  the instrument name under the dial 62% to 85%.
- The state line itself was 40% transparent, measuring 2.97:1. It carries the
  actual instruction, so it should not be the faintest thing on the glass; now
  5.48:1.
- Ring verified square (ratio 1.000) at 320-430px in both palettes, with 4- and
  6-string tunings and in chromatic, and the face still holds its 194px contract
  with 22px clearance.

## v0.100.8 — The simple face's dial is a circle again

Long-standing, not a regression: confirmed squashed in a v0.99.51 build too. The
recent colour work only made it easier to see.

The face is pinned to a hard 194px on purpose - it has to reproduce exactly the
inner height the full readout had, or the housing resizes when you swap layouts
and the screen stops reading as one physical object. Inside that, the ring was
sized WIDTH-first: `width: 100%`, capped at `max-width: 156px`, with
`aspect-ratio: 1` expected to supply the height.

But `.sf-core` only ever has ~117px of height to give, once the pips row (42.5px)
and the instrument strip (34px) take their share. So `max-height: 100%` overrode
the aspect ratio and the "circle" rendered **156 x 122.5** - a 1.33:1 ellipse sat
inside a round bezel, with everything around it pressed to the edges. A square
156px ring needs 227.5px in a 194px box, a 33.5px deficit, so the ratio could
never hold whatever single width was chosen.

- **The ring is now sized from its height instead**: `height: 100%; width: auto;
  max-height: 156px`. The aspect ratio becomes the thing that holds, and the wrap
  simply takes whatever height the row leaves and derives its width from it.
- This also fixes the state the fixed width could never serve. Chromatic hides
  the pips, so it has 160px of height available: it now renders a full square
  156x156, while a 6-string guitar renders 122.5x122.5. Both circular, one just
  larger - the ring grows when there is room rather than stretching sideways.
- Verified square (ratio 1.000) at 320, 360, 393, 412 and 430px, in light and
  dark, with 4-string and 6-string tunings and in chromatic. The face still holds
  its 194px contract with 22px clearance inside the glass, and the canvas backing
  store re-measures correctly (369x369 at DPR 3, uniform scale on both axes).

## v0.100.7 — The flash guard stops depending on where it sits in the file

The pre-paint veil was correct and is still doing its job: traced frame by frame,
every boot path (splash on, splash skipped, pinned, and localStorage throwing)
showed zero frames of the app before the module grid. But the guard depended on
something fragile - the veil is created by an inline script sitting 1.49MB into
the document, roughly 5KB AFTER the .app markup. In an ordinary load nothing has
painted by then, so it wins. Any host that paints an intermediate parse state -
a preview wrapper, a streamed load, a WebView that flushes early - can show the
bare app before that script exists. Position in the document is the wrong thing
to bet on.

- **The app is now hidden from the first byte**, by a rule at the very top of
  <head>: `html:not(.boot-ready) body > .app { visibility: hidden }`. This cannot
  lose the race, because it applies before any body markup is parsed at all. The
  existing boot script clears it the moment the veil, splash or launcher is in
  place, so nothing uncovers a bare tuner.
- **The failsafe lives in <head>, not in the boot script it protects.** Putting it
  inside would have traded a brief flash for a permanent blank screen on any path
  where that script is never reached - verified by truncating the document before
  it: the app stayed hidden forever, and now recovers to visible. An independent
  1500ms timer next to the rule it undoes closes that.
- Verified across five boot paths: reveal fires between 136ms and 987ms, zero leak
  frames, and every path ends with the app visible and the grid built.

Note for the html preview specifically: it renders the file through its own
wrapper, so its paint timing is not the app's. This change removes the app's
dependence on that timing, but a preview is still not a measurement of the
packaged build - the Android/iOS WebView loads the file directly.

## v0.100.6 — The screen is meant to stay dark, and the dead brightness palette is gone

Two answers and a correction.

**lt-bright was dead code, and it is now removed.** `lightBrightSetting()`
migrates any stored 'bright' back to 'soft' and then hard-returns 'soft', so the
class could never be applied and every rule under it was unreachable. Removed 11
CSS rules (~3.4KB) plus the two JS toggles that could only ever pass false.

**v0.100.5's light tint was a mistake, and it is reverted.** The tuner screen
carries `.keep-dark`: it is a signature surface that holds the dark palette in
both modes, framed inside light chrome like a video player on a light page.
Tinting its glass toward paper fought that architecture, which is exactly why the
buttons on it did not improve. The tick and FLAT/SHARP lifts from that pass were
independent of the tint and survive the revert at 6.19:1.

**The faint buttons were never about the glass.** Their fill was
`color-mix(accent 4%, transparent)`, which measured the same colour as the glass
behind them - the cards had no body, only a hairline. Worse, because the screen
is `.keep-dark`, `--accent` inside it is the dark cyan in *both* modes, and cyan
over pale glass cannot separate at any strength: every value tested landed
between 1.03 and 1.05:1. Light mode therefore needs a dark ink rather than more
accent.

- Family buttons: 12% fill and 38% border, with light mode overridden to a
  #00536c fill at 14% and a 40% border. Separation against the glass went from
  1.06:1 to 1.26:1 in light and 1.24:1 in dark; the labels stay at 8.9:1 and
  5.9:1.
- CHROMATIC measured 2.60:1 light and 1.95:1 dark - the faintest thing on the
  screen despite being a real choice beside the five families. Now has a fill, a
  42% dashed border and 78% ink.
- The "what are you tuning?" prompt went from 40% to 75%.

## v0.100.5 — The light screen reads as glass instead of paper

Tint B from the preview, plus the tick lift that went with it.

- **The screen glass was #f9fbfd to #e8eff6 - luminance 0.90, effectively
  paper.** The scanlines, the inset shadow and the bezel's highlight all had
  nothing to sit on, so the panel never read as lit. The soft default is now
  #e8f1f3 to #d2e1e6, luminance 0.82, and the readouts barely move: FREQ 8.33:1,
  OCT 8.91:1, cents 7.43:1.
- **The chroma strip moved with it.** It is the same pane of glass to the eye and
  sits directly under the main screen; leaving it white would have split the
  instrument in half.
- **The meter ticks went from 3.01:1 to 5.69:1.** They were already marginal on
  white and would have sat lower on tinted glass, and they are the scale the
  needle is read against.
- **FLAT and SHARP got the same lift.** They carried the identical faded value
  the ticks did and measured 2.81:1 once the glass was tinted - the labels saying
  which way the needle leans should not be the faintest thing on screen.
- **The bright setting is deliberately untouched.** Soft and bright still read
  differently (0.60 against 0.65), so the control keeps meaning something instead
  of collapsing both options onto one look.

Metro's screen has the same construction in amber and has not been tinted; it
should get the matching treatment if this one feels right on-device.

## v0.100.4 — The meter scale you read the needle against

A contrast pass inside the lit screens themselves, rather than the chrome around
them, measured with the screen in both its idle and lit states so a designed
resting value is not mistaken for a broken one.

- **Dark mode's meter tick labels were `rgba(255,255,255,0.18)`: 1.59:1 on the
  screen glass.** These are the -50/-25/0/+25/+50 scale the needle is read
  against, so they are not decoration - at that level the needle floats against
  nothing. Raised to 0.45 alpha, which measures 4.52:1 and still sits behind the
  needle and the note in the visual order.
- Left alone deliberately: the big note and OCT label measure low in dark mode,
  but that is the idle state with no pitch detected, and the screen has a
  `.listening` class that governs the lit state. Those readings are the screen
  being asleep, not being broken.

Still open, and prototyped rather than shipped: light mode's screen glass is
`#f9fbfd → #e8eff6`, a luminance of 0.90, so it reads as paper rather than as a
lit panel - the scanlines and the inset shadow have nothing to sit on. Tinting it
costs almost nothing in contrast (the note stays above 7.8:1) but is a feel call,
so it is in `screen_tint_preview.html` for a decision on-device.

## v0.100.3 — Controls stop being drawn with transparent ink

A contrast pass over the tuner in both faces and both palettes, measuring the
rendered pixels rather than the declared colours, since most of this UI is built
from color-mix and var() and never states a hex.

The same mistake turned up four times: "this control is resting" was expressed by
making the ink transparent. Alpha lowers contrast, not emphasis, and the resting
state is the one almost every user sees - the hover states that restored full
colour never fire on a phone.

- **FORK measured 3.70:1 in light.** Its label was `color-mix(accent 55%,
  transparent)`, so the button was permanently half-faded despite always being
  live. Now full accent: 5.24:1 light, 10.23:1 dark.
- **The KEY pill's empty state measured 1.82:1** - the dash was very nearly
  invisible. It was `opacity: 0.4`; it now uses the muted token, which is what
  the rest of the app already uses to mean "quiet but legible".
- **The capo stepper buttons** carried the same `color-mix(..., transparent)`
  treatment. They are the controls the whole capo pass existed to make tappable,
  so they are now full accent.
- **The capo's zero readout used `var(--border)` as a text colour**, measuring
  1.31:1 in dark. A hairline token is not an ink token; it now uses muted.
- Left alone deliberately: the chroma strip's resting notes and the cents-meter
  tick labels measure low, but they are a designed inactive state that lights up
  on the note you are playing. Raising them would flatten the distinction the
  strip exists to draw.

## v0.100.2 — The pills stop lying about their own values

v0.100.1 let the value shrink so the label would stop overflowing. It shrank all
the way: "440" rendered as "4." and "NONE" as "NO". A pill that reports the wrong
number is worse than a tight one, so the value no longer gives ground at all and
the room comes from elsewhere.

- **The Hz unit is gone.** The pill is 89px at 412 and 78px at 390, and its
  contents needed 87px - so on every phone narrower than the widest one, the
  value absorbed the entire shortfall. Of the four parts, "Hz" was the only one
  telling the user something "440" had not already told them. Dropping it buys
  8-19px depending on width, which is enough on its own.
- **The arrow stays.** Dropping it instead would have bought 2.2px at 390, which
  is not a fix. It is also the only thing distinguishing these two pills from the
  capo readout beside them, which genuinely is static - without it all three read
  as status text. It already rotates when open, which is the part that says
  "this is a control".
- **KEY shows an em dash when nothing is set.** Every real value is one or two
  characters (B♭, E♭, F); only the empty state was four, so the pill was being
  sized by the single value that means "nothing here". The dash costs 12px
  instead of 34 and pairs with the dimming that was already applied when unset.
  The dropdown still says NONE, because there you are choosing rather than
  reading, and a lone dash in a menu is a riddle.
- Measured at 412, 390 and 360: every pill's content is narrower than its box,
  in the empty state and with all three transpositions applied, and at a
  three-digit reference pitch.

## v0.100.1 — The housing row's ghost pill, clipped A, and a clef pretending to be a fork

- **A second pill was hanging below the row in the full face.** The slot is
  shared: KEY in full, CAPO in simple. A later alignment fix set `display: flex`
  on all three pills at equal specificity, and being further down the sheet it
  quietly cancelled the earlier `#tunerCapoQuick { display: none }`. Both pills
  rendered, the second one overflowing the 28px slot - the ghost under CAPO. The
  face split is re-asserted after the alignment rule so the cascade lands the
  right way round, and each face shows exactly one pill again.
- **The A in the 440 pill sat outside its own padding.** `space-between` with
  non-shrinkable end caps pushed the first child past the pill's content box:
  2.6px past it at 412px wide, 8px at 360. The row centres instead, the value
  carries the slack, and the one-character label's trailing letter-spacing (2px
  of dead air after the only glyph) is pulled back. Measured inside the padding
  at 412, 390 and 360.
- **The fork button was wearing a treble clef.** U+1D11E means "written music",
  not "reference pitch", and the voice fork elsewhere in the app already uses
  something else - the app disagreed with itself. Its ink also sits high in the
  em box with a tail below the baseline, so the glyph read high no matter how
  the box was centred; the boxes measured perfectly centred while looking wrong.
  It is now an inline SVG tuning fork, which says what the button does and
  optically centres because the ink fills the box.

## v0.100.0 — The tuner popovers stay inside the screen and above the guide

v0.99.51 released the card's overflow, which fixed one clipping path; two more
kinds of jank survived it on-device.

- **The capo stepper's + button escaped its own box.** The popover was pinned to
  its 91px anchor with `left:0; right:0`, but its content needs ~114px, so the
  plus button overflowed past the box, past the card, and off the right edge of
  the screen. The popover is now right-anchored with `width: max-content` and
  `min-width: 100%`: it grows leftwards over the card when the anchor is too
  narrow, so every control stays inside the box and the box stays on screen.
- **The A440 popover could still paint under the Tuning & Capo card.** The row's
  z-index of 60 is meaningless whenever any ancestor of the row briefly forms a
  stacking context (entry animation, will-change), because the guide card comes
  later in the DOM and wins on document order. The card itself now takes
  `z-index: 60` alongside its overflow release while a popover is open, so the
  whole card outranks the guide card no matter what context traps the row.
- **The Hz and Key popovers stop being 91px worms.** Anchored to a pill-width
  slot, the seven presets stacked one per row and the Custom input row was
  crushed. Both popovers are now right-anchored at `min(230px, 62vw)`: presets
  wrap four per row, the popover drops from 268px tall to 118px, and the Key
  list fits in a row and a half.
- Verified with Playwright at 412 and 360px, both faces: capo `+` ends inside
  its box (374 < 383 and 322 < 331), the A440 popover renders fully above the
  guide card, and nothing crosses the viewport edge.

## v0.99.51 — Capo adjusts in place, the Hz popover stops being clipped

- **The capo pill now opens a stepper.** It previously scrolled to the guide's
  control and flashed it, which meant tapping a capo control did not change the
  capo - it moved the page. It opens a small − 0 + in place instead, driving the
  same `changeCapo`, so there is still exactly one capo. The `›` arrow is gone
  with the behaviour it advertised.
- **The A440 popover was being CLIPPED, not stacked under something.**
  `.tuner-bpm-card` is `overflow: hidden` and the popover drops 109px below it,
  so no z-index could ever have fixed it. The card releases its overflow only
  while a popover is open, keeping the rounded-corner clipping it exists for the
  rest of the time. The two popovers are mutually exclusive - a row this narrow
  cannot show both.
- **The row was 56px tall in the full face, not 28.** The KEY pill's text wrapped
  to two lines at its shared width, doubling the row and leaving the swap button
  sitting at the top of it - the high alignment. Pills are `nowrap` and the row
  is pinned to 28px, so a wrap can never stretch it again. All four controls now
  share one centre line in both faces (measured spread 0px, down from 14px).
- Verified at 360, 390 and 414px: row 28px, nothing clipped, 13px inside the
  card, capo steps relabel the pips, popovers open fully and restore the card's
  overflow on close.

## v0.99.50 — The housing row fits the card again

Pinning the swap button to a hard 84px in v0.99.49 stopped the row sliding but
overflowed it: four controls at their natural widths need 337px plus 24px of
gaps in a 332px row, so the last pill hung 16px past the card edge in both faces.

- **Fixed basis, not fixed width.** `flex: 0 1 84px` keeps the swap button's
  geometry stable across the label change while still allowing it to give way.
  Every child may now shrink, the gap is 8px to 6px, and the pill padding is
  tightened. The row ends 13px inside the card in both faces.
- **Equal flex on the two pill slots.** With `auto` the A440 pill absorbed a
  different share of the leftover space in each face and pushed the last slot
  11px sideways - the exact shift the previous build set out to remove.
  `flex: 1 1 0` on both makes the widths identical (84/64/80/80) and the measured
  shift across a swap 0px on every control, in English and Italian.
- **KEY was clipping.** Its value reads "NONE" at 13px, the widest content in any
  pill: 88px of text in an 80px slot. The value type now matches the label size.
- **Narrow phones drop the word labels.** At 360px the row is ~26px tighter and
  still clipped; there the "A" and "CAPO" labels hide and the values carry the
  meaning alone. Verified clean at 360, 390 and 414px, both faces.

## v0.99.49 — The glare stops moving, and so does the row

Two things shifting between faces, both mine, both now still.

- **The screen glare moved.** v0.99.38 traded the inner panel's padding from 22px
  down to 10px in simple to buy the ring room. The highlight gradient is painted
  on the padding box, so a different padding lands the reflection somewhere else
  and the screen appears to shift as you swap. Padding is back to 22px in both
  faces and the simple face fits inside the 194px of content the readout had.
- **The row slid sideways.** Hiding transpose outright let the row reflow: every
  remaining control moved 8-26px on each swap and 71px of dead space opened on
  the right. The slot is now kept and its contents swapped - transpose in full, a
  capo readout in simple. Tapping it scrolls to the guide and flashes the real
  control rather than duplicating it; capo stays in one place.
- **The swap button was the other half of it.** Its label alternates Full /
  Simple (Completo / Base in Italian), so a content-sized button changed width on
  every swap and shoved everything after it. Pinned to 84px, sized for the
  longest label. Measured shift across a swap is now 0px on every control, in
  both languages.
- Fixed while testing: changing capo only relabelled the pips on the next pitch
  frame, so with the mic idle it appeared to do nothing. It rebuilds immediately
  now - capo 3 gives G C F A♯ D G the moment it is pressed.

## v0.99.48 — Simple keeps the housing row, minus transpose

The row was hidden wholesale in simple, which left the face looking stripped and
took one control with it that simple actually needs. Judged individually rather
than as a block:

- **A440 stays, and had to.** The simple face already bakes `refPitch` into its
  pip targets, so hiding the control while still honouring the value left a tuner
  quietly tuned to 442 with nothing on screen saying so - hidden state of the
  worst kind. It is visible and works from simple; the popover opens inside the
  card.
- **The fork stays.** Hearing the reference note is exactly a beginner's move,
  and it is one tap with no vocabulary attached.
- **Transpose goes.** It never touches the string grid; it only relabels the
  readout for transposing instruments, which is the one control in the row a
  first-time tuner has no use for.
- With transpose gone the A440 pill inherited its flex space and stretched to
  175px, twice the fork beside it. Capped: the row now reads 77 / 64 / 104 rather
  than one control grown to fill a gap. The wrapper carries an inline
  `style="flex:1"`, so the override needed `!important` - a class alone cannot
  outrank an inline style.
- Verified in both faces and both themes: swap animation unaffected, fork plays,
  A440 set to 442 and back, full face row unchanged at 63/64/88/101, screen
  housing still 29,113,332,256, sweep clean.

## v0.99.47 — The face swap animates

Switching faces was an instant cut. It now cross-fades the glass and travels the
cards, and the three parts are deliberately not simultaneous.

- **The screen contents cross-fade in place.** The glass is 238px tall in both
  faces, so anything that scaled the screen would be animating a lie: only what
  is drawn on it swaps. The leaving face clears in .10s, the arriving one takes
  .30s so it lands with the layout rather than ahead of it.
- **The cards travel.** The tuner card sheds 149px of controls and the guide
  gains 124px of settings, so those get a .42s height transition and carry the
  sense of the layout rearranging. Height cannot transition from `auto`, so both
  cards are measured before and after the switch, driven between those pixel
  values, then released back to `auto` - otherwise they freeze at whatever the
  swap measured and later content changes clip.
- **Pips and setup buttons arrive with a small lift** rather than appearing.
- Fixed a one-frame flash: the leaving face is `display:none`d the moment the
  class flips, which resets its opacity to 1 for a frame, showing the old
  contents at full strength. It is held `visibility:hidden` across the switch.
- Durations are `!important` because the app-wide `*` transition rule otherwise
  replaces them - the same trap that flattened the launcher entry in v0.99.32.
- Verified: both directions trace smoothly (481 to 332px against a 0 to 1 fade),
  zero flash frames, a rapid double-tap strands no inline heights, picking a
  tuning afterwards still reflows, reduced motion switches instantly, and the
  screen housing stays 29,113,332,256 throughout.

## v0.99.46 — Back to five categories, with names that mean something

Listing bowed and plucked members individually saved a tap and cost coverage: a
fixed shortlist cannot hold five bowed and five plucked instruments, so double
bass, bouzouki, lute and harp had no route into the simple face at all, and eight
buttons crowded the glass into three rows.

- **Five categories again**, every string instrument reachable. The second tap
  lands in the guide's list, which already scrolls and already holds everything -
  bouzouki, lute and harp included. Five buttons, two rows, comfortably inside
  the screen.
- **Better names for the two that are instruments rather than tunings.** "BOWED"
  and "PLUCKED" describe how a note is produced, which is not how anyone reaches
  for their case. They are now STRINGS and FOLK, with the members as the subtitle
  (violin · cello, mandolin · banjo) so the category explains itself without the
  jargon. The tuning-shaped families keep their count, since "12 tunings" is the
  useful line for a guitarist and "4 tunings" tells a cellist nothing.
- **Family defaults come from FAMILIES**, not from `Object.keys(INSTRUMENTS)`.
  Key order there is arbitrary and landed FOLK on bouzouki; the curated order the
  guide already uses gives mandolin for folk and violin for strings.
- Verified: zero unreachable instruments, bouzouki selectable with G D A D,
  lute survives a reload with its family and six pips, EN/IT labels (ARCHI in
  Italian), screen parity in both themes, full sweep clean.

## v0.99.45 — Roster audit: two orphans, three ghosts, one crash

Auditing the instrument data turned up three separate faults, one of them a live
crash on a path a user can reach.

- **Bouzouki and lute were unreachable.** Both exist in INSTRUMENTS with correct
  tunings, but `FAMILIES.plucked` listed only mandolin, banjo and harp, so
  nothing in the UI could ever select them. Plucked now lists all five.
- **CHROM. PERC. crashed the instrument list.** The family named organ, melodica
  and mallet, none of which exist in the roster, and `buildInstList` dereferenced
  them unguarded: selecting that family threw `Cannot read properties of
  undefined` and rendered nothing at all. The three phantom entries are gone and
  the loop now skips unknown keys, so a future roster edit degrades instead of
  breaking.
- **Bowed and plucked no longer hide behind a family step.** The two shapes of
  family are genuinely different: guitar, bass and uke are TUNINGS of one
  instrument (twelve guitar tunings; four ukulele sizes all named UKULELE), while
  bowed and plucked are DIFFERENT INSTRUMENTS sharing a technique. Nobody picks
  up a cello and thinks "bowed", so violin, viola, cello, mandolin and banjo are
  now direct choices on the setup grid. Picking one still points the guide at its
  family, so a violinist who meant viola is one tap away.
- Data verified rather than assumed: all 46 instruments checked note-name against
  frequency at A440 (zero mismatches, so every octave number and accidental is
  right), and 23 tunings checked against known standards including DADGAD, drop
  C, open G, baritone and the orchestral strings (zero mismatches).
- Verified: all nine families render, plucked shows five, mandolin survives a
  reload with its family and pips, screen housing unchanged at 332x256, eight
  setup buttons fit in three rows without overflowing the glass.

## v0.99.44 — The restored instrument brings its family with it

Two persistence gaps, both only visible across a real reload rather than a face
round-trip within one session.

- **The family did not restore.** `selectedFamily` initialises to 'auto' every
  load, so restoring the instrument alone left the guide's tab on AUTO with an
  empty tuning list: the choice persisted, but the panel that exists to change it
  showed nothing. The saved instrument's family is now selected first (order
  matters - `selectFamily('auto')` clears the instrument).
- **The tuning itself did not persist.** Only `sfPickInstrument` wrote
  `progState.sfInstrument`, and under the current flow the tuning is chosen from
  the guide, which goes through `selectInstrument`. Picking a 5-string bass and
  coming back next session handed you the family's default 4-string. Now saved
  wherever the choice is made.
- Verified across a genuine page reload: DADGAD restores as instrument and
  family, the guide lists all twelve guitar tunings with DADGAD marked active,
  the pips read D A D G A D, and chromatic restores as chromatic with no pips.
- Capo still resets to 0 on load. That is long-standing and left alone
  deliberately: a capo silently restored from a previous session would mistune
  every string without saying why.

## v0.99.43 — Simple's guide holds settings, not a second string list

The string rows were the pip row again at length. What they add over the pips is
the string number, the exact frequency and a numeric cents readout - precisely
the expert detail simple exists to remove - and both are tappable to hear the
note, so nothing is lost by dropping them there.

They were also expensive: 295px of rows pushed the tuning list to 849px on an
844px screen, so the settings the guide had just been given ownership of started
five pixels below the fold. Hiding the rows in simple brings the list to 540px
and shortens the page from 1261px to 952px.

- String rows hidden in the simple face only. The full face keeps all six with
  their frequencies and cents readouts, unchanged.
- The card is retitled to match what it actually holds: "Tuning & Capo" in
  simple, "String Guide" in full. Calling it a string guide while showing no
  strings would name the panel after the one thing it was not displaying.
  EN/IT both ways (Accordatura e Capotasto / Guida Corde).
- Verified: changing to DADGAD from the guide relabels the pips to D A D G A D,
  capo 2 shifts them to E B E A B E, the capo control is still reachable, screen
  housing byte-identical at 29,113,332,256 across picking, chosen and light, and
  the full face still renders six rows at 295px.

## v0.99.42 — One question per surface

Simple had ended up with two pickers doing overlapping jobs: the screen chose an
instrument AND a tuning, while the string guide below sat there as six passive
rows. They never appeared at once, but they were two mental models for the same
task, which is what made the flow hard to describe.

The split is now by grain rather than by surface:

- **The screen asks the coarse question.** Five families, one tap. Picking one
  selects that family's default tuning so the tuner works immediately, and points
  the guide's own picker at the same family so scrolling down lands on the right
  list rather than on AUTO. The two-step tuning list on the glass is gone.
- **The guide holds the settings.** Tunings and capo, together, because a capo is
  a modifier on a tuning. All twelve guitar tunings, four basses and the rest are
  reachable there, in the picker that already existed. Family tabs stay hidden in
  simple - that question was answered on the screen, and asking it twice was the
  confusing part.
- **Capo is in one place again.** Removing it from the glass also removed the
  second control for one value; the guide's own buttons call `changeCapo`
  directly and the face picks the change up through `_sfKey` on the next frame.
- `selectInstrument` now refreshes the face's label and pips, since under this
  flow the tuning is changed from the guide - without it the glass kept naming
  whichever tuning the family had defaulted to.
- Verified: DADGAD shows D A D G A D and Open G shows D G D G B D on the pips,
  bass family offers four tunings and 5-string gives five pips, capo 1 relabels,
  chromatic still bypasses all of it. Full face untouched; screen housing
  byte-identical at 29,113,332,256 across picking, chosen, chromatic and light.

## v0.99.41 — Simple face reaches the whole roster, and one capo per face

The six-button shortlist was hiding most of what the app already supports: the
roster carries 12 guitar tunings, 4 basses, 4 ukuleles, 4 bowed and 5 plucked
instruments, and a fixed list of six could not reach drop C, a 5-string bass or a
baritone uke.

- **Two steps instead of a shortlist.** Step one picks a family and says how many
  tunings it holds; step two lists them with their note sequences. Only families
  that actually have strings appear - wind, brass and voice have no string set to
  walk through. The tuning list scrolls, since guitar alone has twelve and the
  glass is 238px tall. A back control returns to the families.
- **One capo per face.** The face's own capo and the string guide's drive the
  same `capoFret`, so both showing at once in Simple was two controls for one
  value. The guide's copy is hidden in Simple only - the screen owns it there,
  which is where the instrument was chosen and where the pips relabel. Full is
  untouched and keeps the guide's control exactly as before. Verified the screen
  capo still drives the guide: at capo 1 both read F.
- The chosen-instrument label now uses the instrument's own name, which is
  correct once a family has been chosen: "STANDARD" and "DROP D" read properly
  inside a guitar list, where they did not as a lone label.
- EN/IT for the new strings including the tuning count (accordatura /
  accordature). Screen housing verified byte-identical at 29,113,332,256 across
  families, tunings, picked, and both themes.

## v0.99.40 — Simple face is drawn on the screen, not on top of it

The elements were correct but they were UI, not display: flat greys and white
cards floating on the glass while the full readout beside them is lit type. The
full screen gets its look from three things and the face now uses all of them.

- **Lit type, not text.** The note is the --grad-tune lime-to-cyan gradient
  clipped to the glyphs, exactly as .tuner-screen-note does, with the octave and
  state line drawn as color-mix percentages of --accent so they read as dimmer
  phosphor rather than grey. Idle dims the dash instead of blanking it - a screen
  at rest, not an empty box.
- **Pips are etched segments**, a hairline of tinted accent over a 4% wash, and
  the lit one gains a bloom. They sit in the glass instead of on it. Same
  treatment for the instrument picker, so choosing looks like part of the
  instrument rather than a dialog that opened over it.
- **The ring is drawn with the same gradient** and a shadowBlur bloom, cleared
  after each stroke so later fills do not inherit it.
- **Layout.** Content summed to 233px inside a 218px box, so the bottom strip was
  pushed off the glass: .sf-core needed `min-height:0` before flex would let the
  ring shrink. The ring is now fluid to 156px, the note 68px, and the bottom row
  is a fixed 24px band separated by a hairline rather than controls sitting on
  the edge. Verified everything fits with the housing byte-identical at
  29,113,332,256 across picking, guitar, violin, chromatic and light mode.
- **Chromatic says PLAY A NOTE**, not "play a string", and its pip row collapses
  rather than leaving a gap where the strings would be. EN/IT both ways.
- Noted while chasing a transparent drop-shadow: --theme is scoped to the module
  wrapper, so color-mix against it from inside the screen resolves to nothing.
  The existing .tuner-screen-note has the same issue and computes to
  `filter: none` today - the face now matches it rather than diverging.

## v0.99.39 — Simple face asks what you are tuning

Auto-detect is not reliable enough to run silently, and the numbers are stark:
on D3 fourteen instruments match at exactly 0 cents, so the detector returns
whichever sorted first. Played against real string sets it scores 0/4 on
mandolin and 1/4 on violin - a mandolin player is told guitar, then violin, then
ukulele, changing between strings. In the full face a wrong guess is visible and
one tap from being fixed; in simple it would be quietly wrong all session.

- **Simple asks once, up front.** A six-button strip (guitar, bass, ukulele,
  violin, cello, mandolin) plus a chromatic option fills the screen until a
  choice is made; the readout stands down while there is nothing to read. The
  choice persists, and the instrument name doubles as the button to change it.
  Auto-detect is untouched for the full face, where it belongs.
- **Capo moved onto the screen**, next to the chosen instrument - it is
  meaningless until you have said what you are tuning. It drives the real
  `changeCapo`, so the string guide below stays in step, and it hides entirely
  for bowed and chromatic instruments where a capo does not exist.
- **Chromatic mode** for people who want a tuner rather than a tuning: note,
  ring and cents with no string targets, no pips and no locking. Nothing to tick
  off because nothing was claimed.
- The chosen label comes from the face's own shortlist, not `INSTRUMENTS.name`:
  the default guitar preset is called "STANDARD", which reads correctly inside a
  list of guitar tunings and meaninglessly on its own. Bass is `bass4` in the
  roster, not `bass`.
- Verified: the screen housing stays 29,113,332,256 through picking, picked and
  full; capo +1 relabels pips E to F and drives the real capo state; violin and
  chromatic hide the capo; choice survives a face round-trip; EN/IT both ways;
  module and tool sweep clean.

## v0.99.38 — Simple face: the redesigned screen, in the app

The prototype screen is now the real Simple layout. The standard readout (freq
row, note, verdict, meter) hides in Simple and a purpose-built face takes its
place inside the same glass: a hold ring around a large note, one line of plain
words, and a string pip row along the bottom.

- **Detection, never auto-advance.** Every frame the played pitch picks the
  nearest string - the string guide's own closest logic - and the ring fills
  while that string stays inside the in-tune window. A completed ring locks the
  string with a two-note chime (through `_cueNote`, so it follows the master
  fader) and the pip stays ticked. Nothing moves on its own; playing a different
  string simply moves the highlight. Locks clear when instrument, capo or
  reference pitch changes, since the targets they described have moved.
- **The screen stays one object.** Verified byte-identical housing at
  29,113,332,256 in both faces. The comment `<!-- /tuner-screen-inner -->` turned
  out to label the bezel's close, not the inner's - the face initially landed in
  the bezel and grew the screen to 474px before the parent chain was checked
  directly. Inside the inner, its padding is traded 22px to 10px (invisible from
  outside) and the face pinned to the remaining 218px.
- **Light mode is gradient ink, dark is glow** - the same treatment the standard
  screen note already uses. Canvas colors resolve from the theme vars at draw
  time. Pips speak the string guide's own visual language (closest cyan,
  done green with a tick).
- Tapping a pip plays that string's reference note, like tapping a guide row.
  Chromatic fallback when no instrument is selected: note, ring dot and generic
  too-low/too-high wording, no hold ring (nothing to lock, nothing to "tighten").
- EN/IT strings for all face states; round-trip verified. Swap button pinned to
  28px so it no longer squashes when its row siblings hide.
- Verified: detection walks all six guitar strings, lock fires after the 900ms
  hold and persists across strings, capo +1 relabels pips E to F and clears
  locks, silence idles clean, Reference A/B identical with either face, full
  module/tool/exercise sweep clean.

## v0.99.37 — Tuner face: better placement, and Simple is actually simple

Two problems with yesterday's first pass.

- **The switch was a two-button tab row sitting above the string guide**, which
  is neither where the control belongs nor worth that much width for a choice
  between two things. It is now a single swap button, first item in the housing
  row to the left of the fork, styled as a sibling of the fork and A440 pill so
  the row reads as one set of controls. The label names the current layout rather
  than the destination: a control that renames itself to something you are not
  looking at reads as a bug.
- **Simple was still carrying most of the clutter it exists to remove** - the
  STROBE button on the screen, every teach hint, all the help "?" buttons and the
  detection badge. The strobe is a precision meter, the hints explain controls no
  longer on screen, and the badge narrates a detection the string rows already
  show by highlighting. All hidden in Simple now.
- The swap button lives inside `.tuner-ref-row`, which Simple hides, so the row
  is kept alive and only its other children are hidden - otherwise the control
  that leaves Simple would vanish with it.
- 44pt hit area via a pseudo-element, so the visual stays at 28px in the row's
  rhythm alongside the fork and pill.
- Contrast verified in both themes: 13.8:1 dark, 6.18:1 light. IT round-trip
  verified on the new label (Simple / Base).

## v0.99.36 — Tuner faces

The tuner now offers two layouts, switched from a control on the tuner itself
rather than buried in Settings: a beginner who wants the plainer view will not go
looking for it three menus deep.

- **The screen is untouched by the face.** Its housing, readouts, needle and
  every style inside it are identical in both layouts - verified byte-for-byte at
  (29,113) 332x256 with the note at 80px in each. Switching does not move or
  restyle a single pixel of the display, so the two faces read as one instrument
  rather than two tuners.
- **Simple** keeps the screen, the string rows and the capo, and hides the
  reference row (fork / A440 / transpose), the chroma and pitch-history panel,
  and the instrument picker. **Full** is unchanged from today and one tap away.
  Nothing is gated.
- **Scoped to `body.tuner-simple.theme-tuner`.** The card above the string guide
  is shared with the Reference tool, so a body-level class alone would have
  followed the user into Reference and hidden its controls too. Verified by A/B:
  Reference renders identically with either face selected.
- Light-mode ink: the active chip hit the fill-vs-ink trap the capo and
  panel-badge rules already document - fill and label both drawn from `--accent`,
  converging to 0.78 vs 0.80 luminance, effectively invisible. Paired with a
  deepened ink; now 7.99:1 in light and 10.98:1 in dark.
- EN and IT strings added (Simple / Base, Full / Completo); verified the toggle
  translates and restores on language round-trip. Choice persists via progState.

## v0.99.35 — Master fader now spans a real range

The fader moved the right nodes but barely changed anything audibly, at either
end. Two separate causes.

- **The headroom cap was global when it should be per chain.** `_getEffectiveScale`
  clamped everything at ~1.39, a number set by the LOUDEST chain in the app: a
  0.9-base site reaches its -3 dB threshold at 87% of the fader, so 1.39 is right
  for that one. A quiet 0.32-base site does not reach its threshold until ~246%,
  and the theremin not until ~272% - both were clamped at 1.39 anyway, throwing
  away most of the upper range for everything that was not already loud. The cap
  is now computed from each chain's own base gain. Verified no chain exceeds full
  scale at 200%: loud ones cap at 1.0, quiet ones reach 0.576 where they have the
  headroom for it.
- **The bottom half was worth only 6 dB.** A 50% floor is -6 dB, about one
  perceptual step spread over half the fader's travel, while the top half spanned
  far more. The floor is now 20% (-14 dB), so the two halves are roughly
  symmetrical and the fader can actually quieten things. Still a trim, not a mute.
- Fixed a double-count found while testing: the cap divided by
  `base * BASE_GAIN_BOOST`, but the hand-rolled chains register a base that
  already includes the boost, so their nodes landed at 1.111 - over full scale and
  a genuine clipping risk on percussive transients. `_getEffectiveScale` now takes
  an `alreadyBoosted` flag.
- At and below 100% the cap never binds for any chain, so every existing value is
  unchanged: 0.9 percussive, 1.0 Tonale/theremin, 0.72 and 0.288 for the 0.8 and
  0.32 buildLimiterChain sites. None of the clipping tuning is disturbed.

## v0.99.34 — Five chains now follow the master fader

Most audio runs through the shared `buildLimiterChain`, which `setMasterVolume`
updates live. Eight chains are hand-rolled for good reasons - the percussive ones
sit at -6 dB for transients, Tonale adds a +5 dB shelf at 300 Hz, the organ has a
saturation stage - and five of those were not fully wired to the fader.

- **Tonale and the theremin ignored master volume entirely.** Neither read the
  master scale at all: the Tonale out-bus ran bass -> limiter -> destination with
  no gain node anywhere, and the theremin's bus was pinned at 1.0. Pulling the app
  volume down left both at full level. Confirmed on device before changing
  anything.
- **The three rhythm-card chains** (`rcGetOut`, `rctGetOut`, `rcdGetOut`) read the
  scale correctly at build time but are cached, so they held whatever value was
  current when first built and ignored the fader afterwards.
- All five now register their gain node in `_masterGainRegistry` and are updated
  live, the same pattern `_getOrganChain` already used.
- **Gain only - never the limiter.** These chains keep their own thresholds on
  purpose (-6 dB percussive, -3 dB Tonale/theremin); registering the limiters
  would flatten them onto the shared base and undo the clipping tuning. Tonale's
  new gain stage sits AFTER its limiter so the +5 dB shelf and -3 dB threshold are
  untouched: it scales the finished signal rather than retuning the chain.
- Verified: at 100% every value is byte-identical to before (+5 shelf, -3 and -6
  thresholds, 0.9 gains). At 50% all five halve; at 200% they reach the 1.389 cap
  while keeping their own thresholds. Affected surfaces all open and exit clean.

## v0.99.33 — Entry animation: one movement, not three

The finish felt jerky because three things were moving in sequence at the end
rather than together.

- **The launcher and the card now fade at the same time.** They were staggered
  140ms apart, so the chooser cleared at ~826ms while the card was still at 0.95
  and fading until ~1009ms: the card floated alone over the module for nearly
  200ms, which reads as an extra beat tacked onto the end. Both now start at
  420ms and resolve together (measured within 0.03 opacity of each other).
- **The card was being cut off at 0.21 opacity** rather than reaching zero,
  because teardown fired before the fade finished. The margin is now generous
  enough that the fade always completes.
- **The tab bar waited for the handover.** It slides in when `lnch-open` is
  dropped, which is now mid-fade, so a third element started moving while two
  others were still resolving. It is delayed 300ms during entry only, and holds
  off-screen until both fades are done. A `lnch-settled` flag clears the delay
  afterwards so ordinary tab switching stays instant.
- The bar's delay needed `!important`: the app-wide `*` transition rule was
  replacing both its duration and delay, the same override that flattened the
  entry timings in v0.99.32.
- Verified across all four modules: both layers fade in lockstep, card grows to
  278px, teardown complete, correct theme, bar arrives last.

## v0.99.32 — Entry animation actually animates

The entry read as a snap with no fade because three separate things were
cancelling it, none of them visible in the code that defines the animation.

- **The launcher's own rule was stripping every duration.** The colour-cross-fade
  suppression added in v0.99.28 rewrote `transition-property` with `!important`
  across `#lnch` and all its descendants, which also discarded the durations: the
  entry's .46s travel and .3s fades were silently replaced by the app-wide .06s /
  .2s defaults. It now zeroes only the colour properties and leaves everything
  else alone; the launcher opts back into its own .34s fade explicitly.
- **The morph sits outside `#lnch`**, so the app-wide `*` transition rule applied
  to it instead. Its timings are now `!important` for the same reason.
- **Nested teardown timers drifted.** Each stage was scheduled from inside the
  previous one, so the card's fade started ~220ms late and was then cut off at
  0.45 opacity by a teardown scheduled from an earlier estimate — the card jumped
  from half-faded to gone. All stages now run off one clock, and teardown waits
  for the fade duration plus a frame.
- **Growth raised 1.35x to 1.7x.** At 1.35x a 164px card gained only 57px and
  finished in 300ms, then sat motionless for another 300ms. It now travels 164 to
  278px over ~500ms and the motion fills its own time.
- Verified across all four modules: mid-fade opacity samples between 0.89 and 0.98
  (a fade, not a cut), card grows to 278px, tears down completely, correct theme.
  Reduced motion still bypasses the whole thing.

## v0.99.31 — Entry animation: deal, centre, hand over

The full-screen card expand shipped in v0.99.29-30 was always going to be a flat
coloured rectangle: a real content-carrying clone would have to duplicate ~5400
DOM nodes, and canvases clone blank, so the tuner needle and metronome would
expand as empty boxes. Rather than polish an effect that cannot show what it is
pretending to show, the card now stays a card.

- **Deal → centre → hand over.** The three unpicked cards deal away on their own
  vectors; the chosen card travels to the middle of the screen while growing
  1.35x, holds there, and the module cross-fades in as the launcher clears. The
  card is never asked to stand in for module content.
- **Scale about the card's centre.** With the default `0 0` transform origin the
  growth pushes the box down and right, so the translate meant to centre it landed
  progressively further off the more it grew (206/226/248px against a 195px
  target). `transform-origin: 50% 50%` fixes it: all sizes land dead centre.
- **Opacity left to the stylesheet.** The start state wrote `style.opacity = '1'`
  inline, which beats `.lnch-morph-fade` on specificity, so the card reached the
  centre and then never faded out. The inline value is now removed instead of set.
- Verified across all four modules: cards deal, cloned face paints its real
  gradient, card lands centred at 221px wide, fades and tears down completely,
  correct theme lands, no stuck hold flag. Reduced motion still bypasses it.

## v0.99.30 — Entry animation actually runs

v0.99.29 shipped the entry animation with two faults that between them made it
invisible: the cards never moved and the expanding card was transparent.

- **Cards did not move.** The entry-reveal rule `#lnch .lnch-cell { transform:
  none }` has specificity 1-1-0; the new deal rules were written as
  `.lnch-cell.lnch-other:nth-child(n)` at 0-3-0. An ID beats any number of
  classes, so `transform: none` won every time and the classes applied to no
  visible effect. The deal rules are now scoped under `#lnch` so later-wins
  applies. Verified: cards travel from 25,176 to -11,159 with rotation.
- **The expanding card was invisible.** The morph cloned `.lnch-face` alone, but
  every rule that paints a card is written `.lnch-cell .lnch-face`, and the
  gradient reads `--lc` which is set on the cell. A bare face clone matched none
  of them and rendered as an empty rectangle - the morph was running the whole
  time with nothing to see. It now clones the whole cell and strips the pin badge,
  which keeps the descendant selectors and the custom property intact.
- Verified across all four modules: cards move, the cloned face paints its real
  gradient, the morph grows to 390px, tears down completely, correct theme lands.
  Reduced motion still bypasses the morph entirely.

## v0.99.29 — Launcher entry animation

The chooser used to scale the picked card to 1.05, fade the others, and cross-fade
the whole launcher out over the module. Nothing connected the card to the module,
so it read as a hard cut.

- **Deal + expand.** The three unpicked cards are dealt away on their own vectors
  with rotation, then the chosen card is cloned into a new `#lnchMorph` layer at
  its exact on-screen rect and grown to fill the viewport. Two beats: the choice
  reads first, then the entry. The eye follows one object into the module.
- The clone copies the `.lnch-face` only — the pin badge is chooser furniture and
  must not fly into the module with it. The card's label and peek fade in 100ms
  while its plain background lingers, so the crossover never looks thin.
- **Sequencing.** The morph is the only thing covering the module while the chooser
  is torn down, so it has to outlive both the launcher fade and the `display:none`
  that follows it. `finish()` runs at 260ms; the morph is not released until
  580ms, after `#lnch` is actually hidden. An earlier ordering released it first
  and briefly exposed the module bare.
- Start state is written with transitions suppressed and flushed before the end
  state; setting both in one frame means the browser only sees the end value and
  nothing animates.
- Reduced motion skips the morph entirely and lands instantly, as before.
- Verified across all four modules: clone grows 164→390px, tears down completely,
  correct theme lands, no stuck hold flag; launcher hides while the morph is still
  opaque over the module.

## v0.99.28 — Launcher owns its palette

v0.99.27 deferred the theme swap but the cards still recoloured, because the fix
was aimed at the wrong thing. The card faces were themselves built from
`--surface` and `--panel`, which are themed per module — so all four cards
repainted whenever the theme class landed, no matter when that happened.
Deferring only moved when you saw it.

- **Pinned the launcher's palette.** `#lnch` now declares its own `--surface`,
  `--panel` and `--border-soft` (with a light-mode set), so the chooser looks
  identical whichever module you last used or are about to open. Verified: card
  faces are byte-identical across all four themes in both light and dark, while
  the four cards keep their individual `--lc` tints.
- **No colour cross-fade on the chooser.** A global `*` rule gives every element a
  0.06s background/colour transition to soften per-module theme changes; on a
  surface with a fixed palette that can only animate an artifact. Scoped it out for
  `#lnch`, leaving transform, box-shadow and opacity — the actual press feedback —
  untouched.
- **Pin button hit area now meets the 44pt minimum** via a pseudo-element, so the
  visible dot stays 24px while the tap target no longer competes with the card.
- Verified across all four modules × both themes: cards unchanged on tap, correct
  theme lands after the transition, hold flag cleared every time.

## v0.99.27 — Launcher no longer recolours before the module arrives

Picking a card from the launcher called `setMode()` at tap time, which swapped the
`theme-*` class on body synchronously. The palette therefore changed while the
chooser was still on screen and its pick animation was still running, so the next
module's background and accent flashed around the launcher ~125ms before the
module itself appeared.

- **Split the palette swap out of `setMode`** into `applyModeTheme()`, with a
  `_themeHold` flag. `lnchGo` sets the hold before calling `setMode`, then releases
  it inside `finish()` — the moment the launcher is opaque over the new screen. The
  colour change now happens under cover, so the module is already wearing its own
  palette as the chooser fades away.
- **Reduced-motion path unaffected**: with no animation to hide behind, the theme
  applies immediately as before.
- **Normal tab switching unaffected**: still instant, since the hold is only ever
  set by the launcher.
- **Failsafe**: if a hold is ever left unreleased (an error before `finish()`, or a
  teardown mid-animation), a 600ms timer applies the pending palette anyway rather
  than stranding the app on the previous module's colours.
- Verified across all four modules: palette deferred at tap, correct theme landed
  after the transition, hold flag cleared every time.

## v0.99.26 — Real alto and tenor clefs

Alto and tenor were the only clefs still drawn as a font glyph (U+1D122) via
<text>, which renders as tofu on any device whose system font lacks the musical
C-clef. Now they draw as a real Bravura path like treble and bass.

- **Extracted the SMuFL cClef (U+E05C) from Bravura.otf** at the same scale
  (0.036, y-down) the existing treble/bass paths use, verified by reproducing
  RR_TREBLE from the font byte-for-byte first. Added as RR_CCLEF (pbox
  measured: x0 y-18.22 w25.16 h36.43); both alto and tenor point at it.
- **Corrected the path-clef vertical anchor** so the glyph origin (y=0), which
  every Bravura clef places on the line it names, lands on that staff line. The
  C-clef is symmetric about its notch, so origin-on-line puts the notch on the
  correct line: middle line for alto, fourth-from-bottom for tenor.
- **Fixed tenor pitch reference**: topStep was 31, placing middle C one line above
  the notch; corrected to 30 so C4 sits on the notch line as a tenor clef
  requires. Alto was already correct at 32.
- Verified: 336 renders across all four clefs, zero tofu fallbacks (no <text>
  clefs remain), zero clipped, zero wrong notehead counts.

## v0.99.25 — Light-mode key colour and tone popup skin

Two leftover colour mismatches, both hardcoded salmon that ignored the module's
green accent.

- **Selected note keys turned salmon** in the builder (and the player root grid's
  glow). Four rules hardcoded rgba(255,160,122,...) for the active fill, border
  and shadow. All now route through `color-mix(... var(--accent-warm) ...)`, so
  they follow the module's green in both themes.
- **The VOICE tone popup wore the piano's cream/brown card.** The chord scope
  (`.chd-tonepop`) recoloured the tiles and group labels but never the card
  itself, so the surface stayed cream in light and brown in dark. Added card,
  border and header overrides to the chord scope for both themes: deep green card
  in dark, pale green in light.
- Verified: selected keys render green (rgb 47,112,72) with zero salmon in both
  themes; popup tiles and card both green via the real button flow; 126 staff
  renders across two spelling modes with zero wrong notehead counts.

## v0.99.24 — AUTO cue is now ♯♭, not ♮

The natural sign was misleading: ♮ is itself a spelling instruction ("cancel the
accidental on this note"), so next to ♯ and ♭ it read as a fourth forcing option
rather than "let the app choose".

- **AUTO cell now shows a small combined ♯♭ mark** — reads as "either / let it
  decide", in the same accidental family as the two single-glyph cells without
  claiming to be an instruction. Glyph set at 11px to match the ♯/♭ cells (an
  earlier over-condensed 9px pass rendered it 5px wide, a smudge).
- Behaviour unchanged: ♯♭ is smart per-chord spelling (D♯ major → E♭), ♯ and ♭
  force one throughout. Both cards synced, all three cells select.
- Verified: 189 renders across three modes, zero clipped, zero wrong notehead
  counts; header height unchanged at 24px.

## v0.99.23 — Spelling switch aligned and re-cued

- **Removed the decorative dash** left of the switch. Every `.card-label` carries
  a 14px line via `::before`; on the chord picker headers it pushed the switch
  22px off the note grid's left edge. Suppressed on these headers only, so the
  switch now sits flush and lines up with the C key directly beneath it (x=36 vs
  x=37). Other cards keep their dash.
- **AUTO cue changed from "A" to ♮.** The natural sign reads as the musical
  counterpart to ♯ and ♭ — three accidental glyphs as one set — rather than a
  lone letter. Behaviour is unchanged: ♮ still means smart per-chord spelling
  (D♯ major → E♭), ♯ and ♭ force one throughout.
- Verified: 756 renders across four clefs and three spelling modes, zero clipped,
  zero wrong notehead counts; card height unchanged at 355px.

## v0.99.22 — Spelling switch polished down to header weight

The previous "slim" pass made the switch shorter in width but 36px tall — 14px
taller than the CLR button beside it, so it read as a chunky widget bolted onto
the header. Fixed by matching it to the row it lives in.

- **Switch height 36px → 24px**, level with the undo/clear buttons; vertical
  centres now align across the whole header row.
- **Restyled as a quiet segmented track**: a hairline-gap track with the active
  cell marked by a soft accent fill rather than a full outline, so it reads as a
  setting rather than a control competing with the note buttons. Active-cell
  cascade fixed (the light-mode base fill had been overriding it).
- Undo and clear given matching height, flex-centred glyphs and a subtle
  transition so the row is consistent end to end.
- Verified: 504 renders across four clefs and two spelling modes, zero clipped,
  zero wrong notehead counts; card heights unchanged (355px player, 343px
  builder); every cell selects correctly in both themes.

## v0.99.21 — Slimmer spelling switch, left-aligned

The Builder header was carrying switch, label, undo and clear across 289px of a
316px row, so the label wrapped to two lines and the row felt cramped.

- **Switch moved to the left** of both picker card headers, ahead of the label,
  with undo/clear still right on the Builder.
- **Slimmed from 101px to 80px**: "AUTO" spelled out was 43px on its own, so it is
  now a single "A" with the full meaning in the title attribute, and all three
  cells are an equal 30px wide.
- **Header label shortened** from "Tap notes to build" to "Notes" ("Note" in
  Italian) — the readout above already says TAP NOTES BELOW and the grid is
  directly beneath, so nothing is lost. The label is also allowed to shrink and
  ellipsis rather than wrap the row.
- Both headers now sit on a single 36px line with 30–38px of slack. Tap targets
  are 30×34px.
- Card heights unchanged at 355px player, 343px builder; 252 renders across three
  spelling modes with zero clipped and zero wrong notehead counts.

## v0.99.20 — Spelling switch on the picker cards

- **Moved the AUTO/♯/♭ switch off the readout and onto the cards where notes are
  chosen**: the Root picker in Player, and the note grid header in Builder beside
  undo and clear. Spelling is a property of the input, so the control belongs with
  it; the ledger card goes back to being purely a readout.
- This removes the flex-line contention introduced in v0.99.18 — the chord name no
  longer shares a row with anything, so the auto-fit measures its own box again
  and the header plumbing added to work around it is gone.
- Idle text ("TAP NOTES BELOW") restored to 20px; it had been dropped to 15px to
  survive beside the switch.
- Card heights back to 355px player and 348px→343px builder, recovering the row
  the switch had been occupying.
- Verified: 756 renders across four clefs and three spelling modes, zero clipped,
  zero wrong notehead counts; 200 random builder names, zero clipped.

## v0.99.19 — Name fitting fixed after the switch moved

Both faults traced to the same change: putting the spelling switch on the same
flex line as the chord name.

- **Auto-fit measured the wrong width.** `chdFitName` sized the text against the
  header's inner width, which now includes the switch and the gap, so it thought
  there was ~115px more room than there was. A single calculated pass could not
  converge either — changing the font size changes the width flex hands back, so
  the arithmetic is always one layout behind. It now shrinks in steps and
  re-measures `scrollWidth` vs `clientWidth` until the text genuinely fits.
  Verified: 0 clipped across 250 random chords, sizes 15–36px.
- **Idle labels styled separately.** "TAP NOTES BELOW" is an instruction, not a
  chord symbol, and shrinking 36px type until it fit beside the switch left it
  unreadable. Idle text is now set at 15px and allowed to wrap.
- **The switch could collapse to zero width.** `flex:0 0 auto` on the container
  was not enough because its buttons were themselves shrinkable; the buttons are
  now `flex:0 0 auto` too and the container is `width:max-content`.
- Card heights unchanged: 360px player, 348px builder.

## v0.99.18 — One spelling control, on both cards

- **The hidden per-root flip is gone.** Double-tapping a selected accidental root
  did the same job as the AUTO/♯/♭ switch, so a tap could silently contradict the
  mode the switch was showing. One visible control now owns the decision.
- **The switch moved to the ledger card header** and appears on Player *and*
  Builder — Builder previously had no spelling control at all, which was an
  inconsistency. Both instances stay in sync and write the same setting.
- **AUTO kept.** Measured across the common chord set it yields 3 double
  accidentals (all genuinely correct spellings, e.g. Cdim7's B♭♭) against 35 for
  forced sharps and 21 for forced flats. Removing it would leave new users in a
  mode that writes D♯ major as D♯–F𝄪–A♯.
- Switch shares a line with the chord name rather than taking a row of its own: a
  full row cost 41px of card height for a control most people set once, and the
  name already auto-fits so it simply shrinks around it. Card heights remain
  single values (360px player, 348px builder).

## v0.99.17 — Spelling switch on the Root card

- **AUTO / ♯ / ♭ toggle** added to the Root picker header. AUTO keeps the
  per-chord behaviour from v0.99.16 — each root and quality spells whichever way
  avoids double accidentals, so D♯ major presents as E♭–G–B♭. The two accidental
  buttons force sharps or flats across the entire tool for anyone who wants one
  fixed spelling; the root grid, chord name, note pills, notation and the Builder
  all follow. Choice persists in `progState.chordSpelling`.
- Per-root flipping (tap a selected accidental root again) still works. Doing so
  while a forced mode is active returns the tool to AUTO, so one deliberate flip
  is not immediately recalculated away.
- Measured across the common chord set: AUTO produces 3 double accidentals (all
  genuinely correct spellings such as Cdim7's B♭♭), forced sharp 35, forced flat
  21. The forced counts are the honest consequence of the choice.
- Toggle tap targets are 49×32px; card heights unchanged at 355px player and
  343px builder across all three modes.

## v0.99.16 — Chords audit: enharmonics and a dead control

Full functional scan of the tool. Every id present, every onclick handler
defined, every i18n key resolving, no console errors. Two real faults found.

- **Quality group headers did nothing.** `buildChordQualityGroups()` re-expanded
  whichever group held the active quality, and it ran on every rebuild — including
  the rebuild a header tap triggers. Collapsing the group you were using
  immediately reopened it. Auto-expand is now opt-in (`buildChordQualityGroups(true)`),
  used when the tool opens; header taps and quality picks pass `false`.
- **Enharmonic spelling was naive.** Black-key roots always spelled sharp, so
  D♯ major came out D♯–F𝄪–A♯ (correct arithmetic, notation nobody writes) instead
  of E♭–G–B♭. Each root+quality now defaults to whichever spelling produces fewer
  double accidentals: 7 unreadable chords in the common set down to 0. The six
  remaining double-accidental chords app-wide (Cdim7's B𝄫, Baug's F𝄪) are the
  genuinely correct spellings and are left alone.
- **The enharmonic toggle was undiscoverable.** Re-tapping a selected accidental
  root flips its spelling, with no cue that this was possible. Selected sharp/flat
  roots now carry a small ⇄ mark and a tooltip naming the alternative, and the
  player hint says so in both languages. A manual flip is remembered per root and
  overrides the automatic default from then on.

## v0.99.15 — Notation restored

Fixes a regression introduced with the stable-height work in v0.99.14.

- **The staff drew nothing but its clef.** The octave-placement search was seeded
  with `{cost:0, steps:[]}` as a guard for empty chords, but a real octave choice
  can legitimately score 0, and `cost < best.cost` then never beat the seed — so
  every chord kept the empty steps array. Seeded with `null` instead.
- **Sets without a dictionary entry now get notation too.** Approximate and
  universal names (anything the added-tone describer or `chdNameAnySet` handled)
  had no `def` to render from, so the staff stayed blank for roughly half of all
  tapped combinations. `renderChordStaff` accepts a raw pitch-class list and
  voices it upward from C4, so every named set has a staff. The formula row falls
  back to intervals from the bass in the same case.
- **Staff wrapper de-flexed.** An SVG carrying explicit width/height attributes
  as a flex child is sized by flex rules rather than its own box in some
  WebViews, which can collapse it. The wrapper is a block with the SVG absolutely
  centred, so the element's own dimensions stay authoritative.
- Card heights remain single values: 355px player, 343px builder.

## v0.99.14 — Chords card holds still

- **No more layout shift.** The card resized as you picked chords or tapped
  notes (player 347-373px, builder 264-346px), pushing everything below it
  around. Every variable row now reserves its space: note pills and alternates
  sit on one horizontally-scrolling line, the inversion stepper is a fixed
  six-cell grid with invisible placeholders past the chord's length, the staff
  scales inside a constant 96px frame, and the chord name shrinks inside a fixed
  40px box rather than the box following the font size. The builder's empty state
  keeps its rows occupied so the first tap does not grow the card. Measured: one
  single height in both modes (player 355px across 219 chord/inversion states,
  builder 343px across 151 random note sets), in both themes.
- **Undo and clear moved to the note grid** they act on, as small inline buttons
  on the grid's header rather than sitting in the transport row beside PLAY. They
  stay visible rather than hiding behind a gesture, and dim when there is nothing
  to undo. Transport is now just PLAY and ARP.

## v0.99.13 — Chords tool: staff restored, green accent, auto-fit name

- **The staff disappearing on device.** The SVG carried no width/height
  attributes and relied on `width:100%; height:auto`, which needs the intrinsic
  ratio derived from the viewBox; some WebViews resolve that to zero height, so
  the staff rendered but occupied no space. Width and height are now set
  explicitly and kept in step when the fitter rewrites the viewBox, with a
  min-height on the wrapper as a floor.
- **Orange in light mode.** `--accent-warm` is a salmon (#ffa07a) with no
  light-mode override, so the PLAY button, chord name, chip highlights and the
  selector card's rim all came through orange on a green card. A green accent is
  now scoped to `#toolChords` in both themes (#8fd694 dark, #2f7048 light) and
  every rule referencing the token follows; no other module is affected.
- **Chord name auto-fits.** Universal naming can produce very long symbols, so
  the name shrinks to fit its card (36px down to a 13px floor). Sized by
  font-size rather than transform, since a transform leaves the layout box at
  full width and the name still overflows. Measured out of normal flow, because
  in flow the parent caps the reading and the fit never triggers.
- **FORMULA and WRITTEN swapped**, so the formula sits directly under the notes
  and notation closes the card.
- **Row labels un-indented** by 6px (34px to 28px) with the arrows unmoved.

## v0.99.12 — Every note combination is a chord

- **100% naming coverage.** New `chdNameAnySet()` names any pitch-class set at
  all: it picks the root that yields the cleanest reading, takes whatever triad
  or seventh core is present, and spells every remaining note as a parenthesised
  tension, the way a jazz chart would. Tested across all 1023 sets from a fixed
  root (sizes 1–5): 167 named from the dictionary, 480 by the added-tone
  describer, 376 by the universal namer, **zero unnamed**. C·D♭·D now reads
  Csus2(♭9) rather than UNKNOWN.
- **Clef unboxed.** The frame around the clef read as a widget bolted to the
  stave. The clef now sits on the staff as it would in a score, with a small
  caret beneath marking it as tappable; the hit area stays generous via an
  invisible rect.
- **Row labels aligned.** Foldable and fixed rows now share one padding value, so
  every label starts at the same x (measured 34px on all four) while the arrows
  stay out in the gutter.
- **Tone popup themed.** The shared picker is skinned for the piano console
  (near-black) and the riff surfaces' cream in light mode. Opening it from Chords
  now tags it so it wears this module's greens in both themes; other surfaces are
  untouched.

## v0.99.11 — Chords tool: real glyphs and layout pass

- **Notation now uses the app's own Bravura outlines.** Noteheads are
  `RR_NH_WHOLE` and accidentals are `RR_SHARP` / `RR_FLAT` — the same paths
  Rhythm Reading draws — instead of hand-rolled ellipses and font characters, so
  notation matches everywhere and needs no musical font on the device. Treble and
  bass clefs use `RR_TREBLE` / `RR_BASS`, resolved lazily since those constants
  live in a later script block. Alto and tenor have no extracted outline yet and
  still fall back to the font glyph.
- **Clef centred in its button.** Horizontal centring now uses each path's
  measured bounding box (treble 24.16×63.22, bass 24.8×32.29) and a fit scale, so
  it is exact rather than a guessed width; verified at 0.00px offset on all four
  clefs. Vertical position stays anchored to the line the clef names, as it must.
- **Fold arrows no longer shift their labels.** The arrow is absolutely
  positioned in the label gutter, so foldable and fixed rows put their text at
  the same x. All four row labels measure 25px.
- **Voice picker moved into the action row** beside PLAY/ARP, removing a whole
  labelled block of vertical space, and themed to the module — it was inheriting
  the piano overlay's near-black on a mint card.
- **Layout rhythm** evened out: consistent 10px between the card, actions and
  selector panels.
- **Builder copy fixed** — said "TAP NOTES ABOVE" while the grid sits below it.
  Now "TAP NOTES BELOW" / "TOCCA LE NOTE SOTTO".

## v0.99.10 — Chords tool: on-device fixes

Follow-up to v0.99.9 from device screenshots.

- **Clef could render enormous.** `_chdAlignClef` measures the drawn glyph and
  scales it, but silently returned if `getBBox()` was unavailable, leaving the
  provisional size on screen — which was deliberately oversized. The provisional
  size is now conservative (fail small, not large) and a hard ceiling caps the
  font size regardless of whether measurement succeeded.
- **Light mode.** Light mode restyles `.card` explicitly rather than only
  swapping variables, so the new `.chd-card` picked up dark-token values and
  rendered blue-grey on the mint page. Card, row rules, label gutter and clef
  frame now have explicit light treatments; staff ink deepened to `#2f4a17`.
- **Naming coverage 24% → 72%.** Most tapped sets are not in any dictionary. New
  `chdDescribeSet()` finds the best known chord inside the set and names the
  remainder as an added interval, so C·D·A·B reads Bm7(no5)(♭9)/C instead of
  UNKNOWN. Truly arbitrary clusters still fall back to the interval stack.
- **Accidentals** now centre on their notehead via `dominant-baseline` instead of
  a guessed baseline nudge that made flats ride low.
- **Noteheads** thinner and more tilted (1.9 stroke, −16°) so whole notes read as
  ovals rather than blobs at phone size.
- **Tone bank** replaced with the app's current grouped tone picker (one compact
  voice button opening the family popup), matching the interval and piano
  surfaces; the old horizontal chip strip is gone. Picking a voice refreshes both
  Chords buttons.
- **Removed the duplicate volume sliders** from both panels.

## v0.99.9 — Chords tool rebuilt as the ledger card

**Chords (Player + Builder).** Both modes now share one result-first card:
chord name on top, then labelled rows for NOTES, WRITTEN, FORMULA and ALSO.
WRITTEN and ALSO fold via the arrow next to the row name.

- **Notation row.** Reference chords drawn as whole notes (no stems) on a staff
  rendered in the app's own colours, light mode included. The clef printed at
  the staff head is the control: tap it for a treble/bass/alto/tenor picker.
  Clef choice persists app-wide in `progState.chordClef`. Clef glyphs are
  anchored musically and aligned against the measured ink after render, so they
  land correctly in whatever font the device supplies.
- **One speller everywhere.** Pills, chord name and staff all spell through
  `getSpelledNotes`, so Cm7 reads C·E♭·G·B♭ in every row at once.
- **Inversions (Player).** Stepper under the note pills: name becomes Cm7/G,
  pills rotate with the bass highlighted, staff re-voices, and PLAY voices the
  inversion (rotated-out tones move up an octave).
- **Tappable alternates (Builder).** ALSO lists every valid reading of the
  tapped notes; choosing one re-roots the entire card — name, pills, spelling,
  staff, formula.
- **19 new chord types.** 6/9, m6/9, madd9, 9sus4, 7sus2, 13, maj13, m13,
  shell voicings 7(no5)/m7(no5)/maj7(no5), the Lydian Mb5 triad, and dyad
  entries for every interval (m3, M3, P4, m6, M6, m7, M7) so two taps always
  get a root-position name. Pickable qualities joined their groups; shells and
  dyads are Builder-only (rank 4).
- **Builder volume slider added** (was Player-only); the two sliders stay in
  sync and share the percentage readout.
- Old `.chord-display` CSS left in place, now unused; strip in a later cleanup
  pass rather than risking a large deletion inside this feature build.
 and to what specific value. This
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

## v0.81.58 — @capacitor/app was never installed

**The deep links never had a chance.** Not the original handler, not the flag fix,
not the three-bug autopsy in v0.81.57. All of it was downstream of a plugin that was
never in the build.

`getLaunchUrl()` and the `appUrlOpen` event come from **`@capacitor/app`** — a separate
npm package from `@capacitor/core`. It was never in `package.json`. Share, haptics,
status-bar, notifications, screen-orientation, RevenueCat: all installed. The App
plugin: not. So `window.Capacitor.Plugins.App` was `undefined` on every device, always,
and every deep-link handler ever written waited politely on a plugin that did not exist.

Found because the failure shape finally isolated it: Play-installed v0.81.57, link opens
the app directly (so App Links ARE verified, manifest and assetlinks are right), but the
app opens plain. The URL was reaching the app and dying at the missing plugin.

Fix, on the dev machine:

    npm install @capacitor/app
    npx cap sync

Also added a **tripwire**: if the app is on a native shell and the App plugin never
appears within the poll window, `_intonareDiagAppPlugin` records it, and the 7-tap
diagnostics panel now has an `App plugin` line right under `Capacitor`. This failed
silently for weeks because nothing anywhere was responsible for saying so. Now
something is.

**The v0.81.57 fixes stand** — they were verified against a mocked App plugin and the
logic is right. They simply could not run until the plugin existed. This is the same
lesson as the whip-on-Android copy step, one layer up: the code being correct means
nothing if the artefact never ships with its dependencies.

---

## v0.81.57 — the deep links: three bugs, stacked, and the first one made the other two unfixable

**The links had never worked.** Not since they were written. Every fix before this
one was correct and none of them could possibly have run.

### 1. The handler lived inside `removeSplash()`

This is the whole thing. The deep-link handler — the `getLaunchUrl()` call, the
`appUrlOpen` listener, all of it — was nested inside `removeSplash()`, which runs
when the splash **ends**.

So the handler that exists to skip the splash was only registered *after the splash
had already finished*. It was structurally incapable of doing its only job. A brace-depth
walk settled it: `removeSplash()` spans lines 16720–17040, and the handler sat at 16800.

It explains both symptoms at once, which is how you know it is the real one:

- **the splash never skipped**, because nothing asked it to until it was over;
- **the module never opened**, because `getLaunchUrl()` only resolved ~3.5 s in, by
  which point the splash's handoff to the home screen had wiped out whatever the
  link tried to open.

Moved to the top level of the script block, so it is listening before the splash starts.

### 2. `go()` fired 250 ms before its dependencies existed

Measured, not guessed:

    getLaunchUrl() resolves      ~77ms
    go() therefore fires        ~157ms   (setTimeout(go, 80))
    enterExercise() is defined  ~410ms   ← a script block ~40,000 lines further down

`go()` called `enterExercise` a quarter-second before it existed, threw
`enterExercise is not a function` straight into a bare `catch (e) {}`, and the link
silently did nothing. **That catch is why this never surfaced as an error: it swallowed
the only evidence.**

### 3. Waiting for `enterExercise` to *exist* is not waiting for the app to be *ready*

The first attempt at (2) polled for the function. That turned the bug into a coin flip —
one run gave chordle ✓ tonale ✗ diadle ✗, the next gave the opposite. Same code, same
build.

The functions appear at ~410 ms, but the app is still booting: there are
`DOMContentLoaded` handlers as far down as line ~99500, plus a `window` `load` handler,
and they set up the home screen. Open a module before those run and the boot sequence
calmly resets the view on top of it.

Now it waits for `window` `load`, which fires after every deferred handler — the exact
guarantee needed: nothing else is going to redraw the shell after that point.

### Also: don't give up if Capacitor isn't there yet

`if (!window.Capacitor) return;` — one check, at the earliest moment in the file, no
retry. The bridge is injected by the native shell and is not guaranteed to exist while
this inline script is still parsing. Lose that race and the listener is never registered.
Now polls (100 × 100 ms, bounded, stops cleanly on web).

**Verified 20/20:** all four dailies × both URL shapes × bridge speeds 0/250/700 ms, plus
warm-app (`appUrlOpen`), a second link over an already-open module, and garbage input
(empty/unknown/no `?m=`/wrong domain) falling through to a normal launch.

> **Note for testers:** the dailies are Pro-gated. A non-Pro tester tapping a shared link
> gets the paywall, not the puzzle. Correct behaviour, but it looks exactly like a broken
> link. If links still fail on a Play build, check
> `adb shell pm get-app-links com.lieutenantdan.intonare` first — if App Links are not
> `verified`, Android opens Chrome and none of this code ever runs (that is an
> assetlinks/signing problem, not a JS one).

---

## v0.81.49–56 — Road Trip: per-theme dressing

A `.rt-dressing` layer per theme. Pure CSS gradients, no assets.

**It rendered perfectly and was completely invisible, for two reasons:**

1. It was a **sibling** of `.rt-menu` at `z-index: 1`. But `.rt-menu` is `z-index: 12`
   with a full-height opaque themed background, so it painted straight over the top.
   Moved the layer *inside* the menu.
2. Every theme carries `#exRoadTrip.rt-dsn-X .rt-menu > * { position: relative; }` — a
   wildcard that catches **every** direct child, including the dressing. It forced
   `position: relative`, which made `inset: 0` meaningless and collapsed the layer to
   **zero height** as a flex item. Two classes on the id outranks anything reasonable,
   so: `!important`. Rare, and correct here — a blanket wildcard reaching past its
   business, and a five-place fix would rot the day someone adds a sixth theme.

**Which means the earlier "strengthen the colours" pass was pure theatre** — doubling
alphas on a layer that was zero pixels tall.

Once visible, the design work (all Dan's calls, on-device):

- **Parchment** (v0.81.52–53): coffee rings didn't read — a perfect circle reads as a
  circle, not a stain. Tried fold creases (rendered as huge diagonal light streaks) and a
  white radial to punch a hole in the ring — **under `mix-blend-mode: multiply` white is
  not a hole, it's a lamp**, and it rendered as a sun in the middle of the map. Both cut.
  Now: edge-aging only. Four irregular ellipses so the border isn't symmetric (one even
  inset shadow reads as a photographic vignette, wrong century), corners going first,
  scattered age spots. **Nothing in the middle, because that's where the content lives.**
- **Blueprint** (v0.81.52): the grid alone is wallpaper. Added drafting furniture — a
  title block in the bottom-right corner, a dimension line down the left margin with end
  ticks, an uneven cyanotype exposure wash. Three objects, all in the margins.
- **Blueprint START** (v0.81.54): was `rgba(255,210,63,.1)` — **ten percent**. The most
  important control on the screen was a ghost and read as disabled. Now solid amber,
  dark text (amber-on-amber is not a button).
- **Nautical** (v0.81.54–56): rhumb-line web was a full-screen fan of lines behind the
  content — texture, not decoration, and it fought the cards. Replaced with a compass
  rose; the map already has one, so that was just a second rose. **Cut entirely.** The
  theme carries itself on its grid and palette. Deliberately bare.
- **Night / Ink:** stars, headlight glow, ink bleed. Unchanged.

---

## v0.81.47–48 — Road Trip start screen stopped short of the bottom

The first fix (flex on `.rt-menu`) did **nothing**, and Playwright measured 250 px of
dead space to prove it. `#rtMenu` is a **child** of `.rt-stage-wrap`, not a sibling, and
`.rt-stage-wrap` is `flex-grow: 0`.

**A child cannot outgrow a `flex-grow: 0` parent.** Grow the container, not the leaf.

Then `justify-content: space-between` on the menu: cards read from the top, START sits in
the thumb zone, 264 px of slack between. Measured 0 px dead. In-trip map still a perfect
square (aspect 1.000 — the vehicle/pin maths depends on it).

---

## v0.81.39–46 — rhythm flash cards: the tap zone, and the card that kept growing

Many rejected iterations (pad-as-transport, dome/glow, moved feedback rows, arrows
re-homed) before Dan called it: *"tap area was good two builds ago, just do that."*
Reverted. Arrows now flank the pad inside the tap-zone wrapper; transport hides wholesale.

**The card kept expanding on entry to tap mode, and it took three attempts to find why.**
Not the layout, not the CSS I'd added — `rcArmTap()` was writing `t('rc_tap_ready')` into
`#rcTapFeedback` on mode-entry. Non-empty text defeated its own `:empty { display: none }`,
which added a row *and* a 12 px flex gap. **Don't write text into a feedback row on
mode-entry.** (`rc_tap_ready` is now an unused i18n key. Harmless.)

Also fixed en route: hiding `.rc-transport` had killed the prev/next arrows (siblings of
PLAY); a third stale copy of the tour text at L37989 said "hit PLAY" with no `<strong>`,
so grep had missed it. **Italian apostrophes (`l'entrata`) break single-quoted JS i18n
strings** — escaped; the syntax gate caught it.

---

## v0.81.38 — settings that would not stick, and a feature nobody could reach

A sweep of every module-level setting in the app, after the Road Trip theme turned out
never to have been saved. It was not an isolated bug.

### Nine settings reset to factory on every single launch
- **`chordScaleInstrument`** — *your instrument*. Arguably the most personal setting in
  the app, and a trumpet player was re-picking trumpet every time they opened it.
- **`metroAudioOn`**, **`metroVolume`** — the metronome came back unmuted at 50% no
  matter what you had set.
- **`rtDiff`** — Road Trip difficulty.
- **`ssNoteMode`**, **`ssAutoAdvance`** — Pitch Match's shown/hidden and auto-advance.
- **`gccQuality`** — chord chart quality.

All now persist, via a small `prefGet`/`prefSet` pair. Every access is wrapped:
localStorage can be unavailable (private mode, storage pressure), and a setting that
fails to save should be an annoyance, not a crash. Values are validated on read, so a
stale entry from an older build falls back to the default rather than poisoning the
module.

### What the sweep also found — and deliberately did NOT change
- **Interval Training was never broken.** It already persists range, difficulty, sing
  direction and the rest through `progState.ivPrefs`. The first pass "fixed" it anyway;
  that was reverted, because a second restore path would have fought `ivLoadPrefs()` and
  won or lost depending on load order.
- **`chordScaleInstrument` is reassigned temporarily** in a few places — opening a
  Rhodes card swaps it to `piano` and swaps it back two lines later. Saving on bare
  assignment would have persisted `piano` for anyone who so much as looked at a Rhodes.
  The save is wired to `switchChordScaleInstrument()`, the actual user-facing setter,
  and nowhere else.
- **`gccToolMode`**: every assignment is an internal swap that restores itself. No user
  setter, so nothing to persist.

### And `ssDifficulty` turned out to be a whole feature nobody could reach
It was read but never written — permanently `easy`. Digging in, `SS_DIFFICULTIES` is
**fully implemented**: a real curve for Pitch Match's string mode, from major pentatonic
(no semitones, easy to sing) through major to full chromatic, with step-versus-leap
ratios and sequence lengths tuned to match.

| | scale | notes | max leap |
|---|---|---|---|
| PENTATONIC | major pentatonic | 3 | 2 |
| MAJOR | major | 4 | 3 |
| CHROMATIC | all twelve | 5 | 5 |

**No picker existed anywhere.** String mode is a live tab, so people could play it — and
every one of them was locked to the easiest tier forever, with two thirds of the content
unreachable. There is a picker now, in the settings sheet, shown only for string mode
since nothing else reads the setting. Named by the scale rather than easy/medium/hard,
because that is what it actually changes.

### `ssPlayMode` never persisted either, and the reason is grim
The tab handler called `ssSavePrefs()`, guarded by `typeof ssSavePrefs === 'function'`.
**That function was never written.** The guard swallowed the call, nothing threw, and the
play mode silently failed to persist — for however long that has been there. A defensive
`typeof` check around a function that does not exist is indistinguishable from one around
a function that does.

Restores and saves are symmetric: nine settings restored on boot, the same nine saved
on change. Nothing restored that is never written; nothing written that is never read.

## v0.81.36 — Road Trip: the legs were flat, and the grading was grading the wrong thing

### It was listening to itself
`rtPlayHome()` sounds a 1.2 s reference while `rtPhase` is still `'home'`, so the hold
meter filled from the app's own speaker before the singer opened their mouth. Same bug
Pitch Match had. Detection is now deaf while the reference sounds, and the lock
progress resets so your turn starts clean.

### An A needed 12 cents
A semitone is 100 cents. Twelve cents is a professional standard — trained singers
drift more than that on a held note — and this was asking for it **from memory, after a
distraction, with no reference**. Almost everything came back C or D. A game where good
play looks like failure is not hard, it is discouraging.

Now **25 / 40 / 60 / 85**. Still discriminating: 25 cents is audible and you have to
actually hold it. But a decent attempt now looks like one.

(The result *words* were on different thresholds than the *letters*, so a leg could be
graded B and told you had "lost it". Aligned.)

### It never said which way you missed
The grade is an absolute error, so there was nothing to do differently on the next leg
except try harder. **Sharp or flat is actionable.** Shown after grading, never during —
it teaches without giving the answer away.

### The bar was a clock
It filled on elapsed time whether you sang your heart out or held your breath, and
finished on schedule regardless. Nothing you did changed anything on screen, so the leg
was something happening *to* you. That is the flatness.

**The bar now fills with sung time** — it only advances while a voice is actually being
heard, so the bar *is* your singing, and stopping stops it. It still carries no pitch
information whatsoever: right note or wrong, it does not care and will not tell you.
The recall stays blind. A 260 ms grace window keeps it moving through breaths, and a
wall-clock ceiling stops a silent room hanging the leg.

(A first attempt put a live *needle* on screen. It positioned a dot by cents error and
claimed not to show the target — but dead centre **was** the target, and one leg in you
would have simply tuned to it. That kills blind recall, which is the whole exercise.
Deleted before it shipped.)

### The grading was grading the wrong thing
The median already killed isolated junk — one voice crack, one bad frame. Two things
got through it, and both cost grades that had been earned:

- **Octave errors.** Detectors mis-report 2x or 0.5x the true frequency, and they do it
  in *runs*, not single frames — so the median moves to the wrong octave and you get an
  **F for singing the note perfectly**. Samples are now folded into the octave nearest
  home.
- **Scooping.** Sliding up into a note is how most people sing. Taking the back half was
  meant to skip it, but a slow scoop is still climbing at the halfway mark, so the
  median landed mid-slide. Frames that are still *travelling* (>35 cents of movement
  between frames) are dropped, leaving only the part you actually held.

Neither makes the grade softer. They stop it measuring the wrong thing.

### Your theme and your voice were not being saved
`rtSetDesign()` set the variable and toggled the class but **never persisted** — so
every launch dropped you back to Night whatever you had picked. Worse, nothing applied
the saved value on open either, so even once stored it was ignored until you actively
tapped a swatch.

**And the vocal range was not saved anywhere**, in Pitch Match *or* Road Trip. It reset
to tenor on every app launch. That is not a session preference; it is a fact about the
singer's body, and a bass or a soprano had to re-pick it every single time they opened
the app.

Both now persist and restore.

### "Lock it in" is not scaffolding
It skips the sing-and-hold step of the home phase and starts the drive. A reasonable
valve if the mic is misbehaving — though worth knowing it means recalling a note you
never actually established.

### Layout
`.rt-cz` had no flex growth, so it sat at its natural height and the module — and the
theme with it — stopped short of the bottom of the phone. It now fills and centres, so
the start button, the recall bar and the final passport sit in the middle of the space
rather than hugging the top of it.

## v0.81.32 — the splash skip never ran

App Links work: the link opens the app directly, no browser. But the splash still ran
its full three and a half seconds and the daily did not open — the two things the skip
was written to prevent.

**An ordering trap.** `_intonareSkipSplash` is defined inside the splash IIFE, ~700
lines below the deep-link handler that calls it. On a cold start the handler runs
first, so the function **does not exist yet**. The `typeof === 'function'` guard failed
quietly, and the code fell straight through to *waiting* for the splash — precisely the
behaviour the skip replaced. No error, no symptom except the feature not happening.

- The handler now **raises a flag** (`_intonareWantSkipSplash`) rather than calling a
  function. The splash reads it when it starts and skips itself. **A flag does not care
  who wrote it or when**, so there is no ordering dependency left to get wrong.
- The direct call is kept for the warm case, where the splash has already started.

## v0.81.31 — App Links and Universal Links: the link just opens the app

The bounce page can never open the app on Android without a tap. That is not a bug to
work around; it is Chrome's rule, and it applies to any page. **The way out is to have
no page at all.**

App Links (Android) and Universal Links (iOS) let the **OS** own the URL. It verifies
the domain against a file you publish, and from then on the https link is intercepted
before any browser sees it. No page, no script, and therefore no user-gesture rule.
Tap a shared result in a chat, the app opens on today's puzzle.

**This is why the shared link was https from the start.** Nothing about it changes;
the OS simply starts intercepting it.

### The pieces
- **`.well-known/assetlinks.json`** — names the package and the app-signing SHA-256
  (the Play-managed key, not the upload key; verifying against the upload key fails
  silently on every real install).
- **`.well-known/apple-app-site-association`** — no file extension, which is required
  — names `HAS2KCH36U.com.lieutenantdan.intonare` and the `/Intonare/go.html*` path.
- **Manifest** — a second intent-filter with `android:autoVerify="true"` for the https
  host. The custom-scheme filter stays as a fallback.
- **CI** — writes the Associated Domains entitlement.
- **The handler learned to read https.** App Links deliver the *https* URL, not
  `intonare://`. The regex only matched the custom scheme, so a verified App Link
  would have arrived and been **silently ignored** — the feature would have looked
  like it simply did not work.

### go.html does not go away
It is what people **without** the app get: the store, and an honest explanation. The
OS only intercepts the URL for devices where the app is installed and verified;
everyone else still lands on the page. One link, both audiences.

### Two things must be done by hand
1. **A second GitHub repo, named exactly `LieutenantDan76.github.io`**, holding only
   the `.well-known/` folder. The verification files must be served from the **domain
   root** — `lieutenantdan76.github.io/.well-known/…` — and a *project* Pages site
   (which is what `Intonare` is) can only serve under `/Intonare/`. The root file
   authorises the app for the whole domain, so the links themselves do not move.
2. **Apple Developer portal → Identifiers → com.lieutenantdan.intonare → tick
   Associated Domains.** Without it the capability is absent from the provisioning
   profile and the iOS build fails to sign.

## v0.81.30 — the splash was running at half speed, and it was my fault

### dt60 normalised to the wrong reference
`wavePhase += _spd * dt60`, where `dt60 = dtMs / 16.667` — a **60 fps** reference.
That is the obvious choice and it was wrong.

The original code was `wavePhase += _spd`, frame-coupled, with `_spd` tuned **by eye
on a 120 Hz Android**. So the speed the wave was actually designed at is
~116 × `_spd` per second, not 60 × `_spd`. Normalising to 60 did not preserve the
design — **it halved it, everywhere.**

- **iOS has been running the splash at half speed since v0.81.13.** That is the real
  reason it "looked weird" there, and it is why three rounds of theorising about
  stepping and DPR and frame caps never landed: the wave was not stepping oddly, it
  was crawling.
- **Android inherited the same slowdown the moment it was next built** — it had been
  on v0.81.2, from before `dt60` existed.

Fixed by normalising to the frame time it was tuned at (~8.62 ms) rather than to 60
fps. Frame-independence is kept; the speed is the one the wave was designed with, and
it is now identical on 60 Hz and 120 Hz alike.

### Chart samples: the fix hooked the wrong function
v0.81.27 warmed the instrument's samples when the charts tool opened — except it
hooked the **navigation wrapper**, which only the deep-link and open-with-preset paths
go through. **The actual card button calls `enterTool()` directly** and sailed straight
past it. So the tool still opened on guitar with nothing loaded and played the synth
fallback until you switched instrument and back — exactly the bug it was meant to fix.

Moved into `enterTool()`, which is the path everything uses.

### The whip never reached Android — `go.bat` skipped it
The Adventurer's fanfare played with no crack. The app code was fine; the file simply
was not there.

`go.bat` step 4g copies the audio assets with:

    for /D %%i in (audio_assets\*) do ...

**`for /D` iterates directories only.** Every sample set is a folder — `grand_piano\`,
`violin\` — so this worked perfectly, right up until the first *loose file* landed in
`audio_assets\`. `intonare_whip.mp3` sits at the root, so the loop stepped straight
over it and it never reached the Android assets. iOS was unaffected: Codemagic does
`cp -r audio_assets/*`, which takes files as well as folders. A platform-specific
absence with no error anywhere.

- **`go.bat` now copies loose files too**, every run rather than "if not exist" — a
  replaced file has to actually make it across.
- The diagnostics panel also reports the sample's state now (**READY** with duration,
  **loading**, or **NOT LOADED** with the specific HTTP/decode/network failure), so
  the next audio-file mystery is one screenshot rather than three theories.

### And `go.bat` does not build the APK
Worth stating plainly, because it is how a fixed native feature looks broken: the
script preps everything and then says "hit Run in Android Studio". **Native changes —
the manifest, the .java files — only reach the phone through that Run.** Testing
against the APK already installed gives you the new web code with the old native
behaviour, which reads as a half-broken feature rather than an unbuilt one. The
script's closing message now says so.

## v0.81.29 — deep links actually land

Two bugs, one per platform, both of which made the link look like it did nothing.

### iOS: the module opened behind the splash — and the splash is now skipped
The app opened, but on the home screen rather than the shared module. The handler
waited a fixed 400 ms and then called `enterExercise()` — but on a cold start the
splash owns the screen for about **three and a half seconds**, and its own handoff to
the home screen then wiped out the module that had quietly opened behind it.

Waiting for the splash fixes that, and leaves a toll: three and a half seconds of
branding on **every** shared link, paid by someone who tapped it specifically to see a
puzzle. **The splash is for people opening the app; it is an obstacle for people
opening a link.**

- The deep-link handler now **skips the splash** outright. It calls the splash's own
  `removeSplash()` — not a bare element delete — because that function also performs
  the iOS first-gesture audio unlock and starts sample preloading, and any other
  teardown would silently skip both.
- `getLaunchUrl()` is async and has not resolved when the splash starts, so the
  splash does begin: it is cut off a frame or two in rather than never started. A
  brief flash of the first frame, which beats delaying every launch to wait on a
  plugin call that usually comes back empty.
- If the skip is somehow unavailable, it falls back to **waiting** for the new
  `intonare:splash-done` event rather than opening the module behind the splash.

### And they land on the daily, not the module's front door
Opening the module was not what the link promised. Someone tapping a shared Chordle
result tapped a link **about today's puzzle**; dropping them on a difficulty picker
makes them go and find it themselves.

Each daily already had a proper stateful entry point, and they behave correctly for
someone arriving from a link:

| | |
|---|---|
| already played today | shows the result |
| mid-game | resumes where they left off |
| fresh | starts today's puzzle |

`chordleStartDaily`, `tonaleStartDaily`, `diadleStartDaily`, and — for Music Quiz —
`mqOpenDailyPopup`, which shows its "play the daily?" card rather than launching
straight in. That is its own established behaviour and is left alone.

### All three dailies now count you in
Chordle and Diadle fired their progression **350 ms after entry**. Fine if you had
deliberately tapped "Daily" and were braced for it. Startling if you had just arrived
from a chat, phone still face-down, no idea yet which app you were looking at.

The first instinct was to suppress the auto-play for deep-link arrivals only. That is
a patch, and it leaves someone staring at a puzzle wondering what to do next.

**Tónale already had the right answer** and has had all along — `tonaleReadyIntro()`:
a brief **READY? → 3 → 2 → 1** before the first tone, with a haptic tick on each
digit. So Chordle and Diadle now do exactly the same thing.

- One shared `intonareReadyCountdown()`, used by both.
- The count runs **in the play button** — no new markup, no layout shift, and it is
  where the eye already is.
- Abandons cleanly if the player backs out mid-count.
- Identical behaviour whether you tapped "Daily" yourself or arrived from a shared
  link. **The entry path no longer changes what happens.**

The deep-link special case is gone; it is not needed when the behaviour is right for
everyone. (`READY?` / `PRONTO?` already existed in both languages.)

**Where the count shows:** the first version ran it inside the play button — 13 px of
text in a 56 px control, unreadable. It is now a **module overlay**: the game dims
(55% + blur), and the count sits front and centre at 56 px with Tonale's scale-pop on
each digit and a haptic tick. Covering the controls also says "not yet" more clearly
than any wording could. Mounted in the module's own root (`#exChordle` / `#exDiadle`),
so the app header stays live — backing out mid-count bails cleanly.

**Scope, deliberately narrow:** the countdown fires on a **fresh daily start only**.
Replays are user-initiated (they pressed the button; they are ready), resume means
they know what they are doing, and free play has never auto-played. Only the fresh
daily fires audio at someone, so only the fresh daily counts them in.

Review also caught the overlay's digits using `inherit` inside the `font` shorthand —
invalid CSS, silently dropped wholesale, which would have cost the weight and
line-height. Set as individual properties instead.

### Android needs a tap, and that is the rule — not a workaround
The page fired the app launch automatically on load. **Chrome blocks that, by design:**

> "Chrome won't launch an external app for a given Intent URI if the Intent URI is
> initiated without user gesture." — *Chrome for Developers*

and Chromium's own `external_intents` documentation lists *"launching an app without
user activation"* among the things it refuses outright.

The tap that opened the link was consumed by the navigation to the page. The page's
own script has no user activation left, so an automatic `intent://` fires into a wall
— **every time**, regardless of the manifest, the build, or anything else. (The
earlier iframe version failed for exactly the same reason, one layer down. Two
attempts, one root cause.)

Chrome's guidance is explicit: *"Construct an intent anchor and embed it within a
page, so the user can choose to launch the app."*

- **On Android the page is now the button.** A real `<a href="intent://…">` anchor,
  tapped by a human. No timers, no guessing whether it worked.
- The intent carries `browser_fallback_url`, so **Chrome sends people without the app
  to the Play listing itself** — one tap covers both cases.
- **iOS keeps the automatic path**, because navigating to a custom scheme from script
  does work there and the app opens immediately.

### Android: the earlier iframe attempt
The bounce page tried to launch the app by pointing a hidden iframe at
`intonare://…`. **Chrome has blocked custom-scheme navigation from iframes for
years**, as a security measure. So nothing happened, the fallback timer ran, and the
page showed the stores — to someone who had the app installed.

- Replaced with an **`intent://` URL**, which is Android's own supported mechanism:
  it names the scheme, the package, and a browser fallback, and Chrome makes the
  decision itself.
- The fallback screen also gets a manual **"Open in Intonare"** button, and no longer
  claims the app is missing — the navigation may simply have been blocked (in-app
  browsers do this too), and a tap always works.

## v0.81.28 — deep links: shared dailies open the app

Chordle, Tonale and Diadle results ended with the bare word "intonare". They now end
with a link that actually goes somewhere.

### Why an https link and not `intonare://`
A custom scheme in a message sent to someone **who does not have the app** does
nothing at all. It is dead text, and it makes the app look broken to precisely the
person you were hoping to reach.

So the shared link is https, pointing at a small bounce page:

    .../Intonare/go.html?m=chordle

The page tries `intonare://chordle`. If the app is installed the OS intercepts it and
they land in the right module. If not, the navigation quietly fails, a timer fires,
and they get the store instead.

**All four dailies** carry it: Chordle, Tonale, Diadle, and Music Quiz. (Music Quiz
was nearly missed — it is the fourth share in the app and it opens via its own
`mqOpen()` rather than `enterExercise()`, so the handler special-cases it.)

### The pieces
- **iOS** — `CFBundleURLTypes` written into Info.plist by CI.
- **Android** — a `VIEW` / `BROWSABLE` intent-filter in the manifest. `launchMode`
  was already `singleTop`, so a link arriving while the app is open goes to
  `onNewIntent` rather than starting a second activity.
- **JS** — handles **both** arrival paths: `getLaunchUrl()` for a cold start, and the
  `appUrlOpen` event for an app already running. Handle only one and half your links
  silently do nothing.
- **The page** — detects the platform, leads with the right store, and is honest
  about the ones that are not live yet rather than showing a dead button.

### And this is the foundation for Universal Links, not a detour from them
Universal Links (iOS) and App Links (Android) need an Apple Team ID and the release
keystore's SHA-256, published in verification files served from the domain — none of
which exist until the app is actually on the stores. But **the shared URL is https
either way.** Adding them later changes nothing about the app, this code, or any link
already sent; the OS simply begins intercepting the URL directly instead of routing
through the page.

The store links live on the page, not in the app, so they can be filled in the moment
each store goes live — without an app update, and without breaking links already
shared.

## v0.81.27 — Adventurer sound settled; chart samples; Pitch Match listens properly

### The Adventurer's sound
Settled on the brass fanfare with the real whip cracking just past the arrival note.
The five other variants and the on-device picker are gone — they were scaffolding.

**On how close the homage gets:** copyright protects the MELODY, and it follows that
melody through transposition. So this does not use the Raiders figure. The leap is a
perfect **fourth**, not the original's minor third, and that is the distinction doing
the legal work. What it borrows is style — brass, march-rhythm pickup, a heroic leap
— which is not protectable. Everyone hears "adventure"; nobody is quoting.

The whip is a real recording, played at 0.42 against the brass (0.9 buried the very
thing it was meant to punctuate).

### Chart notes played the synth voice on the first visit
`_chartPlay()` checks `SampleEngine.isReady()` and falls back to the synth if not —
but it never *triggers* a load. The eager loader lived inside
`switchChordScaleInstrument()`, which only runs when you actively pick an instrument
from the sheet. **Open the charts tool normally and it inherits the default
instrument without ever calling it.** So the samples were never requested and every
note came out synthesised, until you happened to switch instrument and switch back.

- The loader is now callable on its own and runs **on tool open** as well as on
  switch. First note you tap is the real instrument.
- Kept its original name (`_loadInstSamples`) because the regression sentinel pins
  it; renaming would have quietly retired a guard for no benefit.

### Pitch Match was listening to itself
The reference tone played for 0.5 s **with the mic live and detection running**. The
reference is a clean sustained tone — precisely what the detector is best at — so it
would lock onto the app's own speaker and report a perfect match before the singer
had made a sound.

- **Detection is suppressed while the reference sounds**, and for a short tail after.
- **Reference is now 1.0 s**, up from 0.5. Half a second is enough to identify a
  pitch and not enough to internalise one.
- "your turn" appears when it starts listening. EN + IT.
- `ssStop()` clears the flag and its timer — without that, stopping a round *while*
  the reference was sounding would have left the detector permanently deaf.

### Not done, deliberately
- **Splash at 120 fps** — impossible in a WebView. Apple caps `requestAnimationFrame`
  at 60 inside WKWebView by design; there is no public API, and the private one is an
  App Store rejection. The only legitimate route is rebuilding the splash as
  GPU-composited CSS, which cannot preserve the particle gather and burst. Not worth
  losing the animation to gain frames on one platform. The plist key from v0.81.22 is
  removed; it did nothing.
- **Deep links for daily shares** — needs a URL scheme on both platforms, an
  `appUrlOpen` handler, and a web landing page to catch people without the app
  installed. Half-done deep links are worse than none. Its own piece of work.

## v0.81.25 — a real whip

Variant E's crack was synthesised from filtered noise. It read as **static, not
leather** — a whip's transient has a very specific shape that a noise burst cannot
fake.

Replaced with a real recording (Pixabay: free for commercial use, **no attribution
required**, modification permitted). Trimmed to the transient, normalised, mono,
96 kbps: **13 KB**. The sample keeps the authentic two-part gesture — the swish of
the wind-up at ~60 ms, then the crack peaking at ~250 ms — with the dead air before
it cut so the sound is instant.

- Played **dry**, straight to the destination: the crack wants no reverb, and the
  brass that answers it already has a tail.
- Loaded by **XHR, not fetch** — the same reason the piano samples need it. On iOS,
  Capacitor serves `www/` from `capacitor://localhost`, and `fetch()` against a
  custom scheme returns status 0. XHR goes through WKWebView's ordinary
  resource-loading path and reads it. (Local-scheme XHR reports status 0 *on
  success*, so the test is "did we get bytes".)
- **Warmed on the first user gesture**, alongside the piano. This matters more than
  it looks: the achievement fires **once**, at a moment that matters, and a buffer
  still loading would have dropped the crack and played brass only — silently, and
  exactly once, on the one occasion anyone would notice. Lazy-loading was not good
  enough here.
- Also preloaded when the diagnostics panel opens, so E cracks on its first tap.
- And if it is *still* not ready when the fanfare fires, the load is kicked off and
  the crack fires **as soon as it lands** (up to 1.5 s) rather than being dropped.
  Late beats absent. The brass runs regardless, so the fanfare is never silent.

Covers every path: the unlock itself, the achievement cue afterwards, the picker,
and a cold start where the sample has not been touched.

## v0.81.24 — four achievement quotes, and six Adventurer sounds to choose from

### Quotes
Four descriptions were generic self-help — "You know what you're doing now" says
nothing. The good ones in this app are twisted pop-culture misquotes; these now match.

| | |
|---|---|
| **Chord Scholar** | "Chords are words, and now you're learning to read" |
| **Practitioner** | "Wax on, wax off" |
| **Musician** | "I pledge allegiance, to the band" |
| **The Adventurer** | "You chose... wisely" |

EN and IT twins. The Italian for Karate Kid is the actual dub line — *"dai la cera,
togli la cera"* — which is the version Italians know.

### Six Adventurer sounds, pickable on-device
**On the copyright line:** music copyright protects the *melody* — the specific
sequence of pitches and rhythms. It does **not** protect intervals, instrumentation,
key, tempo, or style. Nobody owns "brass playing a rising fourth."

So none of these quote the Raiders March. What they borrow is the **gesture**
everyone actually recognises: a march-rhythm pickup, then a heroic leap up a perfect
**fourth**, played brassy and loud. That shape is the fingerprint of adventure
scoring generally and long predates the film. After the leap, every variant goes
somewhere the original does not.

| | |
|---|---|
| **A · fanfare** | Triplet pickup, the fourth, then away upward. Bright, mid-register. |
| **B · horns** | Same gesture an octave down, slower, fatter. Less fanfare, more swagger. |
| **C · march** | Pickup, the fourth, then a full answering phrase. The most tune-like. |
| **D · single** | No pickup. Just the leap, once, with weight under it. Confident, not showy. |
| **E · whip** | A snapped noise transient, then the fourth answers it. The effect and the theme arriving together. |
| **F · discovery** | The quiet one. A held open fifth, the fourth rising out of it. Finding the thing, not escaping with it. |

**Diagnostics panel → ADVENTURER SOUND.** Tap to hear each, back to back, no rebuild.
Whichever wins becomes `playAdventurerChime` and the other five get deleted.

## v0.81.23 — The Adventurer is a real achievement; Clair de Lune's famous bit

### The Adventurer rendered as a blank slot
Because it was not an achievement. It was a `localStorage` key with its own bespoke
toast, bolted onto the side of the system: no entry in `ACHIEVEMENTS`, no icon, no
rarity, no `check()` predicate. The achievements list renders **from** `ACHIEVEMENTS`
— so it drew an empty slot, exactly as it should have.

- Now a real secret achievement: proper entry, `check: s => !!s.rt_parchment_done`,
  a **compass-rose icon**, secret rarity, the standard toast with its ring burst.
- Finishing a parchment trip records the fact in `progState`; the normal engine does
  the rest.
- The old `localStorage` flag is **migrated**, so anyone who already earned it keeps
  it.

### It has its own sound now, and it is an Indiana Jones homage
Not a quote — the Raiders March is under copyright and this reproduces none of it.
What it borrows is the **gesture** everyone recognises: a triplet pickup, then a bold
leap up a **perfect fourth**, brass and swaggering. That interval-and-rhythm shape is
the fingerprint of adventure scoring generally and long predates the film. Voiced
with stacked saw + square for brass edge, a low fifth under the landing so the fourth
reads as an arrival, and a short convolved tail so it lands like a fanfare.

**And it unlocks as a selectable achievement cue** — "Adventurer", alongside "Secret
Found" and "Beethoven's Fifth", hidden until earned, using the same lock pattern as
the others. EN + IT.

### Clair de Lune was not broken; you were waiting for bar 27
The transcription is correct and complete — 93 beats, opening thirds through to the
main theme. The tune everyone knows is the *un poco mosso*, where the left hand
breaks from held chords into rolling quavers. Measured: that happens at **beat 65**,
which at 46 bpm is **~85 seconds** of quiet parallel thirds first.

Correct, authentic, and nobody waits that long. (Road Trip already knew: its entry
for the piece carries `hook:4` — "past the hushed open into the phrase.")

- **`clair_de_lune_famous`** — "Clair de Lune (main theme)". The same notes from beat
  65, rebased to start at beat 1: 43 RH, 43 LH, about 38 seconds of the passage the
  piece is actually famous for. Pedal down from the first note.
- The complete movement stays as `clair_de_lune`. **Both ship; keep whichever sounds
  right and the other can go.**

## v0.81.22 — the splash: iOS was rendering at half Android's frame rate

Same version on both phones, panels side by side, and the numbers ended four
theories at once:

|            | iPhone | Android |
|------------|--------|---------|
| splash fps | 59.2   | **116.3** |
| frames     | 231    | **454** |
| phase      | 26.82  | 26.74   |

**Identical total travel. Half the frames.** iOS advanced the wave in ~0.23 rad
steps where Android used ~0.09. Not slower — **coarser**. A coarsely-stepped
travelling wave reads to the eye as sluggish and lifeless, which is exactly what
"the iPhone wave just expands then dies out" describes.

And iOS was not struggling: 59.2 fps is a clean, capped 60. **WKWebView caps
`requestAnimationFrame` at 60 fps even on a 120 Hz ProMotion display** unless the
app opts in — Apple's default, so that apps written for 60 are not silently handed
a doubled frame budget. The iPhone had the same 120 Hz panel as the Android and was
using half of it.

### Fixed
- **`CADisableMinimumFrameDurationOnPhone`** added to Info.plist by CI. iOS now
  renders at the display's real rate.

### Why this is safe
120 Hz doubles the frame count, so any animation advancing by a **fixed amount per
frame** would run at double speed. Swept every `requestAnimationFrame` loop in the
file — **106 of them** — for that pattern: all are either time-based
(`performance.now()`, `ctx.currentTime`) or do not accumulate a fixed step. **Zero
at risk.**

The splash was the sole exception, and it was already normalised in v0.81.13 by
`dt60`. That fix was written under a wrong theory and dismissed as pointless when
the frame rate came back healthy. It turns out to be the thing that makes *this*
fix possible: without it, unlocking 120 Hz would have doubled the wave's speed.

### For the record, the theories this killed
Frame-rate scaling (v0.81.13 — right fix, wrong reason), canvas DPR (the geometry
is normalised; the wave spans 2.2 cycles of the width on any device), and the easing
curves (all clock-driven). Each was plausible and each was wrong. **The panel
measured its way to the answer**; none of the four rounds of reasoning got there.

## v0.81.21 — full review: mic-stop no longer kills live audio; two diagnoses corrected

A top-to-bottom read of the master-volume system and the iOS session handling,
prompted by the last builds' fixes wounding adjacent code. One real fix, two
corrections of the record, one theory formally killed.

### Fixed: turning the mic off stopped the metronome dead
The mic-stop path switched the session back to `.playback` immediately. That
switch rebuilds WebKit's audio output; everything scheduled ahead of "now" is
dropped, and the metronome — which schedules clicks ahead on a 25 ms interval —
lost its queue and died. A sustained drone glitched the same way.

The switch is only about **volume**, and a slightly-quieter metronome that keeps
playing beats a full-volume one that died. So it is now **deferred while audio is
busy**: if the metronome is running or any ref tone / drone is sounding, the
mic-stop marks the release as pending, and it fires the moment the coast is clear
— `stopMetro()`, the last `stopRef()`, and every natural-expiry timeout all flush
it. The panel shows `playback DEFERRED (audio busy)` when this happens.

Enabling the mic mid-playback still stutters briefly. That one is WebKit's own
`getUserMedia` reconfiguration, recording genuinely requires it, and it is not
ours to prevent. Likewise the short wait after mic-off before starting new audio:
that is the route change itself settling, and deferral cannot help when nothing
was playing to defer for.

### Correction: the makeup-gain loop was never missing
The previous diagnosis — "`setMasterVolume` computes `makeup` and never applies
it" — was wrong. The `_masterMakeupRegistry.forEach` is present and correct; the
diagnosis came from a read window that stopped one screen short of it. No fix was
needed, and none was applied.

### Which means: "slightly louder at 200%" is the system working
With the loop confirmed present, the on-device result is the honest output of the
design. The arithmetic for a metronome click: its peak rides ~-6 dBFS at 100%; at
200% the gain cap, compression and makeup net out to roughly **+4 dB of peak** —
audible, not dramatic. A click is a sparse transient: there are no quiet parts
*within it* to pull up, so loudness processing (which raises average energy) buys
little beyond the peak gain. Sustained material — chords, drones, samples — gets
substantially more from the same curve.

The remaining lever for percussive material is saturation (soft-clipping adds
harmonics the ear reads as loudness). That is new audio design, it colours the
click, and it is not shipping uninvited. Pinned as an option.

### The splash: renderer proven identical; the comparison itself is suspect
The wave geometry is normalized — `sin(u · 2.2 · 2π + phase)` where `u` spans the
width — so the wave has 2.2 cycles across the screen on **any** device, and the
canvas is DPR-corrected (`setTransform(dpr,…)`). Resolution cannot change its
apparent speed; the DPR theory is dead alongside the frame-rate theory. The
measured travel (26.82 rad ≈ 1.9 screen-widths at 59.2 fps) is healthy.

What remains: **the Android being compared against has not been rebuilt since
v0.81.2** — every push since has been iOS-only. If the splash was touched in any
intervening version, the two phones are running different animations. Verdict:
re-compare after the next `go.bat`, same version on both, panel numbers side by
side. If the numbers match and it still looks different, it is display physics,
not code.

## v0.81.20 — the metronome fader, the emoji triangle (properly), and slow mic release

### The master fader did nothing for the metronome
Because pocket mode was throwing it away:

    metroMasterGain.gain.setTargetAtTime(on ? 1 : 0, ...)

Un-muting set the gain to a **hardcoded 1**, wiping out whatever the master fader had
put there. Every pocket-mode toggle silently reset the metronome to unity, which is
why the slider appeared to work everywhere except the one place being tested.

- Unmute now restores the level the fader actually asks for, read from the gain
  registry rather than restating the number and letting the two drift apart.
- `setMasterVolume` now respects pocket mode: moving the fader while the metronome
  is muted no longer un-mutes it.

The metronome runs through `buildLimiterChain`, so with this fixed it gets the full
loudness curve — 4.2× makeup gain at 200%.

### The emoji triangle, actually fixed
v0.81.15 used `font-variant-emoji: text`. **Safari only honours that from 17.4**, so
on anything older it does nothing at all — which is what happened.

The fix that works everywhere is the **variation selector**: appending U+FE0E to the
character explicitly requests text presentation, and has been honoured for decades.
Applied to all **184** occurrences of U+25B6. The CSS property stays as a
belt-and-braces, plus a font stack that has the glyph but no emoji table.

### Mic release was slow
Disabling the mic left the app quiet unless you waited a moment.

`stopMic()` asked iOS to switch to `.playback` **before** stopping the microphone
track. iOS does not release the record path until the track actually stops, so the
category change was fighting a live capture. Waiting "fixed" it, which was the clue.

Moved: the session change now happens after `track.stop()`, when the capture is
genuinely gone.

### Deliberately not changed
The four hand-rolled limiters (Road Trip, rhythm cards, rhythm reader) stay at their
tuned **-6 dB / 20:1 / hard knee** and stay OUT of the loudness curve. The regression
sentinel pins the rhythm reader's value explicitly — someone tuned that and locked
it. They will not get louder above 100%; that is a decision already made, and this
build does not overturn it.

## v0.81.19 — hotfix: the splash diagnostic killed the splash

    Uncaught ReferenceError: Cannot access '_spd' before initialization

The wave-travel measurement added in v0.81.15 read `_spd` twenty-three lines above
where `_spd` is declared. `const` in a temporal dead zone throws on access, so the
splash loop died on its first frame.

Moved below the declaration. The splash-loop scope is now verified clean of any
read-before-declare.

**Both ship gates missed it.** `node --check` passes — a TDZ violation is a *runtime*
error, not a syntax error — and the sentinel does not model scope. Same class as the
`_PITCH_HIST_N` deletion in v0.81.13: code introduced that references something not
present at that point. The discipline that catches it is manual and simple: **when
inserting code that reads a variable, confirm the variable exists there.** Both of
tonight's incidents would have been caught by that one check.

## v0.81.18 — duplicate notifications

More than one of each reminder per day. Not a cadence choice; a bug.

The reminders were scheduled with:

    schedule: { at, repeats: true, every: 'day' }

The Capacitor docs are explicit about this: **"Use EITHER `at`, `on`, or `every` to
schedule notifications."** Passing `at` — a concrete datetime — alongside
`every: 'day'` — an interval — can register **both**, and you get two notifications.

### Fixed
- Both reminders now use **`on`**, the calendar matcher: `{ hour: 19, minute: 0 }`
  means "at 19:00, every day" by definition. Nothing to repeat, nothing to double
  up.
- This also removes the need to roll the date forward to tomorrow when the chosen
  time has already passed today — which `_notifTimeToDate` had to do, and which was
  its own route to a stale pending notification sitting alongside the new one.
- `allowWhileIdle: true` so the reminder still fires if the device is in Doze.

The cancel-then-schedule logic and the fixed IDs were already correct; the schedule
object was the whole problem.

## v0.81.17 — no way to repeat a wind note; Settings would not scroll in the guide

### Wind instruments had no way to repeat a note
Selecting a note on a wind instrument (trumpet, flute, clarinet, the rest) plays it
— but there was no way to hear it **again** without navigating away and back.
Fretted instruments can just re-tap a dot on the diagram; wind instruments have no
diagram, so once the note had sounded, that was that.

- **PLAY NOTE button** on the wind note card, replaying whichever note is showing.
  `gccPlayString()` already knew how to voice a wind instrument — it stops the
  previous note and uses `windSynth` — so this is only about giving that a button.
  EN and IT twins.

### Settings would not scroll inside the Survival Guide
Open the app's Settings while the Survival Guide is up, and the modal would not
scroll on iOS.

The guide's container is a full-viewport flex column with `overflow:hidden` and a
fixed height — it owns the entire screen while open. That starves the fixed-position
modal layered above it of touch scrolling: the gesture is swallowed by the guide's
non-scrolling box before the modal ever sees it. (Not a nesting or clipping problem
— the modal is a top-level sibling with its own `overflow-y:auto`. The guide was
simply competing for the touch and winning.)

- `body.settings-open` takes the guide out of the layout while Settings is up. It is
  behind a full-screen blurred overlay anyway, so there is nothing to see.

**Checked: it is the only module with this shape.** Every other `overflow:hidden` in
the file is a small inner element — a progress bar, a dropdown panel, a photo frame —
none of which own the viewport or can swallow the modal's touch. The guard is listed
by id rather than by a class, deliberately, so that if a future full-screen module
needs it, adding it is a conscious decision rather than something inherited by
accident.

## v0.81.16 — audio leaked out of modules through whichever gap you left by

Backing out of a tool or an exercise could leave its sound still playing.

Both exits stopped audio via a **hand-maintained list**: `exitTool()` had one line
per tool, `exitExercise()` had one line per exercise. And `stopAllAudio()` — which
already existed, already ran on backgrounding and pagehide, and was supposed to be
the complete list — was called by neither.

All three lists had drifted apart. `exitExercise()` knew about `diadleStop`,
`tonaleStop` and `roadtripStop`; `stopAllAudio()` did not. `exitTool()` knew about
`thmnStop`, `rcStop` and `ivrStop`; `stopAllAudio()` did not. Three lists, each with
holes the others filled, and sound leaking through whichever gap you happened to
walk out of.

### Fixed
- **`stopAllAudio()` completed** — all 30 stop functions, grouped and verified to
  exist. It is now genuinely the single source of truth for "make it quiet".
- **Both exits call it.** The per-module stops stay, because several also reset UI
  state (closing panels, clearing active notes) and are not redundant. This is the
  audio safety net underneath them, so nothing can leak because a module was
  forgotten on a list.

## v0.81.15 — metronome one-tap-and-stop, and the emoji triangle

### The metronome fired once and died
Toggling the mic and then starting the metronome would produce a single click and
stop; you had to start/stop again to get it going.

`startMetro()` and `playRef()` were both calling `_iosSyncAudioMode()` — a leftover
from the theory that a new audio source started while the mic is live can be
re-ducked and needs a nudge. But **changing the audio session category while the
metronome is spinning up disrupts the graph mid-schedule.** The click fires once and
the scheduler is left in pieces.

The session only ever needs changing when the **mic state** changes, and those
transitions already call it. By the time any audio starts, the session is already
correct — so both calls were pure downside. Removed. Three call sites remain: first
audio, mic start, mic stop.

### The start button had an emoji triangle
`▶` (U+25B6) appears in 164 buttons. **iOS renders it as a colour emoji; Android
renders it as a plain text glyph.** Same character, completely different button.

Fixed in CSS rather than editing 164 strings: `font-variant-emoji: text` asks for
the text presentation explicitly.

### Splash: the frame-rate theory is dead
The panel measured **58.7 fps**. It is not a frame-rate problem, so the `dt60`
normalisation from v0.81.13 — while correct, and worth keeping for future 120 Hz
devices — was not the fix.

"The iPhone wave just expands then dies out" says the horizontal *travel* is not
happening at all, which is a different bug from "slow". The panel now reports the
wave's **total accumulated phase** (which is literally the travel) and the device
pixel ratio. Compare the number against Android and this becomes arithmetic instead
of a fourth theory.

## v0.81.14 — the launch-quiet was the cache, not the category

Three volume levels, not two: launch audio was quieter than **either** the normal
mic-on or mic-off level, and only a mic toggle knocked it loose. That rules out
`playAndRecord` attenuation — that would land you at the mic-on level, not below it.

The panel showed the mechanism:

    audioMode   playAndRecord (cached) · metro

**The cache is right in principle and wrong at startup.** The app auto-starts the
mic at launch (deliberately — it is a quick-access tuner, and having to enable it
every time would be worse). That fires a session change **before WKWebView has
built its audio engine**. So we configure a session nothing is attached to yet;
WebKit then comes up with its own defaults; and because native cached the state as
applied, no later call ever re-applies it. The audio sits in WebKit's own
configuration, quieter than anything we chose, until a mic toggle changes `micLive`
and happens to bypass the cache.

### Fixed
- `setAudioMode` now takes a **`force`** flag. JS passes it until the first apply
  that lands with a live `AudioContext`; after that the cache is trustworthy and
  rapid start/stop stays free.
- The auto-start stays. It is the right product call; it was just exposing a race
  with WebKit's engine setup.

### Added
- **Splash frame rate in the diagnostics panel.** "The splash feels slower on iOS"
  has now had three theories and zero measurements. The panel reports the actual
  fps and frame count, so the next round starts from a number rather than another
  guess.

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
