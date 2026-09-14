#!/usr/bin/env python3
"""
Intonare Regression Sentinel
============================
A spot-check that every previously-completed fix is STILL PRESENT in the file.

Why this exists: the instrument audit checks data *structure* (array lengths,
registration). It never noticed when behavioural fixes — the long-press guard,
the games-folder header, the embouchure min-height, quiz answer pairings —
silently vanished during a reset-and-reapply pass. Those are the regressions
that keep biting. This script codifies the "treat completed fixes as locked"
rule: each entry is a fix we made, plus a signature string that must appear in
the file. If a signature goes missing, the fix regressed — and you find out in
two seconds instead of by stumbling on it weeks later.

Usage:
    python3 intonare_regression_sentinel.py Intonare.html

Exit code 0 = all fixes present. Non-zero = something regressed.

Maintenance: when you complete a new fix that's the kind of thing that could
silently regress, add a CHECKS entry for it. Keep signatures SPECIFIC enough
that an unrelated edit won't accidentally satisfy them, but not so brittle that
reformatting whitespace breaks them. Prefer a distinctive token (a function
name, a unique string literal, a specific magic number) over a whole line.
"""
import sys, re, argparse

# Each check: (area, description, kind, signature, min_count)
#   kind 'sub'    -> plain substring must appear >= min_count times
#   kind 'regex'  -> regex must match >= min_count times
#   kind 'absent' -> substring must NOT appear. Pins a deletion, so a revert
#                    that drags dead code back in fails the gate. min_count is
#                    ignored; pass 0 to keep the row shape.
# Keep descriptions phrased as the BEHAVIOUR that breaks if the signature is gone.
CHECKS = [
    # ── App-wide UI guards ────────────────────────────────────────────────
    ('UI', 'Long-press does not select text / pop selection callout',
        'sub', '-webkit-touch-callout: none', 1),
    ('UI', 'Text inputs still allow typing/paste (selection re-enabled)',
        'sub', 'user-select: text', 1),
    ('UI', 'Games folder does not show a redundant second header',
        'sub', '#gamesHub .train-header', 1),
    ('UI', 'Embouchure text never resizes the note card (fixed min-height)',
        'sub', 'min-height:78px;display:flex;align-items:center;justify-content:center', 2),
    ('UI', 'Background does not scroll/bounce behind Survival Guide',
        'sub', 'body.sg-open', 1),
    ('UI', 'Dynamic nav-bar height var (bottom-sheet positioning)',
        'sub', '--nav-bar-h', 5),
    ('UI', 'Dynamic header height var',
        'sub', '--header-h', 1),

    # ── Wind instruments / ocarina ────────────────────────────────────────
    ('WIND', 'Out-of-range notes are disabled in the wind note grid',
        'sub', 'Out of range for this instrument', 1),
    ('WIND', 'Ocarina C5 home fingering = verified all-main-closed pattern',
        'sub', '[1,1,1,1,0,0,1,1,1,1,1,1]', 1),
    ('WIND', 'Ocarina fingerings cite their source (not invented)',
        'sub', 'pureocarinas.com', 1),

    # ── Tónale ────────────────────────────────────────────────────────────
    ('TONALE', 'Guess wave tints to score colour on reveal',
        'sub', 'tonaleCmp.colorResolved', 1),
    ('TONALE', 'CSS-var-to-concrete colour resolver present',
        'sub', 'function tonaleResolveColor', 1),
    ('TONALE', 'Per-round breakdown on final score screen',
        'sub', 'function tonaleRenderBreakdown', 1),
    ('TONALE', 'Daily can resume mid-game after backing out',
        'sub', 'dailyInProgress', 1),
    ('TONALE', 'Pitch-memory interference/distractor playback',
        'sub', 'tonalePlayInterference', 1),

    # ── Diadle ────────────────────────────────────────────────────────────
    ('DIADLE', 'Loss screen reveals each degree + note',
        'sub', 'diadleAnswerReveal', 1),
    ('DIADLE', 'Correct slots carry over (locked) between guesses',
        'sub', 'diadleLockedSlots', 2),

    # ── Metronome / progression / audio ───────────────────────────────────
    ('METRO', 'Groove mute button syncs across views',
        'sub', 'metroMuteBtnGroove', 1),
    ('METRO', 'Tick uses prebaked Hann-windowed buffer (no GC pops)',
        'sub', 'Hann', 1),
    ('METRO', 'BPM wheel inertia uses windowed velocity (no direction flips)',
        'sub', '_computeReleaseVel', 1),
    ('METRO', 'Bar-boundary metro alignment helper present',
        'sub', 'startMetroAt', 1),
    ('METRO', 'Groove patterns use dynamic length (not hardcoded 16)',
        'sub', 'groovePattern.length', 1),
    ('PROG', 'Capo root-shift lives at top of voicing builder',
        'sub', 'gccVoicings', 1),
    ('PROG', 'Banjo roll engine present',
        'sub', 'BANJO_ROLL', 1),
    ('PROG', 'Mandocello distinct cache prefix (no shape collision)',
        'sub', 'MANDO_CELLO_OPEN_MIDI', 1),
    ('PROG', 'Sub-tab cold-open fix (_buildSubRow called directly)',
        'sub', '_buildSubRow', 1),
    ('PROG', 'Save-chart keepState flag (root restores correctly)',
        'sub', 'keepState', 1),
    ('AUDIO', 'Harp uses its own dedicated reference tone (not bell)',
        'sub', "_chartPlay('harp'", 3),
    ('AUDIO', 'Shared audio context (clock-drift fix)',
        'sub', 'getAudio()', 5),
    ('AUDIO', 'Harmonica pathMap keyed by MIDI not pitch-class',
        'sub', 'harmonicaPrimaryPath', 1),

    # ── i18n / system ─────────────────────────────────────────────────────
    ('I18N', 'STRINGS translation table present',
        'sub', 'const STRINGS', 1),
    ('I18N', 'Translation function t() present',
        'sub', 'function t(', 1),
    ('I18N', 'Language switch does not false-fire drumkit achievement',
        'sub', 'fromLangSwitch', 1),
    ('SYSTEM', 'Haptic default-ON migration landmark (drumkitVisited)',
        'sub', 'drumkitVisited', 1),
    ('SYSTEM', 'Permission flow: notif immediate, mic on first touch',
        'sub', '_reqMicPerm', 1),
    ('NAV', 'Tools tab can exit a tool folder',
        'sub', 'enterToolFolder', 1),
    ('NAV', 'Survival Guide measured-height var (in-flow layout)',
        'sub', '--sg-h', 1),
    ('UI2', 'Tooltip clean fade-out state',
        'sub', 'fading-out', 1),

    # ── Content landmarks (regression canaries for big data sets) ──────────
    ('QUIZ', 'Truss-rod question present (answer-pairing repair landmark)',
        'sub', 'truss rod', 1),
    ('QUIZ', 'Decades packs intact (noughties pack present)',
        'sub', 'noughties', 1),
    ('RHYTHM', 'Rhythm-reading rest renderer present',
        'sub', 'rrRestSvg', 1),

    # -- Sample engine integration (v0.31.x) --
    ('AUDIO', 'Keys scale play caps note duration to avoid overlap',
        'sub', 'pssStepDelay * 0.82', 1),
    ('AUDIO', 'Chord player sample-aware',
        'sub', '_samplePlay(toneId, freq, ctx, chain.gain, vol, dur, when)', 1),
    ('AUDIO', 'windSynth checks samples first',
        'sub', 'if (toneId && SampleEngine.isReady(toneId))', 1),
    ('AUDIO', 'Sample release tail present',
        'sub', 'releaseTail', 3),
    ('AUDIO', 'Instrument switch eagerly loads samples',
        'sub', '_loadInstSamples', 1),

    # -- Versioning --
    ('VERSION', 'Version stamp comment at top of file',
        'regex', r'INTONARE_VERSION:\s*\d+\.\d+\.\d+', 1),
    ('VERSION', 'Version JS const present',
        'regex', r"INTONARE_VERSION\s*=\s*'\d+\.\d+\.\d+'", 1),
    ('VERSION', 'Runtime version stamp element wired',
        'sub', 'smVersionStamp', 1),

    # ── Tours / help / teaching (the category that silently regressed once) ──
    ('TOUR', 'Press-and-hold-title launches the module tour',
        'sub', 'attachLogoHoldTour', 1),
    ('TOUR', 'Hold-title gesture skips hidden/missing targets safely',
        'sub', 'getClientRects().length === 0', 1),
    ('TOUR', 'Per-module tours block present (Object.assign onto TOURS)',
        'sub', 'Object.assign(TOURS', 1),
    ('TOUR', 'startTour resolves the open exercise to its own tour',
        'regex', r'currentExercise && TOURS\[currentExercise\]', 1),
    ('TOUR', 'Chord tool gets its dedicated tour (name-collision fix)',
        'sub', 'chordtool:', 1),
    ('TOUR', 'Welcome tour teaches the hold-title gesture (EN)',
        'sub', 'press and hold the title', 1),
    ('TOUR', 'Welcome tour teaches the hold-title gesture (IT)',
        'sub', 'tieni premuto il titolo', 1),
    ('HELP', 'Game-mode help content present (chordle/tonale)',
        'sub', 'HELP_CONTENT.chordle', 1),
    ('HELP', 'Sight-singing sub-control help defined (ss_mode)',
        'sub', 'HELP_CONTENT.ss_mode', 1),
    ('TEACH', 'Rhodes teaching hint is translatable (not hardcoded EN)',
        'sub', 'hint_rhodes_keys', 1),
    ('I18N', 'Vocal-range REFERENCE tab label is translatable',
        'sub', 'vr_tab_reference', 1),

    # ── Major features verified in the full-history audit (were untracked) ──
    ('AUDIO', 'Master volume gain registry (live slider updates)',
        'sub', '_masterGainRegistry', 1),
    ('AUDIO', 'Master volume setter present',
        'sub', 'setMasterVolume', 1),
    ('AUDIO', 'Organ uses one shared limiter chain (no per-note stacking)',
        'sub', '_getOrganChain', 1),
    ('AUDIO', 'Organ cross-manual drawbar isolation (onlyManual filter)',
        'sub', 'onlyManual', 1),
    ('AUDIO', 'Dual-manual organ lower drawbar bank',
        'sub', 'organDrawbarsLower', 1),
    ('PROG', 'Capo shows capo-friendly open shapes (gccApplyCapo)',
        'sub', 'gccApplyCapo', 1),
    ('PROG', 'Banjo display-slot remap (high-g on thumb side)',
        'sub', 'gccStringSlot', 1),
    ('PROG', 'Mandocello voicings engine present',
        'sub', 'mandocelloVoicings', 1),
    ('PROG', 'Harmonica path keyed by MIDI (correct octave highlight)',
        'sub', 'harmonicaPrimaryPath', 1),
    ('PROG', 'Bowed-strings chart panel present',
        'sub', 'csPanelBowed', 1),
    ('METRO', 'BPM scrub wheel drag tracking',
        'sub', '_swipeStartX', 1),
    ('METRO', 'Precise bar-boundary metro start (startMetroAt)',
        'sub', 'startMetroAt', 1),
    ('METRO', 'Groove name auto-fit helper',
        'sub', '_fitGrooveName', 1),
    ('TONALE', 'Daily progress saves on back-out',
        'sub', 'tonaleSaveDailyProgress', 1),
    ('TONALE', 'Daily resume restores mid-game',
        'sub', 'tonaleResumeDaily', 1),
    ('RHYTHM', 'Procedural meter generator (RR_GEN configs)',
        'sub', 'RR_GEN', 1),
    ('RHYTHM', 'Personal-best streak stat persisted',
        'sub', 'rrBestStreak', 1),
    ('SAVE', 'Chart save/restore snapshot present',
        'sub', 'svcSnapshot', 1),
    ('SAVE', 'Woodwind sub-type persisted across restore',
        'sub', 'wwSubType', 1),
    ('TUNER', 'A reference pitch system (432-444 + custom)',
        'sub', 'refPitch', 1),
    ('SPLASH', 'Splash waits for stable viewport before animating',
        'sub', 'startWhenStable', 1),
    ('SYSTEM', 'Local notifications wired (Capacitor)',
        'sub', 'LocalNotifications', 1),
    ('QUIZ', 'Reset-stats two-tap confirm (Android confirm() workaround)',
        'sub', 'mqResetStats', 1),
    ('NAV', 'Off-screen drawer transform clears nav bar',
        'sub', 'translateY(calc(100%', 1),
    ('UI', 'Language-agnostic data-len title sizing',
        'sub', 'data-len', 1),

    # ── Rhythm Flash Cards (rc/rct/rcd) ───────────────────────────────────
    ('FLASHCARDS', 'Secondary (sixteenth) beam is per-note with stubs, not a '
                   'full-width beam keyed off the first note in the group. '
                   'Regressing this makes 16ths beamed to 8ths render as 8ths.',
        'sub', 'function is16(idx){ return Math.abs(notes[g[idx]].d - 0.25) < 0.01; }', 1),
    ('FLASHCARDS', 'exitTool HIDES toolRhythmCards (omitting it lets the sub-hub '
                   'bleed over the tool on back-out)',
        'regex', r"'toolVocalRange','toolDrumkit','toolRhythmCards','toolGuitarChords'", 2),
    ('FLASHCARDS', 'Auto-centered evenness grading (median-bias removal) shared '
                   'by tap/test/drill',
        'sub', 'function rctGrade(', 1),
    ('FLASHCARDS', 'Test-mode click grid is continuous/even (each card lays only '
                   'count-in+tap bars; next card carries the read bar)',
        'sub', 'continuous, no overlap, no gap', 1),
    ('FLASHCARDS', 'Drill-to-mastery requires consecutive passes',
        'sub', 'RCD_NEED', 2),
    ('FLASHCARDS', 'Drill records NOTHING to rcStats (stays neutral)',
        'sub', 'neutral by design', 1),
    ('FLASHCARDS', 'Multi-select category model (set, not single string)',
        'sub', 'function rcCatKeys(', 1),
    ('FLASHCARDS', 'Test overlay is full-screen fixed (reserves header + nav)',
        'sub', 'var(--header-h, 56px) + 14px', 1),
    ('FLASHCARDS', 'Haptic on tap only (never on the metronome beat) in tap/test/drill',
        'sub', "typeof hapticLight === 'function') hapticLight();", 3),
    ('LIGHT', 'A lifted accent exists for card-borne use, one per light theme',
        'sub', '--accent-lift:', 4),
    # An empty bar track is --surface-2 on --panel with no border. When the two
    # were the same hex the track was invisible until it filled, in four places:
    # the quiz progress bar, the survival timer, the by-pack stats bars and the
    # Pitch Match track. Dark separates them by 2.1 L*; light needs 3.3 because a
    # recess hides more easily on white. These pin the collision back out.
    # The scheduler takes the perf branch and returns before it reads rh, lh,
    # ctls or tempoMap, so a perf song carrying any of them is data nothing can
    # execute. Clair de Lune's was the last of it, 4.8KB of rubato map for a
    # capture that already carries absolute ms per note.
    ('PIANO PERF', 'Clair de Lune keeps its capture and not the rubato map',
        'absent', 'tempoMap:[[0,50],', 0),
    # Advanced Theory selects by the CARD's level, not by which family list its
    # generator sits on. Reverting to the three lists puts hard back to four jazz
    # kinds and locks Enharmonic out of the pack entirely.
    ('QUIZ GEN', 'Rare scales are weighted, not just present',
        'sub', 'function mqWPick(a)', 1),
    ('QUIZ GEN', 'The exotic generator no longer stamps d:3 on a pentatonic',
        'absent', "var s = mqGPick(MQ_F_EXOTIC);", 0),
    ('QUIZ GEN', 'Advanced Theory rates the card, not the generator list',
        'sub', 'return mqCardLevel(q) === slot;', 1),
    ('QUIZ GEN', 'Every generator is in the pot for every slot',
        'sub', 'kinds: function () { return MQ_GEN_ALL; }', 1),
    ('QUIZ GEN', 'A kind on two family lists is not counted twice',
        'sub', 'return a.indexOf(f) === i;', 1),
    ('QUIZ GEN', 'Enharmonic can build the white-key pairs',
        'sub', "keyEn:'C\\u266f major'", 1),
    ('LIGHT', 'Bar tracks stay recessed under the panel: base',
        'sub', '--panel: #fdfdfe;', 1),
    ('LIGHT', 'Bar tracks stay recessed under the panel: tuner',
        'absent', '--surface-2: #ecf4ff; --panel: #ecf4ff;', 0),
    ('LIGHT', 'Bar tracks stay recessed under the panel: metro',
        'absent', '--surface-2: #faf3e0; --panel: #faf3e0;', 0),
    ('LIGHT', 'Bar tracks stay recessed under the panel: tools',
        'absent', '--surface-2: #e4faf2; --panel: #e4faf2;', 0),
    ('LIGHT', 'Bar tracks stay recessed under the panel: train',
        'absent', '--surface-2: #f5f1ff; --panel: #f5f1ff;', 0),
    ('FLASHCARDS', 'Flash Cards tour uses the new module-tour (fixed-card) style, '
                   'not the old spotlight style',
        'sub', "'drumkit','rhythmcards','cof'", 1),
    ('FLASHCARDS', 'Tuplet detection groups by whole-beat sum (draws UNEVEN swing '
                   'triplets like [2/3,1/3], not just three equal notes). '
                   'Regressing this makes SHUFFLE FEEL render as straight notes.',
        'sub', 'var nearWhole = function(s){ return Math.abs(s-1)<.04 || Math.abs(s-2)<.04; };', 1),
    ('FLASHCARDS', 'Swing tuplet draws a bracket but no straight connecting beam '
                   '(quarter must not beam to the eighth)',
        'sub', 'var beamTrip = tg.every(function(ix){ return notes[ix].d < 0.45; });', 1),

    # ══ QUIZ v2 ══════════════════════════════════════════════════════════
    # Everything below was built while v1 was still the shipping default and
    # is unprotected until now. It is pinned before the v1 cut, so that
    # removing a guard or a selector that these depend on fails the gate
    # rather than quietly reverting a day of work.
    ('QUIZ v2', 'The v1 quiz switch is gone; v1 cannot be turned back on',
        'absent', 'MQ_V2', 0),
    ('QUIZ v2', 'The version stamp carries no hidden gesture',
        'absent', '_bindQuizV2Hold', 0),
    ('QUIZ v2', 'The v1 feedback sheet stays deleted, markup and CSS both',
        'absent', 'mq-fb-', 0),
    ('QUIZ v2', 'Nothing reaches for the deleted v1 feedback elements',
        'absent', 'mqFb', 0),
    ('RHYTHM READ', 'The renamed difficulty picker has no second dead builder',
        'absent', 'rrDiffGrid', 0),
    ('QUIZ v2', 'Question transition: exit, then the question, then the answers',
        'sub', 'var first = root.classList.contains(\'mq2-fresh\')', 1),
    ('QUIZ v2', 'A fresh round builds the whole band from empty',
        'sub', 'mq2-fresh', 4),
    ('QUIZ v2', 'The band is hidden until the question is built, so no stale rule colour shows',
        'sub', '.mq2.mq2-fresh .mq2-band { opacity: 0; }', 1),
    # Repinned v0.201.129. The old frame was 54% x 150px, a landscape box holding
    # portrait artwork, so every mark letterboxed inside it and floated with dead
    # space either side. The frame is bigger than the art now and crops it.
    # The motif entrance must not animate the motif's own opacity: mq2BandIn ends
    # at 1 and fill-mode both beats a declaration, so the mark held at full
    # strength through the entrance and dropped to its tier when the class came
    # off. Shipped once and read as "dark, then fades".
    ('QUIZ v2', 'The motif entrance fades the wrapper, never the tier opacity',
        'sub', '.mq2.mq2-arrive .mq2-motif > div { animation: mq2MotifIn', 1),
    ('QUIZ v2', 'Nothing animates mq2BandIn onto the motif itself',
        'absent', '.mq2.mq2-arrive .mq2-motif { animation: mq2BandIn', 0),
    # Note names run A to G, so 12.4% of generated questions had an option whose
    # text was A, B, C or D sitting beside a badge of the same letter, and the
    # fretboard questions label their dots A to D on top of that.
    # The dot is filled with `accent`, which is var(--text): near-white on a dark
    # band and near-black on a light one. A fixed dark label read fine in dark and
    # vanished in light, near-black type on a near-black dot. Measured after the
    # fix: 14.8:1 dark, 10.7:1 light.
    # The chip was painted inline in two places, both AFTER an answer, so a new
    # round showed the previous round's count until the first question was
    # answered. One painter, called from both starts as well.
    # The boot applyLang() is an inline script; ~29,000 lines of markup come after
    # it, including the whole Music Quiz, so it relabeled a document that did not
    # contain them yet. An Italian user booted into English QUIT, "Did you know?",
    # results labels and Quick Play titles. Measured: 106 stale before, 0 after.
    ('I18N', 'applyLang runs again once the document has finished parsing',
        'sub', "document.addEventListener('DOMContentLoaded', function () {\n    try { applyLang(); } catch (e) {}\n  }, { once: true });", 1),
    ('QUIZ v2', 'The streak chip is painted from state in one place',
        'sub', 'function mqPaintStreak()', 1),
    ('QUIZ v2', 'Nothing writes the streak chip class inline any more',
        'absent', "chip.className=MQ.streak>=2?'mq-streak-chip'", 0),
    ('QUIZ v2', 'A fretboard dot label contrasts with its own dot in both modes',
        'sub', "(d.hollow ? accent : 'var(--surface)')", 1),
    ('QUIZ v2', 'No fixed near-black left on a diagram that flips with the theme',
        'absent', '#0d0f12', 0),
    ('QUIZ v2', 'The key badge is dropped when every answer is a letter or two',
        'sub', "grid.classList.toggle('nokeys', _bare)", 1),
    ('QUIZ v2', 'A keyless tile centers its answer rather than clearing a missing badge',
        'sub', '.mq2-grid.nokeys .mq2-opt { align-items: center', 1),
    ('QUIZ v2', 'Pack mark bleeds off two edges rather than floating in a box',
        'sub', 'top: -10px; right: -18%; width: 62%; height: 230px', 1),
    ('QUIZ v2', 'Pack mark fills its frame and is cropped by it, never letterboxed',
        'sub', "preserveAspectRatio=\"xMidYMid slice\"", 1),
    ('QUIZ v2', 'The five heavy marks sit a tier below the line-work ones',
        'sub', '.mq2.pk-advanced_theory .mq2-motif { opacity: .30; }', 1),
    ('QUIZ v2', 'The pack is named on the root, so a rule can address one pack',
        'sub', "root.className = 'mq2 pk-' + q.pack", 1),
    ('QUIZ v2', 'The 80s fill meets the horizon at 72 rather than floating above it',
        'sub', 'y=\"72\" width=\"120\" height=\"88\"', 1),
    ('QUIZ v2', 'The 80s mark fades at the sides instead of stopping on a straight edge',
        'sub', 'mask id=\"m8m\"', 1),
    ('QUIZ v2', 'Answer feedback has its own colours, not the tuner inks',
        'sub', '--fb-ok: var(--in-tune); --fb-no: var(--sharp);', 1),
    ('QUIZ v2', 'Light mode gets mid-tone feedback colours rather than text inks',
        'sub', 'body.light .mq2 { --fb-ok: #1f8a3b; --fb-no: #c62828; }', 1),
    ('QUIZ v2', 'The wash fades in place and does not travel up the band',
        'sub', '@keyframes mq2WashIn', 1),
    # The CSS surviving is no use if the element it styles is cut with the v1
    # markup around it, which is how the hearts container came to be shown and
    # empty in the first place.
    ('QUIZ v2', 'The wash layer is in the band markup, not only in the stylesheet',
        'sub', '<div class="mq2-wash"></div>', 1),
    ('QUIZ v2', 'The rule effect layer is in the band markup',
        'sub', '<div class="mq2-rulefx"><i></i></div>', 1),
    ('QUIZ v2', 'The hearts container is in the band markup',
        'sub', 'id="mq2Hearts"', 1),
    ('QUIZ v2', 'The game over marker is in the band markup',
        'sub', 'id="mq2Over"', 1),
    ('QUIZ v2', 'Right and wrong differ in rhythm: a spread against a stepped flicker',
        'sub', 'steps(1, end)', 1),
    ('QUIZ v2', 'Both outcomes start from an empty rule',
        'sub', '.mq2.r .mq2-band, .mq2.w .mq2-band { border-bottom-color: transparent; }', 1),
    ('QUIZ v2', 'The score counts up rather than jumping',
        'sub', 'function mq2CountTo(el, to, ms)', 1),
    ('QUIZ v2', 'Survival hearts render in the v2 band, not only in the v1 bar',
        'sub', 'function mq2RenderHearts(lostIndex)', 1),
    ('QUIZ v2', 'The hearts renderer is actually called; defining it is not enough',
        'sub', "if (MQ.mode === 'survival') mq2RenderHearts();", 1),
    ('QUIZ v2', 'The spent heart pops when a life is lost',
        'sub', 'mq2RenderHearts(MQ.lives);', 1),
    ('QUIZ v2', 'Survival hearts match the ear training rack',
        'sub', '.mq2-heart.filled', 1),
    ('QUIZ v2', 'The fatal answer still reveals before the run ends',
        'sub', 'mq2Reveal(idx, dispAns, correct);\n        mqShowFeedback(false, q, true);', 1),
    ('QUIZ v2', 'Losing the last life is announced on the band, not by a button label',
        'sub', 'mq_survival_over', 3),
    ('QUIZ v2', 'Custom is a child of the panel, like the other two pickers',
        'sub', "if (_p && _c && _c.parentElement !== _p) _p.appendChild(_c);", 1),
    ('QUIZ v2', 'The picker sheets carry no scrim, so the landing does not flash on return',
        'sub', 'body.mq2on #mqQuickSheet,\n  body.mq2on #mqSurvivalSheet { background: none;', 1),
    ('QUIZ v2', 'The topbar stays while a holdover is showing, so the landing does not reflow',
        'sub', "var holdover = document.querySelector('.mq-screen.mq2-holdover');", 1),
    ('QUIZ v2', 'Stats sheet uses pack icons, not an emoji fallback',
        'sub', "mqPackIcon(k, 16)", 1),
]

# ── EXACT-VALUE PINS ──────────────────────────────────────────────────────
# Unlike CHECKS (presence), these assert a SPECIFIC value. They catch silent
# DRIFT — a reapply pass bringing a tweak back at the wrong number (78px→72px).
# Cost: when you deliberately change one of these, you must update the pin here,
# or it will (correctly) flag your intentional change. Keep this list SHORT —
# only values that genuinely matter and that you want frozen.
#
# Each: (area, description, must_appear_substring, must_NOT_appear_list)
#   must_NOT entries catch the common wrong-value the drift would introduce;
#   leave the list empty if you only want to assert the exact value is present.
EXACT_PINS = [
    # ── Locked packs must not reach a selection (v0.201.11) ───────────────
    # `Object.keys(PACKS)` counts packs that cannot be dealt from, and the same
    # line written in three places caused three separate bugs: the survival
    # guard let you deselect every playable pack, the tile counts overstated,
    # and select-all highlighted coming-soon packs that then dealt nothing.
    # Each of the three now filters through mqPackReady. If one loses its
    # filter, this catches it.
    ('MUSIC QUIZ', 'select-all takes only playable packs',
        'var ready = Object.keys(PACKS).filter(mqPackReady);',
        ['else MQ.selectedPacks = new Set(Object.keys(PACKS));']),
    ('MUSIC QUIZ', 'the pack hint counts only playable packs',
        "var total = Object.keys(PACKS).filter(mqPackReady).length;",
        ['var n = MQ.selectedPacks.size, total = Object.keys(PACKS).length;']),
    ('MUSIC QUIZ', 'survival cannot be emptied of playable packs',
        'MQ.survivalPacks.forEach(function (p) { if (mqPackReady(p)) readySel++; });',
        ['if (MQ.survivalPacks.size <= 1 && !MQ.survivalOnlineCatSelected) return;']),

    # ── Five songs signed off on-device (v0.115.0) ────────────────────────
    # Hand-tuned legs. If RT_TUNED empties out, the tuner starts badging them
    # again and the work reads as undone.
    ('ROADTRIP', 'The five tuned songs are signed off',
        "'clair_de_lune',\n  'prelude_em',\n  'moonlight',\n  'liebestraum',\n  'fuer_elise',", []),
    # The RT_JOURNEY bpm copies were stale on fourteen entries. Nothing read
    # them, which is why it went unnoticed for months.
    ('ROADTRIP', 'RT_JOURNEY bpm copies match the songs',
        'alla_turca:{tier:\'hard\',bpm:120,', ["alla_turca:{tier:'hard',bpm:100,"]),
    # ── Leg tuning survives a reload (v0.114.8) ───────────────────────────
    # The tuner edited RT_JOURNEY in memory and nothing else, so a reload, a
    # crash or a fresh build threw an entire session away without ever saying
    # so. Edits are written on every change and applied back at module load, so
    # a tuned leg actually plays tuned rather than only reading tuned in the
    # panel. If this write is ever removed the loss is silent again.
    # The save has to come AFTER the ms recompute. Saving first stored the new
    # b and s against the OLD ms, so a restored perf leg would have shown the new
    # position and played the old one.
    ('ROADTRIP', 'Leg tuner saves after the ms recompute, not before',
        'if(isPerf(id)) h.ms=Math.max(0, Math.round(h.b*(60000/bpm)));\n',
        ['h.s=Math.round(s*100)/100;\n    rtTuneSave();']),
    ('ROADTRIP', 'Saved tuning is applied at module load',
        'if (name === \'roadtrip\') { try { rtTuneRestore(); } catch (e) {}', []),
    # ── The leg tuner's EXPORT was copying nothing (v0.114.7) ─────────────
    # document.execCommand('copy') inside a try/catch that swallowed the
    # failure, on a readonly textarea, which the Android WebView will not
    # select. The button looked like it worked every single time and the
    # clipboard stayed empty. navigator.clipboard first, execCommand as a
    # fallback with readonly lifted for the selection, and the label reports
    # which one happened instead of assuming.
    ('ROADTRIP', 'The leg tuner export really copies',
        'navigator.clipboard.writeText(out).then(function(){ say(\'COPIED\'); }).catch(legacy);',
        ["ta.select();\n        try{ document.execCommand('copy'); }catch(e){}"]),
    # ── One hold, one gesture (v0.114.6) ──────────────────────────────────
    # The leg tuner had been on a 600ms long-press of the ROADTRIP title since
    # it was built. Putting the tour replay on the same element at 500ms meant
    # one press fired both, the tour and then the tuner on top of it. The tour
    # keeps the title; the tuner moved to the INTONARE brand pill at 900ms.
    ('LAYOUT', 'The leg tuner is off the Road Trip title',
        "const title=document.querySelector('#exRoadTrip .rt-brandpill');",
        ["const title=document.querySelector('#exRoadTrip .rt-menu-title');\n  if(!title || title.dataset.tunerBound)"]),
    # ── A full-screen module needs its own hold target (v0.114.5) ─────────
    # Every tour replays by pressing and holding the app title. Road Trip draws
    # its own chrome over the header, so the title is still in the DOM, still
    # reports visible, and is covered -- elementFromPoint lands on a difficulty
    # chip. Its tour could fire once and never again. Music Quiz already had
    # this and already had the fix; Road Trip now has the same one.
    ('LAYOUT', 'Road Trip binds hold-to-replay on its own title',
        'function rtBindTitleHold() {', []),
    # ── The mode switch is on every screen (v0.114.4) ─────────────────────
    # Moving it into the card head put it on practice and on the climb's GAME
    # card and nowhere else, so once you reached the climb's intro or its result
    # there was no way back to practice. A switch that vanishes inside one of
    # its own modes is worse than the row of slabs it replaced.
    ('RELPITCH', 'The mode switch is on the intro and the result too',
        "'<div class=\"rlp-head\"><div>' + rlpSeg() + '</div></div>' +\n      '<div class=\"rlp-vu\" id=\"rlpIntroVu\">'", []),
    ('RELPITCH', 'Road Trip has a tour',
        "  roadtrip: [\n    { selector:'.rt-diffstrip'", []),
    # ── Tours cover the modules that shipped (v0.114.2) ───────────────────
    # Thirty tours existed and five exercises had none, including both modules
    # shipped this month. Nobody was maintaining the list as things landed.
    # maybeAutoTour keys off TOURS, so an entry wires the first-run prompt by
    # itself -- which is also why the gap was invisible.
    ('LAYOUT', 'Relative Pitch and Staff Notes have tours',
        '  relpitch: [\n    { selector:\'#rlpTabs\'', []),
    # The mode switch uses the app's own segmented control rather than a pair of
    # full-width slabs this module invented for itself.
    # The switch lives in the card head, where the title used to say PRACTICE --
    # which the switch was already saying one row above it.
    ('RELPITCH', 'The mode switch is the shared segment, in the card head',
        "function rlpSeg() {",
        ['<button class="rlp-tab on"', "t('rlp_head_practice')"]),
    # ── Lifelines are three for the climb, not three a band (v0.114.1) ────
    # They used to refresh at every band edge: twelve across a run at 0.08 of
    # the multiplier each, so spending every one still settled at x1.04. That is
    # not a cost, it is paperwork -- and a resource that refills cannot be
    # hoarded, so the only interesting decision never came up. Three total at
    # 0.25 each: the full set is worth three quarters of the multiplier.
    ('RELPITCH', 'Lifelines do not refresh at a band edge',
        'if (nb !== rlpCurBand) {\n      rlpCurBand = nb;\n      rlpBandReplays = RLP_BAND_REPLAYS;',
        ['rlpLives = { a440:false, fifty:false, bw:false }; rlpBandReplays = RLP_BAND_REPLAYS; }']),
    ('RELPITCH', 'A lifeline costs a quarter of the multiplier',
        'RLP_MULT_STEP = 0.25', []),
    # ── The clean summit achievement (v0.114.0) ───────────────────────────
    # 24 rungs, no lifeline, multiplier still on 2.0, 200,000 settled. Checking
    # the payout alone would let a helped run that happened to bank the same
    # figure through, so the multiplier is part of the condition.
    ('RELPITCH', 'A clean summit is its own achievement',
        "id:'clean_summit'",
        ["(s.stats?.relpitch?.ch?.best||0) >= 200000 }"]),
    ('LIGHT', 'The ladder golds are fills, not ink',
        'background:#d9a621;', ['background:#c9932a;']),
    # ── Secondary ink is re-declared inside a card (v0.113.8) ─────────────
    # The ink audit's real finding was not that anything was too dark alone but
    # that the three levels had collapsed: on a card, text 11.9 / dim 10.2 /
    # muted 9.6, barely two points across three steps meant to be obvious.
    # They cannot just be lightened, because the same tokens carry text on the
    # GROUND where they are already near the AA floor -- so they are redeclared
    # inside .card and inherited, and --ink-tight keeps the ground value
    # reachable for the few sub-10px labels that still need it.
    ('LIGHT', 'Cards redeclare the secondary ink levels',
        'body.light.theme-tuner .card, body.light.theme-tuner .ce-stats-content,', []),
    ('LIGHT', 'A tight ink stays reachable inside a card',
        '--ink-tight: #2d4058;', []),
    # ── Ink is pinned for the card, not the floor (v0.113.7) ──────────────
    # Body ink at 7:1 against the FLOOR lands at 13.8-14.6:1 on a CARD, and
    # almost everything in this app is read on a card. Past AAA by a long way,
    # and it is what made light feel heavy element by element rather than in any
    # one place. 5.6 / 4.8 / 4.55 on the floor; 11.4 / 9.9 / 9.5 on a card.
    ('LIGHT', 'Body ink is softened for the ground it is actually read on',
        '--text: #263343; --text-dim: #2c3d55; --muted: #2d4058;',
        ['--text: #172332; --text-dim: #23344b;']),
    # Right and wrong are the two states you look straight at, and both were
    # wearing floor-pinned status ink on a near-white card.
    ('RELPITCH', 'Answer keys use the lifted status colours in light',
        'body.light #exRelPitch .rlp-key.right {', []),
    # ── Dark chooser cards emit too (v0.113.3) ────────────────────────────
    # The whole language of the dark theme is emission, and the chooser was the
    # one screen not speaking it. Weaker and tighter than the light version: a
    # glow on near-black reads at much lower alpha before it turns to fog.
    ('DARK', 'Chooser cards cast their own light in dark too',
        'body:not(.light) .lnch-cell::before {', []),
    # ── Equal perceptual weight, warm ground (v0.113.2) ───────────────────
    # Mixing a fixed percentage of each module colour into white looks even and
    # is not: the four sources run C .121-.154 and L .769-.880, so tools came
    # out heaviest and metro lightest. Faces are built at matched L and matched
    # C per stop, inheriting only the hue -- equal perceptual distance from
    # neutral is what makes a set read as a family instead of four swatches.
    ('LIGHT', 'Chooser faces are built at matched lightness and chroma',
        '--lf-top:#afe9f8; --lf-mid:#caf2fc;',
        ['color-mix(in srgb, var(--lc) 26%, #ffffff) 0%']),
    # An overcast sky IS a cool grey. The ground sat at hue 260 with C .005,
    # which is the dead zone where a tint reads as an accident. Warm hue, enough
    # chroma to register as a decision, and lifted.
    # Paper: the ground is 1.05:1 from a card's lit top edge, so value no longer
    # holds the grid at all -- the rim, the contact shadow and the pool do. Any
    # of the three getting softened again and the cards dissolve into the page.
    ('LIGHT', 'The chooser ground is paper, and the cards are held by edge',
        'linear-gradient(174deg, #f0ede7 0%, #e8e4dd 55%, #e0dbd3 100%);',
        ['#cbc5bd 52%', '#a8abbe;']),
    ('LIGHT', 'Chooser cards carry a rim firm enough for paper',
        'color-mix(in srgb, var(--lc) 55%, rgba(112,116,132,.62))', []),
    # ── The light screen must not flash black (v0.112.10) ─────────────────
    # brightness(.25) is an unlit display on a near-black panel and a black
    # rectangle on a near-white one, so the light entrance was flashing a screen
    # that belongs to the other theme. Light gets its own compressed range.
    ('RELPITCH', 'The light entrance flicker stays light',
        '@keyframes rlpFlickLight {', []),
    # Titles are lifted with drop-shadow, which follows the glyph alpha. A
    # text-shadow paints under a transparent fill and shows straight through it,
    # so it cannot be used on background-clip:text.
    # One highlight and one shadow. Three shadows around a glyph, two of them
    # white, is an outline: the white bleeds inward at the stroke edges and eats
    # the contrast of the type it is meant to be lifting.
    ('LIGHT', 'Light titles get one highlight and one shadow, not a halo',
        'drop-shadow(0 -1px 0 rgba(255,255,255,.45))',
        ['drop-shadow(0 1px 0 rgba(255,255,255,.55))']),
    # ── Every exercise has a header tagline (v0.112.9) ────────────────────
    # Staff Notes had no entry in the map at all, and Relative Pitch borrowed
    # its CARD subtitle, which is written for a card and twice what the header
    # can hold -- which is why it truncated rather than fitting.
    # Split into two independent pins (v0.131.7). The original matched both
    # keys as one two-line literal, so it depended on them staying adjacent in
    # the map. Notation Cards landed between them and the pin cried wolf while
    # both taglines were perfectly fine. Each key now stands on its own.
    ('LAYOUT', 'Staff Notes has a header tagline',
        "staffread:  'hsub_staffread',", []),
    ('LAYOUT', 'Relative Pitch has a header tagline, not the card subtitle',
        "relpitch:   'hsub_relpitch'",
        ["relpitch:   'ex_relpitch_sub'"]),
    # ── Module header taglines are FITTED, never clipped (v0.132.1) ───────
    # setHeaderModule used to hand the title to _fitHeaderTitle, which finds its
    # available width by walking up to the first ancestor WIDER than the element.
    # In module mode the title sits in a flex row beside the italic subtitle, so
    # when it overflowed that row the walk stepped past it to the header and
    # reported a width the title did not have: Italian RICONOSCIMENTO ACCORDI
    # rendered 283px inside a 264px row and was clipped while the fitter called it
    # comfortable. It also never subtracted the subtitle, so the title was sized as
    # though it owned the whole row.
    ('LAYOUT', 'Module header uses its own fitter, not the section one',
        '_fitModuleTagline(tagline);',
        ["_fitHeaderTitle(tagline.querySelector('.hdr-mod-title'), tagline);"]),
    # The tagline is a flex ITEM and shrink-wraps its own text, so asking IT for the
    # available width says "as wide as what I already hold" and every subtitle looks
    # cornered. The first cut of this hid all 29 subtitles at 320px. Measure the row.
    ('LAYOUT', 'Module fitter measures the parent row, not the shrink-wrapped tagline',
        'var row = tagline.parentElement || tagline;', []),
    # A half-word plus an ellipsis reads as breakage; an absent flourish reads as a
    # decision, and the module's full description is on its card either way.
    ('LAYOUT', 'Over-long module subtitle is hidden outright, never ellipsed',
        "if (textW(sub) > room) sub.style.display = 'none';", []),
    # ── The header tagline is wiped before every write (v0.132.2) ─────────
    # #headerTagline is one element shared by every screen and modules write inline
    # styles onto it. Chordle paints it --in-tune green on a win and only its own
    # daily-reset clears that, so walking out to a folder carried the green along:
    # RHYTHM TRAINING with a lime subtitle, sampled off a real screenshot at #c1e095.
    # Inline beats every stylesheet rule, so the owners of the element wipe first.
    ('LAYOUT', 'setHeaderModule wipes leaked inline tagline styles before writing',
        '_resetTaglineInline(tagline);\n        var mlen = name.length;', []),
    ('LAYOUT', 'setHeaderSection wipes leaked inline tagline styles before writing',
        "{ _resetTaglineInline(tagline); tagline.textContent = (subKey", []),
    # ── Scales is a TOOL, not a Train module (v0.132.3) ───────────────────
    # It never called progUpdate, so it earned no XP and kept no stats; its own
    # subtitle reads "look it up · hear it · play along"; and a comment in the file
    # already called it "the Scales tool". It sat alone on the Train hub under an
    # "Explore" label that existed for nothing else. Now in Tools > Reference.
    ('LAYOUT', 'Scales is registered as a tool in the Reference folder',
        "intervalref: 'reference', scales: 'reference'",
        ["enterExercise('scales')", "scales: 'practice',"]),
    # The screen had to physically move out of .train-only, which CSS hides outside
    # the Train tab; leaving it there would have opened a blank tool.
    ('LAYOUT', 'The Scales panel is closed on tool exit',
        "'toolSurvivalGuide','toolTheremin','exScales'", []),
    # The favourites registry is keyed by string, so the pin key stays on its old
    # 'exercise:' prefix. Renaming it would silently drop the pin of anyone who had
    # starred Scales; tool:musicquiz in the Games hub is the same trick in reverse.
    ('LAYOUT', 'The Scales favourite keeps its old key and launches into Tools',
        "'exercise:scales':     { label: 'SCALES',      type: 'TOOL',",
        ["setMode('practice'); enterExercise('scales');"]),
    # Everything In Its Right Place asks you to visit every module. The visit key
    # went e:scales -> t:scales with the move, and anyone who had already been there
    # should not have to go again to re-earn it.
    ('LAYOUT', 'The all-modules achievement still honours the old e:scales visit',
        "(m === 't:scales' && progState.sesModulesVisited.includes('e:scales'))", []),
    # ── The scale name box is pinned AND fits (v0.132.4) ──────────────────
    # .scale-name-big was declared twice. The second copy, in the dead Scale
    # Reference block, set 40px/line-height 1 and won on order, so two lines needed
    # 80px in a 75px box before anything even wrapped to three. The real rule is
    # 36px/1.04, which is what makes 75px hold exactly two lines.
    ('LAYOUT', 'Only one .scale-name-big rule; the 40px duplicate stays dead',
        'font-size: 36px; letter-spacing: 2px; line-height: 1.04;',
        ['font-size: 40px; line-height: 1; letter-spacing: 2px;']),
    # Three-line names shrink to fit rather than being clipped through the middle.
    # Growing the box would defeat the pin, which exists so the tape below it does
    # not jump every time the scale changes.
    ('LAYOUT', 'Long scale names are fitted to the pinned box',
        'function scaleFitName(el) {', []),
    ('LAYOUT', 'scaleRenderName calls the fitter after the text swap',
        "el.textContent = txt; el.classList.remove('swap'); scaleFitName(el);", []),
    # ── Song transport reaches all three instruments (v0.132.5) ──────────
    # _riffScrubEls() returned a hardcoded pair of piano element ids, so organ and
    # Rhodes had play/pause and stop but no seek line on either surface. A hardcoded
    # list is a list that forgets the next instrument; query the class instead.
    ('LAYOUT', 'The scrubber finds its surfaces by class, not a piano-only id list',
        "document.querySelectorAll('.np-scrub').forEach(function(scrub){",
        ["var c = document.getElementById('pianoNpScrub');"]),
    ('LAYOUT', 'Organ has a seek line on the card and in the overlay',
        'id="organNpScrub"', []),
    ('LAYOUT', 'Rhodes has a seek line on the card and in the overlay',
        'id="rhodesNpScrub"', []),
    # Two call sites refreshed only the card pedal, so the Rhodes overlay pedal sat
    # still through an entire performance. The piano always did both.
    ('LAYOUT', 'Both Rhodes pedals refresh together',
        'function _rhodesRefreshPedals() {',
        ["var rp = document.getElementById('rhodesPedal'); if (rp && rp._refresh) rp._refresh(); }"]),
    # ── Every organ console control is reachable from song data (v0.132.7) ──
    # The driver handled five of twelve. The other setters existed and the save/restore
    # already covered their state; there was just no route from a song to them.
    ('AUDIO', 'Riff driver can reach organ percussion decay and volume',
        "if (what === 'percDecay'&& typeof setOrganPercDecay=== 'function') setOrganPercDecay(val);", []),
    ('AUDIO', 'Riff driver can reach both organ vibrato rockers',
        "if (what === 'vibLower' && typeof setOrganVibLower === 'function') setOrganVibLower(val);", []),
    # The volume rocker is the swell pedal in two steps, which is how an organist phrases.
    ('AUDIO', 'Riff driver can reach the organ volume rocker',
        "if (what === 'vol'      && typeof setOrganVolume   === 'function') setOrganVolume(val);", []),
    ('AUDIO', 'Riff driver can reach the organ hold latch and refreshes both pedals',
        "['organPedal', 'organFullPedal'].forEach(function(id){", []),
    # ── Seven Rhodes performances carry their pedalling again (v0.132.6) ────
    # They shipped with ped:[] on the theory that a Rhodes has its own sustain. It also
    # has a damper. The arrays came from the piano twins, whose notes are byte-identical.
    ('AUDIO', 'Rhodes performances are not shipped with empty pedal arrays',
        'ped:[{t:285,v:1}',
        ['// Pedal stripped (Rhodes has its own sustain); notes play through the Rhodes voice.']),
    # ── Performance pedal events go to the instrument that is playing (v0.132.8) ──
    # The perf scheduler hardcoded _riffPiano('pedal'), so a Rhodes performance moved
    # the PIANO's pedal on the other tab and left its own motionless. Restoring the
    # Rhodes pedal data was necessary and not sufficient; nothing delivered it.
    ('AUDIO', 'Perf pedal events dispatch by instrument, not always to the piano',
        "if (inst === 'rhodes' && typeof _riffRhodes === 'function') _riffRhodes('pedal', pv);",
        ["if (_riffActive && typeof _riffPiano === 'function') { try { _riffPiano('pedal', pv); } catch(e){} }"]),
    # stopAllRhodesDrones() silences every ringing note. Right for a human leaving drone
    # mode by hand, ruinous inside a performance where the pedal lifts 163 times.
    # ── The song picker never silently drops a group (v0.132.12) ──────────
    # _riffBuildList filtered its group order against RIFF_ERAS and rendered only
    # what survived, so any song in an unlisted group vanished from the picker while
    # still existing, loading, holding metadata and launching from a favourite.
    # Salsa Montuno was tagged era 'Afro-Cuban' and was invisible in the piano bank.
    ('LAYOUT', 'Unknown song-picker groups are appended, not dropped',
        "seen.forEach(function(g){ if (groupOrder.indexOf(g) === -1) groupOrder.push(g); });", []),
    # ── Groove picker light scheme (v0.133.7) ─────────────────────────────
    # The picker had no light override at all, so filled khaki cards sat on cream
    # and the step preview measured 1.37:1 — the pattern that distinguishes one
    # groove from another was effectively invisible. Grid takes the khaki, cards
    # become paper. All body.light scoped; dark mode untouched.
    # No khaki slab: a filled tan block dropped into a cream page reads as a mistake
    # rather than a surface. Cards separate on their own via border and shadow.
    ('LAYOUT', 'Groove grid has no filled ground in light mode',
        'box-shadow: 0 1px 3px rgba(120,100,50,.12);',
        ['body.light .groove-card-grid {\n    background: #c3b27b;']),
    # The header subtitle was the same colour as its own bar, near enough 1:1, so
    # "tap steps to edit" was an instruction nobody could read.
    ('LAYOUT', 'Groove pattern subtitle is legible in light mode',
        'body.light .groove-pattern-meta { color: #6f6244; }', []),
    # Step pips: on vs off measured 1.05:1, so you could see the squares but not
    # which were lit — the pattern you are editing was invisible.
    ('LAYOUT', 'Groove step pips distinguish accent, soft and off in light mode',
        'body.light .groove-step.gs-accent { background: #6b5408; border-color: #4a3a05;', []),
    ('LAYOUT', 'Groove step preview is legible in light mode',
        'body.light .gcp-step.on   { background: #8a6d10; }', []),
    # Selected reads as pressed in: warm wash, gold frame, inset glow on the top
    # edge. Outline and box-shadow only, so the grid cannot reflow on selection.
    # Softened in v0.133.9: the original was tuned against a khaki ground, and once
    # the slab went the same dark 2px frame read as harsh on cream. The bright cap
    # line is gone entirely — on a pale card it was the loudest part of the whole
    # treatment. Still outline plus box-shadow only, so no reflow on selection.
    ('LAYOUT', 'Selected groove card is softened, with no cap line',
        'inset 0 7px 9px -8px #a3842c;',
        ['inset 0 9px 10px -7px #8a6d10,', 'inset 0 2px 0 0 #c9a83c;']),
    # The editor is one recessed slate: header and step grid share a well, so the
    # lower half of the panel has depth instead of being one flat cream field.
    ('LAYOUT', 'Groove editor header and steps form one recessed slate',
        'box-shadow: inset 0 2px 6px rgba(120,100,50,.16);', []),
    # `body.light .groove-card.active .gcp-step` outranks `.gcp-step.on`, so without
    # restating these the accent steps get repainted with the off colour and the
    # pattern vanishes on the selected card specifically.
    ('LAYOUT', 'Selected card restates its accent steps after the base rule',
        'body.light .groove-card.active .gcp-step.on   { background: #8a6d10; box-shadow: none; }', []),

    # ── Light-mode metro screen legibility (v0.133.4) ─────────────────────
    # The BPM label and the screen's top icons were translucent amber on an amber
    # screen, so the alpha blended them halfway into their own background: about
    # 2:1, confirmed unreadable on device. Solid #523700 is ~4.9:1 on that ground.
    ('LAYOUT', 'Metro BPM label is solid, not blended into its own screen',
        'body.light .metro-screen .bpm-unit { color: #523700 !important; }',
        ['body.light .metro-screen .bpm-unit { color: rgba(122,84,16,.7) !important; }']),
    ('LAYOUT', 'Metro screen top icons are solid in light mode',
        'body.light .metro-screen .screen-bpm-row { color: #523700 !important; }',
        ['body.light .metro-screen .screen-bpm-row { color: rgba(111,77,0,.6) !important; }']),
    # The mute and setlist icons had NO light override at all: still on the dark-mode
    # rgba(255,209,102,.4), which is 1.7:1 on the cream screen. The first attempt aimed
    # at .metro-screen-top / .screen-bpm-row and missed; the real containers are
    # #screenTopRow and .groove-screen-bpm-row.
    ('LAYOUT', 'Metro mute and setlist icons are legible in light mode',
        'body.light .metro-screen #screenTopRow svg,', []),
    # Third one in the same family: the groove screen's BPM number got a light value,
    # the "BPM" caption inside it did not, and sat on rgba(255,209,102,.28) at 1.14:1.
    ('LAYOUT', 'Groove screen BPM caption is legible in light mode',
        'body.light .metro-screen .groove-screen-bpm span { color: #523700 !important; }', []),

    # ── Navigation motion (v0.133.0) ──────────────────────────────────────
    # Tabs fade through; folders and modules use shared axis Z. Both patterns are
    # named by Material for exactly these relationships. The Z form has NO travel:
    # an earlier cut grew the screen out of the tapped card, which is a container
    # transform without a container, and it read as the screen scooting in.
    # Tab switches are NOT animated. Three crossfade attempts each reduced a flash on
    # the Metro tab without removing it, and it was never reproducible headless: the
    # opacity curve is clean and nothing in the subtree animates. Likely layer
    # promotion on a 772px subtree. Marginal effect, real artifact, so it is gone.
    ('LAYOUT', 'Tab switches carry no animation',
        '.nav-fx-lat  { animation: none; }',
        ['.nav-fx-lat  { animation: navFadeThrough .13s',
         '.nav-fx-lat  { animation: navFadeThrough .15s']),
    ('LAYOUT', 'Parent-child navigation is shared axis Z, scale only',
        '@keyframes navZIn         { from { opacity:0; transform:scale(.88) }', []),
    # Apple: removing animation outright hurts understandability; replace with a fade.
    ('LAYOUT', 'Reduced motion dissolves rather than snapping',
        '.nav-fx-lat, .nav-fx-fwd, .nav-fx-back { animation: navDissolve .12s linear both !important; }', []),
    # Stagger is descend-only. Apple warns against decorating frequent interactions,
    # and a tab switch is the most repeated gesture in the app.
    ('LAYOUT', 'Card stagger is scoped to forward navigation only',
        '.nav-fx-fwd .practice-card-btn { animation: navCardIn', []),
    # One hook wrapping the nav functions, rather than an edit at fifteen call sites.
    ('LAYOUT', 'Navigation motion is installed by wrapping, not per-call-site edits',
        "['enterToolFolder','enterTool','enterExercise','enterEarTraining',", []),
    # Only the outermost navigation animates. setMode calls exitExercise on its way
    # to a new tab, so without the guard the inner exit fired a Z scale-out and the
    # tab's fade landed on top of it. That is why Metro appeared to scale where the
    # Tuner did not: the difference was whether a module happened to be open.
    # setMode stays wrapped with a null kind: it takes part in the depth guard but
    # animates nothing. Unwrapping it entirely brought the Metro-scales bug straight
    # back, because its inner exitTool then became the outermost call.
    ('LAYOUT', 'Nested navigation calls do not stack animations',
        'if (depth === 0 && kind) { try { play(kind); } catch(e){} }',
        ['var out = orig.apply(this, arguments);\n      try { play(kind); } catch(e){}']),
    ('LAYOUT', 'setMode is wrapped as a guard even though it does not animate',
        "wrap('setMode', null);", []),
    # A fade from fully transparent reads as a blink, because the header above never
    # moves and gives the eye a fixed reference for the blackout.

    # ── RIFF_META entries that a bad regex ate once already (v0.132.15) ────
    # A DOTALL `.*?\},\n` used to replace the montuno metadata ran past its own entry
    # and swallowed the two that followed on the same line, so Waldstein and
    # Liebestraum rendered as bare cards with no composer, year or note. Pinned
    # because nothing else in the gate set notices a missing description.
    ('AUDIO', 'Waldstein keeps its RIFF_META entry',
        "waldstein_1: { composer:'Ludwig van Beethoven', year:'1804', era:'Classical'", []),
    ('AUDIO', 'Liebestraum keeps its RIFF_META entry',
        "liebestraum: { composer:'Franz Liszt', year:'1850', era:'Romantic'", []),

    # ── The montunos are transcribed, not invented (v0.132.13) ────────────
    # The old 'montuno' was an original pattern written to convention, and it did not
    # sound right. Replaced by two transcriptions from a public-domain Basic Montunos
    # MIDI, one per clave direction. Percussion tracks (clave, cascara) deliberately
    # excluded: a piano that plays its own clave teaches the wrong lesson.
    ('AUDIO', 'Both clave directions exist as separate pieces',
        "montuno_32: { label:'Montuno · 3-2 Clave'",
        ["montuno: { label:'Salsa Montuno', tempo:1.0, bpm:180,"]),
    ('AUDIO', 'The 2-3 montuno keeps its transcribed source tempo',
        "montuno_23: { label:'Montuno · 2-3 Clave', tempo:1.0, bpm:120,", []),

    # Was pinned on the single invented 'montuno'; that piece was replaced by the two
    # transcriptions in v0.132.13, so the pin follows them. 'Afro-Cuban' stays banned
    # because it is the era value that made a song invisible in the first place.
    ('LAYOUT', 'Both montunos sit in an era the picker renders',
        "montuno_23: { composer:'Traditional', year:'\\u2014', era:'Other',",
        ["era:'Afro-Cuban'"]),

    # ── Rhodes performances get a damper model (v0.132.9) ──────────────────
    # There was no note-off for Rhodes at all: every note ran to the end of its
    # sample, so the whole piece sounded pedalled from bar one and a restored pedal
    # had nothing to damp. Same model the piano riffs use.
    ('AUDIO', 'Rhodes riff notes go through a damper model, not fire-and-forget',
        'function _riffRhodesNoteOn(midi, dur) {', []),
    ('AUDIO', 'Rhodes perf notes are given a finger-lift event',
        "else _riffRhodesNoteOff(mid);", []),
    ('AUDIO', 'The Rhodes pedal drives the damper, not just the mode flag',
        '_riffRhodesPedalDown = !!val;\n    if (!val) _riffRhodesDamp();', []),
    ('AUDIO', 'Rhodes pedal-up only hard-stops notes when leaving drone mode',
        'if (!val && wasDrone && typeof stopAllRhodesDrones === \'function\') stopAllRhodesDrones();',
        ["if (val === 0 && typeof stopAllRhodesDrones === 'function') stopAllRhodesDrones();"]),
    # ── Status colours have two grounds too (v0.112.7) ────────────────────
    # in-tune / sharp / flat / metro are pinned to clear 4.5:1 as small TEXT on
    # the floor. As a filled bar on a near-white card they measured 9.4-10.5:1,
    # and a filled shape only needs 3:1 to be a graphical object. The lifted set
    # exists for fills and must not be collapsed back into the ink set.
    ('LIGHT', 'Lifted status colours exist for card-borne fills',
        '--in-tune-lift: #447124;', []),
    # The chooser ground carried real chroma at hue 293, a violet-grey, with
    # four other hues sitting on it. Four hues on a fifth is why it read muddy.
    # The chooser and the splash share one recipe so the app opens on a surface
    # and stays on it. A flat mid-tone here read muddy behind pastel cards; a
    # flat neutral read bland. The fall is what makes it neither.
    # Every single-hue version of the chooser ground failed the same way: one
    # colour behind four cards in four other colours. Neutral fixed the clash
    # and cost the interest. Four pools, one under each card, so the ground
    # agrees with whatever sits on it everywhere -- it IS the four modules, out
    # of focus. Pool centres are measured against the real card centres.
    # Every single-hue chooser ground failed the same way: one colour behind four
    # cards in four other colours. Four viewport-anchored pools fixed the clash
    # but only lined up at the aspect ratio they were measured on. The light
    # belongs to the CARD -- attached to the cell, it goes where the card goes at
    # any size, and the physics are the right way round: the cards emit onto the
    # ground rather than the ground being tinted under them.
    ('LIGHT', 'Each chooser card casts its own pool',
        'body.light .lnch-cell::before {',
        ['at 27% 32%, rgba(94,226,255', '#a8abbe;', '#aeaba6;']),
    # ── Two accents, two grounds (v0.112.6) ───────────────────────────────
    # --accent is pinned dark enough to clear 4.5:1 as small text on the FLOOR,
    # the hardest ground. Almost everything it is actually seen on is a CARD,
    # where the same value lands near 10:1 and reads as ink rather than colour.
    # --accent-lift exists for card-borne use and must not be collapsed back.
    # (moved into CHECKS as a count, so the palette can move without the pin
    #  firing on every hue change; what must not vanish is the token itself)
    # An unlit lamp on paper is a recess, not a white box. Inset dark at the top
    # edge, light along the lower lip.
    ('RELPITCH', 'Unlit lamps read as recessed in light',
        'inset 0 3px 5px rgba(40,44,80,.20),', []),
    ('RELPITCH', 'Havens are filled in light, not outlined',
        'body.light #exRelPitch .rlp-vur.safe .rlp-seg {', []),
    # ── Light gets volume from edges, not emission (v0.112.5) ─────────────
    # Dark reads three-dimensional because it emits: a lit rim on every card, a
    # theme-tinted bloom from above, two smaller pools. None of that transfers,
    # since a glow on a light ground smears. What does the same work on paper is
    # a defined rim, a crisp top highlight, a four-layer contact-to-far shadow
    # and a diagonal fall inside the card. All four, or light goes fat again.
    ('LIGHT', 'Light cards are modelled with edge and shadow',
        'inset 0 1px 0 rgba(255,255,255,.85),', []),
    ('LIGHT', 'The light field has dark\'s three-pool structure',
        'radial-gradient(ellipse 95% 55% at 50% -8%,', []),
    # A selected chip in light is a tinted LIGHT chip. 70% of --theme over white
    # was fine when the accent was mid-tone; once the ramp took it to OKLCH L .36
    # the same mix became a dark slab at 3.0-3.9:1 against its own label.
    ('LIGHT', 'Selected chips stay light, not inverted',
        "color-mix(in srgb, var(--theme, #6b7bd6) 14%, #ffffff),",
        ['var(--theme, #6b7bd6) 70%, #ffffff']),
    # ── Settings modal geometry (v0.112.4) ────────────────────────────────
    # Adding a light-mode background override split the base rule and carried
    # max-width, padding, max-height and overflow-y into the light selector, so
    # in dark the panel had no width limit and no scrolling: unusable, and no
    # way to reach the theme switch to get out of it. The base rule owns
    # geometry; theme rules may only repaint.
    ('LAYOUT', 'The settings modal keeps its geometry in the base rule',
        "    background: linear-gradient(180deg, var(--surface), var(--bg-1));\n"
        "    border: 1px solid var(--border);\n"
        "    border-radius: var(--r-lg);\n"
        "    padding: 22px 20px;\n"
        "    max-width: 420px; width: 100%;", []),
    # ── Light floors carry EQUAL chroma (v0.112.2) ────────────────────────
    # The first ramp multiplied each hue's existing chroma, which preserved a
    # 2.5x spread: metro and tools sat at C .13-.14 while tuner and train sat at
    # C .05-.07. Same lightness, wildly different weight -- two modes read heavy
    # and two read washed. Chroma is absolute now, .075 on every floor.
    ('LIGHT', 'Every light floor carries the same chroma',
        '--bg-0: #bdab75; --bg-1: #c3b17a;', ['--bg-0: #cca932']),
    # The daylight wash was 62% white at the top falling to 3% at the bottom,
    # tuned for the old pale floor. On a deeper one it repainted the top of the
    # screen and left the bottom raw, which is both halves of the complaint.
    ('LIGHT', 'The daylight wash is a field, not a repaint',
        'rgba(255,253,247,0.20) 0%,', ['rgba(255,253,247,0.62) 0%,']),
    # Sheets fell from card colour to the page floor, so a raised panel wore the
    # page's colour along its bottom edge and stopped looking raised.
    ('LIGHT', 'Raised sheets stay on raised colours',
        'body.light .settings-modal-content {', []),
    # ── The climb is twenty-four rungs (v0.112.1) ─────────────────────────
    # Twelve was too short to be hard: a clean run only had to survive six real
    # questions. Four distance bands over twenty-four rungs, havens on the first
    # three band edges, twelve lifelines to burn so the multiplier floor is
    # reachable and a clean summit means clean.
    ('RELPITCH', 'The ladder is twenty-four rungs with four bands',
        "rungs:[19,20,21,22,23,24],     min:1, max:2 }",
        ['rungs:[7,8,9,10,11,12],  min:1, max:2 }']),
    ('RELPITCH', 'Three havens, one per band edge',
        'var RLP_SAFE = [6,12,18];', []),
    # The light floor gradient ran light at the top, down through the floor and
    # back up to near-white at the bottom, which put the brightest band under
    # every card. It runs one way now.
    ('LIGHT', 'The splash gradient runs light-to-dark downward',
        'var(--bg-0) 66%,',
        ['var(--bg-0) 50%, var(--surface) 100%']),

    # ── Light mode floor ramp (v0.112.0) ──────────────────────────────────
    # The four light palettes are generated from one OKLCH ramp, not picked by
    # hand per mode. Floor L .745, card L .965, borders L .52, accent L .36.
    # If a floor value drifts back toward the old pale set the whole complaint
    # comes back: separation was 1.16:1 in all four modes before this.
    ('LIGHT', 'Light floors sit on the deepened ramp',
        '--bg-0: #8faedc; --bg-1: #94b4e2;', ['--bg-0: #becfe7', '--bg-0: #97aecf']),
    # Cards carry real hue and a real internal fall. They shipped once at chroma
    # .012 with a .019 fall against dark's .037/.029, which is most of why light
    # read flat: a third of the colour and two thirds of the modelling.
    ('LIGHT', 'Light cards carry hue and a fall, matched to dark',
        '--surface: #ddebff; --surface-2: #ecf4ff; --panel: #fbfdff;',
        ['--surface: #e7edf7', '--surface: #d5dde9']),
    # The accent had to deepen with the floor or it drops under AA on it.
    ('LIGHT', 'Light accent deepened with the floor',
        '--accent: #00546d;\n    --accent-warm: #b34a18;',
        ['--accent: #0049aa;', '--accent: #003787;']),
    # Ink and the shared status colours are pinned to the GROUND now, not the
    # card, because the ground became the hard case when it dropped.
    ('LIGHT', 'Status colours re-pinned to the ground',
        '--in-tune: #224700; --green: #224700;', ['--in-tune: #3a7000;']),
    ('LIGHT', 'Tuner accent literals follow the token',
        'body.light .sf-chosen-name { color: var(--accent); }', ['.sf-chosen-name { color: #0049aa']),
    # ── Relative Pitch intro interactions (v0.111.3) ──────────────────────
    # Opening the rules went through rlpRender, which rebuilds the intro card
    # and therefore replays the whole entrance. It edits the DOM in place now.
    # The rules went out from behind the toggle and came straight back: unfolded
    # they are three paragraphs between the record and the button, on a screen
    # whose whole shape ends on START. Behind a link they cost one dim line.
    ('RELPITCH', 'The rules expand in place, they do not re-render',
        "case 'rules': rlpToggleRules(); break;",
        ["case 'rules': rlpRulesOpen = !rlpRulesOpen; rlpRender();"]),
    # The ghost segment belongs behind a real reading. Behind a placeholder it
    # reads as a stray B-flat rather than as dark segments.
    ('RELPITCH', 'No ghost segment behind the placeholder reading',
        "(answered ? '<span class=\"rlp-ghost\">B\\u266d</span>' : '')", []),
    # START hands over rather than cutting, and the first note waits for it.
    ('RELPITCH', 'START animates into the first rung',
        'function rlpStartClimb() {', []),
    ('RELPITCH', 'The first note lands after the transition',
        'rlpRung === 1 ? 620 : 350', []),
    # ── Relative Pitch intro is one card (v0.111.2) ───────────────────────
    # The band chips explained the distractor spacing before you had heard a
    # note, and the game already prints the band and its gap in the card head
    # at the moment it matters. One card, ending on START, rules behind a link.
    ('RELPITCH', 'Intro is a single card ending on START',
        "rlp-start\" data-rlpact=\"start\">",
        ['rlpIntroCard2', 'rlp-chips']),
    # ── Relative Pitch intro ladder (v0.111.1) ────────────────────────────
    # The intro ladder lights your furthest rung. It shipped once with rung 9
    # hard-coded, carried over from the design mock, which made the bars look
    # decorative instead of being the machine's memory of you.
    ('RELPITCH', 'Intro ladder reads the furthest rung, not a fixed number',
        "if (i + 1 === far) { r.classList.add('now');",
        ["if (i === 8) { r.classList.add('now')"]),
    # Nothing sounds on the START tap. The chime belongs to the build and the
    # next sound has to be the question.
    ('RELPITCH', 'START itself is silent',
        "case 'start':\n      rlpStopBoot();\n      rlpStartClimb(); break;", []),
    # ── Relative Pitch entrance (v0.111.0) ────────────────────────────────
    # The welcome chime must stay inside the build. If anything sounds after
    # the intro settles, the first note of the climb stops being unambiguous.
    ('RELPITCH', 'The welcome chime is confined to the build',
        'rlpWelcomeChime();\n\n  rlpBootAt(', ['rlpWelcomeChime(); }, 3000']),
    # Card fade and staged reveal are separate: hiding is a class on each
    # element, not a descendant of the card's own fade class. When they shared
    # a class the whole card appeared at once.
    ('RELPITCH', 'Boot staging is per element, not a descendant of the card fade',
        '#exRelPitch .rlp-hidden { opacity:0;',
        ['.rlp-boot .rlp-ititle {']),
    ('RELPITCH', 'Boot timers are killed on teardown and on START',
        'function rlpStopBoot() {', []),
    # ── Relative Pitch scoring and sound (v0.110.9) ───────────────────────
    # No pitched sound may fire between the target note and the answer. A chime
    # on every correct rung was scrubbing the pitch the drill asks you to carry.
    ('RELPITCH', 'No chime fires on a correct rung',
        'rlpNewRung(); rlpRender(); return;',
        ["rlpChime([0,7]", "rlpChime(rlpRung >= RLP_TOP"]),
    # Terminal sounds go through the app's cue bank so they honour the person's
    # cue set and per-event volumes.
    ('RELPITCH', 'Outcome sounds route through the app cue bank',
        "if (kind === 'gameover' && typeof playCueGameOver === 'function')", []),
    # Lifelines cost a tenth of the multiplier each, which is the only thing
    # making them a decision rather than admin.
    ('RELPITCH', 'Lifelines cost multiplier',
        'return Math.max(RLP_MULT_MIN, RLP_MULT_MAX - rlpLivesUsed * RLP_MULT_STEP);', []),
    ('RELPITCH', 'Every exit settles through the multiplier',
        'var settled = rlpSettle(rawVal);', []),
    # ── Relative Pitch tone bank (v0.110.8) ───────────────────────────────
    # Two shared components default to the piano console's near-black skin, so
    # every new tone row must opt out twice or it ships black on a coloured
    # card. Both halves pinned: the button override keyed on the modal id, and
    # the ex-tonepop skin passed to the builder instead of the Chords default.
    ('RELPITCH', 'Tone bank button opts out of the piano skin',
        '#rlpSettingsModal .piano-overlay-voice-btn {', []),
    ('RELPITCH', 'Tone popup is given a skin explicitly',
        "skin: 'ex-tonepop'\n};\nfunction rlpOpenSettings()", []),
    ('RELPITCH', 'The drill voice is swapped and restored, not left set',
        'finally { if (swapped) selectedRefTone = prev; }', []),
    # ── Relative Pitch answer input (v0.110.7) ────────────────────────────
    # An accidental toggle plus seven letters meant your own wrong answers
    # appeared to move when you switched it, and vanished entirely on natural
    # while the try stayed spent. Twelve buttons keyed by pitch class instead:
    # one tap, one meaning, marks that stay put.
    ('RELPITCH', 'Answers are keyed by pitch class, not letter plus a mode',
        "if (el.dataset.rlppc) { rlpAnswer(+el.dataset.rlppc); return; }",
        ['rlpAcc', 'data-rlpacc']),
    ('RELPITCH', 'Accidentals straddle the seams like a keyboard',
        'transform:translateX(-7.143%);', []),
    # ── Relative Pitch transport row (v0.110.5) ───────────────────────────
    # Replay, next and the A reference are one row of three. They were spread
    # across the card in three places, which is also what made the reveal jump.
    ('RELPITCH', 'Transport is one row, and there is no free reference tone',
        "'<div class=\"rlp-transport\">'",
        ['<button class="rlp-next" data-rlpact="next"', "data-rlpact=\"againstA\""]),
    # HEAR IT AGAINST A handed out a free A440 after every card, which is the
    # fork's entire job without the fork's cost. The fork has to stay the only
    # way to get a reference, or the resource means nothing.
    ('RELPITCH', 'The fork is the only route to a reference tone',
        "case 'fork': rlpSound(69); rlpRun = 0;", ['againstA']),
    # ── Relative Pitch layout stability (v0.110.4) ────────────────────────
    # NEXT and HEAR IT AGAINST A used to be injected on reveal, and the climb
    # swapped a two-up bank row for a single button, so the card jumped under
    # the thumb at the exact moment you were reaching for it. Both action rows
    # are reserved now; if the disabled attribute or the reserved row goes, the
    # jump comes back.
    ('RELPITCH', 'Practice action buttons are always mounted',
        "data-rlpact=\"next\"' + (rlpDone ? '' : ' disabled')", []),
    ('RELPITCH', 'Climb action row is height-reserved',
        '#exRelPitch .rlp-actions { min-height:69px;', []),
    # ── Relative Pitch animation teardown (v0.110.2) ──────────────────────
    # exitExercise stops modules from a hand-maintained list, and bottom-tab
    # switches bypass exitExercise entirely. The comet RAF survived both,
    # burning 60fps on a hidden panel. Two guards: the stop list carries
    # rlpTeardown, and the frame loops bail when their panel is hidden.
    ('RELPITCH', 'Teardown is on the exitExercise stop list',
        'roadtripStop(); rlpTeardown();', []),
    ('RELPITCH', 'The comet bails when its panel is hidden',
        "if (!panel || panel.classList.contains('hidden')) { _rlpAnimRAF = null; return; }", []),
    # ── Relative Pitch ambient bleed (v0.110.1) ───────────────────────────
    # A radial blob tracked the comet head across a box far taller than the
    # lamp row, so it drifted over the header and the readout as a second
    # light and snapped back to the left at the end of each sweep. The
    # three-stop shadows do the spill properly now that nothing clips them.
    ('RELPITCH', 'No free-floating ambient bleed behind the lamps',
        'rlpWrite(lv);\n    _rlpAnimRAF = requestAnimationFrame(frame);', ['rlp-bleed']),
    # ── Relative Pitch (v0.110.0) ─────────────────────────────────────────
    # The ladder escalates on ONE axis: how close the wrong answers sit. An
    # earlier draft also narrowed the note pool in the first band, which made
    # BLACK-OR-WHITE a lifeline that could never tell you anything for a third
    # of the game. If a pool ever reappears in a band, that bug is back.
    ('RELPITCH', 'Distractor bands are the only difficulty axis',
        "{ name:'WIDE',     key:'rlp_band_wide',  gap:'rlp_gap_wide',  rungs:[1,2,3,4,5,6],           min:5, max:6 }",
        ["name:'WIDE', pool:RLP_WHITE", "pool:RLP_WHITE, min:"]),
    # Havens sit on the band boundaries, and lifelines and replays refresh on
    # the same edge. Three structures on one boundary is the whole design; move
    # one and the game silently grows a second rulebook.
    ('RELPITCH', 'Havens land on the band edges',
        "var RLP_SAFE = [6,12,18];", ['var RLP_SAFE = [2,6]', 'var RLP_SAFE = [4,8]']),
    # A wrong answer ENDS the run. Falling back to a haven and continuing made
    # banking pointless, because a run you cannot lose is not worth leaving.
    ('RELPITCH', 'A wrong answer ends the climb',
        "rlpChRecord('lost', rlpHavenValue(rlpRung));", ['rlpRung = haven']),
    # Random fill once served semitone distractors inside the band that exists
    # to guarantee distance. The fallback must sort by distance, not shuffle.
    ('RELPITCH', 'Distractor fallback sorts by distance',
        "rest.sort(function(x, y){ return b.min > 2 ? y.d - x.d : x.d - y.d; });", []),
    # Glows live in an overlay above every housing. Inside the lamp, the next
    # lamp's opaque housing paints over the previous lamp's light, and in the
    # keyboard input the key letter gets erased by its own glow.
    ('RELPITCH', 'Glow overlay sits above the housings',
        '<div class="rlp-glows">', ['<span class="rlp-glow"></span><span class="rlp-lens">']),
    # Lamp colour is var-driven so light mode is an override, not a parallel
    # stylesheet. Hard-coded glows are what shipped the tone banks black.
    ('RELPITCH', 'Lamp colours are theme vars, not hex',
        "body.light #exRelPitch {", []),
    # EN and IT twins for the module's strings.
    ('RELPITCH', 'Italian twin exists for the climb copy',
        "rlp_intro_line:'Ventiquattro note,", []),
    # ── Road Trip journey fallback (v0.109.1) ────────────────────────────
    # The legacy RT_SONGS table was deleted: it was reachable only via the
    # catch below, and when it fired it played a DIFFERENT song against leg
    # durations already cut from the journey song's slices. If it ever comes
    # back, phrases get chopped mid-boundary and nothing throws.
    ('ROADTRIP', 'No legacy RT_SONGS fallback table',
        'rtDistractMelodyStart(g);\n}', ['RT_SONGS = [', 'RT_SONGS.filter']),
    # riffStart is on the line BEFORE rtDistractSong is set, so a throw leaves
    # the flag false and rtDistractStop never calls riffStop. Clear it here or
    # a failed start leaves voices ringing for the rest of the trip.
    ('ROADTRIP', 'Failed journey riffStart clears its own partial playback',
        "try { if (typeof riffStop === 'function') riffStop(); } catch(e2) {}", []),
    # The base .piano-overlay-voice-btn is the piano console's black lid with a
    # mint caret. Any surface that is not the piano must opt out or it inherits it.
    ('TONEPOP', 'Exercise voice buttons opt out of the piano console skin',
        "  #ivToneBank .piano-overlay-voice-btn,", []),
    # Measured 1.068:1 against the card, i.e. invisible. Darkening a light surface
    # is a dark-mode habit; light mode lifts the stave above the card instead.
    ('STAFFRD', 'Light-mode stave is lifted, not dimmed',
        "background:linear-gradient(180deg, #fdfdff 0%, var(--surface-2) 100%);", []),
    ('CHORDEAR', 'Settings rows are all blocks, no inline margins',
        '<div class="ce-opt-block" id="ceSpeedBlock">',
        ['<div class="ce-opt-group" style="margin:8px 0">']),
    ('CHORDEAR', 'Chord pool has its own section head',
        'data-i18n="ce_sec_pool">CHORD POOL', []),
    # Per-row captions were removed as hand-holding (v0.109.4). Two survive because
    # they state something you cannot see: why SPEED greys out, and that touching
    # DIFFICULTY moves you to the CUSTOM tier. Re-adding a caption per row is the
    # regression; .ce-opt-desc was deleted outright so its return is the tell.
    ('CHORDEAR', 'Settings captions stay minimal',
        'data-i18n="ce_speed_arp_note"', ['class="ce-opt-desc"']),
    # Standchen was a complete arrangement the picker could never draw (v0.109.0).
    ('ROADTRIP', 'Standchen has journey hooks',
        "standchen:{tier:'easy',bpm:60,hooks:[{b:1,s:8}", []),
    # ── Staff Notes + the shared tone picker (v0.108.5/.6) ────────────────
    # The tone popup is driven by four surfaces now. When a module owns the
    # pick, the app-wide branch must stay skipped: delete the guard and Staff
    # Notes silently starts writing selectedRefTone again, and the symptom is
    # the PIANO changing voice, which nobody traces back to a reading drill.
    ('TONEPOP', 'Module-owned picks skip the app-wide branch',
        "if (oHooks && typeof oHooks.set === 'function') {", []),
    ('TONEPOP', 'openTonePopup records who opened it',
        '_tonePopOwner = owner || null;', []),
    ('TONEPOP', 'closeTonePopup strips every module skin, not just the Chords one',
        "pop.classList.remove('tone-pop-ivr', 'chd-tonepop', 'sr-tonepop', 'ex-tonepop')", []),
    # The Train exercise modules must not fall through to the Chords tool's skin:
    # chd-tonepop hardcodes #12211a/#0d1712, which is why the popup read as black
    # inside a purple module. ex-tonepop is theme-var driven, so light mode is free.
    ('TONEPOP', 'Train exercise modules pass their own popup skin',
        "var _exToneSkin = { skin: 'ex-tonepop' };", []),
    ('TONEPOP', 'Legacy scrolling tone strip stays deleted',
        "buildChordToneBank('ceToneBank', _exToneSkin)", ['buildExerciseToneBank']),
    # setLang called buildExerciseToneBank('scaleToneBank') three lines after
    # scalesInit() had already built the tabbed picker, so every EN/IT flip
    # replaced the Scales grid with the legacy chip strip.
    ('SCALES', 'setLang does not rebuild the Scales tone bank',
        "try { scalesInit && scalesInit(); } catch(e) {}", ["buildExerciseToneBank('scaleToneBank')"]),
    ('STAFFRD', 'Fretboard resolves theme colours instead of dark literals',
        "function srFretPal() {", ["fill:'#1b1e2e'"]),
    ('TONEPOP', 'Picking a voice previews it',
        '_tonePreviewPick(key, function() {', []),
    ('STAFFRD', 'Staff Notes owns its voice and takes its own popup skin',
        "skin: 'sr-tonepop'", ['skin: null']),
    ('STAFFRD', 'Reveal voice defaults to grand piano, never the empty sentinel',
        "prefGet('srTone', 'grand_piano'", ["prefGet('srTone', ''"]),
    ('STAFFRD', 'Three tries per card',
        'var SR_MAX_TRIES = 3;', []),
    ('STAFFRD', 'Reveal-silencing timer is cancellable, not an orphan setTimeout',
        '_srStopTO = setTimeout(', []),
    # Input surfaces share one outcome path. Two copies of the tries and stats
    # rules would drift the first time either changed.
    ('STAFFRD', 'Grid and keyboard share one scoring path',
        'function _srResolve(isRight, wrongTag)', []),
    ('STAFFRD', 'Keyboard answers are octave-exact',
        '_srResolve(midi === srTarget', []),
    ('STAFFRD', 'Answer input defaults to the note grid',
        "prefGet('srInput', 'grid'", []),
    ('STAFFRD', 'Drill keyboard draws no instrument console strip',
        "svgEl.id === 'srPianoSvg') ? null : 'pcc'", []),
    # The keyboard window is user-driven. Auto-centring it on the card would
    # hand over the octave on exactly the notes the octave question is for.
    ('STAFFRD', 'Keyboard window is two octaves, stepped by hand',
        'var SR_PIANO_OCTS = 2;', []),
    ('STAFFRD', 'Keyboard window never snaps to the target octave',
        'if (srPianoOct == null) srPianoOct = b.min;', []),
    # Fretboard. The written offset is the one a player would notice instantly
    # and nobody else would; guitar and bass are notated an octave high.
    ('STAFFRD', 'Fretboard reads written pitch, not concert',
        "guitar:   { label:'GUITAR',   open:[40,45,50,55,59,64], written:12 }", []),
    ('STAFFRD', 'Fretboard neck is 24 frets in two slices',
        'var SR_FRET_NECK = 24;', []),
    ('STAFFRD', 'Card pool narrows to what the instrument can play',
        'var out = base.filter(srPlayable);', []),
    ('STAFFRD', 'Fret answers convert to written pitch at the tap',
        'var written = it.open[s] + f + it.written;', []),
    # The stave box must not resize when any setting changes. Two earlier
    # attempts got this half right; the range half was fixed in v0.108.14.
    ('STAFFRD', 'Stave box is fixed across clef AND range',
        "var key = 'fixed:' + srAcc + ':' + srKeySig;", []),
    # Three setters used to call srReset, which is the RESET button's function.
    # Turning accidentals on emptied the note table, the position table and the
    # best run. They mark the card stale instead.
    ('STAFFRD', 'Changing a setting does not wipe reading history',
        'var _srCardStale = false;',
        ["prefSet('srAcc', v);   _srMetricCache = {}; srReset();"]),
    ('STAFFRD', 'Stale cards redraw on leaving the sheet',
        'if (_srCardStale) { _srCardStale = false; srNextCard(); }', []),
    # The audio chain has to be opened on the tap itself. Built inside the sample
    # load callback it comes up suspended and the first preview of a session is
    # silent, which is a bug that only ever shows on device.
    # Pinned by what must NOT come back: the context being built inside the load
    # callback, which is where it was when the first preview of a session was
    # silent. v0.108.24 reshaped the function around a _play closure, so the
    # original positional pin no longer described anything.
    ('TONEPOP', 'Preview opens the audio chain on the gesture, not after the load',
        'const ctx = ensureRefCtx();',
        ['        const ctx = ensureRefCtx();\n        SampleEngine.play(key, 69, ctx']),
    ('TONEPOP', 'Tone banks warm the chain when they open',
        'function _toneBankWarm(key)', []),
    # resume() is a promise. Scheduling a note before it settles drops the note,
    # which is only ever audible on device and only on the first pick.
    # A preview reads one buffer. Gating it on the whole instrument meant the
    # first pick of a voice waited for 88 files and read as silence.
    ('TONEPOP', 'A preview costs one sample, not the whole instrument',
        'async warmNote(id, midi, ctx)', []),
    # The whole bug. The preview needs one file; firing all 88 first buried it
    # behind the connection pool and it arrived seconds after the tap.
    ('TONEPOP', 'The previewed note is fetched before the rest of the set',
        'try { await this.warmNote(id, 69, ctx); } catch (e) {}', []),
    # Silence reads as a broken control. If the sample cannot be fetched at all,
    # the preview speaks with the synth rather than saying nothing.
    ('TONEPOP', 'A preview never goes silent when a sample is unavailable',
        "D.via = 'synth fallback';", []),
    ('TONEPOP', 'Single-note fetches are shared, not raced',
        'const _warmPromise = {};', []),
    ('TONEPOP', 'play() works from a partially loaded instrument',
        'if (!this.isReady(id) && !(_buffers[id] && _buffers[id].size)) return null;',
        ['play(id, midi, ctx, dest, vol, dur, at) {\n      if (!this.isReady(id)) return null;']),
    # Reshaped again in v0.108.26 to record the outcome, so pinned on the
    # behaviour rather than the exact line: nothing is scheduled until the
    # resume has settled.
    ('TONEPOP', 'Preview waits for the resume before it schedules anything',
        "if (ctx && ctx.state === 'suspended') {",
        ['ctx.resume();\n  _play();']),

    ('UI',     'Embouchure card min-height is exactly 78px',
        'min-height:78px', []),
    ('WIND',   'Ocarina range is exactly low:69 high:89',
        'ww_ocarina:  { low: 69, high: 89', []),
    ('WIND',   'Ocarina offers octaves [4,5,6]',
        "octaves:[4,5,6], defaultOct:5 },\n      '7hole'", []),
    ('WIND',   'Ocarina C5 home fingering exact bit-pattern',
        '0:  { p:[1,1,1,1,0,0,1,1,1,1,1,1] }', []),
    ('TONALE', 'Reveal color thresholds: 9.5 green / 7 amber',
        "pts>=9.5 ? 'var(--in-tune)' : pts>=7", []),
    ('TONALE', 'Positive-cue threshold is 6.5',
        'pts >= 6.5', []),
    ('DIADLE', 'All three difficulties are 5 guesses',
        'maxGuesses:5', []),   # presence; count enforced below via min in CHECKS-style
    ('METRO',  'Tick partials include 3100 + 4700 Hz',
        '3100', []),
    ('METRO',  'Tick partial 4700 Hz present',
        '4700', []),
    ('AUDIO',  'Bass click ramp uses 3ms (0.003)',
        '0.003', []),
    # ── Audio engine values (deep-read pins; -3 also forbids the -12 brick wall) ──
    ('AUDIO',  'BASE_GAIN_BOOST is 0.9 (not the stale 1.8/1.25)',
        'const BASE_GAIN_BOOST = 0.9', ['BASE_GAIN_BOOST = 1.8', 'BASE_GAIN_BOOST = 1.25']),
    ('AUDIO',  'Main limiter threshold is -3 dB, never the -12 brick wall',
        'threshold.value = -3', ['threshold.value = -12']),
    ('AUDIO',  'Rhythm-reader limiter bus stays at -6 dB',
        'threshold.value = -6;  lim.knee.value = 0', []),
    # v0.99.35: floor lowered 50% -> 20%. A 50% floor is only -6 dB, so the whole
    # bottom half of the fader was worth about one perceptual step while the top
    # half spanned far more. 20% is -14 dB and makes the two halves symmetrical.
    ('AUDIO',  'Master volume slider range is 20-200%',
        'min="20" max="200"', []),
    ('AUDIO',  'Tick scroll rate-limit gate is 38 ms',
        '_last < 38', []),
    # ── v0.80.21: replaced the old 'rms < 0.001' pin. That string lived ONLY inside
    # vrAutoCorrelate(), the vocal-range tool's private pitch detector, which was
    # deleted (plain autocorrelation with no cumulative-mean normalisation = octave
    # errors by construction; also O(N^2); also used the wrong sample rate on native).
    # Vocal range now calls the shared detectPitch(). These pins guard what replaced it.
    #
    # The invariant that actually matters: every amplitude gate must be NATIVE-AWARE.
    # AudioRecord with AGC off is rawer/quieter than the WebView analyser, so any
    # fixed gate silently becomes a much higher bar on the native path — which is how
    # four separate detectors quietly broke at once.
    ('AUDIO',  'Pitch RMS floor is native-aware (native 0.00012)',
        '_floor = _nativeMicActive ? 0.00012', []),
    ('AUDIO',  'Onset detection uses spectral flux with adaptive threshold',
        '_SF_K      = 1.4', []),
    ('AUDIO',  'Interval hold gate is native-aware (native 0.0018)',
        '_IVAL_HOLD_RMS_NATIVE = 0.0018', []),
    ('AUDIO',  'YIN uses FFT (O(N log N)), not the O(N^2) brute loop',
        '_fftInPlace(_fWr, _fWi);', []),
    ('AUDIO',  'YIN FFT cross-correlates WINDOW vs FULL (not full vs full)',
        'for (let i = 0; i < H; i++) _fWr[i] = buf[i];', []),
    ('AUDIO',  'Median pre-filter runs before the EMA (rejects outliers an EMA cannot)',
        '_PITCH_HIST_N = 3', []),
    # v0.80.24: median is 3 not 5. The window is in FRAMES, and native detection runs at
    # the true native frame rate (~21.6 Hz measured, = 2048 samples / 44100), NOT rAF's
    # 60 Hz. 5 frames would be a 231 ms window (laggy); 3 is 139 ms and still outvotes a
    # single bad reading.
    ('AUDIO',  'Detection is gated on genuinely NEW native audio (not every rAF tick)',
        '_nativeRingSeq !== _lastDetectSeq', []),
    ('AUDIO',  'EMA alpha is re-solved for the ACTUAL detection rate (not fixed at 60Hz)',
        'function _rateAlpha(alpha60)', []),
    ('AUDIO',  'Drone notch cache invalidates on sample-rate change',
        '_droneNotchSr', []),
    ('AUDIO',  'Native bandpass rebuilds on sample-rate change',
        '_nfEnsureSr', []),
    # Vocal range now calls the shared detectPitch(). The call site uses a
    # pre-declared `freq` (let), not `const freq = …`, because worklet output
    # can fill freq first and the main-thread path is the fallback.
    ('AUDIO',  'Vocal range uses the shared detectPitch (no private detector)',
        'freq = detectPitch(buf, _vrSr)', []),
    # v0.80.27: the needle EMA is now RATE-AWARE. A fixed 0.18 was tuned for 60 Hz rAF,
    # but detection runs at the true native frame rate (~21.6 Hz), so every frame landed
    # with ~3x too much weight and the needle jerked to each individual reading — the
    # "shaky gauge". _rateAlpha(0.18) re-solves it so the FEEL is 84ms on either path.
    ('TUNER',  'Cents needle EMA is rate-aware (not a fixed 0.18 @60Hz)',
        'const _cAlpha = _rateAlpha(0.18);', []),
    ('TUNER',  'In-tune band is perceptual: 5c instrument / 18c voice',
        'const TOL_VOICE      = 18;', []),
    ('RT',     'Road Trip hold decay is 0.6x (not the punishing 1.5x)',
        'rtHoldAcc - dt * 0.6', []),
    ('PROG',   'Capo keeps only open shapes (maxFret <= 4)',
        'Math.max(...ff) <= 4', []),
    # Min onsets raised from 3 to 4 (worklet/tempo pass) to stop premature BPM
    # readings while the onset window is still filling.
    ('METRO',  'BPM detection needs >= 4 onsets (spectral flux)',
        '_TEMPO_MIN_ONSETS = 4', []),
    ('CALIB',  'Tap-calibration accept window is +/-500 ms',
        'Math.abs(offsetMs) > 500', []),
    ('FONTS',  'Fonts are self-hosted (offline-proof), not on Google CDN',
        '@font-face{font-family:', ['fonts.googleapis.com']),
    # ── Instrument-audit fixes (v0.67.11–.13) — frozen against silent drift ──
    ('WIND',   'Bassoon G2 = all six holes closed (WFG, not flute-style lift)',
        'p:[1, 1,1,1,  0,0,0,0,0,  1,1,1,0,  0,0,0,0] }, // G2', []),
    ('WIND',   'Bassoon F#3 keeps the half-hole LH1 vent (0.5) — high-reg signature',
        'p:[0, 0.5,1,1,  0,0,0,0,0,  1,1,1,0,  0,1,0,0] }, // F#3', []),
    ('WIND',   'Bassoon G4 keeps whisper + half-hole LH1 vent',
        'p:[1, 0.5,1,1,  0,0,0,1,0,  1,0,0,0,  0,1,0,0] }, // G4', []),
    ('WIND',   'Recorder F-instruments (alto/bass) get the +5 pc shift, not raw concertPc',
        "writtenPc = _recF ? ((concertPc - 5) % 12 + 12) % 12 : concertPc",
        ['table = RECORDER_FINGERINGS; layout = RECORDER_LAYOUT; writtenPc = concertPc;']),
    ('WIND',   'Recorder oct2 register threshold is low+12, never the stale 72-trans',
        'const oct2Threshold = _rng.low + 12', ['oct2Threshold = 72 - trans']),
    ('WIND',   'Didgeridoo learn-tab range is A2-G3, never the octave-low C1-G1',
        'A2 to G3', ['C1 to G1']),
    # NOTE: some taste/aesthetic values (splash easing, tick decay 0.012, swipe 45px,
    # 4/4 prob 0.75) are deliberately NOT pinned — they recur across the file so a pin
    # would be false comfort, and they're tuned by feel rather than correctness.
    # ── v0.103.0: GROOVE PATTERNS ─────────────────────────────────────────
    # Pinned because these nine were corrected against sources and a silent revert
    # has already happened once: BULERÍA was fixed, changed back, and caught only
    # because someone happened to re-read the line. Nothing failed. Pinning turns
    # that class of regression into a build failure instead of a lucky catch.
    #
    # Deliberately NOT pinned: the 5 CONSTRUCTED teaching cells and the 3 grooves
    # flagged CEILING REACHED. Those may still legitimately move, and pinning all
    # 60 would make the groove table stiff to work on for no correctness gain.
    # When you change one of these on purpose, update the pin here too.
    ('GROOVE', 'SHIKO pattern (Toussaint 1/6)',
        'steps: [2,0,0,0,2,0,2,0, 0,0,2,0,2,0,0,0],', []),
    ('GROOVE', 'SOUKOUS pattern (Toussaint 2/6)',
        'steps: [2,0,0,2,0,0,2,0, 0,0,2,2,0,0,0,0],', []),
    ('GROOVE', 'GAHU pattern (Toussaint 3/6)',
        'steps: [2,0,0,2,0,0,2,0, 0,0,2,0,0,0,2,0],', []),
    # Deliberately the bare array, NOT anchored to the name line above it. The first
    # version of this pin spanned name+steps because the array is not unique (KPANLOGO
    # is byte-identical, which the groove audit accepts), and it drifted the moment a
    # comment was inserted between the two lines. Anchoring a pin to adjacency makes it
    # fire on edits that changed nothing. Uniqueness is enforced by the count guard
    # below instead: the array must appear EXACTLY twice, son32 and kpanlogo. That
    # catches one of them changing, which is the case that matters.
    ('GROOVE', 'SON CLAVE 3-2 / KPANLOGO shared pattern (Toussaint 4/6)',
        'steps: [2,0,0,2,0,0,2,0, 0,0,2,0,2,0,0,0],', []),
    ('GROOVE', 'RUMBA CLAVE 3-2 pattern (Toussaint 5/6)',
        'steps: [2,0,0,2,0,0,0,2, 0,0,2,0,2,0,0,0],', []),
    ('GROOVE', 'BOSSA NOVA pattern (Toussaint 6/6)',
        'steps: [2,0,0,2,0,0,2,0, 0,0,2,0,0,2,0,0],', []),
    ('GROOVE', 'MAQSUM pattern (matched character by character)',
        'steps: [2,0,1,0,0,0,1,0, 2,0,0,0,1,0,0,0],', []),
    ('GROOVE', 'COMPÁS SOLEÁ pattern (four sources agree)',
        'steps: [1,0,2,0,0,2,0,2,0,2,0,2],', []),
    ('GROOVE', 'FLAMENCO BULERÍA pattern (silently reverted once)',
        'steps: [2,0,0,2,0,0,2,0,2,0,2,0],', []),
    # ── v0.104.0: ROAD TRIP HAND-TUNED LEGS ───────────────────────────────
    # The 17 grid songs below had their five hooks placed by ear on-device, one
    # song at a time, over several sessions. That work leaves no trace in the app:
    # the Leg Tuner's "changed" highlight only diffs against a snapshot taken when
    # the panel opens, so it forgets everything the moment you close it. If a hook
    # drifted back to an earlier value nothing would fail and nothing would look
    # wrong; you would just be listening to a worse entry point and re-tuning a
    # song that was already finished. Same class as the BULERÍA revert.
    #
    # Deliberately NOT pinned: the 21 songs with a perf: block. Those are untuned
    # by definition (RT_TUNED is empty), their hooks are analytic placements, and
    # pinning them would freeze values nobody has approved. Pin each one HERE as
    # it gets signed off into RT_TUNED, not before.
    #
    # When you retune one of these on purpose, update its line here too.
    # ── v0.105.1: BACKUP EXCLUSIONS ───────────────────────────────────────
    # These two are the whole reason the export payload is a filtered copy
    # rather than a dump. hasPro is trusted by isPro(), so if it ever travels,
    # a text editor and one boolean is a free Pro unlock. tapOffsetMs is
    # calibration measured against one device's audio latency, so carrying it
    # makes the receiving phone worse. intonare_backup_audit.py checks the same
    # two by name; this pin is here so the ship gate catches it without anyone
    # remembering to run the audit.
    ('BACKUP', 'hasPro excluded from the export payload',
        "'hasPro', 'tapOffsetMs', 'masterVolume',", []),
    ('BACKUP', 'session scratch excluded from the export payload',
        "'sessionTodayMs', 'sessionDate', 'sessionCompleted', 'sesModulesVisited',", []),
    ('BACKUP', 'reset keeps Pro (a reset button must not revoke a purchase)',
        "'notifications', 'sessionGoalMin', 'hasPro',", []),
    ('BACKUP', 'reset rebuilds from PROG_DEFAULTS, not a local literal',
        'Object.assign(JSON.parse(JSON.stringify(PROG_DEFAULTS)), kept)', []),
    ('BACKUP', 'restore is replace, and progState is written last',
        'progState = staged;\n    progSave();', []),

    ('ROADTRIP', 'Hand-tuned legs: gymnopedie',
        'gymnopedie:{tier:\'easy\',bpm:76,hooks:[{b:0,s:4.74},{b:12,s:7.9},{b:24,s:9.48},{b:62,s:20.53},{b:116,s:16.59}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: gnossienne',
        'gnossienne:{tier:\'easy\',bpm:60,hooks:[{b:0,s:8},{b:69,s:10},{b:128,s:18},{b:191,s:23},{b:301,s:23}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: ave_maria',
        'ave_maria:{tier:\'easy\',bpm:56,hooks:[{b:0,s:8.57},{b:8,s:9.64},{b:17,s:15.01},{b:32,s:16.11},{b:48,s:18.24}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: brahms_lullaby',
        'brahms_lullaby:{tier:\'easy\',bpm:76,hooks:[{b:0,s:3.95},{b:5,s:10.26},{b:18,s:8.68},{b:30,s:13.82},{b:47.49,s:10.27}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: greensleeves',
        'greensleeves:{tier:\'easy\',bpm:80,hooks:[{b:0,s:8.24},{b:12,s:8.27},{b:24,s:15},{b:49,s:17.26},{b:73,s:16.5}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: nocturne',
        'nocturne:{tier:\'medium\',bpm:50,hooks:[{b:0,s:12},{b:10,s:16.8},{b:24,s:15.6},{b:168,s:26.4},{b:189,s:27.6}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: canon_d',
        'canon_d:{tier:\'medium\',bpm:64,hooks:[{b:0,s:7.5},{b:8,s:7.5},{b:16,s:15},{b:32,s:14.53},{b:47,s:18.28}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: minuet_g',
        'minuet_g:{tier:\'medium\',bpm:96,hooks:[{b:0,s:3.78},{b:6,s:5.65},{b:15,s:5.66},{b:24,s:7.53},{b:36,s:8.16}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: ode_to_joy',
        'ode_to_joy:{tier:\'medium\',bpm:120,hooks:[{b:0,s:4},{b:8,s:6},{b:20,s:6},{b:32,s:7.5},{b:48,s:10}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: bella_ciao',
        'bella_ciao:{tier:\'medium\',bpm:100,hooks:[{b:0,s:5.4},{b:9,s:6},{b:19,s:7.8},{b:40,s:19.2},{b:72,s:23.4}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: st_louis_blues',
        'st_louis_blues:{tier:\'medium\',bpm:72,hooks:[{b:0,s:5.83},{b:7,s:6.67},{b:15,s:12.5},{b:58,s:20.82},{b:102,s:18.33}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: maple_rag',
        'maple_rag:{tier:\'hard\',bpm:88,hooks:[{b:0,s:3.41},{b:4,s:3.4},{b:8,s:6.14},{b:16,s:5.46},{b:23,s:7.5}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: entertainer',
        'entertainer:{tier:\'hard\',bpm:104,hooks:[{b:0,s:4.62},{b:7,s:4.62},{b:15,s:5.19},{b:23,s:9.23},{b:31,s:5.19}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: twinkle_stride',
        'twinkle_stride:{tier:\'hard\',bpm:200,hooks:[{b:0,s:4.5},{b:32,s:9.6},{b:119,s:9.9},{b:154,s:20.7},{b:223,s:15.9}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: hungarian_5',
        'hungarian_5:{tier:\'hard\',bpm:130,hooks:[{b:0,s:7.38},{b:16,s:7.39},{b:64,s:14.78},{b:96,s:20.33},{b:170,s:15.25}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: carol_bells',
        'carol_bells:{tier:\'hard\',bpm:144,hooks:[{b:0,s:5},{b:12,s:5},{b:36,s:10},{b:60,s:10},{b:84,s:15}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: arabesque_1',
        'arabesque_1:{tier:\'hard\',bpm:120,hooks:[{b:0,s:4},{b:8,s:10.5},{b:151,s:16},{b:202,s:15},{b:386,s:19.5}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: moonlight_3',
        'moonlight_3:{tier:\'hard\',bpm:152,hooks:[{b:0,s:11.76,ms:0},{b:29,s:9.83,ms:11447},{b:76,s:18.52,ms:30000},{b:122,s:36.6,ms:48158},{b:214.99,s:33.46,ms:84864}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: prelude_c',
        'prelude_c:{tier:\'hard\',bpm:72,hooks:[{b:0,s:13.33,ms:0},{b:16,s:21.67,ms:13333},{b:42,s:24.99,ms:35000},{b:72,s:29.99,ms:60000},{b:107,s:21.66,ms:89167}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: alla_turca',
        'alla_turca:{tier:\'hard\',bpm:120,hooks:[{b:0,s:13.5,ms:0},{b:27.54,s:13.5,ms:13770},{b:81.57,s:27,ms:40785},{b:149.26,s:34,ms:74630},{b:325.45,s:30,ms:162725}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: barcarolle',
        'barcarolle:{tier:\'easy\',bpm:69,hooks:[{b:0,s:13.7,ms:0},{b:16.3,s:14.83,ms:14174},{b:32.81,s:24.79,ms:28530},{b:87.82,s:35.75,ms:76365},{b:220.83,s:37.88,ms:192026}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: butterfly',
        'butterfly:{tier:\'medium\',bpm:132,hooks:[{b:0,s:11.83,ms:0},{b:25.73,s:12.01,ms:11695},{b:51.69,s:18.65,ms:23495},{b:104.81,s:24.45,ms:47641},{b:171.77,s:19.27,ms:78077}]}', []),
    ('ROADTRIP', 'Hand-tuned legs: moonlight_2',
        'moonlight_2:{tier:\'medium\',bpm:80,hooks:[{b:0,s:15.5,ms:0},{b:21.05,s:16,ms:15788},{b:42.73,s:18.25,ms:32047},{b:66.74,s:28.25,ms:50055},{b:140.92,s:19.25,ms:105690}]}', []),
]
# A second presence-with-count guard for the diadle 5-guess pin (needs >=3 hits)
DIADLE_GUESS_MIN = 3
# SON CLAVE 3-2 and KPANLOGO carry byte-identical step arrays; the groove audit
# accepts that as correct, not a duplicate. So the pin needs an EXACT count: two.
# Fewer means one of them was edited; more means a third groove drifted into the
# same pattern, which would also be worth knowing about.
SON_CLAVE_PATTERN = 'steps: [2,0,0,2,0,0,2,0, 0,0,2,0,2,0,0,0],'
SON_CLAVE_EXPECT  = 2


def run(filepath):
    # Windows consoles are often cp1252; checkmarks then crash the gate.
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    try:
        text = open(filepath, encoding='utf-8').read()
    except Exception as e:
        print(f"  ✗ cannot read {filepath}: {e}")
        return 2

    # Version check + report which build we're sentinel-ing
    vm = re.search(r'INTONARE_VERSION:\s*([\d.]+)', text)
    ver = vm.group(1) if vm else '??'
    print(f"\n{'='*70}\n  INTONARE REGRESSION SENTINEL — checking build v{ver}\n{'='*70}")

    failures = []
    by_area = {}
    for area, desc, kind, sig, mn in CHECKS:
        if kind == 'sub':
            cnt = text.count(sig)
        elif kind == 'absent':
            cnt = text.count(sig)
        else:
            cnt = len(re.findall(sig, text))
        ok = (cnt == 0) if kind == 'absent' else (cnt >= mn)
        by_area.setdefault(area, []).append((ok, desc, cnt, mn, sig))
        if not ok:
            failures.append((area, desc, cnt, mn, sig))

    for area in by_area:
        print(f"\n  {area}")
        for ok, desc, cnt, mn, sig in by_area[area]:
            mark = '✓' if ok else '✗ REGRESSED'
            note = '' if ok else f"   (found {cnt}, need {mn}: «{sig[:48]}»)"
            print(f"    {mark}  {desc}{note}")

    # ── Exact-value pins (drift detection) ─────────────────────────────────
    pin_failures = []
    print(f"\n  EXACT PINS (specific values — flag silent drift)")
    for area, desc, must, must_not in EXACT_PINS:
        present = must in text
        bad = [b for b in must_not if b in text]
        # special-case the diadle multi-hit pin
        if must == SON_CLAVE_PATTERN:
            cnt = text.count(must)
            present = (cnt == SON_CLAVE_EXPECT)
            extra = f" (found {cnt}, expected exactly {SON_CLAVE_EXPECT}: son32 + kpanlogo)" if not present else ''
        elif must == 'maxGuesses:5':
            cnt = text.count(must)
            present = cnt >= DIADLE_GUESS_MIN
            extra = f" (found {cnt}, need {DIADLE_GUESS_MIN})" if not present else ''
        else:
            extra = ''
        ok = present and not bad
        if ok:
            print(f"    ✓  [{area}] {desc}")
        else:
            reason = ''
            if not present: reason = f" — expected value «{must[:40]}» missing/changed{extra}"
            elif bad:       reason = f" — drift value present: {bad}"
            print(f"    ✗ DRIFTED  [{area}] {desc}{reason}")
            pin_failures.append((area, desc))

    print(f"\n{'='*70}")
    total_fail = failures or pin_failures
    if total_fail:
        n = len(failures) + len(pin_failures)
        print(f"  ⚠  {n} ISSUE(S) DETECTED — do not ship until resolved:")
        for area, desc, cnt, mn, sig in failures:
            print(f"     ✗ REGRESSED [{area}] {desc}")
        for area, desc in pin_failures:
            print(f"     ✗ DRIFTED   [{area}] {desc}  (intentional? update the pin)")
        print(f"{'='*70}\n")
        return 1
    print(f"  ✓ All {len(CHECKS)} tracked fixes present + {len(EXACT_PINS)} pins hold. No regressions.")
    print(f"{'='*70}\n")
    return 0


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Intonare regression sentinel')
    p.add_argument('filepath', help='Path to Intonare.html')
    args = p.parse_args()
    sys.exit(run(args.filepath))
