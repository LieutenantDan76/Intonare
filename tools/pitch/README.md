# Pitch regression bench

Offline ground truth for Intonare's shared FFT-YIN detector.

This is the measurement layer from the mic audit: before more detector
tweaks, we need numbers that do not depend on one phone session.

## Quick run

From the repo root:

```
tools\pitch_bench.bat
```

Or:

```
node tools/pitch/gen_corpus.mjs
node tools/pitch/run_bench.mjs
node tools/pitch/run_bench.mjs --write-baseline
```

Exit 0 = green. Exit 1 = a clip failed its cents/dropout gate, an app
knob pin drifted, or median cents worsened more than 1¢ vs the stored
baseline.

## What it covers

| Piece | Role |
|---|---|
| `yin_fft.mjs` | Offline port of `detectPitch` + FFT from `Intonare.html` |
| `gen_corpus.mjs` | Builds synthetic mono 44.1 kHz WAVs + `corpus/manifest.json` |
| `run_bench.mjs` | Frames each clip (4096 / hop 2048), reports median \|cents\| and dropout % |
| `baselines/synth_baseline.json` | Last accepted synth snapshot (optional regression compare) |

Synthetic tags: `pure`, `rich` (harmonics), `quiet`, `noisy`, `detune`,
`silence`. Real phone recordings can land later under `corpus/live/` with
entries added to the manifest (`expectedHz`, gates).

## App pins

The bench greps live `Intonare.html` for the detector knobs the port
assumes (YIN dip 0.10, clarity 0.18, FFT 8192, RMS floors). If you change
those in the app, update `yin_fft.mjs` and the pins in `run_bench.mjs` in
the same turn.

## Not covered yet (on purpose)

- Native capture / AEC / iOS WebView path (iOS native is the next slice)
- On-device telemetry dump from the running app

PitchEngine (app, v0.210.112+) owns live smoothing/confidence; this bench
still validates the raw FFT-YIN core those filters feed.
