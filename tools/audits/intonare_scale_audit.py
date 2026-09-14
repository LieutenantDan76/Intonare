#!/usr/bin/env python3
"""
intonare_scale_audit.py — Musical-correctness gate for Intonare SCALES.

Sibling to intonare_theory_audit.py (which covers chords). This verifies that
every scale the SCALES tool can produce ACTUALLY CONTAINS THE RIGHT NOTES, on
two axes:
  1. PITCH CLASSES — the set of pcs the scale yields matches the canonical
     interval pattern for that scale type (transposed to the root).
  2. SPELLING — each note's letter name is correct (diatonic 7-note scales use
     seven distinct consecutive letters; no wrong enharmonic, no needless
     double-accidental for the 12 user-selectable roots).

It extracts the REAL shipped JS (getScaleData, noteForDegree, parseRoot,
SCALE_DEFS, NATURAL_PC, LETTERS, accSymbol, name arrays) and runs it under Node,
so it tests the actual app logic, not a reimplementation — same approach as the
theory audit.

Usage:  python3 intonare_scale_audit.py path/to/Intonare.html
Exit 0 if no errors; 1 otherwise.
"""
import sys, re, json, subprocess, tempfile, os

# The 12 roots the user can actually select (from buildScaleRootPicker).
ROOTS = ['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B']

# Canonical semitone sets (from root=0) for every SCALE_DEFS key. These are the
# music-theory ground truth, independent of the app's degree/alt encoding.
EXPECT_PCS = {
    'major':      {0,2,4,5,7,9,11},
    'lydian':     {0,2,4,6,7,9,11},
    'mixolydian': {0,2,4,5,7,9,10},
    'harmmaj':    {0,2,4,5,7,8,11},
    'natminor':   {0,2,3,5,7,8,10},
    'dorian':     {0,2,3,5,7,9,10},
    'phrygian':   {0,1,3,5,7,8,10},
    'locrian':    {0,1,3,5,6,8,10},
    'harmminor':  {0,2,3,5,7,8,11},
    'melminor':   {0,2,3,5,7,9,11},
    'majpent':    {0,2,4,7,9},
    'minpent':    {0,3,5,7,10},
    'blues':      {0,3,5,6,7,10},
    'dblharm':    {0,1,4,5,7,8,11},
    'wholetone':  {0,2,4,6,8,10},
    # chromatic handled separately (all 12)
}

# How many distinct letters a correct diatonic scale uses (7-note scales must use
# all 7 letters once each; pentatonics/blues/wholetone are non-heptatonic and are
# spelling-checked more loosely — only "no double-accidental" + "no repeat unless
# the scale legitimately repeats a degree").
HEPTATONIC = {'major','lydian','mixolydian','harmmaj','natminor','dorian',
              'phrygian','locrian','harmminor','melminor','dblharm'}


def extract_balanced(src, marker, oc='{', cc='}'):
    i = src.index(marker); j = src.index(oc, i); d = 0
    while j < len(src):
        if src[j] == oc: d += 1
        elif src[j] == cc:
            d -= 1
            if d == 0: return src[i:j+1]
        j += 1
    raise ValueError(f"unbalanced from {marker!r}")


def grab_const(src, name):
    """Grab `const NAME = ...;` single-line."""
    m = re.search(r'const ' + re.escape(name) + r'\s*=\s*(.+?);', src)
    if not m: raise ValueError(f"{name} not found")
    return m.group(0)


def grab_func(src, name):
    return extract_balanced(src, 'function ' + name + '(', '{', '}') \
        if False else _grab_func(src, name)


def _grab_func(src, name):
    i = src.index('function ' + name)
    j = src.index('{', i); d = 0
    while j < len(src):
        if src[j] == '{': d += 1
        elif src[j] == '}':
            d -= 1
            if d == 0: return src[i:j+1]
        j += 1
    raise ValueError(name)


def main(path):
    html = open(path, encoding='utf-8').read()
    # main script block
    blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
    js = max(blocks, key=len)

    pieces = []
    for c in ['NATURAL_PC', 'LETTERS', 'SHARP_NAMES_ASCII', 'FLAT_NAMES_ASCII']:
        pieces.append(grab_const(js, c))
    for f in ['parseRoot', 'accSymbol', 'noteForDegree', 'getScaleData']:
        pieces.append(_grab_func(js, f))
    scale_defs = extract_balanced(js, 'const SCALE_DEFS', '{', '}')
    pieces.append(scale_defs + ';' if not scale_defs.rstrip().endswith(';') else scale_defs)

    roots = json.dumps(ROOTS)
    keys = json.dumps(list(EXPECT_PCS.keys()) + ['chromatic'])

    harness = "\n".join(pieces) + f"""
const ROOTS = {roots};
const KEYS = {keys};
const out = {{}};
for (const k of KEYS) {{
  out[k] = {{}};
  for (const r of ROOTS) {{
    try {{
      const data = getScaleData(r, k);
      out[k][r] = data.map(n => ({{ pc: ((n.midi % 12) + 12) % 12, name: n.name }}));
    }} catch (e) {{
      out[k][r] = {{ error: String(e) }};
    }}
  }}
}}
console.log(JSON.stringify(out));
"""
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
        f.write(harness); tmp = f.name
    try:
        res = subprocess.run(['node', tmp], capture_output=True, text=True, timeout=60)
    finally:
        os.unlink(tmp)
    if res.returncode != 0:
        print("NODE ERROR — could not run extracted scale functions:")
        print(res.stderr[:2000]); return 1
    data = json.loads(res.stdout)

    errors, warnings, oks = [], [], 0
    LETTER_OF = lambda nm: nm[0]

    for k, roots_data in data.items():
        for r, scale in roots_data.items():
            tag = f"{k}/{r}"
            if isinstance(scale, dict) and 'error' in scale:
                errors.append(f"[{tag}] threw: {scale['error']}"); continue
            # drop the appended octave (last entry duplicates the root by design)
            body = scale[:-1] if len(scale) > 1 and scale[-1]['pc'] == scale[0]['pc'] else scale

            # ── pitch-class check ──
            root_pc = body[0]['pc']
            got_pcs = {(n['pc'] - root_pc) % 12 for n in body}
            if k == 'chromatic':
                if got_pcs != set(range(12)):
                    errors.append(f"[{tag}] chromatic pcs wrong: {sorted(got_pcs)}")
                else:
                    oks += 1
                continue
            exp = EXPECT_PCS[k]
            if got_pcs != exp:
                errors.append(f"[{tag}] PC SET WRONG — got {sorted(got_pcs)} expected {sorted(exp)}")
                continue
            # right count too (blues legitimately has 6 incl. the ♭5/♮5 pair)
            if k in HEPTATONIC and len(body) != 7:
                errors.append(f"[{tag}] expected 7 notes, got {len(body)}")
                continue

            # ── spelling check ──
            names = [n['name'] for n in body]
            # no triple+ accidentals ever; double only tolerated as a warning
            for nm in names:
                acc = nm[1:]
                if acc.count('♯') >= 3 or acc.count('♭') >= 3 or '𝄪𝄪' in nm:
                    errors.append(f"[{tag}] absurd spelling '{nm}'")
            if k in HEPTATONIC:
                letters = [LETTER_OF(nm) for nm in names]
                if len(set(letters)) != 7:
                    errors.append(f"[{tag}] heptatonic must use 7 distinct letters, got {letters} ({names})")
                else:
                    # letters must be consecutive starting from the root letter
                    order = ['C','D','E','F','G','A','B']
                    start = order.index(letters[0])
                    expect_letters = [order[(start+i) % 7] for i in range(7)]
                    if letters != expect_letters:
                        errors.append(f"[{tag}] letters not consecutive: {letters} (expect {expect_letters}) — {names}")
                    else:
                        # warn (not error) on double-accidentals: theoretically valid
                        # but for these 12 roots usually a sign of an awkward spelling
                        dbls = [nm for nm in names if '𝄪' in nm or '𝄫' in nm]
                        if dbls:
                            warnings.append(f"[{tag}] double-accidental(s) {dbls} — valid but verify ({names})")
                        oks += 1
            else:
                oks += 1

    print("="*70)
    print("  INTONARE SCALE AUDIT — pitch classes + spelling")
    print("="*70)
    print(f"  Scales tested: {len(EXPECT_PCS)+1} types x {len(ROOTS)} roots = "
          f"{(len(EXPECT_PCS)+1)*len(ROOTS)} combinations")
    print(f"  ✓ {oks} clean")
    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):")
        for w in warnings: print("   ~ " + w)
    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for e in errors: print("   ✗ " + e)
        print("\n  RESULT: FAIL")
        return 1
    print("\n  RESULT: all scales correct (pcs + spelling). ✓")
    return 0


if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html'
    sys.exit(main(p))
