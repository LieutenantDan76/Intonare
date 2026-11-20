# Intonare changelog

What changed in each release, newest first.

## v1.0.5: Search that understands what you mean

- Search now understands categories. Type games, tests, flashcards, instruments, singing, ear, rhythm, reading, theory, harmony or practice (or the Italian word) and you get the modules that fit, best fits first. A single category word also shows a count above the list, like Games, 5.
- Search opens folders. Type games, ear training, reading, harmony or reference to jump straight to that folder. Type tools (strumenti in Italian) to see the Tools folders first, then every tool.
- Two-word searches work, like ear games or rhythm test. So do short phrases like train my ear, learn chords, keep time or read music.
- Search finds Settings now (try settings, dark mode, backup, streak or achievements), and understands wordle, dictation, tonic, do re mi, songs, perfect pitch and overtones.
- Streaks no longer stop at 40. Every further 40 in a row is a Prestige round (45 to 80 is Prestige 2x, 85 to 120 is Prestige 3x, and so on). Each round shows the same card as the first run with a colored frame and a small "Prestige 2x" badge, and pays the normal streak XP times the round number, up to 3x. The title keeps counting up forever.
- The streak toasts and the Mythic card are redesigned as one card for every level: neon glass in dark mode, light glass with dark text in light mode. Each level has its own size, glow, lines and shine, and the card unrolls in from the top edge. Mythic is purple now and carries a winged sword emblem (Lorc, game-icons.net, CC BY 3.0, credited in Credits & Thanks). Streak numbers in a Prestige round match round one (a 45 shows as 5, an 80 as 40).
- The Survival Guide now draws tablature and plays it. Reading Tab has seven pages (how to read it, reading order, tab beside a staff, what tab leaves out, tunings and capo, history, symbols), and Techniques has drawings for hammer-ons, pull-offs, bends, vibrato, palm muting, tapping, slides, harmonics and dead notes. Tap the play button on a drawing to hear all of it, or tap one column to hear just that note. The Bass chapter has two new tab pages, and Bass Clef Basics now shows the open strings on a staff.
- Fixed the Bass Clef Basics page: bass guitar is written an octave higher than it sounds, not at concert pitch, and the open-string positions on the staff were wrong.
- Each result says what it is: Game, Train, Tool or Folder.
- When nothing matches, Search shows category buttons so you can browse instead of staring at an empty list.
- Search finds more of what is inside the screens: capo, strobe, tuning fork, Hammond, Rhodes, tap tempo, ramp, decibel, concert pitch, twelve-bar blues, syncopation and more.
- The Road Trip tour described a different game. It now explains the real one: learn a pitch, hold it while music tries to pull you off it, then sing it back.
- The Games folder text now names all five games, and the Road Trip card says you sing.
- Fixed a doubled phrase in the Relative Pitch tour, and the Italian Polyrhythm tour now uses the right gender.
- New check in the ship tools: the search audit runs 90 real searches against the app and fails if a category stops finding what it should.
- Fixed the Open Full Reference button in Interval Training. The reference opened with no way back to the exercise. A Back to Training button now shows there and returns you to your session.
- Sight Singing now remembers the voice you choose with the voice button.
- If saving a backup file fails on the phone, the app now falls back to the share sheet. That fallback used to stop with an error.
- Security fix in Music Quiz: answers in the online categories come from a public trivia site and were put on the page without escaping. A bad entry there could have run code inside the app. That text is now escaped.
- If you change the language while a tour card is open, the card now changes language too.
- The error report now records which section of the app you were in. It used to leave that out.
- Restoring a backup is safer. The app now checks the file before it changes anything: a damaged or edited file is refused, a field with the wrong kind of data goes back to its default, and the file can only write settings the app knows. A broken file can no longer leave the app unable to start.
- Security fix: names of saved metronome presets, tempo ramp presets and saved chart views were put on the page without escaping. A crafted name, typed in or carried in a backup file, could have run code inside the app. That text is now escaped.
- Security sweep: every saved or typed text field was filled with a test payload and every screen was opened. Three more places put that text on the page as markup: the pinned row on the launcher (saved chart names), the vocal range history (voice type), and the progression grid (chord root and quality from a saved progression). All three are fixed. Drum kit saves are now read value by value, so a damaged save cannot break the Drums screen.
- Italian: 17 screens kept some text in the old language after you changed language, until you closed and reopened them. Among them: the tuner and metronome subtitles, the piano octave label, Rhythm Cards, Interval Reference, the Transposer, the Chordle, Diadle, Tonale and Rhythm Reading difficulty pickers, Relative Pitch, Road Trip, Staff Reading, the Chord Ear chord list and the favorites sheet. All of them now switch at once. Four labels that were English in both languages are now translated: the Chord Ear chord groups, the Rhythm Reading bar count, the favorites count and the Tempo Guess slider label.
- After a language change, each slider section (volume, tempo) had a second copy of itself nested inside, and one tap opened and closed both. Fixed.
- Punctuation pass on app text in English and Italian. Long dashes in tips, help screens, groove names and status lines became colons, commas, periods or a middle dot. Note ranges now read C4–B5. The dash that stands for an empty readout ("— Hz") stays.
- Italian, round two: the launcher, the Music Quiz pack sheet (group tabs, pack names, pack count), the LEVEL chip and the Road Trip map city names now follow a language change too. Text that was English even in Italian mode is now translated: Master Volume, the empty Progress chart, NOW LOADING, the Survival Guide next-page link, the Tempo Lock target label, the chord name in the chord player and on the harp, two BACK buttons and the Theremin range.
- Octave labels read "OCT4" after you changed octave on the piano, Rhodes and Scales. They read "OCT 4" again.
- Sound: eleven of the simple synth voices (sine, piano, flute, bell, marimba, xylophone, vibraphone, pad, guitar, brass, melodica) left every part of every note plugged into the audio engine after the note ended. Over a long session that work piled up and could cause crackle on slower phones. Each note now unplugs itself once it has finished. The sound is unchanged: rendered before and after, the difference is below -120 dB.
- The Çiftetelli groove now plays the real pattern: a 3-3-2 first half, then two dums in a row, one tek and a silent last beat. The old version had a single dum and a busy tek-ka fill where that silence belongs.
- Sound: a bell or guitar note played without a set length kept running silently after it died away. It now stops when its sound has faded. The guitar version also held a faint hum at the end; that fades out now too.
- Italian, round three: opening the app in Italian showed the tuner's instrument families, the "play a note" hint, the piano's sound groups and the metronome sounds in English until you switched language. They now start in Italian. Chord diagrams name their shapes in Italian (Forma di E, Pos. 3, Barré 7, Senza fondamentale), and the piano songs use their Italian titles (Inno alla gioia, Notturno op. 9 n. 2, Rondò alla turca and others). Also translated: the Rhythm Reading RECORD label, the Progression sound chips, some instrument types (ukulele da concerto, 4 corde, bouzouki irlandese and greco, vibrafono), the Tempo Guess feels and the Latin drum category.
- Fixed: the first screen you opened from the launcher would not scroll until you switched tabs and came back.
- Groove names with Turkish letters (KARŞILAMA, ÇİFTETELLİ) now use the same font for every letter. The Ş was drawn in a wider fallback font.
- Opening the app from a shared link skips the splash. The splash animation used to keep running unseen for a few seconds after that, and its timeline still sent its "splash finished" signal a second time. It now stops the moment it is skipped.
- Code cleanup: a lint pass removed 68 functions that nothing called, duplicate translation keys and other leftovers. Old version numbers and a few long story comments in the code were cleaned up too. Nothing you can see or hear changes.
- The vibraphone sound used when samples have not loaded now uses the full vibraphone model with its tremolo. A second, simpler definition was overriding it with a plain bell tone.
- New audit script: a boot test opens every tool, exercise and game in a hidden browser and fails if any of them throws an error.

## v1.0.4: Practice history that counts every answer

- Practice History now counts every answer, right or wrong. Before, only a correct Sing answer in Interval Training reached your Progress screen, so Tap and Test mistakes never showed.
- Tap a row in Practice History to open a card with that exercise's accuracy for the week, how it compares to last week, a bar for each of the last seven days, and the three things you miss most.
- More exercises now show in Practice History: Rhythm Read, Rhythm cards, Relative Pitch, Staff Reading, Notation cards, Diadle, Tonale, Road Trip and Music Quiz. Music Quiz and Rhythm cards now log practice time too.
- Rhythm Read now counts weak rounds. They used to vanish when the score was too low to earn XP.
- Streak bonus XP is paid at the milestones, not on every answer. The streak toast shows every time a streak reaches 5, 10, 15 and so on up to 40, including when you rebuild a broken streak. It pays the bonus each time and names the amount, and the Mythic card shows its award too.
- Theremin: the pitch scale now spaces notes like the real instrument, with the notes crowding toward the antenna. The expanded view needs two hands, like the real thing: right hand on the pitch pad, left hand on the volume bar. Volume follows a real curve with a silent zone at the bottom, and the note slides down when you lift off. In the compact view the hint fades when you touch the field.
- Search no longer flashes dark frames when the keyboard opens on Android, and it remembers your keyboard height.
- Chordle: orange now means the right chord is in the progression but in a different spot, and gray means that chord is not in the progression at all. The ROOT pill is gone from the chord drawer, and the play button there follows your arpeggio setting. Shared daily results show the right squares. They used to show a present chord as black.
- Diadle: Hard mode replays now match what its text says, with no limit.
- Chordle and Diadle drawers: the blank gap at the bottom is gone, and the other bottom drawers were checked for the same gap and blur.
- Music Quiz: the back button in quick play no longer hides under the status bar. The rest of the app was checked for overlaps with the status bar and tab bar.
- Interval reference cards: the stop button works and the tail after a note is shorter.
- Signal chain: the yellow "!" badges are gone. The caution text still shows when you tap a pedal.
- Survival guide: the open page switches language in place.
- Credits: the groups have a new order, Isabella Citti is credited for the bass photos, and the permission line reads "used with permission".
- The developer unlock code no longer unlocks Pro, and the debug trigger is locked behind developer mode.

## v1.0.3: The tuner click stays on the tuner screen

- The tuner's in-tune click now fires only while the Tuner screen is in front. Before, the always-on mic could hear Music Quiz music, call a steady note in tune, and buzz the phone.
- Pocket mode is easier to feel. With the metronome sound off, each beat is now a heavy thump instead of a thin tick. Ghost notes in a groove stay a light tick, and accents are a full thump. At fast tempos the downbeat is a single full thump.
- Haptics on Android: Strong keeps the build-ups and the difference between feels instead of squeezing them flat, and it hits harder by holding each tap a little longer. Normal taps are a touch longer too. Soft and the iPhone are unchanged.
- Muting the metronome now cuts the sound at once. The next click used to leak through for a moment.
- The piano, organ, Rhodes, theremin and the other full-screen modes hide the Android status bar while they are open, and bring it back when you leave.
- Android stays in portrait. After a full-screen mode closed, the screen was free to rotate with the phone. It now goes back to portrait.
- Launch on Android: the system launch screen now stays up until the app draws its first frame. The dark blank gap between the two is gone.
- iPhone: Pro is now a real one-time App Store purchase, with Restore Purchase. The free unlock that TestFlight builds had is gone.
- If a purchase fails, the message now includes the store's reason, so support can tell what went wrong.
- The Pro purchase window now closes by itself when the unlock goes through, instead of sitting behind the confirmation.
- Music Quiz: the question header now runs up behind the status bar on iPhone and Android, with its pack art intact. A dark strip used to sit above it, and a thin one down each side.
- Settings has a new Help & Support link, with an Italian label.
- Search: the tab bar stays put when the keyboard opens. It used to ride up behind the blur.
- Android: the status bar color now comes from the app theme, not a deprecated call. Looks the same, and clears the edge-to-edge warning in Play.
- Back Up Progress now includes the iPhone stay-loud setting and the pin hint flag. The Voice Range legend label "Tessitura center" now has its Italian text.
- Search no longer flickers when the keyboard opens. Android briefly reports a tiny screen while the keyboard slides in, and the card shrank to match, then grew back. The card now waits for the screen size to settle.
- Small flickers across the app are gone. Quick access, the quiz sheets and other popups kept an invisible full-screen blur on the page even when closed. The blur now exists only while a popup is open, and fades in and out with it.

## v1.0.2: Achievements that unlock when they should

- Popups now frost the page behind them the same way quick access does. Settings, level, help, the streak sheet, search, chord and riff popups, and the progress sheets all blur the background, and the panel glass still shows.
- Every popup uses the same soft blur now. Light mode was heavier (22px) and washed out, so it is lighter. Quick access now frosts the header too.
- Dark mode popups all use the same 5px blur now (they ranged from none to 8px). Help and the small picker popups cover the tab bar like settings does.
- The streak sheet now blurs the page behind it. Before, the blur was mixed back with the sharp page.
- Music Quiz: a gray shadow no longer shows along the bottom edge. It came from the hidden answer drawer.
- The start-up animation draws at a lower resolution on high-density phones. It runs much smoother on first launch and looks the same.
- The first-run tour spotlight no longer repaints the whole screen on every frame. Only the glow pulses now.
- First launch from the module selector is smoother. Every embedded font face now loads before you pick a module, background reminder setup waits for idle, and the overlay scan no longer reruns each time a module builds its screen.
- Motion now speaks one language. 61 different easing curves collapse to five (ease out, sheet, standard, exit, spring), and 24 different press sizes collapse to three.
- Sheets and popups (settings, level, search, picker, quiz sheets) now share one open feel: same curve, similar length, no overshoot.
- Opening a module no longer stalls on hidden redraws. Launches skip work for tools that were not running, and the session bar waits for the screen to settle.
- Light mode tab glows are tuned to even brightness across Metro and Train.
- Light mode answer screens use real colors. Tonale's green, amber and red were near-black olive, brown and maroon, and the Target label disappeared. They are now vivid, and the label reads.
- Chordle and Diadle tiles and legends, ear training answers, Music Quiz answers, Survival and Daily cards, and the Volume Meter zones lose their muddy tints in light mode.
- Light mode status text (in tune, close, off) moves from dark olive, chocolate and maroon to a clear green, amber and red that still passes contrast.
- The tab light in light mode glows in each tab's own bright color instead of gray-blue.
- Module headers lose their subtitles. The session timer now sits at the right end of the title row.
- The collapsed header uses a soft blur and tint that fades out, instead of a hard colored bar.
- The tab bar is now a rounded dock with a lifted pill on the active tab.
- The active tab is lit from the top again, with a colored glow line and a soft cone of light under it, in dark and light.
- Light mode gets a frosted glass look on the tab bar, cards, folders, and every popup and sheet (Settings, Progress, Pro, Quick Access, help and more). Dark mode popups get the same surface style with a lighter rim.
- Cards, folders, popups, and their inner boxes share the same rounded corners in both themes.
- One corner scale across modules: 22 for cards, 14 for boxes, 10 for buttons. In light mode, decorative boxes get soft rims instead of dark outlines. Tappable controls keep their outlines.
- Small labels that were too faint now meet a contrast floor, such as the piano lid and tone tabs, BPM unit and tempo name, tuner readout labels, session timer goal, and several hint texts. Both themes.
- Tab labels are a little larger.
- The active tab has no chip anymore. One brighter light bar with a soft glow slides between tabs.
- Scrollbars are hidden on touch screens, which also removes the stray bar in the streak popup.
- Light mode search box and popups are more solid so text is easier to read.
- Settings, Progress and other popups are real frosted glass now: the page shows through the panel, blurred.
- The small glow smudge under the title no longer shows when the session bar is nearly empty.
- A thin line and shadow no longer show at the bottom of the screen on the home grid and in quizzes.
- The search box uses the app fonts instead of the system font.
- Piano keys light up in a clear warm color when you press or hold them.
- I Have You Now did not unlock on a 0ms Tempo Lock round. The app shows the timing error rounded, but the unlock needed an exact zero, so a "0ms" on screen could still miss. It now unlocks on anything that rounds to 0ms. A 0 bpm miss in Tempo Guess counts as well, which it never did before.
- Great Ears Kid could not be earned at all. The interval test now earns it: a perfect 10 out of 10 with every interval turned on (the ALL deck).
- Flawless Victory only worked through the Notation Cards test. A perfect interval test on a deck of eight or more intervals now counts too, and so do a perfect Tónale run above Easy and a perfect Daily Quiz.
- Deaf Composer needed a first-guess solve with no play, which comes down to luck. It is now a solve in two guesses or fewer without pressing play.
- Hard Day's Night read a stale timer and left out the minutes still running. It now reads the live total.
- The Force Is With You unlocked at the next save instead of at the summit. It now unlocks as you land on it.
- Dedicated and Addicted now check every time practice time is logged, not only at the next save.
- Dedicated counted only the last 90 days, because older history is trimmed. A lifetime counter now carries the total, and it starts from the history you already have.
- Daily keys now follow your own calendar day instead of UTC. In California the day used to roll over at 5pm, which could break a streak, reset the session timer early and move the daily challenges. Streaks saved under the old keys carry over without a reset.
- Your saved bests could be overwritten by a worse session. Tempo Lock, Tempo Guess, Polyrhythm, Chordle and Diadle now keep the better of the saved record and the session, and round counts keep adding up.
- Tempo Lock now grades on the whole-bpm error you see on screen, so a result shown as 2 bpm off no longer grades like 1.6.
- Haptics were redesigned. A right answer feels like a bright "da-dink". A wrong answer feels like two dull thumps. Wins and level ups build up to one big hit. Each feel is now one native pattern on iPhone and Android, so the timing no longer wobbles, and a small tap can no longer cut a big celebration short. Phones without a haptic motor keep the old taps.
- Haptics now follow the sound you pick. Each correct, wrong, streak, level up, achievement, game over and new record sound has its own haptic, built from that sound's own notes, so the buzz lands on the same beats you hear. The Music Quiz round endings and the secret unlock sounds have theirs too.
- New in Settings: haptic strength, Soft, Normal or Strong. It is a big step between them now, it also applies on phones that use the basic haptic taps, and tapping a strength plays three equal taps so you can feel the difference.
- Haptics are now on by default for new installs. Anyone who already has the app keeps their current setting.
- Tuner: a small click when the needle settles in tune. The simple tuner also buzzes in time with its two-note lock sound.
- Music Quiz survival: the last wrong answer no longer fires the wrong buzz and the game over feel on top of each other.
- Music Quiz survival: ending a run on your best streak now plays the new record sting. It never did, because the streak was cleared before the check.
- Flute chart: every key now has a label. The thumb and side B♭ keys, the two trill keys, the three foot keys and the gizmo key were blank before. The small mini chart stays uncluttered.
- Two new help buttons: the interval pool popup (it now says that at least two intervals must stay on) and the Tempo Guess difficulty pill. The Tempo Guess help had the wrong ranges and left out Insane.
- Tuner and Metronome from the app icon menu now also work when the app is already open on the module chooser.
- Long-press the app icon for Tuner, Metronome, Daily Chordle and Music Quiz, on iPhone and Android.
- iPhone: the tuner now records through the phone's own audio engine instead of the web view, which stops the app's sound from dropping in volume while the mic is on. Haptics also keep working with the mic on.
- Module screens have a new header. The title is in sentence case. Back is a calm glass pill that says only "Back", with no folder name. The mic and star are calm glass pills too, and the level chip now reads "LEVEL n" in a wider pill.
- The level chip draws your XP progress as a glowing line around its edge. XP awards pop up inside the chip and add up when they arrive close together. A level-up fills the line, shows the new level, then starts the line again.
- The clock and battery now show on every phone, floating transparent over the app, like a native app. The header sits right below them, in one layout for all phones: Back on the left, mic, star and level on the right, title row below. The text color follows light or dark mode. There is no more camera guessing, and the mic no longer sits above the title.
- The subtitle sits beside the title only when it fits whole. If not, it moves under the session bar, left of the timer, and the title always keeps its room.
- The hub, folder and root screens use the same header layout, so the content no longer jumps up and down when you enter or leave a module. Folder and hub titles are in sentence case, and a folder shows the same Back pill. Their subtitle sits under the session bar.
- Titles use one font. The header font only held capital letters, so lowercase letters came from a different face. It now includes lowercase, and the module subtitle is the same weight as the hub subtitle.
- After you leave a module, the space that fixed-height panels reserve for the header now returns to the right value.
- The mic, star and level chip got the new look on every screen.
- The level chip and the Back button now take the color of the tab you are in (cyan, gold, green, purple, and the matching deep tones in light mode). Back is a tinted glass pill with a bolder arrow.
- The level chip is calm when nothing is happening. The line and its glow sit low. When XP arrives, the line brightens and moves, then eases back down. Every chip change (popup, number count, level-up, line reset) now uses smooth easing.
- The mic button now turns green with a small pulsing dot whenever the mic is really on, including when the tuner opens with the mic already running. It used to look idle until you tapped it.
- Android: a small native change shows the status bar and reads its height. This needs a rebuild with go.bat. The navigation bar stays hidden as before; swipe up to show it. iPhone needs a new Codemagic build for the status bar.
- Not in this build: the header collapsing on scroll and returning.
- Music Quiz on iPhone: the answer drawer now reaches the bottom edge of the screen. The quiz panel added the bottom safe area as blank padding under the drawer, so a strip showed below it and the drawer seemed to rise from that strip. The NEXT button keeps its own padding, so it still clears the home indicator.
- iPhone: the sound could stop completely after the mic was switched on and off, and only came back after closing the app. iOS can leave the sound engine in an "interrupted" state when it changes the audio mode, and the app only woke it from "suspended". It now wakes the engine from any state that is not running, and tries again on the next touch.
- The audio debug readout now shows the sound engine state even when the mic is off.
- Settings: the haptic strength chip showed Normal after every restart, even when Strong or Soft was saved. The setting itself was kept, but Settings only read it after you opened the Progress screen. It now reads the saved value when Settings opens.
- iPhone: new "stay loud" mode, on by default. With the mic off, the app now stays in the louder recording audio mode with the speaker forced, instead of dropping to plain playback, which sounds quieter on at least one iPhone. It also removes the mode switch that could leave the sound dead. Turn it off with the STAY LOUD button in the audio debug panel (seven taps on the version number) to compare.
- New streak chip on the home screens, with a search button next to it. The chip counts the days you opened the app. Tap it for a practice sheet: resume your last tool, a calendar of the days you opened the app, and your achievements at a glance. The app starts the calendar log on the day you update, and backups carry it.
- The search button opens a floating glass search card that grows out of the button, like Spotlight on a Mac. The field stays in one place, even when the keyboard comes up. Resume, recent tools and round buttons for the four tabs sit under the field. Typing shows results with the letters you typed lit up, a highlight that slides between rows, filter chips, and an Open pill in the field for the top hit. The placeholder suggests things to try, and a tap gives a light haptic. The tab buttons use the same icons as the bottom tab bar, the list has no scroll bar, and the two Intervals screens have their own names, Interval reference and Interval training. Search now looks inside screens too. It finds every instrument chart (with piccolo, alto sax and the other types), the flute and clarinet trills, every Survival Guide tab and chapter, tunings and instruments in the Tuner, every scale, groove, drum preset and chord progression, time signatures, voice types, and the Organ and Rhodes tabs, and opens the exact spot. It understands words like sax, keys and pedals, and it forgives a typo or two. The streak sheet no longer has a search field.
- Search results now use each screen's own title, such as Chord ear training and Interval reference, and groove, drum and chord change twins read like Samba groove, Samba drums and Samba changes.
- Search works in Italian and with Do Re Mi note names. Italian search was silently off, and the same bug left the streak chip count, the calendar open days and the Resume card in the streak sheet empty. They now read your saved data.
- Closing the search card no longer leaves the page stuck, and short words like "re" no longer rank Reggae above Drop Re tuning.
- Search card on a touch screen: there is no sliding highlight any more, since a tap opens the row. It stays for mouse and keyboard on a computer.
- Module titles are now in title case, such as Pitch Match and Chord Ear Training, with small words like and, or and of left lowercase. Italian titles keep sentence case. Search results use the same names.
- Collapsing header in modules: the title lifts away like on the main tabs, so it no longer hangs below the bar. The bar now fades out softly instead of ending in a hard line, the timer sits right under the buttons, and the small screen name in the collapsed bar is gone.
- Entering a module: the streak and search buttons leave at once instead of fading under the Back button.
- The collapsed header's fade is short now. It ends right under the session timer instead of reaching far down the screen.
- Header titles no longer flash between screens. Entering a folder showed the folder subtitle for a moment before the "Home › Tools" trail replaced it. Titles also now swap while fully faded out, so the new title no longer pops in over the old one.
- The Back button stays solid when you go from a folder into a module and back. It used to dip to about 40 percent because it faded together with the title.
- Metronome tempo wheels only react to sideways swipes. A vertical swipe scrolls the page and leaves the tempo alone.
- Fixed the header buttons snapping when you enter a module from the chooser or open a sheet. The pinned header now holds still while the page locks.
- Folder screens now show a breadcrumb (Home, then the tab) under the title. The Back button and the level chip now take the color of the tab you are in.
- Collapsing header: the button row and the session bar stay pinned while you scroll, and the row no longer jumps when the collapse starts. The big title lifts away from the first pixel of scroll, a bar settles in behind the pinned rows, and the screen name slides up next to the session timer, so the bar always shows where you are. It reverses near the top. Module screens keep their title in the row.
- Smoother first run: the practice sheet is prepared in the background, so its first open is as smooth as the later ones. Screen names ease in when you switch tabs or open a folder, and the Back button slides in.
- The progress menu (tap the level chip) now opens with a fading scrim, a card that unfolds from the chip corner, parts that rise in one after another and an XP bar that fills. It closes with a short reverse. The full-screen background blur behind it is gone.
- Level ups now get the full chip treatment too: a bounce, a ring, a light sweep and the number popping in.
- Level chip: the XP popup now opens with a ring that expands out of the chip, a soft light that crosses it, and the number landing a beat before the XP label. Level ups get a bigger ring.
- Header buttons no longer use a background blur. It forced the phone to redraw the blur every frame on the Tuner and Metro, and it was a big part of the slowdown.
- Practice sheet polish: it slides up with a soft spring, its parts rise in one after another, the day circles pop in, and the achievements bar fills. Months slide when you change them, and the calendar always shows six weeks, so the sheet no longer jumps in height. Dragging the handle moves the backdrop with it, and a quick flick closes the sheet.

## v1.0.1: Piano that recovers, a rebuilt Chordle picker, fairer rhythm grading, quiz fixes

- Piano and Rhodes: if the shared sound path ever picked up bad audio data,
  both went silent for the rest of the session while the organ kept working,
  and the song bank still lit its keys with no sound. The path now checks
  itself while you play and rebuilds when it finds the fault, so you lose one
  note instead of the session. Opening the Piano or Rhodes tab also starts a
  clean path every time.
- Chordle, picker: one screen instead of two swipe cards. Pick a root (I to
  VII, plus a flat row on Medium and up), pick a quality (major, minor, dim,
  aug, sus), then confirm. The extensions under it change with the quality:
  minor offers m7 and m9, major offers 7, maj7 and the rest. The case of the
  numeral follows the quality, so there is no separate major row and minor
  row, and every flat chord can be minor. Each button shows the exact chord it will enter, chords you
  have ruled out are struck through. Before, the flat chords hid behind a
  toggle that only appeared after you picked a numeral, so a flat-heavy answer
  looked like the picker had run out of options.
- Chordle, previews: the picker drawer has a play button that plays the
  answer chord for the slot you are filling, led by a short tonic note, and a
  ROOT button for the tonic alone. Tapping a guessed chord, or a green locked
  one, plays the answer for that spot too. It never plays your own pick, so you
  cannot guess by ear. You no longer have to play the whole line every time.
- Chordle, drawer feel: the drawer slides up and fades in instead of popping.
  Buttons stay in place and change state, extension chips ease in when you
  change the quality, the chosen chip and the confirm button pop, and a chord
  you place pulses into its tile. Tiles show the numeral large with the suffix
  small underneath, so long names like bIImaj7 or bVII7 fit on small phones.
  Phones set to reduce motion get none of it.
- Chordle and Diadle, more polish: both drawers now slide away as well as in,
  and you can swipe them down by the handle or the header. The confirm button
  and the edge buttons no longer grow past the drawer sides when they pop.
  When you submit a guess, its tiles flip over one after another. Diadle's
  drawer got the same treatment: its degree buttons ease in, your current pick
  is highlighted, the header shows the slot and your pick on one line, and a
  placed note pulses into its tile. The "natural / altered" captions and the
  "tap a degree to hear its name" line are gone, since a tap places the note.
- Drums, accuracy pass over all 78 presets and the fills. Trap and Trap 32nds
  had the snare on 2 and 4; trap at 140 is half-time, so the snare now sits
  alone on beat 3 (the kick that shared that beat moved off it). UK Garage had
  its snare on the "+" of 2 and the "a" of 3; 2-step puts it on 2 and 4, at
  128 BPM with a heavier swing, and the kick is now a syncopated figure instead
  of one that landed on the backbeat. 8th Rock had the kick on beats 2 and 4
  under the snare; it now plays 1, 3 and the "and" of 3. Basic House had its
  first open hat a sixteenth late, on the "a" of 2; it is now on the "and".
  The fill called "Porcaro - Rosanna" was never a Rosanna fill, so it is now
  "Shuffle Fill". Copeland Style and Beauford Style stay, and their notes say
  they are style sketches and not transcriptions. The Rosanna Groove note
  described an older triplet version; it now matches the swung-sixteenth
  pattern that is actually in the preset.
- Chordle, ruled-out marks: a numeral was struck out when every guess of it
  scored gray, but gray only means wrong for that spot, so the true answer
  could get struck out. The marks now follow what each slot really proves. If
  a slot shows the right root with the wrong quality, the drawer opens with
  that root already chosen.
- Chordle, sound: inversions (/3, /5, /7) now put the right note in the bass,
  and 7#11 now plays its #11.
- Chordle, sound: minor chords written as a lowercase numeral (ii, iii, iv,
  vi, i) played as major chords, so the chord you heard did not match the
  numeral on screen. They now play as minor. The flat ii chord also played on
  the wrong root. Both are fixed.
- Chordle, custom games: the random line generator could build chords the
  picker could not spell (iim, iiim, vii°°, vii°ø7), which made some lines
  impossible to win. It now spells them the way the picker does, and Medium has
  a half-diminished seventh type.
- Rhythm Reading: a player who taps a little early or late all the way
  through no longer gets red notes for notes they hit. The grader used to
  decide which tap belonged to which note before it allowed for that lean, so
  on fast notes a tap could be handed to the neighbor. It now allows for the
  lean first. A note you really skip still shows one red. Taps that land
  inside a rest are judged with the same allowance.
- Rhythm Reading: during the listen phase and the count-in the tap box was
  dimmed like a disabled control. It now stays bright and still ignores taps,
  so it reads as "wait" and not "broken". Pausing still dims it.
- Music Quiz: on some screen widths the correct answer card spilled its text
  out of the box when you answered. The card keeps the same text area before
  and after the reveal, and the text size is checked again once the fonts load.
- Music Quiz, Theory: questions that name a minor key now say harmonic
  minor, because the fifth and seventh chords are only major and diminished
  there. The explanation reads "Degree 5 of D harmonic minor is a major
  triad." The Italian text says the same.
- Drums: Trap 32nds had hi-hat hits scattered on odd 32nd steps in no pattern,
  which sounded like a stutter. It is now a steady 16th-note hat with a pair of
  32nds at the end of beat 2 and a four-note roll at the end of beat 4.
- Drums: the moving step highlight no longer searches the whole screen on
  every step, which should keep fast patterns like Trap 32nds smooth on
  slower phones.

## v1.0.0: Intonare 1.0

- First public release on Google Play and the App Store.
- The version number moves from the 0.210 dev series to 1.0.0. The app,
  Google Play and the App Store now all show the same number.
- Settings: the Text Size and Master Volume sliders move only when you drag
  them sideways or tap and let go. A vertical swipe that starts on a slider
  scrolls the panel and leaves the slider where it was.
- Survival Guide: the info panel no longer resets when you scroll down to
  read it; only a real tap somewhere else closes it. The part name label now
  opens in place instead of jumping under your finger.
- Chords: the row of other names for a chord no longer clips its chips or
  scrolls up and down inside itself.
- Music Quiz: Survival pack tiles use the same colors as Quick Play, and the
  START SURVIVAL button is gone. Pick a pack, then start from its card.
- Explorer achievement: it now needs a real session in all seven exercises
  (answers or finished rounds), not just opening them. The text says seven,
  to match what it checks.
- Largest text size: Chordle's picker fits the screen (the right-hand
  buttons and CONFIRM were cut off), Road Trip's mode cards grow instead of
  clipping, and the range and design buttons stack so their names fit. When
  the cards are taller than the screen they scroll, and START THE DRIVE stays
  on the bottom edge.
- Drums: the ride bell is about 5 dB quieter on the standard and latin kits
  and 3 dB on jazz, so it sits a little above the ride instead of over the
  crash. The cowbell is 5 dB quieter and now sits under the snare.

Releases before 1.0 are not listed here.
