# Intonare AI copy guide

Read this file before writing or editing any user-facing text in
Intonare: tours, reference text, survival guide pages, step
instructions, i18n strings. For quiz pack content specifically, read
QUIZ_BLURB_GUIDE.md instead.


## The two-stage check

Every user-facing string must pass both stages before shipping.

STAGE 1 — Strip AI-speak tells:
- Marketing verbs and superlatives
- "Not just X, it's Y" constructions
- Rhetorical openers ("Ever wondered...?", "Here's the thing:")
- Quippy sass or forced personality
- Em-dash overuse (use semicolons, commas, or periods instead)
- "Explore," "discover," "unlock," "dive into," "journey"
- "Beautiful," "stunning," "elegant," "powerful," "robust"
- "Seamlessly," "effortlessly," "intuitively"
- "Where X lives/sits" (caught six times in survival guide, v0.210.38)

STAGE 2 — Check rhythm:
- Plain is not clipped. Stripping tells can overshoot into staccato
  fence-posts: short. Choppy. Sentences. That read. Like a telegram.
- Vary sentence length. Add connective tissue.
- Read cold: if it sounds like an instruction manual or a marketing
  brochure, it's wrong. It should sound like a teacher talking to a
  student who is right there.

The tone lint script (intonare_tone_lint.py) is advisory. The manual
read is the gate. Daniele pushed back hard on script-only audits:
"the real pass should've been the first time."


## American English

American English is enforced across the app. Exceptions that must
never be swept (they are proper names, API identifiers, or correct
foreign titles):

- Daft Punk
- Licence to Kill
- Hapshash and the Coloured Coat
- `createAnalyser` / `AnalyserNode` (Web Audio API spelling)
- `userCancelled` (Capacitor API spelling)
- Baduizm (album title)

"Semitone" and "bar" are standard American music usage. Do not replace
them with "half step" or "measure."


## Bilingual sync

- Always sync EN/IT twin strings when editing either language.
- Watch for triplicate strings: the i18n value, a hardcoded DOM
  default, and a JS fallback can all carry the same text. Editing
  one and missing the others creates a mismatch.


## Italian music jargon

Music jargon stays in English when writing Italian copy: pocket,
walking, ghost note, one-drop, tumbao, shuffle, box (pentatonic
shape), slap, strum, pickup, setup, signature, fretless, feedback,
backbeat, riff. Italian equivalents sound wrong to Italian players.

"Andare in diretta" means going on broadcast, not going direct to a
mixer. Use "entrare diretti nel mixer."


## The voice

A teacher's voice, not a critic's, not a marketer's, not a Wikipedia
editor's. Write what a player would say to another player. If the
sentence wouldn't come out of a musician's mouth, rewrite it.
