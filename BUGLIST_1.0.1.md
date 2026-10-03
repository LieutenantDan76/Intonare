# Intonare 1.0.1 bug list (traced Oct 2 2026)

STATUS Oct 2 2026: items 1 to 5 below are FIXED in v1.0.1 and written to C:\Users\citti\Desktop\Intonare (Intonare.html + CHANGELOG.md, not committed, not yet device-tested). Drum cursor lookup also cached. Ship gate passed on the PC copy (integrity, sentinel 157 fixes + 260 pins, changelog gate). Still open: Rosanna and Trap 32nds by ear, tone bank synth-first (parked), the unknown source of the bad audio data that silences piano and Rhodes (self-heal added, diagnostics panel shows `_refDiag`).

Rule: wait for the 1.0 review to clear, then batch. Full ship gate on the build.

## Fix
1. Piano and Rhodes go silent (most important).
   - Cause found: both play through one long-lived biquad, `_pianoLidFilter`, behind `refMasterGain`. One burst of NaN into that path poisons the filter for the rest of the session. Organ does not use it.
   - Proven in headless test (before 0.82 level, after NaN). Trigger in real use NOT found. Not reproducible by Daniele. All 15 Train modules enter/exit clean. All 44 REF_TONES synths clean under bad inputs. Samples are the next suspect.
   - Fix: rebuild `_pianoLidFilter` on entering the piano/Rhodes tab (switchPianoToolTab) and on riffStart; add a NaN watch that logs to the audio diagnostics panel (seven taps on the version stamp); sweep other long-lived biquads for the same weakness.
2. Quiz card overflow. `.mq2-opt` is fixed 120px; `.pr/.pw/.ok` raise border to 2px, which narrows the text box and wraps the label to 4 lines. Fix: drop padding by 1px on those states (and nudge `.mq2-key`) so the content box stays the same. Also mq2FitOpts should measure in the revealed state.
3. Theory quiz "key is D minor, which chord of that key is written here". V and vii° exist only in harmonic minor. Label those questions "harmonic minor" (IT "armonica"). New blurb: "Degree 5 of D harmonic minor, which comes out major. The raised seventh is an accidental, not part of the signature." Distractor pool still adds III+ even though the builder avoids it as an answer. Code: mqGenFunction ~line 136500.
4. Rhythm Reading grader (~line 78254). Taps are matched on RAW time, graded on bias-corrected time. A steady early/late lean lets a neighbor 16th steal a tap: note A orange, note B red, real tap shown as a stray. Fix: pass 1 match raw, take median lean, pass 2 re-match on corrected times. Verify against the photo case (extreme, 88 BPM).
5. Chordle picker: qualities live on card 2 behind a swipe. Make that obvious (qualities visible on card 1, or a clear cue). Scoring is correct. Not a bug.

## Check by ear (no bug proven)
- Rosanna Groove: code comment says triplet grid (trackSub 3), the code is a 16th grid with swing 100 plus nudge. Mismatch.
- Porcaro Rosanna fill: 12-slot 8th-triplet grid at 83 BPM, probably sparser than the groove. May be the "slow" feel.
- Trap 32nds: 60fps on desktop. Suspect per-step `querySelectorAll` in updateCursorForTrack on phones. Cache cursor elements.
- Drum preset audit passes (78 presets, 0 errors). It checks structure, not feel.

## Parked
- Tone bank preview plays synth first: code waits for the sample; synth only on failed state or fetch failure. A failed load sticks for the session. Not reproducible. Possible fix: retry a failed voice on tap.

## Dailies (answer)
Chordle and Diadle: seeded pick, easy 2/6, medium 3/6, hard 1/6, never vhard. Tonale: no tiers. Quiz daily: one seeded pack, mixed difficulties.
