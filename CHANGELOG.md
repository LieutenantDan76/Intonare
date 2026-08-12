# Intonare — Changelog

A human-readable record of what changed, when,

---

## OPEN ITEMS (as of v0.104.0)

Not a release entry. A standing list so these survive outside anyone's memory.

**Road Trip: 21 songs need their legs tuned on device**

clair_de_lune, prelude_em, moonlight, liebestraum, fuer_elise, moonlight_3,
prelude_c, alla_turca, barcarolle, butterfly, fantaisie_impromptu, moonlight_2,
prelude_csharp, prelude_op23, raindrop, sonata_facile, to_spring, traumerei,
troika, waldstein_1, wedding_day.

That is exactly the set with a perf: block, and it is not a coincidence. Hooks
were placed as beat positions against the grid; converting to performance mode
replaced the timing wholesale, so every one of them is either analytic or stale.
RT_TUNED is still empty. Long-press the ROAD TRIP title to open the Leg Tuner,
tune, then add the id to RT_TUNED and pin its line in the sentinel.

The 17 grid songs were hand-tuned by ear and are now pinned (v0.104.0), so a
silent drift becomes a build failure rather than a lucky catch.

**Housekeeping**

`intonare_groove_audit.py` still needs copying into `/mnt/project/`. It ships to
outputs on every build but does not persist, and it already had to be rebuilt
from scratch once for exactly this reason. The same now applies to the sentinel:
v0.104.0 added 17 pins, so the copy in the project must be replaced or those
pins vanish on the next fresh chat.

RESOLVED: groove patterns are pinned. The Toussaint six, maqsum and the flamenco
pair went into the sentinel, which is why Bulería cannot silently revert again.

**On-device listening, ordered by how much actually changed**

- JOROPO — accents moved so the three-against-two hemiola is audible. Should read
  as a cross-rhythm, not as lopsided.
- TUMBAO — new preset, two strokes, empty downbeat. Suspended or broken?
- AFROBEAT — Tony Allen's first pattern. Nothing lands on any of the four beats.
  The extreme version of the same question.
- JAZZ SWING — was genuinely broken and never struck beat 2. Should now sound like
  a swing ride.
- BOOM BAP — had no bap. Now has one.
- SHIKO, SOUKOUS, GAHU — will sound close to son clave. That is correct; the six
  distinguished timelines differ from each other by one or two sixteenths.
- ÇİFTETELLİ — the one place three sources disagreed and a choice was made. Most
  likely of any entry to be wrong.
- BULERÍA — should now open on an accent where Soleá does not. That is the audible
  difference between the pair.

Everything else in v0.102.x was citations only and will not sound different.

**Three grooves are finished in the sense of "as good as desk research gets"**

Montuno's piano guajeo, Samba's tamborim, and New Orleans. Each carries a CEILING
REACHED note naming what would settle it: a Cuban piano method, a bateria chart,
or Antoon Aukes' "Second Line: 100 Years of New Orleans Drumming" — failing those,
a player. Bhangra is technically sourced but sits on the wrong grid for a triplet
feel and its sources contradict each other on accents.

---

## v0.133.9 — softer selection, and the editor gets a floor

**The selection was tuned against a background that no longer exists.** A 2px dark
gold frame reads as definition on khaki and as harshness on cream, so removing the
slab in v0.133.8 changed what the frame had to fight without changing the frame. Now
a mid-gold frame instead of dark, a paler wash, a gentler glow, and the bright cap
line dropped entirely — on a pale card that line was the loudest part of the whole
treatment. Still outline and box-shadow only, so selection still cannot reflow the
grid. Name contrast holds at 4.62:1.

**The lower half of the panel had no depth at all.** Header, step grid and the
button were cream on cream separated by hairlines, so everything below the grooves
read as one undifferentiated field. The header and step grid now share a single
recessed slate — the surface you work on — with the button raised above it. Three
depths where there was one, and the inset shadow says "manipulate this" in the same
language the selected card uses.

Done without adding a wrapper to the markup: the slate is drawn on the pattern
header with square bottom corners and no bottom border, and the step grid continues
it with square top corners, so two adjacent elements share one well.

BAND FLASH gains a little saturation to sit clearly above that well as the action
rather than another panel.

All `body.light` scoped; dark mode confirmed unchanged by reading computed values
back in both schemes.

## v0.133.8 — the khaki slab goes, and the rest of the panel gets a light mode

**The slab was mine and it was wrong.** Giving the card grid a filled khaki ground
made sense on paper: pale cards need something to read against. On a device it is a
hard-edged tan block dropped into a cream page, and it looks like a rendering fault
rather than a surface. Gone. The cards separate on their own instead — pushed
slightly whiter than the page, given a warmer border, and lifted with a soft shadow.
Paper on paper, no slab required.

Which exposed that the rest of the panel had never been converted either, and two of
those were unreadable rather than merely dim:

**The selected-groove header.** Its subtitle measured `#c3b17b` on a `#c3b27b` bar —
the same colour as its own background, near enough 1:1. "tap steps to edit" is an
instruction, and nobody could read it. Now 5.08:1, with the title at 6.15.

**The step pips**, which is the worst of the lot. On measured 1.05:1 against off, so
you could see sixteen squares but not which ones were lit: the pattern you are
editing was invisible while you edited it. Three states need three separated steps
of lightness rather than three tints of one, and a first pass at this only reached
2.12 and 1.29 — better than what it replaced and still not enough to read a rhythm
from. Tuned until every neighbouring pair separates: **off to soft 2.19, soft to
accent 3.04, off to accent 6.66.**

**BAND FLASH** read flat because it was a single cream fill with no edge and no
ground. It now carries a warm vertical gradient, a defined border and a lift, with a
pressed state to match — the same weight START already has, which is right, since
these are the two primary actions on the panel.

All `body.light` scoped; dark mode untouched throughout.

## v0.133.7 — the groove picker gets a light mode

It never had one. The cards were running dark-mode values on a cream sheet, which
put filled khaki tiles on pale ground and made the eleven grooves you did not choose
heavier than the one you did. The step preview was worse: khaki dots on a khaki
card, measured at **1.37:1**, which means the one thing that tells son clave from
rumba clave at a glance was effectively invisible and people were picking grooves by
reading names.

The grid now takes the khaki and each card becomes pale paper on it — the same
construction as the metro screen itself, so it borrows an idiom the app already owns
rather than inventing one. Palette sampled off a device screenshot rather than
guessed, after two earlier attempts at light-mode colour went wrong by guessing.

**Selected reads as pressed in**, not lifted out: a warm wash, a gold frame, and an
inset glow along the top edge. Three cues on three different channels — hue, weight
and light — because on a grid of near-identical pale tiles any one alone is too
quiet, which four separate single-cue attempts demonstrated.

Nothing touches layout. The frame is an outline, which paints outside the box, and
the glow is an inset shadow, which never affects flow; there are no padding or
margin changes. Selected and unselected cards measure identically, so the grid
cannot reflow when the choice moves. An earlier cut of this did shift the rows, and
the cause was a single stray `margin-top` — grid rows size to their tallest cell, so
five pixels on one card dragged everything below it down.

Measured after merging: unselected name 13.19:1, origin 4.63:1, pattern 3.62:1;
selected 4.44, 6.08, 3.62. The pattern went from 1.37 to 3.62.

Dark mode is untouched — every rule is `body.light` scoped, confirmed by reading the
computed values back in both schemes.

## v0.133.6 — the third one in the same family

The groove screen has its own BPM readout, separate from the click screen's. Its
number had been given a light-mode value; the "BPM" caption inside it had not, and
was still on `rgba(255,209,102,.28)` — dark-mode amber at 28% alpha, **1.14:1**
against the cream screen, which is fainter than either of the icons fixed in
v0.133.5. Now `#523700`, the same 4.85:1 as its neighbours.

That is three in a row with an identical shape: a child element left behind when its
parent was converted to light mode. The BPM caption inside a converted number, the
icons inside a converted top row. Worth remembering as a place to look rather than a
coincidence — when a light override exists for a container, check what is nested
inside it.

## v0.133.5 — the screen icons had no light mode at all

The BPM label took the v0.133.4 fix; the mute and setlist icons did not, and the
reason is worse than a wrong colour. They had never been given a light-mode value:
both were still carrying the dark-mode `rgba(255,209,102,.4)`, pale amber at 40%
alpha, which resolves to **1.21:1** against the cream screen. That is the lowest
figure anything in the app has measured, and it is why they looked like ghosts.

The previous pass aimed at `.metro-screen-top` and `.screen-bpm-row` and hit
nothing, because the real containers are `#screenTopRow` and
`.groove-screen-bpm-row`. Found by walking up from the icons themselves rather than
by searching the stylesheet for a plausible-looking selector. Both now resolve to
`#523700`, **4.85:1**, verified by reading the computed colour back off all three
icons in the running app.

Stroke and fill are stated explicitly alongside the colour even though both resolve
from `currentColor`, because the paths carry `fill="currentColor"` as an attribute
and an attribute is an easy thing to lose track of later.

## v0.133.4 — the metro screen was hiding text inside its own background

The light-mode contrast audit reports 22 failures. On device, most of them are
fine: the chromatic strip's unlit note names are dim on purpose, the metro subtabs
read clearly, and the bottom-nav labels are flat but legible. Two were real, and
they turned out to share one cause.

The BPM label and the metronome screen's top icons were both a translucent amber
drawn on an amber screen, so the alpha blended them halfway into their own
background: `rgba(122,84,16,.7)` over `rgb(189,171,117)` resolves to roughly 2:1.
Solid `#523700` measures about 4.9:1 on the same ground, keeps the brass identity,
and still reads as secondary to the big BPM number because that number is far
larger.

**An earlier attempt at this made things worse and was reverted**, which is worth
recording. Guessing at what sat behind each element took the failure count from 22
to 39. The reason the guesses were bad is that light mode was being forced by adding
a class after load, while the audit sets a stored preference before it — two
different states, so every measurement disagreed with the last. Reading the same
state the audit reads gave numbers that matched, and the fix landed first time.

The remaining 21 are being left alone rather than silenced. Several are measurement
artifacts of the audit's own method — it samples the 2nd and 90th percentile pixels
of a text node's box, which under-reports contrast badly when a few small glyphs sit
in a wide button. The active metro subtab reporting 1.48:1 while looking perfectly
clear on a real screen is that. The audit is advisory and not one of the seven ship
gates, so a known-noisy signal is better left honest than allowlisted into silence.

## v0.133.3 — the tab fade is gone

Three attempts at a tab crossfade, from 0, then 0.4, then 0.72, each reduced the
flash on the Metro tab without removing it. So this time the fade went instead of
the number.

It was never reproducible here, and that turned out to be the useful fact. Sampled
on every animation frame, the region's opacity rises cleanly from 0.72 with no
bright frame anywhere; scanned across the whole Metro subtree, nothing inside it
animates or transitions during the switch. The most likely explanation is layer
promotion: animating opacity on a 772px subtree hands it to the compositor as its
own layer, and creating that layer can show a frame of unpainted content on some
hardware. The Tuner region is 317px and never showed it, which fits, and it also
explains why a headless desktop browser sees nothing.

Guessing at a fix for a device artifact that cannot be reproduced is how you end up
with four more versions of the same number. The effect was marginal by admission;
the artifact was not. Tab switches return to instant, which is what they were before
any of this and what nobody ever complained about. Folders and modules keep their
shared axis Z, where the motion means something and the regions are smaller.

**Removing it immediately brought back a bug**, which is worth recording. Unwrapping
`setMode` made its internal `exitTool` the outermost navigation call, so tabbing out
of a module fired a Z scale-out: the exact Metro-scales symptom from v0.133.1. It
stays wrapped with a null kind, taking part in the depth guard while animating
nothing.

If tab feedback is wanted later, the nav indicator is the place for it. Animating a
3px bar promotes a 3px layer.

## v0.133.2 — on a dark theme, a crossfade is a dip to black

The remaining blackout on the Metro card had nothing to do with a second animation;
a sweep of every animating element during a tab switch found exactly one, as
intended. It was the fade itself. Fading opacity on a dark theme fades toward a
near-black ground, so what reads as a crossfade on paper is really a dip to black on
screen, and how badly it shows scales with how much lit surface is dipping. The
Metro region is 772px tall against the Tuner's 317, which is why one looked wrong
and the other looked fine at the same setting.

The floor went 0, then 0.4, now 0.72, and the last move is the one that fixes it:
above roughly 0.7 the dip stops registering as darkness and just softens the swap.
Duration trimmed to 130ms to match.

**Full re-check while in here.** Twenty-six navigations driven in a real browser
covering every tab, every Tools folder and tool, every Train hub and exercise, both
directions, plus tabbing out from inside a folder and from inside a module. Each was
checked for exactly one animation, the right kind for the relationship, no animation
on the header, and nothing stale left behind afterwards. Then the whole run again
with the reduced-motion preference set, confirming every path dissolves instead.
Fifty-two navigations, no failures, no console errors.

## v0.133.1 — the Metro scale was a module closing, and the blink was a blackout

Two reports, one shared cause and one of its own.

**Metro appeared to scale where the Tuner did not.** The tab was never the
difference; whether a module was open was. `setMode` calls `exitExercise` on its
way to a new tab, and the train hubs call their own exits, so a single tap ran two
wrapped navigation functions. The inner exit fired a Z scale-out on the region
being left, and the tab's own fade landed on top of it. Leave Metro from a bare hub
and you saw a clean fade; leave it from inside the piano and you saw the scale
first. A depth counter now means only the outermost navigation animates, which is
also just the correct rule: one gesture, one transition.

**Titles blinking out on a tab switch** was the fade starting from fully
transparent. The header sits above the content and never moves, so it gives the eye
a fixed reference against which the content below going to zero reads as a blackout
rather than a crossfade. It now starts at 0.4 and runs 150ms instead of 190ms.

The 8px lift is gone from tab switches too. On a short hub it read as a lift; on a
full-height screen like the Tuner or the Metro, shifting that much content is a
lurch. Folders and modules keep their shared axis Z, which is where a depth cue
actually means something.

## v0.133.0 — the app moves between screens now

Navigation was instant everywhere. The palette crossfaded on a tab switch, over
0.06s, which is fast enough to read as a snap; the content itself teleported,
because panels are toggled with `.hidden`, and `display` cannot be transitioned.
The app had 133 keyframe animations and used none of them to get from one screen
to another.

Two patterns, picked to match what they mean rather than to look busy. **Tabs fade
through**, which Material names for elements with no strong relationship and
illustrates with bottom-navigation destinations; tabs are peers, so nothing there
implies a direction. **Folders and modules use shared axis Z**, which Material
names for parent-child navigation: scale and fade, no travel.

The no-travel part was learned the hard way. An earlier cut grew the new screen
out of the card you tapped, which sounds like Material's container transform and
is not one: that pattern morphs the card's own bounds into the screen's, keeping
the container visible throughout. Scaling a whole new screen up from a point where
a card happened to be is the same idea with the container missing, and it read as
the module scooting in from nowhere. Deleting the translate fixed the feel and
deleted the origin-rect bookkeeping with it.

**Cards cascade on the way down only**, forty milliseconds apart. Never on the way
back, because returning should feel quicker than descending, and never on a tab
switch: Apple's guidance is to avoid decorating interactions that happen often,
and switching tabs is the most repeated gesture in the app.

**Reduced motion dissolves rather than snapping.** The previous convention here was
a 0.01ms duration, which deletes the animation; Apple's position is that removing
animation outright can hurt understandability and that the replacement should be a
fade, and iOS 18's own zoom transition degrades to a standard transition rather
than to nothing. So travel and scale go, a 120ms dissolve stays, and the stagger
is dropped.

**The header does not animate**, by design. It is persistent chrome, and a still
frame is what makes movement inside it legible. It also must never be scaled:
`_fitModuleTagline` measures text width with a Range, and an ancestor transform
would corrupt that measurement.

Implemented as one hook that wraps the fifteen navigation functions after they
run, rather than an edit at every call site. The animation applies to whichever
mode region is showing, since only one panel inside a region is ever visible. It
is enter-only: a true cross-dissolve needs both panels mounted at once and
`display:none` has already removed the outgoing one. Every path was driven in a
real browser, with and without the reduced-motion preference, and checked for
stale animation classes left behind.

## v0.132.16 — the tumbao in octaves

The source line is an acoustic-bass patch, so it is one note per attack, and a bare
single note down at D2 is thin and woolly on a piano. A pianist plays the tumbao in
octaves, so it does now, on both montunos and the Rhodes twin.

The added octave sits ABOVE the source note rather than below. That keeps the
written bass as the floor and puts the definition where it can actually be heard;
doubling downward would have reached D1, which on this instrument is mud. Range is
now D2 to B3, all eighteen events doubled, and still no gaps between a note and the
next attack.

## v0.132.15 — Waldstein and Liebestraum lost their descriptions, and it was my regex

Both rendered as bare cards: title, no composer, no year, no note. The cause was in
v0.132.13, where the montuno metadata was replaced with a DOTALL `.*?\},\n` pattern.
The metadata entries on that line end with `}, ` and a space, not a newline, so the
first `},\n` the pattern could find was two entries further along, and the
replacement quietly took Waldstein and Liebestraum with it. Restored verbatim from
the last upload and pinned, since nothing in the gate set notices a missing
description.

This is the second failure today from a loose pattern on this file, and the
file's own rule covers it: never DOTALL `.*?` here, use bracket matching and assert
what you matched. Both restores were done that way.

**The montuno import itself is clean.** Checked by extracting the note events back
out of the running app and comparing them against the MIDI: 36 events in the 2-3 and
34 in the 3-2, identical to the source in both position and pitch. Whatever is wrong
with the 3-2 is not a transcription error.

**The left-hand durations are also fine, and measurably so.** Each tumbao note
sustains exactly to the next attack, with no gap anywhere: 0 to 1.5, 1.5 to 3, 3 to
5.5, and so on. It is already legato rather than clipped.

## v0.132.14 — accents from the clave track, and twice through

**Accents.** The source is flat at velocity 49 on every note, so dynamics had to be
added; the question was whether to invent them. They are not invented. A note takes
the accent when it lands on a stroke of the file's own clave track, which is data
already in the file rather than a judgement about style, and everything else sits
back at 0.7. In the left hand the beat-4 anticipation takes the weight, since that
is the gesture the tumbao exists for.

It stays a two-level scheme on purpose. The guajeo mostly falls BETWEEN clave
strokes, and how much it does is the actual difference between the two patterns:
4 of 18 notes coincide in the 2-3, 7 of 17 in the 3-2. That tension is the thing
being taught, and heavy accenting would bury it.

**Length.** Both are written out twice, eight bars, which is 16.8 seconds instead of
8.4. Four bars was barely long enough to hear the pattern, let alone play over it,
and repetition is what an ostinato does. Written out rather than looped because the
transport reports a real length and a real end.

**Pedals need nothing.** Both already carry `_riffPiano('pedal',0)` at bar zero and
that is correct and complete: son montuno is played dry, the articulation is the
point, and a wash glues the offbeats onto the downbeats. With the damper model in
place, pedal-up means each note stops at its finger-lift, which is what the written
durations now actually control.

## v0.132.13 — the montuno is a transcription now, and there are two of them

The old Salsa Montuno was an original pattern written to the documented conventions
rather than transcribed from anything, and it did not sound right. It is gone,
replaced by two transcriptions from a public-domain Basic Montunos MIDI, one per
clave direction.

**The clave direction is measured, not asserted.** The source carries a clave track,
and reading it settles which is which: the first pattern strikes 2 and 3 in its
opening bar, then 1, the "and of 2" and 4 in the next, so the two side leads and it
is 2-3. The second reverses. They ship as separate pieces rather than one piece with
a switch, because playing a 2-3 guajeo over 3-2 clave is the crossed-clave mistake
every salsa pianist learns to hear first, and hearing the two back to back is the
lesson.

**Only the piano parts came across.** The file also carries clave and cascara on
percussion channels; those are excluded, because a piano playing its own clave
teaches the wrong thing. The bass tumbao does come across, into the left hand, since
that is what a solo pianist plays: its chord lands on beat 4 of the bar before, which
is where the forward lean lives.

Two things were adjusted rather than copied. Note durations arrived as 0.948 and
0.473 of a beat, a sequencer's gate setting rather than anyone's intent, and are
snapped to the grid the part was obviously written on. Velocity is flat at 49 across
every note in the source, so it is left to the engine default rather than having
accents invented for it; if the guajeo wants accenting later, that is a musical
decision to make with ears.

Tempo stays at the source's 120, which is slower than a dance floor because the file
was written to be followed rather than danced.

The Rhodes twin was cloned from the deleted invention, so it has been rebuilt from
the 2-3 transcription, keeping its tremolo-off and bright-tine voicing.

## v0.132.12 — a song can exist and still not be in the list

Salsa Montuno was missing from the piano picker, and the cause is one the code
made easy. `_riffBuildList` groups piano songs by era, then filters that grouping
against `RIFF_ERAS` to fix the running order, and renders only what survives the
filter. Anything in a group the list has never heard of is dropped without a word.
Montuno was tagged `era:'Afro-Cuban'`, which is not one of the five, so the piece
loaded, held its metadata, sorted correctly, could be launched from a favourite,
and simply never appeared in the bank.

Fixed on both sides. Unknown groups are now appended after the known order instead
of being filtered away, so a typo or a new genre costs a group in an odd position
rather than a song nobody can find. Montuno itself moves to `Other`, an era the
list already renders, keeping its Latin style tag on the Rhodes twin where organ
and Rhodes group by style rather than era.

Checked the rest of the shelf while there, by building each picker for real and
looking for defined songs absent from the rendered HTML: 41 piano, 5 organ and 16
Rhodes, all present, and metadata coverage complete in both directions for all
three. Montuno was the only one hiding.

## v0.132.11 — two strings that never went through the translator

Ran the eleven audit scripts that sit outside the seven-gate set. Nine passed.
The strings audit found nine hardcoded literals, of which seven were false
positives (the literal appears inside the string table itself, or in a comment) and
two were real, both user-facing and both English-only in every language:

The **sustain pedal cap** on the piano and Rhodes wrote `'SUST'` directly.
Now `lbl_sust`, SUST in English and SOST in Italian; both abbreviated because the
cap is narrow, and sostenuto is the word the abbreviation comes from either way.

The **Music Quiz daily badge** wrote `'RESUME'` directly, so an Italian user with a
half-finished daily saw an English word on it. `rr_resume` already existed with its
twin, RIPRENDI, so it reuses that rather than adding a key.

A third hit, the leg tuner's "Show untuned only", is dev-only: it opens from the
console or a long-press on the brand pill and is not on any user path. Left in
English deliberately.

Key parity holds at 1,804 each side with no orphans in either direction.

The contrast audit reports 22 light-mode failures, mostly small uppercase labels in
the tuner and metro at 2:1 against a 4.5:1 requirement. Not touched here: that is a
palette decision across four modules, not a typo, and it wants its own pass.

## v0.132.10 — cleaning up after myself

Adding the Rhodes all-off call to every place the piano voices are cleared was
done with a blanket string replace, and the six-space indented occurrences contain
the four-space string as a substring, so two of them got the line inserted twice at
the wrong indent. Harmless to run and sloppy to read. Removed.

Also went back over two things from this run that were never actually verified
rather than assumed.

**The two-track Rhodes songs were already fine.** They schedule a finger-lift
through `rhodesCardRelease`, which checks the sustain mode and lets the note ring
if the pedal is down. Only the performance path had no note-off, which is the one
that was fixed. The two paths reach the same behaviour by different routes, worth
knowing but not worth merging today.

**The overlay seek lines are correct.** Measured in portrait they came back 12px
wide by 184 tall, which looked like a broken layout until the cause turned up:
`body.ov-portrait-rotate` rotates the whole overlay -90 degrees, and
getBoundingClientRect reports the transformed box. Re-measured at a landscape
viewport where no rotation applies, both read 184 by 12 inside a 200 by 50 screen,
and both render properly: transport and title on top, seek line and times beneath.

## v0.132.9 — the Rhodes had no note-off at all

The pedal moved correctly after v0.132.8 and still changed nothing you could hear,
and the reason turned out to be bigger than the pedal. A Rhodes performance fired
each note and walked away. There was no finger-lift event anywhere in the path, so
every note ran to the end of its sample regardless of what the score said, and the
entire piece sounded as though the pedal had been nailed down in bar one. That is
also why restoring the pedalling in v0.132.6 was inaudible: a damper needs
something to damp, and nothing was ever being held back.

The piano riffs have had a proper damper model for a while. The Rhodes now uses the
same one, which is the right shape for it: a felt pad landing on a tine is the same
mechanism as one landing on a string. A note rings for its written duration, the
finger lifts, and what happens next depends on the pedal. Down, it keeps ringing.
Up, it stops, and everything still sounding only because the pedal was down stops
with it. Release is the sample engine's own recorded release sample rather than a
gain ramp, so damping is click-free without any per-note shaping.

Verified against Clair de Lune with the state sampled twice a second: notes ring on
past their finger-lift while the pedal is down, the count of those collapses to
zero the instant it lifts, and after a stop nothing is left tracked or sounding.

Two smaller things fixed while in there. `riffStop` silenced Rhodes audio through
`stopAllRhodesDrones`, which knows nothing about the new voice map, so the
bookkeeping survived the song; and `rhodesPlayNote` sets its own teardown timer at
the end of a sample, so a note could already be gone by the time its finger-lift
arrived and left a stale entry behind. Both now clear.

## v0.132.8 — nothing was delivering the Rhodes pedal data

Restoring the pedalling in v0.132.6 was necessary and not sufficient. The
performance scheduler built its pedal events with `_riffPiano('pedal', pv)`
hardcoded, whatever instrument was playing, so a Rhodes performance spent four
minutes moving the PIANO's pedal on a tab nobody was looking at while its own sat
still. The arrays were loaded, timed and correct; nothing carried them anywhere.
Pedal events now dispatch on `inst`.

**Which exposed a second thing, worse than the first.** `_riffRhodes('pedal', 0)`
called `stopAllRhodesDrones()`, and that function silences every ringing note. It
is the right behaviour when a person leaves drone mode by hand, and ruinous inside
a performance: Clair de Lune lifts the pedal 163 times, so every one of those would
have chopped the whole texture dead. The hard stop now only fires when leaving
drone mode, which a performance never enters.

Verified by playing Clair de Lune on the Rhodes and sampling: the sustain state
changes four times in the first thirteen seconds, the card pedal toggles its
engaged class with it, the voice count keeps climbing and falling naturally
through pedal lifts instead of collapsing to zero, and the piano's pedal stays out
of it entirely.

**Worth knowing, and not fixed here:** on the sample path the Rhodes pedal is
visual only. `rhodesPlayNote` plays the sample to its natural end regardless of
sustain state; only the synth fallback lengthens its decay. So the pedal now moves
correctly and truthfully reflects the performance, but it will not sound different
while the electric piano samples are loaded.

## v0.132.7 — the organ console had twelve controls and songs could reach five

Before authoring any organ automation, the plumbing needed checking, and it was
worse than the earlier note suggested. `_riffOrgan` routed drawbars for both
manuals, Leslie, percussion on/off, percussion harmonic and the vibrato/chorus
selector. Percussion decay, percussion volume, the VIB UPPER and VIB LOWER
rockers, the VOL rocker and the HOLD latch all had working setters, and
`_riffRestoreState` was already saving and restoring their state around a song,
but nothing connected song data to them. Six controls sat there unreachable.

The volume rocker is the one that matters. On a real console the swell pedal is
how an organist phrases a line, and NORM/SOFT is the two-step version of that;
without it a song can change its registration but not its dynamics.

All six are routed now, HOLD refreshing both its pedals for the same reason the
Rhodes fix did. Verified by driving each control through `_riffOrgan` in the
running app and reading the state back: twelve for twelve, including both
nine-drawbar manuals.

No song data changed. The five organ pieces still set their registration at bar 0
and never move, which is the next job and the one that needs ears.

## v0.132.6 — the Rhodes gets its pedal back, and three songs that suit it

**Pedal.** Seven Rhodes performances shipped with `ped: []` because an earlier pass
decided a Rhodes has its own sustain and stripped it. It does have its own sustain,
and it also has a damper: felts lifting off tines, the same job a piano's lift off
strings. Stripped, the pedal sat frozen on screen through an entire performance and
the sustain stayed flat.

The seven are the same captured performance as their piano twins, note arrays
identical byte for byte at the same tempo and bpm, so the pedalling transferred
exactly rather than being invented: 1,706 events across Clair de Lune, Moonlight,
Barcarolle, Träumerei, To Spring, the E minor Prelude and Liebestraum. Checked in
the running app, every array spans its piece and lifts after the final note.

**Three songs for the Rhodes bank**, taking it from 13 to 16, all converted from the
piano bank and voiced for tines rather than hammers:

- **Salsa Montuno.** Tremolo off, bright. A wobble fights the clave and the guajeo
  needs its edges; the pattern is percussive, not sung. The electric piano is the
  standard salsa comping voice, so this is the one that most belonged here already.
- **St. Louis Blues.** Soft tremolo, warm tine. The Stage sound from soul records.
- **Blues Lick.** Soft tremolo, bright. A twelve-bar lick wants the attack to define
  each note.

All three keep their pianos' pedal-up marking, which was a deliberate call there and
is the same call here: blues and montuno piano is played essentially senza pedale,
and a wash glues the offbeats back onto the downbeats.

Organ control automation is still untouched and remains the biggest audible gap: all
five organ songs set their registration at bar 0 and never change Leslie speed again.

## v0.132.5 — the seek line only ever knew about the piano

Organ and Rhodes had a play/pause and a stop and nothing else: no seek line on the
card, none in the expand overlay. The transport was never instrument-aware.
`_riffScrubEls()` returned a hardcoded pair of piano element ids, so the render
loop and the drag handler had two surfaces to talk to and the other four did not
exist as far as the player was concerned. It now queries `.np-scrub` and finds
whatever the markup actually contains, because a hardcoded list is a list that
forgets the next instrument.

Both instruments gained a seek row under their riff bar, copied from the piano's,
and their overlay screens changed from the single-line compact panel to the same
stacked LCD the piano overlay uses: transport and title on top, seek line
underneath, inside the one panel. Only the playing instrument's line lights up.
Measured in the running app: all three read 346px wide by 14px tall with the
correct totals (organ 2:33, Rhodes 4:07, piano 2:45), fills advancing, no errors.

**The Rhodes sustain pedal had two separate problems and only one of them was a
bug.** `_riffRhodes('pedal')` and `_riffRestoreState('rhodes')` both refreshed
`rhodesPedal` and never `rhodesFullPedal`, so in full screen the pedal sat still
no matter what the song did. The piano has always refreshed both. There is now one
`_rhodesRefreshPedals()` and both call sites use it.

The second is not a bug and has not been touched. All seven Rhodes performance
songs carry `ped: []`, and the file says why: "Pedal stripped (Rhodes has its own
sustain)." Their piano twins carry 103 to 391 pedal events over byte-identical
note arrays at the same tempo and bpm, so the data could be restored exactly, but
that changes how those seven pieces sound and is a decision rather than a repair.

## v0.132.4 — the scale name never fitted its own box

The card did not shrink in the move. Measured both builds side by side and the
name box is 350px wide and 75px tall in each, character for character; the
clipping was already there and Scales moving into Reference just put it in front
of someone.

`.scale-name-big` was declared twice. The real rule sets 36px on a 1.04 line
height, which is the pair that makes the pinned 75px box hold exactly two lines,
and its comment says as much. A second copy sat further down in the leftover
Scale Reference block — `.scale-display`, `.scale-notes`, `.scale-select`, none of
which appear in the markup any more — setting 40px on a line height of 1. Being
later in the file, it won. At 40/1 two lines want 80px, so even a short name was
five pixels over its own box before anything wrapped to three, and
"E NATURAL MINOR · AEOLIAN" wrapped to three and got sliced through the middle,
top and bottom at once, because the text is flex-centred in a fixed height inside
a card that clips its overflow.

The duplicate is gone. That alone is not enough: three lines at 36px still want
112px, and a name like that genuinely needs three. Growing the box is the wrong
trade, since the pin is what stops the tape below jumping every time the scale
changes, so long names shrink to fit instead, down to a 20px floor.

Checked across every scale in the library at three roots, at 320, 360 and 412, in
both languages: 84 names each pass, none clipped, and the smallest any name had to
go was 24px, so the floor is not doing any work yet. The longest strings are
"F♯ NATURAL MINOR · AEOLIAN" in English and "F♯ DOPPIO ARMONICO MAGGIORE" in
Italian.

## v0.132.3 — Scales was never a Train module

It sat alone on the Train hub, full width, under a section label called "Explore"
that existed for nothing else. The case for moving it was already written into the
file: it never calls `progUpdate`, so unlike the thirteen exercises that do it
earns no XP, keeps no stats and reaches no achievement; its own subtitle reads
"look it up · hear it · play along"; and a comment beside the removed IMPROV tab
already refers to it as "the Scales tool". It is now the fourth card in
Tools > Reference, beside Circle of Fifths, Interval Reference and Vocal Range,
which is the company it was always keeping.

Not a merge with Tonal Center, before anyone asks. They share the drone engine
and nothing else: Tonal Center listens to you sing against the drone, Scales just
plays.

**The screen had to physically move.** `#exScales` lived inside `.train-only`,
which CSS hides outside the Train tab, so re-pointing the card without moving the
markup would have opened a blank tool. The id keeps its `ex` prefix on purpose:
about twenty-five CSS rules key off `#exScales` for its drone-mode skin, and a
cosmetic rename across all of them buys nothing anyone can see.

Rewired throughout: out of EXERCISE_NAME_KEYS, EXERCISE_SUB_KEYS, EXERCISE_PANELS,
MIC_EXERCISES and the exercise back-label map; into TOOL_NAME_KEYS, TOOL_SUB_KEYS,
TOOL_FOLDER_MAP and MIC_TOOLS, with `scalesInit` on the enterTool path and
`scaleStop`/`droneStop` on the exitTool path. The in-page back button was still
calling `exitExercise`. Reference went from four tools to five, badge included.

**Two things that would have quietly cost people something.** The favourite pin
key stays `exercise:scales` rather than becoming `tool:scales` — the registry is
keyed by string and `tool:musicquiz` already lives in the Games hub, so the prefix
and the placement never had to agree, and renaming it would have dropped the pin
of anyone who had starred it. And the Everything In Its Right Place achievement
tracks visits by key, which went `e:scales` to `t:scales`; an old `e:scales` still
counts, so nobody has to walk back and re-earn it.

Pro gating is unchanged, since Scales was in neither FREE_TRAIN nor FREE_TOOLS
before or after.

**Two stale strings on the way past.** The Train tour still told people scales was
on its own card. And the Tools hub tagline claimed "six utilities in three groups"
when there are fifteen in five; a tagline that counts things is a tagline that
goes stale, so it describes instead.

## v0.132.2 — the green subtitle was Chordle, three screens ago

A screenshot of RHYTHM TRAINING came in with its subtitle rendered in lime.
Sampling the pixels off it gave #c1e095, which is `--in-tune` (#b6f25b) with a
JPEG's opinion applied; the TUNER tab label in the same shot sampled #a4a5b9,
exactly `--text-dim`, so the palette was fine and the tagline alone was wrong.

`#headerTagline` is a single element shared by every screen, and modules write
inline styles onto it directly. Solve a Chordle and it fades out, swaps to the
progression's name and sets `tag.style.color = 'var(--in-tune)'` as a small
flourish. The only code that ever clears that again is Chordle's and Diadle's own
daily-reset paths. Leave the game any other way and the green leaves with you,
through folder headers and into other modules, since inline styles outrank every
rule in the stylesheet.

`_resetTaglineInline` wipes colour, opacity, transform, transition, font-size and
the length bucket, and both owners of the element call it before they write:
setHeaderModule, setHeaderSection, and the root branch that restores the INTONARE
tagline. Blunt on purpose. The alternative is chasing each new inline style to its
own cleanup site, which is the race that was already lost once here.

Reproduced against the previous build first, which reported rgb(182, 242, 91) on
the Rhythm folder header after a simulated win, then confirmed back to
rgb(163, 165, 184) on this one. Not a regression from the subtitle work; it has
been reachable for as long as Chordle has had the flourish.

## v0.132.1 — the module header was sizing the title as if it owned the row

A screenshot of Notation Cards showed its tagline reading "know the marks on the
pa...". Chasing that turned up something larger sitting underneath it.

Module headers put the title and its italic subtitle on one flex row and called
`_fitHeaderTitle` on the title. That function finds available width by walking up
to the first ancestor WIDER than the element it is fitting, which is right for a
shrink-wrapped inline box and wrong here: when the title overflowed its row, the
walk stepped straight past the row to the header and reported a width the title
never had. Italian RICONOSCIMENTO ACCORDI rendered 283px inside a 264px row and
the fitter called it comfortable, so the TITLE was being clipped, not merely the
subtitle. It also never subtracted the subtitle's width, so every title was sized
as though it had the whole row, and the subtitle got whatever fell off the end.

`_fitModuleTagline` replaces that call and measures against the row itself, which
is known at the call site. Title first, since the title is content: it shrinks to
its 15px floor only if it does not fit alone. The subtitle then takes what is
left, shrinks to its 9px legibility floor, and if it still does not fit it is
removed rather than ellipsed. A half word trailing three dots reads as breakage;
an absent flourish reads as a decision, and the module's full description is on
its card regardless.

Measured, not counted. The device font-scale setting changes rendered width, so
no character-count rule survives contact with a real phone; the fitter asks the
browser at runtime instead.

**Seventeen subtitles were also simply too long for a header.** The file's own
rule, written when Staff Notes and Relative Pitch were fixed, is three or four
words, and a good few had drifted well past it. Trimmed in both languages, which
took the subtitles dropped at 320px from ten to one in English and twelve to five
in Italian. The stragglers all sit behind titles long enough that no subtitle
would fit beside them: INTERVAL REFERENCE in English, and in Italian CERCHIO
DELLE QUINTE, NOTE SUL PENTAGRAMMA, INTONAZIONE RELATIVA and RICONOSCIMENTO
ACCORDI. Those hide cleanly now instead of showing a fragment. Nothing is clipped
at 320, 360, 390 or 412 in either language.

## v0.132.0 — the folder subtitles were answering the same question twice

Every folder carried a subtitle, and no two of them agreed on what a subtitle was
for. Eight named their contents; Reading described itself. Underneath that sat a
second, entirely separate family of subtitle strings, `folder_X_subtitle`, fully
written and fully translated, that nobody had seen in months: it lives in the
in-page `train-header`, and CSS hides that header whenever `body.in-section` is
on, which is always, once you have opened a folder.

The visible string was doing two jobs at once. On the hub card it is the only
preview of what is inside, so naming the tools earns its place. In the folder
header it sat directly above cards reading CIRCLE OF FIFTHS, VOCAL RANGE and
SURVIVAL GUIDE while itself reading "Circle of Fifths · Vocal Range · Survival
Guide". A label that repeats the labels below it is not telling you anything.

Split by surface. The card names the contents; the header describes the folder.
That put the dead `_subtitle` family back on screen, where four of the nine were
already written in the right voice. The other four were lowercase echoes of the
tool names and have been rewritten, Tools > Rhythm never had one at all and now
does, and all nine were measured in the running app at 320, 360, 390, 412 and
768 in both languages: single line everywhere, worst case the Italian Reference
string at 185px in a 264px box.

**Three things that were simply wrong, found on the way through.** The Reference
folder holds four tools and its card claimed three, omitting Interval Reference
from both the subtitle and the badge. The Games card had a hardcoded fallback
predating Road Trip, so it listed four of five whenever the string table was not
consulted. The Reading card's fallback still read "Staff Notes" alone, from
before Notation Cards shipped.

## v0.131.7 — the mega pass, and the deck was in the wrong order

Chord symbols were the one pack that had never been source-checked. All five
qualities confirmed: the triangle is major seventh, the circle diminished, the
slashed circle half-diminished (minor seventh flat five, 1-b3-b5-b7), the plus
augmented, and the letter after a slash is the bass note.

**A contradiction scan across all 138 glyph cards with a SMuFL description:**
zero conflicts. Up against down, above against below, open against closed, sharp
against flat, first against second. Nothing in a definition contradicts what the
spec says the glyph is.

**Then the visual pass found a real one, and it was structural.** The cards are
authored in two blocks — font glyphs, then the drawn ones — so each pack's drawn
cards landed after its glyph cards and split nine confusion groups into two
separate runs. Whole rest and half rest sat 120 cards away from the other rests.

Worse, the contents list emits a group header only the FIRST time it meets a
group, so that second run appeared with no header of its own, filed silently
under whichever group happened to come before it. Anyone opening the index
looking for the whole rest would have found it listed under something else.

Sorted once at load, by pack and then by the order each group first appears. All
nine groups are single runs now, the seven rests are contiguous, the index has 36
headers and no duplicates, and every card still renders at one height with its
distractors intact.

That is the fourth time this session the fix was ordering or registration rather
than the thing itself — panels, back-map, folder list, favourites, and now the
deck's own sequence.

---

## v0.131.6 — cards that describe instead of instruct

Daniele caught staccato reading shaky, and the bass clef saying "the left hand"
of nothing. Both right, and scanning for the same shapes found two more.

**Staccato hedged so hard it never said what to do.** "Detached from the note
that follows; how short depends on context." Every word is defensible — strictly,
the only thing you can infer from a staccato dot is that the note is not legato —
but a card that qualifies before it instructs teaches nobody. It now says to
shorten the note and leave a gap, and keeps the qualification after.

**Staccatissimo had the same problem** and only made sense read directly after
staccato: "Always very short, regardless of context" never mentions shortening.

**Bass clef said "the left hand"** with no instrument attached. The treble card
says "the right hand at the piano"; this one had lost the referent, so it read as
the left hand of whatever you happened to play.

**Tenuto-staccato** said "slightly separated but held", which specifies neither
how long nor how separated.

All four fixed in English and Italian, and every card still measures 348px with
nothing clipped in either language.

The scan also flagged a dozen cards for stating what something is NOT — laissez
vibrer, harmonic, let ring, arpeggio, the tab staff. Those are left alone: each
contrasts against the default behaviour, which is the informative part. A
harmonic really is defined by touching the string instead of pressing it.

---

## v0.131.5 — full pass over the session

Everything built since v0.120.0, re-verified in the final file rather than
trusted from when it was written.

**One real find: "centre" in the C clef definition.** The US spelling sweep at
v0.117.0 corrected 772 instances across the app; I then wrote 181 new cards and
put a British spelling straight back in. It was the only one — every other card
is clean — but it is a good illustration of why a sweep is not a permanent state.

Everything else held:

  Version synced across all three spots. All seven gates pass, read individually.
  Folders each render exactly their own modules, Games included.
  Zero leaks across 24 exercise-to-folder jumps.
  All six modules back out to their own folder, Music Quiz included.
  181 cards in both languages: one card height, no missing ink, no missing text,
  nothing clipped.
  A full English test scores 10/10, 100%, +20 XP, drill hidden on a clean run.
  A quit run changes XP by zero.
  Shuffle stays on the card, is fresh each time, resumes in place, leaves the
  deck alone.
  Index: 181 rows, none broken, exact deck order with shuffle both on and off.
  Casual counters never unlock Flawless Victory; a completed run does.
  Removing a pin removes it and launches nothing.
  No page errors anywhere in the sweep.

One check reported a false failure again — the index order looked wrong because
the row's textContent includes the SVG label text on drawn cards, so "P.M." was
being read as part of the name. Comparing the name element directly: all 181 in
exact order. Third time this session a test has been wrong rather than the code,
which cuts both ways and is worth remembering.

---

## v0.131.4 — Daniele's tour copy

His wording, applied. Better than mine in the place that matters: "bowing,
blowing, or bending" does in three words what my version explained in a clause,
and naming the three kinds of set up front is clearer than leading with the
instrument case.

Two changes to what he sent. The shuffle button is on the CARD, not inside the
index, and the sentence as written put them together — that would send people
looking in the wrong place. And XP is capitalised everywhere else in the app.

Italian written to match rather than translated literally: "arco, fiati o
bending" keeps the same three-beat shape, and bending stays in English because
that is what Italian players say.

All three steps fire, selectors resolve, and each body fits its card without
scrolling.

---

## v0.131.3 — the tour, held to the standard the sweep set

The rewrite an hour ago failed the rules the v0.118.0 tour sweep was written to
enforce. Written in the same session as everything else, and never read back
cold against them.

What was wrong with it:

  "These are the marks that sit around the notes rather than the notes
  themselves" — the not-X-but-Y construction, explicitly banned.

  "when you want the deck to stop being predictable" — quippy.

  "the wrong answers are always things you could plausibly have picked rather
  than something obviously unrelated", and "so reading through the deck can
  never be mistaken for practice" — explaining our own design reasoning to the
  person using it. They do not care why the distractors are chosen that way;
  they care that the wrong answers are hard.

  "the card teaches on the way out" — a flourish.

Five steps for a module whose card, deck size and TEST button are all on screen
and labelled. The sweep collapsed the two hub tours to one step each on exactly
this reasoning: only say the thing that is hidden.

Three steps now, 46 / 24 / 32 words. Picking a set, because the instrument pools
are worth choosing and the reason is not visible. Browsing, because tapping the
counter opening an index is not discoverable and neither is the shuffle button.
And the test, because only it earns XP. The deck itself needed no step; it is on
the screen behind the card.

---

## v0.131.2 — the tour catches up with the module

The Notation Cards tour was written at v0.121.1, when the module was browse-only
with 17 dynamics cards and a button that cycled between two packs. Everything it
described has since changed and it had never been revisited.

It never mentioned TEST at all — the primary action, and the only thing that
earns anything. It described packs as a cycle when the picker is now a grid with
curated instrument pools. And it predated both shuffle and the contents list, so
two features had no explanation anywhere in the app.

Five steps now: the deck, choosing a set, browsing, the test, and what counts.
The pools step leads with the reason they exist rather than the mechanism — a
guitarist gets bar lines and repeats and never bowing — because that is the part
worth knowing. The last step keeps the design decision out loud: only the test
earns XP, browsing earns nothing, and an abandoned run scores nothing at all.

Verified in the app: all five steps fire in order, every selector resolves at the
moment the tour runs, and Italian is twinned throughout.

This is the same failure mode as the tour sweep back in v0.118.0 — tours drift
silently because nothing checks whether what they describe still exists. The tour
audit confirms a tour is PRESENT and its selectors resolve; it cannot know the
words are describing a button that was replaced three builds ago.

---

## v0.131.1 — removal removes, and a perfect score means something

**Removing a pinned module also launched it.** The long-press timer fired the
removal but never cleared its own handle, so lifting the finger ran the tap path
too: it saw a live timer and no movement, closed the sheet and opened the module
it had just deleted. The press now marks itself as spent. Verified: the item is
removed, the sheet stays open, and nothing launches.

**Flawless Victory was unlocking off casual play.** It fires when an exercise
reports correct equal to total over at least ten attempts — but Chord Ear, Pitch
Match, Staff Notes and Relative Pitch all report RUNNING session counters that
tick upward while you are still playing, so ten right in a row during practice
unlocked a legendary. A perfect score now requires `runComplete`: a scored run
with a defined start and end. Verified both ways — twelve of twelve on running
counters does not unlock; a completed ten-question test does.

Notation Cards' test mode sets that flag. The other exercises need their own pass
to decide which of them have a real completed run; until then they no longer
award it by accident. Anyone who already has the achievement keeps it.

**The pool and contents sheets scrolled the page behind them** once their own
content reached the end. Both now contain their scroll.

**The tap lag is NOT the JavaScript, and I have not blind-fixed it.** Measured:
entering a module costs 3ms for Notation Cards, 7ms for Staff Notes, 8ms for
Intervals, 35ms for Road Trip. None of that is perceptible. The delay is paint or
transition, and the fix would mean restructuring `enterExercise`, which is shared
by fifteen modules and is exactly where the panel-list and back-map misses have
happened. Not something to reorganise speculatively on the way into a build.

---

## v0.131.0 — shuffle, and the contents list stops saying undefined

**43 rows in the contents list were broken.** Every row built a font glyph from
the card's codepoint, but a drawn card has no codepoint and no font metrics
either, so those rows rendered "&#xundefined;" at a NaN size. They now render
their SVG. Checked: 181 rows, 0 containing undefined or NaN, 43 carrying a
drawing.

**Shuffle.** Top left of the card, crossed arrows when on and parallel when off.

It is an ORDER over the deck rather than a reordering of it, which is what keeps
the contents list alone: the deck stays in its natural sequence and only the path
the arrows walk changes. Verified against each thing you asked for — toggling
leaves you on the card you were already looking at, the walk is not sequential,
each switch-on builds a fresh order, turning it off resumes the natural order
from wherever you are rather than jumping, the deck order is untouched, and the
contents list reads in deck order regardless.

Changing pool or preset rebuilds the order, so a shuffle never outlives the deck
it was built for.

One note on the verification: my first check of the contents order failed, and
the code was right — the test selector was picking a nested span inside a drawn
card's artwork rather than the name. Compared directly, the two orders are
identical.

---

## v0.130.3 — everything in its right place

Staff Notes was appearing in Games. It is not in Games: the folder registries and
the hub markup are both correct, and every folder renders exactly the modules it
should. What was happening is a leak.

**Opening a folder never closed the module already open.** `exitExercise()` hides
the panels, but changing folder is a second way out of an exercise and nothing
called it — so going Reading, into Staff Notes, then straight to Games left Staff
Notes sitting on top of the Games hub. It looked like a misplaced module and was
a stale one.

All four folder entry points now close any open exercise first. Tested as a
matrix, six exercises against four folders, 24 combinations: no panel survives
the jump.

**Two registry gaps found by the same scan.** Music Quiz was never added to
`GAMES_EXERCISES`, so backing out of it landed on TRAIN rather than GAMES — the
identical miss notationcards had, sitting there since Music Quiz shipped. And
Notation Cards had no entry in the favourites registry, so pinning it would have
produced a tile with no label and no icon. Both fixed, and the favourites entry
follows the `launch:` convention its neighbours use rather than the shape I first
wrote.

That is now four separate hand-maintained lists a new module has to join: the
panel list, the back-map, its folder list, and the favourites registry. Nothing
checks them against each other, and something has been missed in every one.

---

## v0.130.2 — third sweep, on the dimensions never looked at

The first two sweeps kept finding things, so the question was whether a third was
worth it. Repeating a check that already came back clean finds nothing; each
sweep had paid because it looked at a different dimension. So this one went at
the four that had never been examined at all.

**Switching language mid-test broke the answer marking.** The option buttons are
built once per question and carry no i18n key, so they kept their old-language
text while `ncName()` switched under them — and the right answer was found by
comparing button text to the card name, which then matched nothing. The green
highlight landed on no button at all.

Two fixes. The right answer is now identified by card ID rather than by text,
which cannot drift. And `applyLang` calls a relabel hook, so a live question, its
prompt, its reveal and the missed chips all follow the language. Verified in both
directions, including switching while a reveal is on screen: options follow,
the right answer stays marked, and the marked one is the correct one.

**Edge cases hold.** Every pack off falls back to the whole deck rather than an
empty one. A six-card pack builds a six-question test rather than padding to ten
or crashing. A confusion group with only two members still yields three
distractors through the widening fallback.

**The pool choice survives leaving and re-entering** the module.

**And light mode, which this module had never once been seen in.** Glyphs, drawn
cards and the stand-in notes all measure 10.7:1 against the stage; the name
11.9:1 and the definition 10.2:1 against the card. Nothing washes out, no
hardcoded colour leaked in — every surface uses theme variables, which is what
the light-mode remediation established and what the tone-bank rule exists to
protect.

---

## v0.130.1 — second pass, including the Italian

**Italian terminology checked against Italian sources**, not written from memory:
legatura di valore for the tie (same pitch, sums the duration) against legatura
di portamento for the slur (different pitches, articulation) — a pair that is
easy to swap and that the cards get right; punto di valore, which lengthens the
note by half its value; corona, stanghetta, bequadro, pentagramma; and the
semibreve / minima / semiminima / croma / semicroma chain. All confirmed.

**Functional sweep across both languages.** Every one of the 181 cards stepped
through in EN and IT: all render ink, all have a name and a definition, none
empty. Distractors drawn 60 times per language: always exactly three, never the
answer itself, never a duplicate label. A full ten-question run in Italian scores
10 / 10 and awards its XP, which matters because the correct-answer check
compares button text to the card name — if any site had missed the language
accessor, Italian would have scored zero.

**And the sweep found what eyeballing had not.** The reveal box in test mode
clips longer definitions: 8 in English and 14 in Italian. Browse gives the
definition 70px to itself with a group line beneath; the reveal has to fit the
name as well, so it needed that height back. Harp harmonic's English definition
was 144 characters and too long for any box; trimmed without losing the
instruction, since the bracketed fret is already drawn on the card.

Both cards now measure 348px in both modes and both languages, and nothing clips
anywhere.

---

## v0.130.0 — Italian for all 181 cards

Names and definitions, every card, using the `nameIt` convention the instrument,
interval and tuning tables already use. Verified 181 of 181 have both fields and
none is empty.

**The dynamics cards are not translations.** "Piano means quiet" teaches an
English speaker something and an Italian speaker nothing, because the vocabulary
IS Italian. Those seventeen teach the convention instead: that the mark means
volume and not touch, that it is always relative, where it sits on the ladder,
that the gap between mp and mf is the narrowest on the scale. Same card,
different lesson.

**Note values use the Italian names**, which follow the British system rather
than the American: semibreve, minima, semiminima, croma, semicroma — not
"nota intera". Rests likewise, and the clefs are chiave di violino and chiave di
basso.

Guitar keeps the English technique names players actually read — bend, tapping,
slide, palm mute — while using the real Italian where one is in normal use:
barre, capotasto, pizzicato alla Bartok.

**Every place card text is shown now goes through one accessor.** Browse, the
test reveal, the answer buttons, the contents list, the missed chips. Checked
that no site still reads `.name` or `.def` directly, because missing one leaves
the module half-Italian — and the answer buttons in particular would have scored
wrong, since the correct-answer check compares button text to the card name.

**Two layout fixes the Italian forced.** Italian names run longer and wrap to two
lines, so the name slot needed a fixed height like the definition slot already
had; without it the card grew and the layout jumped between languages as well as
between cards. Card heights now measure a single value, 326px, in both modes and
both languages, with no clipped text anywhere.

---

## v0.129.4 — the drawn cards checked against engraving rules

The last unverified set: the 43 drawn cards, which have no SMuFL glyph to check
against. The guitar ones were already drawn to the Hal Leonard legend and the
bend descriptions; this covers the standard-notation ones.

**Rest positions were right, proportions were not.** A whole rest hangs BELOW the
fourth line and a half rest sits ON the third — both correct, and both land in
the third space, one filling its upper half and one its lower. But the height
should be half the distance between staff lines, and mine was 7px against a 9px
space, near enough a full space. Both rects are now half a space tall and about
1.6 spaces wide, which is what makes the hanging and sitting legible rather than
the block simply filling the gap.

Checked and correct as drawn: the multi-bar rest (thick bar centred on the staff,
vertical caps at each end, count above), first and second endings, slur and tie
curves, the ottava and trill and pedal lines, the tuplet bracket, the glissando
line and the courtesy accidental.

That closes the accuracy pass. Every card in the module has now been checked
against something outside my own memory: 140 glyph cards against the SMuFL
codepoint tables and classification, 181 definitions against published sources,
and 43 drawings against Hal Leonard's legend or standard engraving practice.

Still open: Italian for all 181 cards.

---

## v0.129.3 — the strum arrows were backwards

Went back over how much of the module had actually been verified and the honest
number was worse than I had been saying: 65 of 181 definitions source-checked,
116 not.

**All 116 names cross-checked against SMuFL's own glyph descriptions first** —
free, and it proves no card points at the wrong symbol. All 116 match. So the
glyphs are right and only the explanations were in question.

**Then the explanations, and the strum pair was reversed.** A downstroke moves
toward the floor and sounds the LOWEST string first; an upstroke moves toward the
ceiling and sounds the HIGHEST first. Both cards said the opposite. This is the
error most likely to have actually taught someone something false, because a
beginner has no way to catch it and the two cards sit side by side confirming
each other.

**"Indicio" is not the Spanish for index finger.** The right-hand fingering card
glossed p-i-m-a as pulgar, indicio, medio, anular. Indicio means a clue. It is
indice. That has been wrong since the very first draft of the deck and survived
every pass, including one where I read the card aloud in a changelog.

Everything else in accidentals, note values, rests, navigation, pauses, chord
symbols and the staff pack checked out: accidental duration to the end of the
bar, the note-value chain, whole and half rest positions, the barlines, the
octave and pedal marks, the clefs, the chord-symbol qualities and the slash
chord.

Running total on definition errors found by checking rather than assuming: 5 in
dynamics and ornaments, 8 in strings and winds, 3 here. All 16 were in cards
that read perfectly plausibly.

---

## v0.129.2 — strings and winds get their source pass

The 26 cards that had never been checked against anything. Eight were wrong.

**Sul ponticello was the wrong technique entirely.** Sul ponticello is bowing
NEAR the bridge; this glyph is `stringsBowBehindBridge`, which is bowing BEHIND
it, on the short length between bridge and tailpiece — a different technique with
a different sound. SMuFL's own description reads "Bow behind bridge (sul
ponticello)" and I inherited the spec's looseness. Checked: there is no SMuFL
glyph for sul ponticello at all, because it is written as text. The card is now
"Behind the bridge".

**Buzz pizzicato buzzes against the FINGERNAIL**, not the fingerboard. Snapping
against the fingerboard is Bartok pizzicato, which is the card directly beside
it — so the two cards described the same thing and one of them was wrong.

**Fouetté arrives from the air.** Mine said it "starts from the string", which is
the one thing a fouetté is not: the bow is lifted and whipped back down onto the
string, usually up-bow near the tip.

Also corrected: bowing ON the bridge keeps the hair on the strings, hence quiet
and squeaky rather than a scrape; a flip is a turn off the note; scoop is
specifically a lip slur from about a semitone below; plop is a rapid descent onto
the note.

Half harmonic now says what the mark asks for — press only partway, between a
stopped note and a harmonic — rather than describing a tone I could not source.

**Verified correct and left alone:** down and up bow, harmonic, snap pizzicato,
left-hand pizzicato, thumb position (the thumb works like a capo, which is the
movable-nut framing the card already used), doit, the three falls, brass bend,
the three tone-hole cards, multiphonic and mouthpiece pop.

---

## v0.129.1 — an audit against the spec's own data

Daniele asked whether there is a repository or database for this rather than me
fixing one card at a time. There is, and I should have gone looking before the
fourth alignment pass.

**The W3C publishes SMuFL's own classification** — `classes.json`, 85 classes
over the whole font — and it settles by data what I had been assigning by hand:
which glyphs are articulations, which are ornaments, which are rests or clefs or
barlines. Checked against every card: 96 carry a class, and all 96 agree with the
attachment mode I had given them. That is the first accuracy claim on this module
that is not me marking my own homework.

**Bravura's own metadata is the bigger prize and I could not reach it.** SMuFL
fonts ship a metadata file carrying `glyphsWithAnchors` — `stemUpSE` gives the
exact point where a stem meets a notehead, in staff spaces — and
`engravingDefaults` for stem and staff-line thickness. Those are precisely the
numbers I derived by hand from outlines over the last four builds. Steinberg's
copy is not at any path reachable from here; MuseScore's Leland metadata came
down and confirms the schema, but its values describe Leland, not Bravura, so
they cannot be used. Worth another look from a machine with wider network access.

**New gate: `intonare_notation_audit.py`.** Checks that every codepoint resolves
and matches the id claiming it, that attachment agrees with SMuFL, that no two
cards share a codepoint, and that every confusion group has something to confuse
with. Needs `glyphnames.json` and `classes.json` beside it.

**It found a real bug on its first run.** Trill and Arpeggio each existed twice —
once in Ornaments, once added again during the guitar rewrite — so two cards
pointed at one codepoint. In a test that is a question with two correct answers,
the sf/sfz trap I had explicitly designed against. Merged: packs are a list, so
the surviving card simply belongs to both. 181 cards, and Guitar still counts 47
because nothing was lost.

---

## v0.129.0 — bends drawn from the sources, not from memory

Daniele called out that I was chasing fixes rather than checking against real
notation, and he was right: every previous pass redrew these from memory and then
verified geometry I had chosen myself. This one starts from published
descriptions.

**Bend arrows were the wrong shape.** A bend is a CURVED arrow leaving the note
and turning upward, with the interval label at the PEAK of the arrow. Mine were
straight vertical arrows with the label off to one side. All eight redrawn:
half-step, whole-step, slight, bend and release, unison and grace-note bend now
bow out of the fret number and turn up under their label.

The one that was already right turns out to have been right by accident: a
pre-bend genuinely is a straight vertical line, because the string is bent before
it is struck. That is now deliberate rather than lucky.

**Grace-note bend was greying its fret number.** MuseScore's convention is that
grace-note bend fret numbers are CUE SIZED. It is small now, not faded.

**Rake now runs into the note.** Practically you drag across the muted strings
and land on the target, so the Xs sit directly under the fretted note on the
strings you cross, not floating above it on a separate part of the staff.

**And the whammy text is w/bar**, no space, which is the default MuseScore uses.

183 cards, 43 drawn, every card 296px, nothing overflows, no page errors.

---

## v0.128.1 — guitar cards get their tab

Daniele's on-device pass found things a contact sheet at desk size did not.

**Rake was pointing the wrong way.** You rake INTO a target note, and dragging
from low strings to high puts the muted strings BELOW the fretted note. Mine had
the Xs above and the note on the bottom string, which is a rake nobody plays. The
target note is on an upper string now with the muted strings under it.

**Three cards were a bare symbol where the technique is the point.** A lone C
tells a learner nothing about a barré; it now shows one fret stopped across all
six strings with the bracket that marks it, and half barré across three. A T over
a notehead does not show that tapping is a two-hand move; it is tab with the
tapped fret, a slur, and the fretted note it pulls off to. Muffled strings and
the rhythm slash likewise needed strings to sit on.

**Text was overlapping its own dashes.** "let ring" ran into its extension line,
"P.M." into its dashes, "w/ bar" into the -1, and "full" into the pre-bend hold.
All given clearance.

**And one conversion I got wrong.** I put the string number on tab, where the
line the number sits on already tells you the string — the mark only means
anything on a staff. Reverted to a staff note.

183 cards, 43 drawn, every card 296px, nothing overflows.

---

## v0.128.0 — the drawn cards land

**183 cards.** The 38 that SMuFL cannot represent are in: slur, tie, the eight
bends, both slides, hammer-on, pull-off, all four harmonics, the tab conventions,
the ottava and trill and pedal lines, the tuplet bracket, first and second
endings, the multi-bar rest, the courtesy accidental, and the two rests that need
a staff line to be told apart. Drawn to the Hal Leonard legend where one exists.

The card list carries the SVG directly, so a drawn card is data like any other
and the pools pick them up: Guitar goes from 74 to 109, Staff from 19 to 27,
Beginner from 30 to 35.

Swept all 38 rendered through the app's own renderer, as before. Three wrong.

**Tremolo picking was the wrong concept, not a wrong drawing.** It showed two
fret numbers with strokes between them, which is a fingered tremolo — alternating
between two pitches. Tremolo picking is one note picked as fast as possible. It
is a single fret number with strokes on it now.

The **tie** curve dipped to y 50 inside a 48-tall viewBox and was being clipped;
both tie and slur are rebalanced within their box. And **wide vibrato** was
barely deeper than plain vibrato, which is the entire distinction between them.

Verified in the app: all 183 render, every card still 296px, no drawn card
overflows its stage, no page errors.

---

## v0.127.3 — flags push the head sideways

Last build anchored the plain note cards vertically on the notehead and left the
horizontal axis alone. A flag hangs off the right of an eighth or sixteenth note
and widens the bounding box that way, so centring on the box puts the NOTEHEAD
6.8px left of centre on the eighth and 7.1px on the sixteenth — visible against
the quarter note, which has no flag and sits nearly true.

The renderer only ever applied a vertical shift. It takes a horizontal one now,
and the six note glyphs with a stem or flag carry a `dx` computed from the font:
the distance between the glyph's bbox centre and its notehead's centre.

Measured across whole, breve, half, quarter, eighth and sixteenth: every notehead
is 0 from the stage centre, matching a composed card's head exactly.

---

## v0.127.2 — plain notes anchor on the notehead too

**The tremolo fix in the last build was wrong.** I moved the strokes with
`translate(9px, calc(50% + 4px))`, and a percentage translate resolves against
the element being moved — the 30px slot — not against the stem. That pushed them
19px down, straight onto the notehead. The vertical translate is gone entirely:
the slot already bottoms out just above the head, which puts the strokes across
the stem without being told to. Measured: on the stem to within 1px horizontally,
inside the stem's span vertically, 4px clear of the head, on all three cards.

**Plain note cards were anchored differently from composed ones.** A composed
card centres the notehead on the stage; a bare quarter or eighth note centred its
whole glyph, which puts the head below centre by half a stem. Flipping between
them moved the head. The eight note glyphs — half, quarter, eighth, sixteenth,
both grace notes, whole and breve — now carry a notehead-anchored offset computed
from the font rather than their bounding box. Measured: every one sits at 0 from
the stage centre, the same as a composed card's head.

---

## v0.127.1 — looking at all 145

Rendered every card through the module's own renderer into contact sheets and
read them, rather than measuring. Measurement can prove a thing is where I put
it; it cannot say the thing is wrong. Three problems, and the third is a notation
error rather than a layout one.

**Marks were touching the notehead.** The gap measured a consistent 0, which I
had recorded as a pass. Consistent, but wrong: notation leaves roughly half a
staff space, or the mark reads as part of the head. 5px clearance.

**Tremolo strokes sat at the far end of the stem** instead of crossing its
middle, which is where they belong.

**Eight brass articulations had no direction.** A scoop or plop leads INTO a note
and a doit, fall, flip or bend leaves it — they attach to the notehead on the
correct side. All eight were rendering above the head, which made a fall look
like it rises. Scoop and plop are now `before`, the five falls and bend are
`after`.

The rest checked out against convention: articulations on the notehead side with
the stem turned away, accidentals at head height, grace notes visibly smaller
than the note they lean on, the arpeggio spanning its chord, rests and clefs and
barlines all correct.

---

## v0.127.0 — the notehead is the anchor

Four rounds of nudging the composition and the augmentation dot still was not
beside the fat part of the note. Measuring the font explains why: in
`noteQuarterUp` the notehead centre sits at y -16 while the glyph's bounding box
centre is y 367. Anything aligned to that glyph lands 22px above the head. Every
fix so far had been aligning to the wrong point.

The stand-in note is no longer the composite glyph. It is a `noteheadBlack` with
an absolutely-positioned CSS stem, so the element's box IS the notehead and every
alignment is exact by construction rather than by offset. The stem adds no height
and cannot shift anything.

Full sweep over all 71 composed cards, measuring the gap between mark and
notehead rather than centre to centre — centre distance is SUPPOSED to vary with
the mark's height, which is why the earlier checks looked wrong when they were
not:

    before   7px, one value        after   7px, one value
    grace    7px, one value        above   0px, one value
    stem     0px, one value

Row modes align dead on the notehead's centre line (dy 0 across every card).
Tremolo strokes are offset 9px onto the stem, which runs from the right edge of
the head, instead of being centred over the head.

---

## v0.126.4 — the note is the centred thing

The last two fixes stopped the note moving between cards but left it off-centre
on the stage, because the symbol and note were still being balanced as a PAIR:
centring the group puts the note off to one side by half the symbol's width. On a
sharp it leaned right, on the augmentation dot it leaned left.

The composition is a three-track grid now, with the note in the middle track and
the symbol hanging off whichever side it belongs on. Measured across all 71
composed cards: the note's centre is offset from the stage's centre by 0 in every
one of the six modes.

Getting there took one wrong turn worth recording. In column mode I first put the
mark in grid column 1 and the note in column 2, which gives the grid two columns
and centres the note inside ITS column rather than on the stage — the offsets came
back scattered from 3 to 26px. Both live in column 2 now, different rows.

---

## v0.126.3 — and stops wandering vertically

The same bug on the other axis, which the last fix did not touch. A column sized
to its contents moves the note up or down depending on how tall the mark is: a
staccato dot is 4px of ink and a staccatissimo wedge is 14px, so the note sat in
a different place on each.

The mark now gets a fixed 30px slot, bottom-aligned. Bottom rather than centre
because that is also what the notation asks for — an articulation sits a constant
distance from the notehead whatever its own height, rather than being centred in
whatever space it happens to need.

Verified across all six composition modes: each one resolves to exactly one note
position, x and y. Above 197,267 across all 57 cards; grace, beside, stem, before
and after each a single pair of their own. Nothing overflows the stage.

---

## v0.126.2 — the note stops wandering

Three complaints, one cause. The symbol and its stand-in note were laid out as a
plain centred flex row, which centres the PAIR — so the note slid left or right
depending on how wide the symbol happened to be. A flat and a natural are
different widths, so the notehead landed somewhere different on each card, and
flipping between them looked like the note was drifting.

Each side now gets a fixed 54px slot: the symbol moves within its own half and
the note lands on the same pixel every time. Measured across sharp, flat,
natural, double sharp and double flat: identical x and identical baseline.

**The augmentation dot sits beside the notehead now**, not floating at the
vertical centre of the whole glyph. On a stem-up note the head is at the bottom,
so the accidental and dot slots align to the bottom rather than the middle —
which is also where an accidental belongs.

**And every card is the same height.** The definition was a minimum rather than a
fixed height, so a three-line definition (treble clef) made that card taller than
a one-line one and the whole layout jumped as you flipped. All 145 now measure
296px, verified by stepping through the deck and collecting the distinct heights:
one value.

---

## v0.126.1 — scale, after the scale changed

`NC_SCALE` was 1.65, tuned when every glyph was normalised to roughly the same
ink height. Switching to one uniform font-size made the tallest glyph 99px of ink
BEFORE scaling, so a treble clef was rendering at 163px inside a 104px stage. Now
1.15, with the stage at 124px, and every one of the 145 verified to fit.

**My overflow check could not have caught that**, which is the part worth
recording. It measured `.nc-g`, the span that carries `line-height: 0` and
therefore reports zero height no matter how much ink spills out of it. It
returned "none" on a build where clefs were half again taller than their
container. It now measures the `.nc-gb` wrappers, which carry the real ink
height. Third time this session a check has measured the wrapper instead of the
thing.

Composed cards were oversized for the same reason and now sit correctly: the
stand-in note is 59px against a 6px staccato dot, which is the true ratio.

**The contents list drew every symbol at full card size**, so a treble clef ran
down across five rows. Each row now scales its glyph to fit its slot on BOTH
axes — height alone still clipped the wide dynamics like pppp against the side —
and the slot clips anything left over. Cards carry a width for this.

The counter gave no sign it opened anything. It has a list icon now.

---

## v0.126.0 — one font size, and the notes that were missing

**The sizing approach was wrong from the start.** I was normalising every
glyph's ink height, which meant computing a different font-size per glyph — a 41
to 1 spread across this set, since a treble clef is 1.98em tall and a tenuto line
is 0.05em. Stroke weight scales with font-size, so normalising height necessarily
distorts weight. That is the "some feel thin, some feel stretched" exactly.

SMuFL is designed the other way round: every glyph works at ONE size, 1 em to 4
staff spaces, and ink height is meant to vary. Every card now renders at 50px.
Stroke weight is identical everywhere and relative sizes are the ones the font
was drawn for.

**Which exposed a thing I had never ported.** At true scale a staccato dot is 4px
of ink, and on its own that is not a card, it is a speck. The stand-in note
composition existed in the review sheet and never made it into the app — the
`mode` field was sitting in the card data doing nothing. All six modes are in
now: 57 cards above a stem-down note so the mark is on the notehead side, 5
accidentals before a notehead, the augmentation dot after one, 3 tremolos on the
stem, 2 grace notes leaning on a full note, 3 arpeggios beside a chord. 74 cards
stand alone and should.

A bug caught while porting: dimming the stand-in with `:not(:first-child)` would
have dimmed the augmentation dot instead, because in `after` mode the note comes
first. The note pieces carry their own class now.

**Curated pools are pruned rather than blanket.** Pulling in a whole pack drags
along cards the player never meets: Guitar was including the C clef, the
percussion clef and all three piano pedal marks. Pools take a `drop` list, by
card name or confusion group, and a card in the pool's own instrument pack is
never dropped. Guitar is 74 cards and no longer contains a sustain pedal.

**Presets show their state.** They highlight when the selection matches them, and
Everything now switches every pack on rather than clearing the grid, so the
selection always shows what it includes. Hand-toggling any pack drops back to
Custom.

**And a contents sheet.** Flipping one card at a time through 145 to reach the
one you want was the wrong interaction for a deck this size. The counter is now a
button: grouped list, each row showing the symbol and its name, tap to jump.

---

## v0.125.0 — all thirteen packs

**145 cards, up from 17.** Generated straight from SYMBOL_DECK.md, so the deck
document is the source and the app is the build product rather than a second copy
to keep in sync. Dynamics 17, Guitar 21, Staff 19, Winds & brass 15, Ornaments
12, Strings 11, Articulation 10, Chord symbols 9, Pauses 7, Note values 7,
Navigation 7, Accidentals 5, Rests 5.

Every glyph verified to render real ink: stepped through all 145 with the font
loaded and checked none came back empty. The Bravura subset already covered them,
so no font work was needed.

The curated pools have something to curate now. Guitar draws 74 cards, Woodwind
73, Strings 69 — each their own pack plus the general notation that instrument
actually meets on a page.

**38 drawn cards are deferred.** Slur, tie, the bend family, the tab conventions
and the rest have no SMuFL codepoint and exist only as SVGs in the review sheet;
porting those is its own pass.

**Two layout fixes.** The test card measured 274px against browse's 266 because
the reveal slot and the prompt slot did not match the definition and name they
replace; both are pinned now and measure identical. And the counter read "1 /
100" — the score was butted straight onto the question count with nothing between
them. It now reads "1 / 10 · 0 right".

---

## v0.124.0 — one bar, and the name where it belongs

**The bar was the thing that moved.** Browse and test had separate bars of
different heights, so starting a test shifted everything below them. There is now
one bar that never moves and only swaps its contents: pool chip and TEST on the
left and right in browse, progress and QUIT in test. Measured: bar height delta
0, card top delta 0.

**Rhythm Cards looks better and I finally rendered it side by side instead of
guessing.** Three concrete differences, all now matched:

The name sits ABOVE the figure. Burying it underneath made the card read as an
image with a caption rather than a card about a thing. TEST is a solid filled
accent button, not another outline chip in a row of outline chips — it is the
primary action and now looks like one. And the pool chip is small and
left-aligned rather than a full-width block, so the bar has a shape instead of
being two equal slabs.

Navigation is circular prev/next flanking the counter, same as Rhythm Cards,
rather than three equal full-width blocks.

The test card gains a WHAT IS THIS? prompt in the same slot the name occupies in
browse, so the card body does not reflow between modes either.

---

## v0.123.1 — the glyph was eating the taps

**QUIT did nothing, and the reason is worth writing down.** The glyph span
carries `line-height: 0` so its box collapses to zero height while the ink spills
far outside it. At the sizes this module uses, that invisible zero-height span
was lying on top of the progress row and swallowing every tap aimed at QUIT.
`elementFromPoint` on the button's own centre returned `nc-g`. It now has
`pointer-events: none` — it is decoration, nothing about it should be a hit
target — and the stage clips its overflow. Verified with a real tap rather than
a scripted click, which is what hid this the first time.

**A third hand-maintained registry.** `READING_EXERCISES` decides which hub the
back button returns to, and an unregistered exercise falls through to TRAIN. That
is now three lists a new module must join — panels, back-map, and this — none of
which any audit knows about, and I have missed a different one in each of the
last three builds.

**The pool picker is a grid now**, matching how Rhythm Cards does categories:
packs toggle on and off, and presets overwrite the selection rather than sitting
beside it as a parallel list. That is what stops a pack appearing under two
names. The label reads Everything with nothing filtered, the pack's own name for
one, the preset's name when the selection matches it exactly, and Custom
otherwise.

Two duplication bugs came out of that. Single-pack presets repeated the grid
directly beneath them, so Dynamics is a pack tile only. And Beginner is a
curation rather than a subject, so it is a preset only. Separately, a preset
whose other packs do not exist yet collapsed to the same selection as a single
pack — with only dynamics live, turning dynamics on reported itself as "Guitar".
Only live presets are matched now.

**The card no longer jumps** between browse and test; both are pinned to the same
minimum height, measured identical at 266px.

---

## v0.123.0 — pools, an exit, and a result worth reading

**The leak was mine and my last fix was wrong.** `exitExercise()` hides
everything in `EXERCISE_PANELS`, a hand-maintained list, and I wired the module
into `enterExercise` without ever registering it there. So it was shown on the
way in and never hidden on the way out, by any route. What I patched in v0.122.1
was `exitReading()` — one exit path out of several — which fixed the symptom on
the route I happened to test and left every other one leaking. The panel is now
in the list and the patch is reverted.

**Pool selection replaces the cycling button.** Three kinds, and the curated ones
are the reason to bother: a guitarist needs bar lines and repeats as much as
bends and gets nothing from bowing, so Guitar pulls in dynamics, articulation,
staff and navigation alongside the guitar pack. Woodwind and Strings do the same
with ornaments. Presets are Beginner and Everything; By subject is the raw packs
for drilling one thing.

Curated pools carry a `req` — the pack that makes them worth existing. Without it
all three instrument pools would show the same count while claiming to be
different things, since today only dynamics has cards. They stay hidden until
their own pack lands. Verified by injecting a guitar card: Guitar appears
immediately at 18, correctly pulling dynamics in with it.

**There was no way out of a test but to finish it**, which is a trap rather than
a design. QUIT sits in the progress row. An abandoned run scores nothing and
awards nothing, because it is not a result.

**The finish screen was a number in a box.** Now a ring that fills to the score,
the percentage, the XP earned, and — the part that matters — the names of what
you missed. "8 to work on" tells you nothing; eight names tell you whether you
are confusing a whole family or just guessed badly once.

---

## v0.122.1 — chimes, a still layout, and the folder bug

**Answer cues were never wired.** Both branches called `hapticLight()`, a
placeholder, so a wrong answer felt exactly like a right one and neither made a
sound. Now `hapticCorrect()` + `playCueCorrect()` and `hapticWrong()` +
`playCueWrong()`, which respect the cue choices in Settings like every other
exercise.

**The layout shifted on answer.** The reveal appeared out of nothing and pushed
the option grid down the screen at the exact moment your finger was on it. The
reveal now reserves its height and fades in; measured, the option row's top is
identical before and after answering.

**The classic folder bug.** `exitReading()` swapped the hubs and never hid the
open exercise, so backing out left the module sitting behind the hub. It now
hides both Reading modules first. Worth noting this is a shape the app has hit
before, and nothing checks for it: no audit knows that leaving a folder should
close what was open inside it.

Reading's folder badge still read "1 exercise". Now 2, both languages.

**Visual polish.** The symbol floated in a large empty panel; Rhythm Cards works
because the figure sits ON something. The glyph now has its own inset stage with
a hairline and a subtle inner highlight, the card tightened around it, the
progress counters became pills, and the options got a real press state. Same
type scale as Rhythm Cards so the two decks read as one family.

---

## v0.122.0 — Notation Cards test mode

Ten questions, four options, reveal on answer, drill your misses. Notation Cards
is an exercise now rather than a reference.

**The distractors are the whole design.** They come from the card's confusion
GROUP intersected with the active PACK, which is why `grp` has been a field on
every card since the data was written. Four random wrong answers would make every
question free, because nobody confuses a segno with a fortissimo; the drill only
teaches anything when the wrong answers are things you could plausibly have
picked. Loudness cards draw from the loudness ladder, sudden accents from each
other. Verified over 40 draws: always exactly four options, and the only
off-group cases are crescendo and diminuendo, whose group has just two members,
so the widening fallback fires as designed.

**XP is test-only, by decision.** Two per correct answer, awarded once at the
end. Verified that twenty browse flips move XP by zero, so the deck cannot be
farmed by flipping cards. A drill run pays the same per answer as a clean one,
because replaying your worst cards should not be worth less than a lucky first
pass.

The definition lands on the ANSWER, not the question — that is the teaching
moment, and putting it on the card would give the answer away. Right answers
advance after 900ms, wrong ones hold for 2100ms so the reveal is actually read.

Entering the module always lands on browse, so a half-finished test cannot be
walked back into from the hub.

Verified end to end: a ten-question run scores, awards XP, offers the drill and
hides it on a clean sweep; a deliberately perfect run reads 10 / 10, "Every one."
and no drill button. No page errors.

---

## v0.121.2 — sizing, icon, and the copy Reading had outgrown

Glyphs were scaled 2.2x, a number carried over from the standalone review sheet
where cards sit in a narrow list. On a full-width card it overshoots. Now 1.65
and behind a single `NC_SCALE` constant, so it can be nudged on device without
hunting through the render function. Card height 293px to 259px.

The module icon was a bordered rectangle with a plus in it, indistinguishable
from any other card-shaped icon in the app. It is now a two-card deck with a
fermata on the face: reads as notation at 24px and does not collide with Staff
Notes' stave-and-note beside it.

**And two strings that had quietly gone stale.** Reading's subtitle read "Staff
Notes · treble & bass" and the hub hint described only Staff Notes, both written
when Reading had exactly one module in it. The subtitle is now "notes on the
stave · marks on the page" and the hint covers both, in both languages. Neither
was flagged by any audit, because nothing checks whether a folder's description
still matches its contents; it only showed up in a screenshot.

---

## v0.121.1 — Notation Cards tour

Three steps, closing the gap the tour audit flagged the moment the module
landed: an exercise with no tour at all, which also breaks the welcome tour's
promise that picking a module gets you one.

The deck itself, the packs, and browsing. The third step carries the design
decision out loud — reading cards costs nothing and earns nothing, the scoring
lives in the test — so nobody spends an evening flipping cards expecting XP.

Tour audit back to 0 missing and 0 broken. All three selectors verified present
at the moment the tour fires, and the tour confirmed auto-firing on first entry
rather than only on a title-hold.

---

## v0.121.0 — Notation Cards, first slice

Reading's second module. Browse only, dynamics only: 17 cards, every one read
line by line before a keystroke of this went in.

**Bravura is now embedded.** A 149-glyph subset of Steinberg's SMuFL font
(SIL OFL 1.1), 19KB, base64 inlined as an @font-face. The app previously named
Bravura in a few font-family rules with no font behind it; notation was drawn
from hand-extracted SVG path constants. Reserved Font Name, so the subset keeps
the name and Steinberg needs a line in Credits & Thanks before this ships
publicly. The same subset covers all 183 cards in the full deck, so no further
font work is needed as packs land.

**Each card carries its own font-size and baseline shift**, computed from the
glyph's real bounding box. This is the part that is not obvious: Bravura em-boxes
vary enormously, a treble clef being four staff spaces tall and a staccato dot a
speck, so one font-size makes clefs overflow and dots vanish. Displayed ink is
clamped by a power law instead. Flat normalisation is equally wrong: it makes a
clef and a dot the same height. The glyph also needs a fixed-height wrapper or
its translateY leaks into the layout.

Packs are a LIST on each card rather than a category, so Beginner is a curation
of 8 of these 17 and nothing is written twice. The pack button cycles for now; a
picker comes with the second pack.

**Two bugs found in testing, both in the wiring rather than the module.** With no
entry in `EXERCISE_NAME_KEYS` the header fell back to `k.toUpperCase()` and read
NOTATIONCARDS. And the pack label was set by textContent alone, so switching
language mid-session left it in English; it now carries the i18n key on the
element and `applyLang` picks it up like everything else.

Not in yet: test mode, XP (test only, by decision), the distractor logic, the
drawn cards, the other 166 cards, and Italian for any card text. Module chrome is
EN/IT twinned; card definitions are English until the twins are written.

**A sentinel pin drifted and I shipped anyway before catching it.** The pin
asserted that `staffread` and `relpitch` were ADJACENT lines in
EXERCISE_SUB_KEYS; inserting `notationcards` between them broke the literal
string while leaving the guarded behaviour completely intact. Adjacency was
never the fix being protected — having a tagline entry each was — so the pin has
been split into two that assert exactly that, and the count moves 190 to 191.
The sentinel is green. The process failure is the point worth recording: the
gate said do not ship and the build shipped in the same command, because the
copy step was chained onto the gate with && rather than gated on reading it.

---

## v0.120.1 — Rhythm Cards

The rhythm deck was called FLASH CARDS, which names its format rather than its
contents. A notation symbol deck is coming to the Reading folder on the same
chassis, and two cards both labelled FLASH CARDS would have been
indistinguishable in the two places the app shows a module name with no folder
around it: the launcher's pinned row and the header star sheet. Both are now
named for their subject. Rhythm Cards in Tools, Notation Cards in Reading when
it lands.

Nine live strings, not one. The i18n value in both languages, the hardcoded DOM
default beside it, the folder subtitle in both languages and its DOM default, the
tool's own help text (which already called it "RHYTHM FLASH CARDS", so the card
label was the odd one out), the tools-hub hint in both languages, the launcher
tour's Italian body, the module tour's step title, and the favourites registry
entry. That last one supplies the label for the pinned row, which is exactly
where the collision would have been invisible.

Italian is Carte Ritmiche throughout. Only the section banners and code comments
still say FLASH CARDS, and those are internal.

---

## v0.120.0 — Coming Soon goes away

The Train hub's Coming Soon section and its two cards, MELODY DICTATION and
SCORE READER, are removed. Neither is cancelled and neither has been superseded;
a first public release that advertises two unbuilt exercises just reads badly.

Worth recording accurately, because the reason given was not quite the reason:
Relative Pitch was NOT one of the cards still sitting there. It and Chord
Progressions were pulled back in July as genuinely obsolete, since the shipped
Relative Pitch module and Chordle cover them. What remained were the two that are
still real gaps.

The i18n strings, the `wip_toast` and the `.practice-card-btn.wip` / `.wip-badge`
CSS all stay. Restoring a card is markup only, and the strings are already
twinned EN/IT.

Train now reads: four folders (Ear Training, Rhythm Training, Games, Reading),
then Explore with Scales. Nothing else on the hub referenced the removed cards;
the practice tour dropped to one step in v0.118.0 and never pointed at them.

The build path is unchanged and still one path with something shippable at each
rung: staff renderer, then staff note ID (shipped as Staff Notes), then melody
dictation, then score reader. Dictation needs the renderer plus sequence
playback; score reader needs both of those plus the mic scoring Road Trip already
proves works. Score Reader is still the differentiator nobody else has, in that
none of musictheory.net, tonedear, tonesavvy or teoria listens while you read.

---

## v0.119.2 — copy stops being a secret

The two support rows carried a chevron, which promises a sub-screen. Contact
opens a mail composer and Share opens the system sheet, so neither earns one, and
the rows read as inert. They now carry a COPY chip instead.

That does more than relabel. Copying was the silent fallback from v0.119.1, the
thing that happened only when the mail client or share sheet failed, and a device
with no mail app configured fails with no error at all. Promoting it to a visible
control means the reliable route is the one you can see. Text rather than a glyph
because the app's vocabulary is mono and letterspaced, and the slot one section
up already holds "38 MS".

The parent Support row keeps its chevron. Disclosure is the one thing a chevron
honestly means, and that one already rotates to show state.

Feedback moved from the sub-line to the chip. The sub-line carries the row's
description, and swapping it made the row flicker between two meanings; the chip
just reads "Copied" in --in-tune for 1.6s. Share text is now built by one
function so the chip and the row cannot drift apart.

**Two faults in my first pass at this.** The chip came out 26px tall, which is
not a touch target; it is now 40px, which fits inside the existing ~66px two-line
row without changing the row's height. And my test for whether tapping the chip
also fired the row used a capture-phase listener, which runs *before* the target
handler can call stopPropagation, so it reported a leak that was not there and
would equally have missed a real one. Re-tested by wrapping the row's actual
function: it does not fire.

---

## v0.119.1 — both support rows were no-ops

Shipped two buttons that did nothing. Both my fault, and both fail silently,
which is why the gates and the headless check waved them through: the functions
ran, threw nothing, and produced no effect.

**Share.** Every tier of `intonareNativeShare` ends at `copyFn`, and I passed
`null`. With the Capacitor Share plugin present that does not matter, but opening
`Intonare.html` directly rather than through the installed app means no plugins
at all, and `file://` is not a secure context so `navigator.share` is undefined
too. Tier 1 skipped, tier 2 skipped, tier 3 called a null. A guaranteed no-op in
exactly the way the file gets tested. It now passes a real clipboard ladder
(Capacitor Clipboard, async API, execCommand textarea) and confirms on the row.

**Contact.** `window.location.href = 'mailto:'` is not reliable inside a WebView:
a non-http scheme is resolved in `shouldOverrideUrlLoading`, and a scripted
navigation does not always reach it, so the tap is swallowed with no error and no
mail app. Now built as a real anchor and clicked, which goes through the normal
link path that Capacitor and Android both handle, and the element is removed on
the next tick. A device with no mail client still fails silently and cannot be
detected, so after 900ms — unless `document.hidden` says the mail app took over —
the address is copied to the clipboard and shown on the row.

Feedback goes on the row rather than swapping button text the way the daily
puzzles do, because these rows carry a two-line label and swapping the text would
eat the description. The chevron becomes a tick and the sub-line carries the
message for 1.8s.

**A race in the first version of that fix:** the address line and the "Link
copied" confirmation both wrote `.sm-link-sub`, so which one you saw depended on
whether the clipboard promise had resolved. `supportCopy` now takes the message
as an argument and there is one writer.

Verified with clipboard permissions granted: share copies the full text and
restores the description after the timeout, contact copies the address and leaves
it on the row, no stray mailto anchors left in the DOM, no page errors.

---

## v0.119.0 — settings stops being a pile

The tail of Settings had grown to five identical full-width boxes, and adding a
sixth for the support sheet was what made it obvious. The problem was never the
count; it was that the boxes were the same weight while doing different kinds of
thing. Re-run Welcome Tour and Calibration act on the app. Privacy, Credits and
now Support only open something else. Identical slabs for both meant nothing
grouped and nothing receded.

Actions stay buttons. Openers became one bordered group with hairline dividers
and a right chevron, under a new ABOUT heading. Six boxes down to three, and the
new row cost no visual weight at all because it joined a group instead of
extending a stack. The chevron reuses the slot where Calibration puts its "38 ms",
which was already the best-reading row down there.

**The support sheet.** Two rows for now. Get in touch opens a mail composer to
intonare.dev@gmail.com with version, platform, language and viewport prefilled in
the body, so a bug report arrives with a build number instead of "it doesn't
work"; platform comes from `Capacitor.getPlatform()` with a web fallback, and a
missing mail client falls back to showing the address rather than failing on a
tap. Share reuses `intonareNativeShare`, the same helper the daily puzzles use.

No Rate row yet: it needs a listing that is not live, and a button pointing at a
dead URL is worse than no button. No donation row either. Google's position on
developer tip jars is genuinely unclear (their documented policy covers charity
donations, and the Play community threads asking about BuyMeACoffee have no
public resolution), but the deciding factor is that the Pro unlock already runs
through store billing, and an external payment link beside an existing IAP is
exactly what anti-steering rules are written to catch. Not worth the risk on the
build that goes in for its first production review.

Also checked and worth writing down, because it is the opposite of what the
tester report suggested: the "are you enjoying this app?" pre-prompt is
prohibited. Google's Developer Program Policies name it directly, and Apple
treats routing happy users to the store and unhappy ones to a form as review
manipulation. The sanctioned version of that instinct is Apple's own advice to
keep support contact easy to find, which is what this build adds.

**One flaw the first render caught.** The support panel was appended after the
group, so tapping row one opened a panel below row three. It reads as a different
control opening. The rows are now nested directly beneath their own trigger with
a 28px inset and a `--surface` fill, and the trigger's chevron rotates to show
state.

Strings are EN/IT twinned and verified at two definitions each. Gates: syntax
clean, sentinel at 97 + 190, backup audit at 48 keys, no page errors, both themes
rendered at 412x915.

Still sitting in the file for launch: `smResetProBtn` carries a comment reading
"Strip this button + resetProTesting() before production launch." It is hidden
unless Pro is active, so it is invisible today, but it ships.

---

## v0.118.0 — the tours stop lying

A systematic pass over all 34 tours against what their modules actually contain
now. Tours were written when each module shipped and several never kept up.

**The hub tours were the worst, and the fix was deletion.** TOOLS ran five steps
and TRAIN ran six. Between them they listed every folder's contents by name,
which is text the hubs already print on screen in their own card subtitles, and
those subtitles were current while the tours were not. `folder_ear_sub` reads
"Intervals · Chords · Pitch Match · Relative Pitch"; the tour listed three.
`folder_games_sub` reads "Chordle · Diadle · Tónale · Road Trip · Music Quiz";
the tour listed four. `folder_reading_sub` exists at all; the tour had no Reading
folder. TOOLS opened "Thirteen tools in five folders" and then correctly listed
fourteen across the next two steps. TRAIN's mic step named Chord Ear Training,
which is not in MIC_EXERCISES, while omitting Scales and Road Trip, which are.

Both are now one card. They are menus, not modules, and everything a tour could
say about them is already on the screen behind it, printed correctly. What is
left in each card is the one genuinely hidden thing: pinning is a 500ms
press-and-hold on a hub card, with no affordance anywhere. The old TOOLS step
told people to "tap the ★ button in any tool", which does not exist for this
purpose; that star is `svc-save-star` in Charts and it saves diagram views.
Eleven steps became two, and neither can go stale again, because neither counts
anything or names a module.

**Survival Guide was described as the wrong tool.** Its sections are DYNAMICS,
THEORY, GUITAR, BASS, PLUCKED, STRINGS, WINDS, BRASS, FREE REED, PERCUSSION,
PIANO, VOICE, THEREMIN and PEDALS. The tour called it "a quick-reference music
theory guide" and listed intervals, chords, scales and notation, describing one
section of fourteen as though it were the whole thing.

**Progression and Chord Player were rewritten.** Both were label narration: "Set
the key and scale here", "Plays the selected chord". Chord Player's first two
steps were one idea on two cards. Progression's first step talked about key and
scale while spotlighting `#progAddBarBtn`, the wrong control entirely.

**Three features got a clause each** where the feature changes what you are
practicing rather than just doing a thing: rhythm reading's LISTEN FIRST versus
SIGHT READ, the tonal centre's EQUAL TEMP versus JUST, and the polyrhythm
challenge modes. Drumkit's presets and kits were deliberately left out; they are
labelled buttons on screen and exploring answers them.

Smaller: music quiz dropped two hard counts ("over a thousand questions across
nineteen packs"). Three steps stopped opening by restating their own title.
Verb agreement in the metronome RAMP step, a dangling clause in the piano
keyboard step, a missing conjunction in the tone bank list, and a comma in the
Charts quality step that read as a list of three things. The "handy for" tic
appeared five times across the tours and is down to zero; four
superlative-shortcut constructions went with it. And the three newest tours
(relpitch, roadtrip, staffread) were the only ones in the app written without a
single contraction, which made the warmest writing also the stiffest; they now
match everything else.

**Two mistakes worth recording, both mine, both caught before shipping.**

I deleted the metronome tour. The TOOLS rewrite sliced from `"  tools: ["` to
`"  practice: ["`, and `metronome:` sits between them in the object, so the slice
swallowed all six of its steps. Nothing caught it: syntax passed, the sentinel
passed, the tour audit reported 0 missing and 0 broken because it only checks the
tours that exist. It surfaced only because a later `str.replace` on the RAMP step
asserted count==0. Restored from the shipped baseline and verified at 34 tours
with all six steps and every selector resolving. Index-pair slicing across a
sorted object is not safe when the endpoints are not adjacent; a diff of every
tour's step count against the previous build now runs as part of this work.

I also invented two facts in new copy. I wrote that Music Quiz survival ramps
difficulty as the run gets longer; `mqStartSurvival` sets `qCount=50` with no
escalation, and what it actually offers is pack selection. And I wrote that the
polyrhythm challenge gets harder as you go; `prOpenChallenge` builds a picker
with per-card locks (`prHardcoreUnlocked`, `prEndlessUnlocked`), so the truth is
harder modes that unlock. Both were plausible, both were fabricated, and the only
reason they did not ship is that I went back to read the functions. Separately, I
typed British spellings into new copy twice within an hour of sweeping them out
of the file, and named an Italian button "LETTURA A PRIMA VISTA" when the label
reads "LETTURA VISTA".

Gates: syntax clean across 9 blocks, sentinel at 97 fixes + 190 pins, backup
audit at 48 keys, tour audit 0 missing and 0 broken, US sweep reports nothing
left, and every rewritten tour verified rendering at 412x915 with no page errors.
Tour count 34 before and after; step count 137 to 128.

Three audit tools added: `tour_weight.py` (step counts and body lengths),
`tour_tone.py` (hand-holding tells and title echoes) and `tour_drift.py` (each
module's control labels beside its tour's step titles).

---

## v0.117.0 — one dialect

The app was already inconsistent with itself: identifiers American
(`practiceHub`, `mode:'practice'`, every CSS `color:`), visible copy drifted
British. Daniele is US-based, so the copy moves rather than the code.

772 replacements across 58 distinct forms. The big ones are colour (185), centre
(105), grey (88) and centred (66); the long tail runs through theatre, programme,
equaliser, organise, recognise, memorise, prioritise, labelled, modelling,
cancelling, travelling, neighbour, behaviour, catalogue and favourite. Comments
were swept too, not just user-visible strings: leaving them would have meant
building perfect comment detection purely to preserve a second dialect nobody
reads, and the classification is the risky part, not the replacement.

**What was protected, and why.** A blind find-and-replace on this file eats
`AudioContext`, `createAnalyser` and every design note we have. So the identifier
collisions were enumerated first by scanning every `class=`/`id=`/`data-*`
attribute, every CSS selector, every `function`/`const`/`let`/`var` declaration
and every object key in the file. The full set turned out to be small: the
element ids `mst-analyse` and `mp-analyse`, the i18n KEY `metro_tab_analyse`, the
mode string `'analyse'` the metro subnav switches on, `analyser` and
`analyseVibrato`, a local `centre` in the capo solver, and the `underCentre`
property in a layout diagnostic. Those are masked. `GREY` in the woodwind diagram
renderers is handled by case: lower and Title case sweep, ALL CAPS does not.
Verified after writing that all ten survive at their exact original counts.

The i18n key `metro_tab_analyse` keeps its name while its value became ANALYZE,
which is the split that matters: the label on the button is what people read, the
string the handler switches on is not.

**Two bugs in the audit tooling itself, caught before they did damage.** The
first classifier called `'ANALYSE'` and `'Favourites'` identifiers purely for
being one word long inside quotes, which would have left two visible strings
British; case turned out to separate wiring from display labels cleanly.
`programme(d)` was a false positive throughout, since "programmed" is spelled the
same in both dialects, as are "specialist", "analysis" and "emphasis" without a
verb suffix. And the sweep's first pass silently dropped every pattern carrying a
lookahead (practis, analys, emphasis) because it re-matched the captured text
against a pattern whose lookahead context was outside the capture. Named groups
now carry the dispatch. That one is worth remembering: it failed by doing
nothing, and the only tell was four expected words missing from a summary count.

Gates: syntax clean across 9 blocks, sentinel at 97 fixes + 190 pins, backup
audit at 48 keys and 38 progState fields, tour audit 0 missing and 0 broken. The
quiz audit's 129 criticals are pre-existing and unrelated; identical count on the
pre-sweep baseline.

`intonare_us_spelling_audit.py` is in the toolkit now, so a future drift back is
one command away from being visible.

---

## v0.116.1 — dealing the cards back in

Two device bugs from the v0.116.0 re-run path, both mine, both invisible to the
way I tested it.

**The reopened chooser had no cards.** `lnchGo()` marks every cell `lnch-picked`
or `lnch-other` to fling them off screen behind the morph card, and nothing ever
cleared those classes; both rules set opacity 0, and `lnch-other` adds a
translate of around 125% with a rotation. `lnchReopen()` restored the container
and its classes, so the hint line and the pinned row came back correctly around
an empty space where the grid should be. Measured after re-run: all four cells at
opacity 0 with zero-size rects. Now stripped on reopen, and verified back at
opacity 1 in a 2x2 with real rects.

The reason this shipped is worth writing down: I verified the reopen by reading
classes and computed style on `#lnch` itself, which reported display flex,
opacity 1 and `lnch-gone` cleared. Every one of those was true. The state that
was wrong lived one level down on the children, and a container-level check
cannot see it. Same family as the original bug this release fixed, where the tour
overlay was genuinely active and genuinely visible while everything it pointed at
was not.

**The last card told people to hold a title that isn't there.** `showStep()`
appends the replay note to the final step of every tour, and it names the header
title as the replay gesture. That is correct in every tour but this one: the
chooser has no header, because `body.lnch-open` hides it. So the welcome tour
ended by naming a control that was not on screen and describing a gesture that
could not be performed. The launcher tour now points at Settings then Re-run
Welcome Tour instead, in both languages; every other tour keeps the hold-the-title
note unchanged, verified side by side.

---

## v0.116.0 — the tour that pointed at nothing

A paid tester report came back saying the app had no onboarding for new users.
It does. It has had one the whole time. It just fired at a moment when nothing
it described was on screen.

**What was actually happening.** On first launch, `startTour('overview')` ran on
a flat 600ms timer from the bottom of the main script. The splash runs about
three and a half seconds plus a 1.3s dissolve, so the tour opened underneath it;
the card's entrance animation played in full behind an opaque overlay and the
tour was already sitting there mid-flow when the splash finally cleared. What it
cleared to was the chooser, and the overview is anchored to the app proper.
Measured on a 412x915 viewport with the launcher up: `.logo`, `#micBtn` and
`#levelChip` all sit behind the opaque grid, so their spotlights cut a hole onto
a blank frosted rectangle. `.mode-toggle` measured at y=915 and `#mode-settings`
at y=916, which on a 915px viewport is a full bar-height below the fold, so the
caret on steps 2 and 5 pointed off the bottom edge at nothing at all. Six steps,
zero visible targets. The same anchors measure y=862 and y=863 once a module is
open, so the tour was never broken, only homeless.

**The new shape.** Onboarding is two halves handed to each other. A three-step
`launcher` tour runs on the chooser, about the chooser, and ends on a START
button that gives the person the grid instead of dismissing a document. Whichever
module they pick then introduces itself on arrival via `maybeSectionTour()`. The
four section tours (tuner, metronome, tools, practice) existed but had never been
wired to auto-fire; `maybeAutoTour` only ever covered tools and exercises, and it
keys off `currentTool`/`currentExercise`, both null at section level.

Three steps rather than six by choice. Each card already carries its name, a
subtitle and a static miniature of the real module surface, so a step per card
narrates what the person is reading at that moment. Pinning stayed out of the
walkthrough as its own card and became a clause in step 3: nobody knows their
favourite module before they have opened one, and following that instruction
sets `LNCH_PIN`, which makes `lnchShouldShow()` false and removes the chooser
permanently. Teaching it forty seconds in is teaching someone to delete the
screen they are standing on.

**Fixed card without the preview pane.** Module tours get a centred card and a
scaled DOM clone, because their subject is often on another screen. The launcher
tour wants the first and not the second: a near-fullscreen grid spotlit would
darken four thin margins and leave the card nowhere to sit, and a clone would
show a small copy of what is already behind the card. New `dataset.fixed` flag
rather than a fifth branch in the module list; `showStep` and `positionTour` now
read `_isFixedCard` for scroll-skip and positioning while `_isModuleTour` keeps
owning the preview.

**Triggering.** The boot-time timer is gone. `maybeWelcomeTour()` is called from
`lnchInit()` on both shown paths, hung off the launcher actually being visible
rather than off a duration the splash does not honour, and from the no-chooser
branch for pinned or deep-linked launches, where the in-module overview is the
tour that matches what is on screen.

**Re-running.** The Settings button ran `startTour('overview')` in place, which
from inside a module would have reproduced the original fault in mirror image.
`rerunWelcomeTour()` calls the new `lnchReopen()` to bring the chooser back
first, then runs the launcher tour against it, falling back to the overview only
if there is no launcher to restore. The auto-tour opt-in prompt deliberately does
not fire after the welcome tour on a first launch: it would cover the grid at the
exact moment step 3 says to pick a card. It arrives after the first section tour
instead, and a manual re-run still gets it via `_welcomeTourManual`.

Verified on a genuinely empty profile: tour appears after the splash with the
launcher in, three steps, no spotlight, no preview, START on the last card,
`tune_tour_done` and `intonare_tours_seen` both written, METRO picked afterwards
fires the metronome tour at 1/6 with a real spotlight. Returning users get no
welcome tour and still get unseen section tours. No page errors on any path.

Copy is US English throughout, which the rest of the app is not; a spelling
sweep is queued as its own build. 728 British spellings in the file, 461 of them
in comments, the rest split between user-visible strings and identifiers that
should stay exactly where they are.

---

## v0.115.3 — the targeting computer

Better than mine, and it is the closer mapping. Luke switches off the instrument
and hits the shot on feel alone, which is precisely what the climb asks: no
reference tone, no lifelines, twenty-four notes named on nothing but what you
carry in your head. Mallory was about doing a hard thing for its own sake; this
is about doing it without help, which is the actual condition.

The Force Is With You, described by the line that names the feat rather than the
one everyone quotes: "You switched off your targeting computer." Italian: "Hai
spento il computer di mira." The name is longer than most, and short of the
longest already in the set, so nothing about it is unusual for the card.

One thing to weigh rather than a problem: that makes three Star Wars references
across thirty-six achievements, alongside I Have You Now and Maestro. Still a
minority, and the other thirty-three range across Tolkien, Rowling, the Princess
Bride, Gladiator and Back to the Future — but it is now the most-quoted single
source, which is worth knowing before a fourth.

---

## v0.115.2 — Free Solo

The clean-summit achievement was written in the wrong shape. Looking at the
other thirty-five, the pattern is consistent: the NAME is plain and short, and
the DESCRIPTION is a quotation. Impressive. Most impressive. Inconceivable! A
day may come when your strength would fail, but it is not this day. It's
leviOsa, not levioSA. Mine had a plain name and prose where the quote goes,
which is why it read as written rather than found.

It is Free Solo now, and the description is Mallory on Everest: "Because it's
there." A real line, the most famous thing anyone has said about climbing
something for no reason other than that it can be done, and the right register
for an ascent made without touching a single lifeline. Italian: "Perché è lì."

Worth noting the neighbours, since the module borrowed their vocabulary: The
Climb and The Summit already exist as achievements. No collision — all
thirty-six names are still unique — but the words are spoken for.

---

## v0.115.1 — release check, and a backup that was a live view

Full pass over everything since 0.108.29 before this goes out: forty-seven
releases, the Relative Pitch module start to finish, the light-mode rebuild, the
tour work and the leg tuner. Every screen and every exercise opened in both
themes with no overflow and no console errors, the whole climb played end to end
to a clean 200,000 summit, and every gate green.

One real thing turned up, in the backup. backupBuild copied progState shallowly,
so the object it handed back shared every nested value with the live state — the
"backup" was a window onto the present, not a snapshot of the moment. In the
export path it never mattered, because the object is serialised to JSON on the
next line and the file is a true copy. Anywhere else it would matter a lot: hold
a payload, change something, apply it, and you restore what you have now rather
than what you had then. The tell was a round-trip test restoring zeros.

One JSON round trip at build time cuts it loose, and the round trip now behaves:
build with a score, wipe it, apply, and the score comes back in memory and on
disk. Pro entitlement still excluded, leg tuner state still excluded.

Also worth recording from the same pass: the ink audit sits at 41 and the
project light audit at 29, both steady and mostly sub-12px type where heavy ink
is correct. Neither is a gate.

---

## v0.115.0 — your tuning is in, and five songs are signed off

Sixty-six hand-tuned leg values across five songs, written in from the export:
clair_de_lune, prelude_em, moonlight, liebestraum and fuer_elise, all five legs
on each. Every one of those ids is now in RT_TUNED, so the tuner stops badging
them and the list is the record — the panel's own "changed" highlight only
remembers as far back as the last time it opened, which is what RT_TUNED exists
to fix. Sixteen perf songs still untuned.

**And fourteen stale bpm values, which were nothing to do with the tuning.**
Every song's tempo lives in two places: with the song, and again in RT_JOURNEY.
Fourteen of the newer entries had a placeholder 100 sitting in the second copy —
alla_turca reading 100 against a real 120, troika 100 against 92, waldstein_1 100
against 160. Harmless, because every reader prefers the song's own value and only
falls back to this one, and invisible for exactly the same reason. They now
agree. bella_ciao is genuinely 100 and was left alone.

There is a note on the object saying to treat that field as a fallback for
entries with no song data rather than as a second source of truth, since one
number kept in two places is how it drifted for months without anyone noticing.

Verified in the running app: the five report as tuned, their hooks match the
export leg for leg, the bpm copies agree with the songs, and a trip still picks
a song and builds.

---

## v0.114.9 — the rest of the holes in the leg tuner, found before you spend another hour

You asked whether anything else was waiting to eat an evening. Three things were.

**The save ran before the ms recompute.** Perf songs seek by absolute ms, and the
nudge buttons update ms straight after b and s. I put the save between those two
steps, so the stored snapshot had the new position and the old ms. It would have
survived the reload perfectly and then played the wrong spot — visibly correct in
the panel, audibly wrong on the road. Worse than losing the work, because you
would have tuned against it. Save moved after the recompute and pinned there,
with the reason written down.

**The key was invisible to the backup audit.** It was passed as a const, and the
audit finds keys by matching literals in setItem, so a newly persisted key went
unnoticed by the one check whose job is noticing exactly that. Literal now, and
the audit immediately flagged it as unclassified, which is the tool working.

**And it needed classifying rather than just silencing.** It goes in
BACKUP_KEYS_SKIP on purpose: the tuner is a scratchpad whose output belongs in
the source, and carrying it in a backup would drop a half-finished session onto
another device and silently override that device's hooks. Reasoning is in the
file next to the entry. 48 keys classified now, up from 47.

Verified end to end on the real button path rather than by calling the functions
directly: nudge a perf leg, b and s and ms all change together, all three land in
storage, all three come back after a full reload, backup skips the key, and
FORGET removes it.

---

## v0.114.8 — the leg tuner never saved anything, and now it does

Checking rather than guessing: the tuner edited RT_JOURNEY in memory and wrote
nothing anywhere. No localStorage, no progState, no prompt on close. A reload, a
crash, a fresh build — the whole session gone, silently. So yes, an evening of
tuning is gone, and it was never anywhere to lose: it would have gone the same
way on any reload, with or without a new build.

Nothing I changed took it. The export fix touched only the copy path, and the
hook values in the file are exactly what they were. But that is a small comfort
against a tool that quietly discards work, so it does not do that any more.

Every edit is written to localStorage as it is made. The saved set is applied
back over RT_JOURNEY at module load rather than when the panel opens, which
matters: it means a tuned leg actually PLAYS tuned instead of only reading tuned
inside the tuner. Verified across a full page reload — edit a hook, reload,
values still there and in effect.

A FORGET SAVED TUNING button sits beside the others for when a session needs
throwing away, behind a confirm, since it cannot be undone.

The one thing worth saying plainly: this was the second silent-loss bug in the
same panel in one day. The export looked like it worked and copied nothing; the
editor looked like it worked and saved nothing. Both were quiet in exactly the
same way, and both only surfaced because you asked a direct question about
something that should not have needed asking.

---

## v0.114.7 — the leg tuner's EXPORT was copying nothing

Three empty pastes in a row is not three accidents. The export ran
document.execCommand('copy') inside a try/catch that swallowed the failure, on a
textarea marked readonly — which the Android WebView will not select, so there
was nothing on the clipboard to copy in the first place. Every part of that
fails quietly: the button gave no feedback, the catch ate the error, and the
textarea appeared with the right text in it, so from the outside it looked like
it had worked. It had never worked on the device.

navigator.clipboard.writeText now, with execCommand as a fallback that lifts the
readonly attribute for exactly as long as it needs the selection and puts it
straight back. The button reports which one happened — COPIED, or SELECT AND
COPY BELOW — rather than assuming, and a line under it explains what to do if
the WebView blocked the clipboard entirely. The textarea grew to 300px and has
user-select forced on, so selecting it by hand is a real option rather than a
theoretical one.

Verified end to end with clipboard permissions granted: 5,451 characters, 39
songs, and the clipboard contents match the textarea byte for byte.

**Also struck from the open list: the dormant grid deletion.** It has been
sitting there as a pending cleanup for the seven converted piano songs. Checking
the actual entries, all seven carry only duckV, meter, label, tempo, bpm, perf
and tempoMap — no grid arrays at all. The data went out with the perf conversion
rather than needing a separate pass. Nothing to delete, and nothing about tuning
those songs removes anything.

---

## v0.114.6 — one press was firing two gestures

Both, yes. The leg tuner has been on a 600ms long-press of the ROADTRIP title
since it was built, and yesterday I bound the tour replay to the same element at
500ms. One press fired both: the tour opened at 500, the tuner opened on top of
it at 600. Verified before the fix rather than reasoned about.

Nothing in the code looks wrong. Two handlers on one element, each correct on
its own, added eight months apart, and the only way to notice is to know the
older gesture is there and try it.

The tour keeps the title, because it is the user-facing feature and the title is
where every other tour replays from. The tuner moves to the INTONARE brand pill
at 900ms — 84 by 18, so it is reachable on a phone, and not a thing anyone
presses on the way to something else. window.rtTuner() is unchanged. Verified:
the title now opens only the tour, the pill only the tuner, and a short press on
the pill opens neither.

**The audit gained a collision check.** It cannot find every clash — nothing can
enumerate listeners after the fact — but the leg tuner leaves a dataset marker
behind, so it can at least say whether something else has claimed the element a
tour hold is bound to. That is the one clash that exists today, and it is the
shape of the next one.

---

## v0.114.5 — Road Trip's tour could fire once and never again

Good question, and the answer was worse than it looked.

Every tour in the app replays the same way: press and hold the title. The gesture
is bound to #appLogo and #headerTagline so it works on whichever one is showing.
Road Trip draws its own full-screen chrome over the header — and the trap is that
the tagline is still in the DOM, still reports as visible, and still has pointer
events enabled. Nothing about it looks broken from the code. It is simply
covered: elementFromPoint at the middle of the tagline lands on a difficulty
chip. So the Road Trip tour could auto-fire once, on first open, and then be
unreachable forever.

Music Quiz had exactly this problem and already had the fix, because it is a
modal with no header at all and the failure was obvious there. Road Trip's
failure was not obvious, because it has a header — just not one you can touch.
Same fix, same shape: press-and-hold bound to the module's own ROADTRIP title,
with the movement threshold the Android WebView needs so its constant pointermove
jitter does not cancel every hold.

**The audit now checks this,** which it could not before. Coverage and selectors
were never going to catch it: the tour existed, every step resolved, and it
worked perfectly the one time it ran. The new check asks whether the tour can be
reached a second time, and it asks with elementFromPoint rather than by looking
at visibility, because visibility was the thing that lied.

Both full-screen modules now report bound and reachable.

---

## v0.114.4 — the switch went missing inside its own mode, and a tour audit

**Moving the switch into the card head stranded people in the climb.** It
landed on the practice card and on the climb's GAME card, and nowhere else —
the intro and the result screen have no head, so once you were on either of them
there was no way back to practice. That is worse than the row of slabs it
replaced, and it is exactly the failure that only shows up when someone uses the
thing rather than looks at it. Both screens carry it now, and it is pinned.

**The rules went back behind their toggle.** Unfolded they are three paragraphs
sitting between the record and the button, on a screen whose entire shape is
built to end on START. Behind a link they cost one dim line and are one tap away
for anyone who wants them, which was the right answer the first time.

**And a tour audit, because tours rot silently.** Nothing breaks when a module
ships without one, since the prompt simply never fires. Nothing breaks when a
step points at an element that has been renamed, since the tour skips it. Both
failures are invisible from inside the app, which is why they accumulate.

intonare_tour_audit.py checks three things: coverage against the app's own
module roster, every step opened against the live DOM, and a scan for the
writing tells this project keeps having to strip.

It found Road Trip with no tour — the last one — and it caught a broken selector
in the Road Trip tour I had just written, within a minute of writing it: I had
pointed at #rtDiffstrip and the element carries that as a class, not an id. That
is the whole argument for the tool in one example.

The tone scan flags thirteen. Two were the real thing and are rewritten: the
overview's "TUNER tunes any instrument by mic. METRO is a full metronome." and
the piano's "Fully multi-touch, so chords work. Glide across keys." Both are the
stacked-declarative rhythm rather than anything wrong with the content. The
other eleven are colons doing their proper job in front of a list, or a short
sentence that earns its length; the scan cannot tell those apart and is not
meant to. It says where to look.

Coverage is complete for the first time: every exercise in the roster has a
tour, and every step in all thirty-three resolves.

---

## v0.114.3 — the switch moves into the card, and the tour stops sounding like a tagline

**The switch replaces the title it was duplicating.** It sat in a row of its own
above the card, and the card's first line said PRACTICE — which the switch had
just said, one row up. It lives in the head now, where the title was, with the
settings line underneath it. The climb head does the same, folding the band name
and its gap onto one line. The practice card drops from 519px to 488.

**The rules come out from behind the toggle.** With the tour covering the module
itself, what is left is the terms of the bet, and those have no element to point
at until you are already climbing. Three lines, on the intro, where someone
deciding whether to press START can read them without going looking. The
one-wrong-ends-it rule went, because the intro line already says it and saying
it twice on one screen is worse than not saying it at all. The toggle, its
handler, its two labels and its link style are all gone rather than left
dangling.

**And the tour copy was written in the voice you keep catching.** A colon before
a punchline, "not a skill, it is a crutch", short declaratives stacked three
deep — a tour is somebody showing you round, and it should read like someone
talking rather than like a tagline. All six steps rewritten in both languages,
with the sentences let out to their natural length and the aphorisms taken out.
The fork step now explains why it costs you instead of scoring a point off it.

---

## v0.114.2 — the tour gap, and a mode switch that stops shouting

**No, tours have not been kept up, and asking found it.** Thirty tours exist.
Five exercises have none: Road Trip, Pitch Match, Chord Ear, and both modules
shipped this month, Staff Notes and Relative Pitch. The reason it stayed
invisible is that maybeAutoTour keys off the TOURS object, so a module without
an entry simply never prompts — nothing breaks, nothing warns, the module just
quietly has no first-run explanation while every older one does.

Relative Pitch gets four steps: the two modes, hearing a note with nothing to
compare it to, the screen, and why the fork costs you a run. Staff Notes gets
two. Both in English and Italian, both with every selector verified to resolve
against the live DOM rather than assumed. Road Trip, Pitch Match and Chord Ear
are still open and now written down rather than merely absent.

**The mode switch was this module inventing a control the app already has.**
Two full-width slabs, 358px across, the loudest thing on the screen — for a
choice between two things. .app-seg is what everything else uses for a small
either/or: an inline pill sized to its labels, sitting left. 181px now, and it
reads as a switch rather than as navigation.

Two things that fix took. The pill kept filling the row despite align-self,
because the parent is a GRID and align-self is the wrong axis there —
justify-self is what a grid item needs. And the state class changed from .on to
.active, since the shared control has its own convention and the point of using
it is to stop having two.

**On whether the rules should just be the tour:** mostly yes, and they now
overlap. But they are not the same job. A tour points at elements and runs once;
the rules are the terms of a game with stakes, and a rung-eighteen decision is
exactly when someone wants to re-read what a haven is worth. The tour explains
the module, the rules link explains the bet. Worth revisiting once the tour has
been on a device.

---

## v0.114.1 — you were right about the lifelines

**They were refreshing at every band edge,** which meant twelve across a climb
at 0.08 of the multiplier each. Spend every single one and you still settled at
x1.04. That is not a cost, it is paperwork. And a resource that refills cannot
be hoarded, so the one decision the multiplier was supposed to create — burn
this now, or keep the number — never actually came up, because there was always
another one along in six rungs.

Three for the whole climb now, at a quarter of the multiplier each. Spend all
three and you finish on x1.25 against x2.00 clean, so the full set is worth
three quarters of your score. Only the replays refresh at a band edge, which is
what your rewritten rule text already said before the code agreed with it.

Verified: a lifeline spent in the first band is still spent in the second, a
clean summit pays 200,000 and unlocks No Hands, and a summit with all three
spent pays 125,000.

**The eight rewritten strings are in, with Italian twins.** Two small
corrections inside them. The havens sit at rungs 6, 12 and 18, so "every five
steps" became "every sixth step" in both languages. And the lifeline rule still
said twelve, which was true this morning and is not any more — it says three.

The result captions are noticeably warmer than what they replaced, and losing
now says so plainly rather than describing the mechanics of where you landed.

---

## v0.114.0 — No Hands, a lighter ladder, and an editor for the climb's copy

**An achievement for the clean summit.** Twenty-four rungs with the wrong
answers closing in the whole way, not one lifeline taken, so the multiplier is
still on 2.0 at the top and the payout settles at 200,000. There is exactly one
way to earn it. It is called No Hands and it is legendary, which for once is
literal rather than a rarity tier: nothing else in the app asks for two dozen
correct answers in a row with no help available except the ones you are choosing
not to spend.

The condition checks the multiplier as well as the figure. Checking the payout
alone would let a helped run that happened to bank 200,000 some other way slip
through, and the whole point is the absence of help.

**The ladder was the last thing wearing floor-pinned ink.** A haven at 2.5:1
against the card is not gold, it is brown, and the cleared rungs behind it were
the accent at 42% opacity — which on a dark lamp bed is a lit rung and on a pale
one is a smear. Both are fills rather than text: they have to be findable, not
legible. The golds come up to 1.5 and 1.9 against a plain segment, still a clear
step either way, and a cleared rung is now an opaque lifted accent rather than a
wash of one.

**And an editor for the climb's copy.** ClimbCopy_Editor.html: every string the
CHALLENGE mode shows, English beside Italian, forty-five of them, each with the
place it appears and the width it has to live in. The character counts and
ceilings are measured off the app rather than guessed, so a label that will
ellipsise says so before it ships rather than after.

EXPORT prints only the lines that actually changed, was and now, both languages
— which means a rewrite comes back as a patch I can apply verbatim with no risk
of a stray edit riding along unnoticed. Nothing in the file touches the app.

---

## v0.113.9 — the app has more than one word for "a raised surface"

Read the residue rather than the headline, and it says something structural
about light mode that had gone unnoticed for the whole of this work.

**The card-scoped fix assumed there was one kind of card.** There is not. The
tuner's instrument card is .tuner-bpm-card, the interval card is .iv-card-v2,
the tour is .tour-card, the hub buttons are .practice-card-btn, the chooser
faces are .lnch-face — five raised surfaces holding text, none of them .card. So
the hierarchy fix reached the module cards and nothing else, and every one of
those five kept the ground-pinned ink it should not have had. That is why the
tuner and metro screens between them accounted for twenty-six of the forty-two
remaining findings while the module screens had almost none.

Extending the scope to all five overshot immediately, and the other audit caught
it: the practice hub buttons and the interval card carry sub-9px labels that the
lighter secondary drops below AA, and the tuner card's pill labels are 8px. So
the rule is not "is it raised" but "is its secondary text at label size", which
is not something a selector can ask. The scope now holds the surfaces that pass
that test — the module cards, the sheets, the tour and the chooser faces — and
the ones that failed it are deliberately outside, documented as such.

**Two things worth saying plainly about what this means.** The first is that the
residue is dominated by small type: of the elements still over ceiling, thirty
of forty-two are under 12px, where heavy ink is arguably correct and lightening
it is what breaks AA. The second is that four of the remaining findings are in
dark mode and all four are dark ink on a bright accent fill — a primary button —
which is right by design. The tool has no way to know that, so those stay.

Ends at 39 by the ink audit with the other two audits at zero new failures and
none made worse. That number is not going to zero, and it should not: it is a
hunting tool with a deliberately conservative ceiling, not a gate.

---

## v0.113.8 — what the ink audit actually found

Ran it properly and read the whole list rather than the top of it. Eighty-seven
pairings, and grouping them by the colour rather than by the element turned most
of the list into one fault.

**The hierarchy had collapsed.** Measured on a card: text 11.9:1, dim 10.2,
muted 9.6. Three levels that are supposed to be obviously different, sitting
barely two points apart. Nothing was individually wrong, which is why no
contrast audit ever mentioned it — and it is exactly what "muddy" turns out to
mean. Everything on a card weighed the same, so nothing led.

They cannot simply be lightened, because the same two tokens also carry text on
the GROUND where they are already near the AA floor. So they are redeclared
inside .card and inherited from there: the ground keeps its legal values, the
card gets values pinned for a card. Text stays, dim goes to 7.2:1, muted to 5.0.
The steps are visible again and both still clear AA on the surface they are
actually read on.

That one change cleared twenty pairings. Three more went with the tokens the
audit named individually — the ladder's gold and multiplier, the screen's rung
figure, and the tuner's face-swap control, all still using raw floor-pinned
values where a lifted variant already existed for exactly this.

**The tool needed two fixes of its own to be trustworthy.** It was flagging
primary body ink, which is supposed to be high contrast — black on white is 21:1
and nobody calls that a fault — and that noise was burying the real findings. It
reads the theme's own --text off the root and skips it now. The first attempt at
that silently did nothing, because a custom property comes back as the author
wrote it, and here that is a bare hex the parser did not know.

**And one thing the fix broke, which the other audit caught.** A card-scoped
secondary is right for a label at 10-12px and a step too far below that: the 9px
hint and the inactive instrument tabs lost their footing. --ink-tight keeps the
ground-pinned value reachable inside a card for those, and the card scope
deliberately leaves it alone.

Eighty-seven down to forty-two. The remainder is mostly small and several of
them are deliberate.

---

## v0.113.7 — a tool that finds the fault instead of hunting it

You should not have to hunt these down one screenshot at a time, and the reason
you have been is that a contrast audit can only ask one question: is this dark
enough? Every light-mode fault in this app has been the opposite — a colour
pinned dark enough to clear 4.5:1 on the FLOOR, then used on a CARD two steps
lighter, where the same value lands near 10:1 and reads as ink rather than as
colour. A contrast audit passes that every single time, because more contrast is
never a failure by its rules.

**intonare_ink_audit.py** asks the inverse. It walks twelve screens in both
themes and reports every element whose contrast is far HIGHER than its role
needs: over 9:1 for small text, over 7:1 for large text and graphical fills.
Those ceilings are not standards — nothing forbids high contrast — they are the
line past which, in this app, a colour has reliably turned out to be pinned
against the wrong ground. It prints the ink, the ground, the class and the
screen, so a colour can be found rather than searched for.

It found 87 pairings on its first run, and the single largest was systemic:
**the body ink itself.** Pinned at 7:1 against the floor, it lands at 13.8 to
14.6:1 on a card. That is well past AAA, and since almost everything in this app
is read on a card, it is what made light mode feel heavy element by element
rather than in any one place. The trio is pinned at 5.6 / 4.8 / 4.55 on the
floor now — still clearing AA there — and lands at 11.4 / 9.9 / 9.5 on a card.
Ink rather than tar.

**And the answer keys, which is where you noticed it.** Right and wrong are the
two states you look straight at, and both were wearing floor-pinned status ink
on a near-white card: 8.8:1 for a letter that is supposed to read as green,
which is how it ends up looking like moss. Both take the lifted status colours
in light now, along with the big note reading on the screen.

The audit still reports 81 pairings, most of them minor and several of them
deliberate. It is a hunting tool, not a gate; nothing about it blocks a build.

---

## v0.113.6 — the emboss was eating the letterforms

**Three shadows around a glyph, two of them white, is an outline.** That is what
the title treatment had become: a white pass above at 92% and another below at
55%, with the dark one underneath. Around type rather than around a box, the
white bleeds inward at the stroke edges and eats the contrast of the very thing
it is supposed to be lifting — the letters get a halo and lose their weight, and
at header size that reads as softness rather than as depth.

A raised object needs one highlight and one shadow. The white is a single
hairline on the lit side at 45%, and the dark does the lifting. Same modelling,
nothing eroding the stroke.

**And the paper is a nudge cooler.** Same lightness, chroma pulled back a third
and the hue eased off yellow toward neutral: 82 degrees at C .013 becomes the
same lightness at C .009. Still warm enough not to read as overcast, cool enough
to be paper rather than parchment. The top bloom went with it.

No new contrast failures, project audit steady at 26, module audit zero.

---

## v0.113.5 — paper

The chooser ground is paper. Warm off-white, a shade deeper toward the foot,
with a wide bloom across the top.

**Value stops holding the grid together at this lightness,** and that is the
whole consequence of the choice rather than a side effect of it. The ground sits
1.05:1 from a card's lit top edge and 1.16 from its foot, so the cards are held
entirely by their rim, their contact shadow and their own pool. All three were
tuned against a mid-tone ground and had to be stepped up: a firmer rim carrying
more of the module's own colour, a tighter and darker contact shadow so the card
meets the page somewhere definite, and a longer ambient so it still lifts off a
field this light. Sentinel-pinned, both the ground and the rim, because
softening any one of them now dissolves the grid into the page.

The pools read at their strongest here. On a mid grey they were fighting the
ground for the same territory; on paper they are the only colour in the field
outside the cards themselves.

**Two things the change broke and put back.** The pinned chips were white on a
near-white ground at 1.27:1, a chip with no edges — they carry more of their tool
colour and a firmer rim now. And the hint under the grid was pinned against a
mid ground; on paper it landed at 4.17:1, which is the AA floor with no headroom
at 7.5px. It is pinned against the darkest ground it can land on rather than the
lightest, since it sits over the lower pools and not over bare paper.

No new contrast failures, project audit steady at 26, module audit zero.

---

## v0.113.4 — the dark faces were fighting their own glow

**The vignette on the dark cards had to come down.** The face fell to 22% black
at its foot, which was right when the card had nothing behind it: the falloff
was doing the job a shadow does, and dark shadows are nearly invisible on
near-black. With a pool underneath, the same gradient stops reading as depth and
starts reading as a hard vignette — lit at the top, blackened at the bottom —
and the glow makes the swing worse rather than better, because now there is
light immediately outside the darkest part of the card.

Ten percent instead of twenty-two. The fall is still there, the light gets
through, and the 3D work stays exactly as it was: rim, inset highlight, layered
shadow, and now the pool.

**The mock could not be judged, and that was a fair criticism.** A ground shown
in a box the grid fills is a swatch, not a screen. In the app the field runs the
whole viewport with large empty regions above and below the grid, and those
regions are most of what you actually see. The stage is a phone now — 814px
tall against a 499px grid, so roughly forty percent of it is the dead space the
decision actually turns on — with the nav bar in place so the ground is judged
under the chrome that sits on it.

PAPER and LIFTED WARM are the two you picked out; they are next to each other in
the picker for a straight comparison.

---

## v0.113.3 — dark gets the glows, and the ground goes to a vote

**Yes, dark should have them, and it needed them more.** The whole language of
the dark theme is emission — every card has a lit rim, the page carries pools,
the icons glow — and the chooser was the one screen not speaking it. The same
card-attached pool is there now, weaker and tighter: a glow on near-black reads
at much lower alpha and turns to fog with far less spread, so it runs at 34%
against light's 70% and blurs 20px against 22.

**On the ground: you are not crazy, and the reason is structural.** A mid
neutral is being asked to do two incompatible jobs at once. It has to be dark
enough that pale cards read against it and light enough that it does not feel
like weather, and the value that satisfies both is the value that satisfies
neither. Measured, the cards all sit at OKLCH L .90 at the top and .966 at the
foot — they are very light and very close together, so anything in the middle
distance from them reads as a compromise.

That is a taste call with real trade-offs on each side, and it has now cycled
four times on my judgement, so it goes to a file rather than another guess:
ChooserGround_Mock.html, six grounds on the real components and the real glows,
with the measured value gap under each. WARM MID is what ships today at 1.29:1
to a card top. LIFTED WARM is the smallest possible answer if the complaint is
weight rather than hue. PAPER removes the gap almost entirely and lets border
and shadow hold the cards. DEEP and COOL DEEP go the other way at 2.65 and 2.74,
which is where the glows have something to fall on. INK is a dark chooser inside
a light app at 10:1 — the most striking and the biggest question, since one
screen breaking the theme is either a signature or a mistake.

---

## v0.113.2 — an overcast sky is a cool grey, and the four cards were not equals

Two faults, both measurable, and the reading around colour theory named them
before the eye could.

**The four cards were not the same weight.** Mixing a fixed percentage of each
module colour into white looks even on paper and is not, because the four
sources are not equals to begin with: measured in OKLCH they run C .121 to .154
and L .769 to .880. Tools' mint is the most chromatic and one of the darkest,
metro's gold the lightest, so the grid came out with tools heaviest and metro
faintest. This is the standard failure — two hues at matching perceptual chroma
feel balanced, the same hues at different chroma feel unbalanced with the more
saturated one dominating, and the traditional harmony rules all assume equal
saturation as a baseline.

Faces are built at matched lightness and matched chroma per stop now,
inheriting only the hue. A set of colours reads as a family when each sits at
the same perceptual distance from neutral; it reads as four swatches when they
do not.

**And the overcast feeling was literal.** An overcast sky is a cool grey — that
is the whole description — and the ground was sitting at hue 260 with a chroma
of .005. That value is the dead zone: enough tint to be felt, not enough to
register as a decision, which is exactly the "accidentally off-neutral" trap.
Pure greyscale also does not occur in nature and tends to read as unnatural, and
a neutral surrounded by saturated colour takes on the opponent cast of whatever
is nearest it, so a grey among four hues gets pushed four ways at once.

The ground is a warm neutral now: hue 76, chroma .013 so the tint is a decision
rather than an accident, and lifted. Same value structure, and it stops being
weather and starts being paper in daylight.

Contrast unchanged: no new failures, module audit zero in both themes.

---

## v0.113.1 — the light belongs to the card

The four pools worked, and they only worked at the aspect ratio they were
measured on. Anchoring them to percentages of the viewport meant a shorter
screen, a tablet or a rotation slid every one of them off the card it was
supposed to sit under. Checked at 360x640, 390x844, 430x932 and 768x1024: the
card centres move by up to 190px horizontally between them.

So the pool is attached to the cell. It goes wherever the card goes, at any
size, with no measurement to keep in sync — and it puts the physics the right
way round, which is the better half of the change. The cards emit onto the
ground rather than the ground happening to be tinted underneath them. Move a
card, add a fifth, change the grid, and the light follows on its own.

With the light coming off the cards, the ground goes flat and gets out of the
way: one near-neutral tone with a hair of fall so it is not a dead field.

**The stops are weighted outward,** which looks wrong written down and is the
only thing that works here. A card covers the middle of its own pool, so a
conventional falloff puts all the colour exactly where nothing can see it. The
visible part is the band in the gutters, so that is where the alpha sits: 70% at
the centre, still 62% at the halfway mark, 34% at 78%.

**And they breathe,** nine seconds, out of phase by a quarter cycle each. In
phase they read as the page flickering rather than as four lights. Reduced
motion holds them still at a fixed opacity.

Contrast unchanged: no new failures, module audit zero in both themes.

---

## v0.113.0 — the chooser ground is the four modules, out of focus

Every single-hue version of this failed the same way, and it took four attempts
to see it as one problem. A violet-grey clashed with the mint and the cream. A
neutral grey fixed the clash and read bland. The splash's blue brought the clash
back in a different key. The fault was never which colour — it was that one
colour has to sit behind four cards in four other colours, and there is no
single hue that agrees with all of them.

So the ground carries all four. A soft pool of each module's colour, centred on
the card that owns it: cyan top left, gold top right, mint bottom left, lavender
bottom right, over a near-neutral base. The centres are measured against the
real card positions rather than guessed, so each pool actually sits under its
own module. Nothing on the screen is foreign to what is behind it.

They are wide and shallow on purpose — 84% by 40% each, fading out by three
quarters — so the effect reads as a tint the whole field shares rather than four
blocks. Because the cards cover most of their own pool, what you actually see is
the spill in the gutters and margins, which is why they are stronger than they
look in the numbers.

Contrast unchanged: no new failures, module audit zero, project audit steady.

---

## v0.112.10 — the black flash, the bare top, and titles with a lift

**The challenge screen was flashing black in light mode,** and it was carried
straight over from dark. The entrance dims the display to brightness(.25) before
it stutters on, which on a near-black panel is an unlit screen and on a
near-white one is a black rectangle. Light gets its own range now: the unlit
state is a dim, slightly desaturated panel at .965, and the flicker moves
between .97 and 1.04 rather than a quarter to one and a half. Same stutter, in
the right key.

**The field started too high and fell too far.** Beginning at --surface put a
near-white band across the top of the screen with nothing in it, which is the
bare feeling. It starts one step down and spends more of its height near the
floor, so light still comes from above without giving a third of the screen away
to it. Splash and chooser share the change, since they share the recipe.

**The pinned chips got their colour back.** Rebuilding them as white with a 7%
tint fixed their invisibility and left them anaemic; the tool colour runs at
13-24% through the face now, the border carries nearly half of it, and the icon
is 78% of the tool colour rather than being mixed most of the way to ink.

**And the titles are lifted.** Dark uses a glow, which does not transfer. The
paper equivalent is an emboss: a white pass above, a soft dark one below, the
same modelling the cards get, at type scale. It has to be drop-shadow rather
than text-shadow — the titles are painted with background-clip:text, and a
text-shadow paints beneath a transparent fill and shows straight through it.

Contrast: no new failures, project audit steady at 26, module audit zero.

---

## v0.112.9 — the tagline audit, the chooser, and the last of the muddy darks

**The subtitle was never a header line.** Truncating it was treating the
symptom. Relative Pitch had no header tagline of its own — it was borrowing its
CARD subtitle, which is written for a card and roughly twice what the header can
hold. Staff Notes had no entry in the map at all, so it showed nothing.

Audited all thirteen exercises in both languages: they now all have a tagline,
none clips, and every header sits on one line. Relative Pitch gets "name it
cold" and Staff Notes "read it, name it", which is the register the rest of the
set already uses. The Italian for Staff Notes needed to be shorter than the
English, since NOTE SUL PENTAGRAMMA is the longest title in the app and leaves
its tagline the least room.

**The chooser follows the splash now.** Flat mid-tone read muddy behind pastel
cards, flat neutral read bland — both were flat, which was the actual problem.
The splash already solves the same brief, a field that has to hold anything in
no particular theme, and it does it with a fall from near-white down into the
floor. Sharing the recipe also means the app opens on one surface and stays on
it: splash into chooser, no cut.

**The last two muddy darks.** The fork button and the havens were the remaining
places a warm ink pinned against the floor was sitting on a near-white card,
where it reads brown rather than warm. Both lifted. The havens took a second
pass: gold reads instantly by hue, but hue alone strands anyone who cannot use
it, and at the first value the luminance step off a plain segment was 1.09. The
shipped gold is 1.8, and a cleared haven 2.5, so it is findable either way.

**Two more audit blind spots, both found by this pass.** It could not read
color-mix output, so any gradient starting with one made the backdrop walk fall
through to the page ground. And it treated background-clip:text elements as
having a painted box — those paint into the glyphs and nothing else, and since
the gradient is always an accent, it invented a failure every time. Fixed both:
thirty-one failures cleared, none introduced.

---

## v0.112.8 — the header wrap, the bland ground, and an audit that could not see color-mix

**The header tagline.** The subtitle was shortened once, but that fixed the hub
card, not the header — a different layout with a fixed-height box that the title
scales to fit. The base rule sets nowrap with an ellipsis, which works on the
title alone; with a subtitle appended inline, the SPAN inside still wrapped,
because the ellipsis belongs to the block and not to its inline child. So the
second line ran into the rule underneath. The row is a flex line now with the
ellipsis on the subtitle itself, where the overflow actually is. Header height
goes from 38px back to 19 on the longest one, and the shorter modules are
untouched.

**The chooser ground was bland because neutralising it took its modelling too.**
Fixing the muddiness left a flat field with two pools at 3 to 9 percent. It gets
what the module pages got: a warm key from above, a cool fill at the lower
right, a cool lift at the left, and a real top-to-bottom fall. Neutral in hue,
not neutral in modelling — those are separate decisions and only the first one
was wanted.

**The picker cards were pale because five sixths of each was neutral.** They
mixed 10% of the module colour into white at the top and then ran to the
un-themed surface for the rest of the height, so only the lid carried any
identity. The colour runs through the whole face now, 26% down to 9% and back up
at the foot, with the same four-layer shadow and rim the module cards got.

**And the audit could not see color-mix.** Both its colour parser and its
gradient extractor only knew rgba(). A gradient whose first stop is a color-mix
serialises as color(srgb ...), so the backdrop walk fell straight past the card
to the page ground and reported failures for text that is comfortably legible on
a pale face. Fixed in both places. With honest backdrops it found something
real: the peek labels mix 52% of the module colour into ink, which was tuned
against a nearly white face and lands at 3.5-4.0:1 against a tinted one. 34%
now. Thirty-one failures cleared, none introduced.

---

## v0.112.7 — the status colours had the same two-grounds problem

**The stats chart was a row of near-black bars.** in-tune, sharp, flat and metro
are pinned dark enough to clear 4.5:1 as small text on the floor, same as the
accent was. Used as a filled bar on a near-white card they measure 9.4 to
10.5:1 — and a filled shape is a graphical object, which needs 3:1, not 4.5.
So the chart was reading correct and heavy at the same time. A lifted set now
exists for fills and lands at 5.2 to 5.8:1 on a card: still comfortably above
the graphical floor, and green again rather than nearly black.

**The stats sheet was still wearing the page floor,** the same fault the
settings sheet had: a raised panel that fades to --bg-1 ends up with the page's
own colour along its bottom edge. Paint only — the geometry stays in the base
rule, which is the mistake that made settings unusable two versions ago.

**And the module picker was muddy for a reason.** Its ground carried real chroma
at hue 293, a violet-grey, and four cards in four other hues sat on it — one of
them lavender, right next to it. Four hues on a fifth hue is what makes a screen
look dirty rather than colourful; the ground was competing with everything it
was supposed to hold. Near-neutral now, a touch warm, at the same depth: the
seamless-backdrop trick a product photographer uses so that objects in different
colours can share a frame. The chooser stops being a colour and goes back to
being a surface.

Contrast: no new failures, project audit steady at 26, module audit zero.

---

## v0.112.6 — one accent was doing two jobs, and off did not look off

**Why the dark colours read harsh.** --accent is pinned at OKLCH L .36 because
it has to clear 4.5:1 as small text on the FLOOR, which is the hardest ground in
the app. But almost everywhere you actually see it — chip borders, labels,
controls — it is sitting on a CARD, two full steps lighter, where that same
value measures 9.5 to 10.9:1. That is not colour, it is ink, and ink on a pale
card looks severe.

One token cannot serve both grounds. --accent-lift sits at L .46 for card-borne
use and clears 6.2 to 7.1:1 there, which is comfortably above AA while reading
as a colour again. The floor keeps the darker value, because on the floor it is
genuinely needed. Settings chips take the lifted one for their border and label.

**The havens were the hardest thing to find on the ladder,** which is backwards
for the one mark that tells you where you can fall back to. In dark a gold rim
glows against near-black and reads instantly; on a light card the same rim is a
thin line on a pale ground. Filled in light now, with the rim kept as the edge
rather than as the whole signal. A haven segment measures 7.4:1 against a plain
one, where before it was a hairline.

**An unlit lamp was a white box on a white card.** In dark it is dark glass,
which explains itself. On paper the equivalent of off is recessed, so an unlit
lamp is pressed into the card: the token drops a step, and it takes the standard
soft-UI inset pairing — a dark shadow at the top edge where the surface falls
away and a light one along the lower lip where it catches the ambient. Same
technique as a raised chip, run in reverse. It now sits 1.36:1 below the card
instead of level with it.

That inset pairing is the one genuinely new idea from reading around the current
material on depth-driven UI, and it is the piece light was missing: raised
elements were getting the four-layer treatment while recessed ones were getting
nothing at all, so half the vocabulary was mute.

Contrast: no new failures, project audit steady at 26, module audit zero.

---

## v0.112.5 — light gets volume the way paper does

Side by side, dark reads three-dimensional and light reads fat. The reason is
that dark's depth is all emission: every card has a lit rim, the page carries a
theme-tinted bloom from above and two smaller pools, icons glow. None of that
transfers — a glow on a light ground is a smear, which is why it was stripped in
the first place. But nothing was put back in its place, so light had the geometry
of a design with no lighting model at all.

What does the same job on paper is edge and shadow. Cards now get all four
things that describe a real object on a lit page: a defined rim, a crisp
highlight along the top where the light strikes, a contact shadow directly under
the edge with a wide far falloff behind it, and a diagonal fall inside the card
so it is a surface rather than one flat tint. It is the same information dark
gets from a glowing border, said the other way round.

**The page field got dark's structure too.** Dark paints three theme-tinted
pools; light had a single top-down ramp and a 7% tint, so there was nothing to
read across the screen. Same three-pool geometry now, opposite physics: a warm
daylight bloom from above, a cooler accent lift at bottom right, a faint accent
pool at left. A warm key with a cool fill is what stops a light field reading as
one wash — it is how a real room looks and it is why the flat version felt
synthetic.

**And the selected chips had gone dark in every theme.** They mixed 70% of
--theme over white, which was right when --theme was a mid-tone. The light ramp
took the accent to OKLCH L .36, so the same mix landed at 3.0-3.9:1 against its
own label: a dark slab sitting in a pale sheet, in all four themes. A selected
chip in light should be a tinted LIGHT chip with a firm edge, not an inverted
one. It is 16-26% over white now with the accent as the border and the label,
which is legible and still unmistakably ON.

Contrast unchanged: no new failures, project audit steady at 26.

---

## v0.112.4 — the settings panel was unusable, and it was my fault

Adding the light-mode background override in v0.112.2 split the base rule. I
closed `.settings-modal-content` after its first property and opened
`body.light .settings-modal-content` before the rest, which handed max-width,
padding, max-height and overflow-y to the light selector alone. In dark the
panel had no width limit, no padding and no scrolling, so it rendered oversized
and immovable — and since the theme switch lives inside it, there was no way to
get to light mode and out of the problem.

The base rule owns geometry again; the theme rule may only repaint. Verified in
both themes: 366px wide inside a 420 max, correct padding, scrolls, sits inside
the viewport.

Sentinel-pinned, because the shape of this mistake is not specific to one
selector. Any theme override that reaches past paint into layout can strand a
control that only exists inside the thing it broke.

The lesson for the audits: everything I checked after that change was a
full-screen module view, and every one of them passed. A modal that only opens
on a tap was never in the frame. Screens behind an interaction need opening.

---

## v0.112.3 — light was flat because I had taken the depth out of it

The complaint that dark looks alive and light looks flat turned out to be
measurable rather than a matter of taste. Compared side by side:

    dark   card chroma .037-.042   fall inside one card .029
    light  card chroma .011-.015   fall inside one card .019

A third of the colour and two thirds of the modelling. On top of that light has
no glows, which were removed on purpose because a drop-shadow on a light ground
smears rather than emits. Three of the devices that give dark its depth were
missing from light, and two of them were mine.

Cards carry their hue again, chroma .038 falling to .026 across the card, with
the internal fall widened to match dark's. Every card is now a surface with a
top and a bottom rather than a flat rectangle, and each one wears its module's
colour instead of being white with a rumour of it. Floor-to-card separation is
unchanged at 1.84-1.89.

**The launcher's quick-access chips were wearing the dark palette.** Their
colour comes from --pc, which falls back to the dark theme's cyan, so in light
they were a 9% tint of a colour that does not exist in the light palette, on a
light ground: effectively invisible, which is exactly how they looked in the
module picker. They are small raised chips now, white with a tint of the tool's
own colour, a real border and a contact shadow, and an icon dark enough to read.

**The splash has moved with all of this** — it builds from --surface, --bg-1 and
--bg-0, so it followed the ramp, the chroma equalisation and this pass without
being touched directly. Checked: it runs light at the top into the floor at the
bottom, which is the direction it was fixed to in v0.112.1.

No new contrast failures; the project audit stays at 26 with none introduced.

---

## v0.112.2 — why light mode read washed out and heavy at the same time

Two faults, and between them they explain a complaint that sounded like it
contradicted itself.

**The four floors were not the same weight.** The ramp set every floor to the
same OKLCH lightness and then multiplied each hue's existing chroma by the same
factor — which preserved the inequality it was supposed to remove. Measured:
metro's gold sat at C .137 and tools' mint at C .128, while tuner's blue sat at
C .054 and train's lavender at C .066. Two and a half times the colour at
identical lightness. Perceived weight is lightness AND chroma, so two modes read
heavy and two read washed, from what was meant to be one recipe.

Chroma is absolute now, .075 on every floor. Gold and mint come down a long way,
blue and lavender come up slightly, and all four sit at the same weight with
their hue intact. Separation holds at 1.87 to 1.98.

**The daylight wash was repainting the top of the screen.** A white overlay at
62% at the top falling to 3% at the bottom, tuned when the floor was pale. On a
deeper floor it means the top third is nearly white and the bottom is the raw
floor colour: washed out up there, heavy down here, on every screen. Measured
down the left gutter the swing was about 90 points of luminance top to bottom.
It is 20% to 5% now, and the swing is 18 to 19 points, the same on all four
modes. A light field should be felt, not seen.

**And the sheets were dissolving into the page.** Settings, the favourites
sheet, the launcher sheet and the quiz sheet all ran from the card colour at the
top down to the page floor at the bottom. That reads as depth in dark, where the
floor is the darker end and a panel fading toward it looks like it is receding.
In light the floor is the darker end too, so a raised sheet ended up wearing the
page's own colour along its bottom edge and stopped looking raised at all. They
stay on raised colours now.

Contrast: no new failures, nine fixed, none made worse; the project audit goes
42 to 26 with none introduced. Two per-theme inks and the launcher hint needed
re-pinning by a hair as the floors moved.

**The audit was also measuring elements mid-fade,** which is why the launcher
hint kept reporting a different failing ratio on every run. It now skips
anything with an opacity transition in flight, and three consecutive runs agree.

---

## v0.112.1 — the light gradient ran the wrong way, and the climb got twice as long

**Light was coming from under the floor.** The splash gradient ran from a pale
top, down through the ground colour in the middle, and back up to near-white at
the bottom. That put the brightest band of the screen underneath everything,
which is why cards looked weakest exactly where they sit and the whole thing read
bottom-heavy. It runs one way now: lit at the top, settling into the floor and a
shade below it at the bottom.

The launcher had the opposite problem and the same cause. Its ground is a literal
rather than a token, deliberately, so the chooser does not change colour with
whichever module you last used — but that meant the ramp could not reach it, and
at OKLCH L .787 it stayed lighter than every module floor once those dropped to
.745. On the one screen that is nothing but cards, the cards had the least to sit
against. Re-pinned to ramp depth, still less chromatic than any module so it
reads as a null state. The lower radial pool is softened and lifted off the
bottom edge as well; anchored at 104% it pooled light under the content. The
crossfade veil tracks it exactly, or the background appears to change colour
mid-fade.

**The climb is twenty-four rungs.** Twelve was too short to be hard — two warm-up
rungs, four in the middle, six that could bite, and a clean run only had to
survive six real questions.

Four distance bands now instead of three, because doubling the length without
adding a step would just have meant more of the same: WIDE at a fourth or more,
OPEN at a third to a fourth, CLOSE at a tone to a minor third, ADJACENT within a
tone. Six rungs each. Havens sit on the first three band edges, at 6, 12 and 18,
so there are three places to fall back to rather than two, and each still means
what a haven has always meant here: the value is yours, and the lifelines and
replays refresh.

Values run 25 to 100,000, so a clean summit pays 200,000. The multiplier step
drops from a tenth to 0.08 because there are now twelve lifelines to spend across
four bands rather than nine across three; spend them all and you settle at ×1.04,
which is close enough to the floor that the difference between a careful climb
and a helped one is the whole score. Verified: clean summit 200,000, every
lifeline spent 104,000, a fall at rung 20 leaves 22,000, banking at 15 with two
lifelines gone pays 5,888.

All twenty-four rungs verified to deal four distinct options with the answer
present and every distractor inside its band's distance range.

---

## v0.112.0 — light mode gets a floor

Testers said light mode was washed out across the whole app. Measuring it agreed
and gave the reason: floor-to-card contrast was 1.16:1 in every one of the four
mode palettes. That identical figure across four independently chosen palettes is
the giveaway that it was a systematic architecture choice rather than four
decisions, and at that ratio nothing on screen reads as raised. Everything looks
like haze because everything is the same brightness.

**Generated from one ramp instead of picked by hand.** The four light palettes,
plus the un-themed fallback, now come from a single OKLCH ramp: floor at L .745
with chroma held high, card at L .965 with chroma pulled back, borders at L .52,
accent at L .36. OKLCH rather than HSL because equal perceptual lightness looks
equally deep across hues and equal HSL lightness does not, and because chroma
has to be gamut-aware — the earlier attempt in HSL multiplied saturation, which
did nothing at all for metro's gold and tools' mint since both were already at
the edge of what sRGB can show.

Separation now measures 1.84 to 1.96 across the four, with a spread of 0.12
between best and worst. The mode hue survives in the card as a whisper, which is
what keeps the four modes telling each other apart.

**Dropping the floor broke everything that was pinned to it,** and that was most
of the work. A before-and-after diff across twelve screens in all four modes
found 119 newly failing elements, every one of them text sitting directly on the
background rather than on a card. All resolved:

- The per-theme ink trio had been pinned against the card. The card is no longer
  the hard case, so the trio is pinned to the ground instead, at 7.0 / 5.5 /
  4.6:1. On the card, which got lighter, they now land 13.7 to 14.7.
- `--tab-accent` carries the bottom-nav labels and the session stamp, both drawn
  straight on the ground. Re-pinned with headroom, since the two contrast audits
  resolve the nav bar's backdrop differently and 5.3:1 clears both.
- The shared status colours — in-tune, sharp, flat, metro — had all fallen to
  around 2.6:1. Re-pinned to clear 4.6 on every ground and 8:1 on every card.
- Level chip and phase pills, deepened for the second time; the previous fix was
  measured against the old floor.
- The help button stopped being thinned to 90 percent opacity.
- The accent deepened with the floor, because it had to: at the old value it
  would have dropped from 5.24:1 to 3.66:1 on the new ground.

**Two long-standing failures fixed on the way past.** The session stamp's goal
text was half-opacity ink that never cleared AA even before this, and the panel
badge sat on a translucent wash so its contrast moved with whatever ground it
happened to land on. Both are real colours on real fills now.

**Seven hardcoded copies of the old tuner accent** were sitting in the string
face, the capo popup and the instrument pills, frozen at the old value while the
token moved. They read from the token now. The tonal-centre panel's greys were
left alone deliberately: that is an instrument face, not themed chrome.

Light failures across twelve screens: 150 down to 138, with none introduced.
The project's own light audit: 42 down to 25, none introduced. Dark mode
unchanged at 65, which is the point — nothing outside the light blocks moved.

---

## v0.111.4 — light-mode sweep of the module

A full pass over every Relative Pitch screen in light mode: practice, answered,
chromatic, the entrance settled, mid-game, the result, settings and stats, all
screenshotted and inspected rather than trusted to the contrast numbers.

The module holds up. Lamps, glows, ladder, hearts, the screen panel, the boot
sequence, the transport row and the utility row all read correctly on the light
surfaces, and the automated audit stays at zero failures in both themes.

One inconsistency found and fixed: on an unanswered card the big note reading
dimmed to placeholder grey while the Hz line under it stayed lit in the hit
colour, so half the display looked switched off and half looked on. Both dim
together now and both light together on the reveal.

The wider question — testers finding light mode across the whole app too light —
is a palette decision, not a bug, and it gets its own mockup file rather than a
quiet change: LightMode_Palettes.html, four palettes on the same components.

---

## v0.111.3 — four things on the intro that were not behaving

**THE RULES was restarting the entrance.** The toggle went through rlpRender,
which rebuilds the intro card, which replays the whole boot sequence from the
flicker. Opening a paragraph should not restart the machine. It edits the DOM in
place now; the card node survives, the ladder stays built, and the title does
not blink.

**A ghost B-flat was showing through the placeholder.** The unlit segment behind
the reading is what makes a lit one look lit, but that only works behind a real
value. Behind a two-dash placeholder it reads as a stray letter someone forgot
to clear. The ghosts appear once there is something to read and not before.

**THE CLIMB was sitting on the screen.** 22px above it now.

**START cut rather than handed over.** The intro vanished mid-word and the game
appeared fully formed, which is a page swap, not a machine changing state. The
intro lifts away over 220ms and the first rung arrives from below over 340ms.
The first note was also scheduled 350ms after the card was built, which put it
right in the middle of that; on rung one it waits 620ms instead, so it lands on
a settled screen. Measured at 854ms after the tap, with the transition classes
cleaned up behind it.

Reduced motion skips the hand-off.

---

## v0.111.2 — the intro stopped explaining itself

The second card described the three distractor bands and how close the wrong
answers sit in each one, and it did that before you had heard a single note.
Nobody can use that information at that point; it only becomes real once you are
in ADJACENT and everything on screen is within a tone. The game already prints
the band and its gap in the card head at the moment it matters, so the chips
were a manual for something that explains itself two seconds in.

Gone, along with the card holding them. The intro is one card ending on START,
which is also what the entrance animation was already driving at — the sequence
used to keep going for another half second after the button, fading in a second
card that pulled attention back off it.

The rules survive, because two things genuinely are not discoverable from play:
that lifelines cost multiplier, and that unspent ones expire at the band edge.
They live under a plain text link below the best line now. Closed it is one dim
line; open it is the four rules in place, no second card, and it collapses back.

519px settled instead of two cards and a scroll. The entrance now ends: START at
2.0s, best line at 2.1, rules link at 2.2, and the button starts breathing at
2.3.

---

## v0.111.1 — the intro ladder was showing somebody else's run

**The bars on the start screen were arbitrary, and worse than arbitrary.** They
lit rungs one to eight with nine standing tall, which was a number carried over
from the design mock and had nothing to do with the person looking at it. The
ladder sits on the intro to be the machine's memory of you, so it reads your
furthest rung now: cleared rungs dim, the one you reached standing tall, and a
caption saying FURTHEST 9/12 beside the multiplier you start on. A first-time
player gets twelve dark bars and NO RUNS YET, which still shows the shape of the
climb without pretending to a history.

**START makes no sound of its own.** The entrance is built so the chime belongs
to the build and the next thing you hear is the question; a cue on the button
sat between the two and blurred exactly the line it was meant to draw. Verified
silent at the tap, with the first note arriving on its own.

---

## v0.111.0 — the climb has an entrance

Arriving on the CHALLENGE tab used to look like a different page from the game:
a title, one line, a START button, and a stack of bars looping an attract
pattern. None of the machine you were about to use was on screen.

It is the same machine at rest now. The ladder, the twelve lamps and the
instrument screen are all present before you press anything, and they build
themselves once on arrival while a welcome chime plays over the top.

**The sequence,** five phases with one focal point each, measured in the app:

    0.12  the card lands and the screen stutters to life with its readings on it
    0.64  the ladder climbs a rung per tick, the record rolling up beside it
    1.32  ladder tops out; the lamps sweep once
    1.37  the record lands
    1.82  the title arrives on the chord, then the line and START
    2.42  the bands card follows, chips after it
    2.84  settled, and silent

The screen readings snap on inside the flicker rather than fading in afterwards,
because a display shows its content as it finds mains. Segments land with a
touch of overshoot instead of sliding to a stop, the rung you reached last time
gets a brighter pop as it grows tall, and once everything settles START takes a
slow three-and-a-half second breath.

**The chime lives entirely inside the build, and that is the point.** Once the
intro settles on your records nothing sounds again until you press START, so the
first note after that is unambiguously the question rather than a leftover
flourish. Verified: twenty-two sounds during the build, zero between settling
and START. It is bespoke rather than a cue-bank event, because it is tied frame
by frame to this animation and a user-swappable cue set would break the sync. It
still respects the module's own sound switch.

The idle sweep is one slow pass every two and a half seconds while you decide,
rather than the continuous chase the old attract loop ran.

**Two things the port needed that the mock did not.** The card's fade-in and the
staged reveal of its contents were sharing one class, so the moment the card
appeared everything inside it appeared with it; hiding is now a class on each
element, applied before the first paint. And the boot's timers are on their own
list that gets cleared by teardown and by START, so leaving mid-animation or
starting early cannot leave anything running — verified zero timers after exit.

Reduced motion skips the whole thing and renders the settled state.

---

## v0.110.9 — the chimes were scrubbing the note, and lifelines were free

**The chime after every correct rung had to go, and not for taste.** It fired a
pitched fifth immediately after the target note, in a drill whose whole job is
holding a pitch in your head. It was rinsing the thing you were being asked to
carry. What is left is the shape of a game show: a flourish when you press
START, then nothing but the notes until the run ends one way or the other.

The three remaining sounds — summit, loss, bank — go through the app's own cue
bank rather than being hard-coded arpeggios. That means they follow whichever
cue set the person picked and their per-event volumes, instead of ignoring every
audio setting in Settings.

**Lifelines were free, which made them admin rather than a decision.** Three a
band, expiring at the edge, so the only wrong move was leaving one unspent. They
cost something now: each one takes a tenth off the multiplier the final payout
is settled at. Start at double, drop a tenth per lifeline, floor at level. A
summit reached without asking for help pays 50,000 against 25,000 for the same
climb with help.

The multiplier sits under the ladder while you play, lime while it is still
clean, so the cost is in front of you at the moment you are deciding whether to
take the fork. The result screen shows the working — 25000 × 2.0, no help taken
— and the best take carries its multiplier into the intro and the stats sheet,
since a best score is now a settled figure rather than a rung value.

**The writing.** Every line in the challenge was a run of short declaratives,
which is the tell. "Twelve notes. Four answers each. One wrong and you leave with
your last haven." Three fragments where one sentence would do the work. All of
it rewritten in both languages to breathe: the intro line, the four rules, the
four result captions. The rules also stopped repeating the same
bold-lead-then-fragment shape four times in a row, and one of them now explains
the multiplier, which is new information rather than a restatement of the
replay budget.

---

## v0.110.8 — a voice for the drill, and the climb stopped being a list of lists

**Tone bank in settings.** The drill sounded on grand piano because that is what
the app's reference tone happened to be. It picks its own voice now, from the
same bank every other module uses, and swaps it in for the length of one note
before putting the app's setting back, so choosing a nylon guitar here does not
change what the Chords tool sounds like.

Both halves of the skin opt-out are in, because a tone row that does not ask for
one inherits the piano console's near-black button and the Chords tool's green
popup, and then ships looking broken on a Train card. The button override is
keyed on the modal id and the builder is handed ex-tonepop explicitly. Pinned,
since this is the third time that trap has come up.

**The climb was eleven stacked blocks.** A card of twelve ladder rows, then a
card carrying a header, the lamps, the screen, a replay button, a row of replay
pips, a caption under the pips, a caption over the lifelines, the lifelines, the
options, the verdict and the actions. Almost half of it was labelling the other
half.

Now it is one card of six blocks. The ladder is a horizontal strip of twelve
segments at the top, cleared rungs dim, the one you are on standing taller,
havens in gold, with a line underneath giving the rung and what is already
banked — the same information as twelve labelled rows in a fifth of the height.
The replay budget moved onto the screen as pips, where the hearts sit in
practice, so the two modes read the same way. Replay itself joined the lifelines
as one utility row of four, which is what it always was: something you spend.
And the screen's right-hand reading is what is on the line right now rather than
a lifetime best you cannot act on mid-climb.

The card is 624px, where the two cards together were closer to 930. Identical
across the reveal at rungs 1, 5 and 12, in both languages.

Lifeline labels lost a word each to fit four across — FORK, DROP 2, B OR W.

---

## v0.110.7 — the accidental toggle was rewriting your answers

In chromatic mode the answer input was seven letters and a flat/natural/sharp
toggle. Tap D-sharp, get it wrong, switch the toggle to flats, and the red mark
jumps to E. It is the same pitch class and the app is not lying, but it reads as
your own history moving under you. Worse on natural: the mark disappeared
altogether while the spent try stayed spent, so the card looked like it had
forgotten a guess it was still counting.

The toggle was the problem, not the marking. It was a mode you had to hold in
your head, it cost two taps per accidental, and it meant one button could mean
three different notes depending on state you could not see from the button.

**Twelve buttons instead, laid out as a keyboard.** Five accidentals on an upper
row, shifted half a column so each straddles the two naturals it sits between —
C-sharp between C and D, nothing between E and F, exactly where the gaps fall on
a real keyboard. Seven naturals below. Every note is one tap, every button means
one thing, and a wrong answer stays where you put it because the mark is keyed
to the pitch class rather than to a letter plus a mode.

Names come from the app's existing noteNaming preference, so solfège users get
Do-sharp and Mi-flat without the module needing its own setting. White-key mode
is unchanged, a single row of seven.

Verified all twelve reachable in one tap, marks stable across re-renders, both
pools and both input styles still answer correctly, and the card holds its
height through the cycle at 468 white and 513 chromatic.

---

## v0.110.6 — the free reference tone had to go, and the card lost a third of itself

**HEAR IT AGAINST A was a hole in the design.** Striking the fork costs you your
run; that button handed you the same A440 for nothing, and it arrived at exactly
the moment you would want it, right before the next note. The fork is supposed
to be the resource the whole module is built around. Removed, and pinned, so it
cannot come back as a convenience.

**The hearts now do what they do everywhere else.** The px-heart sprite has a
loss animation — a dark damage flash, then the heart drains and falls away
leaving a pip — and the module was using only its resting states. It fires now
on the try you just spent, and only that one: the flag clears on the next render
so a re-draw does not replay every heart you have already lost.

**The card was loaded, and three things were doing nothing.** The verdict line
under the answers said "it was E flat" while the screen two rows up already
printed the note and its frequency, so it was the same fact twice; mid-card the
key going red and the heart falling say "not that one" better than a caption
does. Gone. The fork was the biggest button on the card despite being the rarest
action, and it sat between the transport and the thing you actually tap — it is
one line now, below the answers, where a rarely-used destructive action belongs.
It also stopped announcing A440, since the button is the fork.

The practice card is 468px, down from 582 two versions ago. Still identical at
every step of the cycle, in both languages, in every input mode: 468 with letter
keys, 511 with the accidental row, 426 with the lamps.

---

## v0.110.5 — one transport row, and a screen that looks like a screen

**The buttons were in three places.** Replay sat on its own above the fork, and
the two reveal actions were stranded at the bottom of the card under the answer
grid. They are the same kind of thing — what you do with the note in front of
you — so they are one row of three now, where replay already was: AGAIN, NEXT,
AGAINST A, each with a small icon, all three the same width. Next and the A
reference are dashed and dimmed until there is an answer to use them on, so the
row never changes shape. Replay carries the accent, since it is the one you
reach for while you are still working.

That also took 69px off the card, because the reserved space at the bottom is no
longer needed. The card is 513px through the whole cycle now, down from 582, and
still identical at every step.

The climb keeps its single wide replay. It has no next and no reference tone, so
a three-up row there would have been two thirds empty.

**The screen.** It had the right shape but was still reading as a box with
numbers in it. Three things fixed that. Scanlines, one pixel on and two off,
multiplied over at low opacity. A corner vignette, so the middle sits brighter
than the edges the way a lit panel does. And the values glow rather than just
being coloured — the note carries a two-stop halo in the lit colour, the streak
gets a smaller one once it is above zero, while the labels take a downward
shadow so they read as etched into the bezel instead of printed on the glass.

All of it is off or inverted in light mode, where a glow washes out and an
etched label wants a highlight above it rather than a shadow below. Contrast
holds at zero failures in both themes.

---

## v0.110.4 — one screen instead of four scattered readouts

The card was telling you four things in four places. The note and its frequency
sat in a thin strip, the tries were two grey dots below the answer buttons where
nobody looked, and the streak was in a card of its own, a scroll further down,
rendered as twelve pips and a caption. Meanwhile the whole thing jumped when you
answered, because NEXT and HEAR IT AGAINST A only existed after a reveal.

**The screen.** All four readings live in one panel now, laid out the way a
tuner front panel would be: the run on the left, the note and its frequency in
the middle, the record on the right, and the tries on a strip underneath. It has
a proper inset and a glass highlight along the top edge so it reads as a panel
let into the card rather than a box drawn on it. The ghost segments behind the
note and the Hz stay — an unlit segment is what makes a lit one look lit.

The tries are the pixel hearts from Music Quiz and Rhythm Survival, the shared
px-heart sprite, so spending one looks the same here as it does there. Two grey
dots said nothing; a heart going out says it without a label.

The climb uses the same screen with the same geometry: rung on the left, best
take on the right, and the strip underneath carries what is on the line. That
also cleared a duplication, since the card header was printing the rung and the
value as well; it now says which band you are in and how close the wrong answers
sit, which is the thing you actually want to know at a glance.

**No more jumping.** Both action buttons are always mounted and simply disabled
until there is an answer to move on from, and the climb reserves the height of
its taller state so the bank row and the CLIMB button swap in place. Measured
across a full card cycle — fresh, one wrong, answered, next — the card is 582px
at every step, and the buttons do not move by a pixel. The climb holds at 663px
across the reveal at rungs 1, 5 and 12.

A disabled control still has to be readable, so it is a dashed outline in muted
rather than the 34%-opacity smudge it started as.

**Contrast, and an audit that was lying.** The app paints cards with a gradient,
and getComputedStyle reports gradient-painted elements as having a transparent
background, so the audit had been resolving text against the body colour two
levels up. Taught it to read the gradient's first colour stop, and to ignore
stops that are themselves translucent, which is what made the fork button look
like a 1:1 failure when it is fine.

With honest backdrops it found three real ones, all in light mode or in states
built from opacity: ruled-out letter keys at 2.08:1, dimmed to the point of
being unreadable by a .5 opacity that a real colour replaces; the lifeline
numerals at 4.36:1; and the option letters at 4.27:1. Both themes are at zero
across eight screens now.

---

## v0.110.3 — reset was disarming itself, and the drill opened mute

Three from on-device, and one more the fix uncovered.

**Reset never fired.** Arm-then-confirm, and the arming tap re-rendered the
stats sheet through rlpOpenStats — whose first line clears the armed flag,
because opening the sheet fresh should never inherit an armed reset. So tap one
armed it, the re-render disarmed it, and every tap was a first tap. The button
never even said TAP AGAIN. Split into rlpOpenStats, which opens fresh and
disarms, and rlpRenderStats, which redraws in place and touches nothing.
Verified: first tap arms and relabels, second tap zeroes the tab you are on and
leaves the other alone.

**The drill opened mute.** rlpInit dealt the first card with silent=true, a
leftover from the prototype where init ran before any user gesture. In the app
you arrive by tapping the card, so the module whose whole point is "hear a note,
name it" opened with nothing to name. It deals live now; the autoplay switch
still decides.

Fixing that exposed a ghost: the note rides a 350ms timeout, and leaving the
module inside that window sounded a note on a hidden panel. Both deferred sounds
— practice card and climb card — now check the panel is still visible before
playing, same guard as every other deferred callback in the module.

**NATURAL and CHROMATIC, not 7 and 12.** The pool picker was labelled with
counts. Counts are what the code sees; names are what a musician reads. Settings
buttons, the card-head summary and the stats sheet subtitle all say the words
now, in both languages — naturali · media · 2 tentativi reads like the app,
7 · mid · 2 read like a debug string.

Also swept content and flow end to end while in there: dirty cards do not extend
the run, the fork zeroes it, 50/50 never eliminates the answer and eliminated
options ignore taps, banking pays the rung below, the SUMMITED badge shows on
the intro, and the lamps input answers by pitch class so it works in any octave.
All held.

---

## v0.110.2 — the module survey: a leak, a lost chime, and the favourites hole

Asked to go back over the whole build with fresh eyes. Three real findings.

**The comet outlived the module.** exitExercise stops every exercise from a
hand-maintained list — ivStop, ceStop, roadtripStop and eleven friends — and
Relative Pitch was not on it. Worse, switching bottom tabs does not call
exitExercise at all, so the comet's requestAnimationFrame loop kept running at
60fps on a hidden panel while the user sat on the Tuner. On a phone that is
compositor work and battery for nothing, invisibly.

Fixed both ways. rlpTeardown is on the stop list now, and every frame loop —
comet, landing, intro attract — bails the moment its own panel is hidden, which
covers any path that hides it without asking. The auto-advance timer got the
same guard, since it could fire after exit and render a hidden panel back to
life, restarting the comet with it. Verified: RAF alive in the module, dead
after back, dead after a tab switch, alive again on re-entry. Both guards are
sentinel-pinned, because the stop list is exactly the kind of thing a refactor
tidies away.

**The favourites hole, and it was not ours.** The hub cards carry data-fav-id
and the star pin works, but the favourites sheet renders from FAV_META, a
separate hand-built registry — and neither Relative Pitch nor Staff Notes was in
it. Pin either module and it silently never appeared in the sheet. So Staff
Notes has been half-favouritable since it shipped and nobody noticed, which is
what happens when the same fact lives in two places. Both entries added, with
icons and launch handlers.

**Small ones.** The START chime on the climb got lost in the port; restored.
Checked the rest of the assumptions while in there: progUpdate is a shallow
merge onto the live object so nothing clobbers the nested challenge stats, and
it feeds the perfect-session and achievement bookkeeping for free; progAddXp
exists; every colour var the module leans on is defined app-wide; all 88 t()
keys and 6 data-i18n keys exist in both languages; per-module settings not
surviving Reset All Progress matches how every other module behaves.

---

## v0.110.1 — the ghost glow, and copy that did not sound like the app

Three things from the first look at v0.110.0.

**The ghost glow.** A soft blob was drifting across the card, out of step with
the lamps. It was the ambient bleed: a 132x150 radial gradient tracking the
comet head, standing 26px above the lamp row and 48px below it, so it swept over
the card header and the readout as a second light that never lined up with the
first. At the end of each pass it snapped back to the left edge, which is what
read as something moving the wrong way.

It was there to give the row some spill back when the glows were clipped. They
are not clipped any more, and the three-stop shadows do that job properly, so
the bleed is gone rather than tamed. Verified: every lit thing on screen is now
an actual lamp, and the overlay sits on its housing to the pixel.

**The subtitle.** Fifty-one characters and it ended on "the fork is a resource",
which is a thing written about a design, not a thing said to a person. Now "Hear
a note alone · name it · no reference first", 48 characters, which sits between
Chord Ear at 42 and Pitch Match at 56. Fixed in all three places the same string
lives: the i18n value, the hardcoded DOM default, and the Italian twin.

The rules card had the same problem in longer form. Each line lost a clause and
a piece of documentation grammar — "Each band is a stage. Clear one and its
value is yours whatever happens after, and you get fresh lifelines and a fresh
set of replays" became "Clear a band and its value is yours for good. Fresh
lifelines and fresh replays with it." Italian rewritten alongside, not
translated after.

**The folder.** EAR TRAINING still said three exercises and listed three. Now
four, with Relative Pitch named, and the folder subtitle leads with pitch.

---

## v0.110.0 — Relative Pitch

The Coming Soon card said "name notes by ear, sing any degree from a given
root". Half of that was already Interval Training's SING mode wearing a
different name, so the module that got built is only the first half: hear a note
cold, name it. No reference before the card, no key established. The only tools
are a note you carry in your head and an A440 fork, which is what the skill
actually is outside an app.

That framing decided the shape. The fork is a RESOURCE, not a difficulty slider,
so there is no anchor setting and no in-app note picker — picking your own
reference lets you cheese it. Drift is not a mode either; it is a number on the
practice screen, notes named since you last reached for the fork, because the
run falls out of the drill for free.

**PRACTICE.** A note sounds, you name it. Letter buttons, or the twelve lamps
themselves if you would rather tap a keyboard. Two tries by default. After a
reveal there is HEAR IT AGAINST A, which plays the fork and then the note, so
you hear the interval you should have been computing.

**CHALLENGE.** Twelve rungs, four answers a rung. The ladder escalates on ONE
axis: how close the wrong answers sit to the right one. Rungs 1-2 offer nothing
closer than a major third, 3-6 a tone to a third, 7-12 everything within a tone.
Same note pool throughout, same tone length, same everything else. Two rungs of
warmup, four in the middle, six where you can actually lose.

Havens at 2 and 6, which are the band edges, and lifelines and replays refresh
on the same edge. One boundary, three meanings: clear a band and its value is
yours, and you get three fresh lifelines and six fresh replays. Anything unspent
is gone. Six replays a band rather than three a note, so where you spend them is
a decision instead of a formality.

One wrong answer ends the run and you leave with your last haven, or nothing if
you never cleared one. Falling back to a haven and continuing, which is what the
first draft did, made banking pointless: a run you cannot lose is not worth
walking away from.

**What the design pass caught, in the order it hurt.**

BLACK-OR-WHITE was dead for a third of the game. The first band had been
white-keys-only, so "is it a black key" always answered no. That was a second
difficulty axis bolted onto the distance one, and removing it fixed the lifeline
and simplified the ladder at the same time. Sentinel-pinned, because a pool
creeping back into a band would bring the bug with it.

A miss taught you nothing. It named the answer and stopped, in a module whose
entire subject is how far apart two notes are. It now says "it was E-flat, you
were a semitone high", on the card and on the result screen.

The distractor fallback filled with random notes when a band could not produce
three, so the band that exists to guarantee distance occasionally served a
semitone. It sorts by distance now. Also pinned.

**The lamps.** The play surface is twelve lamps with a comet running left to
right while you listen, then the answer lands. Getting them to look like lights
rather than coloured boxes took three things: a housing with an inset shadow and
a lens gradient so an unlit lamp reads as dark glass, a three-stop glow so the
falloff is not a hard halo, and a white core above three-quarters brightness,
because a real emitter goes white at full output rather than more violet. Attack
is one frame, release is exponential on a 135ms constant; the first pass used a
linear tail and read flat.

Two bugs there. The glow was clipped by two `overflow:hidden` ancestors, and
even unclipped it sat inside each lamp, where the next lamp's opaque housing
painted over it. Glows now live in one overlay above every housing. That in turn
erased the key letters in keyboard input, so the captions moved into the overlay
too, above the light.

Only opacity and transform are animated. The glow shadows are painted once and
never touched, because animating box-shadow repaints a blurred area every frame.

**Colour.** The palette was already sitting on a complementary pair without
anyone deciding it: the Train violet measures 254 degrees, its true complement
is 74, and the in-tune lime is 84. Ten degrees off opposite is why the reveal
reads before you have read the label. Amber at 17 completes a rough
split-complementary, which is where the fork sits. 60/30/10, one accent lit at a
time.

Every lamp colour is a variable, so light mode is an override rather than a
parallel stylesheet — tighter bloom, denser fill, darker accents, because a glow
that reads on black washes out on white. Pinned, since hard-coded glows are
exactly what shipped the tone banks black twice.

**Contrast and type.** A pass with element opacity counted, not just colour,
found 124 failures across ten screens in the two themes. Nearly all of them were
labels dimmed with `opacity:.55`, which looks fine on black and disappears on
white. Those are real colours now. Type floor is 9px; there were 39 elements
below it, six at 7px, which had crept in card by card. Both themes are at zero
failures.

**Housekeeping.** Settings and stats use the app's own shells: `iv-cog-btn`,
`ce-stats-modal`, `progress-modal-close`, and the `iv-stats-hdr-btn` pattern
where STATS lives in the settings header, the way Staff Notes, Interval, Pitch
Match and Chord Ear all already do. Settings and stats persist inside progState,
so they ride the existing backup instead of adding a forty-eighth standalone
key. Audio goes through chordPlayMidi and inherits the soundfont and the master
volume. Seven sentinel pins added.

Stats are one window with two tabs rather than two windows. The per-note
accuracy stays separate between them on purpose: Challenge gives you four
options and Practice makes you name it cold, so folding a one-in-four guess into
"named first try" would quietly inflate it.

**Not done.** The module is Pro-gated by the existing rule, since FREE_TRAIN is
poly only; whether a brand-new module should be the free taste instead is a
decision, not an oversight. Nothing about feel, audio or animation has been
judged on a device yet — twelve glow layers at 60fps in an Android WebView is a
question, not a fact.

---

## v0.105.2 — reset all progress was revoking Pro

Asked to make reset clear the four keys it was missing. It was worse than that.

**RESET WAS TAKING AWAY PURCHASES.** resetProgress() rebuilt progState from a
literal typed out inside the function, and that literal had drifted: it omitted
hasPro, so a reset left the field undefined, isPro() went false, and a paying
user lost Pro until they happened to find Restore Purchases. The same omission
silently reverted uiScale, notifications, master volume, session goal and the
launch sound, directly under a comment claiming settings were preserved.

The literal is gone. There is now one PROG_DEFAULTS object; progState starts as
a copy of it and reset returns to it, so the two cannot drift again. What
survives a reset is a named list, PROG_KEEP_ON_RESET, and hasPro is on it
deliberately: revoking Pro is the testing button's job, and that button comes
out before launch. A purchase should not be reachable from a reset button.

**AND IT IS A CLEAN PROFILE NOW.** Reset was missing Tónale, Road Trip stats and
its adventurer flag, and both drum kit keys, because the list of things to clear
was typed by hand and had fallen behind. It reads BACKUP_KEYS_PROGRESS instead,
so a key added for one is never absent from the other. Saved metronome and ramp
presets, saved charts and pinned favourites now clear too; those were already
being wiped by the old literal, just by accident rather than on purpose.

Verified by running a reset over a fully populated profile: nine preserved
fields still correct afterwards, fourteen wiped ones actually empty.

## v0.105.1 — backup and restore, and the paywall hole it would have opened

Settings has a Your Data section now: one button writes a JSON file with
everything worth carrying to a new phone, and one reads it back.

**RESTORE IS REPLACE, NOT MERGE.** That is the convention for file-based restore
and it is the right one here. The case this exists for is a new phone with
nothing on it worth keeping, and merging two live copies is the sync problem,
which gets solved when accounts land rather than guessed at now. The merge
rules are written down in BACKUP_LEDGER.md for whenever that happens.

**hasPro DOES NOT TRAVEL, AND NOW CANNOT.** isPro() trusts progState.hasPro
directly and hasPro lives inside intonare_progress_v1, so a backup file would
have been a free Pro unlock for anyone willing to open it in a text editor and
change one word. It is excluded from the payload in both directions, the local
value survives a restore untouched, and there are two independent guards on it:
a sentinel pin and a named check in the new audit script. Both were tested by
removing the exclusion and confirming they fail.

Excluded alongside it: tapOffsetMs and masterVolume, which are measured against
one particular device and make the receiving phone worse if carried; and the
four same-day session fields, which would drop yesterday's practice into today's
goal tracking.

**THE KEY LIST WAS WRONG, TWICE OVER.** The first count of what the app persists
came to 42. The real number is 47. Three of the original 42 were prefixes rather
than keys, and four more are written through const identifiers and never appear
as quoted strings, so no amount of grepping for localStorage finds them. One of
those four was DK_SAVES_KEY: saved drum kit patterns, user-authored content, and
the single worst thing on the list to lose silently. The pref_ family was the
other near-miss; the generic name hides real settings including metronome
volume, SingSing difficulty and playback mode, and Road Trip difficulty.

**intonare_backup_audit.py** exists so that stops being a matter of memory. It
walks every persisted key and every progState field and fails if any of them is
not classified, because a backup gap is invisible: nothing breaks, users just
quietly lose that data when they change phones and nobody hears about it for
months. Currently 47 keys and 36 fields, all accounted for.

Restore validates before it writes anything. A file that is not ours, one that
cannot be parsed, and one from a newer schema are each refused with their own
message rather than partially applied. The confirmation sheet reads the backup
back before you commit: when it was made, which version made it, and the streak,
XP and achievement counts on both sides, so replacing is a decision made against
real numbers. Export is three tiers, the same shape as the share handler: native
file plus share sheet where @capacitor/filesystem is present, a browser download
where it is not, and the JSON through the share sheet as text as the floor.

## v0.105.0 — the save migration is now a function, because restore needs to run it too

Groundwork for backup and restore. Nothing changes on device; this build exists
so the next one can be small.

**THE MIGRATION LADDER MOVED OUT OF progLoad().** Every field added to progState
since the first release needs a default somewhere, because an old save simply
will not have the key and everything downstream assumes it does. That ladder had
lived inline inside progLoad, which was fine while boot was the only thing that
ever read a saved blob. Restore has to run the same ladder over an incoming
file, and two copies of it would drift apart within a release or two. It is now
progMigrate(s): it mutates and returns whatever object it is handed, so progLoad
can call it on the live progState during boot and restore can call it on a staged
copy later. The body is the old body, moved. The extraction was mechanical rather
than retyped, and the result was checked against the original across six shapes
of save, from empty to fully populated, with identical output every time.

**WHAT THE READ TURNED UP, AND DID NOT FIX.** isPro() trusts progState.hasPro
directly, and hasPro is stored inside intonare_progress_v1. A backup file is
plain JSON, so exporting one, flipping a boolean in a text editor and restoring
it would hand over Pro. localStorage is already editable in desktop devtools, so
the hole is not new; a backup feature would just hand it to every phone. hasPro
will be excluded from the export payload in both directions when the serializer
lands, with a sentinel pin to keep it excluded. Nothing about Pro changed here.

Two smaller notes from the same read, both for the next build. tapOffsetMs is
tap calibration measured against one specific device, so carrying it to a new
phone makes the timing worse rather than better; it belongs on the same
exclusion list, along with sessionTodayMs and the rest of the same-day scratch
fields. And the stats loop in the ladder reads s.stats[k] without checking that
s.stats exists, so a blob missing that key throws partway through and silently
skips every migration below it. Harmless today because progLoad's own try/catch
swallows it and a real save always has stats; worth a guard once an arbitrary
file can reach the function.

## v0.104.5 — the polish backlog was mostly the tools lying, and what was left

Cleanup of the findings that survived verification. Most of the list did not
survive, which is the useful part.

**ROAD TRIP COULD BE FAVOURITED AND THE FAVOURITE WAS BROKEN.** The card has
carried data-fav-id="exercise:roadtrip" since it shipped, but FAV_META had no
entry for it. Starring it produced a row with no label, no type and no icon: the
star worked, the favourite appeared, and it led nowhere. Twenty-six of the
twenty-seven entries were complete; this was the one gap. Now added with the
Train hub's own icon, and every entry has been checked for the full shape.

**THE DAILY QUIZ POPUP WAS ENTIRELY HARDCODED ENGLISH.** Six user-facing strings
in a flagship surface never translated: the completed line, VIEW RESULT, the "10
questions, one attempt" meta, the IN PROGRESS counter, RESUME and START. All now
go through t() with Italian twins. Also added `slow` and `fast`, which were
referenced by data-i18n from the scale speed slider and had never existed in
either dictionary, so both rendered as their English DOM defaults regardless of
language.

**HELP BUTTONS WERE TOO FAINT TO READ.** The `?` controls sat at opacity 0.6,
measuring 2.81:1 against a 4.5:1 requirement. Raised to 0.9. Nothing else the
contrast audit flagged was touched, and that is deliberate: the ghost chromatic
note row and the unselected metro tabs are faint because being faint is what
tells you they are inactive. WCAG exempts inactive controls, and flattening that
hierarchy would cost more than it gained. The help button is different because it
is something you are meant to find and press.

**WHAT DID NOT SURVIVE VERIFICATION.** The 82 missing i18n keys were 2. The
"body_it variants exist but render() doesn't select by language" error was wrong;
the Survival Guide has done `(_il && page.body_it) ? page.body_it : page.body`
all along, and the audit was reading a different render() from another module
because it used a bare find() for the first match in the file. The two launchable
cards "missing" data-fav-id are the Coming Soon cards, which correctly have none.
Of thirty contrast selectors, sampling real pixels found six of seven passing.

**AUDIT FIXES, since the tools generated most of that noise.**
- strings audit: render() lookup now starts from the C object instead of the top
  of the file, same first-match trap that had it reading the wrong STRINGS block.
- strings audit: cards with class `wip` or an `svcToast(t('wip_toast'))` handler
  are skipped by the fav-id check. There is nothing to favourite on an unreleased
  tool and a star there would be a dead end.
- Errors dropped from 20 to 9 without a single one being suppressed rather than
  understood.

**STILL HARDCODED, LEFT DELIBERATELY.** Nine remain and they want your wording,
not mine: the GENRE_ORDER table (ELECTRONIC, CLASSICAL / THEORY, ODD METER,
OTHER), the four polyrhythm grades (LOCKED IN, CLOSE, NEEDS WORK, OFF), and the
piano SUST pedal label. Two more are the Leg Tuner's own dev strings and never
need translating. The audit's remaining 'OCT', 'RESUME' and 'DAILY' hits are
false positives: it is flagging the STRINGS definitions themselves.

Verified at runtime: 1532 EN keys, perfect EN/IT parity in both directions, every
markup key resolves, all nine new keys return correctly in both languages, and
the Italian switch returns LENTO, INIZIA and VEDI RISULTATO. No console errors.

---

## v0.104.4 — the audio preflight was about to reintroduce the iOS quiet-audio bug

Sweep of the other startup subsystems after v0.104.3, checking the audio preflight
and the lazy song data against the mic and the sample engine. The preflight had a
real problem on iOS that no test in this container could ever have caught.

**THE PREFLIGHT BROKE A DOCUMENTED INVARIANT.** getAudio() carries the note that it
"only ever RUNS on a user gesture, long after parse". v0.104.2 started calling it
from an idle callback, which is not a gesture. That matters because building the
context calls _iosSyncAudioMode('first audio'), and that function sets
_iosAudioEverApplied as soon as an AudioContext exists, which permanently stops
later calls forcing through native's cache.

On iOS WKWebView does not build its audio engine until something actually plays
after a gesture. Preflighting would therefore configure a session with nothing
attached to it, let WebKit come up with its own defaults immediately afterwards,
and leave native's cache asserting the work was already done. That is precisely the
failure written up on _iosAudioEverApplied: audio quieter than either normal level,
stuck there, until a mic toggle changes micLive and bypasses the cache. Saving
115ms on the first tap is not worth reintroducing a bug that took that long to find.

iOS is now excluded and keeps the gesture-driven path exactly as it was. If the
platform check throws for any reason it assumes iOS and does nothing, so the unsafe
branch is the one that requires positive proof. Android and the PWA keep the win.

**AND IT COULD HAVE RACED THE LAUNCH MIC.** The app auto-starts the mic at launch
when permission is already granted, which is gesture-free on the native path. If
that had come up first, the preflight would have asserted a mic-off session
underneath a live mic. It now returns early when isListening is already true, since
in that case the mic owns the session and has built the context itself.

**TIMING, MEASURED.** load at 4526ms, splash gone at 7613ms, launcher entry at
7656ms, context built at 9057ms. requestIdleCallback waited out both the splash and
the entry animation on its own and landed in the first genuinely idle moment after,
which is exactly the behaviour wanted and the opposite of what the RIFFS idle warm
did in v0.104.1. Only one AudioContext is ever constructed.

**EVERYTHING ELSE CHECKED CLEAN.** The sample engine does not preload at boot and
never did, so lazy RIFFS cannot have disturbed it. Nothing reads RIFFS during boot;
it is still lazy after twelve seconds of idling. No getUserMedia call at boot in
this environment, the mic autostart being Capacitor-gated. The isListening guard
cannot throw: it is typeof-tested, wrapped in try/catch, and the preflight runs
after load by which point the binding exists.

Re-ran the full fifteen-scenario matrix and the data fidelity check on this build:
all pass, 59 songs, 1802 ctl functions, 76,586 notes, fingerprint 8814428228214,
Road Trip 38 entries and 21 untuned, no console errors.

---

## v0.104.3 — the setMode deferral broke reduced motion, and a full sweep of every entry path

Verification pass over the whole startup surface after v0.104.2. It found a
regression I had shipped the build before.

**REDUCED MOTION LANDED IN THE WRONG MODULE.** lnchGo takes an early exit when
prefers-reduced-motion is set: `if (reduce) { finish(); return; }`. Deferring
setMode into the morph's second frame in v0.104.2 meant that path returned before
the mode was ever applied. Tapping METRO with reduced motion on left you sitting in
the tuner, wearing the tuner's theme, with no error in the console. Confirmed
against the reconstructed v0.104.0 build, which correctly reported metronome where
v0.104.2 reported tuner.

The reduce path now calls the deferred applier explicitly. It also sets lnch-settled,
which it never did: lnchGoPin's reduce path always has, .mode-toggle is styled off
that class, and without it a reduced-motion user's toggle sat in its pre-entry state
permanently. That second half was pre-existing, not from v0.104.2.

**FULL MATRIX, ALL PASSING.** Fifteen scenarios at 4x CPU throttle: splash on and
off, picker on and off, pinned modules, dark mode, all four cards tapped under both
normal and reduced motion, and splash-off combined with a tap. Every one lands in
the right mode with the right theme, tears the launcher and morph down to display
none with the morph card emptied, sets lnch-settled, and logs no console errors.

**THE MORPH SEQUENCE IS CORRECT.** Traced frame by frame from the tap: the card
clone appears around 250ms with the launcher still fully opaque behind it, both hold
together to about 700ms, then the launcher fades from BEHIND the card between 830ms
and 950ms, and only then does the card itself fade and the morph layer tear down
near 1000ms. That is the documented intent and nothing is uncovered early at any
point.

**TWO FALSE ALARMS, RECORDED SO NOBODY RE-CHASES THEM.** A white screen appeared in
dark-mode screenshots during splash-off boot, which looked like a bad flash. It was
the test: appearance was forced to dark but the browser context was left light, so
`auto` resolved light and the screenshot was a legitimately white light-theme
screen. With the context actually dark, html and body backgrounds are rgb(0,0,0)
for the whole boot on both this build and the baseline. Separately, lnch-settled
reading false while the chooser is still up is correct; it is set at the end of the
morph teardown, so it only becomes true once a module has been entered.

**STILL OPEN.** With the splash off there is roughly 600ms of empty themed screen
before the chooser fades in, because the launcher waits for boot rather than the
splash. It is the correct colour and nothing pops, so it reads as a slow start
rather than a fault, but it is the weakest moment left in the sequence.

---

## v0.104.2 — the module entry animation was starting late, not running slow

Tapping a card in the chooser dropped frames before the animation finished. It was
two separate stalls, and neither of them was the animation.

**THE FIRST TAP OF A SESSION BUILT THE AUDIO ENGINE.** The audio unlock is bound to
pointerdown in CAPTURE, so it runs before the tap is even a click, and on the first
call getAudio() does `new AudioContext()`. Measured: first pointerdown 115ms, second
1ms, and 248ms inside a real tap with everything else in flight. So the first module
you picked stuttered and every one after it was clean, which is the kind of fault
that disappears the moment you try to reproduce it.

Construction does not need a gesture; only starting audio does. The context is now
built on an idle callback about a second after load, while the chooser is just
sitting there, and arrives suspended exactly as before. The gesture path is
untouched and still does the real unlock. If a user taps before the preflight runs
they pay what they paid yesterday, so it cannot regress.

**EVERY TAP REBUILT THE MODULE BEFORE THE ANIMATION STARTED.** lnchGo called
setMode() synchronously on its first line, and setMode builds the target module:
first-time canvas draws, csDrawKeyboard, hpRender, and a pile of
getBoundingClientRect reads, which was the single largest cost in the profile at
73ms of forced synchronous layout. The whole call blocked for 261ms, with 140ms of
style recalc over 627 elements and 65ms of layout, ALL OF IT BEFORE the morph drew
a single frame. Tuner felt smoother than the other three only because it is the
default mode and setMode had less to change.

It now runs two frames later, inside the morph: the first frame commits the
transform, the second lets it paint, then the module is built underneath. Nothing
about the look depended on the old ordering, because the palette was already held
by _themeHold and released in finish(), and the morph card is opaque over the whole
screen while the build happens. The no-morph fallback applies the mode immediately,
since in that path nothing is covering anything.

**MEASURED, 1.2s window after the tap, 4x CPU throttle.**

    module   frames          median            worst
    Tuner    33 -> 52    19.4 -> 17.7ms    243 -> 102ms
    Metro    10 -> 23    35.4 -> 21.4ms    290 -> 174ms
    Tools    14 -> 40    55.7 -> 17.3ms    259 -> 157ms
    Train    11 -> 32    48.1 -> 16.7ms    421 -> 237ms

Ten frames in 1.2 seconds is about 8fps, which is what "laggy" meant. All four now
sit near a 16.7ms frame. Not perfect: two to four frames per entry still cross
100ms, so there is more in there.

**NOT THE CAUSE, CHECKED AND RULED OUT.** The lazy RIFFS work in v0.104.1 does not
touch this; builtByTap was false on all four modules, so picking a card never
triggers the song build. And this was not a regression from that change either: the
reconstructed pre-lazy build measured the same or slightly worse, Train at a 79ms
median against 48.1ms. The morph code itself is clean, one rect read and one
deliberate reflow.

Verified all four modules still enter correctly with the deferred setMode: tuner,
metronome, tools and practice each land in the right mode with the right theme, the
launcher hides, and no console errors.

---

## v0.104.1 — the launcher was not sluggish, it was waiting for two and a half megabytes of piano

The grid felt heavy coming out of the splash. It turned out not to be the animation
at all, which is worth writing down because the animation is where anyone would look
first and the CSS there has already been tuned twice.

**WHAT IT ACTUALLY WAS.** Traced at 4x CPU throttle: a single 4.3s blocking task.

    RunTask            4309ms
    +- ParseHTML       4301ms   lines 25020 -> 85868
       +- EvaluateScript  3529ms   line 28443
          +- v8.compile      2434ms   notStreamedReason: "inline script"

V8 cannot stream-compile an inline script, so the HTML parser stopped dead while the
5.2MB block was compiled. RIFFS was 49% of it, and it was being compiled and
constructed at every cold launch whether or not anyone ever opened the piano. The
launcher was animating on a main thread that was busy.

**THE FIX.** The literal is wrapped in `__riffsBuild()` and reached through an
accessor. V8 only pre-parses an uncalled function body, so the compile moves off the
boot path and happens the first time a song is asked for. Measured over five runs
each: domInteractive 3417ms -> 2686ms, and the launcher grid appears about 520ms
sooner. Frames during the entry window were 70 before and 67 after, which is the
same within noise: this makes the launcher arrive sooner with less behind it, it does
not repaint faster.

An accessor rather than a variable so nothing else has to know. RIFFS.piano[id] in
Road Trip, RIFFS[inst][id] in the riff player, the `typeof RIFFS === 'undefined'`
guards and anything written later all work untouched. First read builds it, then the
property replaces itself with the plain value so there is no getter cost after that.
It cannot be `var RIFFS`; var creates a non-configurable window property and
defineProperty throws on it.

**TWO THINGS TRIED THAT WERE WRONG, BOTH CAUGHT BY MEASURING.**

Converting RIFFS to JSON was the first plan and it benchmarked beautifully: 77ms to
parse against 613ms to evaluate the literal, and smaller once gzipped. It would also
have been a silent catastrophe. Every ctls entry is an arrow function, 1802 of them
across 58 of the 59 songs, and JSON.stringify drops function values without erroring.
Every piece would have played with no pedal at all and nothing would have thrown. The
round-trip fidelity check missed it too, because it compared JSON.stringify(before)
against JSON.stringify(after) and both sides had already been stripped. A test that
cannot fail is not a test.

Pre-building on requestIdleCallback was the second, and it made the exact thing worse
that this was meant to fix. The 1.4s build landed inside the launcher's entry window
and starved the animation: 75 frames dropped to between 8 and 31 across five runs.
Removed. The cost is paid on first use instead, under a screen transition that is
already moving.

**THE TRADE, STATED PLAINLY.** Boot is ~730ms cheaper every launch. In exchange the
first piano or Road Trip of a session pays a one-time build, 1.4s at 4x throttle in
the container and presumably a good deal less on a real phone. Sessions that never
open a riff surface never pay it at all. If it turns out to bite on device, the next
step is splitting the build per bank so opening Road Trip only constructs the piano.

Verified identical to the old data, not merely working: 59 songs, 1802 ctl functions,
76,586 notes and a summed note fingerprint of 8814428228214 matching the previous
build exactly, with Road Trip reporting the same 38 journey entries, 21 untuned, and
the same duck factor on Fuer Elise.

**FOUND WHILE LOOKING, NOT FIXED.** The app-wide `*, *::before, *::after` rule puts
nine transitioned properties on 5,568 of 5,572 elements, which is why the launcher CSS
is littered with defensive `!important`. And 5,189 elements stay live behind the
launcher while an opaque surface covers them. Both are real and both are minor:
removing them moved the median frame from 30.3ms to 28.7ms. Style and layout are not
the problem here. UpdateLayoutTree, Layout and Paint together came to 1.1s across an
entire 8s boot, against 2.6s of v8.compile.

---

## v0.104.0 — dead code audit: four provable removals, and one that is not dead but wrong

A cleanup pass, run report-first because the last one backfired. The audit swept CSS
classes, DOM ids, i18n keys, top-level globals, function declarations, commented-out
blocks and the piano song data. Most of what it flagged was wrong, which is the finding
worth writing down.

**STATIC ANALYSIS LIES ABOUT THIS FILE, REPEATEDLY.** The first sweep called
`.rarity-common` dead. It is built at runtime by `` `rarity-${a.rarity}` ``. The second
sweep, rewritten to catch template literals, called five Italian i18n keys missing; they
exist, packed several to a line, and the line-anchored regex walked past them. A third
pass reported eight empty CSS rules, two of which were the regex breaking on comments
interleaved inside a live selector list. Every sweep needed a second sweep to correct it.
Of 299 CSS classes initially flagged as unused, the honest number after filtering is
much smaller, and it is still only a lead list rather than a delete list.

**WHAT WAS ACTUALLY REMOVED — 1,145 bytes.** Small, and that is the point; these are the
only four things that could be proven.

- Chordle's picker was declared twice. `chordleOpenSlot`, `chordleOpenSheet` and
  `chordleCloseSheet` appear at top level, then again twenty lines later as the two-card
  sliding sheet. Hoisting means the second set wins, so the first eighteen lines have
  never run. The dead copy has no `chordleLockedSlots` guard, no `chordlePMod`, no
  `chordlePCard`, and never calls `chordleInitPickerSwipe`.
- A global `_salamanderNotes` sat below the `SampleEngine` IIFE. Both of its call sites
  are inside that IIFE, which closes at what was line 57207, so they resolve to the copy
  declared within it. The global was never reachable.
- Eight empty CSS rulesets. Where the braces held an explanatory comment, the comment
  was kept and only the no-op rule dropped, so nothing that documents a deliberate
  non-choice was lost.

**SF_CAPO_FAMS WAS LEFT IN PLACE, AND IT NEEDS A DECISION.** It is the one top-level
global in the file with zero references, so by the rules of this audit it should have
gone. It did not, because of what it says. The live gate is
`CAPO_FAMILIES = ['guitar','bass','uke']`. The orphan reads
`SF_CAPO_FAMS = ['guitar','bass','uke','plucked']`, under a comment explaining that
fretted instruments only should get a capo. Those two lists disagree, and `plucked` is
mandolin and banjo, which take a capo perfectly well. So this is not leftover scaffolding;
it is the only surviving evidence of an intent that was never wired up. Deleting it would
quietly close a question nobody has answered. Either mandolin and banjo should get the
capo control and `CAPO_FAMILIES` is the thing that is wrong, or they should not and the
orphan goes. That is Daniele's call, not the audit's.

**MEASURED, NOT TOUCHED.** Eight piano songs still carry the dormant grid data kept for
rollback, and it is now counted per song rather than estimated: liebestraum 52,900 bytes,
moonlight 37,400, minuet_g 35,468, prelude_c 12,291, prelude_em 10,113, moonlight_3 9,598,
fuer_elise 3,434. About 157 KB in total, waiting on on-device approval song by song.
Separately, five Rhodes arrangements share a byte-identical left hand with their piano
twin: arabesque_1, nocturne, twinkle_stride, gnossienne and gymnopedie, roughly 60 KB of
exact duplication. Their right hands genuinely differ, since the Rhodes versions swap in
tremolo control calls, so only the left hand could be shared. That refactor couples two
songs together and has not been attempted.

The orphaned CSS clusters that survived filtering come to 232 rules and 36.5 KB, which is
0.36% of the file. They fall into coherent islands rather than scattered rot: the old
improv-tab drone markup, `groove-countin`, `tl-`, `tg-`, `rr-`, `ce-pool`, `ss-cents` and
the Leslie rotor. Each one is a removed sub-feature whose skeleton stayed behind. None of
them were touched, and none should be touched in a batch.

---

## v0.103.20 — the quiz audit was scoring the wrong text, and hid 129 giveaways

Daniele reported half-broken quiz questions and obvious answers, and proposed replacing
the whole bank. Two screenshots turned out to contain two different faults that look
identical on screen, and chasing them found a bug in the checker itself.

**THE AUDIT WAS MEASURING TRIMMED TEXT.** It ran every option through `trim_opt`, a copy
of the app's display trimmer, before comparing lengths. The app cuts options at about 60
characters. So STEM MASTERING — a 151-char correct answer against distractors of 26, 32
and 40, a 4.6x dead giveaway — was trimmed to 32 characters before measurement, scored
about 1.0x, and passed clean. The trimmer was hiding the exact fault the script exists to
find.

Measuring the raw options instead:

    before   Critical 0     Warn 100    "No criticals — good to ship"
    after    Critical 129   Warn 69

    Guitar Gods 13   Beatles 11   Jazz Legends 15   Rock & Metal 23
    Theory 14        Studio 14    Gear 20           Music History 19

129 questions, 11% of the bank, where the correct answer is more than 2.5x the average
wrong answer. That is what Daniele was finding by hand while the script said ship it.

**THE TRIMMER CUT SILENTLY, AND THAT BROKE A GOOD QUESTION.** ROOM TREATMENT's four
options are 78-89 characters, a 1.07x balance — genuinely well written. The trimmer cut
the correct one at its first comma:

    "Acoustic panels, bass traps, and diffusers installed to control reflections..."
    displayed as: "Acoustic panels, bass traps"

Shown beside two full sentences, the right answer read as a throwaway. The tester picked
a sentence and got it wrong. The question was fine; the trimmer lost it.

Trimmed options now end in an ellipsis and drop any trailing comma or bracket, so a cut
option reads as "there is more here" rather than as a deliberately terse answer.

**ON REPLACING THE BANK: the questions are not wrong, they are uniform.** Measured across
1,151: 48.9% open "What is", 23.2% "What was", 14.9% "Which". Ninety-one percent are a
definitional lookup. There are five "why" questions and two "how" in the entire bank, and
78.5% contain a quoted term because the scaffold is nearly always What is 'X'?. The
Studio pack runs overdubbing, mastering, parallel compression, sidechain, automation,
tape saturation, punching in, phase cancellation, mic placement consecutively, all in
that shape. That is the "doesn't feel human" complaint, and it is a rewrite of question
STEMS rather than a sourcing problem. No audit fixes it.

**OpenTriviaQA was assessed and rejected.** 5,579 music questions, CC BY-SA 4.0, clean
format. But it is pop-recording trivia rather than music education, it quotes copyrighted
song lyrics verbatim in the questions themselves, its apostrophes have been stripped
throughout ("Its", "shes", "Cant"), and CC BY-SA raises the same ShareAlike question as
the Krueger MIDIs at a scale of thousands.

---

## v0.103.19 — FUNK 4-ON-THE-FLOOR: decided, keep it

v0.103.18 established that this groove is musically a plain quarter click and left the
call open. Daniele's call: keep it.

Written into the file as a DECISION rather than an open flag, with the reasoning,
because the analysis sitting above it makes a compelling case for deletion and the next
person to read it will reach for the delete key.

The reason to keep is not resignation. A four-on-the-floor click is what a producer or a
dancer actually counts to, so it earns its place as a NAMED entry even though it is
musically identical to a click: someone browsing the funk list for it and not finding it
would conclude the app was missing something. Findability is the point, not novelty.

Tempos are also frozen as they stand. 56 of 60 set, graded 8 STRONG / 10 MEDIUM /
12 WEAK, with the four West African dance traditions left unset and each naming what
would settle it.

---

## v0.103.18 — accent sweep, and one groove that cannot exist in this engine

The last dimension nobody had examined. Three candidates came out of a mechanical pass;
two were my checker being wrong and one is real and unfixable by moving accents.

**Cleared: the 15 "all accent, no soft" grooves.** SON CLAVE, the rumbas, TRESILLO,
BOSSA, SHIKO, SOUKOUS, GAHU, KPANLOGO, BULERÍA, KOPANITSA and the rest. A clave has
strokes and rests, not a dynamic layer, so having no soft stroke is the correct shape
rather than a missing one.

**Cleared: MONTUNO.** Flagged as accenting a downbeat its comment called empty. Its
accents at 0, 3, 7, 11, 12 match its comment exactly; the regex had caught the phrase
"step 6 is silent here" and misread it.

**Cleared: MARCH 2/4.** Both beats accented with no weak stroke, which looks like a
flattened march. It is deliberate and sourced: Soundbrenner's definition contrasts a
march's "steady left-right pulse" against a jig's lilt, and the comment already said so.

**FUNK 4-ON-THE-FLOOR has no identity in a one-voice engine.** Its pattern is four equal
accents and nothing else, which is a plain quarter-note click carrying LESS than the
metronome, since the metronome at least emphasises beat 1. Every neighbour carries
something a click does not:

    DISCO                2 0 1 0 | ...   offbeat hat under the four
    BACKBEAT             1 0 0 0 | 2 0 0 0    2 and 4 in front
    MOTOWN               1 0 1 0 | 2 0 1 0    backbeat plus eighths
    THE ONE              2 1 0 1 | 0 1 0 1    the one in front
    FUNK 4-ON-THE-FLOOR  2 0 0 0 | 2 0 0 0    four identical hits

**And it cannot be fixed by moving accents.** Four-on-the-floor's identity is the
layering: kick on all four, backbeat on 2 and 4, hats between. Put the backbeat in front
and you have written BACKBEAT. Add the offbeat and you have written DISCO. This file's
own rule — put the layer that FIGHTS the meter in front — has no answer, because
four-on-the-floor does not fight the meter, it IS the meter.

Left as-is and flagged in the file. The alternatives are duplicating an existing groove
or deleting this one, and both are Daniele's call on-device.

**Origin sweep, prose half.** NEW ORLEANS and SECOND LINE carried origins that were near
synonyms — "New Orleans second line" and "New Orleans brass band" — which does not help
anyone tell two adjacent grooves apart. NEW ORLEANS is now "New Orleans funk / The
Meters", matching the record its tempo was sourced from.

**EN/IT parity: no drift, and the two failures found today were both mine.** A sweep for
Italian strings missing what the English says returned 34 hits, every one a false
positive: it was looking for the literal English word, so "Cuban → cubano" and
"Bulgarian → bulgara" read as missing. The pre-existing Italian was correct throughout.
The only two genuine twin failures this session were DEVR-I HINDI and NEW ORLEANS, and I
introduced both by editing the English and forgetting the twin.

---

## v0.103.17 — MOTOWN in one search, and SEVEN ROCK was mislabelled

**MOTOWN: 105, and it is the best-sourced number in the file.** The Temptations' "My
Girl", 1964, Hitsville USA. Five independent readings: 104, 105, 105, 104, 105. A
one-BPM spread across five sources.

It had been recorded CEILING REACHED after two style-level searches. It took one search
of a named record. That is the third time in this audit the ceiling turned out to be the
query, which is now written into the file next to all three.

**SEVEN ROCK was showing the wrong time signature.** The origin sweep started by checking
every origin string that states a meter against what the app actually sets, and found one
disagreement: the origin says 7/4, the app displayed 7/8.

The cause is structural rather than a typo. `sigMap` looks the denominator up from the
BEAT COUNT alone, so every 7-beat groove gets /8. That is correct for RACHENITSA and
DEVR-I HINDI, which are genuinely 7/8, and wrong for SEVEN ROCK, whose own comment cites
Brubeck's "Unsquare Dance" — a 7/4 tune. One lookup cannot serve both.

Grooves may now override with `denom`, and SEVEN ROCK sets `denom: 4`. **Nothing audible
changes:** 14 steps over 7 beats at the same per-beat tempo either way. This is a label
fix, and the file says so, so nobody hunts for a timing bug that is not there.

The same latent trap exists at 5 and 9 and is currently harmless: sigMap gives 5/4 and
9/8, which is right for everything in the table today. A future 5/8 or 9/4 groove would
need `denom` too.

**Four grooves now carry no tempo, down from nine at the start of the day:** SHIKO, GAHU,
KPANLOGO and FANGA. All four are West African dance traditions rather than recorded
genres, so there is no track database to read a figure off, and tapping along to a
performance is the remaining method.

Every origin string that states a meter now agrees with the app. The rest of the origin
sweep — the prose halves, which no check can verify mechanically — and the accent sweep
are still to do.

---

## v0.103.16 — two of the "ceilings" were my search terms

Daniele pushed back on whether the remaining unknowns were really unknowable. They were
not. Two came back inside one search.

**The mistake was the query, not the world.** For AFROBEAT, BHANGRA and MOTOWN I had
searched for "the tempo of style X", got nothing, and written CEILING REACHED. But the
method that actually worked earlier in this audit was searching a NAMED RECORD: that is
how NEW ORLEANS got 88 from Cissy Strut and TARANTELLA got its cluster. I never applied
it to the three commercially recorded genres on the list, which are exactly the ones
where track data is abundant.

    AFROBEAT   --  -> 132    Fela Kuti, "Zombie"
    BHANGRA    --  ->  98    Panjabi MC, "Mundian To Bach Ke" (98 and 99, two sources)

Both carry their caveats in the file. Afrobeat is often felt in half-time and this
pattern puts nothing on the four beats, so the cycle cannot be cross-checked from the
accents the way the funk family's were; if it runs double on device the answer is 66.
Bhangra's record is fusion pop over a hip-hop beat rather than a dhol ensemble playing
chaal, which is a real limitation on what it proves, and it is written down as one.

**MOTOWN still has no figure, and the right tool for it is not a website.** Play "My
Girl" or "Dancing in the Street" and use the app's own tap tempo. Twenty seconds, and
better evidence than any of the aggregators quoted in this file.

**Five grooves now carry no tempo, down from nine:** SHIKO, GAHU, KPANLOGO, FANGA and
MOTOWN. The four African ones are the genuinely hard cases, being dance traditions
rather than recorded genres, so there is no track database to read a figure off.

**An assert caught me pasting SHIKO's note into AFROBEAT** mid-edit, and a second guard
had to be rewritten because it tested for the word "suggestedBpm" appearing anywhere in
a block rather than being declared on a non-comment line. The cycle comments added in
v0.103.13 mention the field by name, so the naive check saw a key that was not there.
Same class of error as the duplicate-key sweep that first flagged three false positives.

---

## v0.103.15 — a PRACTICE tab for the patterns nobody plays

Four grooves in the library were invented for this app rather than transcribed from a
tradition, and they were scattered: 5/4 OSTINATO and COMPOUND 9 in WORLD, FIVE ROCK and
SEVEN ROCK in FUNK. So 5/4 Ostinato and Five Rock, which are the same kind of object,
lived in different tabs. They now share a PRACTICE tab (ESERCIZI in Italian).

    LATIN 14   AFRICAN 6   FUNK 16   WORLD 20   PRACTICE 4

**An ODD METER tab was considered and rejected, and the reasoning is worth keeping.**
It would have been a tidier nine grooves and dropped WORLD from 22 to 16. But it would
also have to take RACHENITSA, KOPANITSA, KARŞILAMA and DEVR-I HINDI, which are Balkan
and Turkish dances first and odd-metered second, and pulling them out of WORLD would
hide them from anyone browsing by region. More importantly it makes the category filter
ask two questions at once — "where is this from" AND "what meter is it" — and every one
of those nine then has two valid homes, which is what makes a filter unpredictable.

What actually unites the four is not their meter. COMPOUND 9 is 9/8, which is compound
rather than odd. It is that nobody plays them; they are exercises.

**The layout cost was measured, not estimated.** A sixth tab takes the row from one line
to two at 390-412px, costing 29px. At 360px it already wrapped at five tabs, so smaller
phones are unaffected. Shorter labels were tested in a real browser against the real
CSS: the only six-label set that fits 390px is AFRO / PRAC / MINE, and it clears by ONE
pixel, so any font substitution would wrap it anyway. Readable labels and 29px is the
better trade, and the numbers are in the file so the next person does not re-derive them.

**Also checked and found clean: the names.** The transliterations that could plausibly
be wrong were verified — Rachenitsa/Ruchenitsa, Maqsum/Maqsoum, Çiftetelli,
Kopanitsa/Gankino — and all are accepted forms. Nothing like the ESKISTA error, where an
Ethiopian name sat on a Turkish pattern, is present now.

**And a correction to what this changelog said one entry ago.** v0.103.14 described the
category field as filing jazz swing, Take Five and gospel under "funk" as though that
were an error. It is not. The picker has four tabs and there is no JAZZ, BLUES or
CLASSICAL among them, so FUNK is the least-bad home available rather than a misfiling.
LATIN and AFRICAN are both clean. The taxonomy is four slots doing the work of eight,
which is a different complaint and a much smaller one.

---

## v0.103.14 — last tempos, a user-facing error, and me breaking my own rule

**MAQSUM: 105.** Melodigging's Arabic Pop guide names Maqsum as one of the base iqa'at
and gives 70-90 for ballads, 95-120 for dance-pop. Maqsum is the everyday dance groove
rather than the ballad one, so 105 is the middle of the upper band. Graded MEDIUM: the
range is for Arabic pop broadly, not a figure stated for maqsum itself.

**5/4 OSTINATO: 100, declared CONSTRUCTED.** An invented vamp with no repertoire behind
it. Same class as FIVE ROCK.

**BHANGRA and MOTOWN: CEILING REACHED after a second search.** Bhangra now carries three
open problems at once: no tempo, sources that contradict each other on accents, and a
grid that was wrong until v0.103.4. Motown needs one named record with a verified BPM
and it is done.

**DEVR-I HINDI's origin line was wrong where users could see it.** It read "7/8 —
Turkish / Bulg. lesnoto", fusing two traditions that only share a meter: Devr-i Hindi
is a Turkish usul, lesnoto is a Macedonian/Bulgarian dance. Whether this exact pattern
also serves lesnoto was never established, so the claim was REMOVED rather than
rewritten. Naming only what is verified is the safer of the two.

**And then I did the thing this project has a standing rule against.** Having fixed the
English origin, I left the Italian reading "7/8 — turco / lesnoto bulgaro", i.e. shipped
the corrected string in one language and the wrong one in the other. Caught by an
EN/IT parity sweep run immediately afterward, which is the only reason it is not in the
build. Both now read "usul turco".

That sweep also found BOOM BAP's Italian origin was untranslated English ("East Coast
golden age"), now "East Coast, epoca d'oro". The other 15 identical EN/IT strings are
correctly identical: "Jazz / big band", "Fela Kuti / Nigeria", "Motown / soul" and the
like do not translate.

**State of the groove table.** Cycles 60/60. Tempo grades 7 STRONG, 8 MEDIUM, 14 WEAK.
Six grooves still carry no tempo: SHIKO, GAHU, AFROBEAT, KPANLOGO, FANGA, BHANGRA,
MOTOWN. Open questions that name their own resolution: KPANLOGO's grid CONFLICT,
ÇİFTETELLİ's cycle, and the aksak tempos.

Still unaudited, and worth saying plainly rather than leaving implied: CATEGORY
assignment, which is the filter users navigate by, and the groove NAMES themselves. The
category field currently files jazz swing, jazz waltz, Take Five, slow blues, gospel and
two prog-rock cells under "funk", and puts reggae, dancehall and calypso in "world"
while bossa and samba sit in "latin". Naming has been wrong once already: KARŞILAMA
shipped labelled ESKISTA, an Ethiopian name on a Turkish pattern.

---

## v0.103.13 — family 4, and SOLEÁ was running at twice its own range

All 60 grooves now state their cycle. The world set was left until last because its
arithmetic does not follow the other families, and that turned out to matter.

**COMPÁS SOLEÁ: 108 -> 48, and it was the worst error found in this whole audit.**

Flamenco tempo is quoted in COMPÁS COUNTS. This groove holds 12 steps that ARE the 12
counts, with beats:6, so one app beat equals two counts and a quoted figure must be
halved. At 108 it was running 216 counts a minute. Paul Bosauder, a working flamenco
guitarist in Seville, gives soleá as "traditionally interpreted at a speed of between
70 to 120bpm"; a production guide independently puts it at 60-80. So the palo whose
name comes from "soledad", described everywhere as slow and introspective, was playing
at nearly double the top of its own range.

**FLAMENCO BULERÍA: 120 -> 110.** The same article says bulerías is "the same
rhythmical and harmonic structure sped up to around 220 to 240bpm". Richter Guitar
gives 160-275, BeatKey 180-240. 220 counts is where all three overlap; 110 halves to
it. The old 120 sat at the very top rather than inside.

The pair matters more together than apart. They share a compás and differ mainly by
speed, which is what every source says. At 108 and 120 they were nearly the same
tempo, which made the difference between them inaudible. At 48 and 110 the
relationship the sources describe is actually there.

**The aksak set is flagged rather than fixed.** RACHENITSA, KOPANITSA, KARŞILAMA,
DEVR-I HINDI and SEVEN ROCK all now say their cycle is one bar and that tempo for them
is conventionally quoted per eighth, which is what the engine already does, so no
halving applies. But no tempo figure was found for any of them as a named style. Their
existing values are inherited from whoever first typed them and are graded WEAK:
unaudited rather than researched. That is a downgrade, not a fix, and it is the honest
label.

**ÇİFTETELLİ's cycle is left open.** beats:4 with 16 steps reads as one bar, but its own
origin line says "4/4 (8/4 cycle)". If the full cycle is twice the array, the tempo
needs halving like the claves. It is already the library's one pattern CONFLICT, so the
cycle stays open beside it rather than being guessed.

**Every groove now has a documented cycle: 60 of 60.** Tempo source grades stand at 7
STRONG, 7 MEDIUM, 11 WEAK. Nine grooves still carry no tempo at all: SHIKO, GAHU,
AFROBEAT, KPANLOGO, FANGA, MAQSUM, BHANGRA, 5/4 OSTINATO and MOTOWN.

The checker flagged my own prose twice more, on the phrase "not sixteenths" inside the
flamenco cycle note. Reworded rather than loosening the rule.

---

## v0.103.12 — grading my own sources, because they were not equal

Three families of tempos have been written up in one confident voice, and the sources
behind them are not the same quality. Every tempo claim now carries a TEMPO-SOURCE
grade and the audit script reports the spread.

    STRONG  5   SICILIANA, IRISH JIG, SLOW BLUES 12/8, NEW ORLEANS, SAMBA
    MEDIUM  7   the four claves, MONTUNO, THE ONE, TARANTELLA
    WEAK    5   TRESILLO, BOSSA NOVA, SOUKOUS, FUNK 4-ON-THE-FLOOR, SECOND LINE

**Two should have been flagged as I wrote them.**

The Chosic page used for SOUKOUS self-labels part of its content "(AI Generated)".
That was quoted as though it were research.

FUNK 4-ON-THE-FLOOR's 114 comes from a blogger whose own sentence is "by my entirely
non-scientific logic, 114 bpm is the funkiest tempo". That was written up here as
"sourced, loosely", which is too generous by some margin.

**What the grades mean.** STRONG is a printed tempo marking, an official dance body's
guide, or several independent readings of one named record agreeing. MEDIUM is a
genre-level figure from a commercial index or a careful individual, without a specific
recording behind it. WEAK is a single DJ-tool or SEO page with no stated methodology,
or a figure I derived by inference rather than found.

TARANTELLA sits at MEDIUM rather than STRONG for a reason worth repeating: its four
readings are algorithmic and all four mislabel the meter as 4/4. They cluster, which
is why the number is usable, but no human wrote 135 down anywhere.

**Nothing was changed on the strength of this.** The WEAK five are still the best
figures found, and a labelled weak number beats an unlabelled one. What changes is
that anyone reading the file, including me next session, can see which of these to
trust and which to replace first when a better source turns up.

---

## v0.103.11 — family 3, Latin: all 14 have a cycle now

Every Latin groove now states how many conventional bars its array represents, which
is the fact the tempo depends on. Two tempos added, one defended, one flagged as the
widest honest range in the set.

**TRESILLO: 95, and the cycle was read off the accents rather than assumed.** They sit
at 0,3,6 then 8,11,14, which is the 3+3+2 cell twice in SIXTEENTHS, so each cell is
half a bar and the array is one 4/4 bar. That rules out the eighth-note tresillo that
spans a whole bar; the spacing of three sixteenths settles it. Wikipedia's "Dembow
beat" confirms the dembow carries a 3+3+2 tresillo cross-rhythm, so reggaeton is the
reference: 85-100, with bpmcalc naming 95 as the global radio standard.

**MONTUNO: 90, derived rather than searched, and deliberately equal to SON CLAVE.** A
piano guajeo is written across the two-bar clave cycle, so it takes the same halving.
Salsa's 180 is already sourced on son32 in this file. A guajeo and the clave under it
disagreeing about tempo would be worse than either being slightly off.

**TUMBAO's 180 was checked and is correct, which needed saying in the file.** It looks
wrong sitting next to son clave's 90. They agree: son32 is a two-bar cycle at 90, tumbao
is a one-bar cycle at 180, and both land on 180 in salsa terms. The comment now says
not to "fix" it to match.

**SAMBA keeps 130 and admits the range is wide.** Ballroom samba's recommended
competition tempo is 48-56 bars per minute (Wikipedia citing the ISTD guide), which is
96-112 quarters; a Samba Batucada recording reads 135. Escola and batucada samba is the
faster tradition and is what this surdo pattern belongs to, so 130 sits at that end on
purpose. If it feels hectic, the ballroom end is the defensible alternative rather than
a bug, and the file says so.

HABANERA, CHA-CHA-CHÁ, CUMBIA, BOLERO and JOROPO kept their existing tempos and gained
a documented cycle. BOLERO's note points at its own origin line, which already flags
that this is the Spanish 3/4 form and the Cuban bolero is a different 4/4 one.

Three families done. Remaining: the world set (Balkan, Middle Eastern, European dances),
MOTOWN's tempo, and KPANLOGO's unresolved grid conflict.

---

## v0.103.10 — family 2, and a drumming history that was off by double

The funk and soul set. Cycle settled first, and for once it did not need a source.

**CYCLE: 1 bar, proved from the patterns.** BACKBEAT and MOTOWN accent steps 4 and 12
of 16, which is the snare on beats 2 and 4 of a single 4/4 bar; two bars would put
four backbeats in the array. Every other groove in the family accents quarter
positions of one bar the same way. So genre BPM goes in as written, no halving, and
the 2x ambiguity that stalled this twice does not apply here.

    NEW ORLEANS      --  ->  88    Cissy Strut
    THE ONE          --  -> 101    Funky Drummer
    SECOND LINE      --  -> 100    between two anchors, 88 and 112
    FUNK 4-ON-FLOOR  --  -> 114    break-tempo cluster
    BACKBEAT         --  -> 100    constructed default, labelled as one
    FIVE ROCK        --  -> 100    constructed default, labelled as one
    MOTOWN           --      --    searched, not found, still on the dial

**NEW ORLEANS overturns a source rather than agreeing with one.** A drumming history
puts New Orleans funk at "quarter note = 152-208" while also saying the style is
"easily interpreted in double time". Cissy Strut, the canonical record, is 88 BPM on
getsongbpm and sfrbeats, and songbpm's 176 is itself flagged there as half-time 88.
The 152-208 is the double-time count. Taken literally it would have run this groove at
twice the speed of the records it comes from, and it would have looked properly
sourced doing it.

**Two are labelled CONSTRUCTED rather than given a fake citation.** BACKBEAT is not a
style with a tempo; it is the snare-on-2-and-4 cell under most Anglo-American popular
music, played at any speed from a ballad to a punk record. FIVE ROCK is an invented
5/4 cell. Both get a neutral 100 and say plainly that it is a default.

**MOTOWN is still on the dial.** Searched in this pass, nothing found; the break-tempo
analysis covers funk rather than Motown. A named Motown record with a verified BPM
settles it.

**The checker caught me twice more, both times on my own prose.** Writing "swung-bossa
count" flagged BOSSA, and naming COMPOUND 9 inside FIVE ROCK's note flagged FIVE ROCK,
because "compound" is triplet vocabulary. First resolved with an acknowledgement
marker, second by rewording, since the reference was incidental. A checker that only
ever agrees with you is not doing anything.

---

## v0.103.9 — family 1 closed, and KPANLOGO turns out to be a real dispute

Going back for the four grooves left inheriting the dial found one tempo, three dead
ends, and a grid disagreement that matters more than any of them.

**SOUKOUS: 62.** Chosic gives soukous a typical range of 115-130 from artist tempo
data, with individual tracks reading 106, 130 and 144. 125 as the middle, halved for
the two-bar cycle, is 62.

**SHIKO, GAHU and KPANLOGO: CEILING REACHED on tempo,** and each says what would end
it. Shiko is filed under highlife, which sources describe only as "fast" with no
figure. Gahu is an Ewe dance rather than a recorded genre, so there is no track
database to read a number off. Kpanlogo is described as "a street party rhythm from
the Ga tribe" and nothing more. All three keep inheriting the dial, which is the
honest state rather than a number that looks researched.

**KPANLOGO's subdivision is downgraded from INFERRED to CONFLICT, and it is a dispute
about the GRID, not about accents.** globalmusictheory.com states the foundational
Kpanlogo rhythm is "often structured around 6/8 or 12/8 time signatures, which feature
groups of three pulses per beat". If that is right, a straight 16-pulse grid is the
wrong SHAPE for it, in the same way JAZZ SWING was before v0.103.4, and not merely a
quantisation of it.

Against that reading: Wikipedia's Kpanlogo article says the nono bell "plays the key
pattern or timeline of the music" and that the main bell part "is one of the most
common and oldest key patterns found in sub-Saharan Africa", which is the 16-pulse
family. And our array is byte-identical to SON CLAVE 3-2, a 16-pulse timeline, which
the groove audit already examined and accepted.

Two credible sources, opposite answers, on the thing this whole audit is about. It is
recorded rather than resolved, because picking one would be a guess dressed as a
finding. A Ga drumming method or a transcription of the nono part settles it.

Family 1 ledger: 1 SOURCED, 1 CONFLICT, 4 CEILING REACHED, 9 cycles established,
6 tempos set.

---

## v0.103.8 — family 1 tempos, halved for the cycle

First tempos set with the cycle length known, so they are right in genre terms rather
than right in app terms and wrong to a musician.

    SON CLAVE 3-2   110 ->  90     reads as 180 salsa (was 220)
    SON CLAVE 2-3    --  ->  90     had no tempo
    RUMBA CLAVE 3-2  --  -> 112     reads as 224 (was inheriting the dial)
    RUMBA CLAVE 2-3  --  -> 112
    BOSSA NOVA       96  ->  65     reads as 130 (was 192)

**SON CLAVE** now sits at the middle of the form. Salsa runs around 180 BPM across a
150-250 range, most social dancing 160-220. The old 110 read as 220, which is salsa
dura and timba territory, not a neutral reference for a clave.

**BOSSA NOVA was the worst of the five.** Its own defining description is the relaxed,
slower cousin of samba, and at 96 it read as 192 genre BPM, faster than the samba it
is defined as slower than. Reference points cluster near 130: Drumgenius has a plain
bossa phrase at 111 and "The Girl from Ipanema" at 180 in its swung count, and a Blue
Bossa backing track is 140. 130 halves to 65.

**RUMBA CLAVE is referenced to guaguanco,** which is the rumba style that actually
carries rumba clave. Drumgenius lists basic Havana-style guaguanco at 231 and a Robby
Ameen version at 217; halved that is 115 and 108, so 112 sits between them.

**The four African timelines got a cycle and no tempo, on purpose.** SHIKO, SOUKOUS,
GAHU and KPANLOGO have their two-bar cycle written down, but no tempo source was found
for any of them as a style. Halving an invented genre figure would produce something
that looks as researched as the five above and is not. They keep inheriting the dial
and each says so in the file.

Every one of these carries its source and its arithmetic in the comment, so the next
person can check the halving rather than trust it.

---

## v0.103.7 — cycle length declared, and a pin that was anchored to the wrong thing

**Method change first, because it is the point.** Cycle length, subdivision, tempo and
the user-facing origin line are all answered by the same paragraph of the same source.
Auditing them as four separate sweeps means opening sixty comment blocks four times,
which is how SICILIANA sat at more than double its tempo while three other audits
passed it. From here it is one pass per family that resolves everything about a groove
at once, and then that groove is not opened again.

**CYCLE is now written down for the timeline family.** Nine grooves, the four claves
plus BOSSA, SHIKO, SOUKOUS, GAHU and KPANLOGO, each carry a note saying the pattern
spans TWO conventional bars. This was never a new discovery; the CLAVE FAMILY encoding
note at the top of the list already said 16 steps is one app bar of sixteenths holding
a two-bar timeline in cut time. It had just never been written where a tempo decision
would trip over it.

The consequence is stated in each one: one app beat equals two beats of the style, so a
genre tempo must be HALVED before it goes in `suggestedBpm`. Son clave's 110 reads as
220 in salsa terms, against a genre that sits around 180. That is not corrected yet;
the tempo pass for this family comes next, and now it has the fact it needs.

**The SON CLAVE pin drifted, and it was the pin's fault.** It was anchored to the
`name:` line plus the steps line, because the array is not unique (KPANLOGO is
byte-identical, which the groove audit accepts as correct). Inserting a comment between
those two lines broke it, without a single value changing.

A pin that fires on edits which changed nothing trains everyone to ignore it, so it has
been rebuilt as the bare array plus an EXACT-COUNT guard: the pattern must appear
exactly twice, son32 and kpanlogo. Fewer means one of the twins was edited; more means
a third groove drifted into the same pattern, which is also worth knowing.

Verified by sabotage rather than by reading: altering son32's copy while leaving
kpanlogo's alone now reports "found 1, expected exactly 2" and fails the build. The
old pin would have caught that too; the difference is that this one no longer fails
when nothing is wrong.

---

## v0.103.6 — subdivision audit, family 1 of 4: the timelines

First real pass. The script in v0.103.5 could only check a grid against its own
comment, which is circular; this is the start of putting external sources behind the
claims so the check has something true to compare against. Same statuses the pattern
audit uses, and the script now reads them and reports a ledger.

**The research did not come back tidy, which is the useful part.** Three sources,
pulling different ways:

Magill (quoted in Riddim, arXiv:1705.04792) gives the general rule: West African bell
patterns "can nearly always be subdivided into a number of regular pulses (usually 8,
12, or 16)". That is what these arrays are and why they are straight.

Polak's "Rhythmic feel as meter" (2010) then complicates it. Uneven beat subdivision
"play[s] a substantial role in genres from Mali (Mande) and northern Ghana
(Dagbamba) but not in southern and central Ghana (Ewe, Asante)", explicitly against
"the widespread assumption that, in African rhythmic systems, the fast pulse in
general is structurally isochronous". So a straight grid is not universally right or
wrong; it depends on where the groove comes from.

And the quantitative study of Cuban guaguanco measured 186 clave cycles and found the
strokes are not deadpan even where the framework is isochronous: note 2 short, note 3
long, note 4 late, with the deviations "more or less cancel[ling]" so the final
stroke lands where the grid says. A step sequencer has no microtiming, so this is a
CEILING and is written up as one, specifically so nobody later "fixes" it by nudging
a stroke to a neighbouring slot, which would make the pattern wrong rather than
merely quantised.

**Ledger for this family, 6 grooves:**

    SOURCED          GAHU        Ewe; Polak names Ewe as isochronous, so this is the
                                 one groove the study settles outright
    INFERRED         KPANLOGO    Ga, Accra; same region, not one of the two peoples
                                 Polak names. Regional inference, not a citation
    CEILING REACHED  SHIKO       region not pinned by any source found
                     SOUKOUS     Congolese; outside the material studied
                     AFROBEAT    Nigerian; borrowing the Ewe result would be exactly
                                 the overgeneralisation Polak argues against
                     FANGA       Liberian; same

Four CEILING REACHED out of six is not a failure to research. It is what the sources
actually support, and each one names what would settle it.

**Still 32 grooves with no subdivision claim at all.** Three families to go: funk and
soul, the Latin dances, the Balkan and Middle Eastern set.

---

## v0.103.5 — subdivisions checked, and the checker made honest

New audit script, `intonare_subdiv_audit.py`. The pattern audit checked WHICH steps
are struck; this checks whether a groove's grid can express what its own comment says
is being played. It exists because the v0.103.4 bug was three grooves describing a
triplet feel on a duple grid while asserting that was unavoidable, and the wrong
claim had been copied between them.

**Result: no further wrong grids.** The first run flagged five, and all five were
false. MARCH 2/4 and KARSILAMA say "compound" only to contrast themselves with a jig
and with COMPOUND 9. FUNK 4-ON-THE-FLOOR had the word "swing" inside a URL. THE ONE
states outright that swing is a performance property and deliberately not encoded as
a grid position. TRAP's triplets are ornaments over a correct sixteenth base.

**A check that fires on things which are not wrong is worse than no check.** A second
version added GRID-FINER-THAN-USED, which flagged 31 of 61 grooves for using only
even sixteenths on a sixteenth grid. That is not an error; the spare resolution is
what makes a pattern editable. Demoted to an informational column rather than left
as a flag that would train everyone to ignore the script.

**Compromises are acknowledged in the file, not pattern-matched around.** Rather than
keep making the regex cleverer, a groove whose subdivision is knowingly a compromise
now carries a `SUBDIV-AUDIT: ok - reason` marker the script reads. Three do: TRAP,
plus BLUES SHUFFLE and BHANGRA, which were flagging on their own corrective text
describing the sixteenth positions they used to sit on. The reason is required, so
the marker cannot become a silencer someone pastes in to quiet the checker.

The script reports **FLAGGED: 0, acknowledged: 3.**

**What it does NOT prove.** 38 of 61 grooves make no subdivision claim in their
comments, so there is nothing to check them against and the script says so rather
than passing them silently. Their grids may be right; nobody has established it.
Closing that gap means writing a subdivision claim for each, which is research, not
tooling.

---

## v0.103.4 — three grooves were on the wrong grid, and the file said it was unavoidable

JAZZ SWING, BLUES SHUFFLE and BHANGRA are triplet feels. All three were written on a
sixteenth grid, and all three carried a comment saying a sixteenth grid could only
approximate a triplet, so the second stroke sat on the "a" as the nearest available
slot. GOSPEL 6/8 and the 12/8 pair pointed at those notes as precedent.

**That premise was wrong.** The grid is not fixed at sixteenths. `stepsPerBar` is
just the array length, so 12 steps over 4 beats ARE triplet eighths. The scheduler
divides cleanly, the beat markers land at 3 per beat, the pulse dots agree, and the
counting labels already carry a "1 + a" entry for that exact case. Nothing needed
building. The three grooves were simply written on the wrong grid, and the note
explaining why it could not be fixed had been copied between them.

    JAZZ SWING     [1,0,0,0, 2,0,0,1, ...]  ->  [1,0,0, 2,0,1, 1,0,0, 2,0,1]
    BLUES SHUFFLE  [2,0,0,1, x4]            ->  [2,0,1, 2,0,1, 2,0,1, 2,0,1]
    BHANGRA        [2,0,1,0,1,0,0,0, ...]   ->  [2,0,1, 1,0,1, 2,0,1, 1,0,1]

JAZZ SWING's two swung skips now sit on the LAST TRIPLET of beats 2 and 4, steps 5
and 11, which is literally where BYU Percussion and ArtistWorks put them. BLUES
SHUFFLE plays a real shuffle instead of a dotted-sixteenth impression of one; its
accents were not touched, only the grid. BHANGRA's chaal is now the four swung pairs
its own GCSE source vocalises as "dum-di, dum-di, dum-di, dum-di", which is what that
source's "4/4 (12/8)" meter meant all along.

These are the first three grooves in the library on a triplet grid.

**BHANGRA also had a duplicate `steps:` key,** the same array declared twice in one
object. JavaScript takes the last one so nothing ever misbehaved, which is why it
survived. Pre-existing, present in the file before any of this session's edits, and
found only because an assert expecting a unique match got two. A sweep of all 60
grooves for repeated `steps`, `beats`, `name`, `pulse` and `suggestedBpm`
declarations found no others.

**BHANGRA's accents are still contested and still flagged.** Its sources disagree in
opposite directions and this change keeps the old reading (strong on 1 and 3). Only
the grid moved.

**Still open: the swing control does nothing in groove mode.** `advanceNote()`
returns early in the groove branch, before the swing block runs, so the slider only
affects the plain metronome click. Arguably correct now that grooves can carry a real
triplet grid, but it is a silent no-op and the help text does not say so.

---

## v0.103.3 — the dots were lying about the pulse

Moving the audio to the felt pulse in v0.103.1 left the display behind. Three places
compute the beat grouping and after that change they disagreed.

**The pulse dots drew six under a groove you could hear pulsing twice.** They read
`pulseBeats || tsTop` and never learned about `pulse`, so a 6/8 groove clicked on
its two foot-taps while six dots animated underneath. Those dots are the picture of
that click; they now read the same felt pulse the scheduler does.

**The step grid and its counting syllables still use the notated beat, deliberately.**
That is the notation view: for a 6/8 groove it shows the six eighths, which is what
you want when editing a pattern and reading its structure. The pulse dots show what
you hear; the grid shows what is written. Those are different jobs and it is correct
for them to differ. Worth stating outright because it looks like the same
inconsistency that was just fixed and is not.

Caught by Daniele asking whether subdivisions had been checked, which they had not
been; the tempo work had taken all the attention.

---

## v0.103.2 — tempos taken from recordings, not from theory

v0.103.1 fixed the unit and left the numbers where they were, on the assumption that
a value written as a felt pulse was the right value. Checking each against what the
music actually gets played at says otherwise for three of them.

    IRISH JIG        --  -> 100    had no tempo at all; inherited the dial
    GOSPEL 6/8       --  ->  66    had no tempo at all; inherited the dial
    SICILIANA        96  ->  42    was too FAST, not too slow
    TARANTELLA      160  -> 135    above every recording found
    COMPOUND 9      160  ->  53    same sound as before, corrected unit
    SLOW BLUES 12/8  60      kept  52-60 is where the form sits
    GOSPEL 12/8      72      kept

**SICILIANA was wrong in the other direction.** The Clarinet Institute edition of
Bach's Siciliano BWV 1031 prints dotted quarter = 42, and both Wikipedia and San
Francisco Classical Voice describe the form as slow and melancholy. At 96 it was
more than twice that. It is the only value in this whole pass that was playing too
fast rather than too slow, which is a good argument for checking numbers against
recordings instead of reasoning about them.

**TARANTELLA came down.** Four recordings of Tarantella Napoletana read 127, 134,
136 and 149 foot-taps a minute. These are algorithmic readings and all four mislabel
the meter as 4/4, so they are a cluster and not a figure; 135 is the middle of it.
The old 160 sat above all four.

**IRISH JIG had no tempo at all,** so it inherited whatever was on the dial. Tom
Hanway gives the standard metronome setting for jigs as dotted crotchet = 100, Bill
Troxler gives 80-100, and Fiddle Hangout puts the range at 84-120 with dancers
preferring 110-120. 100 is where the session and dance readings overlap.

**COMPOUND 9 was deliberately held at the speed it already had.** It is a
constructed teaching cell with no recording behind it, so there is nothing to check
it against. Its old 160 was almost certainly entered as eighths, and it produced a
3.4-second bar that worked; 53 reproduces that same bar under the corrected unit.
Left at 160 it would have run to eight eighths a second. The comment says not to
restore the old number.

**GOSPEL 6/8's 66 is the weakest claim in the groove table and says so in the
file.** No recording or marking was found for that feel specifically. 66 sits just
above SLOW BLUES 12/8 at 60 and below GOSPEL 12/8 at 72, which is where the form
lives, but it is a considered default and not a citation.

Patterns untouched again; 48 pins held.

---

## v0.103.1 — BPM meant the wrong note

TARANTELLA felt slow because it was slow. It plays at 53 foot-taps a minute and its
own comment cites Wikipedia's "fast upbeat tempo."

**The groove patterns were never the problem.** Not one step array changed in this
entry, and all 48 sentinel pins held throughout. What was wrong is the unit the
tempo number was read in.

**`bpm` was being applied to the notated beat, not the felt one.** Selecting a
groove calls `setTS(preset.beats, ...)`, so a 6/8 groove sets `tsTop` to 6, and the
scheduler computed a bar as `secondsPerBeat * tsTop`. That makes BPM count EIGHTHS.
But a 6/8 bar has two beats, not six: ONE-two-three FOUR-five-six. Every value in
the file was written as the felt pulse, the way a tempo marking on a score is, so
each one played three times too slow. SLOW BLUES 12/8 had a twelve-second bar,
which is five bars a minute.

**Grooves can now declare `pulse`,** the number of felt beats in a bar, and the
scheduler uses that instead of `tsTop`. Anything that does not declare it falls
back to `tsTop`, so all the simple-meter grooves behave exactly as before and the
change cannot reach them. Seven declared it:

    TARANTELLA       2    2.25s bar -> 0.75s     53 -> 160 /min
    SICILIANA        2    3.75s bar -> 1.25s     32 ->  96 /min
    IRISH JIG        2    3.00s bar -> 1.00s
    GOSPEL 6/8       2    3.00s bar -> 1.00s
    SLOW BLUES 12/8  4   12.00s bar -> 4.00s     20 ->  60 /min
    GOSPEL 12/8      4   10.00s bar -> 3.33s     24 ->  72 /min
    COMPOUND 9       3    3.38s bar -> 1.12s     53 -> 160 /min

**Fixing `bpm` rather than the display was the smaller change, not the lazier one.**
`bpm` is read by tap tempo, the drum kit, progressions, the timeline and
`getTempoName`, and rendered in eight places. Leaving it meaning eighths and
correcting only what is shown would have meant patching all of those; `getTempoName`
was already naming compound tempos off the eighth rate and was wrong today. Making
`bpm` mean what a musician means by BPM fixes every one of them at once.

**Two shortcuts rejected, both of which look right until you check.**

Multiplying the seven values by three does not work: `setBPM` clamps at 300, and
five of them need more. TARANTELLA would want 480 and silently clamp to 300,
landing at 100 foot-taps rather than 160. It would have looked fixed and been wrong.

Inferring the grouping from the meter does not work either. "Divisible by three
means compound" gets 6/8 and 12/8 right and then mangles KARŞILAMA, whose 9/8 is
2+2+2+3, four beats of unequal length rather than three even ones. Every grouping
here is declared and taken from the sources already in the file.

**Deliberately left alone, and why.** The flamenco pair is not a compound-meter
case at all: their twelve steps are the twelve counts of the compás, not sixteenths,
so the arithmetic that applies to TARANTELLA does not apply to them. The aksak
meters (RACHENITSA 2+2+3, KOPANITSA 2+2+3+2+2, KARŞILAMA 2+2+2+3, DEVR-I HINDI,
SEVEN ROCK) have UNEVEN pulses, which a single `pulse` count cannot describe, and
their tempo is conventionally given per eighth, which is what they already do.
Whether they are individually too slow is a separate question and still open.

**The background click layer follows the felt pulse now.** In 6/8 it hits the two
foot-taps instead of all six eighths. It is off by default and has its own volume,
so it never touched the groove's own hits either way.

**Listen list.** Every one of the seven is now roughly three times faster, so all of
them want a hearing. TARANTELLA at 160 foot-taps and COMPOUND 9 at 160 are the two
to judge hardest: both are now genuinely quick, TARANTELLA's number is unsourced
beyond "fast upbeat tempo," and COMPOUND 9 is a constructed teaching cell that never
had a source to begin with. If either feels frantic the number is the thing to move,
not the pattern. IRISH JIG and GOSPEL 6/8 still carry no `suggestedBpm` and inherit
whatever is on the dial, which now means foot-taps rather than eighths.

---

## v0.103.0 — the ShareAlike debt, paid

Performance mode plays twenty-one recordings by Bernd Krüger, taken from
piano-midi.de under CC BY-SA 3.0 Germany. ShareAlike means an adaptation has to go
back out under the same licence, and until now the source comments in the file
claimed the adapted MIDIs were "published in repo" when nothing had been published
at all. That is now true instead of aspirational.

**Twenty-one MIDI files, exported back out of the app's own note data.** Not
re-downloaded from piano-midi.de and re-uploaded; exported from the exact
`perf:{notes,ped}` blocks the app plays, so what is published is what ships. All
twenty-one parse clean with balanced note-on and note-off, 423 KB total, from
Träumerei at 2:16 up to the Waldstein first movement at 10:18.

**The seven Rhodes variants are not published separately.** Their note data is
byte-identical to the piano version; the only difference is an empty pedal array,
because a Rhodes has no sustain pedal. Same adaptation, one file.

**The changes are named honestly.** Tempo map flattened to a fixed 120 BPM with the
rubato baked into absolute note positions, hands merged onto one track, velocities
round-tripped through a 0-to-1 float, pedal reduced to CC64 on and off, nothing
trimmed. Everything audible is still his playing.

**Credits now link to the adapted files.** Attribution without access is only half
of ShareAlike; the credits line points at the published folder.

**Two group titles were never translated.** "Performance sequences" and "Fingering
diagrams" sat as hardcoded English inside a bilingual credits screen. Both now have
`data-i18n` keys and Italian twins: Sequenze di esecuzione, Diagrammi di
diteggiatura.

Repo folder to push before this build ships publicly:
`credits/midi-sources/` with the twenty-one `.mid` files, a `README.md`, and an
`index.html` for GitHub Pages. Until that is pushed the in-app link is a 404.

---

## v0.102.24 — closing out: nothing left unexamined

Every groove in the table now has a status and a reason. DESCRIBED is empty. NONE
is empty. There is no entry left that asserts something without saying on what
authority.

**GOSPEL 6/8's frame is sourced and its decoration is flagged.** Practito on the
meter: 6/8 has two main beats, compound duple, each dividing in three, counted
ONE-two-three-FOUR-five-six with the emphasis on 1 and 4. Drumscore is specific
about the backbeat once you are in compound time: where a 4/4 backbeat sits on 2
and 4, the 6/8 equivalent goes on the fourth quaver. Drumhelper gives the same
skeleton as a starting groove, bass drum on count 1 and snare on count 4. So our
accents are the frame plus the backbeat, both verified. The four pushes on the
"and" of 2, 3, 5 and 6 are the gospel ornament on top, and nothing read pins them
there. Frame verified, decoration asserted, and the comment says which is which.

**The last three are marked CEILING REACHED, which is a finished state and not an
open task.** Each says what desk research established, what it could not, and
specifically what would settle it.

MONTUNO: the tumbao is sourceable because the bass has two named landmarks every
source repeats. The piano guajeo has no equivalent; it varies by tune, by pianist,
and by which side of the clave the bar sits on. What would settle it is a Cuban
piano method or a salsa pianist. What ships is one player's ear, which for this
preset is a better authority than another lesson blog.

SAMBA: the surdo half is solid, strong 1 and backbeat on 3. The tamborim carries
samba's identity and is exactly the part no general-audience source notates. What
would settle it is a bateria chart or a percussionist.

NEW ORLEANS: this one has a second problem underneath the disagreement. Second-line
drumming is explicitly not a fixed pattern; the Drummer Cafe notes that every
player has their own way of playing these grooves. So there is no single right
answer to converge on, only a well-chosen example, and this preset should be a
different well-chosen example from Second Line rather than a worse version of it.
What would settle it is Antoon Aukes' "Second Line: 100 Years of New Orleans
Drumming" or a New Orleans drummer.

**Final ledger: 57 of 60 vetted.** 49 sourced, 1 judgement call on conflicting
sources, 5 constructed teaching cells with their claims checked, 2 derived from
their parents by a stated rule, and 3 flagged with the reason and the remedy
written down.

That last number is the honest one. Three grooves in this library are as good as
research without a musician can make them, and they say so on their own faces
rather than in anyone's memory.


## v0.102.23 — the ledger was under-reporting itself

**FUNK 4-ON-THE-FLOOR was the last groove in the table with no comment at all.** It
is also the simplest thing in it, and the definition is the pattern: a bass drum
strike on each of the four quarter notes, creating a steady pulsating foundation.
Soundbrenner adds why nothing else is played, the kick marking every main beat so
the listener never has to guess where the downbeat is. Four accents, no weak
strokes, nothing between. It shares onsets with Backbeat on purpose, and the file
now says the accent weights are the entire difference.

**The bigger fix is to the audit script, which had been grading honest work as
unfinished.** It only recognised a URL as proof, so two whole categories of entry
could never pass no matter how correct they were.

Some presets are invented teaching cells. There is no village that plays "5/4
Ostinato" and no citation will ever exist for it. What CAN be true is that its
comment describes its own notes, and that has been checked. Others are derived from
a neighbour by a rule written in the comment, the way a 2-3 clave is its 3-2 parent
with the halves swapped; the parent carries the citation and repeating it would be
noise.

Two new statuses, CONSTRUCTED and BY-CONSTRUCTION, both counting as done and both
saying plainly that they are done in a different sense from SOURCED. The check
order matters and is commented: constructed cells are classified before the URL
test, so one that mentions a source in passing does not get mislabelled as
transcribed.

The honest count moves from 49 of 60 to **56 of 60**, and none of that jump is new
work. It is the same file, described accurately for the first time. A ledger that
calls correct work unfinished is as wrong as one that calls unfinished work
correct, and the second kind is only more obvious.

What is genuinely left is four entries: Gospel 6/8 and Montuno still want a source,
and Samba and New Orleans are flagged pending a real transcription.


## v0.102.22 — disco, and knowing when NOT to move an accent

**DISCO verified, and its comment's claim holds up unanimously.** MusicRadar says
disco's drums exist to stomp out the four-to-the-floor kick and fill the space
between with the characteristic hiss of the offbeat open hi-hat, calling the hats
the most important ingredient in any disco beat. DRUM! Magazine and Soundbrenner
say the same from their own angles: kick on all four, backbeat on 2 and 4, hats
accented or opened on the offbeat "ands".

**The origin ties two presets in this file together.** Earl Young invented this at
Philadelphia International in the early 70s, on Harold Melvin & the Blue Notes'
"The Love I Lost" in 1973, by turning the Motown beat upside down: he took the
quarter notes Motown put on the SNARE and moved them to the KICK, which freed the
hi-hat hand to do the opening. Disco and Motown are the same idea inverted, and
both have been sitting in this library the whole time without saying so. Now they
point at each other.

**The interesting decision was not moving anything.** Two builds ago Joropo's
accents were moved precisely because the sources called the cross-rhythm the
defining feature and it was inaudible. Disco looks like the same case and is not.

The open hat's distinguishing quality is timbral, not dynamic. Open versus closed,
not loud versus quiet. This engine's two weights mean loud and quiet. Accenting the
"ands" would assert they hit harder than the four-on-the-floor kick, which is
false. Unrenderable is not the same as unimportant, and faking a timbre with a
dynamic accent would be a worse lie than leaving the offbeats light.

Both entries now carry a note pointing at the other, because the difference between
those two situations is subtle and the wrong call in either direction produces a
groove that misrepresents its own genre.

Vetted count is 49 of 60.


## v0.102.21 — trap, and a contradiction that dissolved

**TRAP verified, and one source hands over our exact pattern as a numbered
instruction:** drop the kick on beat 1, add an off-beat kick on the "and" of beat
3, place the snare firmly on beats 2 and 4. Our accents are 1, 2, the "&" of 3, and
4. Kick, clap, kick, clap.

The same source explains why the kick stays thin, and in doing so explains why Boom
Bap and Trap belong at opposite ends of this library rather than next to each
other: in boom-bap the kick is busy and syncopated, in trap it is sparse and
deliberate, leaving room for the 808 to sustain and breathe.

**The apparent contradiction between sources turned out not to be one.** Some say
the snare sits on 2 and 4. Others say that in half-time trap the snare hits on beat
3 of every bar, and call that the defining characteristic of the genre. Both are
true and they describe the same groove counted at two different speeds: trap is
written near 140 BPM but is often felt as a half-time groove around 65 to 85, and
beat 3 of the fast bar is the backbeat of the slow one.

This preset counts at the written rate, so the backbeat lands on 2 and 4. Halve the
BPM and it becomes the other description with no step moving. That is written into
the file, because "the sources disagree" would have been the lazy read and it would
have been wrong.

One thing is deliberately out of scope and labelled as such. Every source agrees
the hi-hats are trap's signature, and they are 32nd rolls and triplet bursts. A
one-voice sixteenth grid can render neither. What ships is the kick-and-clap
skeleton, which is the part a metronome can usefully be.

Vetted count is 48 of 60.


## v0.102.20 — bhangra, where the honest answer is "not from a desk"

**BHANGRA researched properly and left alone, with both reasons written down.** This
is the first entry where the research argued for changing something and the right
call was still to change nothing.

The rhythm is the chaal, and that much is solid. Every source agrees it is the dhol
pattern under all bhangra; musicgcse.co.uk calls it a traditional rhythm featuring
in ALL bhangra music. Two problems sit underneath that, and neither is solvable
here.

**The grid is wrong for it.** The chaal is a triplet feel. A GCSE revision page
gives the meter as "4/4 (12/8)" and vocalises the pattern as "dum-di, dum-di,
dum-di, dum-di", which is four swung pairs, not four straight beats. Our sixteenth
grid cannot place a triplet. This is the same structural limitation already
documented on Blues Shuffle and Jazz Swing, and bhangra now points at those notes
rather than repeating them.

**The sources disagree about the accents, in opposite directions.** The same GCSE
page says "strong accents on first beat of bar", which is what we play. Wikipedia's
Bhangra (dance) article says the dhol gives the music a "syncopated (accents on the
weak beats), swinging rhythmic character" that is the hallmark of the genre. Those
are close to contradictory and both are reputable enough to take seriously.

Nothing moved on that basis. Flipping the accents on a coin toss would be guessing,
and guessing is what put most of the errors in this file to begin with.

The comment now ends with what would actually settle it: a dhol player, or a
transcription of the chaal on a compound grid. Not another search. That is the
ceiling for desk research on this one, and saying so is more useful than another
paragraph of hedging.

Vetted count is 47 of 60.


## v0.102.19 — polka, and a source that disagrees with itself

**POLKA sourced, and the wording correction from two builds ago is vindicated.**
Grokipedia's Oom-pah article states it flatly: in 2/4 time, prevalent in dances
like the polka, the oom falls squarely on beat 1 with the pah occurring on beat 2.
That is exactly what this preset plays, and it is what the old comment had garbled
into an accent on an "and".

Melodigging supplies the origin: polka emerged in early-1830s Bohemia, its hallmark
oom-pah feel being bass on the downbeat and chords on the offbeat.

**One disagreement, and it is inside the same source family.** The Oom-pah article
calls the pattern "a binary strong-weak alternation", which would make beat 2
quieter than beat 1. The Polka article calls the same thing "an accented upbeat
that imparts a buoyant, forward-driving feel", which makes it loud. Those cannot
both be encoded.

Both accents are kept, for two reasons written into the file. The polka-specific
description should win over the general one for a polka preset. And a weak beat 2
would leave this nearly indistinguishable from March 2/4 with a couple of lighter
"ands" added, which defeats the point of having both.

The reversal is a one-character edit and the comment says which character, so if it
reads flat on device it is thirty seconds to change rather than a re-derivation.

Vetted count is 46 of 60.


## v0.102.18 — cumbia, and a deliberate deviation admitted

**CUMBIA's meter and its cell are sourced; the stroke placement is labelled a
reading.** Third entry in the Calypso tier and the pattern is becoming familiar.

Wikipedia states both halves of what the comment already claimed: cumbia "has a 2/2
or 2/4 meter", and "the sound of cumbia can be characterized as having a simple
'chu-chucu-chu' rhythm created by the guacharaca". So the duple claim is right, the
guacharaca really is the instrument responsible, and "chu-chucu" is the source's own
word rather than ours. RF Dance says the same independently.

**One deviation is now admitted rather than glossed.** Traditional cumbia is 2/2 or
2/4 and this preset is 4/4. That is a deliberate choice, not a mistake: 4/4 is
where the rest of the app's cumbia material already lives, and two bars of 2/4 sit
inside one bar of 4/4 without changing a single stroke. Worth writing down because
a Colombian player looking at "4/4 — Colombian" on the card has a fair reason to
raise an eyebrow, and the file should be able to answer that rather than shrug.

What remains a reading is where the guacharaca's strokes land. "Chu-chucu" is
onomatopoeia. Rendering it as a stroke on the beat plus two quick ones on the "and"
and the "a" is a plausible mapping of that sound and is what ships; nothing read
pins the scraper to specific sixteenths.

Vetted count is 45 of 60.


## v0.102.17 — bolero, where the label matters more than the notes

**BOLERO's meter and lineage are now sourced, and its stroke placement is flagged.**
This is the second Calypso-shaped entry: solid on what it is, honest about where
the hits fall.

Wikipedia describes the Spanish bolero as a dance in 3/4 popular in the late 18th
and early 19th centuries, descended from the seguidilla between 1750 and 1772,
accompanied by guitar and castanets. MasterClass draws the split cleanly: the
Spanish bolero of around 1780 was performed in 3/4, while the Cuban bolero is
danced in 2/4 or 4/4.

Which makes the parenthetical in the origin label the important part of this entry
rather than a footnote. Two different dances share the name, they are in different
meters, and the Cuban one is far better known. Anyone reaching for "bolero"
expecting the Cuban ballad will find the meter wrong and reasonably assume we made
a mistake. The label already said so on the card; now the reason is written down
underneath it.

What is not sourced is where the guitar and castanets actually land inside the bar.
The 3/4 is beyond dispute. Accent 1, pickup on the "and" of 2, accent 3 is a
plausible and self-consistent reading, and it is now labelled as exactly that
rather than presented as transcribed.

Vetted count is 44 of 60.


## v0.102.16 — joropo, where the defining feature was inaudible

**JOROPO sourced properly, and then its accents moved.** The onsets were already
right and the problem was one level up.

Sesquiáltera is not a flourish in this music, it is what the genre is for. Pedroza,
writing on the joropo in Venezuela's musical modernity, describes the llanera harp
playing its treble strings "in 6/8 against the 3/4 of the bordones (a vertical
sesquiáltera)", the two producing "a rich array of polyrhythmic encounters".
Melodigging puts it plainly: joropo is famous for the overlay of 3/4 and 6/8,
creating the hemiolas that drive the dance.

Our steps already had both layers in them. Steps 0, 4 and 8 are the 3/4 quarters
and step 6 is the 6/8 midpoint, so nothing was missing. But only step 0 was
accented, which meant the preset played as a light 3/4 with a stray extra stroke
and the cross-rhythm was present in the data and inaudible. Same class of fault as
Boom Bap having no bap: the notes were there, the emphasis was not, and emphasis is
the entire content of the claim.

The 6/8 layer now carries the accents, on steps 0 and 6, with the 3/4-only quarters
weak on 4 and 8. Two against three, which is the hemiola.

Worth stating what this cannot do. A one-voice, two-weight engine cannot sound both
layers of a polyrhythm at once. The choice is which layer to put in front, and the
right answer is the one that fights the meter, because the other one is what the
listener supplies for themselves. That is the same reasoning behind Reggae
One-Drop's empty beat 1 and Tumbao's empty downbeat, and it is now written down in
three places rather than being rediscovered each time.

Vetted count is 43 of 60.


## v0.102.15 — the shuffle, and admitting the grid cannot do triplets

**BLUES SHUFFLE verified.** Every source states the same rule: play the first and
third notes of each triplet and leave the middle one out, giving the long-short
pattern that repeats on every beat. Total Drummer adds the rest of the kit, bass
drum on 1 and 3 and snare backbeat on 2 and 4, which is why all four beats sound in
this preset rather than only two. ArtistWorks supplies the counting our encoding
already uses: straight eighths are "1-and-2-and", shuffle is "1-a-2-a", long-short.
Beat plus its "a" is exactly what these steps play.

**The more useful part of this build is an admission, written into two presets.**

A shuffle's second note is the third triplet of the beat. A sixteenth grid has no
slot there. The "a" is the nearest available position and it sits slightly late. So
Blues Shuffle and Jazz Swing are both approximations, not because anyone got them
wrong but because the grid cannot represent a triplet subdivision at all.

That is now stated in both entries, with a source that acknowledges the same
problem from the notation side: Rhythm Notes points out that the shuffle feel "is
sometimes more of a triplet feel than sixteenth notes" and that written versions
are "open to interpretations". Each entry also points at the other, so anyone
looking at one finds the explanation for both.

This matters beyond these two. Anyone auditing this file later will eventually
notice that the swung presets do not line up with a triplet and may try to "fix"
them. There is no fix available at this resolution. The honest options are to leave
them approximate and labelled, or to give the engine a triplet grid, and that is a
much larger decision than a groove edit.

Vetted count is 42 of 60.


## v0.102.14 — maqsum, matched character by character

**MAQSUM got the tightest confirmation in the whole audit.** Wikipedia's Maqsoum
article prints the basic structure as a 16-slot grid, D-T---T-D---T---, which reads
as dum on 0, tek on 2, tek on 6, dum on 8, tek on 12. Ours sit on exactly those
five and nowhere else. Not a description in words that I then had to translate into
steps; the same grid, the same slots.

The source's own D and T split is doing the same job as this engine's accent and
weak split, since dum is the deep stroke and tek the bright one. So the dums carry
the accents and the teks do not, and that mapping is the source's rather than mine.

One thing written into the file for whoever looks at this next: maqsoum is a
derivative of baladi and the two differ by exactly one stroke. Baladi is
D-D---T-D---T---, meaning step 2 is a dum instead of a tek, and Wikipedia says
outright that the only difference is the accent on the second beat. Change step 2
and this preset silently stops being maqsum and becomes baladi. That is precisely
the kind of one-pulse edit that has gone wrong repeatedly in this file, so it is
now labelled as a tripwire rather than left to be rediscovered.

**KARŞILAMA sourced with a reference that was already in the file.** The Wikipedia
Aksak article that Devr-i Hindi leans on names this grouping specifically: in
Turkish music theory the term refers only to the grouping of nine pulses into
2+2+2+3. Group starts fall on pulses 1, 3, 5 and 7, and the accents are on exactly
those four with pulse 9 weak. Checked rather than assumed, since that is how the
five-four presets got caught out.

Also noted there: the other nine in the library is Compound 9, which is 3+3+3 and
constructed rather than transcribed. Two nines, two different things, and the file
now says which is which.

Vetted count is 41 of 60.


## v0.102.13 — splitting the bass off the piano

**New preset: TUMBAO.** The bass line that MONTUNO had been quietly describing
itself with, now shipping as its own entry and cited on day one.

It is deliberately sparse: two strokes, bombo on the "and" of 2 and ponche on beat
4, with beat 1 left empty. That emptiness is the whole figure. Wikipedia's Tumbao
article explains why: the last note of the measure is held over the downbeat of the
next, so only the two offbeats of tresillo are actually sounded, the first called
bombo and the second ponche. Piano With Jonny puts the same thing in playing terms,
noting beat 4 is tied across the bar line such that beat 1 is rarely played. A salsa
bassist on TalkBass arrives at the identical pair from experience rather than
theory. Three sources, one answer, given by name rather than by inference.

Adding a stroke on beat 1 fills in the gap that makes it work, which is the same
mistake as putting a kick on Reggae One-Drop's beat 1. Noted in the file next to
the pattern.

**MONTUNO's notes are unchanged; its explanation was the thing that was wrong.** It
had been justifying a piano guajeo using the bass tumbao's landmarks and claiming
to land both of them. It lands one. Ponche sits squarely on step 12. Bombo is step
6, and step 6 is silent, with the nearest stroke a sixteenth later on step 7.

That is not a fault in the pattern. The piano montuno leans offbeat and runs against
the clave; marking bombo is the bass's job, and the bass now has somewhere to do it.
The pattern was built by ear by the app's author and is kept exactly as built. The
false claim is gone and the reason it was false is written down.

The two are meant to be heard together, the way Backbeat and The One are, or Soleá
and Bulería. Separately each says one true thing; together they say what the
rhythm section actually does.

Sixty grooves now. Vetted count is 39 of 60, not 40: Tumbao lands vetted, but
Montuno stays unvetted because rewriting its comment removed the only source names
it had and they were never links anyway. It needs a real piano-guajeo transcription,
which is now on the same list as Samba's tamborim and New Orleans.


## v0.102.12 — the Jamaican pair, both clean

Two verifications, no notes moved, and one of them is the tightest source match in
the whole audit so far.

**REGGAE ONE-DROP verified beat by beat.** Tunable spells out all four: nothing on
beat 1, hi-hat or rimclick on beat 2, kick and snare together on beat 3, hi-hat or
rimclick on beat 4. That is this preset exactly, with nothing left over and nothing
missing. MusicRadar says why the empty beat 1 carries the whole idea: the one drop
is defined by the absence of the always-expected kick there, with the emphasis
moving to beat 3. Bass Culture calls beat 3 the single dominant accent of the bar,
which is precisely why it is the only accent we play. Carlton Barrett of the
Wailers is credited with popularising it, and that is now in the file too.

**DANCEHALL matched a source at step-number level**, which has not happened before.
Nearly every rhythm source describes placement in words and leaves the encoding as
an act of translation. This one uses the same 16-step grid the engine does and says
the dembow "places the snare on syncopated 16th-note positions — specifically step
4 and step 7 of a 16-step bar". Ours are on 4 and 7, with their repeats at 12 and
15. No interpretation required, which is the rarest and most reassuring kind of
confirmation available here. Wikipedia covers the kick side: the riddim employs the
tresillo pattern, and takes its name from Shabba Ranks' 1990 track "Dem Bow".

That also explains the last of the tresillo-family overlaps. Dancehall shares a
kick cell with Tresillo by descent, the same way Calypso does. The snare on 4 and 7
is what makes it dancehall rather than the bare cell, and the file says so.

Vetted count is 38 of 59.


## v0.102.11 — calypso, and admitting what a source does not say

**HABANERA verified, and the relationship it claimed turns out to be the textbook
one.** Its comment already said the habanera cell is the tresillo's first half plus
beats 3 and 4. Wikipedia's tresillo article says the same thing from the other
side: tresillo "is a more basic form of the rhythmic figure known as the habanera".
So habanera is tresillo with the back half filled in by two plain quarters, which
is exactly what these steps play. The Puget Sound theory text lands in the same
place independently, listing Bizet's Habanera among its 3+3+2 examples.

**CALYPSO is the first entry where I went looking and came back with less than I
wanted, so the comment says so.** What is properly sourced now is the meter, the
origin and the character of the bass: Trinidad and Tobago, Afro-Trinidadian,
early-to-mid 19th century, rhythms traceable to West African Kaiso, and a bass drum
that plays more syncopated than soca's with a less prominent snare.

What is not sourced is the exact sixteenths. No transcription has been read that
pins calypso to these specific strokes. The cell we play is the tresillo, inherited
rather than independently attested, and the file now states that plainly instead of
implying more confidence than exists.

That also settles the shared-onsets flag the audit has been raising, and settles it
honestly. Calypso and Tresillo land on the same six onsets because calypso's cell
IS the tresillo. What differs is weight: tresillo accents all six evenly, calypso
accents the first two of each half-bar and lightens the third, which is the
boom-boom-CHICK. Written into the file, along with a note that if a real calypso
transcription ever surfaces and disagrees, Calypso is the entry that moves and
Tresillo is not.

Vetted count is 36 of 59.


## v0.102.10 — the 6/8 pair, and the march

Citations only again. All three were already playing the right notes.

**IRISH JIG** verified against four sources that independently name the same two
beats. Six eighth notes felt as two groups of three, emphasis on 1 and 4, which is
what our accents on steps 0 and 6 already were. Soundbrenner happens to describe
our exact encoding for a percussion part: a stronger stroke on 1 and 4 with lighter
taps filling the subdivision.

**SICILIANA** verified too. Slow 6/8 or 12/8, compound dotted rhythm, pastoral and
usually minor. The strokes at 0, 3 and 4 of each group are the dotted-eighth,
sixteenth, eighth figure the comment always claimed.

The interesting part is why those two sound like cousins. It is not an accident and
it is not a duplicate: the sources describe the siciliana as somewhat resembling a
slow jig or tarantella, so they share the two dotted-quarter pulses by definition.
The jig fills them evenly and the siciliana dots them. Both ship, they do not share
onsets, and the file now explains the relationship instead of leaving it looking
like an oversight.

**MARCH 2/4** accents both beats and weakens neither, which is the point. The
left-right pulse of a march is a steady simple-meter tread, set against the
compound lilt of a jig. A march that leans hard on beat one is doing a waltz's job.

One process note. Two edits bounced off the assertion guard this build because my
copy of the existing comment had the line wraps in the wrong places. That is the
guard doing its job on a 10MB file rather than a problem: nothing was written
either time, and the fix was to read the exact bytes back before retrying.

Vetted count is 34 of 59. POLKA 2/4 still needs a citation; its wording was fixed
two builds ago but nothing is linked yet.


## v0.102.9 — the three-four family, verified without moving a note

All three 3/4 presets were already correct. This build is citations only, plus one
recorded disagreement.

**WALTZ** accents beat 1 and softens 2 and 3, which is the whole definition. The
Berliner Philharmoniker describes the waltz, while contrasting it with the mazurka,
as the one "whose rhythm always accentuates the beginning of the bar". TalkClassical
puts it physically: waltzes have a strong down on the first beat that mirrors the
swooping downward step in the dance.

**MAZURKA** accents beat 2, and Grove backs it. Wikipedia quotes the New Grove
Dictionary on the mazur's "strong accents unsystematically placed on the second or
third beat", and the Polish Music Center at USC says the same independently. The
sources say second OR third; a fixed preset has to pick one, and beat 2 is the
commoner reading and the one that contrasts most audibly with Waltz. Noted in the
file so the choice is visible rather than implied.

**VIENNESE WALTZ** got the best find of the three, a source that draws the exact
line between it and Mazurka: the Viennese waltz has "a slight anticipation of the
second beat; this is different from the second-beat accent of a mazurka and gives
the rhythm an exhilarating lift".

That sentence makes the trio coherent for the first time. Waltz accents 1. Mazurka
accents 2. Viennese accents 1 and moves beat 2 early without accenting it. Three
genuinely different things rather than three shades of the same one, which is what
they had been reading as.

One disagreement is written into the file rather than smoothed over. A discussion on
The Session describes the Viennese second beat as slightly delayed rather than
early, though the poster hedges. Anticipation is the commoner account and is what
ships; if better evidence turns up, only that one step moves.

Vetted count is 31 of 59.


## v0.102.8 — the 12/8 family, and a claim that made two presets lie together

**SLOW BLUES 12/8 sourced.** Tunable on the meter: twelve eighth notes grouped into
four beats of three, the compound quadruple feel that is essential to blues,
gospel, doo-wop and slow rock ballads. Beta Monkey's blues drumming guide on where
the snare goes, and it confirms the backbeat correction from the previous build:
play it with a lazier feel, slightly behind, on the 2 and 4 backbeat.

Worth writing down because it will come up again: some 12/8 sources put the snare
on the 7th eighth instead, which is beat 3 of the four. That is the half-time
slow-rock ballad feel and it is a genuinely different groove that happens to share
a time signature. This preset is the blues one, and the file now says which is
which so nobody "fixes" it into the other.

**GOSPEL 12/8's notes moved so its own comment stops being false.** It claimed the
"same four dotted-quarter frame" as slow blues, and then accented beats 1 and 3
while slow blues accented 2 and 4. The two presets did not share a frame at all,
which meant the sentence was describing a relationship that was not in the data.
Backbeat now matches, and the pair differ by density instead, which is the real
distinction and the one the rest of the comment already described: same four beats,
same backbeat, gospel fills every third partial and blues leaves it empty.

**GOSPEL 6/8's claim was under-describing its own notes.** It listed the pushes on
the "and" of 2 and 5 and said nothing about the ones on the "and" of 3 and 6, which
are also played. Four pushes, not two. Notes unchanged, comment corrected, plus a
line on what actually separates it from the 12/8 entry: compound duple, two
dotted-quarter beats, same lilt at half the frame.

Vetted count is 28 of 59.


## v0.102.7 — three comments that named their sources but never linked them

No pattern changes. Three grooves already quoted real sources in prose and cited no
URL, so the audit graded them as unsupported assertions. They are now verified and
linked, which is the cheapest kind of progress available and worth doing before any
more research.

**BACKBEAT and THE ONE** both leaned on PBS Sound Field's "How James Brown Invented
Funk" without a link. Located the episode and checked the transcript: the quotes
already in the file are accurate word for word, including the contrast the two
presets exist to demonstrate. Most music of that era leaned on the back beat, on
the two and the four; Brown moved the emphasis to the one. Both patterns already
played exactly that, so only the citations moved.

**MOTOWN** claimed the snare lands on every quarter note and vaguely gestured at
"Drumeo, Drumhelper, et al". Four sources now sit in the file, and one of them
names the man responsible. Loudlands credits Richard "Pistol" Allen with
popularising the snare on all four beats instead of only 2 and 4, "which gave a
much more driving feel to the music". A Belmont University thesis on Motown
drumming calls the groove Four-On-The-Snare and spells it out as eighth notes on
the hi-hat, quarter notes on the snare, bass drum following the bass guitar. Drumeo
and eMastered agree independently. Our accents on 2 and 4 with the other two
quarters weak is exactly that shape.

Vetted count is up to 26 of 59.


## v0.102.6 — the flamenco pair, and a regression caught

**COMPÁS SOLEÁ verified and left alone.** Four independent sources give the same
five accents on the twelve-count compás: beats 3, 6, 8, 10 and 12, counted from
one. Studio-flamenco, flamencometronome.com, chromatone, and Paul Bosauder writing
for NZ Musician from Seville all say it identically. Our steps 2, 5, 7, 9 and 11
are exactly those counts. Nothing moved.

**FLAMENCO BULERÍA had the right idea and the wrong arithmetic.** Its comment said
"accents on 12, 3, 6, 8, 10 → steps 0, 2, 5, 7, 9". If step 0 is count 12 then
count 3 is step 3, not step 2, so every accent after the first was landing a step
early. The mapping is now 12→0, 3→3, 6→6, 8→8, 10→10.

Worth understanding rather than just patching, because it explains the pair.
Bulería carries the same five accents as soleá. The only difference is where the
counting starts, and NZ Musician says why that is deliberate: flamenco musicians
count bulerías from beat 12 "to keep things consistent between the soleá and
bulerías styles so that internal accents, harmonic changes and closes happen in
the same place". In a looping metronome that shared accent set with a shifted
start is exactly what makes them feel different. Bulería opens on an accent. Soleá
does not.

**This one was a regression, not a fresh mistake.** Steps 0, 3, 6, 8, 10 were
correct in this file at one point and were changed to 0, 2, 5, 7, 9 later. Noted in
the comment so nobody re-derives the wrong version a third time.


## v0.102.5 — checking every claim against its own notes

Ran one mechanical sweep comparing what each remaining groove's comment asserts
against what its steps actually play. Eight mismatches, found in a single pass.
That is more bugs than three rounds of searching turned up, and it cost nothing.

**JAZZ SWING was the bad one.** The comment described the swing ride correctly and
the notes played something else entirely: accents landed on the "a" of 1 and the
"e" of 3, and beat 2 was never struck. Anyone who reached for a swing click got
something that was not swing and was not a click either.

Rebuilt to the actual pattern. BYU Percussion describes it as even quarter notes
with swung eighths on the "and" of beats two and four, plus a hi-hat chick on two
and four. ArtistWorks describes the same figure as spang-a-lang, quarter notes
with a triplet skip between beats 2 and 3 and between 4 and 1. So quarters on all
four, the swung skip after 2 and after 4, hi-hat backbeats as the accents. The
skip is the last note of a triplet and a sixteenth grid cannot place it exactly,
so it sits on the nearest slot, the "a". Kenny Clarke invented the figure, which
is why every source describes the same one.

**BOLERO** promised accents on 1 and 3 and delivered one; beat 3 was weak. Fixed.

**SLOW BLUES 12/8** called the backbeat essential in its own comment and then
accented beats 1 and 3, burying it. Now accented on 2 and 4, which is how the
Backbeat preset already treats the same idea in simple time.

**BHANGRA and VIENNESE WALTZ had labelling errors, not note errors.** Both comments
named the wrong subdivision, calling a stroke on the "a" an "and". The notes were
right in both cases; the words were one sixteenth out. Words fixed.

**POLKA's wording contradicted its own data.** It said the chord fell on "the
offbeat" and produced "the accented upbeat", which reads as an accent on an "and".
Nothing on an "and" is accented and nothing should be. In 2/4 the pah is beat 2.

**SAMBA and NEW ORLEANS are flagged rather than fixed.** Samba's comment listed
tamborim pushes on the "and" of 1, 2 and 4 while the data plays the "and" of 1, 3
and 4. New Orleans says the bass sits on 1 and 3 while beat 3 carries no accent. In
both cases one of the two is wrong and no source has been read that settles it, so
picking would have been guessing. Samba's comment was corrected to describe the
data honestly and marked unsourced. New Orleans is marked as a disagreement, with
a note that Second Line above is already the sourced New Orleans entry and this one
should end up being a genuinely different part rather than a second attempt at the
same one.


## v0.102.4 — the invented ones were lying too

New rule for the library, and it is a good one: a preset does not have to be
transcribed from anywhere, but if it asserts something it had better do it. Four
of the six constructed presets asserted a grouping their notes did not play.

**5/4 OSTINATO** claimed a 2+3 grouping and accented beats 1, 2 and 3. A 2+3 has
group starts on 1 and 3, so that is not a 2+3, it is three loud beats followed by
two quiet ones. Accents on 1 and 3 now.

**FIVE ROCK** claimed "4+1: driving four then an extra beat" and accented 1, 3 and
5, which is a 2+2+1 feel. Group starts for 4+1 are 1 and 5, so that is where the
accents sit now, and it finally sounds like the thing it is named after.

**TAKE FIVE** contradicted itself in a single line: it said "3+2 grouping" and
then listed accents on 1, 3 and 4. A 3+2 has group starts on 1 and 4 only, and the
accent on 3 belonged to no group at all, which made the whole thing read as
2+1+2. Take Five exists to teach the 3+2 division, so it now plays one.

**SEVEN ROCK lost its Brubeck reference, because the reference was wrong.** The
comment claimed "4+3 grouping, Unsquare Dance feel". Unsquare Dance is not 4+3. E.
Michael Harrington puts it plainly: in Unsquare Dance, 7 = 2+2+3. Jazz Backstory
describes the parts and lands in the same place, with the bass tapping 1, 3 and 5
against claps on 2, 4, 6 and 7, and 1-3-5 is exactly the 2+2+3 group start. That
rhythm was already in the library, correctly, as Rachenitsa. So the preset was
duplicating an existing groove and misattributing it at the same time. It is now
an honest 4+3 with no Brubeck claim attached, which means three genuinely distinct
sevens ship: 2+2+3, 3+2+2, and 4+3.

**JAZZ WALTZ's claim was rewritten** rather than its notes. It promised a strong 1,
a brushed 2 and a "medium" 3, but steps carry two weights and there is no medium,
so beats 2 and 3 were identical in the data while the comment insisted they were
not. The comment now describes what plays.

**COMPOUND 9 was checked and is fine.** Three groups of three, group starts on 1, 4
and 7, accents on exactly those. Left alone and marked verified.

All six now say CONSTRUCTED where that is the truth, so nobody later mistakes a
teaching cell for a transcription.


## v0.102.3 — the audit was lying to us

**The audit script had a parsing bug and it flattered the numbers.** It only read
comments sitting above a groove's `id:` line, so anything documented below its id
came back as undocumented. That is what produced the "20 unverifiable" figure and
sent a whole session chasing grooves that were already fine.

Rebuilt, and it now grades on a harder curve. A groove counts as done only if its
comment contains an actual URL. Five classes: SOURCED has a citation, CONFLICT
means the sources disagree and a reversible judgement was made, FLAGGED means
known-unresolved with the reason written down, DESCRIBED means someone asserted
something and cited nothing, NONE means silence. DESCRIBED is the honest new
category and it is not a pass, however confident the sentence sounds.

The real number is 18 of 59 vetted. That is worse than the old count claimed and
it is the number to work from.

**TARANTELLA verified, not changed.** Compound duple with the accents on the 1
and the 4 of the six eighths, gallop stroke on the third eighth of each group.
Melodigging is explicit: two strong pulses per bar, tamburello accents on 1 and 4.
Naples LDM describes the same thing from the listener's side, a very fast
ONE-two-three ONE-two-three.

**CHA-CHA-CHÁ: beat 3 promoted from weak to accent.** Jorrín simplified mambo's
syncopation on purpose, and part of that simplification was keeping a strong
metric accent on beats 1 and 3 in the cowbell. Our beat 3 was weak, which
contradicted the one thing the composer was deliberately doing. All four quarters
still sound; the triple still lands on 4, the "&" of 4, and 1; beat 2 is now the
only weak stroke.

**ÇİFTETELLİ is the one where sources genuinely disagree.** Three written readings
were found, all calling themselves çiftetelli, and no two match. The old pattern
matched none of them and cited nothing. Adopted the Darbuka Ritim Solo table
because it is the only version written at sixteenth resolution, which is what this
engine stores, so encoding it takes no interpretation. Dums on 1 and 3, teks and
kas filling the rest. All three readings are written into the file so this can be
reversed on better evidence.

**New check: shared onsets.** Same hits, different accent weights, which the old
duplicate check could not see. It found five clusters straight away. Tresillo and
Calypso land identically. So do Disco and Motown, and Funk 4-on-the-Floor and
Backbeat. Take Five, 5/4 Ostinato and Five Rock are all the same five-beat cell,
and Rachenitsa, Devr-i Hindi and Seven Rock are all the same seven. Some of those
are probably fine and some are three presets wearing one rhythm. Next job.

Grooves vetted: 18 of 59, honestly counted for the first time.


## v0.102.2 — Allen's first pattern, and fanga found

Both grooves I was ready to write off turned out to have real transcriptions
behind them. Neither is guesswork now.

**AFROBEAT is Tony Allen's first pattern.** Allen picked this one out himself; per
Rolling Stone he said the most important thing an aspiring afrobeat drummer needs
to learn is the first of the five patterns he demonstrates in "Birth of Afrobeat".
Joe Ospalla's transcription PDF builds it up one instruction at a time, and the
captions fix every stroke: bass on 1e and 3e, snare on 1a, snare on the "e" and
"&" of 2, snare on 4e, snare on the "&" of 4. Kick takes the accents, the snare
figures sit weak underneath, and the hi-hat layer is dropped because one voice
cannot carry three.

Fair warning before you hear it: nothing lands on 1, 2, 3 or 4. That is not a bug
and it is not a rounding error, it is the entire reason Allen sounds like Allen.
He pushes the kick off the downbeat onto its "e", so the groove floats over the
pulse rather than stamping it. Reggae One-Drop already drops beat 1, so an empty
step 0 is not new here, but four empty downbeats is. If it reads as broken rather
than as floating on device, say so and we will decide what to do about it.

**FANGA is the Djembe 1 accompaniment.** Two independent transcriptions give a
byte-identical sound row, which is the cross-check that made it shippable: the
Server Hosted African Rhythm Exchange and Kresimir Oreski's "15 Essential
Rhythms" both write it B--T -TT- B-B- TT--. Bass strokes at 0, 8 and 10 become
the accents; tones at 3, 5, 6, 12 and 13 become the weak strokes, which is the
same distinction the source notation already makes. The sparser dunun bass part is
noted in the file in case this ever wants simplifying.

The context stays written down rather than buried. Fanga as the world plays it is
partly a mid-century staging: Pearl Primus choreographed her version in 1959 and
LaRocque Bey wrote the "Fanga alafia" chant in New York in the late 50s. The drum
part is still the drum part that gets played, and it is now the one we play.

The two presets also no longer share onsets, which they never should have.

Grooves with no source behind them: down from 13 to 11.


## v0.102.1 — boom bap had no bap

**BOOM BAP corrected.** The preset accented beats 1 and 3 and put nothing at all
on 2 and 4. The name is onomatopoeia, per Wikipedia, for the kick drum and the
snare drum in that order, so the entire second half of the name was missing from
the pattern.

Every source gives the same skeleton. Hip Hop Music History: "The one and three
count on the beat would typically have a kick drum and the two and four count of
the beat would have a snare." Native Instruments goes further and supplies the
syncopation: snares on beats 2 and 4, kicks on the first, fourth and sixth 8th
notes. That works out to accents on all four beats with weak ghost kicks on the
"&" of 2 and the "&" of 3.

Its origin label said "Hip-hop / trap", which is backwards. Boom bap is the
late-80s and early-90s East Coast golden age, and trap is the thing that departed
from it. Trap is its own preset a few rows up. Label now reads East Coast golden
age.

**SECOND LINE verified, not changed.** It was already right and simply had nothing
written down. The accents sit on 1, the "&" of 2, and 4, which is the 3-side of
the son clave exactly as second-line players count it, and the accent on beat 4 is
the big four that the whole phrase leads to. Four independent sources now sit in
the file next to it, including the Ethnomusicology Review transcription that
identifies the weak stroke on the "and of 3" as the anticipation into that big
four.

**FANGA's origin corrected.** It said Mandinka. Fanga is from the Vai people of
Liberia. The pattern itself is still not signed off, and the comment now explains
why rather than pretending otherwise: fanga as the world plays it is largely a
mid-century American concert-dance construction, choreographed by Pearl Primus in
1959 with a song written by LaRocque Bey in the early 60s, set to a melody
popularised by minstrels. There is no single village transcription to be accurate
to, and the rhythm is an ensemble part in any case.

**AFROBEAT flagged, with the reason.** There is no one afrobeat timeline. Tony
Allen, who invented the drumming, said it plainly: "Afrobeat has different
varieties of rhythm... all what I'm doing is on 4/4 time signature, so it's just a
question of the composition of the patterns." In the same clip he demonstrates
five of them. The features that are citable are two-voice, an eighth-plus-two-
sixteenths figure on the ride against kicks on 1, 1e, 3 and 3e, and this engine
plays one voice. What ships is a plausible afrobeat-flavoured cell rather than a
cited one, and the file now says so out loud.

Grooves with no source behind them: down from 15 to 13.


## v0.102.0 — the six distinguished timelines

**SHIKO, SOUKOUS and GAHU corrected.** All three were undocumented and matched no
source. All three now sit on the canonical pattern, and the two long-standing
UNRESOLVED flags in the groove table are closed.

The thing that cracked it: shiko, son, rumba, soukous, bossa-nova and gahu are not
six unrelated grooves. They are one family. Toussaint's "The Geometry of Musical
Rhythm" (ch. 7) calls them the six distinguished timelines: six rhythms of five
strokes across sixteen pulses, each differing from the others by one or two
pulses. Diaz-Banez et al., "Measuring Musical Rhythm Similarity", prints the box
notation for all six in a single table.

Three of ours already sat exactly on it. Son, rumba and bossa-nova were correct
and are now annotated to say so. The other three were not:

    shiko     was 0,4,7,10,14   now 0,4,6,10,12
    soukous   was 0,3,6,8,11,14 now 0,3,6,10,11
    gahu      was 0,3,5,8,11,13 now 0,3,6,10,14

Each fix has a second source behind it, not just Toussaint.

**Shiko** cross-checks against Cuba. The shiko necklace is the same one Cuban
players call the cinquillo, and cinquillo doubled from eighths into sixteenths is
0, 4, 6, 10, 12. Two traditions, one answer.

**Gahu** is confirmed by Locke's own transcription. Johnston, citing Locke 1998
"Drum Gahu" p.124, describes a five-stroke timeline with inter-onset intervals of
3-4-4-2-3, beginning on an anacrusis, with the final onset landing on the
downbeat. Count 3-4-4-2-3 backwards from that downbeat and you land on 0, 3, 6,
10, 14. Identical to Toussaint, arrived at from the opposite direction. Gahu had
been carrying six strokes in two identical halves, which a five-stroke timeline
cannot be.

**Soukous** was byte-identical to tresillo, which cannot be right for two
differently named styles. It is now the soukous timeline: the son clave with its
last stroke pulled one sixteenth earlier. One caveat is written into the file
rather than hidden. Soukous's ensemble signature is really the cavacha, a
two-voice hi-hat and kick figure, and this engine plays one voice. It cannot
render a cavacha, so what ships is the timeline the literature files under the
name.

**SON CLAVE 2-3 and RUMBA CLAVE 2-3 documented.** Neither needs its own citation.
Each is its 3-2 parent with the two halves swapped, which is exactly what the
sources say a 2-3 form is, and the swap is now verified in the data and written
down.

Grooves with no source behind them: down from 20 to 15.

## v0.101.24 — THE ONE was not on the one

**THE ONE — corrected.** The preset accented beats 1 AND 3 equally, in two
identical halves. That is a half-bar pulse, and it gives beat 3 the same weight
as beat 1 - which loses the exact contrast the groove is named for.

Sources are unanimous and specific. PBS Sound Field: "most music of that era gave
heavy emphasis to the back beat, on the two and the four... What James Brown did
was he put the emphasis on the one, on the downbeat of the measure." Wikipedia's
Funk article: "a heavy emphasis on the first beat of every measure ('The One'),
and the application of swung 16th notes and syncopation".

Beat 1 is now the only accent. The surrounding sixteenths stay as weak strokes,
which is the other half of what the sources describe: "emphasizing the one
created space in the groove, so that the band could add syncopation to the other
beats."

**BACKBEAT annotated** rather than changed - it is correct at 2 and 4, and it is
the pattern THE ONE was invented against, so the two presets only make sense next
to each other. Said so in the source.

**TRESILLO and HABANERA verified.** Tresillo's onsets sit at steps 0, 3, 6, 8,
11, 14 - exactly 3+3+2 twice, matching Puget Sound's music theory text ("the
sixteenth-note version is known as tresillo"). Habanera hits 1, the "&" of 2, 3,
4, exactly as its own comment claims.

Unverified count is down from 23 to 20.

## v0.101.23 — Clave family verified; the bossa clave had six strokes

**BOSSA NOVA — corrected.** Wikipedia's Clave article gives the rule exactly: the
bossa nova clave "has a similar rhythm to that of the son clave, but the second
note on the two-side is delayed by one pulse." Applying that to our son clave
(1, the "a" of 1, the "&" of 2 | the "&" of 3, 4) delays beat 4 to the "e" of 4,
giving five strokes: **1, 1a, 2&, 3&, 4e**. That matches The Signal Beat's
transcription of the 3-2 bossa nova clave.

Ours had **six** strokes: an extra one on the "e" of 3 that son clave does not
have, beat 4 left undelayed, and an added "&" of 4. Every clave has five strokes,
so the count alone was a tell.

**The four claves verified and annotated.** Son 3-2, son 2-3, rumba 3-2, rumba
2-3 all check out:

- The son/rumba difference is the third stroke of the 3-side moving one sixteenth
  later - ours has son on the "&" of 2 and rumba on the "a" of 2, which is
  precisely what LANDR describes.
- Both 2-3 forms are exact half-swaps of their 3-2 forms, which is what the
  sources require: "3-2 and 2-3 are not two different rhythms... they are two
  directions of the same two-bar pattern."

A note on the ENCODING is now in the source above the clave block, because
misreading it is what caused the montuno to be "corrected" in the wrong direction
earlier in this session: 16 steps is ONE bar of sixteenths, with the two-bar
clave written in cut time across it.

**CUMBIA checked and left alone.** It looked wrong in the audit summary - a hit
on every eighth - but it is the guacharaca "chu-chucu" cell: accents on the
beats, weak strokes on the "&" and "a". The audit line does not distinguish
accent from weak stroke, which is a limitation of the summary, not a fault in the
pattern.

Unverified count is down from 26 to 23.

## v0.101.22 — Turkish and Balkan set: one misnamed groove, three verified

Wikipedia's "Aksak" article carries a table of pulse-counts, subdivisions and
names that makes this whole family checkable, and it settled four entries at
once. https://en.wikipedia.org/wiki/Aksak

**AKSAK → DEVR-I HINDI.** The article is explicit: "Strictly speaking, in Turkish
music theory the term refers only to the grouping of NINE pulses into a pattern
of 2+2+2+3." Our AKSAK was a SEVEN-pulse 3+2+2, which the same table names
Devr-i Hindi (Bulg. lesnoto / četvorno). The nine-pulse 2+2+2+3 that Turkish
theory actually calls aksak is already in the app - as KARŞILAMA, which is a
real Turkish 9/8 dance in that meter, so that entry stands. Renamed, with the
Italian origin string synced.

The pattern itself was already right: its accents land exactly on the 3+2+2
group starts. This was a label on the wrong rhythm, not a wrong rhythm.

**Verified and left alone, with sources now in the code:**

- RACHENITSA — 7-pulse 2+2+3. Wikipedia's table gives Bulg. Račenica as 2+2+3;
  the Bulgarian dances article agrees. Accents sit on the group starts.
- KOPANITSA — 11-pulse 2+2+3+2+2, accents at steps 0, 4, 8, 14, 18. Confirmed by
  the same table (Bulg. Gankino) and by Melodigging's "11/16 (2+2+3+2+2, e.g.,
  kopanitsa)".
- KARŞILAMA — 9-pulse 2+2+2+3, accents on every group start.

**ÇİFTETELLİ — flagged.** The D-K-T-K-T-D-D-T cell is the standard darbuka
teaching pattern, but I could not find a citable transcription fixing it to
specific sixteenths, and the rhythm differs between the Turkish and Greek
traditions that share the name. Recorded as unverified rather than asserted.

## v0.101.21 — African grooves: two errors found, two flagged, sources in the code

Started the source audit with the African set, where the risk of being visibly
wrong to a native player is highest.

**KPANLOGO — corrected.** Wikipedia's Kpanlogo article states the bell pattern
"is the same as the son clave pattern heard in Cuban music". Ours had a stroke on
the "e" of 3 where son clave has the "&" - one sixteenth early - so it was
neither the clave nor kpanlogo's bell. Now byte-identical to this file's own SON
CLAVE 3-2, which makes it self-checking.

**SOUKOUS — flagged, not guessed.** The audit found it byte-identical to
TRESILLO, which cannot be right for two differently-named styles. Sources agree
soukous's percussion signature is the *cavacha*: Wikipedia calls it "an
unyielding, fast-paced beat, most commonly referred to as cavacha", and World
Music Method describes cavacha as "a fast sixteenth-note hi-hat groove with
syncopated bass drum accents". That is a two-voice figure and this engine plays
one voice, so the honest options are a cavacha kick pattern or dropping the
preset. Recorded in the source rather than replaced with a guess.

**GAHU — flagged.** Two sources say the gahu timeline has FIVE strokes (Johnston,
citing Locke 1998; and a Grokipedia figure). Ours has six, arranged as two
identical halves, which a five-stroke timeline cannot be. Not rewritten: Locke's
transcription is the authority and I have not read it directly, and the
Grokipedia figure is AI-generated and hedged.

Every claim above is now a comment beside the pattern with its URL, so the next
person can check the source rather than trust the code.

**The audit script gained a duplicate check** (`intonare_groove_audit.py`), which
is what found the soukous error. It distinguishes documented matches - kpanlogo
genuinely should equal son clave - from unsourced ones.

## v0.101.20 — The montuno, corrected by ear and then checked

Daniele built the pattern he expected to hear on the custom grid. It differs from
the stored one at 10 of 16 steps, and the sources back it.

  his:     accents on 1, the "a" of 1, the "a" of 2, the "a" of 3, and beat 4
  stored:  accents on 1, 2e, 3, 4e

Two independent checks favour his:

- The tumbao a montuno locks to accents **"the and of 2 and the downbeat of beat
  4"** (Rhythm Notes; Piano With Jonny). His pattern hits beat 4. The stored one
  hits 4e and never beat 4 at all.
- The two sounded offbeats of tresillo are **bombo** (the "a" of 1 in cut time)
  and **ponche** (beat 4), and Wikipedia's Tumbao article identifies their
  consistent accentuation as what "gave the son montuno texture its unique
  groove". His lands both. The stored pattern landed neither.

It also shares three of five accents with the app's own SON CLAVE 3-2 and pushes
the other two a sixteenth later, which is the guajeo-against-clave relationship.

The reasoning is now recorded in a comment beside the pattern, because I have
already "corrected" this groove once this session in the wrong direction and a
future pass should not repeat that.

## v0.101.19 — The playhead outline stops lingering after stop

`grooveUpdateCursor()` writes `.gs-cursor` to three grids: the CLICK panel's
`.groove-step` cells, the VISUAL panel's `gvs-*` cells, and the main screen's
`gs-step-*` cells. `stopMetro()` cleared the first two and not the third - so the
one grid actually on screen kept its outline on whichever step happened to be
playing when you hit stop.

Cleared now, and cleared across every `gs-step-*` in the DOM rather than looping
to `groovePattern.length`, so switching to a shorter pattern cannot strand a
cursor on a cell past the new end.

## v0.101.18 — Groove names: stop splitting words, let the fitter do its job

The names were breaking mid-word - "MONTUN / O", "HABANE / RA" - and my previous
two attempts made it worse by treating it as a measurement problem. It is not.

Calibrated off the device screenshot ("MONTUN" spans 157px at 36px, so 0.727px
per character per font-px) against the real 172px column, the arithmetic is
unambiguous: **with wrapping between words only, all 60 names fit at 16.9px or
above**, and only FUNK 4-ON-THE-FLOOR reaches that. MONTUNO needs 24.4px on a
single line; HABANERA needs 21.5px. Both had enormous headroom.

So a word split was never necessary, and permitting it was the whole fault: the
browser resolved the overflow by breaking the word, which meant the fitter saw
text that already "fit" and had no reason to shrink. `overflow-wrap: anywhere`
did it, `break-word` still did it.

- `overflow-wrap: normal` and `word-break: keep-all`. Overflow is now resolved by
  shrinking, which is what the fitter was written to do.
- Floor lowered 17px to 16px. The worst case needs 16.9px for its longest word,
  so a 17px floor left it 0.1px short - and the only way the browser could
  resolve that was by breaking the word again.
- Verified arithmetically across all 60 names: none require a size below the
  floor, and none require a word split.

## v0.101.17 — The name fitter was measuring the wrong element

Measured from the device screenshot rather than guessed: "MONTUN" renders at
~36px - the fitter's MAXIMUM - across ~157 CSS px, in a name column that computes
to ~172px. Full "MONTUNO" needs ~183px, so it wraps. Two steps down to 32px would
fit it on one line. The fitter had stepped down zero times, which means its
measurement was never seeing the real constraint.

`#gsName` is `display: -webkit-box` with `-webkit-line-clamp` and
`background-clip: text`, and its own `clientWidth` does not report the limit
reliably through that combination. The fitter now measures the parent column,
which is a plain block and is the actual constraint.

The previous attempt - swapping `overflow-wrap: anywhere` for `break-word` -
addressed the symptom and not the cause, and on its own would not have fixed
this. It stays, because a mid-word break is still the wrong failure mode here,
but the sizing is what was broken.

## v0.101.16 — Groove audit: the name fitter, and a montuno correction I got wrong

**The name overflow.** MONTUNO rendered as "MONTUN / O" - a 7-character name in a
168px column that it fits at any size the fitter can choose. The cause was
`overflow-wrap: anywhere`, which splits inside a word as soon as the measured
column looks too narrow, combined with `_fitGrooveName()` running in the same
frame the groove screen becomes visible, when that column can still be resolving.
It guards against a zero width but not a stale one.

- `overflow-wrap: break-word` instead of `anywhere`. Every preset name fits the
  column at the fitter's 17px floor, so a mid-word break is always the wrong
  answer; shrinking is the right one.
- The fit runs again after two frames, so a measurement taken mid-layout cannot
  stick.
- The fitter always restarts from 36px. It set the size on every call but began
  from whatever was left over, so a name could stay smaller than necessary once
  the column widened.

**A structural audit of all 59 grooves.** Step counts divide evenly into beats
for 57 of them at 2, 3 or 4 steps per beat. The two exceptions - KARŞILAMA and
COMPOUND 9, both 9 steps over 9 beats - are correct: they are counted in nine,
not subdivided.

**And a correction to my own earlier change.** I rewrote the montuno pattern
this session on the reading that 16 steps meant two bars of eighths. The engine's
own comment settles it the other way: "Step duration = one bar duration / pattern
length - e.g. 16 steps in 4/4 = 16th notes." So SON CLAVE 3-2 is stored in cut
time, one bar of sixteenths, and decodes correctly as 1, 1a, 2&, 3&, 4. Under
that reading the original montuno accents 1, 2e, 3 and 4e - the "e" positions are
offbeat pushes, not downbeats, and the pattern was fine as written. Reverted.

## v0.101.15 — Share links stop showing the chooser first

Opening a shared daily flashed the module picker before the daily loaded.
Measured on a simulated cold-start deep link: the launcher was visible at full
opacity from 547ms to 1681ms - **1134ms of chooser** before the module took the
screen.

The logic was already correct and in the wrong place. `lnchShouldShow()` checks
`_intonareWantSkipSplash` and returns false for a deep link, and `lnchInit()`
hides the launcher when it does, with a comment naming this exact case. But the
flag is raised at ~116ms while `lnchInit` does not run until ~1020ms, so the
launcher had already built and painted; all `lnchInit` could do was hide
something the user had been looking at for 200ms.

- **The check moved to the pre-paint script**, where the pinned case is already
  decided. A deep link now means the chooser never paints at all, rather than
  painting and being taken away. The launcher is never visible on that path.
- Both arrival shapes are covered: the flag when Capacitor has already resolved
  the launch URL, and the URL itself read straight off `location` when it has
  not.

Normal launches are untouched: the launcher still appears on both non-pinned
paths, still stays hidden when a module is pinned, and the boot guard still
reports zero app-before-launcher frames across all five paths.

## v0.101.14 — SOSTENUTO stops running into DAMPER

The pedal column is 46px wide and "SOSTENUTO" needs about 47px at 10px Bebas with
1px tracking - sitting exactly on the boundary, so any font substitution or
rounding tips it over and it runs into the label beside it. That is the collision
on the piano's pedal row.

- The label is **SOST** now, matching the legend on the pad directly above it,
  which is what a player reads first anyway. It leaves margin rather than
  balancing on the limit.
- `white-space: nowrap` and `overflow: hidden` added to `.ppc-name`, so a long
  label can never bleed into its neighbour again.
- Both piano instances updated - the inline one and the full-screen one.

Left alone deliberately: DAMPER measures ~31px in the same 46px column, so it had
room and was not part of the fault. The pedal diagram elsewhere also says
SOSTENUTO, but its boxes are 64px with the text centred and the size already
tuned to fit, so it is a different situation.

## v0.101.13 — The tab bar was arriving after the module

The jar at the end of the handover was not the animation - it was the navigation
turning up late.

The tab bar carried a `.30s` transition delay, added so it would not start moving
mid-handover. With the faster morph that delay now landed AFTER the module was
already on screen: measured the launcher gone at 715ms, the morph gone at 788ms,
and the bar only beginning to move at 821ms. So the module appeared complete, and
then its navigation slid up as a separate event about a tenth of a second later.

- **The delay is gone.** The bar now leads the uncover rather than trailing it:
  on a card launch it starts at 508ms and lands at 788ms against a cover that
  clears at 712ms; on a pin launch it lands at 692ms against a cover clearing at
  692ms - exactly together.
- **Zero frames on either path** where the module is on screen without its tab
  bar, down from 6 on the card path.
- It also picked up the same ease-out curve as the rest of the entry, instead of
  the springy `cubic-bezier(.22,1,.36,1)` it was using.

Checked and found correct: the palette swap happens at 409ms with the launcher
still at full opacity, so the module is already wearing its own colours before
anything uncovers. That was not the cause.

## v0.101.12 — Motion polish on the first thing anyone does

The launch sequence was running on three different easing families at once. This
standardises the whole path on one idea: anything ARRIVING uses ease-out, so it
enters at speed and settles, which is what iOS does for touch-triggered motion.

- **The picked card was on an ease-IN-out curve.** `cubic-bezier(.36,0,.28,1)`
  ramps up from a standstill, so the first ~110ms after a tap produced no visible
  movement - measured 0px across three frames, then 10px/frame once the curve got
  going. That stall before the card commits is what read as jitter. Now
  ease-out: motion starts at 12.6px/frame and decelerates.
- **The launcher entry used Material's `.4,0,.2,1`**, which also accelerates into
  the motion. The launcher surface, the module cards, the quick pins and the hint
  all now share `cubic-bezier(.22,.61,.36,1)`, close to UIView's curveEaseOut.
- The hint was on a bare `ease`, which is symmetric and ramps both ends - on an
  arrival that reads as hesitant.
- Durations nudged from .34s to .38s on the surfaces that carry the entry, since
  an ease-out spends less of its time visibly moving than a symmetric curve.

Checked and left alone: `setMode()` costs 1-2ms for every module, so it is not
what delays the morph. The residual gap before motion in the container is the
headless harness's frame scheduling, not the app - worth stating because it looks
like a stall in the trace and is not one.

Boot, note fit and launch all re-verified: five boot paths with zero leak frames,
combined coverage never below 99%, every note inside the ring, and the pin launch
still uncovering a finished module.

## v0.101.11 — The skip-splash boot stops flashing, and the note fits its circle

A 120fps screen recording made the boot problem measurable: five distinct visual
states across ~1.7s before the module picker, including ~200ms of pure black.
Decoded from the frames - 16,000 colours at full brightness, then 3,500, then 11
colours at 79% flat, then two more states - which matches "three or four quick
card flashes, a background, something else, the tuner" exactly.

- **The boot guard was released 1.4 seconds too early.** `boot-ready` fired at
  263ms while the launcher did not reach full opacity until 1670ms, so the app sat
  uncovered underneath while the launcher slowly faded in over it. The reveal now
  waits for the launcher to be doing the covering on that path; the veil covers
  the gap, and combined coverage never drops below 99% at any frame.
- **The veil was lifting ahead of the launcher.** Both fades are .34s, but the
  launcher's starts a frame or two later - measured the veil at 0 with the
  launcher still at 0.82, a ~170ms window with nothing covering. The veil is held
  260ms so the two overlap instead of racing.
- **The launcher is covered by the boot guard too.** It ships visible so the
  pre-paint script can decide synchronously whether to keep it, which also meant
  it painted its own ground before that script ran.
- **The module-select morph was three events, not one.** ~105ms of nothing, a
  burst of 10px/frame, then a 270ms crawl at 0.1px/frame where it looks stopped,
  and only then the fade. Shortened .58s to .42s on a curve without the dead tail,
  dropped the .04s start delay, and moved the fade from 420ms to 300ms so it
  overlaps the travel rather than following it.
- **The note letter overflowed the ring.** 68px type in a circle of radius 45.3px:
  the glyph's corner reached 47px, outside the ring. The strip below gave up 6px
  of padding so the circle grows to 112.5px (R 47.3), and the note comes down to
  60px - corner now 42.5px, clearing with margin at every note including the
  sharps. Ring still square, face still 194px, meter still exact.

## v0.101.10 — Clipped on the other axis too, and the grow was overdoing it

v0.101.9 gave the launch grow vertical headroom and left the horizontal alone, so
the leftmost chip was still cut 6px on its left edge - the same bug, the other
axis. Padding on both sides now, pulled back by matching negative margins so the
row's position and scroll origin are unchanged: the first pin still starts at
x=29, and the grid, hint and row all hold their positions.

Checked every position rather than just the one reported: leftmost, middle and
last, in a 3-pin row and an 8-pin row, and at three scroll positions in the
scrolling case. All clear by 5px or more on every side.

**The grow is smaller.** 1.18 was sized when it had to carry the cover on its
own; the three-phase timing is really doing that work, so it comes down to 1.09
with a 3px lift instead of 6px. The unpicked chips also step back less - .3
opacity rather than .18, which was reading as a separate effect rather than the
row deferring to one of its own.

## v0.101.9 — The grow had nowhere to grow

The launch grow was clipped 10px at the top. The chip lifts -6px and scales to
1.18, but the pins row is a horizontal scroll container, and `overflow-x: auto`
forces overflow-y into a scrollport too - so `overflow-y: visible` is ignored by
spec and there was nothing to do but clip.

Fixed with 12px of top padding for the grow to expand into, pulled back by an
equal negative margin so nothing below moves. Measured after: the grown chip sits
2px INSIDE the row's bounds with 6px spare below, and the grid, hint and row all
hold their positions at both 915px and 800px viewports.

**On whether the card path loads under cover too - it does, and with more room
than the pins:**

| | module built | cover after build |
|---|---|---|
| card | 43ms (`setMode` runs before the morph starts) | ~530ms |
| pin | ~205ms (during the chip grow) | ~140ms |

The card gets the whole morph as post-build cover because `setMode` is called
first, then the clone grows for ~500ms on top of an already-finished module. The
pin's cover is shorter but still comfortably clear of the worst measured build
(81ms). Verified by sampling `elementFromPoint` every frame on both paths:
neither shows the app before the module.

## v0.101.8 — A pin grows, the module loads behind it, then the launcher fades

The pin launch is three phases now, and the middle one is the point.

1. The tapped chip grows in place - larger and slower than a press nudge, so it
   reads as the chip becoming the module rather than acknowledging a tap. The
   rest of the row steps back.
2. **The module is built while that grow is on screen**, with the launcher still
   fully opaque. Measured launch cost across all 26 favourites: 4ms median, 81ms
   worst - the exercises, which build more UI, not the tools as expected. Piano
   and Charts are 2-4ms. A 150ms grow covers the worst case comfortably.
3. Only then does the launcher fade, so it uncovers a module that is already
   finished instead of one assembling itself in view.

Verified with `elementFromPoint` sampled every frame through the handover: by the
time the fade starts, the module's own content is what is painted at screen
centre, and there are **zero frames where the app shows before the module** -
including on the slowest entry in the roster.

The first attempt left a 330ms hold on a static grown chip: two
requestAnimationFrames were waiting for a build that takes 4ms, and the outer
timeout did the rest. Trimmed to one frame, and the total is ~580ms with nothing
sitting still in the middle.

## v0.101.7 — The launcher never actually faded out

Tracing the exit the same way as the entry found a bug older than the pins: the
launcher's fade-out has never run. `.lnch-gone` sets `opacity: 0`, but the entry
state `.lnch-nosplash-in` sets `opacity: 1` at the same specificity and LATER in
the sheet, so the exit lost on source order. Isolated test - add the class with
nothing else running, sample for 600ms - opacity held at 1 and then the element
was displayed none. Confirmed with reduced motion both on and off.

A card launch hides this completely: its morph clone grows 164x268 to 278x456 and
carries the eye while the chooser cuts underneath. A pin launch has no morph, so
it showed the cut plainly - which is why it looked abrupt next to a card.

- **`.lnch-gone` is `!important` now.** It is the exit and has to beat every
  entry state. Measured afterwards: 20 distinct opacity values over ~330ms, a
  real ramp, on both paths.
- **A second bug found on the way.** The rule that cancels colour cross-fades
  inside the chooser included `body #lnch` itself, which restricted the
  launcher's own `transition-property` to a colour list and made opacity
  untransitionable regardless. Scoped to descendants, which is what its own
  comment describes.
- **Pins get a launch acknowledgement.** The tapped chip lifts and lights while
  the rest of the row steps back, so the module reads as coming from the thing
  you touched. Deliberately not a morph: growing a 72px chip to fill the screen
  would be a different gesture rather than a matching one.
- The pin path also now holds the palette swap under cover and releases it the
  way `lnchGo` does, so the module's colours no longer flash in around the
  chooser during the handover.

## v0.101.6 — The entry plays in the right order, and during the dissolve

Asked to state exactly what should be visible, the trace answered instead - and
showed the sequence was wrong in three ways.

- **The hint arrived FIRST, alone.** It had its own .72s delay, so a line of
  small grey text faded up on an empty launcher roughly 200ms before the four
  cards it describes. It now rides the same class as everything else and trails
  them.
- **The cards arrived AFTER the splash had fully gone** - 167ms of empty launcher,
  then a grid appearing on top of nothing. They now start while the splash is
  still fading (measured 66ms before it clears), so it hands over to a grid that
  is already forming. That is what the entry was designed to do and had stopped
  doing.
- **It was slow.** 767ms of arrival on every single launch, now 599ms, with each
  element's fade trimmed from .42s to .34s.

Measured sequence, splash-on path: splash begins fading 5693ms, cards 5793-5959
(overlapping the dissolve), pins 5959-6192, hint 6026-6292. Cards, then pins,
then the hint - reading order, with the modules first because they are what the
screen is for.

The hint's delay needed !important for the same reason the pins' did: the
app-wide `*` transition rule replaces the whole shorthand, so without it the
delay is dropped and the hint fades in lockstep with the cards rather than after
them.

## v0.101.5 — One fade, and it happens after the handover

Three passes at re-timing the stagger never helped because the stagger was never
the problem. The measurement that found it: the veil fades OUT in lockstep with
the launcher fading IN - veil .93 against card .07, veil .42 against card .58,
veil .07 against card .93. They cancel each other, the screen's net brightness
barely moves, and the eye reads one soft reveal rather than anything arriving.

That crossfade is deliberate and stays - it is what keeps the app underneath from
ever being uncovered. What changed is WHEN the contents arrive.

- **The launcher surface still covers immediately**, doing its half of the
  handover exactly as before. Only the cards and pins wait, on a new `lnch-in`
  class set a beat after the veil is gone - so the fade has a settled background
  to be seen against instead of a disappearing overlay.
- **Every stagger is gone**, on both entry paths and on the pins. Staggering
  inside a crossfade only smears it, and the delays were tuned for a rise that
  no longer exists.
- **The rise is gone too.** One calm opacity fade, which is what was asked for
  and what is actually perceivable here.
- Measured: the veil completes 1 to 0 by 1531ms with the cards still at 0, and
  they fade from 1704ms afterwards. Boot guard still reports zero
  app-before-launcher frames across all five paths, and both cards and pins are
  visible on every path where the launcher is shown.

## v0.101.4 — The launcher entry finally happens where you can see it

Both symptoms had one cause, and it was older than the pins.

The module cards' stagger was written against "the splash's 1.3s dissolve", but
the splash actually runs about three and a half seconds - its own comment says
so, and the two numbers never agreed. Traced frame by frame, the cards rose and
settled at **1457ms with splash opacity still 1**. Verified in a control build
with the pins stripped out entirely, so this predates them: the grid has been
finishing its arrival behind an opaque overlay and then simply being uncovered.
That is the jank - not motion, but the absence of it where motion was expected.

v0.101.3 fixed the pins by hanging them off the splash's real dissolve event, and
that left the cards on the old assumption - so the two halves of the launcher
arrived four seconds apart.

- **One gate for both.** `_lnchWhenVisible()` runs its callback when the splash is
  dissolving, has finished, or never ran, with an unconditional 4.2s fallback.
  `lnch-entering` now comes off through it, and the pins release through it.
  Nothing is timed against an assumed duration any more.
- **The designed effect works now.** Measured: the cards rise from 5305ms as the
  splash passes 0.08 to 0, the pins follow from 5338ms, and the whole entry plays
  THROUGH the fade - which is what the original comment describes and what was
  never actually visible.
- Verified across all four entry paths, plus the boot guard's five: cards and
  pins both arrive on the two paths where the launcher is shown, both correctly
  untouched on the pinned paths where it is not, and zero app-before-launcher
  leak frames throughout.

## v0.101.3 — The pin animation was running where nobody could see it

You were right that there was no animation, and v0.101.2's verification was
wrong. The transitions were firing correctly - they were just finishing
underneath the splash.

Measured with the browser's own `transitionstart` events: all four pins animated
at **1610-1720ms while the splash was still at full opacity**. By the time it
dissolved the row had long since settled, so it appeared fully formed. The module
cards do not have this problem because their stagger is deliberately timed to be
watched THROUGH the dissolve; the pins, added later on a copied delay, landed
before it.

- **The release is now an event, not a delay.** A fixed number cannot work here:
  the splash waits on fonts, sample preload and the viewport settle, so its real
  length is not a constant - measured well past 2.2s in the container against the
  1.3s the design assumed. The row is held hidden until `.lnch-qa-in` is set,
  which hangs off the splash's own dissolve, its completion, and the no-splash
  path's viewport settle.
- **A hard 4.2s fallback fires first and unconditionally**, so a missed event can
  never leave the row invisible.
- Verified across all four entry paths. The first attempt broke the skipped-splash
  case - that path returns early from `lnchInit` and never reached the release, so
  the row stayed hidden - caught by testing every path rather than only the one
  being fixed.
- With the splash on, the pins now animate as its opacity passes 0.08 to 0. With
  it skipped, they animate during the veil crossfade. Both are the moment the
  launcher becomes visible.

On the verification itself: v0.101.2 claimed the animation worked because
computed styles and `transitionstart` both reported it running. They were telling
the truth about the transition and nothing about whether it was on screen. A
control build with the change removed behaved identically, which is what showed
the measurement rather than the code was the problem.

## v0.101.2 — The pins arrive like the cards do

The quick-access row faded in as one block while the four module cards above it
rose and staggered. Same screen, same arrival, so it now uses the same gesture -
rise and fade - scaled to the object.

- **A smaller lift and a tighter step.** The cards travel 14px on an 80ms stagger;
  the pins travel 8px on 40ms, because they are smaller buttons and there can be
  eight of them - 80ms each would have run the entry on far too long. Capped at
  six: past that the remainder arrives with the sixth, since a stagger nobody can
  follow is just latency.
- **The delays needed `!important`.** All nine computed to 0s without it and every
  button arrived at once: the app-wide `*` transition rule replaces the whole
  shorthand, which is the same trap that flattened the launcher entry in v0.99.32
  and the tab bar's slide. Measured 0.70 / 0.74 / 0.78s afterwards, and traced in
  motion to confirm they actually cascade rather than merely computing correctly.
- **Press feedback survives it.** The entry rule gives transform a .46s duration
  so the buttons can rise, and a tap inheriting that would take half a second to
  respond. `:active` re-states .09s and, at ID specificity, wins - verified at
  `scale(0.96)` and `0.09s`.

Worth recording: the press appeared broken through several rounds of testing
because a synthetic mouse-down does not hold `:active` on a button that has a
click handler. Forcing the pseudo-state through CDP showed the CSS had been
correct for some time. The harness was wrong, not the app.

## v0.101.1 — The launcher hint mentions quick access

With no pins the row hides itself, so nothing on the launcher suggested the
feature existed. The hint line now carries it:

> Pin a module here · star tools for quick access

Deliberately NOT an empty-state row. The hint above it is always on screen in
both states, so an empty shelf saying "star tools to pin them here" would put two
different meanings of "pin" side by side on the one screen where a new user is
already working out what pinning does - pinning a MODULE skips the grid, starring
a TOOL adds it to a row. One clause on the existing line teaches the second
without competing with the first, and the star sheet still does the real teaching
at the moment you can act on it.

- The Italian is not a literal translation: "stella gli strumenti per l'accesso
  rapido" wraps to two lines at 320px, and a wrapped hint reads worse than no
  nudge, so the shorter "stella per l'accesso rapido" ships instead. Both
  measured at one line at 320 and 393px.

## v0.101.0 — Quick access on the launcher

The launcher asks "which module". Quick access already knows what you actually
do. So the pinned list now sits under the module grid: open the app, tap DROP D,
land on the chart.

- **Built from the same `progState.favorites` the star sheet manages**, so there
  is one place to pin things and two places to reach them - the launcher never
  becomes a second inventory to keep in sync.
- **Saved chart views come first**, ahead of tools and exercises. "Open the app
  and go straight back to my Drop D chart" is the case this exists for, and a
  saved view carries more context than a bare tool.
- **Colour carries the type**, reusing the fav sheet's own vocabulary: cyan
  tools, purple exercises, green saved views. No new language to learn.
- **It scrolls rather than wrapping.** Measured 292-312px of usable width, so
  three fit without scrolling and five sit at 54-58px each; beyond that the row
  scrolls. A wrapping list would change the launcher's height as the pin list
  grew, pushing the four module cards - the thing the eye lands on first - down
  the screen. The launcher being the same shape every time is what makes it fast.
- **No pins, no row.** It is `hidden` entirely rather than showing an empty
  shelf.
- Stale keys are skipped quietly, so a favourite left over from a removed tool
  cannot take the row down with it.

Two things worth recording. `.lnch-pin` was already taken - it is the
absolutely-positioned pin badge on each module card - and reusing it stacked all
eight buttons at the same coordinates; the row is `.lnch-qa` now. And the
document-level `touchmove` blocker that would have killed the horizontal scroll
on device turned out to be correctly scoped to the Survival Guide, so it does not
reach the launcher; checked rather than assumed, since it would have looked fine
in a desktop browser either way.

## v0.100.17 — Picking an instrument lights the panel too

Choosing an instrument and going back to the picker both snapped: the change is a
plain `display` toggle on the setup strip, with nothing between the two states.
They are the same event as a face swap - the glass showing something different -
so they now use the panel's own re-light rather than a separate effect. One
visual language for "the screen changed", not three.

- `_sfRelight()` replays the same `sfScreenOn` glow the face swap uses: opacity
  0 -> 1 with brightness settling 1.55 -> 1.06, no transform. Traced on both
  legs; picking and clearing ramp identically.
- Retrigger-safe by the same means as the face swap - the class is removed and a
  reflow forced before re-adding, since an animation will not restart while its
  class is already present. Verified firing across five consecutive transitions
  (pick, clear, pick, clear, chromatic) with state intact each time: pips, the
  tuning list and the strip label all correct.
- The face swap, the guide's independence from Simple, and the meter geometry are
  all unaffected.

## v0.100.16 — Less cathode ray, more lit segments

The squash-and-overshoot read as a glitch, and it was the wrong reference. A tube
collapses its beam vertically because there is a physical thing bouncing; this
glass is a lit segment display in a bezel - amber and cyan glyphs on dark glass -
and segments have no inertia and no geometry. Any transform on them is a jump,
not a screen.

- **The transform is gone entirely.** Verified across four consecutive swaps:
  peak scaleY deviation is now exactly 0, where the CRT version measured 0.14.
- **All the character is in the glow ramp now**, which is what a VFD actually
  does: the segments strike over-bright and settle. Traced frame by frame,
  brightness 1.55 -> 1.31 -> 1.12 -> 1 with a matching saturation lift, while
  opacity rises 0 -> 0.54 -> 0.9 -> 1.
- Slightly gentler than the CRT version too: the brightness peak drops from 1.9
  to 1.55 and the duration from .34s to .30s, since without the geometry move the
  bloom is doing all the work and does not need to shout.

**On the transport bar:** it was genuinely left out, and it stays out - but not
for want of trying. The row sits inside `#tunerReadout`, and that subtree is
`display: none` during the swap itself, so an animation started on it never gets
a start time and freezes on its first keyframe. Two attempts to drive it
separately both stuck: once at `opacity: 0` for the entire ramp, once at
`brightness(1.5)`. Since the readout it belongs to already re-lights as one
object, the row travels with its parent, which is the correct behaviour anyway -
the chrome and the numbers are the same panel.

## v0.100.15 — The glass re-lights instead of cross-fading

The face swap dissolved its contents: 100ms out, 300ms in, pure opacity. That is
a slideshow gesture. A real display does not dissolve between two pictures - it
blanks and re-lights, and the character comes from how the panel responds, not
from the content's opacity.

The app already had that vocabulary: the tonal-centre CRT's `tcPowerOn` does a
brightness overshoot with a vertical squash that settles. The face swap now
borrows the same grammar rather than inventing a second visual language for the
same idea.

- **`sfScreenOn`**: the arriving face starts blanked and squashed to 0.86 on Y at
  brightness 1.9, snaps past 1.0 to a 1.03 overshoot, then settles. Traced frame
  by frame: 0.86 -> 1.03 -> 0.995 -> 1.0, brightness 1.9 -> 1.35 -> 1.06 -> 1.
- **Y only, never both axes.** A display's image collapses vertically; scaling
  both reads as a zoom, which is the PowerPoint move being replaced.
- The out-leg is a blank rather than a fade (60ms linear, and the dark gap
  shortened from 90ms to 70ms), so the panel cuts and comes back rather than the
  two faces overlapping.
- Retrigger-safe: the class is removed and the reflow forced before it is
  re-added, so the animation replays on every swap. Verified firing in both
  directions across four consecutive swaps with identical amplitude, and it
  respects `prefers-reduced-motion`.
- The surrounding choreography is untouched: the screen still never resizes, the
  card still sheds its 149px on the .42s curve, and the card sheen still holds
  still.

## v0.100.14 — The sheen that actually moved

v0.100.13 fixed the wrong reflection. There are two: the glass shine on the
screen, and a second sheen on the CARD behind it - and the card one was the one
being pushed around.

`.tuner-bpm-card::after` was sized as a percentage of the card (`top: -60%;
height: 200%`). The card's height animates on a face swap - traced frame by
frame, 481px down to 332px over .42s - so that highlight's height ran 962px to
664px and its anchor slid the whole way with it. Anchored in px now (`top:
-180px; height: 620px`), it holds still at exactly those values across the entire
transition while the card resizes underneath.

The same block appears **three** times - the tuner card declares it twice,
identically, and the metro card is built the same way. All three are fixed, since
the later declaration would otherwise win and undo the earlier one. The
`assert count == 1` in the edit script is what caught this; the first attempt
would have patched one copy and left two.

**On the swap feeling like a bigger change than a readout:** it is, and it is
deliberate. Measured across a swap, the screen holds perfectly still (256px, same
y) while the card sheds 149px and the guide below it moves up 149px and shrinks
139px. The existing design note is explicit that this is intentional - the glass
never resizes because that would be "animating a lie", and the card and guide
carry the sense of the layout rearranging. An attempt to also collapse the bottom
section on the same curve made it worse, not better: the section animated first
and the card only snapped afterwards, turning one movement into two. Reverted.

## v0.100.13 — The glass reflection sits on the front in both faces

The glare was never moving. The housing, the bezel, the glass and the gradient
itself measure pixel-identical between the two faces - same box, same 443.78 x
238px pseudo-element, same peak column. What differed was which SIDE of the
content it was drawn on.

`.tuner-screen-inner::before` carried `z-index: 1`, but `#simpleFace` is
`z-index: 2`. So the simple face had its highlight painted BEHIND the setup
buttons and the pips, while the full face - whose readout has no stacking context
- had it in front of the readout. One gradient, opposite sides of the content,
which is what read as the light having moved when you swapped.

- The shine is now `z-index: 3`, in front of the content in both faces. A
  reflection is on the front of the glass either way.
- Verified the highlight peaks at the same column and the same brightness in the
  full face, the simple setup screen and the simple readout, and that the
  content underneath is unaffected: the setup buttons measure 10.17:1 with the
  shine over them, since it peaks at 0.07 alpha.

## v0.100.12 — "PLAY A STRING" stops showing before there is a string

A regression from v0.100.9, and the rule that should have caught it was already
there: `body.sf-needs-pick` stands the readout down while you are choosing,
because there is nothing to read yet. The state line used to live inside
`.sf-core` and was hidden with it. Moving it out of the ring - so it would stop
crossing the dial - quietly took it out of that rule's reach, so the setup screen
told you to play a string before you had said what you were tuning.

- `.sf-state` joins `.sf-core`, `.sf-pips` and `.sf-chosen` in the needs-pick
  rule. The setup screen is now just the question.
- Checked all four states rather than only the one reported: while choosing, only
  "WHAT ARE YOU TUNING?" shows; after picking, the ring, pips and state line all
  return; chromatic keeps the ring and the state line but has no pips, which is
  correct; and clearing the instrument goes back to the bare question. The face
  still holds its 194px with 22px of clearance in every one.

## v0.100.11 — Each face gets its own tuning list

v0.100.10 stopped Simple from overwriting the guide, but it took Simple's own
tuning list with it. The card under the glass rendered from the guide's
`selectedFamily`, so once Simple stopped setting that, the list came up empty:
picking a family gave you pips and nothing to change the tuning with.

The card is shared markup serving two independent selections, so it now renders
for whichever face is showing.

- **Simple has its own family** (`sfFamily`) alongside its own instrument, and
  `buildInstList` reads Simple's pair in the simple face and the guide's in the
  full one. Its pills call `sfPickInstrument` rather than the guide's
  `selectInstrument`, which was the coupling this whole change existed to remove.
  The Reference tool keeps using the guide's selection.
- **The card is rebuilt on every face swap.** One list serving two selections
  otherwise keeps whichever face built it last.
- **Two leftovers from the split, both caught by testing rather than reading.**
  `_sfSyncChosen` still read `selectedInstrument`, so the strip on the glass
  showed "—" instead of the instrument Simple was actually tuning. And the entry
  path still built the pips from `selectedInstrument`, so the row could show the
  guide's tuning while detection measured against Simple's.
- Verified end to end: the guide holds drop D on the guitar tab with 12 pills and
  its chip, while Simple independently holds a 5-string bass with 4 pills, its own
  chip and 5 pips; changing the tuning inside Simple's list moves only Simple;
  swapping faces changes neither; and detection targets the right instrument on
  each face.

## v0.100.10 — Light-mode chips, matching pips, and two pickers that stop fighting

- **The selected tuning was the hardest thing to read in light mode.**
  `.inst-pill.active` hardcoded the dark-mode cyan for its text, fill and
  sub-label with no light override, so on the light panel the chip telling you
  what you are tuning measured **1.29:1**. It now uses the light palette's own
  accent: 5.80:1 for the label, 4.69:1 for the sub.
- **The string pips did not match the picker beside them.** They carried their own
  light override at 5% fill / 13% border, which sat under the v0.100.9 base fix
  and left them far fainter than the family buttons on the same glass. Both are
  now #00536c at 14% fill / 40% border - two controls doing the same job on one
  screen should not be two different weights.
- **Simple and the string guide are independent now.** Simple's picker called
  `selectInstrument()` and `selectFamily()` - the guide's own setters - so
  answering "what are you tuning?" on the glass silently replaced a specific
  tuning chosen in the guide, swapped its family tab and dropped its active chip.
  Entering Simple did it again on every swap, which is why the guide always came
  back showing Simple's choice. Simple now holds its own `sfInstrument`.
- The coupling is kept in the direction that was always deliberate: the guide is
  where a specific tuning is chosen, so it still pushes down to the glass. That
  push is now unconditional - while it was gated on the simple face being
  visible, changing the tuning from the guide left Simple's target stale, and the
  next swap rebuilt the pips from one instrument while detection measured against
  another. Verified: guide set to drop D survives a bass pick in Simple with its
  tab, all 12 pills, active chip and 6-string grid intact, while Simple
  independently holds bass4 - and a tuning chosen in the guide still reaches the
  glass with pips, saved state and detection target all in agreement.

## v0.100.9 — The state line leaves the dial, and the readout gets a body

**The meter works and is correctly aligned.** Driven with simulated pitch rather
than the mic: the dot at 0 cents lands exactly on top of the circle (0.00px error
on both axes), note detection and closest-pip highlighting track correctly, and
the per-pip bar fills to exactly 25% at 25 cents and 50% at 50. The small values
seen on the first frame are the smoothing filter ramping, not a bug.

- **"PLAY A STRING" has left the ring.** It sat below the note, which put it
  32.8px below centre and 28.4px from the bottom arc - crossing it. Moving it
  above the note failed the same geometry in mirror image. The real constraint:
  the longest state, "TOO HIGH - LOOSEN", is 117.6px wide and the widest chord the
  circle offers is 104.5px, so NO position inside the ring works. It now has its
  own row between the dial and the pips, where it reads as a status line for the
  readout rather than a label painted on the dial. The ring pays 14px for it
  (108.5px with pips, still a perfect circle).
- **The readout's own elements got the treatment the picker got in v0.100.6.**
  The pips were `accent 4%` fill on `12%` border - the same colour as the glass,
  so the string buttons had no body, only a hairline. Now 12% fill and a 38%
  border. The note letters went 55% to 88%, their octave numbers 30% to 62%, and
  the instrument name under the dial 62% to 85%.
- The state line itself was 40% transparent, measuring 2.97:1. It carries the
  actual instruction, so it should not be the faintest thing on the glass; now
  5.48:1.
- Ring verified square (ratio 1.000) at 320-430px in both palettes, with 4- and
  6-string tunings and in chromatic, and the face still holds its 194px contract
  with 22px clearance.

## v0.100.8 — The simple face's dial is a circle again

Long-standing, not a regression: confirmed squashed in a v0.99.51 build too. The
recent colour work only made it easier to see.

The face is pinned to a hard 194px on purpose - it has to reproduce exactly the
inner height the full readout had, or the housing resizes when you swap layouts
and the screen stops reading as one physical object. Inside that, the ring was
sized WIDTH-first: `width: 100%`, capped at `max-width: 156px`, with
`aspect-ratio: 1` expected to supply the height.

But `.sf-core` only ever has ~117px of height to give, once the pips row (42.5px)
and the instrument strip (34px) take their share. So `max-height: 100%` overrode
the aspect ratio and the "circle" rendered **156 x 122.5** - a 1.33:1 ellipse sat
inside a round bezel, with everything around it pressed to the edges. A square
156px ring needs 227.5px in a 194px box, a 33.5px deficit, so the ratio could
never hold whatever single width was chosen.

- **The ring is now sized from its height instead**: `height: 100%; width: auto;
  max-height: 156px`. The aspect ratio becomes the thing that holds, and the wrap
  simply takes whatever height the row leaves and derives its width from it.
- This also fixes the state the fixed width could never serve. Chromatic hides
  the pips, so it has 160px of height available: it now renders a full square
  156x156, while a 6-string guitar renders 122.5x122.5. Both circular, one just
  larger - the ring grows when there is room rather than stretching sideways.
- Verified square (ratio 1.000) at 320, 360, 393, 412 and 430px, in light and
  dark, with 4-string and 6-string tunings and in chromatic. The face still holds
  its 194px contract with 22px clearance inside the glass, and the canvas backing
  store re-measures correctly (369x369 at DPR 3, uniform scale on both axes).

## v0.100.7 — The flash guard stops depending on where it sits in the file

The pre-paint veil was correct and is still doing its job: traced frame by frame,
every boot path (splash on, splash skipped, pinned, and localStorage throwing)
showed zero frames of the app before the module grid. But the guard depended on
something fragile - the veil is created by an inline script sitting 1.49MB into
the document, roughly 5KB AFTER the .app markup. In an ordinary load nothing has
painted by then, so it wins. Any host that paints an intermediate parse state -
a preview wrapper, a streamed load, a WebView that flushes early - can show the
bare app before that script exists. Position in the document is the wrong thing
to bet on.

- **The app is now hidden from the first byte**, by a rule at the very top of
  <head>: `html:not(.boot-ready) body > .app { visibility: hidden }`. This cannot
  lose the race, because it applies before any body markup is parsed at all. The
  existing boot script clears it the moment the veil, splash or launcher is in
  place, so nothing uncovers a bare tuner.
- **The failsafe lives in <head>, not in the boot script it protects.** Putting it
  inside would have traded a brief flash for a permanent blank screen on any path
  where that script is never reached - verified by truncating the document before
  it: the app stayed hidden forever, and now recovers to visible. An independent
  1500ms timer next to the rule it undoes closes that.
- Verified across five boot paths: reveal fires between 136ms and 987ms, zero leak
  frames, and every path ends with the app visible and the grid built.

Note for the html preview specifically: it renders the file through its own
wrapper, so its paint timing is not the app's. This change removes the app's
dependence on that timing, but a preview is still not a measurement of the
packaged build - the Android/iOS WebView loads the file directly.

## v0.100.6 — The screen is meant to stay dark, and the dead brightness palette is gone

Two answers and a correction.

**lt-bright was dead code, and it is now removed.** `lightBrightSetting()`
migrates any stored 'bright' back to 'soft' and then hard-returns 'soft', so the
class could never be applied and every rule under it was unreachable. Removed 11
CSS rules (~3.4KB) plus the two JS toggles that could only ever pass false.

**v0.100.5's light tint was a mistake, and it is reverted.** The tuner screen
carries `.keep-dark`: it is a signature surface that holds the dark palette in
both modes, framed inside light chrome like a video player on a light page.
Tinting its glass toward paper fought that architecture, which is exactly why the
buttons on it did not improve. The tick and FLAT/SHARP lifts from that pass were
independent of the tint and survive the revert at 6.19:1.

**The faint buttons were never about the glass.** Their fill was
`color-mix(accent 4%, transparent)`, which measured the same colour as the glass
behind them - the cards had no body, only a hairline. Worse, because the screen
is `.keep-dark`, `--accent` inside it is the dark cyan in *both* modes, and cyan
over pale glass cannot separate at any strength: every value tested landed
between 1.03 and 1.05:1. Light mode therefore needs a dark ink rather than more
accent.

- Family buttons: 12% fill and 38% border, with light mode overridden to a
  #00536c fill at 14% and a 40% border. Separation against the glass went from
  1.06:1 to 1.26:1 in light and 1.24:1 in dark; the labels stay at 8.9:1 and
  5.9:1.
- CHROMATIC measured 2.60:1 light and 1.95:1 dark - the faintest thing on the
  screen despite being a real choice beside the five families. Now has a fill, a
  42% dashed border and 78% ink.
- The "what are you tuning?" prompt went from 40% to 75%.

## v0.100.5 — The light screen reads as glass instead of paper

Tint B from the preview, plus the tick lift that went with it.

- **The screen glass was #f9fbfd to #e8eff6 - luminance 0.90, effectively
  paper.** The scanlines, the inset shadow and the bezel's highlight all had
  nothing to sit on, so the panel never read as lit. The soft default is now
  #e8f1f3 to #d2e1e6, luminance 0.82, and the readouts barely move: FREQ 8.33:1,
  OCT 8.91:1, cents 7.43:1.
- **The chroma strip moved with it.** It is the same pane of glass to the eye and
  sits directly under the main screen; leaving it white would have split the
  instrument in half.
- **The meter ticks went from 3.01:1 to 5.69:1.** They were already marginal on
  white and would have sat lower on tinted glass, and they are the scale the
  needle is read against.
- **FLAT and SHARP got the same lift.** They carried the identical faded value
  the ticks did and measured 2.81:1 once the glass was tinted - the labels saying
  which way the needle leans should not be the faintest thing on screen.
- **The bright setting is deliberately untouched.** Soft and bright still read
  differently (0.60 against 0.65), so the control keeps meaning something instead
  of collapsing both options onto one look.

Metro's screen has the same construction in amber and has not been tinted; it
should get the matching treatment if this one feels right on-device.

## v0.100.4 — The meter scale you read the needle against

A contrast pass inside the lit screens themselves, rather than the chrome around
them, measured with the screen in both its idle and lit states so a designed
resting value is not mistaken for a broken one.

- **Dark mode's meter tick labels were `rgba(255,255,255,0.18)`: 1.59:1 on the
  screen glass.** These are the -50/-25/0/+25/+50 scale the needle is read
  against, so they are not decoration - at that level the needle floats against
  nothing. Raised to 0.45 alpha, which measures 4.52:1 and still sits behind the
  needle and the note in the visual order.
- Left alone deliberately: the big note and OCT label measure low in dark mode,
  but that is the idle state with no pitch detected, and the screen has a
  `.listening` class that governs the lit state. Those readings are the screen
  being asleep, not being broken.

Still open, and prototyped rather than shipped: light mode's screen glass is
`#f9fbfd → #e8eff6`, a luminance of 0.90, so it reads as paper rather than as a
lit panel - the scanlines and the inset shadow have nothing to sit on. Tinting it
costs almost nothing in contrast (the note stays above 7.8:1) but is a feel call,
so it is in `screen_tint_preview.html` for a decision on-device.

## v0.100.3 — Controls stop being drawn with transparent ink

A contrast pass over the tuner in both faces and both palettes, measuring the
rendered pixels rather than the declared colours, since most of this UI is built
from color-mix and var() and never states a hex.

The same mistake turned up four times: "this control is resting" was expressed by
making the ink transparent. Alpha lowers contrast, not emphasis, and the resting
state is the one almost every user sees - the hover states that restored full
colour never fire on a phone.

- **FORK measured 3.70:1 in light.** Its label was `color-mix(accent 55%,
  transparent)`, so the button was permanently half-faded despite always being
  live. Now full accent: 5.24:1 light, 10.23:1 dark.
- **The KEY pill's empty state measured 1.82:1** - the dash was very nearly
  invisible. It was `opacity: 0.4`; it now uses the muted token, which is what
  the rest of the app already uses to mean "quiet but legible".
- **The capo stepper buttons** carried the same `color-mix(..., transparent)`
  treatment. They are the controls the whole capo pass existed to make tappable,
  so they are now full accent.
- **The capo's zero readout used `var(--border)` as a text colour**, measuring
  1.31:1 in dark. A hairline token is not an ink token; it now uses muted.
- Left alone deliberately: the chroma strip's resting notes and the cents-meter
  tick labels measure low, but they are a designed inactive state that lights up
  on the note you are playing. Raising them would flatten the distinction the
  strip exists to draw.

## v0.100.2 — The pills stop lying about their own values

v0.100.1 let the value shrink so the label would stop overflowing. It shrank all
the way: "440" rendered as "4." and "NONE" as "NO". A pill that reports the wrong
number is worse than a tight one, so the value no longer gives ground at all and
the room comes from elsewhere.

- **The Hz unit is gone.** The pill is 89px at 412 and 78px at 390, and its
  contents needed 87px - so on every phone narrower than the widest one, the
  value absorbed the entire shortfall. Of the four parts, "Hz" was the only one
  telling the user something "440" had not already told them. Dropping it buys
  8-19px depending on width, which is enough on its own.
- **The arrow stays.** Dropping it instead would have bought 2.2px at 390, which
  is not a fix. It is also the only thing distinguishing these two pills from the
  capo readout beside them, which genuinely is static - without it all three read
  as status text. It already rotates when open, which is the part that says
  "this is a control".
- **KEY shows an em dash when nothing is set.** Every real value is one or two
  characters (B♭, E♭, F); only the empty state was four, so the pill was being
  sized by the single value that means "nothing here". The dash costs 12px
  instead of 34 and pairs with the dimming that was already applied when unset.
  The dropdown still says NONE, because there you are choosing rather than
  reading, and a lone dash in a menu is a riddle.
- Measured at 412, 390 and 360: every pill's content is narrower than its box,
  in the empty state and with all three transpositions applied, and at a
  three-digit reference pitch.

## v0.100.1 — The housing row's ghost pill, clipped A, and a clef pretending to be a fork

- **A second pill was hanging below the row in the full face.** The slot is
  shared: KEY in full, CAPO in simple. A later alignment fix set `display: flex`
  on all three pills at equal specificity, and being further down the sheet it
  quietly cancelled the earlier `#tunerCapoQuick { display: none }`. Both pills
  rendered, the second one overflowing the 28px slot - the ghost under CAPO. The
  face split is re-asserted after the alignment rule so the cascade lands the
  right way round, and each face shows exactly one pill again.
- **The A in the 440 pill sat outside its own padding.** `space-between` with
  non-shrinkable end caps pushed the first child past the pill's content box:
  2.6px past it at 412px wide, 8px at 360. The row centres instead, the value
  carries the slack, and the one-character label's trailing letter-spacing (2px
  of dead air after the only glyph) is pulled back. Measured inside the padding
  at 412, 390 and 360.
- **The fork button was wearing a treble clef.** U+1D11E means "written music",
  not "reference pitch", and the voice fork elsewhere in the app already uses
  something else - the app disagreed with itself. Its ink also sits high in the
  em box with a tail below the baseline, so the glyph read high no matter how
  the box was centred; the boxes measured perfectly centred while looking wrong.
  It is now an inline SVG tuning fork, which says what the button does and
  optically centres because the ink fills the box.

## v0.100.0 — The tuner popovers stay inside the screen and above the guide

v0.99.51 released the card's overflow, which fixed one clipping path; two more
kinds of jank survived it on-device.

- **The capo stepper's + button escaped its own box.** The popover was pinned to
  its 91px anchor with `left:0; right:0`, but its content needs ~114px, so the
  plus button overflowed past the box, past the card, and off the right edge of
  the screen. The popover is now right-anchored with `width: max-content` and
  `min-width: 100%`: it grows leftwards over the card when the anchor is too
  narrow, so every control stays inside the box and the box stays on screen.
- **The A440 popover could still paint under the Tuning & Capo card.** The row's
  z-index of 60 is meaningless whenever any ancestor of the row briefly forms a
  stacking context (entry animation, will-change), because the guide card comes
  later in the DOM and wins on document order. The card itself now takes
  `z-index: 60` alongside its overflow release while a popover is open, so the
  whole card outranks the guide card no matter what context traps the row.
- **The Hz and Key popovers stop being 91px worms.** Anchored to a pill-width
  slot, the seven presets stacked one per row and the Custom input row was
  crushed. Both popovers are now right-anchored at `min(230px, 62vw)`: presets
  wrap four per row, the popover drops from 268px tall to 118px, and the Key
  list fits in a row and a half.
- Verified with Playwright at 412 and 360px, both faces: capo `+` ends inside
  its box (374 < 383 and 322 < 331), the A440 popover renders fully above the
  guide card, and nothing crosses the viewport edge.

## v0.99.51 — Capo adjusts in place, the Hz popover stops being clipped

- **The capo pill now opens a stepper.** It previously scrolled to the guide's
  control and flashed it, which meant tapping a capo control did not change the
  capo - it moved the page. It opens a small − 0 + in place instead, driving the
  same `changeCapo`, so there is still exactly one capo. The `›` arrow is gone
  with the behaviour it advertised.
- **The A440 popover was being CLIPPED, not stacked under something.**
  `.tuner-bpm-card` is `overflow: hidden` and the popover drops 109px below it,
  so no z-index could ever have fixed it. The card releases its overflow only
  while a popover is open, keeping the rounded-corner clipping it exists for the
  rest of the time. The two popovers are mutually exclusive - a row this narrow
  cannot show both.
- **The row was 56px tall in the full face, not 28.** The KEY pill's text wrapped
  to two lines at its shared width, doubling the row and leaving the swap button
  sitting at the top of it - the high alignment. Pills are `nowrap` and the row
  is pinned to 28px, so a wrap can never stretch it again. All four controls now
  share one centre line in both faces (measured spread 0px, down from 14px).
- Verified at 360, 390 and 414px: row 28px, nothing clipped, 13px inside the
  card, capo steps relabel the pips, popovers open fully and restore the card's
  overflow on close.

## v0.99.50 — The housing row fits the card again

Pinning the swap button to a hard 84px in v0.99.49 stopped the row sliding but
overflowed it: four controls at their natural widths need 337px plus 24px of
gaps in a 332px row, so the last pill hung 16px past the card edge in both faces.

- **Fixed basis, not fixed width.** `flex: 0 1 84px` keeps the swap button's
  geometry stable across the label change while still allowing it to give way.
  Every child may now shrink, the gap is 8px to 6px, and the pill padding is
  tightened. The row ends 13px inside the card in both faces.
- **Equal flex on the two pill slots.** With `auto` the A440 pill absorbed a
  different share of the leftover space in each face and pushed the last slot
  11px sideways - the exact shift the previous build set out to remove.
  `flex: 1 1 0` on both makes the widths identical (84/64/80/80) and the measured
  shift across a swap 0px on every control, in English and Italian.
- **KEY was clipping.** Its value reads "NONE" at 13px, the widest content in any
  pill: 88px of text in an 80px slot. The value type now matches the label size.
- **Narrow phones drop the word labels.** At 360px the row is ~26px tighter and
  still clipped; there the "A" and "CAPO" labels hide and the values carry the
  meaning alone. Verified clean at 360, 390 and 414px, both faces.

## v0.99.49 — The glare stops moving, and so does the row

Two things shifting between faces, both mine, both now still.

- **The screen glare moved.** v0.99.38 traded the inner panel's padding from 22px
  down to 10px in simple to buy the ring room. The highlight gradient is painted
  on the padding box, so a different padding lands the reflection somewhere else
  and the screen appears to shift as you swap. Padding is back to 22px in both
  faces and the simple face fits inside the 194px of content the readout had.
- **The row slid sideways.** Hiding transpose outright let the row reflow: every
  remaining control moved 8-26px on each swap and 71px of dead space opened on
  the right. The slot is now kept and its contents swapped - transpose in full, a
  capo readout in simple. Tapping it scrolls to the guide and flashes the real
  control rather than duplicating it; capo stays in one place.
- **The swap button was the other half of it.** Its label alternates Full /
  Simple (Completo / Base in Italian), so a content-sized button changed width on
  every swap and shoved everything after it. Pinned to 84px, sized for the
  longest label. Measured shift across a swap is now 0px on every control, in
  both languages.
- Fixed while testing: changing capo only relabelled the pips on the next pitch
  frame, so with the mic idle it appeared to do nothing. It rebuilds immediately
  now - capo 3 gives G C F A♯ D G the moment it is pressed.

## v0.99.48 — Simple keeps the housing row, minus transpose

The row was hidden wholesale in simple, which left the face looking stripped and
took one control with it that simple actually needs. Judged individually rather
than as a block:

- **A440 stays, and had to.** The simple face already bakes `refPitch` into its
  pip targets, so hiding the control while still honouring the value left a tuner
  quietly tuned to 442 with nothing on screen saying so - hidden state of the
  worst kind. It is visible and works from simple; the popover opens inside the
  card.
- **The fork stays.** Hearing the reference note is exactly a beginner's move,
  and it is one tap with no vocabulary attached.
- **Transpose goes.** It never touches the string grid; it only relabels the
  readout for transposing instruments, which is the one control in the row a
  first-time tuner has no use for.
- With transpose gone the A440 pill inherited its flex space and stretched to
  175px, twice the fork beside it. Capped: the row now reads 77 / 64 / 104 rather
  than one control grown to fill a gap. The wrapper carries an inline
  `style="flex:1"`, so the override needed `!important` - a class alone cannot
  outrank an inline style.
- Verified in both faces and both themes: swap animation unaffected, fork plays,
  A440 set to 442 and back, full face row unchanged at 63/64/88/101, screen
  housing still 29,113,332,256, sweep clean.

## v0.99.47 — The face swap animates

Switching faces was an instant cut. It now cross-fades the glass and travels the
cards, and the three parts are deliberately not simultaneous.

- **The screen contents cross-fade in place.** The glass is 238px tall in both
  faces, so anything that scaled the screen would be animating a lie: only what
  is drawn on it swaps. The leaving face clears in .10s, the arriving one takes
  .30s so it lands with the layout rather than ahead of it.
- **The cards travel.** The tuner card sheds 149px of controls and the guide
  gains 124px of settings, so those get a .42s height transition and carry the
  sense of the layout rearranging. Height cannot transition from `auto`, so both
  cards are measured before and after the switch, driven between those pixel
  values, then released back to `auto` - otherwise they freeze at whatever the
  swap measured and later content changes clip.
- **Pips and setup buttons arrive with a small lift** rather than appearing.
- Fixed a one-frame flash: the leaving face is `display:none`d the moment the
  class flips, which resets its opacity to 1 for a frame, showing the old
  contents at full strength. It is held `visibility:hidden` across the switch.
- Durations are `!important` because the app-wide `*` transition rule otherwise
  replaces them - the same trap that flattened the launcher entry in v0.99.32.
- Verified: both directions trace smoothly (481 to 332px against a 0 to 1 fade),
  zero flash frames, a rapid double-tap strands no inline heights, picking a
  tuning afterwards still reflows, reduced motion switches instantly, and the
  screen housing stays 29,113,332,256 throughout.

## v0.99.46 — Back to five categories, with names that mean something

Listing bowed and plucked members individually saved a tap and cost coverage: a
fixed shortlist cannot hold five bowed and five plucked instruments, so double
bass, bouzouki, lute and harp had no route into the simple face at all, and eight
buttons crowded the glass into three rows.

- **Five categories again**, every string instrument reachable. The second tap
  lands in the guide's list, which already scrolls and already holds everything -
  bouzouki, lute and harp included. Five buttons, two rows, comfortably inside
  the screen.
- **Better names for the two that are instruments rather than tunings.** "BOWED"
  and "PLUCKED" describe how a note is produced, which is not how anyone reaches
  for their case. They are now STRINGS and FOLK, with the members as the subtitle
  (violin · cello, mandolin · banjo) so the category explains itself without the
  jargon. The tuning-shaped families keep their count, since "12 tunings" is the
  useful line for a guitarist and "4 tunings" tells a cellist nothing.
- **Family defaults come from FAMILIES**, not from `Object.keys(INSTRUMENTS)`.
  Key order there is arbitrary and landed FOLK on bouzouki; the curated order the
  guide already uses gives mandolin for folk and violin for strings.
- Verified: zero unreachable instruments, bouzouki selectable with G D A D,
  lute survives a reload with its family and six pips, EN/IT labels (ARCHI in
  Italian), screen parity in both themes, full sweep clean.

## v0.99.45 — Roster audit: two orphans, three ghosts, one crash

Auditing the instrument data turned up three separate faults, one of them a live
crash on a path a user can reach.

- **Bouzouki and lute were unreachable.** Both exist in INSTRUMENTS with correct
  tunings, but `FAMILIES.plucked` listed only mandolin, banjo and harp, so
  nothing in the UI could ever select them. Plucked now lists all five.
- **CHROM. PERC. crashed the instrument list.** The family named organ, melodica
  and mallet, none of which exist in the roster, and `buildInstList` dereferenced
  them unguarded: selecting that family threw `Cannot read properties of
  undefined` and rendered nothing at all. The three phantom entries are gone and
  the loop now skips unknown keys, so a future roster edit degrades instead of
  breaking.
- **Bowed and plucked no longer hide behind a family step.** The two shapes of
  family are genuinely different: guitar, bass and uke are TUNINGS of one
  instrument (twelve guitar tunings; four ukulele sizes all named UKULELE), while
  bowed and plucked are DIFFERENT INSTRUMENTS sharing a technique. Nobody picks
  up a cello and thinks "bowed", so violin, viola, cello, mandolin and banjo are
  now direct choices on the setup grid. Picking one still points the guide at its
  family, so a violinist who meant viola is one tap away.
- Data verified rather than assumed: all 46 instruments checked note-name against
  frequency at A440 (zero mismatches, so every octave number and accidental is
  right), and 23 tunings checked against known standards including DADGAD, drop
  C, open G, baritone and the orchestral strings (zero mismatches).
- Verified: all nine families render, plucked shows five, mandolin survives a
  reload with its family and pips, screen housing unchanged at 332x256, eight
  setup buttons fit in three rows without overflowing the glass.

## v0.99.44 — The restored instrument brings its family with it

Two persistence gaps, both only visible across a real reload rather than a face
round-trip within one session.

- **The family did not restore.** `selectedFamily` initialises to 'auto' every
  load, so restoring the instrument alone left the guide's tab on AUTO with an
  empty tuning list: the choice persisted, but the panel that exists to change it
  showed nothing. The saved instrument's family is now selected first (order
  matters - `selectFamily('auto')` clears the instrument).
- **The tuning itself did not persist.** Only `sfPickInstrument` wrote
  `progState.sfInstrument`, and under the current flow the tuning is chosen from
  the guide, which goes through `selectInstrument`. Picking a 5-string bass and
  coming back next session handed you the family's default 4-string. Now saved
  wherever the choice is made.
- Verified across a genuine page reload: DADGAD restores as instrument and
  family, the guide lists all twelve guitar tunings with DADGAD marked active,
  the pips read D A D G A D, and chromatic restores as chromatic with no pips.
- Capo still resets to 0 on load. That is long-standing and left alone
  deliberately: a capo silently restored from a previous session would mistune
  every string without saying why.

## v0.99.43 — Simple's guide holds settings, not a second string list

The string rows were the pip row again at length. What they add over the pips is
the string number, the exact frequency and a numeric cents readout - precisely
the expert detail simple exists to remove - and both are tappable to hear the
note, so nothing is lost by dropping them there.

They were also expensive: 295px of rows pushed the tuning list to 849px on an
844px screen, so the settings the guide had just been given ownership of started
five pixels below the fold. Hiding the rows in simple brings the list to 540px
and shortens the page from 1261px to 952px.

- String rows hidden in the simple face only. The full face keeps all six with
  their frequencies and cents readouts, unchanged.
- The card is retitled to match what it actually holds: "Tuning & Capo" in
  simple, "String Guide" in full. Calling it a string guide while showing no
  strings would name the panel after the one thing it was not displaying.
  EN/IT both ways (Accordatura e Capotasto / Guida Corde).
- Verified: changing to DADGAD from the guide relabels the pips to D A D G A D,
  capo 2 shifts them to E B E A B E, the capo control is still reachable, screen
  housing byte-identical at 29,113,332,256 across picking, chosen and light, and
  the full face still renders six rows at 295px.

## v0.99.42 — One question per surface

Simple had ended up with two pickers doing overlapping jobs: the screen chose an
instrument AND a tuning, while the string guide below sat there as six passive
rows. They never appeared at once, but they were two mental models for the same
task, which is what made the flow hard to describe.

The split is now by grain rather than by surface:

- **The screen asks the coarse question.** Five families, one tap. Picking one
  selects that family's default tuning so the tuner works immediately, and points
  the guide's own picker at the same family so scrolling down lands on the right
  list rather than on AUTO. The two-step tuning list on the glass is gone.
- **The guide holds the settings.** Tunings and capo, together, because a capo is
  a modifier on a tuning. All twelve guitar tunings, four basses and the rest are
  reachable there, in the picker that already existed. Family tabs stay hidden in
  simple - that question was answered on the screen, and asking it twice was the
  confusing part.
- **Capo is in one place again.** Removing it from the glass also removed the
  second control for one value; the guide's own buttons call `changeCapo`
  directly and the face picks the change up through `_sfKey` on the next frame.
- `selectInstrument` now refreshes the face's label and pips, since under this
  flow the tuning is changed from the guide - without it the glass kept naming
  whichever tuning the family had defaulted to.
- Verified: DADGAD shows D A D G A D and Open G shows D G D G B D on the pips,
  bass family offers four tunings and 5-string gives five pips, capo 1 relabels,
  chromatic still bypasses all of it. Full face untouched; screen housing
  byte-identical at 29,113,332,256 across picking, chosen, chromatic and light.

## v0.99.41 — Simple face reaches the whole roster, and one capo per face

The six-button shortlist was hiding most of what the app already supports: the
roster carries 12 guitar tunings, 4 basses, 4 ukuleles, 4 bowed and 5 plucked
instruments, and a fixed list of six could not reach drop C, a 5-string bass or a
baritone uke.

- **Two steps instead of a shortlist.** Step one picks a family and says how many
  tunings it holds; step two lists them with their note sequences. Only families
  that actually have strings appear - wind, brass and voice have no string set to
  walk through. The tuning list scrolls, since guitar alone has twelve and the
  glass is 238px tall. A back control returns to the families.
- **One capo per face.** The face's own capo and the string guide's drive the
  same `capoFret`, so both showing at once in Simple was two controls for one
  value. The guide's copy is hidden in Simple only - the screen owns it there,
  which is where the instrument was chosen and where the pips relabel. Full is
  untouched and keeps the guide's control exactly as before. Verified the screen
  capo still drives the guide: at capo 1 both read F.
- The chosen-instrument label now uses the instrument's own name, which is
  correct once a family has been chosen: "STANDARD" and "DROP D" read properly
  inside a guitar list, where they did not as a lone label.
- EN/IT for the new strings including the tuning count (accordatura /
  accordature). Screen housing verified byte-identical at 29,113,332,256 across
  families, tunings, picked, and both themes.

## v0.99.40 — Simple face is drawn on the screen, not on top of it

The elements were correct but they were UI, not display: flat greys and white
cards floating on the glass while the full readout beside them is lit type. The
full screen gets its look from three things and the face now uses all of them.

- **Lit type, not text.** The note is the --grad-tune lime-to-cyan gradient
  clipped to the glyphs, exactly as .tuner-screen-note does, with the octave and
  state line drawn as color-mix percentages of --accent so they read as dimmer
  phosphor rather than grey. Idle dims the dash instead of blanking it - a screen
  at rest, not an empty box.
- **Pips are etched segments**, a hairline of tinted accent over a 4% wash, and
  the lit one gains a bloom. They sit in the glass instead of on it. Same
  treatment for the instrument picker, so choosing looks like part of the
  instrument rather than a dialog that opened over it.
- **The ring is drawn with the same gradient** and a shadowBlur bloom, cleared
  after each stroke so later fills do not inherit it.
- **Layout.** Content summed to 233px inside a 218px box, so the bottom strip was
  pushed off the glass: .sf-core needed `min-height:0` before flex would let the
  ring shrink. The ring is now fluid to 156px, the note 68px, and the bottom row
  is a fixed 24px band separated by a hairline rather than controls sitting on
  the edge. Verified everything fits with the housing byte-identical at
  29,113,332,256 across picking, guitar, violin, chromatic and light mode.
- **Chromatic says PLAY A NOTE**, not "play a string", and its pip row collapses
  rather than leaving a gap where the strings would be. EN/IT both ways.
- Noted while chasing a transparent drop-shadow: --theme is scoped to the module
  wrapper, so color-mix against it from inside the screen resolves to nothing.
  The existing .tuner-screen-note has the same issue and computes to
  `filter: none` today - the face now matches it rather than diverging.

## v0.99.39 — Simple face asks what you are tuning

Auto-detect is not reliable enough to run silently, and the numbers are stark:
on D3 fourteen instruments match at exactly 0 cents, so the detector returns
whichever sorted first. Played against real string sets it scores 0/4 on
mandolin and 1/4 on violin - a mandolin player is told guitar, then violin, then
ukulele, changing between strings. In the full face a wrong guess is visible and
one tap from being fixed; in simple it would be quietly wrong all session.

- **Simple asks once, up front.** A six-button strip (guitar, bass, ukulele,
  violin, cello, mandolin) plus a chromatic option fills the screen until a
  choice is made; the readout stands down while there is nothing to read. The
  choice persists, and the instrument name doubles as the button to change it.
  Auto-detect is untouched for the full face, where it belongs.
- **Capo moved onto the screen**, next to the chosen instrument - it is
  meaningless until you have said what you are tuning. It drives the real
  `changeCapo`, so the string guide below stays in step, and it hides entirely
  for bowed and chromatic instruments where a capo does not exist.
- **Chromatic mode** for people who want a tuner rather than a tuning: note,
  ring and cents with no string targets, no pips and no locking. Nothing to tick
  off because nothing was claimed.
- The chosen label comes from the face's own shortlist, not `INSTRUMENTS.name`:
  the default guitar preset is called "STANDARD", which reads correctly inside a
  list of guitar tunings and meaninglessly on its own. Bass is `bass4` in the
  roster, not `bass`.
- Verified: the screen housing stays 29,113,332,256 through picking, picked and
  full; capo +1 relabels pips E to F and drives the real capo state; violin and
  chromatic hide the capo; choice survives a face round-trip; EN/IT both ways;
  module and tool sweep clean.

## v0.99.38 — Simple face: the redesigned screen, in the app

The prototype screen is now the real Simple layout. The standard readout (freq
row, note, verdict, meter) hides in Simple and a purpose-built face takes its
place inside the same glass: a hold ring around a large note, one line of plain
words, and a string pip row along the bottom.

- **Detection, never auto-advance.** Every frame the played pitch picks the
  nearest string - the string guide's own closest logic - and the ring fills
  while that string stays inside the in-tune window. A completed ring locks the
  string with a two-note chime (through `_cueNote`, so it follows the master
  fader) and the pip stays ticked. Nothing moves on its own; playing a different
  string simply moves the highlight. Locks clear when instrument, capo or
  reference pitch changes, since the targets they described have moved.
- **The screen stays one object.** Verified byte-identical housing at
  29,113,332,256 in both faces. The comment `<!-- /tuner-screen-inner -->` turned
  out to label the bezel's close, not the inner's - the face initially landed in
  the bezel and grew the screen to 474px before the parent chain was checked
  directly. Inside the inner, its padding is traded 22px to 10px (invisible from
  outside) and the face pinned to the remaining 218px.
- **Light mode is gradient ink, dark is glow** - the same treatment the standard
  screen note already uses. Canvas colors resolve from the theme vars at draw
  time. Pips speak the string guide's own visual language (closest cyan,
  done green with a tick).
- Tapping a pip plays that string's reference note, like tapping a guide row.
  Chromatic fallback when no instrument is selected: note, ring dot and generic
  too-low/too-high wording, no hold ring (nothing to lock, nothing to "tighten").
- EN/IT strings for all face states; round-trip verified. Swap button pinned to
  28px so it no longer squashes when its row siblings hide.
- Verified: detection walks all six guitar strings, lock fires after the 900ms
  hold and persists across strings, capo +1 relabels pips E to F and clears
  locks, silence idles clean, Reference A/B identical with either face, full
  module/tool/exercise sweep clean.

## v0.99.37 — Tuner face: better placement, and Simple is actually simple

Two problems with yesterday's first pass.

- **The switch was a two-button tab row sitting above the string guide**, which
  is neither where the control belongs nor worth that much width for a choice
  between two things. It is now a single swap button, first item in the housing
  row to the left of the fork, styled as a sibling of the fork and A440 pill so
  the row reads as one set of controls. The label names the current layout rather
  than the destination: a control that renames itself to something you are not
  looking at reads as a bug.
- **Simple was still carrying most of the clutter it exists to remove** - the
  STROBE button on the screen, every teach hint, all the help "?" buttons and the
  detection badge. The strobe is a precision meter, the hints explain controls no
  longer on screen, and the badge narrates a detection the string rows already
  show by highlighting. All hidden in Simple now.
- The swap button lives inside `.tuner-ref-row`, which Simple hides, so the row
  is kept alive and only its other children are hidden - otherwise the control
  that leaves Simple would vanish with it.
- 44pt hit area via a pseudo-element, so the visual stays at 28px in the row's
  rhythm alongside the fork and pill.
- Contrast verified in both themes: 13.8:1 dark, 6.18:1 light. IT round-trip
  verified on the new label (Simple / Base).

## v0.99.36 — Tuner faces

The tuner now offers two layouts, switched from a control on the tuner itself
rather than buried in Settings: a beginner who wants the plainer view will not go
looking for it three menus deep.

- **The screen is untouched by the face.** Its housing, readouts, needle and
  every style inside it are identical in both layouts - verified byte-for-byte at
  (29,113) 332x256 with the note at 80px in each. Switching does not move or
  restyle a single pixel of the display, so the two faces read as one instrument
  rather than two tuners.
- **Simple** keeps the screen, the string rows and the capo, and hides the
  reference row (fork / A440 / transpose), the chroma and pitch-history panel,
  and the instrument picker. **Full** is unchanged from today and one tap away.
  Nothing is gated.
- **Scoped to `body.tuner-simple.theme-tuner`.** The card above the string guide
  is shared with the Reference tool, so a body-level class alone would have
  followed the user into Reference and hidden its controls too. Verified by A/B:
  Reference renders identically with either face selected.
- Light-mode ink: the active chip hit the fill-vs-ink trap the capo and
  panel-badge rules already document - fill and label both drawn from `--accent`,
  converging to 0.78 vs 0.80 luminance, effectively invisible. Paired with a
  deepened ink; now 7.99:1 in light and 10.98:1 in dark.
- EN and IT strings added (Simple / Base, Full / Completo); verified the toggle
  translates and restores on language round-trip. Choice persists via progState.

## v0.99.35 — Master fader now spans a real range

The fader moved the right nodes but barely changed anything audibly, at either
end. Two separate causes.

- **The headroom cap was global when it should be per chain.** `_getEffectiveScale`
  clamped everything at ~1.39, a number set by the LOUDEST chain in the app: a
  0.9-base site reaches its -3 dB threshold at 87% of the fader, so 1.39 is right
  for that one. A quiet 0.32-base site does not reach its threshold until ~246%,
  and the theremin not until ~272% - both were clamped at 1.39 anyway, throwing
  away most of the upper range for everything that was not already loud. The cap
  is now computed from each chain's own base gain. Verified no chain exceeds full
  scale at 200%: loud ones cap at 1.0, quiet ones reach 0.576 where they have the
  headroom for it.
- **The bottom half was worth only 6 dB.** A 50% floor is -6 dB, about one
  perceptual step spread over half the fader's travel, while the top half spanned
  far more. The floor is now 20% (-14 dB), so the two halves are roughly
  symmetrical and the fader can actually quieten things. Still a trim, not a mute.
- Fixed a double-count found while testing: the cap divided by
  `base * BASE_GAIN_BOOST`, but the hand-rolled chains register a base that
  already includes the boost, so their nodes landed at 1.111 - over full scale and
  a genuine clipping risk on percussive transients. `_getEffectiveScale` now takes
  an `alreadyBoosted` flag.
- At and below 100% the cap never binds for any chain, so every existing value is
  unchanged: 0.9 percussive, 1.0 Tonale/theremin, 0.72 and 0.288 for the 0.8 and
  0.32 buildLimiterChain sites. None of the clipping tuning is disturbed.

## v0.99.34 — Five chains now follow the master fader

Most audio runs through the shared `buildLimiterChain`, which `setMasterVolume`
updates live. Eight chains are hand-rolled for good reasons - the percussive ones
sit at -6 dB for transients, Tonale adds a +5 dB shelf at 300 Hz, the organ has a
saturation stage - and five of those were not fully wired to the fader.

- **Tonale and the theremin ignored master volume entirely.** Neither read the
  master scale at all: the Tonale out-bus ran bass -> limiter -> destination with
  no gain node anywhere, and the theremin's bus was pinned at 1.0. Pulling the app
  volume down left both at full level. Confirmed on device before changing
  anything.
- **The three rhythm-card chains** (`rcGetOut`, `rctGetOut`, `rcdGetOut`) read the
  scale correctly at build time but are cached, so they held whatever value was
  current when first built and ignored the fader afterwards.
- All five now register their gain node in `_masterGainRegistry` and are updated
  live, the same pattern `_getOrganChain` already used.
- **Gain only - never the limiter.** These chains keep their own thresholds on
  purpose (-6 dB percussive, -3 dB Tonale/theremin); registering the limiters
  would flatten them onto the shared base and undo the clipping tuning. Tonale's
  new gain stage sits AFTER its limiter so the +5 dB shelf and -3 dB threshold are
  untouched: it scales the finished signal rather than retuning the chain.
- Verified: at 100% every value is byte-identical to before (+5 shelf, -3 and -6
  thresholds, 0.9 gains). At 50% all five halve; at 200% they reach the 1.389 cap
  while keeping their own thresholds. Affected surfaces all open and exit clean.

## v0.99.33 — Entry animation: one movement, not three

The finish felt jerky because three things were moving in sequence at the end
rather than together.

- **The launcher and the card now fade at the same time.** They were staggered
  140ms apart, so the chooser cleared at ~826ms while the card was still at 0.95
  and fading until ~1009ms: the card floated alone over the module for nearly
  200ms, which reads as an extra beat tacked onto the end. Both now start at
  420ms and resolve together (measured within 0.03 opacity of each other).
- **The card was being cut off at 0.21 opacity** rather than reaching zero,
  because teardown fired before the fade finished. The margin is now generous
  enough that the fade always completes.
- **The tab bar waited for the handover.** It slides in when `lnch-open` is
  dropped, which is now mid-fade, so a third element started moving while two
  others were still resolving. It is delayed 300ms during entry only, and holds
  off-screen until both fades are done. A `lnch-settled` flag clears the delay
  afterwards so ordinary tab switching stays instant.
- The bar's delay needed `!important`: the app-wide `*` transition rule was
  replacing both its duration and delay, the same override that flattened the
  entry timings in v0.99.32.
- Verified across all four modules: both layers fade in lockstep, card grows to
  278px, teardown complete, correct theme, bar arrives last.

## v0.99.32 — Entry animation actually animates

The entry read as a snap with no fade because three separate things were
cancelling it, none of them visible in the code that defines the animation.

- **The launcher's own rule was stripping every duration.** The colour-cross-fade
  suppression added in v0.99.28 rewrote `transition-property` with `!important`
  across `#lnch` and all its descendants, which also discarded the durations: the
  entry's .46s travel and .3s fades were silently replaced by the app-wide .06s /
  .2s defaults. It now zeroes only the colour properties and leaves everything
  else alone; the launcher opts back into its own .34s fade explicitly.
- **The morph sits outside `#lnch`**, so the app-wide `*` transition rule applied
  to it instead. Its timings are now `!important` for the same reason.
- **Nested teardown timers drifted.** Each stage was scheduled from inside the
  previous one, so the card's fade started ~220ms late and was then cut off at
  0.45 opacity by a teardown scheduled from an earlier estimate — the card jumped
  from half-faded to gone. All stages now run off one clock, and teardown waits
  for the fade duration plus a frame.
- **Growth raised 1.35x to 1.7x.** At 1.35x a 164px card gained only 57px and
  finished in 300ms, then sat motionless for another 300ms. It now travels 164 to
  278px over ~500ms and the motion fills its own time.
- Verified across all four modules: mid-fade opacity samples between 0.89 and 0.98
  (a fade, not a cut), card grows to 278px, tears down completely, correct theme.
  Reduced motion still bypasses the whole thing.

## v0.99.31 — Entry animation: deal, centre, hand over

The full-screen card expand shipped in v0.99.29-30 was always going to be a flat
coloured rectangle: a real content-carrying clone would have to duplicate ~5400
DOM nodes, and canvases clone blank, so the tuner needle and metronome would
expand as empty boxes. Rather than polish an effect that cannot show what it is
pretending to show, the card now stays a card.

- **Deal → centre → hand over.** The three unpicked cards deal away on their own
  vectors; the chosen card travels to the middle of the screen while growing
  1.35x, holds there, and the module cross-fades in as the launcher clears. The
  card is never asked to stand in for module content.
- **Scale about the card's centre.** With the default `0 0` transform origin the
  growth pushes the box down and right, so the translate meant to centre it landed
  progressively further off the more it grew (206/226/248px against a 195px
  target). `transform-origin: 50% 50%` fixes it: all sizes land dead centre.
- **Opacity left to the stylesheet.** The start state wrote `style.opacity = '1'`
  inline, which beats `.lnch-morph-fade` on specificity, so the card reached the
  centre and then never faded out. The inline value is now removed instead of set.
- Verified across all four modules: cards deal, cloned face paints its real
  gradient, card lands centred at 221px wide, fades and tears down completely,
  correct theme lands, no stuck hold flag. Reduced motion still bypasses it.

## v0.99.30 — Entry animation actually runs

v0.99.29 shipped the entry animation with two faults that between them made it
invisible: the cards never moved and the expanding card was transparent.

- **Cards did not move.** The entry-reveal rule `#lnch .lnch-cell { transform:
  none }` has specificity 1-1-0; the new deal rules were written as
  `.lnch-cell.lnch-other:nth-child(n)` at 0-3-0. An ID beats any number of
  classes, so `transform: none` won every time and the classes applied to no
  visible effect. The deal rules are now scoped under `#lnch` so later-wins
  applies. Verified: cards travel from 25,176 to -11,159 with rotation.
- **The expanding card was invisible.** The morph cloned `.lnch-face` alone, but
  every rule that paints a card is written `.lnch-cell .lnch-face`, and the
  gradient reads `--lc` which is set on the cell. A bare face clone matched none
  of them and rendered as an empty rectangle - the morph was running the whole
  time with nothing to see. It now clones the whole cell and strips the pin badge,
  which keeps the descendant selectors and the custom property intact.
- Verified across all four modules: cards move, the cloned face paints its real
  gradient, the morph grows to 390px, tears down completely, correct theme lands.
  Reduced motion still bypasses the morph entirely.

## v0.99.29 — Launcher entry animation

The chooser used to scale the picked card to 1.05, fade the others, and cross-fade
the whole launcher out over the module. Nothing connected the card to the module,
so it read as a hard cut.

- **Deal + expand.** The three unpicked cards are dealt away on their own vectors
  with rotation, then the chosen card is cloned into a new `#lnchMorph` layer at
  its exact on-screen rect and grown to fill the viewport. Two beats: the choice
  reads first, then the entry. The eye follows one object into the module.
- The clone copies the `.lnch-face` only — the pin badge is chooser furniture and
  must not fly into the module with it. The card's label and peek fade in 100ms
  while its plain background lingers, so the crossover never looks thin.
- **Sequencing.** The morph is the only thing covering the module while the chooser
  is torn down, so it has to outlive both the launcher fade and the `display:none`
  that follows it. `finish()` runs at 260ms; the morph is not released until
  580ms, after `#lnch` is actually hidden. An earlier ordering released it first
  and briefly exposed the module bare.
- Start state is written with transitions suppressed and flushed before the end
  state; setting both in one frame means the browser only sees the end value and
  nothing animates.
- Reduced motion skips the morph entirely and lands instantly, as before.
- Verified across all four modules: clone grows 164→390px, tears down completely,
  correct theme lands, no stuck hold flag; launcher hides while the morph is still
  opaque over the module.

## v0.99.28 — Launcher owns its palette

v0.99.27 deferred the theme swap but the cards still recoloured, because the fix
was aimed at the wrong thing. The card faces were themselves built from
`--surface` and `--panel`, which are themed per module — so all four cards
repainted whenever the theme class landed, no matter when that happened.
Deferring only moved when you saw it.

- **Pinned the launcher's palette.** `#lnch` now declares its own `--surface`,
  `--panel` and `--border-soft` (with a light-mode set), so the chooser looks
  identical whichever module you last used or are about to open. Verified: card
  faces are byte-identical across all four themes in both light and dark, while
  the four cards keep their individual `--lc` tints.
- **No colour cross-fade on the chooser.** A global `*` rule gives every element a
  0.06s background/colour transition to soften per-module theme changes; on a
  surface with a fixed palette that can only animate an artifact. Scoped it out for
  `#lnch`, leaving transform, box-shadow and opacity — the actual press feedback —
  untouched.
- **Pin button hit area now meets the 44pt minimum** via a pseudo-element, so the
  visible dot stays 24px while the tap target no longer competes with the card.
- Verified across all four modules × both themes: cards unchanged on tap, correct
  theme lands after the transition, hold flag cleared every time.

## v0.99.27 — Launcher no longer recolours before the module arrives

Picking a card from the launcher called `setMode()` at tap time, which swapped the
`theme-*` class on body synchronously. The palette therefore changed while the
chooser was still on screen and its pick animation was still running, so the next
module's background and accent flashed around the launcher ~125ms before the
module itself appeared.

- **Split the palette swap out of `setMode`** into `applyModeTheme()`, with a
  `_themeHold` flag. `lnchGo` sets the hold before calling `setMode`, then releases
  it inside `finish()` — the moment the launcher is opaque over the new screen. The
  colour change now happens under cover, so the module is already wearing its own
  palette as the chooser fades away.
- **Reduced-motion path unaffected**: with no animation to hide behind, the theme
  applies immediately as before.
- **Normal tab switching unaffected**: still instant, since the hold is only ever
  set by the launcher.
- **Failsafe**: if a hold is ever left unreleased (an error before `finish()`, or a
  teardown mid-animation), a 600ms timer applies the pending palette anyway rather
  than stranding the app on the previous module's colours.
- Verified across all four modules: palette deferred at tap, correct theme landed
  after the transition, hold flag cleared every time.

## v0.99.26 — Real alto and tenor clefs

Alto and tenor were the only clefs still drawn as a font glyph (U+1D122) via
<text>, which renders as tofu on any device whose system font lacks the musical
C-clef. Now they draw as a real Bravura path like treble and bass.

- **Extracted the SMuFL cClef (U+E05C) from Bravura.otf** at the same scale
  (0.036, y-down) the existing treble/bass paths use, verified by reproducing
  RR_TREBLE from the font byte-for-byte first. Added as RR_CCLEF (pbox
  measured: x0 y-18.22 w25.16 h36.43); both alto and tenor point at it.
- **Corrected the path-clef vertical anchor** so the glyph origin (y=0), which
  every Bravura clef places on the line it names, lands on that staff line. The
  C-clef is symmetric about its notch, so origin-on-line puts the notch on the
  correct line: middle line for alto, fourth-from-bottom for tenor.
- **Fixed tenor pitch reference**: topStep was 31, placing middle C one line above
  the notch; corrected to 30 so C4 sits on the notch line as a tenor clef
  requires. Alto was already correct at 32.
- Verified: 336 renders across all four clefs, zero tofu fallbacks (no <text>
  clefs remain), zero clipped, zero wrong notehead counts.

## v0.99.25 — Light-mode key colour and tone popup skin

Two leftover colour mismatches, both hardcoded salmon that ignored the module's
green accent.

- **Selected note keys turned salmon** in the builder (and the player root grid's
  glow). Four rules hardcoded rgba(255,160,122,...) for the active fill, border
  and shadow. All now route through `color-mix(... var(--accent-warm) ...)`, so
  they follow the module's green in both themes.
- **The VOICE tone popup wore the piano's cream/brown card.** The chord scope
  (`.chd-tonepop`) recoloured the tiles and group labels but never the card
  itself, so the surface stayed cream in light and brown in dark. Added card,
  border and header overrides to the chord scope for both themes: deep green card
  in dark, pale green in light.
- Verified: selected keys render green (rgb 47,112,72) with zero salmon in both
  themes; popup tiles and card both green via the real button flow; 126 staff
  renders across two spelling modes with zero wrong notehead counts.

## v0.99.24 — AUTO cue is now ♯♭, not ♮

The natural sign was misleading: ♮ is itself a spelling instruction ("cancel the
accidental on this note"), so next to ♯ and ♭ it read as a fourth forcing option
rather than "let the app choose".

- **AUTO cell now shows a small combined ♯♭ mark** — reads as "either / let it
  decide", in the same accidental family as the two single-glyph cells without
  claiming to be an instruction. Glyph set at 11px to match the ♯/♭ cells (an
  earlier over-condensed 9px pass rendered it 5px wide, a smudge).
- Behaviour unchanged: ♯♭ is smart per-chord spelling (D♯ major → E♭), ♯ and ♭
  force one throughout. Both cards synced, all three cells select.
- Verified: 189 renders across three modes, zero clipped, zero wrong notehead
  counts; header height unchanged at 24px.

## v0.99.23 — Spelling switch aligned and re-cued

- **Removed the decorative dash** left of the switch. Every `.card-label` carries
  a 14px line via `::before`; on the chord picker headers it pushed the switch
  22px off the note grid's left edge. Suppressed on these headers only, so the
  switch now sits flush and lines up with the C key directly beneath it (x=36 vs
  x=37). Other cards keep their dash.
- **AUTO cue changed from "A" to ♮.** The natural sign reads as the musical
  counterpart to ♯ and ♭ — three accidental glyphs as one set — rather than a
  lone letter. Behaviour is unchanged: ♮ still means smart per-chord spelling
  (D♯ major → E♭), ♯ and ♭ force one throughout.
- Verified: 756 renders across four clefs and three spelling modes, zero clipped,
  zero wrong notehead counts; card height unchanged at 355px.

## v0.99.22 — Spelling switch polished down to header weight

The previous "slim" pass made the switch shorter in width but 36px tall — 14px
taller than the CLR button beside it, so it read as a chunky widget bolted onto
the header. Fixed by matching it to the row it lives in.

- **Switch height 36px → 24px**, level with the undo/clear buttons; vertical
  centres now align across the whole header row.
- **Restyled as a quiet segmented track**: a hairline-gap track with the active
  cell marked by a soft accent fill rather than a full outline, so it reads as a
  setting rather than a control competing with the note buttons. Active-cell
  cascade fixed (the light-mode base fill had been overriding it).
- Undo and clear given matching height, flex-centred glyphs and a subtle
  transition so the row is consistent end to end.
- Verified: 504 renders across four clefs and two spelling modes, zero clipped,
  zero wrong notehead counts; card heights unchanged (355px player, 343px
  builder); every cell selects correctly in both themes.

## v0.99.21 — Slimmer spelling switch, left-aligned

The Builder header was carrying switch, label, undo and clear across 289px of a
316px row, so the label wrapped to two lines and the row felt cramped.

- **Switch moved to the left** of both picker card headers, ahead of the label,
  with undo/clear still right on the Builder.
- **Slimmed from 101px to 80px**: "AUTO" spelled out was 43px on its own, so it is
  now a single "A" with the full meaning in the title attribute, and all three
  cells are an equal 30px wide.
- **Header label shortened** from "Tap notes to build" to "Notes" ("Note" in
  Italian) — the readout above already says TAP NOTES BELOW and the grid is
  directly beneath, so nothing is lost. The label is also allowed to shrink and
  ellipsis rather than wrap the row.
- Both headers now sit on a single 36px line with 30–38px of slack. Tap targets
  are 30×34px.
- Card heights unchanged at 355px player, 343px builder; 252 renders across three
  spelling modes with zero clipped and zero wrong notehead counts.

## v0.99.20 — Spelling switch on the picker cards

- **Moved the AUTO/♯/♭ switch off the readout and onto the cards where notes are
  chosen**: the Root picker in Player, and the note grid header in Builder beside
  undo and clear. Spelling is a property of the input, so the control belongs with
  it; the ledger card goes back to being purely a readout.
- This removes the flex-line contention introduced in v0.99.18 — the chord name no
  longer shares a row with anything, so the auto-fit measures its own box again
  and the header plumbing added to work around it is gone.
- Idle text ("TAP NOTES BELOW") restored to 20px; it had been dropped to 15px to
  survive beside the switch.
- Card heights back to 355px player and 348px→343px builder, recovering the row
  the switch had been occupying.
- Verified: 756 renders across four clefs and three spelling modes, zero clipped,
  zero wrong notehead counts; 200 random builder names, zero clipped.

## v0.99.19 — Name fitting fixed after the switch moved

Both faults traced to the same change: putting the spelling switch on the same
flex line as the chord name.

- **Auto-fit measured the wrong width.** `chdFitName` sized the text against the
  header's inner width, which now includes the switch and the gap, so it thought
  there was ~115px more room than there was. A single calculated pass could not
  converge either — changing the font size changes the width flex hands back, so
  the arithmetic is always one layout behind. It now shrinks in steps and
  re-measures `scrollWidth` vs `clientWidth` until the text genuinely fits.
  Verified: 0 clipped across 250 random chords, sizes 15–36px.
- **Idle labels styled separately.** "TAP NOTES BELOW" is an instruction, not a
  chord symbol, and shrinking 36px type until it fit beside the switch left it
  unreadable. Idle text is now set at 15px and allowed to wrap.
- **The switch could collapse to zero width.** `flex:0 0 auto` on the container
  was not enough because its buttons were themselves shrinkable; the buttons are
  now `flex:0 0 auto` too and the container is `width:max-content`.
- Card heights unchanged: 360px player, 348px builder.

## v0.99.18 — One spelling control, on both cards

- **The hidden per-root flip is gone.** Double-tapping a selected accidental root
  did the same job as the AUTO/♯/♭ switch, so a tap could silently contradict the
  mode the switch was showing. One visible control now owns the decision.
- **The switch moved to the ledger card header** and appears on Player *and*
  Builder — Builder previously had no spelling control at all, which was an
  inconsistency. Both instances stay in sync and write the same setting.
- **AUTO kept.** Measured across the common chord set it yields 3 double
  accidentals (all genuinely correct spellings, e.g. Cdim7's B♭♭) against 35 for
  forced sharps and 21 for forced flats. Removing it would leave new users in a
  mode that writes D♯ major as D♯–F𝄪–A♯.
- Switch shares a line with the chord name rather than taking a row of its own: a
  full row cost 41px of card height for a control most people set once, and the
  name already auto-fits so it simply shrinks around it. Card heights remain
  single values (360px player, 348px builder).

## v0.99.17 — Spelling switch on the Root card

- **AUTO / ♯ / ♭ toggle** added to the Root picker header. AUTO keeps the
  per-chord behaviour from v0.99.16 — each root and quality spells whichever way
  avoids double accidentals, so D♯ major presents as E♭–G–B♭. The two accidental
  buttons force sharps or flats across the entire tool for anyone who wants one
  fixed spelling; the root grid, chord name, note pills, notation and the Builder
  all follow. Choice persists in `progState.chordSpelling`.
- Per-root flipping (tap a selected accidental root again) still works. Doing so
  while a forced mode is active returns the tool to AUTO, so one deliberate flip
  is not immediately recalculated away.
- Measured across the common chord set: AUTO produces 3 double accidentals (all
  genuinely correct spellings such as Cdim7's B♭♭), forced sharp 35, forced flat
  21. The forced counts are the honest consequence of the choice.
- Toggle tap targets are 49×32px; card heights unchanged at 355px player and
  343px builder across all three modes.

## v0.99.16 — Chords audit: enharmonics and a dead control

Full functional scan of the tool. Every id present, every onclick handler
defined, every i18n key resolving, no console errors. Two real faults found.

- **Quality group headers did nothing.** `buildChordQualityGroups()` re-expanded
  whichever group held the active quality, and it ran on every rebuild — including
  the rebuild a header tap triggers. Collapsing the group you were using
  immediately reopened it. Auto-expand is now opt-in (`buildChordQualityGroups(true)`),
  used when the tool opens; header taps and quality picks pass `false`.
- **Enharmonic spelling was naive.** Black-key roots always spelled sharp, so
  D♯ major came out D♯–F𝄪–A♯ (correct arithmetic, notation nobody writes) instead
  of E♭–G–B♭. Each root+quality now defaults to whichever spelling produces fewer
  double accidentals: 7 unreadable chords in the common set down to 0. The six
  remaining double-accidental chords app-wide (Cdim7's B𝄫, Baug's F𝄪) are the
  genuinely correct spellings and are left alone.
- **The enharmonic toggle was undiscoverable.** Re-tapping a selected accidental
  root flips its spelling, with no cue that this was possible. Selected sharp/flat
  roots now carry a small ⇄ mark and a tooltip naming the alternative, and the
  player hint says so in both languages. A manual flip is remembered per root and
  overrides the automatic default from then on.

## v0.99.15 — Notation restored

Fixes a regression introduced with the stable-height work in v0.99.14.

- **The staff drew nothing but its clef.** The octave-placement search was seeded
  with `{cost:0, steps:[]}` as a guard for empty chords, but a real octave choice
  can legitimately score 0, and `cost < best.cost` then never beat the seed — so
  every chord kept the empty steps array. Seeded with `null` instead.
- **Sets without a dictionary entry now get notation too.** Approximate and
  universal names (anything the added-tone describer or `chdNameAnySet` handled)
  had no `def` to render from, so the staff stayed blank for roughly half of all
  tapped combinations. `renderChordStaff` accepts a raw pitch-class list and
  voices it upward from C4, so every named set has a staff. The formula row falls
  back to intervals from the bass in the same case.
- **Staff wrapper de-flexed.** An SVG carrying explicit width/height attributes
  as a flex child is sized by flex rules rather than its own box in some
  WebViews, which can collapse it. The wrapper is a block with the SVG absolutely
  centred, so the element's own dimensions stay authoritative.
- Card heights remain single values: 355px player, 343px builder.

## v0.99.14 — Chords card holds still

- **No more layout shift.** The card resized as you picked chords or tapped
  notes (player 347-373px, builder 264-346px), pushing everything below it
  around. Every variable row now reserves its space: note pills and alternates
  sit on one horizontally-scrolling line, the inversion stepper is a fixed
  six-cell grid with invisible placeholders past the chord's length, the staff
  scales inside a constant 96px frame, and the chord name shrinks inside a fixed
  40px box rather than the box following the font size. The builder's empty state
  keeps its rows occupied so the first tap does not grow the card. Measured: one
  single height in both modes (player 355px across 219 chord/inversion states,
  builder 343px across 151 random note sets), in both themes.
- **Undo and clear moved to the note grid** they act on, as small inline buttons
  on the grid's header rather than sitting in the transport row beside PLAY. They
  stay visible rather than hiding behind a gesture, and dim when there is nothing
  to undo. Transport is now just PLAY and ARP.

## v0.99.13 — Chords tool: staff restored, green accent, auto-fit name

- **The staff disappearing on device.** The SVG carried no width/height
  attributes and relied on `width:100%; height:auto`, which needs the intrinsic
  ratio derived from the viewBox; some WebViews resolve that to zero height, so
  the staff rendered but occupied no space. Width and height are now set
  explicitly and kept in step when the fitter rewrites the viewBox, with a
  min-height on the wrapper as a floor.
- **Orange in light mode.** `--accent-warm` is a salmon (#ffa07a) with no
  light-mode override, so the PLAY button, chord name, chip highlights and the
  selector card's rim all came through orange on a green card. A green accent is
  now scoped to `#toolChords` in both themes (#8fd694 dark, #2f7048 light) and
  every rule referencing the token follows; no other module is affected.
- **Chord name auto-fits.** Universal naming can produce very long symbols, so
  the name shrinks to fit its card (36px down to a 13px floor). Sized by
  font-size rather than transform, since a transform leaves the layout box at
  full width and the name still overflows. Measured out of normal flow, because
  in flow the parent caps the reading and the fit never triggers.
- **FORMULA and WRITTEN swapped**, so the formula sits directly under the notes
  and notation closes the card.
- **Row labels un-indented** by 6px (34px to 28px) with the arrows unmoved.

## v0.99.12 — Every note combination is a chord

- **100% naming coverage.** New `chdNameAnySet()` names any pitch-class set at
  all: it picks the root that yields the cleanest reading, takes whatever triad
  or seventh core is present, and spells every remaining note as a parenthesised
  tension, the way a jazz chart would. Tested across all 1023 sets from a fixed
  root (sizes 1–5): 167 named from the dictionary, 480 by the added-tone
  describer, 376 by the universal namer, **zero unnamed**. C·D♭·D now reads
  Csus2(♭9) rather than UNKNOWN.
- **Clef unboxed.** The frame around the clef read as a widget bolted to the
  stave. The clef now sits on the staff as it would in a score, with a small
  caret beneath marking it as tappable; the hit area stays generous via an
  invisible rect.
- **Row labels aligned.** Foldable and fixed rows now share one padding value, so
  every label starts at the same x (measured 34px on all four) while the arrows
  stay out in the gutter.
- **Tone popup themed.** The shared picker is skinned for the piano console
  (near-black) and the riff surfaces' cream in light mode. Opening it from Chords
  now tags it so it wears this module's greens in both themes; other surfaces are
  untouched.

## v0.99.11 — Chords tool: real glyphs and layout pass

- **Notation now uses the app's own Bravura outlines.** Noteheads are
  `RR_NH_WHOLE` and accidentals are `RR_SHARP` / `RR_FLAT` — the same paths
  Rhythm Reading draws — instead of hand-rolled ellipses and font characters, so
  notation matches everywhere and needs no musical font on the device. Treble and
  bass clefs use `RR_TREBLE` / `RR_BASS`, resolved lazily since those constants
  live in a later script block. Alto and tenor have no extracted outline yet and
  still fall back to the font glyph.
- **Clef centred in its button.** Horizontal centring now uses each path's
  measured bounding box (treble 24.16×63.22, bass 24.8×32.29) and a fit scale, so
  it is exact rather than a guessed width; verified at 0.00px offset on all four
  clefs. Vertical position stays anchored to the line the clef names, as it must.
- **Fold arrows no longer shift their labels.** The arrow is absolutely
  positioned in the label gutter, so foldable and fixed rows put their text at
  the same x. All four row labels measure 25px.
- **Voice picker moved into the action row** beside PLAY/ARP, removing a whole
  labelled block of vertical space, and themed to the module — it was inheriting
  the piano overlay's near-black on a mint card.
- **Layout rhythm** evened out: consistent 10px between the card, actions and
  selector panels.
- **Builder copy fixed** — said "TAP NOTES ABOVE" while the grid sits below it.
  Now "TAP NOTES BELOW" / "TOCCA LE NOTE SOTTO".

## v0.99.10 — Chords tool: on-device fixes

Follow-up to v0.99.9 from device screenshots.

- **Clef could render enormous.** `_chdAlignClef` measures the drawn glyph and
  scales it, but silently returned if `getBBox()` was unavailable, leaving the
  provisional size on screen — which was deliberately oversized. The provisional
  size is now conservative (fail small, not large) and a hard ceiling caps the
  font size regardless of whether measurement succeeded.
- **Light mode.** Light mode restyles `.card` explicitly rather than only
  swapping variables, so the new `.chd-card` picked up dark-token values and
  rendered blue-grey on the mint page. Card, row rules, label gutter and clef
  frame now have explicit light treatments; staff ink deepened to `#2f4a17`.
- **Naming coverage 24% → 72%.** Most tapped sets are not in any dictionary. New
  `chdDescribeSet()` finds the best known chord inside the set and names the
  remainder as an added interval, so C·D·A·B reads Bm7(no5)(♭9)/C instead of
  UNKNOWN. Truly arbitrary clusters still fall back to the interval stack.
- **Accidentals** now centre on their notehead via `dominant-baseline` instead of
  a guessed baseline nudge that made flats ride low.
- **Noteheads** thinner and more tilted (1.9 stroke, −16°) so whole notes read as
  ovals rather than blobs at phone size.
- **Tone bank** replaced with the app's current grouped tone picker (one compact
  voice button opening the family popup), matching the interval and piano
  surfaces; the old horizontal chip strip is gone. Picking a voice refreshes both
  Chords buttons.
- **Removed the duplicate volume sliders** from both panels.

## v0.99.9 — Chords tool rebuilt as the ledger card

**Chords (Player + Builder).** Both modes now share one result-first card:
chord name on top, then labelled rows for NOTES, WRITTEN, FORMULA and ALSO.
WRITTEN and ALSO fold via the arrow next to the row name.

- **Notation row.** Reference chords drawn as whole notes (no stems) on a staff
  rendered in the app's own colours, light mode included. The clef printed at
  the staff head is the control: tap it for a treble/bass/alto/tenor picker.
  Clef choice persists app-wide in `progState.chordClef`. Clef glyphs are
  anchored musically and aligned against the measured ink after render, so they
  land correctly in whatever font the device supplies.
- **One speller everywhere.** Pills, chord name and staff all spell through
  `getSpelledNotes`, so Cm7 reads C·E♭·G·B♭ in every row at once.
- **Inversions (Player).** Stepper under the note pills: name becomes Cm7/G,
  pills rotate with the bass highlighted, staff re-voices, and PLAY voices the
  inversion (rotated-out tones move up an octave).
- **Tappable alternates (Builder).** ALSO lists every valid reading of the
  tapped notes; choosing one re-roots the entire card — name, pills, spelling,
  staff, formula.
- **19 new chord types.** 6/9, m6/9, madd9, 9sus4, 7sus2, 13, maj13, m13,
  shell voicings 7(no5)/m7(no5)/maj7(no5), the Lydian Mb5 triad, and dyad
  entries for every interval (m3, M3, P4, m6, M6, m7, M7) so two taps always
  get a root-position name. Pickable qualities joined their groups; shells and
  dyads are Builder-only (rank 4).
- **Builder volume slider added** (was Player-only); the two sliders stay in
  sync and share the percentage readout.
- Old `.chord-display` CSS left in place, now unused; strip in a later cleanup
  pass rather than risking a large deletion inside this feature build.
 and to what specific value. This
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
