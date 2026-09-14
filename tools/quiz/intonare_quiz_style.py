"""AI-writing tells in quiz questions and blurbs, which nothing has checked yet."""
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
# Tolerant of q_it/opts_it sitting between the fields and of whitespace after
# the commas. The strict version matched zero questions in every bilingual
# pack, so guitar_gods, theory_fundamentals, seventies and bass were being
# reported clean because nothing had been read.
QRE=re.compile(r'\{\s*q\s*:\s*"((?:[^"\\]|\\.)*)"'            r'(?:\s*,\s*q_it\s*:\s*"(?:[^"\\]|\\.)*")?'            r'\s*,\s*opts\s*:\s*\[((?:[^\]\\]|\\.)*)\]'            r'(?:\s*,\s*opts_it\s*:\s*\[(?:[^\]\\]|\\.)*\])?'            r'\s*,\s*ans\s*:\s*(\d+)'            r'(?:.*?fact\s*:\s*"((?:[^"\\]|\\.)*)")?', re.S)
STR=re.compile(r'"((?:[^"\\]|\\.)*)"')
TELLS = [
 ('em-dash',      re.compile(r'\u2014')),
# The rhetorical triple, not any list of three. The old pattern matched
 # "E, A, D and G" (a tuning), "Emerson, Lake and Palmer" (a band) and
 # "Italy, France and Spain" (three countries), which is why it reported 176
 # hits file-wide and nobody could act on it. Proper nouns, single letters and
 # digits are excluded, so what is left is three adjectives or verbs in a row.
 ('tricolon',     re.compile(r'\b[a-z]{4,}, [a-z]{4,},? and [a-z]{4,}\b')),
 ('not just',     re.compile(r"\b(not just|isn't just|more than just)\b", re.I)),
 ('hedge',        re.compile(r"\b(it's worth noting|keep in mind|of course|essentially|ultimately|arguably)\b", re.I)),
 ('marketing',    re.compile(r"\b(iconic|legendary|revolutionary|game.chang\w+|unparalleled|timeless|masterful)\b", re.I)),
 ('rhetorical',   re.compile(r"^(But |And |So )", re.M)),
]
want = sys.argv[1] if len(sys.argv)>1 else None
tot=collections.Counter(); per=collections.Counter()
hits=collections.defaultdict(list)
for n,(pos,k) in enumerate(keys):
    end = keys[n+1][0] if n+1<len(keys) else pos+90000
    if want and k!=want: continue
    for m in QRE.finditer(seg[pos:end]):
        text = m.group(1) + ' ' + ' '.join(STR.findall(m.group(2))) + ' ' + (m.group(4) or '')
        for name,pat in TELLS:
            f=pat.findall(text)
            if f:
                tot[name]+=len(f); per[k]+=1
                hits[name].append((k, m.group(1)[:44], (f[0] if isinstance(f[0],str) else f[0][0])[:28]))
print('TELL COUNTS' + (f'  [{want}]' if want else '  [all packs]'))
for name,_ in TELLS:
    print(f'  {name:12} {tot[name]:>5}')
print()
for name,_ in TELLS:
    if not hits[name]: continue
    print(f'--- {name}')
    for k,q,f in hits[name][:5]: print(f'    {k:16} {q:46} {f}')

# ── Repetition: the fault that is only a fault in bulk ───────────────────────
# Added after on-device testing of the Bass pack. Every one of these reads fine
# in a single blurb. Seven of them in one pack is the cadence that gets called
# out as AI writing, and no per-question check can see it, because nothing is
# wrong with any single instance.
#
# The rate is per question. Measured across the file: the cleanest packs sit at
# 0.00 to 0.03, the median is about 0.04. Anything at or above WARN_RATE is a
# pack where one construction has become a habit.
TICS = [
 ('most of what/reason', re.compile(r'most of (?:what|the reason)', re.I)),
 ('which is why',        re.compile(r'which is why', re.I)),
 ('is where',            re.compile(r'\bis where\b', re.I)),
 ('comes from',          re.compile(r'comes? from', re.I)),
 ('turns up',            re.compile(r'turns? up', re.I)),
 ('built on/around',     re.compile(r'built (?:on|around|out of)', re.I)),
 ('the whole point',     re.compile(r'whole point', re.I)),
 ('runs on',             re.compile(r'\bruns on\b', re.I)),
 ('is all about',        re.compile(r'is all about', re.I)),
 ('to this day',         re.compile(r'to this day', re.I)),
 ('ever since',          re.compile(r'ever since', re.I)),
]
WARN_RATE = 0.08

ticcount = collections.defaultdict(collections.Counter)
qcount   = collections.Counter()
for n,(pos,k) in enumerate(keys):
    end = keys[n+1][0] if n+1<len(keys) else pos+90000
    if want and k!=want: continue
    block = seg[pos:end]
    qcount[k] = len(QRE.findall(block)) or 1
    for name,pat in TICS:
        c = len(pat.findall(block))
        if c: ticcount[k][name] = c

# Which packs have actually been rewritten. Everything else is queued for the
# same treatment the Bass pack got, so polishing its wording now is work that
# gets thrown away when the pack is rebuilt from its topic list. Read from the
# file rather than hardcoded, so this list cannot drift from what ships.
_mq = re.search(r"MQ_PACK_READY\s*=\s*\[(.*?)\]", H, re.S)
DONE = set(re.findall(r"'([a-z_]+)'", _mq.group(1))) if _mq else set()

print()
print('REPEATED CONSTRUCTIONS  (rate per question; warn at %.2f)' % WARN_RATE)
print('  Packs not in MQ_PACK_READY are marked "queued": they are awaiting a full')
print('  rewrite, so their wording is provisional and their rate is FYI only.')
rows = sorted(ticcount.items(), key=lambda kv: -sum(kv[1].values())/qcount[kv[0]])
flagged = 0
for k,c in rows:
    rate = sum(c.values())/qcount[k]
    done = k in DONE
    mark = ('  WARN' if rate >= WARN_RATE else '      ') if done else '  queue'
    if rate >= WARN_RATE and done: flagged += 1
    worst = ', '.join('%s x%d' % (n,v) for n,v in c.most_common(3))
    print('%s %-20s %5.2f   %s' % (mark, k, rate, worst))
if not rows:
    print('       none')
print('  %d rewritten pack(s) over the line  (of %d rewritten)' % (flagged, len(DONE)))
