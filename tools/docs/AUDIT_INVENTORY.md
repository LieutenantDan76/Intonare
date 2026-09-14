# Intonare audit inventory

Checked against v0.150.119 on 21 August 2026. Every script was run, not assumed.

There are two problems this document solves. The first is that thirty-odd scripts
have accumulated and nobody can hold them all in mind. The second is worse: a
few of them no longer run, and a broken audit that is never invoked looks exactly
like a passing one.

---

## Run these before every ship

The gate from the working notes, in order. All seven run clean today.

| script | what it protects |
|---|---|
| `intonare_regression_sentinel.py` | 97 tracked fixes and 247 pinned code fragments. The one that has actually blocked bad ships. Any number lower than **97 fixes + 247 pins** means a stale copy. |
| `intonare_backup_audit.py` | every persisted key and progState field is classified, so backup export stays complete |
| `intonare_stopall_audit.py` | every audio stop function is wired into `stopAllAudio`, so nothing keeps ringing |
| `intonare_changelog_gate.py` | the changelog's top entry matches the shipped version |
| `intonare_audio_handle_audit.py` | audio nodes are tracked and released |
| `intonare_scale_audit.py` | 228,764 scale notes, pitch classes and spelling |
| `intonare_dev_flag_audit.py` | **not yet in the project.** Developer tools unreachable, nothing behind the flag grants Pro |

---

## Working, run when you touch that area

| script | area |
|---|---|
| `intonare_i18n_audit.py` | translation coverage, categories A–G. Slow; give it a few minutes |
| `intonare_quiz_audit.py` | quiz answer text, including the length-bias measurement |
| `intonare_theory_audit.py` | chord and interval theory |
| `intonare_instrument_audit.py` | instrument definitions |
| `intonare_strings_audit.py` | string tunings |
| `intonare_capo_audit.py` | capo transposition |
| `intonare_subdiv_audit.py` | rhythmic subdivisions |
| `intonare_groove_audit.py` | 60 metronome grooves against their sources |
| `intonare_tour_audit.py` | onboarding tour steps |
| `intonare_open_dead_string_audit.py` | open and dead string markers |
| `intonare_audio_display_audit.py` | audio state versus what is displayed |
| `intonare_ink_audit.py` | ink and contrast tokens |
| `intonare_draw_color_sweep.py` | drawing colours |
| `intonare_us_spelling_audit.py`, `us_sweep.py` | British spelling |

---

## Needs a local server first

Two scripts drive a real browser over HTTP and fail with `ERR_CONNECTION_REFUSED`
if nothing is serving. That failure reads like a broken script and is not one.

```
cd /home/claude && (setsid python3 -m http.server 8899 >/dev/null 2>&1 < /dev/null &)
```

- `intonare_state_leak_audit.py` — state left behind when a module closes
- `intonare_lang_sweep.py` — language sweep across rendered screens

---

## Quiz pack tooling, current as of the Bass pack

| script | state |
|---|---|
| `intonare_pack_audit.py` | **UPDATED.** Now warns on the inverted stem in both languages. Takes `--allow` for findings that are noise in a given pack: a bass pack trips the subject cap on the word "bass". |
| `intonare_blurb_voice.py` | **UPDATED.** Now warns on the verdict closer. Two other detectors were written and removed; the reasons are in the file so nobody rebuilds them. |
| `intonare_quiz_style.py`, `intonare_quiz_leak.py`, `intonare_quiz_dup.py`, `intonare_quiz_trim_audit.py` | **UPDATED.** All four hardcoded `/home/claude/Intonare.html` and so had never seen a pack in draft. They now honour `INTONARE_HTML`. |
| `intonare_bass_draft_build.py` | **NEW.** Injects a drafted pack into a copy of Intonare.html at `/tmp/draft.html` so the four tools above can run before anything touches the real file. |
| `QUIZ_VOICE.md` | **NEW.** Twelve approved questions in full, extracted from the shipped Guitar Gods pack, plus the three tests and the omega read. Read before writing. |

## Broken or stale

| script | state |
|---|---|
| `intonare_notation_audit.py` | **FIXED.** It needed `glyphnames.json` and `classes.json` from the W3C SMuFL repo; both are now in outputs, so drop them next to the script. First clean run reports 181 cards, 138 glyph and 43 drawn, all codepoints resolving and matching SMuFL, no shared codepoints. It had been unable to run at all until 21 August. |
| `intonare_light_contrast_audit.py` | **REMOVED** from the project. Superseded by `_v3`. |

---

## Added to the project since this list was written

`intonare_dev_flag_audit.py`, `intonare_dom_leak_audit.py`, `intonare_lang_diff.py`,
`intonare_symbol_audit.py` and `intonare_a11y_sweep.py` are all in now, and the
timing-out contrast script is out. Nothing further is required from the list
below; these are optional.

## Optional, still only in outputs

| script | what it does |
|---|---|
| `intonare_sg_audit.py` | Survival Guide structure, wiring, parity, copy tells, instrument reach |
| `intonare_sg_claims.py` | extracts every checkable factual claim from the guide, sorted by risk |
| `intonare_sg_style.py` | scores pages for AI writing markers: burstiness, lexical diversity, tricolons |
| `intonare_twin_audit.py` | data tables whose display fields lack an Italian twin |
| `intonare_ste_rules.py` | the register rewrite rules, as documentation |
| `measure_glyphs.py`, `gen_glyphs2.py` | measure SMuFL codepoints against the embedded Bravura before adding one |

**Two cautions carried from this session.** `intonare_sg_style.py` and
`intonare_twin_audit.py` both flag SHAPE, not quality: the style scorer rates
some hand-written replacements worse than the originals, and the twin audit
flags real enumerations like "flat, natural, and sharp" as padding. Read their
output, do not obey it.

---

## Disposable

Everything matching `it_*.py`, `perc*.py`, `sg_rewrite*.py`, `sg_it_sync.py`,
`sg_dashes.py`, `sg_headings.py`, `sg_dedupe.py`, `tag_terms.py`,
`rumble_panel.py`, `hash_codes.py`, `back_button.py`, `cut_wiki.py` and similar
are one-shot edit scripts. They did their job and are recorded in the changelog.
Nothing to keep.


---

## Open finding, 21 August

`intonare_a11y_sweep.py` now runs and reports **313 contrast values below AA**
and **41 tap targets under 44px**, concentrated on the tuner tab (17 small taps,
35 contrast fails). Some of that will be muted text that is low-contrast on
purpose and decorative rather than informational, so the number is a starting
point, not a defect count. Nobody has read the list yet. It is the largest
untriaged audit output in the project.


---

## Quiz tools, added after this list was first written

Nine scripts, all in the project as `intonare_quiz_*.py`. They are separate from
the audits above because they cover one feature rather than the whole app, and
because three of them WRITE.

Every one carries a banner stating whether it writes and how to call it, and
every one exits with a readable message rather than a traceback when it is called
wrongly or when `Intonare.html` is not at `/home/claude/`.

| script | writes? | notes |
|---|---|---|
| `intonare_quiz_style.py` | no | AI-cadence tells in questions and blurbs |
| `intonare_quiz_leak.py` | no | answer leaks that are not about length |
| `intonare_quiz_dup.py` | no | same-topic duplicates by word set |
| `intonare_quiz_trim_audit.py` | no | questions the option trimmer gives away |
| `intonare_quiz_progress.py` | no | regenerates the spec's progress table |
| `intonare_quiz_livecheck.py` | no | takes a pack id; measures the RUNNING app |
| `intonare_quiz_strip.py` | **yes** | strips option detail; idempotent |
| `intonare_quiz_addit.py` | **yes** | takes a json batch; adds Italian |
| `intonare_quiz_difficulty.py` | one-shot | tier installer, already applied |

**The one trap worth knowing:** the six source-parsing tools cannot see the
bilingual schema. A question with `q_it` between `q` and `opts` does not match
their regexes. Guitar Gods reported 52 questions while holding 100. Use
`livecheck` on any bilingual pack until they are updated.
