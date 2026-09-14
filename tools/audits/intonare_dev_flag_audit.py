"""Can a user reach the developer tools, and can anything there grant Pro?

There was a script for this on the checklist that was never written, and the
version described would have grepped for a plaintext `DEV_CODE` that stopped
existing in v0.150.75 when the unlock codes were hashed to SHA-256. A grep for a
string that cannot be there passes every time, which is worse than no check at
all: it reports safe without looking.

So this checks the things that actually gate the tools now.

  FLAG      INTONARE_DEV must default to false and come only from a manually
            set localStorage key. If any UI path sets it, the tools are one
            gesture away for a curious user.
  BUTTON    the Reset Pro control must be display:none in markup AND gated on
            INTONARE_DEV at every place that shows it.
  FUNCTION  resetProTesting must return early when the flag is off, so calling
            it from a console does nothing.
  MONEY     nothing behind the dev flag may set hasPro true. Revoking Pro is
            harmless; granting it is revenue.
  CODES     unlock codes must be hashed, not present as plaintext literals.
"""
import re, sys, os, hashlib

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'Intonare.html')

H = open(path, encoding='utf-8').read()

fails, notes = [], []

def check(ok, label, detail=''):
    (notes if ok else fails).append((label, detail))

# ── FLAG ────────────────────────────────────────────────────────────────────
check(bool(re.search(r'let INTONARE_DEV = false;', H)),
      'INTONARE_DEV defaults to false')

# Line-based, not regex: a pattern starting with [^/\n]* rescans backward from
# every position in a 10MB file and never finishes.
lines = H.split('\n')
setters = [ln for ln in lines if "setItem('intonare_dev'" in ln]
# A commented-out console recipe is documentation, not a path.
live = [ln for ln in setters if not ln.strip().startswith('//')]
check(len(live) == 1 and 'function setDevMode' in H,
      'only setDevMode writes the flag', f'{len(live)} live writer(s)')

# Is setDevMode reachable from any onclick or listener?
ui = [ln for ln in lines
      if 'setDevMode' in ln and ('onclick=' in ln or 'addEventListener' in ln)]
check(not ui, 'no UI path calls setDevMode', f'{len(ui)} found' if ui else '')

# ── BUTTON ──────────────────────────────────────────────────────────────────
btn = re.search(r'<button id="smResetProBtn"[^>]*>', H)
check(bool(btn) and 'display:none' in btn.group(0),
      'Reset Pro button is display:none in markup')

# Sliced by hand rather than matched with a wildcard span: [\s\S]{0,220} across a
# 10MB file backtracks for minutes.
shows = []
for m in re.finditer(r"getElementById\('smResetProBtn'\)", H):
    seg = H[m.start(): m.start() + 260]
    d = re.search(r"display\s*=\s*([^;]+);", seg)
    if d:
        shows.append(d.group(1))
ungated = [s for s in shows if 'INTONARE_DEV' not in s and "'none'" not in s]
check(not ungated, 'every show of the button checks INTONARE_DEV',
      f'{len(ungated)} ungated' if ungated else f'{len(shows)} site(s) checked')

# ── FUNCTION ────────────────────────────────────────────────────────────────
i = H.find('function resetProTesting()')
body = H[i:i + 320] if i >= 0 else ''
check(bool(body) and 'INTONARE_DEV' in body and 'return' in body,
      'resetProTesting returns early without the flag')

# ── MONEY ───────────────────────────────────────────────────────────────────
# Every assignment that grants Pro, and whether any sits in a dev-gated block.
grants = [m.start() for m in re.finditer(r'hasPro\s*=\s*true', H)]
risky = []
for g in grants:
    window = H[max(0, g - 700):g]
    if 'INTONARE_DEV' in window:
        risky.append(g)
check(not risky, 'nothing behind the dev flag grants Pro',
      f'{len(grants)} grant site(s), {len(risky)} dev-adjacent')

# ── CODES ───────────────────────────────────────────────────────────────────
plain = [ln.strip()[:60] for ln in lines
         if re.search(r"(?:DEV_CODE|UNLOCK_CODE)\s*=\s*'[A-Z_]{4,}'", ln)]
check(not plain, 'no plaintext unlock code constant', ', '.join(plain))
hashes = re.findall(r"'([a-f0-9]{64})'", H)
check(len(hashes) >= 2, 'unlock codes stored as SHA-256', f'{len(hashes)} hash literal(s)')

# ── REPORT ──────────────────────────────────────────────────────────────────
print('DEV TOOLS REACHABILITY')
print('=' * 62)
for label, detail in notes:
    print(f'  ok    {label}' + (f'   ({detail})' if detail else ''))
for label, detail in fails:
    print(f'  FAIL  {label}' + (f'   ({detail})' if detail else ''))
print('=' * 62)
if fails:
    print(f'  {len(fails)} issue(s): the dev tools may be reachable in a shipped build.')
    sys.exit(1)
print('  Dev tools are unreachable without manually setting localStorage,')
print('  and nothing behind the flag can grant Pro.')
