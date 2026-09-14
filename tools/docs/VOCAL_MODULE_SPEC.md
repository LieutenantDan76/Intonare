# Intonare Vocal Module Spec
## Warmup + Range Assessment, Ground-Up Design

Last updated: September 9, 2026
Research basis: Six-school vocal pedagogy review, SOVTE clinical literature,
Cooksey adolescent voice stages, voice range profile (phonetogram) research,
competitor app audit (Vanido, SingTrue, Warm Me Up, VoCo, Vocalise).

---

## 1. What this module is

Two modes of one module, sharing onboarding, exercises, the pitch engine,
and history:

**Warm Up** — the daily event. Repeatable, age-aware, two to ten minutes.
The thing a student opens before rehearsal, a lesson, or just because the
app reminded them.

**Find Your Range** — periodic, maybe monthly. Requires a warmup first (or
lets you skip with a warning), then runs the assessment flow. This is the
existing six-step system with upgrades.

Both live under one hub with two doors. Eventually the warmup becomes a
standalone module accessible from the launcher (its own card, like the
tuner or metro). For 1.0 or near-term, it lives where Vocal Range currently
sits but with the hub redesigned.

### Where it lives

Right now Vocal Range is in Tools > Reference, fifth item in a five-item
folder. That's too deep for a daily warmup. Options:

- **Near-term:** Move to its own card on the Tools hub (same level as
  Pitch & Sound, Harmony, etc.), with a name change to "Voice" or
  "Vocal." The card says "Warmup · Range · Voice Type."
- **Long-term:** Its own launcher card as a fifth module, or integrated
  into Train alongside the ear training exercises.
- **Shortcut:** Pin-able and star-able from day one so a returning user
  skips the depth.

---

## 2. Onboarding (once, editable in settings)

Five tappable questions. No typing. Stored in progState and revisitable
from Settings or from the module's gear icon.

1. **Age bracket:** Under 13 / 13 to 17 / 18 and up
   → Drives safety gates, exercise selection, copy tone, range caps.

2. **Experience:** New to singing / Some experience (choir, lessons) /
   Trained (years of study or performing)
   → Drives exercise complexity, cue wording, which tiers are offered.

3. **Is your voice changing?** (shown for ages 10–17 only)
   Yes / Not sure / No
   → Triggers Cooksey-aware reduced-range mode, reassurance copy,
   more frequent re-assessment prompts.

4. **How loud can you be right now?**
   Full volume / Keep it down
   → Toggles quiet mode. Re-asked each session (a chip, not a screen).
   Quiet mode substitutes: hum stays, lip trill stays (it's soft),
   siren becomes a gentle glide on "oo" at lower volume, scales become
   hummed scales. No belting, no loud vowels.

5. **Default session length:**
   Quick (≈2 min) / Standard (≈5 min) / Full (≈10 min)
   → Changeable per session from the warmup hub.

---

## 3. The warmup engine

### Physiological order (never violated)

Every tier follows this sequence. Nothing gets reordered. Shorter tiers
skip later stages, they never skip earlier ones.

1. **Body release** — neck rolls, shoulder drops, jaw stretch
2. **Breath** — sustained hiss on counts, silent rib expansion
3. **Gentle SOVT phonation in mid-range** — hum, lip trill, tongue trill,
   straw phonation (rotate by day)
4. **Glides and registration** — sirens, octave slides connecting chest
   and head
5. **Range and agility** — descending five-note patterns, scales,
   arpeggios
6. **Articulation** — tongue twisters, consonant drills

### Tier breakdown

**Quick (≈2 min):** Steps 2–4 only.
  Breath hiss (15s) → Hum (20s) → Lip trill (20s) → Siren (20s)
  Honest framing: "Wakes up your voice." Not "full warmup."
  Evidence: 1 min of SOVTE produces measurable jitter/shimmer reduction.

**Standard (≈5 min):** Steps 2–5.
  Breath hiss (20s) → Hum (20s) → Lip trill or tongue trill (25s) →
  Siren (25s) → Descending five-note on "oo" (30s) → Octave slides (30s)
  → Scale pattern (30s)
  Evidence sweet spot: 5 min improves ease of singing (EASE P=0.029)
  and female highest F0 (P=0.017).

**Full / pre-performance (≈10 min):** All six steps.
  Neck and shoulder release (30s) → Breath hiss + rib expansion (30s) →
  Hum (25s) → Straw phonation (25s) → Lip trill (25s) → Siren (30s) →
  Octave slides (25s) → Descending five-note "oo" then "ah" (40s) →
  Arpeggio patterns (40s) → Tongue twister (20s)
  10 min maximizes phonation threshold pressure benefit. 15 min adds
  nothing (Ragsdale/Lloyd 2020).

### Exercise rotation

Each slot in the sequence has 2–3 variants that rotate by day:

- SOVT slot: hum / lip trill / tongue trill / straw phonation
- Glide slot: siren / octave slide / fifth slide
- Scale slot: descending five-note / major scale / pentatonic
- Vowel slot: "oo" / "ee" / "ah" / "oh"
- Articulation slot: "red leather yellow leather" / "unique New York" /
  "she sells seashells"

Rotation prevents the routine from feeling identical every day.

### Exercise screen (each exercise)

- **Breathing ring and countdown timer** (already built, keep it)
- **Piano reference** on pitched exercises: the app plays the target
  pattern so the user has something to match. Uses the existing synth
  engine (the piano is already in the app). Key adapts to the user's
  stored range.
- **Pitch trace** on pitched exercises (siren, scales, arpeggios):
  a live scrolling line showing where the user is against where the
  pattern goes. Same pitch detection the tuner uses.
- **Steadiness indicator** on SOVT exercises (hum, trills, straw):
  pitch detection is unreliable on trills, but you can read amplitude
  steadiness. Show a simple "steady / wavering" indicator.
- **One plain-language cue** per exercise about what it does FOR the
  user, not how it works physiologically:
  "Loosens your cords before you ask them to work"
  NOT "reduces phonation threshold pressure."
- **Skip** always available, no penalty, no guilt.

### End of warmup

**"How does your voice feel?"** Three taps: Easy / Fine / Tight.
This is the self-rated ease metric from the research. It's the most
useful data point you can collect because the mic can't measure perceived
effort. Stored with the session. Drives the safety prompts (see §7).

---

## 4. Age gates

### Under 13

- **Quick and Standard only.** No Full tier.
- Sirens capped to the comfortable range from their last assessment, or
  a conservative default (A3–A4 for most children).
- **Playful exercise names:**
  Siren → "Fire truck"
  Hum → "Cat purr" or "Bee buzz"
  Lip trill → "Motorboat"
  Tongue trill → "Rolled R race"
  Straw → "Bubble straw" (if available)
- No straw phonation, no arpeggios, no belting exercises, no distortion.
- Cues talk about play, not technique: "Make the sound go up like a
  fire truck!" not "Connect your registers through the passaggio."
- Range assessment available but no pushing. "As high as feels good"
  with no pressure language.

### 13 to 17, voice changing

- All tiers available.
- Sirens and scales capped to a narrower band (stored comfortable range
  minus a buffer of 2 semitones at each end).
- **Reassurance copy:** "Your voice is changing and that's completely
  normal. Some days it'll crack or feel different from the day before.
  That's fine. We'll keep the exercises where your voice is right now."
- Range assessment recommends re-running every 2–4 weeks.
- No push toward high notes. "That's your comfortable top for today"
  language.
- The voice type result adds: "Voice types shift during these years.
  This is where you are right now, not where you'll end up."

### 13 to 17, voice NOT changing (or female)

- Standard adult exercises with slightly simpler cues.
- Full tier available.

### 18 and up

- Everything available. Full toolkit.

### Seniors (future consideration)

- Gentle, systematic 10–15 min warmups.
- Account for presbyphonia (fold thinning), reduced breath support.
- Slower exercise pacing.

---

## 5. Range assessment upgrades

Keep the existing six steps:
1. Warmup
2. Lowest comfortable note
3. Highest comfortable note
4. Tessitura scan (free singing, app tracks center)
5. Extended low (optional)
6. Extended high (optional)

### Additions

**Required warmup on first run.** After that, optional but recommended
with a note: "A warmed-up voice and a cold one measure differently.
Results are most reliable after a warmup."

**Falsetto flip detection.** During the high comfortable and extended
high steps: when the pitch jumps roughly an octave or the harmonic
spectrum thins out suddenly (detectable as a drop in higher partials),
show: "That sounded like it shifted to a lighter register. Try again
with the same fullness you had a note ago, or tap Skip if that's your
comfortable top."

**Strain detection.** Volume spike plus pitch instability at the top
of the range = pushing. The app stops the step: "That's your comfortable
top for today. No need to push further."

**Confidence on the result.** If the tessitura center is within 2
semitones of the boundary between two voice types, show both:
"Likely Baritone, possibly Tenor." Never present voice type as a verdict.
The existing vrMatchVoiceType uses nearest-center matching, which is
correct. The upgrade is in how the result is displayed, not computed.

**Passaggio zone estimation.** During the siren or glide exercises,
watch for spots where:
- Pitch tracking wobbles (detection confidence drops)
- The timbre shifts (spectral centroid changes)
- Dynamic control narrows (volume range compresses)
Mark these on the range strip as "transition zones" with a soft gradient
edge, not a hard line. Label: "Your voice shifts somewhere around here."
Don't claim precision. This is an approximation.

**Day-to-day stability band.** Normal fluctuation between consecutive
measurements is about 3.5% for frequency and 2 dB for intensity
(Printz et al. 2018). Show a stability band on the range chart so
users don't misread noise as progress or loss.

---

## 6. History and progress

Keep what's there (session history, range over time, voice type). Add:

- **Stability band** on the range chart (see above)
- **Warmup streak** as its own counter (separate from practice streak)
- **Voice feel trend** from the Easy/Fine/Tight taps, shown as a simple
  color strip over time. Three "Tight" in a row triggers a nudge.
- **Breath duration** from the hiss exercise (how many counts they hold),
  tracked over time
- **Pitch accuracy** on scale exercises (average cents deviation),
  tracked over time. Only on open-vowel exercises, not SOVT.
- **Tessitura center** tracked over sessions, showing whether it's
  stable or drifting (relevant for adolescents)

---

## 7. Safety

- **"Stop if anything hurts, feels scratchy, or sounds hoarse"** stays
  visible on every exercise screen. Not just the intro.
- **Entry check** at the start of every warmup session:
  "Sore throat or hoarse today?" Yes → Rest Mode (one minute of gentle
  hum at a comfortable mid-range pitch, then done) or skip entirely.
- **Never say "your highest note."** Always "as high as is comfortable."
- **Three "Tight" in a row** → "Your voice has felt tight the last few
  sessions. Consider a rest day. If it stays that way for two weeks,
  it's worth seeing a teacher or a doctor."
- **No repeated maximal-note demands.** Cap range probes. Let users bail
  without penalty.
- **Not medical advice disclaimer** on the range results screen:
  "This is an estimate based on what the mic heard, not a clinical
  assessment. For persistent voice issues, see a specialist."
- **Children and teens** never see belting, distortion, or max-range
  exercises.

---

## 8. Quiet mode

Toggled per-session from the warmup hub (a chip or toggle, not buried
in settings). Substitutions:

- Hum → stays (it's already quiet)
- Lip trill → stays (soft enough)
- Tongue trill → stays
- Siren → gentle glide on "oo" at lower volume
- Scales → hummed scales
- Arpeggios → hummed arpeggios
- Tongue twister → whispered or dropped
- Straw phonation → stays (near conversational volume)

The point: a user in a shared apartment, a dorm, or backstage can still
warm up without annoying everyone around them. SOVT exercises are
designed to be low-volume, which is one of their advantages.

---

## 9. Rest mode

For sick or vocally fatigued days. Triggered by the entry check or
selectable manually.

- One minute of gentle humming at a self-chosen comfortable pitch
- No pitch detection, no feedback, no scoring
- Breathing exercise (hiss on counts) if they want more
- Voice feel rating at the end
- Counts toward the warmup streak (so you don't lose it for being sick)
- Copy: "Some days the best thing for your voice is almost nothing."

---

## 10. Progression

Exercises get harder as the user's history builds. Tracked per exercise
slot, not globally.

**Beginner (first 2 weeks or "New to singing"):**
- Narrow range on all pitched exercises (one octave centered on
  tessitura)
- Slower tempo on scales and arpeggios
- Simpler patterns (five-note descending, no arpeggios)

**Intermediate (after 2 weeks or "Some experience"):**
- Range widens toward comfortable boundaries
- Tempo increases slightly
- Arpeggios introduced
- More vowel variety

**Advanced (after 2 months or "Trained"):**
- Full comfortable range
- Faster agility patterns
- Chromatic runs
- Style-specific warmups (classical vowels, CCM belting prep, etc.)
  as unlockable add-ons

Progression is automatic based on consistency and stored range, but
the user can override in settings.

---

## 11. Technical integration with existing Intonare systems

**Pitch detection:** Uses the same YIN/autocorrelation engine the tuner
uses. Already accurate to ±1–2 cents on clean single tones. Works well
for sustained tones, scales, and glides. Less reliable on SOVT sounds
(trills), so those exercises use steadiness/duration feedback instead.

**Piano reference tones:** Uses the existing grand piano synth from the
Piano tool. Patterns are generated from the user's stored range center,
transposed to sit comfortably.

**Mic and audio:** Uses the existing mic pipeline (startMic, analyzer,
the native mic path on Android). The null-analyzer fix from v0.209.35
is relevant here.

**Session timer:** Contributes to the existing practice session timer
(the 0:XX / 20:00 counter in the header).

**Streak system:** Warmup sessions count toward the existing daily
practice streak if they meet a minimum duration (completing at least
one full tier).

**Bilingual:** All exercise names, cues, onboarding questions, results
copy, and safety messages need EN and IT strings. The playful child
names ("fire truck," "motorboat") need Italian equivalents
("autopompa," "motoscafo").

---

## 12. What a guided app does well vs what needs a teacher

**The app does well:**
- Consistent, well-sequenced warmups every time
- Pitch and range mapping
- Real-time pitch feedback on open-vowel exercises
- Progress tracking over weeks and months
- Enforcing timing and structure
- Being available anywhere, any time

**What still needs a teacher:**
- Diagnosing breath support and laryngeal tension
- Correcting registration and mix
- Judging healthy vs strained production
- Posture and body work
- Catching bad habits before they entrench
- Nuanced problem-solving for individual voices

**The app's responsibility:** pair every metric with a plain-language
"what this means" note, never claim clinical precision, and recommend
a teacher when something is outside its scope.

---

## 13. Competitor gap

| Feature | Vanido | SingTrue | Warm Me Up | VoCo | Intonare (planned) |
|---|---|---|---|---|---|
| Physiological exercise order | No | No | Partial | No | Yes |
| Age-aware safety gates | No | No | No | No | Yes |
| SOVTE core | No | No | Yes | Yes | Yes |
| Pitch feedback during warmup | Yes | Yes | No | No | Yes |
| Tessitura-based classification | No | No | No | No | Yes |
| Passaggio estimation | No | No | No | No | Yes |
| Strain/flip detection | No | No | No | No | Yes |
| Session length options | No | No | Yes | No | Yes |
| Quiet mode | No | No | No | No | Yes |
| Voice-change support (teens) | No | No | No | No | Yes |
| Progress tracking | Yes | Partial | No | No | Yes |
| Plain-language coaching cues | No | No | Partial | Yes | Yes |

No competing app combines a physiologically sequenced, age-gated warmup
with a tessitura-based range assessment and plain-language feedback.
That's the opening.

---

## References

- Titze, I.R. (2006). Voice training and therapy with a semi-occluded
  vocal tract. Journal of Speech, Language, and Hearing Research.
- Ragsdale, Marchman, Bretl, Diaz, Rosow, Anis, Zhang, Landera & Lloyd
  (2020). Effects of warm-up duration on voice range profile. Journal
  of Voice. n=9 pilot.
- Kang, Xue, Gong, Hao (2019). Straw phonation and phonation threshold
  pressure. Journal of Voice.
- Printz, T. et al. (2018). Reliability of VRP measurements. Logopedics
  Phoniatrics Vocology.
- Cooksey, J.M. (1977–2000). Male adolescent voice change stages.
- Miller, R. (1996). The Structure of Singing. Wadsworth/Cengage.
- Sundberg, J. (1987/2001). The Science of the Singing Voice. Northern
  Illinois University Press.
- Roers, Mürbe & Sundberg (2009). Vocal fold length and voice
  classification. Journal of Voice.
