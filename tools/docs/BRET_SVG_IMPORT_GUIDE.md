# Bret Pimentel FDB SVG Import Guide
## For Intonare — Claude working reference

---

## Scope

Woodwind instruments only. Other families have their own renderers unrelated to FDB:

| Family | Instruments | Renderer | FDB? |
|---|---|---|---|
| `woodwind` | flute, clarinet, sax, oboe, bassoon, recorder, whistle, ocarina | `woodwindHoleDraw` → per-instrument SVG fn | ✅ YES |
| `brass` | trumpet, flugelhorn, french horn, euphonium, tuba | CSS div circles (3 valves) | ❌ |
| `brass` | trombone | `tromboneSlideDraw` (positions 1–7) | ❌ |
| `harmonica` | harmonica, chromatic harp | `harmonicaDraw` (reed grid) | ❌ |
| `freereed` | didgeridoo | no diagram | ❌ |
| `fretted` | guitar, bass, uke, mandolin, banjo, lute, bouzouki | fretboard SVG | ❌ |
| `chromperc` | piano, organ, melodica, harp, mallet | keyboard/bar SVG | ❌ |
| `bowed` | violin, viola, cello, double bass | neck SVG | ❌ |

---

## Complete sub-type export plan

**CORE PRINCIPLE: every diagram must match the real instrument exactly.**
A player looking at the diagram for their specific instrument should never see a
key that isn't on their instrument, or be missing one that is. "Why is there an
extra button here?" is the failure we are avoiding.

**Two independent axes** — never conflate them:
- **Diagram (SVG)**: does this sub get its own visual, or reuse another's?
- **Fingering data**: which `*_FINGERINGS` table does it read? (Verified against
  `wwGetFingering` — this part IS confirmed from the code.)

### The "shares diagram" column is a HYPOTHESIS, not a verified fact

The fingering-table column below is verified against the app code. The SVG-sharing
column is **my best guess from instrument knowledge** and MUST be confirmed by
diffing actual FDB exports before sharing. Sharing a diagram that's even slightly
wrong defeats the whole point.

**Mandatory verification step per family:** export the reference SVG AND a separate
SVG for each "candidate to share" sub from the FDB. Diff them (visually or by
comparing path data). If byte-identical in keywork → safe to share. If ANY key
differs → give that sub its own SVG. Never assume.

| App key | Sub | SVG sharing (CONFIRM by diff) | Fingering table (verified from code) |
|---|---|---|---|
| `ww_flute` | flute | reference | `FLUTE_MIDI_FINGERINGS` |
| `ww_flute` | piccolo | **own** — no foot joint, will differ | `FLUTE_MIDI_FINGERINGS`, slots 14–17 = 0 |
| `ww_flute` | alto flute | candidate to share flute — CONFIRM | `FLUTE_MIDI_FINGERINGS`, +5 transpose |
| `ww_clarinet` | bb | reference | `CLARINET_MIDI_FINGERINGS` |
| `ww_clarinet` | a | candidate to share bb — CONFIRM | `CLARINET_MIDI_FINGERINGS` |
| `ww_clarinet` | eb | candidate to share bb — CONFIRM ⚠️ | `CLARINET_MIDI_FINGERINGS` |
| `ww_clarinet` | bass | **own** — extra low keys | `BASS_CLARINET_FINGERINGS` |
| `ww_bassclarinet` | bb | shares clarinet-bass | `BASS_CLARINET_FINGERINGS` |
| `ww_sax` | alto | reference | `SAX_FINGERINGS_WRITTEN` |
| `ww_sax` | tenor | candidate to share alto — CONFIRM | `SAX_FINGERINGS_WRITTEN` |
| `ww_sax` | soprano | candidate to share alto — CONFIRM ⚠️ | `SAX_FINGERINGS_WRITTEN` |
| `ww_sax` | bari | candidate to share alto — CONFIRM ⚠️ low A | `SAX_FINGERINGS_WRITTEN` |
| `ww_oboe` | oboe | reference | `OBOE_FINGERINGS` |
| `ww_oboe` | coranglais | **own** — different bell/keys | `COR_ANGLAIS_FINGERINGS` |
| `ww_coranglais` | f | shares oboe-coranglais | `COR_ANGLAIS_FINGERINGS` |
| `ww_recorder` | soprano | reference | `RECORDER_FINGERINGS` |
| `ww_recorder` | alto | candidate to share soprano — CONFIRM ⚠️ | `RECORDER_FINGERINGS` |
| `ww_recorder` | tenor | candidate to share soprano — CONFIRM ⚠️ | `RECORDER_FINGERINGS` |
| `ww_recorder` | bass | candidate to share soprano — CONFIRM ⚠️ bell key | `RECORDER_FINGERINGS` |
| `ww_whistle` | d | reference | `WHISTLE_FINGERINGS` |
| `ww_whistle` | low_d | candidate to share d — CONFIRM | `WHISTLE_FINGERINGS` |
| `ww_bassoon` | bassoon | own ✅ | `BASSOON_FINGERINGS` |
| `ww_bassoon` | contra | own ✅ | `BASSOON_FINGERINGS` |
| `ww_ocarina` | 12hole | **own** | `OCARINA_12_FINGERINGS` |
| `ww_ocarina` | 7hole | **own** | `OCARINA_7_FINGERINGS` |

### Known real-world differences to watch for (export-time checklist)

These are the specific spots where "candidate to share" is most likely to FAIL
the diff. Check each one against the FDB explicitly:

- **Bari sax** — most baritone saxes have a **low A key** that alto/tenor/soprano
  lack. If FDB's bari preset includes it, bari needs its own SVG. Note: the app's
  `SAX_FINGERINGS_WRITTEN` table likely doesn't reference low A, so if you give
  bari its own diagram with a low A key, the key will render but never activate
  unless the fingering data is extended too.
- **Soprano sax** — usually identical keywork to alto, but some sopranos have a
  slightly different front-F / high-F# arrangement. Diff to be sure.
- **Eb clarinet** — sopranino Eb clarinets sometimes omit certain low keys or have
  a reduced key set vs full Boehm Bb. Confirm the FDB Eb preset matches Bb keywork.
- **Recorder alto/tenor/bass** — the big one. Soprano recorders are a clean 8-hole
  baroque layout. **Bass (and sometimes tenor) recorders add a low key and a bocal**
  that sopranos don't have. These very likely need their own SVGs. Also note the
  app models all recorder sizes on one fingering table (a known simplification —
  alto is really an F instrument), but the DIAGRAM must still match the physical
  instrument the player holds.
- **Alto flute** — generally the same Boehm keywork as concert flute, but confirm
  the foot joint matches (some alto flutes have a B foot, some a C foot).
- **Tenor sax** — typically identical keywork to alto; low confidence it differs,
  but diff anyway since it costs nothing.

### Decision rule

For each candidate-to-share sub:
1. Export the reference SVG (all keys shown, crop to all keys, SVG format)
2. Export the candidate sub's SVG the same way
3. Diff the keywork (compare path data, or overlay visually)
4. **Identical → share** (delete duplicate, use reference in renderer)
5. **Any difference → own SVG** (the player must see THEIR instrument)

When in doubt, give it its own SVG. The cost of an extra export is trivial;
the cost of a wrong diagram is a player losing trust in the app.

## Half-hole usage per instrument

The `keyPath` function needs a half-hole (0.5) branch only for instruments that
actually use it. Check the fingering data — `0.5` in a `p:[]` array = half-hole.

| Instrument | Uses half-holes? | Which slot(s) |
|---|---|---|
| `ww_whistle` | ✅ Yes | All 6 main holes — chromatic notes |
| `ww_recorder` | ✅ Yes | Slot 0 (thumb) — second octave venting |
| `ww_oboe` | ✅ Yes | Slot 2 (dedicated half-hole key) |
| `ww_coranglais` | ✅ Yes | Slot 2 (same as oboe) |
| `ww_bassoon` | ❌ No | All values are 0 or 1 only |
| `ww_flute` | ❌ No | No half-holes |
| `ww_clarinet` | ❌ No | No half-holes |
| `ww_bassclarinet` | ❌ No | No half-holes |
| `ww_sax` | ❌ No | No half-holes |
| `ww_recorder` (mini) | ✅ Yes | Thumb only |
| `ww_ocarina` | ❌ No | No half-holes |

For instruments without half-holes, `keyPath` is simply:
```js
function keyPath(d, slot) {
  const closed = (data[slot] || 0) === 1;
  g.appendChild(path(d, closed ? ACCENT : 'none', closed ? ACCENT : GREY, sw));
}
```

For instruments with half-holes, add the clip-rect branch:
```js
function keyPath(d, slot) {
  const v = data[slot] || 0;
  const closed = v === 1, half = v === 0.5;
  if (half) {
    const uid = 'hh_' + slot;
    const nums = d.match(/[-+]?\d*\.?\d+/g).map(Number);
    const xs = nums.filter((_, i) => i % 2 === 0);
    const cx = (Math.min(...xs) + Math.max(...xs)) / 2;
    const defs = el('defs', {});
    const cp = el('clipPath', { id: uid });
    cp.appendChild(el('rect', { x: String(cx - 50), y: '-10', width: '50', height: '600' }));
    defs.appendChild(cp);
    g.appendChild(defs);
    g.appendChild(path(d, 'none', GREY, sw));
    g.appendChild(el('path', { d, fill: ACCENT, stroke: 'none',
      'clip-path': 'url(#' + uid + ')', 'fill-rule': 'evenodd' }));
  } else {
    g.appendChild(path(d, closed ? ACCENT : 'none', closed ? ACCENT : GREY, sw));
  }
}
```

---

## Slot counts per instrument

The dispatch guard in `woodwindHoleDraw` checks `data.length >= N`. Use the
correct N for each instrument — wrong value = silent render of garbage data.
Find the exact count by reading the instrument's `LAYOUT` constant and counting
all slots across all arrays (lhMain + lhPinky + rhMain + rhPinky + extras).

| Instrument | Slot count | Guard |
|---|---|---|
| `ww_bassoon` | 17 | `data.length >= 17` |
| `ww_flute` | 18 | `data.length >= 18` |
| `ww_clarinet` | 14 | `data.length >= 14` |
| `ww_sax` | 13 | `data.length >= 13` |
| `ww_oboe` | 18 | `data.length >= 18` |
| `ww_recorder` | 8 | `data.length >= 8` |
| `ww_whistle` | 6 | `data.length >= 6` |
| `ww_ocarina` | 12 or 7 | check active sub |

**Always verify against the LAYOUT constant before coding the guard** —
these counts could change if fingering data is ever expanded.

---

## Renderer function signature convention

All bassoon-era renderers use ad-hoc booleans (`isContra`, etc.).
Going forward, use a consistent signature:

```js
function _instrumentSvgDraw(containerEl, data, mini, subKey)
```

Where `subKey` is the string from `wwActiveSub()?.key` (e.g. `'bass'`, `'piccolo'`).
Check inside the renderer:

```js
const isBass    = subKey === 'bass';
const isPiccolo = subKey === 'piccolo';
```

This is easier to grep, easier to extend, and consistent across all renderers.
**Bassoon already uses a boolean `isContra` — that's fine, don't refactor it.
Start using `subKey` string for all new renderers.**

---

## What to do with old hand-coded renderers

When a new FDB-based renderer is complete and tested:

1. **Delete** the old function entirely — don't comment it out, don't keep as fallback.
   Dead code in an 80k-line file is a liability.
2. The dispatch in `woodwindHoleDraw` already points to the new function, so the
   old one is unreachable anyway once the dispatch is updated.
3. Run the sentinel after deletion to confirm nothing breaks.

The only exception: if the old renderer handled something the FDB SVG doesn't
(e.g. a very specific trill key visual), note it explicitly before deleting.

---

## Mini mode requirements

Mini diagrams appear in scale/chord grid cards — roughly 80px tall cells.
In mini mode the renderer must:
- Show key shapes and body only — no section labels, no key labels
- Scale down cleanly (use `mini ? 110 : 300` for maxH, `mini ? '32px' : '200px'` for maxWidth)
- Keep stroke weight legible: `const sw = mini ? '3' : '2'` (slightly heavier in mini)
- Not overflow the cell — test by looking at the chord/scale grid view

No other logic changes for mini — same paths, same colours, just smaller.

---

## Export workflow (FDB → SVG)

1. Go to https://fingering.bretpimentel.com
2. Select instrument + key set (e.g. "Standard Boehm" for Bb clarinet)
3. **"Show keys → All"** — critical. Keys set to "Never" are absent from SVG.
4. Set fingering to fully open (no keys pressed)
5. **Format: SVG** (donors-only)
6. **Crop: "All keys"** — consistent bounding box. Never use "Visible keys".
7. Download. Name descriptively: `BbClarinet_Boehm.svg`, `AltoSax.svg`

---

## Renderer architecture

### Transform group
```js
const g = el('g', { transform: 'matrix(.75 0 0 .75 3.718 2.395)' });
svg.appendChild(g);
// All path d= coords are in original (pre-transform) space — never modify them
```

### ViewBox
`'0 0 255.778 371.889'` — verbatim from Bret's SVG. Never modify.

### Colors (never change across instruments)
```
ACCENT = '#2ec78f'   // closed key fill + stroke
GREY   = '#8a99a6'   // open key stroke, body stroke, section labels
```

### Sizing
```js
const maxH = mini ? 110 : 300;
const w = Math.round(maxH * VBW / VBH);
svg.style.maxWidth = mini ? '32px' : '200px';
```

**Flute exception**: transverse instrument needs sideways layout. Reuse the
`ww-sideways` CSS class approach from the existing `_fluteSvgDraw` — same
logic, just swap in Bret's paths.

### Section labels
Placed on `<svg>` directly (NOT inside transform group):
```
LT  x=4,   y=22,  anchor=start   top-left:    left thumb / whisper
RT  x=252, y=22,  anchor=end     top-right:   right thumb / rollers
LH  x=4,   y=200, anchor=start   bottom-left: left hand fingers
RH  x=252, y=200, anchor=end     bottom-right: right hand fingers
```
Adjust y=200 if the LH/RH split falls higher or lower visually.
Font: `JetBrains Mono, monospace`, size 10, weight 700, fill GREY.
**No key labels inside key shapes — ever.** Quadrant labels only.

---

## The mapping step

### Analysis script
```python
import re

def split_subpaths(d):
    parts = re.split(r'(?=M\s*[-\d])', d.strip())
    return [p.strip() for p in parts if p.strip()]

def bbox(sub):
    nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+',
            re.sub(r'[MLCQZASmzlcqaz]', ' ', sub))]
    if not nums: return None
    xs, ys = nums[0::2], nums[1::2]
    cx, cy = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
    return cx*0.75+3.718, cy*0.75+2.395, (max(xs)-min(xs))*0.75, (max(ys)-min(ys))*0.75

svg = open('YourInstrument.svg').read()
paths = re.findall(r'<path\s[^>]*d="([^"]*)"[^>]*/>', svg)[1:]  # skip white bg

for pi, path_d in enumerate(paths):
    subs = split_subpaths(path_d)
    print(f"\nPath [{pi}] — {len(subs)} subpath(s):")
    for si, sub in enumerate(subs):
        b = bbox(sub)
        if b:
            sx, sy, sw, sh = b
            print(f"  sub[{si}]: screen cx={sx:.0f} cy={sy:.0f} size={sw:.0f}x{sh:.0f}")
```

### Cross-reference with LAYOUT constant
```bash
grep -n "CLARINET_LAYOUT\|FLUTE_LAYOUT\|SAX_LAYOUT" Intonare.html
```
Slot 0 is always the leftmost/topmost key (thumb/register/whisper).

### Shape classification
| Shape | Classification |
|---|---|
| Width or height ≈ 0 | Body (bore line or connector) |
| Near-circle 15–45px, right column | RH main hole |
| Near-circle 15–45px, left column | LH main hole |
| Tall narrow crescent, top-left | LH thumb key (C, D…) |
| Asymmetric blob, top-left | Whisper/register key |
| Small oval, left-mid | Named key (F, G#…) |
| Overlapping rounded rects, bottom | Boot/pinky keys |
| Small curves, bottom-left | LH boot keys (Db, Eb) |
| Half-moon pair at same x, slightly different y | RT rollers → **body** |
| Large rounded shape, very bottom | Bell → **body** |
| Decorative S-curve or swirl | Ornamental → **body** |

Draw body paths first, keyPaths on top, top to bottom order.

---

## Wiring into the app (4 locations for sub-variants)

### 1. Dispatch in `woodwindHoleDraw`
```js
if (chordScaleInstrument === 'ww_clarinet' && data.length >= 14) {
  const subKey = (wwActiveSub && wwActiveSub()?.key) || 'bb';
  _clarinetSvgDraw(containerEl, data, mini, subKey);
  return;
}
```

### 2. Default wwSubType on instrument switch
Near `if (inst === 'ww_whistle') wwSubType = 'd'`:
```js
if (inst === 'ww_clarinet') wwSubType = 'bb';
```

### 3–4. Sub-variants need all four locations — miss any one and tabs break

| Location | Purpose | Search anchor |
|---|---|---|
| `WW_SUBS` | Sub object definitions (key/label/transposition) | `const WW_SUBS` |
| `CS_INSTRUMENTS` | `subs:` array for picker UI | instrument key e.g. `ww_clarinet:` |
| `switchSubType` | Sets wwSubType on tab tap | `if (inst === 'ww_whistle')` |
| `_buildSubRow` currentSub chain | Highlights active tab | long inline ternary |

---

## Per-instrument checklist

- [ ] Identify subs needing own SVG vs candidate-to-share (see table above)
- [ ] Export the reference SVG: Show all keys + Crop all keys + SVG format
- [ ] **For each candidate-to-share sub: export ITS SVG too and DIFF the keywork**
- [ ] **Identical keywork → share. Any difference → own SVG. When unsure → own SVG**
- [ ] Cross-check known-difference list (bari low A, recorder bass key, Eb clarinet, etc.)
- [ ] Run Python analysis script on each SVG
- [ ] Look up instrument's LAYOUT constant — confirm slot count
- [ ] Classify every subpath: bodyPath or keyPath(slot)
- [ ] Determine if instrument uses half-holes (see table) — include/omit branch
- [ ] Write `_instrumentSvgDraw(containerEl, data, mini, subKey)` following bassoon
- [ ] Delete the old hand-coded renderer function
- [ ] Wire into `woodwindHoleDraw` dispatch with correct slot count guard
- [ ] Set wwSubType default in instrument switch block
- [ ] If sub-variants: update WW_SUBS + CS_INSTRUMENTS + switchSubType + _buildSubRow
- [ ] Test note that closes keys in all regions (thumb, LH, RH, boot)
- [ ] Test half-hole notes if applicable
- [ ] Check mini mode doesn't overflow grid cells
- [ ] `python3 intonare_regression_sentinel.py Intonare.html` → exit 0
- [ ] JS validation on all 6 script blocks → no errors
- [ ] Bump version (Y within chat, X on new chat)

---

## Priority order

1. **Bb Clarinet** → covers Eb/A as shared, Bass clarinet as variant
2. **Alto Sax** → covers soprano/tenor/bari as shared
3. **Concert Flute** → covers alto flute as shared, piccolo as variant (sideways layout)
4. **Oboe** → covers cor anglais as variant
5. **Soprano Recorder** → covers alto/tenor/bass as shared
6. **D Whistle** → covers low D as shared
7. **Ocarina** → two separate SVGs (12-hole + 7-hole)

---

## Common pitfalls

**Dim keys when they should be filled**
→ Subpath appears in both bodyPath and keyPath. Remove from body.

**Sub tab doesn't switch**
→ Check all four wiring locations. `_buildSubRow` currentSub ternary is the most
   commonly missed — it's one long inline chain and easy to overlook.

**Keys missing from SVG**
→ FDB exported with "Crop: Visible keys" not "All keys". Re-export.

**Half-hole branch left in for instruments that don't use it**
→ Dead code. Remove it. Bassoon had this and it was removed.

**Wrong slot count in dispatch guard**
→ Silent failure — renderer runs but maps wrong data to wrong keys.
   Always verify against the LAYOUT constant.

**Renderer function uses ad-hoc boolean instead of subKey string**
→ Fine for bassoon (already shipped). Use subKey string for all new ones.

**Off-by-one in sub[] index**
→ Most common error in compound paths with 10+ subpaths. Re-run analysis script.

**Boot keys appear cut off**
→ Boot keys extend to y≈480 in original coords (screen y≈362 after transform),
   which fits inside the 371.889 viewBox. If still cut off, check viewBox wasn't
   accidentally modified.
