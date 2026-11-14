# Tools

Checks and helpers for `Intonare.html`. The app does not need this folder to run or to build. It is the test suite.

## Ship check

Run this before every release:

```
tools\ship_check.bat
```

It runs nine steps and stops at the first failure:

1. HTML integrity (file size, end tag, brace balance, no sudden shrink against the last commit)
2. Regression sentinel
3. Changelog gate
4. Achievement audit
5. Backup audit
6. Drum preset audit
7. US spelling audit
8. Search audit
9. Boot smoke test

Steps 8 and 9 use a headless browser. They are skipped with a warning if Playwright is not installed.

Requirements: Python 3, then `pip install playwright` and `playwright install chromium`.

## `audits/`

Each script takes the path to `Intonare.html` unless noted, and exits non-zero on failure.

| Script | What it checks |
|---|---|
| `intonare_html_integrity.py` | The file is whole: size, end tag, brace balance, no CRLF damage |
| `intonare_regression_sentinel.py` | Every past fix is still in the file. One pin per fix |
| `intonare_changelog_gate.py` | The top changelog entry matches the app version |
| `intonare_achievement_audit.py` | Every achievement can be earned, and stays locked one step short |
| `intonare_backup_audit.py` | Every saved key is either in the backup or skipped on purpose |
| `intonare_drum_preset_audit.py` | Drum presets fit their time signature and step grid |
| `intonare_us_spelling_audit.py` | User-facing English uses American spelling |
| `intonare_search_audit.py` | Real searches return the modules they should |
| `intonare_boot_smoke.py` | Every tool, exercise and game opens without an error |
| `intonare_taint_audit.py` | Saved text (presets, saves, sessions) can never reach the page as markup. Needs Playwright |
| `intonare_stopall_audit.py` | Every sound source is covered by the stop-all function |
| `intonare_audio_handle_audit.py` | Audio nodes are tracked and released |
| `intonare_scale_audit.py` | Scale spellings and pitch classes are correct |
| `intonare_groove_audit.py` | Groove patterns are well formed |
| `intonare_i18n_audit.py` | User-facing strings have an Italian translation (slow) |
| `intonare_dev_flag_audit.py` | Developer tools cannot be reached or grant Pro in a release build |
| `intonare_light_gate.py`, `intonare_light_vars.py`, `intonare_light_shots.py` | Light mode contrast and leftover dark-mode colors |

Run the area audits (audio, scales, grooves, translations, light mode) when a change touches that area. They are not part of the ship check because some of them are slow.

## `pitch/`

An offline benchmark for the pitch detector. It generates test tones, runs the same detector the app uses, and compares the result with a stored baseline.

```
tools\pitch_bench.bat
```

Run it before and after any change to microphone or pitch code. It needs Node.

## `patch_intonare.py`

Applies an exact text replacement to `Intonare.html` and keeps the file's line endings and size intact. Each old string must match exactly once. It runs the integrity check after writing and restores the file if that check fails.

```
python tools/patch_intonare.py --old "unique old text" --new "replacement"
```
