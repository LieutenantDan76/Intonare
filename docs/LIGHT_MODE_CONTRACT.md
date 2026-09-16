# Light mode contract (v1)

Locked before more hex tweaks. Dark mode is out of scope.

Prototypes (edit these first; do not touch `Intonare.html` until a family locks):
- Hub: `tools/prototypes/light-mode/index.html`
- Shared tokens: `tools/prototypes/light-mode/contract.css`
- Tuner chrome: `tools/prototypes/light-mode/tuner.html`
- Metro / drums: `tools/prototypes/light-mode/metro.html`
- Music Quiz: `tools/prototypes/light-mode/quiz.html`
- Road Trip: `tools/prototypes/light-mode/roadtrip.html`
- Four-tab A/B ref: `tools/prototypes/light-mode-mockup.html`

Labs may simplify layout for judging materials. Shipping work is color,
depth, shading, and material only; live layouts stay.


## Goal

Readable, deep, interesting, polished. Not office-white. Not mid-pastel rooms.
Personality from accent + wash + keep-dark stages. Page stays the calm stage.


## Roles (only these)

| Role | Job | Not for |
|------|-----|---------|
| `--ground` | Page / chrome behind cards | Text, fills |
| `--surface` | Cards, sheets, lists | Page wash |
| `--panel` | Highest lift (modals, key panels) | Body text color |
| `--ink` | Primary text / icons | Fills |
| `--ink-muted` | Secondary labels | Primary CTAs |
| `--outline` | Borders, tracks, hairlines | Text |
| `--accent-ink` | Links, icons, small accent text | Large fills |
| `--accent-fill` | Selected chips, soft state washes | Body text |
| `--accent-large` | Big numerals, hero marks (large text only) | 7–12px labels |
| `--on-accent` | Text on solid accent buttons | Everything else |

Alias old tokens to these. Do not add new accent roles without retiring one.


## Budgets (OKLCH)

Pinned across all four tab hues. Hue changes; L and C stay in band.

| Role | Lightness (L) | Chroma (C) |
|------|---------------|------------|
| ground | 0.88 – 0.92 | 0.025 – 0.040 |
| surface | 0.96 – 0.98 | 0.008 – 0.018 |
| panel | 0.985 – 0.995 | 0.004 – 0.010 |
| ink | 0.22 – 0.30 | ≤ 0.030 |
| ink-muted | 0.40 – 0.48 | ≤ 0.030 |
| outline | 0.55 – 0.65 | 0.015 – 0.035 |
| accent-ink | 0.38 – 0.46 | 0.10 – 0.14 |
| accent-fill | 0.82 – 0.90 | 0.04 – 0.08 |
| accent-large | 0.42 – 0.50 | 0.12 – 0.16 |

Tab hues (approx): tuner 250, metro 90, tools 170, train 290.

Live floors stay per-tab (#8faedc / #bdab75 / #79bca8 / #ada4d8).
Cards and accents share one L/C weight so Metro does not read lighter
or darker than Tuner.


## Contrast floors

- Body / UI text on surface or panel: ≥ 4.5:1
- Tab bar labels, small chrome: ≥ 4.5:1 on ground
- Large numerals (≥18px / bold): ≥ 3:1
- Borders that define controls: ≥ 3:1 against adjacent surface
- Never use dark-mode accent hexes at low alpha as the light fix


## Elevation

1. Ground quieter and slightly dimmer than cards.
2. Cards lift with tinted contact + soft far shadow (hue of ground, not gray dirt).
3. Optional primary tonal wash on elevated surfaces (Material-style), low alpha.
4. One ambient light field (top wash). No multi-pool blooms.
5. Few elevation levels. Same stack everywhere.


## Keep-dark

Tuner glass, CRT, theremin, and streak reward stages stay dark islands.
They re-declare the dark palette locally. Light chrome frames them.

## Road Trip (own theme system)

Road Trip is out of the Solid/Glass light pass. It already has skins
(parch, blueprint, night, nautical, ink). Do not frost or retoken it
with the app light contract.

Defaults tied to app appearance:
- Dark (or auto→dark): Night
- Light (or auto→light): Nautical

If the user is on Night or Nautical, flipping appearance swaps that pair.
Parch, Ink, and Blueprint stay put.


## Glass material (optional iOS polish)

Backed by Apple HIG Materials / Liquid Glass (2025), WCAG 1.4.3, and
Material elevation practice. Prototypes toggle Solid vs Glass.

**Where glass belongs (live hierarchy)**
- Full Regular frost on chrome: tab bar, launcher faces, settings /
  fav / tour sheets. Specular rim + sheen so frost still reads when
  blur is weak.
- Content cards: denser soft panel (higher fill) with the same rim /
  lift. Not Clear glass; not every surface at chrome opacity.
- Keep-dark instrument islands stay opaque (not frosted).
- Nested controls need their own planes: recessed rails / trays under
  chips and step grids so empty cells do not melt into card white
  (Metro lab is the reference for this hierarchy).
- Light modal scrims stay tinted (not 70% black) so sheet glass can
  still pick up stage hue.
- Morph flight locks a solid pastel face; translucent frost over a
  fading chooser sampled dark and looked like a black flash.

**Recipe (Regular, not Clear)**
1. Solid readable fill first (fallback for Android / no blur).
2. Then backdrop blur ~14–22px + saturate ~1.55–1.85.
3. Chrome fill ~36–42% white; content cards denser (~48–68%).
4. 1px light edge + specular streak + tinted soft lift.
5. One glass layer only. No glass-on-glass.
6. `prefers-reduced-transparency`: frostier fill, keep rim/sheen;
   never collapse to flat paper; never make contrast depend on blur.
7. Glass needs stage structure (hue pools). Flat single color makes
   frost look broken.

**Clear glass:** not used in Intonare light chrome. Apple reserves Clear
for rich media with dimming; our chrome has labels.

Sources: Apple HIG Materials; Adopting Liquid Glass; WWDC25 Liquid Glass;
WCAG 1.4.3 contrast against worst-case backdrop.


**Card lift (so frost doesn't melt into the stage)**
- Main cards use denser fill than chrome (~white 55–72% mix, later
  raised toward ~85–90% for readability on tinted stages)
- Single bright rim; avoid double outlines (reads as plastic 3D)
- Specular streak stays subtle

**Elevation by size (important)**
Small controls need sharper lift to read as raised. Large surfaces
amplify shadow, so they need *softer* lift or a stack of mode cards
looks louder than the Tuner.
- `--lift-xs`: chips, pills, badges
- `--lift-sm`: chrome bars, toggles, compact buttons
- `--lift-md`: medium content cards (Tuner panels)
- `--lift-lg`: large rows / sheets (Quiz mode cards); softer than md

Depth cue priority: white fill contrast first, rim second, shadow last.


## Do / don't

**Do**
- Generate ramps in OKLCH; lock pairs with WCAG.
- Put vivid color in accent-fill containers and keep-dark stages.
- Put glass on chrome only; keep content opaque enough for AA.
- Audit by screen family with on-device shots (iOS and Android).

**Don't**
- Paint the whole page at mid L / mid C.
- Frost every card (that is not Apple’s model).
- Deepen one accent until it is near-black, then invent vivid siblings forever.
- Match dark mode's mean saturation.
- Ship another global chroma pass without checking this contract.


## Success check

Same four screens, light vs dark, on device:
1. You can read every label without squinting.
2. Cards sit on the page (depth).
3. Tab personality is obvious within one second.
4. Nothing feels like a stain, a washout, or office gray.
