#!/usr/bin/env python3
"""
intonare_pack_audit.py — checks a quiz pack against every criterion in
QUIZ_SPEC.md section 1 that a machine can actually hold.

Why this exists: the voice audit caught blurb mechanics, and everything else was
being caught by Daniele reading drafts. Over one pack that meant eleven faults
found by eye across five passes, six of them countable and therefore avoidable.
Each check below fired on a real fault in the Seventies pack, and the comment on
each says which one, so nothing here is a rule I invented for tidiness.

    python3 intonare_pack_audit.py pack.json [--voice] [--cap 2]

Input is a JSON list of objects:
    {d, q, q_it, opts, opts_it, ans?, fact, fact_it, loc?}
`ans` may be omitted if the correct answer is written first, which is the
authoring convention; pass --answered if `ans` is already an index.

ERROR fails the run. WARN is for things that are sometimes right.
"""

import sys, os, re, json, argparse, unicodedata
from collections import Counter, defaultdict

# ── thresholds, each traceable to a real fault ──────────────────────────────
# The one answer-length rule, shared with the draft check so a pack cannot pass
# one stage and fail the other. It used to be 12 here, 2.0x in the draft check
# and 1.6x in the padding pass: same fault, three verdicts, all landing on
# Daniele. Measured over 561 questions in both languages across the six authored
# packs, a gap over 15 is clean on the four packs he read question by question.
# See intonare_quiz_lib.LEN_GAP_ERROR for the table.
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import intonare_quiz_lib as _lib
LEN_GAP        = _lib.LEN_GAP_ERROR   # answer longer than the next longest by this many chars.
                      # Caught the 42-vs-27 appoggiatura answer in Theory.
STEM_SHARE     = 0.60 # share of the stem's distinctive words reappearing in the
                      # blurb. Caught the Baglioni blurb restating its own stem.
SUBJECT_CAP    = 3    # same proper-noun subject across a pack. A decades pack
                      # wants --cap 2, since variety is its whole point; a pack
                      # about guitarists legitimately returns to Hendrix, and
                      # the approved Guitar Gods does so three times.
SUBJECT_ORDINARY = 0.25  # a capitalized word that also appears lowercase this
                      # often, relative to its capitalized uses, is an ordinary
                      # word that happened to start a field. See the note in
                      # audit() for the measurement.
SUBJECT_MIN_OV = 2    # shared proper nouns before two questions count as
                      # the same subject.
TIER_TOLERANCE = 0.12 # drift allowed from 40/40/20.

STOP = {'which','what','where','when','who','whose','why','how','the','and','for',
        'from','with','that','this','they','their','there','then','than','into',
        'over','after','before','about','song','band','album','film','movie',
        'year','italy','italian','america','american','english','british'}

CROSS_REF = [
    'that soundtrack', 'that album', 'that film', 'that song', 'the same band',
    'this pack', 'earlier question', 'as mentioned', 'that first', 'the above',
]

# A question tacked onto the end of a statement. Not a length problem: the Bass
# stems match the approved pack on median length exactly. It is word order.
INVERTED = re.compile(
    r'(?:does what|doing what|is called what|of what|tuned how|, how|'
    r'for which reason|and what)\s*\?\s*$', re.I)
INVERTED_IT = re.compile(
    r'(?:facendo cosa|cosa fa|si chiama cosa|di cosa|accordate come|, come|'
    r'per quale motivo)\s*\?\s*$', re.I)

def words(s):
    return re.findall(r"[\w'\u2019-]+", s or '')

def content(s):
    """Distinctive words: long enough to matter, not a question word."""
    return {w.lower() for w in re.findall(r"[A-Za-z\u00C0-\u017F]{5,}", s or '')
            if w.lower() not in STOP}

def propers(s):
    """Capitalized words that are not sentence-initial, as a subject proxy."""
    out = set()
    for sent in re.split(r'(?<=[.!?])\s+', s or ''):
        toks = re.findall(r"[A-Z][A-Za-z\u00C0-\u017F']{2,}", sent)
        out |= {t.lower() for t in toks[1:]} if len(toks) > 1 else set()
        if toks:
            out.add(toks[0].lower())
    # A capitalized word is not automatically a subject. Months, days,
    # nationalities and the ordinary nouns inside titles are furniture: World Cup
    # and New York and Saturday Night were being counted as recurring subjects.
    light = {
        'which','what','where','when','who','whose','why','how','the','and','for',
        'january','february','march','april','may','june','july','august',
        'september','october','november','december',
        'monday','tuesday','wednesday','thursday','friday','saturday','sunday',
        'american','americans','british','english','italian','italians','german',
        'french','swedish','japanese','jamaican','romanian','australian',
        'world','cup','new','york','night','day','special','star','wars','picture',
        'show','song','album','film','movie','band','group','best','first','last',
        'north','south','east','west','city','records','company','television',
        'radio','magazine','national','international','festival','olympics',
    }
    return {w for w in out if w not in light}

def has_digit(s):
    return bool(re.search(r'\d', s or ''))

def roman_or_num(s):
    return bool(re.search(r'\d|\b[IVXLC]{1,4}\b', s or ''))


def audit(rows, cap=SUBJECT_CAP, answered=False):
    errs, warns = [], []
    # Words used by more than a seventh of the pack are its furniture, not its
    # subjects: guitar in a guitar pack, sound in a pack about amplifiers.
    # Per language: an English common-word list cannot tell you that chitarrista
    # is furniture in the Italian half.
    df, df_it = Counter(), Counter()
    for x in rows:
        df.update(content(f"{x.get('q','')} {' '.join(x.get('opts') or [])} {x.get('fact','')}"))
        df_it.update(content(f"{x.get('q_it','')} {' '.join(x.get('opts_it') or [])} {x.get('fact_it','')}"))
    thresh = max(3, len(rows) / 7)
    common = {w for w, n in df.items() if n > thresh}
    common_it = {w for w, n in df_it.items() if n > thresh}
    def E(i, m): errs.append((i, m))
    def W(i, m): warns.append((i, m))

    # ── per question ────────────────────────────────────────────────────────
    for i, x in enumerate(rows, 1):
        ans_i = x.get('ans', 0) if answered else 0
        opts, opts_it = x.get('opts') or [], x.get('opts_it') or []

        # every question tagged
        if x.get('d') not in (1, 2, 3):
            E(i, f"difficulty is {x.get('d')!r}, must be 1, 2 or 3")

        # both languages present
        for k in ('q', 'q_it', 'fact', 'fact_it'):
            if not (x.get(k) or '').strip():
                E(i, f'missing {k}')
        for k, o in (('opts', opts), ('opts_it', opts_it)):
            if len(o) != 4:
                E(i, f'{k} has {len(o)} entries, needs 4')
            elif len(set(o)) != 4:
                E(i, f'{k} has a repeated option')
        if len(opts) != 4 or len(opts_it) != 4:
            continue
        ans, ans_it = opts[ans_i], opts_it[ans_i]
        rest = [o for j, o in enumerate(opts) if j != ans_i]
        rest_it = [o for j, o in enumerate(opts_it) if j != ans_i]

        # ── shape tells: the answer must not stand out ──────────────────────
        # Caught in Theory (42 vs 27) and again in the Star Wars box question,
        # where only the ITALIAN answer was the long one.
        if len(ans) - max(len(o) for o in rest) > LEN_GAP:
            E(i, f'answer is {len(ans)} chars against {max(len(o) for o in rest)}; '
                 'findable by length')
        if len(ans_it) - max(len(o) for o in rest_it) > LEN_GAP:
            E(i, 'Italian answer is findable by length even though the English is not')
        # Caught the Atari question, where 2600 was the only numeral on screen.
        if has_digit(ans) and not any(has_digit(o) for o in rest):
            E(i, 'answer is the only option containing a number')
        if not has_digit(ans) and all(has_digit(o) for o in rest):
            E(i, 'answer is the only option WITHOUT a number')
        # a lone multi-word answer among single words, or the reverse
        wc = [len(words(o)) for o in opts]
        if wc[ans_i] >= 4 and all(w <= 2 for j, w in enumerate(wc) if j != ans_i):
            W(i, 'answer is the only phrase among single-word options')

        # ── stem must not contain the answer ────────────────────────────────
        # Caught the Guccini locomotive stem and the Celentano title.
        def shares(a_set, b_set):
            # exact, or a shared six-character prefix: locomotive/locomotiva,
            # inversion/inversione, referendum/referendum.
            out = set()
            for w in a_set:
                for v in b_set:
                    if w == v or (len(w) >= 6 and len(v) >= 6 and w[:6] == v[:6]):
                        out.add(w)
            return out
        sq, sa = content(x.get('q')), content(ans)
        leak = {w for w in shares(sa, sq)
                if w not in common and not any(w[:6] in o.lower() for o in rest)}
        if leak:
            E(i, f'stem shares {sorted(leak)} with the answer and no distractor')
        sq_it, sa_it = content(x.get('q_it')), content(ans_it)
        leak_it = {w for w in shares(sa_it, sq_it)
                   if not any(w[:6] in o.lower() for o in rest_it)}
        leak_it = {w for w in leak_it if w not in common_it}
        if leak_it:
            E(i, f'Italian stem shares {sorted(leak_it)} with the Italian answer')

        # ── the inverted stem ──────────────────────────────────────────────
        # Added after the Bass pack. Five stems stated a fact and then hung the
        # question off the end: "The Bass VI has six strings, tuned how?",
        # "...is called what?", "...by doing what?". Every one is grammatical,
        # every one passed every other check, and nobody speaks like that. The
        # 90 approved Guitar Gods stems contain none of this shape.
        if INVERTED.search((x.get('q') or '').strip()):
            W(i, 'stem states a fact and hangs the question off the end; '
                 'ask it forwards instead')
        if INVERTED_IT.search((x.get('q_it') or '').strip()):
            W(i, 'Italian stem hangs the question off the end')

        # ── blurb must add something ────────────────────────────────────────
        # Caught the Baglioni blurb, which restated its own stem.
        sw, bw = content(x.get('q')), content(x.get('fact'))
        new = bw - sw - content(ans)
        if sw and len(sw & bw) / len(sw) > STEM_SHARE and len(new) < 4:
            E(i, f'blurb repeats the stem and adds only {len(new)} new ideas')

        # ── no question may refer to another ────────────────────────────────
        # Caught "that soundtrack", which is meaningless once a round shuffles.
        for phrase in CROSS_REF:
            if phrase in (x.get('q') or '').lower():
                E(i, f'stem refers to another question: "{phrase}"')
            if phrase in (x.get('fact') or '').lower():
                W(i, f'blurb refers to another question: "{phrase}"')

        # ── locale ──────────────────────────────────────────────────────────
        if x.get('loc') not in (None, 'en', 'it'):
            E(i, f"loc is {x['loc']!r}, must be absent, 'en' or 'it'")

    # ── across the pack ─────────────────────────────────────────────────────
    # Subject cap. Caught three Sanremo questions, three Ali, and the two
    # outright duplicates (the 1970 semifinal, and Life of Brian twice).
    def _ans(x):
        o = x.get('opts') or ['']
        k = x.get('ans', 0) if answered else 0
        return o[k] if k < len(o) else ''
    subj = [propers(f"{x.get('q','')} {_ans(x)}") for x in rows]

    # A capitalized word that ALSO appears lowercase across the pack is an
    # ordinary word that happened to start a field, not a subject. "Play loudly"
    # as an option made "play" a recurring subject of the theory pack, and
    # "bass" a recurring subject of the Bass pack. Both are the tool being
    # wrong, and both cost a look on every run.
    #
    # Measured over the six authored packs, lowercase uses against capitalized:
    # bass 5.90, life 0.80, love 0.40, play 0.32, road 0.30, and then a gap down
    # to apple 0.08 and 0.00 for Lennon, Harrison, Ringo, Beatles, Jimmy, Page.
    # The line goes at 0.25, in the middle of the gap.
    #
    # Apple is why this is a ratio and not a plain "appears lowercase" test.
    # Blurb 77 has a green apple in a Magritte painting, and Apple is still a
    # subject of that pack twelve times over.
    corpus = ' '.join(' '.join([x.get('q', '')] + list(x.get('opts') or [])
                               + [x.get('fact') or '']) for x in rows)
    ordinary = set()
    for w in {w for s_ in subj for w in s_}:
        pat = r'\b' + re.escape(w) + r'\b'
        lo = len(re.findall(pat, corpus))
        hi = len(re.findall(pat, corpus, re.I)) - lo
        if hi and lo / hi >= SUBJECT_ORDINARY:
            ordinary.add(w)
    subj = [s_ - ordinary for s_ in subj]

    # Count every proper noun across the pack. Anything over the cap is a subject
    # appearing too often, however few words its questions happen to share.
    freq = defaultdict(list)
    for i, s_ in enumerate(subj, 1):
        for w in s_:
            freq[w].append(i)
    for w, where in sorted(freq.items()):
        if len(where) > cap:
            errs.append((0, f'subject "{w}" appears in {len(where)} questions '
                            f'{where}, cap is {cap}'))
    groups = defaultdict(list)
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            ov = subj[i] & subj[j]
            if len(ov) >= SUBJECT_MIN_OV:
                groups[frozenset(ov)].append((i + 1, j + 1))
    seen_pairs = Counter()
    for ov, pairs in groups.items():
        members = sorted({n for p in pairs for n in p})
        if len(members) > cap:
            errs.append((0, f'{len(members)} questions share subject {sorted(ov)}: '
                            f'{members} (cap is {cap})'))
        else:
            for p in pairs:
                seen_pairs[p] += 1
    for (a, b), _ in seen_pairs.items():
        warns.append((0, f'questions {a} and {b} share a subject; allowed at {cap} '
                         'but worth a look'))

    # Same answer, twice. The 1970 semifinal was asked twice from different
    # angles and sat inside the cap, so nothing fired.
    norm = lambda t: re.sub(r'[^a-z0-9]', '', (t or '').lower())
    byans = defaultdict(list)
    for i, x in enumerate(rows, 1):
        o = x.get('opts') or ['']
        k = x.get('ans', 0) if answered else 0
        if k < len(o) and o[k]:
            byans[norm(o[k])].append(i)
    for a_, where in byans.items():
        if len(where) > 1:
            errs.append((0, f'questions {where} share the same answer'))

    # A blurb must not answer another question.
    for i, x in enumerate(rows, 1):
        bl = content(x.get('fact'))
        for j, y in enumerate(rows, 1):
            if i == j:
                continue
            ya = content(_ans(y))
            if ya and ya <= bl and len(ya) >= 2:
                warns.append((i, f'blurb names the whole answer to question {j}; '
                                 'fine in passing, a giveaway if that is the point'))

    # Tier split.
    c = Counter(x.get('d') for x in rows)
    n = max(1, len(rows))
    for tier, want in ((1, .40), (2, .40), (3, .20)):
        got = c[tier] / n
        if abs(got - want) > TIER_TOLERANCE:
            warns.append((0, f'tier {tier} is {got:.0%} of the pack, target {want:.0%}'))

    # Answer position spread, when positions are already assigned.
    if answered:
        pos = Counter(x.get('ans', 0) for x in rows)
        if pos and max(pos.values()) - min(pos.values()) > max(2, len(rows) * .12):
            warns.append((0, f'answer positions uneven: {dict(sorted(pos.items()))}'))

    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--cap', type=int, default=SUBJECT_CAP)
    ap.add_argument('--answered', action='store_true')
    ap.add_argument('--allow', help='JSON allowlist; a finding containing one of '
                                    'its substrings is reported as accepted rather '
                                    'than failing. A LIST of substrings works, and '
                                    'an OBJECT of substring -> reason is better, '
                                    'because an entry with no reason rots. If this '
                                    'is left off, allow_<name>.json next to this '
                                    'script is used when it exists.')
    a = ap.parse_args()
    rows = json.load(open(a.path, encoding='utf-8'))
    errs, warns = audit(rows, a.cap, a.answered)

    # Every pack that legitimately trips the subject cap needs its own file, or
    # the cap gets ignored wholesale. Running the beatles pack without one gave
    # 15 errors, every one of them the pack doing its job, which is how a real
    # error hides. So the file is found automatically from the pack name.
    allow_path = a.allow
    if not allow_path:
        here = os.path.dirname(os.path.abspath(__file__))
        guess = os.path.join(
            here, 'allow_' + os.path.basename(a.path).rsplit('.', 1)[0] + '.json')
        if os.path.exists(guess):
            allow_path = guess
            print(f'  using allowlist {os.path.basename(guess)}')
    allow = json.load(open(allow_path, encoding='utf-8')) if allow_path else {}
    reasons = allow if isinstance(allow, dict) else {s: '' for s in allow}
    if reasons:
        keep, moved = [], []
        for i, m in errs:
            hit = next((s for s in reasons if s in m), None)
            (moved if hit else keep).append((i, m, hit))
        errs = [(i, m) for i, m, _ in keep]
        for i, m, hit in moved:
            why = reasons.get(hit) or 'no reason recorded'
            warns.append((i, f'accepted ({why}): {m}'))
    print('=' * 72)
    print(f'PACK AUDIT  [{a.path}]  {len(rows)} questions')
    print('=' * 72)
    for i, m in errs:
        print(f'  {("Q%d" % i) if i else "pack":>5}  ERROR  {m}')
    for i, m in warns:
        print(f'  {("Q%d" % i) if i else "pack":>5}  warn   {m}')
    print('-' * 72)
    print(f'  {len(errs)} errors, {len(warns)} warnings')
    print('=' * 72)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
