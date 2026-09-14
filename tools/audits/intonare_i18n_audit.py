#!/usr/bin/env python3
"""
intonare_i18n_audit.py — find EVERY user-facing string that does not translate.

Written after chasing individual untranslated strings one screenshot at a time.
The point is to stop doing that: this looks in all six places a string can hide,
rather than the one place someone happened to notice.

    python3 intonare_i18n_audit.py Intonare.html

CATEGORIES
  A  data-i18n keys missing from the EN or IT table
  B  static markup text with no data-i18n attribute
  C  JS assigning an English literal to textContent / innerHTML
  D  data tables with a `name` but no `nameIt` twin (grooves, presets, kits)
  E  t() called with a key that exists in neither table (prints the key itself)
  F  note names rendered without getDisplayNote (breaks Solfège)

Category D is the one that bites hardest: those are content tables, so a missing
twin silently ships English inside an otherwise Italian screen.
"""
import re, sys, json
from collections import Counter

PATH = sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html'
H = open(PATH, encoding='utf-8').read()

def section(t):
    print('\n' + '=' * 70)
    print('  ' + t)
    print('=' * 70)

# Locate the two string tables by an anchor known to exist in both.
def string_blocks():
    en_i = H.index("gtool_play_asc:'\u25b6\ufe0e PLAY ASCENDING'")
    it_i = H.index("gtool_play_asc:'\u25b6\ufe0e SUONA ASCENDENTE'")
    # widen generously; overlap is harmless because we only test membership
    return H[en_i - 90000:en_i + 90000], H[it_i - 90000:it_i + 90000]

EN_BLK, IT_BLK = string_blocks()
issues = Counter()

# ── A: data-i18n keys present in markup but missing from a table ──────────────
section('A  data-i18n keys missing from a language table')
keys = sorted(set(re.findall(r'data-i18n="([\w.]+)"', H)))
miss_en = [k for k in keys if f'{k}:' not in EN_BLK]
miss_it = [k for k in keys if f'{k}:' not in IT_BLK]
print(f'  {len(keys)} keys used in markup')
for label, lst in (('EN', miss_en), ('IT', miss_it)):
    if lst:
        issues['A'] += len(lst)
        print(f'  MISSING from {label}: {len(lst)}')
        for k in lst[:25]:
            print(f'     {k}')
    else:
        print(f'  {label}: complete')

# ── B: visible markup text with no data-i18n on its element ──────────────────
section('B  static markup text with no data-i18n')
# Only flag things that look like prose/labels: starts uppercase or is a word
# with a space. Skip note names, numbers, symbols, single letters.
SKIP = re.compile(r'^(?:[A-G][#b\u266f\u266d]?\d?|\d+|[\W_]+|[A-Z]|BPM|Hz|OFF|ON|VOL|LV)$')
b_hits = []
for m in re.finditer(r'>\s*([A-Za-z][A-Za-z0-9 ,\'\u2019/&\.\-\u00e0-\u00ff]{2,60})\s*<', H):
    tag = H[max(0, m.start() - 400):m.start()].rsplit('<', 1)[-1]
    if 'data-i18n' in tag:
        continue
    txt = m.group(1).strip()
    if not txt or SKIP.match(txt):
        continue
    # Inside <script>/<style>? Look back for the opener. The 3000-char window was
    # too small: a long script block put the opener out of reach, so HTML built
    # inside JS template strings (organ drawbars, Leslie controls, chart internals
    # around line 110k) was counted as static markup. It is not — applyLang()
    # cannot reach it, because it is regenerated on every render. Those need the
    # _tf() treatment at the point of construction instead, so counting them here
    # inflated B by roughly a thousand and hid the real static strings.
    before = H[:m.start()]
    if before.rfind('<script') > before.rfind('</script'):
        continue
    if before.rfind('<style') > before.rfind('</style'):
        continue
    b_hits.append(txt)
bc = Counter(b_hits)
issues['B'] = len(bc)
print(f'  {len(bc)} distinct untagged strings')
for t, n in bc.most_common(40):
    print(f'   {n:3d}x  {t[:64]}')

# ── C: JS writing an English literal straight to the DOM ─────────────────────
section('C  JS assigning a literal to textContent / innerHTML')
c_hits = []
for m in re.finditer(r'\.(?:textContent|innerHTML)\s*=\s*([\'"])([A-Za-z][^\'"]{2,60})\1', H):
    txt = m.group(2)
    if SKIP.match(txt) or txt.startswith('<'):
        continue
    ln = H[:m.start()].count('\n') + 1
    c_hits.append((ln, txt))
issues['C'] = len(c_hits)
print(f'  {len(c_hits)} sites')
for ln, t in c_hits[:40]:
    print(f'   line {ln:>6}  {t[:60]}')

# ── D: content tables with name but no nameIt ────────────────────────────────
section('D  data entries with `name` but no `nameIt`')
d_hits = []
# Scan object literals that carry a name: field, look for a sibling nameIt.
for m in re.finditer(r'\{[^{}]{0,400}?\bname\s*:\s*([\'"])(.*?)\1[^{}]{0,400}?\}', H, re.S):
    blob, nm = m.group(0), m.group(2)
    if 'nameIt' in blob:
        continue
    if len(nm) < 3 or SKIP.match(nm):
        continue
    ln = H[:m.start()].count('\n') + 1
    d_hits.append((ln, nm))
issues['D'] = len(d_hits)
print(f'  {len(d_hits)} entries with no Italian twin')
for ln, nm in d_hits[:50]:
    print(f'   line {ln:>6}  {nm[:60]}')

# ── E: t() keys that exist in neither table ──────────────────────────────────
section("E  t('key') where the key is in neither table")
e_hits = []
for m in re.finditer(r"\bt\(\s*'([\w.]+)'\s*\)", H):
    k = m.group(1)
    if f'{k}:' in EN_BLK or f'{k}:' in IT_BLK:
        continue
    ln = H[:m.start()].count('\n') + 1
    e_hits.append((ln, k))
seen = set()
uniq = [(l, k) for l, k in e_hits if not (k in seen or seen.add(k))]
issues['E'] = len(uniq)
print(f'  {len(uniq)} keys resolve to their own name (t() returns the key)')
for ln, k in uniq[:30]:
    print(f'   line {ln:>6}  {k}')

# ── F: note-name output bypassing getDisplayNote ─────────────────────────────
section('F  note names rendered without getDisplayNote (Solfège)')
f_hits = []
NOTE_ARRAYS = re.findall(r'\b(_BN|NOTE_NAMES|GCC_ROOT_DISPLAY|LETTERS)\b\s*\[', H)
for m in re.finditer(r'\.textContent\s*=\s*([A-Za-z_]\w*)\s*\[', H):
    arr = m.group(1)
    if arr not in ('_BN', 'NOTE_NAMES', 'GCC_ROOT_DISPLAY', 'LETTERS'):
        continue
    ln = H[:m.start()].count('\n') + 1
    f_hits.append((ln, arr))
issues['F'] = len(f_hits)
print(f'  {len(f_hits)} direct note-array writes to the DOM')
for ln, a in f_hits:
    print(f'   line {ln:>6}  {a}[...]')

# ── G: translated builders that no language change will ever re-run ──────────
section('G  builders emitting translated text that setLang never re-runs')
# The failure this catches: a function renders text through t() or a nameIt twin,
# is called once when its screen opens, and is neither in setLang's builder list
# nor registered via registerRelabel(). Switching language leaves it stale, and
# nothing anywhere reports it — you find out from a screenshot.
i = H.index('function setLang')
seg = H[i:i + 4000]
called = set(re.findall(r'(\w+)\s*&&\s*\1\(\)', seg)) | set(re.findall(r'try\s*\{\s*(\w+)\(\)', seg))
registered = set(re.findall(r'registerRelabel\([^,]+,\s*function\s*\(\)\s*\{([^}]*)\}', H))
reg_calls = set()
for blob in registered:
    reg_calls |= set(re.findall(r'(\w+)\s*\(', blob))
covered = called | reg_calls

starts = [(m.group(1), m.end()) for m in re.finditer(r'^function (\w+)\s*\(', H, re.M)]
g_hits = []
for idx, (fn, st) in enumerate(starts):
    if fn in covered:
        continue
    end = starts[idx + 1][1] if idx + 1 < len(starts) else len(H)
    body = H[st:min(end, st + 20000)]
    # builds DOM AND emits translated text AND looks like a one-shot builder
    if not re.search(r'\b(innerHTML|createElement)\b', body):
        continue
    if not ("t('" in body or 'nameIt' in body or "lang === 'it'" in body):
        continue
    if not re.match(r'^(build|render|init|draw|make|populate|fill)', fn, re.I):
        continue
    g_hits.append(fn)
issues['G'] = len(g_hits)
print(f'  setLang covers {len(called)} builders; registerRelabel covers {len(reg_calls)}')
print(f'  {len(g_hits)} builders emit translated text and are covered by neither:')
for fn in g_hits[:30]:
    print(f'     {fn}')
print('\n  Each is a screen that MAY keep the old language until it is rebuilt.')
print('  Fix by adding registerRelabel(elementId, fn) next to the others in setLang.')

# ── summary ──────────────────────────────────────────────────────────────────
section('SUMMARY')
total = sum(issues.values())
for k in 'ABCDEFG':
    print(f'   {k}: {issues[k]}')
print(f'\n   TOTAL: {total}')
print('\n   B and C need judgement: many are dev-only surfaces or symbols.')
print('   A, D, E, F and G are unambiguous — those ship English inside Italian.')
sys.exit(1 if (issues['A'] or issues['D'] or issues['E'] or issues['F']) else 0)
