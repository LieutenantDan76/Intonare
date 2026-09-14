"""Continuous audit of a pack draft held as JSON. Run after every edit.

Written after the Bass pack, where duplicate answers and cross-tier collisions
surfaced only at the final read. Holding the draft as data instead of prose
makes those checkable from the first stem onward.

REWRITTEN, and the reason matters. Every check in here was ENGLISH ONLY. Not
one reference to q_it, opts_it or fact_it existed in the file, so an Italian
fault could not fail the draft gate no matter how bad it was. It got found later
by livecheck at ship, or by Daniele, or by Linda. In v0.189 that was 12
answer-length tells where the draft check reported none, half of them Italian,
and 16 Italian drifts against the draft checker's 4.

Every lexical check now runs once per language with the right stop list. Running
the English stop list over Italian took the leaning-pair count from 12 to 60 on
the same pack, because "quale", "della" and "parte" counted as content words and
every stem matched every other one.

    python3 intonare_draft_check.py draft.json
    PACK_SUBJECTS="Lennon,McCartney,Harrison,Ringo" python3 intonare_draft_check.py draft.json

Draft rows put the answer at opts[0]. Shipped rows put it at opts[ans]. This
reads either.
"""
import collections
import itertools
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intonare_quiz_lib as lib

P = sys.argv[1] if len(sys.argv) > 1 else 'draft.json'

# Answers that are deliberately shared by two questions, as {answer: reason}.
# The path comes from the gate, which looks for allow_answers_<pack>.json.
# Lower-cased on load because the check compares lower-cased answers.
ANSWER_ALLOW = {}
_aa = os.environ.get('ANSWER_ALLOW', '')
if _aa and os.path.exists(_aa):
    ANSWER_ALLOW = {k.strip().lower(): v
                    for k, v in json.load(open(_aa, encoding='utf-8')).items()}
if not os.path.exists(P):
    sys.exit(P + ' not found')
rows = json.load(open(P, encoding='utf-8'))
if not rows:
    sys.exit('no rows in ' + P)

# Subjects the pack is ABOUT. A Bass pack naming one player four times is a
# concentration worth flagging; a Beatles pack naming Lennon four times is just
# a Beatles pack. Set this per pack, or the warning trains you to ignore it. The
# cost of getting it wrong is not a false alarm but a bad edit: the uncalibrated
# warning once pushed a Love Me Do question from Lennon playing harmonica to the
# flatter "which instrument opens Love Me Do". Reverted.
EXEMPT = {w.strip().lower() for w in os.environ.get('PACK_SUBJECTS', '').split(',')
          if w.strip()}

err, warn, note = [], [], []
LANGS = lib.langs(rows)


def side(row, lang):
    """One language's side. Draft rows have no ans and put the answer first."""
    q, opts, i, fact = lib.view(row, lang)
    if 'ans' not in row:
        i = 0
    return q, opts, i, fact


for lang in LANGS:
    tag = '' if lang == 'en' else ' [it]'

    seen = collections.Counter()
    for r in rows:
        q, o, i, f = side(r, lang)
        if o and 0 <= i < len(o):
            seen[o[i].strip().lower()] += 1
    for a, n in seen.items():
        if n > 1:
            # Two questions sharing an answer is a fault in English. In the
            # other language it is often correct: bass 16 answers "the double
            # bass" and bass 89 answers "the upright bass", two English terms
            # for one instrument, and Italian has one word for both. Worth
            # reading, because an Italian round could deal both, and not worth
            # failing a gate over.
            #
            # It can also be correct in English, when one word names two
            # different things. The 80s pack answers "Thriller" twice: once for
            # the album that outsold everything, once for the video John Landis
            # directed. Those are two subjects, not one question asked twice.
            # An allowed answer still prints, because the pack still deals both
            # in a round and that is worth seeing; it just stops failing.
            if a in ANSWER_ALLOW:
                note.append(f'answer used {n}x{tag}: {a}  '
                            f'[allowed: {ANSWER_ALLOW[a]}]')
            else:
                (err if lang == 'en' else warn).append(
                    f'answer used {n}x{tag}: {a}')

    for idx, r in enumerate(rows, 1):
        q, o, i, f = side(r, lang)
        if not q:
            err.append(f'{idx}: no stem{tag}')
            continue
        if o and len(o) > 1:
            gap, level = lib.length_tell(o, i)
            if level == 'error':
                err.append(f'{idx}: answer {gap} chars longer than any '
                           f'distractor{tag}: {q[:44]}')
            elif level == 'warn':
                warn.append(f'{idx}: answer {gap} chars longer{tag}: {q[:44]}')
            if len({x.strip().lower() for x in o}) != len(o):
                err.append(f'{idx}: repeated option{tag}: {q[:44]}')
        if o and any(x.strip() != x for x in o):
            err.append(f'{idx}: option has stray whitespace{tag}: {q[:44]}')
        # Word boundary and a minimum length. A substring test fired on four
        # approved Bass diagram questions whose answer is a single note name:
        # "C" is inside "Which", "D" is inside "sounD", "E" is everywhere.
        if o and 0 <= i < len(o) and len(o[i]) > 3 and \
                re.search(r'\b' + re.escape(o[i]) + r'\b', q, re.I):
            err.append(f'{idx}: stem contains its answer{tag}: {q[:48]}')

    # Repeated stem openings, advisory. If varying an opening costs a natural
    # sentence, keep the sentence and vary what is being ASKED instead.
    shapes = collections.Counter(' '.join(side(r, lang)[0].lower().split()[:4])
                                 for r in rows)
    for s, n in shapes.items():
        if n > 3:
            warn.append(f'{n} stems open "{s}..."{tag}')

subj = collections.Counter()
for r in rows:
    body = ' '.join(r.get('q', '').split()[2:])
    for w in re.findall(r"\b[A-Z][a-z']+(?: [A-Z][a-z']+)?\b", body):
        if w.lower() in EXEMPT:
            continue
        if w not in ('Which', 'What', 'Who', 'Where', 'When', 'Why', 'The',
                     'In', 'A', 'An'):
            subj[w] += 1
for s, n in subj.items():
    if n > 3:
        warn.append(f'subject named in {n} stems: {s}   '
                    f'(set PACK_SUBJECTS if that is what the pack is about)')

# ── Stem freeze ──────────────────────────────────────────────────────────────
# The omega read keeps finding options that stopped answering a rewritten stem:
# three of them on the Bass pack, every audit passed. That is bookkeeping, not
# taste, so it can be a gate that never cries wolf. Seal a row once you have
# read it whole; change either stem afterward and it goes stale.
stale, unsealed = lib.stale_rows(rows)
for i in stale:
    err.append(f'{i}: STEM CHANGED since the options and blurb were approved. '
               f'Read the whole question again, then re-seal.')

tier = collections.Counter(r.get('d', 0) for r in rows)
print(f'{len(rows)} rows | tiers {tier[1]}/{tier[2]}/{tier[3]} | '
      f'languages {"+".join(LANGS)}')
if tier[0]:
    print(f'  {tier[0]} row(s) with no difficulty tag')
print(f'  errors {len(err)} | warnings {len(warn)}')
for e in err:
    print('  ERR  ' + e)
for w in warn:
    print('  warn ' + w)
for w in note:
    print('  note ' + w)
if unsealed:
    print(f'  {len(unsealed)} of {len(rows)} rows unsealed. Normal while '
          f'writing, a fault at ship. Seal with intonare_pack_seal.py')

# ── Questions that lean on each other ────────────────────────────────────────
# A pack can hold two questions on one subject where one hands over the other's
# answer without either being a duplicate. The medium tier asked what artificial
# double tracking is; the hard tier asked who built the machine that does it.
# Three shared content words is a low bar and throws false positives, which is
# the right trade: this is a prompt to read the pair, not a verdict.
for lang in LANGS:
    lean = []
    for x, y in itertools.combinations(range(len(rows)), 2):
        qx, qy = side(rows[x], lang)[0], side(rows[y], lang)[0]
        kx, ky = lib.content_words(qx, lang), lib.content_words(qy, lang)
        if kx and ky and len(kx & ky) >= 3:
            lean.append((x + 1, y + 1, qx, qy, sorted(kx & ky)))
    if lean:
        label = 'pair(s)' if lang == 'en' else 'Italian pair(s)'
        print(f'  {len(lean)} {label} to read together (one may answer the other):')
        for a, b, x, y, s in lean[:12]:
            print(f'    {s}')
            print(f'      [{a:3}] {x[:66]}')
            print(f'      [{b:3}] {y[:66]}')
        if len(lean) > 12:
            print(f'    ... and {len(lean) - 12} more')

# ── Definition questions ─────────────────────────────────────────────────────
# "What is X?" is a glossary entry, not a question about music. Shipped packs
# measure around 5%; packs awaiting rewrite run 85% and up.
#
# Narrowed once already. Daniele rewrote 20 of 25 stems in guitar_technique
# TOWARD the plain question form, because a beginner pack should ask directly.
# Avoiding "What is X" so hard that stems become riddles is worse than the
# glossary it replaced: "Your first finger has to lie flat across every string.
# What are you playing?" is a puzzle. The fault is the BARE glossary entry, with
# no context and nothing to reason from.
defn = [r['q'] for r in rows
        if re.match(r"^(What|Which) (is|are) (a|an|the) [\w\s-]{1,24}\?$",
                    r.get('q', '').strip(), re.I)]
rate = len(defn) / len(rows)
print(f'  bare glossary stems: {len(defn)} of {len(rows)} = {rate*100:.0f}%  '
      f'(shipped ~5%, unrewritten 85%+)')
if rate > 0.15:
    for q in defn[:14]:
        print('    ' + q[:74])

sys.exit(1 if err else 0)
