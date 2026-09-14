#!/usr/bin/env python3
"""
intonare_audio_handle_audit.py — catch unstoppable audio before it ships.

THE PATTERN THIS EXISTS FOR
The same bug was found nine separate times in one session: a function starts a
note and throws away the handle the player returned, so no stop function can
ever silence it. The session token / timer clearing that usually sits alongside
it only prevents notes that HAVEN'T started; anything already sounding runs to
its full length. Found in interval training, the interval reference tool, the
interval peek, harp chords, both chart dot-taps, the 12-string doubled course,
sight singing, and addLowFreqHarmonics (which returned nothing at all).

It hides well because the stop function LOOKS right — it clears timers, bumps a
session counter, maybe stops one tracked node — so the bug only shows as "some
audio kept playing" in a specific register or a specific instrument.

WHAT IT CHECKS
  Part 1  the structural fixes from the audio work are still in place
  Part 2  [A] play calls whose return value is discarded
          [B] hand-maintained partial stop lists (these drift; three did)
          [C] textContent-based DOM lookups (break under translation)
          [D] synth voices that create nodes and never disconnect them

Part 2 findings are NOT automatic failures. Some are legitimate: a fire-and-
forget UI blip nobody needs to stop, a label match on an untranslated string.
Read them, decide, and fix or leave deliberately.

USAGE: python3 intonare_audio_handle_audit.py [Intonare.html]
"""
import re, sys
h = open(sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html', encoding='utf-8').read()

def fn_body(name):
    m = re.search(r'\nfunction '+re.escape(name)+r'\s*\([^)]*\)\s*\{', h)
    if not m: return None
    i = m.end(); d = 1
    while i < len(h) and d:
        if h[i] == '{': d += 1
        elif h[i] == '}': d -= 1
        i += 1
    return h[m.start():i]

FAIL = []
def check(label, cond, detail=''):
    print(f"  {'✓' if cond else '✗'} {label}" + (f"  {detail}" if detail and not cond else ''))
    if not cond: FAIL.append(label)

print("="*74); print("  PART 1 — THIS SESSION'S FIXES STILL PRESENT"); print("="*74)

check("master bus exists",            'function _getMasterOut' in h)
check("lookahead limiter worklet",    'lookahead-limiter' in h and 'registerProcessor' in h)
check("sliding-window max detector",  '_pushMax' in h and 'monotonic' in h.lower())
check("per-context bus map",          '_masterBuses = new Map()' in h)
check("per-context worklet promises", '_limiterWorkletPromises = new Map()' in h)
raw_dest = len(re.findall(r'\.connect\(\w+\.destination\)', h))
check("only master bus hits destination", raw_dest == 2, f"found {raw_dest}, expected 2")
check("adaptive headroom (fail-safe)", 'let SYNTH_HEADROOM = 0.32' in h and 'SYNTH_HEADROOM_LIMITED' in h)
check("audioPathStatus diagnostic",   'function audioPathStatus' in h)
check("organ stagger on mass release",'v.stop(false, i * 0.006)' in h)
check("organ node teardown list",     '_toDisconnect' in h)
check("organ finite-voice cleanup",   'voice.stop(true)' in h)
check("harmonics return a handle",    'addLowFreqHarmonics' in h and 'return {\n    stop(at)' in h)
check("chart button registry",        'CHART_BTNS' in h and 'function _chartBtnsResetAll' in h)
check("harp chord nodes tracked",     'hpChordNodes' in h)
check("iv node tracking",             'let ivNodes' in h)
check("kit lookup by data-kit",       "b.dataset.kit === p.kit" in h)
check("clearAll resets to custom",    (fn_body('clearAll') or '').count('_customIdx') > 0)
check("tray syncs categories",        'function progSyncTrayCategories' in h)
check("drum preset selection tracked",'progDkSelectedName' in h)
sa = fn_body('stopAllAudio') or ''
check("stopAllAudio covers drones",   all(x in sa for x in
      ['stopAllRhodesDrones','stopAllPianoDrones','stopAllRef','_organStopAll','diadleStopDrone']))
csa = fn_body('chordScaleStopAllAudio') or ''
check("chart stop list complete",     all(x in csa for x in
      ['gccStop','gssStop','pccStop','pssStop','hpStop','trpStop','_bowedStopAll',
       'bowedScaleStop','_organStopAll','didiStop','fluteTrillStop']))
check("chart stop resets buttons",    '_chartBtnsResetAll' in csa)

print()
print("="*74); print("  PART 2 — SAME PATTERNS ELSEWHERE"); print("="*74)

# A. fire-and-forget: play call whose return value is discarded, on its own line
print("\n  [A] Discarded audio-node returns (nothing can stop these)")
players = ['_chartPlay', '_samplePlay', 'practicePlayNote', 'ssPlayNoteEnhanced',
           'windSynth', r'\w+\.synth', 'addLowFreqHarmonics']
ff = []
for ln, line in enumerate(h.split('\n'), 1):
    s = line.strip()
    for p in players:
        if re.match(r'^'+p+r'\s*\(', s):        # bare call, return discarded
            ff.append((ln, p, s[:78]))
if ff:
    for ln,p,s in ff: print(f"      line {ln:>6}  {s}")
else:
    print("      none")

# B. partial hand-maintained stop lists
print("\n  [B] Partial stop lists (subsets of a fuller list)")
partial = []
for m in re.finditer(r'^\s*(\w*[Ss]top\w*\(\);\s*){2,}$', h, re.M):
    partial.append(m.group(0).strip()[:70])
print("      " + ("\n      ".join(partial) if partial else "none"))

# C. label-based DOM lookups (break under translation)
print("\n  [C] textContent-based element lookups (locale-fragile)")
lc = re.findall(r'.{0,70}textContent(?:\.toLowerCase\(\))?\s*===[^\n]{0,50}', h)
if lc:
    for x in lc: print(f"      {x.strip()[:100]}")
else:
    print("      none")

# D. synth voices creating nodes with no disconnect
print("\n  [D] Synth voices creating nodes with zero .disconnect()")
start = h.find('const REF_TONES')
seg = h[start:start+400000]
names = list(re.finditer(r'\n  (\w+): \{', seg))
leaky = []
for i,m in enumerate(names):
    end = names[i+1].start() if i+1 < len(names) else len(seg)
    body = seg[m.start():end]
    if 'synth(ctx' not in body: continue
    nc = len(re.findall(r'create(?:Gain|BiquadFilter|WaveShaper|Delay)\(', body))
    nd = len(re.findall(r'\.disconnect\(', body))
    if nc and not nd: leaky.append((m.group(1), nc))
for n,c in leaky: print(f"      {n:22s} creates {c} nodes, disconnects none")
if not leaky: print("      none")

print()
print("="*74)
print(f"  PART 1 RESULT: {'ALL PASS' if not FAIL else str(len(FAIL))+' FAILED: '+', '.join(FAIL)}")
print("="*74)
