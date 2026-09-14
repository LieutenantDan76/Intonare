#!/usr/bin/env python3
"""
intonare_blurb_voice.py — checks quiz blurbs against the rules in QUIZ_SPEC.md
section 2b, with thresholds measured from the SHIPPED Guitar Gods pack rather
than invented.

Why this exists: the blurb rules were being applied from memory and drifting
every pass. Two failures kept recurring. Blurbs opened with a bare pronoun,
which the spec forbids outright and which Guitar Gods never does once in sixty.
And the drafts ran about two thirds the approved length, in two short balanced
sentences, which is the exact "fragment" shape the spec records as tried,
rejected and corrected once already.

Second reference set, the 42 approved Bass easy-tier blurbs, August 2026. They
run tighter than Guitar Gods and the thresholds below still hold:
    words           30 min, 40 median, 47 max
    verdict closers 0, after three were cut by hand; see VERDICT_STRONG

Measured from the 60 approved Guitar Gods blurbs:
    words           28 min, 39 median, 58 max
    sentences       27 of 60 are one sentence, 32 are two, 1 is three
    two-sentence    first sentence is the longer one in 29 of 32
                    median long:short ratio 2.13, 10th percentile 1.24
    pronoun opens   0 of 60
    participles     13 of 60 carry a ", <verb>ing" clause

Usage:
    python3 intonare_blurb_voice.py <file.json | file.html> [--pack NAME]
    JSON input may be a list of strings or a list of {fact, fact_it} objects.

Exit code is 1 if any ERROR fires. WARN never fails the run; it marks things a
human should look at, because some of them are legitimate in the right blurb.
"""

import sys, re, json, statistics, unicodedata

# ── thresholds, all derived above ───────────────────────────────────────────
WORD_MIN, WORD_MAX = 24, 60          # spec says 24-40; shipped runs to 58, so
                                     # the ceiling follows the shipped pack and
                                     # the floor follows the spec
WORD_SOFT_LOW = 28                   # below the shipped minimum: warn
RATIO_MIN = 1.24                     # 10th percentile of approved two-sentence
BALANCED_SHORT_TOTAL = 34            # a balanced PAIR only fails when both are
                                     # short; the approved pack has balanced
                                     # pairs at 44, 41, 47 and 58 words total

PRONOUN_OPEN = re.compile(r'^\s*(He|She|It|They|His|Her|Its|Their|Them|Him)\b')
# "not a clause first" — a blurb opening on a subordinator delays the subject
SUBORDINATOR_OPEN = re.compile(
    r'^\s*(Because|When|After|Before|Although|Though|While|Since|If|As|Having|'
    r'Despite|During|Once|Until|Unless|Whereas|Given)\b')

BRITISH = {
    'colour':'color','colours':'colors','favourite':'favorite','honour':'honor',
    'labour':'labor','neighbour':'neighbor','rumour':'rumor','humour':'humor',
    'behaviour':'behavior','flavour':'flavor','armour':'armor','harbour':'harbor',
    'centre':'center','centres':'centers','theatre':'theater','metre':'meter',
    'litre':'liter','fibre':'fiber','sombre':'somber',
    'realise':'realize','realised':'realized','organise':'organize',
    'organised':'organized','recognise':'recognize','recognised':'recognized',
    'apologise':'apologize','analyse':'analyze','analysed':'analyzed',
    'criticise':'criticize','memorise':'memorize','emphasise':'emphasize',
    'specialise':'specialize','minimise':'minimize','maximise':'maximize',
    'travelled':'traveled','travelling':'traveling','cancelled':'canceled',
    'labelled':'labeled','modelling':'modeling','marvellous':'marvelous',
    'defence':'defense','offence':'offense','licence':'license','practise':'practice',
    'grey':'gray','plough':'plow','programme':'program','programmes':'programs',
    'aluminium':'aluminum','moustache':'mustache','pyjamas':'pajamas',
    'storey':'story','tyre':'tire','kerb':'curb','aeroplane':'airplane',
    'maths':'math','sceptical':'skeptical','cheque':'check','draught':'draft',
    'jewellery':'jewelry','woollen':'woolen','enrol':'enroll','fulfil':'fulfill',
    'instalment':'installment','skilful':'skillful','wilful':'willful',
}
# vocabulary, not spelling: reads as British even when spelled correctly
BRITISH_USAGE = {
    'queue':'line','queued':'lined up','queueing':'lining up','queuing':'lining up',
    'queues':'lines','trousers':'pants','lorry':'truck','pavement':'sidewalk',
    'petrol':'gas','football':'soccer','autumn':'fall',
    'lift':'elevator','biscuit':'cookie','sweets':'candy',
    'rubbish':'trash','telly':'TV',
    'whilst':'while','amongst':'among','learnt':'learned','spelt':'spelled',
    'round the block':'around the block','at the weekend':'on the weekend',
    'in hospital':'in the hospital','sat the':'took the',
}
MARKETING = {'iconic','legendary','revolutionary','timeless','masterful',
             'game-changing','groundbreaking','unforgettable','seminal',
             'quintessential','definitive','pioneering','visionary','stunning',
             'breathtaking','beloved','celebrated','renowned','acclaimed'}
EMPTY_CLOSERS = [
    'and the rest is history', 'the rest is history', 'to this day it remains',
    'never looked back', 'changed everything', 'changed music forever',
    'stood the test of time', 'goes without saying', 'needless to say',
]
HEDGE_OPEN = re.compile(r'^\s*(Interestingly|Notably|Remarkably|Amazingly|'
                        r'Surprisingly|Perhaps|Arguably|Of course|In fact|Indeed)\b',
                        re.I)
GLOSS = [
    'which is why it matters', 'which has since', 'a decision that',
    'a trade that', 'which would go on to', 'proving that', 'showing that',
    'cementing', 'solidifying', 'in what would become',
]
# ── the verdict closer ─────────────────────────────────────────────────────
# Added after the Bass easy tier. Daniele cut three closing sentences that no
# existing check saw, because none of them was empty in the EMPTY_CLOSERS sense
# and all of them were true:
#     "Anybody chasing a Motown thud still buys them."
#     "They kept booking gigs anyway."
#     "Learning the two together is worth more than learning either alone."
# What they share is that each states a VERDICT on the fact just given rather
# than another fact. A blurb ends on information or it ends.
# Two strengths, because one list caught real facts. "Nobody ever wrote the part
# down" and "Berry's publisher sued him over the lyrics anyway" are both facts
# and both fired on the first version.
VERDICT_STRONG = re.compile(
    r'\b(worth more than|either alone|says it all|and nothing more|'
    r'not for nothing|still buys?|still use|still worth)\b', re.I)
VERDICT_WEAK = re.compile(r'\banyway\b', re.I)
VERDICT_OPEN = re.compile(
    r'^\s*(Anybody|Anyone|Everybody|Everyone|People|Fans|Plenty)\b')
VERDICT_MAX_WORDS = 13   # longer than this and it is usually carrying a fact
VERDICT_WEAK_MAX = 7     # "anyway" in a longer sentence is normally a real fact

# ── the non-sequitur closer ────────────────────────────────────────────────
# Added after the Bass pack. Daniele found four closing sentences that were true,
# were not verdicts, and still read as arriving from nowhere:
#     "Justice, the album made after he died, is the one with the bass mixed
#      almost out of it."          (the blurb was about a different album)
#     "Kumalo had learned on a bass strung with fishing line."
#     "Leo Fender was involved, years after selling the company..."
#     "Good Times has been built on ever since."
# NOT DETECTABLE. Lexical overlap was tried: flag a closing sentence sharing no
# content word with the one before it. It fired on 51 of the 106 approved Bass
# blurbs and caught one of the three examples above, because a deliberate turn
# ("He never slapped a note in his life", "There is no guitar on the riff at
# all") looks identical to a bolted-on fact from the outside. The difference is
# whether the last sentence answers a question the one before it raised, and
# that is a reading job. It is in QUIZ_SPEC 2b as a fourth move, with these four
# examples, and it needs a person.

# TRIED AND REMOVED: a check for a long sentence with a second independent
# clause hung off ", and", on the theory that the approved rewrites split those
# into two sentences. It fired on seven of the forty-two approved Bass blurbs
# including Daniele's own A7, which is exactly the failure this file already
# records once: a tool enforcing my restraint back onto his voice. The move is
# real, it is just not machine-detectable. It lives in QUIZ_SPEC 2b instead.
NOT_JUST = re.compile(r"\bnot just\b.{0,40}\bbut\b", re.I)
RHETORICAL = re.compile(r'\?\s*$')
VERBS = set("""is are was were be been being has have had do does did can could
will would should may might must says said tells told makes made made takes took
gets got goes went came come sold sells built build wrote writes won wins lost
plays played kept keeps ran runs put puts gave gives left leaves found finds
began begins ended ends died dies named names called calls turned turns
paid held sent bought brought caught chose drew flew knew led met read saw
spent stood felt kept meant sat shot spoke thought understood wore rose fell
grew hit cost let bore sang rang drove broke spoke woke chose froze
cut put set shut split spread burst beat bet quit hurt built rebuilt
sent lent bent dealt felt knelt leapt slept swept wept crept kept left""".split())


def sentences(text):
    # Protect decimals (.013, 3.5) and common abbreviations before splitting,
    # or a string-gauge blurb reads as three fragments.
    t = re.sub(r'(?<=\d)\.(?=\d)', '\x00', text)
    t = re.sub(r'(?<=^)\.(?=\d)', '\x00', t)
    t = re.sub(r'(?<=\s)\.(?=\d)', '\x00', t)
    for ab in ('Mr.', 'Mrs.', 'Ms.', 'Dr.', 'St.', 'Jr.', 'Sr.', 'vs.', 'U.S.', 'No.'):
        t = t.replace(ab, ab.replace('.', '\x01'))
    # Single capital letters followed by a period are initials, not sentence ends:
    # C.W. McCall, J.R.R. Tolkien, B.B. King.
    t = re.sub(r'\b([A-Z])\.(?=\s*[A-Z])', lambda m: m.group(1) + '\x01', t)
    # The last letter of a dotted acronym has no capital after it, so the rule
    # above leaves R.O.B. ending in a real period and "attached to it." reads as
    # a three-word sentence. Protect a capital that follows an already-protected
    # initial, however many letters the acronym runs to.
    while True:
        t2 = re.sub('\x01([A-Z])\\.', lambda m: '\x01' + m.group(1) + '\x01', t)
        if t2 == t:
            break
        t = t2
    parts = re.findall(r'[^.!?]+[.!?]+', t)
    tail = re.sub(r'.*[.!?]', '', t).strip()
    if tail:
        parts.append(tail)
    out = [p.replace('\x00', '.').replace('\x01', '.').strip() for p in parts]
    return [p for p in out if p]


def words(s):
    return [w for w in re.findall(r"[\w'\u2019-]+", s)]


def check(fact, idx, stem=None, lang='en'):
    errs, warns = [], []
    if not fact or not fact.strip():
        return [('ERROR', 'blurb is empty')], []

    w = words(fact)
    sents = sentences(fact)

    # ── the two rules that kept being broken ───────────────────────────────
    if PRONOUN_OPEN.match(fact):
        errs.append(('ERROR', 'opens with a pronoun; spec says name the subject '
                     'first, and Guitar Gods does it 0 times in 60'))
    if SUBORDINATOR_OPEN.match(fact):
        errs.append(('ERROR', 'opens with a subordinate clause; the subject is '
                     'delayed past the first words'))

    # ── length ─────────────────────────────────────────────────────────────
    # Reported, not judged. A blurb is the right length when it has said its
    # thing and stopped; a word count cannot tell whether it has. The spread is
    # still printed at the foot of the run, where it is useful as a comparison
    # against the shipped packs rather than as a gate.
    pass

    # ── rhythm ─────────────────────────────────────────────────────────────
    if len(sents) == 2:
        a, b = len(words(sents[0])), len(words(sents[1]))
        ratio = max(a, b) / max(1, min(a, b))
        total = a + b
        if ratio < RATIO_MIN and total < BALANCED_SHORT_TOTAL:
            errs.append(('ERROR', f'two balanced short sentences, {a} and {b} words, '
                         f'ratio {ratio:.2f}; this is the "state the fact, add the '
                         'color" shape the spec records as already rejected'))
        elif ratio < RATIO_MIN:
            warns.append(('WARN', f'two sentences of similar length, {a} and {b} words'))
    if len(sents) > 3:
        warns.append(('WARN', f'{len(sents)} sentences; approved pack has at most 3'))

    # ── fragments ──────────────────────────────────────────────────────────
    for s in sents:
        sw = words(s)
        if len(sw) < 4:
            errs.append(('ERROR', f'sentence of {len(sw)} words; the approved pack '
                         f'has none under 4: "{s.strip()}"'))
        elif not any(x.lower() in VERBS or x.lower().endswith(('ed', 'ing'))
                     for x in sw):
            warns.append(('WARN', f'possible fragment, no finite verb found: "{s.strip()}"'))

    low = fact.lower()

    # ── prose rules ────────────────────────────────────────────────────────
    if lang == 'en':
        for b, us in BRITISH.items():
            if re.search(r'\b' + re.escape(b) + r'\b', low):
                errs.append(('ERROR', f'British spelling "{b}", use "{us}"'))
        for b, us in BRITISH_USAGE.items():
            if not us:
                continue
            if re.search(r'\b' + re.escape(b) + r'\b', low):
                warns.append(('WARN', f'British usage "{b}", consider "{us}"'))
    for m in MARKETING:
        if re.search(r'\b' + m + r'\b', low):
            errs.append(('ERROR', f'marketing adjective "{m}"'))
    for c in EMPTY_CLOSERS:
        if c in low:
            errs.append(('ERROR', f'empty closer "{c}"'))
    for g in GLOSS:
        if g in low:
            warns.append(('WARN', f'glossing the fact rather than stating one: "{g}"'))

    # ── verdict closer, and the clause that wants to be its own sentence ────
    if len(sents) > 1:
        last = sents[-1].strip()
        lw = words(last)
        hit = ((len(lw) <= VERDICT_MAX_WORDS
                and (VERDICT_STRONG.search(last) or VERDICT_OPEN.match(last)))
               or (len(lw) <= VERDICT_WEAK_MAX and VERDICT_WEAK.search(last)))
        if hit:
            warns.append(('WARN', 'closing sentence reads as a verdict on the '
                          f'fact rather than another fact: "{last}"'))
    if NOT_JUST.search(fact):
        errs.append(('ERROR', '"not just X but Y" construction'))
    if HEDGE_OPEN.match(fact):
        errs.append(('ERROR', 'hedging or rhetorical opener'))
    if RHETORICAL.search(fact.strip()):
        errs.append(('ERROR', 'ends on a question'))
    if '\u2014' in fact or '--' in fact:
        errs.append(('ERROR', 'em-dash'))
    if fact.count('!') > 1:
        errs.append(('ERROR', 'more than one exclamation'))

    # ── must add something the question did not ────────────────────────────
    if stem:
        sw = set(x.lower() for x in words(stem) if len(x) > 4)
        bw = set(x.lower() for x in w if len(x) > 4)
        if sw and len(sw & bw) / len(sw) > 0.6:
            warns.append(('WARN', 'largely restates the stem'))

    return errs, warns


def load(path, pack=None):
    if path.endswith('.json'):
        data = json.load(open(path, encoding='utf-8'))
        if data and isinstance(data[0], str):
            return [{'fact': d} for d in data]
        return data
    raise SystemExit('pass a .json of blurbs, or extract from the HTML first')


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    rows = load(sys.argv[1])
    n_err = n_warn = 0
    excl = 0
    print('=' * 70)
    print(f'BLURB VOICE AUDIT  [{sys.argv[1]}]  {len(rows)} blurbs')
    print('=' * 70)
    for i, r in enumerate(rows, 1):
        for lang, key in (('en', 'fact'), ('it', 'fact_it')):
            fact = r.get(key)
            if not fact:
                if key == 'fact':
                    print(f'  {i:>3} ERROR  no English blurb')
                    n_err += 1
                continue
            if lang == 'en' and '!' in fact:
                excl += 1
            errs, warns = check(fact, i, r.get('q'), lang)
            for level, msg in errs:
                print(f'  {i:>3} [{lang}] ERROR  {msg}')
                n_err += 1
            for level, msg in warns:
                print(f'  {i:>3} [{lang}] warn   {msg}')
                n_warn += 1
    print('-' * 70)
    print(f'  exclamations: {excl}/{len(rows)}  (reported, not judged: where one '
          f'fits is a feel call and a percentage cannot see it)')
    lens = [len(words(r['fact'])) for r in rows if r.get('fact')]
    if lens:
        print(f'  words: min {min(lens)}  median {statistics.median(lens):.0f}  max {max(lens)}'
              f'   (approved: 28 / 39 / 58)')
    print('=' * 70)
    print(f'  {n_err} errors, {n_warn} warnings')
    print('=' * 70)
    sys.exit(1 if n_err else 0)


if __name__ == '__main__':
    main()
