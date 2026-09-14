"""Duplicate detection by shared distinctive words, not by an exact core match.

Three earlier scans each missed pairs: "Tin Pan Alley" vs "Tin Pan Alley and when
did it end", "No Wave scene" vs "No Wave movement", "loudness war" vs "loudness
war and what ended it". All failed the same way: they required the same normalised
key, and one extra content word changes the key.

This compares SETS instead. Two questions in the same pack that share most of
their distinctive words are asking the same thing however they are phrased.
"""
# ─────────────────────────────────────────────────────────────────────────────
# READ ONLY. Safe to run at any time; never writes to Intonare.html.
# ─────────────────────────────────────────────────────────────────────────────
import os, sys
HTML_PATH = os.environ.get(
    'INTONARE_HTML',
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), 'Intonare.html'))

if not os.path.exists(HTML_PATH):
    sys.exit(f"{HTML_PATH} not found. Copy it there or set INTONARE_HTML.")

import re, sys, itertools, collections
H=open(HTML_PATH,encoding='utf-8').read()
i=H.index('PACKS = {'); seg=H[i:]
keys=[(m.start(), m.group(1)) for m in re.finditer(r'\n(\w+):\s*\{\n  group:', seg)]
QRE=re.compile(r'\{q:"((?:[^"\\]|\\.)*)"')
STOP=set("""what is a an the does do mean in on of and or why it matter to for which used when who how
are was were with from that this its his her did had have been being by as at be about most into
significant significance known famous first main primary role impact effect""".split())
def words(q):
    q=re.sub(r'\\.','',q).lower(); q=re.sub(r'[^a-z0-9 ]',' ',q)
    return {w for w in q.split() if w not in STOP and len(w)>2}
packs=collections.defaultdict(list)
for n,(pos,k) in enumerate(keys):
    end=keys[n+1][0] if n+1<len(keys) else pos+90000
    for m in QRE.finditer(seg[pos:end]):
        packs[k].append(m.group(1))
def same(a,b,thresh=0.85):
    wa,wb=words(a),words(b)
    if len(wa)<2 or len(wb)<2: return False
    inter=wa&wb
    return len(inter)>=2 and len(inter)/min(len(wa),len(wb)) >= thresh

pairs=[]
for k,qs in packs.items():
    for a,b in itertools.combinations(qs,2):
        if same(a,b): pairs.append((k,a[:52],b[:52]))
print(f'{sum(len(v) for v in packs.values())} questions, {len(pairs)} same-topic pairs WITHIN a pack\n')
for k,a,b in pairs[:26]:
    print(f'  {k:18} {a}\n  {"":18} {b}\n')

# ── Across packs ─────────────────────────────────────────────────────────────
# Packs are built from what they should contain, so topic overlap between them
# is expected and fine: Bass and Gear both cover strings, Guitar Gods and Guitar
# Technique both cover picking. What costs something is the same QUESTION in two
# packs, because a custom round can select both and deal it twice. That is the
# only cross-pack fault worth reporting, so the bar here is deliberately higher
# than the within-pack one.
cross=[]
names=list(packs.keys())
for ka,kb in itertools.combinations(names,2):
    for a in packs[ka]:
        for b in packs[kb]:
            # Jaccard, not containment. Containment divides by the SHORTER
            # question, so two short unrelated ones score high: "Which Beatle
            # played bass?" against "Who played bass in The Who?" came out as a
            # duplicate. Intersection over union punishes that, because the
            # union carries the words they do not share.
            wa,wb=words(a),words(b)
            if len(wa)<3 or len(wb)<3: continue
            u=len(wa|wb)
            if u and len(wa&wb)/u >= 0.7: cross.append((ka,kb,a[:56],b[:56]))
print(f'{len(cross)} question(s) appearing in more than one pack\n')
for ka,kb,a,b in cross[:20]:
    print(f'  [{ka}] {a}\n  [{kb}] {b}\n')
if not cross:
    print('  none — topic overlap between packs is expected and is not reported here.')
