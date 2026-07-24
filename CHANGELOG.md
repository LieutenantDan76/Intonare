# Intonare — Changelog

A human-readable record of what changed, when,

---

## OPEN ITEMS — groove audit (as of v0.102.24)

Not a release entry. A standing list so these survive outside anyone's memory.

**Two decisions waiting on Daniele**

1. `intonare_groove_audit.py` needs copying into `/mnt/project/`. It ships to
   outputs on every build but does not persist, and it already had to be rebuilt
   from scratch once for exactly this reason.
2. Undecided: whether groove patterns should join the regression sentinel's pin
   list. Bulería had been correct in this file once and was silently changed back;
   the audit caught it, but only because someone happened to be looking. Pinning
   the Toussaint six, maqsum and the flamenco pair would make that class of
   regression impossible rather than merely detectable.

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
