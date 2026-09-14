# Intonare — Instrument Chart Audit Ledger

Purpose: a single, honest record of which instrument charts have been verified
against credible sources, by what method, and what remains. This is the
"worry-free coverage" document. Status is per instrument×variant.

Legend:
- ✅ VERIFIED — checked against a named credible source, value confirmed correct
- 🔧 FIXED — error found and corrected during audit (see note)
- ⏳ PENDING — not yet audited
- 🖼️ NEEDS IMAGE — verification needs a chart image the sandbox can't load (Daniele uploads)
- 🧭 CONVENTION — value depends on a judgment call; decision logged

Verification method:
- COMPUTED — deterministic (tuning math, fret arithmetic, keyboard = 1 key 1 note)
- TEXT — confirmed against a text/credible web source
- IMAGE — confirmed against a chart image
- PLAYER — would benefit from a player's eyes (low confidence otherwise)

Last updated: 2026-06-19 · app version 0.67.x

---

## TIER 1 — Strings & Keyboards (deterministic, low risk)

### Fretted / plucked tunings

| Instrument | Variant | Status | Method | Source / Note |
|---|---|---|---|---|
| Guitar | standard EADGBE | ✅ | TEXT | E2 A2 D3 G3 B3 E4 confirmed (guitartuner.io, gtdb). |
| Guitar | baritone (B-B) | ✅ | TEXT | B1 E2 A2 D3 F#3 B3, down P4. B-standard is common default (A-standard also exists). guitarguitar/Stringjoy confirmed. |
| Guitar | tenor CGDA | ✅ | TEXT | fifths tuning |
| Bass | 4-string EADG | ✅ | TEXT | E1 A1 D2 G2 confirmed (StringsByMail tuning chart). |
| Bass | 5-string BEADG | ✅ | TEXT | B0 E1 A1 D2 G2 confirmed (StringsByMail; Wikipedia Standard Tuning). |
| Bass | 6-string BEADGC | ✅ | TEXT | B0 E1 A1 D2 G2 C3 confirmed (StringsByMail). |
| Ukulele | soprano (re-entrant gCEA) | ✅ | TEXT | G4 C4 E4 A4 re-entrant confirmed (Kala, ukulele-arts). |
| Ukulele | tenor (low-G GCEA) | ✅ | TEXT | G3 C4 E4 A4 linear low-G confirmed (Kala, get-tuned). |
| Ukulele | baritone DGBE | ✅ | TEXT | D3 G3 B3 E4 linear confirmed (Kala baritone guide). |
| Ukulele | U-bass EADG | ✅ | TEXT | E1 A1 D2 G2, same as bass guitar. |
| Mandolin | GDAE | ✅ | TEXT | G3 D4 A4 E5, = violin (StringsByMail, orchestral sources). |
| Mandola | CGDA | 🔧 | TEXT | **FIXED**: was GDAE (octave-mando tuning). Now C3 G3 D4 A4 = viola pitches, per Wikipedia/Mando references. Note: continental EU sometimes calls the GDAE instrument "mandola"; US/UK/Irish standard is CGDA. |
| Mandocello | CGDA | ✅ | TEXT | C2 G2 D3 A3, fifth below mandola |
| Octave mandolin | GDAE | ✅ | TEXT | G2 D3 A3 E4, octave below mandolin |
| Banjo | 5-string open G (gDGBD) | ✅ | TEXT | D3 G3 B3 D4 + g4 high drone, correctly placed as highest. Lost Lake/McNeela confirmed. |
| Lute | Renaissance 6-course | ✅ | TEXT | G2 C3 F3 A3 D4 G4, confirmed |
| Lute | Renaissance 7-course | ✅ | TEXT | F2 G2 C3 F3 A3 D4 G4 = 6-course G + low F. Confirmed (Thomann, Aquila, Early Music Shop). Note: Dowland often used D for the 7th course; F is also standard. Both valid; app's F is fine. |
| Lute | Baroque (D-minor) | 🔧 | TEXT | **FIXED**: now A2 D3 F3 A3 D4 F4 (D-minor accord nouveau, top-down f-d-a-F-D-A). Was a G-flavored hybrid. Source: Wikipedia, Mateus Lutes, Lute Society. |
| Lute | Theorbo | 🔧 | TEXT | **FIXED**: now theorbo in A — A2 D3 G3 B3 E3 A3 (top two courses dropped an octave). Added explicit re-entrant override [4,5] + made the re-entrant detector and 2-oct-hide logic handle trailing dropped courses (not just leading uke-style). Uke/guitar detection unchanged. Source: Tempesta di Mare, LSA, Lynda Sayce. |
| Lute | Mandore | ✅ | TEXT | G3 C4 E4 A4 |
| Bouzouki | Irish GDAD | ✅ | TEXT | G2 D3 A3 D4 confirmed (StringsByMail Irish GDAD). |
| Bouzouki | Irish GDAE | ✅ | TEXT | G2 D3 A3 E4 confirmed (StringsByMail Irish 5ths). |
| Bouzouki | Irish ADAD | ✅ | TEXT | A2 D3 A3 D4 confirmed as real Irish variant (Muzikkon, Ayan). |
| Bouzouki | Greek 3-course DAD | ✅ | TEXT | D3 A3 D4 trichordo confirmed (Muzikkon, Wikipedia). |
| Bouzouki | Greek 4-course CFAD | ✅ | TEXT | C3 F3 A3 D4 tetrachordo, Hiotis ~1956 confirmed (Wikipedia Irish bouzouki, academickids). |
| Bouzouki | Cittern CGDAD | ✅ | TEXT | English/Celtic CGDAD confirmed standard |

### Bowed strings

| Instrument | Variant | Status | Method | Source / Note |
|---|---|---|---|---|
| Violin | GDAE | ✅ | TEXT | G3 D4 A4 E5 confirmed (Wikipedia Standard Tuning). |
| Viola | CGDA | ✅ | TEXT | C3 G3 D4 A4, fifth below violin (Wikipedia). |
| Cello | CGDA | ✅ | TEXT | C2 G2 D3 A3, octave below viola (Wikipedia). |
| Double bass | EADG (fourths) | ✅ | TEXT | E1 A1 D2 G2, ascending fourths (Wikipedia). |

### Keyboards / chromatic percussion

| Instrument | Variant | Status | Method | Source / Note |
|---|---|---|---|---|
| Piano | standard | ✅ | N/A | Interactive chromatic keyboard, not a fixed-range chart instrument. 1 key = 1 real note by construction; range is a scrollable view, not a transposition claim. Nothing to verify. |
| Organ | standard | ✅ | N/A | Same as piano — chromatic keyboard layout, non-transposing, no verifiable convention. |
| Melodica | standard | ✅ | N/A | Same as piano — chromatic keyboard, non-transposing. |
| Mallet | glockenspiel | ✅ | — | TRACED — not a bug. MALLET_RANGES drives ONLY the cosmetic bar-taper, not labels or playback. Notes come from selected octave+root directly; app treats mallets as non-transposing (shown/played C is a real C). Misleading comment fixed (v0.67.8). Octave transposition deliberately not modelled — pitch-accurate learning layout. |
| Mallet | xylophone | ✅ | — | Same trace as glock — MALLET_RANGES is taper-only, non-transposing layout. Not a bug. |
| Mallet | marimba | ✅ | TEXT | C2–C7, non-transposing (5-octave). Correct. |
| Mallet | vibraphone | ✅ | TEXT | F3–F6, non-transposing. Correct. |
| Harp | standard | ✅ | — | Pedal logic exhaustively verified + fixed this session (v0.67.6/.7). Diatonic strings + 7 pedals; backtracking assigner correct. |

---

## TIER 2 — Brass & Woodwind fingerings (higher risk, named sources needed)

### Brass (valve combinations / slide)

| Instrument | Variant | Status | Method | Source / Note |
|---|---|---|---|---|
| Trumpet | Bb standard | ✅ | TEXT | WIND_FINGERINGS 3-valve map matches canonical chart exactly (fingeringchart.org, spinditty, mysterytomastery). Physics confirmed: V1=-2, V2=-1, V3=-3. C# uses 1+2+3; E/A use 1+2 (correct default, not the sharp 3-alt). |
| Trumpet | piccolo | ✅ | TEXT | Same 3-valve map; piccolo's 4th valve (range extension) not modelled — fine simplification. Concert range F#4–C7. |
| Flugelhorn | standard | ✅ | TEXT | Same fingerings as trumpet, confirmed (spinditty: chart covers cornet/flugelhorn/baritone/euphonium/tuba). Concert range E3–Bb5. |
| French horn | F standard | ✅ | TEXT | Shares the 3-valve pc→valve map (rotary, but same semitone system). Double-horn Bb side / thumb valve not modelled — fine for a learning baseline. |
| French horn | contrabass | ⚠️NOTE | TEXT | REAL but FRINGE — a contrabass horn exists (stands a 4th below F), but builders call it 'a new instrument'; not standard orchestral. Defensible to list, but obscure for a learning app. Your call whether to keep. Not a bug. |
| Euphonium | standard | ✅ | TEXT | 3-valve map correct as the standard baseline. 4th valve (replaces 1+3, better intonation + range) is an enhancement not modelled — fine. Concert Bb1–C5. |
| Tuba | BBb | ✅ | TEXT | Same 3-valve map (Britannica/West Music confirm 3-valve baseline; 4th/5th valves are intonation aids). Concert range Bb0–F4. |
| Trombone | tenor | ✅ | IMAGE+TEXT | Tunable/Wikibooks charts, full range verified |
| Trombone | soprano | ✅ | TEXT | shares slide logic, octave up |
| Trombone | bass (F/D) | 🔧 | IMAGE | **FIXED**: low register was all pos-1. Now full Tunable + Christian Waage F/D chart. Pedal notes B1=TT6, C2=T7, etc. NOTE: chart is F/D config; F/Gb differs on some pedal notes (see Open Questions). |

### Woodwind (fingering tables)

| Instrument | Variant | Status | Method | Source / Note |
|---|---|---|---|---|
| Flute | C concert | ✅ | TEXT | First octave (B3–C#5) verified note-by-note against WFG closed-G# Boehm chart — all 15 correct incl. forked F#, 1-and-1 Bb, closed-G# key, universal Eb key. MIDI-keyed across 3 octaves with documented alternates (Briccialdi/side Bb, gizmo). |
| Flute | piccolo | ✅ | TEXT | Same Boehm fingerings as flute (WFG: identical for piccolo/concert/alto/bass). Sounds 8va up — octave display, not a fingering difference. |
| Flute | alto | ✅ | TEXT | Same fingerings; sounds P4 down (G transposition). wwTransposition handles the offset; fingering identical to concert flute. |
| Clarinet | Bb | ✅ | TEXT | Chalumeau (E3-F4) verified note-by-note vs WFG Boehm chart — all 13 correct (LH/RH E+F key pairs, fork F#, C# spatula). CRITICAL: clarion register correctly = chalumeau fingering + register key, overblowing a TWELFTH (19 semitones) — verified all 13 clarion notes B4-C6. Throat tones (G#/A/Bb) correct + throat/side Bb alts. MIDI-keyed table is live path; pc table fallback. Transposition Bb−2/A−3/Eb+3/bass−14 correct. |
| Clarinet | A | ✅ | TEXT | Same fingerings as Bb (WFG: identical all sizes). Transposition −3 correct. |
| Clarinet | Eb | ✅ | TEXT | Same fingerings. Eb sopranino +3 (sounds m3 HIGHER) correct. |
| Clarinet | bass | ✅ | TEXT | Uses BASS_CLARINET_FINGERINGS (verified separately). Transposition −14 correct. |
| Bass clarinet (standalone) | — | ✅ | TEXT | Primary fingerings byte-identical to verified soprano clarinet (same Boehm system, confirmed vs WFG). Transposition −14 correct. Minor: standalone uses pc-table (no octave-accurate twelfth-break MIDI path soprano has) — data correct, less register-nuanced. |
| Saxophone | soprano | ✅ | TEXT | First octave verified note-by-note vs WFG sax chart — all 12 correct (fork F#, G# spatula, low C/C# keys). bis Bb primary + 1-and-1/long-Bb alts (WFG-standard). Transposition −9/−14/−2/−21 (alto/tenor/sop/bari) all correct; wwGetFingering applies concert→written conversion properly (NOT the brass bug). Same fingerings all 4 sizes per WFG. |
| Saxophone | alto | ✅ | TEXT | First octave verified note-by-note vs WFG sax chart — all 12 correct (fork F#, G# spatula, low C/C# keys). bis Bb primary + 1-and-1/long-Bb alts (WFG-standard). Transposition −9/−14/−2/−21 (alto/tenor/sop/bari) all correct; wwGetFingering applies concert→written conversion properly (NOT the brass bug). Same fingerings all 4 sizes per WFG. |
| Saxophone | tenor | ✅ | TEXT | First octave verified note-by-note vs WFG sax chart — all 12 correct (fork F#, G# spatula, low C/C# keys). bis Bb primary + 1-and-1/long-Bb alts (WFG-standard). Transposition −9/−14/−2/−21 (alto/tenor/sop/bari) all correct; wwGetFingering applies concert→written conversion properly (NOT the brass bug). Same fingerings all 4 sizes per WFG. |
| Saxophone | baritone | ✅ | TEXT | First octave verified note-by-note vs WFG sax chart — all 12 correct (fork F#, G# spatula, low C/C# keys). bis Bb primary + 1-and-1/long-Bb alts (WFG-standard). Transposition −9/−14/−2/−21 (alto/tenor/sop/bari) all correct; wwGetFingering applies concert→written conversion properly (NOT the brass bug). Same fingerings all 4 sizes per WFG. |
| Oboe | standard | ✅ | TEXT | First octave Bb3-A4 verified vs WFG oboe chart — 11/12 exact. Eb4: app uses LH-Eb key, WFG basic uses RH-Eb key — BOTH are standard oboe Eb fingerings (WFG lists LH-Eb as documented alt on same note), defensible primary choice not error. Octave system correct: half-hole vent C#5-Eb5, Oct I key E5-G#5, Oct II key A5-C6 (matches WFG + Wikipedia register-key). Models conical-bore octave behavior properly. |
| Oboe | cor anglais | ✅ | TEXT | Same fingerings as oboe (WFG: identical oboe/English horn). Transposition −7 (P5 lower) correct. Verified separately as COR_ANGLAIS table. |
| Cor anglais (standalone) | — | ✅ | TEXT | First-octave + oct2 fingerings byte-identical to verified oboe (correct — WFG: oboe/English horn share fingering system). Transposition −7 (P5 lower, F instrument) correct. Same octave-key/half-hole structure. |
| Recorder | soprano/descant | ✅ | TEXT | First octave verified against WFG (woodwind.org), the cited source. Correct ENGLISH/BAROQUE fingerings: forked F (T123 4_67), forked Bb (T1_3 4). Baroque-vs-german alts present for F/F#. NOTE: low C#=C and Eb=D is CORRECT per WFG (those lowest semitones genuinely share the natural's fingering), not a placeholder bug — verified, not assumed. |
| Recorder | alto/treble | ⚠️→✅ FIXED v0.67.12 | TEXT | **BUG FOUND & FIXED.** Alto is an F recorder (all-holes-closed=F), using same fingering SHAPES as soprano's C. App's pc lookup used writtenPc=concertPc (ignored transposition) so alto showed C-recorder fingerings — wrong. Fixed: F-recorders get +5 pc shift → sounding F maps to soprano C entry. Verified F/G/A/Bb/C map to correct shapes. Also fixed oct2 register threshold (was 67, now lowest+12=65). Confirmed F-recorder fact vs Wikipedia + WFG. |
| Recorder | tenor | ⚠️→✅ FIXED v0.67.12 | TEXT | Fingerings correct (C recorder, same as soprano, pc unaffected). But oct2 register threshold was 72 (an octave too high — tenor lowest C3, 2nd reg should start C4=60). Fixed via lowest+12 rule → now 60. |
| Recorder | bass | ⚠️→✅ FIXED v0.67.12 | TEXT | **BUG FOUND & FIXED.** Bass is an F recorder — same pc-mapping bug as alto (showed C-recorder fingerings). Fixed via +5 F-recorder pc shift. Bass oct2 threshold was 77 (badly wrong — two octaves up); fixed to lowest+12=53. Note: alto & bass both need +5 pc shift despite different octave-transpositions (-5 vs +5), since pc mapping is mod-12 — naive wwTransposition() would have broken bass. |
| Tin whistle | D | ✅ | TEXT | All 7 naturals (D-major + C#) match standard 6-hole D whistle exactly. Accidentals use half-holing (the standard chromatic approach on 6-hole whistle). Verified vs standard chart + WFG cited. |
| Tin whistle | low D | ✅ | TEXT | Same fingering pattern as D whistle (low D is the same instrument an octave down). |
| Bassoon | standard | ⚠️→✅ FIXED v0.67.11 | TEXT | **BUG FOUND & FIXED.** All three register tables (base Bb1–A2, oct2 Bb2–B3, oct3 C4–B4) had wrong main-hole patterns from E2 up — used flute-style lift-fingers instead of bassoon's all-holes-closed-plus-keys reality. Bb1–Eb2 were correct; E2–B4 were wrong. Rebuilt all three from WFG Heckel charts (basn_bas_1/2/3): correct holes, half-hole LH1 venting (F#3/G3/G#3/G4/G#4), whisper-key + flick logic intact. Every note re-verified vs WFG hole-truth. node✓ sentinel✓. |
| Contrabassoon | — | ✅(diagram) | IMAGE | FDB import done — re-confirm |
| Ocarina | standard (12+7 hole) | ✅ | TEXT | Structurally correct. Home note C5 (all main closed, subholes open) ✓; natural lift sequence monotonic C5→G5 (covered count 10→6, right-to-left lift) matches Helmholtz total-open-area principle (Pure Ocarinas); subhole descent A4(both)/B4(one)/C5(none) correct; continuous no-register-break model correct; 7-hole same structure verified. MINOR: low Bb4 shares B4 fingering — genuinely awkward/maker-variable accidental on real 12-hole ('don't worry about low Bb' per TON), honest approximation not a bug. |
| Harmonica | diatonic Richter, 12 keys | ✅ | TEXT | All 10 holes blow+draw verified note-by-note vs canonical Richter C tuning (Blow C E G C E G C E G C / Draw D G B D F A B D F A). Includes the genuine Richter quirks: missing low F/A, octave anchors C4/C5/C6/C7, upper-octave draw pattern. 12 keys = correct semitone-offset transpose. harmonicaFindNote reads arrays directly + honestly reports 'not available' for unbendable notes. |
| Chromatic harmonica | standard | ✅ | TEXT | Hohner Chromonica solo tuning verified (Blow C E G C.../Draw D F A B...); holes 1–4 give full C-major scale C D E F G A B C (correct solo-tuning hallmark, vs Richter's gaps). Slide = +1 semitone to all reeds (correct chromatic mechanism). |

---

## TIER 3 — Other / convention-dependent

| Instrument | Status | Note |
|---|---|---|
| Didgeridoo | ✅ (drone) | Correctly modeled as a drone — no fingerings/note-grid (right call). Synth F0=D2 (73.42Hz), the common beginner key, with odd-harmonic emphasis + circular-breathing/breath LFOs + fixed formant filters. FIXED learn-tab range text: was 'C1 to G1' (an octave too low); now 'A2 to G3' per Wikipedia (fundamental A2–G3) + maker sources (common keys C–E ≈ C2–E2, C didge = 2 oct below middle C). IT body has no range claim, left as-is. Prior session also fixed two formant comments. |

---

## OPEN QUESTIONS / DECISIONS NEEDED FROM DANIELE

1. **Bass trombone valve config**: app now uses F/D (Doug Yeo / Waage chart). The
   other common config is F/Gb, which differs on a few pedal notes. Confirm F/D is
   the intended standard, or specify F/Gb.
2. **Recorder fingering system**: baroque (English) vs German fingering differ.
   Which should the charts show? (Baroque is the modern default.)
3. **Ocarina system**: which ocarina (12-hole English/Pacchioni, 4-hole, etc.)?
4. **French horn contrabass**: confirm this is a real intended variant or a stray entry.
5. **Baroque lute tuning**: RESOLVED — retuned to true D-minor (option a). ✅
6. **Archlute / 13-course baroque**: DECIDED not to add. On a fingering chart their
   fretted courses are identical to existing entries (Renaissance 6 and Baroque
   respectively); the only difference is unfretted bass diapasons, which a fingering
   diagram can't show. Revisit if diapason display is ever added to lute diagrams.
7. **Theorbo renderer**: RESOLVED — added explicit re-entrant override + generalized
   detection. Correct A tuning now applied. ✅
8. **Diapason support** (open question): adding the unfretted bass courses would make
   archlute/theorbo/13-course meaningfully distinct on the chart. Doable (~half-day):
   needs data, a renderer element for off-fretboard open strings, and a constraint in
   the voicing/scale builders so diapasons only play their open pitch. Caveat: real
   diapasons are retuned per-piece, so any shown tuning is one representative choice.
   Deferred as a deliberate future feature, not a quick add.

---

## ERRORS FOUND SO FAR (running list)

1. **Bass trombone low register** — every note below ~E2 defaulted to Position 1.
   Fixed v0.67.0–0.67.1 with full sourced chart.
3. **Mallet transposition labels** — `MALLET_RANGES` comment says "written pitch"
   but glockenspiel/xylophone values are the SOUNDING range. Either the comment is
   wrong or the values need an octave shift, depending on how the range is consumed.
   FLAGGED, not yet fixed — needs a trace of the mallet pitch path.

4. **Baroque lute tuning** — was a G-flavored hybrid, not standard D-minor baroque.
   FIXED to A2 D3 F3 A3 D4 F4.
5. **Theorbo tuning** — was a re-entrant Renaissance-G, not a real theorbo. FIXED to
   theorbo in A (A2 D3 G3 B3 E3 A3) + generalized the re-entrant renderer to handle
   trailing dropped courses via an explicit override. Uke/guitar behavior preserved.

---

## SCALE SYSTEM AUDIT (v0.67.5)

### Existing 12 scales — all VERIFIED correct (interval patterns match standard theory)
major, dorian, phrygian, lydian, mixolydian, aeolian (natural minor), locrian,
harmonic minor, melodic minor, major pentatonic, minor pentatonic, blues.
Checked against canonical interval sets; all exact.

### Architecture finding
Chords are universal (pitch physics — a G chord is G+B+D on every instrument, cannot
differ). Scales are the only place traditions genuinely differ. The app applied ONE
global Western scale set to every instrument — correct but Eurocentric/incomplete for
instruments with their own modal traditions.

### Added: 6 world scales (all 12-TET expressible, sourced)
| id | name | intervals | source |
|----|------|-----------|--------|
| phrygdom | Phrygian Dominant (Hijaz/Freygish) | 0,1,4,5,7,8,10 | Wikipedia; 5th mode harmonic minor |
| dblharm | Double Harmonic (Byzantine/Bhairav) | 0,1,4,5,7,8,11 | Wikipedia, filmmusictheory |
| hungmin | Hungarian Minor | 0,2,3,6,7,8,11 | filmmusictheory |
| hungmaj | Hungarian Major | 0,3,4,6,7,9,10 | Wikipedia |
| hirajoshi | Hirajoshi (Japanese koto) | 0,2,3,7,8 | pianoscales.org, filmmusictheory |
| wholetone | Whole Tone | 0,2,4,6,8,10 | standard |

NOT added: quarter-tone maqamat (Bayati etc.) — cannot be expressed in 12-TET semitones.
Deliberate equal-temperament limitation, documented.

### Added: per-instrument scale-group ordering system
- New 'World' group in GSS_SCALE_GROUPS; groups now carry an `id`.
- GSS_INSTRUMENT_SCALE_ORDER: per-instrument group order. 'lead' groups render
  open/first; the rest collapse under a "More scales" toggle. Cross-pollination
  preserved (every scale reachable on every instrument).
- gssGroupsForInstrument(activeId, instOverride): single source of ordering logic,
  shared by fretted/piano/bowed menus. Active scale in a collapsed group force-opens it.
- csRebuildGrouped extended with collapsible "More scales" section + CSS.
- Currently configured: default (Western-first, World collapsed); bouzouki (World+Major
  open, rest collapsed). Adding an instrument = one line in GSS_INSTRUMENT_SCALE_ORDER.

### Open / to verify on device
- Harp scale menu shows the new scales (flat list, not grouped). Pedal-harp physical
  constraints with augmented-2nd scales not yet checked on device. Converting harp to
  the grouped/collapsible menu is a possible later consistency pass.
- Visual check of the "More scales" toggle on a real device.

---

## HARP PEDAL FIX (v0.67.6)

### Bug found (predated world scales)
The harp scale tool only had pedal data for the 9 diatonic scales (major modes +
harm/mel minor). The two pentatonics and blues — already in the app — silently fell
back to MAJOR-scale pedals and showed wrong. My 6 world scales joined them: 9 scales
total displaying incorrect pedals.

### Why the harp is the one instrument where "impossible to play" is real
A pedal harp has 7 pedals (one per letter C-D-E-F-G-A-B), each flat/nat/sharp. A scale
is playable only if its notes map to 7 distinct letters with no letter needing two
positions at once. Fretted/bowed instruments can fret any note, so nothing is ever
"impossible" there (the only greying there is re-entrant context strings, unchanged and
interval-agnostic). The harp genuinely can't play augmented-2nd scales at some roots.

### Fix
- Added hpAssignPedals(): backtracking pedal assignment. The old greedy hpPcsToPositions
  was far too pessimistic (reported even MAJOR as impossible at E/Gb/B) — couldn't be used
  for detection. Backtracking gives the musically correct answer.
- Harp scale branch: diatonic scales still use the hand-tuned table (correct enharmonic
  spelling); pentatonic/blues/world scales now compute pedals from pitch classes.
- When assignment fails, sets hpUnplayable: shows "not playable on pedal harp in this key"
  under the title, disables PLAY, and blocks hpPlayScale().

### Verified impossible combinations (flagged correctly, confirmed by running file code)
- blues at D
- double harmonic at Ab
- Hungarian minor at Db
- Hungarian major at E and B
All other scale+root combinations playable and now show CORRECT pedals.

### Still open
- Harp scale menu is still a flat list (not the grouped/collapsible World menu the
  fretted/piano/bowed tools use). Functional, just not grouped. Possible later consistency pass.
- The greedy hpPcsToPositions is still used for CHORD mode and may mis-assign pedals for
  some chord+key combos (same pessimism). Not touched this round — separate from scales.
- On-device visual check of the warning text + disabled PLAY button.

---

## HARP CHORD PEDAL FIX (v0.67.7)

### Confirmed the scale impossibility flags are real (hand-checked Ab double harmonic)
Ab double harmonic = Ab A C Db Eb E G. A can ONLY come from A-pedal-natural; G can ONLY
come from G-pedal-natural; Ab needs G-sharp OR A-flat — both neighbors already locked by
the natural A and natural G. Three notes, two pedals, no respelling escapes it. The
backtracker is correct, not over-cautious. Enharmonic borrowing (Eb as F-flat etc.) is
already tried by the backtracker since it works on pitch classes; it only reports
impossible when every respelling is exhausted. Pretty-spelling display (showing "Fb" vs
"E") deliberately NOT pursued — cosmetic rabbit hole.

### Chord-mode bug fixed
Exotic chord qualities used the greedy hpPcsToPositions, same flawed assigner that broke
scales. Replaced with hpAssignPedals (backtracking). Verified 3 common chord+key combos
were wrong before and are correct now: Gb13, Db min9, Eb dom7b9 (all genuinely playable,
greedy just mis-ordered pedals). Backtracker found ZERO false-impossibles among common
chords, so nothing playable is wrongly blocked.
- Unplayable chords now flagged (hpUnplayable), PLAY CHORD disabled + guarded, warning shown.
- hpUnplayable reset once at top of hpRender so it never goes stale across modes.
- Added id hpPlayChordBtn for the disable handling.

### Note
hpPcsToPositions (greedy) is now only used in pedal-override display paths, which are
user-driven and lower-risk. Could be retired entirely in a later pass.

---

## BRASS FINGERINGS AUDIT (v0.67.9)

### Result: WIND_FINGERINGS map is CORRECT — no fingering changes needed
The single shared pitch-class→valve map (WIND_FINGERINGS) is used by trumpet, flugelhorn,
French horn, euphonium, and tuba. Verified against canonical charts and valve physics:
- V1 = -2 semitones, V2 = -1, V3 = -3 (combinations sum). Confirmed multiple sources.
- Full map matches the standard chart: C[], C#[1,2,3], D[1,3], Eb[2,3], E[1,2], F[1],
  F#[2], G[], Ab[2,3], A[1,2], Bb[1], B[2]. E/A use 1+2 (correct default, not the sharp
  3-only alternate). C# uses the classic 1+2+3.
- Sharing one map across the valved-brass family is correct (sources confirm the trumpet
  chart applies to cornet/flugelhorn/baritone/euphonium/tuba).

### Variant notes (not bugs)
- Piccolo trumpet / 4-valve euphonium / 4-valve tuba: app models the 3-valve baseline.
  The 4th valve is an intonation+range aid that replaces the 1+3 combo; not required for
  basic chromatic fingerings. Fine simplification.
- French horn: rotary valves, same semitone system. Double-horn Bb side / thumb valve not
  modelled — fine for a learning baseline.
- French horn "contrabass": REAL but FRINGE (builders call it a new/experimental
  instrument, not standard orchestral). Kept as ⚠️NOTE — your call whether to keep it in
  the picker. Not a bug.

### Comment fix
- Trumpet standard range comment said "concert E3–C6"; the value (midi 54) is written
  F#3 (which sounds E3 concert on a Bb trumpet). Comment corrected to avoid confusion.
  Range value itself unchanged and correct.

### Trombone (slide) — already done earlier this session (v0.67.0/.1), not part of valved brass.

BRASS COMPLETE. Remaining pending = woodwinds only (flute, clarinet, sax, oboe, recorder,
whistle, ocarina, harmonica + standalone bass clarinet/cor anglais) + didgeridoo drone.

---

## BRASS TRANSPOSITION FINGERING BUG (v0.67.10) — found on re-check

### The bug
WIND_FINGERINGS is a WRITTEN-pitch map (open = written C and G — correct). But the brass
render path fed it CONCERT pitch class (midi%12, no transposition offset). So for every
TRANSPOSING brass instrument the displayed fingering was wrong:
- Bb trumpet, concert C showed "open" — but concert C is written D = 1+3. Wrong.
- Same error for flugelhorn (Bb), euphonium (Bb), French horn (F).
- Tuba unaffected (non-transposing in this context).
The note card even computed the correct writtenPc for its subtitle label, then ignored it
and fingered the concert pc. The valve MAP was right all along; it was being fed the wrong
pitch.

Why missed first pass: I verified the map against charts (correct) and confirmed the map
is shared across the family (correct), but did NOT trace whether the pc fed in was written
or concert. Caught on re-check.

### Fix
Added brassWrittenPc(concertPc): applies the written offset (Bb +2, F horn +7, tuba/none
+0) ALWAYS, independent of the concert/written DISPLAY toggle — because a fingering is a
property of the written note regardless of how the note name is shown. Routed all three
brass fingering sites through it (note-card diagram, scale-builder note.valves, fingering
text label). Downstream FD/nav render paths inherit via note.valves.

Verified via file functions: trumpet concert C -> 1+3, concert Bb -> open, concert F ->
open; horn concert F -> open, concert C -> open; tuba unchanged (concert C open, F = 1).

### Note
Woodwind path (wwGetFingering) already converted concert->written correctly; the bug was
brass-only, from the shortcut else-branch never getting the same treatment. Now consistent.

### Status correction
Brass fingerings: previously marked verified-correct (v0.67.9). The MAP was correct but the
PITCH FED TO IT was not. Now actually correct after this fix. Brass complete (for real).

---

## EMBOUCHURE AUDIT (added v0.67.x — checking alongside fingerings per Daniele)

windEmbouchure() (line ~65405) generates register-by-register technique guidance text
shown on every wind instrument note card. This is QUALITATIVE teacher-advice, not binary
data — verifiable only for outright pedagogical errors and misplaced register boundaries,
not exact wording. Tracking which instruments have had embouchure checked:

| Instrument | Embouchure checked | Notes |
|---|---|---|
| Clarinet (Bb) | ✅ | Register structure (chalumeau/throat/clarion/altissimo) correct. "Avoid biting" in chalumeau, "ee" voicing in altissimo, throat-tone support — all confirmed vs pedagogy sources (jennyclarinet, martinfreres). Boundaries in concert pitch (Bb sounds whole step down) — structure right. |
| Flute family | ✅ | Low=relaxed/warm air/larger aperture, high=fast narrow airstream/small aperture, lip plate ~1/4 covered — all confirmed vs flute pedagogy (randwickmusiclessons, scienceinsights, banddirectors). Piccolo 'unforgiving/avoid overblow' + alto 'rounder darker' correct. |
| Recorder | ✅ | Gentle breath through windway, half-thumb (pinch) venting for 2nd octave, fast narrow air + precise thumb venting for 3rd — standard duct-flute technique, consistent with verified fingerings. |
| Whistle | ✅ | Soft relaxed breath lower octave, firmer/faster upper octave (same fingering, hole-1 lift) — standard tin whistle technique. |
| Sax | ✅ (with note) | Low=relaxed jaw/slow warm air/avoid biting, upper/palm=fast focused air/high 'ee' tongue — confirmed vs Allard/Teal pedagogy (wikipedia sax technique, cafesaxophone, bettersax). NOTE: strict pedagogy says embouchure stays CONSTANT across registers (air speed + voicing do the work); app's 'slightly firmer' upper-register wording is defensible (mainstream minimal-firming view) but low='relaxed'/high='firmer' framing could nudge toward biting. Borderline-improvable, not an error. |
| Oboe | ✅ (minor note) | 'Let the double reed resonate', firm-not-biting low register, more pressure + lips-rolled-in + faster air high register — all confirmed vs oboe pedagogy (oboehelp, oboe.com, Ray Still, Fredonia). Core anti-biting message present. MINOR: strict pedagogy frames low as 'open/rolled-out' rather than app's 'firm controlled'; high as 'rolled-in firm'. App defensible, not an error. |
| Cor anglais | ✅ | 'Wider bore than oboe needs more air', pear-shaped bell richness, looser-than-oboe approach — all confirmed (musicalinstrumenthub oboe-vs-coranglais, Wikipedia cor anglais, magicreed). More air than oboe / less than bassoon is exactly right. |
| Bass clarinet | ✅ | Open/loosened jaw vs soprano is THE key difference — app emphasizes 'very relaxed jaw, open resonant throat' correctly (confirmed: instrumentalist 'whistling vs eating an apple', martinfreres, D'Addario). Clarion 'firm lip, fast air, no biting, register key' matches D'Addario exactly. |
| Bassoon | ✅ | Whisper key (G3 and below), flick keys (A/Bb/B/C around middle), round 'O' not-biting embouchure, very little lip pressure low / more pressure in 3rd octave — all confirmed vs bassoon pedagogy (USC School of Music, Blue Moon Bassoon, Lowe Modern Guide, PlayWoodwinds). Correctly references the bassoon-specific whisper + flick techniques. |
| Ocarina | ✅ | No octave registers; pitch rises with fingering + gradual breath pressure; 'never overblow', soft low / firmer high, raise pressure gradually — all confirmed vs ocarina breath-curve pedagogy (Pure Ocarinas breath curve, healing-sounds, TON). Correctly captures the vessel-flute breath-curve principle. |
| Trumpet | ✅ | Low relaxed/slow warm air → high firm corners/fast air/'tee' tongue arch; piccolo 'more precision throughout'. Verified vs brass pedagogy (Grokipedia/Farkas, trumpet.biz, hornmatters): tension+air rise with register, tongue 'ee' high/'oh' low. |
| Flugelhorn | ✅ | Rounder/softer/darker buzz than trumpet, conical-bore fullness, less brilliant up high — correct (mellower conical brass). Register tension/air progression matches brass consensus. |
| French horn | ✅ | Right hand in bell (~¾), withdrawn for high register, bell opened fully for pedal-like lows; firm corners, 'ee' tongue high. Verified vs horn pedagogy (hand-stopping per NW School of Music, tongue arch per HornMatters/Farkas). |
| Euphonium | ✅ | Pedal wide aperture/max air → relaxed low 'oh' → firmer mid → 'tee' arch high; upper register 'like upper trombone'. Correct low-brass pedagogy (more relaxation/air for low brass per Grokipedia/BandDirector). |
| Tuba | ✅ | Contrabass + standard both: extreme aperture/vast slow air for sub-pedal/pedal, wide relaxed buzz low, firmer corners/faster air high. Correct — most-relaxed setup of the brass family (Grokipedia: tuba most relaxed vs trumpet). |
| Trombone | ✅ | Soprano 'trumpet territory' (firmer), tenor balanced, bass 'F-attachment engaged' for pedals + open throat; all with low-relaxed/high-firm + 'toh/tee' tongue progression. Correct across all three sizes. |
