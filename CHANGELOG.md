# Intonare — Changelog

A human-readable record of what changed, when,

---

## v0.201.192 — Hi-hat choke group, ghost sample fix, drum gain rebalance

- Hi-hat choke group: closing the hi-hat (closed or pedal) now kills any ringing
  open hi-hat with a 15ms fade-out. Tracked per source; works on both sample and
  synth paths.
- Ghost note double-reduction fixed: ghost samples (velocity layer 1) were being
  played at 0.4x volume on top of already being a soft articulation. Now played
  at 0.85x, letting the sample provide the dynamics. Flam ghost bumped to 0.55x.
- Clave removed from sample map (was mapped to cross stick, sounded wrong). Falls
  through to synth clave which sounds correct.
- Drum gain rebalance: kick boosted (1.0 to 1.4), cymbals pulled back, hierarchy
  set to kick > snare > toms > cymbals > percussion. Starting values for on-device
  tuning.

## v0.201.191 — AVL drum samples, spectral-flux tempo detector, tap tempo upgrade

- Drum samples: replaced Real Drums Vol. 1 with AVL Drumkits (GPL). Black Pearl
  for Standard kit, Blonde Bop for Jazz kit. 40 MP3 files (656KB total) at 192kbps
  mono, trimmed with per-voice fade-outs. Ghost notes use real soft velocity layers
  (layer 1) instead of gain-scaled normal hits. Electronic and brush kits stay
  synthesized. Synth fallback still fires if samples haven't loaded.
- Sample map restructured: entries are now { n:'normal', g:'ghost' } per voice.
  triggerInstrument passes ghost flag to _dkPlaySample which picks the right layer.
  Pitch-shift for tom1 (from tomhi) and tom2 (from floor) preserved.
- Tempo detector rewritten: spectral-flux onset detection replaces RMS energy gate.
  Half-wave-rectified flux across all frequency bins with adaptive threshold (running
  mean + 1.4x stddev). Outlier rejection (40% from median) on inter-onset intervals.
  Log-Gaussian octave-error prior centered at 120 BPM. EMA smoothing on final BPM.
  Settling state shows "listening..." while gathering first 3 onsets. 5-second onset
  window with 16-onset cap.
- Tap tempo upgraded: median filtering replaces simple average, 40% outlier rejection
  on intervals. Single mistap no longer shifts the reading.
- Tonale volume boost (main gain 0.16 to 0.32, octave doubler 0.07 to 0.10, low-shelf
  +5 dB to +10 dB). Replay preserves slider position.
- Drum BPM slider routed through progSetBpm (was calling setBPM directly, leaving
  progBpm stale so the debounced retime snapped the slider back).

## v0.201.190 — Notation/rhythm card polish, Tonale fixes, drum slider, full audit

- Notation Cards: horizontal swipe transitions (old card slides out, new slides in,
  direction-aware in browse and test modes). Two-element approach: snapshot cloned
  before content update, both animate simultaneously.
- Notation Cards: Next button after every answer (appears below options, not replacing
  them). Correct answers show after 700ms delay; wrong answers immediately.
- Notation Cards: result screen redesigned. Ring enlarged (140px, r=60), score split
  into big number + "/ total". Percentage moved outside ring. Subtext removed. Missed
  chips in red (var(--bad, #ff6b6b)). Result buttons: Again spans full width when
  Drill is hidden. Staggered entrance animations on ring, XP, and missed chips.
- Notation Cards: nc_next i18n key added (EN/IT). var(--bad) fallback #ff6b6b added
  to all notation card CSS rules (the variable was never defined; every other usage
  had the fallback, these didn't). Phase visibility fixed for track wrapper.
- Rhythm Cards: horizontal swipe in browse mode (same two-element pattern as notation
  cards, direction-aware from prev/next arrows).
- Rhythm Cards: test card slides in from right on each new question.
- Rhythm Cards: result breakdown rows cascade in with staggered slide-up animation.
- Tonale: volume boost (main gain 0.16 to 0.32, octave doubler 0.07 to 0.10,
  low-shelf +5 dB to +10 dB). Replay preserves slider position.
- Progression: drum BPM slider routed through progSetBpm (was calling setBPM directly,
  leaving progBpm stale; the debounced retime snapped the slider back on every drag).
- Full audit: all gate scripts pass. No dead code found. _rh song variants confirmed
  live (Rhodes voicings, dynamically loaded).

## v0.201.189 — Kit auto-play on mode switch, groove swap, blues shuffle tempo

- Fixed kit not auto-playing when switching from groove to drums mid-playback:
  mode switch now loads the named drum preset through the real loader (loadPreset)
  instead of relying on progRhythmState field-by-field apply, which missed timing
  fields and carried stale values from a different meter.
- Fixed mode switch overwriting progRhythmState with Drums module's state: added
  skipSave flag to progStopSyncSource so a mode switch hands the engine back
  without clobbering the Progression's saved drum and groove setup.
- Added explicit groove-mode guard in progStartSyncSource to force grooveModeActive
  and groovePattern when the preset has a groove, preventing straight-metronome
  playback from stale progRhythmState.
- Reverted groove/kit swap to restart-from-top (attempt 4 at phase-aligned hot swap
  failed on device, same as the previous three).
- Blues Shuffle tempo bumped from 88 to 96 BPM (groove and progression preset).

## v0.201.188 — Compound-meter sync, grace note pop, harmonica octave, BPM slider

- Fixed grace note pop in riff playback: grace note-offs were killing regular notes
  through the wrong voice pool (refOscs vs _riffVoices). Routed to pianoCardRelease.
  Affected Minuet in G, Ave Maria, Gnossienne, St. Louis Blues.
- Harmonica octave selector now highlights the specific hole at the selected octave;
  other holes on the same pitch class get a soft in-scale hint.
- Fixed BPM slider not tracking in progression sync tray: sliders and tempo name
  labels read the global bpm instead of progBpm.
- Fixed compound-meter sync between chords, groove, and kit. Root cause: the chord
  scheduler counted eighths while the groove engine counted dotted beats, producing a
  3:1 bar-length mismatch in 6/8, 9/8, and 12/8. All three engines now derive bar
  length from a shared felt-pulse helper. Flamenco, compas, and eskista pulse values
  declared in groove data. Kit tempo derived from TIME_SIGS table.
- Added 12/8 to PROG_TIME_SIGS (was missing; three 12/8 presets loaded with whatever
  meter the previous preset left behind).
- Corrected preset tempos: compound_jazz 160 to 53 (same speed, unit changed from
  eighths to dotted beats), solea 108 to 48 (previous groove fix was being overridden).
- progSetBpm now re-anchors all three engines through debounced retime, fixing tempo
  drift that accumulated when dragging the progression BPM slider.
- Groove/kit swap rewritten from restart-from-top to clock-based phase alignment.
  Falls back to restart when audio context is unavailable.

## v0.201.187 — Mandolin reverted to gleitz, lute doubled-course, drum gain fix

**Mandolin samples reverted to gleitz/FatBoy banjo** (v0.201.185-186). The
G-Town Church samples had too much reverb and the 14-note coverage caused
pitch-shift artifacts. Mandolin, bouzouki, and lute now map to the gleitz banjo
sample set via INST_TONE_MAP. Full chromatic coverage, no gaps. G-Town Church
credit removed.

**Doubled-course simulation made instrument-aware** (v0.201.186). The `dc`
flag is now passed by the caller based on `selectedInstrument`, not baked into
the SampleEngine descriptor. Banjo samples play as single strings for banjo,
doubled for mandolin/bouzouki/lute. All sub-types verified: mandolin (4),
bouzouki (6), lute (5), 12-string guitar (handled separately in chord tool).

**Lute added to doubled-course list** (v0.201.187). All five lute sub-types
(renaissance 6, renaissance 7, baroque, theorbo, mandore) now get the paired-
string simulation.

**Drum sample gain corrected** (v0.201.184). The original gain table used
full-sample RMS, which is meaningless for cymbals (3-second decay pulls the
average down 15dB). Corrected to attack RMS (first 50ms). Ride and crash
no longer boosted 2-3x; cowbell and tambourine pulled back.

---

## v0.201.182 — Real tambourine sample

Tambourine track now uses a real sample instead of the shaker placeholder.
`tambourine.mp3` (8.5KB) added to the drums folder. Both standard and jazz
kit maps updated.

---

## v0.201.181 — Real drum samples

Sample-based drum playback for Standard and Jazz kits. 17 MP3 files (292KB
total) from the Real Drums Vol. 1 pack replace the oscillator-based synthesis.
Electronic and Brush kits stay synthesized until dedicated sample sets are found.

`dkLoadSamples()` fetches and decodes all samples on first use (drum kit open or
Progression kit mode). `triggerInstrument` tries the sample path first and falls
through to the synth if the buffer is not ready.

Jazz kit routes through a BiquadFilterNode high-shelf (-6dB at 5kHz) that
darkens every hit without needing separate samples for shared pieces (toms,
hats, crash, cowbell). Distinct jazz kick, snare, and ride samples give the
kit its own character on top of the filter.

Derived pieces by pitch-shift: hi-hat pedal (closed hat at 0.85x), low tom
(mid tom at 0.80x). Placeholders: clave uses rim, tambourine uses shaker.

Latin kit maps to the standard sample set (same acoustic sounds, different
patterns).

---

## v0.201.180 — Bugfixes, progression BPM block, mandolin samples

**DONE button after daily (v0.201.159).** The daily result hid the DONE button
and rewired the primary to `mqGoLanding`. Neither was ever reset, so every
quick play result after a daily had no way out.

**Daily quiz locale filter (v0.201.160).** `mqBuildDailyQuestions` skipped the
`mqQInLocale` check entirely, serving Italian-tagged questions to English users.

**Drawer always GPU-composited (v0.201.163).** Push mode animated `height`
(layout recalc every frame); overlay animated `transform` (GPU). Push mode
removed; one animation path, always smooth.

**Question band taller (v0.201.159).** 196px to 220px for longer questions.

**Double back arrow (v0.201.162).** `mq_back` string carried `←` while markup
already had its own arrow. Stripped from both languages.

**Solfege in all charts (v0.201.165).** Seven display paths routed through
`getDisplayNote`: harmonica, Road Trip, Tonale, vocal range, harp pedals.

**ALL PACKS button (v0.201.167-173).** Name left, pack count pill, arrow right.
Full width aligned with the grid below via `display: flex; width: calc(100% - 28px)`.

**Console.logs cleaned (v0.201.164).** Six removed; two kept (fallback toast,
mock data injector). Orphan `</div>` between mqModal and mqQuickSheet removed.
Markup balanced at 2783/2783.

**TDZ crash fixed (v0.201.175).** `_rcHolder` was `let` at line 95699 but
`_rcActive()` was called during boot 38,000 lines earlier via `setBPM` →
`progSyncBpmDisplays`. Changed to `var` to avoid the temporal dead zone. This
crash interrupted Pro status restore and version stamp handler wiring.

**Progression BPM block (v0.201.174-178).** Groove/beat name in the BPM pill
only shows when metro or kit mode is active. Transport row buttons all 56px.

**Mandolin samples (v0.201.179-180).** G-Town Church Sampling Project (Tobias
Marberger, CC Sampling+ 1.0). 14 WAV samples converted to MP3 (356KB total).
SampleEngine registration with custom `sampledNotes` list. Doubled-course
simulation: second source at +7 cents, 4ms delay, -2dB for the paired-string
mandolin sound. Credit added to Credits & Thanks.

---

## v0.201.165 — Solfege mode reaches every chart and tool

Seven display paths were using hardcoded English note-name arrays instead of
going through `getDisplayNote`, so switching to solfege mode in settings changed
the tuner and some tools but left the rest showing C D E. All seven now route
through the same function:

    Harmonica chart       inline arrow fn → getDisplayNote wrapper
    Harmonica info bar    noteNames[pc] → getDisplayNote(noteNames[pc])
    Road Trip labels      RT_NOTE_NAMES → getDisplayNote(RT_NOTE_NAMES)
    Tonale reveal keys    TONALE_NOTE_NAMES → getDisplayNote(TONALE_NOTE_NAMES)
    Vocal Range (3 sites) VR_DISPLAY_NOTES → getDisplayNote(VR_DISPLAY_NOTES)
    Harp pedal labels     NOTE_NAMES[pc] → getDisplayNote(NOTE_NAMES[pc])

Verified in headless Chrome: C→Do, D→Re, F#→Fa♯, Bb→Si♭ in solfege mode,
unchanged in english mode. The chord/scale charts already went through
`gccRootDisplayName` which calls `getDisplayNote`, so those were fine.

---

## v0.201.164 — Cleanup: console.logs, orphan div, double back arrow

**6 console.logs removed.** Mic debug, sync diagnostic (3), sample engine ready,
road trip tuner. Two kept: the fallback toast error path (last resort) and the
mock data injector (console-only dev tool).

**1 orphan `</div>` removed.** Sat between mqModal closing and mqQuickSheet
opening. The initial count of 4 extras was wrong: 3 were inside JS template
strings where the regex counted `</div>` in a return statement without seeing
the matching `<div` concatenated on the same line. Markup is now balanced:
2783 opens, 2783 closes.

**Double back arrow fixed in v0.201.162.** The `mq_back` string carried its own
`← ` while the markup already had an SVG or entity arrow. Every back button
rendered two arrows.

---

## v0.201.163 — Blurb drawer always uses the smooth path

The blurb panel after a quiz answer had two animation modes: an overlay that
slides up with `transform: translateY` (GPU-composited, always smooth) and a
push mode that grows with `height` transitions (triggers layout recalc every
frame, stutters on mid-range phones). Push mode fired when the blurb was short
enough to fit under the answers without covering them. The two modes had
different corners and shadows until v0.201.161, and different animation
smoothness that v0.201.161 could not fix because the issue was the animation
engine itself, not the timing or the curve.

Push mode is now disabled. The overlay handles every case push did: the verdict
line restates the answer when the overlay covers it, and the drawer scrolls if
the blurb is tall. One animation path, one visual, always GPU-composited.

The three push-specific CSS rules are left in place (dead but harmless) so they
do not need to be found and removed in a file this size.

---

## v0.201.161 — Push drawer matches the overlay drawer visually

The blurb panel has two modes: an overlay drawer (slides up over the answers)
and a push panel (sits under them when there is room). The overlay had rounded
top corners and a shadow; the push had flat corners and no shadow. They looked
like two different UI elements doing the same job.

Push now gets `border-radius: 16px 16px 0 0` and a lighter shadow (18px spread
at 18% rather than 32px at 42%, since it is not floating over content).

The animation smoothness difference (overlay slides, push might snap) still
needs device investigation. The CSS transitions are structurally identical:
both run the same cubic-bezier over 520ms. The measurement and timing are
correct on paper. A screen recording from device shows the fault; reproducing
it in headless Chrome has not been possible.

---

## v0.201.160 — Daily quiz skipped the locale filter

The regular round builder calls `mqQInLocale` on every question, so a question
tagged `loc:'it'` never appears for an English user. The daily builder did not
call it at all: it checked `q.q && q.opts && q.opts.length === 4` and nothing
else. An English user playing a daily 70s round could get Guccini and Celentano
questions that are tagged Italian-only.

One line: added `&& mqQInLocale(q)` to the daily's pool filter.

---

## v0.201.159 — DONE button vanishes after a daily, question band taller

**The DONE button.** The daily result hides it (`display: none`) and points the
primary button at the landing page. Neither was ever reset. So every quick play
result after a daily showed only PLAY AGAIN, which was still wired to
`mqGoLanding` from the daily rather than to `mqPlayAgain`. It looked like PLAY
AGAIN was taking you to the menu because it was: it was the daily's button
wearing the wrong label.

Non-daily results now restore both: DONE is shown and the primary is rewired to
`mqPlayAgain`.

**Question band height.** Was 196px, now 220px. Long Beatles and 70s questions
were cramped at 24px Fraunces over four lines, and the auto-shrink floor meant
the text dropped to 15px before the container gave any more room.

---

## v0.201.158 — Advanced Theory goes live

Three things that were blocking it:

**Removed from MQ_GEN_ONLY.** The list told the app this pack has no written
questions and must never deal one. It was true before the 40 were written and
never updated. The list is now empty.

**No blend floor needed.** With 40 written questions across tiers 11/16/13,
MQ_GEN_SHARE at 34% means a 10-question medium round asks for about 7 written
and 3 generated, so the written ones are not buried. The existing cap handles it.

**Italian translation of all 40.** Questions, options, and blurbs, all installed
via pack_build with a clean round trip. Italian check, draft check and spelling
audit all pass.

The pack now serves six topics the generators cannot produce: voice leading,
non-chord tones, modulation, modal interchange, form and phrase, and texture.

---

## v0.201.157 — The Survival Guide term audio has never worked

`SG_TERM_DEMOS` (36 demo entries) and `sgPlayTermDemo` (the function that plays
them) are defined inside a script block that is a plain `<script>` child of
`<body>`, with no module type, no IIFE wrapper, no SVG namespace and balanced
braces. `node --check` passes. The `var` assigns correctly inside the block:
a log placed right after the closing brace shows an object with 36 keys.

And then it vanishes from global scope. Every function declaration in the same
block is also invisible to the rest of the page. `typeof SG_TERM_DEMOS` returns
`undefined` from any other script block and from the console. `typeof
sgPlayTermDemo` returns `undefined`. The onclick handlers in the Survival Guide
markup could never reach either one, so tappable term sounds have never played.

The root cause is not identified. The workaround is to assign both onto `window`
explicitly: `window.SG_TERM_DEMOS = {` instead of `var SG_TERM_DEMOS = {`, and
`window.sgPlayTermDemo = sgPlayTermDemo` right after the function definition.
All three read sites updated to `window.SG_TERM_DEMOS[...]`.

The boot check now passes clean for the first time this session.

---

## v0.201.156 — One more Vader quote in a name slot

Master's Italian name was "Ora sono io il maestro", which is the Vader line from
the description. Every other rank in the ladder is a plain word: Apprendista,
Praticante, Musicista, Gran Maestro. This one was a sentence sitting in the
middle of them. Now "Maestro", and the ladder reads as a ladder.

Found by printing all 240 fields and reading them, which is the sixth time
tonight that the check which caught the fault was reading the output rather than
running a test.

---

## v0.201.155 — Boom/Headshot was backwards

The English is: name Boom, quote Headshot. Two gaming words for the same hit.
Both are universal, both are what Italian gamers say. The Italian had the quote
in the name slot (Headshot) and an invented replacement in the quote slot
("Primo colpo, centro!"). The fix is the simplest one tonight: Boom / Headshot,
the same words, because they are the same in both languages.

Checked whether the same fault existed on any other entry: it did not. This was
the only one where I had moved an English quote into the Italian name and then
written something to fill the gap I created.

---

## v0.201.154 — Last achievement fix: Boom had Headshot twice

Name and description were both "Headshot", so the card showed the same word
twice. The English has two different words for the same hit: Boom / Headshot.
The Italian desc is now "Primo colpo, centro!" which carries the same energy
without repeating the name.

All 40 achievements verified clean by automated sweep: no name that is a quote,
no name identical to its description, no empty Italian description, no
untranslated name that should have been, no sentence punctuation in a name.

---

## v0.201.153 — Crikey! gets the Dundee knife scene

The didgeridoo pun did not survive translation: "Let's Didgeridon't and Say We
Didgeridid" is English syllable play with no Italian equivalent. Three attempts
at an Italian version (a literal meaning, a didgeri-no/si flip, a spelling joke)
all died on contact.

The Crocodile Dundee knife scene is the most repeated Australian quote in Italian
pop culture. The dubbed line is "Quello un coltello? Questo e un coltello!" and
an Italian blog noted it has been repeated by "every single Italian for years."
Swapping knife for instrument:

    EN  That's not an instrument... THAT'S an instrument
    IT  Quello uno strumento? Questo e uno strumento!

An Italian reads that and immediately hears Dundee, which gets you to Australia,
which is the whole joke. And the didgeridoo is exactly the instrument you would
hold up doing the bit.

---

## v0.201.152 — Eight descriptions were my translations, not the real dub lines

The research found the actual dubbed wording. The descriptions were written
before the research, and nobody went back to install it. Eight swapped to the
sourced lines:

     6  "Non dirmi le probabilità"         ->  "Non t'ho chiesto pronostici"
     8  "Hai spento il computer di mira"    ->  "Ha spento il computer di bordo"
    12  "Non tutti coloro che vagano..."    ->  "Né gli erranti sono perduti"
    13  "Dove stiamo andando, non abbiamo"  ->  "Strade? Dove stiamo andando non
                                                 c'è bisogno di strade!"
    14  "Troverò la mia strada..."          ->  "Posso farcela, posso andare lontano"
    21  "Hai scelto... saggiamente"         ->  "Hai scelto... bene"
    24  "Datti da fare per vivere..."        ->  "O fai di tutto per vivere..."
    36  "Non siete forse divertiti?"         ->  "Non vi siete divertiti?!"

Two more:

    29  "Colpo alla testa" -> "Headshot". Italian gamers say it in English, and
        the name is already Headshot, so "Colpo alla testa" underneath it was the
        only translated gaming term in the whole set.

    32  "Facciamo finta di averlo fatto..." -> "Didgeri-no e poi Didgeri-sì".
        The English pun is did-geri-DON'T / did-geri-DID. The literal Italian
        had no joke. The Italian keeps the didgeridoo root and flips no to sì.

---

## v0.201.151 — Daily Grind was still a quote

"Stessa ora domani?" is "Same time tomorrow?", which is the description, not a
name. Every other name in the list is a noun phrase; this was a question. Now
"Tran tran quotidiano", which is the Italian for the daily grind.

All 40 achievement names audited against their unlock conditions. Every name is
either a plain Italian word matching its English counterpart, an established
title (film, piece, show), or kept in English where that is authentic Italian
usage. No quotes pretending to be names remain.

---

## v0.201.150 — Four more quotes where names belong

Same fault as the previous thirteen, caught by Daniele on a second read.

    Addicted             Assuefatto          (was "Sono i chilometri")
    Last One Standing    L'ultimo in piedi   (was "Non vi siete divertiti?")
    The Adventurer       L'avventuriero      (was "Hai scelto bene")
    Great Ears Kid...    Orecchio fino       (was the full nine-word dub line)

The dub lines stay in the descriptions.

---

## v0.201.149 — Thirteen achievement names had the quote where the name goes

The English structure is: the NAME says what you did, the DESCRIPTION carries the
joke. Apprentice is a rank; "You have taken your first step into a larger world"
is the Obi-Wan line underneath it. Thirteen of the Italian names were the quote
from the description stuffed into the name slot, so the name stopped describing
anything and the level ladder collapsed into five unrelated film quotes.

Fixed:

    Perfect Pitch    Orecchio assoluto    (was the Yu-Gi-Oh quote)
    Curious          Curioso              (was the Tolkien sentence)
    Explorer         Esploratore          (was the BTTF quote)
    The Climb        La scalata           (was the Hercules song)
    Apprentice       Apprendista          (was the Obi-Wan quote)
    Practitioner     Praticante           (was the Karate Kid quote)
    Musician         Musicista            (was the pledge quote)
    Maestro          Gran Maestro         (was the Yoda fragment)
    Dedicated        Devoto               (was the Shawshank quote)
    First Blood      First Blood          (was "Rambo"; it is a Halo callout)
    Trivia Night     Serata quiz          (was the Millionaire lifeline)
    Golden Ear       Orecchio d'oro       (was the Qui-Gon quote)
    Completionist    Completista          (was the Pokemon slogan)

The sourced dub lines stay in the descriptions where they belong.

---

## v0.201.148 — Achievement names in Italian, sourced rather than translated

All 40 have a `name_it` now, read through one helper, `achName`. The descriptions
have had `desc_it` since they were written; the names never had a twin.

Where a name is a quote, the Italian is the line that was actually dubbed, taken
from Italian Wikiquote, the 1977 Guerre stellari transcript, Pokemon Central Wiki
and the rest, not a translation of the English:

    I Have You Now        Ora ti tengo
    Great Ears Kid...     Sei grande, ma non ti montare la testa
    Master                Ora sono io il maestro
    Maestro               Bello non sembrerai
    Practitioner          Dai la cera, togli la cera
    The Adventurer        Hai scelto bene
    Explorer              Non c'e bisogno di strade
    Last One Standing     Non vi siete divertiti?
    Completionist         Acchiappali tutti!
    Know-It-All           Sapientona
    Perfect Pitch         Il cuore delle carte
    The Climb             Posso farcela

Seven stay English on purpose, because that is what Italians say: Flawless
Victory, Headshot, Giant Steps, Crikey!, I Got a Fever, It's Dangerous to Go
Alone, and Everything Everywhere All at Once, which is the Italian release title.
Two use the Italian release title instead: Rambo for First Blood, Tutti per uno
for Hard Day's Night, and Gli amici di papa for Full House.

**Four entries write their name in double quotes** because the name contains an
apostrophe. A bulk pass matching single quotes skipped those four, then inserted
their value into the NEXT entry along, giving three achievements two `name_it`
keys where the second silently won. Caught by listing all forty and reading them,
which is the only check that would have found it.

---

## v0.201.147 — Deaf Composer

The id is `deaf_composer`, the unlock is solving a Chordle without ever pressing
play, and the description is Beethoven on music being a dream he cannot hear. The
name said "Dead Composer", which is a different and much worse joke. Confirmed
with Daniele and corrected.

Achievement names in Italian are still open. The descriptions have been localised
with real dub lines since they were written; the 40 names have not. Draft and
sourcing notes are in ACHIEVEMENTS_TRIAGE.md.

---

## v0.201.146 — Twelve strings that were never wired for translation at all

The previous version fixed elements that HAD a `data-i18n` attribute and were not
being relabeled. This is the other half: text that had no attribute, so no sweep
was ever going to find it and no relabel could ever reach it.

    tcToggleBtn         START DRONE          AVVIA BORDONE
    hpPlayBtn           PLAY ASCENDING       SUONA IN SALITA
    bowedScalePlayBtn   PLAY ASCENDING       SUONA IN SALITA
    bowedNoteLabel      SELECT A NOTE        SCEGLI UNA NOTA
    bowedScaleName      SELECT ROOT + SCALE  SCEGLI TONICA + SCALA
    bowedDsPlayBtn      PLAY DOUBLE STOP     SUONA BICORDO
    prGoBtn             START                AVVIA
    pmGraphPeriod       THIS WEEK            QUESTA SETTIMANA
    pmXpText            XP to LV             XP al LIV
    diadleStatusText    NAME EACH NOTE       NOMINA OGNI NOTA
    rrSurvEndTitle      GAME OVER            PARTITA FINITA
    rr-surv-end-again   PLAY AGAIN           GIOCA ANCORA

The rhythm survival panel was the clearest case: GAME OVER and PLAY AGAIN in
English, SERIE and ESCI in Italian, in the same box, because two of the four
happened to have been wired and two had not.

The XP line was hidden differently. It was built in a template literal, with the
English sitting inside the string where no attribute could reach it, so it read
"120 / 300 XP to LV 4" in both languages. It takes a key with placeholders now.

Boot measured at zero stale in both languages.

Two things deliberately left in English: the credits, where Open Trivia Database
and the Noun Project are proper names, and the achievement titles, which are
jokes that do not survive translation. Say the word if the achievements should be
Italian and they can be done properly rather than literally.

---

## v0.201.145 — 106 English strings inside the Italian app, one ordering fault

Not missing translations. Every one of them existed: ESCI, Lo sapevi?,
PRECISIONE, FATTO, PARTITA VELOCE were all sitting in the Italian dictionary and
resolving correctly when asked. They were simply never applied.

`applyLang()` at boot is an inline script, so it runs while the parser is still
working, and roughly 29,000 lines of markup come after it, the whole Music Quiz
among them. It relabeled a document that did not contain those elements yet.

That is why it looked like scattered random leaks. Anything a function drew later
with `t()` came out in Italian; anything sitting in static markup with a
`data-i18n` attribute stayed English. Same screen, both behaviours, which sent
several searches looking for missing strings that were never missing.

One more pass on DOMContentLoaded. Measured on a boot with Italian saved:

    before   106 stale of 1059
    after      0 stale of 1058

English boots clean, Italian boots clean, and switching language mid-session is
unaffected. Pinned, since the fault is invisible in the file and only appears on
a cold start in the second language.

---

## v0.201.144 — PATCH NOTES on the update card

A link under the subtitle, opening the store listing, where the release notes
already are.

**There is no way to read the notes from Play directly.** `AppUpdateInfo` carries
an availability flag, a version code, a priority, staleness in days and a byte
count, and nothing else; release-note text is not in the API at all. The Play
Developer API does hold the listing, but it needs a service-account key, and a key
shipped inside a client gives anyone who unzips the APK write access to the
listing. So the store page is the only honest source, and pointing at it means the
notes can never fall out of step with what was actually published, which a copy
bundled in the app would.

A link rather than a third button, since the row underneath is where the decision
happens and this is only for reading first. It reuses `openAppStore` from the same
plugin the card already uses. Both languages.

On iOS it will open the App Store listing once there is one; TestFlight builds
carry their notes in the TestFlight app instead.

---

## v0.201.143 — ALL PACKS

The button said ALL PACKS with an arrow, which reads as a promise to start. It
opens a sheet now, so it is just the name of the thing. Both languages, and the
markup default matches so it is right before the translations load.

---

## v0.201.142 — ALL PACKS gets the popup too

Same fault as the online categories, in the one place left with it. ALL PACKS
started the moment you tapped it, on a hardcoded ten questions, at whatever
difficulty happened to be set from before. Every individual pack offers a choice
first; the button that plays all of them did not.

It opens the same sheet now, and all three routes into it behave alike:

    ALL PACKS   PLAY, 3 difficulties, 4 counts, "MED . 10 questions . ALL PACKS"
    local pack  PLAY, 3 difficulties, 4 counts, "MED . 10 questions . The Beatles"
    online cat  PLAY, 3 difficulties, 4 counts, "MED . 10 questions . BANDS"

The button label loses its promise of ten, in both languages, since the count is
now chosen rather than fixed.

On the report of it starting easy: the blend is not at fault. `MQ_BLEND.medium`
asks for 2/6/2 out of ten and the shipping packs hold 281 easy, 278 medium and
136 hard, so nothing runs dry. The likelier explanation is that the button never
offered a difficulty, so the last one set carried over silently. With the sheet in
front of it that is now visible either way.

---

## v0.201.141 — The summary under the play button

Two faults in the line that reads "MED, 10 questions, BANDS".

**It was hidden when the sheet opened.** I had switched it off for online
categories on the grounds that a fetched set has no local statistics, which was
wrong twice: the line is a summary of the choices, not a stats readout, and
tapping any chip called `mqRenderPopupSummary` and showed it anyway. So it
appeared out of nowhere the first time you changed something.

**And it ended on a stranded separator.** The last field is the name of what you
are about to play, read from `PACKS[MQ_POPUP_PACK]`. An online category has no
entry there, so the name came back empty and the line rendered as "MED, 5
questions," with nothing after the comma. It reads the category name now, and the
three fields are joined rather than concatenated, so an empty one can never leave
a separator hanging whatever the reason.

    on open       MED · 10 questions · BANDS
    survival      MED · 3 lives, no end · BANDS
    local pack    MED · 10 questions · The Beatles

---

## v0.201.140 — The online popup's play button had no label

`mqShowPackPopup` ends by setting the button text, either PLAY or START SURVIVAL.
The online version did not, so the button came up blank and only filled in when a
difficulty tap happened to re-render the sheet.

Two other things were missing with it. Survival hides the question count row,
since survival sets its own length, and the online popup was showing it. And the
survival label was never applied at all.

    online quick      PLAY →
    online survival   START SURVIVAL →, count row hidden
    local pack        unchanged

---

## v0.201.139 — Online packs get the same popup every local pack gets

Tapping an online category in the quick sheet started the round immediately.
Every local pack goes through `mqShowPackPopup` first and is offered a difficulty
and a question count; the online ones went straight past it. The odd part is that
`mqRunOnlineFetch` already reads `MQ.diff` and already sets `MQ.qCount`. The
choice existed the whole time and nothing ever offered it.

`mqShowOnlinePopup` fills the same sheet from an online category, and
`mqPopupPlay` finishes the job for either kind. A separate entry point rather than
a branch inside `mqShowPackPopup`, because that function reads `PACKS[packId]` a
dozen times and an online category is not a pack.

**And a warning about the edit itself.** The original was
`async function mqQuickPlayOnlineCat`. The replacement started at `function`, so
the `async` keyword was left stranded in front of a comment, where it parses as a
bare identifier and throws at runtime. `node --check` passed the file. The error
killed the rest of that script block, which took out `MQ2_DIFFS`, the difficulty
chips and the local pack popup as well, none of them anywhere near the edit.

`intonare_boot_check.mjs` now loads the app in a real browser, fails on any error
thrown during boot, and checks that a set of globals exist that only exist if
their block ran to the end. It catches the fault above in about four seconds.

---

## v0.201.138 — A wrong date in a shipping blurb

Daniele asked whether the Fundamentals blurbs had been through the same passes as
the questions. They had not: register, tells and leaks were all done, but nothing
had checked whether the blurbs are TRUE.

Twenty of the sixty carry a checkable claim. Nineteen hold up: the 1939 London
conference and the 1955 ISO adoption of 440, Vienna and Berlin at 443, baroque at
415, Cristofori's gravicembalo col piano e forte, Maelzel's 1815 patent and
Beethoven's marks on eight already-published symphonies, rubato meaning stolen,
Chopin's left hand, BACH in the unfinished fugue of The Art of Fugue, Bernstein's
America, Ut queant laxis.

One was wrong. **Q51 said the earliest source connecting the Picardy third to
Picardy is a French dictionary from 1703.** It is Rousseau's Dictionnaire de
musique, 1767. The blurb now names Rousseau and the right year, and adds what the
sources agree on: most scholars no longer believe the Picardy connection at all,
and think the name comes from an old French word for sharp.

Both languages changed together.

**The lesson is the pass, not the date.** Checking that a question has one right
answer and checking that its blurb states the truth are two different jobs, and
only the first had been done here. Nineteen of twenty is a good rate, but the
twentieth was live in the app.

---

## v0.201.137 — Reading the options against the stems, on Fundamentals this time

Daniele asked whether the same pass had been run here as on Advanced Theory. It
had not. The register work, the leak pass and the tell sweep were all done; the
read that finds a SECOND correct answer was not, and on Advanced Theory that read
turned up three faults every checker had passed.

Sixty questions read. One real fault and two borderline, which is a cleaner
result than 3 in 40 and reflects how much this pack has already been looked at.

**Q30 asked which naming system Italy, France and Spain use, with "Ut Re Mi" as a
distractor.** French solfege still uses ut for C, so naming France made the
distractor defensible. Italy and Spain alone are unambiguous.

**Q25 asked which pair of white keys has no black key between them.** B and C
also qualifies. It was not among the options so the question worked, but "which
pair" implies one and there are two. It asks "which of these pairs" now.

**Q48 is left as it is, and noted.** A plain double bar marks a section change
and the end of a piece takes a final barline, thin-thick. "At the very end" in
the stem carries it, but the two terms are not the same and a strict reader would
notice.

Both stems changed in English and Italian together.

---

## v0.201.136 — Theory Fundamentals passes the AI-tell check

Twenty-two of them, cleared. The checker was built earlier tonight against
Daniele's own 194 blurbs, so a pack written before it existed was always going to
fail it; that was the tool working, not a regression.

    which is why / the / what   4       exactly what / why    3
    the rest of the             3       everyone              3
    and that is, at all, is what makes  6
    rather than                 7   (done in the previous version)

Worth recording: **three of my own fixes introduced a new tell.** Swapping
"which is what makes a rhythm pull" for "and that is what pulls a rhythm" traded
one flagged construction for another, in three separate blurbs, and the checker
caught it on the rerun. That is the exact failure the tool exists for, and it
happened within a minute of the edits that were meant to fix the problem.

Where the packs stand on this check:

    beatles             0       eighties            4
    guitar_technique    0       guitar_gods         5
    theory_fundamentals 0       seventies           7
                                bass                7

The two at zero are Daniele's own writing, which is what the checker is
calibrated on. Fundamentals now joins them.

---

## v0.201.135 — Seven closing beats out of Theory Fundamentals

Not a rewrite. The pack runs two-sentence blurbs at a median 37 words and that is
right for it: it teaches things people half-know, so a second sentence carrying
the part they did not know earns its place. Advanced Theory defines terms, where
one sentence is the whole answer. Different jobs.

What came out is the second sentences that were a flourish rather than
information. A crude check flagged 13; reading them, only seven were:

    52  "The tension is the point."                          cut
    9   "...entirely up to whoever is in charge!"            the names stay, the joke goes
    56  "an expensive bow is not built for hitting things!"  replaced with what players do
    28  "which is why it outlived the argument"              mine, from earlier tonight
    49  "which is the whole bargain"                         says the benefit instead
    50  "a trade Bach clearly thought worth making"          states the other half of the trade
    29  "That was the whole point:"                          explains the difference instead

The other six the checker flagged were false positives and are untouched. Their
second sentences teach something: the semibreve etymology, what the bass clef
covers, that a sharp holds for the rest of the measure. One was not a two-sentence
blurb at all, the splitter broke on the period in "D.C."

All fourteen strings, seven English and seven Italian, changed together.

---

## v0.201.134 — The streak chip kept the last round's number

It was written inline in two places and both of them run AFTER an answer. Both
start paths already set `MQ.streak = 0`, but neither had any way to say so on
screen, so quitting on a streak of five and starting again left the chip reading
five until the first question of the new round was answered.

One painter, `mqPaintStreak`, reading `MQ.streak` and nothing else. Called from
the answer path, the render path, and now from both starts. Verified in a
browser: five and visible mid-round, zero and hidden the moment a new round
begins.

---

## v0.201.133 — Fretboard dot labels were near-black on a near-black dot

The dot is filled with `accent`, which is `MQ_INK`, which is `var(--text)`. That
is near-white on a dark band and near-black on a light one. The letter on top was
a fixed `#0d0f12`, so it read at 14.8:1 in dark mode and disappeared entirely in
light, where it was near-black type on a near-black circle.

The label takes `var(--surface)` now, which is the opposite of `--text` in both
modes by definition, so it contrasts with its own dot whichever way round the
theme is. Measured in a browser:

    dark    dot near-white   letter near-black   14.8:1
    light   dot near-black   letter near-white   10.7:1

That was the only fixed near-black left on a diagram that flips with the theme,
and the sentinel now refuses to let another one in.

---

## v0.201.132 — The motif flashed at full, and the answer keys collided with the answers

**Dark, then fades.** The motif's entrance ran `mq2BandIn`, which is
`opacity: 0 -> 1` with fill-mode `both`. An animation beats a plain declaration,
so the mark sat at FULL opacity for the whole entrance and only dropped to its
tier value when `.mq2-arrive` came off. That drop is the fade. The wrapper carries
its own keyframe now and the tier opacity is never touched. Measured: 0.17 during
and 0.17 after on theory, 0.26 either side on the eighties.

**The key badges were wearing the answers' letters.** Measured over 18,000
generated questions:

    an option whose text is literally A, B, C or D     12.4%
    every option two characters or fewer               19.8%

Note names run A to G, so a badge reading A beside an answer reading A is two
different things in the same letter. On the fretboard questions it is three deep,
because the diagram labels its dots A to D as well, and "which of the marked
positions is an F" stops being readable at all.

A badge is shorthand for a long answer. When every answer is two characters or
fewer there is nothing left for it to be shorthand for, so it is dropped and the
answer centres in the tile instead of sitting under the gap where a badge used to
be. Verified in a browser: note names lose the badges, "Four / One / Two / Three"
keeps them, because those are words.

---

## v0.201.131 — Eleven lines, not fifteen, and light mode stops darkening the ink

**The 80s grid, against references this time.** The laser grid has a settled
shape and the teaching versions all agree on it: one line down the middle and
five to each side, converging on a central vanishing point, with five or six
horizontals crowding toward the horizon. Fifteen verticals and nine horizontals
smeared the top third into a solid band, which is the opposite failure to the one
before it, where nine lines never converged at all and it read as slanted stripes.

    v0.201.129    9 verticals, none converging      ambiguous
    v0.201.130   15 verticals, 9 horizontals        busy
    now          11 verticals, 6 horizontals        the convention

**Light mode stops pushing the ink toward black.** On a dark band the mark is
lifted toward white, so the obvious mirror was to push it toward black on a pale
one. That is wrong: a mark tinted toward black reads as dirt on a pale ground
rather than as a tint of the pack. 80% was soot, 62% was still muddy. It takes
the pack ink as it is now, and the opacity alone decides how far back it sits.

    dark    0.45 / 0.30
    light   0.26 / 0.17,  ink undarkened

**And the guitar packs were the wrong way round.** guitar_technique is the heavy
one and belongs in the lower tier; guitar_gods goes back to 45%.

---

## v0.201.130 — The 80s grid had no vanishing point

**Why it read as ambiguous.** The nine perspective lines ended spread across
x=24 to x=96 at the horizon. They never met. It was not a grid going away from
you, it was nine slanted lines, and no amount of opacity was going to fix that.

Fifteen lines now, all converging on a single point at (60, 72), which is where
the first horizontal sits. And nine rows instead of six, spaced by a power so the
gaps widen from 2.8 at the horizon to 19.3 at the bottom, the way real ones do.

**guitar_gods drops to the lower tier**, joining bass, keys, vocals and the two
theory packs. It is a drawn object rather than line work, so it carries the same
weight those do.

**Light mode gets its own numbers rather than the dark ones reused.** The ink was
pushed 80% toward black, so a mark was both darker AND at the same opacity, and
it sat heavier on a pale ground than the same mark does on a dark one. 62% now,
which holds against the surface without going to soot, and both tiers drop a step:

    dark   0.45 / 0.30
    light  0.30 / 0.20

---

## v0.201.129 — The motifs bleed instead of floating

**Why some looked wrong.** The frame was `54% x 150px`, which on a 393px phone is
a 212x150 landscape box. Every one of the eight SVGs is portrait, between 0.75
and 1.00, so each letterboxed inside it: rendered at 150 tall and about 112 wide,
marooned with 50px of dead space either side. Not squashed, stranded.

They are drawn larger than the frame now and cropped by it, running off two
edges, so a mark reads as a detail of something bigger rather than a small
picture placed in a corner. `preserveAspectRatio` goes from `meet` to `slice` in
`mq2Motif`, because it is an SVG attribute and no CSS rule can reach it.

**Two opacity tiers.** 45% for guitar_gods, beatles, seventies, eighties and
guitar_technique. 30% for bass, keys, vocals and the two theory packs, which
carry far more ink at the same number: the theory marks are solid type rather
than line work, and the other three are heavy filled shapes. The pack now goes on
the root as a class as well as a color variable, since a rule had no way to name
one pack before.

**The 80s grid.** Its horizon is at y=72: every perspective line converges there
and the first horizontal sits at 76.5. The gradient fill started at y=64, eight
units above it, so its top edge floated clear of the grid it belongs to. And the
fill ran to both sides and stopped dead. The whole mark is drawn through a
horizontal mask now, so it fades out at the left and the right instead of ending
on a straight edge.

Both theory packs are single font glyphs rather than SVGs, so the frame moves
them but cannot reshape them. Worth knowing if they still read differently from
the other eight.

---

## v0.201.128 — The review screen was never inside the body

Five attempts at this were all built on a false premise, and the premise was only
visible in a browser:

    mqScreenLanding  <  mqBody  <  mqPanel
    mqScreenQuiz     <  mqBody  <  mqPanel
    mqScreenReview   <  mqPanel              outside
    mqScreenResults  <  mqPanel              outside

`#mqScreenReview` is not a child of `#mqBody`. It sits directly under `#mqPanel`,
alongside the results screen, so it has never had the body's `padding: 6px 16px`
and its back button has always been flush against the edge of the phone. Every
fix aimed at `.mq-body` missed it entirely, including the `height: 100%` theory
and the `mq2-fill` class, neither of which could reach an element that is not in
there.

Reading the markup did not show this: a tag walk through the source counts the
review as one level inside the body, and the browser's parser puts it somewhere
else. The only way to see it was to ask the page.

The review carries its own padding now, matching the body's, and `mq2-fill` is
back to serving only the quiz.

**A headless Chromium is now in the container and `intonare_mq_layout.mjs` uses
it.** It drives the app to the review screen and asserts that the back button,
the list and the cards all start at the same inset, across three phone widths.
Two evenings of this screen were spent reasoning about CSS that was attached to
the wrong element; the probe takes four seconds.

---

## v0.201.127 — Review misses had no box to sit in

The screen carried `height: 100%`. `.mq-body` is declared `height: 0` and takes
its real height from flex, and a percentage height resolves against the DECLARED
value, so 100% computed to zero. The review screen had no box: its children
spilled out of it, and nothing sat where its container said it should. That is
why BACK ended up flush against the edge of the phone while the cards below it
kept their inset.

Filling by flex instead, which is what every other screen does and which cannot
resolve against nothing. That needs `.mq-body` to be a flex column, since it is
`display: block` by default and a flex request to a block parent is ignored
silently, so the review now gets the same `mq2-fill` class the quiz uses. Its
bottom padding comes back, because the quiz cancels that with a negative margin
and the review has nothing to cancel it with.

The header row also pads itself now rather than trusting whatever is above it.

This is the third screen tonight to hit the same wall: `.mq-body` is a block, so
anything inside it asking to fill by flex gets nothing and anything asking by
percentage gets zero.

---

## v0.201.126 — A pinned Music Quiz opened in the tuner's colors

Two separate faults, both on the launcher pin.

**The quiz was the only one of thirty pins that did not set its mode.**

    tool:piano       setMode('tools');    enterTool('piano')
    exercise:scales  setMode('tools');    enterTool('scales')
    tool:musicquiz   mqOpen()

`setMode` is what swaps the palette class, so opening the quiz from a pin left
whatever theme was already on. At cold start that is the tuner, which is why it
came up blue. Every other entry in `FAV_META` had it; this one alone did not.

**And the chip color was hardcoded by type rather than by mode.**

    meta.type === 'TOOL' ? '#5ee2ff' : '#b8a3ff'

So anything labelled TOOL came out tuner blue wherever it actually lived, and the
pin was the wrong color before it was even tapped. It reads the mode out of the
launcher now, which is the same string that picks the theme, so the two can no
longer disagree. The old type test stays as a fallback for an entry with no
`setMode` in it.

With the quiz fixed, all thirty pins now resolve to a mode: 15 tools, 15 practice.

---

## v0.201.125 — A beat after the bar, not the same frame

The drawer went the instant `animationend` fired, so it began on the frame the
bar stopped and the two read as one continuous move. 180ms between them, which is
long enough to register as a pause and short enough not to feel like a wait.

It hangs off the same event, so it is still a beat after the bar has actually
finished rather than a beat after a guess at when it would.

The number to pull if the sequence wants tightening is the 180 in `_once`.

---

## v0.201.124 — Listen for the bar instead of guessing when it ends

The drawer was told to wait by putting a delay in CSS and working out when the
line under the question would finish spreading. Three versions of that were
wrong, in three different ways: the two animations have different lengths
(`mq2RuleSpread` 400ms, `mq2RuleFlicker` 520ms), push mode carried a transition of
its own that overrode the delay entirely, and a number in a stylesheet cannot see
a dropped frame.

The wait is now an `animationend` listener on the bar itself. The browser says
when it has finished and the drawer goes then, so it is right by construction and
stays right if either animation is ever retimed. A 820ms timeout is kept as a
floor, reached only when there was no animation to end, which is what happens
under `prefers-reduced-motion`.

Every CSS delay that existed to pad around the guess has come back out. The
offsets inside the drawer are relative to the drawer moving again, as they were
written to be.

---

## v0.201.123 — Push had its own transition, and no delay on it

The 800ms wait went onto the drawer and not onto push mode, which carries its own
`transition: height .44s` with nothing in front of it. So in push the panel opened
the instant the class landed and climbed straight over the accent bar, which is
what the timing work was meant to stop.

It went unnoticed because push used to be rare. Shortening the cards from 152 to
120 took the grid from 360px to 284px, which moves the switch point down by
76px and makes push the normal case on a large screen:

    viewport 640   cover on every blurb
    viewport 780   push on everything but the longest

Both modes now wait 800ms and move for 520ms on the same curve, and both leave in
240ms with no delay.

---

## v0.201.122 — The drawer waits for the accent bar, which is the slow one

Last version had the drawer wait for the cards. The cards are not the last thing
to finish; the bar under the band is. It starts with the reveal at 260ms and runs
`mq2RuleSpread` for 400ms when you are right or `mq2RuleFlicker` for 520ms when
you are wrong, so it lands at 660 and 780. The drawer set off at 650, straight
over the top of it.

800ms clears the slower of the two with a breath after it, and everything inside
moves back to sit behind the drawer again:

    your card answers        0 - 110ms
    the other three turn     260 - 600ms
    accent bar, right        260 - 660ms
    accent bar, wrong        260 - 780ms
    drawer sets off          800ms
    heading                  1200ms
    blurb                    1290ms
    drawer lands             1320ms
    multiplier               1420ms
    streak                   1540ms
    NEXT                     1620ms

The number to pull if the whole thing runs long is the 800ms delay on
`.mq2-fbwrap`; everything after it is offset from that.

---

## v0.201.121 — One voice asking, four answering, and a sequence that queues

**The answers take the question's face.** A serif stem sitting over four
monospace tiles read as two screens stapled together. The mono is the app's data
face, right for a fretboard readout and wrong for four sentences you are choosing
between. Same family now, with `mq2FitOpts` still setting the size.

**The drawer waits for the reveal.** It was told to move at 300ms while the other
three cards were still turning, so it climbed over an animation in progress. It
now carries a 650ms delay of its own, which is the moment the reveal finishes:
110ms for the card under your thumb, 260 plus 340 for the rest.

**And it arrives slower.** 520ms on Material's emphasized-decelerate curve,
`cubic-bezier(.2, 0, 0, 1)`, which is what large surfaces coming on screen use:
it leaves fast and lands slowly. The old 440ms on a general-purpose ease is a
small-control speed, and a sheet crossing most of the screen at that pace reads
as snapped into place rather than placed.

Out is 240ms on an accelerate curve with no delay at all. Leaving is not an event,
and roughly half the entry duration is the usual ratio.

**Everything inside the drawer was written for a drawer that arrived at 300ms**,
so the heading, blurb, multiplier and streak all played out while it was still
travelling and the sheet turned up already full. They are offset from the moment
it lands now:

    you touch a card         0
    your card answers        0 - 110ms
    the other three turn     260 - 600ms
    drawer sets off          650ms
    heading                  1050ms
    blurb                    1150ms
    drawer lands             1170ms
    multiplier               1300ms
    streak                   1420ms
    NEXT                     1500ms

NEXT is last on purpose. A button that appears with the text invites a tap before
the blurb has been read.

---

## v0.201.120 — The answers get measured, and the blurb stops rubber-banding

**Answer text is fitted, not guessed.** The old s0..s4 buckets set the size from
the longest option alone, so a card holding "They were cousins" was set for "They
had played in an earlier band together" sitting beside it, and on a 120px tile
that left most cards two thirds empty. `mq2FitOpts` walks 18px down to 11px and
stops at the largest size every tile in the row will carry. All four stay the
same size, because a row where one card is 17px and its neighbour is 12px reads
as a fault rather than a fit.

**Scrolling only when the panel had to clamp.** `.mq2-fb` carried
`overflow-y: auto` at all times, so every blurb rubber-banded under the thumb
whether there was anything below or not, which reads as hidden content when there
is none. It is switched on only when the measured height hit the 92% ceiling,
which on the numbers should be almost never.

---

## v0.201.119 — The blurbs stop scrolling, and the verdict line earns its place

**The scrolling, finally.** The verdict line is `display: none` until `.go` is
added, and `mq2PanelFit` runs before that. So it contributed nothing to the
measurement, then appeared and pushed roughly 40px of text out the bottom of
every panel. It is forced visible for the measurement now and put back after.

**The verdict line only shows when a card is actually hidden.** Daniele's call,
and it is right: restating the answer while the answer is sitting in plain view
above the drawer is noise. The two cards that matter are compared against where
the top of the drawer will land, and if both clear it the line is dropped and its
height comes back off the panel.

**Shorter answers.** 152px was a true square and too tall: most answers are two
or three words, so the card was mostly empty and it pushed the panel down onto
the ones below. 120px is 4:5, still a card rather than a list row, and hands the
panel 64px it did not have. Diagram questions go 112 to 96.

**A bigger font step for short answers.** A card holding "Treble" was set at the
same size as one holding "Rage Against the Machine". Options of ten characters or
less now take 17px, which is 12% of every question in the app.

---

## v0.201.118 — Measuring the box instead of the text, and answers in the wrong half

Two faults from the last build, both visible on device.

**Every blurb was scrolling.** `mq2PanelFit` read `wrap.scrollHeight`, but
`.mq2-fb` is `overflow-y: auto`, so its scrolled content does not count towards
its parent's scrollHeight. The measurement returned the height of the clipped
box, came back short on every single blurb, and the panel opened too small.
`max-height` was still applied during the measurement too, capping it before it
was taken. The measurement now lifts both, reads the height, and puts them back.

**The answers were centred in the stage**, so they sat in the middle of it with
the drawer rising into them from below. The drawer covered the answers and left
the empty half untouched. They sit up under the band now, where the drawer
reaches them last.

The verdict line has moved out of `.mq2-fb` and become its own row in the drawer.
Inside the scrolling part it scrolled away with the blurb and came out sliced in
half across the top.

---

## v0.201.117 — The panel takes what the blurb needs, and the answers never move

The feedback panel measures itself and then decides where to sit. If it fits
under the answers at their full size it takes its own row and covers nothing. If
it does not, it becomes a drawer and carries a line naming what you picked and
what was right, so nothing behind it is lost:

    ✕ Joey Ramone  /  ✓ Johnny Ramone

**The answers never resize either way**, which is the point. Earlier drafts had
the cards giving ground to make room; the numbers say that cannot work on a
phone. Measured over all 1,390 blurbs: median 210 characters, 90th percentile
256, longest 434. For a median blurb to sit under the grid with nothing moving on
a 640px screen, the cards would have to rest at 88px, which is the 1.75:1 slab
the square grid replaced. Square answers do not come back until about 780px.

So on a phone it is nearly always the drawer, and push is what happens on a
tablet or in landscape, where there is genuinely room.

**Nothing scrolls.** Height is measured off-screen at the real width rather than
estimated from a line count, because the blurbs run from 60 characters to 434 and
an estimate is wrong often enough to matter. The longest blurb in the app takes
79% of the stage on a 640px phone and still leaves the top of the grid showing,
so the 92% clamp should never be reached.

`push` is cleared in `mq2FbClose`, since it is decided per question: left on, a
short blurb followed by a long one would open at a height meant for the other.

---

## v0.201.116 — The fill class was set before the class it tested for

v0.201.115 had the right rule and put the switch for it in the wrong place. It
set `mq2-fill` in `mqShowScreen`, guarded by whether the quiz screen carried
`.v2`. But `.v2` is added inside `mq2RenderQ`, which runs afterwards, so the test
was false every time and the rule never applied to anything.

The class is now added beside `.v2` in `mq2RenderQ`, which is the first moment
the screen is actually in v2. `mqShowScreen` only removes it, on the way to any
other screen.

Three versions on one ledge, and the useful part is what each was wrong about:
0.201.114 blamed padding that was not the cause; 0.201.115 found the cause and
wired the switch to a class that did not exist yet.

---

## v0.201.115 — The ledge, found properly this time

Last version blamed 24px of padding on `.mq-body` and cancelled it. The ledge
stayed, because that was not what it was.

`#mqScreenQuiz` is a direct child of `#mqBody`, and **`.mq-body` is
`display: block`**. So `flex: 1 1 auto` on the quiz screen has been doing nothing
whatsoever: the screen is only ever as tall as its contents, which is 196 for the
band plus 348 for the answers. Everything below that is leftover body, which is
the ledge, and it is far more than 24px, which is why cancelling the padding did
not move it.

`#mqBody` becomes a flex column while the quiz is up, so the chain flexes the
whole way down and the stage reaches the bottom of the screen. Driven by a class
set in `mqShowScreen` rather than by `:has()`, which would fail silently on an
older WebView and look like the fix simply had not worked again.

---

## v0.201.114 — The lip under the drawer

`.mq-body` carries 24px of bottom padding and `.mq2` cancelled only the top and
the sides, so the quiz has always sat on a 24px strip of background. That was
invisible for as long as the answers ended well short of the bottom. The drawer
is pinned to the bottom of the stage, so it stopped 24px above the screen edge
and looked like it was rising out of a ledge rather than off the bottom.

Bottom margin now cancels it too.

---

## v0.201.113 — NEXT was scrolling away with the blurb

The drawer carried `overflow-y: auto` on the whole element, so when a blurb ran
long everything inside scrolled, including the button that had just been moved in
there. NEXT ended up half below the drawer's own rounded bottom edge, which is
the notch that showed up on device.

The drawer is a flex column now. `.mq2-fb` scrolls and nothing else does, and
`.mq2-foot` is `flex-shrink: 0` so the button holds the bottom whatever the blurb
is doing. Max height went 62% to 74%, since the button now takes a fixed share of
it.

---

## v0.201.112 — The answers came back

`.mq2-grid` was carrying `position: absolute; inset: 0`, lifted straight out of
the mockup where the grid is a direct child of the stage. In the app it sits
inside `.mq2-scroll`, and out of flow in there nothing sizes it, so every answer
disappeared. The band was fine, both locked heights were fine; there was simply
nothing under them.

The grid is in normal flow again and `.mq2-scroll` centers it with
justify-content, which is what the absolute positioning was doing badly.

Worth writing down, since it is the third time tonight the same shape of mistake
has landed on a device: a rule that is correct in a standalone mockup is not
correct in the app, because the mockup's DOM is two levels shallower. Copying
geometry across needs the parent chain checked, not just the rule.

---

## v0.201.111 — The quiz question screen, rebuilt

Worked out against a mockup rather than by shipping guesses at the phone, after
two builds that were wrong on device.

**Two locked band heights, not a range.** The diagrams draw at a fixed 118px and
cannot shrink and stay readable, so one height cannot serve both kinds: at 250px
a question carrying a diagram would have 20px left for its text. A question
without one takes 196px and square answers. A question with one takes 290px and
4:3 answers, which comes to 558 on a 620px screen. Nothing moves within either
kind, and four of the eight packs never show a diagram at all.

`mq2FitStem` now measures the stem against its own box rather than the whole
band, so it fits whatever the diagram leaves.

**Square answers on the 8-point grid.** The tiles were about 1.9:1, which reads
as a list row rather than a card. They are 1:1 now, 154 x 152, in a grid with
16px padding and 12px gaps, centred in what is left. Research on card sets is
consistent on this: one ratio across a collection, and a standard one.

**Lit means brighter.** The old states washed the tile in green or red, and a
colour wash over a pale card darkens it, so on the light themes the card meant to
stand out came back duller than the three fading behind it. The live cards now
take the lightest surface in the set and carry their colour in the border, the
text and a lift. The two you did not touch drop to 26% at once.

**Selection lands on the frame you touch.** Three things were stacked against it.
It listened for `click`, which waits for the finger to lift and for the browser
to rule out a scroll. There was no `touch-action`, so the browser held every
touch back while it decided. And `mq2Reveal` held EVERY tile behind a 260ms
timeout, including the one under the thumb. It is `pointerdown` now, the tile
answers in 110ms, and only the other three keep the staged timing.

NEXT moved inside the drawer. It was a separate slab below it, which is why it
looked like it was cutting the blurb off.

---

## v0.201.110 — The drawer was sitting in plain sight before it opened

Two faults on device from the last build, and one cause behind both.

`.mq-screen` is a flex child of `#mqPanel` with no flex-grow, so the quiz screen
has always sized to its content rather than to the modal. That never showed
while the feedback panel lived inside the scroll box at max-height 0, because a
zero-height thing is invisible wherever it sits. An absolutely positioned drawer
needs a stage with a real height to sit against, and it did not have one.

So the closed drawer, pushed down by translateY(101%), simply hung below the
stage in the open, an empty white box between the answers and the bottom of the
screen. And once opened it ran past the stage and under the NEXT button, which
clipped the blurb mid-sentence.

Two lines. `.mq2-stage` gets `overflow: hidden`, which is what keeps a closed
drawer out of sight. `#mqScreenQuiz.v2` gets `flex: 1 1 auto` so the screen fills
the panel it is in and the stage has a height worth 62% of.

---

## v0.201.109 — The quiz band stops moving, and the blurb comes up as a drawer

Four of Daniele's notes were one fault: the band holding the question grew with
the question, so a long stem pushed everything down and took NEXT off the screen,
and the blurb sat below the answers where the code scrolled you to reach it. The
last line of `mq2Feedback` literally called `scrollTo(scrollHeight)`.

**The band now has a range rather than a height.** A single number cannot serve
both, and the measurements say why: 1,390 written stems, median 66 characters and
longest 150, plus 18,000 generated ones at median 44, and half of those carry a
staff or a fretboard underneath. So min-height 178px stops a short question
hugging the top, max-height 46vh stops a long one reaching NEXT, and `mq2FitStem`
shrinks the type between the two. Floor 15px, and it measures scrollHeight against
clientHeight rather than guessing at line counts, the same way `_fitHeaderTitle`
already does.

**The blurb is a drawer over the answers.** It was moved out of the scrolling box
into a new non-scrolling `.mq2-stage`, because an absolutely positioned drawer
inside a scroller scrolls away with the content, which is the bug in the first
place. Capped at 62% of the stage so the top of the grid stays visible behind it,
which is the reason Daniele picked this over the blurb replacing the answers: you
can see what you chose next to what was right while you read why.

NEXT was already dimmed until you answer. That one needed nothing.

**Dynamics in the Survival Guide.** The ladder was lopsided rather than subtle:

    pp -> p    +7.0 dB        mf -> f    +4.6 dB
    p  -> mf  +14.2 dB        f  -> ff   +1.4 dB

Forte to fortissimo was 1.4 dB, which nobody can hear, while piano to mezzo forte
was a 14 dB cliff. Every step is 4.0 dB now, from .038 to .95 across eight marks.
Two of those marks did not exist: pianississimo and fortississimo were among the
silent terms. Mezzo forte and mezzo piano were never missing at all, the table
spelled them with a hyphen and the markup with a space.

Twelve terms are still genuinely silent: arpeggio, augmentation dot, breath mark,
caesura, mordent, niente, slur, staccatissimo, tie, trill, turn, una corda.

---

## v0.201.108 — Two questions in Fundamentals were handing over the answers to two others

Question 31 asks what singers could do with **Guido's** staff. Question 60 then
asked which 11th-century Italian monk gave the notes their syllables. His name
was in the earlier stem, so the later question was free. Taking the name out of
31 removes the context that makes it a question at all, so 60 changed instead and
now asks where the syllables came from:

    Where did Guido of Arezzo get the syllables ut, re and mi from?
    -> The first syllable of each line of a hymn

Every line of Ut queant laxis starts one step higher than the last, which is the
whole trick and a better fact than the one it replaces. Bilingual, and the option
lengths are balanced so the answer is not the longest on the card.

Question 28's blurb ended "Beethoven's own marks are famously brisk", and
question 33 asks which composer first wrote metronome marks into his symphonies.
Rewritten to say why a number outlived the argument about it instead.

Omega leaks in this pack went from six to one, and the one left is unavoidable:
question 59's answer is "B flat, A, C, B natural", so its blurb has to name B
natural, which is question 32's answer.

Left alone deliberately, and worth recording as a decision rather than an
oversight: six blurbs say "X is Italian for Y", and question 27 asks which
language the markings are in. That is the pack teaching a thing six times and
then testing it. Stripping the word out of six blurbs would gut all six.

---

## v0.201.107 — Crotchets and quavers in an English question

Theory Fundamentals question 43 asked what a C with a line through it means and
offered "Two minim beats in a bar", "Six quaver beats in a bar" and "Four
crotchet beats in a bar". Those are the note names that genuinely are British
rather than a spelling difference, sitting in the English options of a shipping
pack. Now half-note, eighth-note and quarter-note, blurb to match.

Twelve places said "on the stave", "in the stave", "under the stave" or "off the
stave". American says staff. The plural staves is correct in both and is left
alone, as in "middle C sits between the two staves".

Nothing else in the app: minim was almost always "minimum", breve is Italian for
short, and the semibreves are in the Survival Guide glossary as the Italian name
for a whole note, which is right.

Reading rows 31 to 60 of Fundamentals turned up two things for Daniele rather
than for the gate. Question 31 names Guido in its stem, which hands over question
60, "which 11th-century Italian monk". And questions 20, 46 and 47 rotate one set
of options between them: how many beats in a bar, which note value gets the beat,
how fast the beats go. Each is the answer to one and a distractor in the other two.

---

## v0.201.106 — British idiom, which the spelling audit could never see

Spelling was half the job. These read as British but are spelled correctly in
both dialects, so no spelling rule could ever have caught them. Six were sitting
in the app after the audit reported it clean, three of those in shipping packs:

    guitar_gods       the flames "put him in hospital"       -> in the hospital
    bass              "nobody had got out of a bass before"  -> had gotten
    bass              "the band have spent twenty years"     -> the band has
    survival guide    "a full stop in the sound"             -> a complete stop
    survival guide    "the trickiest of the lot"             -> of them
    cadence blurb     "a comma rather than a full stop"      -> and not a period

The audit now carries an idiom list and a grammar rule. The grammar one is that
a collective noun takes a singular verb in American English: the band has, not
the band have.

Both are written to leave real English alone. "Two couples inside the band were
splitting up" is correctly plural, because the subject is the couples. "The 2nd
of natural minor" is a scale degree and not a date. "Its own spot on the neck"
is not the idiom. Each of those fired once and each is now excluded by name.

Nothing else outstanding: spelling 0, mangled words 0, names under two spellings
0, idioms 0, collective-plural 0.

---

## v0.201.105 — American English, and the sweep that had already gone wrong once

180 British spellings replaced across the whole file, copy, code and comments.
The audit now reports zero.

**The reason this needed doing twice is the interesting part.** A rule in
`intonare_us_spelling_audit.py` read `specialis(e|es|ed|ing|t|ts)`. The `t` and
`ts` are the fault: "specialist" and "specialists" are correct American English,
and rewriting them produces "specializt". That same shape of rule is how
"organist" became **organizt** and "programmer" became **programr**, and four of
those had shipped and were sitting in the file at the start of this session.
Repaired: three organists, one programmer, one organistica in the Italian
Survival Guide, and an optimiztic interval description. "Baduizm" is left alone
because Erykah Badu spells it that way.

**A live break was caught during the sweep and is worth recording.** A rename
protected `createAnalyser`, which is a Web Audio API name, by ignoring anything
within 45 characters of it. That left `analyser` on two lines while renaming it
to `analyzer` in 46 others, so the tuner's microphone setup read

    analyser.fftSize = 4096; analyzer.smoothingTimeConstant = 0;

with the second name undefined. `node --check` passed it, because an undefined
variable is a runtime fault and not a syntax one. The mic would have failed on
every launch.

**The audit now watches for its own wreckage,** which is the only durable fix:

- **mangled words** — anything ending -izt, -izm or -iztic, which real English
  does not do. Baduizm is on an allow list.
- **names living under two spellings at once** — a token present as both
  `analyser` and `analyzer` means one of them is unreachable. This is the check
  that would have caught the mic break in seconds.

Proper nouns are protected by name rather than by luck: Daft Punk, Licence to
Kill, Hapshash and the Coloured Coat, createAnalyser, userCancelled.

Two other fixes in shipping packs, found before any of this: guitar_gods ended a
B.B. King blurb on "anything that daft again", and eighties offered "a
synthesised marimba". The -ise list had no rule for synthesise, in a music app.

---

## v0.201.104 — The last three tables, and rarity

Exotic scales 4 to 9, jazz scales 5 to 9, chord-scale pairs 4 to 9.

    exotic       Phrygian dominant, octatonic, Hungarian minor, augmented, in-sen
    jazz         bebop dominant, half-whole diminished, Lydian augmented, Dorian \u266d2
    chord-scale  maj7/Ionian, m7/Dorian, dim7/whole-half, m(maj7)/melodic minor,
                 maj7\u266f11/Lydian

    exotic       48 \u2192 108 cards      jazz  60 \u2192 108      chord-scale  48 \u2192 108

**Rarity.** Items carry a weight, and the picker respects it, so the Hungarian
minor and in-sen sit in the deck at roughly half the frequency of the common
scales rather than taking an equal share. Measured across 12,000 picks the four
rare exotic scales come out at 6\u20139% each against 14\u201315% for the others. Without
this the choice was between leaving them out and letting them crowd the pack, and
a set that only holds the common scales is not an advanced set.

**One generator was fighting its own ratings.** `mqGenExotic` refused any request
below tier 2 and then wrote `d: 3` onto whatever it built, so a major pentatonic
came out rated as hard as the altered scale. The tier is on the scale now.

Round quality, measured over 1,200 rounds at each stage of this work:

    repeat a blurb      EASY 29% \u2192 24% \u2192 10% \u2192 6% \u2192 1%
                        MED  30% \u2192 31% \u2192  0% \u2192 0% \u2192 0%
                        HARD 41% \u2192 44% \u2192  0% \u2192 0% \u2192 0%
    come up short       0% throughout
    repeated ANSWER     4\u20136%, unchanged and still open

A hard round now reads: bebop dominant, a perfect eleventh, the mediant in a hard
key, in-sen, 12/8, a secondary dominant, the tritone substitution for F\u266f7, the
raised seventh of D\u266f minor spelled C\u266f\u266f, a major seventh, and which scale fits
D\u266d7\u266f11.

Bass, Guitar Technique and Theory Fundamentals still fill 10 of 10 in every tier.

Still open, unchanged from the last entry: about one round in twenty has two
questions with the same answer, usually a scale name reached from two directions.
The batcher deduplicates cards, not answers.

---

## v0.201.103 — Meters and progressions reach their real ceiling

Two of the thin tables filled out. Both were short of what exists rather than
short by design.

**Time signatures, 9 to 14.** Added 2/2, 6/4, 3/2, 7/4 and 5/8. Every one fills a
bar on the first try, so nothing was added that the note-value pool cannot write.
660 cards to 1,784.

6/4 mattered beyond its own card. Meters that hold the same amount of music are
twins: they can never be offered against each other, and the blurb names the twin
to turn that constraint into the lesson. 12/8 had no twin in the table, so on
that card the sentence silently vanished. Three meters now hold six quarter
notes, so the blurb names all of them and agrees its verb in both languages
rather than naming the first and stopping.

**Progressions, 4 to 10.** Added I–V–vi–IV, the doo-wop I–vi–IV–V, I–V–IV, the
royal road IV–V–iii–vi, iii–vi–ii–V and the jazz turnaround vi–ii–V–I. 28 cards
to 70, and the first three are rated level 1, which is where a pop loop belongs.

Two of the new blurbs were written badly and caught before they shipped. One
opened "the same four chords as the one above," which is meaningless in a round
that shuffles. The other named I–vi–ii–V, which is the answer to a different
card in the same pack. Both rewritten.

Round quality after both:

    rounds that repeat a blurb    EASY 10% → 6%    MED 0%    HARD 0%
    rounds that come up short     0%

Bass, Guitar Technique and Theory Fundamentals still fill 10 of 10 in every tier.

Still short of their ceiling and not yet touched: exotic scales at four, jazz
scales at five, and chord-scale pairs at four.

---

## v0.201.102 — Advanced Theory rates the card, not the generator

Difficulty came from which list a generator sat on. Core meant easy, upper meant
medium, jazz meant hard. So hard held exactly four kinds and every hard round was
about 70% jazz, while a plain ii–V–I counted as hard because it is jazz and a
German augmented sixth counted as medium because it is not.

Measuring the generators showed five of them carried no difficulty at all. Jazz
scales, jazz chords, tritone subs and chord-scale pairs every one reported tier 1
whatever they built; the pack simply stamped the slot number on afterwards. Two
more were rated wrong outright: the exotic generator called major and minor
pentatonic hard, and the inversion generator called a plain major triad hard.

`mqCardLevel` now reads what was actually built and returns 1, 2 or 3. The table
is small and it is the whole argument:

    inversions   triads 1, sevenths 2
    exotic       pentatonics 1, blues and whole tone 2
    chromatic    secondary dominants and Neapolitan 2, the augmented sixths 3
    jazz scales  melodic minor and lydian dominant 2, altered and harmonic major 3
    jazz chords  13 and 7♭9 2, 7♯9 and 7♯11 3
    chord-scale  Mixolydian over a dominant 2, the rest 3
    progressions I–IV–V and vi–IV–I–V 1, the two-fives 2
    tritone sub  3, in all twelve keys

Anything not listed keeps the level its generator gave it, so the kinds that
already tier themselves properly are untouched. Advanced Theory now puts every
generator in the pot for every slot and keeps whatever matches the slot's level.

Three kinds sat on two family lists at once and therefore got two chances at
every slot, which was the other half of why Inversion was dealt half again as
often as anything beside it. The combined list drops the duplicates.

Measured over 1,200 rounds, before and after:

    rounds that repeat a blurb     EASY 24% → 10%   MED 31% → 0%   HARD 44% → 0%
    kinds available in a hard round               4 → 20
    rounds that come up short                     0% → 0%

Theory Fundamentals, Bass and Guitar Technique are unaffected: they keep their
own profiles and still fill 10 of 10 in every tier.

One thing this did not fix, left as a note rather than a change. Roughly one
round in ten still has two questions with the same answer, usually a scale name
reached from two directions: what scale is this, and which scale fits this chord.
The batcher deduplicates cards, not answers.

---

## v0.201.101 — One of Advanced Theory's twelve generators had never run

`mqGenEnharmonic` opened with `if (d !== 2) return null`. Advanced Theory asks
every generator for its hardest output, always tier 3, so the answer was always
no. Measured over 9,000 generated questions the kind appeared exactly zero times
in that pack, in any tier. It has presumably never run there.

It was also the thinnest well in the app at ten cards, and both faults were the
same fault: the table only held the five black-key pairs.

The table now holds nine and each side carries its own spelling rather than a
midi number, because midi cannot express an F flat. The pitch is E, and deriving
the notehead from the pitch puts it on the E line where a flat sign reads as E
flat. The staff renderer already accepted `{ l, o, a }` for exactly this reason
and nothing was using it.

    B♯ / C     the seventh of C♯ major
    E♯ / F     the seventh of F♯ major
    C♭ / B     the fourth of G♭ major
    F♭ / E     the fourth of C♭ major

Those four are flagged advanced, and they say something better than the shared
line about pianos and paper: the key that forces the spelling, which is the only
reason the note exists. Theory Fundamentals question 15 already told the player
that C flat is B and F flat is E, and until now the generator could not ask it.

18 cards, up from 10. Easy rounds now repeat a blurb 24% of the time rather than
29%.

Fixing the tier exposed the seam it was hiding. With the white pairs marked
advanced, the easy slot rejected them, the medium slot had no Enharmonic in its
list, and the kind was locked out of every slot again. It is now on the medium
list as well as the core one. That is a patch, not a fix: a kind whose easy half
and hard half belong in different slots cannot be described by one family list,
which is the argument for rating items rather than lists.

`mqEnhIt` is gone, replaced by `mqEnhName`. The old one appended " bemolle" to
anything without a sharp sign, so a natural C would have come out as Do bemolle.
Nothing had ever passed it a natural before.

---

## v0.201.100 — The dormant piano grids are closed out

The pending cleanup was to strip dead `rh`, `lh` and `ctls` arrays from the seven
piano songs that were converted to real performance captures, about 157KB. Almost
all of it was already gone. What was actually left was four dead `tempoMap`
arrays, and Clair de Lune held nearly all of it at 4.8KB.

A tempoMap is a rubato curve for converting beats to milliseconds. A performance
capture carries absolute ms on every note and needs no such curve, and the
scheduler takes the perf branch and returns before it ever reads one. So this was
a map nothing could consult, sitting beside 1,491 notes that already knew when
they happened.

Removed from clair_de_lune, liebestraum and moonlight_3. Verified by extracting
`__riffsBuild()` into node and loading it: 42 piano songs, 21 with performance
data, all seven of the converted set intact with their pedal data, and no perf
song anywhere still carrying rh, lh or tempoMap.

    liebestraum     1888 notes, 220 pedal      moonlight_3    6538 notes, 721 pedal
    clair_de_lune   1491 notes, 327 pedal      prelude_em      604 notes, 133 pedal
    moonlight       1144 notes, 308 pedal      fuer_elise     1041 notes, 150 pedal
    prelude_c       1284 notes,  70 pedal

Fourteen perf songs still carry a single 57-byte `ctls` entry that opens the lid
and clears the pedal at beat zero. That is 800 bytes and it stays: it is the
template every new perf song is written from, and removing it buys nothing worth
the edit.

Also in the 80s pack tooling, not the app. The duplicate-answer rule had no way
to express a legitimate exception, so it failed on "Thriller" being both the
album that outsold everything and the video John Landis directed. Two subjects,
one word. That now lives in allow_answers_eighties.json and prints as a note with
the reason instead of failing. Separately, the Italian check was reading the
"the" in "Welcome to the Jungle" as English leaking into Italian prose; it now
drops any run of three or more words that appears verbatim in both twins before
scanning. Beatles, Guitar Technique, Bass, Seventies and Guitar Gods all still
come back clean, so nothing was loosened. The 80s pack now passes every automated
stage.

---

## v0.201.99 — Light bar tracks come back from the dead

`--panel` moves up in all five light themes. That is the whole change.

    base    #f3f3f9 -> #fdfdfe        tools   #e4faf2 -> #f9fefc
    tuner   #ecf4ff -> #fbfdff        train   #f5f1ff -> #fdfcff
    metro   #faf3e0 -> #fefdf9

A bar track is `--surface-2` and the panel under it is `--panel`, and in light
mode those were set to the same hex in every theme. Four tracks have no border to
save them, so an empty one was not visible at all until it started to fill: the
quiz progress bar, the survival timer, the by-pack stats bars, and the Pitch
Match track. Dark mode separates the two by 2.1 L*. Light now runs 3.3, because a
recess hides more easily on a white ground than on a black one.

This replaces the palette pass proposed in v0.201.98, and it is worth writing
down why. The measurement that pass was built on was correct and pointed at the
wrong thing. Light does have a 20-point jump between `--bg-1` and `--surface`,
but that pair is a sheet and the tiles sitting on it, and they are meant to be
far apart. Redistributing the ramp to close that gap would have dropped
`--surface` by 7 L*, and the quiz band is `--surface`: all nineteen pack ink
colours are hand-tuned to land between 4.75 and 4.98 on it, so every one of them
would have fallen to about 4.0. Eleven more hardcoded colours across the tuner,
metronome and drum kit were in the same position.

The real fault was the step that measured zero, not the one that measured twenty.
It is one token per theme and it costs nothing else: background, card and track
all keep the values they ship with, so no ink moves and no label changes.

Border contrast on the new panel goes up rather than down, from about 3.3 to
about 3.6 in every theme. Text is unaffected at 15.8.

Pinned in the sentinel, one check per theme, phrased as the collision rather than
the value: the four themes that declare the pair on one line pin that line out
by absence, and base light pins the panel by value.

---

## v0.201.98 — The old quiz is cut out, and a hidden gesture goes with it

The v1 quiz has been dead code since the redesign shipped. It is now gone: 212
lines of JavaScript, 83 lines of CSS, the feedback sheet markup, and the two
entries that kept it in the quiz back stack.

The reason to do it now was not tidiness. `_bindQuizV2Hold` bound a one-second
press on the Settings version stamp to `setQuizV2`, with no developer gate and
nothing telling the user it was there. It reloaded the app and changed nothing,
because turning the flag off called `removeItem` while the reader on the next
boot looked for the string `'0'`. A user could hit it by accident and get an
unexplained reload. Both faults left with the flag, and `MQ_V2` no longer exists.

Removing the markup left `mqHideFeedbackSheet` reaching for an element that was
no longer there, on every question. That would have thrown on the first answer.
It was caught by a new whole-file sweep for unguarded `getElementById(...)`
calls on ids that appear nowhere in the markup. The same sweep found a second
one: `rrBuildDiffGrid` and `rrTogglePopup('diff')` still pointed at `rrDiffGrid`
and `rrDiffPopup`, left behind when the Rhythm Reading picker was renamed to
`rrDiffPicker`. Nothing called them, so nothing broke, but they are gone too.

The sentinel gained an `absent` kind. It could only pin that something is
present, which meant a deletion could be silently undone by a revert. Five
deletions are pinned with it now.

Two light pins were stale for a real reason, not a wrong one: the palette moved
deliberately over the last several versions and nobody updated them. The accent
pin now matches what ships. The lifted-accent pin was an exact hex on one theme,
so any hue change fired it; it now checks the token exists in all four themes
that carry it, which is what the description meant in the first place.

One error in the 80s pack: blurb 57 opened on "He" instead of naming George
Michael. The other one is left alone. Rows 22 and 64 both answer Thriller, and
fixing that means rewriting a question, which is not a gate's decision to make.

Not shipped, sitting alongside as a preview file: three candidate light surface
ramps. Every light theme has `--surface-2` and `--panel` set to the identical
hex, so the fifth surface does not exist and a panel inside a card has nothing
to sit on. Measured in L*, all five themes run the same shape:

    DARK    steps  2.7 · 3.5 · 3.7 · 2.1
    LIGHT   steps  2.1 · 20.1 · 3.3 · 0.0

The candidates hold each theme's own hue and saturation and move lightness
only, which is what the last attempt got wrong. Worst-case text contrast goes
up rather than down, from 4.61 today to 4.93 on all three.

---

## v0.201.97 — The surface redistribution is reverted

The even-step surfaces from the last two versions are removed. Spacing them
evenly was the right diagnosis and the wrong execution: the steps were derived
from `--bg-0` and `--bg-1`, which are blue-based, so evening them out amplified
the blue and pushed the whole quiz off the app's violet scheme. It fixed the
flatness by breaking the identity, which is a worse trade.

The measurement still stands and is worth keeping for whoever picks this up:

    DARK    surfaces span .013   steps .004, .005, .004
    LIGHT   surfaces span .485   steps .032, .376, .078

Light has one long jump and two crowded pairs, and that is why the picker tiles,
the pack popup and the sheets all read flat. The fix is to redistribute those
four values while holding the violet hue the app actually uses, rather than the
hue the current tokens happen to carry. That is a palette pass with a before and
after across the tools, not a scoped override.

---

## v0.201.96 — The four sheets outside the modal get the same surfaces

`#mqQuickSheet`, `#mqSurvivalSheet`, `#mqStatsSheet` and `#mqPackPopup` are
siblings of the quiz modal rather than children, so the previous version left
them on the old light surfaces while everything inside the modal moved. All five
now carry the scope. Verified: the five report the new surface, the body still
reports the old one, and a tool screen outside the quiz is untouched.

---

## v0.201.95 — Light mode gets its steps back, inside the quiz

Light had its four surfaces at luminance .413, .444, .820 and .898: one long jump
and two crowded pairs. Three of them sat near white with nothing in between, so
anything built from two of those three came out flat and bright. That is the
picker tiles, the pack popup and the sheets, all showing the same gap from
different angles.

Dark reads as layered because its four steps are even, at about .004 each. The
quiz surfaces are evenly spaced now at about .16 a step, hue and saturation
untouched:

    --bg-0      #8eaedc   .412
    --bg-1      #b3caea   .578
    --surface   #cce1ff   .739
    --surface-2 #ebf3ff   .890

The sheets and the popup are siblings of the modal rather than children, so
scoping to `#mqModal` alone left four surfaces on the old values: both pickers,
the stats sheet and the pack popup. All five carry the scope now.

**Scoped to the quiz on purpose.** The same redistribution belongs app-wide, and
it should be its own pass with a before and after across the tools. Confined here,
nothing outside the quiz can move: the body still reports the old surface and
only the modal reports the new one.

The pack popup was the clearest case. It is a real sheet, so being lighter than
its ground is right, but both colours in its gradient were from the crowded three
and it landed at the very top of the range. It has somewhere to sit now.

---

## v0.201.94 — The packs keep their colour in light mode

The previous pass lifted the light inks by blending each one toward its
dark-mode colour. Blending toward another colour pulls saturation out, so every
pack came back a muted version of itself and the identities went with it: the 80s
and the 70s were both a brownish red, the two theory packs were the same violet.

They are built from the dark colour now by keeping its hue and its saturation and
lowering only the lightness, with a little extra chroma to survive the darkening.
The 80s reads as the same pink in both themes, the 70s the same orange, the
Beatles the same blue.

Saturation across the nineteen packs went up rather than down: the 80s from 0.61
to 1.00, the Beatles 0.63 to 0.89, Theory Fundamentals 0.43 to 0.92, vocals 0.54
to 0.98. All of them sit between 4.6 and 4.9 against the light surface, so the
contrast that pass was aiming at is still there. It was the method that was
wrong, not the target.

---

## v0.201.93 — Hover cannot stick to a finger any more

A mouse leaves a button; a finger does not. Android applies `:hover` when you tap
and holds it until you tap something else, so the last thing touched keeps its
hover appearance for as long as you look at the screen. That is what the stray
box on the DECADES tab was, and the file had 241 hover selectors of which 195
changed something visible and 2 were guarded.

All 235 remaining rules are wrapped in `@media (hover: hover) and (pointer: fine)`.
Both conditions matter: the first asks whether the device can hover at all, the
second whether the pointer is precise. A phone fails both, so the rules never
apply and nothing is left behind.

Verified from both sides: a mouse context matches the query and a touch context
does not, no hover selector is left unguarded, all four style blocks still close
evenly, and 7060 rules load with no console errors. The sentinel holds at 123
fixes and 250 pins.

Nothing changes on a desktop. On a phone a whole class of leftover marks stops
happening, including ones nobody had reported yet.

---

## v0.201.92 — The picker tiles carry their pack colour

Custom tinted a tile with its pack colour and the two sheets did not, so the same
pack looked like three different things depending on which picker you opened.
Quick Play was the worst case because it never selects anything, so nothing ever
triggered the colour at all.

A ready pack now carries its colour in all three: the border mixed 55 percent
toward the pack and the fill at 5 percent. Survival keeps its stronger selected
state on top of that, so a chosen pack still reads as chosen rather than merely
present. Packs that are not ready stay grey, which is the one case where the
absence of colour is the message.

---

## v0.201.91 — A gradient nobody could see, and hover stuck on a touch screen

**Three attempts at the picker background failed because a rule further down was
winning and I never looked for it.** `body.light .mq-sheet` paints a near-white
gradient with `!important`, so Quick Play and Survival ignored every value I set
while Custom, which is a screen rather than a sheet, was unaffected. That is the
whole difference between them.

The two full-screen pickers now paint `--bg-0`, which is what Custom's panel
actually shows. Verified in both themes: sheet and panel report the same colour.

`--panel` is worth recording as a trap. It reads like the panel's colour and it
is a near-white surface token; the element paints `--bg-0`. Pointing the sheets
at it last version made them lighter rather than matching.

**And the stray box on a tab was `:hover`.** A touch screen leaves it applied to
whatever was last tapped, so an inactive tab kept a fill and read as a second
active state. The file has 241 hover rules and none were guarded. The two on the
pack tabs and the pack tiles are now behind `@media (hover: hover) and
(pointer: fine)`; the rest are a separate pass.

---

## v0.201.90 — Two boxes, and two picker backgrounds

**The tab row was showing two active boxes at once.** The pill, and the tab's own
`.active` background underneath it. The rule setting that background ran after
the rule clearing it, so it won, and the newly tapped tab lit up instantly while
the pill was still travelling. That is the box arriving early. The active tab
only changes colour now, and the pill carries the surface and the shadow, so
there is one indicator that moves rather than two that disagree.

**And the three pickers did not match.** Quick Play and Survival painted `--bg-1`
where Custom paints `--panel`, which is a shade darker. All three take the panel.

---

## v0.201.89 — The tab row stops being rebuilt

The pill jitter had a cause underneath the one fixed last version. Every picker
threw its tab row away and built a new one on each group change, so the pill was
a brand new element every time with no position to travel from. Placing it where
the old tab had been and releasing it was a workaround, and it still sat still
for three frames and then jumped.

The row is built once and only its active state changes after that, so the pill
is the same element throughout and simply moves. Measured in the Quick Play
sheet: 4, 4, 18, 48, 118, 144, 163, 177, 187, 194, 199, 201. It starts where the
previous tab is rather than snapping to the left edge first.

**Not reproduced: the light background difference between the pickers.** Quick
Play and Survival look brighter than Custom on the device. Sampling the painted
pixels in the gaps between tiles returns identical values for all three here,
and the screens do not switch cleanly in the harness, so this needs looking at on
a real device rather than guessed at from a measurement I do not trust.

---

## v0.201.88 — The pill stops restarting, and light mode stops darkening

**The tab pill looked like it began at the first tab on every change.** It did.
`mqGroupTabs` queues a placement on the next frame, and that fired after
`mqSetGroup` had already started the pill moving, snapping it back with no
transition and then letting it travel from there. It skips any row a group change
has already positioned. Measured across a change: 4, 15, 45, 83, 117, 143, 162,
177, 194, 202, one smooth run.

**And the light accents come up.** The default light theme's accent measured
9.18:1 against the surface where 4.5 is the requirement, so it read as near-black
rather than blue. Nine colours across the four light themes now sit at about
4.75:1, the same target the pack inks use: the blue, its two lifts and its
gradient, plus the amber, green and purple themes and their lifts.

This is the last of the same fault: the wash, the rule, the NEXT button, the pack
inks, and now the accents. Light mode had been built by darkening a colour until
it felt safe rather than until it met a ratio, and there was a lot of room under
the bar in every case.

---

## v0.201.87 — its, not it's, and a translation check worth trusting

Three possessives corrected: "came with it's own cartoon", "after it's launch"
and "loving it's sound".

**The translation check across all 134 took three attempts and the first two were
wrong.** The first flagged 32 rows as Italian blurbs written in English; every one
was a false positive, caused by matching English words inside quoted titles like
A Deal with God and Hungry Like the Wolf. The second flagged 17 English blurbs as
reading Italian, because the word list I was matching against contained a, e, i,
in, so and la, which are ordinary English words.

With only unambiguously Italian words and quoted titles excluded, the pack comes
back with one row to read and it is correct: a blurb that is mostly two
proper names and two numbers, so there is little grammar in it either way.

What the check now covers per row: both languages present and distinct, four
Italian options with none empty or duplicated, every number in an English blurb
present in its Italian twin, neither blurb wildly shorter or longer than the
other, and no Italian stem containing its own answer.

Recorded because it has now happened three times in this work: a tool that
reports many failures at once is usually wrong about the data and right about
itself. Both bad versions of this check looked authoritative.

---

## v0.201.86 — The 80s pack is complete at 134

Thirty-three rows translated: the twenty-two hard-tier questions and the eleven
locale additions. Every one of the 134 now carries a stem, four options and a
blurb in both languages.

134 questions: 55 easy, 53 medium, 26 hard. Locale 91 both, 22 English, 21
Italian, which is exactly the 70s split with twenty-one more questions on top.
English players see 113, Italian players 112.

Checked row by row rather than in aggregate: no number present in an English
blurb missing from its Italian twin, no Italian blurb under 55 percent the length
of its English, no stem left identical to the English, and every Italian option
set complete at four.

Italian release titles are used where an option is a title, so an Italian player
reads Una poltrona per due and I Robinson rather than a literal translation of
Trading Places and The Cosby Show, which would read as wrong to them.

Known and deliberate, recorded so the next pass does not report them again: the
word "the" inside Welcome to the Jungle in an Italian blurb, Thriller answering
two questions, and three cross-question name overlaps Daniele has already ruled
on. The omega pass also flags "Wall Street" in the Batman blurb, which is The
Wall Street Journal.

---

## v0.201.85 — Light mode gets its colour back

The light pack inks were darkened far past what contrast asks for, so a pack read
as near-black with a hint of hue rather than as its colour. Advanced Theory sat
at 10.14:1 where 4.5 is the requirement, bass at 8.56, nineties at 8.52.

Every pack now sits at about 4.75:1 against the light surface. Fifteen come up:
Advanced Theory from #3a2578 to #6a56b8, bass from #3a2c9e to #6353cc, the
nineties from #7a1f1f to #b04040.

**And four were failing.** The sixties read 3.75:1, the seventies 4.06, jazz
4.16, music history 4.32, all under the 4.5 that normal text needs. Those go the
other way, down to the same target. One number for the table rather than a spread
from 3.75 to 10.14, which is what let both faults sit there at once.

The NEXT button that started this is on the same principle: light mode had been
treating every colour as something to darken until it was safe, when the bar is a
ratio and there is a lot of room under it.

---

## v0.201.84 — The NEXT button was near-black on dark green in light mode

A light-mode contrast pass over every quiz surface changed in this work found
one real fault. After a correct answer the NEXT button painted `#0a0a12` on
`#224700`, which measures 1.85:1. That is `--in-tune` again: a bright green on a
dark ground, and a dark ink on a pale one, and the button had been written for
the first case only.

It uses the feedback green with white text in light mode, 4.41:1, and keeps the
near-black in dark, where it measures 14.87:1 because the green there is bright.
This is the third place `--in-tune` has been wrong in light: the wash, the rule
and now the button. Anywhere it is used as a fill rather than as text is worth
checking.

Two other things the pass reported and neither was a fault. A dimmed distractor
tile reads 1.79:1, which is the deliberate 30 percent fade on the answers you did
not pick. And the correct tile reported 1.96:1 on the first pass but 93:1 on the
second: the probe cannot read a `color-mix` background reliably, so that number
was the tool failing rather than the tile.

Recording the tooling lesson too, because it cost two passes. The first sweep
returned 35 failures, almost all of them elements sitting behind an opaque sheet.
Checking `elementFromPoint` at each node's own centre cut that to three. A
computed style says nothing about whether anyone can see the element.

---

## v0.201.83 — The Vamos a la playa blurb moves off the song

Two attempts at it both described the lyric, and the stem already tells you the
song is about a bomb, so both were answering the question a second time. That is
why it read as disjointed rather than as a fact: it was a restatement with an
extra clause bolted on.

It is about the band instead. Righeira were two men from Turin, both called
Stefano, and they sang in Spanish because it made the record sound like it had
come from somewhere warmer. One thread, and nothing the question already said.

Also verified, after the triage merge and reinstall: no row missing a translated
field, none where the Italian is identical to the English, every Italian option
set complete at four, and every number and name in an English blurb present in
its Italian twin. 101 of 101 bilingual.

---

## v0.201.82 — Batch three triaged, and a warning about the triage export

Thirteen of the fourteen edited, one flagged. All applied.

**#2 was the flagged one.** The blurb explained the joke, that the song sounds
like a beach record but the lyric is about fallout, and explaining it is what made
it awkward. It states the fact and stops: the bomb has gone off by the second
line and the sea is radioactive, and they sang it over a beach rhythm.

**The triage export drops every Italian field.** The returned rows carry only
`ans`, `d`, `fact`, `opts` and `q`: no `q_it`, no `opts_it`, no `fact_it`. All
fourteen rows came back with the Italian gone, and applying that file directly
would have wiped the translation out of the pack without any error.

The English edits were merged over the existing rows instead, with the Italian
kept and then brought in line where the English had moved: eleven blurbs and four
stems retranslated to match. Verified 101 of 101 rows still bilingual after the
merge and after the install.

Worth knowing for the hard tier, which will go through the same tool: triage the
English first, translate afterwards, or the round trip costs the Italian every
time.

---

## v0.201.81 — The pack pills settle at one height

Taking the count off left a grid that stepped up and down: 40px for a short name,
51 with COMING SOON under it, 53 where the name wrapped to two lines. Three
heights in one grid, which is more restless than the extra line ever was.

The wrapped case is the floor now, so every pill is at least that tall and a row
of them reads as one row. 53px is that case measured rather than a number picked
to look right.

---

## v0.201.80 — The question count comes off the pack pills

The popup you open next leads with it, "90 QUESTIONS IN PACK", so the pill was
saying the same number twice and paying a second line of height to do it. Both
places that emitted it, the Quick Play grid and the Survival grid, now show the
pack name alone. COMING SOON stays, because that is not a count and it is the
only thing telling you the pack is not playable yet.

With one line of text the tile does not need the height it had: padding comes
down from 10px to 9 and the floor from 44 to 40, which takes a pill from 66px to
53. Six pills fit where four and a half did.

---

## v0.201.79 — The Online chips stop starting low

Entering the Online tab hides the pack grid and shows the chip lists in its
place. The grid's container was holding its height for the length of the move,
so the chips rendered below that reserved space and jumped up when it released.

A page that is hidden on the tab being moved to gives its space back at once
rather than at the end. The reservation exists to stop the container collapsing
mid-slide, and a page that is not going to be there has nothing to hold open.

Measured through the move in both directions: the chips sit at 238 across all
fourteen frames going in, and the pack grid sits at 238 across all twelve coming
back out.

---

## v0.201.78 — Timings from the guidance, a guard on fast taps, and the Online tab

**The durations were wrong in a specific way.** Material's numbers: mobile
transitions sit around 300ms, large full-screen ones at 375, and past 400 they
read as slow. Distance scales it, and entrances should run 30 to 50 percent
longer than exits, because what arrives matters more than what leaves.

Mine ran the same 378ms in both directions. They are now 315ms in and 237ms out,
a ratio of 1.33, both inside the range rather than either side of it.

Getting there exposed a mistake in how I was deriving them. I had been using a
spring's full settle time as the CSS duration, which put the first attempt at
466ms in and 398ms out: past the point where a transition reads as slow, purely
because the last fraction of a percent of a spring is being waited for. The
cutoff is a perceptual one now.

**Tapping faster than the move broke it.** A second change started on top of the
first, so leaving copies stacked up, the held height was never released and the
pill chased a target that had already moved. A change during a move is queued and
runs once at the end. Hammering four tabs in one frame now ends on the last one
tapped, with no copies left behind and no heights still locked.

**And the Online tab was the odd one out.** It hides every pack grid and shows
chip lists instead, so it had nothing to slide and nothing to swipe on: the one
tab of four that behaved differently. The chip lists are wired as pages in their
own right. Caught mid-flight: going in, the chips run the entrance while the pack
grid runs the exit; coming out, the reverse.

---

## v0.201.77 — Three faults behind the jank

Not one problem. Three, and the patching had been treating symptoms.

**A swipe was changing two tabs.** `mq2WireSwipe` was attached to
`grid.parentElement`, and the wrapper added for the transition changes what that
parent is, so a second listener landed on the wrapper while the first was still
on the old one. Both fired. It attaches to the grid itself now, which never
moves in the tree. Measured: one swipe moves exactly one tab.

**The container collapsed mid-slide.** The moment the outgoing grid was taken out
of the flow, the container snapped to the incoming grid's height and everything
below jumped while the pages were still travelling. The height is held for the
length of the move, at whichever of the two is taller. Measured across twelve
frames of a tall-to-short change: 366px throughout, no shift.

**And the pages were cross-fading as well as moving**, which reads as two things
dissolving into each other rather than one replacing the other. That was the
muddiness. Pure translate now, and a full width each way rather than a quarter,
so one page is off the screen before the other is on it.

---

## v0.201.76 — The sheet stops re-running its own entrance on a tab change

The jank was a second animation on top of the slide: `.mq-sheet` was running
`mq2PageIn` for 420ms every time a tab changed, so the entire sheet crossfaded
while the grid was travelling.

The cause was the host. The leaving copy needs a positioned, clipping container,
and I had used the grid's `parentElement` for it, which in the Quick Play sheet
is `.mq-sheet` itself. Adding and removing classes there disturbed the sheet's
own entrance animation.

The grid now gets a wrapper of its own, created once and reused, so nothing
outside the grid is touched at any point. Checked across all three pickers: the
sheet no longer animates during a tab change, and the header, the ALL PACKS
button and the tab row hold still through every frame while the grid slides.

---

## v0.201.75 — The leaving grid stops crossing the whole screen

The copy that travels away was absolutely positioned inside whatever the grid's
parent happened to be. In the Quick Play sheet that parent is the sheet itself,
880px tall, so the outgoing packs slid across the header, the ALL PACKS button
and the tabs on their way out, over the top of everything.

Two things fixed it. The copy is now pinned to the grid's own box, its top, left,
width and height taken from the grid rather than stretched to the parent.
And the container clips while a transition is running, so nothing travels outside
the area the grid occupies. Both are set only for the length of the move and
removed afterwards, so nothing else on the sheet is affected.

Verified mid-transition in the Quick Play sheet: the copy sits 0px from the
grid's top, matches its width exactly, and its container reports overflow hidden.

---

## v0.201.74 — The pack tabs slide, and the pill travels

All three pickers share `mqGroupTabs` and `mqSetGroup`, so Custom, Quick Play and
Survival get this together.

**A sliding pill sits behind the active tab.** It travels rather than the active
state switching on, which is what makes four tabs read as one control instead of
four buttons.

**The grid slides in the direction you moved**, and swiping the grid left or
right changes tab. The swipe locks direction once, on the first eight pixels, so
a diagonal drag is either a scroll or a page change and never both.

**The curves are real springs, not a bezier that resembles one.** Apple's model
takes a duration and a bounce, and the same two numbers drive springs in UIKit
and Core Animation as well as SwiftUI, so that is the thing to match. CSS cannot
express a spring, so each is solved and sampled into `linear()`, with a
`cubic-bezier` above it as the fallback. The page runs duration .36 bounce .10;
the pill runs .30 bounce .22, bouncier because it is the thing you touched, while
a grid of text overshooting reads as a glitch.

Apple's duration is perceptual rather than the settle time: a .36 spring is still
moving at 378ms. The CSS durations are the measured settle, so no curve is cut
off mid-overshoot.

**Two things needed continuity that was not there.** Every picker throws its grid
away and builds a new one on a group change, so there was nothing to animate out;
the outgoing grid is cloned and the clone leaves while the real one arrives. The
tab row is rebuilt too, so a fresh pill had no position to travel from and simply
appeared in place: it is now put where the previous tab was and then released.

And the pill is positioned by measuring against the row rather than computing
from `offsetLeft`, which landed a few pixels out because the row has both a
border and padding.

---

## v0.201.73 — Only Survival keeps a line, and the streak rules do not agree

Quick Play said "Select a pack, set question count" and Custom said "Choose
packs, difficulty, and length", which is the same sentence twice and explains
neither. Both are gone. Survival keeps a line because it is the only card with
rules you cannot guess from the title, and it is now "3 lives, endless" rather
than three clauses separated by dots.

The three-emoji line the toast used before the flame was still in the file,
unread. Removed.

**And the streak system is not global.** The same flame means different things
depending on where you are:

    chord ear training   lit at 3    glow at 5    blaze at 10
    quiz streak toast    lit at 5    glow at 10   blaze at 20

There is a third scale as well: the chord module's own tier count steps at 5, 10
and 25. So a player who hits a blazing flame in ear training at ten answers meets
a flame in the quiz at ten that has only just started glowing.

Not changed here, because picking one set of numbers changes how a module that
was not part of this work feels, and that is a decision rather than a fix. The
quiz numbers follow its own multiplier tiers, which step at 3, 5, 10 and 20, so
there is an argument for either.

---

## v0.201.72 — One flame, three states

The toast was swapping between a flame, a lightning bolt and a crown depending on
how long the streak was: three emoji doing one flame's job, added straight after
the rest of the module had been cleared of them.

It uses the flame the chord and interval racks already use, with the same three
states. Lit at five, glow at ten, blaze at twenty. The treatment escalates, not
the symbol, so a streak looks the same everywhere in the app.

`mqShowXP` only ever set `textContent`, so a flame with its own classes had
nowhere to live. It takes markup as a second argument now and the old call sites
are untouched.

---

## v0.201.71 — The streak toast becomes a milestone again

It was firing on every answer past a three streak, which is most of a good run
and turns a reward into a tic. It fires on multiples of five, the way the rest of
the app marks a streak: 5, 10, 15, 20 and on.

The milestone haptic and cue were on 5, 10 and 20 only, so a fifteen streak got
nothing and a twenty-five got nothing either. They run on the same rule now, so
the sound, the buzz and the toast arrive together.

**And the multiplier comes out of the toast.** It already sits beside the score
in the feedback block, so the toast said it twice. It carries the streak alone:
the icon changes at ten and at twenty, which is the only thing marking how far in
you are.

---

## v0.201.70 — The streak toast comes back

The chip beside the multiplier is retired and the toast returns. It was dropped
because it would have repeated the points the feedback block already counts up,
which was a fair objection to the old toast and the wrong fix: the toast now
leaves the points out and carries only the streak and the multiplier, which
nothing else on the screen says.

`mq2ToastPlace` already positioned it under the band rather than over the
answers, so the machinery was there the whole time. Measured: band ends at 179,
toast opens at 195.

---

## v0.201.69 — The landing badges go

INSTANT START, YOUR RULES and ENDLESS are removed. Each card already carries a
description that says the same thing better: Quick Play selects a pack and sets a
question count, Custom chooses packs and difficulty and length, Survival is three
lives and no end. The badge was a second, vaguer version of the line above it.

Two things reported alongside this that turned out not to be faults, recorded so
they are not chased again.

**The streak message is present.** It is a chip beside the multiplier rather than
a toast: on a five streak `mq2Streak` reads "5 STREAK" next to a ×1.5. The toast
was v1, and it was dropped deliberately because under v2 the feedback block
already shows the points, so the toast said the same thing twice and landed on
the answers while doing it.

**The pack counts are right, but they are per language.** The 70s reads 92 and
holds 113; the 80s reads 87 and holds 101. The difference is the locale-tagged
questions the other language sees. The number is what you can actually play,
which is the useful one, but it will never match a pack total quoted from the
build file.

---

## v0.201.68 — The v1 guards come out

`MQ_V2` sites drop from 46 to 11. Every inline guard is collapsed to its v2
branch: the screen switches, the holdover, the picker sheets, the custom rows,
the reveal, the feedback, the pack labels, the review and daily paths. The dead
v1 half of each is gone.

Walked from a clean browser context in both languages after the cut: landing,
Quick Play sheet, Survival sheet with its pack labels, Custom, a survival
question with three hearts, a fatal answer that reveals and says OUT OF LIVES,
and the results screen. No console errors in either language.

**Three orphaned `else` branches were left behind on the way**, each one a
substring replacement that removed an `if` without understanding the structure
attached to it. Every one broke the file outright and was caught by
`node --check` before it went anywhere. Worth recording because it is the
argument for doing the rest slowly: text replacement does not know what an else
belongs to.

**The sentinel earned its keep twice.** It flagged the topbar holdover pin and
the fatal-answer pin, both of which I had deliberately changed by collapsing the
guard inside them. Those are the "intentional? update the pin" case and the pins
were updated. Had either been an accident, the same alarm would have caught it.

**What is left, and deliberately not done here:** three functions still open with
`if (MQ_V2) { ... return; }` and carry a v1 tail after it, `mqShowWin`,
`mqShowResults` and `mqShowDailyResult`. Removing those means deleting whole
function bodies rather than single lines, and they are tied to the v1 markup, the
feedback sheet, the heart bar, the skull and the win screen. The dev toggle in
settings also still expects to be able to turn v2 off, which stops being true the
moment those tails go.

That is a deletion pass rather than an edit pass, and this file is clean right
now. Better to start it from a clean state than to continue from a long one.

---

## v0.201.67 — Survival's last question, and a net under the v1 cut

**The fatal answer never revealed.** Losing the last life called
`mqShowFeedback` and returned before `mq2Reveal` ran, so the final question of a
survival round showed no tile states, no wash and no rule: you answered, nothing
happened, and the only sign the run had ended was the next button's label
changing to RESULTS. It reveals like every other question now, and the band says
OUT OF LIVES, with the spent hearts dimmed behind it. Both languages.

**And the quiz v2 work is pinned before any of v1 is cut.** The sentinel tracked
97 fixes, none of which covered anything built here: the transition, the pack
marks, the palette, the feedback sequence, the score count, the hearts, the
Custom overlay, the picker scrim. It tracks 123 now.

The pins were tested by breaking the file nine ways, each a plausible slip while
removing v1: dropping a `MQ_V2` guard, renaming a function, cutting an element,
losing a CSS override, flipping the default back. All nine are caught.

Three of those pins only exist because the first version of them failed the test.
`function mq2RenderHearts` is a prefix of `function mq2RenderHeartsOLD`, so a
rename walked straight through; the signature is pinned instead of the name.
Defining the hearts renderer is not the same as calling it, so the call site is
pinned separately. And pinning the CSS is no use if the element it styles is cut
with the markup around it, which is precisely how the hearts container came to be
shown and empty. The markup is pinned too.

v1 has not been removed. The net is in place first, which is the point.

---

## v0.201.66 — v2 becomes the quiz

`MQ_V2` defaulted to false and only turned on if `localStorage.intonare_mq2` was
set to '1' by hand. **A fresh install got the old quiz.** Everything built in this
work, the question transition, the pack marks, the palette, the answer feedback,
the survival hearts and the Custom overlay, was invisible to anyone who had not
set that key. Confirmed from a clean browser context: the v2 band, grid and marks
all hidden, the v1 answer buttons rendering.

The default is on. The key still works in reverse, so setting it to '0' turns v2
off from the console if something turns up on a device.

**The fork is narrower than it looked.** Only `mqScreenQuiz` has separate v2
markup, 26 elements against 1 v1 leftover. The landing, Custom, results, review
and the daily screens are the same DOM restyled through `body.mq2on`. So this is
one screen rebuilt plus a lot of CSS, not a parallel application.

Walked from a clean context in both languages: landing, Custom, survival picker,
a survival question with hearts, an answered question with the wash and the rule,
and results. No console errors in either language, and the v1 answer buttons stay
hidden throughout.

**This also explains the empty hearts.** `mqUpdateHearts` writes to the v1 heart
bar because v1 was the live path; v2 was the branch that had not been wired up.
That class of fault should now stop appearing, since there is one live path
rather than two.

Still open, and now visible to everyone rather than to whoever set a key: the
survival game over announces itself only by relabelling the next button.

---

## v0.201.65 — Survival gets its lives back

**The v2 quiz showed an empty hearts container.** `mqRenderQ` sets
`mq2Hearts` to display flex for a survival round and never puts anything in it,
so it collapsed to zero height, while `mqUpdateHearts` faithfully updated the v1
heart bar that v2 does not show. Survival has been running with no visible lives
and no way to learn that you get three.

They render now, using the same mask, the same fill and spent states and the same
pop as the chord ear training rack, so a heart means the same thing in both
places. The one just spent pops as it goes.

**And the emoji I reported are not on screen.** A sweep found a skull, a trophy, a
clipboard and a tick, and I reported them as live in the quiz UI. Driving a real
survival game over and reading only what is actually painted returns none of
them: the skull and the trophy are both hidden in the v2 path. The sweep queried
elements without checking visibility, and when that was challenged I confirmed
the element existed rather than that it rendered. Presence in the DOM is not
presence on screen, which is the same mistake that reported two blank pack marks
as fine earlier in this work.

Still open: the game over moment itself. Losing the last life sets lives to zero
and changes the next button's label to RESULTS, and that is the whole event.

---

## v0.201.64 — The spread lands sooner, and the score stops jumping

The correct-answer spread runs in 400ms instead of 500, on a slightly firmer
curve.

**The score was the one thing in the answer sequence that jumped.** Everything
around it eases: the tiles dim over about 300ms, the rule opens, the wash fades,
the next button arrives. The number went from 300 to 400 in a single frame. It
counts up over 420ms on an ease-out, so it lands rather than stopping, and it is
short enough not to hold up the next question. Measured at 22 distinct values
across the run. Reduced motion sets it directly.

A sweep of the rest of the quiz for anything that changes without moving turned
up three things that need a decision rather than a fix:

**The results ring reads zero in the harness**, so whether it animates is still
unknown. Driving that screen from the console does not reproduce a real round,
and I would rather say so than report a clean result I did not actually get.

**The per-pack bars on the stats sheet appear at their final width.** Growing
them from zero is the obvious treatment, and the sheet is a moment of rest where
it would be welcome, but it is a change to a screen that was not part of this
work.

**Four emoji are still in the quiz UI**: a skull on the survival game-over
screen, a trophy, a clipboard on the share control, and a tick on the feedback
verdict. The earlier emoji removal covered the stats sheet only.

---

## v0.201.63 — The wash stops travelling

Sliding the gradient up from below the band dragged a hard edge through it and
finished as a large coloured field behind the question. It fades in where it
already sits and reaches only 34 percent up the band, so nothing moves across the
text and the question stays on its own background.

---

## v0.201.62 — The band stops recolouring on an answer

Tinting the whole band toward the answer colour is the largest signal available
for a message the answer tiles have already delivered, and it makes the question
harder to read past while you are still looking at it. It is replaced by two
smaller things.

A wash sits at the bottom of the band, behind the question and the beat strip
rather than over them. It fades in where it already is: animating it upward
dragged a visible edge through the band, and by 300ms it had climbed behind the
question and become a large coloured field, which is the recolour it replaced
wearing a different shape. It stops at 34 percent of the band height, well below
the text. And the rule carries the outcome: it opens from a point at
the centre over 500ms for a right answer, and blinks in hard steps for a wrong
one. Both start from an empty rule, so the difference is entirely in what happens
next. **The two outcomes differ in rhythm as well as in hue**, which means neither
depends on telling green from red.

**Answer feedback gets its own two colours.** `--in-tune` and `--sharp` are used
229 and 125 times across the tuner and the exercises, and in light mode they are
inks meant for text on a pale ground: 8.8:1 and 9.7:1 against the quiz band. Used
as a fill they read as bottle green and brown, which is what "muddy" was.
`--fb-ok` and `--fb-no` are mid tones in light, 3.7:1 and 4.7:1, still past the
3:1 a coloured indicator needs. Dark keeps the existing pair, which already works
against a dark ground.

Two faults on the way in, both mine. A rule written for the motif, "everything in
the band sits above the mark", was sweeping `position: relative` onto the new
layers: the wash collapsed to zero height and the rule effect dropped into the
text flow at the top of the band. And the mockup had been carrying a hand-written
light palette rather than the app's, so its background and its blue were both
wrong; the values are read out of the running file now.

---

## v0.201.61 — The four recheck edits reverted

The duplicate Thriller answer and the three cross-question name overlaps are
Daniele's call and go back as they were. Thriller answers both the album question
and the Landis video question; the Nintendo stem, the Reagan stem and the Indiana
Jones blurb all read as written.

The two Italian rhythm fixes stay, since those were faults introduced in
translation rather than choices.

---

## v0.201.60 — Medium finished, and four faults the recheck found

**Rechecking the installed pack surfaced four things the per-batch tools could
not see**, because each of them only ever looked at fifteen rows at a time, and
all four were then reverted as deliberate.

*Thriller* answers two questions, the 1982 album and the 1983 video. Three
questions name another question's answer: a stem reading "Which **Nintendo**
character", a stem naming **Ronald Reagan**, and a blurb naming **Indiana
Jones**. Recorded here so the next pass does not report them again as new.

The check itself was worth adding and stays: duplicate answers and cross-question
leaks are now measured across all 101 rows in both languages rather than inside a
batch of fifteen. It just does not get to decide.

Two Italian blurbs had landed as balanced sentence pairs in translation where the
English did not. Fixed. The English pair at 56 and the pronoun opening at 57 are
Daniele's own edits and stay.

**Medium is finished at 47**, which matches the 70s. Fourteen new questions, ten
of them locale-tagged, which takes the locale spread from 8 and 9 to 13 English
and 14 Italian.

101 questions, all bilingual: 54 easy, 47 medium. English players see 87, Italian
players 88.

The new Italian rows are the ones an English-language pack cannot carry: Battiato
being the first million-seller, what Vamos a la playa is actually about, how
Canale 5 broadcast nationally before it was allowed to by posting the same tapes
to dozens of local stations, the cacao meravigliao, Gianna Nannini in Berlin.

---

## v0.201.59 — The 80s pack was English only

All 87 questions installed in the last version carried no Italian at all: no
`q_it`, no `opts_it`, no `fact_it`. The 70s, Beatles and Guitar Gods packs carry
them on every single row. An Italian player opening the 80s pack was reading
"Which car did Doc Brown turn into a time machine in Back to the Future" in
English, on a pack marked playable.

All 87 are translated: stem, four options and blurb each. Italian players see 79
questions, English players 78.

**And I had the `loc` field wrong.** I had taken `loc: 'it'` to mean the row is
written in Italian. It does not: it controls who is shown the row, and every
locale-tagged question in the shipped packs still carries both languages in full.
An Italian-only question in the 70s pack has complete English text sitting in
`q` and `fact` that no English player will ever see.

The Italian check reports one error and four reads. The error is the word "the"
inside Welcome to the Jungle, which is a song title. The four reads are quoted
material rendered into Italian rather than kept verbatim: a banner at a Naples
cemetery, Fred Astaire on the telephone, and two sets of song titles.

---

## v0.201.58 — The 80s pack goes in, and two dead fields come out

**Everything written for the 80s this session was sitting in JSON, not in the
app.** The pack in the file was an old draft of 68 questions, 59 of them with no
difficulty tier at all, opening with stems that did not survive triage: "What did
a Sony Walkman let you do", "What is a Rubik's Cube?", "What happened to the
Berlin Wall". It was also not marked playable.

The 87 triaged questions are in, through the builder's round trip: every field
read back out of the written file and compared against the draft. 54 easy, 33
medium, locale split 70 both / 8 EN / 9 IT, all answer-first, all four options,
all with a blurb. The pack is playable, which takes the app from seven packs to
eight.

**And the pack colour was defined in two places that disagreed.** Every pack
carried its own `color`, left over from before `MQ_PACK_COLORS` existed, and four
of them no longer matched: the 80s said violet where the table says leg warmer
pink. Nothing reads the field. `mqPackCol` goes through the table as a CSS
variable, verified by watching the property at runtime rather than by reading the
code. Removed from all 19, along with the `emoji` field, which nothing has read
since the stats sheet moved to `mqPackIcon`.

That leaves one source for a pack's colour, which matters because the next person
to change one would have had a coin flip on where to do it.

---

## v0.201.57 — Two measured faults in accidental spacing

The stacking itself is correct. Accidentals in a chord are packed into columns,
anything within a vertical threshold moves one column further left, and across
every case tested there were no collisions. What was wrong was both of the
constants it uses, neither of which cleared the glyphs they were meant to.

Measured glyph boxes: a flat is 8.14 by 22.1, a sharp 8.96 by 25.13, a double
flat 14.8 by 22.03, a natural 6.05 by 24.34.

**The clash threshold was 25 and a sharp is 25.13 tall.** Two sharps exactly 25
apart passed as clear while their glyphs touched. It is 28 now, which clears the
tallest sign with a little air.

**The column step was 12.5 and a double flat is 14.8 wide.** Two double flats in
adjacent columns overlapped by more than 2px. The step is 17, which clears the
widest sign; a plain flat simply gets more room.

Verified with three flats, three sharps and three double flats: three columns
each, 17px apart, zero overlapping pairs.

**Not reproduced: the misalignment in the reported screenshot.** Every stacked
case renders correctly here, so whatever is in that shot is either one of these
two constants in a case I did not think to build, or something else entirely. The
exact question would settle it.

---

## v0.201.56 — The first round of a session stops tearing down a question that was never there

Starting a round ran the transition's exit path first: 190ms of fading out an
empty band before the question was built. It only showed on the first launch,
because after that the timing happens to hide it.

The check for a fresh start was `!root.classList.contains('mq2') || MQ._v2first`,
and on a cold app the root already carries `mq2`, so this read as a mid-round
change. `mq2-fresh` is the honest signal: `mqShowScreen` sets it every time the
quiz screen is entered and it means the band is empty. Nothing to fade out, so
nothing is faded out.

Verified across three consecutive rounds from a cold load: no tear-down path,
entrance begins at 1ms rather than 190. And question to question inside a round
still uses the exit path, which is what makes the band hold still while the
question turns over.

---

## v0.201.55 — No fade on the way back from any of the three

The replayed entrance added last version is reverted, and Custom no longer fades
the landing either. All three routes simply reveal it.

**The last flash was caused by the fix for it.** Custom suppressed the landing's
`mqFadeUp` with a class and then removed that class 80ms later, which restarted
the very animation it was suppressing: the landing dropped to opacity 0 and
climbed back while fully on screen. Traced frame by frame, it was at 0 at 412ms,
0.08 at 445, 0.26 at 462, back to 1 by 520.

The suppression is cleared when a screen is next hidden instead, where there is
nothing visible to animate. The landing still gets its normal entrance
everywhere else, verified by leaving and returning through the quiz screen.

Measured across three runs of each route, sampling actual pixels: worst dip 0.12
for Custom, 0.04 for both pickers, against a settled 20.6.

Also recorded: the landing is now made active behind Custom before Custom starts
leaving, so it is uncovered rather than swapped in. Two earlier orderings of that
handoff both left a frame where neither was painted.

---

## v0.201.54 — The landing fades back in from the pickers too

Coming back from Custom, the landing is re-shown from hidden, so it replays its
own `mqFadeUp` entrance and arrives rather than appearing. Quick Play and
Survival never hide it: it sits untouched behind the sheet the whole time, so
the return has no fade at all and the landing is simply revealed as the sheet
clears. That is the difference between the three routes.

The landing replays that entrance explicitly on the way back from a picker,
starting at 170ms so it comes forward as the sheet gets out of the way rather
than behind it. Opacity and an 8px rise over 380ms, with a reduced-motion path.

The three routes now read the same on the way out and on the way back.

---

## v0.201.53 — The flash was the sheet's own scrim, not the landing

`.mq-sheet-overlay` carries a `rgba(0,0,0,.6)` scrim in its base style, and the
v2 rule that clears it was written against `.active`. Removing that class at the
end of the exit reverted the background to black at 60 percent instantly, while
the overlay's own opacity took 200ms to fade out. So a dark sheet painted across
the landing for a fifth of a second, after the picker had already slid away.

The scrim is cleared whether or not the overlay is active.

**This took four attempts because I kept measuring the wrong thing.** The landing's
opacity, `#mqBody`'s opacity and the panel's classes are all unchanged through the
entire return, which is why every trace came back clean while the flash was
plainly there on device. Sampling actual pixels found it immediately: mean
luminance across the top of the screen dropped to 13.4 for one frame against a
settled 20.5.

Measured now, frame by frame on both pickers: no dip at all. When a computed
style says nothing is happening and the screen disagrees, the screen is right and
the property being watched is the wrong one.

---

## v0.201.52 — Quick Play and Survival stop flashing on the way back

The difference between Custom and the two pickers was the dim, not its timing.
Custom dims the landing while the page rises and lets go after 460ms. The pickers
held the landing at 45 percent for as long as the sheet was open, so coming back
always meant brightening something, and that brightening is the flash.

The sheet is opaque and covers the panel once it has arrived, so holding the
landing down underneath achieves nothing. The pickers release the dim after the
entrance now, exactly as Custom does.

Measured on both: the landing sits at 1 while the sheet is open, and the return
shows a single value rather than a ramp. Custom reads the same, which is the
point. The 150ms delay added in the last version is gone, since there is no
longer anything to delay.

---

## v0.201.51 — Custom is an overlay now, not a screen imitating one

Quick Play and Survival cover the panel because they are children of it. Custom
sat inside `#mqBody` and imitated them: reaching over the topbar by a measured
offset, re-padding its own content to compensate, and hiding the bar behind it.
Three workarounds to make one kind of thing behave like another, and it still
stopped short on device.

It is moved to the panel on first open and styled like the two pickers. Measured:
parent is `mqPanel`, starts at 0, 880px tall against an 880px panel, with its own
BACK at 8px from the top. The topgap variable, the compensating padding and the
rule that hid the topbar are all gone with it.

**And the landing was brightening while the sheet was still sliding out over it**,
which is the flicker. The sheet takes 340ms to clear and the dim came off at
frame zero. It comes off at 150ms instead, so the landing arrives as the sheet
gets out of the way: at 136ms the sheet is 60px down and the landing is still at
45 percent, at 269ms the sheet is at 390 and the landing is at 89.

---

## v0.201.50 — Custom becomes a full page, and the landing stops blinking

**Custom stopped 42px short of the top.** Quick Play and Survival are overlays
sitting on the panel, while Custom is a screen inside `#mqBody`, which begins
below the topbar. It reaches over the bar now by the gap `mq2CustomEnter`
measures, so the figure lives in one place rather than being written into the
stylesheet twice.

Two things fell out of that. The topbar's stats button ended up sitting on top of
the page, so the bar goes invisible while Custom is open while keeping its 42px,
which is what stops the landing behind from reflowing. And extending the page
upward took its content with it, putting Custom's own BACK above the screen, so
the scroller carries the same offset as padding. BACK measures 48px from the top
of the panel, where it was.

**Coming back from Quick Play and Survival, the landing blinked.** `mq2-picking`
dims it to 45 percent, and removing the class snapped it to full instantly while
the sheet was still sliding out over it. The opacity eases now on a 340ms curve
that matches the exit. Measured across the return: ten intermediate values rather
than a jump.

Custom never had the blink because it holds the landing with `mq2-holdover`
rather than dimming it, which is why the two routes felt different.

---

## v0.201.49 — The stats sheet drops its emoji and comes up to the type floor

The per-pack breakdown used `pack.emoji`, falling back to a music note for any
pack without one, which is every pack since the emoji field was removed. It uses
`mqPackIcon` instead: the app's own line icon in the pack's own colour, the same
mark the pack grid and the quiz band already use.

**And the sheet was still typeset below the floor the quiz uses.** One label at
7px, two at 8 and two at 9, against the 11px minimum set for the quiz screens.
All five lifted, labels to 11 and figures to 12. Nothing on the sheet is under
11px now.

The emoji was the reported problem and the type was the one underneath it. Worth
noting the type floor pass covered the quiz module only; the stats sheet sits
outside it and was never swept.

---

## v0.201.48 — The empty band no longer shows, and the marks fit their box

**A blank band with the previous pack's rule colour was still flashing up.**
Choosing the Beatles showed an empty band with a red line across the bottom,
which is Guitar Gods, until the question built. The rule I wrote to clear it
targeted the root rather than `.mq2-band`, which is where the border actually
lives, so it did nothing at all. The whole band is hidden until the question is
ready and fades in with it. Measured across six frames of entry: band opacity 0
throughout.

**And the artwork was still being scaled past its own layer**, which is what kept
cutting the top off the bass headstock. It is no longer scaled at all: the layer
is 150px, the drawing fits inside it, and the bleed comes from the layer hanging
off the right edge rather than from blowing the drawing up beyond its box. Every
mark is now whole.

---

## v0.201.47 — A round starts from nothing, and the headstock keeps its tuners

**The mark is solid from the top.** It starts 46px down, below the top row, so
there was nothing up there to protect and the fade was taking the tuners off the
bass headstock, which is the part that identifies it as one.

**A new round now builds the whole band, not just the question.** Blanking the
question alone left the previous round's pack name, score, beat strip, band
colour and mark sitting on screen while the new one built, so a fresh game opened
on the tail of the last one. The band is held completely empty on the way in and
everything arrives together: score and difficulty first, then the pack name at
60ms, the mark at 120, and the beat strip at 200. Measured across the first six
frames of entry: pack, mark and beats all at zero, and the band rule transparent.

The staggered arrival applies only to a fresh round. Question to question inside
a round, the band holds still, which is what the anchoring work established
earlier.

---

## v0.201.46 — The topbar, the stale question, and two mark faults

**The shift was the topbar, exactly as reported.** `mqShowScreen` hides the BACK
and stats bar the moment another screen becomes active, and under v2 the landing
is still on screen underneath as a holdover, so pulling 34px out from over it
reflowed it upward. The bar stays while a holdover is showing. The landing's hero
measures 106px before and during, where it was 106 then 64.

**Entering a round showed the previous question**, complete with its revealed
answer, until `mqRenderQ` ran a few frames later. Measured at eight stale frames.
The quiz screen is blanked on the way in and held invisible until the new
question is built: zero stale frames now.

**The marks were being clipped by their own layer.** The artwork was scaled to
1.7 inside a 112px box, so its top was sliced off by the layer's overflow rather
than by the mask. The layer is 152px and the scale is 1.25, and the mask fades
into the top rather than meeting it.

**And Guitar Gods was almost invisible.** A deep red at 20 percent on a near-black
band has very little to work with. The mark now takes its pack colour mixed 72
percent toward white in dark mode and 80 percent toward black in light, so the
dark colours come up without the bright ones blowing out.

---

## v0.201.45 — Custom's padding, the mark's height, and a clearer unison question

**Custom lost its side padding and the landing shifted behind it**, and both were
the same cause: making a screen `position: absolute` takes it out of `#mqBody`,
which is where the 16px came from. Custom's scroller and the held-over landing
both carry it themselves now, and the START bar is inset to match. Verified: the
landing's hero does not move when Custom opens, 86px before and during.

**The mark started at the very top of the band**, which is where the score sits,
so the segno was drawn across the 500. It starts 52px down and stands 112px tall,
which clears the score by 6px on every pack. It still holds its position when a
question brings a diagram and the band grows.

**The unison question said "the next string up"**, where up can mean higher in
pitch or higher on the diagram and the player should not have to work out which.
It names the target string outright now: the marked note is on string 3, which
fret on string 2 gives the same note. Both languages.

**Not fixed: the accidentals in a stacked chord.** In a B flat major progression
the flats sit on top of each other. The renderer does stack them into columns,
12.5px apart, treating anything within 25px vertically as a clash, so the
machinery is there and something about it is not firing on this case. The
accidentals are drawn as paths rather than text, so it needs its own look rather
than a guess at the end of a long session.

---

## v0.201.44 — The pack mark becomes an edge bleed, and the column goes

The reserved column is gone. The mark hangs off the right edge at 1.7x, cropped,
at 20 percent in dark and 26 in light. It reads as texture rather than as a
picture that has to fit, and that removes the entire class of problem the column
created.

**The question gets its full width back** in every pack and both languages: 372px
against 268. The extra line a long Italian question cost is gone with it. Nine
packs stop paying for an empty column.

**Nothing needs tuning per mark any more.** `fit`, `ink` and `drop` are deleted
along with the table that held them. A cropped mark does not need to be sized,
weighted or dropped, because it was never going to fit in the first place. That
is a dozen versions of per-mark adjustment removed in one edit.

**And it holds still.** The mark is positioned against the band's top and its own
132px height rather than against whatever the question contains, so a generated
question with a fretboard under it does not move it. Measured across six cases
including one where the band grows from 187px to 338: mark top 0, height 132,
stem width 372, every time.

**The alignment sweep asserted that the stem must never reach the mark**, which
was right when a column kept them apart and is now a test for the thing we chose,
since an edge bleed sits behind the text on purpose. That is the second check my
own edit has invalidated, so rather than delete it, it is replaced with the one
the guidance actually gives: contrast against the worst pixel rather than the
average, computed by compositing the mark at full strength over the band. Worst
case across six packs and both themes is 6.73:1 against the 4.5:1 body text
needs, and dark mode never drops below 9.61.

---

## v0.201.43 — One table for size, weight and position

Every mark had its own box, its own scale and its own baked opacity, which is
why the bass looked cut off and too large while the piano overwhelmed everything
around it. They go through one table now:

  fit    how much of the column the artwork fills
  ink    how present it is, because a solid silhouette at the same alpha as line
         art reads far heavier
  drop   the mark is tall enough to reach the score, so it starts lower

The piano runs at 0.68 fit and 0.62 ink because it is a large solid shape; the
guitar cabinet runs at 0.92 and full ink because it is thin outlines. That is the
adjustment that was missing, and no amount of tuning a shared opacity was going
to find it.

Removing the top fade in the last version exposed something it had been hiding:
the Abbey Road crossing reaches the top of the band and was running behind the
score. It drops now, like the headstock and the cabinet.

---

## v0.201.42 — The top fade goes, and marks for Vocals and Keys

**The bass headstock was faded across its top**, which is where the tuners are,
so the one part that identifies it was the part being hidden. The mask faded the
top 20 percent to protect the mark from a top bar it no longer touches, since the
layer already starts 30px down and tall marks start 56. It is solid from the top
now and fades only as it approaches the beats.

**Vocals is a microphone by Uswa KDT and Keys is a grand piano by dinnerchief**,
both from the Noun Project, both credited in Credits and Thanks. The credit text
is stripped from each file so it does not render inside the mark, and every fill
is rewritten to the pack colour so they take the theme like the rest.

Worth flagging: the microphone is 105 paths and about 60KB, against 3KB for the
piano. It carries the file from 11.50 to 11.57MB and it is the most detailed
thing in the module by a wide margin. It reads well at this size, but a flatter
silhouette would cost a twentieth of the bytes if one turns up.

---

## v0.201.41 — The headstock and the cabinet sit lower

Both are tall enough that their tops were reaching the score. They start 56px
down now instead of 30, and the floor comes up to 46px with them, because moving
only the top pushed the artwork into the beat strip instead.

Recording a run of measurement mistakes, because four in a row on one small
question is a pattern rather than bad luck. `svg.getBoundingClientRect()` returns
the layer box, not the drawing, so with `preserveAspectRatio="meet"` it reports a
shape far larger than the ink. Sampling pixels instead then caught the score digit
and the beat strip, which live in the same column as the mark. The reliable check
here was a zoomed screenshot and a pair of eyes, which is how the problem was
reported in the first place.

---

## v0.201.40 — A real bass headstock

The supplied Noun Project icon by Studio TROISQUATRE is in, and it is what a
headstock should look like, which my freehand attempt was not.

The file is a 100x125 box: the artwork occupies the top 100x100 and the credit
sits underneath as two lines of text. The viewBox crops to the artwork so the
credit does not render inside the mark, and the attribution goes where it belongs,
in Credits and Thanks alongside Bret Pimentel's diagrams. New `credits_icons`
heading in both languages.

Verified there are no text nodes left inside the mark.

---

## v0.201.39 — A wave for Bass, and the segno sized down

The segno filled more of its box than a clef does, so at the same nominal size it
read much larger. `mq2Glyph` takes an optional scale and the segno runs at 0.74,
which puts it in step with the treble clef beside it.

**Bass is a long, low wave**, one and a half slow cycles across the column with a
second pass behind it. Bass is the bottom of the spectrum, so a low frequency says
it without drawing an instrument.

Worth naming the pattern, because it explains which of these have worked. The
marks that landed are geometric: a perspective grid, a sunset of straight bands, a
crossing of parallel stripes, a rectangle of speaker circles. The ones that did
not were organic objects drawn freehand: a headstock, a grand piano, a
microphone. A waveform is geometry.

The reference sent for the headstock was a watermarked stock illustration, so
tracing it was not an option regardless.

---

## v0.201.38 — Reverted to the seven marks that were actually asked for

The icon reuse is out, and so are the hand-drawn headstock, grand piano and
microphone. Seven marks remain, all of them ones Daniele picked by name: the 80s
grid, the 70s sunset, the Abbey Road crossing, the wall of amps, the pick, the
treble clef and the segno.

Twelve packs run on colour alone, which is where they should sit until the packs
themselves exist. Keys and Vocals are not playable yet, so drawing marks for them
was work done ahead of the thing it was for.

The `mq2IconMark` helper is gone with them rather than left behind unused.

---

## v0.201.37 — Stop hand-drawing vectors and use the icons that already exist

The headstock was a blob, the grand piano was a shape with a diagonal line
through it, and the microphone was a lollipop. Hand-drawing a vector of an
instrument is the wrong tool, and what came out looked hand-traced because it
was.

Every pack already has a properly drawn line icon in `mqPackIcon`, all nineteen
of them, in the visual language the rest of the app uses. Seven marks are that
icon at size now, with the stroke thinned from 1.7 to 0.85 so it does not turn
into a woodcut on the way from 20px to 104.

Four keep a drawing of their own, because they are things an icon set has no
entry for: the 80s grid, the 70s sunset, the Abbey Road crossing and the wall of
amps. Those were worth the effort. A microphone was not, because a good one
already existed twelve feet away.

---

## v0.201.36 — Four marks that are the instrument, not a symbol for it

**The circle of fifths was an answer key.** It sat beside the question with every
note name on it, on the pack whose questions are about note names. Theory
Fundamentals is a treble clef, which says the same thing about the pack and gives
nothing away.

Bass is a headstock with three tuners one side and two the other. Keys is a grand
seen from above, the bent side against the straight spine, with the bench. Vocals
is a stage mic.

The clef, the pedal mark and the breath mark were all defensible as symbols and
none of them was the instrument. A pedal mark says a piano is involved somewhere;
a grand piano says Keys.

Recording an error worth not repeating: I sliced the motif table by searching the
whole file for its keys, and `advanced_theory` appears earlier in the file than
the table does, so the slice came back empty and the edit silently did nothing.
The assertion caught it. Slice inside the block, not the document.

---

## v0.201.35 — Eight glyphs removed for saying nothing about their pack

I filled every empty column with a notation glyph, and eight of them were
notation for its own sake rather than a mark that means anything.

Gone: a quarter note for Drums, a bend for Jazz, a marcato for Rock & Metal, a
fermata for Studio, and a coda, a trill, an fff and an end repeat for the four
decades. None of those symbols says anything about the pack it was standing in
for. A decade in particular cannot be said by a notation glyph at all, which is
why the Seventies and Eighties have a sunset and a grid.

Four are kept because the glyph IS the thing. The F clef is what bass music is
written in. The pedal mark belongs to a piano and to nothing else. The breath
mark is literally where a singer breathes. The C clef is the one you meet in old
scores, which is what Music History is about.

Eleven packs carry a mark and eight run on colour alone, which is the right
answer until those eight earn something drawn.

---

## v0.201.34 — Every pack has a mark

Twelve packs had an empty column. All twelve have one now, and since Bravura is
already loaded the useful ones are real notation rather than something I would
have had to invent: an F clef for Bass, a pedal mark for Keys, a breath mark for
Vocals, a bend for Jazz, a marcato for Rock & Metal, a fermata for Studio, a C
clef for Music History, a coda for the Fifties, a trill for the Sixties, an fff
for the Nineties, an end repeat for the Noughties, and a quarter note for Drums.
Nineteen of nineteen.

**Hand-tuned baselines do not survive contact with a music font.** Glyphs sit at
wildly different heights inside their em box, and a percussion symbol drawn high
landed outside the visible area entirely. Each mark measures its own ink through
the canvas metrics and centres on that, which also removed twelve pairs of
hand-picked numbers.

**And a codepoint can be present in a subset font with its outline stripped.**
The snare drum and the sforzando both measured as present, reported a sensible
advance width, and drew nothing at all. Two marks would have shipped blank. They
are a quarter note and an fff now, and `mq2Glyph` returns empty rather than an
invisible mark when the ink box comes back with no height, so this fails loudly
next time instead of quietly.

Worth recording that my own blank-detector then reported three false positives,
because it sampled the red channel and the fermata, the coda and the pick are all
green or teal. The render is the check; a one-channel threshold is not.

---

## v0.201.33 — The real segno, and a pick that is actually pick-shaped

**Bravura is already loaded** for the notation elsewhere in the app, so the segno
is the real glyph at U+E047 rather than my approximation of one. Verified that
the font resolves before drawing it.

**And the pick was symmetrical top to bottom**, which is what made it read as a
leaf. A 351 has broad rounded shoulders in the top third and sides that fall away
to a small rounded tip. Redrawn to that shape.

---

## v0.201.32 — A pick and a segno, and the rule that is no longer needed

The simpler answer to two staves on one screen was not a rule that hides one of
them. It was to stop drawing a staff.

Guitar Technique is a plectrum. Advanced Theory is a segno. Neither duplicates
anything a question can render, so both can stay up while a fretboard or a staff
is on screen underneath, and the two read as different objects rather than as one
thing drawn twice.

**The suppression rule is gone with them.** It existed only to stop the
duplication, and duplication is not possible now. That removes a class toggle
from the render path, a pair of CSS overrides, and a behaviour where the layout
changed shape depending on the question, which was its own small unpleasantness.

Verified on four cases: the pick and the segno both hold their column with a
diagram present and without, and the stem keeps the same width either way.

---

## v0.201.31 — The mark stands down when the question brings its own drawing

A question with a `vis` renders a real staff, a real fretboard or a real rhythm
line. The marks for Advanced Theory and Guitar are a staff and a fretboard, so
on those questions there were two staves and two necks on the screen at once,
and the decorative one was competing with the one the player has to read.

The rule is automatic rather than per pack: if `q.vis` is set, the mark is hidden
and the question takes the full width back, so the diagram gets the whole band.
It covers every pack and every future one without a list to maintain.

Verified across three cases: a staff question and a fret question both drop the
mark and widen the stem from 268px to 372px, and a question with no diagram keeps
its mark and its column.

This also answers the earlier complaint that the marks looked wrong on generated
questions. Generated questions are exactly the ones that carry diagrams.

---

## v0.201.30 — The cabinet was upside down, and Advanced Theory gets its own mark

**The amp was inverted.** The control panel belongs along the top of a head with
the grille below it, and I had drawn it the other way round. Flipped.

**Advanced Theory had no mark at all**, so its column was empty. It gets a stack
of thirds climbing off the staff with a 13 above, which is the thing that
separates it from the fundamentals, rather than the circle of fifths a second
time. Noteheads a third apart sit on adjacent staff positions, so they alternate
either side of the stem the way they do on paper; stacked in a single column they
read as a blob.

**And the 56px drop applied to everything.** It was added to stop the cabinet
running under the score, and the cabinet is the only mark tall enough to reach
it. It is a `.tall` class on that one mark now, so the other five sit 26px higher
and use the room they have.

---

## v0.201.29 — The mark clears the score, and the two themes meet nearer the middle

**The mark started at the very top of the band**, so on a short question the amp
ran under the score. It starts 56px down now and the smallest gap between the two
across every pack and both themes is 10px.

**Light was much louder than dark.** The layer ran at 53 percent on dark against
100 on light, because I had boosted the baked strength for light and dialled dark
back to compensate. That is a big gap to leave in place: 72 and 86 now.

**The colours were correct all along.** Every pack's label and mark match their
table entry exactly in both themes, checked across four packs. My earlier
measurement said otherwise and it was the harness: the transition defers a render
by 190ms, and reading immediately after `mqRenderQ` picks up whatever the
previous pending timeout writes. Waiting for the transition to land before
reading gives an exact match every time.

Third time this session that measuring during an animation has produced a fault
that was not there. Worth a rule: never read computed style in the same tick as a
render that goes through `mq2Transition`.

---

## v0.201.28 — Soft on every side, and the sun stops being sliced

The bottom fade starts earlier and runs longer, so nothing in the column ends on
a line. Paired with the horizontal fade from the last version, the mark now
dissolves on all four sides rather than meeting a rectangle.

**The 70s sun had a hard cut I put there myself.** It was clipped flat at the
horizon with a `clipPath`, which is a straight edge wherever the mask does not
happen to reach. It fades out through a radial mask instead, so the shape ends
where it should rather than where the rectangle did.

**What the hero guidance says about all this**, which is worth writing down since
it settles two arguments we have been having:

Text left, visual right is a named standard pattern, not an improvisation. The
reserved column is the split hero.

And on scrims: a flat overlay dulls the whole image to protect the corner where
the text sits, which costs you the image to save the copy, while a gradient
darkens only where it is needed. That is exactly the trap the opacity tuning was
in. The reserved column solves it better than either, because there is no text
over the mark at all, so nothing has to be dulled to protect anything.

---

## v0.201.27 — The marks fade out at every edge

The mark stopped at a hard rectangular boundary, which showed worst on the 80s
grid: a perspective drawing that should recede into nothing instead ended on a
straight vertical cut. Two gradients intersected now, so it fades on all four
sides. The right side fades sooner because that edge meets the screen.

**Checked in Italian at the narrowest width.** The longest real Italian question
in the shipped packs is 150 characters, and at 360px it runs five lines and takes
the band to 259px where English runs four. The clearance between the question and
the mark holds at 8px, the mark grows with the band rather than being stranded,
and the answer tiles are unaffected at 129px.

That extra line is the price of the reserved column and it is worth stating
plainly: a long Italian question in a narrow column is the worst case this layout
has, and it costs about 26px of band height against English.

---

## v0.201.26 — The marks get their own space instead of more opacity

The published guidance says two things I had been ignoring while tuning alpha
values. Take advantage of white space, because without it a composition looks
busy and confusing. And prefer simple patterns behind text, because a repeating
one competes with reading.

The band had no white space at all: a centred stem runs the full width, so every
mark was forced underneath the text and the only lever left was making it
fainter, which is a choice between invisible and in the way.

**The stem keeps to the left now and a column is reserved on the right.** The
mark lives there and crosses nothing. Measured: 8px of clearance between the
right edge of the question and the left edge of the mark.

**And the wall of amps is one cabinet.** A three by two grid of speaker cones is
exactly the repeating pattern the guidance warns about, and it was the busiest
thing on the screen by some distance.

Two mechanical faults surfaced on the way. The marks were set to stretch to
whatever box they were given, which was fine across a wide band and turned a
circle into an egg in a narrow column. Switching to crop kept the proportions
but then cut most of the artwork away, because it had been drawn to sit at the
right-hand end of a wide box. All six are redrawn for a portrait column,
centred, one simple shape each.

The circle of fifths now carries all twelve names rather than six, because it
finally has the room.

**A note on the alignment sweep, because weakening a check that your own edit
broke is exactly the move to be suspicious of.** It asserted that the stem's
right edge lines up with the beat strip's, which was the edge that mattered when
the stem ran the full width. The stem now stops short by design, so that check
fails on all 21 cases by construction. It checks the LEFT edges instead, which
still have to agree, and adds a new assertion that the question never runs into
the mark. Both pass at 360, 384 and 412px across all seven content cases.

---

## v0.201.25 — The pack colours, and the marks stop fighting the beat strip

**The palette was designed and never applied.** Theory Fundamentals, Advanced
Theory and Guitar Gods sat at 247, 249 and 252 degrees, which is one colour with
three names, and the screen showed it: three identical purples in both themes.
Both tables are updated, 38 entries across the dark set and the ink set.

Colour by association rather than by a system, with separation enforced only
inside a tab, since two packs in different tabs never appear side by side.
Beatles blue, Guitar Gods a deep stage red, the 80s leg warmer pink, the 70s
burnt orange, the 90s a grunge red, Rock & Metal cold steel, Keys ivory. Theory
and Advanced Theory stay close on purpose and the harder one is darker.

Measured: nothing inside a tab is under 22 apart perceptually except that family,
and every colour clears 3:1 on its own ground in both themes.

**And the marks were at full strength exactly where the beat strip sits.** The
layer ran the whole height of the band, so the amp wall and the 70s sun were
drawn straight through the beats and the two fought. The layer stops 30px short
of the bottom now and fades out as it approaches, so the strip has the band to
itself.

---

## v0.201.24 — The marks stopped being sliced in half

The mask was a hard cut through the reading column, so any mark that spanned the
band lost its middle. The circle of fifths was a top arc and a bottom arc with no
ring between them, the crossing was two sets of stripe ends, and the amp wall was
a row of cabinets above a row of cabinets. They did not read as marks sitting
behind the text; they read as broken.

It fades now rather than cutting. A shape carries through the reading column at
about a third of its strength and stays whole, which is the difference between
something behind the text and something with a hole in it.

The text still reads. Sampled across the stem rows: 14.8:1 in dark and 10.6:1 in
light, against the 4.5:1 body text needs.

---

## v0.201.23 — The pack marks read in light mode

The marks were drawn at 11 to 34 percent opacity, tuned against a dark ground
where a bright colour at low alpha still glows. In light mode the same alpha of
a dark ink has nothing to glow against and goes grey, so the 80s grid was a
smudge and the circle of fifths was invisible.

They are baked at roughly double strength now and the whole layer is dialled
back to 53 percent in dark mode, which leaves dark exactly where it was and
gives light the full drawing. Thirteen baked opacities boosted, capped at 0.78
so nothing turns into a solid block.

The accent colours themselves needed nothing. Measured on the real screen rather
than on swatches: the pack label, the band rule and the tile keys all sit
between 7.0 and 8.2 against their backgrounds in light mode, because
`MQ_PACK_INK` already swaps a dark ink in and the bright dark-mode colour never
touches the pale surface. A light-mode contrast problem I had spent a while
solving did not exist.

---

## v0.201.22 — Polish pass on the quiz module

Audited the module for the class of fault that caused the last three bugs:
something with higher precedence quietly winning, and animation state left
switched on.

**`will-change` was promoting five elements for the life of every question.** It
tells the browser to give an element its own compositor layer and keep it there,
which is worth doing for the frames that are actually animating and is pure cost
the rest of the time. It is scoped to the transition classes now, and `q-in` is
released once the last tile lands, so the promotion goes with it. Measured: 0
promoted at rest, 5 during the transition, 0 after it settles.

Releasing `q-in` is safe again because `mq2-anim` no longer sits underneath it.
That was the thing that replayed last time. Verified: **0 replays** after the
tiles land.

**Reduced motion is clean.** Rendered the quiz with the preference set and
checked every element on the screen: nothing animating at all.

Two things checked and found correct rather than fixed. The band's colour change
on an answer runs 24 frames and settles at 347ms, in step with the question's
340ms rather than snapping. And the module declares 8 keyframe sets, all
`mq2`-prefixed, with no collisions against the rest of the app.

A note for the next audit: reading `transitionDuration` by looking up
`background-color` returns the wrong entry when the rule declares the
`background` shorthand, because the computed property list keeps the shorthand.
Two of my probes reported a 60ms transition on things that actually take 280.

---

## v0.201.21 — The answers were animating twice

**Reported: the answers wipe in, flash out, and wipe in again.** The tiles still
carried `mq2-anim`, the entrance from the original v2 build. Releasing `q-in`
after 1100ms handed the animation-name back to that class, which then replayed
from the start. Two entrances on the same elements, the second one arriving a
second after the tile had settled.

The transition owns the entrance now, so `mq2-anim` is gone from the tiles and
`q-in` is no longer released on a timer. Verified across 91 frames after the
tiles settle: **zero frames that clip again**.

Releasing it on a timer was also hiding a second fault. `.mq2.q-in .mq2-opt` sets
`opacity: 1`, which outranks the dimming on the two options nobody picked, so
whether the reveal looked right depended on whether the timer had fired yet.
`q-in` is released in `mq2Reveal` instead, which is the moment it stops being
wanted. Measured after answering: 0.3, 1, 0.3, 1.

**And the marks were being scaled to the wrong box.** Most of the SVGs had no
`preserveAspectRatio`, so they defaulted to fitting the width and overflowing a
band that is wider in proportion than the viewBox. The artwork ended up shifted
and clipped, which is the jank in the amp stacks. All ten now map exactly to the
band.

The first question of a round also gets an entrance now. It used to render with
no animation at all, because the path that skips the fade-out skipped the
fade-in with it.

---

## v0.201.20 — Two things the ship gate caught

**`intonare_mq2` was an unclassified storage key.** The backup audit exists to
make sure every persisted key is deliberately either exported or skipped, and
the quiz redesign switch had never been put in either list. It is on the skip
list now, for the same reason as `intonare_dev`: an export carrying it would
turn an unfinished redesign on for whoever restored it. 52 keys and 43
progState fields all classified again.

**The alignment sweep was measuring stale tiles.** `mq2Transition` defers the
render by 190ms, and the sweep measures synchronously, so from the second case
onward it was reading the previous question's grid, and eventually an empty one.
The harness renders through the same immediate path the first question of a
round uses. Seven content cases at three widths, all clean.

Both were mine, both from the transition work, and neither was visible without
running the gate.

---

## v0.201.19 — The question transition, and a mark for each pack

**The transition.** The question fades out on a symmetric curve with a whisper of
scale, the band holds completely still, the question fades back in, and then the
four answers wipe in left to right, 70ms apart. Measured in the app: question
gone at 171ms, back up at 521ms, answers at 671 / 737 / 821 / 887, everything
settled at 887ms, with a **150ms beat between the question landing and the first
tile**. That beat is the whole effect: the question gets a moment on its own
before the options arrive.

The band is anchored on purpose. A container that moves while its contents change
leaves nothing steady to look at, and it was the thing that made the slower
settings feel disjointed. Pack name, difficulty pill, score, beat strip and
motif all hold at full opacity throughout.

**Four bugs on the way in, three of them the same class of mistake.**

An entrance with `animation-fill-mode: both` pins its final keyframe, and an
animation beats a transition in the cascade, so the exit ran against something
holding opacity at 1 and did nothing at all. The question was not fading; it held
solid and vanished when the markup was replaced. The class is released before
the exit now.

Rendering new markup and starting its animation in the same frame means the
browser is laying out when the first keyframe is due, and that frame is dropped.
It renders into a held-invisible state, forces the layout, and starts on the
next frame.

The option tiles carried an inline `animationDelay`, which beats any stylesheet
rule, so the wipe was running on the original entrance's timing and the answers
arrived before the question. Both sets of delays are in CSS now.

And `position: absolute` with `inset: 0` on the motif resolved against the
nearest positioned ancestor rather than the band, so the layer came out 531px
tall against a 180px band and the mask cut the wrong region. `.mq2-band` is the
containing block now, and the mask is measured: the stem occupies 46 to 76
percent of the band, so the mark is cleared from 40 to 82 and lives above and
below it.

**Six marks**, drawn in the pack colour: the 80s perspective grid, the Abbey Road
crossing, the circle of fifths, guitar frets and inlays, a wall of stacks, and
the 70s sunset. Each is the thing its pack is about rather than a texture with a
music theme. Packs without a real association get none.

---

## v0.201.18 — The review screen, which the type pass could not reach

The stats sheet, the daily popup and the loading screen all came out clean on
inspection: zero elements below the floor, because they were built from classes
the type block already covers.

**The miss review did not**, because its card is assembled with inline sizes in
JavaScript, which the stylesheet cannot reach. Fifteen elements below the floor:
the pack label at 7.5px and every answer option at 9px. The label is 11px now
and the options 12px, with the padding and radius opened to suit.

**And it held the last emoji in the module.** The pack label was built as
`pack.emoji + ' ' + packName(pack)`, so the review was the one screen still
using the emoji field as an icon. It draws `mqPackIcon` instead, the same mark
the pack grids use.

The empty state was a hardcoded English string at 10px, "No misses to review."
It is 12px and translated.

Verified with three real misses: zero below the floor, zero emoji, the drawn
icon present in the label.

---

## v0.201.17 — Custom's grid joins the other two, and the hint stops guessing

**The pack hint said "All 8 packs selected" on first paint.** It was the static
markup string with a hardcoded 8, left alone until something else happened to
refresh it. `mqGoCustom` calls `mqUpdatePackHint` now, so it reads the real
count from the moment the screen opens: All 7, against 7 playable packs.

**And Custom's tiles were the third presentation of one component.** The two
picker pages were unified earlier; Custom kept a shorter tile with a 7px
description where the others carry the question count. It takes the same rule
now, measured at 85px against 87 on the pickers, with the same name size, the
same count line and the tick in the corner rather than floating in the row.

That closes the pack grid: one construction, one wording for a pack's size
through `mq2PackCountLabel`, across all three screens that show it.

---

## v0.201.16 — The type floor, and the last emoji standing in for an icon

**49 quiz rules sat below 11px**, the smallest at 7px, against an 11pt platform
minimum. Every one is lifted, grouped by what it is rather than flattened onto a
single value: labels, badges and chips to 11px, and the things that are read
rather than scanned — card descriptions, pack descriptions, the miss review, the
fact block — to 12px. Letter-spacing set for 7px is far too loose at 11, so the
six worst offenders get that corrected too.

Two of them were inline `font-size:8px` in the markup, which beat the stylesheet:
the pack hint and the DESELECT ALL button. Those are fixed at source, so the old
path gets them as well.

Measured across landing, custom, both pickers, the quiz, results and review:
**zero elements below 11px**, from 24 on Custom alone before.

**And the emoji.** A sweep of what actually renders under the flag found one:
`🏆` and `⚡` in front of the personal-best lines on the results screen. They are
gone. The banner is already gold and already says what it is, so they were
decoration standing in for icons.

The rest of the module's emoji are on screens the flag replaces or in the
instrument pickers elsewhere in the app, which are outside this work.

Worth recording for the audit tooling: my first sweep reported six, because it
tested each element's own computed style and not its hidden ancestors. Five were
a `✓` inside the old feedback sheet, which is inert under the flag and never
seen.

---

## v0.201.15 — BACK was unreachable on the landing

The landing was covering the whole panel, top bar included. `position: absolute`
with `inset: 0` resolves against the nearest POSITIONED ancestor, and `#mqBody`
is not positioned, so it anchored to the panel instead and sat over the top bar.
`elementFromPoint` at the BACK button returned `.mq-hero`: the title was on top
of it, so the press went to the hero and nothing happened.

`#mqBody` becomes the containing block. Measured after: the landing starts at
42px rather than 0, BACK and the stats button are both the topmost element at
their own coordinates, pressing BACK closes the modal, and Custom's BACK still
returns to the landing.

Custom had the same fault. It went unnoticed only because Custom hides the top
bar, so there was nothing underneath to block.

---

## v0.201.14 — The landing holds still, the title grows, and the daily joins the hero

**The page you are leaving no longer moves.** It was scaling to 94 percent and
taking a 2px blur while it faded, which pulls the eye back to it at the exact
moment the arriving page is asking for attention. Movement should belong to the
thing entering. It holds its position and only fades: measured mid-takeover,
transform `none`, filter `none`, opacity falling.

**The wordmark was too small.** The clamp was 34 to 60px against a viewport
share of 6.4vh; it is 40 to 70 at 7.6vh. On a 660px frame that is 50px against
42 before, and on 880 it is 67 against 58.

**And the daily chip moves into the hero.** It was absolutely positioned over
the top right of the title, belonging to neither the title nor the mode list,
which is what made it read as something stuck on rather than placed. Centred
under the strapline it becomes the last line of one block, so the top of the
screen reads as a single composition that ends on the thing you can act on, and
the eye runs title, strapline, daily, player, modes without a detour.

It stays a chip rather than becoming a card. The three cards are modes you
configure; the daily is one fixed round. Giving it the same weight as a mode
would say they are the same kind of thing.

Verified at 660 and 880: cards pinned 16px off the bottom, nothing scrolling,
the badge static and in flow.

---

## v0.201.13 — The landing goes bottom weighted

The mode cards are anchored to the foot and the hero takes whatever height is
left over, so the empty space ends up ABOVE the content instead of below it. The
hero can afford to be generous and the three things you tap sit where the thumb
already is.

The hero scales rather than being one fixed size: its padding, its gaps and the
wordmark itself all move with the viewport. Measured in the app with the cards
pinned, 16px clear of the bottom at every height:

| frame | wordmark | scrolls |
|---|---|---|
| 640 | 41px | no |
| 700 | 45px | no |
| 780 | 50px | no |
| 900 | 58px | no |

Against the fixed-height version, which left 286px of dead space at 930 and the
same cards stranded across the middle at every size.

Quick Play takes the larger box and the larger name, because it is the one used
most. Hierarchy by frequency rather than by decoration.

**Three faults on the way in.** `margin-top:auto` cannot push if there is no
slack, and the screen was sizing to its content inside a taller body, so nothing
moved. Filling the body then left the body's own padding behind and the cards
ran edge to edge. And the DAILY badge is absolutely positioned at `top:4px`
inside the hero, which with the hero now starting at the top of a full-height
screen put it straight on top of the stats button.

Nothing was removed: the stats button, the DAILY chip, the Now Playing player
with both transport controls and the wordmark are all where they were.

---

## v0.201.12 — Three sentinel pins so the locked-pack mistake cannot come back

`Object.keys(PACKS)` counts packs that cannot be dealt from, and the same line
written in three places caused three separate bugs: the survival guard let you
deselect every playable pack, the tile counts overstated what a language would
be served, and select-all highlighted coming-soon packs that then dealt nothing.

Rather than a new tool, three pins in the sentinel that already runs on every
build, one per call site. Each asserts the `mqPackReady` filter is present and
names the exact wrong line it replaced, so reintroducing the old code is what
trips it rather than some approximation of it.

Proved by putting the select-all bug back in a scratch copy: the pin reports
DRIFTED and names the site. The real file passes at 250 pins.

---

## v0.201.11 — Select all could pick packs that cannot be played

`mqTogglePack` already refuses to select a coming-soon pack by hand. Select all
went round it: it set the selection to every key in `PACKS`, locked ones
included, so those tiles highlighted, the hint counted them, and the round then
dealt nothing from any of them. The screen was already disagreeing with itself
about it, since the hint said "All 8 packs selected" while the run summary said
7.

Select all now takes only playable packs, and its own on/off test counts
playable packs too, so a full selection still reads as full. The hint counts and
totals the same way, which is why it reads "All 7 packs selected" against 19
packs in the file.

Verified: after select all, 7 selected of 7 playable, **0 locked packs in the
selection**, and the hint, the button label and the run summary all agree.

This is the third instance of one mistake: `Object.keys(PACKS)` counts packs
that cannot be dealt from. It caused the survival guard to let you empty the
selection, the pack counts to overstate, and now this. Worth a sentinel pin so a
new use has to justify itself.

---

## v0.201.10 — The pinned START was not pinned

It landed in the middle of the page with the setting rows continuing below it,
and the reason is worth writing down: **`position: absolute` does not pin inside
a scrolling container.** It anchors to the bottom of the scrollable CONTENT, not
to the viewport, so the footer sat wherever the content happened to end and
everything after it carried on underneath.

The screen is a flex column now. The content is the scrolling child and the
footer is simply the last one, so it cannot move. Verified at the top of the
page and scrolled to the bottom: the footer sits at 725 to 820 in both, flush
with the bottom of the screen, and the last setting row ends above it at 682.

The bottom padding that existed only to clear the floating footer is gone with
it, and the footer takes a hairline top border instead of a gradient fade, since
it is now a real edge rather than something hovering over the content.

---

## v0.201.9 — Custom rebuilt: four rows, a real timer, and scoring that runs the right way

**Four setting rows replace four banks of chips.** Each reads: what it is, what
it is set to, and the control. No section headings and no explanations, because
Custom is the screen you reach by choosing to configure something. Difficulty
reads MEDIUM while its control keeps EASY/MED/HARD; length reads 10 QUESTIONS or
ENDLESS; timer reads OFF or 5/10/15 SECONDS; mode reads NORMAL or SURVIVAL. On
survival the length control greys out rather than lying about a number that will
not be used.

**The timer is a duration now.** It was a boolean pinned to 15 seconds, with the
progress bar computed as `timerVal / 15`. 5 and 10 are real options rather than
labels, and the bar scales to whichever window is running.

**And the scoring ran backwards.** Points were `100 + timerVal * 6`, where
timerVal is the seconds LEFT. An instant answer on a 15 second timer paid 190;
the same answer on a 5 second timer paid 130. Choosing the harder setting paid
less, and adding 5 and 10 would have made that visible. It scores the share of
the window you did not use: full speed is 190 at any duration, half the window
is 145 at any duration, and the shorter windows are simply harder to hit.

**START is pinned** to the bottom with a summary reading `7 packs · MED · 10
questions`, so it does not drift down the page as the grid grows and the run is
described before you commit to it.

The pack tiles carry the question count instead of a 7px description, through
`mq2PackCountLabel`, which is now the single place that decides how a pack's
size is worded across all three grids.

Two faults caught in testing: the pinned footer duplicated the in-flow button,
so the screen briefly had two STARTs, and I wrote CSS for a selection tick that
already existed as `.mq-pack-check`.

**Still below the floor: 24 elements**, worst being BACK at 9px and the COMING
SOON tags at 8.5px. Those are shared components rather than Custom's own, so
they want one pass across the module.

---

## v0.201.8 — Custom was dimming itself on the way in

The rise looked transparent because it was. The drop-back rule was written for
the two overlay pickers, where the active screen is the landing behind the page.
Custom IS the active screen, and it sits inside `#mqBody`, which the same rule
also dims, so the page arriving was being taken to 50 percent opacity and put
through a 2px blur by the effect meant for the thing behind it.

The held-over landing carries the drop-back itself now and Custom never touches
the panel class. Verified mid-rise: Custom at opacity 1 with no filter, the
landing at 0.52.

A second cause underneath it: `min-height: 100%` did not resolve against the
flex-sized body, so the page stopped 129px short of the bottom and the landing
showed underneath as it moved. It fills the body outright now, measured at 880
against 880, and scrolls if the content needs it.

---

## v0.201.7 — Survival loses its all-packs button, Custom joins the page move

**The START SURVIVAL button under the grid is hidden under the flag.** Survival
picks one pack now, so a button meaning "all of them" under the grid was a
second and contradictory way to start the same mode.

**Custom shares the move.** It is a screen rather than an overlay, so it cannot
sit over the landing the way the two pickers do; instead the screen rises while
the landing is held rendered behind it and drops back, and leaving plays it in
reverse. Verified in both directions: entering runs `mq2PageIn` with the landing
held and the panel in its picking state, and 700ms later the hold is released;
leaving runs `mq2PageOut` and lands on the landing with both classes cleared.
The exit hangs off `mqGoLanding`, which is the only route out of Custom, and is
gated so the other screens that call it are unaffected.

**What the audit of Custom found.** Nine distinct type sizes on one screen, and
23 elements below the 11px floor: the pack descriptions at 7px, the section
labels at 8px, the back button at 9px. The pack tiles are 54px against the 87px
tiles on the two picker pages, so `mqPackGrid` is a third presentation of the
grid the other two now share. Every pack is selected by default, which is the
same thing Daniele objected to on Survival, and the hint reads "All 8 packs
selected" while showing one tab of four. And difficulty now appears both here
and in the pack popup.

None of that is fixed yet; it needs decisions rather than edits.

**A false alarm worth recording.** The Questions row looked empty and I nearly
reported it as a bug. It renders from `mqGoCustom`, and my test had called
`mqShowScreen('mqScreenCustom')` directly with only `mqRenderPackGrid`. Opened
through its real entry point it has all four chips. Third time this session that
driving the app from the side has produced a fault that was not there.

---

## v0.201.6 — The survival guard counted the wrong packs, and the pool selection goes

**You could deselect every playable pack.** There was a guard against emptying
the selection, but it counted the whole set, and the default selection is every
key in `PACKS` including the coming-soon ones. Those can never be toggled off,
so once you deselected the last playable pack the set still held four or five
locked ones, the guard saw more than one and let it through. The result was a
screen with nothing highlighted and a pool that could not deal a question. It
counts only selectable packs now: verified that toggling every ready pack off
leaves exactly one standing.

**And the pool selection itself goes, under the flag.** Highlighting every pack
by default asked people to notice a selection they never made, spread across
four tabs most will never open. Survival picks one pack the way Quick Play does,
and everything is the button at the bottom, asked for rather than assumed.

Both pages now share one grid, one page treatment and one popup. Survival's
popup drops the question count, because the mode has no end, and its button
reads START SURVIVAL. The summary line was still promising "10 questions" on an
endless mode; it reads "3 lives, no end" there.

Copy in both languages: the subtitle said "select packs" for a screen that is
now single-pick.

**The pool stays in Custom**, where a multi-pack run is the point of the screen.

The old behaviour is untouched with the flag off: the toggle path is still
wired, and only the guard fix applies to both.

---

## v0.201.5 — Survival becomes the same page, through one helper

Survival had its own bottom sheet and its own pack grid, which made it the last
place carrying a third copy of the component. It inherits the Quick Play page
rather than getting a second design: same takeover, same reverse exit, same BACK
button, same tiles, same locale-aware counts.

**Both pages now open and close through one pair of functions**, `mq2PageOpen`
and `mq2PageClose`, so the two cannot drift apart the way three pack grids did.
`mqShowQuickSheet` and `mqShowSurvivalSheet` are one line each now.

**Two things folded back in while porting.**

The count filter I wrote by hand for the Quick grid already existed as
`mqPackQuestions`, which filters by locale. Both grids and the popup use the
helper now instead of three spellings of the same rule.

Survival's tile carried a 7.5px "90Q" badge floated to the right, below the 11px
floor and saying less than the words do. It reads "90 questions" on a second
line, matching Quick, with the same `+` for generator packs and "endless,
generated" for a pack with no authored questions.

Verified: two columns, 87px tiles, BACK present, the entry keyframe running, no
overflow on the start button, and Quick Play still opening and closing correctly
through the shared helper.

---

## v0.201.4 — Going back plays the move backwards

The page slid up on the way in and then vanished on the way out, so the landing
arrived from nowhere. BACK now runs the same move in reverse: the page slides
down over 340ms on a curve that starts slower and ends faster, which is the
right shape for a dismissal, while the landing comes forward at the same time
rather than waiting for the page to finish.

Verified mid-flight: the exit keyframe is running, the landing is part-way back
through its scale, and the panel has already dropped its picking class so the two
halves of the move happen together. Verified settled: both classes cleared, and
the page reopens cleanly afterwards.

Under `prefers-reduced-motion` it closes immediately, with no timer.

---

## v0.201.3 — The pack counts were wrong in both directions, and the ALL PACKS button overflowed

**No crossover.** Checked every question in every pack for text appearing in more
than one: zero. That part was clean.

**But the number was `pack.questions.length`, which is wrong twice over.**

The decades packs tag questions by locale. The Seventies holds 113, of which an
English player can be served **92** and an Italian **91**: the tile was promising
twenty-one questions the reader's language would never show them. The count is
filtered by the current language now, on the tile and in the popup, and it moves
when the language does.

A generator pack's authored total is a floor rather than a total, because the
round adds generated questions on top of it. Those read `60+`, `104+`.

Measured after, English then Italian: Theory 60+, Guitar 104+, Bass 104+, Guitar
Gods 90, Beatles 90, The 70s **92 in English and 91 in Italian**, and Advanced
Theory keeps "endless, generated" since it has no authored questions at all.

**The ALL PACKS button ran 15px past the sheet.** It resolves to `width: 412px`
and the 15px margins I added in the rework were applied on top of that, so it
was 442px wide in a 412px sheet. Auto width lets the margins do their job.
Measured at 23px of clearance now.

---

## v0.201.2 — Three faults in the Quick Play rework, one of them a trap

Found on device.

**There was no way back.** The old sheet was dismissed by tapping the area
outside it. Turned into a full page there is no outside, so the only control on
the screen was ALL PACKS and the only exit was leaving the quiz. A BACK button
sits above the title now, and it restores the landing: verified that the sheet
closes, the panel drops its picking class and the landing returns to full
opacity.

**The animation never played.** The sheet had no transition of its own beyond
`background 0.06s`, so the opaque page appeared instantly and covered the
landing before the landing could be seen dropping back. It uses a keyframe
rather than a transition, because the overlay starts from `display:none` and a
transition will not run from there.

**The tile was half empty.** 96px tall holding one line of text, bottom aligned.
It carries the question count as a second line now, the way the mockup did, and
comes down to 87px, which is the height the content needs.

That last fix exposed a fourth: a generator-only pack has no authored questions
to count, so its tile came out blank beside a counted neighbour and read as a
fault. Those say "endless, generated" instead.

---

## v0.201.1 — Quick Play takes the page, and difficulty moves to where it applies

Three changes, all behind the flag. The landing keeps its shape.

**The difficulty chips leave the landing.** Difficulty is a property of a run,
and it was being set on a screen two steps away from where it took effect, then
offered again inside Custom: one setting, two controls, neither next to the run
it governed. It now lives in the pack popup, above the question count, with the
meanings Custom already carried: Familiar, Some digging, Deep cuts. A summary
line under PLAY reads back the whole decision.

**The Quick Play sheet becomes the page.** The landing drops back, dims and
blurs behind it over 420ms rather than being covered, so it reads as a layer you
will come straight back from rather than as a new place. The panel carries the
state, so every route in and out goes through one class.

**The pack grid becomes tiles** in the same language as the answer grid: two
columns, same radius, same padding, the icon and name reading down the tile.

Two faults found while porting, both in my own new code. The tile drew a badge
box in the corner for an icon that renders inline with the name, so every tile
carried an empty square. And difficulty landed below the question count when it
is the larger of the two decisions and the one that just moved there.

Survival still has its own sheet and its own pack grid. That is the next one,
and it should get the same treatment rather than a second design.

---

## v0.201.0 — Slice 2: the feedback comes out of the drawer

The bottom sheet is gone. The blurb sits in the flow under the answers, so the
question, the answer you gave, the one that was right and the blurb are all on
screen together. A sheet covers the thing it is talking about and reads as
transient; the blurb is what the pack work is for.

**Three things are cut, because the reveal already said them.** By the time the
feedback opens, the band has gone green or red, the tick is on the right answer
and the beat has filled. So the verdict word was the fourth way of saying it, the
"DID YOU KNOW" label was announcing something that no longer needed announcing,
and "The correct answer was" was restating what the tick already marks.

What replaces the verdict is the points: **an italic "Did you know?" on the left,
`+150` with a multiplier pill on the right.** The number counts up rather than
appearing.

**The XP toast is suppressed under the flag.** It was saying what the block now
says and landing on the answers while doing it. The milestone moves into the
head as a chip, so a five-in-a-row round reads `+150  x1.5  5 STREAK` on one
line. `hapticMilestone` and `playCueMilestone` are untouched, so the milestone
still has a felt moment.

**Colour is one event, disclosure is a sequence.** Every state colour now moves
on a single 280ms beat: the band, the tile borders and backgrounds, the dim on
the two you did not pick, the answer keys and the beat strip. They were at 450,
150, 200, 300 and instant, which is five things starting together and finishing
at five different moments. The reveal stays deliberately staggered on top of it:
the rule draws, the label and points fade in behind it, the blurb lifts, and
NEXT arrives last so it does not invite a skip before the blurb is readable.

One i18n key, both languages: `mq_did_you_know_q`.

---

## v0.200.2 — The record ending stops saying it twice, and the gold stops being mud

Three faults on the survival record screen, all found on device.

**Yellow does not survive being mixed into a dark navy.** Green and red stay
recognisable at a 40 and 24 percent mix; `--metro` at 34 percent came out khaki,
so the most rewarding screen in the module read as dirt. The band carries 15
percent now and the gold lives in the headline and the rule, which is where it
reads as gold.

**`--metro` in light mode is `#503600`, a dark brown**, so the reward button was
mud there too. Light gets a real gold, `#f0b429` with `#3a2a00` text, at 7.5:1.
Dark is `#ffd166` on `#1a1206` at 12.9:1. Same shape in both, rather than one
being the other's opposite.

**And the screen said the same thing twice.** The headline reads NEW RECORD and
the banner underneath read "New survival best". The banner drops that line when
the headline already carries it, and hides entirely when nothing else is left in
it, which on a plain record run is the usual case. That takes two lines off the
screen.

---

## v0.200.1 — Survival gets a third ending, and light mode stops diluting dark ink

**Beating your own survival record now ends the run differently.** It used to
read GAME OVER with a line in the personal-best banner underneath, which is the
wrong way round in the one mode whose entire point is your own record. There are
three endings now:

- **NEW RECORD**, gold band, with how far past your best you got
- **GAME OVER**, muted red, with how far short you fell
- **CLEARED**, green, for surviving the whole pack with lives left

On a first run there is no number to beat, so it reads "your first survival run,
that is the mark to beat" instead of a comparison against zero.

**A real bug came out of building it, and it predates the redesign.**
`mqShowResults` calls `mqCommitSessionStats()` before anything reads the stats,
so every later `mqGetStats()` already includes the run being reported. The
record check compared 31 against 31. **The old screen's "New survival best" and
"New streak record" banners have the same fault and could never have fired.**
The snapshot is taken before the commit now and both paths read it.

**Light mode bands were dark ink diluted into white.** `color-mix(--in-tune 40%,
--surface)` takes #224700, a dark green, and thins it, which gives sage; the
same treatment gave the failing state a dusty pink. Light mode has its own pale
washes with a saturated ink for the rule, so the band reads as tinted paper
rather than thinned paint: #d9ecd3, #f7e7ce, #f4dcd7, #fbeec2.

The primary button on a good result was dark green text on dark green. It is
light text on dark green now.

---

## v0.200.0 — Slice 3: one results screen for every ending

The module had two results screens that shared no visual language, plus a third
for a cleared pack. Behind the flag they are one.

A normal round, survival, the daily and a cleared pack all render into one
block. The band is the same object as the question screen, neutral until the
outcome colours it, and the record under it is the same beats the player watched
fill. That replaces three notations for one fact: the bars on the old results
screen, the emoji grid on the daily, and nothing at all on the pack-clear
screen. Everything leads with correct out of total; points are off the headline.

**The round replays on arrival.** The beats land in the order they were answered
and the headline counts up underneath, timed to finish together. It is the one
thing that happens here and nowhere else, which is what makes it read as an
arrival rather than another question screen.

Survival keeps its own headline, because it is not graded on accuracy: 27
CORRECT and GAME OVER rather than a percentage band. The breakdown only appears
with more than one pack, since on a single pack it is one full-width row
repeating the header. The daily keeps its share button and swaps PLAY AGAIN for
DONE.

Four new i18n keys, both languages: `mq_pack_cleared`, `mq_every_q_answered`,
`mq_pb_survival`, `mq_pb_streak`.

**Four faults on the way in, each found by measuring rather than looking.**

The two hide-siblings rules both matched any `.mq-screen.v2`, so on the results
screen one hid everything that was not `.mq2` and the other hid everything that
was not `.mq2r`. Between them they hid the lot. Each is scoped to its own screen
now.

The new block was inserted BETWEEN two screens, so it is a sibling of them
rather than a child of the results screen, and the parentage selector never
matched. The rules address it as a sibling.

`.mq-panel` does not exist; the element is `#mqPanel`. That selector matched
nothing at all.

And the one worth remembering: **the module's screens are split across two
containers.** The landing, setup and quiz screens live inside `#mqBody`, while
the results, win, daily and review screens are direct children of `#mqPanel`.
Hiding `#mqBody` therefore did nothing to the results screen, which is 860px
tall and pushed the new block off the bottom of the panel. Both containers are
hidden now.

---

## v0.199.15 — Light mode on the quiz screens that are staying

A contrast audit of all seven quiz screens in light mode, then fixes only where
the screen survives the redesign.

The panel behind the landing and setup screens composites to rgb(143,174,220), a
mid periwinkle, and two shared tokens fail on it: `--accent-soft` (#5238a5) at
3.75:1 and `--accent-warm` (#b34a18) at 2.37:1. Both are used for the first
things you read. Darker members of the same hue, chosen by measuring against
that exact background: **#3a2578 at 5.39:1** and **#6b2909 at 4.76:1**.

Fixed: the MUSIC QUIZ wordmark gradient, the INTONARE pill, the mode card names
and badges, the XP toast, the selected question-count chip, the selected global
difficulty chip, the difficulty names on the setup chips, the DAILY badge, and
the medium pill on the new quiz screen, which was sitting at 4.45 and needed a
nudge rather than a rescue.

Every override is scoped to the quiz. The global tokens are shared with every
other tool and are not touched.

| screen | before | after |
|---|---|---|
| landing | 6 | **0** |
| custom | 3 | **0** |
| quiz (v2) | 2 | **0** |
| review | 1 | **0** |
| results | 3 | 2 |
| cleared | 3 | 2 |
| daily | 4 | 3 |
| **total** | **22** | **7** |

The seven left are all on the results, cleared and daily screens, which slice 3
replaces. Painting them now means painting screens that are about to be deleted,
so they stay on the list instead. The numbers to beat when those are rebuilt:
`mq-res-btn` at 3.75, `mq-stat-val` at 4.45, the daily label at 2.37 and the
daily's big score at 2.37 against a 3.0 threshold.

A coherence note that matters more than any single number: the module currently
holds three visual languages. The new quiz screen is flat band and ink rule. The
results and cleared screens are rings, trophy emoji and gradient text. The
landing is a third, a large gradient wordmark over glass cards. In dark that
reads as variety; in light it reads as unfinished, because the old screens lean
on glow and gradient and neither survives a pale ground.

---

## v0.199.14 — Pack colours become theme-aware everywhere, and the light-mode audit that should have run first

Daniele asked whether the whole quiz was checked for light mode. It was not.
v0.199.13 fixed one screen and left the pattern open, which was said at the time
and should not have been left there.

**Ten places write a pack colour into an inline style**: the stats rows, the pack
icons, the survival grid, the sheet grid, the quiz category badge, the results
breakdown, the miss review, the daily popup and the question-count chips. Every
one wrote the DARK colour whatever the theme was.

All ten now ask for `var(--pk-<pack>)`. The two tables are published as one
custom property per pack, defined for both grounds, so the browser picks. Every
use is a plain CSS value (background, color, border-color, `color-mix`,
`linear-gradient`), all of which take a variable, and the side effect is that a
theme switch now recolours the module live instead of waiting for a re-render.
Raw `MQ_PACK_COLORS[...]` reads are down to the table's own definition.

**And the audit that should have come first is now a tool.**
`intonare_mq_light_audit.py` walks every visible text element on all seven quiz
screens in light mode and reports foreground against composited background,
against the WCAG AA thresholds. It composites translucent layers rather than
returning the first one it finds, which the first version got wrong: a chip with
a 7 percent tint over a card was being compared against its own tint and scoring
1.0.

**121 text elements checked, 22 below AA.** They collapse to eight classes:
`mq-xp-toast`, `mq-hero-pill`, `mq-card-name`, `mq-card-badge`, `mq-chip-val`,
`mq-res-btn`, `mq-gd-chip` and `mq-diff-name`, plus `mq-stat-val` and `mq2-diff`
sitting marginally under at 4.45. The worst are at 2.37. **These are not fixed.**
Most of them are on screens the redesign is going to replace, and guessing at
them would mean touching a light palette the whole app shares. The numbers are
in the tool; the call is Daniele's.

---

## v0.199.13 — The quiz gets a real light palette instead of dimmed dark colours

Daniele: the light mode schemes never look good, and does the quiz even match
the rest of the app? No, and the numbers say so plainly.

**The app has 783 `body.light` overrides.** The tuner has 30, the metronome 39,
the piano 31, exercises 34, PTO 41. **The Music Quiz has 8.** It is the least
adapted tool in the app for light mode, and it shows.

**And every light-mode pack colour was a dark-mode colour muddied down.**
`MQ_PACK_COLORS` is nineteen brights chosen for a dark ground, with no light
counterpart, so the redesign had been mixing them toward navy to stop them
glowing. That is compensation, not design, which is exactly why it came out
muddy. Measured: those nineteen colours sit at 1.3:1 to 3.4:1 against the light
surface. Most of them fail plain legibility before anything aesthetic is
considered.

The app's own light system is not dimmed brights, it is deep saturated ink on
pale ground. Its most used light values are #004a60, #5238a5, #095c3a, #8f2344,
#8f2215 and #664700.

**`MQ_PACK_INK` gives every pack a real light colour** in the same hue family,
drawn from that palette. All nineteen sit between 6.5:1 and 8.5:1 on the light
surface, against 1.3 to 3.4 before. It is used for the band rule, the pack name,
the answer keys and the streak ramp, and the ramp's top two tiers warm through
#8a3d0b and #b8430c rather than through `--metro`, which is a dark brown in
light mode.

The glows stay off in light. A coloured shadow on a pale ground is a smudge.

---

## v0.199.12 — The streak tiers, rebuilt for light mode

Daniele: the ember is dark in light mode and feels weird. Two reasons, both
mine.

**A glow is a light-on-dark idea.** A coloured box-shadow on a near-white
surface reads as a smudge, not as heat. The glows come off in light mode
entirely, and height plus colour carry the tiers on their own.

**`--metro` in light mode is `#7a5200`**, a dark brown. The top tier was being
painted with it, so the hottest state in the app came out as the deadest colour
on the screen. Light mode warms through `--accent-warm` instead, which is a
burnt orange built to sit on a pale ground.

Two faults came out of fixing it, both found by measuring rather than looking.

Tier 3 was mixed toward black and came out DARKER than tier 4, so the ramp ran
backwards at the top. The ramp is built off one variable now and the tiers
cannot cross.

Tiers 1 and 2 came out **identical** in light mode. In dark they differ only by
the halo, so removing the halo removed the difference. Light mode gives each
tier its own colour and escalates through hue and saturation rather than
brightness, which is what works on a pale ground: purple, deeper purple, red,
orange. Measured separation between steps is 59, 119 and 37 in RGB distance,
against 0, 96 and 79 in dark, where the first step was carrying no colour
difference at all.

Contrast against the band, light mode: 3.4, 6.4, 5.6, 4.1. The pack colours are
chosen for a dark ground and go pale on white, so the lower tiers are mixed down
before they are used.

---

## v0.199.11 — The slot on deck, and the empty beats made visible

**The question you are answering now is cut to the tier it would reach, and left
hollow.** A streak visibly reserves its next place before you have earned it: on
a run of four the empty slot is already standing at the height of five, waiting.
Get it right and it fills; get it wrong and everything settles flat. Verified
across six states, and the band stays at 157px through all of them.

| run | live beats | slot on deck |
|---|---|---|
| nothing | none | 5px, plain |
| 2 | none | 8px hollow |
| 4 | 4 at 8px | 10px hollow |
| 9 | 9 at 10px | 12px hollow |
| 19 | 19 at 12px | 13px hollow |
| after a miss | none | 5px, plain |

The slot breathes on a 2.4 second cycle, so a waiting slot reads as waiting
rather than as an empty one. It is off under `prefers-reduced-motion`.

**The unanswered beats were invisible.** They were `--surface-2` sitting on
`--surface`, which is almost no contrast, so the row stopped saying how many
questions were left as soon as you looked at it on a real screen. They are
`--text-dim` at 22 percent now.

Three further animations are built but NOT shipped: a landing pop on a newly
answered beat, a ripple that runs along the streak when it crosses a tier, and a
cascade that collapses a broken run right to left instead of dropping it all at
once. They are in the mockup with individual toggles, because that is a judgement
best made with a thumb.

---

## v0.199.10 — The streak rises out of the bar, and only while you hold it

The joined-run bar is out. Merging the beats read as one long shape rather than
a run of separate answers, which is not what a record is.

**The live run rises.** Consecutive right answers grow out of the row and take
colour, on the same tiers as the score multiplier, so what rises and what pays
change on the same question: 8px at three, 10px and a halo at five, 12px and
warming at ten, 13px and amber at twenty.

**Only the LIVE run.** A run that has already been broken drops back to plain
ink. A coloured run you no longer hold is the bar claiming something untrue, and
it also meant a bar full of old colour said nothing about how you are playing
now. Get one wrong and everything settles back to a flat row of marks; start
again and only the new run lifts.

**Nothing else moves.** The row reserves its tallest height, so a streak growing
from nothing to twenty and dying again leaves the band at exactly 187px
throughout. Verified across seven states.

The rise uses the spring curve, which is the one place a spring is allowed on
this screen besides the right answer, and it is the same gesture: something
arriving rather than something changing.

---

## v0.199.9 — Points multiply with the streak; XP does not

The streak used to pay a flat bonus: 100 points, or 120 from three in a row, and
nothing more after that. A streak of 3, 5, 10 and 20 all paid 120, so the
milestones announced themselves with a haptic and a cue and were worth nothing.

Points now multiply, on the same tiers `hapticMilestone` already fires on, so
the thing you feel and the thing you are paid change on the same question:

| streak | multiplier | points |
|---|---|---|
| 0-2 | 1 | 100 |
| 3-4 | 1.2 | 120 |
| 5-9 | 1.5 | 150 |
| 10-19 | 2 | 200 |
| 20+ | 3 | 300 |

**XP is untouched**, deliberately: 10, or 15 from three in a row. Points are the
round's own currency and can swing; XP is the long-term progression and should
not be distorted by one hot round.

The multiplier applies to the timed score too, which is `100 + timerVal * 6`,
so answering fast and holding a streak compound rather than one replacing the
other.

The toast leads with the points now instead of the XP, because points are the
number that changed: "+150  fire  x1.5  5 STREAK". Under a multiplier of 1 it
still reads "+10 XP".

Verified end to end over a 22 question run: 100 at streak 1, 120 at 3, 150 at 5,
200 at 10, 300 at 20, with XP climbing 10 then 15 a question throughout.

---

## v0.199.8 — The toast was firing under the fold, and the bar now shows the streak

**The streak toast was invisible, and it was my fault.** When the screen was
ported I moved the toast to `bottom: 96px` to stop it landing on the question.
It is `position: fixed`, so the bottom of the viewport is exactly where there is
least screen, and it was firing below the fold. The band's height cannot be
known in CSS, because it changes with the stem length and with whether the
question carries a diagram, so it is measured now and the toast is placed ten
pixels under the band. Checked at 915px and at 620px: on screen in both.

**Runs join in the bar.** Consecutive right answers lose the gap between them
and square off their inner corners, so a streak reads as one long bar instead of
three separate marks. From three in a row the run takes the pack colour. That
gives the streak a permanent home in the thing that was already on screen, which
is the job the removed pill was doing.

**Survival gets a moving window.** It used to grow one segment per question
without limit, so every segment was thinner than it had been on the question
before and the bar was a different shape each time you looked at it. It grows to
twenty and then holds, keeping the most recent twenty. Verified: an eight
question run draws ten segments, a thirty question run draws twenty.

Still open, and it needs a decision rather than a fix: **the streak pays a flat
bonus, not a building one.** `mqAnswer` gives 100 points and 10 XP, or 120 and
15 from three in a row, and it stops there. A streak of 3, 5, 10 and 20 all pay
120. The milestones fire `hapticMilestone` and `playCueMilestone` and change the
toast, but they are worth nothing extra.

---

## v0.199.7 — The streak pill goes, the difficulty sits on the centre line

**The streak pill is gone from the header.** The beats under the question
already show the run, so the pill was saying the same thing twice and taking the
room that made the header overflow in the first place. Nothing else changed
about streaks: `mqAnswer` still counts them, still pays 120 points and 15 XP from
three in a row, still fires `hapticMilestone` and `playCueMilestone` at 3, 5, 10
and 20, and still throws the toast. The signal moved from a permanent readout to
the moment it happens, which is when it means something.

**The top row is a three-column grid now**, so the difficulty pill sits on the
exact centre line whatever the two sides weigh. Measured at 0px offset from
centre at 360 and 412, with a five-figure score and the Italian DIFFICILE label.
Header overflow is gone with it, so the narrow-screen workaround the pill needed
came out too.

Removal was checked by count rather than by eye: `mq2Streak`, `mq2-streak`,
`mq2-goal`, `mq2-track`, `MQ2_TIERS` and `mq2-right` are all at zero
occurrences. The alignment sweep is still clean, seven cases at three widths.

---

## v0.199.6 — The round's difficulty, colour-coded, in the header

Daniele asked for the chosen difficulty where the pack name used to sit. It is a
small pill in the top row, and it uses the three colours the difficulty chips on
the hub already use rather than inventing new ones: easy is in-tune green,
medium is accent-warm, hard is sharp red. Both languages, both themes:

| | dark | light |
|---|---|---|
| EASY / FACILE | `#b6f25b` | `#224700` |
| MED / MEDIO | `#ffa07a` | `#b34a18` |
| HARD / DIFFICILE | `#ff5252` | `#6e1810` |

**Adding it overflowed the header, which the measurement caught.** Four items in
one row is too many for a 360px phone once the Italian label meets a streak pill
and a five-figure score: the score ran 15px past the band edge. Under 400px the
streak's target number is dropped and the gaps tighten. The target is the least
load-bearing thing in that row, because the bar beside it already shows how
close the milestone is. Worst case now clears the edge by 18px at every width.

A note on the first test run of this, because it wasted a round: it reported the
pill as green for all three difficulties and the Italian labels as English. Both
were the test being wrong. It set `localStorage.intonare_lang`, which is not
where the language lives (`progState.lang` is), and it read the colour before
the theme class had been applied. The code was correct the whole time.

---

## v0.199.5 — Two alignment faults found by measuring instead of looking

Daniele asked for a thorough check, so this was done by reading bounding boxes
rather than by eye: seven content cases at 360, 384 and 412 CSS pixels, checking
edges, first-line positions, key positions, tile heights and text overflow.

**Answers in a row did not line up when one of them wrapped.** The text was
centred in its tile, which looks right until one answer in a row takes two lines
and the other takes one. At 360px "Diminished triad" wraps and its first line
then sat 10px above the one-line answer beside it. It is top-aligned now, so the
first line of every answer in a row starts on the same pixel whatever the wrap.
This only appeared at 360 and 384; at 412 nothing wrapped, which is why looking
at the wide preview never showed it.

**The pack name truncated to "THEORY ..." whenever the streak pill appeared.**
It shared the top row with QUIT, the pill and the score, and there was not room
for four things. It has its own line under the header now, centred, and the stem
margin came down to pay for the height.

The sweep is clean at all three widths for: one-word answers, a mixed set where
one answer wraps, four long answers, the longest option set in the library, a
long stem, a two-digit streak, and survival mode.

---

## v0.199.4 — One layout for the answers, always

The quiz screen used two layouts: a grid when every answer was short, a list
when any answer was long. Daniele read the switch as a bug, and he is right.
Two shapes for the same control look like something went wrong, not like a
rule.

**The grid is now the only layout. The text scales instead.** Measured over
every option set in the shipped packs, including the eighties draft: the longest
answer in the whole library is 65 characters, and it is Italian, which runs
longer than the English throughout. 65 characters is three lines at 11px in a
half-width tile, so there is room.

| longest answer | size | share of questions |
|---|---|---|
| up to 20 chars | 15px | 61% |
| up to 28 | 13.5px | 78% |
| up to 40 | 12px | 93% |
| over 40 | 11px | 7% |

11px is the floor and it is only reached by 7 percent of questions. Nothing
overflows its tile at any step, checked against the three worst cases in the
library.

The cost is honest: a long answer is smaller in a tile than it would be across
the full width. The gain is that the answers are the same shape on every
question, which is what a control should be.

---

## v0.199.3 — Two alignment faults in the new quiz screen

Both found by Daniele on device, both real.

**The pack name moved between questions.** The top row was `space-between` with
three children, so the label's position depended on how wide the right-hand
group happened to be. At streak 0 there is no streak pill, and the label sat
near the centre. At streak 3 the pill appeared, and the same label jumped left
and truncated. QUIT and the pack name are one left group now and the rest is
pushed right, so the label starts at the same place every time. Measured at
x=91 in both states.

**A one-word answer floated in the tile.** The tile put the key at the top and
the answer at the bottom with `space-between`, which reads fine for two lines of
text and looks broken for "ii" or "One": a letter, a large hole, then two
characters. The key is out of flow now, pinned to the corner, so the answer
centres in the whole tile rather than in what is left underneath the key.
Measured: the text centre and the tile centre are the same pixel for both a
one-word answer and a two-line one, with 15px of clearance under the key.

A note on the layout question this came from, because it reads as a rule and is
not one: the grid is chosen by ANSWER LENGTH, not by question type. Four answers
of twenty characters or fewer get the grid; anything longer gets the list. A
notation question with long answers gets the list, and a written question with
short answers gets the grid.

---

## v0.199.2 — A way to reach the switch without a code

The quiz redesign switch was in the app Settings, under the developer tools. The
developer tools only appear after you enter the developer code. That is two
gates in front of a preview switch, and Daniele hit both.

**Press and hold the version number in Settings for one second.** That toggles
the redesign and reloads. It needs no code and no console. A short tap does
nothing, so it cannot fire by accident. Tested both ways: a 1000ms hold flips
the flag and writes the key, a 150ms tap leaves it alone.

The Settings button stays for anyone already in developer mode. It shows the
current state, so you can read the mode without turning anything on.

---

## v0.199.1 — The redesign was drawing underneath the old screen, and you could not turn it on

Two faults, both mine, both found on the first device run.

**The v2 block was visible with the flag off.** `.mq2` carried `display: flex`
unconditionally, so the new band rendered underneath the old question screen
whether the switch was on or not: an empty QUIT row and a score of 0 sitting
below the answers. It is `display: none` by default now and only becomes a flex
column under `.mq-screen.v2`.

The reason the automated check missed it is worth writing down. The flag-off
test asserted that the OLD answer wrapper was still visible and that there were
zero v2 buttons. Both were true. It never asserted that the v2 ROOT was hidden,
which is the thing that was wrong. The test now reads the computed display and
the bounding box of `#mq2Root` in both states: off gives `none` and 0x0, on
gives `flex` and 408x459, with the old wrapper going to `none`.

**And the switch was not reachable.** It read `localStorage` only, and there is
no console on a Capacitor build, so a localStorage-only switch is the same as no
switch. There is a button in Settings now, under the other developer tools, that
reads "Quiz redesign: ON/OFF" and reloads. It is only rendered while developer
mode is on, so a normal user never sees it.

---

## v0.199.0 — The quiz redesign lands behind a switch

Slice 1 of 3: the question screen. Turn it on with
`localStorage.setItem('intonare_mq2','1')` and reload; `removeItem` puts it back.
Off by default, so a half-ported screen never reaches a tester.

**Nothing in the old path was rewritten.** The v2 elements live inside
`mqScreenQuiz` with their own ids and are hidden unless the screen carries `.v2`.
`mqRenderQ` and `mqAnswer` keep every line they had, and a single call is
appended to the end of each. So with the flag off, the two functions behave
exactly as before and the flag is a real off switch rather than a branch that
has to be trusted. Verified both ways in the live app: flag off gives no `.v2`
class, zero v2 buttons and a visible original answer wrapper; flag on gives four
v2 tiles, a hidden original wrapper, and no console errors either way.

**What the screen does now.**

Six type sizes with an 11px floor. The module has 21 classes below that floor,
the smallest at 7px, against Apple's HIG minimum of 11pt.

Neutral at rest. The band is plain surface with the pack colour reduced to a
rule underneath, so answering is the only colour event on the screen. A right
answer fills the band; a wrong one mutes it rather than flooding it, because a
full red wash over a third of the screen was louder than the mistake.

Answer keys are lettered, and the reveal swaps the letter for a tick or a cross.
WCAG 1.4.1 is Level A: colour must not be the only visual means of conveying
information, and roughly one in twelve men has some colour vision deficiency. The
right answer is legible with no colour perception at all.

The grid adapts. Measured across 1,208 question and language pairs in the real
packs, the median option is 14 characters, the 90th percentile 31 and the longest
65, and only 32.5 percent of questions have all four options short enough for a
tile. A fixed two-by-two would truncate two thirds of the material, so four short
options get tiles and anything longer gets a single column.

The streak pill shows the count, a bar, and the next milestone. The quiz already
escalates at 3, 5, 10 and 20 with `hapticMilestone`, so the bar fills toward
whichever of those is next instead of only counting up. It hides under 2, the
way the old chip already did.

Under the band is the record: one beat per question, solid for a hit, hollow for
a miss, pack colour on the one you are answering. It replaces the progress bar,
and in slice 3 it becomes what the results screen ends on, which is where the
module currently has three different notations for the same fact.

Motion is ease-out at 150 to 340ms, since past 400 feels slow and under 100 goes
unnoticed. There is exactly one spring, on the right answer, because overshoot
reads as instability when it is spent on routine actions. A 260ms beat sits
between the tap and the reveal.

**Two faults found on the first render and fixed.** The pack label carried the
question counter and truncated to "THE BEATLES · 4…" once the streak pill sat
beside it; the beats already are the counter, so the label is just the pack now.
And the XP toast is pinned 70px from the top, which used to clear the old
progress bar and now landed on the question, so under v2 it comes up from the
bottom instead.

Slice 2 is the reveal sheet, which still uses the old bottom sheet. Slice 3 is
the unified results screen.

---

## v0.198.3 — Two Daniele found on device: a Daily with no staff on it, and alto clef on medium

**A Daily on a generator pack served zero generated questions.** Theory
Fundamentals is a generator pack whose whole identity is reading a staff, and
its Daily was authored questions only, so it did not look like the pack it
claimed to be. `mqBuildDailyQuestions` built its pool straight from
`pack.questions` and never called `mqGenBatch`.

The reason it never did is real rather than an oversight: the generators run on
`Math.random`, and a Daily has to come out the same on a resume and the same for
everybody. So the batch now runs with `Math.random` swapped for today's seeded
stream and put back afterwards, which makes the generated questions exactly as
deterministic as the shuffle already was. Measured: a Theory Daily is 7 authored
and 3 generated, identical across repeated builds, and `Math.random` is its own
self again on the way out.

**Alto and tenor clefs on medium, and there were two separate causes.**

The defect first. `mqGenInversion` called `mqPickClef(3)` with the tier
hardcoded, so inversions rolled for an advanced clef whatever their difficulty.
Over 5,000 generated questions, inversions came out **28.1 percent alto or
tenor** while every other generator sat between 2.4 and 11.4. It takes the
question's own tier now.

Then the judgement. Alto and tenor were gated on the QUESTION's tier, and a
medium round is 40/40/20, so a fifth of it is tier 3 and the two clefs a player
is least likely to read arrived in a round they never asked for. ABRSM sets alto
at Grade 4 and tenor at Grade 5, which is not medium. They are gated on the
ROUND now, so picking hard is what puts them on screen.

Measured after, 4,000 generated questions per difficulty:

| round | alto | tenor | bass | treble |
|---|---|---|---|---|
| easy | 0 | 0 | 45% | 42% |
| medium | 0 | 0 | 45% | 46% |
| hard | 9.2% | 9.1% | 37% | 36% |

---

## v0.198.2 — Every game mode now ends the same way

Daniele suspected the Daily was missing its ending. It was, and so was the
pack-clear screen, and the cause was one `return`.

`mqShowResults` handed the Daily off on its second line, **before** it reached
`mqAmbStop()` and the stinger a few lines below. So finishing a Daily left the
background music still playing underneath a result screen that made no sound at
all. `mqShowWin`, the screen you get for clearing an entire pack, never called
either one: the rarest thing in the module was the only ending with nothing
attached to it.

**One closing sequence now, shared by all of them.** `mqEndRound()` stops the
music, resyncs the Now Playing widget, and fires the sting and its haptic after
the fade has cleared. Quick Play, Custom, Survival, the Daily and the pack-clear
screen all call it. They used to do three different things and two of them did
nothing.

**The ending is graded, the way the streak already was.** In-quiz celebration
has been rationed properly since the streak tiers went in: 3, 5, 10 and 20 each
get their own emoji and `hapticMilestone` instead of `hapticCorrect`. The
endings had no such thing. A single `won` boolean at 50 percent meant 10 out of
10 and 6 out of 10 made exactly the same sound. There are three grades now:
a clean sweep, a pass, and a miss. `mqStingWin` takes a flag that adds the
triad again an octave up after the chord lands, so a perfect round and a
cleared pack arrive on something a 6 out of 10 does not get.

**Reviewing your misses works everywhere.** It was on the normal results screen
only, though `MQ.misses` is filled on every mode. It is on the Daily and the
pack-clear screen now, and the BACK button on the review screen knows which of
the three sent it there.

There is no pack breakdown on the Daily and that is deliberate: the Daily is a
single pack, so the bar chart would be one full-width row repeating what the
header already says.

One correction to the audit that produced this. The first pass reported that
the Daily skipped `mqCommitSessionStats` and `mqClearInProgress` as well. It
does not; both run before the early return. That finding came from reading the
body of `mqShowDailyResult` instead of the path into it, which is the same
mistake as grepping for a function name and reporting the absence of what you
failed to find.

---

## v0.198.1 — The six open findings, and a subject cap that was counting ordinary words

The findings left open in v0.198.0 are closed, and the pack audit turned up two
more of the same kind once it was run over all six packs rather than the two
that had just been rewritten.

**Two answers repeated a word from their own stem and no distractor did.**
Theory 37 asked what it means to *accordare al diapason* and answered *il
riferimento comune su cui accordano tutti*; the English did the same thing with
"tune" and "tunes to". The answer now reads "The reference the whole group
shares" and "Il riferimento comune di tutto il gruppo". Guitar Gods 33 asked
how a talk box shapes words out of the sound and was the only option saying
"sound", so it now runs from a small speaker instead. Both are shorter than
what they replaced, which closes a length gap on the way past.

**Theory 52 gave an Italian reader a hard question for free.** The stem says
*un'appoggiatura* and the answer said *si appoggia*. The blurb already teaches
where the word comes from, so the option does not need to: it reads *si posa
sopra* now. English is untouched.

**Theory 56 stays as it is.** The marking is *col legno* and the answer names
the wood of the bow, so the Italian repeats the stem and there is no other
correct way to write it. Fixing this would make the Italian worse to make a
checker quieter. It goes on an allowlist with that reason instead.

**Guitar 43 had two faults and the number was the smaller one.** The P-90 was
the only option carrying a digit, and also the only option that was a pickup:
the other three were a bridge, a vibrato and a switch, so anyone who knew what
a P-90 is scored without knowing anything the question asks. All four are
Gibson pickups now, the three wrong ones are humbuckers, and two of the four
carry a number.

**Beatles 28 lost one word.** "Which record label did the Beatles start in
1968?" pointed at Apple Records. It asks "Which label" now. The Italian keeps
*etichetta discografica*, because *etichetta* on its own is a sticker.

**The subject cap was counting ordinary words as subjects.** "Play loudly" as
an option made "play" a recurring subject of the theory pack, and "bass" was a
recurring subject of the Bass pack. Both were the tool being wrong, and both
cost a look on every run. A capitalized word that also appears lowercase across
the pack is now dropped. Measured over the six packs, the ordinary words sit at
a lowercase-to-capitalized ratio of 0.30 and up and the real subjects sit at
0.08 and below, so the line goes at 0.25 in the middle of that gap. It is a
ratio rather than a plain lowercase test because of Apple: blurb 77 has a green
apple in a Magritte painting, and Apple is still a subject of that pack twelve
times over.

**And packs that legitimately trip the cap now carry their own allowlist.**
Running the pack audit on the Beatles gave fifteen errors, every one of them
the pack doing its job, which is how a real error hides in a wall of expected
ones. `allow_beatles.json`, `allow_theory_fundamentals.json` and `allow_guitar_gods.json`
are found
automatically from the pack name, and the file is an object of finding to
REASON rather than a bare list, because an allowlist entry with no reason rots.

**All six packs now audit clean.** The last finding was a judgement rather than
an edit and Daniele made it: Jimmy Page anchors four Guitar Gods stems against
a cap of three, and he is the answer to none of them. Four of ninety, in a pack
about guitarists, where he is the landmark the question is measured from rather
than the thing being asked about. `allow_guitar_gods.json` records that.

Every edit was read back out of the file afterward and diffed field by field
against a snapshot taken before the session. Eight fields changed across four
packs and nothing else moved.

---

## v0.198.0 — Five faults the rebuilt quiz tools found in shipped packs

The quiz toolchain was rebuilt this session and immediately found five faults in
packs that had already passed their own gates. Three of them were only visible
in Italian, which is the whole reason the rebuild happened: the draft checkers
contained no reference to `q_it`, `opts_it` or `fact_it`, so every check they
ran was English and an Italian fault could not fail the gate no matter how bad
it was.

**The clef question asked two different things in the two languages.** English
read "Which clef do bass guitar and cello parts normally use?" and Italian read
"le parti di violoncello e trombone". On top of the twins disagreeing, the
English handed over its own answer, which is "Bass". The English now matches the
Italian and names cello and trombone, both of which the blurb already covers.

**"Slides between two neighbouring pitches"** was a British spelling sitting in
a live option. It is the only one in all seven rewritten packs; a sweep of every
stem, option and blurb in both languages found nothing else.

**Three answers stood out by length, and two of them only in Italian.** The
appoggiatura answer carried "come dissonanza" where the English carries no such
phrase, which made it nineteen characters longer than any distractor; the
dissonance is in the blurb on both sides and the option now matches its twin.
The delay-and-reverb answer ran twenty-three characters clear in Italian, and
fret sprout sixteen. Those two were fixed the way the spec says to fix them, by
lengthening the distractors rather than hacking words off the answer, since
shortening gives four clipped fragments.

**Fender was named in five stems against a cap of three.** Dropped from two of
them, where the Stratocaster already says Fender and the brand was doing
nothing: "the scale length of a standard Stratocaster", "which pickup design was
the Stratocaster built around in 1954". The other three are about the company
and keep it.

**Both packs were installed through the new builder, which reads its own work
back.** After writing, it re-parses the file and compares every field of every
row against the source JSON; a mismatch restores the original and installs
nothing. That exists because `assert count == 1` catches a miss but not a script
that asserts on one substitution, applies it, then throws on the next and writes
nothing, which is how three fixes silently failed in one session and were nearly
reported as done.

All seven rewritten packs now pass the gate clean in both languages.

**Four findings are left and are not fixed here**, because they were in the file
before this session and each needs a judgement rather than an edit: three
Italian stems sharing a root with their own answer, where "appoggiatura" and
"si appoggia" is the shape and may be unavoidable, and one guitar_technique
question whose answer is the only option carrying a number.

---

## v0.197.0 — The quiz music tracks take Italian too

The nine instrumentals had no Italian names at all. Ritorno al bossa, Turno di
notte, Giro di domenica, La strada lunga, L'ultimo giro, Alisei, Quartieri alti,
Ora blu, Aeroplanini di carta. Italy keeps English song titles, but these are
mood labels rather than works, so they translate the way a chapter heading does.

**The picker already honoured `nameIt` and nothing else did.** The now-playing
line, the up-next line and the deck readout each read `.name` directly, so an
Italian player would have seen the name translated in the track list and English
everywhere else. All four now go through `mqTrackName()`, which falls back to the
English name, so an untranslated track behaves exactly as before.

Same fault as the classical pieces two versions ago, in a different place, and
worth noting that adding the field alone would have looked correct in testing:
the track list is the screen you would check.

---

## v0.196.1 — Classical before Studio

Swapped so the general group runs theory, then artists, then Classical, then
Studio. Classical sits with the music; Studio is craft and belongs last.

---

## v0.196.0 — Gear removed, Music History becomes Classical

**Gear & Equipment is gone**, 56 questions and all three references: the pack,
its colour and its icon path. The instrument packs were eating it from
underneath. Guitar already covers pickups, action, cables, buffers and string
gauge; Bass covers pickups and strings; Drums and Keys will take kit hardware
and synth architecture when they are rewritten. What was left for Gear to own
was speakers, formats and cables, which is not a pack. Anyone looking for gear
is filtering by instrument anyway.

**Music History becomes Classical.** History was defined by exclusion: every
other pack in the app is history, so it held whatever had not been claimed, and
its questions ran from Motown to Napster to Northern Soul with nothing in common
but that.

Classical is bounded, and it is the pack that matches what the app already is.
**Sixty-three performance pieces already ship**, and the composer list is
Beethoven, Chopin, Debussy, Grieg, Satie, Bach, Mozart, Tchaikovsky, Schubert
and Schumann. A player can learn Für Elise in the piano module and not be asked
a single thing about Beethoven anywhere else. Bravura notation and two theory
packs are already there to support it.

Considered and rejected: **Genre History**, which would summarise packs that
already exist. **Music Business**, a real subject nobody covers but about the
industry rather than about music. **Songs-to-bands**, which is one question shape
repeated and is really a separate game mode with audio, not a pack.

Nineteen packs now. Seven ready, twelve to go.

**The 57 questions still sitting under Classical are the old Music History
ones** and most are about popular music. They stay until the rewrite, which will
replace them, but nothing serves them meanwhile since the pack is not in
MQ_PACK_READY.

---

## v0.195.0 — Pack order, and six decade descriptions that were not doing their job

General group reordered: Theory Fundamentals, Advanced Theory, Guitar Gods, The
Beatles, Rock & Metal, Jazz Legends, Gear & Equipment, Studio & Recording, Music
History.

**Four pack descriptions said "telly".** British, sitting in user-facing text on
the pack picker, and no check looks at pack metadata: every spelling and
vocabulary sweep in the toolchain reads question and blurb fields only.

**The decade descriptions were two pairs of twins.** The 60s and 70s were word
for word identical, and so were the 80s and 90s, which makes a column of six
cards read as one repeated card. Each decade says something about itself now.

---

## v0.194.0 — Pack order

Decades run in order now: 50s, 60s, 70s, 80s, 90s, 00s. They were 60, 70, 80,
50, 90, 00. Instruments run Guitar, Bass, Vocals, Keys, Drums.

Checked before moving anything: nothing indexes PACKS by position. The only
positional read is the daily pack picker, and that filters MQ_PACK_READY rather
than PACKS, so a reorder cannot change which pack the daily serves. Confirmed
over 365 simulated dates.

---

## v0.193.0 — Bass gets a third generator and blurbs that rotate

**The octave shape.** A bass is tuned in straight fourths with no exception, so
the octave is always two strings up and two frets up, anywhere on the neck. It
is the most used shape in bass playing and the exact opposite of what the guitar
generator drills, where the G-to-B gap breaks every shape. Hard tier sits on the
five-string, where the same move has to clear the low B.

12,000 sampled answers verified against MIDI arithmetic, no dot outside its own
fret window, no nulls.

**Blurbs rotate**, four per kind, picked from a hash of the gkey so a question
always carries the same one. Distinct blurbs 2 to 12; unique questions 672 to
818.

**Two calibration passes, and the second was chasing noise.**

The first cut gave eight distinct positions at easy, because both the string
choice and the fret window were narrow. Widened, and then widened again by
letting the five-string appear at medium, since a four-string only has two roots
that can reach two strings up and the string choice cannot grow otherwise.

Between those passes the repeat rate read 13%, then 15.5%, then 17%, and I very
nearly kept tuning against it. Measured properly over 40 sessions of 20 rounds
it is **12.9% for Bass and 13.1% for Guitar, unchanged from before the generator
existed**. Twenty rounds is far too small a sample to steer by, and the earlier
readings were noise.

Tier spread unchanged: easy 74/26/1, medium 21/59/20, hard 1/25/73.

---

## v0.192.0 — A generator-only pack could not fill a hard round

**Advanced Theory hard rounds measured 1/41/58 against a 0/25/75 target.**
`mqGenBatch` always built its batch at 40/40/20, which is right for a pack that
also has authored questions but cannot fill a round wanting 75% tier 3. The
batch ran out of hard questions and the top-up quietly filled the gap with
mediums.

The batch now takes an optional mix. A pack with authored questions of its own
keeps 40/40/20 so its generated share matches the written one; a generator-only
pack IS the round, so it is built to the round's mix directly. Advanced Theory
now measures 0/26/74 on hard and hits target on all three settings.

**Two things I went looking for turned out not to be faults, and one of those
was my own bad test.**

`mqServeKey` looked like it was keying generated questions by slot index. It is
not: they carry `gen: true` and the guard fires correctly. I had tested it with
a hand-made object that lacked the field. Worth recording because the code
already documents that keying generated questions WAS tried and measured worse,
repeats inside forty questions going 18 to 23, so the change I was about to make
had already been made and reverted once.

**Theory Fundamentals returning null on 42% of easy requests is by design.**
Five of its generators decline at tier 1 outright: degree, function, enharmonic,
cadence and minor scale are not easy questions. The batch absorbs it by retrying
and fills every time, at every size tested. Wasted work, not a fault.

Tier spread across all seven rewritten packs, 300 rounds each: exact on the five
authored packs at all three settings, and Bass and Guitar within 1 to 2 points,
which is the shape cap swapping across a tier when it refuses a third question
of the same shape.

---

## v0.191.0 — The difficulty blend never hit its own targets

**Every question in every rewritten pack is tagged**, no gaps: 90/90/60/113/104/104
across the six authored packs, and the generators honour the tier they are asked
for in 3600 of 3600 samples.

**The blend was the problem, and it was asking for eleven questions to fill a
round of ten.** `Math.round(10 * 0.75)` is 8 and `Math.round(10 * 0.25)` is 3.
The pool shuffle then dropped one at random, so an easy round came out 73/27
against a 75/25 target. Only ever at qCount 10, which is why it survived.

Two fixes went in and both were wrong before the third:

- **Capping at what is left** fixes the count but freezes the mix: 7.5 always
  rounds to 8, so every easy round is exactly 8 and 2 forever.
- **Rounding each fraction stochastically** skews the other way, to 77.5/22.5,
  because the top-up loop refills from the first tier in the order and quietly
  hands it the slack.
- **Largest remainder with the leftovers raffled** is right. The quota splits
  exactly, the spare seats go to the tiers with a real fraction in random order,
  and the long-run ratio lands on target while the mix still moves round to
  round.

Measured over 8000 rounds: easy 75.1/24.9/0.0, medium 20.0/60.0/20.0, hard
0.0/24.9/75.1. Always exactly ten questions, at every count from 5 to 25.

**And the new unison generator was returning null 4% of the time it was asked
for an easy question.** With the answer at fret 1, dropping anything below fret
1 left only two distractors. The easy bucket came up short and the top-up pulled
harder questions in. Pool widened; 0 nulls in 3000, and all 3000 answers still
verify against MIDI.

Bass and Guitar still sit 1 to 3 points off on easy and hard. That is the shape
cap doing its job: when it refuses a third question of the same shape it swaps
from the spare pool, and the swap can cross a tier. Correct behaviour, and worth
more than a perfect ratio.

---

## v0.190.0 — A third guitar generator, and blurbs that stop repeating

**Both things reported after testing checked out, and neither was a bug.**

Drawing one generated question in a round is ordinary: the pack averages 2.9
generated per ten, so one happens often. And the answers clustering on A is
chance, not bias. Every pack ships `ans:0` on every row and the position is
randomised at render by a Fisher-Yates shuffle; run 200,000 times it puts the
answer in A/B/C/D at 24.9 / 25.1 / 24.9 / 25.1 percent.

**What testing did expose was thin generator coverage.** Theory has eight
generator kinds. Guitar and Bass had two each, with exactly one blurb apiece, so
a player drawing three generated questions read the same two did-you-knows.

**Third kind: the unison shape.** The same note on the next string up sits five
frets back, except across the G and B strings where it sits four. That single
exception is what this whole pack is built around, and a generated question
drills it in a way an authored one cannot because the position moves every time.
Hard tier sits on the G-to-B pair by construction, 103 of 103. All 540 sampled
answers verified against MIDI arithmetic, no dot outside its own fret window.

**Blurbs rotate now**, four per generator kind, picked from a hash of the gkey
rather than at random so a given question always carries the same blurb and
nothing shifts between renders. Ten distinct blurbs where there were two.

817 unique generated questions, up from 664, tier spread still exactly 40/40/20.

---

## v0.189.0 — Guitar ships, bilingual

**104 questions, 40/43/21, plus 16 shared in from Guitar Gods and a generator
producing 664 unique fretboard questions at a 40/40/20 spread.** Seventh
rewritten pack, and the second in the instrument tab.

**What this pack taught, which the others had not.**

An instrument pack wants ORIGINS where a people pack wants anecdotes. The easy
tier came back with 33 of 40 rewritten, and the measurable reason was that I had
carried the Beatles voice across without asking whether the subject had changed:
blurbs resting on a named player went 9 to 1 in Daniele's edits, blurbs about
where the thing came from went 2 to 10.

Avoiding definition-style stems, I turned 14 of 40 questions into riddles, and
he rewrote 20 of 25 back toward a plain question word. The check that counted
"What is X?" had been driving that, and after his edits it read 15% and was
calling his direction a fault. It now flags only the bare glossary entry.

**Italian.** 104 stems, 416 options, 104 blurbs. Note names go to Do-Re-Mi, and
imperial converts to metric because an Italian reader has no feel for pounds.
The trap in this pack is that **nut and capo are the same word**: the nut is
`il capotasto` and the capo `il capotasto mobile`.

The read caught five things no check sees, the worst being **"ricordare" used
for re-stringing a guitar in two places, which means "to remember"**. The verb
is "rincordare". Also "Quale è" where Italian elides to "Qual è", and two
missing apostrophes.

**Three checker faults found by running the tools that had been skipped.**

`intonare_quiz_livecheck.py` reported 12 answer-longest tells where the draft
checker reported none: the draft check only ever looked at English, and half of
them were Italian. Every option list at 1.6x or worse is padded now, in both
languages.

The Italian sweep flagged 16 drifts against the draft checker's 4, because it
predates the metric-conversion and worded-decade calibrations. Ported across.

And **the English used curly quotes while the Italian used straight ones**, so
three pairs of twins looked different on screen. Only visible reading the
installed file, since the draft JSON normalises them.

**One leak found in Italian that existed in English too.** Blurb 102 said "a
25.5-inch scale" while question 41's answer is "25.5 inches" — the omega pass
compares whole option strings, so the different wrapper never matched. There is
now a check for an answer restated in another form.

---

## v0.188.0 — The daily was serving unrewritten packs

**`mqGetDailyPack` picked from every pack in `PACKS`.** Fifteen of the twenty
are still awaiting a rewrite, so most days the daily quiz was handing out
questions nobody had checked. It now draws from `MQ_PACK_READY` only, minus the
generated-only packs, which have no authored questions for a seeded shuffle to
work on. Over 365 simulated dates it lands on five packs and no others.

**The hero content sits below the daily badge.** The badge is absolutely
positioned, and an absolutely positioned child is placed against the padding
box, so padding on `.mq-hero` moves the pill, title and subtitle down and leaves
the badge alone. Measured: at 320px with the Italian label the badge's left edge
and the pill's right edge met at exactly the same pixel. Now 7px of vertical
clearance at every width in both languages.

**Song titles take Italian.** `riffLabel()` follows the same rule as everything
else: a work with a real Italian title takes it, one without keeps the original.
Per Elisa, Sonata al chiaro di luna, Preludio in Do maggiore, Minuetto in Sol,
Chiaro di luna, Sogno d'amore. Maple Leaf Rag and The Entertainer stay as they
are. The fallback is the English label, so an untranslated entry behaves exactly
as before.

An apostrophe in "Sogno d'amore" inside a single-quoted string broke a script
block, which `node --check` caught before it went anywhere.

---

## v0.187.0 — Guitar generators, and a script that reported success while writing nothing

Groundwork for the Guitar pack. The fretboard renderer already carries
`guitar: { open:[40,45,50,55,59,64] }`, so no new renderer was needed: the two
Bass generators port across with the tuning table swapped.

**What a bass cannot have is the major third between the G and B strings.**
Every shape a guitarist drills changes when it crosses that gap, so the hard
tier is built to sit on it: hard interval questions place the two marked notes
on either side by construction, 116 of 116, and hard note questions sit on the
two strings above the break where lower-position shapes stop transferring.

662 unique questions, tier spread 40/40/20, all 1200 sampled answers verified
against MIDI arithmetic, no dot outside its own fret window.

**The install script reported success and wrote nothing.** It asserted on three
anchors while replacing, and threw on the third, so the file was never written.
The two lines it had already printed made it look done, and the audit I ran next
returned a plausible 969 unique questions for a pack with no generators.

The spec already warns about exactly this: `assert count == 1` catches a miss, it
does not catch a script that applies one substitution then throws on the next.
The rebuilt installer **checks every anchor before writing anything, writes once,
then reads the file back off disk and confirms each edit is present.** That last
step is the only proof that matters and it is now how generator installs are
done.

---

## v0.186.0 — A theory stem that read as a follow-up

**"Where does mezzo forte sit between the other two?"** refers to nothing. It
reads as the second half of a pair, and the quiz deals questions in isolation.
Now "What volume does mezzo forte ask for?", which is what the Italian twin had
said all along.

Swept every rewritten pack for stems leaning on something the player has not
seen: "the other two", "the previous question", "the above", "the first two".
One more hit, "Which of these tempo markings asks for the slowest speed?", which
points at the options on screen and is fine.

**A reported double space in the Fool blurb is not in the file.** Traced from
source to render: no double space, no `text-align: justify`, no `word-spacing`,
and `factEl.textContent` is assigned directly with no transformation. It is
monospace line wrapping.

---

## v0.185.0 — Questions can belong to more than one pack

Fifteen questions across the rewritten packs now serve two packs each. "Which
Beatle played lead guitar" is a Beatles question that lives in Guitar Gods;
McCartney's Höfner is a Beatles question that lives in Bass.

**Not implemented by copying the row, and the reason matters.** A question takes
its identity from the pack it is read out of:

    Object.assign({}, q, { pack: packId, idx: i })

Two copies would carry different pack ids, the round dedupe could not tell they
were one question, and a round selecting both packs would deal it twice. That is
the repeat bug fixed at v0.181, reintroduced by the back door.

So a shared question stays home and carries `also:['beatles']`. A second sweep
pulls it in **keeping its home pack and index**, which means the dedupe, the
serve counts in `mq_served` and the shape cap all keep working untouched.

**Deduped at pool-build time rather than downstream.** The existing dedupe runs
after `mqBlendTiers` has already taken its qCount, so a duplicate removed there
leaves the round SHORT instead of full. Verified: 400 rounds with the home pack
and the borrowing pack both selected produce 0 repeats and 0 short rounds, and
the survival pool comes out 338 distinct of 338.

**`mqPackQuestions` deliberately still counts only a pack's own questions**, and
both callers need that. The picker prints it as the pack's size, and
`mqCheckPackCleared` compares it against `seenQ[packId]` — a shared question is
marked seen under its HOME pack, so counting it in the borrowing pack's total
would make that pack impossible to clear.

**The daily is untouched.** `mqBuildDailyQuestions` reads `pack.questions`
directly rather than going through the pool, so it draws home-pack questions
only and stays byte-identical. Confirmed rather than assumed.

**Which fourteen, out of 31 the scan raised.** A question about where the
Precision Bass got its name matches "Fender" and "single-coil" and is still a
bass question. Survivors: three Beatles questions in Guitar Gods, three in Bass,
three guitar questions in Beatles, four notation questions from Bass into Theory,
and two from Bass into the Seventies.

Held back because their target pack has not been rewritten: Ludwig and three
drummer questions want Drums; backwards tape, the Leslie cabinet, the tape loops
and four-track all want Studio Recording.

Beatles alone now deals 96 distinct questions where it has 90.

---

## v0.184.0 — The Beatles pack ships, and the other five get measured against it

**90 questions, 36/36/18, both languages, live as the sixth rewritten pack.**
Every question was hand-sifted by Daniele one at a time through a triage tool
built for the purpose, so this pack is the standard the others now answer to.

**The Italian checks written for Beatles were run over every rewritten pack.**
Drift between the twins, English leaking into Italian prose, stripped accents,
options left untranslated. **Three real faults**, all the same kind: a nickname
sitting bare in the prose in both languages, "the Hook", "the Bass of Doom",
"the pleasure pit". All three are now quoted on both sides, which is what
Beatles does with a nickname.

**Everything else the sweep found was correct and the checks were wrong.** The
list is worth keeping because each one taught the tool something:

- `meta` without an accent is the rugby term, `portare in meta`, not `metà`
- `flatwound`, `roundwound`, `in the pocket`, `four on the floor`, `chorus`,
  `wah` are what an Italian bassist actually says
- `@`, `#`, `&`, `%` and `.009` are the same in every language
- `"...And Justice for All"` opens on punctuation, not a lower-case word
- `sedici` for 16 and `18:45` for "a quarter to seven" are not drift, they are
  Italian doing it properly; `top 40` as a numeral is in the spec

**Two shipped checks fired on the gold standard and were recalibrated.**

The blanket ban on participial closers fired on **13 of 90 approved Beatles
blurbs**, several of them Daniele's own words: "leaving Paul to fill the gap",
"citing Britain's involvement", "resulting in the raw gritty vocal tone". A
participial closer is a fault only when it COMMENTS. One carrying a fact is
fine. Now checked against a list of commentary verbs rather than any gerund.

The run-on check counted commas inside a LIST as clause joins, so "A bass is
tuned E, A, D and G" read as three joins and one clause. Lists are discounted
now.

**The finding that matters: the four older packs differ from Beatles on
register, not on faults.**

| per blurb | beatles | guitar_gods | seventies | bass | theory |
|---|---|---|---|---|---|
| quoted material | 0.24 | 0.00 | 0.01 | 0.08 | 0.00 |
| contractions | 0.40 | 0.20 | 0.18 | 0.15 | 0.15 |
| "which" as a joiner | 0.03 | 0.13 | 0.13 | 0.20 | 0.25 |

Structure is already consistent: sentences per blurb 1.5 to 1.7 everywhere,
median sentence 25 to 33 words, longest 44 to 48. The older packs were written
before the triage findings existed, so they read a shade more like reference
books and reach for the actual quote far less often. **That is a retrofit
decision, not a defect**, and it is 367 blurbs.

---

## v0.183.1 — Release-readiness sweep

Production access cleared and the rhythm renderer checked out on device, so this
is the state of everything else.

**Clean:** dev tools unreachable without setting localStorage by hand and nothing
behind the flag grants Pro; unlock codes stored as SHA-256 with no plaintext
constant; every stop function wired into `stopAllAudio` or exempt with a stated
reason; `data-i18n` complete in both languages across 890 keys; the tour has no
missing or broken steps.

**One British spelling was shipping in a question:** "An earlier sign is
cancelled", in two option arrays. Now canceled.

**The light-mode contrast audit reports 264 failures and cannot be trusted as
it stands.** Spot-checking the worst entries found elements that render at zero
size: `.tc-temp-key` measures 0x0 with its own tool open, and several others are
absent from the DOM entirely. The audit has a guard for exactly that and it is
not catching these, so the report is a mix of real findings and unmeasurable
ones. Triaging it is its own job and it is pre-existing, not a regression from
the quiz work; noted here so the number is not mistaken for 264 real defects.

---

## v0.183.0 — Repeat spacing, and one change that measured worse and was reverted

Survival is allowed to repeat as long as the gap is wide, so the gap is what
got measured, averaged over fifteen trials rather than read off one run.

**No question ever repeats inside a single round.** That is the guarantee, and
it holds in every mode.

**Median gap between seeing a question twice: 78 questions in survival, 164 in
Quick.** Survival deals 40 at a time, so a repeat sits about two full runs away.

**The shape-cap spare pool was undoing the weighting.** A swap pulled from a
shuffled spare list, so it could hand back a question the player had just
answered. The spares sort by the same fewest-then-oldest rule now.

**Serve counts gained a recency tiebreak.** Count alone left ties broken at
random, so a question dealt late in one run could return early in the next.
Stored as [timesServed, lastServedOrdinal]; plain numbers from the old format
are still read, so nobody loses their history.

**One change measured worse and was reverted.** Generated questions were keyed
as well, on the reasoning that leaving them untracked let them sort to the front
of every tier forever. Repeats inside 40 questions went from 18 to 23. A
generated batch is rebuilt every round, so ranking a throwaway set against a
persistent one just displaced the authored ordering. The reasoning was sound and
the measurement disagreed; the comment in `mqServeKey` records why, so nobody
tries it again.

Daily verified identical after 60 rounds of play. Served map: 105 keys, 1.9 KB.

---

## v0.182.0 — Stress-testing the serve counts, and a starvation bug they exposed

Three questions asked of the weighting: does it hold up over a long session,
does it hide questions or grow without limit, and is it quiz-wide. Tested rather
than reasoned about, and one of the three found a real bug.

**It does not grow.** 500 consecutive rounds tracks 104 keys and 1.4 KB, because
only authored questions are counted and a pack has a fixed number of them. The
map is bounded by the size of the packs, not by how much anybody plays.

**It was hiding two questions, and the cause was the generator.** After 500
rounds the least-served question had been dealt 3 times against a tier average of
28. Both offenders were the authored fretboard questions the new generator was
built to replace: they share a stem with generated ones, so the shape cap evicted
them almost every round. They are redundant now, so they are gone. Least-served
is 21 against an average of 28 across every tier, and no tier's most-served is
more than twice its least.

**The daily quiz is untouched, which was the risk worth checking first.**
`mqBuildDailyQuestions` builds from a seeded RNG on its own pool and never
reaches the weighted path, so the daily is byte-identical after 80 rounds of
play. Had it not been, every player would have got a different daily.

**Quick and Custom are effectively repeat-free**, at 0 to 2 repeats per 50 or
100 questions dealt, across every rewritten pack.

**Survival still repeats, by design, and it is worth being plain about.** A
survival run deals 40 questions on an easy-first ramp: 24 tier-1, 11 tier-2, 5
tier-3. Five runs therefore pull about 120 tier-1 questions from a tier-1 pool
near 70, so repetition is forced by the ramp rather than by the weighting. The
serve count still helps where it can, holding run-to-run overlap to 7 of 40.
Fixing it properly would mean changing what survival IS, which is a design
decision rather than a bug.

---

## v0.181.0 — Per-question serve counts, because the repeats were arithmetic

Reported from playing several Bass rounds in a row. Measured before changing
anything: three consecutive ten-question rounds repeated **2.2 questions on
easy, 1.7 on medium and 3.5 on hard**.

**Hard was the worst and it was not luck.** The hard blend wants 75% of a round
from tier 3, which is 7.5 questions a round against 21 authored hard ones, so by
the third round a repeat is forced. Both explanations were right: no cross-round
memory, and the difficulty concentration making that memory matter most exactly
where the pool is thinnest.

**`MQ.seenQ` already existed and fed nothing but an achievement.** Selection
never consulted it, so every round started from a clean slate and dealt with
replacement.

There is now a serve count per question in `mq_served`, and each tier bucket is
shuffled and then **stable-sorted by how often each question has been served**.
Stable sort means equal counts keep the shuffled order, so it is least-served
first with a random tiebreak, not a fixed running order. That is the same shape
as the rotation `mqGenBatch` already uses to stop one generator kind eating a
round.

Repeats across three rounds: **2.2 / 1.7 / 3.5 → 0.4 / 0.4 / 0.4.** Ten
consecutive hard rounds now serve 90 distinct questions out of 100 dealt, with
nothing served more than twice.

**Only authored questions are counted.** Generated ones vary themselves and their
keys are effectively unbounded, so tracking them would grow the map forever for
nothing. After 200 rounds across four packs the stored map is 348 keys and 6 KB,
with no generated keys in it.

**The backup audit caught the new key before it shipped**, which is what it is
for: `mq_served` is progress, so it is in `BACKUP_KEYS_PROGRESS` and it clears
with RESET STATS. A player wiping their stats expects the quiz to feel new rather
than to keep steering away from everything they have already answered.

---

## v0.180.0 — Packs are built from what they should contain, and overlap is fine

A design call, and it reverses something I did two versions ago.

**Bass cannot be fully separated from Gear, and it should not be.** Guitar Gods
overlaps Guitar Technique, the Seventies overlaps Music History, and carving them
apart produces packs with holes: a Bass pack with nothing about strings or amps
because Gear "owns" those is a worse Bass pack, and no player thinks about it
that way. Each pack is built from what a player would expect to find in it, full
stop, and double dips where the subject calls for it.

**So the three questions cut in v0.178 are back.** A key signature, an interval
between written notes, and counting a bar were removed for being "Theory wearing
a Bass badge". Reading a key signature in bass clef is a thing a bass player
does, and a Bass pack should contain it whether or not Theory also does. 106
again.

**The fault worth checking is the same QUESTION in two packs**, because a custom
round can select both and deal it twice. `intonare_quiz_dup.py` checks across
packs now, not only within one. Topic overlap is not reported at all.

The cross-pack test needed a different measure from the within-pack one. The
within-pack test divides the shared words by the SHORTER question, which is right
for catching a long rephrasing of a short question. Across packs it made "Which
Beatle played bass?" a duplicate of "Who played bass in The Who?" and reported
33 collisions. Intersection over union punishes that, because the union carries
the words they do not share: **4 real ones, all in packs awaiting rewrite**, and
one of those four is a false positive on hair metal versus nu-metal.

**A near-miss worth writing down.** The first attempt to restore the three
questions anchored on `"\n  bass: {"` across the whole file, matched an
unrelated object, and inserted three quiz rows into it. `node --check` passed,
because it was still valid JavaScript. Only the question count staying at 103
gave it away. Reverted from the exported build and redone scoped inside the
`PACKS` object. **A structural edit has to be anchored inside the structure it
belongs to, and a syntax check will not tell you that it was not.**

---

## v0.179.0 — The Bass generator was ignoring the tier it was handed

Asked whether the new generator was tuned across the difficulty tiers. It was
not, and nothing in the toolchain would have said so.

**It generated zero hard questions.** `mqGenBatch` passes the requested tier into
every generator; both Bass ones took the argument and ignored it, returning a
hardcoded d:1 and d:2. So a HARD round on Bass got no generated content at all,
which is exactly where fresh questions matter most. The spread was 50/50/0
against a 40/40/20 target.

Both honour the tier now, and the tiers are actually different rather than
differently labelled: easy sits in first position on a four-string, medium climbs
to frets 5-8, and hard moves to frets 7-12 with a five-string about half the
time, where the low B has to be counted from rather than recalled. Intervals band
the same way: fourths, fifths and octaves at easy, thirds added at medium, the
minor seventh at hard. Measured spread is now 40/40/20, and a hard round receives
28% generated questions where it received none.

**The check now measures tier spread, and the bar is absence rather than drift.**
Theory Fundamentals generates 17/56/27 because its profile tags by content rather
than by the slot asked, and that is fine: `mqBlendTiers` tops a round up from the
authored pool, and it still delivers 73/27/0 on easy and 0/27/72 on hard, both on
target. A tier a generator can NEVER produce is the real fault, because then the
blend has nothing to top up from once the authored pack runs thin.

All 1200 generated questions re-verified against MIDI arithmetic across all three
tiers, zero wrong, and no dot outside its own fret window on either instrument.

---

## v0.178.0 — The Bass diagram questions now generate, and three of them were Theory in disguise

**"The A7 above the staff" referred to something never drawn.** `mqVisHtml` does
not forward `labels` to `pitchedStaffSvg`, so the chord symbol the question named
has never once appeared on screen. Asked without the staff now, because the
question does not need one: naming the third of A7 is a chord question.

**The one-drop diagram answered its own question.** A stem asking which beat is
left empty, over a bar with a rest on beat one. Same fault as the three found
last version, so it is now five; the diagram is gone.

**Bass was not in `MQ_GEN_PACKS` at all.** Its 22 diagram questions were fixed
payloads showing the same dots on the same frets forever, so a player who has
seen "which note is marked" has learned the picture rather than the neck.
`mqGenBassNote` and `mqGenBassInterval` build both from a random position and
derive the answer from `SR_FRETS`, so the drawing and the correct option are one
decision. **685 unique questions where there were 11**, every answer verified
against MIDI arithmetic across 1200 samples.

The Italian needed the same accidental-matching the tritone generator needed:
Italian spells a sharp out as "Do diesis" against a bare "Re", so a sharp answer
among natural distractors was the longest option every time. 46 length tells,
now 0.

**Switching a generator on broke the shape cap, and the simulator caught it.**
Every generated question shares a stem, so the cap immediately mattered more, and
the version shipped last time only pushed over-cap questions to the back of a
list that was already exactly qCount long. They stayed in the round. It now swaps
them for spares the blend did not take. Worst same-shape count went 2 → 6 → 2.

**Three questions were pure Theory wearing a Bass badge.** A key signature with
two flats, an interval between two written notes, and how many beats a bar holds:
no bass content, and the Theory generator already produces all three endlessly.
Removed rather than kept for the count. Bass is 103 authored plus the generator.

---

## v0.177.0 — Three device-testing bugs, fixed pack-wide rather than one at a time

**Three diagrams answered their own question.** The five-string fret question drew
a dot on the fret it was asking you to name. "Which fret carries the double dot?"
is answered by the renderer, which draws the inlays. And "how far below the E does
the lowest string reach" prints the string names B E A D G down the side, so the
interval is readable off the picture. All three are text questions that never
needed a diagram; the diagrams are gone. Audited all 27 diagram questions rather
than the one that was photographed.

**Options that are diagram labels no longer shuffle.** A question about the dot
marked A, offered as "A → B, B → A, C → D, D → C", asks a player to hold two
alphabets at once. Those options now sort, so the row reads A→A, B→B, C→C, D→D
and the answer sits in whichever slot its label belongs to.

The detection matches the option against the labels actually drawn on that
diagram, not against a shape. A first version tested for "a single capital
letter", which also caught note-name options like E / C / D / F, and sorting
those would have quietly stopped randomising which slot the answer sits in. That
is a worse bug than the one being fixed and it would not have shown up on a
screenshot. Six Bass questions qualify; the note-name ones still shuffle.

**A round could deal the same question shape three times.** The identity dedupe
was already there and works, so this was not a literal repeat: three Bass
questions open "What do you call a note..." and six share "Which ... marked
position ...", which on a phone reads as being asked the same thing twice. A
round now caps any one shape at two, where shape is the first four words of the
stem plus the diagram type. Spilled questions go to the back rather than the bin,
so a thin pack still fills a round.

Ordering matters here and the first attempt had it wrong: the shuffle has to
happen BEFORE the cap, or it mixes the spilled questions straight back in.

**`intonare_round_sim.js` is new.** It builds 400 real rounds headless and
reports repeated questions and the worst same-shape count. Currently 0 and 2.

---

## v0.176.0 — Two Bass stems reworded from device testing

**"Every Ampeg SVT prototype in existence" was overclaiming and reading like
copy.** The sources say the Stones got the prototypes, not that they got every
one that existed, and the sentence was doing work the blurb should do. The stem
asks which band took the prototypes on tour in 1969; the blown backline, the
voltage and the technician stay in the blurb where they belong.

**The Tower of Power question described a technique with no record attached.**
"Muted almost every note and ran sixteenths under Tower of Power's horns" asks
you to recognise a playing style in the abstract. It names "What Is Hip?" now,
so the question points at something a player can go and listen to. The blurb no
longer names the record, since the stem does.

Both reworded in Italian at the same time. The English first attempt ended
`"What Is Hip?"?` with two question marks, which is what happens when a title
that is already a question goes on the end of a question; both languages now
open with whose line it is instead.

---

## v0.175.0 — Checking the claim instead of making it

Asked whether the packs and the module were both actually done. They were not.

**The daily share text was English.** "Intonare Daily Quiz — " and "7/10
correct", both hardcoded, so an Italian player sharing a result sent an English
message to an Italian friend. It is the one string in the app that leaves the
app, which makes it the worst place for this.

**Three proper nouns across two packs needed their category word**, found by
sweeping all five rewritten packs rather than only Bass. Nearly every hit was a
false positive, because people, cities and song titles read correctly bare in
Italian; the three real ones were a book, a school and an album, where an Italian
reader cannot infer what kind of thing it is: `nel libro Geddy Lee's Big
Beautiful Book of Bass`, `della scuola Ashfield Boys High`, `sull'album Jack
Orion`.

Everything else the quiz paints now resolves through `t()`, `packName()` or an
explicit Italian twin. The two literals left in the block are `||` fallbacks
behind keys that exist, so they are unreachable rather than leaking.

---

## v0.174.0 — The in-quiz streak toast, and how proper nouns should read in Italian

**The streak toast baked the word into each branch.** `'+15 XP 🔥 5 STREAK!'` was
a literal in all three branches, so the toast that fires mid-quiz said STREAK in
Italian while every other streak label on the screen said SERIE. The word comes
from `mq_streak_toast` now: STREAK in English, DI FILA in Italian, which is how
Italians actually say it about a run of correct answers.

**Proper nouns, checked against Italian sources rather than assumed.** The rule
is what the thing was called when it reached Italy, and it splits three ways;
QUIZ_SPEC now carries it.

South Park keeps its name in Italy, Comedy Central is Comedy Central there, and
**the series airs with the original American theme**, so the Claypool question
works for an Italian player exactly as it does in English. Company and model
names never translate. Song and album titles never translate.

Films are the opposite: most pre-1990 cinema got an Italian release title, which
is why the Seventies pack correctly says Guerre stellari and Lo squalo.

The third case is the one that was actually wrong here. An Italian reader needs
the category word where an English one infers it, so `a Musician` became `alla
rivista Musician`, `il corto Spirit of Christmas` became `il cortometraggio The
Spirit of Christmas`, and `della Fairfax High` became `del liceo Fairfax High`.
Also `top forty`, which Italy writes as `top 40`.

---

## v0.173.0 — Finishing the Music Quiz, having claimed it was finished

The previous version fixed two screens and I described the subsystem as covered.
Sweeping the whole quiz block found seven more, all painted by JS and therefore
invisible to a markup audit.

**The pack picker was entirely English.** "No packs selected", "All 8 packs
selected", "3 of 8 packs", SELECT ALL and DESELECT ALL were literal strings on
the one screen whose whole job is choosing packs.

**The online category chips.** BANDS, MUSICALS and VIDEO GAMES had no Italian
twin, their shared subtitle was English, and the ONLINE ONLY / OFFLINE badge was
a literal on both branches of a ternary.

**The daily label rebuilt what a helper already does.** `packName()` exists,
takes the Italian twin, and has done since it was written. Three call sites
concatenated `pack.name` by hand and prefixed a hardcoded "DAILY", so the daily
quiz showed an English pack name under an Italian header. All three call the
helper, and the prefix uses `mq_daily_badge`, which was already in both tables.

Every string the quiz paints now goes through `t()`, `packName()` or an explicit
Italian twin. `data-i18n` coverage is complete in both languages and no `t()`
call resolves to its own key.

---

## v0.172.0 — English strings leaking through Italian mode

Reported from the device, and the quiz stats screen was the worst of it.

**The whole stats grid was literal English.** `mqShowStats` built its six labels
as plain strings rather than through `t()`, so ANSWERED, ACCURACY, BEST STREAK,
TOTAL XP, BEST SURVIVAL and CORRECT stayed English in Italian mode even though
three of those keys already existed in both tables. BY PACK and the pack sheet's
"113 QUESTIONS IN PACK" were the same. Five new keys, and every label now goes
through `t()`.

**The quiz BACK button was bare text beside an SVG**, so a `data-i18n` on the
button would have wiped the icon. It is a span now.

**The streak toast fell back to English on most days.** `_dailyStreakMsg` returns
a translated string on milestone days and on multiples of ten, and a hardcoded
`count + ' day streak.'` on every other day, which is most of them.

**The tuner badge ignored the Italian twins it was given.** It read `inst.name`
and `inst.sub` straight, so BASS stayed BASS and 4-STRING stayed 4-STRING even
where a `subIt` was already sitting in the table. Twenty instrument entries
gained `nameIt` and `subIt` and the badge reads them. CAPO was hardcoded too.

**Static markup:** the theremin volume label, the tuner KEY pill and the piano,
organ and Rhodes tabs. ORGANO in Italian; the other two stay.

Untagged static strings are down from 128 to 124, and the ones left are mostly
symbols, brand names and dev surfaces. `data-i18n` keys remain complete in both
languages, and no `t()` call resolves to its own key.

---

## v0.171.0 — Scoping the style checks to the packs that are actually finished

Five packs have been rewritten: Guitar Gods, Theory Fundamentals, Advanced
Theory, the Seventies and Bass. The other fifteen are queued for the same
treatment, so **editing their wording now is work that gets deleted when they are
rebuilt from a topic list.** Some of that happened in the previous version.

`intonare_quiz_style.py` reads `MQ_PACK_READY` and marks everything else as
"queued", reporting its rate for information without counting it as a failure.
The gate is now the five that are done.

**The tricolon check was too loose to act on.** It matched any list of three and
reported 176 hits, including "E, A, D and G" (a tuning), "Emerson, Lake and
Palmer" (a band) and "Italy, France and Spain" (three countries). It now requires
three lowercase words of four letters or more, which is the rhetorical triple and
not an enumeration.

Measured against that, the rewritten packs were already clean: Guitar Gods 0,
Theory Fundamentals 0, the Seventies 2, Bass 4, and all but one of those six are
genuine lists. The one real triple, in the Tutmarc blurb, is rewritten. The 82
remaining sit in the queued packs, which is the rot the rewrites exist to remove.

---

## v0.170.0 — The style tool had never read a bilingual pack, and every pack got the cadence pass

**`intonare_quiz_style.py` matched zero questions in four of the twenty packs.**
Its question regex wanted `q:"..." , opts:` with nothing between, and every
bilingual pack puts `q_it` there. Guitar Gods, Theory Fundamentals, the
Seventies and Bass were being reported clean because the tool had never read a
word of them. That is the same silent-zero as the audit parser two versions ago,
in a different file, and it is now the second one found by checking a number
that looked too good.

With the parser fixed, the file was carrying **nine em-dashes, four "not just"
constructions and four hedges** in live question text. All cleared.

**The repetition check is now a tool rather than a memory.** The style tool
measures eleven overused constructions per pack and reports a rate per question,
warning above 0.08. The threshold is measured, not guessed: the cleanest packs
sit at 0.00 to 0.03 and the median is about 0.04.

On the first run, seven packs were over. Rock and Metal used "built on" seven
times, Music History six. Theory Fundamentals and Guitar Gods each used "which is
why" three times. Bass had "turns up" four times. Every one of those reads fine
alone, which is exactly why no per-question check has ever caught them, and why
this had to become a per-pack measurement instead of a rule in a document.

**Forty-four rewrites across nine packs.** Every pack is now under the line.

## v0.169.0 — On-device testing found two giveaways I created and a verbal tic

Two of these came from last night's own fixes, which is worth writing down: both
were introduced while correcting something else, and both passed every audit.

**The numbered fretboard positions gave away any question about a degree.**
"Which marked position is the third of the scale?" with the positions labelled
1, 2, 3 and 4 answers itself. The numbers only exist because the letters A to D
collided with the easy tier when the tiers were first assembled together. They
are W, X, Y and Z now, which are neither note names nor scale degrees.

**Renaming a chord to A7 put the answer in the stem.** "Which written note is
the root of the A7 above the staff?" has one possible answer and the question
states it. The chord became A7 last night purely to stop its answer colliding
with a fretboard question. It asks for the third now, which the symbol does not
hand over, and the options spell out "A natural" and the rest so the one
accidental is not the longest.

**A verbal tic across the pack.** "Most of what" or "most of the reason" seven
times, "is where ... comes from" four, "turns up" six, "which is why" three.
Each is fine once. Together they are the cadence that gets called out, and no
tool looks for a construction that is only wrong by repetition. Twenty-one
rewrites, English and Italian, and the counts are down to one or two apiece.

---

## v0.168.0 — The generated pack had never been read, and the old packs got their answers back to a normal length

**Advanced Theory is generated at runtime and nobody had ever seen its output.**
It ships with an empty question array, so every read of the authored packs
skipped it entirely while it sat in `MQ_PACK_READY`. `intonare_gen_check.js` and
`intonare_gen_harness.js` now run the generators headless in node, which is
enough of a browser to build a thousand questions and check them.

**Its chord-scale questions served English options to Italian players.**
`opts_it: all.slice()` copied the English list, so the stem and the blurb were in
Italian and the four scale names in between were not, while the sibling scale
generator had translated them all along. The table carries `scaleIt` now.

**Two generated stems were setup sentences**, in both languages, which is the
shape section 3c bans. Asked forwards now.

**The tritone substitution answer was the longest option ten times in a hundred**
because a flat root spells out in Italian as "Re bemolle7" against a plain
"Sol7". The distractor pool was built from major intervals only, so a natural
root had no accidental candidates to balance against; it now draws on minor and
perfect intervals too and takes accidental roots first. Down to five in nine
hundred, and the remaining ones are an Italian spelling artifact with no
equivalent in English.

**Zero criticals across all 1324 questions for the first time.** Twenty-three
answers in the older packs were essays sitting beside three-word distractors:
"A modulated delay that creates a shimmering, doubled sound by mixing slightly
pitch-shifted and delayed copies of the signal" against "A type of reverb". Each
correct answer is a normal option length now and the shortest distractors were
lengthened. **These packs still need the full rewrite the Bass pack got**; this
makes them playable, not good.

**Six giveaway questions in the decades packs** named a band and asked for the
album, where the album is that band's self-titled debut. All six ask by way of a
song from the record instead.

---

## v0.167.0 — A shipped audit had never seen the Bass pack

**`intonare_quiz_audit.py` reported BASS (0Q) and called it clean.** Its parser
looks for `opts:[...],ans:` with no space after the comma, and the Bass rows are
written `opts:[...], opts_it:[...], ans:0`. A hundred and six questions were
skipped in silence, which is worse than an error, because the report says
"clean ✓" next to the pack name. The parser is whitespace-tolerant now and the
file's total went from 1218 questions to 1324.

**Four answers in Bass were findable by length**, all invisible until the parser
was fixed. Each was fixed by lengthening the distractors rather than trimming the
answer, which is the rule this file records after the last pack: the Rolling
Stones question gained a longer fourth option, the key signature options all say
"major" now, "Continuum" became "Three Views of a Secret", and G&L became G&L
Guitars.

**Six giveaway questions in the decades packs.** Each named a band and then asked
for the album, where the album is the band's self-titled debut, so the stem
contained its own answer: the Doors, the Stone Roses, LCD Soundsystem, Franz
Ferdinand, Vampire Weekend and Fleet Foxes. All six ask by way of a song from the
record instead.

**Two generated stems in Advanced Theory were setup sentences.** "A seventh chord
is written here. Which inversion is it?" and "This bar has had its time signature
removed. Which one fits it?" Both were the exact shape section 3c bans, in both
languages, and both are asked forwards now. Advanced Theory is generated at
runtime and has an empty question array by design, which is why no read of the
authored packs had ever looked at it.

---

## v0.166.0 — Every Italian line in every live pack, read out loud

369 bilingual questions read one at a time, in Italian, the way the English got
read: does a native speaker say it this way, does the sentence hold together,
does the answer still fit the question. Guitar Gods, Theory Fundamentals, the
Seventies and Bass.

**Fourteen stripped accents were already shipping**, four of them in questions a
tester could have hit on the first round. "gli e venuto" for "gli è venuto",
"Angus provo" for "provò", "la mattina trovo" for "trovò", "si e procurato" and
"si e fatto". The rest were in packs not yet live: perche, piu, citta. None of
these is a translation problem; the accents were lost somewhere in handling and
nothing in the toolchain looks for them.

**Grammar that no check could see.** "L'editore di Berry lo fece causa" (fare
causa takes an indirect object). "A New Orleans si sbatteva le corde" (impersonal
si wants a plural verb before a plural object). "Che cosa chiede a un archi" and
"chiede all'archi" (archi is plural). "battè" for "batté". "il Höfner" four times
over, where a silent H takes l'.

**Two questions asked one thing and answered another.** The Italian ghost-note
stem asked which notes are ghosted while its options answered where they fall;
the English had the same fault and both are fixed. A Nadia Comaneci question
opened "Il tabellone non poteva mostrare un dieci pieno" as a separate sentence
and never named her, so it only made sense next to the question before it, which
the shuffle does not guarantee.

**Things translated that should not have been.** "Il Sottile Duca Bianco" for
The Thin White Duke, which nobody in Italy says. "i flamenchi", which is not a
word. "cartelli stradali" for signposts, read literally. "la sigla f" for a
dynamic marking, where sigla means an abbreviation or a TV theme tune.

**And one fact contradicted its own question**: a clef question asked about
guitar and flute parts and its blurb answered about guitar and violin.

Thirty-eight corrections in all. The pack audit, the sentinel, the backup audit
and the changelog gate all pass, and every script block still parses with the
accented strings in place.

**Still unresolved, and it is Linda's call, not mine.** "barrè" appears seven
times; the word is French and Italian guitarists write it both ways.

---

## v0.165.0 — The Bass pack, and rests in quiz rhythm notation

The Bass pack is written: 106 questions in English and Italian, 42 easy, 43
medium and 21 hard, replacing 66 old ones that were mostly "What is 'X' on
bass?" definitions with no Italian and no difficulty tags. 27 of the questions
carry a diagram: 14 fretboard, 8 rhythm and 5 staff.

**`mqRhythmSvg` can draw rests and triplets.** It could not before, and the
absence nearly cost three good questions: a reggae one-drop is a question about
the beat that is left empty, and an empty beat needs a rest. The Rhythm Reading
tool has drawn both for a long time. `rrRestSvg` is a shipped function and the
triplet beam and bracket are drawn in `rrRenderRow`, so this calls the first and
copies the second rather than inventing either. The two renderers now have to
agree on what a triplet looks like, which is a duplication worth watching.

**The pack is NOT in `MQ_PACK_READY` and still shows COMING SOON.** No native
Italian speaker has read it. Linda's pass comes before it goes live, and the
question text and blurbs are in the project files for her to read on paper
rather than through the app.

**One question lost its diagram.** "Where do the ghost notes fall" needs a
ghosted notehead, which is a notation glyph the app does not have in any module.
Rather than adding one unreviewed, the question asks which notes in a
sixteenth-note funk line usually get ghosted, and the diagram waits.

Every fretboard dot was verified by computing its pitch from `SR_FRETS` rather
than by eye, and all 26 payloads were rendered in isolation before loading: 21
through the note and fretboard renderers, 5 through the staff renderer, with the
staff geometry checked against known positions. Bass clef top line A3, bottom
line G2, low E on the first ledger line below. The one diagram question without
a payload asks where that low E sits, and is answered in words.

---

## v0.164.0 — Fretboard diagrams in the quiz

Third visual type for quiz questions, after staff notation and rhythm notation.
`vis:{t:'fret', inst:'bass', lo:1, hi:5, dots:[...]}` renders a neck with string
names, fret numbers, inlays and marked positions.

**Why a new renderer rather than reusing one of the three that exist.** The app
already draws necks in `srRenderFret` (Sight Reading), `gccDrawDiagram` (chord
charts) and `gssDrawFretboard` (scales). All three append DOM nodes into a fixed
element by id, and `srRenderFret` also reads seven module globals and wires click
handlers for its drill. `mqVisHtml` builds a string. Refactoring a working,
tuned, interactive tool to serve a pack that does not exist yet is speculative
surgery, so this borrows the geometry and returns markup instead. If the Bass
pack proves it out, folding the two together later is a safe refactor with the
quiz as a second test case.

Carried across from `srRenderFret`, all of them things that were got wrong once
already and are commented as such: inlays sit in the fret they mark rather than a
cell early, a nut is only drawn where the nut is, lane height near square reads
as a neck instead of a grid, and every color arrives concrete because SVG
attributes cannot resolve `var()`.

Three faults found in the prototype and fixed: fret numbers were clipped against
the bottom edge and now have their own label strip; asking for an open column and
a fret zero drew the same column twice; and the board rectangle spanned the label
strip.

**Regression checked against a baseline captured before the change.** All six
instruments in Sight Reading across both fret windows produce identical node
counts and viewBoxes, and the chord and scale diagrams are unchanged at 25 and 89
nodes. `SR_FRETS` already carried bass at 28/33/38/43 and five-string at
23/28/33/38/43, so both work without new tuning data.

## v0.163.2 — Full criteria pass on the thirty new Guitar Gods questions

Three more found by checking rather than assuming.

**The Italian mixed articles** in one option set: three bands took "I" and the
Allman Brothers kept the English "The".

**Muddy Waters had a loose stem.** Taking the Delta sound to Chicago and plugging
it in describes Howlin' Wolf equally well, so the question now anchors on the
1941 Lomax field recording, which is his alone, and the Chicago move went into
the blurb.

**The Carter question gave away half the board.** Naming the Carter scratch in
the stem meant a player could ignore Kitty Wells and Patsy Montana without
knowing anything. The stem now asks which member of the Carter Family played
guitar, all four options are Carters, and the technique name moved to the blurb.

Everything else checked clean across the thirty: no duplicate options in either
language, no answer findable by length or number format, no stem sharing a
distinctive word with its answer that a distractor does not also carry, no
pronoun openings, both languages complete on every row.

## v0.163.1 — Answer-level fact check on the thirty new Guitar Gods questions

Nine of the thirty have an answer resting on a claim rather than an event. Two
needed fixing, and one of those was a question with two correct answers.

**The homemade guitar question had two right answers.** I asked which guitarist
from Niger built his first instrument from bicycle brake wire and listed
Tinariwen's Ibrahim Ag Alhabib as a distractor. Both stories are true: Ag Alhabib
built his from a tin can, a stick and bicycle brake wire, and Mdou Moctar built
his from scrap wood, bicycle brake cable and the key off a sardine tin. The stem
was leaning entirely on "from Niger" to separate them, and Bombino, another
distractor, is also Nigerien. The question now anchors on the sardine tin, which
only Moctar has, and the blurb credits Ag Alhabib's tin can.

**Lonnie Johnson's sessions were not duets.** He guested on Armstrong's Hot Five
records and played on Ellington's The Mooche and Hot and Bothered, but the duets
he is famous for were with Eddie Lang, who was sitting in the distractor list.
The stem now says he played on records by both, which is what happened, and the
Lang duets moved into the blurb where they belong.

**Verified and unchanged:** Sharon Isbin has commissioned more concertos than any
other guitarist and founded Juilliard's guitar department in 1989; Randy Rhoads
was Ozzy's first solo guitarist; Joni Mitchell's tunings; Malmsteen; Garcia's
Wolf; and Ali Farka Toure's nickname.

## v0.163.0 — Guitar Gods to 90

The padding fix in v0.162.4 exposed how thin this pack was: survival used to loop
the deck forever, and once it stopped doing that, Guitar Gods hard-stopped at 60
against 91 for Theory Fundamentals and 92 for the Seventies. Six rounds of ten
and the pack was done.

Thirty new questions at 12/12/6, which lands the split at exactly 40/40/20.

**What the old sixty was missing.** Classical guitar, flamenco, African and
Brazilian playing, punk, metal beyond Iommi, country beyond one Chet Atkins
question, prog, and the pre-war blues foundations. Three women in sixty.
Chronologically it stopped around 1990.

**Now in:** Robert Johnson, Johnny Ramone, Randy Rhoads, Dimebag Darrell, Joni
Mitchell, Santana, Muddy Waters, Segovia, Paco de Lucia, Malmsteen, Metallica and
Blackmore at easy; Scotty Moore, Maybelle Carter, Buddy Guy, T-Bone Walker,
Curtis Mayfield, Eddie Hazel, Steve Cropper, James Burton, Jerry Garcia, Johnny
Marr, Nancy Wilson and Tommy Emmanuel at medium; Lonnie Johnson, Elizabeth
Cotten, Ali Farka Toure, Mdou Moctar, Emily Remler and Sharon Isbin at hard.

Women go from three to eight. The pack now runs from Mississippi in the 1930s to
Niger in the 2020s.

**Checked against the existing sixty before writing**, which caught four things:
Zappa was already in as the answer to the Steve Vai question; a name check said
only Gretsch collided, but a theme check found tunings would have hit seven,
blues roots eleven and makers nineteen; and I had proposed Robert Johnson twice
in my own list. Seven candidates were cut on that basis.

**Two more caught by the audit after writing.** Naming Hendrix in the Buddy Guy
stem pushed him to four questions, over the cap, so the stem now anchors on the
hundred-foot cable instead. John Williams was dropped for Julian Bream and then
for nobody: in a guitar pack, that name reads as the Star Wars composer.

## v0.162.4 — Survival was dealing the same question seventeen times

Custom survival sets the question count to 999 as a stand-in for endless, and the
builder had two loops that padded a short pool up to the requested count by
reshuffling and dealing again. On Guitar Gods that meant 999 questions drawn from
a pool of 60, with some cards appearing seventeen times in one run. The Seventies
and Theory packs repeated up to eleven times.

The comment on that code said "cap at qCount (50)", which was true when it was
written and stopped being true when custom survival started asking for 999.

Both padding loops are gone. A run now ends when the lives go or the pack runs
out, and a fixed round with a thin pool is simply shorter rather than padded with
repeats. `MQ.qCount` follows what was actually dealt, since the progress bar
reads it as the denominator.

**Separately, the pool itself could contain duplicates.** Two generator batches
can independently produce the same card, so all-packs survival still showed six
repeats in 999 after the padding fix. The pool is now deduped before anything is
dealt, keying authored questions on pack and index and generated ones on gkey.

Verified: every ready pack, alone and combined, in both languages, at survival
and at 5/10/20/50, deals unique questions only. The 144-combination custom sweep
passes clean, and the answer shuffle was checked separately over 400 renders with
an even spread across the four positions, zero desyncs between the shuffled index
and the real answer, a perfect round scoring 10 of 10 and a deliberately wrong
round scoring 0 with every miss review showing the true answer.

## v0.162.3 — Answer-level fact check on the Seventies pack

Eighteen of the 113 questions have an answer that rests on a claim rather than
on an event: a first, a superlative, an attribution, a specific number. Those
are the ones where being wrong makes the app look broken, because a player who
knows the topic sees a correct option marked wrong. All eighteen are now
resolved.

**Two were wrong and are fixed.**

The smiley question asked which slogan the Spain brothers added to Harvey Ball's
design and gave "Have a Nice Day" as the answer. They added "Have a happy day"
and copyrighted that in 1971; the nice-day wording came later. The stem now asks
what ended up attached to the smiley through the decade, which the listed answer
does fit.

The Atari question asked which console Atari released in 1977 and answered "The
2600". It launched in September 1977 as the Video Computer System and was only
renamed the 2600 in November 1982, when the 5200 arrived and the two needed
telling apart. The question now asks what it was actually called, with Stella,
the real development codename, as a distractor.

**Corrected blurbs in the same pass**: the Beatles press release went out a week
before the album rather than six days; the Ramones debut cost $6,400 rather than
about six thousand; Barry Gibb's falsetto came from Arif Mardin asking him to
scream in tune rather than from a happy accident; Farrah Fawcett held out for a
one-piece against the poster company's bikini rather than choosing the red suit
for the scar; Charlie Hall's chair held three hundred pounds of liquid starch
and he called the bed the pleasure pit.

**Removed for being unsourceable** rather than searched indefinitely: Evel
Knievel's broken-bone count, Jim Fixx's two packs a day, the Muppet Show's
hundred countries, landlords banning waterbeds, and the Holiday Special's twenty
million viewers.

**Verified and unchanged**: Studio 54's thirty-three months and the tax case,
Voyager's disc, the Wrigley's barcode, PFM on Manticore, RAI going to colour on
1 February 1977, Comaneci's 1.00, the Fiat 127, Boba Fett, Chic, the waterbed,
the Betamax tape length, the Sugarhill settlement, and Farrah's twelve million.

Blurb colour beyond these is at the same standard the four shipped packs already
carry. The errors clustered hard in specific counts and in first/only claims,
which is worth knowing when writing the next pack.

## v0.162.2 — Fourteen untranslated strings in the Music Quiz

Reported from an Italian round: the quit button and several labels stayed in
English on a screen that was otherwise translated.

Fourteen visible strings across seven quiz screens had no `data-i18n` at all:
QUIT, BACK, DAILY, RESUME, the timer label and its OFF state, START in two
places, CLEARED, CORRECT OUT OF, REVIEW MISSES, SHARE RESULT, PLAY, the daily
popup's one-attempt line, the survival lives line, and the loading message.

Three of them already had Italian values sitting in the language table and had
simply never been wired to the markup, which is the more annoying kind of
missing: the translation existed and nobody could see it. The other eleven
needed new keys.

QUIT and RESUME carry an icon beside the label, so the text now sits in its own
span rather than the attribute eating the icon.

Verified by switching to Italian and walking every quiz screen: nothing renders
English any more, and QUIT reads ESCI. The i18n audit reports 885 keys in markup
with both tables complete, up from 870.

Also corrected on the fact-check: the Beatles press release went out a week
before the album rather than six days, the Ramones debut cost six thousand four
hundred dollars rather than about six thousand, and Evel Knievel's broken-bone
count is no longer asserted, since the usual 433 figure is itself disputed.

## v0.162.1 — The correct answer was never translated

Reported from a real Italian round: the whole feedback sheet was in Italian and
the correct answer inside it was in English.

The sheet read `q.opts[q.ans]` directly. Every other read point in the quiz goes
through `mqLOpts`, and this one had been missed since before the bilingual work
started, so it has been showing English answers to Italian players on every
wrong answer in every pack. It only became visible now because the Seventies
pack has Italian questions that are obviously Italian.

Also: the Comaneci scoreboard question gave no way in. Knowing that a board
showing 1.00 means a perfect ten requires already knowing the story, so the stem
now supplies the setup, and the question is what the machine did with a score it
could not display.

## v0.162.0 — The Seventies pack, rebuilt and locale-aware

113 questions replacing the old 58, which are archived under
`seventies_pre_rebuild`. Twenty-two of those opened with "What was the
significance of", the pack was entirely music despite its own description
promising television and fashion, and two were factually impossible: an Elton
John album that never contained both of the songs named, and Dark Side of the
Moon described as the best-selling instrumental album.

**Questions can now carry a locale.** A decade means different things in
different countries, so `loc:'en'` or `loc:'it'` marks a question as being FOR an
audience rather than translated for it. Both languages are still written on every
row, because the pool builder drops any question with an empty English stem
before it checks the locale, and because a player can switch language mid-round.

- 70 shared, 22 American, 21 Italian
- An English player draws from 92, an Italian from 91
- Split 39/42/19 against a 40/40/20 target

The Italian slice is Carosello ending on New Year's Day, Goldrake arriving on
Rete 2, the divorce referendum, Mina's Cedrata spots and her retirement, De
André's Spoon River album, PFM signing to Manticore, rotten eggs at Sanremo, and
De Gregori being put on trial from the stage of the Palalido. The American slice
is Roots, the tall ships, streaking at the Oscars, Hank Aaron, Billie Jean King,
Secretariat, the Immaculate Reception, Schoolhouse Rock and the empty Star Wars
box at Christmas.

**Sourcing.** Sixteen claims were checked across the build. Three were flat
wrong: Kraftwerk's Autobahn as a 22-minute hit, Jochen Rindt's nationality and
the timing of his title, and the Fiat 127's predecessor winning the same award.
Three more were too disputed to state: the Rumble in the Jungle's exact hour, the
Lucas sledgehammer quote, and Rapper's Delight as the first rap on radio. One is
a myth kept because the correction is better than the legend, being the Space
Invaders coin shortage. Four unsourced details were removed or attributed rather
than searched indefinitely.

**Both audits found eleven faults that reading did not**: the 1970 semifinal
asked twice, three Sanremo questions and three Carosello questions, two stems
sharing a distinctive word with their own answer, Concorde as the only option
without a number, Studio 54 and the Atari 2600 as the only options with one, and
two Italian answers findable by length while the English was balanced.

## v0.161.3 — Pat Metheny question rebuilt, and a pack audit to find the rest

`intonare_pack_audit.py` checks the half of the definition of done that a machine
can hold: answers findable by length in EITHER language, an answer that is the
only option carrying a number, a stem sharing a distinctive word with its answer,
a blurb that restates its stem rather than adding to it, cross-references between
questions, a subject appearing more often than the cap, two questions with the
same answer, untagged difficulty, missing Italian, tier drift.

Every check was tested against a reconstruction of a real fault found by eye
while building the Seventies pack, and it catches all ten classes.

Run against the shipped Guitar Gods pack it found ten things, of which one was
worth fixing. **Question 54 had three tells stacked on it**: "synthesized" in the
stem pointing at "synthesizer" in the answer, GR-300 as the only numeral on
screen, and an Italian answer of 44 characters against 28, 22 and 21. Any one is
survivable; three on the hardest card in the pack means it can be solved without
knowing anything about Pat Metheny. The stem loses the word and two distractors
gained model numbers.

Left alone deliberately: "sound" appearing in both stem and answer on the talk
box question, where all four options are plausible mechanisms of similar length;
the humbucker question, whose Italian answer is long because that is how the
sentence goes in Italian and padding the distractors would make them worse; and
Jimmy Page appearing in four questions, which in a pack about guitarists is the
pack working rather than failing.

**Six bugs in the audit itself, all caught by running it against known-good and
known-bad rather than trusting its output.** It read `opts[0]` while the pack
stores an answer index, so it called Eddie Van Halen and Eric Clapton the same
answer. Its subject cap of 2 came from the decades pack and fired on three
Hendrix questions, which is the design of a guitar pack; default is now 3 and a
decades pack passes `--cap 2`. It flagged "guitar" against "guitarist" in a pack
about guitars, so common words are suppressed by frequency rather than by a
stoplist I would have had to guess. The stem-restating check punished short
stems, so it counts new ideas instead of overlap. A blurb naming another
question's answer in passing became a warning. And the common-word list was
computed from English and applied to Italian.

## v0.161.2 — Three wrong blurbs, and key signatures that overlapped

Reported from a real round, and the blurb fault was the important one.

- **The raised seventh was claimed on every minor chord.** The ii diminished in
  A flat minor is B flat, D flat and F flat, which contains nothing raised at
  all, and the blurb said otherwise. Only triads on degrees 3, 5 and 7 hold the
  leading tone, and only those say so now.
- **Cadence blurbs printed major numerals in minor keys**, so a minor plagal
  cadence was described as IV to I when it is iv to i. The numerals are now built
  from the triads themselves rather than written into the table.
- **The mode blurb claimed every mode is the same seven notes read from a
  different starting point.** That was true when modes were all white-note
  scales; since they generate from any root it is false. It now says a mode is
  named by its pattern of tones and semitones.

**Key signatures overlapped at five accidentals and piled onto the clef at
seven.** The step between them was narrower than the glyphs: a flat is 8.14 wide
against a 7.4 step, a sharp 8.96 against 8.2. Now 9.6 and 10.4, with the
signature starting clear of the clef.

A sweep now checks every generated blurb against the card it describes, across
roughly 100,000 questions: that the numerals match the mode, that a claimed
quality matches its own numeral, that a named degree count matches the answer,
that a signature count matches the drawing, and that no template hole prints
undefined. It comes back clean, and it caught two faults in ITSELF first, both
false positives from sloppy counting.

## v0.161.1 — Advanced Theory ended after one question

Reported from a real round, and the cause is worth writing down.

`mqCheckPackCleared` counts a pack's authored questions and returns true once the
player has seen them all. Advanced Theory has none, so total was zero, and a set
of size one is already greater than or equal to zero. The first question marked
the pack cleared, the round jumped to the win screen, and ten questions became
one. A generated-only pack can never be cleared, so zero total now returns false.

Three more from the same report:

- **Italics printed as literal tags.** The stems italicise foreign terms and the
  question element sets textContent. It now escapes everything and allows only
  `<i>` back, rather than switching to innerHTML, because the quiz can serve
  online questions that are not authored here.
- **Accidentals sat too close to the noteheads**, and the stacking gap was under
  the height of the glyphs it was separating. The gap before a head goes from 6
  to 9, the vertical clearance from 21 to 25, and the column spacing from 11 to
  12.5.
- **Advanced Theory had an emoji where every other pack has a line icon.** It now
  carries the Fundamentals book with a corner mark, so the pair reads as a set,
  and it sits to the right of Fundamentals in the grid rather than before it.

## v0.161.0 — Theory Fundamentals gets its written tier

Sixty authored questions, both languages, replacing the pre-restart set. Those
are archived in full under `theory_fundamentals_pre_rebuild` and restorable. All
sixty of them were "What is X?" definitional framing, and most are now covered by
a generated question type anyway.

Split 30 / 20 / 10. The easy tier is deliberately heavy, because that is the hole
the generators cannot fill: an easy generated question gives itself away through
its own small vocabulary, and a written question about what a fermata asks for
does not.

The pack now serves BOTH sources. `MQ_GEN_PACKS` says which packs receive
generated questions and `MQ_GEN_ONLY` says which have no authored tier at all,
which is Advanced Theory by design.

**The share was wrong at first.** MQ_GEN_SHARE is a share of the round, but the
code added a flat count to the pool, so once sixty written questions existed the
generated ones fell to 8 percent. The batch is now sized against the pack's own
authored count. Theory Fundamentals runs 59 percent written to 41 generated,
Advanced stays fully generated, and a round mixing Theory with Guitar Gods sits
at 23.

**Ten faults caught before shipping**, all by the audit scripts rather than by
eye:

- An appoggiatura answer 42 characters long against a 27-character field.
- Three questions sharing a distinctive word between stem and answer: bar line
  and "music", double bar and "piece", pedal point and "harmony".
- Six giveaways visible only in Italian, where the clefs are named after the
  instruments. "Which clef do guitar and violin parts use" answers itself when
  the answer is *chiave di violino*, so the Italian stems name a flute and a
  trombone instead.
- The clarinet question named its own answer in both languages. It now asks about
  a written D, so the answer is C.

**One giveaway left, and it is inherent.** *Col legno* means "with the wood" to
any Italian speaker, so the hard-tier question about it is easier in Italian than
in English. The same is true in reverse for *a cappella* in English. Some of that
is unavoidable in a bilingual music app.

## v0.160.1 — Seconds displaced

Two notes a step apart cannot share a column: the heads overlap. Engraving pushes
one of the pair sideways by a notehead width, which is now what happens. The
French augmented sixth was the visible case, since it holds a C and a D.

It deliberately does not chain. A run of three steps alternates rather than
marching further right with each note. Chords without a second, which is nearly
all of them, are untouched.

The rest of the layout engine is not being built: beaming buys almost nothing
here, because meter questions never offer 3/4 against 6/8 anyway, and multi-bar
melodic phrases would need every note to carry both a staff position and a
duration, plus stems, spacing, barlines, ties and a way to point at one note. Two
question types is not worth that.

## v0.160.0 — The six coverage gaps

Everything the audit said was missing.

- **All four clefs.** Treble only was half a syllabus; ABRSM sets bass from Grade
  1, alto at Grade 4 and tenor at Grade 5. Every pitched question now picks a
  clef and shifts by whole octaves to sit on it, so the spelling never changes.
  Alto and tenor stay in the hard tier.
- **Descending intervals**, which are half of what an exam asks and were entirely
  absent. Kept out of the easy tier, since reading one downwards is harder.
- **Minor keys for cadences and chord function.** Both stems used to say "reading
  the signature as a major key". A minor key raises its seventh, which the
  signature does not supply, so the triads are spelled rather than left to the
  signature. Roman numerals are now derived from what the triad actually is
  rather than read off a table, so `vii°` and `III+` come out right on their own.
  Harmonic minor's augmented third degree is excluded, because it is a fight
  nobody needs in a four-option question.
- **9/8 and 12/8**, and the meter tiers corrected against the syllabus: the
  compound meters are Grade 3, the irregular ones Grade 5.
- **Minor scales as scales.** Major, natural, harmonic and melodic minor, named
  from the page.
- **Chord-scale matching and progression identification** for Advanced, the two
  things a jazz student would look for first.

**Balance.** Simple meters moved into the easy tier, where the syllabus puts
them. The blanket ban was set when this pack was imagined for people who had
never played an instrument, which it is not, and it was starving d:1.

Fundamentals now holds 1750 unique across 193 / 720 / 923, Advanced 2115 across
1592 / 579 / 165. Inversions went from 0.4 percent of a round to 10.4, and the
worst single kind in one round is four out of ten.

## v0.159.0 — Chromatic harmony in any key

The last three hand-typed tables are formulas now.

| Topic | Was | Now |
|---|---|---|
| Chromatic harmony | 6 | 54 |
| Scale alteration | 5 | 60 |
| Double accidentals | 3 | 8 |

Chromatic harmony was the one that needed real work, because a chord tone has to
know what the SIGNATURE has already done to its letter. `mqShowAcc` answers that:
an alteration the signature supplies prints nothing, a natural note in a key that
alters its letter prints a natural to cancel it, and anything else prints its own
sign. So the German sixth in B flat major writes a flat on the G, nothing on the
B, a flat on the D and a natural on the E, and the same formula gives the right
answer in every key.

Verified against three hand-worked chords rather than by eye: the French sixth in
A flat, the German in B flat, and V/V in D.

Double accidentals are now generated from two real contexts, the raised seventh
of a minor key that already sharpens that letter and the seventh of a diminished
seventh chord, with wrong answers that are mistakes people actually make: the
pitch it sounds like, the same letter singly altered, and the neighbouring letter
doubled.

Totals: Fundamentals 704 unique, Advanced 821.

**A near miss worth recording.** The first attempt at this edit cut by line range
and silently deleted five generators, because a marker I searched for no longer
existed and the fallback matched a line inside the block I had just added. The
build still passed `node --check`; only a runtime smoke caught it. Redone with
cuts that assert a single match at both ends. Line numbers are not a safe handle
on this file.

## v0.158.0 — A speller, and the hand-typed tables become formulas

The audit found six topics sitting at seven unique questions or fewer, all of
them lists I had typed out rooted on C. Advanced Theory's whole hard tier was
thirteen questions, which repeats inside two rounds.

They were rooted on C because midi cannot say whether a pitch is an A sharp or a
B flat, and guessing wrong in a theory quiz is worse than not asking. So the
spelling is now COMPUTED. A note is a letter, an alteration and an octave; an
interval is a number of letters plus a number of semitones; add them and the
correct spelling falls out, double accidentals included. A formula that would
need a triple accidental on a given root simply drops that root.

Every one of those tables is now a formula applied across twelve roots:

| Topic | Was | Now |
|---|---|---|
| Modes | 7 | 84 |
| Jazz scales | 5 | 60 |
| Altered dominants | 4 | 45 |
| Exotic scales | 4 | 48 |
| Tritone substitution | 4 | 12 |

Advanced Theory's hard tier went from 13 unique to 117, and the two packs now
hold 642 and 714 unique questions.

**Two theory errors the generalisation exposed**, both invisible while everything
was rooted on C:

- The tritone substitution was being spelled as an augmented fourth, making A7's
  substitute D sharp 7 rather than E flat 7.
- Correcting that to a strict diminished fifth then gave E flat 7 a substitute of
  B double flat 7. Chord ROOTS are named for readability, not by letter
  arithmetic, so both spellings are now generated and the one with fewer
  accidentals wins. All twelve pairs verified against the expected answers.

Still thin and next in line: chromatic harmony at 6, double accidentals at 3, and
scale alteration at 5. All three are the same job again, and chromatic harmony
needs the generator to derive from the key signature which chord tones need an
explicit accidental and which are already covered.

## v0.157.1 — Written letters, and the altered scale

A note passed to `pitchedStaffSvg` may now be an object stating what to WRITE
rather than a midi number: `{ l:'F', o:4, a:'b' }`. Midi cannot express an F flat
at all, because the pitch is E, and deriving the position from the pitch puts the
notehead on the E line where a flat sign makes it E flat instead. Additive, so
every existing caller is untouched.

That was the last thing blocking the **altered scale**, the seventh mode of
melodic minor and the scale for a 7alt chord. It is in Advanced Theory's d:3 now,
correctly spelled with its F flat on the F line.

## v0.157.0 — Advanced Theory, a second pack

Difficulty is relative to a pack's audience, which is how the exam boards do it:
Grade 5 hard and Grade 8 hard are both called hard and nobody is confused,
because they are different exams. One three-rung ladder holding both a Grade 1
key signature and an altered dominant makes every rung mean two things.

So there are two theory packs now rather than a fourth difficulty tier, which
would have meant changing machinery every pack runs through in order to serve
one.

- **Theory Fundamentals**, roughly ABRSM Grades 1 to 5.
- **Advanced Theory**, Grade 6 to 8 through AP and into jazz. Its d:1 IS
  Fundamentals' d:3, so the two packs meet rather than leaving a cliff. d:2 is the
  chromatic harmony and double accidentals, d:3 the jazz vocabulary.

Both are generated-only and both ship at 1.0, which makes five packs at launch
and no extra authored questions to write.

Which generators a pack may use, and how a slot maps onto their content, is now a
per-pack profile rather than one global list. `mqIsAdvanced` keeps anything above
Grade 5 out of Fundamentals however it was generated, so widening a table later
cannot leak a ninth chord into the beginner pack.

New at the top:

- **Melodic minor and its modes**: melodic minor, lydian dominant, Locrian
  natural 2, and harmonic major.
- **Altered and extended dominants**: 7♯9, 7♭9, 7♯11 and 13.
- **Tritone substitution**, which needs no drawing because the question is the
  relationship.

`pitchedStaffSvg` now takes per-note spelling as well as per-column. Every
altered chord needs it: C7♯9 holds a B flat and a D sharp at once, and one
preference for the column gets one of them wrong whichever way it is set.

**The altered scale is deliberately absent.** It wants an F flat, and a flat sign
on the E position is not an F flat, it is a wrong note in the wrong place. That
needs the renderer to take a written letter rather than deriving it from midi.

## v0.156.0 — Real accidental paths, and accidental stacking

Two engraving faults, both spotted on device.

**The double accidentals were font text, not paths.** Everything else on that
staff is an extracted outline positioned so `translate(x, y)` lands on the note's
line. The doubles were Bravura text with two offsets typed in by eye, so they sat
off centre. Measuring them does not help: `getBBox` on SVG text returns the line
box, and a Bravura em box is nothing like its ink, which is why the notation deck
stores per-glyph metrics in the first place.

Fixed properly. The double sharp, double flat and natural outlines are now
extracted from the embedded subset at the same scale as `RR_SHARP`, one em to
four staff spaces with y flipped. The extracted sharp comes out ink 8.96 by
25.13 with its centre on the origin, matching the existing path exactly, which is
how I know the convention is right. Each carries a DX that right-aligns it
against the sharp, since a double flat is nearly twice as wide.

**Accidentals in a chord all sat at the same x.** Three of them inside a sixth
overlapped, which is what made the augmented sixths look cramped. Engravers stack
them in columns: highest closest to the noteheads, anything that would collide
vertically pushed one column further left. That is now what happens. A chord with
one accidental, which is nearly all of them, is unaffected.

Still outstanding: noteheads a second apart want horizontal displacement, which
the French augmented sixth needs, since it holds a C and a D.

## v0.155.0 — Double accidentals, and the top of the ladder

`pitchedStaffSvg` now takes `opts.accs`: an explicit accidental per note instead
of one derived from midi. Three things needed that and none can be spelled from a
pitch number. A double sharp or flat, which midi cannot tell from the plain note a
tone away. A natural, which only means anything against a key signature. And the
empty string, which suppresses a sign the signature has already supplied, without
which a chord in a sharp key prints every accidental twice.

The change is additive: anything not listed falls through to the derived
spelling, so Staff Notes and the Chords tool are untouched. Sentinel confirms.

Unlocked by it, all Grade 6 to 8, AP or college:

- **Secondary dominants**, V/V and V/vi.
- **The Neapolitan sixth**, and the Italian, French and German augmented sixths,
  with the wrong answers drawn from the same family, since telling a French from
  a German is the actual skill.
- **Double accidentals in context**: the raised seventh of G sharp and D sharp
  minor, and the seventh of a diminished seventh chord.
- **Diminished seventh chords**, which were deliberately absent for two versions
  because C diminished seventh wants a B double flat and the speller wrote A
  natural.

Bravura already carried E263 and E264 for the notation deck, so the glyphs are
drawn as font text rather than extracted paths, the same fallback the Chords tool
uses for the alto and tenor clefs.

Chromatic harmony is C major only for now. In a key with a signature every chord
tone needs an explicit accidental or an explicit blank, and one wrong entry
prints a sign that is not there.

## v0.154.0 — A hard tier that is actually hard

Ten questions on hard did not feel hard. Measured against the published
syllabuses, our d:3 topped out around ABRSM Grade 4. `THEORY_LADDER.md` records
the mapping and the sources.

Added, all of it Grade 5 or above:

- **Cadences.** Perfect, plagal, imperfect and deceptive, drawn as two triads
  with the signature supplying the accidentals. ABRSM sets these at Grade 5 and
  AP tests deceptive cadences directly.
- **Compound intervals** to a major thirteenth. Grade 5.
- **Seventh chord inversions**, which is the only way a third inversion can come
  up at all.
- **Ninth chords**: dominant, major, minor, and the flat ninth. College level and
  the jazz end of the vocabulary.
- **Whole tone, both pentatonics and the blues scale.** The first three are on
  the AP list.
- **Key range opened to seven accidentals** for scale degree and chord function,
  which were capped at five.

Also: the mode question wording is now just "What mode is this?".

Two faults caught in testing. The interval pair finder assumed everything fit
inside one octave, so no compound could ever generate. And restricting triad
inversions to three sensible answers left the card with three options instead of
four, when a third inversion is a perfectly fair wrong answer for a triad.

**Diminished sevenths are deliberately absent.** C diminished seventh wants a B
double flat and this speller writes A natural, which would be wrong on the page.
Double accidentals need a glyph before they can have questions.

## v0.153.1 — Tiers become tendencies, and one shared picker

Noticed on device: each difficulty only ever asks for certain things, so an
early question in a round can be answered without reading it. An easy chord card
was always major or minor.

- **One `mqTierPick` for every generator.** Each type rolled its own filter, which
  is how two of them leaked d:1 cards, and how every tier ended up a wall.
- **Content spills one tier either way, a quarter of the time**, and the question
  is tagged with the tier of the CONTENT, never the tier of the slot that asked.
  A diminished triad is a d:2 question wherever it turns up.

**This does not fix what was noticed, and cannot.** With a small vocabulary the
tier and the answer set are the same thing: if the only easy chords are major and
minor, an easy chord card gives itself away no matter how it is selected. The fix
is more to choose from, which is the authored text tier.

One measured side effect: because most generated content sits at tier 2, the
served mix now runs about 18/70/14 against the 40/40/20 the batch asks for, so
an easy round is slightly less easy than the blend intends. That corrects itself
as the text tier fills the easy end.

## v0.153.0 — Six more generated types

Nine in total now. All of them draw with `pitchedStaffSvg`, which takes a
sequence of columns; the first three only ever used one, so a scale or an
interval costs nothing new to draw.

- **Interval on the staff.** Two notes, name the distance. Taken between naturals
  only, because a sharp makes augmented and diminished spellings ambiguous from
  midi alone.
- **Altering a scale.** C major is drawn and the ask is which notes to lower to
  make it Dorian, Phrygian, natural or harmonic minor, Mixolydian. Every wrong
  answer is another scale's alteration, so all four options are true of
  something.
- **Mode from the starting note.** White notes from D to D, name the mode.
- **Scale degree.** Signature plus one note: tonic, mediant, leading tone.
- **Chord function.** Signature plus a triad: which degree of that key. Written as
  naturals with the signature supplying the accidentals, the way Staff Notes
  does it, so a chord in five sharps needs no inline signs and cannot be
  misspelled.
- **Enharmonics.** Written one way, name it the other.

Two faults the tests caught, neither of which any existing audit could see:

- **The octave interval never generated.** Stepping seven letters lands on the
  same letter, so the high note equalled the low one and the semitone check
  failed silently. A tier can be missing a member and look perfectly healthy.
- **Chord function and scale degree were dealing d:1 cards.** Their key filter was
  a ternary with only two arms, so the easy tier fell through to the hard one and
  offered a five-flat signature as an easy question.

Round mix across forty rounds is now roughly even across all nine, and the worst
single kind in one round dropped from seven to three.

## v0.152.2 — Generated blurbs rewritten

They were templated and padded, with a moral tacked on the end of each one.

- Key signatures now name the actual accidentals: "Three sharps, F C G. A major,
  or F sharp minor."
- Chords carry their own line rather than a list of semitone counts.
- Inversions say which note is in the bass for THAT card instead of reciting all
  three cases.
- Meter names the twin it can never be offered against, so the constraint that
  keeps 3/4 and 6/8 apart becomes the thing the blurb teaches.
- Italian accents restored throughout the generated strings.

## v0.152.1 — Generated question mix

Reported from a real round: six of ten were chord questions.

- **Rotation let the deepest well win.** A kind only gave up its turn when it
  failed, so once the key signatures in a round were spent, chords filled the
  rest. Each slot now starts with whichever kind has been used least.
- **A hard ceiling per kind**, so a batch comes back short rather than handing
  every leftover slot to meter, which has unlimited variants.
- **Minor keys from d:2 up**, not d:3 only. The medium tier had four possible
  signature questions against nine chords.

Batch mix is now even, about 7/6/7 in twenty. Across forty rounds the served mix
is roughly 30 percent signatures, 26 chords, 43 meter. Meter still leads because
at d:2 it is the only kind with unlimited variants; the fix for that is more
medium-tier content, not more shuffling.

## v0.152.0 — Generated questions, and Theory opens

Three question types that are BUILT rather than written. The generator picks the
answer first and then draws it, so the picture and the correct option are one
decision and cannot disagree.

- **Key signature**: name the major or minor key from the signature. Reuses
  `pitchedStaffSvg` and the `SR_KEYS` table Staff Notes already uses.
- **Chord on the staff**: name the quality, or at d:3 the inversion. Roots are
  restricted to the ones that spell correctly from midi alone, because F
  diminished wants a C flat and this speller writes B natural.
- **Meter**: a bar drawn WITHOUT its time signature; add up the note values.

**Theory is now playable and serves generated questions only.** Its authored
questions predate the restart, so `MQ_GEN_ONLY` keeps them out of the pool
entirely until the text tier is written.

Four faults the validator caught before this shipped:

- **Ambiguous meter options.** Filtering distractors against the answer's length
  was not enough: 3/4 and 6/8 hold the same music, so two wrong answers could be
  indistinguishable from each other. All four options now differ in length.
- **Meter tagged easy.** With no meters at tier 1 the generator fell through to
  the whole table and labelled reading note values a d:1 question.
- **Kind skew.** Random choice plus deduplication gave 199 meter questions out of
  240, because meter has endless variants and key signatures have thirty. Kinds
  now rotate.
- **The batch stalled at 18.** The tier index came from the output length, so once
  a tier ran out of unique questions it was retried forever. Slots are now
  bounded and skipped, and the easy tier was widened from seven possible
  questions to about twenty.

Also: the staff ink is a CSS variable rather than a colour baked at build time,
so it follows a theme switch mid-round. And the miss review was printing English
stems in Italian and passing an undeclared `opts` to the trimmer, which a
generated question made obvious, since without its drawing the stem says nothing.

## v0.151.1 — COMING SOON on the compact pack cards

- The big pack grid already swapped the description for a COMING SOON tag. The
  two compact grids did not: a locked pack was only dimmed, with no reason given.
  Both now carry the tag under the name.
- **Survival pack grid was not applying the lock at all.** Locked packs rendered
  at full brightness, advertised a question count like `57Q`, and did nothing
  when tapped, because only the toggle function was guarded. It now dims, tags,
  and drops the count, since a count on a pack you cannot draw from is a promise
  the app does not keep.
- Card height is unchanged for single-line pack names. Names that already
  wrapped to two lines grow by about 12px, which is inside the sheet layout.

## v0.151.0 — Guitar Gods rebuilt from scratch

The pack was written fresh under QUIZ_SPEC section 12 rather than revised. The
old hundred questions are archived verbatim in `quiz_removed.json` under
`guitar_gods_pre_rebuild` and can be restored if anything is wanted back.

- **60 questions, 24 easy / 24 medium / 12 hard**, every one tagged `d:1`,
  `d:2` or `d:3`, and bilingual from birth. No question was carried over.
- **Correct answer index spread evenly**, 15 questions at each of the four
  positions, so position tells a player nothing.
- **Every date, name and number checked against sources.** Nine claims were
  softened or corrected in the process: the duck walk is "usually credited" to
  Chuck Berry because T-Bone Walker was crouching with a guitar in the 1930s;
  Greeny is a reversed pickup MAGNET, not out-of-phase wiring; the Marshall
  stack came from cutting an 8x12 cabinet in half; Link Wray went at the
  tweeters and left the main speaker alone; the Don't Worry fuzz was a
  transformer failing in the console, not an amp; Rosetta Tharpe's white SG is a
  1960s guitar and the blurb no longer implies she had it in the 1940s;
  Vaughan's "13s" were a custom set and he went lighter when his hands were
  bad; the Satisfaction blurb omits the hotel because Richards names a different
  place in his own memoir than the sources do; and the Black Mountain Side blurb
  states what each man actually credited rather than calling it theft.
- **One option set rebalanced** after the validator caught it: the St. Vincent
  answer ran 51 characters against distractors of 16 to 31, which gives the
  question away on shape alone.
- Gates: sentinel 97 fixes + 247 pins, backup audit, stopall audit, quiz style
  (0 tells), quiz leak (0), livecheck (60 questions, 0 missing Italian, 0 broken
  indices, 0 giveaways), node --check on all 9 script blocks, headless smoke in
  both languages with a clean console.

## OPEN ITEMS (as of v0.104.0)

Not a release entry. A standing list so these survive outside anyone's memory.

**Road Trip: 21 songs need their legs tuned on device**

clair_de_lune, prelude_em, moonlight, liebestraum, fuer_elise, moonlight_3,
prelude_c, alla_turca, barcarolle, butterfly, fantaisie_impromptu, moonlight_2,
prelude_csharp, prelude_op23, raindrop, sonata_facile, to_spring, traumerei,
troika, waldstein_1, wedding_day.

That is exactly the set with a perf: block, and it is not a coincidence. Hooks
were placed as beat positions against the grid; converting to performance mode
replaced the timing wholesale, so every one of them is either analytic or stale.
RT_TUNED is still empty. Long-press the ROAD TRIP title to open the Leg Tuner,
tune, then add the id to RT_TUNED and pin its line in the sentinel.

The 17 grid songs were hand-tuned by ear and are now pinned (v0.104.0), so a
silent drift becomes a build failure rather than a lucky catch.

**Housekeeping**

`intonare_groove_audit.py` still needs copying into `/mnt/project/`. It ships to
outputs on every build but does not persist, and it already had to be rebuilt
from scratch once for exactly this reason. The same now applies to the sentinel:
v0.104.0 added 17 pins, so the copy in the project must be replaced or those
pins vanish on the next fresh chat.

RESOLVED: groove patterns are pinned. The Toussaint six, maqsum and the flamenco
pair went into the sentinel, which is why Bulería cannot silently revert again.

**On-device listening, ordered by how much actually changed**

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
