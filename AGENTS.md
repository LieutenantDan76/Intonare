# Intonare agent notes

## Start every chat

1. Read `docs/PROJECT_STATUS.md`
2. Rules auto-load from `.cursor/rules/` (`daniele.mdc`, `intonare.mdc`;
   copy/quiz rules when those files are in play)
3. Keep `CHANGELOG.md` in sync with `INTONARE_VERSION` before Codemagic

## Edit safety (giant HTML file)

- Exact unique string replace only. Never DOTALL regex on `Intonare.html`.
- Never rewrite the whole file. Prefer a short `tools/_patch_*.py` with
  uniqueness checks; avoid PowerShell inline Python (quoting corrupts).
- Before/after every edit: confirm ~12MB size and file still ends with
  `</html>`. Tool "success" is not enough.
- If size collapses (~12MB → much smaller): stop, `git checkout --
  Intonare.html`, re-apply. Do not keep patching a truncated copy.
- After JS edits: `node --check` on touched script blocks when practical.
- Before ship: `tools\ship_check.bat` (sentinel + changelog gate).

## Deploy

- Day-to-day Android: `go.bat` → Android Studio Run → clear device cache.
- Play upload day: then `release.bat` → signed AAB.
- iOS: start Codemagic manually (auto-trigger is OFF).
- Native masters: `native_src/` only.

## Tooling

- Audits: `tools/audits/` (see `tools/README.md`)
- Quiz pack tools: `tools/quiz/` (set `INTONARE_HTML` only if not using repo root)
- Run Python tools from the repo root. Defaults resolve to `./Intonare.html`.

## Do not

- Truncate or rewrite all of `Intonare.html` for a tiny change. If
  size collapses after an edit, restore from git first; never keep
  patching the truncated copy.
- Run `release.bat` for everyday testing.
- Assume production is live on Play until Daniele says cutover happened.
