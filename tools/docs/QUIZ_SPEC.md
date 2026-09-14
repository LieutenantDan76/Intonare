# Intonare quiz: the working specification

> **STOP. Open `QUIZ_VOICE.md` and read the twelve questions in it before
> writing a single stem.** That file holds the approved artifact; this one holds
> the reasons. Reading the reasons instead of the artifact is how the style gets
> rebuilt from a description every session and drifts toward the spec sheet every
> time. It is twelve questions and takes a minute.


Everything needed to take a pack from where it is to finished, without asking
again. Written after seven packs of trial and error; every rule here exists
because something went wrong without it.

**The goal, as of the restart in v0.150.164.** Four packs for 1.0 at about 60
questions each, written fresh. The rest ship as free content after launch. Every
question correct, answerable, fairly built, difficulty-tagged, and bilingual from
birth.

**The 1.0 four:** theory_fundamentals, guitar_gods, eighties, and one more
instrument pack. Theory goes first because it is also the proving ground for the
generated question types in section 11.

Everything written before v0.150.164 is locked behind COMING SOON and is a TOPIC
AND FACT SOURCE, not a set of drafts.

**Standing instructions, agreed with Daniele:**

- **Err toward searching on anything new.** A search now is cheaper than a second
  pass later. This applies to decade facts as much as music ones: launch years,
  first broadcasts, who was in what.
- **Order of work: depth first, then breadth.** One pack goes all the way to
  finished, Daniele judges it, and only then does the same treatment scale to the
  other three. Writing a pack before anyone has seen the shape is the one mistake
  that would cost a full repass, and it has already happened once.
- **Time is not the constraint, repassing is.** Move deliberately. This is a
  quality gate for 1.0, not a race to a number.
- **Italian needs a native check before scale.** Nobody has reviewed the Italian
  in this app. Linda should spot-check the first finished pack before the rest
  are written in it.

**Current position** lives in section 9 and is regenerated from the file, not
kept by hand, because the hand-kept version went stale within two sessions. Run
`intonare_quiz_progress.py` rather than trusting any number typed elsewhere in
this document.

---

---

## Before anything else: the working setup

Not obvious from anywhere else in this document, and every tool assumes it.

**The app is one file.** `Intonare.html`, about 10MB and 124,000 lines. All the
quiz data lives inside it in a `PACKS` object. There is no separate content file
and no build step for the data.

**Copy it to `/home/claude/Intonare.html` before doing anything.** Every script
here hardcodes that path. They now exit with a readable message when it is
missing rather than a traceback, but they will not find it anywhere else.

**Ship it back as plain `Intonare.html`** into the outputs directory. Never
version-suffix the filename: the Windows build script depends on the plain name.

**Version bump is three places** and the changelog gate checks all three: the
HTML comment at the top, the `<span>` in the settings UI, and
`const INTONARE_VERSION`.

**The app-level gates are separate from the quiz tools** and live in the project
as `intonare_*.py`. The ones that must pass on every ship:
`intonare_regression_sentinel.py` (97 tracked fixes and 247 pinned fragments; any
lower number means a stale file), `intonare_backup_audit.py`,
`intonare_stopall_audit.py` and `intonare_changelog_gate.py`. `AUDIT_INVENTORY.md`
lists the rest.

**Smoke test every build** by loading the file in a headless browser, opening the
quiz, and checking the console is clean in both languages. A syntax check alone
will not catch a broken question object.

---

## This document replaces QUIZ_PLAN.md

`QUIZ_PLAN.md` (July 2026) is superseded and should be deleted from the project.
It reached most of the same conclusions by measuring the question bank; this one
reaches them by playing it. Everything it had that this does not is salvaged into
section 11, including the audio question formats and the sourcing options already
rejected.

Keeping both would mean a future session reading two overlapping specs and
working out which wins. There is one.

---

## Where to start reading

If you are picking this up cold, read in this order and skip nothing:

0. **Section 12 FIRST.** It is the restart decision and it overrides anything
   earlier in this document that describes reviewing existing questions or a
   target of 100 a pack. Where section 12 disagrees with an earlier section,
   section 12 wins.
1. **Section 2** for what easy, medium and hard actually mean. This is the thing
   that was wrong for longest.
2. **Section 2b** for the craft of a question. Reread it before writing anything.
3. **Section 3b and 3c** for the two failure modes that no tool detects.
4. **Section 5** for the sequence to work a pack.
5. **Section 7a** before touching the file, or you will lose edits to the same
   traps everyone else did.
6. **Section 11** for the audio question formats, which are the best unbuilt idea
   here, and for the sourcing routes already ruled out.

Sections 8a and 8b are reference: how the difficulty code works, and every wrong
fact found so far with its correction. 8b in particular took hours to establish
and would be expensive to rediscover.

---

## 1. Definition of done, per pack

A pack is finished when ALL of these are true. Not most.

- [ ] Every question read in full: stem, all four options, and the blurb
- [ ] Every factual claim correct, and anything that is a date, name, first,
      number or quantity checked against a source
- [ ] Exactly one defensible answer per question
- [ ] No answer identifiable from the SHAPE of the options, as opposed to from
      knowing or reasoning about the subject
- [ ] All four options plausible to someone learning the topic
- [ ] Every blurb true, and adding something the question did not
- [ ] No AI cadence
- [ ] No duplicates inside the pack
- [ ] Every question tagged `d:1`, `d:2` or `d:3`
- [ ] About 60 questions, split roughly 40 percent easy, 40 medium, 20 hard
- [ ] Both languages present and saying the same thing
- [ ] All gates green, quiz loads with no console errors

Then and only then update the progress table at the bottom.

---

## 2. Difficulty, with the standard that matters

Daniele's test, quoted because it is the clearest statement of it:

> easy should be mostly softball, medium stuff that a hobbyist would know, then
> hard for the niche. It should be closer to "who's the guitarist in AC/DC" or
> "Who played the song Purple Haze?"

### d:1 — easy

**Someone who listens to music but has never picked up an instrument gets this.**
No technical vocabulary. No dates. No gear. The test: would a person who likes
music but has never played know this from hearing songs and reading sleeves?

Good: Angus Young plays an SG. Van Halen played the Beat It solo. Clapton is
Slowhand. B.B. King's guitar is Lucille. Hendrix played right-handed guitars
upside down.

**Not easy, even though it feels basic to a player:** what a capo does, what a
power chord is, what palm muting is. Those are d:2. A non-player has never heard
of any of them.

### d:2 — medium

**A hobbyist who has spent a year with the instrument knows this.** Technique
names, common gear, the famous stories, basic theory.

Tapping, sweep picking, CAGED, open G, Floyd Rose, harmonics, the Telecaster
twang, what a compressor does, what a mode is.

### d:3 — hard

**Niche.** Specific sessions, gauges, materials, dates, deep cuts, theory past
the basics.

SRV's .013 gauge, the Coricidin bottle, Frippertronics, compound radius,
Metheny's GR-300, the Nashville Number System, hemiola, the Neapolitan sixth.

### The tagging rule, for every pack

Guitar Gods was tagged first and Daniele's verdict was "these all still feel like
mediums to me". He was right, and the reason generalises to all nineteen packs.

The instinct is to tag as easy anything a PLAYER finds obvious, and a player is
not the audience for the easy tier. What a capo does, what a power chord is, what
palm muting is: all trivial to anyone who plays, all d:2, because someone who has
never held a guitar has not met any of them.

**When torn between 1 and 2, choose 2. Every pack, every time.** The easy tier
gets filled by WRITING new softballs, not by demoting mediums into it. A d:1
question that turns out to be a d:2 makes the easy tier feel like a test; a d:2
question left where it belongs costs nothing, because the blend pulls 25 percent
of medium into easy anyway.


---

## 2a. Conventions borrowed from people who write quizzes for a living

Researched rather than invented. Where the sources agree, it is worth following.

**The 40/40/20 split is the industry standard.** Daniele picked it independently
and the quiz-writing sources land on the same numbers. Some prefer 30/50/20. The
principle behind both: easy questions build confidence, medium ones carry the
round, hard ones separate the top.

**Hard means most people miss it.** One guide puts it plainly: expect only one or
two teams to get a hard question. That reframes d:3. It is not "an obscure fact",
it is "a question most players will not get, and that is the design". A hard tier
where everyone scores is not hard.

**Open easy, close soft.** The round has a shape and it is not a random bag.
First two gettable by anyone, difficulty climbing to roughly four fifths through,
then the LAST question steps back down. Ending on the hardest question is the
natural instinct and it sends the player away having just failed. Implemented in
`mqShapeRound` in v0.150.149.

**Weak distractors are the most common mistake.** "Resist the urge to throw in
funny or obviously wrong answers. These weak distractors do little to challenge."
Every pack reviewed so far had them, usually as "A minor period" or "They were
all the same".

**Vary the question TYPE, not just the subject.** Straight recall is the default
and gets monotonous:

- Who did X? (recall)
- Which of these is a real X? (recognition, and forgiving)
- What did X actually do? (function, no date needed)
- Why was X unusual? (invites reasoning)
- Which came first? (ordering, guessable from feel)
- True or false, properly framed as four options

**Questions should start a conversation.** The sources keep returning to this:
a good question makes people talk, not just answer. "What was a mixtape" is
better than "in what year did the compact cassette appear", because everyone who
made one has a story.

**Fun first, educational second.** Daniele's framing, and it matches the sources.
The blurb is where the teaching happens. The question's job is to be worth
answering. A quiz of correct facts nobody knows is a test, and nobody plays a
test for pleasure.


---

## 2b. The craft of the question itself

From people who write trivia weekly. This is the section to reread before writing
anything.

### The line that matters most

> "It's easy to write bad hard questions, but hard to write good easy ones."
> — Toronto Trivia League, via Trivia Hall of Fame

That is the whole problem with our easy tier in one sentence. Anyone can find an
obscure fact. Writing a question that is easy AND worth answering is the skill.

### The three-reaction test

Every question should land as one of these, and nothing else:

1. **"I know this!"**
2. **"I used to know this. Let me think."**
3. **"No idea, but I reckon I can work it out."**

A question that produces "no idea, and no way in" has failed regardless of how
correct it is. **The best trivia does not punish you for not knowing** — it gives
you something to take a swing at.

### Distractors: the difficulty lives here, not in the answer

> "In a multiple choice question, the difficulty does not live in the correct
> answer. It lives in the other three. Three obviously wrong options turn a hard
> question into a free point."

**The rule that makes this concrete: wrong answers should be true about something
adjacent.** If the question is which planet has the most moons, the wrong answers
are planets that also have a lot of moons, not Mercury. If it is about the first
woman to win a Nobel Prize, the wrong answers are other women who won Nobel
Prizes.

Applied here: a question about which guitar Angus Young plays should offer other
Gibsons, not a ukulele. A question about a 1985 film should offer other 1985
films.

Also:
- The key should match the distractors in tone, length and style. If it stands
  out in ANY of those, the question is answerable without knowledge.
- Options must be mutually exclusive. If one distractor being true would make
  another true, the question is broken.
- No "all of the above" or "none of the above".
- No always, never, all, none. Players dismiss them on sight.
- Joke distractors reduce four options to two or three. Fine in a party game;
  they weaken this.

### Wording

**Read it aloud. If you stumble, the player will too.** Trivia rewards rhythm.
Short punchy phrasing pulls people through; dense sentences lose them.

**Front-load the subject, put context after the ask.** If the reader only knows
what is being asked in the last five words, the setup was too long.

**Put the wording in the stem, not repeated across the options.** Four options
each restating the same clause is a wall of text with a needle in it.

**Never phrase it negatively.** Instead of "which of these is NOT a primary
colour", ask which one IS. Negatives get misread and the question fails for a
reason that has nothing to do with knowledge.

**One ask per question.** Compound questions muddy the answer and the scoring.

### The Nintendo example, worth copying

Bad: "Nintendo translates loosely to what phrase in English?"
Good: "'Leave luck to the heavens' is a loose translation of the name of what
company that made playing cards before it made video games?"

The first has several defensible translations and no way in for someone who does
not already know. The second has exactly one answer, rewards the person who knows
the fact, and still lets someone reason their way there from playing cards.

**Rewrite in this direction whenever a question is unguessable.** Move the
obscure part into the stem as a CLUE and ask for the thing people can reach.

### Fun

> "A really great question is kind of funny too."

Surprise is the engine. The best questions leave the player thinking "that is
really interesting", which is also what makes them repeat it to somebody else.
Prefer facts that are counterintuitive, or that connect to something the player
already cares about, over facts that are merely true.

### Sourcing

Professional writers fact-check against three sources and do not count Wikipedia
as one of them. That is stricter than we need for a music app, but the principle
holds: one source is not verification, and a claim repeated everywhere can still
be wrong. The Lemmy umlaut, the Funk Brothers count and the Sam Phillips quote
were all universally repeated and all wrong.

---

## 3. Writing new questions

About 240 to write for the 1.0 four, most of them easy. Everything already in the
file is a topic and fact source rather than a draft; see section 12.

### Where easy questions come from

The reliable well is **famous songs, famous bands, famous people, and the
instrument itself**:

- Who played / sang / wrote X?
- Which band was X in?
- What instrument does X play?
- What is this part of the instrument called?
- Which of these is a real X?

Avoid, in the easy tier: years, chart positions, producer credits, studio names,
technique vocabulary, gear model numbers.

### Question construction rules

**The stem asks one thing.** "What is X and who invented it?" is two questions.
It is acceptable when both halves have the same answer; it is not acceptable as a
way of padding.

**Four options of comparable length.** Measured after any trimming. The single
most common fault in this quiz was a full-sentence answer standing against three
short dismissals.

**Every distractor is something a learner might believe.** "A minor period",
"They were all the same", "Only a modest success" are not choices, they are
scenery. If a distractor could not fool anybody, it is wasting one of four slots.

**Educated guessing is allowed and wanted.** A player who reasons "AC/DC look
like a Gibson band, and the SG is the Gibson on that list" has PLAYED the
question. That is the pleasure of trivia and it must survive. What has to go is
the guess that needs no thought about the subject at all: the longest option, the
one with an ellipsis, the only one without an absolute, the only one that agrees
grammatically. Those reward test-taking rather than interest.

The distinction in one line: **narrowing four options to two by thinking about
music is good. Picking the right one by looking at the shape of the text is
not.**

**No detail after an em-dash in an option.** It gets trimmed, the trim leaves an
ellipsis, and the ellipsis marks the answer. 276 questions had exactly this fault.
Put the detail in the blurb.

**No absolutes in the distractors unless the answer has one too.** Three options
saying only, never or all, with a plain answer, hands the question to anyone who
has taken a test before.

**No hedge on the answer alone.** "Usually", "typically", "most" on the correct
option and nowhere else is the same tell in a quieter voice.

### Blurb rules

**Complete sentences that run on, not fragments and not two balanced clauses.**

This rule was wrong once already and the correction matters. The first version
said fragments, because the failure looked like prose. It was not. Daniele
rewrote five samples and the difference was the opposite of what I had assumed:
his are LONGER, they flow, and they end warm.

    my fragment    Built it with his dad, aged 16. Neck from an 18th-century
                   fireplace mantel, body from an old oak table. Wormholes
                   filled with matchsticks. Still plays it.

    his version    Brian built it with his dad at the age of 16, making the neck
                   from an 18th-century fireplace mantle and the body from an
                   old oak table, filling the wormholes with matchsticks. He
                   still plays it to this day!

Same facts. The fragments are clipped and a bit cold; his carries you through on
participles and lands somewhere.

**What his five actually do:**

- **Name the subject first.** "Brian built it", "Bass strings sound", "The
  Walkman, built in 1979". Not a pronoun, not a clause first.
- **One long sentence carrying several facts**, joined with commas and
  present participles: making, filling, playing, allowing.
- **A short warm close, often exclaimed.** "He still plays it to this day!"
  Three of his five end on one. I had banned that as a flourish. It is not a
  flourish, it is the voice.
- **Explain the consequence, not just the fact.** "making the fretboards almost
  identical to navigate" is why the tuning matters. The fact alone would not
  have said it.
- **Attribute a disputed claim inside the sentence**, not as a caveat bolted
  after it: "according to the Washington Post".

**The actual failure was never sentence completeness.** It was TWO SENTENCES OF
NEARLY EQUAL LENGTH, over and over: state the fact, add the colour. That shape
had a sentence-length SD of 3.0 across 100 blurbs. Daniele's have one long
sentence and one short one, which is a completely different rhythm and reads as
somebody talking.

**Rules that follow:**

- Never two sentences of similar length. One long and one short, or one long
  alone.
- Open with the subject named, never with He, She, It or They.
- A warm closing line is welcome. An empty one is not: "He still plays it to
  this day!" earns its place; "and the rest is history" does not.
- Say why the fact matters where there is a reason to.
- Source it rather than composing around it, and put the attribution inside the
  sentence.
- Length follows content, but err longer than a fragment.

### Daniele's second set, the Bass pack, August 2026

Eight more rewrites in his hand, and they are more useful than the first five
because the drafts they corrected had already passed both audits. Three moves
account for all eight.

**1. Cut the closing sentence that carries a verdict rather than a fact.**

    draft   ...records from either side of that line sound so different.
            Anybody chasing a Motown thud still buys them.
    his     ...records from either side of that line sound so different.

    draft   ...meant to be a single support slot. They kept booking gigs anyway.
    his     ...meant to be a single support slot.

The cut sentences were true, were not on the EMPTY_CLOSERS list, and still had
to go. What they share is that each one comments on the fact just stated. A
blurb ends on information or it ends. `intonare_blurb_voice.py` now warns on
this as VERDICT_STRONG, though the list only catches the obvious ones.

**2. Fold a small related fact into the sentence instead of tacking it on.**

    draft   ...the bass sat out in front of the band rather than under it.
            The others called him Thunderfingers.
    his     ...the bass sat out in front of the band rather than under it,
            earning him his nickname, Thunderfingers.

A five-word sentence carrying one more fact belongs on the end of the sentence
before it, as a participle. This is the same move as the fireplace-mantle blurb
in the first set.

**3. Break a distinct second idea into its own sentence rather than hanging it
off an "and".**

    draft   ...aimed at players coming across from other instruments, and
            blending the two pickups gives you a bright bridge sound...
    his     ...aimed at players coming across from other instruments. Blending
            the two pickups gives you a bright bridge sound...

Moves 2 and 3 look contradictory and are not. A fact that MODIFIES the subject
of the sentence folds in; a fact that introduces a new subject gets its own
sentence.

**A machine check for move 3 was written and thrown away.** It fired on seven of
the forty-two approved blurbs including Daniele's own A7. The note is in the
tool. The rule is real and the detector is not.

**4. The closing sentence has to follow from the one before it.**

Found on the second read of the Bass pack, after every mechanical check passed.
All four of these are true, none is a verdict, and all four had to go:

    "Justice, the album made after he died, is the one with the bass mixed
     almost out of it."            (the blurb was about a different album)
    "Kumalo had learned on a bass strung with fishing line."
    "Leo Fender was involved, years after selling the company with his name on
     it."                          (flat, and connected to nothing above it)
    "Good Times has been built on ever since."

The test: does the last sentence answer something the one before it raised? If
it is simply the next true fact about the subject, it is a bolt-on, and the
blurb ends better without it or with the fact folded upward.

**This one cannot be automated and the attempt is recorded in the tool.** A
lexical-overlap check fired on 51 of 106 approved blurbs and caught one of the
four, because a deliberate turn ("He never slapped a note in his life") looks
identical to a bolt-on from the outside. Read the closers. All of them.

**And two smaller things from the same pass:**

- Plainer verbs, no editorializing. "the frets far enough apart to matter"
  became "the frets farther apart"; "aimed squarely at" became "made for";
  "losing the argument with two amplified guitars" became "losing the sound
  battle".
- Cut the qualifier that adds nothing: "crowding the strings and the singer
  above it" became "crowding the strings or the singer".

### The inverted stem, and what was pushing me into it

Found on the third read of the Bass pack. Five stems stated a fact and then hung
the question off the end:

    The Bass VI has six strings, tuned how?
    What flips on an Ampeg B-15 flip-top?
    ...is called what?      ...by doing what?      ...absence of what?

All grammatical. All passed every check. Nobody speaks like that. The 90 approved
Guitar Gods stems contain none of this shape, which is the measurement that
settled it. `intonare_pack_audit.py` now warns on it in both languages.

**Two things in this file were pushing me toward it, and both need saying out
loud so the next pass does not fall for them again.**

**The one-clause rule was over-applied.** Section 3c bans a setup sentence
followed by a question, and it is right to. But "one clause" is not what it says,
and enforcing it that hard produces stems with the verb at the end. The approved
pack runs a median of 11 words with a maximum of 23; the Bass stems came out at a
median of 11 and a maximum of 21, so length was never the problem. Word order
was. Ask forwards: "Why is the Ampeg B-15 called a flip-top?" is one clause and
it is a sentence a person would say.

**The answer-length check pushed the options into shorthand.** Trimming an
answer until it stops being findable by length is correct, and doing it by
hacking words off produces four clipped fragments. Lengthen the distractors
instead.

### The complete idea

A stem and its blurb have to add up to something whole. Three faults from the
same read:

- **The record went unnamed.** A question about Rocco Prestia's muted sixteenths
  that never says "What Is Hip?" leaves the player with a technique and no way to
  go and hear it.
- **The stem did the blurb's job.** "...gets two notes from one thumb by doing
  what?" hands over the interesting part in the question. The stem asks how the
  double thump works; the two-notes-from-one-thumb detail belongs in the blurb.
- **Two questions contradicted each other.** One asked who was selling an
  electric bass fifteen years before Fender, others treat the 1951 Precision as
  the start of the instrument. Both are true and together they read as a mistake,
  so the Tutmarc blurb now closes the loop: he sold about a hundred, the design
  went nowhere, and Fender got the credit fifteen years later with a factory
  behind him.

### Prose rules

**US spelling, everywhere, including comments.** There is an audit for it and it
had been reporting 99 hits, which is the wrong way round: the audit exists
because the spellings keep appearing. Color, center, practice, analyze, favorite,
labeled, traveled, gray. A comment written in British English is how the habit
spreads to the next thing somebody writes. `intonare_us_spelling_audit.py` in the
project checks it.

Two exceptions that are not English and must not be changed: CSS values like
`grayscale` and `text-align: center`, and any constant already named `GREY` in
the code.

Plain, literal, human. No marketing adjectives: iconic, legendary, revolutionary,
timeless, masterful, game-changing. No "not just X but Y". No hedging openers. No
rhetorical questions. Vary sentence length; do not stack same-length declaratives.


---

## 3a. The decades packs are general, not musical

**Changed in v0.150.147.** The six decade packs were music-only, which made them
a thinner copy of the genre packs. Live Aid appeared twice inside the eighties
pack and once more in rock_metal. They are now GENERAL decade packs: music stays,
but so does everything else people remember about living through it.

Daniele's framing: "my mom loves decades knowledge, so it'd be fun for 80s to
have shit about leg warmers, walkmen, and 90s to have Gameboys, hip hop and
Pokemon."

This solves the ceiling problem. A music-only decade pack runs out of fair
questions somewhere past sixty. A general one does not, and almost everything it
adds is naturally d:1, which is exactly the tier that needs filling.

### The wells to draw from

Every decade has all of these. Use them.

- **Music** as now, but no longer the whole pack
- **Television**: the shows everyone watched, catchphrases, the big finales
- **Film**: the blockbusters, the lines people quote
- **Fashion**: what people wore and later regretted
- **Technology and gadgets**: what was in the house and in your pocket
- **Toys and games**: what children wanted that year
- **Food and drink**: what was new, what was everywhere
- **Cars**: what was on the drive
- **News and events**: the moments people can place themselves in
- **Sport**: the tournaments and names that crossed over
- **Adverts and slogans**: often the most vivid memory of all

### Concrete anchors, as a starting point

| decade | anchors |
|---|---|
| 50s | rock and roll, drive-ins, tailfins, hula hoop, I Love Lucy, the first colour TV, Meccano, milk bars |
| 60s | the space race, Mini, miniskirt, Beatlemania, Thunderbirds, Twister, the first Bond films |
| 70s | flares, space hoppers, glam, the three-day week, Star Wars, Chopper bikes, Pong, Watergate |
| 80s | Walkman, leg warmers, shoulder pads, Rubik's Cube, Live Aid, ZX Spectrum, Ghostbusters, the Berlin Wall |
| 90s | Game Boy, Tamagotchi, Pokemon, Furby, Britpop vs grunge, Friends, dial-up, Jurassic Park, the Spice Girls |
| 00s | iPod, flip phones, low-rise jeans, MySpace, Harry Potter, the Wii, YouTube, Big Brother |

### A caution on where "everyone" lives

The app ships in English and Italian, and Daniele's own tester is Italian. A
question about a British children's TV show is not general knowledge in Milan and
a question about Sanremo is not general knowledge in Manchester.

Prefer anchors that crossed borders: the Walkman, Pokemon, Star Wars, the Rubik's
Cube, the moon landing, the Berlin Wall, the iPod. Where something is
country-specific and still worth asking, say so in the stem: "In Britain, what
was...". That keeps the question fair instead of quietly excluding half the
users.

### Overlap with the music packs

A decade question about music is fine. A decade question that duplicates one in
rock_metal or music_history is not, and the duplicate scan runs within a pack
only, so this one needs watching by eye. When in doubt the specialist pack keeps
the question and the decade pack asks something a non-player would know instead.


---

## 3b. Trivia, not a lesson

**The single most useful piece of feedback in this whole process**, from Daniele
after reading a sample:

> "The questions aren't bad necessarily, just wordy and kinda boring, and they
> all feel like they're trying to teach me something, not be a trivia game."

He was right, and it explains something the mechanical checks kept missing. Four
bass questions passed every automated test and I defended all four as already
good. Look at them together:

    What is 'playing in the pocket'?
    What is a 'walking bass line'?
    What is the role of the bass in a band context?
    What is the standard tuning of a four-string bass guitar?

**Every one is "What is X?"** That is a textbook question wearing a quiz costume:
a definition hidden among three wrong definitions. Correct, fair, balanced, and
a lesson rather than a game.

### The rule, corrected after getting it wrong once

The first attempt at this over-corrected badly and Daniele caught it. Forcing
every definition into an anecdote produced worse questions than the ones it
replaced: a stem that named "Motown bassist" when only one option was Motown, a
pointless "two instruments sit side by side" scenario, and a set of four options
that each varied two things at once, which is a logic puzzle rather than trivia.

**The fault was never that a question was definitional. It was that they were
WORDY, and that every single one was definitional.**

So the rule is two parts:

1. **Cut the throat-clearing.** "In which style would you expect to hear a
   walking bass line under almost every song" is "Walking bass is the signature
   sound of which style". Same question, six fewer words of nothing.
2. **Vary the framing across a pack.** A definition question is fine. Twenty of
   them in a row is a lesson. Mix in people, objects, numbers, and things that
   happened.

Where an anecdotal version exists naturally, prefer it. Where it does not, do not
manufacture one: ask the definition, briefly.

| instead of | ask |
|---|---|
| What is playing in the pocket? | Which Motown bassist is the usual example of it? |
| What is a walking bass line? | In which style would you hear one under every song? |
| What is the role of the bass? | A bass and a guitar side by side: what is the obvious difference? |
| What is the standard tuning? | A bass is tuned like which four guitar strings? |

Same facts. Same topics. The blurb still teaches. But the QUESTION is now
something a person could be asked in a pub.

### Why this changes the plan

The earlier conclusion was revise rather than rewrite, based on 85 percent of
questions passing the mechanical checks. That conclusion was wrong, because the
checks cannot see the fault Daniele can.

**The method is now: keep the TOPIC, recreate the QUESTION.** Work through a pack
using the existing questions as a topic list, not as drafts. A question that is
already anecdotal and lively survives as it stands. A question that opens "What
is" almost never does.

### The three-second test

Read the stem aloud. If it sounds like the opening of a lesson, recast it. If it
sounds like something one person would ask another across a table, keep it.

---

## 3c. Two failure modes found by showing samples

Both caught by Daniele reading questions I had just written, and neither is
visible to any tool.

**Comparative answers.** "How many strings does a bass have compared with a
guitar?" answered "Two fewer / Two more / The same number / One fewer" makes the
player hold two numbers before they can even read an option. Ask for the thing,
not the difference. If the answer is a comparison, the question is usually
pointing at the wrong fact.

**Two-sentence stems.** "A bass plays the same note names as a guitar's bottom
four strings. How much lower?" is a setup and then a question, and by the time
the ask arrives the player has forgotten the start. One sentence. If it needs
two, the second one is usually the whole question and the first belongs in the
blurb.

**And a warning against over-working.** The tuning question was fixed once, well,
by moving four repetitions of "from lowest to highest" out of the options and
into the stem. Then it got rewritten again into something worse. **A question
that works after one fix should be left alone.** Showing a sample early is
cheaper than a second opinion late.

---

## 4. Italian

The quiz is the only part of the app with no translation at all. No `q_it`,
`opts_it` or `fact_it` exists in the schema and the renderer has no support for
them.

**The plumbing is in as of v0.150.146.** `mqL(q, field)` returns the Italian
when the app is in Italian and the field exists; otherwise English. `mqLOpts(q)`
is separate because the answer index points into that array: an Italian array of
a different length would silently mark the wrong option correct, so a length
mismatch falls back to English WHOLE rather than mixing the two.

Every read point is wired: question text, options, the trim context and the fact
blurb, in both the answer screen and the miss review. A question with no Italian
behaves exactly as it does today, which matters because translation lands pack by
pack.

**Then:** new questions get both languages at the time of writing. Existing
questions get translated pack by pack, after the pack is otherwise finished, so
nothing is translated twice.

Music terms stay in the form Italians actually use. LOOP not CICLO. The note
names are Do Re Mi in Italian, which matters: a question asking for "the seven
note names" has two correct answers unless it says LETTER names.

---

## 5. Building a pack, one tier at a time

Rewritten at the restart. The old version described reviewing existing questions;
that is no longer the job. Packs are written fresh and the old ones are a source
of topics and verified facts, nothing more.

**One pack at a time, and one DIFFICULTY TIER at a time within it.** A tier is
about 24 questions, which is small enough to hold a single standard across the
whole of it. A whole pack is not; that is how the last attempt drifted between
batch one and batch three.

### The sequence, per tier

Rewritten after the Bass pack, which is the first one where the style held. The
order below is what actually worked; steps 0, 8 and 9 are new and each of them
caught faults that everything before them had passed.

0. **Read `QUIZ_VOICE.md`.** Twelve approved questions in full, before writing a
   word. Skipping this is how the voice gets rebuilt from a description instead
   of from the artifact, and the drift is always toward the spec sheet.

1. **List the topics.** Mine the old pack for subjects and the corrected facts in
   8b and 8c. Take the subject, leave the wording. Check each topic against the
   other packs before writing: five bass subjects were already answers elsewhere.

2. **Write all the STEMS first.** One pass, in a column, where an odd one shows.

3. **Write all the OPTION SETS.** One pass, so the adjacent-distractor rule is
   applied the same way every time.

4. **Write all the BLURBS last.** Read 2b's thirteen approved rewrites first, not
   after.

5. **Search anything the answer depends on**, before it goes in. Every pack so
   far has produced three to five wrong facts at this step, and they are always
   attributions or superlatives, never bare dates.

6. **Write the Italian with the English.** Not afterward. `opts_it` must match
   `opts` in length or the answer index points at the wrong option.

7. **Show Daniele four or five**, then stop.

8. **Assemble EVERY tier written so far and audit them together.** A tier audited
   alone is a tier that has not been audited. Assembling easy and medium together
   found two diagram questions answering the same letters, a staff question
   colliding with a fretboard question, and a pair of blurbs each giving away the
   other's answer. None of that is visible inside one tier.

9. **Build the scratch file and run the HTML tools.** `intonare_bass_draft_build.py`
   injects the drafted pack into a copy of Intonare.html at `/tmp/draft.html`;
   set `INTONARE_HTML` and run style, leak, dup and trim against it. These four
   read the real file and had never once seen a pack in draft.

10. **The omega read.** Every question in the pack, in order, stem and options
    and blurb together, on the screen at once, read as a person. No script. This
    is the step that found eleven faults after everything above came back clean,
    including three questions whose options had stopped answering their own stems
    because I had rewritten the stem and not looked underneath it. **Any time a
    stem changes, its options and its blurb are now stale.**

11. **Ship gate**, then `MQ_PACK_READY`.

### The omega pass is a READ, and it cannot be replaced by a rule

Two real leaks were missed by a check that required two shared subject words
between the blurb and the other question, because "drums" in the question and
"drumming" in the blurb are different strings. The looser version reports about
fifteen pairs on a ninety-question pack and most are harmless: "Liverpool" in a
blurb does not answer "which city's airport is named after Lennon".

So the tool lists the pairs and the shared words, and the pairs get read. Every
time this pass was skipped, something got through.

### A blurb states a FACT, not an observation

Fifteen of forty blurbs in a Guitar draft had no name, no number and no date in
them. They read as remarks about how things generally are, and that is not a
did-you-know:

    observation   Factories ship guitars set high so nothing rattles in the box.
    fact          Action is measured at the twelfth fret, and a factory electric
                  leaves at about 1.6mm treble and 2mm bass.

    observation   Guitarists spent the fifties slitting speaker cones.
    fact          Willie Kizart's amp turned up damaged at the Rocket 88 session
                  in 1951, and Sam Phillips stuffed the torn speaker with
                  newspaper and kept the sound.

`intonare_blurb_draft_check.py` reports any blurb carrying none of the three,
and flags the generalisations that usually stand in for one: "most beginners",
"nobody", "players learn", "teachers say". A handful of mechanism blurbs
legitimately have none, so it reports rather than errors.

### Blurb length follows the pack, not one number

Beatles blurbs run 43 words because they are stories about people. Guitar runs
24 because it is information-heavy and one idea per blurb is enough. Daniele's
model blurb for Guitar is 27 words carrying one idea; the first draft averaged
36 trying to fit three.

Set the short threshold from the pack being written, not from the last one.

### An instrument pack wants ORIGINS. A people pack wants anecdotes.

The Guitar easy tier came back with 33 of 40 rewritten, against 26 of 90 for
Beatles, and the reason was one mistake made twice.

**The blurbs.** I built them on player anecdotes because that is what Beatles
does. Measured across the rewrite: blurbs resting on a named player went 9 to 1,
and blurbs about where the thing came from went 2 to 10.

    mine  B.B. King asked Billy Gibbons why he was working so hard, and
          Gibbons dropped to .007 gauge strings and never went back.
    his   String bending originated in the 1960s, notably popularized by
          Clarence White, who bent notes on his Telecaster.

    mine  Allan Holdsworth built entire solos out of hammer-ons and pull-offs.
    his   The technique has roots in 19th-century banjo tutorials, notably
          Herbert Ellis's 1898 school for the five-string banjo.

Beatles is a pack about people, so a story about a person IS the subject. Guitar
is a pack about a thing, and the interesting fact about a thing is where it came
from and who first did it. Same for Bass, Drums, Keys and Vocals when they land.

**The questions.** Avoiding definition-style stems, I turned 14 of 40 into
scenarios, and he rewrote 20 of 25 back toward a plain question word.

    mine  Your first finger has to lie flat across every string. What are you
          playing?
    his   What kind of chord calls for a finger to lie flat across multiple
          strings?

A beginner pack should ask directly. The riddle form is worse than the glossary
form it was avoiding, and `intonare_draft_check.py` now flags only the bare
glossary entry, "What is a barre chord?", rather than any direct question.

### If the real quote or number exists, use it instead of describing it

The single most useful thing to come out of a real edit pass. Three of the
rewrites replaced a sentence ABOUT a fact with the fact itself:

    mine   Portugal gave him the real words
    his    "Scrambled eggs / Oh my baby how I love your legs"

    mine   a mathematician ran the recording through a Fourier transform
    his    Harrison said he played an Fadd9 and to ask Paul about the bass note

    mine   a band that laughs a great deal more than the 1970 version suggested
    his    Jackson called it a documentary about a documentary, 21 days, 42 minutes

A blurb that gestures at something interesting is worse than one that hands it
over. Look for the quote before writing the summary.

### Register: the numbers from a real edit pass

Measured over 26 rewritten blurbs, the rhythm was already identical, median 2
sentences of 24 words in both. Every structural rule derived before that pass
was aimed at the wrong axis. What differed:

| per blurb | drafted | corrected |
|---|---|---|
| contractions | 0.19 | 0.42 |
| exclamation marks | 0.04 | 0.19 |
| quoted words or lyrics | 0.15 | 0.54 |
| "only" / "just" | 0.00 | 0.12 |
| "which" as a joiner | 0.23 | 0.12 |

Reference-book prose against a person telling somebody a good bit. The gap is
small words.

### British VOCABULARY is separate from British spelling

"Zebra crossing" passes every spelling check and is still wrong; it is a
crosswalk. Also caught: coach, cinema, posh, fortnight, storeys, holiday, flat,
lorry, queue, autumn, motorway, petrol.

### Two questions can lean on each other without being duplicates

The medium tier asked what artificial double tracking is. The hard tier asked
who built the machine that does it. Neither is a repeat, both are good, and a
single round could deal them in either order, in which case one hands over the
other. No duplicate check catches this, because the answers differ and so do
most of the words.

`intonare_draft_check.py` now reports any pair sharing three or more content
words. The bar is deliberately low and it throws false positives on shared
function words: it is a prompt to read the pair, not a verdict.

**Also watch for a stem that cannot point at one person.** "Which DJ called
himself the fifth Beatle" has no answer, because George Martin, Billy Preston,
Stuart Sutcliffe and Pete Best have all worn that title. A phrase being famous
is not the same as it being specific.

### The repetition warnings are advisory. Phrasing wins.

Two separate stems were made worse in one session by obeying a checker. A
repeated opening is a real smell in a pack of sixty questions about sixty
different subjects; in a pack about one band it is often just English. Fixing it
by inverting the sentence produces things nobody says:

    bad    Lennon lifted the words of which song almost whole from a poster?
    good   Which song's words did Lennon lift almost whole from a poster?

    bad    Harrison wrote which song in Eric Clapton's garden?
    good   Which song did Harrison write in Eric Clapton's garden?

    bad    On which Beatles record about a lonely woman does no Beatle play?
    good   Which Beatles song about a lonely woman has no Beatle playing on it?

**If varying an opening costs a natural sentence, keep the sentence.** Vary the
ask by changing what is being asked instead, which is the real fix: five songs
in a row is a sameness of SUBJECT, not of grammar, and moving one to an
instrument or a person solves both.

### Calibrate the repeat checks to the kind of pack

A subject named four times is a concentration worth flagging in Bass, where
dozens of different players appear and nobody should dominate. In a Beatles pack
it is just a Beatles pack: four men will be named constantly and correctly.

`intonare_draft_check.py` takes `PACK_SUBJECTS` for exactly this, and it should
be set before the first stem is written:

```
PACK_SUBJECTS="Lennon,McCartney,Harrison,Ringo,Starr,Martin" python3 check.py
```

**The cost of getting this wrong is not a false alarm, it is a bad edit.** The
uncalibrated warning made a Love Me Do question worse: it named Lennon playing
harmonica, which is a person doing something and passes the QUIZ_VOICE test, and
the flag pushed it to the flatter "which instrument opens Love Me Do". Reverted.
A check nobody trusts gets ignored; a check that is trusted while miscalibrated
gets obeyed.

### Sharing a question between packs: how, and why not by copying

A question takes its identity from the pack it is read out of:

    Object.assign({}, q, { pack: packId, idx: i })

So **copying a row into a second pack is not sharing, it is duplicating**. The
two copies carry different pack ids, the round dedupe cannot tell they are the
same question, and a custom round selecting both packs deals it twice.

A shared question stays in its home pack and carries a tag naming the packs it
also belongs to. The pack reader and the round builder pull it in while leaving
its home pack and index alone, so the dedupe already in place does the right
thing without being touched.

A candidate has to pass a read, not a keyword match. A scan across the six
rewritten packs raised 31 pairs and 14 survived: a question about where the
Precision Bass got its name matches "Fender" and "single-coil" and is still a
bass question. The test is whether a player who chose only the second pack would
expect to be asked it, and whether the question stands up without the first
pack's context.

### A pack is defined by what it should contain, not by what other packs own

Overlap between packs is expected and allowed. Bass cannot be fully separated
from Gear, Guitar Gods cannot be fully separated from Guitar Technique, and the
Seventies cannot be separated from Music History. Trying to carve them apart
produces packs with holes in them: a Bass pack with nothing about strings or
amps because Gear "owns" those is a worse Bass pack, and no player ever thinks
about it that way.

**Build each pack from what a player would expect to find in it, full stop.**
Double dip where the subject calls for it. A truss rod question belongs in Gear
because Gear is about equipment, and it belongs in Bass if the bass answer is
different from the guitar answer, or if the framing is a bass player's.

**What actually costs something is the same QUESTION in two packs**, because a
custom round can select both and deal it twice. That is the fault to check for,
and `intonare_quiz_dup.py` now checks it across packs rather than within one.
Topic overlap is free; a duplicate question is not.

**Corollary, learned the hard way.** Three questions were cut from the Bass pack
in v0.178 for being "Theory wearing a Bass badge": a key signature, an interval
between written notes, and counting a bar. Under this rule that was wrong.
Reading a key signature in bass clef is a thing a bass player does, and a Bass
pack should contain it whether or not Theory also does. They are back.

### Proper nouns in the Italian: released title wins

Checked against Italian sources rather than guessed. The rule is what the thing
was actually called when it reached Italy, which splits three ways.

**Keeps the original.** South Park, Comedy Central, Seinfeld, Happy Days, Beavis
and Butt-Head, King of the Hill. Company and model names always: Fender, Höfner,
Ampeg, Music Man, Rotosound, Morley. Song and album titles, always, in every
pack; Italy does not translate them.

**Takes the Italian release title.** Films that got one, which is most
pre-1990 cinema: Guerre stellari, Lo squalo, La febbre del sabato sera, Il
padrino, Brian di Nazareth. The Seventies pack already does this and it is
correct; do not "fix" it back to English.

**Keeps the name and gains a common noun.** An Italian reader needs the category
where an English one infers it: `alla rivista Musician`, not `a Musician`. `il
cortometraggio The Spirit of Christmas`. `il liceo Fairfax High`. Same for
`la top 40`, which Italy writes as a numeral rather than spelling out "top
forty".

**One useful finding:** South Park airs in Italy with the original American
theme, so a question about who wrote that theme works for an Italian player
exactly as it does for an English one. Worth checking per question rather than
assuming, because the answer sometimes changes whether the question is fair.

### The gate is the rewritten packs only

Five are done: guitar_gods, theory_fundamentals, advanced_theory, seventies,
bass. The other fifteen are queued for the same rebuild, so **their wording is
provisional and editing it is work that gets deleted.** A pack rewrite starts
from a topic list and keeps nothing but the subjects.

`intonare_quiz_style.py` reads `MQ_PACK_READY` and marks the rest "queued",
reporting their numbers without counting them as failures. When a pack is
rewritten and added to that list, it starts being gated automatically.

This matters because the style tools run file-wide by default, and a file-wide
number invites a file-wide fix. Twenty packs of polish on questions that are
about to be thrown away is the trap.

### Repetition is measured per pack, not per question

Added after on-device testing. "Most of what" seven times, "built on" seven
times, "which is why" three times in one pack. Every instance reads fine alone,
which is why no per-question check has ever caught one, and why this could not
stay a rule in a document.

`intonare_quiz_style.py` now counts eleven constructions per pack and reports a
rate per question, warning above 0.08. The threshold is measured, not chosen:
the cleanest packs sit at 0.00 to 0.03 and the median is about 0.04. On the first
run seven of twenty packs were over.

**The list is short on purpose.** most of what · which is why · is where · comes
from · turns up · built on · the whole point · runs on · is all about · to this
day · ever since. Add to it when a new habit shows up in a read, not
speculatively; a long list makes the rate meaningless.

### Two shipped tools were reading nothing at all

Both found by checking a number that looked too good, both the same shape, both
worth remembering because the failure is invisible:

- `intonare_quiz_audit.py` reported **BASS (0Q)** and printed "clean ✓" beside
  it. Its parser wanted `opts:[...],ans:` with no space; the Bass rows are
  written `opts:[...], opts_it:[...], ans:0`.
- `intonare_quiz_style.py` matched **zero questions in every bilingual pack**,
  because its regex wanted `q:"..." , opts:` with nothing between and every
  bilingual pack puts `q_it` there. Four live packs had never been read.

**A parser that silently matches nothing is worse than one that crashes.** When a
tool reports a pack clean, check that it counted the questions.

### Tried and abandoned, so nobody rebuilds them

Three detectors were written during the Bass pack and thrown away. Each is
recorded in the tool it would have lived in, and the shared reason is worth
stating once: **a check that fires on the approved material is worse than no
check, because it teaches you to ignore the output.**

| detector | what happened |
|---|---|
| second clause hung off ", and" should be its own sentence | fired on 7 of 42 approved blurbs including Daniele's own rewrite |
| closing sentence sharing no content word with the one before it | fired on 51 of 106 approved blurbs and caught 1 of the 3 known bad ones |
| trivia question with no named record, year or second proper noun | 23 flags, 3 real. Kept as a one-off reading list, never as a gate |

The three faults they were aiming at are all real and all live in this document
as reading instructions instead: the split, the non-sequitur closer, and the
complete idea. Some things only a person catches. Say so rather than shipping a
detector that cries wolf.

### Two rules in this file that push the wrong way

Both were followed correctly and both produced worse writing, so they carry a
counterweight now.

**"No two-part stems" is not "one clause".** Enforced hard it produces stems with
the verb at the end: "The Bass VI has six strings, tuned how?" The approved pack
runs a median of 11 words and a maximum of 23, so length was never the
constraint. Ask forwards.

**"Answer findable by length" does not mean shorten the answer.** Hacking words
off the correct option gives four clipped fragments. Lengthen the distractors.

### Why element-by-element rather than question-by-question

Writing a question end to end means switching standard three times per question:
stem craft, then distractor craft, then prose. Forty switches a tier is how the
standard slips. Batching by element holds one rule in mind at a time and makes
the outliers visible, because forty stems in a column show the odd one instantly
and forty stems scattered through forty questions do not.

## 6. Ship gate

Every build, no exceptions:

```
python3 quiz_style.py            # marketing 0, hedges near 0
python3 quiz_leak.py             # grammar and absolute leaks 0
python3 qdup2.py                 # no unintended same-topic pairs
python3 allpacks.py              # length and giveaway counts
python3 ellip.py                 # ellipsis-on-answer-only
python3 /mnt/project/intonare_regression_sentinel.py   # 97 fixes + 247 pins
python3 /mnt/project/intonare_backup_audit.py
python3 /mnt/project/intonare_changelog_gate.py
node --check on every script block
playwright smoke: quiz opens, no console errors, both languages
```

Then version bump in three places, changelog entry, copy to outputs as plain
`Intonare.html`.

---

## 7. Traps, every one of which happened

**Deleting by text fragment hits the wrong question.** Searching rock_metal for
"power chord" matched the OPTION text inside the Smoke on the Water question and
removed a good unique question. Always confirm the fragment is in the STEM, and
keep a copy of anything removed.

**Every removal goes into `quiz_removed.json`** with full source, so it can be
restored verbatim. Twenty-six were removed before this rule; one had to come
back.

**Duplicates hide fixes.** The second Napster question still carried revenue
figures corrected two versions earlier. A fix lands on one copy and the other
keeps teaching the error.

**Cross-pack duplicates are allowed.** Daniele's call: a question relevant to two
packs can live in both and it pads the thinner categories. Only same-pack repeats
must go.

**Removing questions shifts everything.** It used to change which questions were
"easy", because difficulty was array position. That is fixed, but it is the kind
of coupling worth watching for.

**`re.sub` expands escapes in its replacement.** `\\n` becomes a real newline and
breaks the string. Use a function replacement or escape it.

**Apostrophes inside single-quoted JS strings need escaping.** Several edits
reverted on this alone.

**Syntax-check after every step, not at the end of a batch.** A batch that fails
tells you nothing about which edit did it.

---

---

## 7a. How to edit the file without breaking it

Every one of these cost a reverted edit or a broken build during this work. The
quiz data lives inside a 10MB single-file app and the usual habits do not
survive it.

**Every replacement asserts a single match.** `assert h.count(old)==1` before
writing. A string that appears twice will silently edit the wrong question; a
string that appears zero times will silently do nothing and report success.
Several edits this session hit `MISS(2)` and `MISS(3)` on option text like "A
type of jazz" that recurs across packs. Scope those by including a neighbouring
option in the match.

**Syntax-check after EVERY step, not at the end of a batch.** Extract every
`<script>` block and run `node --check` on each. A batch that fails tells you
nothing about which edit did it, and one session lost time to exactly that.

**`re.sub` expands escapes in the REPLACEMENT string.** `\n` becomes a real
newline and breaks the JS string. Sixteen Italian headings were destroyed this
way. Use a function replacement, or escape it, or use `str.replace`.

**Apostrophes inside single-quoted JS strings need escaping**, and double
apostrophes break it the other way. `dell\\'Arco` is wrong; `dell\'Arco` is
right. Several edits reverted on this alone.

**Do not run DOTALL regex or backward-scanning patterns on the whole file.** A
pattern starting `[^/\n]*` rescans from every position in 10MB and never
finishes. Split on newlines and filter lines instead. Two audit scripts had to be
rewritten line-based after timing out.

**Deleting a question: match the STEM, never an option.** Searching rock_metal
for "power chord" matched the option text inside the Smoke on the Water question
and removed a good unique question. Confirm the fragment is in `q:"..."` before
walking the braces.

**Everything removed goes into `quiz_removed.json`** with full source, keyed by
pack and question, so it can be restored verbatim. Twenty-seven questions were
removed before that rule existed and one had to come back.

**Bounding a pack:** the last pack in `PACKS` has no following pack, so a naive
"scan 90000 characters forward" runs into the melody data after it. A progress
counter reported 220 tagged questions in a 60-question pack for exactly this
reason. Bound on `\n};` instead.

**Version bump is three places**, and the changelog gate checks them: the HTML
comment, the `<span>` in the UI, and `const INTONARE_VERSION`.

**Ship as plain `Intonare.html`** into the outputs directory. Never version-suffix
the filename; the Windows build script depends on the plain name.

---

## 8. Tools

| script | what it finds |
|---|---|
Every script carries a banner saying whether it writes. Four of the nine are read
only and safe to run at any time; three write to Intonare.html; two need an
argument and print usage without one.

| script | writes? | what it does |
|---|---|---|
| `intonare_quiz_style.py` | no | marketing words, hedges, "not just", rhetorical openers |
| `intonare_quiz_leak.py` | no | article, plural, hedge-only and absolute-distractor leaks |
| `intonare_quiz_dup.py` | no | same-topic pairs by shared word sets |
| `intonare_quiz_trim_audit.py` | no | questions the trimmer gives away |
| `intonare_quiz_progress.py` | no | regenerates the progress table from the file |
| `intonare_quiz_livecheck.py` | no | **takes a pack id.** Measures from the RUNNING app |
| `intonare_quiz_strip.py` | **YES** | strips trailing detail from options. Idempotent |
| `intonare_quiz_addit.py` | **YES** | **takes a json batch.** Adds Italian to existing questions |
| `intonare_quiz_difficulty.py` | one-shot | the tier and blend installer, already applied |

**Use `livecheck` rather than the source-parsing tools on any pack with
bilingual fields.** A question carrying `q_it` between `q` and `opts` does not
match their regexes, so they under-count badly: guitar_gods reported 52 questions
while holding 100. Updating them for the schema is outstanding work.

**Do not run `strip` as part of "check everything".** It rewrites the app. It is
safe to re-run and refuses anything that would collapse two options into the same
text, but it is not an audit.

### Which of these you actually need under the restart

Being honest about it, because nine scripts implies nine jobs and there are not
nine jobs.

**Needed every pack:** `livecheck` (the only schema-aware measure), `style` (the
cadence check, which is the failure mode that caused the restart), `leak`, `dup`,
and `addit` for the Italian.

**Needed occasionally:** `progress` when the spec's table needs refreshing.

**Effectively spent, kept as documentation:** `strip` and `difficulty` were
one-shot repairs to the OLD bank. Questions written fresh to section 2b carry no
em-dash detail and no untagged difficulty, so neither has anything to do. Verified:
strip re-run today changes 0 questions. Keep them for the record of what was done
and why, not as part of any workflow.

**Superseded:** `trim_audit` measures the trimmer giving answers away. If no
option exceeds 100 characters the trimmer never fires, and `livecheck` reports
the same giveaway count anyway. Its 8 remaining hits are all in old locked packs.

So: five scripts in the working loop, four in the archive.

**All of the above parse the SOURCE and none of them understand the bilingual
schema.** A question carrying `q_it` between `q` and `opts` is invisible to every
regex in the list, so guitar_gods reports 52 questions when it holds 100. Measure
a bilingual pack from the live app instead, reading `PACKS[name].questions`
directly. `intonare_quiz_livecheck.py` does that and reports totals, missing Italian, broken
answer indices, over-long answers, ellipsis giveaways and stem giveaways in one
pass. Updating the source-parsing tools for the new schema is outstanding work.

All in `/mnt/user-data/outputs/`. Two cautions carried from the guide work: these
measure SHAPE, not quality. Read their output, do not obey it.

---

---

## 8a. The difficulty mechanism, as built

Documented because the spec described the STANDARD for tagging but never the code
that consumes the tags, and nobody picking this up cold would find it.

**`mqTier(q)`** returns `q.d`, defaulting to 2. An untagged question is a medium
question as far as every other function is concerned.

**`MQ_BLEND`** holds the proportions. Easy is 75/25/0, medium is 20/60/20, hard
is 0/25/75. These are proportions, not quotas: `mqBlendTiers` takes its share
from each bucket and then tops up from the neighbouring tiers if one ran short,
so picking HARD on a pack with four hard questions still returns a full round.

**`mqSurvivalOrder`** ignores the chosen tier entirely and concatenates easy,
then medium, then hard. Survival ramps rather than filtering: losing on question
forty because the run finally got difficult is a better ending than losing on
question three to a deep cut.

**`mqShapeRound`** orders the round after the blend has chosen it. First two
questions from the easiest available, difficulty climbing to about four fifths
through, and the LAST question stepped back down. Ending on the hardest question
is the instinct and it sends the player away having just failed.

**Bilingual reads** go through `mqL(q, field)` for the question and the fact, and
`mqLOpts(q)` for the options. The options helper is separate on purpose: the
answer index points into that array, so an Italian array of a different length
would silently mark the wrong option correct. A mismatch falls back to English
whole rather than mixing the two.

Not built, agreed in principle: shifting the tier by the player's current streak,
and letting the player select more than one tier at once.

---

## 8b. Every wrong fact found so far

Kept because these were expensive to find, several were repeated in sources
everywhere, and anyone re-deriving them would spend hours. Fifteen across six
packs.

| pack | was | is |
|---|---|---|
| theory | Hemiola is three groups of two felt as two groups of three | The other way round. Two groups of three felt as three groups of two |
| theory | Rallentando drifts, ritardando is deliberate | Grove calls them interchangeable; modern sources argue OPPOSITE distinctions |
| theory | The subdominant is "the note below the dominant" | It is a fifth BELOW the tonic, mirroring the dominant above |
| theory | Accenting 2 and 4 is syncopation | That is the backbeat. Those beats are still on the beat |
| music history | Bach's Well-Tempered Clavier established equal temperament | WELL temperament, an unequal tuning. Equal temperament came long after his death |
| music history | Revenues fell from $28bn (1999) to $7bn (2015) | IFPI: $22.2bn in 1999, bottoming at $13.1bn in 2014 |
| music history | Gated reverb was found during an In the Air Tonight session | Found on Peter Gabriel's third album in 1980, Collins on drums. It reached In the Air Tonight the year after |
| music history | The Funk Brothers played on more number ones than the Beatles, Elvis, the Stones and the Beach Boys combined | A tagline from Standing in the Shadows of Motown, never independently checked |
| music history | Sam Phillips said he wanted "a white man who had the Negro sound" | He denied it. Usually traced to his assistant Marion Keisker |
| guitar gods | Clapton's Cream guitar was the Beano Les Paul | The SG painted by The Fool. The Beano was stolen during Cream's first rehearsals |
| guitar gods | Greeny sold for around 2 million pounds in 2022 | Hammett bought it in 2014; the $2m was the ASKING price and he paid well under half |
| guitar gods | Standard tuning's open strings are all notes of E major | E major has G# and D#, not G and D. E and Em simply ring across all six strings |
| guitar gods | Santana has played PRS almost exclusively since the 1970s | Gibson and Yamaha through the 70s, including the SG at Woodstock. PRS from the early 80s |
| rock & metal | Lemmy started the metal umlaut trend | Blue Oyster Cult used it around 1970. Lemmy said he pinched it from them |
| bass | Larry Graham accidentally invented slap bass | Worked out on the UPRIGHT bass in New Orleans around the 1910s. Graham brought it to electric in the late 1960s |

**The pattern worth carrying forward:** every one of these was repeated
confidently in multiple places. None of them would have been caught by any tool.
Reading plus a search is the only thing that finds them, which is why step 2 of
the sequence exists.

**And one caught by playing rather than reading:** the Sonic Youth question was
tagged medium and is a hard question. A mistagged difficulty is invisible to
every check and only shows up when somebody meets it in a round.

---

## 8c. Wrong facts found in the Bass pack, August 2026

Same shape as 8b every time: an attribution or a superlative, never a bare date.

    Claypool wrote the music, Parker and Stone the words   (he wrote all of it)
    Leary came a distant last                              (invented; the
                                                            campaign folded when
                                                            he was jailed)
    Gibson EB basses are short scale at 30 inches          (30.5)
    Louis Johnson played on which MJ song                  (two right answers;
                                                            he is on Thriller too)
    Papa Was a Rollin' Stone, one chord and a bass figure   (describes Ball of
                                                            Confusion equally)

The Leary one is the one worth remembering. It was not sourced wrong, it was
composed: a plausible ending written to close a sentence. **A blurb sentence
that exists to land the rhythm is exactly where an invented fact goes.**

## 9. Progress

**Rebuilt packs, current as of v0.164.0.** Anything not listed here is still
pre-restart material behind COMING SOON, kept as a topic and fact source only.

| pack | authored | generated | tiers | languages | in MQ_PACK_READY |
|---|---|---|---|---|---|
| guitar_gods | 90 | none | 36/36/18 | both | yes |
| theory_fundamentals | 60 | ~1700 unique | 30/20/10 authored | both | yes |
| advanced_theory | 0 by design | ~2100 unique | generated only | both | yes |
| seventies | 113 | none | 44/47/22 | both | yes |
| bass | not started | | | | no |

The Seventies is 70 shared, 22 American-locale, 21 Italian-locale, so each
language draws from about 92. Guitar Gods went 60 to 90 in v0.163.0 because the
survival padding fix in v0.162.4 exposed it as the thinnest playable pack: it
hard-stopped at 60 while the others ran past 90.

Bass is the last pack of the five scoped for 1.0. The fretboard visual type
landed in v0.164.0 specifically for it.

### Still outstanding on every rebuilt pack

**No native Italian speaker has read any of it.** Linda's pass is the one thing
none of the tooling substitutes for, and it is the gate between "ready for
review" and "ready to ship".

## 10. Open decisions

- **Streak weighting.** Agreed in principle: shift the tier by the player's
  current streak. Not built, and deliberately so until several packs carry tags,
  because with one pack tagged it would have nothing to shift between.
- **Multi-tier selection.** Agreed in principle: let the player pick more than
  one tier at once. Not built. Needs a UI change as well as a filter change.

- **Italian needs a native reader.** Every Italian string in this app was written
  by me and nobody has checked it. Linda should read one finished pack before the
  remaining hundreds of questions are written in it.
- **The eight giveaways** are all in the decades packs and all the same shape: a
  question naming a band whose self-titled album is the answer. These need the
  QUESTION rewritten, not the options.
- **Weak questions: RESOLVED, no cutting rule.** A scan for the signals of dull
  (blurb restating the answer, no proper noun anywhere, short generic stem)
  returned 17 candidates and every single one is a theory fundamental: the
  leading tone, the dominant, the subdominant, the seventh chord, modulation, the
  relative minor. Those are not padding, they are the floor of the theory pack.
  The detector was really finding "definitional with no famous name attached",
  which describes correct fundamentals. Nothing is cut for dullness.

- **Pack sizes are decided per pack, not globally.** 100 is the target, but a
  pack where softballs are abundant can go further. Guitar Gods could carry
  hundreds on players, bands and instruments alone. A decades pack has a harder
  ceiling because its questions are inherently recall of specific records. Judge
  at the point of writing rather than padding to a number.


---

---

## 11. Salvaged from QUIZ_PLAN.md, July 2026

`QUIZ_PLAN.md` was written eight months before this session and reached most of
the same conclusions from measurement rather than from play. It has been scrapped
in favour of this document, because its framing was "the quiz has fixable faults"
and the real problem was that the quiz was not fun. Everything below is what it
had that this document did not.

### The measurement that started it

Context rather than a rule. It is the evidence behind everything this session
concluded from playing, and it is worth keeping only because it shows the two
routes reached the same place.

Across 1,151 questions, grouped by the shape of the stem:

| shape | count | avg length ratio | avg answer | avg stem |
|---|---|---|---|---|
| What is / are | 566 | **1.78x** | 89 chars | 43 |
| What was | 267 | 1.65x | 101 | 61 |
| **Which** | 171 | **1.01x** | **21** | 75 |
| Who / Why / How | 23 | 1.89x | 68 | 59 |

**"Which" questions were already right.** Near-perfect balance, short parallel
options, and they read as a puzzle rather than a vocabulary check. Everything
this session concluded about wordiness and giveaways is visible in that table.

### Two rules from it that were NOT kept

Both were reviewed and rejected, recorded here so nobody re-adopts them.

**"No two consecutive questions in the same shape."** Written when questions were
served in array order. They are not: the pool is shuffled, blended across tiers
and then ordered by `mqShapeRound`, so what a player sees consecutively has
nothing to do with what sits next to it in the file. The rule is unenforceable at
the data level and meaningless at runtime. What survives is the version already
in section 2b: vary the question TYPE across a pack, which is about the pack
reading well, not about adjacency.

**"One breath."** A duplicate of "read it aloud and if you stumble the player
will too", which is in section 2b and says the same thing with a clearer test.
Two rules for one idea is how a spec stops being read.

### Audio and interactive question types

The single best idea in the old plan and absent from this one. The quiz is text
inside an app with a synth, sixty audited grooves, tuned instruments and live
pitch detection.

> Any website can ask what a perfect fifth is. Only Intonare can play one.

| format | packs | source |
|---|---|---|
| Interval, chord and scale ID | Theory, Keys, Vocals | generated from code, infinite, no copyright |
| Groove ID | Drums | the 60 audited grooves |
| Tempo estimation | Drums, Studio | play a groove, guess the BPM within a tolerance |
| Play-to-answer | Theory, Keys, Guitar | tap the note that completes the scale |
| Gear and anatomy images | Gear, Guitar, Bass | the Survival Guide reference photos |
| Sing or play the answer | Vocals, Guitar | scored by the existing pitch detection |

Start with **interval ID**: pure code, no assets, and the most useful skill the
app can test. These also sidestep the trust problem completely, because a synth
cannot be wrong about the interval it just played.

### When to build them: NOT during the pack passes

Decided rather than assumed. Each of these needs a new rendering path in the quiz
screen, and the content is GENERATED rather than authored, which is a different
job from reading and rewriting text questions.

Mixing them into a pack pass would stall the pass and produce a half-built
feature. They are a separate workstream, and the right moment is after two or
three packs are finished, when the text workflow is running without correction
and there is something to interleave the new types with.

The order when it starts, cheapest first:

1. **Interval and chord ID.** Pure code, infinite content, no assets, no bank to
   maintain. The single most useful thing the app can test.
2. **Groove ID.** The 60 audited grooves already exist and are sourced. The
   groove audit becomes quiz content for free.
3. **Notation ID.** The staff renderer and 37 SMuFL symbols already ship in the
   Survival Guide. Show a symbol, name it. Same argument as interval ID: the
   asset exists and cannot be wrong.
4. **Tempo estimation**, then **play-to-answer**, then **sing-the-answer**. Each
   needs progressively more UI work.

Steps 1 to 3 need no new content authored at all, which is what makes them worth
doing before the remaining 750 text questions rather than after.

### Sourcing options already rejected, with reasons

Recorded so nobody proposes them again.

- **OpenTriviaQA and similar repos.** 5,579 music questions, CC BY-SA 4.0, clean
  format, but pop-recording trivia rather than music education, quotes
  copyrighted lyrics verbatim, apostrophes stripped throughout, and ShareAlike at
  a scale of thousands.
- **Scraping quiz sites.** Facts are free; phrasing, invented distractors and the
  selection and arrangement of a set are not. The EU database right applies from
  Italy even where the contents are bare facts.
- **Full LLM regeneration.** 1,151 unverifiable questions in one voice is how the
  bank got into this state.
- **Runtime API generation.** Needs network, costs money per play, unverifiable
  live, and this app does not phone home.
- **Licensed pub-quiz banks.** Real money, and still pop trivia.

### One engagement idea worth keeping

Re-queue missed questions at the end of a run. Roughly twenty lines, and worth
more than any leaderboard.

---

## 12. The restart, from v0.150.164

Daniele's call after reading the finished Guitar Gods pack: the new questions
ranged from fine to weirdly worded, and the blurbs carried AI cadence throughout.
Measured, the blurbs had a sentence-length SD of 3.0 and 33 percent were exactly
two sentences of near-identical length. Not vocabulary, rhythm.

**The reasoning for restarting rather than continuing**, in his words: too much
content to sift, too many things falling through cracks, past instructions
bleeding into each other. Chasing leaks with tape.

The arithmetic agrees. Continuing means reading 1,116, fixing 250, writing 780
and translating all 1,116. Restarting at 60 a pack means writing about 1,140
clean and bilingual from birth. **The hidden cost is translation:** a kept
question still needs Italian, and translating something you did not write is
slower than writing the pair together.

And the leak metaphor is accurate. This work found eight distinct fault classes,
each invisible until something exposed it: length, ellipsis, absolutes,
duplicates, wrong facts, definitional framing, comparative answers, blurb
cadence. There is no reason to think that list is complete, and each new one
meant reading everything again.

### The shape of it

**Packs ship as free content after launch.** That is the unlock. 1.0 needs four
or five excellent packs, not nineteen mixed ones. About 300 questions for launch
instead of 1,900, each with real attention, and every later pack is a reason to
reopen the app.

**60 questions a pack, not 100.** The padding to 100 is audible. Sixty excellent
beats a hundred mixed, and the repeat problem it was meant to solve is better
solved by the generated question types.

**One pack, one difficulty tier at a time.** Not one pack at a time. A tier is
small enough to hold one standard in mind for the whole of it.

### The methods agreed, from the options weighed

1. **Blurbs become fragments, not prose.** "Fender, 1954. Shape unchanged since"
   rather than "It arrived in 1954 and the shape has barely changed". The AI
   voice lives in complete balanced sentences; fragments are almost impossible to
   write in it, they read faster on a phone, and they halve the prose volume.
2. **Build the generated question types early**, not after several packs.
   Interval ID, chord ID, groove ID, notation ID. Zero prose, no distractor
   writing, no fact-checking, and they fill the repeat gap that made 100 a
   target. Previously scheduled late; that was wrong, because they attack the
   volume problem which is the root cause.
3. **Pass by ELEMENT, not by question.** All the stems, then all the option sets,
   then all the blurbs. Batching by task holds one standard rather than switching
   three times per question.
4. **Source the blurb, do not compose it.** Report a fact from a reference rather
   than writing around it. Much harder to drift into cadence when reporting.
5. **Daniele writes five blurbs in his own voice** and they become the reference.
   The tone rules here are abstract; five real examples are worth more than a
   page of description.

### What is salvaged, not torched

The **fifteen corrected facts** in section 8b, expensive to find. The roughly 450
questions that pass every check, kept as a TOPIC AND FACT SOURCE rather than as
drafts. And this document.

### The lock mechanism

`MQ_PACK_READY` lists the playable packs. Everything else draws greyed with
COMING SOON and cannot be selected, played or drawn from, with guards at four
levels: the grid render, the toggle, quick play, and the pool builder itself.

Packs stay VISIBLE on purpose. Hiding them would shift the grid every time one
came online and make it easy to lose track of what is left.

**Add a pack id the moment it passes its ship gate and not before.** A player
cannot tell a finished pack from an unfinished one, and a bad first round is
worse than a locked door.

### The risk worth naming

Restarting is also how a project ends up eight months later with three packs and
no launch. The discipline that makes this work is shipping 1.0 with four packs
and meaning it.

---

## 13. Locale-tagged questions

A decade means different things in different countries. Watergate lands in Ohio
and nowhere else; Carosello lands in Milan and nowhere else. A question may
carry `loc:'en'` or `loc:'it'` to say which audience it is FOR, as opposed to
which language it is written in. No `loc` means shared.

    { q:'...', q_it:'...', opts:[...], opts_it:[...], ans:0, d:2,
      loc:'it', fact:'...', fact_it:'...' }

**Both languages are still mandatory on a locale question.** This is not
politeness, it is mechanical. The pool builder filters on `q && q.q && q.opts &&
q.opts.length` BEFORE it checks locale, so a question written only in Italian is
dropped in both languages and vanishes without an error. Proven by test. A
second reason: a player can switch language mid-round from Settings, and the
round is already built, so the off-language side gets rendered.

The off-language side needs to be correct and complete. It does not need the
same care as the served side, because it is only ever read when somebody
switches language mid-round.

### What it touches

Three places, and they must agree or the count and the deal drift apart:

- `mqQInLocale(q)` — the predicate
- `mqPackQuestions(packId)` — used by the cleared check and the survival card count
- the pool builder's filter

That third agreement is the one that bites. A pack whose count says 92 and whose
deal gives 91 will read as a bug for months before anyone traces it.

### Pairing is not worth it

Making one record hold an English question and an unrelated Italian one was
considered and declined. The schema has a single `ans` index, so two unrelated
questions need two; the miss review, share card and resume path all render a
stored question object and would show a card the player never played; and it
forces exact pairing forever, so adding one Italian question means inventing an
English one to sit beside it.

### Sizing

Both slices should be the same size, or one language is tailored and the other
garnished. The Seventies runs 70 shared, 22 American, 21 Italian, which puts
roughly 2.5 locale questions in a round of ten. At 12 per side it was 1.4, which
is a rounding error rather than a tailored pack.


---

## 14. Question visuals

`mqVisHtml` dispatches on `vis.t`. Three types exist.

**Staff notation**, the default. Any clef, key signature, explicit accidentals,
per-note spelling. Bass clef works, so a bass line reads correctly without new
code.

    vis:{ chords:[[45,52]], clef:'bass', keySig:{n:2,type:'#'} }

**Rhythm notation**, `t:'rhythm'`. Note values and rests on a single line.

    vis:{ t:'rhythm', notes:[...] }

**Fretboard**, `t:'fret'`, added v0.164.0. String names, fret numbers, inlays,
marked positions, any instrument in `SR_FRETS` including bass and five-string.

    vis:{ t:'fret', inst:'bass', lo:1, hi:5, open:false,
          dots:[{s:1,f:3,label:'R'},{s:3,f:2,hollow:true}] }

`s` indexes `SR_FRETS[inst].open` from the LOWEST string up, and rows render
reversed so the highest string sits on the top line, which is tab order.

### Why there are four neck renderers in the file

`srRenderFret` (Sight Reading), `gccDrawDiagram` (chord charts) and
`gssDrawFretboard` (scales) all append DOM nodes into a fixed element by id, and
`srRenderFret` reads seven module globals and wires click handlers. `mqVisHtml`
builds a string. Refactoring a working interactive tool to serve a pack that did
not exist yet was judged speculative surgery, so `mqFretboardSvg` borrows the
geometry and returns markup. Folding them together later is a safe refactor with
the quiz as a second test case; doing it first was not.

### Lessons carried into the renderer, each got wrong once

- Inlays sit IN the fret they mark, not a cell early
- A nut is drawn only where the nut is; elsewhere that line is a fret
- Lane height near square reads as a neck; a tall lane reads as a grid
- Every color arrives concrete, because SVG attributes cannot resolve `var()`
- Fret numbers need their own label strip or they clip against the board edge
- An open column and a fret zero column are the same thing, so drawing both
  duplicates it

### No audio questions

A question whose answer is only available with the volume up is broken rather
than hard, for anyone playing on a train. The app has a full synth engine and it
stays out of the quiz.


---

## 15. Fact checking, in two tiers

Checking every claim is not affordable and not necessary. The Seventies pack has
220 checkable assertions across 113 blurbs. Guitar Gods shipped after a spot
check, not a sweep: section 8b records fifteen wrong facts found across SIX
packs.

**Tier one, mandatory: every claim a question's ANSWER depends on.** These are
the ones where being wrong makes the app look broken, because a player who knows
the topic sees a correct option marked wrong. Eighteen of 113 in the Seventies,
nine of thirty in the Guitar Gods expansion. That is a short, finite list.

**Tier two, as time allows: blurb colour.** Numbers, fees, counts, dates inside
a blurb. Wrong ones are embarrassing rather than broken. This is the standard
the four shipped packs already carry.

### The risk pattern, which is the whole point of this section

Every flat-wrong claim found so far was a **superlative, a first, or an
attribution.**

    Kraftwerk's Autobahn as a 22-minute HIT       (the album track; the single was 3:27)
    the Fiat 127's predecessor winning the SAME award (the 850 never won anything)
    Rindt winning the title BEFORE Monza          (posthumously, after)
    Dark Side of the Moon as best-selling INSTRUMENTAL album (it has singing)
    Rapper's Delight as the FIRST rap on radio    (King Tim III came earlier)
    the slogan the Spain brothers ADDED           (Have a happy day, not nice day)
    the console Atari RELEASED in 1977            (the VCS; 2600 came in 1982)

Bare years and ordinary events came back clean every time. **Write fewer
superlatives and the checking gets cheaper.**

### Two-correct-answer questions

The worst failure mode, because no audit catches it. Two found:

- "Which guitarist from Niger built his first instrument from bicycle brake
  wire?" — Mdou Moctar AND Tinariwen's Ibrahim Ag Alhabib both did. The stem
  leaned entirely on the country, and Bombino is also Nigerien. Fixed by
  anchoring on the sardine tin, which only Moctar has.
- "Which bluesman took the Delta sound to Chicago and plugged it in?" — Howlin'
  Wolf equally. Fixed by anchoring on the 1941 Lomax field recording.

**Test: can you name a second person the stem also describes?** If yes, find the
detail that belongs to one of them.

### What cannot be sourced does not get written

Removed rather than searched indefinitely: Evel Knievel's broken-bone count, Jim
Fixx's two packs a day, the Muppet Show's hundred countries, landlords banning
waterbeds, the Holiday Special's twenty million viewers, Kabir Bedi still being
recognized. A disputed claim can survive if it is attributed INSIDE the sentence:
"Ray Tomlinson said he went looking for a character that…".


---

## 16. Tooling, and the discipline it does not replace

### `intonare_pack_audit.py`

Checks the half of section 1 a machine can hold. Answer findable by length in
EITHER language, answer as the only option carrying a number, stem sharing a
distinctive word with its answer, blurb restating its stem, cross-references
between questions, a subject over the cap, two questions with the same answer,
untagged difficulty, missing Italian, tier drift.

    python3 intonare_pack_audit.py pack.json --cap 2 --answered --allow allow.json

`--cap` is **2 for a decades pack**, where variety is the point, and **3 for a
subject pack**, where returning to Hendrix three times is the design rather than
a fault. `--allow` takes a JSON list of substrings for genuine collisions that
word matching cannot resolve, such as Rocky and The Rocky Horror Picture Show.

Every check was tested against a reconstruction of a real fault and against the
approved Guitar Gods pack. **Six bugs were found in the audit itself that way**,
including reading `opts[0]` while the pack stores an answer index, and computing
the common-word list from English then applying it to Italian.

### `intonare_blurb_voice.py`

Blurb mechanics, with thresholds MEASURED from the shipped Guitar Gods pack
rather than invented: 28 to 58 words, median 39, zero pronoun openings, first
sentence longer in 29 of 32 two-sentence blurbs.

It reports the exclamation count and does not judge it. A percentage cannot see
where one fits, and an earlier version enforced my own restraint back onto
Daniele's voice.

### What neither tool can do

Whether a question is fun. Whether a distractor is genuinely arguable. Whether a
fact is true. Whether a question is answerable by reasoning or only by already
knowing — the Comaneci scoreboard question was mechanically perfect and
unanswerable until the stem supplied the setup.

### The discipline that matters more than either tool

**Read every edit back out of the shipped file before reporting it done.**

Three separate fixes silently failed in one session and were nearly reported as
complete: two on whitespace inside an option array, one because the answer-spread
step had rotated the options since the string was written. A fourth appended a
comma next to an existing one and left a sparse array hole that made the pack
count 91 while filters saw 90.

`assert count == 1` catches a miss. It does not catch a script that asserts on
one substitution, applies it, then throws on the next and writes nothing.

### Order of work

Write, run everything, fix, THEN show. Not write, show, fix. Every review pass
that went to a human first found faults that the audits would have caught for
free.
