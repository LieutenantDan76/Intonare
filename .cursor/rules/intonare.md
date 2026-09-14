---
description: Core rules for editing Intonare. Applies to all work on this project.
globs: ["Intonare.html", "*.bat", "*.py", "*.js", "*.json"]
---

# Intonare project rules

## Architecture

This is a single-file HTML/CSS/JS app (~131,000+ lines). All code
lives in one IIFE-structured file. There is no build system for the
app itself. Capacitor + Vite handle native wrapping only.

## Editing the file

- Use exact string replacement, not regex. Find a unique string,
  replace it. Verify the match is unique before applying.
- Never use DOTALL regex on this file. It is ~10MB.
- After any edit, run `node --check` on every script block to catch
  syntax errors.
- The version lives in three synced spots: an HTML comment near the
  top (grep `INTONARE_VERSION:`), a JS const, and the Settings footer
  string. All three must be bumped together.

## Language

- American English throughout. Exceptions that must not be changed:
  Daft Punk, Licence to Kill, Hapshash and the Coloured Coat,
  `createAnalyser`/`AnalyserNode`, `userCancelled`, Baduizm.
- "Semitone" and "bar" are standard American music usage; do not
  replace with "half step" or "measure."
- No em-dashes in user-facing copy. Use semicolons, commas, or
  periods.

## Audio

- One shared AudioContext via `getAudio()`. Never create a second
  one. iOS Safari caps at ~6 contexts and the Capacitor WebView
  goes silent.
- Use the existing `buildLimiterChain()` pattern for all audio output.
- Parameter changes during playback need the bus-swap pattern: fade
  old buses, create fresh ones, reset the scheduler. Gain muting
  alone is not enough.

## CSS

- CSS brace balance must stay at zero diff. Stray braces silently
  break large sections.
- `@property`-registered custom properties are used for animated
  theme transitions. Don't remove them.
- `transition: all` fights requestAnimationFrame updates. Use
  targeted transitions on non-conflicting properties only.

## Common bugs

- Variable named `t` shadows the global `t()` translation function.
  Name loop vars `tone`, `trk`, `tick`, `mode`, etc.
- Dead code: static analysis misses onclick, querySelector, and IIFE
  invocations. Do a full-file sweep before deleting any function.
- Capacitor: `npx cap sync` alone doesn't reliably update assets.
  The go.bat uses manual copy commands. Clear device cache after
  every Android Studio run.

## Workflow

- Prototype-first for visual or audio changes: build a standalone
  HTML mockup, review on-device, then touch the main file.
- On-device screenshots are the reliable verification method.
- When auditing the app, do a real read of the actual screens. A
  regex count is not a finding.
- Read docs/PROJECT_STATUS.md for current state, pending items, and
  known gotchas.
