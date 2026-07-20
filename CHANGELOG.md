# Intonare — Changelog

A human-readable record of what changed, when, and to what specific value. This
is the companion to `intonare_regression_sentinel.py`: the sentinel proves a fix
is *present*; this log tells you what the fix *was* and what exact value it used.

**How to use:** newest at top. When something feels off, scan here first — you're
looking for "when did this value last change, and to what?" rather than digging
through old chats. Each entry: version · area · what changed · (old → new) where a
value moved. Values marked 📌 are exact-pinned in the sentinel — changing them
deliberately means telling Claude so the pin updates too.

> Entries before v0.20.36 were reconstructed from chat history and are
> approximate on dates/versions; values were verified against the file where
> still present. From v0.20.36 on, entries are recorded live as work happens.

---

## v0.97.82 — Launcher titles, icon glows, and the purple pulled back

Three separate things.

**Light titles were not changing, and the reason was a duplicate rule.** `body.light .lnch-cell .lnch-nm { color: var(--text) }` appears twice in the stylesheet, 16k characters apart. The tinted ink from the last build was landing on the first one, and the later copy was quietly winning on source order. Worse, `--text` on the launcher resolves to whichever module the body class happens to be, so all four cards wore the tuner ink no matter which module they named. Each cell already sets its own `--lc`, so the title derives from that now. Capped at 22% tint: 42% looked right but measured 2.6–3.8:1, while 22% clears 4.5:1 on every surface the launcher can sit on.

Worth recording as a method note: I added a competing rule at matching specificity first, and it did nothing, because the problem was source order rather than specificity. Searching for *later* duplicates should come before reasoning about specificity at all.

**The icon glows were a dark-mode device left running in light mode.** `.practice-icon svg` carries `drop-shadow(0 0 6px …)` with no light override. On a dark ground that reads as light emission; on a light surface it smears a dark halo under the icon, which is why the folders looked dirty. Filter removed in light mode.

**Dark train was too intense** because I kept FLAT's saturation *percentage* while raising lightness, and the same percentage produces far more chroma at higher lightness. Train's channel spread went from 19 steps to 29. Each theme is now solved for its own original spread instead: train back to 19, tools 10, metro 9, so the tint survives the lift without amplifying.

---

## v0.97.81 — Tinted ink in light mode; dark lift pulled back

**Why light mode read like a reversed image.** The ink was a near-neutral dark grey at 14% saturation, and the same three values were used on every module. Against a 42%-saturated lavender, gold or teal surface, neutral text does not belong to what it sits on: the surface carries chroma, the text does not, and the eye reads it as an inverted photograph rather than a designed light theme.

Each module's ink now carries that module's own hue at 30% saturation, holding identical contrast floors. Tuner takes a blue-violet ink (`#232742`), metro a warm brown (`#2e2919`), tools a deep green (`#182d29`), train a purple (`#292546`). Same 7.0 / 5.0 / 4.6:1 as before; the difference is that the text now belongs to its surface.

**On dark being washed out, the lift was not the main culprit.** I had also flattened per-theme saturation to a uniform 22%, where FLAT ran 36–58% per module. That drained the colour: train's channel spread went from 19 steps to 11. Each theme now keeps its own saturation, and the base lift is pulled back from luminance 0.0075 to 0.0050 — under Material's `#121212` reference rather than past it, and still roughly double FLAT's elevation step.

Result: train's base returns to a deep blue-violet instead of a washed grey, and every theme's channel spread is now wider than FLAT rather than narrower. Text holds at 11.7:1 worst case with `--muted` at 5.23:1.

---

## v0.97.80 — Light mode saturation restored; dark LIFTED goes live

**Reverting an overreach.** The ask in v0.97.76 was fonts, SVGs and element colours. In v0.97.78 I rewrote the surface palette from 42% saturation down to 13% and shipped it as part of a "matching" pass. The 60-30-10 reasoning behind it was sound, but whether Intonare's light mode should read as coloured or as neutral is a design decision, and it was not mine to fold into a maintenance change without asking. "Lifeless and colorless" is the correct description of the result.

All four module themes are back to the values approved in v0.97.75: tuner `#acb2dd`, metro `#c7b375`, tools `#6ec4b2`, train `#b4b0df`, at 42% saturation.

Two things reverted with them, because they were solved *against* the desaturated surfaces and fail on the real ones. The softened ink would have landed at 6.28:1, 4.51:1 and 4.25:1 — all three under their floors — so the v0.97.75 values are back at 7.04:1, 5.05:1 and 4.61:1. And the tab pill's outline returns: at this saturation an accent-coloured pill genuinely cannot separate itself on hue alone, so the border is doing real work rather than propping up a weak palette.

Kept from that pass: the stale-token replacements, the three missing dark-element overrides, and the tab bar being built from the ramp instead of from white. Those were the actual fixes.

**Dark mode LIFTED is now the default.** Base lifted off near-black, elevation steps roughly tripled in absolute luminance, text at ~14.5:1 instead of 17.3:1, and `--muted` moved from a failing 2.54:1 to 4.64:1. FLAT stays available in Settings for the old ramp, and still carries the `--muted` fault by definition.

---

## v0.97.79 — Dark mode gets an opt-in rebuilt ramp

Not a hard change: this ships behind **Settings → Dark Depth (FLAT / LIFTED)**, defaulting to FLAT, which is byte-identical to what has been shipping. Nothing moves unless it is switched on.

First, the thing dark mode does **not** have: light mode's saturation problem. The per-module dark backgrounds report 36–58% HSL saturation, which looks alarming until you check the channel spread — `#050f0d` is RGB(5,15,13), a span of 10 steps out of 255. HSL saturation is a ratio, so it inflates as lightness approaches zero. The light-mode fault was 42% saturation at luminance 0.46, an ~80-step spread and genuinely vivid. Different geometry, so the fix does not transfer.

What dark mode does have, measured:

**Elevation steps of ~0.0024 in absolute luminance,** against the rebuilt light ramp's ~0.08 — roughly 40× smaller. That is the same "cards dissolve into their containers" problem Linda reported in light mode. Contrast *ratios* hide it because the WCAG formula adds 0.05 to both terms, which compresses everything near zero; the ratio reads 1.045:1 and looks merely tight rather than invisible. LIFTED spaces elevation by absolute luminance instead, roughly tripling each step.

**`--bg-0` at luminance 0.0033,** effectively pure black. Sources are consistent that pure black causes eye strain and leaves shadows unreadable; Material puts its dark surface near `#121212`.

**Text at 17.3:1.** Above roughly 15:1, light text on a dark ground starts to bloom, worst for readers with astigmatism. LIFTED uses an off-white at ~14.5:1, still double the 7:1 AAA floor.

One genuine bug surfaced on the way: **`--muted` was failing dark mode at 2.54:1**, well under the 4.5:1 floor, and has been for as long as it has existed. LIFTED puts it at 4.64:1. Worth noting that FLAT still carries this fault, since FLAT is defined as "unchanged"; fixing it there is a separate decision.

Recommendation stands from the last message: dark mode is the default, it has been in testing for months, and nobody has reported it. Compare the two on a real screen before deciding, and leave it on FLAT for the production push if there is any doubt.

---

## v0.97.78 — Light mode restructured as a system, not a set of tokens

"Still feels a little off" was right, and reading the design literature found the reason. I had been tuning individual values without checking the structure they sat in.

**The 60-30-10 split.** The established professional distribution puts 60% on a dominant neutral (backgrounds, containers, surfaces), 30% on secondary surfaces, and 10% on accents, where colour does its heaviest lifting. Keeping accents at 10% is what preserves their signal value.

I had the surface tier — the largest area on screen — running at 42% saturation. That is accent-level colour on the dominant layer, and it explains every symptom left over. The accents had nowhere to go: metro's accent sat 4° from its own background hue, tools 12°, train 9°. Same hue family, differing only in lightness, on a surface already carrying heavy chroma. Active states read weakly, and the tab pill needed a border to be legible at all — a crutch, not a design.

The literature also warns that high-saturation surfaces cause simultaneous contrast at boundaries and leave no room for hover, active or selected variations. Both were happening here.

**The surface tier is now a chromatic neutral at 13% saturation:** tinted enough to read as deliberate rather than accidentally off-neutral, quiet enough to stop competing. Each module keeps its own hue, so the identity survives; the colour just stops shouting from the background.

Consequences worth noting. Accents now carry 4.4–6.0:1 against backgrounds and 6.6–9.2:1 on panels, and they are the only saturated thing on screen, so the tab pill's border is gone. The active state reads on its own.

**And the text lightening asked for two builds ago is now possible.** With the surfaces quieter there is finally headroom: `--text` 7.87:1, `--text-dim` 5.64:1, `--muted` 5.15:1 before any change, so all three inks were softened (`#272834`→`#2f303e`, `#3d3e51`→`#44455a`, `#424458`→`#47495f`) and still clear their floors. Last build that was impossible without brightening the whole app; the problem was never the ink, it was what sat behind it.

---

## v0.97.77 — Tab bar rebuilt from the ramp instead of from white

The white backgrounds were my mistake in the last build. I mixed both the bar and the active pill with `#ffffff`, which made the pill 86% white: a foreign chip sitting on a coloured bar rather than part of the surface family, and mixing the bar with white too pulled it away from `--bg-0` so the strip stopped matching the screen above it.

Both now come from the palette. The bar is `--bg-0` exactly, so it continues the screen. The active pill is `--panel`, the ramp's own raised layer, which lands 1.43–1.45:1 above the bar and carries the module accent at 5.6–7.8:1. No white anywhere in the strip.

Checked the rest of the file for the same mistake: the other light rules touching `#ffffff` are white *text* on coloured fills, which is correct, and the settings chip mixes 30% white into a dark accent, which still reads as the accent.

**On lightening text and symbols universally: I did not do it, and the numbers are the reason.** The three ink tokens currently sit at 7.04:1, 5.05:1 and 4.61:1 worst-case across the four themes — each already at its floor with zero headroom. Lightening them 15% while the surfaces hold drops `--muted` to 3.92:1, which is the exact failure that made light mode hard to read before this whole pass began.

Contrast is a ratio, so the only way to soften the ink is to lift the surfaces with it. Solving for that puts `--bg-0` at luminance 0.62 against the current 0.46 — considerably brighter, the opposite of the complaint that started this. If the ink genuinely reads too heavy on the device, that is the trade to make deliberately rather than by accident, and it means accepting a brighter app.

SVG strokes and fills were swept separately: exactly one value falls under the 3:1 UI-graphics floor, a deliberately pale piano lid fill.

---

## v0.97.76 — The rest of light mode caught up with the new palette

Follow-up pass on the elements the palette rebuild did not reach.

**39 stale values were frozen at the old palette.** Surfaces like the old panel and surface colours were hardcoded in 65 places rather than referencing the token, so they did not move when the palette changed and sat visibly against the new backgrounds. Those now use `var(--surface)`, `var(--panel)`, `var(--bg-0)` and friends, so they follow the palette from here on. The `lt-bright` restore block was deliberately left alone, since its whole job is holding the old values.

**The tab bar had no light-mode rules at all.** It inherited dark styling: the active pill used `--panel`, which against a light bar is a 1.4:1 difference and reads as nothing, and no element carried the module colour, so every tab looked identical regardless of which was selected. That is the "odd and colorless" complaint. The active tab now takes a tinted surface with the module accent on its icon, label and border (6.5–8.6:1 on the pill), while inactive tabs stay muted.

**Three elements never got a light value** and kept their dark fill as smudges on a light surface: spent hearts, lost pixel-hearts, and the Rhodes knob indicator.

On "some text feels dark": the tokens themselves measure 9.1:1, 6.5:1 and 5.9:1 against the new surfaces, which sits in the comfortable band rather than the harsh one, so they were left alone. The near-black text values that turned up in the sweep are all sitting on bright accent buttons, where dark ink is correct.

Also confirmed the six draw functions flagged as having no light branch are all inside `keep-dark` regions (CRT screens, piano overlay, Road Trip, splash), which opt out of light mode deliberately. Their colours are right as they are.

---

## v0.97.75 — Light mode rebuilt around measured luminance

Linda's report was "too bright, hard to read". Measuring it turned up three separate problems, only one of which was brightness.

**Brightness was inconsistent between modules.** Metro and tools sat at luminance 0.66 while tuner and train were at 0.53, so switching tabs changed how bright the screen was. Every module theme is now normalised to the same luminance (0.46, dimmer than all four were), so the app no longer flashes brighter when you move between them.

**Layers were invisible.** Surfaces sat 1.04–1.11:1 apart, well under the ~1.2:1 where a light surface reads as separate from the one behind it, so cards dissolved into their containers. That is most of the "hard to see things". Steps are now ~1.13:1 with borders at 2.2:1 against panels.

**`--muted` was already failing WCAG at 4.29:1** before any of this, on the darkest theme. Text tokens were re-solved against the new backgrounds: 7.0:1, 5.0:1 and 4.6:1 worst-case across all four modules.

On the suggestion of saturating the backgrounds — that was the right instinct with a catch worth recording. Saturation moves luminance in opposite directions depending on hue: blue contributes 7% of perceived brightness, green 72%. Saturating tuner and train darkens them; saturating metro and tools *brightens* them. Applied uniformly it would have made the two worst offenders worse. So the target here is luminance directly, with saturation (42%, up from 29%) landing wherever each hue needs it.

**Settings → Light Brightness (SOFT / BRIGHT)** restores the previous palette exactly, for whoever prefers it. Real values rather than a filter, so nothing shifts hue. The control only appears in light mode.

Also darkened 21 hardcoded colour values across the piano overlay, riff cards and tone chips. Those were already marginal at 3.0–4.4:1 and the dimmer surfaces made them slightly worse; all now clear 4.6:1 on every module theme.

---

## v0.97.74 — Dragging the tempo slider no longer machine-guns the kit

Direct consequence of the last build. A re-anchor cancels pending audio and restarts every track's pattern from phase 0, which is right for one tempo change and wrong sixty times a second. Dragging a range input fires roughly that many `input` events, so every one was re-triggering the downbeat.

The tempo value and the re-anchor are now separated. `bpm`, `dk_bpm`, the beat length and the readout all update on every event, so the display tracks your finger exactly as before. The re-anchor waits 140ms for the drag to settle and then fires once. That is also the musically sensible moment for it — there is no point realigning the groove to a tempo you are still scrubbing past.

During the drag itself nothing is rescaled, so both engines simply continue from their existing pointers using the same new beat length and stay locked to each other. The grid keeps its old phase until you let go.

Simulated a 60-event drag from 120 down to 45: **one** re-anchor instead of sixty, and every track still lands on the new grid with chords 0.0ms from a drum hit. A single tap on +/- still produces exactly one re-anchor and updates the readout immediately, so discrete changes feel no different.

---

## v0.97.73 — Stopped rescaling and just re-anchored everything

Yes, there was a simpler solution, and asking for it was the right call. This deletes more than it adds.

Every fix in this run shared one assumption: that a tempo change means taking each engine's pending times and multiplying the remainder by `prevBpm / newBpm`. That built up three rescale functions, a shared-anchor variable and a latency constant, and it kept failing for a reason the arithmetic hides. Every pending value is itself derived from the *old* tempo, each engine holds a different number of them, and any error scales with the ratio — which is precisely why it got worse the further the slider moved.

**Nothing now reads the old tempo at all.** A tempo change picks one restart point 60ms out and tells the chords, the kit and the metronome to resume exactly there with the new seconds-per-beat. Anything already committed past that point is cancelled. There is no ratio in the code, so alignment no longer depends on the size of the change: 30→300 is the same operation as 120→118.

Verified at 120→45, 45→120, 120→200, 200→30 and 30→300. Every kit track's spacing is a whole multiple of the new grid and every chord lands 0.00ms from a drum hit, including the 6.7× and 10× changes that are far harsher than anything the slider does.

Gone: `dk_retimeForBpm`, `retimeMetroForBpm`, `_retimeAnchor`, `PROG_COMP_LATENCY`, and the per-engine rescaling inside `setBPM`. Four moving parts replaced by one function.

Kept: the drum node registry, because cancelling already-committed audio is still necessary — the scheduler calls `start()` ahead of time and those nodes cannot be rescheduled, only stopped.

The lesson worth keeping: the reason this took so many attempts is that each fix was locally correct. Rescaling *is* the right way to convert a duration between tempos. It was the wrong thing to be doing at all.

---

## v0.97.72 — Reverted the snap, and cancelled the stale hits instead

The snap in v0.97.71 was a regression and this reverts it.

**Why it was wrong.** It snapped each track independently to the next step boundary on the new grid. Every track sits at a different point in its own step, so each got a different correction, and any track more than one step out was clamped down to a single step by a `Math.min(1, …)`. Tracks that were locked together landed on different beats — hits appearing where they were never due. The kit's tracks are one groove and have to move as a rigid body; proportional rescaling from a common instant is the only transform that preserves their relative positions, so that is what both engines do again.

**Two real causes fixed underneath it.**

Both retimes read `ctx.currentTime` themselves, at different points inside `setBPM`. The audio clock advances between those two reads, so the kit and the chords were rescaling from slightly different origins — at a ratio of 2.67 even a 2ms gap puts the grids ~3ms apart, and every later event inherits it. `setBPM` now captures the instant once and both retimes use it.

And the part that was actually audible: the scheduler had already called `start()` on every hit inside its lookahead, carrying the old tempo's spacing. Rescaling pointers moves future hits and cannot touch those. Measured ~80ms of old-tempo audio surviving each change, consistently, on every track. Drum voices now register their nodes, and a tempo change stops any that were due after the change; a hit that never sounds is far less noticeable than one landing at the previous tempo, and the scheduler refills from the corrected pointer on its next tick.

Verified across 120→45, 45→120, 120→200 and 200→60: every track's spacing is a whole multiple of the new grid, and chords land 0.0ms from a drum hit in all four. Steady playback with no tempo change triggers no cancellation and is untouched.

One note on the measurement, since it cost time here: hooking `triggerInstrument` records hits that were *scheduled*, including ones later cancelled, so the log kept showing an 80ms residue that was no longer in the audio. Filtering to surviving nodes is what made the fix legible.

---

## v0.97.71 — Tempo changes stretched the wait instead of snapping to the new grid

Stepping back and taking the three constraints seriously — kit only, on tempo change, worse the bigger the change — finally located it. Every previous fix was aimed at steady-state playback, which was never broken.

**What the retime was doing.** Both engines rescaled the time remaining until their next event by `prevBpm / newBpm`. That is mathematically correct: it preserves exactly how many beats away the next event is, and I verified that it does. It also stretches the *wait* by the full tempo ratio. Slowing 120→45 turned a 0.29s wait into 0.77s.

For that stretched moment the kit produces nothing new, while the hits already handed to the audio graph keep sounding at the old spacing. Caught in the act: right after a 120→45 change the kicks were 0.667s apart — the old half-beat — while the new grid was 1.333s. The chords, which commit far fewer events per bar, were already on the new tempo. Hence chords ahead of drums, only with the kit, and worse the larger the change.

**The fix is to snap rather than stretch.** Both engines now keep the unelapsed *fraction* of the current step and apply it to the new step length, so playback resumes in tempo almost immediately and leaves no window for stale audio to disagree.

Measured across 120→45, 120→200 and 45→120: every chord now lands within 0.0ms of a kick, and every gap between kicks after a change is a whole multiple of the new grid. Before, the first gap was half what the new tempo called for.

Also worth stating plainly: the steady-state timing was correct the whole time, and I kept re-measuring it because it was the thing I knew how to measure. The bug only ever existed in the transition.

---

## v0.97.70 — The chord scheduler could not survive a busy main thread

Every measurement so far has come back clean while the problem stayed audible, which meant the measurements were wrong, not the ear. They were all taken on an idle headless container. The phone is not idle.

**The chord scheduler queued only 0.1s ahead and drove itself with a chained `setTimeout`.** The drum kit queues 0.12s ahead on a `setInterval`. That difference is invisible when nothing else is competing for the thread and decisive when something is.

Simulated a phone's render load — a 70ms stall every 200ms — and measured how far ahead of the audio clock each chord was actually scheduled. With the widened lookahead the tightest case had 9.4ms to spare. Under the old 0.1s window the same stall would have put it at **−90.6ms**: the note handed to the audio graph after the moment it was supposed to start, which the browser then plays immediately. Late by however long the thread was blocked.

That is not a fixed offset, which is why compensating by a constant never worked. It varies with how hard the device is working, and it only ever hit the chords — the kit's larger window and `setInterval` cadence meant a stalled tick never pushed its next one back. Chords late, drums on time, exactly as reported.

Three changes:

Lookahead widened from 0.1s to 0.2s, so a tick can be delayed by up to 200ms and still schedule its notes in the future.

The per-chord grid rebuild now runs in a `requestAnimationFrame` instead of inline. It was firing on the main thread at the precise moment a chord started — the same moment the scheduler needed to queue the next one — putting layout and paint work directly in the audio path. Cheap in a container, not cheap on a phone.

Added `progSyncDiag()`, reachable from the console or the diagnostics panel. It records actual scheduled times on the device along with `baseLatency` and `outputLatency`, two numbers that do not exist in a headless container and differ wildly between devices. If this still is not fixed, run it while the drift is audible and the numbers will say where the time is going rather than leaving me to guess.

---

## v0.97.69 — The drums now share the same output chain

"Groove works, kit doesn't" was the detail that solved this, and I had been walking past it for three builds.

The chords and the metronome/groove both run through `buildLimiterChain`. The drum kit connected straight to its own gain node. That chain contains a `DynamicsCompressorNode`, which carries a 256-sample lookahead — measured at 5.99ms. So chords and groove were both delayed by the same 6ms and matched each other perfectly, while the drums came out 6ms ahead of both.

That is why the groove always sounded right. It was never that the groove was correct and the kit was broken; it was that the groove shared the chords' delay and the kit didn't.

**And it means the previous fix was actively wrong.** Compensating on the chord side aligned the chords to the drums while simultaneously pushing them 5.8ms off the groove, which had been correct all along. Fixing one pair broke the other, which is what you were hearing. That compensation is reverted.

The drums now go through the same chain as everything else. All three voices carry one identical latency, so nothing needs per-voice correction — measured separately, each path now sits at 5.99ms with 0.0ms spread between them. In the app, chord and drum scheduling times are identical at 45, 120 and 200 BPM.

Two things worth recording from the hunt. Instrumenting both engines showed the schedules were always correct, including at the tempo extremes, with zero accumulating drift over 16 seconds — so every tempo-scaling fix was aimed at a bug that wasn't there. And a fixed offset in the output path is the thing that behaves exactly like your description: constant in milliseconds, inaudible when beats are close together, obvious when they are far apart.

---

## v0.97.68 — The chords and drums take different signal paths

The scheduling was never the problem. Instrumenting both engines at 50 BPM showed chord onsets at 0.0, 2.4, 3.6 and 4.8 seconds and drum onsets at 0.0, 1.2, 1.8, 2.4, 3.6 and 4.8 — every chord landing exactly on a drum. Perfectly aligned on paper, and still audibly off.

**Because they do not come out of the speaker at the same time.** Chords run through the limiter chain: a low shelf into a `DynamicsCompressorNode`. The drum kit connects straight to its own master gain with no compressor. A `DynamicsCompressorNode` has a spec-mandated 256-sample lookahead — it delays the signal so it can react to peaks before they arrive — which at 44.1kHz is 5.8ms. Measured the two paths against each other in an offline context: 5.99ms of extra delay on the chord side, matching the spec figure almost exactly.

So the chords were scheduled correctly and arriving 6ms late, every time, on every beat. A constant offset like that is buried at fast tempos and exposed once the beats have space around them — which is precisely "it's only obvious when I slow it down", and why two rounds of tempo-scaling fixes did not touch it.

Chords are now handed to the audio graph 5.8ms earlier so both paths reach the output together. Verified in an offline render: the two arrive within 0.18ms, down from 6ms.

The compensation applies only to the moment the note is handed over. `progNextAudioTime` still holds the true musical position, so the sequence's own spacing is untouched and nothing accumulates. The visual chord highlight also stays on the musical grid rather than the compensated time — the sound leaves the compressor on the grid, so that is when the eye should see it.

---

## v0.97.67 — The drums were running at a different tempo

The actual cause, and it was never the attack envelopes.

**The drum machine keeps its own tempo in `dk_bpm`**, and its scheduler computes every step length from that rather than from `bpm`. The two were being allowed to diverge, so the kit and the chords ran at genuinely different speeds. Measured after loading Mixed Rhythm: chords at 90, drums at 95. Changing tempo live was far worse — the chords went to 45 while the drums stayed at 90, a 2:1 mismatch.

Two clocks a few BPM apart do not sound like a fixed offset. They slide continuously, which is why the chords seemed late at one point in the loop and early at another, and why it was obvious at slow tempos where each beat has space around it.

**Two separate leaks, both closed:**

Loading a preset set `dk_bpm = bpm` and *then* called `loadPreset()`, which ends with `dk_bpm = p.dk_bpm` — so the drum preset's own tempo won every time. The order is now reversed.

Live tempo changes only synced `dk_bpm` inside `progRetimeForBpm`, which runs solely while the progression is playing and only in 'kit' sync mode. Every other tempo change left the drums behind entirely. The sync now lives in `setBPM`, which is the single place tempo changes and therefore the one place nothing can bypass.

**Another temporal dead zone bug on the way in.** `dk_bpm` is a `let` declared far below `setBPM`, and a `let` accessed before its declaration throws rather than reporting undefined — so the `typeof dk_bpm !== 'undefined'` guard I wrote protected nothing and killed `setBPM` outright on early calls. Now a try/catch. Second time this pattern has bitten in this session; the rule is that `typeof` only guards `var` and undeclared globals, never `let` or `const`.

Verified across preset loads, live changes from 30 to 200 BPM, and the drum machine's own setter: the two clocks now match in every case, and the standalone drum machine still keeps its independent tempo as it should.

---

## v0.97.66 — Chords were arriving late because of their attack, not their timing

This one was not a scheduling bug at all, which is why the previous two fixes did not touch it.

The chords were being scheduled at exactly the right moment. What was late was the *sound*: the default sine voice ramped from silence to full volume over **40ms**, and the low-frequency harmonic layer that runs under any note below 200Hz took **50ms**. A drum transient peaks in one to three milliseconds. So on every downbeat the kit hit its peak while the chord was still fading in, and the ear placed the chord roughly 20ms behind the drum.

**And that explains the tempo detail exactly.** The lag is a fixed number of milliseconds, so it never changes with tempo — but at 180bpm it is 12% of a beat, buried in the groove, while at 60–90bpm there is space around every beat and nothing to mask it. Fast tempos hide attack lag; slow ones expose it. "Only when I slow it down" was the clue that it was a constant offset rather than drift.

Attacks are now 8ms for the main tone and 12ms for the low harmonics — the latter kept slightly longer because a hard onset on a 60Hz sine is a thump rather than a note. That puts all three voices (synth, harmonics, samples at 9ms) within a few milliseconds of each other and well under the ~20–30ms threshold where two sounds start to register as separate events.

Checked the ramps are still long enough to avoid the click they were guarding against: a ramp needs roughly half a waveform cycle to remove the step edge, and the shortest case here — a low C at 12ms — spans 0.78 cycles. Every register passes.

---

## v0.97.65 — Presets keep their name, and stop inheriting the last time signature

Two bugs, and the screenshot showed both at once.

**Presets showed CUSTOM immediately on load.** `progLoadPreset` set the active preset first, then called `progApplyTimeSig()` — which clears the active preset, correctly, because changing the signature by hand means the grid has diverged. During a load it runs as part of *applying* the preset, so clearing was wrong. Any preset declaring a time signature wiped its own name a moment after loading: 23 of the 66 presets do, which is the "a lot" in the report.

Fixed by claiming the preset last, after every call that might legitimately clear it, with a flag that suppresses the clear for the duration of a load. Verified both directions: loading a preset keeps its name, and a hand edit afterwards still falls back to CUSTOM.

**And the stretched bars: Mixed Rhythm was being played in 7/8.** It declares no time signature, so the old code skipped the block entirely and left whatever the previously-loaded preset had set. Its bars are written for four beats, so against a seven-beat bar they render as those long single-chord rows in the screenshot. The preset was fine; the state was leaking.

A preset without an explicit signature is a 4/4 preset — its durations assume it — so loading one now resets to 4/4 rather than inheriting. Confirmed by loading a 3/4 preset and then Mixed Rhythm: it comes up in 4/4.

---

## v0.97.64 — The progression name is a label, not a second title

You were right that it looked awkward, and the reason is a specific one rather than a matter of taste.

I had given the progression name the same typeface, the same weight and the same theme colour as the module header directly above it. That makes two headings at the same visual level, and the standard guidance on this is blunt: levels must differ in more than size, and two elements styled alike compete for attention instead of establishing an order. The eye had no idea which to read first.

It also mislabels what the thing *is*. TOOLS is the page title. The progression name says what is loaded inside that page — a level below, closer to what design systems call an eyebrow or a supporting label. Guidance for those is consistent: noticeably smaller than the heading, and never styled so prominently that it rivals it.

Rendered five treatments side by side against the real header to compare rather than guess: the current one, a mono label, a demoted Cinzel, a mono label tinted with the module colour, and a Fraunces italic echoing the splash wordmark. The competing version is obvious once they sit next to each other.

Went with the tinted mono label — it matches the label language the app already uses everywhere else, and keeping a trace of the module colour stops it reading as inert chrome. The header is Cinzel 700 at 33px; the label is mono 500 at 10px with wide tracking. Contrast measured 7.85–10.83:1 on dark and 5.75–7.05:1 on light, comfortably clear for small text.

---

## v0.97.63 — Progression title styled properly; the rest of the tempo drift

**The title was still Bebas in flat white** — it had its own rule and never picked up the treatment the header titles got. Now Cinzel 700 in the module's theme colour, with the same light-mode ink treatment, and it truncates with an ellipsis so a long preset name cannot shove the buttons beside it off the row.

**Preset name removed from the chip.** The title carries it now, so repeating it there was both redundant and the thing pushing the button around as names got longer. The chip is just PRESETS and a caret.

**The remaining tempo drift, and why lowering tempo was worse.** The previous fix rescaled `progNextAudioTime` — the pointer for the next event *not yet queued*. But the chord already sounding was handed to the audio graph with the old beat length baked in, and nothing rescaled that. So the gap between the sounding chord and the next one was wrong by exactly the tempo delta. Slowing down made that gap too short, which is heard as the following chords landing off the pulse once your ear locks to the new tempo.

The in-flight chord is now faded out to meet the recalculated boundary, so it does not overhang the new grid. A chord cut slightly short is far less noticeable than one that holds the wrong length and displaces everything after it.

**The drum kit had the same bug and now has the same fix.** It keeps a per-track `nextTime`, each queued at the tempo in force when it was scheduled, so a change left every track spaced for the old tempo — the kit sliding against the chords. All pending track times are rescaled by the same ratio the chords and metronome use.

Modelled the whole system across a slow-down and a speed-up: chords, metronome and every kit track keep their exact relative positions, so nothing slides against anything else.

---

## v0.97.62 — Progression can play sampled instruments

Chord voice picker in the sync tray: SYNTH (the default and the fallback), plus Grand Piano, Rhodes, Nylon Gtr, Vibraphone and Harpsichord.

**The engine needed a change first.** `SampleEngine.play()` started every note at `ctx.currentTime` — fine for tap-to-play, useless for a sequencer. The progression scheduler queues events about 100ms ahead, so a note that ignores its scheduled time fires whenever the tick happened to run: modelled at up to **89ms of jitter**, which against a properly-scheduled drum kit is audibly loose. `play()` now takes an optional absolute start time, defaulting to `currentTime` so every existing caller is untouched, and clamped so a stale time cannot schedule into the past. With it, onsets are sample-accurate.

**Falls back rather than failing.** The instrument id resolves to null unless the buffers are actually loaded, so an unloaded, still-loading or failed instrument gets a synth chord instead of silence. The check runs per scheduler tick, so a progression started before the piano finished loading picks it up mid-playback rather than staying synth until restarted. The status line under the picker says which state it is in, because "I chose piano and it sounds like a sine wave" is otherwise a mystery.

Two things caught while building this, both by testing rather than reading:

**A temporal dead zone crash.** The status hook and the preload touched `SampleEngine` at parse time, but it is a `const` declared much further down the file. Unlike an undeclared variable, a `const` accessed before its declaration *throws* — so the `typeof` guard I had written was worthless, and the page logged "Cannot access 'SampleEngine' before initialization" along with two knock-on errors. Both now defer past parse.

**A wrong instrument id.** I had listed the piano as `acoustic_grand`; the registry calls it `grand_piano`. That would have rendered a chip that silently never resolved — the exact failure the fallback is meant to make impossible, arriving through the front door instead. All five ids are now verified against the live registry.

Your choice persists, and a stored instrument preloads 2.5s after launch so it is ready before the first play rather than stalling on the first chord.

---

## v0.97.61 — Tempo changes land immediately; progression title says what is loaded

**The session stamp was escaping its own box.** It sits inside `.session-bar`, which is only 4px tall — that element is the progress hairline, not a container — and the stamp was anchored `bottom: 4px`, which put the text entirely outside those 4px, rendering over whatever happened to be above it. It survived on luck until the header above changed height. Now anchored below the hairline, in the empty space where nothing overlaps it.

**Tempo changes now apply immediately instead of at the next bar.** The scheduler queues audio about 100ms ahead, and each queued event carries the beat length that was in force when it was queued. Change the tempo and those events keep the old spacing, so playback drifts until the sequence loops and re-anchors — the "out of sync until the measure starts over" symptom exactly.

Waiting it out was never going to work, so the pending timeline is rescaled instead: the time still remaining before the next event is multiplied by the tempo ratio, so that event lands where the new tempo says it should. Notes already sounding keep their original length, since retuning one mid-flight would click. The bar anchor is rescaled too, or the groove swap on the next boundary fires at the wrong moment.

**The metronome had the identical bug** and now has the same fix, since it is frequently the thing the progression is playing against.

Modelled the correction: a 120→180 change previously left the next beat 167ms late, and over a 16-beat phrase that accumulates to roughly 2.7 seconds — the chords and the kit end up a full beat apart. With the rescale the error is zero.

**Progression title is dynamic.** It was a hardcoded "PROGRESSION" sitting directly beneath a header that already said the same word. It now shows the loaded preset's name, or CUSTOM once the grid no longer matches one. Every path that clears the active preset already refreshed the label, so the fallback works without new plumbing.

**On the sample engine question: progression is synth-only.** Chords are built from `REF_TONES[...].synth()` — Web Audio oscillators with added low-frequency harmonics — not the sampled instrument library. Worth knowing that moving it onto samples would be real work rather than a flag, since the scheduler currently assumes a synth node it can stop and fade.

---

## v0.97.60 — Nothing pops over the picker

**Splash Screen now sits above Open To**, matching the order the two things actually happen.

**The streak toast was firing over the module picker**, and the cause is a good example of an assumption quietly expiring. The toast was scheduled on a flat 3200ms timer, picked so it would land just after the splash — with a comment saying exactly that. The launcher moved the goalposts: 3200ms now lands on the picker, so a celebration covered the cards before anything had been chosen. Skipping the splash made it worse, firing the toast over the splash's own replacement.

A timer cannot know where the person is, so guessing at a delay was always going to break. Startup celebrations now go through a queue that drains on **module entry** instead: choosing a card drains it, and so does a pinned launch where the picker never appears. Held items fire 900ms after the module settles, staggered 4s apart so two never overlap.

Both streak paths (the celebration and the reset notice) go through it. A 12-second failsafe drains the queue if the launcher never initialises — losing a streak toast is minor, but silently dropping every future one because a flag never flipped is not.

Verified across all four paths: suppressed while the picker is up, fires after choosing a card, fires correctly on a pinned launch, and anything queued after the drain still fires rather than being stranded.

---

## v0.97.59 — Header Title is not a setting; splash row is just ON/OFF

**Header Title removed from Settings.** Adding it was inventing a preference for a question already answered — module names are simply what the app does, not something to configure. The flag stays in code, default on, because `setMode` reads it; it just is not a choice any more.

Removed with it: `setHeaderModuleTitles()`, `_applyHdrTitleUI()`, the row markup, and six now-unused strings. Checked explicitly that `HEADER_MODULE_TITLES` itself and its declaration survived — that is precisely the mistake from v0.97.55, where a deletion took a still-referenced declaration with it.

**Splash row is ON and OFF with no sub-captions.** The two-line chips were 39px tall against 24px for the pin row above them; they now match at 24px, and the row uses the same compact chip treatment.

Verified after the removal: no page errors, launch still shows the module name, the splash toggle persists in both directions, and nothing stale is left in the panel.

---

## v0.97.58 — Launch settings grouped, and the header-title flag comes out of the code

The three launch settings now sit as sub-rows under one **Startup** heading:

- **Open To** — grid, or straight into a pinned module
- **Splash Screen** — full intro, or straight in
- **Header Title** — module names, or the app name

They were already adjacent, but the pin row had no sub-label of its own, so it read as *being* the section and Splash Screen underneath looked like a separate one. Giving it a label makes all three read as peers answering the same question.

**Header Title was code-only until now** — `HEADER_MODULE_TITLES`, set by hand or by whatever was in storage. It belongs in this group: it decides what the header says the moment a module opens, which is the same question as the other two rows.

Unlike its neighbours it applies **immediately** rather than from the next launch, because it changes something already on screen. Verified both directions live: MODULE shows TUNER, APP shows Intonare, the choice persists, and the chip state follows.

Checked the rendered panel in both languages at 360px: one Startup heading with three sub-rows beneath it, nothing clipped.

---

## v0.97.57 — Skip the splash (safely)

**Splash Screen ON / OFF**, sitting under Startup with the pin chips, since both answer "what happens when I open this".

**On the danger question: there is one, and it is not what it looks like.** The risk is not loading straight into a module — that path is already well tested, because deep links have always done exactly that. The risk is *how* you skip.

`removeSplash()` is not just teardown. It fires the `splash-done` event, kicks off staggered sample preloading, and installs the iOS first-gesture audio unlock. That last one matters: WebKit creates the AudioContext suspended, and only a real user gesture can start it — a `resume()` from a timer silently fails. Tearing the splash down any other way would leave iOS with no sound at all, and nothing would look broken until someone tried to play a tone.

So the preference routes through the same path deep links use, which calls `removeSplash()`. Verified by instrumenting `addEventListener` and comparing both paths: with the splash skipped, all four unlock listeners (`touchend`, `pointerdown`, `click`, `keydown`) are registered immediately; with the splash running they arrive once it finishes. Same handlers, same state — skipping just gets there sooner.

Also checked that both paths converge: splash element removed, `_splashGone` set, launcher shown, header correct, no page errors either way.

The setting applies from the next launch, since by the time Settings is reachable the splash has already run or been skipped.

---

## v0.97.56 — Fixing what the scaffold removal broke

My fault, and a clean lesson in checking what a deletion takes with it.

**`HEADER_MODULE_TITLES` was declared inside the switcher block.** When that scaffold came out in the previous build, the declaration went with it — leaving two live references to a variable that no longer existed. Referencing an undeclared `let` throws, so the branch that names the tuner and metronome failed silently and fell through to the app name. That is the "says Intonare on load".

The flag is now declared at top level, next to `setMode` which uses it, where a future deletion elsewhere cannot take it out.

**The header was also never set at boot.** The app comes up on the tuner, but `setMode` does not run at startup, so the logo underneath kept whatever it was initialised with. Nothing revealed that while the launcher covered it, but a pinned launch or a fast dismissal showed the stale name. A sync now runs once on startup.

Deliberately **not** hung off the launcher: whether the header names its module has nothing to do with the grid, and tying it to a splash event would leave it stale on every path that skips the splash — deep links, reloads, pinned launches. It runs on its own once the DOM is ready.

Verified in a browser rather than by reading: launch shows TUNER, all four tabs show their own name, no page errors, and every function the scaffold removal could have touched still resolves.

---

## v0.97.55 — New title face, per-module colour, and the switcher scaffold is gone

**The title switcher was still in the build.** 46 variants, 112 CSS rules, the long-press picker, the shortlist cycling — all for choosing a treatment for a header state that the launcher work made obsolete. Removed: 15,098 characters of JS and 26,461 of CSS, with zero remaining references to any of it.

**Module titles are now the default.** `HEADER_MODULE_TITLES` was still shipping `false`, so tuner and metro showed the app name unless the flag had been toggled by hand. Every tab now names itself, which is what the launcher work was heading toward: the app name is established on the splash and again on the grid, so a header repeating it was the inconsistency this whole thread started from. A stored preference still wins if one was set.

**New face: Cinzel 700, replacing Bebas 400.** Bebas is a light condensed sans; at header size with a gradient fill it read as thin outlines, which is the "plain" in the report. Cinzel has real stroke weight and serifs, so it reads as chosen type rather than a default. It was already embedded for other surfaces, so this adds nothing to load.

**Per-module colour.** In dark mode the title now takes the tab's `--theme-a` as a solid fill with a soft glow of the same colour, rather than a two-stop gradient clipped to the glyphs — the gradient was what made the letters read as hollow in the first place. Light mode keeps the flat ink from the previous build. Each module's title now carries its own colour in both modes: measured 9.20–13.65:1 on dark and 7.33–8.93:1 on light.

Rendered both modes in Chromium to confirm Cinzel actually resolves rather than falling back silently.

---

## v0.97.54 — Light titles are flat ink; the Tools peek matches the others

**The title fix last build was aimed at the wrong thing.** Testing the real rules in a browser showed the darkened gradient *was* applying — contrast was never the remaining problem. What made it look washed out and plain is the treatment: a gradient clipped to text renders each glyph as a fill with no edge, and Bebas at weight 400 on a pale ground then reads as hollow outlines rather than letters.

So light mode now drops the gradient entirely and uses flat ink, with the theme hue mixed in at 42%. A solid fill has a hard edge at every stroke, which is what makes it read as type instead of an outline. Measured 7.33–8.93:1 across the four tabs, and a faint white text-shadow gives it the slight lift that ink on paper has.

**The Tools peek was the odd one out**, and it was two problems at once. Visually it was a photoreal keyboard — white and black keys with a drop shadow — sitting among three flat line diagrams, so it read as a different kind of object. Structurally its solid block sat higher than the other peeks' content, which is the "a little high" in the report.

It is now a pitch read drawn in the same language as the rest: thin bars in the module colour with the detected peak highlighted, a baseline axis, and the note and frequency underneath. Content now starts within 5px across all four cards, where the piano was noticeably above the others. The dead piano CSS and markup were removed rather than left behind.

Verified by rendering both modes in Chromium: zero collapsed elements, alignment measured, and the light-mode piano rules replaced with spectrum equivalents so nothing was left pointing at deleted markup.

---

## v0.97.53 — Light mode for the header titles and the launcher cards

Two things the screenshots showed, both the same root cause: elements designed against a dark ground and never re-anchored for paper.

**Header titles were washed out.** The section and module titles are a gradient clipped to the text, built from `--theme-a` and `--theme-b`. Those flip to pale tints in light mode, so the word sat on an equally pale page: measured at **3.58:1** for the tuner and **3.62:1** for the metronome, under the 4.5:1 floor — and since the pale end of the gradient covers most of the word, it read worse than the numbers suggest. Both stops now mix 55% toward ink in light mode, which keeps the hue and puts every tab between **5.47:1 and 7.89:1**.

**Launcher cards were nearly invisible.** The card faces, the peek elements and the module names were all tuned for a dark card. On light the metronome peek disappeared completely — pale amber body and BPM label on a pale amber face — and the names sat near-black on an almost-white card, so the cards read as flat rectangles rather than objects.

Every tier is now re-anchored: faces take a real edge, the colour wash strengthens, names take ink, and each peek element mixes 52% toward ink so it holds against a light face instead of blending into it. The piano keys invert properly too — white keys lighten, black keys stay dark, the lit key keeps its tint.

Verified by rendering the launcher in light mode in Chromium rather than reasoning about it: all four peeks legible, and card text measured at 10.49:1 for names and 5.35:1 for descriptions.

---

## v0.97.52 — Notifications could be turned off but not back on

A one-way switch, and worse than it looked.

Turning a reminder **off** never needed permission, so it always worked. Turning it back **on** called `notifRequestPermission()` and bailed with a bare `return` if that came back false. Once Android has latched "don't ask again", `requestPermissions()` resolves denied *without showing a prompt* — so the button did nothing, explained nothing, and looked broken. Same on web or PWA, where the plugin does not exist at all and every enable attempt failed silently.

The greyed-out time picker was correct behaviour, incidentally: it disables while the reminder is off. The bug was that the toggle beside it had stopped responding, so there was no way back.

Now a refused enable says so, in a hint under the Notifications heading pointing at the device setting, in both languages. The app has no general-purpose toast — `dtFireDailyToast` is a streak celebration and the wrong semantics for a refusal — so the message is inline where the control is.

Verified by simulating all three cases: with permission granted the round trip works, with permission denied the enable is refused *and reports why*, and with no plugin at all the same. Previously the second and third cases were indistinguishable from a dead button.

---

## v0.97.51 — Startup moved to the top; launcher subtitles fit

**The tuner subtitle was clipped because the launcher was borrowing the header's text.** `tuner_sub` is the subtitle shown in the header when a module names itself, where it has a full row; a card has two short lines, and 41 characters does not fit in them. Shortening the shared key would have changed the header too, so the launcher now has its own set: `lnch_sub_tuner`, `lnch_sub_metro`, `lnch_sub_train` alongside the existing tools one. All four are 16–26 characters in both languages.

**And yes, they translate** — every launcher string has both an EN and IT definition, verified: the eleven keys the launcher touches all have exactly two definitions. Rendered the Italian set at 360px, which is the tighter case since Italian runs longer: nothing clipped, every subtitle on one line.

**Startup moved from second-to-last to first.** It was sitting between Help Buttons and Advanced, which meant the one setting that changes what happens *every time the app opens* was among the hardest to find in the panel. Order is now Startup → Language → Feedback → Practice → Hints & Display → Advanced, which runs roughly from "what happens when I open this" through preferences to rarely-touched maintenance.

Audited the panel while in there: all six onclick handlers resolve to defined functions, and all four section titles have both translations. No dead controls found.

---

## v0.97.50 — Fixing what the screenshot showed

The screenshot surfaced several things, including two real bugs.

**The train staff was invisible, not sparse.** Its lines are `<span>` elements, so they are `display: inline` by default, and an absolutely positioned inline element with a height but no content collapses to nothing. The notes drew because they have a width; the staff never did. Every peek element that needs a box is now explicitly `display: block`. Measured after the fix: zero zero-sized elements across all four peeks.

**The pins were still there and had landed on top of the peeks** — removing the card icons left the pin in the top-right corner, where it now covered the preview (on the tuner it sat squarely over the first row). Pins moved to the bottom-left, beside the text and clear of the peek, with the text block padded to make room. Verified: the pin sits below the peek boundary on all four cards.

**The tuner peek was showing the wrong screen.** String rows are the reference-tone list, not the tuner. It now shows what the tuner actually shows: the large note readout, the frequency, and a cents bar with the needle just off centre.

**The metronome was ambiguous** because a ring with a number in it could be any dial. It now has the metronome's body and swinging beam with the weight on it, plus the accented beat row and the BPM, so the object is unmistakable.

**The cards did not line up.** The face used `justify-content: flex-end`, so a three-line description pushed its card's title higher than the others — Tools was 5.1px out. The text block is now a fixed region in the lower part of the card, vertically centred, and Tools has its own shorter launcher subtitle (the full one belongs on the hub, not on a card) with a two-line clamp as a backstop. Measured after: all four titles align to 0.0px.

Verified by rendering the real CSS in Chromium at phone width rather than reading it: zero peek overflow, zero collapsed elements, pins clear, titles aligned.

---

## v0.97.49 — Peeks show the actual modules

The previous peeks were invented abstractions — a swinging needle, bouncing bars — rather than pictures of the app. They now show the real surfaces, built from the same elements the modules use:

- **Tuner** — string rows, exactly as the tuner draws them: note name, cents readout, the active row highlighted
- **Metro** — the beat ring with its BPM, beat dots above it, first beat accented
- **Tools** — piano keys, the hub's most recognisable surface, one key lit
- **Train** — the interval staff from ear training, two notes a third apart

**And they are static now**, which you were right about: a preview does not need to move to be understood. That removes four running animations, all their keyframes, and any question about what they cost on launch.

**The card icons are gone.** With a real preview on each card, a glyph in the corner was saying something the peek already says better. The icons remain in the tab bar, where there is no room for a preview. Removing them made `LNCH_ICONS` and `lnchSvg()` dead, so both were deleted rather than left as unused code in a file this size.

**Settings chips fit one row.** Five options at the default chip size was far too heavy for a single setting. The app already had a precedent in `.sm-toggle-compact`, so these follow it: no wrap, tighter padding, 10px labels, chips sharing the width equally with ellipsis as a backstop. Measured against a 360px phone — the row needs roughly 221px in English and 249px in Italian, against about 300px available, so it fits in both with headroom.

---

## v0.97.48 — Cards preview their module

The coloured top hairline is gone; the peek does that job better.

**Each card now previews its module in the top half**, fading down into the module's colour and then into the text below. The tuner's needle settles either side of centre; the metronome's four beats sweep in time with the accent brighter; Tools reads a waveform; Train steps a note up a staff as if answering the one before it. Tools and Train each pick one representative idea rather than trying to depict six utilities at once.

**These are CSS animations, not engine instances.** Four live canvases running behind a launcher would cost battery and startup time for a screen that shows for a couple of seconds and, once a module is pinned, may never be seen at all. Everything here is transform and opacity only, which the compositor handles without touching layout. They stop entirely under `prefers-reduced-motion` and pause the moment a card is chosen, so nothing animates during the exit.

The icon moved to the opposite corner from the text and shrank — the peek owns the top of the card now, and the icon is a marker rather than the main event.

**The background was flat because it was near-black and themed.** It used `var(--bg-0)`, which is set per tab, so the launcher's ground changed colour depending on which module you last used — the chooser sits above all four modules, so it should not inherit any of them. It now has its own neutral ground with two very soft radial pools giving the surface a lit centre, which also addresses the standard dark-UI advice that pure black reads as dead space.

**Light mode was asked about, so it was audited rather than assumed.** Of 64 launcher rules, only three hardcode colours — the background, the card face and the pin — and all three already had light counterparts, with the new background getting one in this build. Everything else resolves through `var(--lc)`, the text tokens, or `rgba()`, all of which follow the theme automatically. Peek elements were checked for contrast against the card face in both modes: 8.1–12.2:1 on dark, 3.8–5.6:1 on light, all clearing the 3:1 floor for non-text.

---

## v0.97.47 — No flash, no title, real depth, and the metronome finally renames itself

**The flash.** The launcher shipped `display:none` and was revealed by script, so anything between the splash finishing and that script running showed the bare tuner and its tab bar. It now ships *visible*, and a small inline script immediately below the markup hides it when a pin is set. That script is synchronous and runs before the browser paints, so the decision is made without any frame in which the wrong thing is on screen. The deep-link case still resolves later, since the launch URL isn't known until a promise settles, but it can only turn the launcher off rather than on.

**The metronome kept saying Intonare, and it was a real bug.** The consistency branch tested `m === 'metro'`, but `setMode` is called with `'metronome'` — the tab button passes `setMode('metronome')`. The condition never matched, so only the tuner ever renamed itself. Fixed in both the tab handler and the toggle helper. Swept the file for the same mistake; the one other `=== 'metro'` is the progression tool's sync mode, where 'metro' is correct.

**Title removed from the grid.** The splash showed it at 58–82px seconds earlier; repeating it above the cards was the same redundancy that started this whole thread. The grid is now cards centred in the space.

**Why it felt flat, and what changed.** Card layouts deliberately flatten hierarchy — they present everything as peers, which is the pattern's known weakness, and four identical tiles is that weakness at full strength. The fixes are the standard remedies: cards now have real elevation so they read as objects resting on a canvas rather than regions painted onto it, using an inset top highlight since drop shadows are nearly invisible on a dark ground; the flat fill became a directional gradient tinted by the module's colour; each card gets a hairline of its own colour along the top edge so it has structure that is unmistakably its own; and each card now has three internal tiers instead of one — the icon sits in a tinted well, the name leads in the text colour, and the description recedes.

**Settings uses the app's chips.** The bespoke segmented control is gone, replaced with `.sm-toggle-chip` so the row matches every other setting. The no-pin option is **OFF** rather than GRID, since the row asks which module to launch into and the empty state is that shortcut being off, not a fifth destination.

An escaping mistake in the Italian string (`all\'avvio`) broke a script block and was caught by the block checker before it shipped; it now uses double quotes.

---

## v0.97.46 — The grid is a choice, not a screen you are already in

Two changes, same intent.

**The tab bar is gone while the grid is up.** It was showing because the bar is `z-index: 1000` and the launcher is 900, so it sat on top. Raising the launcher would have fixed the overlap without fixing the meaning: you have not entered a module yet, so there is nothing for the bar to indicate. It now slides down out of the way when the launcher opens and slides back as the chosen module arrives, which also makes the bar read as belonging to the module rather than to the app frame.

The risk with a body-class approach is a stale class leaving the bar invisible forever, so the class is cleared on every path that skips the launcher, and the removal happens at the *start* of the exit so the bar rises while the launcher is still fading rather than appearing after everything settles. Verified by execution across four paths, including one with a deliberately stale class: unpinned boot hides it, choosing a module restores it, pinned boot clears it, deep-link boot never sets it.

**Cards are smaller with room around them.** They were stretching to fill the screen, which reads as a screen you are already inside. Now they are capped at 340px wide and 60vh tall and centred in whatever space is left, with the gap opened from 9px to 13px. On a tall phone they stay card-shaped instead of stretching into panels. Hiding the tab bar contributed here too, since the grid gets the full height to be centred within.

Also added a small press state — the card face scales down slightly on touch — so a tap feels like pressing a physical thing rather than triggering a screen change.

---

## v0.97.45 — The splash dissolves into the grid

The launcher popped in after the tuner had already appeared, which is a sequencing bug with a nice fix hiding behind it.

**Why it popped.** The splash does not cut — it dissolves over 1.3 seconds, and `removeSplash()` only runs when that finishes. The launcher was listening for `intonare:splash-done`, which fires *after* all of it. So the splash faded to reveal the tuner, and only then did the grid appear on top.

**The fix.** A new `intonare:splash-dissolving` event fires as the dissolve *begins*, one frame before opacity starts moving. The launcher listens for that instead, so it is already in place and the splash dissolves into the grid. The old `splash-done` listener stays as a fallback for the paths where a dissolve never happens at all — deep-link skip, the 7-second failsafe, an early error — and a guard makes the start idempotent so the two listeners cannot double-fire. Verified across all five boot paths: exactly one start each.

**Tying them together visually.** The launcher is not faded in, because the splash is fading out on top of it — it is *revealed*. What animates is underneath: the cards rise and fade up in a short stagger while the tagline and hint follow, so the splash's own logo appears to stay put as the grid arrives beneath it.

That only works if the logo really does stay put, which exposed a second seam. The splash wordmark is Fraunces **italic 300** with the theme gradient; the launcher had roman 400 in flat off-white. Cross-fading those morphs one logo into a different one. The launcher wordmark now matches the splash exactly — same face, same weight, same gradient — with only the size differing (58–82px down to 34–46px), so the dissolve reads as the logo settling into place rather than changing into something else.

Reduced motion skips the stagger entirely, and the picked-card animation overrides the entry delays so a fast tap doesn't fight the entrance.

---

## v0.97.44 — Module launcher

The 2x2 grid is in the app. After the splash you pick a module; the card you tap grows while the others drop away, then the app appears behind it.

**It also fixes the launch-mic problem as a side effect.** The tap is a real user gesture, so the AudioContext unlocks *and* we land on a mic surface in one action — no race with the RECORD_AUDIO grant, which was the suspected cause of the intermittent mic bug and the reason auto-start was deferred. That fix comes free with a navigation change we wanted anyway.

**The tap is optional.** Pin a module from its card or from Settings → Startup and launch goes straight there; the launcher never appears. The settings row is the control rather than an escape hatch: a five-way segmented picker (GRID · TUNER · METRO · TOOLS · TRAIN) so a mis-pin is fixed in place instead of by hunting for a screen that no longer shows up. Both paths write the same state through `lnchSetPin()`, so they cannot disagree, and a stale pin naming a module that no longer exists is discarded on read.

**Deep links bypass it entirely.** A shared link must open its module, not a chooser — the same reasoning behind the existing splash skip, where a link landing on a menu looks like the link failed. `lnchShouldShow()` checks the deep-link flag.

Sequencing follows the lesson already learned the hard way in the deep-link handler: wait for the `intonare:splash-done` event rather than guessing a delay, with a fallback for the case where the splash has already finished. `prefers-reduced-motion` skips the card animation.

Verified by executing the real code against a stub DOM, not by reading it: unpinned boot builds 4 cells and 5 segments and shows the launcher without setting a mode; choosing a card sets the right mode; pinning then rebooting skips the launcher and lands on the pinned module; unpinning from settings restores the grid and leaves exactly 5 segments; and the deep-link flag suppresses the launcher. EN and IT strings both present for all five new keys.

Still open, and the reason this wants on-device time before it's considered done: the tab bar is `position:fixed` with `env(safe-area-inset-bottom)`, so the launcher currently overlays it rather than animating it. The card-becomes-header swoop from the prototype is not in this build; getting it right in the real app means transforming a wrapper, not the fixed element, or it jumps on home-indicator devices.

---

## v0.97.43 — Should the header say the app name at all?

Daniele's question, and it reframes everything the last several builds were doing: I was iterating on the treatment of something that may not belong there.

Mapping the four header states makes the case. **Tools** and **Train** name themselves. **Every module screen** names itself. All three use Bebas Neue tracked caps with the theme gradient. **Tuner and metro** are the only states showing the app name, and the only ones using Fraunces italic. So that state is the odd one twice over: wrong content and a different typeface from everything else.

The splash already shows "Intonare" in Fraunces italic with the same gradient at 58–82px, against the header's 36–52px. The app name is established on launch, larger and with the animation; repeating it smaller in the header tells you which app you're in while you're using it.

Added `HEADER_MODULE_TITLES`, toggleable from the top of the title picker. Turn it on and tuner/metro name themselves like every other tab, with new subtitles ("chromatic · instruments · reference tones", "tempo · grooves · drum kits") in both EN and IT. The existing `setHeaderSection` machinery already did all the work; the change is passing a name instead of null, plus a guard so re-entering the same tab doesn't re-fire the animation.

Left as a toggle rather than shipped on, because it's a real design call and the tuner is the default landing screen — some argument exists for brand presence there, though the tagline underneath already carries the app's voice. Worth living with both ways for a day.

If it stays on, the 55 title variants become decoration on a state nobody sees, and the honest follow-up is deleting the switcher and matching the module typeface instead. That's a good outcome: the title stopped feeling wrong because it *was* wrong structurally, not typographically.

---

## v0.97.42 — The combination without the hierarchy, plus shortlist cycling

Dropping the value hierarchy leaves three treatments pulling the same direction — colour, spacing, depth — with nothing dividing the word, which is closer to the "one dominant move" principle than the four-way version was. The hierarchy was the element working against the others.

Six variants, so it can be dialled rather than accepted or rejected whole. **k1** is the straight answer: 18% tint, tight tracking, overlay depth. **k2** and **k3** vary the tint (26% and 12%), **k4** and **k5** vary the tracking (eased and tighter), **k6** strengthens the depth cue to test whether the subtle version is doing anything at all on-device.

Tint was swept specifically for whole-word use, where saturation matters more than on a fragment: 12% reads barely tinted, 34% pushes the tuner blue to 0.75 saturation and into vibration territory. 18–26% keeps every tab theme under about 0.7 while staying clearly coloured, and all six sit at 13.2–14.8:1. Light mode mirrors each as ink on paper, since `--theme-a` flips to a dark value there.

**Also fixed a usability problem the switcher had grown into.** At 55 variants, double-tap cycling takes 55 taps to loop and the k-family sits at index 49 — useless for comparing two candidates. The picker now has a star against each variant: star two or more and the cycle visits only those, falling back to the full list when fewer than two are starred. The flash tag shows a star when a shortlist is active. Verified by simulation including the edge case of cycling from a variant that isn't itself shortlisted.

55 variants total.

---

## v0.97.41 — The combination, graded; and a light-mode bug in the whole family

Built the requested combination — tinted to the theme, tight tracking, light-overlay depth, value hierarchy — as five variants rather than four toggles, graded from restrained to full-strength. Wordmark practice is consistent that a mark wants one dominant move, and stacking four is a real risk, so the grading exists to find where it stops being tasteful: **h1** is tint plus tight tracking only, **h2** adds the value hierarchy, **h3** is all four, **h4** flips the hierarchy so the tint closes the word instead of opening it, and **h5** is all four at normal tracking, since tight tracking is a decision that deserves testing against not-tight.

Colours were computed rather than picked. The bright tier is 18% theme mixed into the neutral, landing at 13.7–14.7:1 across all four tab themes with saturation between 0.25 and 0.59, so it re-tints per tab without vibrating. The dim tier needed more care: a 50% mix scored **2.4:1**, below even the 3:1 large-text floor, and this is half the app name — so the dim tier is #9b9ea8 at 7.3:1, still a clean 2x step below bright but never anywhere near unreadable.

**Then measuring caught a bug affecting everything built in the last two versions.** The g and h families hardcode light colours (#dfe2ee, #9b9ea8), which is right on the dark ground they were designed against. In light mode the same values put near-white text on a near-white page: **1.5:1, versus a 4.5:1 floor**. Light mode also flips `--theme-a` to a dark value (#00546d and friends), so the tint mix produces a pale wash rather than a tint. Every affected variant now has a light-mode override mirroring the tiers as ink-on-paper: bright tier is 18% dark theme mixed into #1e2030 (12.8–13.6:1 across themes), dim tier is #6f717d (4.45:1). All 15 g/h variants verified covered.

49 variants total, all validated by execution.

---

## v0.97.40 — The calm baseline, taken through colour, spacing and hierarchy

Took the f8 baseline (Fraunces roman, off-white, no effects) and built a family of ten treatments around it. Same font throughout, so any difference between them is the treatment rather than a different typeface — the point being to find what the treatment should be now that the face is settled.

**Building it surfaced a flaw in the baseline itself.** Inspecting the embedded Fraunces shows it is a *static* font with only three faces: 400 roman, 300 italic and 400 italic. There is no 450 roman — so f8's `font-weight:450` was being **synthesised by the browser**, a smeared 400 rather than a drawn weight. Faux weight distorts stems, which is precisely what type practice says to avoid, and it may be part of why the baseline felt nearly-right rather than right. Audited every variant for this and found three more doing the same thing: the split-weight variant asked for 300/600 roman, tight tracking asked for 500, weight contrast asked for 200/700. All four now use real drawn faces, with weight contrast built from italic 300 against roman 400 rather than two synthesised weights.

The ten treatments: corrected baseline at a real 400; tinted neutral with 18% theme mixed into the off-white (14.4:1, ties to the active tab without ever being a saturated word); warm paper white as a deliberate counterpoint to the cool UI; tight tracking; open tracking; value hierarchy inside the word; an accent hairline underneath; the tittle of the i as the only colour; light-overlay depth (shadows are invisible on dark grounds, so lift comes from a faint top highlight); and tracked caps.

Colour throughout follows the dark-UI findings from the previous build: the neutral base rather than pure white, and where the theme hue appears it is either heavily diluted into the neutral or confined to something small — 1.5px of hairline, or a tittle — never a large saturated word.

44 variants total, all validated by execution: every variant has matching CSS, every wrap class is styled, every variant preserves `textContent`, the `[data-logo^="g"]` prefix rule doesn't leak onto non-family variants, and no rule anywhere now requests a Fraunces weight that has no drawn face.

---

## v0.97.39 — Double-tap advanced twice; colour and perception research

**The double-tap bug was mine.** I bound both `touchstart` (which runs a tap counter) and `dblclick` to the cycle. Browsers synthesize a `dblclick` after a touch double-tap, so both fired and the title jumped two variants. Fixed: touch devices use the counter only, and `dblclick` is now a mouse-only fallback suppressed once any touch has been seen. Verified by simulation — one gesture, one advance.

**The research went wider this time**, into colour theory and perception rather than just wordmark construction, and it turned up something measurable about the app's own palette.

Material's dark-theme guidance is explicit that saturated colours should be avoided on dark backgrounds: they optically vibrate and cause eye strain, and desaturated colours are the recommended alternative. Measuring this app's palette against #0b0d14: **`--theme-a` (#5ee2ff) and `--theme-b` (#7aafff) are both 100% saturated**, and `--in-tune` is 85%. Contrast was never the issue — the title sits at 12.75:1, far above the 4.5:1 floor — but saturation is, and the title is the largest coloured element on any screen, so it's the worst-affected element in the app. Desaturating to ~60% holds 10.8:1 while removing the vibration.

Two other findings applied: pure white on dark reads as stark and haloed, with light grey the recommendation (the current title uses a gradient rather than flat white, but the softened variants use #dfe2ee); and the distinction between mathematical and optical alignment — round letters need overshoot to read as level, which matters for "Intonare" where o, a and e are most of the word, and optical centring beats mathematical centring because of the gravity effect.

Eight new variants apply these directly: desaturated theme colour, softened off-white, neutral word with the colour carried by a small dot (a saturated 5px dot doesn't vibrate the way a saturated 40px word does), round-letter overshoot, weight contrast instead of colour contrast, low-luminance fill with a bright hairline (light overlays are the dark-mode substitute for shadows, which vanish on dark grounds), optically lifted caps, and a deliberate no-effects baseline as the control the rest are judged against.

34 variants total. All validated by execution: every variant has matching CSS, every wrap class is styled, every variant preserves `textContent`, and no invalid colour values remain (one was caught in this pass).

---

## v0.97.38 — Quick-cycle, eight research-driven variants, and a real bug in the switcher

**The long-press wasn't conflicting with the tour.** The tour fires automatically 600ms after first launch when `tune_tour_done` isn't set; the Settings entry is a button, not a logo gesture. Long-pressing the title on a fresh install just meant the tour landed on top of the picker. No collision to fix.

**But the switcher did have a real bug.** `#appLogo` doubles as the section title ("TOOLS", "TRAIN"), and `setHeaderSection` decides whether to animate by comparing the element's `textContent` against the app name. The bracketed variant set that text to `[Intonare]`, which never matches — so returning to the tuner or metronome tab would have fired a spurious section animation every single time. Fixed by making the brackets CSS pseudo-elements so `textContent` stays exactly "Intonare". Every variant is now checked for this, and the span-wrapping ones were already safe since spans preserve text.

**Quick-cycle, no picker.** Double-tap the title steps to the next variant; two-finger tap steps back; a small tag shows which one you landed on for about a second. The picker is still there on long-press, and `logoPick()` / `logoNext()` work from a console. The point is being able to flip through while actually using the app, which is a different test from choosing in a modal.

**Eight more variants, sourced from wordmark practice rather than my own taste.** The literature is consistent on two things: a wordmark needs *one* distinctive move — a ligature, a notch, a colour break, a spacing decision — rather than stacked effects, and it has to survive monochrome and favicon size. Also that wide tracking is an all-caps technique, since lowercase letters are drawn to sit close. So: a notch cut into the n, tight optical tracking, an na ligature, a counter dot inside the o, tracked monochrome caps, a raised initial, the i's tittle replaced by the in-tune dot, and a centre-line passing through the word. Each makes exactly one move.

26 variants total. Verified by execution: every variant has matching CSS, every wrap class is styled, every variant preserves `textContent`, and cycling forward from any starting point visits all 26 and returns to the beginning.

---

## v0.97.37 — Title style switcher (18 variants, on-device)

Mockups can only get you so far with a title; the real test is seeing it every time the app opens. So the eighteen candidates are now in the app itself. **Long-press the title for 700ms** to open a picker, choose one, and it persists across launches. "Current" is the shipping look and the default, so doing nothing changes nothing.

Variants: the shipping treatment, three with the same Fraunces but less treatment (solid 400, roman, theme-tinted), five in faces already embedded (Cinzel, Bebas, Bebas wide-tracked, IM Fell, Rajdhani), three lockups with a mark (centre-marker bar, in-tune dot, accent letter), and six creative treatments (cents ticks underneath, split weight, bracketed mono, letterpress deboss, extended t-crossbar, octave dots).

Scaling was the point of the design. Each variant is one CSS block keyed on `data-logo` plus one entry in `LOGO_VARIANTS`; adding another is those two things and nothing else. Variants that style part of the word (the accent letter, split weight, brackets, the t-crossbar) declare an optional `wrap` function and the renderer rebuilds the text with spans, so the header markup stays a single element and nothing else has to know the switcher exists. Everything inherits the base `.logo` rule and overrides only what it changes, and the theme-coloured variants use `--theme-a`, so they re-tint per tab like the rest of the app.

Verified by executing all eighteen against a stub DOM: every one applies cleanly, every one has a matching CSS block, the wrap functions preserve the word, and selecting "Current" fully removes the `data-logo` attribute rather than leaving a stale one behind.

---

## v0.97.36 — Missing glyphs: every font was falling back on ♭ and ♯

Extracted all twelve embedded fonts and tested their cmap tables against the characters the app actually renders. The result was worse than the one bad symbol that prompted this:

**Every font is missing ♭ and ♯** — used 719 times, including the tuner's "♭ Flat / Sharp ♯" readout and every note name in the app. All of it was rendering in whatever the browser fell back to, which is the mismatch that was visible. Also missing everywhere: ş Ş İ (Karşılama). Cinzel and IM Fell additionally lack ã Ã (Baião, the Portuguese one) and ø (half-diminished). Rajdhani is the worst at 84 glyphs, no accented characters at all.

Fixed by subsetting GNU FreeSans (GPL with font exception, so shippable) down to just the fifteen missing characters — 3.5KB — and embedding it as `GlyphFix` with a `unicode-range` covering only those codepoints. Appended to all 945 font-family declarations that use a custom face. Because the range is restricted to the missing glyphs, it fills gaps and cannot affect any character the real fonts already have.

I'd initially said this needed a local re-subset on your machine. That was wrong: fonttools and the FreeFont family are both available here, so the whole fix is buildable in-container.

Also produced `intonare_title_options.html`, fourteen title treatments rendered in the real embedded fonts at real sizes against the real background, for choosing on-device. Covers three groups: the same Fraunces with less treatment, alternative faces already in the app, and drawn lockups with a mark.

---

## v0.97.35 — Descriptions in roman numerals, and two cadence presets that contradicted their own names

**All 65 descriptions rewritten.** Two changes:

*Roman numerals instead of literal chords.* This matters more than consistency: the progression tool transposes, so a description reading "Am Dm E7" becomes wrong the moment someone hits ♯. Numerals stay true in any key. Key names are kept where the preset loads in a specific one ("in Cm"), since that's information rather than drift.

*No editorialising.* Phrases like "the groove does the work", "two chords, endless groove", "the extensions are the sound" and "by design" were stating a stance rather than describing the preset. Descriptions now say what the thing is and stop.

**Two cadence presets did not demonstrate their own cadences.** Checked every description against its actual chord data, which turned up a real content bug in the theory section:

- **Authentic Cadence** was C Am F G, ending on V. That's a half cadence, which the app has separately. Now ii V I (Dm G7 C C), so it actually resolves to the tonic.
- **Plagal "Amen"** was C G Am F, ending on IV — the reverse of what a plagal cadence is. Now I IV I (C C F C).

Half Cadence (C Am Dm G, stops on V) and Deceptive Cadence (C F G Am, V steps up to vi) were already correct and are untouched.

Five other descriptions misstated their own chords and were corrected: Soul Gospel is in F, not C; Minor 5/4 ends on v; Country Waltz's numerals were incomplete.

Full table re-validated with the description checks added to the suite: no literal chord symbols in any description, no em-dashes, every preset categorised, and all the existing structural checks (groove and kit resolution, meter matching including kit time signatures, bar durations, chord roots and qualities) still passing across 60 grooves, 65 presets and 62 kits.

---

## v0.97.34 — Fix: seven presets were invisible in the picker

**You couldn't find the new presets because they weren't being rendered.** The picker grouped presets by time signature using a hand-written list of six meters, and anything that didn't match a filter was silently dropped. Two separate failures:

- **12/8 and 2/4 had no group at all**, so Slow Blues 12/8, Slow Blues (9ths), Gospel 12/8, Polka and March never appeared.
- **The 4/4 filter tested `!p.timeSig`**, meaning presets that carry an explicit `[4,4]` fell through every filter. That hid Cumbia and Bossa (tritone sub) — and explains why Cumbia seemed to "disappear" after the audit moved it from 6/8 to 4/4. It wasn't relocated to a different section; it stopped rendering entirely.

Seven presets in total were in the data and unreachable from the UI.

**Regrouped by genre instead of meter**, which fixes the immediate bug and the underlying fragility. Genre now comes from a `cat` field on each preset, and anything without one falls through to an OTHER section rather than vanishing, so a new preset can never silently disappear again. Sections: Rock/Pop, Blues, Jazz, Soul/Funk, Latin, World, Electronic, Classical/Theory, Odd Meter, Other. This also matches how people actually look for presets, by style rather than by time signature.

**Descriptions rewritten.** All 65 now avoid em-dashes, the word "cadence" as decoration, and the general register of AI filler. Plain and literal: "Three chords, most of rock built on them", "Two chords, endless groove", "V points at the tonic, then goes to vi instead". Chord spellings kept where they're the useful information. En-dashes remain in *labels* like "ii–V–I" since that's chord-relation notation rather than prose.

Verified: 65 of 65 presets render, every preset has a category, zero em-dashes and zero instances of "cadence" in descriptions, and the full table still validates (60 grooves, 66 presets, 62 kits, all groove/kit references resolving, all meters and bar durations correct, including the kit-meter check added in 0.97.33).

---

## v0.97.33 — Salsa, 2/4 meter, and a piano montuno in the song bank

**Salsa was a conspicuous hole.** The montuno groove and Son Clave kit both existed but nothing reached them, while cumbia, samba, bossa, cha-cha-chá and bolero were all present. Added **Salsa** (i–iv–V–i montuno vamp) and **Salsa (ii–V vamp)** with the half-diminished ii and altered dominant that gives minor-key charts their heat.

**2/4 was the one missing meter.** Grooves existed for 3, 4, 5, 6, 7, 9, 11 and 12 beats but nothing in 2, though sigMap already mapped it. Added POLKA 2/4 and MARCH 2/4 grooves plus **Polka** (I–V–I–IV) and **March** (I–IV–V–I) presets. Sources: polka's hallmark is the oom-pah — bass on the downbeat, chord on the offbeat, producing the accented upbeat that makes it bounce; marches share the duple frame but are squarer, which is why the two grooves differ.

**A real piano montuno in the song bank.** Right hand plays a guajeo — the syncopated two-bar ostinato that fills the mid-range and locks to clave, accenting offbeats rather than downbeats. Left hand plays a tumbao that accents the "and of 2" (the 5th) and beat 4, where it *anticipates the next bar's root*; beat 1 is tied over and deliberately not restruck after the opening statement, which is what produces salsa's forward lean. Verified programmatically: all four bars anticipate correctly, exactly one left-hand note falls on a beat 1, and half the right-hand notes are offbeat. Written as an original demonstration pattern to the documented conventions, not a transcription.

**Two new drum kits, and the check that forced them.** Pairing the March preset with the existing "6/8 March" kit looked fine to every existing validator, but that kit declares ts=6 against a 2/4 preset. Kits aren't meter-validated anywhere, so this class of mismatch was invisible. Wrote a new kit-ts-vs-preset-meter check, which revealed that **no ts=2 kit existed at all** — so the 2/4 presets had nothing correct to pair with. Added **2/4 Polka** (kick on the downbeat, snare on the offbeat) and **2/4 March** (both beats firm, no lilt) to the ODD TIME category. The new check now reports zero clashes across all 66 presets.

Totals: 60 grooves, 66 presets, 62 kits. Meters covered: 2/4, 3/4, 4/4, 5/4, 6/8, 7/8, 9/8, 12/8.

---

## v0.97.32 — Audit of the new presets: one harmony error, one tempo error, two mislabels

Re-checked everything added in 0.97.28–31 against sources, with the roman-numeral claims verified programmatically against the actual chord data rather than trusted.

**Disco (Philly strings) had a real harmony problem.** It used Dmaj7, which puts a C♯ against an A-minor tonic — a stretch even for Philly soul's borrowed colour — and the description called it "IVmaj7", which is wrong twice over since IV in a minor key is minor. Changed to Dm9: the lushness stays, it's in key, and the ♭VIImaj7→V7 turn is the actual gospel-tinged cadence the sources describe for the style.

**Bulerías was at half speed.** Sources put it at 195–240bpm counting the individual beats of the 12-count. The groove is 6 beats per bar (two bars = one compás), so the bpm field is the beat rate, and 120 gave a 6.0-second compás against a real ~3.0–3.7. Now 200, giving 3.6s. Soleá stays at 108 (a 6.7s compás), which is right for the slow grave end of the same family, and now says so in a comment.

**Two labelling fixes.** The bossa tritone sub was described as D♭7♯11 while the data says C♯7♯11 — same pitches, but the sub of G7 is properly spelled D♭. CHORD_ROOTS is sharps-only app-wide so D♭ isn't expressible; documented at the chord rather than left as a silent discrepancy.

**Verified correct and left alone:** the Dorian IV in Afrobeat, Deep House (Dorian) and Disco is genuinely major over a minor tonic (D7 supplies the F♯ that natural minor lacks), which is exactly the "im7 to IV7" move sources describe — and House (Dorian 9ths) is correctly distinct from Deep House, which uses Dm7 and stays natural-minor. Trap's Phrygian ♭II checks out: A♯maj7 contains A natural, so it sits consonantly over an A tonic. Samba's I–VI7–ii–V7, the Afrobeats im7–♭VImaj7–♭VII, and the 12/8 blues I7–IV7–V7 all match their sources.

Full table re-validated: 58 grooves, 62 presets, 60 kits, no duplicate ids, all step arrays match their meters, all beats values in sigMap, every groove and kit reference resolves, every bar's durations sum to its time signature, and every chord quality exists in CHORD_DICT (the check that caught the silent B♭13 in 0.97.29).

---

## v0.97.31 — 12/8 meter, plus disco, cha-cha-chá and trap

**The structural gap: 12/8 didn't exist.** There were 12/8 Blues and 12/8 Gospel *kits* in the drum machine, but no 12-beat groove and no 12/8 progression preset — so the meter was unreachable from both tools and those kits could never be selected. 12/8 is compound quadruple (four dotted-quarter beats, each split into three) and is not interchangeable with 6/8, which has two; sources describe it as essential to slow blues, gospel, doo-wop and slow rock ballads. Added SLOW BLUES 12/8 and GOSPEL 12/8 grooves plus three presets: **Slow Blues 12/8** (I7–IV7–V7), its spicier twin **Slow Blues (9ths)** for the uptown B.B. King voicing, and **Gospel 12/8** (I–vi–IV–V ballad).

**Disco** got its own groove rather than reusing funk4. Four-on-the-floor with the backbeat on 2 and 4 is only half of it; sources single out the open hi-hat on every offbeat "and" as the key to the whole groove, which is exactly what distinguishes it from plain funk. Presets: **Disco** (im7–IV7 club vamp, deliberately minimal since the groove is the genre) and **Disco (Philly strings)** for the lush Philadelphia-soul end.

**Cha-cha-chá** — new groove and preset. Jorrín deliberately reduced the syncopation so dancers could follow it, so the groove is steady quarter-note cowbell with the "cha-cha-chá" triple step landing on 4-and-1, less syncopated than mambo by design. The preset is a ii–V–I coro vamp, matching how the coro section cycles a short harmonic loop for the rest of the tune.

**Trap** — new groove and two presets. Sparse half-time kick (beat 1 and the "and" of 3) leaving room for the 808, clap on the backbeat, busy hats; the contrast between sparse kicks and rushing hats is the genre. **Trap** (im–♭VI–♭VII) and **Trap (sus + Phrygian)**, since sus voicings on the tonic and the Phrygian ♭II are both cited trap moves. Harmony stays minimal on purpose: sources note trap's character comes from *when* chords change rather than which ones.

Caught during validation: both 12/8 grooves were first written with 12 steps when the grid needs 24 (the app uses two steps per eighth, matching the existing 6-beat compound grooves). Fixed before shipping.

Totals now 58 grooves / 62 presets / 60 kits, full table valid. Reachability: grooves 26→31, kits 31→37. Meters covered: 4/4, 3/4, 6/8, 12/8, 5/4, 7/8, 9/8.

Deliberately not added: progression presets over the bare clave grooves (son/rumba/tresillo) and the African bell patterns (shiko, gahu, kpanlogo, fanga) — those are rhythm-teaching primitives, not song forms, and a chord loop over them would be arbitrary. The FILLS kits are fills by definition. Coverage for its own sake would be padding.

---

## v0.97.30 — Eight new progression presets, chosen to unlock unused content

Audited which grooves and kits the progression tool could actually reach, and found that **31 of 53 grooves and 33 of 60 kits had no progression preset pointing at them** — more than half the rhythm content in the app was invisible from this tool. So rather than inventing new material, these eight presets expose what was already built.

Each is sourced, and each ships with a "spicier" twin so the pair teaches something:

**Samba** — I–VI7–ii–V7 (Cmaj7–A7–Dm7–G7). Sources describe this circle as the foundation of traditional samba, samba pagode and samba enredo; the VI7 secondary dominant is what keeps it turning, and it's distinct from the bossa ii–V–I already present. Twin: **Samba (tritone subs)**, Jobim's "One Note Samba" move — iii–VI–ii–V with tritones substituted for the VI and V, giving the chromatic bass descent Em7–E♭7–Dm7–D♭7.

**Afrobeat** — Fela-era modal vamp, im7 to IV7 (Am7–D7). Afrobeat sits on one or two chords for minutes while the groove works. Twin: **Afrobeats (modern)** — im7–♭VImaj7–♭VII, deliberately separate because modern Nigerian pop (Wizkid, Burna Boy) is a genuinely different genre from Fela's Afrobeat despite the near-identical name; sources are explicit that conflating them is a mistake.

**Deep House** — Am7–Dm7, the two-chord m7 foundation. Deep house uses extended voicings exclusively (plain Am is "too thin", m7 the minimum). Twin: **House (Dorian 9ths)** — the same vamp with the IV going major (Am9–D9), the Larry Heard move that shifts it from melancholy to soulful.

**Bulerías** — A–B♭ por medio. Bulerías is the fastest 12-beat palo, normally in A Phrygian with a sharpened third, and the traditional rasgueado alternates just those two chords rather than the full Andalusian descent. Twin: **Soleá** — the same Andalusian cadence slow and grave over the 12-beat compás accented on 3, 6, 8, 10, 12, which is exactly what the app's COMPÁS SOLEÁ groove plays.

Reachability: grooves 22→26 of 52, kits 27→31 of 60. Newly exposed: the samba, afrobeat, funk4, flamenco and compás grooves, and the Samba, Afrobeat, 4-on-Floor and Basic House kits.

Validated with the eval-based method: all 54 presets resolve their groove and kit, every groove's beats match its preset's time signature, every bar's durations sum correctly, and every chord root and quality exists in CHORD_ROOTS and CHORD_DICT.

---

## v0.97.29 — Final audit pass: a silent chord in Jazz Blues

Re-audited everything with a changed method: instead of regex extraction (which is what hid the BOOM BAP groove), the three arrays — 53 grooves, 46 presets, 60 kit presets — were eval'd in a real JS engine and cross-checked structurally: duplicate ids, step-array lengths vs meters, sigMap coverage, groove/kit resolution, bar durations summing to the time signature, and every chord's root and quality validated against CHORD_ROOTS and CHORD_DICT.

That last check — which no previous pass performed — caught one real, audible, pre-existing bug: **Jazz Blues bar 3 contained a B♭13, and no `13` quality exists in CHORD_DICT.** `chordGetMidi` returns `[]` for unknown qualities and the caller passes the empty array through, so those two beats played *silence*. Changed to B♭9 — same dominant function, already used elsewhere in the preset. (Adding a proper 13th quality to the global chord dictionary is the fuller alternative if ever wanted; it touches the chord tool's picker, so it wasn't done as a drive-by.)

Everything else verified clean: bar durations sum correctly across all 46 presets including the four new variants, no duplicate ids, all references resolve, all audit fixes from 0.97.26–28 intact. A session-wide sweep also re-confirmed the lid unlock, Waldstein's perf block and credits line, the 38 journey entries with the two tier moves and the six hand-tuned ms sets, the RT_TUNED badge machinery with the TDZ fix, all five Leg Tuner perf-mode fixes, the flagged-off auto-start scaffold, and vocalrange in the native mic surfaces — 22/22.

(Two initial "failures" in the sweep were the checker tripping over its own artifacts: the lid selector legitimately appears in both the lock list and the later unlock rule that overrides it, and the only remaining `q:'13'` string is inside the explanatory comment documenting the fix.)

---

## v0.97.28 — Audit correction + four "spicier" preset variants

**Correction first: the v0.97.26 claim that the Hip-Hop preset's groove didn't exist was wrong, and the "fix" made things worse.** The groove is real — its id is `'hip hop'`, with a space, and it's called BOOM BAP (kick on 1, snare on 2, kick on the "and-a" of 3, snare on 4). My extraction regex matched ids as `\w+`, which excludes spaces, so the groove was invisible to the audit; I declared it missing and rerouted the preset to a generic backbeat, replacing a genuine boom-bap pattern. Reverted — `hiphop_minor` points at BOOM BAP again. Re-audited with space-tolerant matching: it's the only spaced id, so nothing else was hidden, and the real groove count is 53, not 52.

Also worth recording, since it looked like a bug: **the Cumbia preset didn't disappear.** The picker groups presets by time signature, and moving cumbia from 6/8 to 4/4 in the audit relocated it out of the 6/8 section into the larger 4/4 list.

**Four new preset variants**, each teaching a specific harmonic technique rather than just adding extensions. Because the picker groups by meter, each lands beside its plain twin, so they A/B directly:

- **Andalusian (flamenco)** — Am–G–F–E7♭9. The ♭9 is the F natural flamenco guitarists leave ringing on the E, turning it into a Phrygian dominant. Kept separate so the plain preset stays the clean teaching shape.
- **Neo-Soul (extended)** — Am9–Fmaj9–Cmaj9–G9. The original was diatonic sevenths, which is jazz-lite; the 9ths and 13ths *are* the genre.
- **Bossa (tritone sub)** — Dm9–D♭7♯11–Cmaj9. Same ii–V–I with the V replaced a tritone away; shared guide tones keep the pull to C while the bass walks D–D♭–C.
- **Gospel 6/8 (passing)** — C–C7–F–Fm–C–G7–C. Gospel's signature is what happens between the triads: the I7 pulling to IV, the borrowed minor iv walking home.

Caught during validation: the Andalusian twin had been given the `flamenco` groove, which is a 6-beat bulería, against a 4/4 preset. Corrected to `habanera` to match the plain version. Full meter/groove/kit cross-check now passes across all 46 presets.

---

## v0.97.27 — Three flagged grooves resolved with sources

Went back to the six items the v0.97.26 audit had flagged rather than fixed. Three turned out to be answerable from sources and are now corrected; three are genuine judgment calls and stay flagged. Report updated with the reasoning and citations for each.

**REGGAE ONE-DROP** — beat 1 is dropped entirely and the kick lands with the cross-stick *on beat 3*, where it must dominate. The old pattern accented 2, 3 and 4 equally, flattening the exact effect that names the groove. Now beat 1 empty, beat 3 strong, 2 and 4 light.

**MOTOWN** — the signature is snare on every quarter note, not the "&-of-1 / &-of-3" push that was there. Sources are consistent on this (Drumeo, Drumhelper, Redison; Richard "Pistol" Allen on "It's the Same Old Song"). Now quarters throughout with 2 and 4 strongest.

**DANCEHALL** — dembow is documented precisely as a 3+3+2 tresillo with the snare on 16th-steps 4 and 7. The old pattern was kick-only on 0/6/10/14 with no snare interlock, so it had the syncopation roughly but not the "boom-ch-boom-chick".

**Still flagged, and not for lack of research:** jazz swing is a representation limit (swing is triplet-based; the grid is 4 steps per beat and cannot divide by three, so any pattern is an approximation chosen by ear); bossa is a design-intent question (the clave is documented, but whether this preset should be the clave or a comping figure is a choice); gahu has real regional variants and the literature treats it comparatively rather than canonically, so "fixing" it would mean elevating one school's version.

---

## v0.97.26 — Progression tool audit: meters, patterns, pairings (20 fixes)

Full audit of all 42 progression presets, 52 grooves, and 60 drum-kit presets against genre sources. Full report with sources in progression_audit_report.md. Headline findings, all fixed:

**Cumbia was wrong three ways.** Built as 6/8 when cumbia is duple (2/2, 2/4, modern 4/4 — no source anywhere supports 6/8); the app even disagreed with itself, since the rhythm cards and the drum machine's own 4/4 Cumbia kit already had it right while the progression preset ignored that kit for a generic "6/8 Feel". Rebuilt: 4/4 at 92bpm, i–iv–V–i (Am–Dm–E7–Am, the Sampuesana-family tonic/dominant vocabulary), paired with the actual Cumbia kit, groove rewritten as the guacharaca "chu-chucu" cell.

**The Hip-Hop preset's groove never existed.** `groove: 'hip hop'` matched no groove id; the lookup failed silently but groove mode still switched on, so whatever groove was previously loaded leaked through. Now points at funkback.

**Five more meter errors:** calypso 6/8→4/4 (duple per Merriam-Webster/MasterClass), siciliana 3/4→6/8 (Oxford: 6/8 or 12/8 dotted lilt), çiftetelli 11/8→4/4-over-8/4 with the real D-K-T-K-T-D-D-T cell (11/8 is kopanitsa, already listed separately), joropo 4/4→3/4 with the sesquiáltera cross-accent, and ESKISTA renamed KARŞILAMA — the 2+2+2+3 pattern is textbook Turkish 9/8, while the actual Ethiopian groove (chikchika) is 6/8; the Ethiopian Minor preset relabelled to match.

**Eight pattern fixes where the steps contradicted the canon and usually the app's own comments:** tresillo (was 3+4+1; comment says 3+3+2), habanera (now the real dotted-quarter/eighth/quarter/quarter bass), blues shuffle (was a dotted-8th hemiola chain; now swung pairs per beat), maqsum (now the documented D.T...T.D...T... skeleton), irish jig (was accenting every 3rd 16th — the anti-jig hemiola), tarantella (now the quarter+eighth gallop), aksak (now a real 3+2+2), rachenitsa (now a real 2+2+3 — the old steps confused 8th positions with 16th steps).

**Also:** QUINTILLO renamed 5/4 OSTINATO (cinquillo is a Cuban duple cell, not 5/4); BOLERO origin clarified (the 3/4 bolero is Spanish; Cuban bolero is 4/4); pachelbel's incoherent Bossa-kit-under-backbeat pairing → Half-Time.

**Verified correct, untouched:** all four claves (son/rumba × 3-2/2-3), kopanitsa, shiko, soleá compás, the waltz family, all jazz/blues/funk pairings, andalusian cadence, Royal Road, rhythm changes.

**Flagged in the report but deliberately NOT changed (feel judgment calls):** jazz swing's grid approximation, the bossa pattern vs the bossa clave, one-drop beat-3 emphasis, Motown accents, dancehall looseness, gahu variant, fifties/pop1645 near-duplication, and two optional new grooves (real boom-bap hip-hop; Ethiopian 6/8 chikchika).

Validated after the fixes: all 52 step arrays match their meters, all beats values covered by the metronome sigMap, every preset's groove and kit reference resolves.

---

## v0.97.25 — Leg Tuner works on performance-mode songs

The Leg Tuner was written for grid songs and never updated for performance mode, so every perf song behaved wrongly in it. Three separate bugs, one of them destructive.

**Export silently dropped `ms`.** The serializer emitted only `{b,s}`, so pasting an exported table back into the file deleted every `ms` value — reverting all 21 perf songs to beat-based seeking, which is meaningless without a beat grid. Anyone who tuned a song and pasted the result would have quietly broken the rest. Export now preserves `ms` where present and stays clean for grid songs.

**Playback seeked by beats.** `playLeg` used `b*beatMs` regardless of song type. Perf songs' `b:` values are nominal placeholders, so ▶︎ landed nowhere near the intended music — the "too short / wrong spot" behaviour. It now prefers the hook's absolute `ms` for perf songs, matching what `rtDistractSongStart` does at runtime.

**Timelines were blank.** `songBeats()` and the note-tick renderer both read `rh`/`lh`, which perf songs don't have, so the bar count fell back to a default and no ticks were drawn — the "no legs at all" symptom. Both now derive a nominal beat axis from the perf block's real duration and map note onsets onto it.

Also: the edge-edit buttons moved `h.b` only, so on perf songs the row would change while playback kept hitting the old position. `edgeEdit` now keeps `h.ms` in step.

Export round-trip verified against both a grid and a perf song: grid stays `{b,s}`, perf keeps `{b,s,ms}`.

---

## v0.97.24 — Fix: Leg Tuner rendered empty (regression from v0.97.23)

The badge work in v0.97.23 left `card.dataset.needs=(_needs?'1':'0')` sitting one line ABOVE the `const _needs = ...` that defines it. `const` is subject to the temporal dead zone, so reading it early throws `ReferenceError: Cannot access '_needs' before initialization` — on the first song, which killed the whole `Object.keys(RT_JOURNEY).forEach` loop and left the panel with no cards at all.

Moved the declaration above its first use. Verified by extracting the card-building loop and executing it against stub data: renders the card, sets `dataset.needs`, emits the badge. Also reconstructed the previous ordering in isolation to confirm it was genuinely the cause rather than a coincidence.

Worth noting for future edits here: `node --check` passes on TDZ bugs because they're runtime faults, not parse errors, so the syntax gate can't catch this class. Reordering a declaration relative to its use needs an actual execution check.

---

## v0.97.23 — Leg Tuner marks songs that still need tuning

The tuner's yellow "changed" highlight compares against a snapshot taken when the panel opens, so it forgets everything the moment you close it — useful for spotting edits in the current session, useless for tracking what's been tuned across sessions. Added a persistent marker instead.

`RT_TUNED` is a sign-off list (starts empty) and `rtNeedsTuning(id)` returns true for any song that plays from a `perf` block and isn't on it. Those songs get a "NEEDS TUNING" badge in the tuner card header, plus a "Show untuned only (n)" toggle in the toolbar that hides everything else. Add an id to `RT_TUNED` once its legs feel right and it stops being badged.

Perf songs default to untuned deliberately, and it catches both cases: the fourteen entries added in v0.97.21 have analytically-placed hooks no human has heard, and the seven older ones (Clair de Lune, Prélude in E minor, Moonlight I & III, Liebestraum, Für Elise, Prelude in C) *were* tuned by ear — but against their pre-conversion grid versions. Performance mode replaced the timing wholesale, so that tuning is stale and wants redoing. Grid songs keep their original hand-tuned hooks and aren't flagged.

Currently flags 21 of 38 journey songs; the other 17 are grid-based and left alone.

---

## v0.97.22 — Road Trip tier corrections

Audited the tier assignments from v0.97.21 by measuring note density across the whole table, and found the new entries had been tiered on a scale the existing ones were never measured against. Perf songs capture every real note (ornaments, pedal-blurred passagework), grid songs are simplified arrangements — so density isn't comparable between the two kinds. Grid songs in the table run 1.3–7.7 notes/sec; perf songs run 3.2–19.6.

The visible symptom: Fantaisie-Impromptu (11.3 n/s) and Wedding Day at Troldhaugen (11.7 n/s) sat in MEDIUM while being denser than *every* grid song in HARD (max 7.7). Moved both to HARD. Fantaisie-Impromptu is a virtuoso showpiece by any reading, so it was misfiled regardless of the numbers.

Distribution is now easy 10 / medium 13 / hard 15 across 38 entries.

Left alone deliberately: pre-existing grid-song placements that look odd numerically (Carol of the Bells at 3.8 n/s in HARD, Raindrop at 5.6 in EASY). Those were presumably tiered by ear when the table was built, and ear beats formula here — especially since in Road Trip the song is a *distractor* you sing against, where tempo, register and harmonic activity matter as much as raw note count. A slow dense piece distracts less than a fast sparse one. Final tiering wants a few trips per difficulty on-device.

---

## v0.97.21 — Road Trip journey entries for the performance-mode songs

Road Trip draws its journey songs from `RT_JOURNEY`, which is a separate table from the piano bank — adding a song to RIFFS doesn't put it in Road Trip. Twenty-one perf songs had accumulated without journey entries, so they could never be picked for a trip. Added the fourteen piano ones: Alla Turca, Barcarolle, Butterfly, Fantaisie-Impromptu, Moonlight II, Prélude in C-sharp minor, Prélude Op. 23 No. 5, Raindrop, Sonata Facile, To Spring, Träumerei, Troika, Waldstein I, Wedding Day at Troldhaugen. Table goes 24 → 38 entries (easy 10 / medium 15 / hard 13).

Hooks carry absolute `ms` rather than beats. That's required, not stylistic: `rtDistractSongStart` prefers `hook.ms` whenever the song has a perf block, and falls back to `hook.b * (60000/bpm)` otherwise — which is meaningless for a perf song, since it has no beat grid. `b:` is retained as a nominal value only.

Hook placement used the same note-density approach as the original table: five target positions across the piece, each nudged to the densest 2-second window within ±6s so legs land on active material rather than quiet spots. Tiers assigned by notes per second (<7 easy, <12 medium, else hard). These are analytic starting points and have NOT been tuned by ear — they want a pass with the Leg Tuner (long-press the ROAD TRIP title, or `window.rtTuner()`, which has an Export table button for pasting values back).

Rhodes (`_rh`) songs deliberately excluded: `rtPickJourneySong` filters on `RIFFS.piano[id]` and `riffStart('piano', id)` is hardcoded to the piano bank, so a rhodes entry could never be selected — and they're the same music as their piano twins, which would only repeat pieces in the pool.

Waldstein is worth a look when tuning: at 10.3 minutes its evenly-spread hooks sit ~2 minutes apart, far wider than any existing entry, so its legs may want clustering into one dense stretch instead.

---

## v0.97.20 — Waldstein Sonata, first movement (performance mode)

Beethoven's Sonata No. 21 in C major, Op. 53, first movement, from Bernd Krueger's captured performance (piano-midi.de, CC BY-SA). 8,576 notes, 497 pedal changes, 3,242 tempo events in the source (heavy rubato — genuinely performed, not sequenced flat), 81 distinct velocities, 10.31 minutes.

This is now the largest piece in the bank by a wide margin: the perf block is 259,101 characters, against roughly 200k for Moonlight III and ~33k for a typical song. Worth knowing before adding movements 2 and 3 — the complete sonata would run to something like half a million characters, around 5% of the file for one work.

Perf-native, so there's no dormant grid data underneath and nothing for the later grid-deletion cleanup pass to strip. Verified after insertion: all 8,576 notes and 497 pedal events parse, MIDI range 29–93 (F1–A6, correct for the movement's reach), velocities 0.173–0.835, and the first event is the quiet low C of the opening repeated-chord pulse.

Road Trip hooks are proportional defaults at even quarter-points across ten minutes, so they sit far apart; they want retuning on-device via the Leg Tuner. Metadata and the credits modal both updated.

---

## v0.97.19 — Piano lid becomes a listener control

The lid position (closed / stick / open) was set by the song and locked during playback. Every one of the 39 piano songs opened with `_riffPiano('lid','open')` at beat 0, and `.riff-locked` dimmed the lid segment control to `pointer-events:none` alongside the sustain pedal and tone picker, so you couldn't change it mid-song.

Worth being clear about what the lid is: it isn't in the MIDI and it isn't in the score. Krueger's files carry notes, timing, velocity and sustain pedal only, and composers don't notate lid position — it's a performer/venue decision made on the day. So there was never a "score-accurate" setting to look up; every song was just inheriting `open` from the song template.

Changed it to what it actually is — a listening choice:
- Removed the beat-0 lid call from all 39 songs. Nothing forces the lid now, so whatever position you set persists into and through playback.
- Unlocked `.piano-lid-seg-wrap` during playback, joining the octave nav and expand buttons that were already exempt from the riff lock.
- Tidied one organ song whose ctls contained nothing but the (meaningless for an organ) lid call.

The lid filter already retunes via `setTargetAtTime` with a 0.08s time constant, so switching mid-note morphs smoothly instead of clicking. Hearing one performance under three lid positions is a genuinely useful demonstration of what the lid does — closed is 900Hz, stick 4000Hz, open 18000Hz on the lowpass.

Note the save/restore in `_riffSaveState`/`_riffRestoreState` still snapshots and restores the lid around playback; with songs no longer setting it, that path is now effectively a no-op for the lid.

---

## v0.97.18 — Launch mic auto-start scaffold (Android, flagged OFF)

Diagnosed the "tuner needs a tap every launch" behaviour and built the fix behind a flag, defaulted off. **No behaviour change in this build.**

Diagnosis: the 7-tap panel at cold launch reports AudioContext NOT CREATED / NO STREAM / NO ANALYSER / audioMode "not attempted". It is not a permission failure and not native-vs-WebView flakiness — nothing calls `startMic()` at boot, because `startMic`'s `_surfaceWantsNative` test reads mode/currentTool/currentExercise and the boot state isn't treated as a mic surface until you interact. Touching anything both unlocks audio (gesture) and lands you on a mic surface, so the mic appears to need a tap. Ordering, not a platform wall.

Key finding that makes the fix possible: on Android, native capture needs neither a gesture nor the AudioContext. `_nativeMicStart()` only talks to the Capacitor plugin and pushes PCM into `_nativeRing`; `processAudio()` reads `_nativeRing`/`_nativeSampleRate` whenever `_nativeMicActive`, touching analyser/audioCtx only on the WebView branch. So listening is gesture-free; playback (reference tones) still needs the unlock.

Scaffold: `INTONARE_AUTOSTART_MIC` in removeSplash, currently `false`. When enabled it waits 600ms after splash, checks platform is Android, mode is tuner, and the mic isn't already live, then calls `startMic({native:true})` — the explicit native opt-in bypasses the surface test that blocks it at boot. Any failure logs and falls through to today's tap behaviour.

Flagged off because auto-starting this early races MainActivity's RECORD_AUDIO grant, the prime suspect for the original intermittent launch-mic issue. Needs verification across a dozen cold launches on real hardware before it becomes default. iOS deliberately excluded — no native plugin there yet, so it genuinely requires the gesture; when the Swift plugin lands, drop the platform check and both match.

Context: native tuner apps (Fender Tune, Perfect Tuner) auto-enable the mic on open; web tuners require an explicit start. Intonare ships as a native app, so the undocumented tap reads as broken rather than as a design choice.

---

## v0.97.17 — Native mic routing: cover all pitch-consuming surfaces

Audited every mic-using surface against the native-routing lists and found the routing had drifted from the mic-show lists. `MIC_TOOLS` shows the mic on piano/tonal/volume/vocalrange, but `_NATIVE_SURFACES_TOOLS` only routed tonal/piano native — so vocalrange (which runs its own pitch-detection loop for range assessment) was silently on the WebView path, and volume (level meter) too. Added both to native. vocalrange is the real fix: it's a pitch-holding surface, exactly what native stabilizes. volume is a level meter with no pitch detection, added for uniformity, native costs it nothing.

Deliberately left `scales` OUT of native: it appears in MIC_EXERCISES (shows the mic button) but its pitch detection was removed long ago (it's a visual scale strip now, per scalesInit's own comment), so it scores nothing from the mic — routing it native would gain nothing. Flagged separately: the scales mic button is effectively dead UI and may want hiding.

The WebView path stays as the automatic fallback (and remains the only mic path on iOS, which has no native plugin). Full pitch-consumer inventory confirmed complete: tuner, tools/tonal, interval (+ interval test), singsing, roadtrip, vocalrange all consume pitch and now all route native on Android.

NEEDS ON-DEVICE RE-TEST: vocalrange lock/stability was tuned against WebView signal levels; native AudioRecord has different gain/levels, so the comfortable-low/high auto-lock and tessitura detection should be re-checked on-device to confirm the thresholds still behave. If locks feel too eager or too reluctant, the vocalrange stability thresholds need a native-levels pass.

---

## v0.97.16 — Vocal range: Italian localization of the singing-step instructions

Closed the localization gap flagged in v0.97.15. The five singing-step instruction blocks (comfortable low/high, tessitura, extended low/high) had their label, heading, body, and tip hardcoded in English inside vrRenderSingingStep, so an Italian user read English instruction text on every step. Added `labelIt`/`headingIt`/`bodyIt`/`tipIt` twins to all five configs and a language pick (progState.lang === 'it') right after the config lookup, which reassigns the four fields on the fresh per-render config object before the template uses them. Also localized the tessitura status placeholder ("Sing freely in your comfortable range…" / "Canta liberamente nella tua zona comoda…") inline, since it had no i18n key.

Translations follow house style for the module (fry → vocal fry kept as the term, tessitura kept, plain literal phrasing). The scan-complete status was already localized via vr_scan_complete.

---

## v0.97.15 — Vocal range: tessitura window 15s → 20s + sampling nudge

Last item from the vocal range audit. Bumped the tessitura scan from 15 to 20 seconds and rewrote the tip to push the behavior that actually improves the estimate: moving around the comfortable range (varying tunes, sliding between notes) rather than parking on one note, which is what biases a short scan. The center estimate tightens mainly for users near a voice-type boundary; for everyone else it just makes a correct classification a bit more confident. Kept it at 20s rather than 30 to avoid "ran out of things to sing" dead air, which adds clustered samples that don't help. The live trace from v0.97.14 reinforces this — a user can see they've been sitting in one spot and naturally wander.

Noted while here (NOT fixed — logged as its own task): the vocal-range singing-step instructions (all 5 steps' body/tip, plus the tessitura status placeholder) are hardcoded English with no Italian variants. An Italian user hits English instruction text on every singing step. Pre-existing gap, not introduced by this change; wants a dedicated localization pass.

Deferred still: synthesized audio demos of the warmup exercises (#1).

---

## v0.97.14 — Vocal range: live pitch trace on the tessitura step

The tessitura scan previously showed only scattered dots plus a running count and center marker, giving little live feedback that the mic was hearing you or that you were moving around your comfortable zone. Added a real-time pitch trace inside the same strip: the last ~6 seconds of your pitch drawn as a scrolling line (x = time, newest at the right; y = pitch on the E2–C6 range, high = top). Silence between phrases renders as a break in the line, so you see your voice sliding around as you sing.

This replaces the deferred "live trace during the siren warmup" idea. Tessitura was chosen deliberately over the warmup: the mic is already live on this step (no new early mic-start, which matters while the launch-time mic init is under observation), and a live trace does more functional good on an actual measurement step than on a passive warmup timer.

Implementation notes: canvas overlay in the existing dots-wrap (strip height 30→54px), samples pushed every detection frame (~20fps) into a rolling buffer capped at ~200 samples, drawn with the literal-color light/dark pattern (canvas can't read CSS vars), width/height guarded against per-frame reallocation. Buffer resets on scan start and full reset; the trace freezes as a snapshot when the scan completes.

Still deferred: synthesized audio demos of the warmup exercises (#1), and the tessitura-window lengthening from the original audit.

---

## v0.97.13 — Vocal range: stall nudge + clearer lock-button hierarchy

Two follow-ups from the vocal range audit, both aimed at newer singers who get stuck on the comfortable-low/high steps.

**Stall-aware nudge.** Previously, if the ring wasn't filling (voice wobbling, too quiet, or a breathy/fry tone with no clean pitch), the status label just sat on "Locking in… 34%" with no explanation. Now, once progress has stalled below the lock threshold for ~3 seconds, the label tells the user *why*: "Hold it as steady as you can" (pitch is wobbling past the lock window), "A little louder or longer helps" (stable but not climbing), or "Sing a clear, connected tone" (no clean pitch detected — the fry/breathy case). The hint clears the instant progress resumes and resets between steps. New state is reset in vrResetState and vrShowStep; EN+IT strings added.

**Lock-button hierarchy.** The comfortable low/high steps auto-lock once you hold steady, but the fallback button read "Detecting…" then became a bare active button at 40%, which looked like a required press (and pressing it means breaking your held note to reach the screen). It now reads "Listening…" while waiting and "Lock manually" once available, so the auto-lock is clearly primary and the button is an obvious optional override. Extended-range steps are unchanged ("Confirm Note →" — those are manual by design).

Still deferred from the audit: synthesized audio demos of the warmup exercises and a live pitch trace during the siren (paired for their own session), plus the tessitura-window lengthening.

---

## v0.97.12 — Vocal warmup phase-timing fix

Audited the vocal range tool against professional warmup and range-finding practice. The architecture holds up well (canonical hum/trill/siren warmup order, tessitura-based voice classification rather than range extremes, correctly-placed fry and falsetto guidance). One real mechanics bug surfaced: all three warmup exercises shared fixed phase durations of 4s/1.5s/4s/1.5s, which gave the trill and siren "up" slides only 1.5 seconds while the on-screen instruction says "slide up slowly." A full-range siren in 1.5s is a whip, not a slide.

Fix: per-exercise `cycleDurs` on each VR_WARMUP_EXERCISES entry. Hum keeps its original cycle (the short slot is phonation onset; the hum carries through the 4s exhale). Trills and sirens now get a 3s inhale and symmetric 4s up / 4s down slides. Runner falls back to the old durations if an exercise omits `cycleDurs`.

Deferred from the same audit (not shipped): lengthening the 15s tessitura window with a copy nudge toward multiple tunes, a live pitch trace during the siren exercise, an audio demo of a lip trill, and a note that vocal fry won't register on the extended-low step.

---

## v0.97.11 — Rhodes gets performance mode (7 songs)

The Rhodes song bank is a separate set of entries (its own _rh IDs) from the piano bank, so perf conversions do not flow to it automatically. The perf scheduler already routes non-piano instruments through _riffSound, so a Rhodes entry with a perf block plays the captured performance through the Rhodes voice. Pedal data is stripped from the Rhodes perf blocks (Rhodes has its own sustain; the piano damper model should not drive it).

Converted the 2 existing grid Rhodes entries to perf and added 5 new Rhodes songs, chosen to fit the mellow electric-piano character:
- **Prélude in E Minor** (Chopin) — was grid, now perf.
- **Liebestraum No. 3** (Liszt) — was grid, now perf.
- **Clair de Lune** (Debussy) — new.
- **Moonlight Sonata I** (Beethoven) — new.
- **Barcarolle** (Tchaikovsky) — new.
- **Träumerei** (Schumann) — new.
- **To Spring** (Grieg) — new.

Each carries Rhodes trem/vibe ctls and its own metadata in the electric-piano voice. The other 6 Rhodes songs (Gnossienne, Nocturne Op.9, Ständchen, Gymnopédie, Twinkle stride, Arabesque) have no Krueger source and stay on grid. Fast/percussive perf songs (Alla Turca, Fantaisie-Impromptu, Troika, Wedding Day, etc.) deliberately NOT added to Rhodes; they fight the voice.

---

## v0.97.10 — Ten more piano-midi.de performances (five new composers)

Big performance-mode expansion: ten Krueger captured performances (piano-midi.de, CC BY-SA), adding five composers who were absent from the app (Tchaikovsky, Mozart, Grieg, Schumann, Rachmaninoff).

- **Barcarolle** (Tchaikovsky, The Seasons: June): 1502 notes, 671 tempo, 391 pedal, 3:51.
- **Troika** (Tchaikovsky, The Seasons: November): 1852 notes, 661 tempo, 245 pedal, 2:55.
- **Alla Turca** (Mozart, Sonata K. 331 mvt 3): 2819 notes, 947 tempo, 376 pedal, 3:09.
- **Sonata Facile** (Mozart, K. 545 mvt 1): 2714 notes, 1680 tempo, 304 pedal, 4:21.
- **To Spring** (Grieg, Lyric Pieces Op. 43 No. 6): 1626 notes, 615 tempo, 224 pedal, 2:34.
- **Wedding Day at Troldhaugen** (Grieg, Op. 65 No. 6): 3842 notes, 918 tempo, 370 pedal, 5:29.
- **Butterfly** (Grieg, Op. 43 No. 1): 937 notes, 710 tempo, 210 pedal, 1:36.
- **Träumerei** (Schumann, Scenes from Childhood Op. 15 No. 7): 456 notes, 144 tempo, 103 pedal, 2:08.
- **Prélude in C-sharp minor** (Rachmaninoff, Op. 3 No. 2): 1725 notes, 298 tempo, 336 pedal, 4:04.
- **Prélude Op. 23 No. 5** (Rachmaninoff, Alla marcia): 3861 notes, 673 tempo, 374 pedal, 3:17.

All ten are NEW songs (no replacements). Sustain-only (CC64), same as prior batches; one-time CC7/10/91 mixer settings ignored. Each got composer/year/era/note metadata in plain house voice. Credits modal Krueger line now lists all 20 performances. Road Trip hooks not yet wired for the new songs (proportional ms defaults only; retune via Leg Tuner). Twenty Krueger performances now shipping.

---

## v0.97.9 — Four more piano-midi.de performances (Bach, Chopin ×2, Beethoven)

Added Bernd Krueger captured performances (piano-midi.de, CC BY-SA) for four pieces:

- **Prelude in C** (Bach WTC I, BWV 846): replaces the old grid version with Krueger's performance — 1284 notes, 358 tempo events, 70 pedal, 3:45. This is a replace, not a new song (prelude_c already existed).
- **Raindrop Prélude** (Chopin Op. 28 No. 15): NEW song — 1518 notes, 997 tempo events, 485 pedal, 4:30.
- **Moonlight Sonata (II)** (Beethoven, Piano Sonata No. 14, 2nd mvt): NEW song, slots between the existing I and III — 898 notes, 348 tempo events, 131 pedal, 2:04.
- **Fantaisie-Impromptu** (Chopin Op. 66): NEW song — 3050 notes, 2142 tempo events, 491 pedal, 4:30.

All Krueger files are sustain-only (CC64), same as prior batches; one-time CC7/10/91 mixer settings ignored (bach also had CC93 chorus depth, ignored). Three new songs got composer/year/era/note metadata in plain house voice. Credits modal Krueger line updated to list all ten performances. Road Trip hooks not yet wired for the new songs (proportional ms defaults only; retune via Leg Tuner). Ten Krueger performances now shipping.

---

## v0.97.8 — Liszt Liebestraum No. 3 to performance mode

Liebestraum now plays Bernd Krueger's captured performance (piano-midi.de, CC BY-SA): 1888 notes, 970
tempo events, 220 pedal (dedicated pedal track), 82 velocity levels, bpm 23-192 through Liszt's big
rubato, 4:09. Replaces the old grid version. This completes the confirmed direct matches from
piano-midi.de. Road Trip hooks converted to ms defaults (retune via Leg Tuner). Six Krueger
performances now shipping (Clair de lune, Für Elise, Moonlight I & III, Prélude in E minor,
Liebestraum No. 3).

## v0.97.7 — Chopin Prélude in E minor to performance mode

Prélude Op.28 No.4 now plays Bernd Krueger's captured performance (piano-midi.de, CC BY-SA): 604
notes, 335 tempo events, 133 pedal, 67 velocity levels, 1:43. Replaces the old grid version. Road Trip
hooks converted to ms defaults (retune via Leg Tuner). Credits updated. Five Krueger performances now
shipping.

## v0.97.6 — Three Beethoven pieces to performance mode (Für Elise, Moonlight I & III)

Second perf-mode batch. Für Elise, Moonlight Sonata mvt I, and Moonlight Sonata mvt III now play
Bernd Krueger's real captured performances (piano-midi.de, CC BY-SA), replacing the old grid
reconstructions — same treatment as Clair de lune.

All three are rich sequences: Für Elise (1041 notes, 923 tempo events, 150 pedal, 52 velocity
levels); Moonlight I (1144 notes, 720 tempo events, 308 pedal — Krueger sequenced a dedicated pedal
track here); Moonlight III (the big one — 6538 notes, 1223 tempo events, 721 pedal, bpm 14-184 through
the Presto agitato's dramatic ritardandos, ~200KB perf block). Playback lengths match the source files
(2:46 / 6:02 / 6:50).

Road Trip hooks for all three converted to absolute-ms defaults (proportional; retune via Leg Tuner).
Credits modal updated: the Krueger entry now lists all four performance-mode pieces under CC BY-SA.
Adapted MIDIs to be published in the repo's SA folder.

As with Clair: only Krueger's performance data drives playback now; the old Mutopia/authored grid data
stays dormant in the file. Single-layer sample ceiling still applies (dynamics faithful, timbre flat).

## v0.97.5 — Fix overlay scrubber touch mapping under portrait rotation

The expand-overlay scrubber's touch target was off because in portrait the whole overlay is
`transform: rotate(-90deg)`. The drag math read screen `clientX` against the track width, but under
rotation the horizontal track's length runs along the screen's VERTICAL axis (its bounding box is
tall/thin — measured 12×650 on a phone), so horizontal finger motion wasn't tracking the handle.

Drag is now rotation-aware: when the overlay is portrait-rotated it computes the fraction from
`(rect.bottom - clientY) / rect.height` (song start at screen bottom → end at top, matching the
rotate(-90deg) mapping, verified against ground-truth positions). Non-rotated surfaces (card, true
landscape) keep the original clientX/width math. Matches the existing rotation handling used by the
overlay's organ faders.

## v0.97.4 — Transport scrubber in the expand overlay

The song scrubber now appears in the piano expand overlay, not just the card. Kept the time readouts
(the useful part): restructured the overlay now-playing screen into a vertical stack — transport +
marquee tightened and lifted into a top row, full-width scrubber with M:SS current/total times on a
second row below. Buttons and title shrink slightly to make room; no overflow (screen ~50px,
scrub track ~147px on a 412px phone).

Under the hood the scrubber logic is now multi-surface: `_riffScrubEls` returns every present scrubber
(card + overlay), and render/drag/`np-scrub-on` toggling drive all of them in sync off the same
ms-space seek engine. Dragging either scrubber seeks identically. Card scrubber unchanged.

## v0.97.3 — Expanded overlay: pedal indicator now tracks perf playback

The expanded piano overlay has its own damper indicator (`pianoFullPedal`) separate from the card's
(`pianoPedal`). `_riffPianoPedal` was only refreshing the card's, so in expand mode the keys lit
correctly but the overlay's pedal indicator never moved during playback. Now refreshes both. The
overlay keys themselves were already driven (via `_riffFlashPianoFullKey`) and already got the
real-duration hold from v0.97.2, so expand mode is now fully in sync: keys, pedal, and audio.

## v0.97.2 — Perf-mode key visuals hold for real note duration

The held-key highlight wasn't matching perf playback: `_riffPianoNoteOn` flashed the key with no
duration, so every key lit for a fixed ~170ms regardless of how long the note actually sounded. Fine
in grid mode (short re-striking notes) but wrong in perf mode, where his notes have long real
durations — the opening chord rings ~4s but the key released in 170ms, so notes sustained (audio,
correct) while keys looked released and the pedal indicator seemed uncorrelated.

Added a `holdMs` param to `_riffPianoNoteOn`; perf mode passes each note's real duration `n.d`, so the
key highlight now holds for the actual finger-time. Under pedal, the key still releases at the written
duration while the note rings on (pedal) — physically correct. Grid mode unchanged (still defaults to
the 170ms flash).

## v0.97.1 — Perf-mode pedal routing fix

The pedal-routing check in `_riffPiano` only handed control to the damper model when a song had
`rh || lh`. Clair happens to keep those as dormant data so it worked, but any future perf-ONLY song
(no vestigial grid) would have fallen through to `setPianoSustainMode`, which stops all voices — pedal
would have broken. Fixed to recognize `perf` songs explicitly so the damper model (and the visual
pedal indicator refresh) works for perf mode regardless of whether grid data is present.

Note on Clair's pedals: Krueger's file uses ONLY sustain (CC64, 327 events). No sostenuto (CC66) or
una corda (CC67) — those aren't in his sequence. CC7/10/91 present are just one-time mixer settings
(volume/pan/reverb), not performance pedals. Una corda mainly changes timbre, which single-layer
samples can't reproduce anyway, so nothing audible is lost.

## v0.97.0 — Performance mode: real captured MIDI playback (no quantization)

New playback path. Songs can now carry a `perf` block — a flat list of notes with ABSOLUTE
millisecond times/durations plus a pedal event stream, taken straight from a real performance MIDI.
No beat grid, no tempoMap, no quantization: the engine fires each note at its real captured time, so
the performer's micro-timing, pedalling, and dynamics play back intact.

**How it fits:** the scheduler already worked in ms-space, so perf mode just fills the same
`_riffEvents` timeline a different way. Seek, the transport scrubber, and pedal-state reconstruction
all carry over unchanged (pedal transitions ride the timeline as _isCtl events through the same damper
model). Perf branch runs before the grid rh/lh path and returns; grid songs are untouched.

**First conversion — Clair de Lune.** Now plays Bernd Krueger's actual performance (piano-midi.de,
CC BY-SA): 1491 notes, 327 pedal transitions, 58 velocity levels, his real rubato. This REPLACES the
old Mutopia grid reconstruction + extracted tempo curve as what you hear. The Mutopia rh/lh/tempoMap
stay in the file as dormant PD reference data but no longer drive playback. Track length 4:07, his
actual performance.

**Licensing:** shipping his real note/timing/pedal data makes this song a derivative, so CC BY-SA
Share-Alike applies to the adapted MIDI (not the app — SA is viral only onto the derived work). Adapted
MIDIs to be published under CC BY-SA in the public repo. User-visible credit already in the Credits
modal.

**Road Trip:** its beat-based hooks can't index a gridless perf song, so the RT seek path is now
perf-aware — perf songs use absolute-ms hooks (`hook.ms` / `hookMs`) instead of beat math. Clair's 5
journey hooks + 1 fallback hook were given proportional ms defaults so nothing breaks; these want a
precise retune via the Leg Tuner on-device.

**Reusable pipeline:** the MIDI→perf converter emits the notes+pedal block and the ms hook table for
any cleanly-licensed performance MIDI. Future songs convert in a small batch-ship-screenshot loop.

**Known ceiling:** velocity drives dynamics but samples are single-layer, so louder≠brighter-attack
like a real piano. Dynamic shape is faithful; full timbral realism needs a multi-layer sample set
(separate future work).

## v0.96.10 — Clair de Lune tempo from a real performance MIDI (Bernd Krueger, CC BY-SA)

Replaced the audio-derived tempo curve (v0.96.9, which read a touch slow through the animated
section) with one extracted from a real hand-sequenced performance MIDI: Bernd Krueger's Clair de
lune from piano-midi.de.

**Why this source:** it's licensed CC BY-SA (attribution + share-alike, NO non-commercial clause), so
unlike MAESTRO (NC) or GiantMIDI (performance copyright), it can actually be used in a paid app. The
file carries 733 genuine tempo events (range 8-133 BPM) — real fine-grained rubato, not step marks.

**What we took, and what we didn't:** only the abstract tempo CURVE (a list of numbers — tempo is
fact, not copyrightable expression), applied to our existing Mutopia public-domain notes. We did NOT
transplant Krueger's actual notes/pedal/velocity (that would be a derivative work and drag Share-Alike
onto the app). His beat span (319.5) maps ~1:1 onto ours (322), so no stretching needed. Extracted
curve validated against ground truth: our playback lands 4:05 vs his file's 4:08 — essentially exact.

The 404-point curve confirms the user's repeated instinct: motion arrives SOONER than my timid
hand-maps had it (animato peak ~beat 167, the piece reaches real movement early). Isolated sub-40bpm
single-point dips were floored so they read as ritenuto, not a stall; the 11 sharp agogic accents are
Krueger's genuine phrasing and were kept.

**Attribution (required by CC BY):** added a user-visible credit in the Credits & Thanks modal —
Bernd Krueger / piano-midi.de under CC BY-SA for tempo shaping, plus the Mutopia Project (PD) as the
notes source for Clair de lune.

**Reusable:** the MIDI tempo-curve extractor works for any cleanly-licensed performance MIDI — a
scalable path for future pieces.

## v0.96.9 — Clair de Lune tempo from a REAL recording (audio beat-tracking)

Stopped hand-authoring. Ran librosa beat-tracking on an uploaded performance recording (4:48 solo
piano) to extract its actual tempo curve — the library does the listening, we read the numbers.

**What the real performance showed:** settled A-section ~quarter 99bpm-equiv, animated middle only
~1.15-1.2× that (not the 1.4-2.0× I'd been inventing). CONFIRMS the perceived "faster" is mostly note
DENSITY (the 16th arpeggios, ~5× the onset rate) plus dynamics, not a big tempo jump. Also confirmed
the user's ear: motion arrives SOONER than my timid hand-maps had it (Un poco mosso now ~2:10 vs my
2:32), because the real settled tempo is a touch quicker than my cautious 46-52.

Derived curve, rescaled to app base 54 and phrase-smoothed:
`[[0,44],[9,52],[18,57],[27,53],[63,56],[108,60],[126,57],[171,53],[180,56],[279,59]]`

**Honest limits:** librosa's tracker is noisy on rubato solo piano (occasional pulse doubling / drift
in sparse passages), so the tempo RANGE is trustworthy but exact beat-placement of each change is
approximate — audio position doesn't map perfectly linearly to score beat. Good enough, and finally
grounded in a real performance rather than my guesses. The recording was analysis-only (not shipped).

**Reusable:** the beat-extraction approach works for any uploaded performance audio — a scalable path
for future pieces instead of per-piece hand-authoring.

## v0.96.8 — Clair de Lune: humanistic tempo shaping (denser, phrase-level)

The "robotic" feel wasn't about peak SPEED — it was the SHAPE. A coarse 10-point map holds tempo
constant within each span then jumps; real rubato is continuous and phrase-level. Also corrected a
wrong assumption: reverse-engineering a real 5:01 recording's section timestamps showed pros BROADEN
at the climax (take time for weight), not rush it — my prior map accelerated INTO the peak, which is
both mechanical and interpretively backwards.

Rebuilt as a 20-point map with phrase-level give-and-take, grounded in a real recording's contour +
standard practice: flowing opening (~52, not a dragging 46), forward motion into En animant, climax
BROADENS (82→72) for weight, ritardando into every section change, relaxed A' return, and a final
slowing into the quiet close. Total ~6:07 (matches real recordings).
`[[0,52],[18,48],[36,54],[63,50],[81,54],[108,46],[117,60],[144,68],[162,76],[175.5,82],[184.5,72],
[189,54],[207,60],[216,44],[225,52],[243,50],[261,46],[279,50],[292.5,44],[306,38]]`

**Honest ceiling:** even 20 segments is still stepped, not truly continuous. The remaining mechanical
edge is WITHIN-phrase micro-timing (leaning into downbeats, stretching phrase tops) — that lives at the
NOTE level, not the tempo-segment level, and this data-model (beat-quantized notes + tempoMap) can only
approximate it. Fully human timing would require per-note time offsets, which only a real performance
MIDI carries. This is the best the notation-derived source supports; it's a large step toward human,
not a perfect one.

## v0.96.7 — Clair de Lune: stronger, progressive accelerando

The v0.96.6 tempoMap was too timid (flat ×1.4 plateau). Checked the uploaded Oguri performance to
rip its tempo — but that sequence is also ~metronomic (589 beats at flat 120 ≈ its 302s length), so
the acceleration was never in either source file. The dramatic speed-up is INTERPRETIVE (what pianists
do), so it's authored by reference, not ripped.

Grounded in performance/teaching sources: En animant (bar 37) is "bring the tempo forward with real
eagerness… until nothing holds you back"; mainstream readings (Grimaud, Cho) take it markedly faster
than restrained ones (Richter ~25% slower). So: a PROGRESSIVE accelerando, not a step —
46→58→64→72→84→92 through bars 27-42, CLIMAX at ~bar42 (2.0× opening), hard pullback to Calmato
(bar43), settle, a Tempo 1º (bar51). New map:
`[[0,46],[63,46],[117,58],[144,64],[162,72],[175.5,84],[184.5,92],[189,66],[207,56],[225,46]]`

Climax now hits 2× the opening — unmistakable. Peak ~3:34, total ~6:20.

**Tuning levers (by ear):** the climax bpm is the `[184.5,92]` entry — raise 92 for a faster peak.
The build steepness is the 72/84 entries. The pullback depth is `[189,66]`. All single-number nudges.

## v0.96.6 — Clair de Lune tempo changes (tempoMap)

**The piece was playing at one flat tempo — Debussy's tempo changes were missing.** Root cause: they
were lost at COMPILE, before the converter. LilyPond's `\tempo "Un poco mosso"` etc. are TEXT LABELS,
not metronome marks; without an explicit `\tempo 4=N` they don't render to MIDI. The compiled MIDI had
exactly one tempo event (60bpm at tick 0), so the data was genuinely flat and the app played it faithfully.

**Fix:** authored the tempo shifts as the engine's `tempoMap` (already supported — `_beatMs()`
accumulates real time per segment; moonlight/arabesque/liebestraum already use it). Mapped Debussy's
markings to app-beats via the LilyPond `\barNumberCheck` positions (9/8 → 4.5 beats/bar):
`[[0,46],[63,46],[117,56],[162,64],[189,52],[225,46]]` — Andante base 46, Un poco mosso @117 (×1.22),
En animant peak @162 (×1.4, the fast arpeggios), Calmato @189 (×1.12), a Tempo 1º @225 (back to base).

The animated middle now runs 1.39× the opening — clearly audible. Fast arpeggio section lands ~3:20;
whole piece ~6:34 (was a flat 7:00). Scrubber/seek unaffected: they work in ms space (post-`_beatMs`),
so the tempoMap just reshapes the timeline they already read.

**Caveat:** the bpm values are interpretive (Debussy gave Italian markings, not numbers) — the SHAPE is
correct (slow→animated→calm→return) and the ratios musical, but the exact peak speed is a by-feel tweak
if you want to nudge it.

## v0.96.5 — Scrubber layout fix (full-width row)

The v0.96.4 scrubber was nested INSIDE the small `.np-screen` readout, so it rendered ~1px wide.
Moved it out to its own full-width row directly under the riff bar (sibling of `.pto-riff-bar`,
not a child of `.np-screen`). Track is now ~266px usable. Visibility switched from
`.np-screen.np-active .np-scrub` (parent-dependent) to its own `.np-scrub-on` class toggled in
`_riffUpdateTransport` only for active piano playback.

## v0.96.4 — Song transport scrubber (piano card)

**New feature: a seek line under the piano song screen.** Scrub/tap to any point in a track
instead of waiting through it — big time-saver for testing a passage.

- Engine already had the seek primitive (`_riffScheduleFrom(offsetMs)` from pause/resume) and
  a precomputed event list. Added `_riffTotalMs` (track length), and `riffSeek(ms)`.
- **Control-state reconstruction (the careful bit):** a naive reschedule skips every pedal/lid
  ctl before the seek target, landing with the wrong pedal state (notes wouldn't sustain). ctl
  events are now tagged `_isCtl`; riffSeek REPLAYS all ctls up to the target (state-only, silent)
  so the damper/lid is correct at the landing point, then schedules audio forward. Verified
  headless: seeking to 6s replayed exactly the pedal events at 0/2/5s, skipped the 8s one.
- **UI:** thin rail + cyan fill + draggable handle + elapsed/total time (M:SS), shown only while
  a song is active. Full pointer drag + tap-to-seek; a RAF loop advances the fill, suppressed
  while dragging so the handle doesn't fight the finger. Freezes at the paused position. Light-mode
  styled.
- Scoped to the **piano card** for now (first surface). Piano full overlay, organ, and Rhodes
  reuse the same engine — their scrubber UI is a follow-up once the feel is confirmed on-device.

## v0.96.3 — Song playback velocity (dynamics)

**Song playback was fully flat — every note at fixed refVolume.** The scheduler called
`_riffPianoNoteOn(mid)` with no velocity, and the per-note `v:` field (present in some songs) was
dead data, read nowhere.

**Wired velocity through:** scheduler now passes `n.v` → `_riffPianoNoteOn(midi, vel)` → gain on
both sample and synth paths. Curve: `0.32 + 0.68 * v^1.4` (v is 0..1). Perceptual (pow 1.4), soft
floor 0.32 so pp stays audible-but-quiet, ceiling at the user's refVolume so it never exceeds their
level. Absent `v` → full (back-compat; velocity-less songs unchanged). Verified end-to-end headless:
gain is monotonic across v0→v1 (0.32→1.0), absent→1.0.

**Scope of benefit — honest:** these are single-layer samples (one sample per pitch, gain-scaled),
so velocity shapes DYNAMICS (loud/soft swells), NOT timbre (a soft note is a quieter version of the
same tone, not a rounder one). That's most of what matters perceptually, especially on phone speakers.

**Clair de Lune** re-emitted with its per-note velocity (from the Mutopia MIDI). Caveat: LilyPond's
preview dynamics are coarse (here only 2 levels, 0.71/0.87), so the audible gain here is subtle — the
ceiling is the SOURCE, not the engine. Any richly-dynamic MIDI (a real performance, properly licensed)
now gets full shading through the same path.

## v0.96.2 — Clair de Lune replaced with complete public-domain version

**The kunstderfuge Oguri file was NOT usable** — its terms are all-rights-reserved by default
(the file had no CC marking), a subscription doesn't grant commercial use, the NC clause on their
CC subset would exclude a paid app anyway, and it's a protected performance/arrangement (your hard-no
rule). Free-tier placement wouldn't help: the app is commercial regardless of which module a file sits in.

**Clean replacement sourced instead:** Mutopia Project's Clair de Lune (Debussy, Suite bergamasque
L.75), typeset in LilyPond and placed in the PUBLIC DOMAIN by the typesetter — commercial use fine,
no attribution required. Sparse-cloned from github.com/MutopiaProject (GitHub is reachable; ibiblio
isn't), added a \midi block, compiled with LilyPond to MIDI, converted via the new pipeline:
- Two LilyPond staves → real rh/lh split (not guessed).
- 996 note/chord events, full 88-key range, 322 beats, ~2.5% overlap (clean).
- 163 pedal changes authored bar-bass from the LH (LilyPond's sparse \sustain marks didn't render
  to CC64, so pedal was authored the same way as the v0.96.0 pass).
- bpm:46 to match the existing catalog metadata + Road-Trip journey entry (which is a SEPARATE system
  that happens to share the name — untouched).

Replaces the old partial clair_de_lune (pedalled only through b93, the ghost-note remainder). Honest
trade vs the Oguri performance: dynamics are flat and timing is metronomic (notation-derived, not a
performance) — but it's complete, correctly pedalled, and bulletproof on rights.

**MIDI→app converter now exists and is proven** on heavy-rubato + dense-pedal input. Reusable for any
cleanly-licensed MIDI. **Policy going forward: CC0 / CC-BY / PD / self-created only** — never
kunstderfuge or default-ARR performance sequences.

The Oguri .mid was evaluation-only and is NOT in the build.

## v0.96.1 — Brahms Wiegenlied: missing melody restored (OpenScore Lieder, CC0)

**Root cause of "sounds off" found: the transcription had NO MELODY.** Every event was
accompaniment — the rocking thirds, harmony, bass. The famous vocal line (G–G–Bb pickup rising a
minor third, the whole Guten-Abend tune) was absent; the MusicXML export had captured only the
piano staves of this voice+piano lied, dropping the Soprano staff.

**Fix:** pulled the authentic Soprano line from the OpenScore Lieder Corpus (github.com/OpenScore/
Lieder, CC0 public domain, scholarly transcription) via sparse git clone; extracted staff 1 from
the .mscx (54 notes, 3/4, Eb major). Verified alignment against the app's existing accompaniment
by consonance sweep across offsets -6..+3 — offset 0 gave 2% dissonance (best + natural), confirming
the voice maps directly onto the accompaniment beat grid. Merged into rh, then deduplicated 12
exact-beat pitches the voice doubled in the accompaniment (prevents phasing double-strikes).
Same-pitch overlaps 35→22 (remaining are legitimate cross-voice sustains, on par with nocturne).

The pedal added in v0.96.0 now underpins a REAL melody. This is the piece to re-listen to first.

**Method note for future gap-fills:** GitHub-hosted CC0/CC-BY MusicXML is reachable from the build
env (raw.githubusercontent + git clone; kunstderfuge/MuseScore/IMSLP are proxy-blocked, GitHub is
not). OpenScore Lieder (voice+piano, CC0) and OpenScore String Quartets are the good wells.

## v0.96.0 — Pedal-authoring pass (10 songs), moonlight visible repedals, clair ghost fix

**Method:** pedal points derived from each song's OWN encoded LH bass line — bar-bass legato
pedalling (repress at the lowest attack per bar when its pitch-class changes, 1-bar max hold;
2-bar for the gnossienne drone). Grounded against sources: Beethoven's documented con/senza
sordino practice in the Presto agitato; Satie bar-bass wash; stride/blues played dry as standard
practice. All new repedals use the VISIBLE two-event pattern (pedal,0 at b / pedal,1 at b+0.07).

**Pedal authored (repedal counts):** gymnopedie 46 · gnossienne 41 · brahms_lullaby 17 ·
standchen 58 · ode_to_joy 15 · bella_ciao 36 · carol_bells 32 · arabesque_1 102 (replaces
stuck press-no-release) · liebestraum 90 (same) · moonlight_3 con/senza (pedal each arpeggio
sweep, LIFT at the sf chord pairs b7/15/23/27/31, b32 bass arrival + bar-bass tail).

**moonlight (mvt I) flat-pedal fix:** its 149 repedals were same-instant `pedal0;pedal1` in one
ctl — the pedal graphic never visibly lifted (the reported "flat pedal"). All split into the
two-event visible pattern.

**Deliberately dry, documented in code:** blues, st_louis_blues, twinkle_stride (stride/blues
practice — the LH pattern IS the sustain; pedal smears it). Harpsichord/organ/ragtime unchanged.

**clair_de_lune ghost note FIXED:** `{b:84,d:1.5,m:[63,66]}` held F#4 to b85.5 while
`{b:84.75,m:[66,78]}` re-struck it — physically impossible same-string overlap, audible as a
phasing double-strike. Chord split: Eb3 holds 1.5, F#4 trimmed to 0.75.

**brahms_lullaby audit:** melody tones verified consistent with the Eb-major Wiegenlied (no
foreign pitches, no wrong-key notes). Likely "sounded off" because it played bone-dry — now
pedalled. Re-listen before deeper MuseScore comparison.

**Library-wide same-pitch overlap audit (informational, NOT auto-fixed — most are legitimate
merged-tie wash / polyphony / organ voice-crossing; trim only where audibly reported):**
gnossienne 298 · st_louis_blues 104 · toccata_dm 31 · arabesque_1 27 · liebestraum 22 ·
nocturne 17 · air_g 8 · hallelujah 6 · ave_maria 4 · gymnopedie 4 · hungarian_5 2 · singles in
moonlight_3, entertainer, minuet_g, carol_bells, prelude_em, twinkle_stride.

Backup of pre-pass file: /tmp/Intonare.beforePedalPass.html (session-local).

## v0.95.7 — Sostenuto overlay highlight + song pedal audit

**Sostenuto on the FULL PIANO OVERLAY:** the audio logic is provably correct (verified headless
across 5 scenarios: capture, new-note-after-pedal not held, damper-holds-through-sost-off, per-note
finger tracking). The real defect was VISUAL: stopRef only cleared the inline card's `pb-` key
highlight, never the overlay's separate `pwkf-`/`pbkf-` keys. So a sostenuto-held note released on
pedal-lift stopped its audio but kept its lit key on the overlay — reading as "the note didn't stop".
Fix: stopRef now refreshes highlightPianoFull from refOscs when the overlay is open. Verified headless:
note stops AND highlight clears.

**Song pedal audit (all 30 chart songs):** classified pedal coverage. Correct-as-is: harpsichord
(prelude_c, minuet_g, canon_d) + organ (toccata_dm, air_g, hallelujah, lacrimosa, bridal_chorus) +
ragtime (entertainer) legitimately have no damper pedal; RH-only practice variants likewise.
- **hungarian_5**: was organ with a stuck pedal-down (pressed at b:0, never released) → pedal removed
  (organ has no damper).
- **arabesque_1, liebestraum**: stuck pedal-down (press-no-release) — LEFT as-is pending proper
  per-phrase pedalling (documented below, not faked with a single release).
- **11 songs flagged NO PEDAL that arguably want it** (moonlight_3, ode_to_joy, gymnopedie,
  bella_ciao, carol_bells, gnossienne, brahms_lullaby, standchen, blues, st_louis_blues,
  twinkle_stride): deferred to a dedicated pedal-authoring session — correct pedalling needs
  per-piece harmonic-rhythm work, not a batch.
- **clair_de_lune**: known-partial — pedalled only through beat 93 per its own source comment;
  the un-authored remainder is the likely source of the reported "ghost notes". Also deferred to
  the pedal session.

**PINNED FOR NEXT SESSION: pedal-authoring pass** — 11 no-pedal songs + arabesque/liebestraum
stuck-down + clair_de_lune remainder + brahms_lullaby MuseScore re-audit.

## v0.95.6 — App-wide parity + content audit pass

**Ran intonare_light_contrast_audit + intonare_draw_color_sweep + intonare_strings_audit.
Verified every session color fix is properly `_nkLight`/theme-branched (dark preserved).
False positives confirmed: splash, Road Trip (keep-dark), tonale wave (deliberately dark via
its own light rule). Real fixes:**

- **sgDrawModeKeyboard (Survival Guide mode keyboard)**: emphasis INVERTED on light — bright
  in-scale keys blended into the light panel while "dimmed" dark keys popped. Now `_lt`-branched:
  light gets washed-pale dims / solid lits (root white `#0f7d99`, root black `#0d6d86`, on-black
  `#3d4454`, dims `#d7dae2`/`#a7abb8`); dark unchanged.
- **fluteTrillPulseApply**: open-key trill label hardcoded pale `#c4d2dd` → `#2a3442` on light.
- **vrRenderHistory**: sparkline strokes α.6 green/salmon washed out on light card →
  `rgba(15,110,72,.85)` / `rgba(184,80,50,.85)` on light; dark unchanged.
- **prChallengeEnd summit flag**: near-white pole `#d8d8e0` invisible on light end screen →
  `#5a5a72` on light.
- **tc-stop text**: `#2f6e28` (3.49:1) → `#275e21` for contrast headroom.
- **CONTENT FIX — transposing-instruments learn card**: claimed "recorder and tin whistle sound
  at concert pitch" — contradicted by the v0.95.0 range audit (both are octave-transposing).
  EN corrected; matching IT paragraph ADDED (the IT twin had never had the closing paragraph —
  pre-existing drift fixed in the same stroke).
- Verified clean: tours have no CRT/phosphor/dark-screen references; tonal help body is
  mode-neutral; theremin hint's "dark surface" stays true in both modes; "tap keys to hear"
  scale hint is accurate again post-pssPlayNote fix.

**Pre-existing debt logged, not fixed** (for a future session): 6 i18n-html keys missing from
both dicts (rr_mode_listen, rr_mode_sight, rt_hero_title, tc_standby, vr_duration_hint,
vr_safety_hint — fall back to hardcoded EN); 20 borderline 3.0–4.5:1 light-mode text colors
(mostly piano overlay / riff cards); tuba contrabass low E0 unverified.

## v0.95.5 — Muted-string X more legible

- Chord-diagram mute-X was thin salmon `rgba(255,138,101,0.8)` at size 10 — low contrast on the
  light panel. Now theme-aware: deep red `rgba(184,42,28,0.95)` on light / brighter coral
  `rgba(255,120,90,0.95)` on dark, size 13, weight 700. Baseline nudged to `topFret - 10` so the
  bigger glyph still clears the nut.

## v0.95.4 — Chord diagram open/mute markers clear the nut

- Open-string ring + mute-X in gccDrawDiagram sat at `topFret - 10`; the ring (r4) bottom edge
  landed on the nut top (both at y≈22), clipping. Raised ring to `topFret - 13` and X to
  `topFret - 11` for a clean gap. Still inside the 28px top margin. Scale-view open notes use a
  proportional `topFret - fretSpacing*0.65` offset — already clear, untouched.

## v0.95.3 — Barre/glyph light-mode + DMG-olive green cohesion

- **Fretted barre line + markers light-mode**: barre line was near-white `rgba(232,232,240,.6)`
  (invisible on the pale light neck) → slate `rgba(48,50,72,.85)` on light. Open-string ring
  `rgba(52,211,153,.8)` → deep green `rgba(15,110,72,.9)` on light. Fret-position + capo labels
  (gcc + gss) green-on-panel deepened to `rgba(15,110,72,.95)` on light. Muted-X salmon reads
  on both — left. gssDrawPosition open-string already handled last round.
- **Tonal green cohesion (DMG olive)**: the active-keycap/start-button green was modern mint
  `#34d399` (cyan-leaning, ~157°, borrowed from global tools-teal) fighting the authentic
  DMG-olive screen (~140°, yellow-tinted). Per Game Boy palette references (#0D5E1F/#3E9E4F
  family), retuned the whole module to one hue family: active keycaps `#34d399`→`#4a9e3f`
  (mid-olive), start button `#34d399`→`#4a9e3f`..`#6ec254` (brightest olive = CTA), stop text
  `#2f6e28`. Screen unchanged (it was the olive source). Now: sage screen · mid-olive pressed ·
  bright-olive CTA — hierarchy within one family instead of two decades of green colliding.

## v0.95.2 — Fretted note dots, harmonica green, tonal green match

**Three more from the device pass.**

- **Fretted note dots readable in light mode**: non-root scale dots (gssDrawPosition) and
  chord finger dots (gccDrawDiagram) were near-white `rgba(225–232,...)` — invisible on the
  pale light neck. Now `_nkLight`-aware: deep slate `rgba(48,50,72,.9x)` fill on light with
  light `rgba(235,236,244,.92)` numerals; white-on-dark unchanged. Open-string hollow stroke
  also darkened on light. Out-of-bound dots already handled. gssDrawFretboard was token-based
  (var(--text)/var(--accent-warm)) — already correct, untouched.
- **Harmonica → diagram green**: blow/draw cell active/in-scale/primary states moved from the
  cyan `rgba(94,226,255)` family to `--diagacc` (color-mix for the alpha tiers), matching the
  other woodwind diagrams. Active-cell dark text still reads on the green fill.
- **Tonal active-keycap green matches start button**: selected root/octave/temperament caps
  went from deep forest `#2f7a52→#1f5c3b` to the start button's arcade family
  `#34d399→#22936c` with dark text; kept a touch deeper than the CTA so a pressed key still
  reads as pressed. Stop-button text bumped to `#1a7d5b` to match.

## v0.95.1 — On-device feedback round + scale-screen tap regression

**Six fixes from Daniele's v0.95.0 device pass, including one real regression found via
headless hit-test elimination.**

- **REGRESSION FOUND & FIXED — pssPlayNote amputated tail**: the scale screen's manual
  key-tap player computed ctx/chain/dur/toneId then ended after the organ branch — a past
  edit ate the non-organ playback. Every non-organ instrument's scale-screen taps were
  SILENT (noticed on mallets). Restored `_chartPlay` + harmonics-fallback tail mirroring
  pccPlayNote. Verified headless: taps now trigger voices for mallet + piano. Candidate
  for a sentinel pin next session.
- **Diagram accent token**: woodwind/ocarina hole fills, ww-hole CSS, trill overlay moved
  from `var(--accent)` (resolved dark forest in light tools) to new `--diagacc: #2ec78f` 📌
  pinned at the original light green in BOTH modes.
- **Chromatic harmonica slide lever**: light-mode rules — light metallic stem/head, drop
  shadow removed, diagacc-tinted when active.
- **Metro screen whitened**: `#d4d2cc→#c8c5bd` → warm white `#f0eee6→#e5e1d5` 📌, border
  `#cec8b6`; scanlines whisper override rgba(70,60,30,.018) matching the tuner treatment.
- **Tonal centre chrome → Game Boy shell grey**: cabinet `#dcdeda→#c5c8c1`, strips
  `#dadcd7→#cdd0c9`, keycaps `#eeefec→#cfd2cb` (sharps darker), dd/help/stop surfaces
  `#e4e5e1`, scale-map ring greys. Screen stays DMG sage; active keycaps stay green.
- **Theremin box**: the module-level keep-dark soft-frame rule (1px rgba(180,180,205,.5)
  outline) removed for #toolTheremin (obsolete now that theremin has real light rules);
  dead #toolTonal selector removed with it.

## v0.95.0 — Light-mode completion sweep + instrument range audit

**Big batch: the light-mode visual cluster closed out, plus a full audit of WIND_RANGES
against standard orchestration references (the tin whistle bug turned out to have siblings).**

**Fixes / features:**
- **Subtype sample loading**: `switchSubType()` never called `_loadInstSamples()` — only default
  subtypes (marimba, alto sax) ever loaded samples. Now loads on switch; mallet branch added.
- **Tin whistle octave**: D whistle 74–98 (D5–D7 concert), low-D 62–86; tone remapped flute → piccolo;
  register/embouchure breaks made range-relative.
- **Piano voice preview**: sample-backed tones defer preview until loaded (no synth-first blip).
- **Scale-stop stuck key** (all isPianoRenderInst): `pssStop` now re-renders via `pssRender()`;
  `pssFlashKey` never captures flash green as "original".
- **Woodwind hole accents** unified to `var(--accent)` across all 7 SVG renderers + ocarina + CSS.
- **Fretted/harp necks light mode**: `_lt` in-draw flags; NK_/FB_CTX_ ink constants; bowed boards stay dark (wood rationale).
- **Appearance switcher**: outline SVG icons (auto/moon/sun, currentColor) + dynamic label via
  `appearance_auto/dark/light` i18n (finally used); `applyAppearance()` sets label; `setLang` re-localizes; titles removed.
- **Tuner + chroma screens (light)**: `#b6bdd3→#a6afc8` → bright cool-white `#e6e9f3→#d8dce9` 📌;
  scanlines to whisper rgba(30,40,70,.018).
- **Chroma glow (light)**: theme-aware `_chromaGlowStyle(g)` — dark keeps cyan halo; light blooms deep teal
  `#00536c`; JS sets color with 'important' priority; CSS active rule demoted to resting fallback.
- **Theremin**: compact pad-wrap heavy drop (0 6px 20px black) → soft lift 📌; expand overlay dropped
  `keep-dark` → two-tier (backdrop/console follow light; `.thmn-ov-pad` + `.thmn-vol-col-track` held dark).
- **Tonal centre light mode = retro LCD (DMG sage)** — approved via tonal_light_proof.html variant A.
  `#toolTonal` dropped `keep-dark`; `--tc-*` ink set remapped (screen `#cfd8b4→#bfcb9e→#aab88a`, ink `#16351f`);
  sage cabinet/scale-map; light keycaps (green when on); chrome cards on tokens (tools teal);
  start button stays arcade green; `tcWinflashL` light win-flash. Dark mode untouched.

**Range audit (WIND_RANGES, concert MIDI, old → new):**
- Recorder family was an OCTAVE LOW (written-as-sounding, the whistle's bug-class):
  soprano 60–84 → **72–96**, alto 53–77 → **65–89**, tenor 48–72 → **60–84**, bass 41–65 → **53–77**;
  embouchure bands made range-relative (`low+12/+24`). Fingering oct-2 logic already range-relative — unaffected.
- Sax: alto 44–87 → **49–80** (low was tenor's), tenor 44–82 → **44–75**, soprano 56–94 → **56–87**,
  bari 32–75 → **36–68** (low-A floor). All lows now land exactly on written Bb3/A3 via wwTransposition.
- Trumpet std 54–84 → **52–82** (written pasted as concert); piccolo 66–96 → **64–94**.
- Flugelhorn 52–82 → **52–80**; soprano trombone 54–91 → **52–82** (G6 top was fantasy).
- Clarinet A 50–89 → **49–88**, Eb 50–89 → **55–91** (were Bb clones).
- Cor anglais 51–77 → **52–81** (both sub + standalone).
- Chromatic harmonica 60–108 → **60–98** (12-hole tops at D7).
- Verified correct, unchanged: horn, euphonium, tuba std, tenor/bass trombone, flute/piccolo/alto flute
  (comment fixed to G3–G6), Bb clarinet, bass clarinet, oboe, bassoon, ocarina, diatonic harmonica.
- Flagged, not changed: tuba contrabass low 16 (E0) looks optimistic but tuba pedal claims vary; needs a source.

## v0.81.58 — @capacitor/app was never installed

**The deep links never had a chance.** Not the original handler, not the flag fix,
not the three-bug autopsy in v0.81.57. All of it was downstream of a plugin that was
never in the build.

`getLaunchUrl()` and the `appUrlOpen` event come from **`@capacitor/app`** — a separate
npm package from `@capacitor/core`. It was never in `package.json`. Share, haptics,
status-bar, notifications, screen-orientation, RevenueCat: all installed. The App
plugin: not. So `window.Capacitor.Plugins.App` was `undefined` on every device, always,
and every deep-link handler ever written waited politely on a plugin that did not exist.

Found because the failure shape finally isolated it: Play-installed v0.81.57, link opens
the app directly (so App Links ARE verified, manifest and assetlinks are right), but the
app opens plain. The URL was reaching the app and dying at the missing plugin.

Fix, on the dev machine:

    npm install @capacitor/app
    npx cap sync

Also added a **tripwire**: if the app is on a native shell and the App plugin never
appears within the poll window, `_intonareDiagAppPlugin` records it, and the 7-tap
diagnostics panel now has an `App plugin` line right under `Capacitor`. This failed
silently for weeks because nothing anywhere was responsible for saying so. Now
something is.

**The v0.81.57 fixes stand** — they were verified against a mocked App plugin and the
logic is right. They simply could not run until the plugin existed. This is the same
lesson as the whip-on-Android copy step, one layer up: the code being correct means
nothing if the artefact never ships with its dependencies.

---

## v0.81.57 — the deep links: three bugs, stacked, and the first one made the other two unfixable

**The links had never worked.** Not since they were written. Every fix before this
one was correct and none of them could possibly have run.

### 1. The handler lived inside `removeSplash()`

This is the whole thing. The deep-link handler — the `getLaunchUrl()` call, the
`appUrlOpen` listener, all of it — was nested inside `removeSplash()`, which runs
when the splash **ends**.

So the handler that exists to skip the splash was only registered *after the splash
had already finished*. It was structurally incapable of doing its only job. A brace-depth
walk settled it: `removeSplash()` spans lines 16720–17040, and the handler sat at 16800.

It explains both symptoms at once, which is how you know it is the real one:

- **the splash never skipped**, because nothing asked it to until it was over;
- **the module never opened**, because `getLaunchUrl()` only resolved ~3.5 s in, by
  which point the splash's handoff to the home screen had wiped out whatever the
  link tried to open.

Moved to the top level of the script block, so it is listening before the splash starts.

### 2. `go()` fired 250 ms before its dependencies existed

Measured, not guessed:

    getLaunchUrl() resolves      ~77ms
    go() therefore fires        ~157ms   (setTimeout(go, 80))
    enterExercise() is defined  ~410ms   ← a script block ~40,000 lines further down

`go()` called `enterExercise` a quarter-second before it existed, threw
`enterExercise is not a function` straight into a bare `catch (e) {}`, and the link
silently did nothing. **That catch is why this never surfaced as an error: it swallowed
the only evidence.**

### 3. Waiting for `enterExercise` to *exist* is not waiting for the app to be *ready*

The first attempt at (2) polled for the function. That turned the bug into a coin flip —
one run gave chordle ✓ tonale ✗ diadle ✗, the next gave the opposite. Same code, same
build.

The functions appear at ~410 ms, but the app is still booting: there are
`DOMContentLoaded` handlers as far down as line ~99500, plus a `window` `load` handler,
and they set up the home screen. Open a module before those run and the boot sequence
calmly resets the view on top of it.

Now it waits for `window` `load`, which fires after every deferred handler — the exact
guarantee needed: nothing else is going to redraw the shell after that point.

### Also: don't give up if Capacitor isn't there yet

`if (!window.Capacitor) return;` — one check, at the earliest moment in the file, no
retry. The bridge is injected by the native shell and is not guaranteed to exist while
this inline script is still parsing. Lose that race and the listener is never registered.
Now polls (100 × 100 ms, bounded, stops cleanly on web).

**Verified 20/20:** all four dailies × both URL shapes × bridge speeds 0/250/700 ms, plus
warm-app (`appUrlOpen`), a second link over an already-open module, and garbage input
(empty/unknown/no `?m=`/wrong domain) falling through to a normal launch.

> **Note for testers:** the dailies are Pro-gated. A non-Pro tester tapping a shared link
> gets the paywall, not the puzzle. Correct behaviour, but it looks exactly like a broken
> link. If links still fail on a Play build, check
> `adb shell pm get-app-links com.lieutenantdan.intonare` first — if App Links are not
> `verified`, Android opens Chrome and none of this code ever runs (that is an
> assetlinks/signing problem, not a JS one).

---

## v0.81.49–56 — Road Trip: per-theme dressing

A `.rt-dressing` layer per theme. Pure CSS gradients, no assets.

**It rendered perfectly and was completely invisible, for two reasons:**

1. It was a **sibling** of `.rt-menu` at `z-index: 1`. But `.rt-menu` is `z-index: 12`
   with a full-height opaque themed background, so it painted straight over the top.
   Moved the layer *inside* the menu.
2. Every theme carries `#exRoadTrip.rt-dsn-X .rt-menu > * { position: relative; }` — a
   wildcard that catches **every** direct child, including the dressing. It forced
   `position: relative`, which made `inset: 0` meaningless and collapsed the layer to
   **zero height** as a flex item. Two classes on the id outranks anything reasonable,
   so: `!important`. Rare, and correct here — a blanket wildcard reaching past its
   business, and a five-place fix would rot the day someone adds a sixth theme.

**Which means the earlier "strengthen the colours" pass was pure theatre** — doubling
alphas on a layer that was zero pixels tall.

Once visible, the design work (all Dan's calls, on-device):

- **Parchment** (v0.81.52–53): coffee rings didn't read — a perfect circle reads as a
  circle, not a stain. Tried fold creases (rendered as huge diagonal light streaks) and a
  white radial to punch a hole in the ring — **under `mix-blend-mode: multiply` white is
  not a hole, it's a lamp**, and it rendered as a sun in the middle of the map. Both cut.
  Now: edge-aging only. Four irregular ellipses so the border isn't symmetric (one even
  inset shadow reads as a photographic vignette, wrong century), corners going first,
  scattered age spots. **Nothing in the middle, because that's where the content lives.**
- **Blueprint** (v0.81.52): the grid alone is wallpaper. Added drafting furniture — a
  title block in the bottom-right corner, a dimension line down the left margin with end
  ticks, an uneven cyanotype exposure wash. Three objects, all in the margins.
- **Blueprint START** (v0.81.54): was `rgba(255,210,63,.1)` — **ten percent**. The most
  important control on the screen was a ghost and read as disabled. Now solid amber,
  dark text (amber-on-amber is not a button).
- **Nautical** (v0.81.54–56): rhumb-line web was a full-screen fan of lines behind the
  content — texture, not decoration, and it fought the cards. Replaced with a compass
  rose; the map already has one, so that was just a second rose. **Cut entirely.** The
  theme carries itself on its grid and palette. Deliberately bare.
- **Night / Ink:** stars, headlight glow, ink bleed. Unchanged.

---

## v0.81.47–48 — Road Trip start screen stopped short of the bottom

The first fix (flex on `.rt-menu`) did **nothing**, and Playwright measured 250 px of
dead space to prove it. `#rtMenu` is a **child** of `.rt-stage-wrap`, not a sibling, and
`.rt-stage-wrap` is `flex-grow: 0`.

**A child cannot outgrow a `flex-grow: 0` parent.** Grow the container, not the leaf.

Then `justify-content: space-between` on the menu: cards read from the top, START sits in
the thumb zone, 264 px of slack between. Measured 0 px dead. In-trip map still a perfect
square (aspect 1.000 — the vehicle/pin maths depends on it).

---

## v0.81.39–46 — rhythm flash cards: the tap zone, and the card that kept growing

Many rejected iterations (pad-as-transport, dome/glow, moved feedback rows, arrows
re-homed) before Dan called it: *"tap area was good two builds ago, just do that."*
Reverted. Arrows now flank the pad inside the tap-zone wrapper; transport hides wholesale.

**The card kept expanding on entry to tap mode, and it took three attempts to find why.**
Not the layout, not the CSS I'd added — `rcArmTap()` was writing `t('rc_tap_ready')` into
`#rcTapFeedback` on mode-entry. Non-empty text defeated its own `:empty { display: none }`,
which added a row *and* a 12 px flex gap. **Don't write text into a feedback row on
mode-entry.** (`rc_tap_ready` is now an unused i18n key. Harmless.)

Also fixed en route: hiding `.rc-transport` had killed the prev/next arrows (siblings of
PLAY); a third stale copy of the tour text at L37989 said "hit PLAY" with no `<strong>`,
so grep had missed it. **Italian apostrophes (`l'entrata`) break single-quoted JS i18n
strings** — escaped; the syntax gate caught it.

---

## v0.81.38 — settings that would not stick, and a feature nobody could reach

A sweep of every module-level setting in the app, after the Road Trip theme turned out
never to have been saved. It was not an isolated bug.

### Nine settings reset to factory on every single launch
- **`chordScaleInstrument`** — *your instrument*. Arguably the most personal setting in
  the app, and a trumpet player was re-picking trumpet every time they opened it.
- **`metroAudioOn`**, **`metroVolume`** — the metronome came back unmuted at 50% no
  matter what you had set.
- **`rtDiff`** — Road Trip difficulty.
- **`ssNoteMode`**, **`ssAutoAdvance`** — Pitch Match's shown/hidden and auto-advance.
- **`gccQuality`** — chord chart quality.

All now persist, via a small `prefGet`/`prefSet` pair. Every access is wrapped:
localStorage can be unavailable (private mode, storage pressure), and a setting that
fails to save should be an annoyance, not a crash. Values are validated on read, so a
stale entry from an older build falls back to the default rather than poisoning the
module.

### What the sweep also found — and deliberately did NOT change
- **Interval Training was never broken.** It already persists range, difficulty, sing
  direction and the rest through `progState.ivPrefs`. The first pass "fixed" it anyway;
  that was reverted, because a second restore path would have fought `ivLoadPrefs()` and
  won or lost depending on load order.
- **`chordScaleInstrument` is reassigned temporarily** in a few places — opening a
  Rhodes card swaps it to `piano` and swaps it back two lines later. Saving on bare
  assignment would have persisted `piano` for anyone who so much as looked at a Rhodes.
  The save is wired to `switchChordScaleInstrument()`, the actual user-facing setter,
  and nowhere else.
- **`gccToolMode`**: every assignment is an internal swap that restores itself. No user
  setter, so nothing to persist.

### And `ssDifficulty` turned out to be a whole feature nobody could reach
It was read but never written — permanently `easy`. Digging in, `SS_DIFFICULTIES` is
**fully implemented**: a real curve for Pitch Match's string mode, from major pentatonic
(no semitones, easy to sing) through major to full chromatic, with step-versus-leap
ratios and sequence lengths tuned to match.

| | scale | notes | max leap |
|---|---|---|---|
| PENTATONIC | major pentatonic | 3 | 2 |
| MAJOR | major | 4 | 3 |
| CHROMATIC | all twelve | 5 | 5 |

**No picker existed anywhere.** String mode is a live tab, so people could play it — and
every one of them was locked to the easiest tier forever, with two thirds of the content
unreachable. There is a picker now, in the settings sheet, shown only for string mode
since nothing else reads the setting. Named by the scale rather than easy/medium/hard,
because that is what it actually changes.

### `ssPlayMode` never persisted either, and the reason is grim
The tab handler called `ssSavePrefs()`, guarded by `typeof ssSavePrefs === 'function'`.
**That function was never written.** The guard swallowed the call, nothing threw, and the
play mode silently failed to persist — for however long that has been there. A defensive
`typeof` check around a function that does not exist is indistinguishable from one around
a function that does.

Restores and saves are symmetric: nine settings restored on boot, the same nine saved
on change. Nothing restored that is never written; nothing written that is never read.

## v0.81.36 — Road Trip: the legs were flat, and the grading was grading the wrong thing

### It was listening to itself
`rtPlayHome()` sounds a 1.2 s reference while `rtPhase` is still `'home'`, so the hold
meter filled from the app's own speaker before the singer opened their mouth. Same bug
Pitch Match had. Detection is now deaf while the reference sounds, and the lock
progress resets so your turn starts clean.

### An A needed 12 cents
A semitone is 100 cents. Twelve cents is a professional standard — trained singers
drift more than that on a held note — and this was asking for it **from memory, after a
distraction, with no reference**. Almost everything came back C or D. A game where good
play looks like failure is not hard, it is discouraging.

Now **25 / 40 / 60 / 85**. Still discriminating: 25 cents is audible and you have to
actually hold it. But a decent attempt now looks like one.

(The result *words* were on different thresholds than the *letters*, so a leg could be
graded B and told you had "lost it". Aligned.)

### It never said which way you missed
The grade is an absolute error, so there was nothing to do differently on the next leg
except try harder. **Sharp or flat is actionable.** Shown after grading, never during —
it teaches without giving the answer away.

### The bar was a clock
It filled on elapsed time whether you sang your heart out or held your breath, and
finished on schedule regardless. Nothing you did changed anything on screen, so the leg
was something happening *to* you. That is the flatness.

**The bar now fills with sung time** — it only advances while a voice is actually being
heard, so the bar *is* your singing, and stopping stops it. It still carries no pitch
information whatsoever: right note or wrong, it does not care and will not tell you.
The recall stays blind. A 260 ms grace window keeps it moving through breaths, and a
wall-clock ceiling stops a silent room hanging the leg.

(A first attempt put a live *needle* on screen. It positioned a dot by cents error and
claimed not to show the target — but dead centre **was** the target, and one leg in you
would have simply tuned to it. That kills blind recall, which is the whole exercise.
Deleted before it shipped.)

### The grading was grading the wrong thing
The median already killed isolated junk — one voice crack, one bad frame. Two things
got through it, and both cost grades that had been earned:

- **Octave errors.** Detectors mis-report 2x or 0.5x the true frequency, and they do it
  in *runs*, not single frames — so the median moves to the wrong octave and you get an
  **F for singing the note perfectly**. Samples are now folded into the octave nearest
  home.
- **Scooping.** Sliding up into a note is how most people sing. Taking the back half was
  meant to skip it, but a slow scoop is still climbing at the halfway mark, so the
  median landed mid-slide. Frames that are still *travelling* (>35 cents of movement
  between frames) are dropped, leaving only the part you actually held.

Neither makes the grade softer. They stop it measuring the wrong thing.

### Your theme and your voice were not being saved
`rtSetDesign()` set the variable and toggled the class but **never persisted** — so
every launch dropped you back to Night whatever you had picked. Worse, nothing applied
the saved value on open either, so even once stored it was ignored until you actively
tapped a swatch.

**And the vocal range was not saved anywhere**, in Pitch Match *or* Road Trip. It reset
to tenor on every app launch. That is not a session preference; it is a fact about the
singer's body, and a bass or a soprano had to re-pick it every single time they opened
the app.

Both now persist and restore.

### "Lock it in" is not scaffolding
It skips the sing-and-hold step of the home phase and starts the drive. A reasonable
valve if the mic is misbehaving — though worth knowing it means recalling a note you
never actually established.

### Layout
`.rt-cz` had no flex growth, so it sat at its natural height and the module — and the
theme with it — stopped short of the bottom of the phone. It now fills and centres, so
the start button, the recall bar and the final passport sit in the middle of the space
rather than hugging the top of it.

## v0.81.32 — the splash skip never ran

App Links work: the link opens the app directly, no browser. But the splash still ran
its full three and a half seconds and the daily did not open — the two things the skip
was written to prevent.

**An ordering trap.** `_intonareSkipSplash` is defined inside the splash IIFE, ~700
lines below the deep-link handler that calls it. On a cold start the handler runs
first, so the function **does not exist yet**. The `typeof === 'function'` guard failed
quietly, and the code fell straight through to *waiting* for the splash — precisely the
behaviour the skip replaced. No error, no symptom except the feature not happening.

- The handler now **raises a flag** (`_intonareWantSkipSplash`) rather than calling a
  function. The splash reads it when it starts and skips itself. **A flag does not care
  who wrote it or when**, so there is no ordering dependency left to get wrong.
- The direct call is kept for the warm case, where the splash has already started.

## v0.81.31 — App Links and Universal Links: the link just opens the app

The bounce page can never open the app on Android without a tap. That is not a bug to
work around; it is Chrome's rule, and it applies to any page. **The way out is to have
no page at all.**

App Links (Android) and Universal Links (iOS) let the **OS** own the URL. It verifies
the domain against a file you publish, and from then on the https link is intercepted
before any browser sees it. No page, no script, and therefore no user-gesture rule.
Tap a shared result in a chat, the app opens on today's puzzle.

**This is why the shared link was https from the start.** Nothing about it changes;
the OS simply starts intercepting it.

### The pieces
- **`.well-known/assetlinks.json`** — names the package and the app-signing SHA-256
  (the Play-managed key, not the upload key; verifying against the upload key fails
  silently on every real install).
- **`.well-known/apple-app-site-association`** — no file extension, which is required
  — names `HAS2KCH36U.com.lieutenantdan.intonare` and the `/Intonare/go.html*` path.
- **Manifest** — a second intent-filter with `android:autoVerify="true"` for the https
  host. The custom-scheme filter stays as a fallback.
- **CI** — writes the Associated Domains entitlement.
- **The handler learned to read https.** App Links deliver the *https* URL, not
  `intonare://`. The regex only matched the custom scheme, so a verified App Link
  would have arrived and been **silently ignored** — the feature would have looked
  like it simply did not work.

### go.html does not go away
It is what people **without** the app get: the store, and an honest explanation. The
OS only intercepts the URL for devices where the app is installed and verified;
everyone else still lands on the page. One link, both audiences.

### Two things must be done by hand
1. **A second GitHub repo, named exactly `LieutenantDan76.github.io`**, holding only
   the `.well-known/` folder. The verification files must be served from the **domain
   root** — `lieutenantdan76.github.io/.well-known/…` — and a *project* Pages site
   (which is what `Intonare` is) can only serve under `/Intonare/`. The root file
   authorises the app for the whole domain, so the links themselves do not move.
2. **Apple Developer portal → Identifiers → com.lieutenantdan.intonare → tick
   Associated Domains.** Without it the capability is absent from the provisioning
   profile and the iOS build fails to sign.

## v0.81.30 — the splash was running at half speed, and it was my fault

### dt60 normalised to the wrong reference
`wavePhase += _spd * dt60`, where `dt60 = dtMs / 16.667` — a **60 fps** reference.
That is the obvious choice and it was wrong.

The original code was `wavePhase += _spd`, frame-coupled, with `_spd` tuned **by eye
on a 120 Hz Android**. So the speed the wave was actually designed at is
~116 × `_spd` per second, not 60 × `_spd`. Normalising to 60 did not preserve the
design — **it halved it, everywhere.**

- **iOS has been running the splash at half speed since v0.81.13.** That is the real
  reason it "looked weird" there, and it is why three rounds of theorising about
  stepping and DPR and frame caps never landed: the wave was not stepping oddly, it
  was crawling.
- **Android inherited the same slowdown the moment it was next built** — it had been
  on v0.81.2, from before `dt60` existed.

Fixed by normalising to the frame time it was tuned at (~8.62 ms) rather than to 60
fps. Frame-independence is kept; the speed is the one the wave was designed with, and
it is now identical on 60 Hz and 120 Hz alike.

### Chart samples: the fix hooked the wrong function
v0.81.27 warmed the instrument's samples when the charts tool opened — except it
hooked the **navigation wrapper**, which only the deep-link and open-with-preset paths
go through. **The actual card button calls `enterTool()` directly** and sailed straight
past it. So the tool still opened on guitar with nothing loaded and played the synth
fallback until you switched instrument and back — exactly the bug it was meant to fix.

Moved into `enterTool()`, which is the path everything uses.

### The whip never reached Android — `go.bat` skipped it
The Adventurer's fanfare played with no crack. The app code was fine; the file simply
was not there.

`go.bat` step 4g copies the audio assets with:

    for /D %%i in (audio_assets\*) do ...

**`for /D` iterates directories only.** Every sample set is a folder — `grand_piano\`,
`violin\` — so this worked perfectly, right up until the first *loose file* landed in
`audio_assets\`. `intonare_whip.mp3` sits at the root, so the loop stepped straight
over it and it never reached the Android assets. iOS was unaffected: Codemagic does
`cp -r audio_assets/*`, which takes files as well as folders. A platform-specific
absence with no error anywhere.

- **`go.bat` now copies loose files too**, every run rather than "if not exist" — a
  replaced file has to actually make it across.
- The diagnostics panel also reports the sample's state now (**READY** with duration,
  **loading**, or **NOT LOADED** with the specific HTTP/decode/network failure), so
  the next audio-file mystery is one screenshot rather than three theories.

### And `go.bat` does not build the APK
Worth stating plainly, because it is how a fixed native feature looks broken: the
script preps everything and then says "hit Run in Android Studio". **Native changes —
the manifest, the .java files — only reach the phone through that Run.** Testing
against the APK already installed gives you the new web code with the old native
behaviour, which reads as a half-broken feature rather than an unbuilt one. The
script's closing message now says so.

## v0.81.29 — deep links actually land

Two bugs, one per platform, both of which made the link look like it did nothing.

### iOS: the module opened behind the splash — and the splash is now skipped
The app opened, but on the home screen rather than the shared module. The handler
waited a fixed 400 ms and then called `enterExercise()` — but on a cold start the
splash owns the screen for about **three and a half seconds**, and its own handoff to
the home screen then wiped out the module that had quietly opened behind it.

Waiting for the splash fixes that, and leaves a toll: three and a half seconds of
branding on **every** shared link, paid by someone who tapped it specifically to see a
puzzle. **The splash is for people opening the app; it is an obstacle for people
opening a link.**

- The deep-link handler now **skips the splash** outright. It calls the splash's own
  `removeSplash()` — not a bare element delete — because that function also performs
  the iOS first-gesture audio unlock and starts sample preloading, and any other
  teardown would silently skip both.
- `getLaunchUrl()` is async and has not resolved when the splash starts, so the
  splash does begin: it is cut off a frame or two in rather than never started. A
  brief flash of the first frame, which beats delaying every launch to wait on a
  plugin call that usually comes back empty.
- If the skip is somehow unavailable, it falls back to **waiting** for the new
  `intonare:splash-done` event rather than opening the module behind the splash.

### And they land on the daily, not the module's front door
Opening the module was not what the link promised. Someone tapping a shared Chordle
result tapped a link **about today's puzzle**; dropping them on a difficulty picker
makes them go and find it themselves.

Each daily already had a proper stateful entry point, and they behave correctly for
someone arriving from a link:

| | |
|---|---|
| already played today | shows the result |
| mid-game | resumes where they left off |
| fresh | starts today's puzzle |

`chordleStartDaily`, `tonaleStartDaily`, `diadleStartDaily`, and — for Music Quiz —
`mqOpenDailyPopup`, which shows its "play the daily?" card rather than launching
straight in. That is its own established behaviour and is left alone.

### All three dailies now count you in
Chordle and Diadle fired their progression **350 ms after entry**. Fine if you had
deliberately tapped "Daily" and were braced for it. Startling if you had just arrived
from a chat, phone still face-down, no idea yet which app you were looking at.

The first instinct was to suppress the auto-play for deep-link arrivals only. That is
a patch, and it leaves someone staring at a puzzle wondering what to do next.

**Tónale already had the right answer** and has had all along — `tonaleReadyIntro()`:
a brief **READY? → 3 → 2 → 1** before the first tone, with a haptic tick on each
digit. So Chordle and Diadle now do exactly the same thing.

- One shared `intonareReadyCountdown()`, used by both.
- The count runs **in the play button** — no new markup, no layout shift, and it is
  where the eye already is.
- Abandons cleanly if the player backs out mid-count.
- Identical behaviour whether you tapped "Daily" yourself or arrived from a shared
  link. **The entry path no longer changes what happens.**

The deep-link special case is gone; it is not needed when the behaviour is right for
everyone. (`READY?` / `PRONTO?` already existed in both languages.)

**Where the count shows:** the first version ran it inside the play button — 13 px of
text in a 56 px control, unreadable. It is now a **module overlay**: the game dims
(55% + blur), and the count sits front and centre at 56 px with Tonale's scale-pop on
each digit and a haptic tick. Covering the controls also says "not yet" more clearly
than any wording could. Mounted in the module's own root (`#exChordle` / `#exDiadle`),
so the app header stays live — backing out mid-count bails cleanly.

**Scope, deliberately narrow:** the countdown fires on a **fresh daily start only**.
Replays are user-initiated (they pressed the button; they are ready), resume means
they know what they are doing, and free play has never auto-played. Only the fresh
daily fires audio at someone, so only the fresh daily counts them in.

Review also caught the overlay's digits using `inherit` inside the `font` shorthand —
invalid CSS, silently dropped wholesale, which would have cost the weight and
line-height. Set as individual properties instead.

### Android needs a tap, and that is the rule — not a workaround
The page fired the app launch automatically on load. **Chrome blocks that, by design:**

> "Chrome won't launch an external app for a given Intent URI if the Intent URI is
> initiated without user gesture." — *Chrome for Developers*

and Chromium's own `external_intents` documentation lists *"launching an app without
user activation"* among the things it refuses outright.

The tap that opened the link was consumed by the navigation to the page. The page's
own script has no user activation left, so an automatic `intent://` fires into a wall
— **every time**, regardless of the manifest, the build, or anything else. (The
earlier iframe version failed for exactly the same reason, one layer down. Two
attempts, one root cause.)

Chrome's guidance is explicit: *"Construct an intent anchor and embed it within a
page, so the user can choose to launch the app."*

- **On Android the page is now the button.** A real `<a href="intent://…">` anchor,
  tapped by a human. No timers, no guessing whether it worked.
- The intent carries `browser_fallback_url`, so **Chrome sends people without the app
  to the Play listing itself** — one tap covers both cases.
- **iOS keeps the automatic path**, because navigating to a custom scheme from script
  does work there and the app opens immediately.

### Android: the earlier iframe attempt
The bounce page tried to launch the app by pointing a hidden iframe at
`intonare://…`. **Chrome has blocked custom-scheme navigation from iframes for
years**, as a security measure. So nothing happened, the fallback timer ran, and the
page showed the stores — to someone who had the app installed.

- Replaced with an **`intent://` URL**, which is Android's own supported mechanism:
  it names the scheme, the package, and a browser fallback, and Chrome makes the
  decision itself.
- The fallback screen also gets a manual **"Open in Intonare"** button, and no longer
  claims the app is missing — the navigation may simply have been blocked (in-app
  browsers do this too), and a tap always works.

## v0.81.28 — deep links: shared dailies open the app

Chordle, Tonale and Diadle results ended with the bare word "intonare". They now end
with a link that actually goes somewhere.

### Why an https link and not `intonare://`
A custom scheme in a message sent to someone **who does not have the app** does
nothing at all. It is dead text, and it makes the app look broken to precisely the
person you were hoping to reach.

So the shared link is https, pointing at a small bounce page:

    .../Intonare/go.html?m=chordle

The page tries `intonare://chordle`. If the app is installed the OS intercepts it and
they land in the right module. If not, the navigation quietly fails, a timer fires,
and they get the store instead.

**All four dailies** carry it: Chordle, Tonale, Diadle, and Music Quiz. (Music Quiz
was nearly missed — it is the fourth share in the app and it opens via its own
`mqOpen()` rather than `enterExercise()`, so the handler special-cases it.)

### The pieces
- **iOS** — `CFBundleURLTypes` written into Info.plist by CI.
- **Android** — a `VIEW` / `BROWSABLE` intent-filter in the manifest. `launchMode`
  was already `singleTop`, so a link arriving while the app is open goes to
  `onNewIntent` rather than starting a second activity.
- **JS** — handles **both** arrival paths: `getLaunchUrl()` for a cold start, and the
  `appUrlOpen` event for an app already running. Handle only one and half your links
  silently do nothing.
- **The page** — detects the platform, leads with the right store, and is honest
  about the ones that are not live yet rather than showing a dead button.

### And this is the foundation for Universal Links, not a detour from them
Universal Links (iOS) and App Links (Android) need an Apple Team ID and the release
keystore's SHA-256, published in verification files served from the domain — none of
which exist until the app is actually on the stores. But **the shared URL is https
either way.** Adding them later changes nothing about the app, this code, or any link
already sent; the OS simply begins intercepting the URL directly instead of routing
through the page.

The store links live on the page, not in the app, so they can be filled in the moment
each store goes live — without an app update, and without breaking links already
shared.

## v0.81.27 — Adventurer sound settled; chart samples; Pitch Match listens properly

### The Adventurer's sound
Settled on the brass fanfare with the real whip cracking just past the arrival note.
The five other variants and the on-device picker are gone — they were scaffolding.

**On how close the homage gets:** copyright protects the MELODY, and it follows that
melody through transposition. So this does not use the Raiders figure. The leap is a
perfect **fourth**, not the original's minor third, and that is the distinction doing
the legal work. What it borrows is style — brass, march-rhythm pickup, a heroic leap
— which is not protectable. Everyone hears "adventure"; nobody is quoting.

The whip is a real recording, played at 0.42 against the brass (0.9 buried the very
thing it was meant to punctuate).

### Chart notes played the synth voice on the first visit
`_chartPlay()` checks `SampleEngine.isReady()` and falls back to the synth if not —
but it never *triggers* a load. The eager loader lived inside
`switchChordScaleInstrument()`, which only runs when you actively pick an instrument
from the sheet. **Open the charts tool normally and it inherits the default
instrument without ever calling it.** So the samples were never requested and every
note came out synthesised, until you happened to switch instrument and switch back.

- The loader is now callable on its own and runs **on tool open** as well as on
  switch. First note you tap is the real instrument.
- Kept its original name (`_loadInstSamples`) because the regression sentinel pins
  it; renaming would have quietly retired a guard for no benefit.

### Pitch Match was listening to itself
The reference tone played for 0.5 s **with the mic live and detection running**. The
reference is a clean sustained tone — precisely what the detector is best at — so it
would lock onto the app's own speaker and report a perfect match before the singer
had made a sound.

- **Detection is suppressed while the reference sounds**, and for a short tail after.
- **Reference is now 1.0 s**, up from 0.5. Half a second is enough to identify a
  pitch and not enough to internalise one.
- "your turn" appears when it starts listening. EN + IT.
- `ssStop()` clears the flag and its timer — without that, stopping a round *while*
  the reference was sounding would have left the detector permanently deaf.

### Not done, deliberately
- **Splash at 120 fps** — impossible in a WebView. Apple caps `requestAnimationFrame`
  at 60 inside WKWebView by design; there is no public API, and the private one is an
  App Store rejection. The only legitimate route is rebuilding the splash as
  GPU-composited CSS, which cannot preserve the particle gather and burst. Not worth
  losing the animation to gain frames on one platform. The plist key from v0.81.22 is
  removed; it did nothing.
- **Deep links for daily shares** — needs a URL scheme on both platforms, an
  `appUrlOpen` handler, and a web landing page to catch people without the app
  installed. Half-done deep links are worse than none. Its own piece of work.

## v0.81.25 — a real whip

Variant E's crack was synthesised from filtered noise. It read as **static, not
leather** — a whip's transient has a very specific shape that a noise burst cannot
fake.

Replaced with a real recording (Pixabay: free for commercial use, **no attribution
required**, modification permitted). Trimmed to the transient, normalised, mono,
96 kbps: **13 KB**. The sample keeps the authentic two-part gesture — the swish of
the wind-up at ~60 ms, then the crack peaking at ~250 ms — with the dead air before
it cut so the sound is instant.

- Played **dry**, straight to the destination: the crack wants no reverb, and the
  brass that answers it already has a tail.
- Loaded by **XHR, not fetch** — the same reason the piano samples need it. On iOS,
  Capacitor serves `www/` from `capacitor://localhost`, and `fetch()` against a
  custom scheme returns status 0. XHR goes through WKWebView's ordinary
  resource-loading path and reads it. (Local-scheme XHR reports status 0 *on
  success*, so the test is "did we get bytes".)
- **Warmed on the first user gesture**, alongside the piano. This matters more than
  it looks: the achievement fires **once**, at a moment that matters, and a buffer
  still loading would have dropped the crack and played brass only — silently, and
  exactly once, on the one occasion anyone would notice. Lazy-loading was not good
  enough here.
- Also preloaded when the diagnostics panel opens, so E cracks on its first tap.
- And if it is *still* not ready when the fanfare fires, the load is kicked off and
  the crack fires **as soon as it lands** (up to 1.5 s) rather than being dropped.
  Late beats absent. The brass runs regardless, so the fanfare is never silent.

Covers every path: the unlock itself, the achievement cue afterwards, the picker,
and a cold start where the sample has not been touched.

## v0.81.24 — four achievement quotes, and six Adventurer sounds to choose from

### Quotes
Four descriptions were generic self-help — "You know what you're doing now" says
nothing. The good ones in this app are twisted pop-culture misquotes; these now match.

| | |
|---|---|
| **Chord Scholar** | "Chords are words, and now you're learning to read" |
| **Practitioner** | "Wax on, wax off" |
| **Musician** | "I pledge allegiance, to the band" |
| **The Adventurer** | "You chose... wisely" |

EN and IT twins. The Italian for Karate Kid is the actual dub line — *"dai la cera,
togli la cera"* — which is the version Italians know.

### Six Adventurer sounds, pickable on-device
**On the copyright line:** music copyright protects the *melody* — the specific
sequence of pitches and rhythms. It does **not** protect intervals, instrumentation,
key, tempo, or style. Nobody owns "brass playing a rising fourth."

So none of these quote the Raiders March. What they borrow is the **gesture**
everyone actually recognises: a march-rhythm pickup, then a heroic leap up a perfect
**fourth**, played brassy and loud. That shape is the fingerprint of adventure
scoring generally and long predates the film. After the leap, every variant goes
somewhere the original does not.

| | |
|---|---|
| **A · fanfare** | Triplet pickup, the fourth, then away upward. Bright, mid-register. |
| **B · horns** | Same gesture an octave down, slower, fatter. Less fanfare, more swagger. |
| **C · march** | Pickup, the fourth, then a full answering phrase. The most tune-like. |
| **D · single** | No pickup. Just the leap, once, with weight under it. Confident, not showy. |
| **E · whip** | A snapped noise transient, then the fourth answers it. The effect and the theme arriving together. |
| **F · discovery** | The quiet one. A held open fifth, the fourth rising out of it. Finding the thing, not escaping with it. |

**Diagnostics panel → ADVENTURER SOUND.** Tap to hear each, back to back, no rebuild.
Whichever wins becomes `playAdventurerChime` and the other five get deleted.

## v0.81.23 — The Adventurer is a real achievement; Clair de Lune's famous bit

### The Adventurer rendered as a blank slot
Because it was not an achievement. It was a `localStorage` key with its own bespoke
toast, bolted onto the side of the system: no entry in `ACHIEVEMENTS`, no icon, no
rarity, no `check()` predicate. The achievements list renders **from** `ACHIEVEMENTS`
— so it drew an empty slot, exactly as it should have.

- Now a real secret achievement: proper entry, `check: s => !!s.rt_parchment_done`,
  a **compass-rose icon**, secret rarity, the standard toast with its ring burst.
- Finishing a parchment trip records the fact in `progState`; the normal engine does
  the rest.
- The old `localStorage` flag is **migrated**, so anyone who already earned it keeps
  it.

### It has its own sound now, and it is an Indiana Jones homage
Not a quote — the Raiders March is under copyright and this reproduces none of it.
What it borrows is the **gesture** everyone recognises: a triplet pickup, then a bold
leap up a **perfect fourth**, brass and swaggering. That interval-and-rhythm shape is
the fingerprint of adventure scoring generally and long predates the film. Voiced
with stacked saw + square for brass edge, a low fifth under the landing so the fourth
reads as an arrival, and a short convolved tail so it lands like a fanfare.

**And it unlocks as a selectable achievement cue** — "Adventurer", alongside "Secret
Found" and "Beethoven's Fifth", hidden until earned, using the same lock pattern as
the others. EN + IT.

### Clair de Lune was not broken; you were waiting for bar 27
The transcription is correct and complete — 93 beats, opening thirds through to the
main theme. The tune everyone knows is the *un poco mosso*, where the left hand
breaks from held chords into rolling quavers. Measured: that happens at **beat 65**,
which at 46 bpm is **~85 seconds** of quiet parallel thirds first.

Correct, authentic, and nobody waits that long. (Road Trip already knew: its entry
for the piece carries `hook:4` — "past the hushed open into the phrase.")

- **`clair_de_lune_famous`** — "Clair de Lune (main theme)". The same notes from beat
  65, rebased to start at beat 1: 43 RH, 43 LH, about 38 seconds of the passage the
  piece is actually famous for. Pedal down from the first note.
- The complete movement stays as `clair_de_lune`. **Both ship; keep whichever sounds
  right and the other can go.**

## v0.81.22 — the splash: iOS was rendering at half Android's frame rate

Same version on both phones, panels side by side, and the numbers ended four
theories at once:

|            | iPhone | Android |
|------------|--------|---------|
| splash fps | 59.2   | **116.3** |
| frames     | 231    | **454** |
| phase      | 26.82  | 26.74   |

**Identical total travel. Half the frames.** iOS advanced the wave in ~0.23 rad
steps where Android used ~0.09. Not slower — **coarser**. A coarsely-stepped
travelling wave reads to the eye as sluggish and lifeless, which is exactly what
"the iPhone wave just expands then dies out" describes.

And iOS was not struggling: 59.2 fps is a clean, capped 60. **WKWebView caps
`requestAnimationFrame` at 60 fps even on a 120 Hz ProMotion display** unless the
app opts in — Apple's default, so that apps written for 60 are not silently handed
a doubled frame budget. The iPhone had the same 120 Hz panel as the Android and was
using half of it.

### Fixed
- **`CADisableMinimumFrameDurationOnPhone`** added to Info.plist by CI. iOS now
  renders at the display's real rate.

### Why this is safe
120 Hz doubles the frame count, so any animation advancing by a **fixed amount per
frame** would run at double speed. Swept every `requestAnimationFrame` loop in the
file — **106 of them** — for that pattern: all are either time-based
(`performance.now()`, `ctx.currentTime`) or do not accumulate a fixed step. **Zero
at risk.**

The splash was the sole exception, and it was already normalised in v0.81.13 by
`dt60`. That fix was written under a wrong theory and dismissed as pointless when
the frame rate came back healthy. It turns out to be the thing that makes *this*
fix possible: without it, unlocking 120 Hz would have doubled the wave's speed.

### For the record, the theories this killed
Frame-rate scaling (v0.81.13 — right fix, wrong reason), canvas DPR (the geometry
is normalised; the wave spans 2.2 cycles of the width on any device), and the easing
curves (all clock-driven). Each was plausible and each was wrong. **The panel
measured its way to the answer**; none of the four rounds of reasoning got there.

## v0.81.21 — full review: mic-stop no longer kills live audio; two diagnoses corrected

A top-to-bottom read of the master-volume system and the iOS session handling,
prompted by the last builds' fixes wounding adjacent code. One real fix, two
corrections of the record, one theory formally killed.

### Fixed: turning the mic off stopped the metronome dead
The mic-stop path switched the session back to `.playback` immediately. That
switch rebuilds WebKit's audio output; everything scheduled ahead of "now" is
dropped, and the metronome — which schedules clicks ahead on a 25 ms interval —
lost its queue and died. A sustained drone glitched the same way.

The switch is only about **volume**, and a slightly-quieter metronome that keeps
playing beats a full-volume one that died. So it is now **deferred while audio is
busy**: if the metronome is running or any ref tone / drone is sounding, the
mic-stop marks the release as pending, and it fires the moment the coast is clear
— `stopMetro()`, the last `stopRef()`, and every natural-expiry timeout all flush
it. The panel shows `playback DEFERRED (audio busy)` when this happens.

Enabling the mic mid-playback still stutters briefly. That one is WebKit's own
`getUserMedia` reconfiguration, recording genuinely requires it, and it is not
ours to prevent. Likewise the short wait after mic-off before starting new audio:
that is the route change itself settling, and deferral cannot help when nothing
was playing to defer for.

### Correction: the makeup-gain loop was never missing
The previous diagnosis — "`setMasterVolume` computes `makeup` and never applies
it" — was wrong. The `_masterMakeupRegistry.forEach` is present and correct; the
diagnosis came from a read window that stopped one screen short of it. No fix was
needed, and none was applied.

### Which means: "slightly louder at 200%" is the system working
With the loop confirmed present, the on-device result is the honest output of the
design. The arithmetic for a metronome click: its peak rides ~-6 dBFS at 100%; at
200% the gain cap, compression and makeup net out to roughly **+4 dB of peak** —
audible, not dramatic. A click is a sparse transient: there are no quiet parts
*within it* to pull up, so loudness processing (which raises average energy) buys
little beyond the peak gain. Sustained material — chords, drones, samples — gets
substantially more from the same curve.

The remaining lever for percussive material is saturation (soft-clipping adds
harmonics the ear reads as loudness). That is new audio design, it colours the
click, and it is not shipping uninvited. Pinned as an option.

### The splash: renderer proven identical; the comparison itself is suspect
The wave geometry is normalized — `sin(u · 2.2 · 2π + phase)` where `u` spans the
width — so the wave has 2.2 cycles across the screen on **any** device, and the
canvas is DPR-corrected (`setTransform(dpr,…)`). Resolution cannot change its
apparent speed; the DPR theory is dead alongside the frame-rate theory. The
measured travel (26.82 rad ≈ 1.9 screen-widths at 59.2 fps) is healthy.

What remains: **the Android being compared against has not been rebuilt since
v0.81.2** — every push since has been iOS-only. If the splash was touched in any
intervening version, the two phones are running different animations. Verdict:
re-compare after the next `go.bat`, same version on both, panel numbers side by
side. If the numbers match and it still looks different, it is display physics,
not code.

## v0.81.20 — the metronome fader, the emoji triangle (properly), and slow mic release

### The master fader did nothing for the metronome
Because pocket mode was throwing it away:

    metroMasterGain.gain.setTargetAtTime(on ? 1 : 0, ...)

Un-muting set the gain to a **hardcoded 1**, wiping out whatever the master fader had
put there. Every pocket-mode toggle silently reset the metronome to unity, which is
why the slider appeared to work everywhere except the one place being tested.

- Unmute now restores the level the fader actually asks for, read from the gain
  registry rather than restating the number and letting the two drift apart.
- `setMasterVolume` now respects pocket mode: moving the fader while the metronome
  is muted no longer un-mutes it.

The metronome runs through `buildLimiterChain`, so with this fixed it gets the full
loudness curve — 4.2× makeup gain at 200%.

### The emoji triangle, actually fixed
v0.81.15 used `font-variant-emoji: text`. **Safari only honours that from 17.4**, so
on anything older it does nothing at all — which is what happened.

The fix that works everywhere is the **variation selector**: appending U+FE0E to the
character explicitly requests text presentation, and has been honoured for decades.
Applied to all **184** occurrences of U+25B6. The CSS property stays as a
belt-and-braces, plus a font stack that has the glyph but no emoji table.

### Mic release was slow
Disabling the mic left the app quiet unless you waited a moment.

`stopMic()` asked iOS to switch to `.playback` **before** stopping the microphone
track. iOS does not release the record path until the track actually stops, so the
category change was fighting a live capture. Waiting "fixed" it, which was the clue.

Moved: the session change now happens after `track.stop()`, when the capture is
genuinely gone.

### Deliberately not changed
The four hand-rolled limiters (Road Trip, rhythm cards, rhythm reader) stay at their
tuned **-6 dB / 20:1 / hard knee** and stay OUT of the loudness curve. The regression
sentinel pins the rhythm reader's value explicitly — someone tuned that and locked
it. They will not get louder above 100%; that is a decision already made, and this
build does not overturn it.

## v0.81.19 — hotfix: the splash diagnostic killed the splash

    Uncaught ReferenceError: Cannot access '_spd' before initialization

The wave-travel measurement added in v0.81.15 read `_spd` twenty-three lines above
where `_spd` is declared. `const` in a temporal dead zone throws on access, so the
splash loop died on its first frame.

Moved below the declaration. The splash-loop scope is now verified clean of any
read-before-declare.

**Both ship gates missed it.** `node --check` passes — a TDZ violation is a *runtime*
error, not a syntax error — and the sentinel does not model scope. Same class as the
`_PITCH_HIST_N` deletion in v0.81.13: code introduced that references something not
present at that point. The discipline that catches it is manual and simple: **when
inserting code that reads a variable, confirm the variable exists there.** Both of
tonight's incidents would have been caught by that one check.

## v0.81.18 — duplicate notifications

More than one of each reminder per day. Not a cadence choice; a bug.

The reminders were scheduled with:

    schedule: { at, repeats: true, every: 'day' }

The Capacitor docs are explicit about this: **"Use EITHER `at`, `on`, or `every` to
schedule notifications."** Passing `at` — a concrete datetime — alongside
`every: 'day'` — an interval — can register **both**, and you get two notifications.

### Fixed
- Both reminders now use **`on`**, the calendar matcher: `{ hour: 19, minute: 0 }`
  means "at 19:00, every day" by definition. Nothing to repeat, nothing to double
  up.
- This also removes the need to roll the date forward to tomorrow when the chosen
  time has already passed today — which `_notifTimeToDate` had to do, and which was
  its own route to a stale pending notification sitting alongside the new one.
- `allowWhileIdle: true` so the reminder still fires if the device is in Doze.

The cancel-then-schedule logic and the fixed IDs were already correct; the schedule
object was the whole problem.

## v0.81.17 — no way to repeat a wind note; Settings would not scroll in the guide

### Wind instruments had no way to repeat a note
Selecting a note on a wind instrument (trumpet, flute, clarinet, the rest) plays it
— but there was no way to hear it **again** without navigating away and back.
Fretted instruments can just re-tap a dot on the diagram; wind instruments have no
diagram, so once the note had sounded, that was that.

- **PLAY NOTE button** on the wind note card, replaying whichever note is showing.
  `gccPlayString()` already knew how to voice a wind instrument — it stops the
  previous note and uses `windSynth` — so this is only about giving that a button.
  EN and IT twins.

### Settings would not scroll inside the Survival Guide
Open the app's Settings while the Survival Guide is up, and the modal would not
scroll on iOS.

The guide's container is a full-viewport flex column with `overflow:hidden` and a
fixed height — it owns the entire screen while open. That starves the fixed-position
modal layered above it of touch scrolling: the gesture is swallowed by the guide's
non-scrolling box before the modal ever sees it. (Not a nesting or clipping problem
— the modal is a top-level sibling with its own `overflow-y:auto`. The guide was
simply competing for the touch and winning.)

- `body.settings-open` takes the guide out of the layout while Settings is up. It is
  behind a full-screen blurred overlay anyway, so there is nothing to see.

**Checked: it is the only module with this shape.** Every other `overflow:hidden` in
the file is a small inner element — a progress bar, a dropdown panel, a photo frame —
none of which own the viewport or can swallow the modal's touch. The guard is listed
by id rather than by a class, deliberately, so that if a future full-screen module
needs it, adding it is a conscious decision rather than something inherited by
accident.

## v0.81.16 — audio leaked out of modules through whichever gap you left by

Backing out of a tool or an exercise could leave its sound still playing.

Both exits stopped audio via a **hand-maintained list**: `exitTool()` had one line
per tool, `exitExercise()` had one line per exercise. And `stopAllAudio()` — which
already existed, already ran on backgrounding and pagehide, and was supposed to be
the complete list — was called by neither.

All three lists had drifted apart. `exitExercise()` knew about `diadleStop`,
`tonaleStop` and `roadtripStop`; `stopAllAudio()` did not. `exitTool()` knew about
`thmnStop`, `rcStop` and `ivrStop`; `stopAllAudio()` did not. Three lists, each with
holes the others filled, and sound leaking through whichever gap you happened to
walk out of.

### Fixed
- **`stopAllAudio()` completed** — all 30 stop functions, grouped and verified to
  exist. It is now genuinely the single source of truth for "make it quiet".
- **Both exits call it.** The per-module stops stay, because several also reset UI
  state (closing panels, clearing active notes) and are not redundant. This is the
  audio safety net underneath them, so nothing can leak because a module was
  forgotten on a list.

## v0.81.15 — metronome one-tap-and-stop, and the emoji triangle

### The metronome fired once and died
Toggling the mic and then starting the metronome would produce a single click and
stop; you had to start/stop again to get it going.

`startMetro()` and `playRef()` were both calling `_iosSyncAudioMode()` — a leftover
from the theory that a new audio source started while the mic is live can be
re-ducked and needs a nudge. But **changing the audio session category while the
metronome is spinning up disrupts the graph mid-schedule.** The click fires once and
the scheduler is left in pieces.

The session only ever needs changing when the **mic state** changes, and those
transitions already call it. By the time any audio starts, the session is already
correct — so both calls were pure downside. Removed. Three call sites remain: first
audio, mic start, mic stop.

### The start button had an emoji triangle
`▶` (U+25B6) appears in 164 buttons. **iOS renders it as a colour emoji; Android
renders it as a plain text glyph.** Same character, completely different button.

Fixed in CSS rather than editing 164 strings: `font-variant-emoji: text` asks for
the text presentation explicitly.

### Splash: the frame-rate theory is dead
The panel measured **58.7 fps**. It is not a frame-rate problem, so the `dt60`
normalisation from v0.81.13 — while correct, and worth keeping for future 120 Hz
devices — was not the fix.

"The iPhone wave just expands then dies out" says the horizontal *travel* is not
happening at all, which is a different bug from "slow". The panel now reports the
wave's **total accumulated phase** (which is literally the travel) and the device
pixel ratio. Compare the number against Android and this becomes arithmetic instead
of a fourth theory.

## v0.81.14 — the launch-quiet was the cache, not the category

Three volume levels, not two: launch audio was quieter than **either** the normal
mic-on or mic-off level, and only a mic toggle knocked it loose. That rules out
`playAndRecord` attenuation — that would land you at the mic-on level, not below it.

The panel showed the mechanism:

    audioMode   playAndRecord (cached) · metro

**The cache is right in principle and wrong at startup.** The app auto-starts the
mic at launch (deliberately — it is a quick-access tuner, and having to enable it
every time would be worse). That fires a session change **before WKWebView has
built its audio engine**. So we configure a session nothing is attached to yet;
WebKit then comes up with its own defaults; and because native cached the state as
applied, no later call ever re-applies it. The audio sits in WebKit's own
configuration, quieter than anything we chose, until a mic toggle changes `micLive`
and happens to bypass the cache.

### Fixed
- `setAudioMode` now takes a **`force`** flag. JS passes it until the first apply
  that lands with a live `AudioContext`; after that the cache is trustworthy and
  rapid start/stop stays free.
- The auto-start stays. It is the right product call; it was just exposing a race
  with WebKit's engine setup.

### Added
- **Splash frame rate in the diagnostics panel.** "The splash feels slower on iOS"
  has now had three theories and zero measurements. The panel reports the actual
  fps and frame count, so the next round starts from a number rather than another
  guess.

## v0.81.13 — the volume race, and the splash was frame-rate coupled

### The splash animation had less travel on iOS
Not lag — the frames were smooth. The wave simply covered less horizontal ground.

Everything driven by `gatherEl` (the gather, the easing curves, the timing of every
beat) reads `performance.now()` and was already correct on any device. But the
wave's horizontal travel advanced by a **fixed amount per frame**:

    wavePhase += _spd;

which makes its speed directly proportional to frame rate. Every constant was tuned
by eye on Android; on a device rendering at a different rate the wave covers less
distance per second and the whole thing reads as sluggish **without ever dropping a
frame**. Which is exactly what it looked like. The colour, glow and pulse eases had
the same bug, so on iOS the palette was also arriving out of step with the motion it
is meant to be lighting.

- Now normalised by `dt60` — how many 60 fps frames this frame actually took. **At a
  true 60 fps `dt60` is 1.0 and every constant behaves exactly as tuned**, so Android
  is unchanged; at 30 fps it is 2.0 and each frame advances twice as far, covering
  the same ground per second.
- Clamped to 3 frames, so a stall (backgrounded tab, GC pause) cannot produce one
  enormous jump and tear the wave.
- The frame clock resets when the animation starts, or a stale timestamp from a
  previous run would hand frame 1 an enormous `dt`.

### The volume race

"Sometimes it works, sometimes it takes a second, sometimes I have to hit the mic,
and start/stopping the metronome sometimes gets stuck." Unreproducible, because it
was a **race**.

Three call sites (first audio, mic start, mic stop) each fired an async bridge call
that set the audio session, with a one-second throttle on top and no sequencing
between them. Start and stop the metronome quickly and:

    call A fires  → sets .playback
    call B fires  → sets .playAndRecord   (before A has landed)
    A resolves    → .playback wins, wrongly, because it finished last
    throttle      → blocks the corrective call
    result        → stuck quiet until something else happened to nudge it

### Fixed
- **One method, one owner.** `assertAudioMode()` / `releaseAudioMode()` are gone,
  replaced by `setAudioMode(micLive:)`. JS reports what the app **is**; native
  decides what the session should therefore **be**.
- **Serialised natively.** All session work runs on a dedicated serial
  `DispatchQueue`, so two calls cannot interleave. Ordering is deterministic by
  construction rather than by timing.
- **Idempotent.** Native remembers the last state it applied; a redundant call —
  which rapid start/stop produces constantly — returns immediately and touches no
  hardware. **The throttle is gone**, because it is no longer needed: repeat calls
  are already free.
- On failure the remembered state is deliberately *not* updated, so the next call
  retries rather than assuming a state that was never reached.
- All five JS call sites now use the one function, with no guards (the call is free
  when nothing changed). The mic-start call was also **moved to after
  `isListening = true`** — it had been firing while the flag was still false, which
  asked for `.playback` at the exact moment the mic was coming up.

### Caught by the sentinel, not by me
The JS rework accidentally deleted `_PITCH_HIST_N`, `_pitchHist`, `_pitchSort` and
`_pitchHistIdx` — a slice-based edit whose end index overshot into the pitch-median
declarations sitting just past it. `node --check` passed cleanly, because a missing
`const` is a runtime `ReferenceError`, not a syntax error; the tuner would have
thrown on every detected pitch. The regression sentinel flagged the drifted pin.
Restored, verified, and a good argument for the ship gate existing.

## v0.81.12 — Italian permission prompt, and the launch sound on iOS

### The iOS launch sound
It never played on iOS, and it was never going to: the JS called
`window.IntonareNative` — the Android `@JavascriptInterface` bridge, which does not
exist on iOS. Absence by construction, and completely silent about it.

The obvious shortcut (just play it from Web Audio) is dead on arrival, and the
comment at the call site has said why all along: *"Native playback isn't
gesture-gated, so this keeps true autoplay while syncing exactly."* The splash
fires at cold launch, before any user gesture, and **WebKit will not autoplay Web
Audio without one**. Native or nothing.

- **`IntonarePlugin.playSplashSound()`** — `AVAudioPlayer`, holding a reference for
  the lifetime of playback (a local player is deallocated the instant the method
  returns, and you hear nothing; a classic, and a silent one).
- **The file ships in `www/audio/`**, which Capacitor copies into the bundle as
  `public/audio/`. That folder is *already* a registered Xcode resource — it is how
  the entire app loads — so the sound needs **no `project.pbxproj` surgery**, which
  matters because `cap add ios` regenerates the project file every build.
- **CI transcodes it.** The Android source is Vorbis (`.ogg`); iOS cannot decode
  Vorbis at all. Now converted to AAC alongside the original, with ffmpeg installed
  on the fly if the build image lacks it.
- JS falls through: Android bridge if present, else the iOS plugin.

### The Italian microphone prompt
The permission dialog was English-only, on an app whose primary market is Italy.

- `en.lproj` / `it.lproj` `InfoPlist.strings`, plus `CFBundleLocalizations` in the
  plist (without which iOS does not even look for a localized string and uses the
  plist value verbatim regardless of device language).
- Written by Python rather than shell, because the Italian needs a real **né** and
  typographic apostrophes, and pushing UTF-8 accents through bash quoting inside an
  indented YAML block is a fight not worth having. (An earlier pass wrote "ne" to
  dodge the escaping. Not shipping that.)

**One open bet.** Strictly, a `.lproj` must be registered in the Xcode project to
be copied into the bundle. The bet is that `cap add ios` registers the contents of
`App/App/`, so a `.lproj` dropped inside gets copied for free. **If the Italian
prompt does not appear on an Italian device, that bet was wrong** and the fix is a
pbxproj patch or an `InfoPlist.xcstrings` catalogue. Flagged rather than assumed.

## v0.81.11 — quiet until the mic was touched; and the fader's dead top half

Two separate volume bugs, both now fixed. Neither was iOS-only in cause, though
only one showed up on iOS.

### Fixed: the app was quiet until you touched the mic
v0.81.10 set `.playback` at launch, which is the right category — but **iOS does
not apply a category until the session is ACTIVE**, and it does not activate one
until something needs audio. WKWebView gets there first and activates the session
with *its* defaults. So the first sounds of a session played under WebKit's
config, not ours; only touching the mic ran the plugin and made it stick.

- Both plugin methods now call `setActive(true)`.
- `getAudio()` asserts the session when the shared AudioContext is first created —
  before the first note, rather than after the first mic tap.
- It asserts the category matching the **current mic state**: `releaseAudioMode()`
  (`.playback`) when the mic is off, `assertAudioMode()` (`.playAndRecord`) when
  it is live. Calling the latter unconditionally would have claimed the microphone
  for nothing and dragged the app back into the attenuated category it is trying
  to escape.

This is **not** the launch-time `setActive(true)` removed in v0.81.3. That one
claimed the audio hardware from app open, before any user action, for a session
nobody was using. This runs on demand, after a gesture.

### Fixed: the master fader's top half did nothing
At 100% a typical chain computes `0.8 × 0.9 = 0.72`, and the limiter threshold is
`-3 dB` (≈0.708) — the signal **sits on the threshold at normal volume**. That is
where it should sit; it is what all the clipping and chord-pumping work converged
on, and it is not being touched.

But it means the fader's upper half was dead. At 200% the gain becomes 1.44 —
about 6 dB over the threshold, into a 20:1 ratio. The limiter handed back roughly
**a third of a decibel**. The fader raised the gain and the limiter immediately
took it away, so "louder" only ever meant "more compressed".

- **Above 100%, the limiter ceiling now rises with the gain**
  (`threshold = -3 + 20·log₁₀(scale)`, capped at 0 dBFS), so the added gain passes
  instead of being squashed.
- **At and below 100% the threshold is exactly the -3 dB it has always been.**
  Identical maths, identical sound, none of the existing tuning disturbed. Only
  the currently-dead range changes.
- Limiters are now registered alongside their gain nodes, because chains are
  cached and reused — without this, a limiter built at 100% would keep its old
  ceiling forever and the fader would move the gain into a fixed wall.

### And then: gain alone cannot reach 200%
Raising the ceiling helped, but exposed the real wall. **Digital audio stops at
1.0.** At 100% a chain sits at 0.72; a gain of 1.0 — reached around **139%** — is
the format's hard maximum. 200% asks for 1.44, which is 44% more than exists. No
threshold, no fader, no code can produce it; ask anyway and the peaks get sliced
flat, which the ear hears as buzz rather than volume.

So above 100%, the compressor **morphs from limiter into loudness processor.**

The ear judges loudness by *average* energy, not peak. A signal that touches 1.0
once and sits at 0.2 sounds quiet; one that never exceeds 0.9 but *lives* at 0.7
sounds far louder. So rather than push the peaks up (impossible), pull the quiet
parts up: compress harder, then make up the gain. Average level climbs toward the
ceiling without crossing it. This is what mastering does, and it is why modern
records sound loud on phone speakers.

| fader | gain | threshold | ratio | makeup | |
|---|---|---|---|---|---|
| **≤100%** | 0.72 | **-3 dB** | **20:1** | **1.00×** | **pure limiter — untouched** |
| 120% | 0.86 | -6 dB | 16.8:1 | 1.71× | loudness 19% |
| 139% | **1.00** | -8.8 dB | 13.8:1 | 2.29× | gain hits full scale |
| 175% | 1.00 | -14.2 dB | 8:1 | 3.74× | loudness 75% |
| 200% | 1.00 | **-18 dB** | **4:1** | **4.22×** | full loudness mode |

**At and below 100% the chain is electrically identical to what it always was.**
Same gain, same threshold, same ratio, unity makeup. Every hour of clipping and
chord-pumping work is untouched, and anyone who never moves the fader never
encounters any of this.

The price above 100% is dynamic range: a piano's decay flattens, attack and tail
move closer. For a metronome click that is ideal. For a sampled instrument you are
listening to musically, it costs life. **The user chooses** — which is the point.

All sixteen manually-created master gains (drums, theremin, Road Trip) were also
switched to the capped scale, so they cannot be driven past full scale either.

### Known gap
Five hand-rolled limiter chains (Road Trip, drum kit) build their own compressors
outside `buildLimiterChain` and connect straight to the destination. Their gains
are now capped so they will not clip, but they receive **no loudness processing** —
at 200% they will be full-scale-but-not-louder while the main surfaces get the
boost. Scoped follow-up, not a mystery.

## v0.81.10 — black screen: the storyboard needs the module

v0.81.9 built green and launched to a **black screen**. Nothing loaded.

`Main.storyboard` names the root view controller by class. The patcher swapped
`CAPBridgeViewController` for `IntonareViewController` — and **stripped the
`customModule` / `customModuleProvider` attributes** along with it, on the theory
that a class in the app target needs no module qualifier.

Wrong. UIKit resolves a storyboard's `customClass` **through its module**. With
the attributes gone it could not find the class, instantiated nothing, and the app
came up black. It compiled; the build was green; the failure is entirely at
runtime. (Xcode's own message for this is "Unknown class X in Interface Builder
file" — invisible without a Mac to read the device console.)

### Fixed
- The storyboard now reads
  `customClass="IntonareViewController" customModule="App" customModuleProvider="target"`.
  `CAPBridgeViewController` lives in the Capacitor module; ours lives in the app
  target, whose module is `App`. **Both** attributes had to change, not just the
  class.
- `@objc(IntonareViewController)` on the class, so the Objective-C runtime that
  storyboards actually use can see it.
- The patcher now **fails the build** if `customModule="App"` is absent after
  patching, or if any `CAPBridgeViewController` reference survives — and prints
  the resulting `viewController` line to the log. This class of bug will not ship
  green twice.

## v0.81.9 — the volume design: full loudness except while the mic is live

**Why iOS is quieter than Android even with routing fixed:** the `playAndRecord`
category runs output through a voice-processing chain that attenuates it — the
category is built for phone calls, where a loud speaker feeds back into the mic.
Apple's developer forums confirm it plainly ("when using .playAndRecord, all
sounds will be played with a low volume"), and WKWebView makes it worse: when
`getUserMedia` starts, WebKit reconfigures the session itself, flipping the mode
toward voice chat, which engages **Voice Processing IO**. Output ducks. No JS API
can undo it.

Note what this rules out: removing `.mixWithOthers` — the prior suspect — would
NOT have fixed this (multiple reports confirm `.defaultToSpeaker` +
`overrideOutputAudioPort(.speaker)` still cannot reach 100% on this category).
It would only have made Intonare pause everyone's Spotify for nothing.

### The design
Can the ducking be bypassed outright? Almost. The literal off-switch exists —
`kAUVoiceIOProperty_BypassVoiceProcessing` — but it lives on the VoiceProcessingIO
audio unit, and on iOS that unit belongs to **WKWebView's internal audio engine**,
which no API lets us touch. What IS available, per the Apple dev forums thread on
VPIO volume (721535): once VPIO has ducked the output, **re-calling `setCategory`
or `overrideOutputAudioPort(.speaker)` restores the level** — and any audio source
started afterwards may duck again and need another nudge. So:

- **Launch / mic off: `.playback`, mode `.default`.** No mic claim, no voice
  processing anywhere near the output, full volume. This is the app's resting
  state. (Previously `playAndRecord` was set at launch, which parked the whole app
  in the attenuated state before the mic was ever touched.)
- **Mic starts: `assertAudioMode()`** — `playAndRecord`, `.defaultToSpeaker`, mode
  `.default`, then `overrideOutputAudioPort(.speaker)` — the snap-back call.
- **New audio source while mic is live** (reference tone, drone, metronome):
  throttled re-nudge, max one per second, gated on `isListening`.
- **Mic stops: `releaseAudioMode()`** — back to `.playback`. Full volume returns.

The residual truth: while actually recording, iOS never grants quite the full
playback level on this category. Everything outside mic-time is now full volume,
and mic-time is as loud as the platform allows.

### Added
- **`IntonarePlugin.swift`** — Intonare's first real iOS Capacitor plugin. Two
  methods, `assertAudioMode()` / `releaseAudioMode()`, both one-shot,
  JS-triggered, **zero observers** (the observer-based ancestor of this idea
  looped `setCategory` against its own route-change notification and hung the
  app; the design constraint is written into the file header). Failure resolves
  `ok:false` rather than rejecting — a volume nudge must never break mic setup.
- **JS call site** right after `micStream` is set, iOS-gated, wrapped so no
  failure can propagate. Silently a no-op on Android/web/older builds.
- **Registration via `bridge.registerPluginInstance()`** from an
  `IntonareViewController: CAPBridgeViewController` subclass. Capacitor 8's
  config-based discovery (`packageClassList`) does not see local app plugins
  (capacitor#7409); instance registration from `capacitorDidLoad()` is the
  documented route. `patch_ios_appdelegate.py` now appends the plugin + subclass
  to AppDelegate.swift (same no-pbxproj-surgery reasoning as ever) and repoints
  `Main.storyboard` at the subclass, with hard verification and a printout of the
  storyboard if the anchor is missing. Dry-run tested against a faithful mock of
  the Capacitor 8 template, including idempotency on re-run.
- Panel now shows `audioMode: asserted / assert failed / plugin absent / not
  attempted`.

### Also fixed: haptics — and no Swift was needed
The plan was to add a haptic method to the new plugin. Reading the code first
made that unnecessary. The haptic functions call `window.Haptics` — the official
`@capacitor/haptics` plugin, which is installed, has an iOS implementation, and
is exposed by `main.iife.js`. The chain was correct end to end. Except:

    if (/^https?:/.test(location.protocol)) { ...load main.iife.js... }

**The loader's protocol guard only allowed http/https.** On iOS the protocol is
`capacitor:`, so the regex failed, `main.iife.js` never loaded, `window.Haptics`
never existed — and since every haptic function is try/catch'd by design, there
was no error anywhere. The buttons just didn't buzz. (The guard exists so nothing
is fetched when the raw HTML is opened from `file://` on desktop; it accidentally
excluded iOS.)

Fix: allow `capacitor:` in the guard. One regex. The panel now also reports
`Haptics bridge present/absent`.

### Why the plugin still matters
`IntonarePlugin` is the registration scaffolding the splash sound (and any future
native work) was waiting for. Adding a method to a registered plugin is trivial;
registering the first one was the wall.

## v0.81.7 — XHR fallback; the fetch scheme problem, actually fixed this time

Two prior attempts at the sample-loading bug did not survive contact:

- **v0.81.5** set `server.iosScheme: "https"`. Invalid — Capacitor's docs on
  `iosScheme`: *"Can't be set to schemes that the WKWebView already handles, such
  as http or https."* Silently ignored; origin stayed `capacitor://localhost`.
- **v0.81.6** enabled `CapacitorHttp` to patch `fetch` through native HTTP. On
  double-checking before shipping: native HTTP is URLSession, and **URLSession has
  no idea what `capacitor://` is** — it is a WKWebView scheme, registered inside
  the WebView. Whether the patched fetch handles local asset URLs is stated
  nowhere. It also has documented fallthrough cases (Request-object calls silently
  revert to browser fetch). A global fetch patch on both platforms for an
  unverified maybe is risk without proven reward. **Not shipped.**

### Fixed
- **`_fetchBuffer` now falls back to `XMLHttpRequest`** when `fetch` returns
  status 0 or throws. XHR goes through WKWebView's ordinary resource-loading path —
  the same one `<script>` tags and images use — which **can** read the
  `capacitor://` scheme. Old API, boring, works. Note: local-scheme XHR responses
  report status 0 *on success*, so the success test is "got bytes", not "2xx".
- Normal platforms are untouched: fetch succeeds, XHR never runs.
- The diagnostics panel now shows which transport loaded the samples
  (`via fetch` / `via xhr`).
- CI cleans any lingering invalid `iosScheme` from `capacitor.config.json` so it
  does not sit there looking intentional.

## v0.81.5 — fetch() cannot read the capacitor:// scheme

**Every sample on iOS was failing. All of them.** The diagnostics panel from
v0.81.4 gave the answer in two lines:

    origin       capacitor://localhost
    last error   HTTP 0
    ok / fail    0 / 294

**294 fetches, zero successes.** Not the piano — *everything*.

iOS Capacitor serves `www/` from the custom scheme `capacitor://localhost` by
default. WKWebView will load that scheme for `<script>`, `<img>`, `<link>` — but
**`fetch()` against it returns a response with status 0.** A custom scheme is not
treated as a normal HTTP origin, so the request never really happens.

Every audio sample is loaded with `fetch()`. Hence: synth, everywhere, silently.

### Fixed
- **`server.iosScheme` is now forced to `"https"` by CI**, before `cap add ios`
  runs. Capacitor then serves from `https://localhost`, which *is* a normal origin,
  and `fetch()` works.

  Patched in the pipeline rather than trusted to the file in the repo: `cap add
  ios` regenerates platform config every build, and a value this load-bearing
  should not depend on anyone remembering it. The step fails the build if
  `capacitor.config.json` is missing.

### Note on v0.81.4
The `document.baseURI` fix from v0.81.4 was correct and stays. It just resolved to
an origin that `fetch()` refuses — right instinct, wrong layer. The URI-encoding fix
(for filenames with spaces, like `Rdcus 024 060.mp3`) also stays; that bug is real
and would have surfaced the moment the scheme was fixed.

### Still open
- **Volume lower than Android**, though audio now comes from both speakers, so the
  routing fix worked. Next suspect is `.mixWithOthers`, which asks iOS to duck the
  app so it can share the output with other apps.
- **Haptics and splash audio**: `IntonareNative` reports absent. The bridge was
  never written for iOS. Both need real Capacitor plugins.
- **Top padding** still feels heavy under the notch.

## v0.81.4 — samples were never loading on iOS

The piano was still playing synth on iOS. The files are correct (30 mp3s, tracked
in git, copied into `www/audio/` by CI, no FATAL from the guard), so the failure is
between the file and the fetch.

### Fixed
- **`_capacitorAssetUrl` built a root-relative path.** It returned `/audio/<folder>/
  <file>`, and its own comment said why: *"Android assets under public/ are served
  directly from localhost/"*. That is an Android assumption, written when Android
  was the only target. iOS serves `www/` through a local server on a different
  scheme (`iosScheme: "https"`), so a root-relative path is not guaranteed to
  resolve the same way. Now built from `document.baseURI`, which is correct on
  every platform by construction and assumes nothing.
- **Filenames are now URI-encoded.** Some sample sets have **spaces** in their
  names — `Rdcus 024 060.mp3`. An unencoded space in a fetch URL is a silent
  failure, and it would have hit the Rhodes while sparing the piano, which is
  exactly the kind of half-working bug that wastes a day.
- **`grand_piano` had its own inline `assetUrl`** duplicating the shared helper.
  Routed through `_capacitorAssetUrl` so there is one implementation to fix.

### Added
- **Sample diagnostics in the audio panel** (seven taps on the version stamp):
  load state, ok/fail counts, the last URL actually fetched, the specific error
  (HTTP status, fetch throw, or decode failure with byte count), and
  `location.origin`. `_fetchBuffer` already threw a precise error; it was being
  swallowed into a `console.warn` that nobody can read on iOS without a Mac.

### Confirmed working (from the v0.81.3 panel)
AudioContext `running` at 48 kHz; mic track `live`, hardware rate 48 kHz matching;
`aec false`; peak reading real room noise. **The iOS audio path is healthy.**

`IntonareMic` and `IntonareNative` both report **absent** — neither native bridge
was ever written for iOS. So haptics and the splash sound are not broken; they were
never implemented on this platform. Both need real Capacitor plugins. The mic does
not: WebView capture at 48 kHz is working.

## v0.81.3 — the audio session was looping on itself

**The iOS lag was mine.** `IntonareAudioSession.swift` registered an observer on
`routeChangeNotification` whose handler called `setCategory()`. But `setCategory()`
can itself post a route change. Observer → setCategory → route change → observer,
on the main thread, from launch, forever.

That explains both symptoms together, which no other theory did: the app was
unusably laggy **from the splash screen**, before any user action; and the volume
meter read **silence**, because the session was thrashing its own category
thousands of times a second and the microphone never got a stable configuration.

### Fixed
- **Observer removed.** `IntonareAudioSession` is now one `setCategory` call, once,
  at launch. `.defaultToSpeaker` — the actual volume fix — is kept, because it is a
  flag on a category, not a thread or a callback, and it costs nothing.
- Also gone (all shipped in the same bad version, all removed):
  `setPreferredIOBufferDuration(0.005)` — asked iOS to wake the audio thread 200×/s
  and cross into WKWebView on each callback, for no gain, since detection latency
  is bounded by rAF and the FFT window. `setPreferredSampleRate(48000)` — iOS picks
  per route and the AudioContext reports the real value anyway. `setActive(true)` at
  launch — claimed the audio hardware from app open whether the mic was used or not;
  WKWebView activates the session itself when it needs one.
- The file now carries a header listing each of these and why it must not come back.

### Added
- **Audio diagnostics panel.** Seven rapid taps on the version stamp. (The
  long-press on the same element still opens the unlock-code entry; separate
  gestures, no collision.) Shows live: AudioContext state and real sample rate,
  whether a mic stream and track exist and what the OS reports for them, and the
  **raw peak amplitude off the analyser** — the number that distinguishes a dead
  microphone from a quiet one. Inert until opened: no DOM, no listeners, no polling.

  It exists because iOS audio fails silently. WKWebView refuses `getUserMedia`
  without saying so, an AudioContext can report `running` while producing nothing,
  and a broken `AVAudioSession` yields zeroes with no error. Without a Mac there is
  no console to read, so the app has to report on itself. Three wrong diagnoses
  tonight came from guessing at state we could simply have measured.

### Note on v0.81.2
The piano sample conversion (51 MB of WAV → 10.8 MB of mp3) was shipped as a fix
for this lag. It was not the cause — the app lagged before any sample loaded. The
conversion was worth doing anyway: 40 MB off the Android download, and no reason to
ship uncompressed PCM in a mobile bundle. But it did not fix what it was shipped to
fix, and that should be recorded honestly.

## v0.81.2 — piano samples were 51 MB of uncompressed WAV

**The app became unusable on iOS.** Cause: `grand_piano` shipped as **29.8 MB in
30 uncompressed WAVs**; `electric_piano` as **21.5 MB in 13**. Every other
instrument in the library is mp3 at 15–25 KB per note. These two were outliers by
roughly a factor of eighty.

`SampleEngine.load('grand_piano')` fires shortly after launch and fetches all 30
notes with `Promise.all` — thirty simultaneous requests, then thirty
`decodeAudioData` calls on raw PCM. Android serves those from the APK's local
assets and absorbs it. **iOS serves `www/` over a localhost HTTP server inside the
app**, so the same load is thirty HTTP round trips plus thirty decodes on a phone.

Before v0.81.1 the files were not bundled at all, every fetch 404'd instantly, and
the synth fallback ran. Bundling them is what exposed the weight.

### Fixed
- **`grand_piano`: 29.8 MB → 7.9 MB.** Source is already mono 16-bit/44.1k, so
  transcoding to 192 kbps mp3 loses nothing.
- **`electric_piano`: 21.5 MB → 2.9 MB.** Source is **stereo**; kept stereo at
  192 kbps. (An earlier pass folded it to mono to save 0.5 MB. Reverted — a Rhodes
  has real stereo width and a musician on headphones would hear it flatten. Not
  worth half a megabyte.)
- **Net: 51 MB → 10.8 MB.** The Android download shrinks by the same 40 MB.
- Both `noteToFile` maps repointed `.wav` → `.mp3` (59 references), plus the
  shared `_salamanderNoteToFile` helper. No other instrument touched: the other
  36 route through `_gleitzNoteToFile` and were always mp3.

### Note
This is the second time this bug has been fixed. The comment above the preload
(`removeSplash`) records the first: eager-loading *every* registered instrument at
launch made the tuner feel laggy, and the fix was to warm only the grand piano.
Correct as far as it went — but the grand piano was itself 15× heavier than any
other instrument, and that part survived. Android tolerated it. iOS did not.

### Known open
- **`audio_assets/mandolin/` is empty.** Zero files. It has been failing to load
  and falling back to synth silently. Unrelated to the above; needs sourcing.
- **The iOS audio session (`IntonareAudioSession.swift`) is still untested.** It
  shipped in a build that TestFlight buried below the old `1.0` version group, so
  no tester has ever run it. Whether `.defaultToSpeaker` actually fixes the
  earpiece-routing problem is still unknown.

## v0.81.1 — iOS build pipeline

> **Changelog gap:** entries between v0.73.37 and v0.81.1 (the audio detection
> overhaul, Road Trip journey slices, FFT pitch detector, Leg Tuner) are not in
> this file. They were shipped and sentinel-verified but the log was not kept.
> Reconstruct from chat history when there is time.

**iOS shipped to TestFlight for the first time.** Signed build, three internal
testers, microphone confirmed working on WebKit. No native audio plugin needed:
the same web code drives all seven mic surfaces on iOS.

### For testers
> TestFlight "What to Test" notes are written by hand in App Store Connect
> (TestFlight → Builds → the build → What to Test). Not automated: a build that
> refuses to run because the release notes were not written is a build that gets
> the check deleted. Copy from here if useful.

Fixed: the piano and other sampled instruments now play real samples rather than
falling back to synth; audio should be much louder once the microphone is on (it
was going to the earpiece speaker instead of the loudspeaker); the header no
longer sits under the notch; buttons buzz again (haptics were missing entirely);
real app icon.

To test: turn the microphone on, then play a reference tone or start the
metronome — is it loud enough now? Start a drone and sing over it: does the tuner
still track your voice, or does the drone coming out of the speaker confuse it?
If you have Bluetooth headphones, does the audio play through them?

### Web (`Intonare.html`)
- **iOS safe-area padding fixed.** `body { padding-top: min(8px, max(2px,
  env(safe-area-inset-top))) }` caps the top inset at **8px**. That cap exists for
  Android sticky-immersive, which zeroes the reported inset. On iPhone the inset
  is the real notch (**47–59px**), so the cap threw it away and the header sat
  under the Dynamic Island. Added `html.ios body { padding-top:
  env(safe-area-inset-top) }` — full inset on iOS, cap retained on Android.
- **Platform class set on `<html>` from JS** in `DOMContentLoaded`
  (`documentElement.classList.add(Capacitor.getPlatform())`). Capacitor may do
  this itself; doing it here means the CSS rule above does not depend on that
  behaviour holding.

### Build pipeline (`codemagic.yaml`)
Codemagic builds and signs iOS on every push; `ios/` is **not committed** and is
regenerated each build, so all native customisation happens as CI steps. This is
the same pattern as `go.bat [4b]–[4c2]` restoring `MainActivity.java` after
`cap sync` overwrites it.

- **Audio samples were missing → every sampled instrument fell back to synth.**
  The app fetches from `/audio/<instrument>/`, but they live in
  `audio_assets/<instrument>/`; `go.bat [4g]` does that rename and the CI step
  did not. Now mirrored, and the step **fails the build** if `audio_assets/` is
  absent rather than silently shipping a synth-only app.
- **`main.iife.js` was never built → haptics silently dead on iOS.** `go.bat [4a]`
  runs `npm run build` (Vite compiles `main.js` into the Capacitor haptics
  bridge); the CI step skipped it. Its absence produces no error anywhere. Now
  built and guarded.
- **App icon.** `cap add ios` writes a placeholder `AppIcon.appiconset` fresh
  every build. Real icon injected from `ios_icon/AppIcon-1024.png`. Rebuilt as
  **SVG** (`intonare_icon.svg`) traced from the 512 raster, so it renders at any
  size — the largest Android asset was 192px, and a 5× upscale to Apple's required
  1024 would have been mush. **Flat RGB, no alpha:** Apple rejects transparency in
  app icons at *upload*, not at review.
- **`Info.plist` patched** via PlistBuddy: `NSMicrophoneUsageDescription` (without
  it iOS *terminates* the app the instant `getUserMedia` fires — not a permission
  denial, an immediate crash), `UIBackgroundModes: audio`,
  `UISupportedInterfaceOrientations: portrait`, and
  `ITSAppUsesNonExemptEncryption: false` (pre-answers the export-compliance
  question App Store Connect otherwise asks on every upload).
- **`capacitor.config.json` · `server.iosScheme: "https"`** — iOS Capacitor
  defaults to the `capacitor://` scheme, which WebKit does not reliably treat as a
  secure context. Without this, `getUserMedia` and Web Audio are blocked outright
  and all seven mic surfaces fail silently.
- **Signing.** Certificate + provisioning profile are generated in the Codemagic
  UI, not at build time. `fetch-signing-files --create` cannot work alone: Apple
  only ever holds the *public* half of a certificate, so it can issue one but
  cannot return a private key to pair with it. Build is flagged
  `testFlightInternalTestingOnly` — internal testers need no Beta App Review.
- **`.gitignore` patterns anchored to root** (`ios/` → `/ios/`). Without the
  leading slash, git matches the pattern **at any depth**, so `ios/` was silently
  ignoring `native_src/ios/` too.

### Native (`native_src/ios/`)
- **`IntonareAudioSession.swift` + `patch_ios_appdelegate.py`.** When WKWebView
  calls `getUserMedia`, iOS switches the audio session to `playAndRecord`, which
  routes output through the **earpiece receiver** rather than the loudspeaker — the
  OS assumes an app that records and plays at once is a phone call. Everything the
  app plays goes quiet the moment the mic is touched. **WebKit exposes no way to
  change this**; there is no JS API. `AVAudioSession` is the only lever and it is
  native-only.
  - `.defaultToSpeaker` — the fix.
  - **`.allowBluetoothA2DP`, deliberately NOT `.allowBluetooth`.** A2DP is
    high-quality, output-only, no microphone. `.allowBluetooth` enables the HFP
    headset profile, which collapses the **entire session, both directions**, to
    **8–16 kHz mono**. With AirPods connected the tuner would silently start
    reading an 8 kHz mic feed (Nyquist ceiling 4 kHz), gutting the harmonic content
    the FFT detector depends on. No error, no warning. 📌
  - `.mixWithOthers`; preferred sample rate **48 kHz**; IO buffer **5 ms**.
  - Category is **re-asserted** on `routeChangeNotification` and after
    `interruptionNotification` ends — plugging in headphones or taking a call
    resets it, and without this the app returns quiet.
  - Applied by appending to the generated `AppDelegate.swift` rather than adding a
    new source file: Xcode tracks sources in `project.pbxproj`, and scripted
    surgery on pbxproj is exactly the kind of thing that breaks quietly later.

### Known open
- **`_iosBetaUnlock()` still grants Pro to every iOS user with no purchase path.**
  This gates everything: no external testing, no public TestFlight link, no App
  Store, under Guideline 3.1.1. Needs the RevenueCat iOS key, an IAP product in
  App Store Connect, StoreKit wired, Restore Purchases verified.
- **Microphone permission string is English-only.** Needs `InfoPlist.strings` in
  `it.lproj`/`en.lproj`, registered as Xcode resources.
- **Loudspeaker now fires next to the microphone.** The drone notch measures
  **−38 dB** on the drone with voice at −0.1 dB, so the detector should stay clean —
  but the mic's input stage now sees a much hotter signal, and any AGC iOS applies
  could duck the voice to compensate. Unverified on hardware.
- **Version string pinned at `1.0`** in TestFlight (comes from the regenerated
  Xcode project, not `INTONARE_VERSION`). Cosmetic until public release.

## v0.73.37
- **TONAL · temperament toggle restyled into the CRT language.** The old
  `ref-toggle` pill (last thing breaking the retro illusion) rebuilt as a keycap
  segment (`.tc-temp-seg` / `.tc-temp-key`) in matching dark housing — lit label
  only on the active key, same look as the root/octave keys. Explanatory hint line
  kept (teaching-app: the toggle is contextual, beginners need it explained). `?`
  help moved into a `.tc-strip-lab-row`.
- **TONAL · HUD mode mirror added.** Display-only `◈ EQ` / `◈ JUST` tag
  (`#tcTempMirror`) inside the CRT HUD shows the current temperament like real
  hardware; the keycap below controls, the tag reflects. Plain 7px pixel text (NOT
  a bordered box — the HUD is pinned `height:10px; overflow:hidden` for layout
  stability, a box would clip).
- **`toggleTemperament()` rewired** to drive both keycaps + mirror; hidden
  `#tempLabel` span kept so legacy reads don't crash. `temperament` still the only
  consumer of the value (feeds the just-intonation cents target in
  `updateIntervalDisplay`); it lives ONLY in tonal-centre, nowhere else in the app.
- **i18n:** new `tuner_tuning_system`, plus short keycap labels `tc_temp_equal` /
  `tc_temp_just` (so the key reads "JUST" not "JUST INTON."; the longer
  `tuner_just_inton` is untouched for the main tuner). EN + IT.

## v0.73.36
- **TONAL · CRT screen height reduced** `412px → 348px` (felt too tall on-device,
  ~half the viewport). Internal spacing tightened to match: `.tc-hud` margin-bottom
  `18→14px`, `.tc-iv-stage` margin-top `18→12px`, `.tc-reticle` margin `20→14px`,
  `.tc-crt` padding `22px 18px 22px → 18px`. Layout-stability invariants intact
  (fixed height + `.tc-screen-body` flex:1 + tabular-nums → no reflow on drone
  on/off).

## v0.73.35
- **TONAL · tour repointed at the CRT.** The `tonal` module tour still pointed at
  the now-hidden `#tcToggleBtn` (preview rendered blank). Repointed at visible
  elements: `#tcCrt` (readout) → `#tcRootGrid` (root/scale/octave + scale map) →
  `#tcStartBtn` (power-on + blue/red/green colour meaning) → `#micBtn`. EN + IT.
- **TONAL · `tonal_center` help rewritten** for the CRT layout (was describing the
  removed "What Am I Singing?" panel). Added `?` help button in the ROOT NOTE
  strip-label row (`.tc-help` pixel-chrome style, carries `help-btn` class so it
  respects the global hide-help-tips toggle).

## v0.73.34
- **TONAL · CRT/retro redesign ported into the app** (from `tonal_redesign_v6.html`
  preview). Full markup swap: cabinet + fixed-height CRT screen, DRONE↔YOU note
  pair, interval-name hero, lock-on reticle tuning bar, control strip with keycap
  root grid + custom (non-native) scale dropdown + octave keycaps + second SCALE
  MAP screen with live scale-degree highlight. Volume slider dropped per design.
- **Removed elements kept as hidden legacy hooks** (`#pianoIntervalName`,
  `#pianoCentsBadge`, `#tcDroneState`, `#tcScaleType` native select, etc.) inside a
  `display:none` div so `updateIntervalDisplay()` keeps writing them without crashing.
- **JS wiring:** `tcInit` builds keycaps + dropdown; `tcUpdateScale` builds the
  root-anchored scale map w/ degree numbers; `tcDroneStart`/`tcToggleDrone` drive
  power-on/standby (preserved the critical `droneRoot`/`droneOctaveIdx`/`_dronePureSine`
  sync before `droneStart()`). Live readout EXTENDS `updateIntervalDisplay` via a
  `tcRenderCRT(mode,data)` hook at its 3 exit points — all existing hold/temperament/
  JI/highlightPiano logic untouched.
- **Colour is meaningful 📌:** flat=blue, sharp=red, in-tune=lime/green; the hero,
  YOU note, reticle marker, and cents all tint by tuning direction.
- **Press Start 2P font self-hosted** as base64 (12.5KB woff2 from npm fontsource;
  Google Fonts CDN forbidden by sentinel pin). Used for HUD/chrome labels ONLY;
  Bebas for big content, JetBrains Mono for Hz.
- **i18n:** tc_drone_off, tc_listening, tc_drone_lab, tc_you_lab, tc_scale_map,
  tc_flat, tc_sharp, tc_iv_start, tc_standby, tc_matching_root/above_root/below_root,
  drone_stop — EN + IT. Orphaned (harmless): tc_what_singing, tc_set_root_hint.

---

## Gap reconstruction: v0.20.43 → v0.73.33 (~June 6–30)

> ⚠️ **Reconstructed from chat history, NOT live-logged.** Live logging lapsed
> after v0.20.43 and didn't resume until the CRT work (v0.73.34+). This block
> covers ~53 version bumps across ~15 chats. It is grouped by feature area, not
> per-version — individual version numbers below are anchors I could verify, not a
> complete bump-by-bump record. Exact values were not re-verified against the file.
> Treat as "what shipped in this window," not as precise as the live entries.

### Instruments · woodwind fingering charts (the dominant work of this window)
- **Oboe + cor anglais fingerings finalized** (~v0.43.2–0.43.4). Main fingerings
  verified vs wfg.woodwind.org; full alternate-fingering sets added across both
  octave registers (Side Bb, Fork Eb/F/G#/A, Oct I alts, etc.); fixed a bug where
  second-octave alts weren't surfaced to the UI alt-cycle buttons. Oboe altissimo
  added (MIDI 85–93, C#6–A6); range bumped high:93, octave 6. Cor anglais fully
  synced to oboe (no altissimo — non-standard).
- **Woodwind chart visuals normalized.** All renderers (oboe, recorder, whistle,
  clarinet, sax) unified to open-key GREY `#8a99a6` matching flute; closed ACCENT
  hardcoded `#2ec78f` (SVG can't resolve CSS vars). Clarinet/sax maxWidth caps
  added to stop sprawl.
- **Bassoon + contrabassoon FDB import** (v0.58.5–0.59.3). First instrument built
  from Bret Pimentel Fingering Diagram Builder SVG exports (CC BY-NC-SA 4.0, Bret
  emailed + granted permission; credit added to Credits modal). Verbatim path data
  wrapped in the original transform `matrix(.75 0 0 .75 3.718 2.395)`; `bodyPath()`
  grey-stroke structure + `keyPath(d,slot)` interactive keys (ACCENT fill closed,
  GREY stroke open, fill-rule evenodd). Quadrant labels only (LT/RT/LH/RH) — in-key
  labels abandoned as un-centerable. Sub-tab switching needs 4 synced sites
  (WW_SUBS, CS_INSTRUMENTS, switchSubType, _buildSubRow ternary) — pinned learning.
- **`BRET_SVG_IMPORT_GUIDE.md` written** — Claude-targeted process doc for importing
  the remaining 9 woodwind families. Clarinet identified as next (Standard Boehm
  Bb/A/Eb + Bass clarinet pro), parked on Daniele needing desktop FDB donor auth.
- **Flute trills + clarinet** (earlier in window, ~v0.38–0.39). Flute renderer
  traced via potrace (18 toggleable key slots); TRILLS subtab infrastructure built
  for woodwinds from scratch; trill audio via alternating pitches. Clarinet got
  MIDI-direct fingering lookup (register-break accuracy) + trills. Flute collapsed
  to one `ww_flute` with Flute/Piccolo/Alto sub-types (piccolo 8va up, alto P4 down).

### Charts · audit pass (fretted + brass + woodwind ledger)
- **`INSTRUMENT_AUDIT_LEDGER.md`** built — full tier'd status of every instrument's
  chart/fingering correctness with sources + open questions.
- **Bass trombone low register fixed** (v0.67.0–0.67.1): notes below ~E2 all
  defaulted to Position 1; replaced with full sourced F/D chart (Doug Yeo / Waage).
- **Mandola tuning fixed** GDAE → CGDA (viola pitches; code comment said "fifth
  below mandolin" but MIDI didn't match).

### Tools · new + finalized
- **Rhythm Flash Cards** built and finalized (v0.53.0–0.54.2). 29-card deck
  (whole→sixteenth, dotted, ties, triplets, syncopation, RESTS), onset-distinctness
  validator to kill tap-identical collisions, multi-select category Set, Fisher-Yates
  shuffle on open, full-screen `position:fixed; inset:0` overlay, drill-to-mastery
  mode (3 consecutive passes at ≤0.10 bar, neutral stats by design), tap-only
  haptics. Uneven-tuplet bracket rendering fixed (group by whole-beat sum).
- **Polyrhythm** finalized (through v0.68.83): tempo-leak fixes (constants not
  inherited prBpm), downbeat-drop scheduler fix (late clicks clamp to currentTime,
  only >20ms dropped), end chimes, help modal.
- **Metronome grooves** expanded earlier in window: +27 patterns across odd meters
  (3/4–11/8) → 51 grooves, +18 chord presets → 37, preset pairings audited,
  suggestedBpm hints.

### Train · interval / ear-training
- **Interval Training + Flash Cards** work (v0.66.50–0.66.57). Mic-powered; share
  helper `intonareNativeShare()` confirmed as 3-tier (native → web → clipboard).

### Launch prep (the pre-Play-Store push)
- **Privacy policy** drafted + shipped (`privacy.html`, github.io/Intonare/privacy),
  styled to app; covers mic, local storage, gleitz soundfont fetches, children's
  privacy, GDPR, Italian jurisdiction.
- **App icon + notification icon** built: `intonare_icon_512.png` + adaptive
  launcher set (`icon_res.zip`, mdpi→xxxhdpi, mask-verified circle+squircle);
  `ic_stat_intonare` notification icon (5 densities).
- **Splash audio sync fix** in `MainActivity.java` (native): removed `runOnUiThread`
  from `playSplashSound()` so `MediaPlayer.start()` fires on the binder thread; added
  audio pipeline pre-warm in `prepareSplashSound()`.
- **RevenueCat / IAP Pro unlock (Layer 1) — DONE** (built June 24 splash session).
  One-time-purchase model, integrated + shipping. Public RevenueCat SDK key ships by
  design (`goog_rbcoHGgwLmrhKklhmYPGFtvsSKL`); security scan clean (no secrets/
  keystore/service-account in repo).
- **Play Console submission published to CLOSED TESTING** (resolved an Advertising-ID
  declaration blocker → answered No).
- **DYK / fact-bank copy pass** (v ~0.73.x, late June): tone/AI-speak cleanup across
  the fact bank; flagged-not-fixed content dups (two Wes Montgomery near-dups, a
  Beatles/Decca pair, a `},,` double-comma at the Leo Fender entry).

### Native groundwork (scaffolding, not user-facing)
- **Web AEC stopgap** shipped v0.73.13: `_ECHO_TOOLS=['tonal']`,
  `_ECHO_EXERCISES=['interval','singsing']` → `_wantEcho` requests
  `echoCancellation:{ideal:true}` for reference-tone modes; tuner stays raw. Marked
  scaffolding for removal when native lands.
- **`NATIVE_AUDIO_ENGINE_PLAN.md`** written; **Phase 0 native mic plugin**
  (`IntonareMicPlugin.java`, `ping()`) placed. Key learning pinned: Capacitor 8 does
  NOT auto-discover app-embedded plugins — explicit `registerPlugin(...)` before
  `super.onCreate()` required. go.bat got a `[4c2]` native-restore line.

### Tooling
- Sentinel grew **85 → 97 tracked fixes** (9 new from Flash Cards) + pins 21 → 27.
- `intonare_quiz_audit.py` regex repaired (over-escaped raw string crashed
  `re.compile`); now parses cleanly.

---

## v0.20.43
- **NAV · folder reorg (per Daniele).** (1) Train "Rhythm" renamed → "RHYTHM
  TRAINING" (EN) / "ALLENAMENTO RITMICO" (IT) to end the clash with the Tools
  "Rhythm" (drumkit) folder; also fixed the JS routing key for the tools folder
  (`folder_rhythm_title` → `folder_rhythm_tools_title`) so the tools folder header
  still reads just "Rhythm". (2) "Analysis & Reference" (5 items) split into
  **Reference** (Circle of Fifths, Vocal Range, Survival Guide) + **Utilities**
  (Volume Meter, Transposer). New folder ids `toolFolderReference` /
  `toolFolderUtilities`, routing map + IDs updated, two new hub entry cards, full
  EN/IT i18n. Old `folder_analysis_*` keys now orphaned (harmless). (3) Drumkit
  folder left as-is per Daniele.
- **i18n · all 6 flagged hardcoded strings fixed** + the Diadle guess counter:
  PLAYING/PAUSE/RESUME (rhythm-reading), ALL chip, TAP AGAIN TO CONFIRM (×2),
  GUESS N OF M. New keys rr_*, chip_all, confirm_tap[_warn], diadle_guess_of
  (placeholder-interpolated). Strings audit now 0 hardcoded.
- **FAV · Diadle can now be favorited** — added `exercise:diadle` FAV_META entry.
- **QUIZ · 2 criticals fixed** (Music History): lengthened the distractors on #61
  Philly Soul and #24 outlaw country so the correct answer is no longer a
  length-giveaway. Quiz audit: no criticals.
- **TOOLING · both audit scripts repaired this session** (strings key-extraction
  regex; quiz filepath arg) — re-shipped.

## v0.20.42
- **UI · stale folder counts fixed.** Games badge 3→4 (Diadle was added but the
  count + sub-string never updated); now uses its own `folder_badge_games4` key
  instead of sharing Ear Training's `folder_badge_ex3`. Analysis & Reference
  badge 4→5 (has cof, volume, transpose, vocalrange, survivalguide); new
  `folder_badge_5` key. `folder_games_sub` now lists Diadle (EN + IT).
- **Tooling · strings audit repaired.** Its key extractor matched only
  one-per-line keys (`\n    key:`), missing all multi-per-line keys → 372 FALSE
  "key not in STRINGS" errors. Fixed regex to catch keys after `,` too;
  extraction 542→933 keys, false errors gone.
- **Tooling · quiz audit repaired.** Had a hardcoded input path; now takes a
  filepath argument like the others.
- **Audit findings logged (NOT yet fixed — Daniele to action):**
  FAV_META missing for `exercise:diadle` (can't be favorited); 6 hardcoded UI
  strings (ALL, PLAYING, RESUME, PAUSE, GUESS, TAP AGAIN TO CONFIRM); 2 quiz
  criticals in Music History (correct answer ~2.7× longer than wrong: #61 Philly
  Soul, #24 outlaw country) + 89 milder length warnings.
- **Pending (waiting on Daniele's spec):** folder module moves + renames.

---

## v0.20.41
- **UI · long-press text-selection guard restored** (regression). Global
  `user-select:none` + `-webkit-touch-callout:none` re-added on
  `html, body, button, .practice-card-btn, [onclick]`; re-enabled
  `user-select:text` on inputs/textareas/select/contenteditable so typing & paste
  still work. Had silently vanished from the global rule.

## v0.20.40
- **UI · games folder extra header fixed.** Added `#gamesHub .train-header` to the
  in-section header-hiding CSS rule — it was the only sibling hub left off the
  list, so Games showed a redundant second header.

## v0.20.39
- **Tónale · score decimals unified.** Final count-up + share now whole-number to
  match the live header (`N / 50`). Was: header whole, count-up `.toFixed(1)`,
  share `.toFixed(0)` — three representations of one score.
- **Tónale · per-round breakdown** added to final screen (`tonaleRenderBreakdown`):
  per-round colored dot + cents-off + points. New i18n key `tonale_round_abbr` ('R'/'R').
- **Tónale · guess wave tints to score color on reveal.** Wave uses
  `tonaleCmp.colorResolved` (concrete color from `tonaleResolveColor`, since canvas
  can't read CSS `var()`); only overrides during `revealed` state.

## v0.20.38
- **Audit · Pass 19** added to instrument audit: flags any woodwind pitch class
  in-range but missing from its fingering table (silent home-fingering fallback).
  Hardened `parse_ranges` to handle nested `subRanges`.
- **UI · embouchure card min-height 📌** set to `78px` with flex-centering on
  `#trpCardEmbouchure` and `#trpEmbouchure`, so variable-length embouchure text
  never resizes the note card. (was: no min-height → card grew/shrank per note)

## v0.20.37
- **WIND · ocarina C4 bug — real fix.** Wind note grid offered any octave×pitch-class
  with no range check, so out-of-range notes (e.g. C4, below ocarina A4 floor)
  showed the same fingering as the in-range octave. Now: octave selector only
  offers octaves containing in-range notes; out-of-range pitch buttons are
  disabled/greyed ("Out of range for this instrument"); selection snaps to lowest
  in-range note. General fix — applies to all wind instruments.
- **WIND · ocarina range 📌** `octaves:[4,5]` → `[4,5,6]` so high C6–F6 are reachable
  (12-hole high `89`/F6; 7-hole capped `84`/C6).

## v0.20.36
- **WIND · ocarina fingerings rebuilt from source** (pureocarinas.com / Hickman).
  Old data was invented (fake octave-register split). Now one continuous
  hole-opening sequence; diatonic naturals verified, accidentals = labeled
  cross-fingerings. C5 home 📌 = `[1,1,1,1,0,0,1,1,1,1,1,1]`.
- **Audit · Pass 18** added: asserts the 6 verified ocarina diatonic naturals
  against expected values (catches invented/regressed fingerings).
- **Breath hints** corrected (no "register/overblow" language — ocarina has no
  octave registers).

---

## Earlier (reconstructed from history, pre-live-logging)

### Tónale (added ~v0.20.x, "Adding Tonale" chat)
- Pitch-memory game modeled on dialed.gg/sound. 5 rounds, scored /50, easy/hard
  modes + daily challenge with mid-game resume (`dailyInProgress`).
- Reveal color thresholds 📌: `pts>=9.5` green, `pts>=7` amber, else red.
- Positive-cue (haptic/sound) threshold 📌: `pts >= 6.5`.
- Frequency skew biases targets higher (`Math.pow(r, skew)`); per-mode ceilings
  raised (easy E5, medium C6, hard A7, insane G8).
- Wave visualizer: crest speed made constant across pitch (phaseStep scales with
  cycle count). Slider reskinned to "wide pitch-field" with frequency ladder.

### Diadle (scale-degree ear-training game)
- Wordle-style; name each note's scale degree. Difficulties 📌: all three
  `maxGuesses:5` (easy len 3/drone, medium 4/button, hard 5/once).
- Locked-slot carryover between guesses; loss screen reveals each degree + note;
  daily mode w/ shareable emoji grid; first-try firework.
- Piano-timbre voice through reverb bus; click fixed with 18ms attack +
  asymptotic release.

### Quiz (19 packs, 1153 questions)
- **Major regression repaired:** ~116 `opts` arrays were scrambled onto wrong
  questions (truss-rod Q had amplifier options, etc.). Re-paired across 8 packs;
  spot-checked. The clean June-3 474Q build had never merged in.
- Beatles rooftop/George-Martin question swap fixed.
- 14 compound questions trimmed to just the "what".
- Background scroll/bounce lock (`body.sg-open`); two-tap reset stats;
  missed-questions scroll + centered title; game-over redesign.
- Daily streak toast opacity 📌: solid base layer on all tiers (`opacity:1`),
  regression-proofed.

### Metronome / Progression
- BPM scrub wheel: flywheel inertia, windowed velocity (fixed direction-flip from
  ghost mouse events + sign error in `_bpmFrac`), `_computeReleaseVel` ignores
  stale samples.
- Tick sound 📌: two detuned sines `3100Hz + 4700Hz`, 12ms exp decay; Hann-windowed
  prebaked buffers (no GC pops); 38ms rate limiter.
- Groove mode: dynamic `groovePattern.length` (not hardcoded 16); 51 grooves,
  37 chord presets; mute syncs across views (`metroMuteBtnGroove`); long-press
  sort needs 10px threshold + `touch-action:pan-y`.
- Shared `getAudio()` context to kill clock drift; `startMetroAt` for bar-boundary
  alignment; time sigs 2/4–11/8.

### Charts / instruments
- Capo root-shift moved to top of `gccVoicings()` (universal across instruments).
- Added banjo (roll engine), mandolin, mandocello, uke bass, baritone/tenor guitar.
- Mandocello cache-prefix fix (was returning mandolin shapes); sub-tab cold-open
  fix (`_buildSubRow` called directly); save-chart `keepState` (root restores).
- Bass synth click 📌: 3ms (`0.003`) linear ramp from zero; removed redundant
  sub-oscillator (phase-beating buzz).
- Harmonica pathMap keyed by MIDI not pitch-class (wrong-C highlight fix).
- Ocarina diagram: traced geometry from PDF; rule = change labels, never positions.

### System / layout / i18n
- Lang switch no longer false-fires drumkit achievement (`fromLangSwitch` guard).
- Haptic feedback default-ON with `progLoad` migration.
- Permission flow split: notifications immediate on splash removal, mic on first
  touch (`_reqMicPerm`).
- Survival Guide: in-flow layout w/ measured `--sg-h`; dynamic `--nav-bar-h` /
  `--header-h` from live DOM; tools tab exits folder.
- Version lives in 3 synced spots (top comment, JS const, `#smVersionStamp`).
- Renamed Sonoro → Intonare; appId `com.lieutenantdan.intonare`.
