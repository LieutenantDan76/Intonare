# Quiz toolchain, rebuilt August 2026

Replaces the quiz-tool half of `AUDIT_INVENTORY.md`. The app-level audits
(`intonare_regression_sentinel.py`, `intonare_backup_audit.py`,
`intonare_stopall_audit.py`, `intonare_changelog_gate.py` and the rest) are
unchanged and still live in that document.

Nothing here touches `Intonare.html` except `intonare_pack_build.py --install`,
and that one restores the file if its own verification fails.

---

## Why this rebuild happened

Three tools were dead. `intonare_pack_faults.py`,
`intonare_double_dip_scan.py` and `intonare_italian_sweep.py` each carried a
hardcoded list of twenty pack keys, and deleting `gear_equipment` in v0.196.0
killed all three with the same `AttributeError` before they printed a line. A
broken audit that is never invoked looks exactly like a passing one.

The bigger problem was that packs still needed heavy triage, and the reason was
not taste. **The draft gate and the ship gate were different programs checking
different things**, so faults survived the draft and landed on Daniele.

Three findings, all measured:

**The draft tools never read Italian.** `intonare_draft_check.py` and
`intonare_blurb_draft_check.py` contained zero references to `q_it`, `opts_it`
or `fact_it`. Every check they ran was English. An Italian fault could not fail
the draft gate no matter how bad it was, and got found by livecheck at ship, or
by Daniele, or by Linda. In v0.189 that was twelve answer-length tells the draft
check reported as none, half of them Italian.

**Two Italian checkers disagreed.** The sweep reported sixteen drifts on
guitar_technique and the draft checker reported four, because the draft checker
predated the metric-conversion and worded-decade calibrations. Twelve
differences, no way to tell from either output which tool was right.

**One fault had three thresholds.** Answer-findable-by-length was 2.0x in the
draft check, 12 characters in the pack audit, and 1.6x in the v0.189 padding
pass. A pack could clear the draft, get padded, and still fail at ship. Same
fault, three verdicts.

---

## The rule this rebuild follows

**Every checker takes either a draft JSON or an installed pack, and runs the
same code over both.**

    python3 intonare_draft_check.py draft.json
    python3 intonare_draft_check.py --pack bass

A pack that passes while you write it passes once it is in the file, or the tool
is wrong in both places at once, which is the only honest kind of wrong.

---

## Thresholds, measured not chosen

Every number below was taken with `intonare_quiz_lib.py` over the six authored
packs, in both languages. They live in that one file and every tool imports
them.

### Answer findable by length

561 questions per language:

| rule | gods | beatles | bass | 70s | theory | technique |
|---|---|---|---|---|---|---|
| gap > 12 | 1 | 1 | 0 | 0 | 3 | 11 |
| **gap > 15** | **0** | **0** | **0** | **0** | **1** | **3** |
| ratio > 1.6 | 0 | 0 | 3 | 2 | 1 | 0 |

`gap > 15` is the error, because it is clean on the four packs Daniele read
question by question. 13 to 15 is a warning and a reading list.

**The ratio rule is dropped.** Every one of its hits was a name or term whose
length is inherent and cannot be padded away: "four on the floor" against "a
shuffle", "Quattro" against "Uno / Due / Tre", "The Complete Book of Running"
against "Aerobics". A check that fires on material nobody can fix teaches you to
ignore the output.

### Run-on ceiling

The old check used 45 words for both languages. The first thing the bilingual
run flagged was the Angus Young blurb out of `QUIZ_VOICE.md`, in Italian, at 44
words. The gold standard failing its own check.

Measured over 870 English and 867 Italian sentences:

| | p90 | p95 | p99 | max |
|---|---|---|---|---|
| EN | 39 | 41 | 45 | 48 |
| IT | 39 | 42 | 48 | 53 |

Italian is only 5 to 10 percent longer at the tail, so it needs its own number
rather than a shared one. Set at the approved maximum: 48 English, 53 Italian, 5
commas, 6 and 7 connectives. All six packs now report zero.

---

## The tools

| script | reads | what it is for |
|---|---|---|
| `intonare_quiz_lib.py` | — | the shared loader and every threshold. Import it, do not copy from it |
| `intonare_pack_gate.py` | draft or pack | **the one command.** Runs everything below in the order faults appear |
| `intonare_draft_check.py` | draft or pack | structure: duplicate answers, giveaways, stem seals, leaning pairs. Bilingual |
| `intonare_blurb_draft_check.py` | draft or pack | blurb register, run-ons, threads, omega leaks. `--lang it` for the other side |
| `intonare_italian_check.py` | draft or pack | coverage, drift, English leaking through. Replaces the two that disagreed |
| `intonare_pack_seal.py` | draft | stamps a stem so a later edit to it cannot go unnoticed |
| `intonare_pack_build.py` | draft | installs a pack and proves it landed |
| `intonare_pack_audit.py` | pack json | the ship-side audit, now on the shared threshold |
| `intonare_pack_faults.py` | file | fault counts across every ready pack, both languages |
| `intonare_italian_sweep.py` | file | Italian drift across every ready pack |
| `intonare_double_dip_scan.py` | file | questions that belong in a second pack |

Deleted: `intonare_italian_draft_check.py`, superseded by
`intonare_italian_check.py`.

---

## The stem seal

The omega read keeps finding the same fault. On the Bass pack, three questions
had options that had stopped answering their own stems: "The fretless solo does
what in its second half?" was rewritten to "How did the engineers make it?" and
the options were left reading "repeats the first half backwards". Every audit
passed. The question was nonsense.

That is bookkeeping, not taste, so it can be a gate that never cries wolf.

A sealed row carries `sq`, a short hash of the English and Italian stems
together. `intonare_draft_check.py` recomputes it and errors on any row whose
stem has moved since. Change a stem afterward and the row fails until somebody
reads the whole question again and re-seals it.

    python3 intonare_pack_seal.py draft.json --status
    python3 intonare_pack_seal.py draft.json --rows 1-24

**Seal a tier once you have read it, not while you are still writing it.**
Sealing everything at the end defeats the point: the seal records that somebody
read the row whole, and a blanket stamp records nothing.

`sq` never reaches `Intonare.html`. The builder strips it.

---

## The round trip

`intonare_pack_build.py` does not trust itself. After writing, it parses the
written file back through the same loader the audits use and compares every
field of every row against the draft JSON. A mismatch is an error, and on
`--install` the real file is restored and nothing lands.

    python3 intonare_pack_build.py draft.json --pack bass
    python3 intonare_pack_build.py draft.json --pack bass --install

This exists because the spec's discipline is "read every edit back out of the
shipped file before reporting it done", and `assert count == 1` does not cover
it: it catches a miss, but not a script that asserts on one substitution,
applies it, then throws on the next and writes nothing. Three fixes silently
failed that way in one session and were nearly reported as complete.

Verified against the shipped Bass pack: 104 rows out and back with no field
difference, nine script blocks still passing `node --check`, the regression
sentinel still reporting 97 fixes and 247 pins. Verified to FAIL by corrupting
one name during the write, which it caught in four fields of row 1.

---

## False positives the tools now leave alone

Each of these fired on approved material once, and each is recorded in the tool
so nobody re-adds it.

- **"Rumours" and "Hapshash and the Coloured Coat"** read as British spellings.
  A title keeps its own spelling. British spelling is checked field by field
  now; joining the fields put the first option straight after the blurb's
  closing period, so a title in that slot looked sentence-initial and lost its
  proper-noun exemption.
- **"in the pocket" and "four on the floor"** in Italian prose read as English
  leaking through. They are what an Italian bassist writes.
- **"C", "D", "E" and "X"** as answers to Bass diagram questions read as stems
  containing their own answer, because the test was a substring match. It needs
  a word boundary and more than three characters.
- **"cinema"** read as British vocabulary. It is standard American for the art
  form; "British cinema" is fine.
- **"il contrabbasso"** as the Italian answer to two different questions. Bass
  16 answers "the double bass" and bass 89 answers "the upright bass", two
  English terms for one instrument. A duplicate answer is an error in English
  and a warning in the other language.

---

## Real faults these found in the shipped file

Not fixed, because nothing here has touched `Intonare.html`.

1. **`theory_fundamentals`** ships an option reading "Slides between two
   neighbouring pitches". British spelling, live.
2. **`theory_fundamentals` Q24** asks "Which clef do bass guitar and cello parts
   normally use?" and answers "Bass". The stem hands over the answer.
3. **`theory_fundamentals` Q52** has an Italian answer 18 characters longer than
   any distractor.
4. **`guitar_technique` Q65 and Q82** have Italian answers 23 and 16 characters
   longer than any distractor. **Q99** has the same fault in English at 16.
5. **`guitar_technique`** names Fender in five stems against a cap of three.
6. Three pairs of curly-against-straight apostrophes between twins, in
   `beatles` and `guitar_technique`. Only visible in the installed file, because
   draft JSON normalizes them.

---

## What is still a read, and why

Three detectors were built during the Bass pack and thrown away. One fired on 7
of 42 approved blurbs including Daniele's own rewrite; one fired on 51 of 106
and caught 1 of the 3 known bad ones; one gave 23 flags for 3 real faults.

**A check that fires on approved material is worse than no check, because it
teaches you to ignore the output.** So these stay in stage 5 of the gate as a
printed list, and the gate prints them every time because they are the part that
gets skipped:

- read every blurb alone, not in a block
- read each closing sentence against the one before it: does it answer something
  that sentence raised, or is it just the next true fact?
- confirm every superlative, first and attribution. Bare years come back clean
  every time; those three never do
- read the options against the stem for a second correct answer. Can you name
  another person the stem also describes?
- read the stem aloud
- would the player repeat this answer to somebody else?
