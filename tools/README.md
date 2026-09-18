# Claude tooling triage (Sep 2026)

Source: `intonare_project_files.zip` → staged under `tools/`.
Original inventory dated **21 Aug 2026 / v0.150.x**. App is now **v0.210.66**.
Treat every script as **useful but possibly stale** until it has a clean run
against the current `Intonare.html`.

## Decision

Start lean. Do **not** run thirty audits before every edit.
Keep the high-value gates; run area tools only when touching that area;
leave the rest archived.

## Ship check (daily gate)

From the repo root, or double-click / run:

```
tools\ship_check.bat
```

Runs: HTML integrity → regression sentinel → changelog gate. Exit 0 = green.

Integrity gate (`intonare_html_integrity.py`) fails on truncate, sudden
shrink vs HEAD (including the Windows CRLF→LF rewrite), missing `</html>`,
or wild brace imbalance. Patch `Intonare.html` with `tools/patch_intonare.py`
(bytes-safe), not `read_text`/`write_text`.

Web PWA: `sw.js` is network-first for the app shell; Capacitor never
registers a service worker (native bundle is the source of truth).

## Needs Python first

This machine had no `python` / `py` on PATH when imported. Install Python 3
(and enable "Add to PATH") before any of these scripts will run.

## Keep — `tools/audits/` (ship / regression)

| File | Role |
|---|---|
| `intonare_regression_sentinel.py` | Pins past fixes. Highest value. Renamed from `…-6.py`. |
| `intonare_changelog_gate.py` | Changelog top = HTML version (Codemagic also checks this). |
| `intonare_light_gate.py` | Light-mode NEON / ROLE static + Playwright LIVE AA (Tools). |
| `intonare_light_shots.py` | Light screenshots for `light-mode/review.html`. Default `--family train` (Train+Tuner+Metro). Tools: `--family tools`. |
| `intonare_backup_audit.py` | Backup/restore key coverage |
| `intonare_stopall_audit.py` | Audio stop wiring |
| `intonare_us_spelling_audit.py` | American English ship check |
| `intonare_audio_handle_audit.py` | Node tracking / release |
| `intonare_scale_audit.py` | Scale spelling / pitch classes |
| `intonare_drum_preset_audit.py` | Drum presets |
| `intonare_groove_audit.py` | Groove patterns |
| `intonare_i18n_audit.py` | Translation coverage (slow) |
| `intonare_dev_flag_audit.py` | Dev-flag / Pro leakage |
| `glyphnames.json`, `classes.json` | Needed by notation audit if revived |

Suggested ship order once Python works:

1. `node` script-block check (manual / existing habit)
2. `python tools/audits/intonare_regression_sentinel.py Intonare.html`
3. `python tools/audits/intonare_changelog_gate.py`
4. spelling + backup + stopall if the change touched those areas

## Keep — `tools/quiz/` (only when editing quiz packs)

Pack build/audit/voice/Italian tools + `QUIZ_TOOLING.md` + `QUIZ_VOICE.md`.
Do **not** overwrite `docs/QUIZ_BLURB_GUIDE.md` or `docs/AI_COPY_GUIDE.md`;
the repo copies are the live guides (zip blurb guide was smaller/older).

## Keep — `tools/docs/` (reference, not auto-run)

`AUDIT_INVENTORY.md` (historical), `GROOVE_AUDIT.txt`, Bret SVG guide,
vocal module spec, instrument ledger, store `App_Description.md`,
`QUIZ_SPEC.md`.

## Archived — `tools/_incoming_archive/`

Full zip contents for archaeology. Includes one-shot allowlists,
older duplicate guides, JS harnesses, calibrators, etc. Do not put these
on a daily path until someone re-validates them on v0.210+.

## Do not use blindly

- Paths hard-coded to `/home/claude/...` (fix or set `INTONARE_HTML`)
- `AUDIT_INVENTORY` “run before every ship” list as gospel; refresh after
  a clean sentinel run on current HTML
- Zip copies of `AI_COPY_GUIDE.md` / `QUIZ_BLURB_GUIDE.md` over repo `docs/`

## Next steps (when you want)

1. Install Python 3 for Windows.
2. Run the sentinel once; fix or retire dead pins.
3. Add a tiny `tools/ship_check.bat` that runs sentinel + changelog gate.
4. Delete `_claude_import/` after you’re happy (duplicate of archive).
