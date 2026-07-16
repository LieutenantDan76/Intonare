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

## v0.94.4

**Drop exact-alarm dependency from reminders (Play review risk reduction)**

Removed `allowWhileIdle: true` from both LocalNotifications schedule blocks (practice + streak
reminders). allowWhileIdle is what pulls Android's SCHEDULE_EXACT_ALARM permission into the
build; that permission is on Google Play's restricted list (meant for alarm-clock / calendar
apps) and is an avoidable question on a first production review. Daily practice/streak nudges
don't need to-the-second timing — without it they're inexact, so on a phone in deep Doze they
may arrive a few minutes late; in normal use they're on time. No feature loss for a reminder.

COMPANION EDIT (manual, on the build machine — NOT in the HTML): delete this line from
native_src/AndroidManifest.xml:
    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
Then verify the MERGED manifest (android/app/build/intermediates/merged_manifests/) no longer
contains SCHEDULE_EXACT_ALARM — the local-notifications plugin can re-inject it. If it does,
add a tools:node="remove" override in the source manifest.

Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.94.3

**Organ + Rhodes now-playing / SONGS / song-bank all match their instrument motif**

The NOW PLAYING screen, SONGS button, and song-bank popup were piano-flavoured everywhere: the
organ/rhodes panels showed the generic blue-grey keep-dark fallback for np-screen/songs, and the
shared popup opened CREAM over the wood organ + dark Rhodes (the cream .riff-popup rule wasn't
instrument-scoped). Now each instrument's controls match its skin:

- ORGAN (keeps its dark wood console in light mode): np-screen -> dark wood (#2a1a0c), transport
  buttons + SONGS -> warm brown (#5a3a1d) with amber text (#f0d0a0). Song-bank popup themed via
  riffOpenPopup's data-inst="organ" -> wood-dark card, amber era headers, amber accent.
- RHODES (dark stage-piano skin, silver + red accents): np-screen -> dark neutral, transport +
  SONGS -> brushed silver (#d8d8d8) with the Rhodes RED (#a01015) as the accent. Popup via
  data-inst="rhodes" -> dark card, silver face, red era headers/accent.
- PIANO popup stays cream (data-inst="piano"/unset); [data-inst] attribute selectors outrank the
  generic cream rule so each instrument themes independently.

Verified via Playwright: organ np/songs/popup = wood, rhodes = silver/red, piano popup = cream.
All body.light CSS, no JS (data-inst was already set by riffOpenPopup). Dark mode untouched.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.94.2

**Cream piano tab strip — whole strip adopts the ACTIVE instrument's family**

The light tab strip tinted each tab by its OWN instrument permanently (organ always wood,
rhodes always silver), so the strip looked like three different materials no matter what was
selected — e.g. on the Rhodes panel the strip still showed a cream PIANO + wood ORGAN + silver
RHODES mishmash. Dan wants the whole strip to match whichever panel is open.

Rewrote the light tab rules with :has(): the strip detects which tab is .active and tints ALL
THREE tabs in that instrument's family — all cream on piano, all wood on organ, all silver on
Rhodes. Active tab is the brighter version, inactive siblings dimmer. Pure CSS, no JS.

Verified via Playwright across all three active states: PIANO->cream trio, ORGAN->wood trio,
RHODES->silver trio, each with the active tab brightest. :has() renders correctly in the WebView.

Dark mode tab strip untouched (its inactive tabs are neutral grey which already reads fine on dark).
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.94.1

**Splash CRT — remove the bar's extra glow layer at the seam (both modes)**

The crossfade (0.94.0) already runs in BOTH light and dark — the waveFade/barFadeIn logic
was never light-gated, only the glow *reduction* is. So dark already crossfades; confirmed.

Remaining mismatch: the CRT bar drew a fat wide-glow layer (7px / blur 24) that the wave core
has no equivalent for — and the wave's own wide/mid halos have already faded out by the hand-off
(they ride waveFade). So the bar showed "extra glow" the wave didn't, right at the join. Fixed
by gating the bar's wide-glow layer to the PINCH: ×_smoothstep(p2), so it's ZERO during the flat
hold/crossfade (matching the wave's faded-halo seam) and ramps in only as the bar collapses inward
— where the CRT power-off actually wants that bloom. Mode-independent, so light and dark both match
at the seam now. The gold core (2.2/blur14) + faint white centre (1.0/blur6) already matched the
wave core and are unchanged.

Light crossfade continuity re-confirmed via frame sampling; dark uses the identical code path.
Splash draw only.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.94.0

**Splash CRT hand-off — true crossfade (kills the snap for good)**

Previous attempts matched the bar's *recipe* to the wave but kept them mutually exclusive
in TIME: wave drew until T_WAVE_END, bar drew after — a hard cut. Even a perfectly-matched
line cut-swaps visibly. Fixed with an actual crossfade:

- Added a 0.28s overlap window on each side of T_WAVE_END. The wave line now keeps drawing
  ACROSS the boundary, fading out (waveFade 1->0), while the CRT bar fades IN (barFadeIn
  0->1) over the same window — both at full width, identical line recipe (gold core 2.2px /
  blur 14 + faint 0.7x white centre). The wave amplitude is ~0 there (raised-cosine decay),
  so the near-flat wave dissolves seamlessly into the flat bar.
- Bar gate changed from `crt > 0` to `crt > 0 || barFadeIn > 0.01` so it starts drawing
  during the crossfade; its alpha ×barFadeIn. After the window it's business as usual
  (hold -> pinch -> flare).

Verified via Playwright frame-sampling across 2.6s-3.1s (spanning T_WAVE_END=2.8): the line
stays continuous every frame — no vanish, no brightness spike, no white bar. Zoomed boundary
crop shows one clean gold line throughout.

Dark splash unchanged (crossfade applies in both, recipe identical to before outside the
window). Splash draw only.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.9

**Splash CRT hand-off — make the two lines identical (fix the white-bar snap)**

0.93.8 made it worse: reducing the CRT bar's coloured glow (_glowMul) gutted its gold but
left the white core at full alpha/1.8px, so the bar rendered as a BRIGHT WHITE bar while the
wave was a thin gold line — gold->white jump at the pinch.

Fix: the collapsing bar now uses the EXACT same recipe as the wave core instead of a white
bar — gold `col` at 2.2px / shadowBlur 14, plus a faint 0.7× white centre at 1.0px (mirrors
the wave's crisp-core + white-hot-centre pair). Also matched the bar's pickup brightness to
the wave's core: holdLvl now starts at 0.72 (was 0.34) so there's no dim step at the hand-off.
Net: the pinch reads as the wave straightening and collapsing to centre, same colour + weight
throughout — not swapping into a different bright line.

NOTE: this is a timing/feel change I can't fully verify headless (the transition frame is non-
deterministic to catch). The recipe now provably matches the wave line; on-device confirmation
of the actual motion is the real test.

All in the splash draw. Dark splash unchanged.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.8

**Cream piano nameplate shadow + splash CRT hand-off**

NAMEPLATE: the silver "GRAND PIANO" oval had a hard black drop shadow (0 2px 8px
rgba(0,0,0,.7)) + dark ring — fine floating on the old black card, heavy on cream.
Light-mode override: tight warm shadow (0 1px 3px rgba(120,95,40,.28)) + warm hairline
ring, so the plate sits on the surface without punching a dark halo. Inner bevels warmed
too. Dark card untouched.

SPLASH CRT SNAP: the real cause of the abrupt hand-off — in light mode the WAVE glow was
reduced (0.93.7) but the CRT bar that the wave pinches into still drew its glow at FULL
strength (shadowBlur 24 / 10). So the halo popped back on at the exact transition frame =
visible snap. Applied the same _glowMul (0.18) / _blurMul (0.35) to the CRT bar's coloured
glow + softened its white-core blur (×0.6) in light mode, so wave-end and bar now carry a
matching minimal halo and the pinch is continuous. Dark splash unchanged.

All body.light CSS + scoped splash-draw branches. Dark mode untouched.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.7

**Cream piano lid — the actual fix (WebView native button bevel) + splash wave halo**

LID (finally): after removing every shadow/border/filter and still seeing the dark edge
on-device (while desktop rendered pixel-perfect cream), the culprit was the one thing left:
.piano-lid-seg is a <button> and my rules only set border-right — the other three sides fell
back to the WebView's NATIVE BUTTON bevel (a dark inset chrome the Android WebView draws but
desktop Chromium doesn't). Fix: -webkit-appearance:none + appearance:none + explicit
border:0 solid transparent on all sides (border-right kept as the divider), outline:none.
Applied to both inline (#ptoPianoPanel) and expanded (#pianoOverlay) lids. This is the real
root cause — the previous three attempts were chasing shadows that were never there.

SPLASH WAVE: on the light splash the wave's coloured glow halo (shadowBlur strokes) muddied
into a dark fringe on the lavender bg, and since the CRT bar it pinches into at the end has no
halo, the hand-off looked abrupt. Added an html.light-root check in drawGatherParticles: in
light mode the outer wide+mid glow layers drop to 18% alpha / 35% blur, so the wave reads as a
clean bright line that matches the CRT. Dark splash unchanged. Core + white-hot centre untouched
(they're the bright line, not the halo).

TONE BANK: non-issue — that was just the phone held in portrait (confirmed by Dan).

All body.light CSS + one scoped splash-draw branch. Dark mode untouched.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.6

**Cream piano — lid bulletproofed (WebView dark-edge fix)**

The lid segment control kept showing a dark edge on-device despite rendering clean cream
in every desktop test (verified down to pixel sampling: the only sub-cream pixels were the
antialiased brown TEXT, no dark outline anywhere in the CSS). Concluded the on-device edge
is the Capacitor WebView compositing the inset box-shadows / near-transparent segment
backgrounds differently from desktop Chromium.

Bulletproofed both views (inline #ptoPianoPanel + expanded #pianoOverlay): removed ALL
inset box-shadows from the segments (the most likely WebView culprit), swapped the near-
transparent segment backgrounds (rgba(120,95,40,.06)) for flat OPAQUE cream (#e8dcc0),
active segment flat #fbf6ec, single clean #cbb891 warm border. Also removed the redundant
v0.93.1 duplicate lid-seg rules that were shadowed by the later block (source-order
confusion risk). Text darkened slightly (#7a6844 / #3a2f1c) for contrast on the opaque fill.

All body.light CSS, no JS. Dark mode untouched.

STILL OPEN (need on-device screenshots, can't reproduce/verify headless):
- Expanded tone bank opens vertically; wants horizontal + scrollable to match the inline
  bank. Layout change — need to see the actual vertical popup before restructuring it.
- Splash sine wave has a faint dark outline on the light splash. It's a canvas-drawn glow
  (coloured shadowBlur strokes over the light bg); the fringe mechanism needs the animation
  rendered to pin down. Flagged, not yet touched.

Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.5

**Cream piano — fullscreen leftovers (key-lip strip, tone-bank button, lid polish)**

Landscape screenshot of the expanded piano caught three stragglers:

- BLACK STRIP along the top of the keys: .piano-keyboard-full::before is a 14px
  #020204 shadow lip where keys meet the fallboard — invisible on the old dark stage,
  a hard black bar on cream. Warmed to a soft brown key-shadow (rgba(120,95,40,.35)->
  transparent) so keys still look seated in the case.
- TONE-BANK BUTTON: the "⌨ GRAND PIANO" chip in the overlay header (.piano-overlay-
  voice-btn) was still dark (#1c1c22). It's populated into #pianoOverlay (keep-dark) so
  body.light skipped it. Creamed + cocoa text, green caret kept as accent. Also pinned
  .tone-chip cream in the overlay in case any render as chips.
- LID: renders confirm the wrap border + segments are already cream in BOTH views (the
  black-outline look was a photo/contrast artifact, not a real dark value — verified via
  Playwright element crops). Defensively softened the active-segment inset ring across
  all three lid rule sites (card / dup / overlay): rgba(150,125,70,.25)->rgba(165,142,95,
  .16) so there's zero chance it reads as a dark edge against the white active segment.

All #pianoOverlay-scoped body.light CSS, no JS. Dark mode untouched.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.4

**Cream piano — the expanded fullscreen piano (its own pass)**

The fullscreen EXPAND view was still fully dark. Root cause: the old body.light rules
targeted .piano-key-well / .piano-fallboard, but the overlay's real classes are
.piano-overlay-key-well / .piano-overlay-fallboard — so they never matched and the
overlay stayed on its dark stage. Rewrote the whole overlay treatment.

#pianoOverlay is .keep-dark (excluded from body.light), so every rule targets
#pianoOverlay explicitly to override. .keep-dark only re-declares CSS vars, and these
rules set literal !important colours, so no conflict. Dan-approved: fullscreen goes
cream too (not spotlit-on-dark).

Converted, warm-neutral convention (cream surface, mid-beige frame, cocoa text, one
green accent):
- Stage background: dark room (#111114->#050507) -> warm cream (#efe4cc->#ddcfb0).
- Key-well frame + fallboard -> cream lacquer case (correct -key-well/-fallboard classes).
- Keyboard bed behind the keys -> warm cream so key gaps read as wood shadow, not a void.
  White div-keys unchanged (they already look right on any bg).
- Chrome buttons (close, octave nav, width toggle) -> cream + cocoa text + hover states.
- Pedals / lid / now-playing / SONGS button reuse the inline cream treatment, re-scoped.
- Brushed-metal nameplate left as-is (reads fine on any background).

Verified via Playwright: overlay/key-well/fallboard/bed/chrome all compute cream in
forced light mode; screenshot confirms it reads as one coherent warm instrument.

NOTE on the lid "black outline" from the 15:20 screenshot: that was a pre-0.93.3 build.
The .piano-lid-seg-wrap border fix landed in 0.93.3 (v0.93.1 only styled the segments,
not the wrap, so the wrap kept its base black box-shadow). Computed border in the current
file is #cbb891 cream — confirmed via Playwright. Re-download resolves it.

All body.light CSS, no JS. Dark mode untouched.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.3

**Cream piano — pedals, lid frame, and the SONG BANK / TONE popups**

More dark holdouts cleared from the light acoustic-piano tab (screenshots):

- PEDALS: the chrome pads are real pedals and stay silver; the black recessed SLOT
  they sat in read as a hard outline on cream. Warmed the slot to a shallow cream
  recess (#d8c8a4->#ebe0c8) so each pad sits in wood, not a black hole. Pad-down glow
  colours (soft violet / sost cyan / damper green) untouched. Pedal names -> warm brown.
- LID segment control: the CLOSED/STICK/OPEN wrap border was faint-white-on-cream so
  the left edge looked unfinished. Frame + segments + text rewarmed; active segment
  brighter cream.
- SONG BANK popup + TONE popup: shared full-screen modals (piano/organ/rhodes). A black
  modal over a light app reads as forgotten, so creamed them — warm card (#f6efdd),
  cocoa body text, mid-beige dividers, green kept for the accent rail (era headers, play
  carets, active tile). Scrim -> warm-dark (rgba(60,48,24,.5)) so it dims like a lit room
  rather than a blackout. creditsModal reuses .riff-popup-card so it follows too.

All body.light-scoped CSS, no JS. Dark mode untouched.

DEFERRED to its own pass: the EXPANDED fullscreen piano (#pianoOverlay, .keep-dark). It's
a large immersive surface — nameplate, nav, fallboard, key-well borders, dark background,
plus the dark keyboard well — and converting spotlit-on-dark to cream-on-light is a full
redesign that needs its own screenshot loop, not a tail-end batch.

Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.2

**Cream piano — the remaining dark holdouts (tabs, expand, screens, tone bank)**

On-device screenshots showed the v0.93.1 cream card still had black islands. Cleared
them all, following warm-neutral UI convention (cream surfaces, mid-beige structure,
deep cocoa text — not washed-out grey; one accent kept for the CTA):

- TABS: inactive ORGAN/RHODES tabs no longer share one flat dark gradient. Each previews
  its instrument in a muted cream-friendly tint (organ dusty-wood, rhodes pewter-silver,
  piano neutral cream) so the strip reads as three instruments before you tap. Strip
  border -> #d0bf98.
- EXPAND button -> warm cream, cocoa text (#5a4a2c).
- LID direction-icon: silhouette + lid line rewarmed (#pianoLidSvg rect/line light-branched).
- NOW-PLAYING screen: was a black LCD recess reading as a hole in the cream. Lightened to
  a warm off-white display (#f6efdd->#efe4cc) with softened scanlines + inset so it still
  reads as a screen; idle text -> cocoa. Transport buttons creamed.
- SONGS button -> amber-cream, kept the green CTA text so it stays the primary action.
- TONE bank: family pills + all instrument tiles -> cream tile bodies, cocoa labels, emoji
  kept (content not chrome). Selected pill/tile gets a sage-tinted state so the choice pops.

All body.light + #ptoPianoPanel-scoped CSS; ID specificity beats the global .np-screen dark
rule so organ/rhodes screens stay dark. No JS touched. Dark mode untouched.
Sentinel: all 97 tracked fixes present + 39 pins hold.


## v0.93.1

**Cream piano — finish the card chrome + kill the dark seam on the keys**

Two loose ends from the v0.93.0 cream-piano pass:

1. CARD CHROME: the piano panel's card base, nameplate strip, lid bar, and the PIANO
   tab were all still tuned for a black lacquer slab, so on light the cream keybed sat
   inside a black box. Added body.light overrides scoped to #ptoPianoPanel: card base ->
   warm cream gradient (#f4ecdb->#e2d5ba), softened the black-tuned gloss arc + specular
   line, nameplate/lid borders -> warm brown alphas, lid labels/segments -> cream family,
   and #ptoPianoTab.active -> cream gradient so the tab matches the panel below it.

2. KEY SEAM: the octave-separator line (drawn every 7th white key in csDrawKeyboard) was
   hardcoded rgba(46,46,72,0.8) dark blue-grey. On the cream/white keys it read as a dark
   scratch splitting the keyboard down the middle at the octave boundary. Light-branched
   via the existing _csLightPiano flag -> rgba(180,162,120,0.5), 1px (was 1.5px).

Dark mode untouched — all changes are body.light CSS + one _csLightPiano-gated ternary.
Sentinel: all 97 tracked fixes present + 39 pins hold.



































































## v0.93.0

**Cream piano — light-mode Elton-white treatment (closes the color checklist)**

The acoustic-piano tab now reads as a warm white-lacquer instrument in light mode instead of
a black slab on the pale card. Dan-approved option F: option B's bright cream case + lid, with
TRUE WHITE keys (not ivory) and a heavier warm outline so they read crisply against the cream.

Inline card (CSS, body.light, scoped to #ptoPianoPanel): .piano-key-well body #f0e6d2,
.piano-fallboard lid cream gradient, octave-bar buttons cream. Playable keyboard
(csDrawKeyboard, scoped via pianoToolTab==='piano'): natural keys -> pure white gradient,
keyboard bg rect -> cream #f0e6d2, black keys stay dark. Reference diagram (buildPianoKeyboard):
white keys + 1.4px outline, cream-friendly marker/octave labels.

Expanded fullscreen piano: cream piano BODY but the immersive DARK stage stays (white piano
spotlit on a dark stage — chosen to keep the fullscreen drama, not a fully light overlay).

Scoping is careful: pianoToolTab==='piano' gates the keyboard changes so ORGAN (Hammond) and
RHODES keep their own skins, and the chord/scale keyboards are untouched. Dark mode verified
byte-equivalent — keyboard region still #09090f, grey keys. Highlights (Middle C, A4) and
labels preserved in both modes.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.92.9

**Light-mode washout batch #2**

Pitch-stability graph structure alphas boosted + 2px trace. Vocal-range waveform + history
deepened (new vrVoiceColor mapper). Polyrhythm challenge-end panel (badge/buttons/stats via
CSS). Trombone slide diagram. Splash particles (light-root deepening). Two mode-staff ticks.
All in-draw light branches; dark untouched.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.92.8

**Light-mode washout batch #1**

Settings toggles solid ON state. Polyrhythm rings, rhythm-reading picker, latency canvas all
deepened for light. Dark untouched.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.92.7

**Survival Guide title pages** — _ttDarkenForLight() darkens bright per-page tab_color hues on
the mint card; split --tt-color (dark title) from --tt-glow (bright wash). Dark untouched.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.92.6

**SG notation diagrams** (clef/values/bars/roadmap) light-branched; sgDrawModeStaff white block
fixed. Built intonare_draw_color_sweep.py. Dark byte-identical.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.92.5

**Second contrast pass** — six accent hexes bumped from 3.1-4.2:1 to >=4.6:1, light-scoped, dark
byte-identical.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.92.4

**Programmatic contrast audit — stop eyeballing, start measuring**

Instead of Dan spotting faint text one screenshot at a time, built a contrast audit that
measures every light-mode text/background pair and flags failures. Found the real answer
to "hard to see": ~41 accent text colors that PASS AA-large (3:1) but sit at 3.0-3.5 —
technically legible but marginal, especially for smaller text / older eyes (Linda).

Deepened the whole borderline accent family by one step to ~4-4.8:1 (comfortable, not
barely-passing): all/rose #c0335f->#a3284d, red #c0331f->#a32718, gold #8a5f00->#6f4d00,
green #0b7048->#095c3a, purple #6248bf->#5238a5, and game-label cyan #006f8f->#005570
(scoped to labels, not the tuner screen hero). Borderline count 41 -> 25 (rest are
dup-counted selectors + tinted-bg cases that are fine).

Verified the deepened hexes only appear in light-mode contexts (the light --sharp/palette
+ game overrides); dark-mode base accents untouched.

Shipped the audit script (intonare_light_contrast_audit.py) so this is repeatable, not a
one-off — future light-mode work can run it instead of screenshot-hunting.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.92.3

**Methodical Train/Tools screen-by-screen audit (the real one)**

Mapped all 31 modules, scanned each for the two light-mode failure modes (hardcoded dark
screens + bright-color content), categorized intentional-dark vs orphans, fixed orphans.

DARK-SCREEN scan: only toolTonal is keep-dark (intentional). CSS scan of all dark-bg
rules showed the rest are intentional instrument surfaces (piano-*, tc-* CRT, thmn-*
theremin, np-screen now-playing, org-/mel-/leslie- organ+melodica). Orphans (ce-screen,
rr-tap-zone) already lifted in 0.92.0.

BRIGHT-COLOR scan (per module prefix) found the real concentrations + fixed:
- INTERVAL (iv-, 15 rules): hit/miss dots (#34d399/#f87171 -> #0b7048/#c0331f), perfect,
  correct/wrong answers, target-miss, difficulty chips + pills (medium #6248bf, hard
  #8a5f00, all #c0335f, custom #006f8f), reveal note. All deep-on-light.
- RHYTHM READING (rr-, 8): survival streak/stats/diff/best/bar reds deepened. Tap-zone
  feedback (fg/fy/fo/fr) left bright — those sit on the dark charcoal tap zone (correct).
- CHORD EAR (ce-, 6): difficulty labels are INSIDE the lifted ce-screen (dark) so bright
  is correct there; verified nesting, left as-is.
- TEMPO (tg-): normal-tier difficulty label deepened.
- SURVIVAL GUIDE (sg-): mode chars/rungs already had light overrides; confirmed.

Method: per-module inventory, context-check each (on-dark-screen vs on-light), fix only
what's genuinely on light. Not screenshot-driven this time.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.92.2

**Metro screen: groove pips visible + warmer/airier (fix "seems dark")**

- **Groove pips (.gs-step beat cells):** were faint white/gold (rgba .04-.35),
  near-invisible on light. Themed all states: base cell, beat-marker, soft, accent,
  cursor, beat-pulse — deep warm with clear fills + borders so the beat grid reads.
- **"Seems dark" fix:** the accumulated deep-brown text (BPM was #5a3d00 = 5.8:1, heavy)
  read muddy. Lightened the screen bg (#c6c4c0->#d4d2cc airier) AND warmed the content
  from heavy brown to a lively amber-gold (BPM #7a5410, name #8a5e10, groove-name
  gradient warmer). Now reads as a warm amber display, not dark brown. Still AA-large.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.92.1

**Metro screen: full content pass (every element, not 5 of 25)**

The metro screen was rough because I'd themed ~5 of its ~25 on-screen elements. Did a
proper inventory (grepped every class rendering inside .metro-screen) and themed ALL of
it deep-warm-on-light:
- drum sound buttons (CLICK/WOOD/COWBELL/CONGA/RIM/HI-HAT/etc) — were faint gold 4%
  fill, invisible; now readable brown with visible borders + active state
- beat number (rose "1") deepened, top vol/menu icons
- GROOVE mode: label, name (gradient), origin/style, beat cells, bpm, grid borders
- pulse toggle + dots + pulse-off state
All verified for contrast (BPM 4.9:1, buttons 3.8:1, deepened the borderline rose/origin
to hold on the screen).

Next: the promised methodical screen-by-screen Train/Tools audit.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.92.0

**Orphan game screens found + lifted (the audit I should've done)**

Dan rightly called out that my "comprehensive" passes weren't — the chord-ear display,
rhythm-reading tap zone, and note-pop screen were pure-black-on-light and had never been
touched. They're ORPHANS: hardcoded dark, not keep-dark (intentional), not following
light. Never audited because they're deep in game modules the screenshots hadn't hit.

Systematic grep for hardcoded dark backgrounds on light-following elements found them.
Lifted (they're immersive game displays — dark is fine, but pure-black reads broken):
- ce-screen (chord ear): purple-charcoal gradient matching the module hue
- np-screen (note pop): charcoal
- rr-tap-zone (rhythm reading): charcoal + charcoal-next state

HONEST NOTE: this is a partial fix of a real gap. A truly complete screen-by-screen
audit of every Train/Tools game module is still owed — difficulty chips, survival
sub-buttons, and any other module-specific colors need a dedicated pass rather than
more screenshot-driven patching. Metro screen readability also still being tuned.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.9

**Metro screen readability fix + tuner bloom restored**

- **Metro screen was too yellow + low contrast:** the warm C2.5 (#d0c9b0->#c2ba9c) was
  over-saturated and the all-brown content blended in — BPM barely readable, drum
  buttons (CLICK/WOOD/etc) were ghosts. Shifted the screen to a NEUTRAL-warm dusty
  (#c6c4c0->#b8b5ae, much less yellow), deepened content (BPM #5a3d00), and gave the
  on-LCD sound buttons real contrast (deep brown text + visible borders + active fill).
  BPM wheel gold deepened to match.
- **Tuner lost its bloom:** the soft color-wash on the tuner card came from the dark
  screen's colored glow bleeding into the card. When the screen went light (C2.5) that
  colored glow became a plain shadow, so the bloom vanished. Re-added it as a background
  radial (same safe method as String Guide) on .tuner-bpm-card. Both cards now carry
  the matching bloom.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.8

**HOTFIX: bpm wheel canvas crash (my quoting bug from 0.91.7)**

The 0.91.7 bpm-wheel light-awareness edit wrapped the template literals in single
quotes: '`rgba(${_wg},...)`' — so JS passed the literal string (backticks and all) to
addColorStop, which threw "could not be parsed as a color" and crashed the wheel draw.
Fixed: stripped the surrounding single quotes so they're real backtick template
literals. All 11 occurrences corrected. Verified: node --check clean, template
evaluates to proper rgba(111,77,0,0.14), scanned for any other quote-wrapped-backtick
mistakes (none). No other screen affected.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.7

**Tuner screen fully audited/completed + metro LCD converted to light**

- **String Guide bloom (safe version):** re-added the top color-wash, this time baked
  into the card's own background gradient (radial over the surface) — no pseudo-element,
  no child positioning, so it CAN'T break layout like the 0.91.5 version did.
- **Tuner screen element audit — found + fixed gaps:** cross-referenced every DOM child
  of .tuner-screen against the light overrides. Missing: tuner-screen-label (OCT, was
  coral), tuner-screen-side (muted), tuner-screen-unit, meter-fill glow, and the
  verdict feedback (perfect/close/off used bright neon text-shadows). All themed
  deep-on-light + neon glows softened to subtle 1px shadows (neon muddies on light).
- **Metro LCD -> warm C2.5 light:** screen bg warm dusty (#d0c9b0->#c2ba9c), BPM number
  + unit + labels deep warm (#6f4d00), and the BPM WHEEL canvas made light-aware (deep
  gold at boosted alpha; was faint gold-on-dark).

Checkpoint: tuner (flagship) + metro both fully light now. Volume meter already
light-aware (dbCanvas). Theremin + tonal-centre controls next.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.6

**String Guide bloom bug fixed + C2.5 screens + hero content deepened**

- **BUG: String Guide card blew up to full height.** The bloom ::after I added in
  0.91.5 came with `#stringGuideCard > * { position:relative }` which broke the card's
  internal grid layout, expanding it. Removed the bloom entirely — it caused more than
  it solved, and the tuner/guide difference was always cosmetic. Card back to normal.
- **C2.5 screens:** both tuner LCD + chroma to the midpoint between C2 and C3
  (#b6bdd3->#a6afc8) per Dan. Between "light card" and "slate display."
- **Screen content audit + deepened:** verified every screen element holds AA-large+ on
  C2.5, then deepened the HERO elements for more pop: note letter + freq (#004a60),
  cents/needle states (in-tune #264c00, sharp #8f2416, flat #163b8f). Strobe canvas
  synced to the same deepened palette. Now the lit elements stand up clearly against
  the screen instead of sitting soft.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.5

**Screens -> C3 slate + bezels matched + String Guide bloom added**

- **C3 slate:** both tuner LCD and chroma strip swapped from C2 to C3 (darker slate
  #aab2ca->#9aa4bf) per Dan's pick — more "display" presence while staying light.
  Content deepened to match (meter track #8f9ab8, chroma notes deeper).
- **Bezels unified:** the tuner and chroma screens had different base 3D edges (tuner
  0 4px thick raised edge, chroma 0 3px) making one look more dimensional. Gave both
  the SAME light box-shadow recipe (inset well + edge-light + soft drop) so they read
  as matching displays.
- **String Guide bloom (Dan's idea):** rather than explain away the tuner-card-has-a-
  screen-bloom difference, ADDED a matching soft radial bloom to the top of the String
  Guide card (via #stringGuideCard::after, theme-tinted). Now the two cards read
  consistently instead of one having screen-glow and one flat.

Pending on-device: C3 look + whether the String Guide bloom makes them match.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.4

**Chroma strip -> light C2 + inset softened + String Guide bloom identified**

- **Chroma strip converted to C2 light** matching the tuner LCD: light dusty blue-grey
  bg, note labels dark-on-light (rgba(40,55,95,.32) resting, #005c78 active), label
  deep cyan. Now the whole tuner top (screen + chroma) is consistent light screens.
- **Inset shadow softened:** the recessed-well shadow was a touch harsh (.22/.18) ->
  eased to .14/.13 + brighter top edge-light. Still reads recessed, less severe.
- **String Guide "different color" SOLVED (Dan figured it):** it IS the same card token
  — but the tuner card CONTAINS the screen, whose drop-shadow blooms down into the card
  bottom; String Guide has no screen so no bloom. Same color, different content casting
  a gradient. Genuinely cosmetic + not matchable without faking a bloom on the guide.

Pending on-device look at the whole tuner page (both screens light now) to judge overall
theming coherence before rolling to metro/volume/theremin.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.3

**TRUE LIGHT SCREEN — tuner LCD converted to C2 (flagship)**

Big direction change: instead of a lifted-charcoal dark screen (which is inherently
harsh on a light page), the tuner LCD is now a true LIGHT recessed display (C2 "dusty
blue-grey" from the prototype Dan picked). A light screen with real inset depth so lit
elements have something to read against — how real light-mode instrument apps do it.

Full content re-theme (a light screen is not a bg swap — every element flips):
- bg: dusty blue-grey gradient (#c2c8dc->#b2bad2) + strong inset shadow (recessed well)
- note letter: deep cyan->green gradient (was glow-on-dark)
- freq/cents/octave: deep cyan (#005c78)
- cent meter: track #a6b0cc, dark ticks, needle deep green/red/blue by tune-distance
- FLAT/SHARP head, STROBE button, OCT: deep-on-light
- strobe CANVAS: made light-aware (deep colors at higher alpha; was bright-on-dark glow)

This is the FLAGSHIP — one screen done fully right. Pending Dan's on-device approval
before rolling the same treatment to metro, volume meter, etc. Tonal-centre CRT stays
dark by design (green phosphor is its identity); its surrounding CONTROLS will follow
light once the pattern's proven.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.2

**Screens tinted per-module + metro START softened**

- **Screen module-tinting:** the lifted charcoal screens were neutral grey; gave each a
  hint of its tab hue so they feel integrated + easier on the eyes. Tuner LCD + chroma
  = cool blue-charcoal (#3a4058), metro LCD = warm-charcoal (#46402f), tonale = violet-
  charcoal (#2a2640), theremin + CRT already green. Content contrast still 8:1+.
- **Metro START button:** grad-metro (gold->coral->pink) + a big 30%-opacity glow read
  aggressive against the soft light palette. Softened in light mode to a calmer amber
  gradient (#f0b93d->#e89b52) with dark text (9:1) + a lighter shadow. Still clearly the
  primary "go" action, just not shouty.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.1

**Splash to light + screens lifted from "dark smudge" to medium charcoal**

- **Splash light palette:** now uses the tuner light palette (#bdc1db gradient) when
  light mode is detected (auto — via the existing html.light-root pre-paint boot, same
  intonare_appearance pref the app reads). Dimmed the bright particle animation (opacity
  0.35) and remapped the logo gradient (bright #5ee2ff/#7aafff -> deep #006f8f/#2358c8)
  + sub/tag colors so they read on the light bg. No more black-splash-into-light-app jar.
- **Screens lifted (the "big dark smudge" fix):** measured that the LCD content (cyan
  text, green needle, white readouts) keeps 8-11:1 contrast even on a medium charcoal,
  so there was tons of headroom. Lifted every screen a full step:
  - keep-dark palette: bg-0 #0a0a12 -> #262636, surface #181826 -> #313146
  - tuner/metro LCD layers: #38342c/#2b2833/#211f2a -> #40405a/#34344a/#2a2a3c
  - chroma strip, tonale wave/slider: matched to the charcoal family
  - theremin pad + tonal-centre CRT: lifted (green-charcoal)
  Screens now read as dark instrument panels in a lit room, not black slabs punched in
  the page. Housing>bezel>inner depth order preserved.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.91.0

**Header buttons matched to FORK + light-mode splash background**

- **Header buttons (mic/QA/level) mismatched FORK + flat:** they used theme 24% while
  FORK used accent 10% — different intensities = visible mismatch, and FORK had no
  border/shadow so it read flat. Aligned BOTH to accent 16% tint + matching border
  (accent 34%) + subtle layered shadow. Header buttons and FORK now read as one family,
  neither flat.
- **Light-mode splash:** a pure-black splash before a light app is jarring. Added a
  medium-tint splash background (#3a3a52 gradient) when light mode is detected (via the
  existing html.light-root class from the pre-paint boot) + bumped splash-bg canvas
  opacity so the animation still reads. Chose MEDIUM not full-light because the splash
  waveform/particles are drawn bright for a dark bg and would wash out on a pale one;
  medium is clearly lighter than black + less jarring while keeping animation contrast.
  (On-device judgment: can go lighter if the animation still holds.)

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.9

**Light mode: header buttons strengthened + specifics audit round**

- **Header buttons (mic/QA/level) still stark:** the 12% theme tint was too weak and
  the bright white edge-light (0.4) was fighting it, reading glossy-white. Bumped tint
  12->24%, border 22->40%, softened edge-light 0.4->0.18. They now clearly carry the
  tab color instead of reading white.

Specifics audit (8 categories):
1. data-theme signal: 0. Clean.
2. Canvas light-checks: cof/db/pitchHist done; latDraw green (ok). Clean.
3. Active-state faint fills: all covered. Clean.
4. White text on light: 5, all on colored/dark bg. Clean.
5. **Bright text on light (FOUND):** chord-ear + interval trainer labels (ce-hud-diff-lbl,
   iv-diff-pill-lbl, iv-test-dot.hit, reveal notes) used #5ee2ff/#b8a3ff/#34d399 on light
   surfaces -> mapped to deep (#0b7048/#523aa0/#006f8f).
6. Dark backgrounds on light: all guarded/boot. Clean.
7. **White overlays (FOUND):** gs-step + settings notification rows (sm-notif-*) had
   rgba(255,255,255,.0x) resting backgrounds that vanish on light -> dark tint.
8. Sentinel: all 97 + 39 pins.

Net: header button tint strengthened, ce/iv bright labels + gs-step/notif overlays fixed.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.8

**Light mode: AUTO DETECT fixed + real app-wide faint-fill scan**

Dan called out I hadn't actually scanned app-wide — fair. Did it properly:

- **AUTO DETECT (.auto-banner):** the real element (built dynamically, class .auto-banner)
  used a 4-6% green/cyan gradient — invisible on light. Boosted to a 16%/10% theme-tinted
  gradient + stronger border, with a matching hover.
- **Systematic scan:** grepped all faint accent-fill backgrounds (5 accent RGBs at
  <=12% opacity) app-wide = 139 hits. Categorized: ~16 are hover/decorative (fine to
  stay subtle), ~21 are resting/active states that actually matter. Boosted the active
  states that read as "on/selected": tg-phase-pill, pr-mode-chip, cs-family-btn,
  groove-cat-tab, prog-sync/loop/groove/metro, ts-preset, vibrato-toggle, scale-ghost,
  kbd-oct, cs-picker-inst, cs-trumpet-strip-pill, pr-bpm-preset-chip, rs-chip,
  tg-popup-chip, trp-full-note, tempo-verdict, tg-resultbox. All to ~18% theme tint (or
  10% surface-tint for result boxes).

Left the hover/decorative faint fills alone — subtle-on-hover is correct; boosting them
would read busy. Active/selected/listening states now clearly fill across every module.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.7

**Light mode: dim accent-fill backgrounds boosted + APPEARANCE label centered**

- **Dim state backgrounds:** buttons like LISTENING (panel-badge), FORK, active
  tiles/chips used low-opacity accent fills (0.05-0.10) tuned for dark backgrounds. On
  the richer light base they barely registered as "filled/active". Boosted app-wide via
  light-mode overrides using color-mix on the tab --theme: panel-badge to 20%, active
  states (stb-tab/tile, tone-tile, metro-mode-chip, subdiv-btn, ts-opt, capo) to 18%,
  fork buttons to a 10% accent-tinted surface, drone-mode greens to 20%, detect CTA to
  a green-tinted surface. Active/listening/selected now clearly reads as filled.
- **APPEARANCE label centered** over the toggle (was left-aligned via align-items:
  flex-end on the wrap; now center + text-align center).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.6

**Pitch graph visibility fix + appearance toggle label/position**

- **HIDDEN BUG — pitch-stability trace invisible in light:** the actual pitch trace
  LINE (the data you watch) used bright #b6f25b/#ffd166/#ff8a65 by tune-distance — all
  ~1.1-2:1 on the light plot = invisible. Plus the in-tune zone band was bright green
  at 7%. Deepened both in light (#3a7000/#875d00/#c0331f trace, deeper green band). The
  gridlines/labels were already fixed in 0.89.2; this is the trace itself, which is the
  whole point of the graph. Good catch asking to verify since it needs mic to test.
- **Appearance toggle:** was colliding with the settings close X (both top-right) and
  ambiguous (icon-only). Added an "APPEARANCE" label above the toggle + padded the
  title row 34px on the right so it clears the X. Now labeled and unobstructed.

On the String Guide "different color": confirmed again it's the SAME .card token — it's
an optical illusion from context (top card sits under the dark tuner screen so its
surroundings read darker; String Guide is ringed by open light space so it reads
brighter). Same pixels, different neighbors. Not fixable without faking a tint.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.5

**Settings switcher relocated + header buttons themed + border pass**

- **Appearance switcher moved:** was a full-width row below the SETTINGS title; now a
  compact icon-only toggle (◐ ● ○) top-right of the title, in a flex row with the
  title block. Titles keep their tooltips (Auto/Dark/Light). Fits clean up top.
- **Header buttons (mic / quick-access / level) themed:** they read flat white and
  didn't shift per-tab. Now mix 12% of the tab --theme into their surface + 22% into
  the border, so they tint with each module (tuner blue, metro warm, etc.) and got the
  layered shadow + edge-light. No longer stark static white.
- **String Guide vs tuner card:** confirmed via inspection they are the SAME .card
  token — no color difference. The tuner card just contains the dark tuner screen,
  giving it visual weight; String Guide is all-light content so it reads lighter. Not a
  bug, and the deeper borders give String Guide its own definition. (Didn't fake a tint
  — they're genuinely the same surface.)
- Borders: the deeper --border/--border-soft from 0.90.4 push bordered elements solid
  app-wide. Left border:none elements alone (mostly intentional icon buttons); adding
  borders everywhere would read busy. "Push solid where needed" best judged on-device
  now that the tokens are stronger.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.4

**Light mode: deeper borders — the "blends too hard / flat" fix**

Dan nailed the root cause of the residual flat feeling: borders too soft, so buttons
and cards blend into the background. Measured it: --border-soft was 1.01:1 against the
base (LITERALLY invisible), --border only 1.33:1. That's why elements had no definition
and the folders (which have stronger elevation) stood out while everything else didn't.

Deepened both borders across all 5 palette blocks (base + 4 tabs):
- --border: ~1.33:1 -> ~1.8:1 (#a3a3c4 -> #8a8ab0 and per-tab equivalents)
- --border-soft: ~1.01:1 -> ~1.4:1 (#bcbcd6 -> #a3a3c4 etc)
Kept per-tab hues (tuner blue-grey, metro warm, tools teal, train lavender borders).
This defines every bordered element — buttons, chips, cards, inputs — without going
harsh, and directly attacks the flatness.

On String Guide vs the tuner card above it: they're structurally different — the tuner
"card" contains the dark chroma screen (visual weight), String Guide is a plain light
card. Not a bug, but the deeper borders give String Guide more definition so it floats
less. Metro time-sig chips (.ts-opt) already share the unified button treatment; deeper
borders make them read consistently now.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.3

**Light mode: exhaustive 8-point audit**

Ran every failure-category scan across the whole file:

1. Wrong theme signal (data-theme): 0 left. Clean.
2. Canvas light-awareness: cof/db/pitchHist done; latDraw draws green (legible),
   rest are in guarded screens. Clean.
3. White-overlay backgrounds on light surfaces: fixed the remaining light-following
   ones — octave-badge, groove-countin-btn, gs-pulse-toggle/chip, tuner-refpitch-pill.
   Survival Guide set already covered.
4. White text on light: all 6 verified on colored/dark backgrounds. Clean.
5. **color:var(--bg-0) on accent buttons (FOUND LEAKS):** 20 uses; only a few were
   covered. In light --bg-0 is light -> low-contrast text on accent-filled buttons.
   Expanded the white-text-in-light override to catch pr-go-btn, pr-ch-end-again,
   metro-sound-btn.active, mq wrong letter, iv-diff-pill.active, ce-diff-cell.hit,
   cs-picker-fam-tab.active, and the .active accent states.
6. Hardcoded dark backgrounds: all verified inside guarded screens (tc-CRT, tuner
   meter, rhodes piano). Clean.
7. Heavy dark shadows on light chrome: all in guarded screens (streak card, tuner,
   piano). Clean.
8. Shadow tokens: both palette blocks carry the layered premium shadow. Clean.

Net new fixes this pass: expanded accent-button white-text coverage (5) + remaining
white-overlay controls (5).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.2

**Light mode: comprehensive module sweep + color-legibility audit**

Two asks: (1) String Guide vs Utilities still mismatched, (2) every-module pass so all
colored elements (greens/yellows/reds) match and are visible on the new richer base.

**String Guide / Utilities matched:** they use different classes (.card vs
.practice-card-btn) and had picked up slightly different backgrounds + layered shadows.
Gave practice-card-btn the SAME gradient + layered shadow as .card so folder cards and
content cards read identical.

**Color legibility audit (measured on the deeper #bdc1db base):**
- The deepened semantic colors (in-tune, sharp, metro, flat, accent) are AA-large on
  the base and full AA on cards — fine, they're on large UI.
- Raw bright chordle/feedback hexes (#22c55e/#eab308/#ef4444) FAIL on the light base
  (1.1-2.7:1) — they're supposed to route through diffColorFor. Found 4 LEAKS that set
  them raw: daily win/loss titles, two result titles, the confirm-tap warning. All now
  routed through diffColorFor so they deepen in light.

**Module sweep — bright dark-mode colors on light-following surfaces:**
- Survival Guide (NOT guarded, follows light) used hardcoded #5ee2ff/#ffd166/#8b9cff
  text + rgba(255,255,255,.03) white-overlay backgrounds that vanish on light. Mapped
  all to deep equivalents + dark-tint backgrounds.
- Fixed remaining white-overlay backgrounds on light-following buttons (mq-np-btn,
  sg-cad-chip/vl-prog/vl-toggle).
- Confirmed no old-pale literal values leaked anywhere from the richer-base migration.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.1

**Light mode: sweep fix + premium polish (layered shadows)**

Sweep caught a real miss: the BASE body.light surfaces (--surface/-2/panel + bg-0/1)
still held the OLD pale values (#d1d1e0 etc) — my 0.90.0 richer-base edit had only
partially landed. So any non-tab context showed pale. Updated to the richer values
(#bdbddb base). Also fixed the COF hub literal + stale fallback literals. This is why
the String Guide card read lighter — plus its full-height gradient; tightened the card
gradient to a top-22% sheen so tall cards don't skew light.

Premium polish (researched — the techniques that separate "good" from "$10K"):
- **Layered shadows:** replaced the single flat card shadow with a STACKED set (4
  layers, increasing blur + decreasing opacity) for a smooth realistic falloff instead
  of one muddy drop. Applied to the --shadow-card token so it propagates app-wide, plus
  cards and folder cards directly.
- **Edge-light:** a 1px inset white highlight at the top of cards so they "catch light"
  from above (glassmorphism dual-border technique), consistent light source.
These are subtle by design — premium polish is felt, not announced.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.90.0

**Light mode: richer + atmosphere — "plain" -> dynamic**

Side-by-side, light felt plain vs dark's depth. Dan's read was right and he named the
fix: a COLORED lighter version, not near-white, with the atmosphere dark has. Three moves:

- **Richer, more saturated base:** pulled lightness down from ~85% to ~80% and bumped
  saturation ~28-30%. Base is now a clear periwinkle #bdbddb, per-tab hues genuinely
  colored (tuner blue-grey #bdc1db, metro warm sand #dbd4bd, tools teal #bddbd5, train
  lavender #c0bddb) — reads as tinted paper, not off-white wash.
- **Atmosphere restored:** the header glow (body::before) was dialed to 9%/5% when I
  over-flattened for cohesion — dark uses 32%/18%/12%. Brought light up to 22%/13%/9%
  (three-point), so light now has the light-pouring-in depth dark has, scaled for a
  pale page.
- **Card dimension:** restored a gentle top->bottom card gradient (surface-2 -> surface)
  so surfaces have depth, not flat slabs. This is the RESTRAINED version, not the muddy
  bloom from the early builds.
- Deepened --muted to hold AA on the richer base; accents sit at AA-large on bg-0
  (they're on large UI) and full AA on the lighter cards.

Rolled to 0.90.0 — this is the pass that gives light mode its own character instead of
reading as a washed-out dark mode.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.89.3

**Light mode: title weight (the "thin" fix, done surgically)**

Dan flagged light mode feeling thin — title especially, text/tabs a little. Diagnosis
before acting:
- It's partly perceptual: dark-on-light reads lighter than light-on-dark at the SAME
  weight (no glow to bulk it out). Real effect, Dan's eye is right.
- But the concrete cause for the TITLE: .logo is font-weight 300 (light) and leaned on
  a drop-shadow GLOW for presence — and a colored glow does nothing on a light page.
  So in light mode it's just thin 300-weight strokes with no glow. That's the thinness.
- Tabs are weight 500 (medium) with wide tracking — fine as-is; bolding them would go
  heavy-handed. Body text is fine. Did NOT touch either (avoiding the bold-everything
  cascade Dan worried about).

Fix: bumped ONLY the main .logo to weight 400 + removed the now-useless glow filter in
light mode. Scoped to the title. If it still reads thin on-device the next lever is
deepening the title gradient endpoints (current ~4.4:1 -> ~7:1, more substantial) —
held for now to keep this a single evaluate-then-escalate change, not a blanket bold.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.89.2

**Light mode: final sweep — one hidden stone found**

Did a systematic audit for remaining dark-only assumptions:
- data-theme wrong-signal checks: 0 left (all converted to body.light).
- Canvas visuals: audited all 12 canvas contexts. cofDraw, dbDraw, pitchHistDraw now
  light-aware; strobe/bpmWheel/thmnKnob are inside guarded dark screens (stay dark,
  correct).
- **HIDDEN STONE FOUND — pitch-stability graph:** pitchHistoryCanvas sits on a light
  --bg-1 in light mode but drew its gridlines/labels in rgba(255,255,255,...) = white
  on light = invisible. The tuner's pitch-history graph would render blank. Fixed with
  a light flag drawing dark ink (same pattern as dB meter). This one was genuinely
  hidden — only shows when you're actively holding a pitch.
- latCanvas (Settings > Calibration) draws in green, legible on light — left as-is
  (rarely-used, and touching the calibration draw risks more than it gains).

Known cosmetic (deferred): Tonale wave/scope touch the side edges — a grid-overflow
that resisted two blind fixes; needs an inspector reading to nail without guessing.

Light mode is otherwise comprehensive: palette, cards, buttons, difficulty/feedback
colors, all canvas visuals, and every dark screen (tuner, metro, theremin, CRT, Tonale).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.89.1

**Tonale: the real fix — side bleed, not vertical clipping**

Dan clarified: the preview is scrollable, so vertical height was never the issue — the
wave and slider were cut off on the SIDES, running past the content margin while the
header sat inset.

Root cause: #exTonale is a .stack (CSS grid). Grid items default to min-width:auto,
which lets them overflow their track when a child is intrinsically wide (the wave
canvas). So the wave-wrap pushed past the column edge and the width:100% canvas
filled the over-wide box. Fix: min-width:0 on the grid children + max-width:100% +
box-sizing:border-box on the tonale screens, so they shrink to the column and align
with the rest of the app.

Reverted the 0.89.0 height trims (wave 150px, slider min 300px restored) — those were
solving a non-issue; the width constraint is the actual fix.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.89.0

**Tonale: layout clip fix + screen contrast dialed in**

- **Layout clipping:** the wave (150px) + slider (min 300px) + gaps/margins exceeded
  the viewport on some screens, clipping the bottom DRAG TO MATCH text and edges.
  Conservative trim: wave 150->132px, slider min-height 300->250px, margins tightened.
  Fits without clipping, proportions preserved. (Not a light-mode issue; helped dark too.)
- **Screen contrast:** first attempt lifted the slider to a medium grey — but the pitch
  ladder + reference lines draw in var(--accent) at low opacity and would vanish on
  grey. Dialed back to the screen-charcoal family (#242230 slider, #1a1822 wave) so
  the lines stay readable AND it's consistent with tuner/CRT/metro. Lifted just enough
  off pure-black to soften the contrast jump from the lavender page without losing the
  glow the neon wave needs.

Lesson logged: canvas/overlay content colours constrain how far a dark screen can lift
— check what draws ON the surface before lightening it.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.9

**Tonale screens lightened (this WAS the Tonale screen)**

The "pitch-match" screen Dan flagged is actually Tonale — the DRAG TO MATCH / LOCK IN
pitch game. Its two dark screens were the last black slabs:
- tonaleWaveWrap (top wave display): was pure #000 -> #16141c charcoal in light.
- tonaleSlider (the big scope): was linear-gradient(#0e0e15,#0a0a0f) -> charcoal
  gradient (#211f2a,#1a1822) in light.
Both now match the tuner/CRT/metro screen-charcoal family, so Tonale reads cohesively
instead of as two black holes on the light page.

Layout check: the REPLAY/LOCK IN right-rail buttons use inline var(--surface) styles,
NOT any class in the button-unify list from 0.88.8 — so that change did not shift this
layout. What looked like a shift is Tonale's normal cramped right-rail; the buttons
were already light because they read the surface token. No regression.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.8

**Light mode: COF rings, button consistency, Tonale**

- **COF rings darker:** the wheel segment tints were pale on light. Boosted the
  sectorTint alpha 1.7x in light mode so the color rings read with proper depth.
- **BUTTON CONSISTENCY (Dan's catch):** equivalent controls across modules used
  DIFFERENT surface tokens — metro-mode-chip=surface-2, subdiv-btn=panel, etc. In
  dark those tokens are close; on light the gaps showed as "some lighter some darker".
  Pinned the common interactive buttons (subdiv, ts-opt, mode chips, sound btns,
  toggle chips, iv-mode, tg-seg) to one surface + border in light mode so modules
  match each other.
- **Tonale:** the reveal-key cells already use tokens (adapt fine) and the neon-wave
  screen is a legit dark instrument display (like pitch-match, stays dark). The one
  fix: its wave wrap was pure #000, harsher than the charcoal screen family — lifted
  to #16141c in light so it's consistent with tuner/CRT/metro.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.7

**Light mode: Circle of Fifths, volume meter re-fit, card presence**

- **Circle of Fifths** was heavily dark-mode: the center TAP hub drew as a black
  circle (canvas read --bg-1 via the @property fallback = dark initial) and every key
  label (wedge names + center) was hardcoded white, invisible on the light wheel.
  Added a light flag to cofDraw: hub fills light, all labels (wedge major/minor, TAP,
  sub-labels) draw dark ink in light mode.
- **Volume meter:** the charcoal plot from 0.88.6 clashed with the light green Tools
  tab (dark slab on light page). Reverted to a tint-following light surface — AND
  fixed the dB canvas gridlines/labels (hardcoded translucent-white) to draw dark in
  light mode, so a light plot actually shows its content. This is the right fix: the
  meter now matches the tab instead of fighting it.
- **Card presence:** nudged .card one step darker (surface-2 -> surface) so the metro
  settings panel and similar have a bit more weight against the tinted page.

Pattern noted: canvas-drawn tools (circle of fifths, dB meter, staffs) don't get CSS
overrides — each needs an in-draw light check. Circle + dB + staffs now all handled.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.6

**Light mode: cohesion pass — flat cards, visible staffs, real meter plot**

Dan's "they don't feel cohesive" was exactly right. Three root causes:

- **Card bloom/fade:** every .card uses a top->bottom gradient (surface->bg-1) PLUS a
  corner radial glow (.card-glow), both tuned for dark. On light they read as a muddy
  vertical bloom — some surfaces flat, these faded = incohesive. Flattened cards to a
  solid surface and killed the glow in light mode. This is the big cohesion fix.

- **HIDDEN BUG — music staffs invisible:** the staff renderers checked
  `data-theme==='light'` to pick black-vs-white ink, but light mode uses the .light
  CLASS, not that attribute — so they ALWAYS drew white, invisible on light cards
  (the transposer YOU READ / IT SOUNDS staves). Fixed the signal in 5 staff functions
  + gave pitchedStaffSvg (which had no check at all) a proper light branch. Staffs now
  draw dark ink on light.

- **Volume-meter graph washed out:** the dB plot used var(--bg-1) (light), but the
  canvas draws translucent-WHITE gridlines + faint zones designed for a dark plot. So
  it washed out. Restored a charcoal plot in light mode = the meter reads like an
  instrument display again.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.5

**Light mode: full polish sweep (systematic, not reactive)**

Did a proper audit pass instead of one-at-a-time. Found and fixed:
- **Chroma strip shadow:** still had the heavy 0 5px 14px rgba(0,0,0,.7) dark drop
  haloing onto the page. Softened to a clean lift, recessed inset kept.
- **Header buttons (mic / fav / level chip):** used var(--surface) = near-white, so
  they read as stark white circles on the header. Tinted to surface-2 with a defined
  border + soft shadow.
- **Big mic button:** same near-white gradient; retinted and softened.
- **HIDDEN BUG — accent-button text contrast:** buttons like the interval-trainer
  primary use color:var(--bg-0) as "contrast text" (dark text on bright accent). In
  light mode --bg-0 is light grey, giving ~4:1 light-on-mid-tone (below AA). Forced
  white text on accent-filled buttons = 5.7-6.6:1. This was invisible until audited.
- **Card definition:** stark near-white panels (metro settings) got a slightly
  stronger border so they read as distinct surfaces on the tinted page.
- Softened remaining heavy shadows on light chrome (fork/subtab/mode chips).

Audit noted 178 heavy-dark-shadow + 106 white-inset-bevel declarations total, but the
vast majority are INSIDE guarded screens (knobs, keys, pedals) and correctly stay
dark. Only the light-following chrome was swept.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.4

**Light mode: chroma strip, stark card definition, softer screen frame**

Three on-glass catches:
- Tuner CHROMA STRIP (the C/C#/D... note strip under the tuner LCD) was still
  near-black while the LCD above it went charcoal — inconsistent. Lifted its 3 layers
  to the same charcoal so the tuner reads as one unit.
- Cards read stark/flat on light (metro settings panel especially): near-white
  surface on a near-white page with a border too faint to define the edge. Added a
  slightly stronger card border in light mode so panels have definition.
- The guarded-screen FRAME was a near-opaque cream ring (rgba 250,248,243 @ .9) that
  read as a hard white border around the theremin/CRT/tuner. Softened to a single
  subtle 1px edge + soft drop.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.3

**Color-coding stragglers swept + screen scope locked**

- Chordle "locked slot" cell (the confirmed-correct note at the current guess
  position) escaped the feedback-color remap — still bright #22c55e. Routed through
  diffColorFor. This was the green "I" that stayed bright while its neighbour deepened.
- Interval-trainer + tempo-game feedback greens/golds (CSS hardcoded: .iv-test-dot,
  .iv-test-perfect, .iv-answer-btn.correct, tg-hud diff) deepened for light mode.

**Screen-lift scope decided (correctly, with Dan on glass):**
- Lifted screens (done): tuner LCD, metro display, theremin, tonal-centre CRT — the
  genuine near-black slabs. These read as dark panels in a lit room now.
- NOT lifted (intentional): the piano "bed" is deliberately evoking a real piano —
  the black is the instrument metaphor, not a neutral screen, so it stays black. The
  game scopes read fine dark too.

Remaining light-mode item: **Tónale** needs its own pass — it's layout + bespoke
colour, not the screen-lift recipe, so it's a separate focused session.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.2

**Game color-coding goes universal + screen charcoal rolled out**

Difficulty text was just the tip — the same bright hexes (#22c55e correct, #eab308
present, #ef4444 wrong, #3b82f6 root, #a855f7 inversion) do all the game COLOR-CODING
and washed out identically on light. Fixed comprehensively:
- diffColorFor() map extended to every feedback hex (+ #2ec78f, #facc15, #fbbf24,
  #c084fc, #60a5fa).
- Chordle/diadle guess-CELL colors (JS inline) now routed through the mapper — the
  correct/present/inversion/rootonly states deepen on light.
- Legend swatches (inline-styled dots) remapped via attribute-substring CSS.
- Re-applied on appearance toggle so switching mid-session updates everything.

**Screens charcoal-lift rolled out.** Tuner proof confirmed on-device (subtle but
correct), so lifted the values a notch brighter and rolled the same recipe to the
metro LCD (warm charcoal), theremin pad + console (green charcoal, radial highlight
kept), and tonal-centre CRT (green charcoal glass). Each keeps its hue character and
the housing>bezel>inner depth order so screens read as dark panels in a lit room, not
black slabs.

Still dark by design: piano keybed and the game scopes (next rollout candidates if
these read right).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.1

**Difficulty text: universal fix + tuner-screen charcoal proof**

- Difficulty labels were fixed for only ONE variant last build; there are several
  (chordle & diadle set colours from JS as inline styles; ce-hud and iv-chip set them
  in CSS). Now universal: a light-aware mapper (diffColorFor) deepens the JS inline
  colours when light mode is active, re-applied on appearance switch; and the CSS
  variants (.ce-hud-diff, .iv-diff-chip) get light-mode overrides. All difficulty
  pills — chordle, diadle, chord-ear, intervals, pitch-match — now legible on light.

- **Screen lightening — started, tuner as proof.** Lifted the tuner LCD's three
  near-black layers (housing #1a150a, bezel #08070c, inner #010408) to warm charcoal
  in light mode, keeping the housing>bezel>inner darkness order so the recessed depth
  survives. This is one screen as a test: if it reads right on-device, the same
  approach rolls out to metro, theremin, CRT, piano and the game scopes. If not, only
  one screen was touched, not all six.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.88.0

**Light mode: difficulty-label readability + a scope decision on the screens**

- Difficulty-pill labels (EASY/MEDIUM/HARD/ALL on pitch-match & interval trainers)
  used bright DARK-mode colours hardcoded — ~1.2:1 on the pale light pill, effectively
  invisible. Deepened to AA in light mode (easy #2e7d4f, medium #6248bf, hard #8a5f00,
  all #c0335f, custom #006f8f). This was the "difficulty text hard to read" report.

- **Decision on lightening the guarded screens:** inventoried the work — 31 distinct
  near-black backgrounds across the screens, each with its own character (theremin
  cool-black, metro warm-black, CRT green-black). Properly lifting each to charcoal
  is a genuine multi-session job, and done carelessly it damages the exact aesthetics
  the .keep-dark guards exist to protect. Holding: the screens stay dark for now. A
  dark instrument display framed in a light page is a legitimate pattern (dark video
  player on a light page); the actual bug was puffy FRAMES around them, now fixed.
  Per-screen charcoal remains available as deliberate future work if testers still
  want it, but it is not blocking and not worth rushing.

Tónale still flagged for its own polish pass (partly a screen, partly layout).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.9

**Light mode: metro/theremin halos + guard the expand views**

Structural fixes from screenshots (the remaining "awkward" items that are fixable
without the per-screen charcoal lift):
- Metro display and theremin console had heavy dark drop shadows + coloured glows
  (0 6px 20px rgba(0,0,0,.8) etc.) that haloed onto the light page. Softened the
  OUTER drop to a clean soft lift in light mode; the internal recessed bevels are
  kept so the screens still read as real displays.
- The piano and theremin EXPAND/fullscreen overlays (#pianoOverlay, #thereminOverlay)
  had no .keep-dark guard — light mode was trying to lighten these dark instrument
  views and breaking them. Guarded; they stay dark like their inline versions.

Known remaining (needs the deferred per-screen charcoal lift, bigger job): the piano
keys, theremin knobs and metro-screen internals still read a bit awkward because the
screens are pure-black slabs on a light page. Lightening the guarded screens from
black to charcoal will resolve most of these at once — that's the next real Phase 2
item, not more shadow-chasing.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.8

**Light mode: flatten the screen frames, re-elevate the folder cards**

Two opposite fixes from screenshots. (1) The tuner/metro MAIN cards still looked very
3D — those are the housing frames (.tuner-bpm-card / .metro-bpm-card) that hold the
dark screens, and they carry a heavy `0 20px 60px rgba(0,0,0,.55)` drop shadow plus
inset bevels tuned for dark. On light that reads as a puffy beige slab. Flattened to
a soft 2px lift. (2) The folder/group cards had been over-flattened last build into
plain blocks with no separation — restored a GENTLE soft shadow (no bevel) so they
lift off the tinted backdrop again.

Colour/tint from 0.87.7 confirmed good on-device (train lavender, tools green-grey,
tuner blue-grey all read correctly now).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.7

**Light mode: the diagnosis paid off — real tint + flatten the child 3D**

The 0.87.6 test marker (loud coral cards + red borders) confirmed the changes DO
reach the preview — some cards showed it, proving the rules apply. So the problem was
never the pipeline; it was that my "tinted" values were 94% lightness = effectively
white, and the 3D lived on CHILD elements I hadn't touched.

Fixes:
- Surfaces genuinely tinted now: bg-0 dropped from ~94% to ~85% lightness with 20%+
  saturation, so each tab's hue is actually VISIBLE (tuner blue-grey, metro sand,
  tools teal, train lavender) instead of reading white. Cards a touch lighter than
  the backdrop but still clearly tinted, not white islands.
- Child-element 3D flattened: instrument pills, toggle chips, tab buttons, folder
  cards etc. carried their own dark-tuned inset-bevel + drop shadows that read puffy
  on light. Neutralized to a single soft flat shadow app-wide in light mode. Guarded
  dark subtrees keep theirs.
- Test marker removed.

Guarded signature screens unchanged.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.5

**Light mode: cards carry the tint, and flatten the 3D**

Two on-device problems. (1) The per-tab backdrop tint WAS landing (train lavender,
metro cream, etc.) but the cards were near-white (#f5f5f7) and cover most of the
screen, so the whole thing still read white. (2) Cards looked puffy/embossed.

Fixes:
- Card surfaces (--surface / --surface-2 / --panel) pulled DOWN into each tab's tint:
  now a visibly lighter-tinted lavender/cream/teal that sits above the backdrop
  without going white. Cards read as "tinted paper", not "white islands on a tinted
  page". Applied to all four tabs + the base.
- Shadows flattened. The old card shadow had a bright inset bevel (rgba white .6
  inset) which reads as elegant depth on DARK but puffy/3D on light. Replaced with a
  single soft low drop shadow (research: light mode wants 1-2 soft levels, no bevel).
- The module/folder cards in the Tools hub share .practice-card-btn, so they now pick
  up the tinted gradient too instead of white.

Guarded signature screens unchanged (still dark, soft frame; charcoal lift = Phase 2).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.4

**Light mode: lightened version of the app palette, per tab**

Still read as generic white because the base was neutral stone, not a lighter version
of the app's actual colours — and it flattened every tab to one near-white despite
each tab having its OWN hue in dark mode (tuner navy-blue 232, metro amber 45, tools
teal 168, train violet 246).

Reworked: each tab's light base is now derived from ITS OWN dark hue — a lightened
version of that tab's colour, not neutral. Tuner is a soft blue-grey, metro a warm
sand, tools a teal-grey, train a violet-grey. Subtle but present, so each tab reads
as "itself, brighter" instead of "white app". Base surfaces keep hue 240 (the app's
navy family). All accents re-verified for WCAG AA/AA-large on the tinted bases.

The direct-paint block is now token-driven (with light literal fallbacks baked in) so
the per-tab tint actually carries through to the backdrop, cards and ambient glow,
instead of being overpainted with one flat literal.

Guarded signature screens still dark with the soft warm frame; per-screen charcoal
lift still Phase 2.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.3

**Light mode: warm elevated-neutrals instead of stark white**

On-device the previous pass was too stark — near-white chrome next to pitch-black
signature screens read as a jarring slab, exactly the aggressive-contrast trap the
research warns against. Reworked to the 2026 "elevated neutrals" direction (soft
warm stone/oatmeal, not #FFFFFF):

- Base is now a warm stone #e7e4dc with surfaces stepping up through #f4f2ec to a
  soft #faf8f3 — warm, grounded, far easier on the eyes, and it NARROWS the gap to
  the dark screens so they stop clashing.
- Accents deepened slightly to keep WCAG AA on the warmer base (cyan #006f8f, green
  #3a7000, etc. — all >=4.5:1 verified).
- Per-tab tints warmed to match; shadows warmed (brown-grey, not blue-black).
- Signature screens: a soft warm frame + light-side glow now eases the edge between
  the dark screen and the light page, so it reads "dark instrument in a lit room".

Deferred to Phase 2 (noted honestly): actually LIGHTENING the guarded screens from
near-black to charcoal. Each screen (tuner, CRT, metro, theremin) paints its OWN
hardcoded dark background, not the palette token — so it needs a per-screen override,
not a token swap. The half-done token lift was pulled rather than shipped inconsistent.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.2

**Light mode: fix the dark backgrounds in the in-app HTML preview**

Root cause found via the app's HTML preview (not a real browser): the palette tokens
(--bg-0, --surface, --theme, --accent...) are all @property-registered so the theme
crossfade can animate them. The preview engine only partially supports @property — a
registered custom property resolves to its dark INITIAL-VALUE instead of the cascaded
light value. So light mode changed the unregistered vars (--text, --muted) but the
registered ones stayed dark: dark backgrounds, light text. The CSS cascade was
correct (verified with a resolver); the engine just wasn't honouring the override on
registered properties.

Fix: in light mode, paint the page chrome from LITERAL light values rather than via
the registered tokens — html/body background, the ambient ::before glow (now a faint
tint wash), and the structural surfaces (cards, panels, practice buttons, hints).
Registered tokens still drive the animated crossfade where supported; these
guarantee a correct static paint everywhere. html gets a .light-root class (the
.light class is on body, but html paints --bg-0 as the parent and needs its own
hook). Also darkened the TRAIN card sub-text that was cyan-on-white.

.keep-dark signature surfaces are untouched — they re-declare their own dark values.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.1

**Light mode actually lights up now, and the toggle shrank**

On-device screenshots showed 0.87.0 only changed the TEXT — dark text on dark
backgrounds. Cause: the per-tab theme blocks (body.theme-tuner/-metro/-tools/-train)
come AFTER body.light in the stylesheet and re-declare the full dark surface set at
equal specificity, so on every themed tab (which is every tab) the dark backgrounds
won and only un-themed vars like --text went light.

Fix: compound body.light.theme-X blocks placed after the theme overrides — higher
specificity AND later in source — restore the light chrome on every tab. Personality
survives per the Linear approach: each tab keeps its hue as a DEEPENED accent
(tuner #007a9c, metro #8a5f00, tools #0b7a4e, train #6d4fc4 — all verified >=4.5:1
AA on the light base) plus a barely-there 2-3% tint of that hue in the backdrop.

The giant Appearance chips are gone. Replaced with a compact segmented control
(AUTO / DARK / LIGHT with tiny half/filled/empty circle icons) sitting in one subtle
line right under the Settings title. Same three-way behaviour, same live auto-follow.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.87.0

**LIGHT MODE — Phase 1 (foundation)**

Requested by several testers. Built to researched professional spec (Material/HIG
guidance, WCAG AA verified by contrast math, not eyeballed):

- **Light palette** under body.light: soft off-white base #eef0f4 (never pure white),
  surfaces stepping TOWARD white for elevation, dark-slate text #1a1c26 (never pure
  black, 15.96:1), every accent deepened to hold >=4.5:1 AA on the light base while
  keeping its hue (cyan #007a9c, green #3f7a00, gold #8a5f00, blue #2563cc, red
  #d92626, purple #6d4fc4). Shadows lightened for light surfaces.
- **Signature surfaces guarded.** A .keep-dark wrapper re-declares the dark palette
  for its subtree, so these keep their identity in both modes: tuner glass, tonal
  centre CRT, theremin pad, Road Trip (has its own five themes), and the premium
  Legendary/Mythic streak reward cards (gold-on-dark IS the reward). Regular
  achievements, Music Quiz and Survival Guide follow light mode — reading surfaces
  benefit from it.
- **Settings > Appearance: AUTO / DARK / LIGHT.** Auto follows the device via
  prefers-color-scheme and re-applies live when the system changes. Stored in
  localStorage. Default is Auto.
- **No flash-of-wrong-theme:** a tiny inline script right after <body> applies the
  class before first paint (the main script block sits 61% into a 7.7MB file; without
  this, light users would get a dark flash every boot). NOTE: script block count is
  now 7 (was 6) — update any tooling that assumes 6.

Phase 2 (next): on-device tuning from screenshots — the ~15 hardcoded dark chrome
colors, white-inset highlights, per-tab tint whisper (Linear-style 3-5% surface wash),
and whatever dark patches only real glass reveals. Per-tab personality is preserved:
vivid accents on the loud elements, barely-there tint on surfaces.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.86.2

**COMPARE: cross-degree moves now show an arrow**

Ab Egyptian vs minor pentatonic drew a dropped-note X on the b3 and a glowing pip on
the 2, but NO arrow — and the caption read the clunky "MINOR PENTATONIC ADDING 2
WITHOUT b3". The ear hears that as one note sliding (b3 down a semitone to 2), so the
missing arrow felt wrong.

Cause: move-detection only paired notes with the SAME degree NUMBER. b3 (degree 3)
becoming 2 (degree 2) crosses a degree boundary, so it read as an unrelated add +
drop.

Added a second pass: any leftover add and drop that sit ONE semitone apart (circular
distance, so an octave wrap still counts) are paired into a move — giving the arrow.
Egyptian now shows the arrow and the caption collapses to the clean "MINOR PENTATONIC
with ♮2".

Verified it does not create false moves: pure-subset scales (minor/major pentatonic
dropping notes from their parent, In dropping from phrygian) have no adds to pair, so
they still read as drops; blues' b5 has no adjacent drop, so it stays an add.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.86.1

**COMPARE overlay: fades in as one unit, no morph-matching**

Trying to time the arrows against the note morph kept reading as mistimed jank, in
every variant (defer, draw-on). Stopped matching the morph at all.

The whole ghost overlay — dashed markers, add-rings, drop-Xs and arrows — is one SVG
group, and it now simply fades in together as a unit over 0.28s on an animated change,
decoupled from the notes' movement. The arrows appear WITH their own markers because
they are the same layer; nothing tracks the moving notes. Toggling COMPARE with no
scale change still shows everything instantly.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.86.0

**COMPARE arrow: draws on instead of fading up**

The fade-in read slow: it held invisible for 0.27s, then ramped opacity over a
further 0.18s, so the arrow did not even begin to appear for over a quarter second
and had no sense of motion when it did.

Replaced the opacity fade with a stroke DRAW-ON: the arrow wipes from the parent note
toward the current note along its own path (stroke-dashoffset animation), after a
short 0.14s hold and over 0.32s with a snappy ease. Faster overall, and directional —
the arrow traces the path the note took, which reads as intentional rather than a
vague fade. Dash length is set to 100, comfortably longer than the widest ghost arc
(~85 units at a 3-semitone move) so the stroke is always fully hidden before it draws.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.9

**COMPARE overlay: markers stay, only arrows fade in**

The 0.85.8 approach (defer the whole overlay 440ms) fixed the wrong-position arrows
but replaced them with a dead pause and a hard pop-in. Worse.

Split the overlay by what it is anchored to. The dashed parent-note markers, the
add-rings, the drop-Xs and the pip-glow all sit at FIXED tick positions — they do not
depend on the moving notes, so they now appear immediately. Only the ARROWS connect a
parent position to the current note's FINAL spot, so only the arrows wait: on an
animated change they hold invisible through the morph and ease in as the notes land
(keyframe stays at opacity 0 for the first 60%, then fades to full).

Result: something is always on screen, nothing points at a stale position, and the
one element that genuinely needs the settled layout arrives softly instead of
popping. Toggling COMPARE with no scale change draws everything instantly as before.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.8

**COMPARE arrows wait for the scale to settle**

Rolling the dice (or changing scale) with COMPARE on drew the ghost arrows
immediately, while the notes were still mid-morph to their new positions — so the
arrows pointed at where the notes USED to be, then everything slid. Looked broken.

The ghost overlay is now deferred until just past the .42s FLIP morph on animated
changes, so the arrows are drawn against the notes' settled positions. The previous
scale's arrows and pip-glow are wiped immediately (they must not hover over the
morphing notes), and a per-render token cancels a stale pending draw if the scale is
changed again mid-morph. Toggling COMPARE itself is unaffected — no morph is running,
so it still draws instantly.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.7

**Anchor coloring: the octave was never actually an anchor**

The root lit cyan but the octave stayed plain blue — visible in every screenshot.
The anchor test was `d.deg === '8'`, but the octave note usually does NOT carry deg
'8': getScaleData already includes the octave, so scaleTapeData's '8'-labelling
append is skipped, and the degrees array has no entry at the octave's index — so it
fell through to deg '·'. The test never matched, so only the root (index 0) got the
anchor.

Fixed by testing the SEMITONE instead: the octave is simply the note at semi 12,
whatever its degree label. Also labelled that note's degree '8' properly (it was
showing '·' under the octave dot before). Every scale now has exactly two anchors,
root and octave.

Drone mode too: the bright-green highlight targeted .root, leaving the octave dim.
Now targets .anchor, so both ends light green in drone mode, matching normal mode.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.6

**Anchor coloring: fix the purple, brighten, enlarge**

The anchors came out purple, not cyan. Cause: the CSS used var(--accent), and under
the TRAIN tab body.theme-train remaps --accent to #b8a3ff (purple). The Scales tool
lives under TRAIN, so every "accent" element there is purple, anchors included.

Switched the anchor colour to an explicit bright cyan (#6ef0ff) so it is independent
of the tab theme and reads as a deliberate boundary colour against the blue notes.
Also enlarged the anchor dots (radius 6.7 vs 5.5) — sized via the radius attribute,
NOT a CSS transform, because the dot's transform is already used by the hit-pop and
drone-latched scale animations and a static scale would collide with them.

Both ends get it: the root (degree 1) and the octave (degree 8) are both anchors, so
the tape is framed at both ends.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.5

**Scales: anchor coloring**

Small, deliberate polish after previewing a much larger set of changes and rejecting
most of them. The root and its octave (degrees 1 and 8 — the frame of the scale) are
now cyan instead of the same blue as every other note, with the two octave-boundary
ticks faintly tinted to match. "Home" now reads at a glance on any scale, sparse or
full.

That is the whole change. The gradient rail, halos, pitch-brightness gradient and
per-note entrance animation from the previews were all cut: invisible, fussy, or
fighting the note-shifting morph that scale changes already have. The morph stays as
the only entrance motion.

Cascade verified: anchor cyan is the base dot colour, and every meaningful state
overrides it correctly by specificity or source order — hit (white), COMPARE moved
(gold), drone latched and drone root (green). No state conflicts.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.4

**Transport dot: the actual fix (synchronous teleport, no timing games)**

Three previous attempts all fought the TIMING of when to re-enable the transform
transition — single rAF, then double rAF. That was the wrong frame entirely, and
under rapid tapping the deferred re-enable raced the next tap and the dot flew back
and forth.

Dropped the timing approach completely. New helper scalePlaceDot(x, show):
  - adds a `.snap` class ( transition: none !important )
  - forces a reflow (flush the "transitions off" state)
  - sets the transform and visibility
  - forces a second reflow (commit the new position while still off)
  - removes `.snap`
Because the transform CHANGES while transitions are hard-off, the browser has
nothing to tween — the dot teleports. It is fully SYNCHRONOUS, so rapid up/down/stop
taps cannot race it; each press does a clean stop, teleport, and re-arm in one go.

.moving (the transform animation) is added only AFTER the dot is already sitting on
the start note, so the only thing it can ever animate is the step to the next note —
never the arrival at the first. Same helper used for play-start, loop-restart and
stop, so all three behave identically.

If it still flies after this, it is not the transform transition and the next step is
a remote-inspector capture — but this removes every timing race by construction.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.3

**Transport dot fly-home (real fix), and the Exotic group split up**

**The dot.** Two prior attempts missed the mechanism. The dot's transform is relative
to cx=0 (far left), and the .moving class carries `transition: transform`. If the
transform is set while .moving is present — or in the SAME frame it is added — the
browser animates from x=0 to the start note. That is the fly-home, and a single
requestAnimationFrame was not enough to separate the two.

Now every placement (initial play AND loop restart) strips .moving, kills the
transition, sets the transform, forces a commit with getBoundingClientRect, then
waits TWO frames before re-enabling. .moving is added only once the dot is already
sitting on the start note, so the first thing it can ever animate is the step to the
second note — never the arrival at the first. If it still flies after this it is not
the transition and needs a remote-inspector look, but the mechanism is now airtight.

**Scale groups.** The Exotic bucket had swollen to 13 scales — over a third of the
library in one bin, mixing jazz modes, folk scales and symmetric scales. Split into
three coherent families:
  JAZZ · MELODIC MODES  — Lydian Dominant, Altered, Locrian nat2
  WORLD & EXOTIC        — Double Harmonic, Phrygian Dominant, Hungarian Minor/Major, Hirajoshi
  SYMMETRIC             — Diminished W-H, Diminished H-W, Augmented, Whole Tone, Chromatic
Six groups now, none larger than six. Applied to both scale pickers and the Tonal
Centre picker. All 28 scales verified present exactly once, EN + IT labels.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.2

**AKA line: stop repeating the title**

Two scales carry their mode name in the title itself — "MAJOR · IONIAN" and
"NATURAL MINOR · AEOLIAN". Their AKA entries were Ionian and Aeolian, so the strip
read "AKA IONIAN" right under a title that already said IONIAN. Redundant.

Dropped both entries (the mode name earns its place in the title; the AKA line is
for names the title does NOT show — Byzantine, half-diminished, acoustic scale).
Added a guard in scaleMaybeNote so any AKA that already appears in the title is
filtered out, in case a mode suffix is added to another title later.

Now major and natural minor show nothing under the title, while double harmonic still
shows "AKA Byzantine · Arabic · surf scale" and the rest are unchanged.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.1

**Scales: alternative names ("AKA")**

Many scales carry two or three names depending on who is teaching — jazz, classical,
klezmer, surf. The caption strip under the scale name now shows them when it is not
busy with something more important, prefixed AKA (DETTA ANCHE in Italian):
  DOUBLE HARMONIC   -> AKA Byzantine · Arabic · surf scale
  LOCRIAN nat2      -> AKA half-diminished
  LYDIAN DOMINANT   -> AKA acoustic scale · Lydian b7
  PHRYGIAN DOMINANT -> AKA Spanish Phrygian · Freygish
  ALTERED           -> AKA super Locrian · diminished whole-tone
...16 scales in all. Only well-attested names — no guitar-forum folklore. (The surf
connection is real: Misirlou is double harmonic major.)

The caption strip now has a clear precedence, since it can only show one thing:
COMPARE sentence (when on) > melodic-minor practice note > AKA names. So turning on
COMPARE replaces the AKA line with the comparison, and turning it off restores it.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.85.0

**Full audit: tours, help panels, hints and i18n across the app**

After a session of heavy restructuring (improv tab removed, Scales rebuilt, scale
library grown 20 -> 28), the guidance layer had drifted from reality. Audited all of
it mechanically: every tour selector against the markup and JS-created classes, every
help panel against current behaviour, every data-i18n key against both language
tables.

**Broken tour steps (selector no longer exists):**
- Interval trainer: two steps previewed `.iv-target-card`, a class renamed to
  `#ivTargetZone` at some point. Repointed.
- Tempo Lock: the "Your Score" step targeted `#tlResult`, which does not exist in the
  rebuilt layout. Repointed at the real HUD (`#tlHudBest` / `#tlBarRow`).

**Stale text describing the removed Improv tab (7 places):**
- HELP_CONTENT.scales rewritten for the TAPE tool (was describing the old text strip
  and its green glow)
- HELP_CONTENT.scaledrone rewritten as "Drone Mode" (was a full panel for the deleted
  Improv tab, START button and all; key kept for existing lookups)
- TRAIN hub hint, Scales card subtitle, tool subtitle DOM default: all still said
  "improvise" — now describe hear / drone / compare (EN + IT + markup defaults)
- A tour step still offered "Listen, Sing, or Improv mode"; another listed "Scales
  Improv" as a mic user (the Scales tool no longer uses the mic at all). Both fixed,
  both languages.
- Dead i18n keys scale_tab_reference / scale_tab_improv removed (the sub-tab nav they
  labelled was deleted in 0.83.0).

**i18n integrity: all 690 data-i18n keys verified to resolve in EN and IT.** One real
gap found and filled: `tl_target` ("target tempo") was used in Tempo Lock markup but
never defined in either language, so Italian users saw English. Added both.

**Also:** duplicate `class` attribute removed from the progression practice card
(browsers ignore the second, but it was sloppy); the vr_safety_hint audit flag was
confirmed a false positive (defined in both languages; the audit regex trips on an
escaped quote).

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.84.5

**Full musical audit of the scale system**

**Correctness: all 28 scales verified against independent authoritative pitch-class
sets** (not the file's own data — a hand-written truth table). Zero errors.

**Three COMPARE pairs improved after a musical review of every pair:**
- PHRYGIAN DOMINANT now references PHRYGIAN ("phrygian with a major 3rd" — one move,
  the Spanish-scale lesson as actually taught) instead of harmonic minor (mode-theory
  correct but three moves)
- DOUBLE HARMONIC was wrongly marked "no parent" — it is HARMONIC MAJOR with a b2,
  one move
- HUNGARIAN MAJOR likewise — it is LYDIAN DOMINANT with a #2, one move

Every scale that has a tonal parent now has one; only the five genuinely symmetric
scales (chromatic, whole tone, augmented, both diminished) show NO PARENT.

**Melodic minor's descending form is now acknowledged.** The tool plays the ascending
(jazz) form both directions — silently swapping to natural minor on the way down
would confuse anyone who doesn't know the convention and annoy anyone who does. So
it is stated instead: the caption strip under the scale name reads "CLASSICAL
PRACTICE DESCENDS AS NATURAL MINOR" whenever melodic minor is selected and COMPARE
isn't using the strip. Information, not behaviour. EN + IT.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.84.4

**Scale coverage: the instrument overlay had none of the new scales**

The new scales from 0.84.2 went into the Scales tool and Tonal Centre but NOT into
GSS_SCALE_TYPES — the scale overlay for the instrument fretboard/keyboard views. So a
guitarist picking scales saw 18 while the Scales tool showed 28. Now consistent: all
8 new scales added to the instrument overlay (ids match SCALE_DEFS, intervals derive
automatically via scaleDefIntervals), slotted into GSS_SCALE_GROUPS with two new
groups (Melodic/Dominant, Symmetric).

Also caught a pre-existing gap: HARMONIC MAJOR was in SCALE_DEFS but never in the
instrument overlay. Added. Now the only scale missing from the overlay is chromatic,
omitted on purpose — an all-twelve-note "scale" is not a useful fingering shape.

Every bank now carries the same library bar that one deliberate exclusion.

**Transpose:** confirmed it already exists where it belongs — the dedicated Transposer
tool handles concert/written pitch for transposing instruments, and the Tuner has its
own B♭/E♭ transpose. Not duplicated into the Scales tool or the instrument charts,
where a third instance would risk inconsistency for little gain.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.84.3

**COMPARE: pentatonics and blues get their reference back, rooted in theory**

I had made the wrong call in 0.84.2: pentatonics were given NO parent because the
diff could only compare equal-length scales. That let the algorithm's limitation
decide a teaching question, which is backwards. Minor pentatonic against natural
minor, and blues against minor pentatonic, are among the most useful comparisons in
the tool.

So the diff was rewritten to work in PITCH CLASSES and classify each difference as a
move, an ADD, or a DROP:
  MINOR PENTATONIC -> NATURAL MINOR without 2 and b6   (the subset, shown by what it omits)
  MAJOR PENTATONIC -> MAJOR without 4 and 7            (drops the half-step tendency tones)
  BLUES            -> MINOR PENTATONIC adding b5        (the blue note, one added chromatic)
  HIRAJOSHI        -> NATURAL MINOR without 4 and b7
  IN               -> PHRYGIAN without b3 and b7
  EGYPTIAN         -> MINOR PENTATONIC with the 2 for the b3

On the tape: a moved note still draws its arc arrow; an ADDED note draws a bright ring
with a "+"; a DROPPED note draws a faded hollow marker with an x where the parent's
note would sit, so you see exactly what the scale leaves out.

Parents are now chosen from the theory, not from what the diff finds convenient. Every
scale with a real parent gets one; only the genuinely symmetric scales (chromatic,
whole tone, augmented, both diminished, double harmonic, hungarian major) show NO
PARENT.

Captions verified for all pairs in EN and IT.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.84.2

**Scales: playhead fly-home killed, 8 scales added, ghost pairs audited, BPM range raised**

**Playhead no longer flies home.** scaleStop() was setting `transform = ''`, which is
translateX(0) — the far LEFT — so the next play() animated the dot from there to the
root. Now stop() kills the dot (transition off, drop .show/.moving) but LEAVES the
transform where it is; play() repositions it WHILE INVISIBLE and reveals it a frame
later via requestAnimationFrame. The .moving state no longer animates opacity, so the
dot can't fade mid-jump on a loop wrap. It appears where it belongs and never travels
to get there.

**Library 20 -> 28.** Added the melodic-minor modes that matter (Lydian Dominant,
Altered, Locrian ♮2), both octatonic diminished scales (W-H and H-W), Augmented, and
two world pentatonics (In, Egyptian). All eight verified for pitch classes and
spelling by the scale audit. Wired into SCALE_DEFS, TC_SCALE_GROUPS, both picker group
arrays, SCALE_SHORT_NAMES, and EN+IT scale_opts.

**Ghost pairs audited and fixed.** The COMPARE parent map had real bugs the audit
caught: pentatonics were being compared to 7-note parents (note-count mismatch, not a
moved degree), and egyptian vs minor pentatonic were IDENTICAL pitch classes (egyptian
is a rotation of it). Pentatonics now get NO parent — there is no clean heptatonic
scale to compare a 5-note scale against, and the dice covers exploring them. New
heptatonic scales got tight parents: lydian dominant -> lydian (1 move), altered ->
locrian (1), locrian ♮2 -> locrian (1). Full re-audit: zero bad pairs (no note-count
mismatches, no identical pairs). The three remaining 3-move pairs (major<->natural
minor, phrygian dominant->harmonic minor) are correct — those scales genuinely differ
by three notes, and the caption states it accurately.

**BPM range raised.** Slider was 40-200, default 100. Now 60-260, default 120: the
floor at 40 was tediously slow for scale practice and running scales fast is a real
mode. The gradient-fill calc, which hardcoded (v-40)/(200-40), now reads the slider's
own min/max so it can't go stale on a future range change.

Sentinel: all 97 tracked fixes present + 39 pins hold.
## v0.84.1

**Tone bank: stopped fighting the shared component, gave it its own classes**

Four attempts at aligning this produced four different wrong layouts, which is the
tell that the approach was wrong rather than the values.

The shared `.tone-tile` is a `<button>` carrying a base rule (display:flex, its own
padding, min-height, background gradient) plus SIX more rules keyed on
`data-count` / `data-cols` / `:nth-child(4n+1)` / `:last-child`, all written for the
OTHER tone banks in the app. Every override from `#exScales` was landing in a
different fight: one attempt collided with the orphan `grid-column: 1 / -1` rule and
stacked the tiles, one produced uneven widths, one centred a ragged row into a
floating island. I could not reason about the cascade from here, and could not
measure it either (Chromium is not installable in this container).

So: the Scales tone bank now has its OWN class namespace (`stb-tabs`, `stb-tab`,
`stb-grid`, `stb-tile`, `stb-ico`, `stb-name`). Nothing inherited, nothing to
override, nothing to collide with.

`.stb-grid` is a plain 4-column grid with `grid-auto-rows: 54px` and a reserved
`min-height: 114px` (two rows), so every tile is exactly one column wide and one row
tall, a short final row simply ends flush-left, and switching families never resizes
the card. No spacer tiles, no data attributes, no nth-child arithmetic.

Less clever than reusing the shared component. It works.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.84.0

**GHOST rethought as COMPARE; tone bank rebuilt properly**

Both of these had been patched three times without being reconsidered. Backed up.

**TONE BANK — spacer-padded grid.**
Centring a ragged last row is WORSE than left-aligning it: a floating 2-tile row with
dead space either side reads as a bug. And the flex/grid hybrid kept fighting the
shared stylesheet.

Now a plain 4-column grid, with the final row padded out by invisible spacer tiles
from the JS. Every row is always full. No orphan rules, no explicit grid-column
placement, nothing to collide with.

Also: icons are now uniformly desaturated including the active one. Letting only the
selected tile's emoji go full-colour (grand piano's bright keyboard against seven
grey neighbours) read as a broken tile rather than a selected one. Selection is
carried by border, background and label colour.

**GHOST -> COMPARE. The concept was wrong, not the rendering.**

Three versions of the overlay all failed the same way: they asked you to mentally
subtract one scale from another. That is a puzzle, and this is a tool people open
BECAUSE they do not know the answer yet.

The teaching frame is the fix. Nearly every scale in the picker is its parent scale
with one or two degrees moved:
  DORIAN         = NATURAL MINOR with a natural 6
  HARMONIC MINOR = NATURAL MINOR with a natural 7
  LYDIAN         = MAJOR with a sharp 4
  MIXOLYDIAN     = MAJOR with a flat 7
That sentence IS the lesson. So the tool now says it, and shows it:

- the button reads `VS NATURAL MINOR` (explicit about what it is comparing against)
- a caption under the scale name states the difference in words:
  "NATURAL MINOR WITH natural-6"
- on the tape, only the degrees that MOVED are drawn, and they are drawn as MOTION:
  a dashed marker where the parent puts the note, an arc arrow, and the current pip
  glowing gold at the end of it. Dorian against natural minor is ONE arrow, Ab -> A.

Nothing to decode. Parent scales are assigned by rule (b3 -> natural minor, else
major) with overrides where a different parent is the honest one: phrygian dominant
and hungarian minor reference HARMONIC minor (phrygdom is its 5th mode), blues
references minor pentatonic. Symmetric/exotic scales with no meaningful parent
(chromatic, whole tone, hirajoshi, double harmonic, hungarian major) return none and
the button reads NO PARENT.

Caption height is RESERVED, not animated -- growing it 0 -> 16px would push the tape
and everything below it down, which is the card-jank this layout was built to avoid.

EN + IT twins for the new strings; the caption generator is language-aware
("MINORE NATURALE con natural-6").

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.83.3

**Tone bank overlap, and the GHOST overlay rethought**

**Tone tiles were overlapping.** I had set explicit `grid-column` on the trailing
tiles to centre a ragged last row. Two problems: explicit `grid-column` without an
explicit `grid-row` lets the browser auto-place the row, and it collided with the
shared stylesheet's own orphan rule (`grid-column: 1 / -1` on a lone last child).
The tiles stacked.

Dropped the grid gymnastics entirely. `#exScales .tone-tile-row` is now
`flex-wrap` + `justify-content: center` with a `calc(25% - 5px)` basis, so every
row — full or ragged — centres itself with no positional maths. The JS column
calculation went with it.

**GHOST now shows the whole reference scale, not just the deltas.**

v0.83.2 rang only the notes that differ. Denser, but a puzzle: three rings on
empty ticks mean nothing to someone who has not been told the rule, and this is a
tool a beginner opens to find out what a scale IS.

Now the overlay draws the entire reference scale, with two weights:
- notes both scales SHARE get a faint ring (opacity .22) — you can see the
  reference passes through here too, so the overlay reads as "the other scale,
  laid over this one"
- notes ONLY the reference has get a bright ring, a solid dot and their note name
  above the tape — because those ARE the difference

C major with the NATURAL MINOR ghost: faint rings on C D F G, bright named rings on
Eb Ab Bb. It reads as "minor lowers these three" without a legend.
C harmonic minor with the same ghost: exactly one bright ring, on Bb — the note
harmonic minor raises. The whole distinction between the two scales, in one mark.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.83.2

**Scales tool: CSS and layout fixes from the second device build**

**NOW PLAYING off-centre (again).** v0.83.1 made the hero side columns FIXED but
UNEQUAL (104px / 40px). Fixed is not the same as symmetric: unequal columns keep the
centre column from *moving*, but put its midpoint off the card's midpoint. Now
equal (88px / 88px); the dice is `justify-self: end` inside its column and the ghost
`justify-self: start` inside its own, so neither can disturb the centre.

**GHOST button was permanently wide.** It now sizes to its content — a small pill
when off, growing only as far as its 88px column allows when a reference name
appears.

**Tone picker was a black hole.** The shared `.tone-tile` / `.tone-group-tab`
components carry a near-black gradient (#1c1c20 -> #111114) tuned for the card they
normally live in; inside the purple Scales card it read as a black rectangle.
Re-skinned to the panel/border tokens, scoped to `#exScales` so no other tone bank
is affected.

**SLOW / FAST / tempo value rendered at default body size.** `.speed-label` and
`.tempo-val` do not exist in the app — they were mockup class names I carried over.
Defined them, scoped to `.scale-speed-row`.

**Tone bank rows were ragged.** 6 KEYBOARD tones in 4 columns gives 4+2 with the
orphan row jammed left. Column count now prefers an even divisor (6 -> 3 columns,
two full rows of 3), and where none exists (5, 7) the final row is centred by CSS
rather than left-aligned.

**GHOST now rings only the DIFFERING notes.** It was drawing a ring on every note of
the reference scale, including the ones both scales share, which buried the signal.
The point of the overlay is "what makes this scale different", so it now rings only
what the reference has that the current scale does not. C harmonic minor against
natural minor is now exactly ONE ring — the b7 that harmonic minor raises. That is
the whole difference between the two scales, in one mark.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.83.1

**Scales tool: tone tabs unstyled, ghost button overflowing** (on-device fixes)

Two bugs visible on the first device build of TAPE.

**Tone group tabs rendered as bare grey blocks.** The JS gave them
`class="tgt"` — a class I invented. The app's real class is `.tone-group-tab`
(defined at line ~7320, with the gradient fill, active state and hover already
written). They were matching no rule at all. Same failure mode as the
`scalePlay`/`playScale` name mismatch caught during the port: inventing a name
instead of reading the existing one.

Also: the tile row now sets `data-count` / `data-cols`, which the existing
`.tone-tile-row` CSS keys off for orphan-row centring and for its reserved
2-row height (so switching families never resizes the card). Those attributes
were missing, so those rules never fired either.

**GHOST button spilled out of its column.** The hero-top side columns were both
76px, but the left one holds a scale NAME and the right holds only a dice icon.
"NATURAL MINOR" ran straight out of the box. Fixed three ways:
- side columns are now asymmetric (`--hero-l: 104px`, `--hero-r: 40px`); still
  FIXED, so the centred prompt cannot be pushed off-centre
- the label ellipsises rather than clipping
- the button uses the abbreviated scale name ("NATURAL", not "NATURAL MINOR")

`SHORT` was a local const inside `buildScaleTypePicker`, so the ghost could not
reach it. Hoisted to module scope as `SCALE_SHORT_NAMES` — one source, shared by
the type chips and the ghost button, so adding a scale updates both.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.83.0

**Scales tool rebuilt: TAPE**

The Scales tool was the last module still on its original design: a text strip of
note names, three transport buttons, and an IMPROV sub-tab. Rebuilt as an
instrument-agnostic scale browser.

**The view.** The scale is drawn on a chromatic ruler: twelve semitone ticks, scale
degrees as pips. The EMPTY ticks are the intervals, so the shape of the gaps IS the
scale formula; no second diagram needed. Gap sizes are printed underneath, and any
gap >= 3 semitones renders in gold (harmonic minor's augmented 2nd flags itself).
Degree labels (1, 2, b3, 4, 5, b6, 7) come from `SCALE_DEFS.degrees` -- the payoff
of the v0.82.2 unification, since a bare interval list cannot tell you a b3 is a
FLAT THIRD rather than "3 semitones".

Positions derive straight from `getScaleData()` semitones, so pentatonics thin out,
chromatic fills every tick and whole-tone spaces evenly, with no special-casing.
Switching scales morphs (FLIP): the pips slide to their new positions rather than
redrawing, so harmonic minor -> melodic minor visibly raises the b6.

**New capability: DRONE mode.** Holds the tonic; tap any degree to hear it against
the root. Exclusive latch (a second tap replaces the first, never stacks). The tool
visibly shifts register in drone mode -- green rail, dimmed ticks and gap numbers,
tempo disabled. Transport (UP/DOWN/LOOP) exits it.

This is NOT a Tonal Centre duplicate: TC listens to YOU (mic + detection + interval
readout). This plays intervals AT you. Nothing else in the app did that.

**Drone honours a real engine constraint.** REF_TONES entries now carry a `sustain`
flag (4 of 46: sine, organ, pad, flute). A synth voice called with dur=0 leaves its
oscillators running and can hold indefinitely. A SAMPLE-backed voice is a recording
of a note decaying -- there is nothing to hold. So in drone mode the sampled voices
dim to 20% and go inert, whole tab groups with no sustaining voice dim out, and
selecting drone from e.g. grand piano hops you to sine and hands the piano back on
exit. The constraint is legible instead of mysterious.

**Tone bank upgraded.** The Scales tool was using `buildExerciseToneBank` -- a flat,
ungrouped row -- while the Reference tool used the good tabbed `TONE_GROUPS_DEF`
picker (KEYBOARD / WAVES / PLUCKED / BRASS / WOODWIND, ~26 instruments incl.
grand piano, harpsichord, trombone, harmonica). Third instance of the
"two parallel implementations, Scales reads the worse one" pattern. Now uses the
tabbed picker. Audio routes through `practicePlayNote()` / `practiceMasterGain`, so
it inherits the +5 dB low shelf @300 Hz, the limiter, makeup gain, sample playback
and `addLowFreqHarmonics()`.

**Also added:** octave stepper (OCT 2-6), dice (random root+scale, with a tumbling
roll animation), GHOST overlay (compares against natural minor if the scale has a
b3, else major; overrides for blues->minpent, major<->natminor, chromatic->none).

**IMPROV sub-tab removed.** It was a drone plus a scale strip -- Tonal Centre with
the detection removed -- and everything it did, TC does better. Sub-tab nav removed;
`scalesTab()` kept as a no-op shim since external callers reference it.

**The dangerous part, and how it was handled.** The drone AUDIO ENGINE is shared:
`tcDroneStart()` (Tonal Centre) calls `droneStart()`, and Diadle uses it too. But
`droneStart`/`droneStop`/`updateDroneDisplay`/`setDroneVolume` wrote to the improv
tab's DOM **unguarded** -- `document.getElementById('droneToggleBtn').innerHTML = ...`.
Deleting the markup would have thrown a TypeError and killed Tonal Centre's drone.
Added a `_dq(id, fn)` null-safe helper and routed every drone DOM write through it.
`updateDroneDisplay()` still computes `droneFreq` unconditionally -- TC and the
detection notch consume it.

**Bugs caught by the port's own smoke tests (would have shipped broken):**
- markup called `scalePlay()`, function was named `playScale()` -> three dead
  transport buttons. Alias added.
- `setScaleVolume()` wrote to `scaleVolPercent`, an element removed with the old
  layout, unguarded -> would throw. Guarded.
- the module tour had a step anchored to `#sst-improv` describing the removed
  sub-tab -> replaced with steps for DRONE and the dice.
- `scaleSustain()` called a `getPracticeMaster()` that does not exist (invented);
  rewritten against the real `practiceMasterGain` pattern.
- `scaleTapeData()` assumed `getScaleData()` returned a `degree` field; it does not
  (returns `{midi, name, semitones}`). Degree labels now built from SCALE_DEFS.

**Layout stability** (the tonal-centre lesson, applied): hero-top is a fixed 3-column
grid, not flex -- the GHOST button's label changes width when it toggles and would
otherwise shove the centred prompt off-centre. The title box is pinned to two lines
(75px) so the card does not resize when "C# PHRYGIAN DOMINANT" wraps.

Verification: 6/6 script blocks pass `node --check`; sentinel all 97 fixes + 39 pins;
scale audit all scales correct (pcs + spelling); every onclick handler, DOM id and
i18n key in the new markup resolves; EN + IT twins for all 11 new strings.

NOT yet verified on-device. Check: the tape renders for pentatonic/chromatic/whole
tone; drone latching; the tone tabs; and that Tonal Centre's drone still works
(that is the shared-engine risk).

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.82.2

**Scale system unified: SCALE_DEFS is now the single source of truth**

The app had two hand-maintained scale tables that had drifted: `SCALE_DEFS`
(degrees format; Scales tool + Tonal Centre; 16 scales) and `GSS_SCALE_TYPES`
(semitone intervals; all instrument scale views; 18 scales). Different ids for the
same scales (`aeolian`/`natminor`, `harmmin`/`harmminor`, `melmin`/`melminor`) and
four scales (phrygdom, hungmin, hungmaj, hirajoshi) existed only on the GSS side --
the Scales tool literally could not see Phrygian Dominant even though the app knew it.

Changes:
- `SCALE_DEFS` extended with `phrygdom`, `hungmin`, `hungmaj`, `hirajoshi` (degrees
  format, derived from the GSS intervals, verified by construction and by test)
- New `scaleDefIntervals(key)` derives semitone intervals from degrees;
  `SCALE_DEGREE_SEMIS` is the degree->semitone map
- `GSS_SCALE_TYPES` is now **generated** from SCALE_DEFS via `scaleDefIntervals()`.
  It keeps its own ids and short display names (instrument UIs and saved state
  reference them); `GSS_SCALE_ALIAS` bridges the id mismatches. Intervals are never
  hand-written there again -- a scale added to SCALE_DEFS is automatically
  consistent everywhere.
- All four scale pickers extended with the new scales: EN `scale_opts`, IT
  `scale_opts`, the Scales tool chip picker (`SHORT` map + groups), the TC dropdown
  groups, and `TC_SCALE_GROUPS`

Verification:
- Baseline captured BEFORE any edit (`scale_baseline.json`): all 18 GSS scales'
  ids, names, nameIt, intervals
- Derived table proven equal to baseline **18/18, byte-identical** (node harness
  running the real extracted code)
- Functional smoke through the real `getScaleData`: E phrygdom = E F G# A B C D
  (correct Hijaz spelling -- G# not Ab, because degrees carry alteration), C hungmin,
  C hungmaj, A hirajoshi all correct; existing scales unchanged
- Cross-check of the 14 previously-overlapping scales: degrees-derived intervals
  matched GSS hand-written intervals exactly even before the change (zero drift in
  content, only in coverage/ids)

NOT a shipped build yet by agreement -- scale tool display redesign still to come
in this same effort. Instrument scale views should be eyeballed on-device (any
instrument, any scale, especially the four new ones and natural minor) since the
sentinel cannot see rendering.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.82.1

**iOS: long-press magnifier loupe suppressed app-wide**

Tap-and-hold on iOS was popping the text-selection magnifier over interactive elements.

Root cause: the global selection-deny rule enumerated element types --
`html, body, button, .practice-card-btn, [onclick]` -- which covers the 820 inline
`onclick` attributes but **misses every element bound via `addEventListener`**. There are
~147 of those (82 `click`, 19 `touchstart`, 46 `pointerdown`), and the `pointerdown` /
`touchstart` ones are exactly the drag-and-hold surfaces where a long press is expected,
so they were the worst offenders.

Fix: inverted the rule. Blanket `*` deny, opt back IN for `input, textarea, select,
[contenteditable], .selectable`. Selection is now opt-in rather than opt-out, so new
interactive elements can't silently regress this.

Note for future reference: the loupe and the callout are **two different iOS behaviours**.
`-webkit-touch-callout: none` kills the Copy/Look-Up context menu; the magnifier glass is
part of text *selection* and is only suppressed by `user-select: none` on the element
actually being pressed. The old rule had `-webkit-touch-callout` in only 2 places against
68 `user-select` declarations. Both properties are needed, together, on everything.

Verified safe: all three clipboard paths (`_tpCopyFallback`, `chordleDailyExecCopy`,
`tonaleExecCopy`) use `navigator.clipboard.writeText()` with a temp-`<textarea>` +
`execCommand('copy')` fallback. None depend on user-initiated text selection, and
`textarea` is re-enabled by the opt-in rule, so the fallback still works.

Sentinel: all 97 tracked fixes present + 39 pins hold.

## v0.82.0

**Clair de Lune: opening thirds restored (real bug fix)**

The transcription was keeping only the **top note of every parallel third**. Beat 1 was
`m:77` (F5 alone) where the score has `[77,80]` (F5+Ab5). Same for the left hand and for
most of the piece. That is why it sounded hollow and unrecognisable; the opening of Clair
de Lune *is* parallel thirds, and half the notes were missing.

Notes re-derived from a LilyPond-engraved score MIDI (score-exact, no rubato, hands
pre-split as `upper`/`lower`). The new beat grid matches the old one exactly, so the
rhythm was already right; only the voicing was broken.

- `clair_de_lune`: rh 118 events, lh 81 events, runs to beat 93 (B-major arrival)
- Hand-authored pedal `ctls` (22 changes, 0-85.5) kept verbatim; they were correct
- Final chord duration extended to `d:3` so it rings out instead of clipping

**`clair_de_lune_famous` removed**

It only ever existed as a workaround for the broken opening. With the thirds restored the
opening *is* the main theme, so a separate "skip to the good bit" entry is redundant.
Removed its `PIECE_META` entry and its riff entry. No other references existed.

**Not done / open**

- The full movement runs to **beat 319.5** (~6:56 at bpm 46). Only beats 0-93 ship.
  The remainder is withheld because **its pedalling has not been authored**. Three
  algorithmic derivations were tried against the 22 known-good hand-authored pedal points
  and all failed: min-gap bass-change (degenerates to a metronomic 1.5-beat pulse),
  pitch-class-change (500 points, fires on arpeggio figuration), and plain bass-change
  (520 points). The harmony is defined by the full vertical, not the LH bass line, and the
  arpeggiation deliberately obscures it. **Back-half pedal must be hand-authored.**
  Parsed full-length note data is reproducible from the source MIDI.
- `RT_JOURNEY.clair_de_lune` hooks (`b:1,18,36,48,81`) are **untouched and still valid** --
  same beat grid, all within the 93-beat range. But they were only ever spread across the
  truncated piece. If/when the full movement ships, re-tune the five legs with the Leg
  Tuner (cf. gnossienne reaching b:301, arabesque_1 b:386).
- `RT_SONGS` entry for `clair_de_lune` is `hook:4` ("past the hushed open into the
  phrase"). That rationale is now questionable -- the hushed open is the good part.
  Revisit in the same tuning pass.

Sentinel: all 97 tracked fixes present + 39 pins hold.

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
