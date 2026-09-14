# Bugbot notes for Intonare

- Single-file app: treat `Intonare.html` edits carefully; flag risky
  bulk rewrites or truncation risk.
- Native masters live in `native_src/`, not only under `android/`.
- Do not suggest a second AudioContext; use shared `getAudio()`.
- American English. No em-dashes in user-facing copy suggestions.
- Before iOS ship claims: top CHANGELOG version must match
  `INTONARE_VERSION`.
- Prefer concrete bugs over style nits unless style causes real harm.
