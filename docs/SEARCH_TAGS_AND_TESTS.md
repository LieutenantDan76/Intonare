# Intonare 1.0.5 Search: tags, ranking, and test list

Status: BUILT in 1.0.5 (branch search-1.0.5). Updated Nov 1 2026 to match the code.
Source of truth for module facts: the module tours in `TOURS` (Intonare.html around line 55569 and 55852), the Tools hub text `hint_tools_main`, and the code. Subtitles alone were not enough (Road Trip, Diadle).

## Decisions so far

- Build: category tags, concept words (EN and IT), phrases, folder results, two-word queries, a useful empty state, a type label on every row, and a ship-gate test list.
- Not building: the misses log, a difficulty search (no difficulty data per item).
- Nine folders are searchable results: Games, Ear Training, Rhythm, Reading (Train) and Pitch & Sound, Harmony, Rhythm, Reference, Utilities (Tools).
- "games" shows the five Games folder items first. Relative Pitch (The Climb) and Tempo Guess (scored, INSANE mode) show after them.
- Rhythm Cards test and Notation Cards test count as tests.
- Tuner and Metronome count as practice, ranked below the Train items.

## Final decisions (these replace the draft where they differ)

- Scoring: a name hit scores 100/92/80/60. A top-level main tag scores 96, a deep main tag 70, a top-level related tag 40, a deep related tag 20. A name hit plus a tag hit gives the higher score plus 10.
- Folder results use pri 2, so "pitch" still shows Pitch Match first.
- "practice" is a main tag on every Train exercise. Tuner and Metronome keep it as a related tag, so they rank below.
- Removed concept words: "hearing" (ear), "learn" (theory), "scale" (Theremin extra words). Not used as concept words: "tempo", "keys", "pitch". "daily" is not a game word. "training" was added to practice. The British "practise" was left out on purpose (US spelling gate); fuzzy match covers it.
- The "rhythm" test checks the top 5 for both rhythm folders, not first place.
- The header above a group of results shows a count, for example "GAMES - 5".
- Known caveats: "theory" ranks the Survival Guide first. "tuning" ranks the Tuner first, ahead of the guide chapter "Tuning". The Italian phrase list is short.
- The test list now lives in `tools/audits/search_queries.json` (72 queries) and runs through `tools/audits/intonare_search_audit.py` in a real headless browser. `tools/ship_check.bat` runs it as step 8 of 8.

## Ranking

1. A name match beats a tag match (typing "chordle" puts Chordle on top).
2. Main tag = weight 3. Related tag = weight 1.
3. Ties break by the existing `pri`, then by label length.
4. "practice" is a special case: every Train item counts the same, ordered by `pri`. Tuner and Metronome come after them.
5. Two-word queries: an item must match both words (by name, tag, or extra word) to rank in the top group. Items that match one word follow.

## Tag set (15)

game, test, cards, instrument, voice, ear, intervals, rhythm, reading, theory, harmony, reference, practice, daily, tuning

## Item table

| Item | Folder | Main | Related |
|---|---|---|---|
| Chordle | Games | game, test, ear, harmony | daily |
| Diadle | Games | game, test, ear, intervals | theory |
| Tónale | Games | game, test, ear | daily |
| Road Trip | Games | game, voice, ear | practice |
| Music Quiz | Games | game, test, theory | daily |
| Interval Ear | Ear | ear, intervals, test | voice, practice |
| Chord Ear | Ear | ear, harmony | practice |
| Pitch Match | Ear | voice, ear | practice |
| Relative Pitch | Ear | ear | game, practice |
| Tempo Lock | Rhythm | rhythm | test, practice |
| Tempo Guess | Rhythm | rhythm, test | game, ear, practice |
| Polyrhythm | Rhythm | rhythm | test, practice |
| Rhythm Reading | Rhythm | rhythm, reading | practice |
| Staff Notes | Reading | reading | test, practice |
| Notation Cards | Reading | cards, reading, test | practice |
| Scales | Train | theory, intervals | voice, ear, reference, practice |
| Rhythm Cards | Tools | cards, rhythm, test | reading, practice |
| Piano | Tools | instrument | harmony |
| Drum Kit | Tools | instrument, rhythm | |
| Theremin | Tools | instrument | |
| Tonal Center | Tools | ear, voice | instrument, intervals |
| Guitar Charts | Tools | reference, instrument | harmony |
| Chords | Tools | harmony, reference | ear, instrument |
| Progression | Tools | harmony, theory | |
| Circle of Fifths | Tools | theory, harmony, reference | |
| Intervals (reference) | Tools | intervals, reference, theory | ear |
| Transposer | Tools | theory, reference | instrument |
| Vocal Range | Tools | voice, reference | |
| Volume Meter | Tools | reference | |
| Survival Guide | Tools | reference, theory, instrument | |
| Tuner | Tab | tuning, instrument | practice |
| Metronome | Tab | rhythm | practice |

Items inside screens get tags by id prefix: guide chapters = theory plus their instrument (instrument tag), voice chapters = voice, grooves = rhythm, chord and scale entries = harmony.

## Extra search words (from the tours)

- Tuner: capo, tuning fork, A440, strobe, vibrato, transposing, cents
- Metronome: tap tempo, ramp, analyze, rushing, dragging, son clave, bossa, swing, groove
- Piano: organ, Hammond, Leslie, Rhodes, pedal, sustain, harpsichord, vibraphone, glissando
- Theremin: glide, waveform, vibrato, snap to scale
- Drum Kit: drum machine, sequencer, time signature, swing, subdivision, triplets
- Guitar Charts: capo, fingering, fretboard, clarinet, sax
- Tonal Center: drone, temperament, just intonation, solfege
- Vocal Range: voice types, soprano, alto, tenor, bass, warm-up
- Volume Meter: decibel, hearing, loud, NIOSH
- Transposer: concert pitch, B-flat trumpet, E-flat sax, horn
- Progression: blues, twelve-bar, turnaround
- Rhythm Cards: syncopation, triplets, rests, drill
- Notation Cards: symbols, bowing, bending, custom deck
- Music Quiz: trivia, survival, packs
- Intervals reference: unison, ninth, semitones, tritone

## Concept words (typed word -> tag), each with an Italian twin

- game: games, game, play, fun, daily, challenge | giochi, gioco, giocare, sfida
- test: test, tests, quiz, exam, score, trivia | prova, verifica, quiz, punteggio
- cards: cards, flashcards, flash cards | carte, schede
- instrument: instrument, instruments | strumento, strumenti, suonare
- voice: sing, singing, voice, vocal, hum | canto, cantare, voce
- ear: ear, listen, hearing, ear training | orecchio, ascolto
- intervals: interval, intervals, degree, degrees | intervallo, intervalli, grado, gradi
- rhythm: rhythm, beat, timing, groove | ritmo, tempo
- reading: read, reading, sheet music, notation | lettura, leggere, spartito
- theory: theory, learn, lesson | teoria, imparare, lezione
- harmony: chords, harmony, keys | accordi, armonia
- reference: reference, lookup, chart | riferimento, consultare
- practice: practice, train, exercise, drill | esercizi, allenamento
- daily: daily, today | giornaliera, oggi
- tuning: tune, tuning, pitch | accordare, accordatore

## Phrases (full sentences people type)

"train my ear", "learn chords", "keep time", "read music", "sing in tune", "hold a note", "find my range", "check my tempo". Each maps to one or two tags. List to be finished with Daniele.

## Empty state

When nothing matches: show the category chips (Games, Tests, Instruments, Singing, Rhythm, Theory) instead of a blank screen.

## Test list (ship gate)

Format: query -> what must appear. "top N" = within the first N rows. "first" = row 1.

Folders
1. games -> Games folder first, then Chordle, Diadle, Tónale, Road Trip, Music Quiz in the top 7; Relative Pitch and Tempo Guess listed after them
2. giochi -> same as games
3. ear training -> Ear Training folder first
4. reading -> Reading folder first
5. harmony -> Harmony folder first, then Chords, Progression, Circle of Fifths
6. reference -> Reference folder first
7. utilities -> Utilities folder first (Volume Meter, Transposer)
8. rhythm -> Rhythm folder first (Train) and Rhythm folder (Tools)

Concepts
9. tests -> Music Quiz, Chordle, Diadle, Tónale, Interval Ear, Tempo Guess, Notation Cards, Rhythm Cards in top 10
10. quiz -> Music Quiz first
11. flashcards -> Notation Cards and Rhythm Cards in top 3
12. carte -> same as flashcards
13. instruments -> Piano, Drum Kit, Theremin, Guitar Charts, Survival Guide in top 8
14. strumenti -> same as instruments
15. singing -> Pitch Match, Road Trip, Tonal Center, Vocal Range in top 5
16. canto -> same as singing
17. voice -> same as singing
18. ear -> Chordle, Diadle, Tónale, Road Trip, Interval Ear, Chord Ear, Pitch Match, Relative Pitch in top 10
19. intervals -> Interval Ear, Diadle, Scales, Intervals reference in top 5
20. rhythm test -> Tempo Guess, Rhythm Cards in top 3
21. practice -> every Train item before Tuner and Metronome
22. esercizi -> same as practice
23. theory -> Music Quiz, Scales, Circle of Fifths, Survival Guide in top 8
24. chords -> Chords, Chord Ear, Chordle in top 5
25. accordi -> same as chords
26. daily -> Chordle, Tónale, Music Quiz in top 4
27. tuning -> Tuner first

Two-word
28. ear games -> Chordle, Diadle, Tónale, Road Trip first
29. voice game -> Road Trip first
30. rhythm cards -> Rhythm Cards first
31. interval test -> Interval Ear first

Phrases
32. train my ear -> Ear Training folder and Interval Ear in top 3
33. learn chords -> Chords or Chord Ear in top 3
34. keep time -> Tempo Lock or Metronome in top 3
35. read music -> Staff Notes or Notation Cards in top 3
36. sing in tune -> Pitch Match first

Extra words
37. capo -> Tuner and Guitar Charts in top 3
38. strobe -> Tuner first
39. organ -> Piano first
40. rhodes -> Piano first
41. hammond -> Piano first
42. blues -> Progression first
43. bossa -> Metronome or Drum Kit in top 3
44. swing -> Drum Kit or Metronome in top 3
45. decibel -> Volume Meter first
46. hearing -> Volume Meter in top 3
47. concert pitch -> Transposer first
48. trumpet -> Transposer in top 3
49. soprano -> Vocal Range first
50. drone -> Tonal Center first
51. temperament -> Tonal Center first
52. tap tempo -> Metronome first
53. ramp -> Metronome first
54. theremin -> Theremin first
55. syncopation -> Rhythm Cards first

Name regressions (must not break)
56. chordle -> Chordle first
57. tuner -> Tuner first
58. metro -> Metronome first
59. piano -> Piano first
60. chrodle (typo) -> Chordle in top 3
61. metronom (typo) -> Metronome first

Empty state
62. xyzzy -> category chips show, no blank screen

Ship gate also checks: every FAV_META key has tags, every tag in a table row exists in the concept list, and every concept word has an Italian twin.

## Copy fixes found while reading the tours (separate from search)

- Road Trip tour describes an interval-naming game. The game is sing-and-hold pitch memory with distraction melodies (code: `rt_sing_lock`, `rtOnPitch`, `rtVoiceHeard`). Tour looks stale. Rewrite EN and IT.
- Games hub hint (`hint_games_exs`) names three of five games. Diadle and Road Trip are missing.
- Road Trip card subtitle does not say you sing into the mic.
- Relative Pitch tour EN: "keeps no score, with no score" (duplicate phrase).
- Polyrhythm tour IT: "il poliritmia" should be "la poliritmia" (two places).
