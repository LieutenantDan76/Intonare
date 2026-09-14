"""Leaks that are not about length: grammar, form and specificity.

Four ways an option can be identifiable without knowing the answer.

  ARTICLE    the stem ends "a" or "an" and only one option agrees.
  PLURAL     the stem asks "which guitarists" and only one option is plural.
  ONLY-QUALIFIED  only the correct answer carries a hedge (usually, often,
             typically, generally). Test writers add them to make an answer
             defensible and hand it over instead.
  ABSOLUTE-DISTRACTOR  every WRONG option carries never/always/all/only. A
             sophisticated guesser eliminates absolutes and lands on the answer.
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

import re, sys, collections
H=open(HTML_PATH,encoding='utf-8').read()
i=H.index('PACKS = {'); seg=H[i:]
keys=[(m.start(), m.group(1)) for m in re.finditer(r'\n(\w+):\s*\{\n  group:', seg)]
QRE=re.compile(r'\{q:"((?:[^"\\]|\\.)*)",\s*opts:\[((?:[^\]\\]|\\.)*)\],\s*ans:(\d+)')
STR=re.compile(r'"((?:[^"\\]|\\.)*)"')
HEDGE=re.compile(r'\b(usually|often|typically|generally|most|commonly|tends? to)\b', re.I)
ABS=re.compile(r'\b(never|always|all|only|every|no other|entirely|exclusively)\b', re.I)
want=sys.argv[1] if len(sys.argv)>1 else None
found=collections.defaultdict(list)
for n,(pos,k) in enumerate(keys):
    end=keys[n+1][0] if n+1<len(keys) else pos+90000
    if want and k!=want: continue
    for m in QRE.finditer(seg[pos:end]):
        q=m.group(1); o=STR.findall(m.group(2)); a=int(m.group(3))
        if a>=len(o) or len(o)<3: continue
        # ONLY-QUALIFIED
        hedged=[j for j,x in enumerate(o) if HEDGE.search(x)]
        if hedged==[a]: found['only-qualified'].append((k,q[:46],o[a][:40]))
        # ABSOLUTE-DISTRACTOR
        absol=[j for j,x in enumerate(o) if ABS.search(x)]
        if len(absol)==len(o)-1 and a not in absol:
            found['absolutes-in-wrong'].append((k,q[:46],o[a][:40]))
        # PLURAL agreement
        # Real plural nouns only. The first version matched "what IS", because
        # "is" ends in an s, and reported 220 false positives.
        VERBS = {'is','was','has','does','goes','makes','means','gives','uses','sounds'}
        pm = re.search(r'\b(which|what)\s+(\w+s)\b', q, re.I)
        if pm and pm.group(2).lower() not in VERBS and not pm.group(2).lower().endswith('ss'):
            plur=[j for j,x in enumerate(o) if re.search(r'\b(and|both|,)\b', x)]
            if plur==[a]: found['plural-agreement'].append((k,q[:46],o[a][:40]))
        # ARTICLE agreement
        mm=re.search(r'\b(an?)\s*[\?\'"]?\s*$', q.strip())
        if mm:
            art=mm.group(1).lower()
            fit=[j for j,x in enumerate(o) if (x[:1].lower() in 'aeiou')==(art=='an')]
            if fit==[a]: found['article-agreement'].append((k,q[:46],o[a][:40]))
print('NON-LENGTH LEAKS' + (f'  [{want}]' if want else '  [all packs]'))
for kind in ('only-qualified','absolutes-in-wrong','plural-agreement','article-agreement'):
    v=found[kind]
    print(f'  {kind:22} {len(v)}')
print()
for kind,v in found.items():
    if not v: continue
    print(f'--- {kind}')
    for k,q,a in v[:8]: print(f'    {k:16} {q:48} -> {a}')
