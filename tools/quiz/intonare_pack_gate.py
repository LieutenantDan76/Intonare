"""One gate for a pack. Runs every check in the order faults appear.

Built because every review round found something an earlier check would have
caught for free. The spec's rule is "write, run everything, fix, THEN show", and
this makes that one command.

REWRITTEN. The old version called check.py, blurbcheck.py and itcheck.py, short
names that had to be copied into the working directory by hand, so the gate
worked in the session that wrote it and nowhere else. It also ran the English
side only, which is how twelve answer-length tells reached ship in v0.189 with
half of them Italian.

    python3 intonare_pack_gate.py draft.json --subjects "Lennon,McCartney"
    python3 intonare_pack_gate.py --pack bass

Takes a draft JSON or an installed pack, and runs the same checks over both, so
a pack that passes while you write it passes once it is in the file.

Exit code is the number of stages that reported an error, so it can gate a
script. The last stage is the part no tool does, and it is printed every time
because it is the part that gets skipped.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intonare_quiz_lib as lib

argv = sys.argv[1:]
if '--subjects' in argv:
    os.environ['PACK_SUBJECTS'] = argv[argv.index('--subjects') + 1]
os.environ.setdefault('PACK_SUBJECTS', '')

if '--pack' in argv:
    pack_id = argv[argv.index('--pack') + 1]
    rows = lib.as_draft(lib.rows(pack_id))
    src = os.path.join('/tmp', f'gate_{pack_id}.json')
    json.dump(rows, open(src, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    label = pack_id
else:
    args = [a for a in argv if not a.startswith('-')]
    src = args[0] if args else 'draft.json'
    if not os.path.exists(src):
        sys.exit(f'{src} not found. Pass a draft JSON, or --pack <id>.')
    rows = json.load(open(src, encoding='utf-8'))
    label = os.path.basename(src)

if not rows:
    # advanced_theory authors nothing: its questions are built at runtime by the
    # generators. A pack with no authored rows is not a failure, it is a pack
    # with nothing for this gate to read.
    print(f'{label}: no authored rows. Generator-only packs are checked by '
          f'their own harness, not here.')
    sys.exit(0)

HAS_IT = lib.has_italian(rows)
HAS_BLURBS = any(r.get('fact') for r in rows)
failed = []


def stage(n):
    print('\n' + '\u2500' * 62)
    print('  ' + n)
    print('\u2500' * 62)


def run(script, label_, extra=()):
    stage(label_)
    r = subprocess.run([sys.executable, os.path.join(HERE, script), src, *extra],
                       capture_output=True, text=True, env=os.environ)
    out = (r.stdout.rstrip() or r.stderr.rstrip())
    print(out)
    if r.returncode:
        failed.append(label_.split('.')[0])


print(f'PACK GATE  [{label}]  {len(rows)} rows  '
      f'languages {"en+it" if HAS_IT else "en"}')
if os.environ['PACK_SUBJECTS']:
    print(f'  PACK_SUBJECTS = {os.environ["PACK_SUBJECTS"]}')
else:
    print('  PACK_SUBJECTS is empty. Set it to what the pack is ABOUT, or the')
    print('  subject warning fires on the pack doing its job. Getting this')
    print('  wrong costs a bad edit, not a false alarm.')

# A pack may share one answer between two questions on purpose, when the word
# names two different things. That lives in allow_answers_<pack>.json next to
# this script, as {answer: reason}, and it downgrades the error to a note rather
# than hiding it: a round can still deal both, which is worth seeing.
_aa = os.path.join(HERE, 'allow_answers_' + str(label).lower() + '.json')
if os.path.exists(_aa):
    os.environ['ANSWER_ALLOW'] = _aa
    print(f'  using answer allowlist {os.path.basename(_aa)}')

run('intonare_draft_check.py', '1. STRUCTURE  answers, giveaways, stem seals, leaning pairs')

if HAS_BLURBS:
    run('intonare_blurb_draft_check.py', '2. BLURBS  register, run-ons, threads, omega leaks')
    if HAS_IT:
        run('intonare_blurb_draft_check.py',
            '2b. BLURBS, Italian  the side that used to go unread',
            ('--lang', 'it'))

if HAS_IT:
    run('intonare_italian_check.py', '3. ITALIAN  coverage, drift, English leaking through')

# ── Register against the measured numbers ───────────────────────────────────
stage('4. REGISTER against Daniele\'s edit-pass numbers')
F = [r['fact'] for r in rows if r.get('fact')]
if not F:
    print('  no blurbs yet')
else:
    import re
    import collections
    joined = ' '.join(F)

    def per(p, flags=0):
        return len(re.findall(p, joined, flags)) / len(F)

    m = {
        'contractions': (per(r"\b\w+['\u2019](s|ll|re|ve|t)\b"), 0.42),
        'exclamations': (sum(1 for f in F if '!' in f) / len(F), 0.19),
        'quoted': (per(r'["\u201c\u201d]') / 2, 0.54),
        'only/just': (per(r'\b(only|just)\b', re.I), 0.12),
        'which-join': (per(r'\bwhich\b', re.I), 0.12),
    }
    for k, (got, want) in m.items():
        off = '' if abs(got - want) <= max(0.15, want * 0.6) else '   <-- off'
        print(f'  {k:14} {got:.2f}   his {want:.2f}{off}')
    sc = [len(lib.sentences(f)) for f in F]
    print(f'  sentences/blurb  {dict(sorted(collections.Counter(sc).items()))}'
          f'   (Beatles 28 one / 61 two)')
    print('\n  These are a direction, not a target. The gap between reference-book')
    print('  prose and a person telling somebody a good bit is small words:')
    print('  contractions, a quoted phrase, an occasional "only".')

# ── The part no tool does ───────────────────────────────────────────────────
stage('5. NOT AUTOMATED  do these before showing anyone')
print('  Three detectors for this list were built during the Bass pack and')
print('  thrown away. One fired on 7 of 42 approved blurbs including Daniele\'s')
print('  own rewrite; one fired on 51 of 106 and caught 1 of the 3 known bad.')
print('  A check that fires on approved material is worse than no check,')
print('  because it teaches you to ignore the output. So these stay a read.\n')
for s in [
    'read every blurb ALONE, not in a block',
    'read each closing sentence against the one before it: does it ANSWER '
    'something that sentence raised, or is it just the next true fact?',
    'check no blurb carries a verdict where it should carry a fact',
    'confirm every superlative, first and attribution. Bare years come back '
    'clean every time; those three never do',
    'read the options against the stem for a SECOND correct answer. Can you '
    'name another person the stem also describes?',
    'read the stem aloud. If you stumble, the player will',
    'ask of each: would the player repeat this answer to somebody else?',
]:
    print('  [ ] ' + s)

stale, unsealed = lib.stale_rows(rows)
print(f'\n  Seals: {len(rows) - len(unsealed) - len(stale)} holding, '
      f'{len(stale)} stale, {len(unsealed)} never sealed.')
print('  Seal a tier once you have read it. The seal is a record that somebody')
print('  read the row whole, so stamping the pack at the end records nothing.')

print('\n' + '=' * 62)
if failed:
    print(f'  {len(failed)} stage(s) reported errors: ' + ', '.join(failed))
else:
    print('  every automated stage clean. Stage 5 is still yours.')
print('=' * 62)
sys.exit(len(failed))
