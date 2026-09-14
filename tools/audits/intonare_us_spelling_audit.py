#!/usr/bin/env python3
"""
intonare_us_spelling_audit.py — find British spellings in USER-VISIBLE English only.

The naive version of this job is a find-and-replace, and it destroys the app: the
file is 10MB of CSS, JS identifiers, HTML comments and Italian, and a blind sweep
eats `AudioContext`, `#mst-analyse`, `const GREY`, `getContext` and every design
note we have ever written.

So this classifies each hit instead of assuming:

  COMMENT     inside /* */ or // — nobody reads these but us. Never touch.
  IDENT       a JS/CSS/DOM identifier: adjacent to - or _, or the whole quoted
              token has no spaces. Renaming these is risk with no user benefit.
  COPY        prose. This is the list that matters.

Usage: intonare_us_spelling_audit.py [Intonare.html] [--copy|--ident|--comment]
"""
import re, sys, io
from collections import Counter, defaultdict

PAIRS = [
    (r'practis(e|es|ed|ing)',      lambda m: 'practic'+m.group(1)),
    (r'favourite(s?)',             lambda m: 'favorite'+m.group(1)),
    (r'colour(s|ed|ing)?',         lambda m: 'color'+(m.group(1) or '')),
    (r'centre(s?)',                lambda m: 'center'+(m.group(1) or '')),
    (r'centred',                   lambda m: 'centered'),
    (r'customis(e|es|ed|ing|ation)', lambda m: 'customiz'+m.group(1)),
    (r'personalis(e|es|ed|ing|ation)', lambda m: 'personaliz'+m.group(1)),
    (r'organis(e|es|ed|ing|ation)', lambda m: 'organiz'+m.group(1)),
    (r'recognis(e|es|ed|ing)',     lambda m: 'recogniz'+m.group(1)),
    (r'analys(e|es|ed|ing)',       lambda m: 'analyz'+m.group(1)),
    (r'normalis(e|es|ed|ing|ation)', lambda m: 'normaliz'+m.group(1)),
    (r'visualis(e|es|ed|ing|ation)', lambda m: 'visualiz'+m.group(1)),
    # The -ise list was a hand-picked handful and "synthesise" was not on it, so
    # thirty-odd synthesisers sat in the packs untouched. These are the rest of
    # the verbs this app is ever likely to use.
    (r'synthesis(e|es|ed|ing|er|ers)', lambda m: 'synthesiz'+m.group(1)),
    (r'specialis(e|es|ed|ing|ation)\b', lambda m: 'specializ'+m.group(1)),  # \b or it eats "specialist"
    (r'standardis(e|es|ed|ing|ation)', lambda m: 'standardiz'+m.group(1)),
    (r'emphasis(e|es|ed|ing)',     lambda m: 'emphasiz'+m.group(1)),
    (r'summaris(e|es|ed|ing)',     lambda m: 'summariz'+m.group(1)),
    (r'memoris(e|es|ed|ing)',      lambda m: 'memoriz'+m.group(1)),
    (r'minimis(e|es|ed|ing)',      lambda m: 'minimiz'+m.group(1)),
    (r'maximis(e|es|ed|ing)',      lambda m: 'maximiz'+m.group(1)),
    (r'prioritis(e|es|ed|ing)',    lambda m: 'prioritiz'+m.group(1)),
    (r'criticis(e|es|ed|ing)',     lambda m: 'criticiz'+m.group(1)),
    (r'apologis(e|es|ed|ing)',     lambda m: 'apologiz'+m.group(1)),
    (r'utilis(e|es|ed|ing|ation)', lambda m: 'utiliz'+m.group(1)),
    (r'theoris(e|es|ed|ing)',      lambda m: 'theoriz'+m.group(1)),
    (r'hypnotis(e|es|ed|ing)',     lambda m: 'hypnotiz'+m.group(1)),
    (r'synchronis(e|es|ed|ing)',   lambda m: 'synchroniz'+m.group(1)),
    (r'initialis(e|es|ed|ing)',    lambda m: 'initializ'+m.group(1)),
    (r'memoris(e|es|ed|ing)',      lambda m: 'memoriz'+m.group(1)),
    (r'emphasis(e|es|ed|ing)',     lambda m: 'emphasiz'+m.group(1)),
    (r'prioritis(e|es|ed|ing)',    lambda m: 'prioritiz'+m.group(1)),
    # NOT t or ts. "specialist" and "specialists" are correct American English,
    # and a rule that rewrote them produced "specializt", which is how
    # "organist" became "organizt" and shipped. A suffix list on a -ise verb
    # must only hold the verb's own endings.
    (r'specialis(e|es|ed|ing|ation)\b', lambda m: 'specializ'+m.group(1)),
    (r'stabilis(e|es|ed|ing)',     lambda m: 'stabiliz'+m.group(1)),
    (r'utilis(e|es|ed|ing)',       lambda m: 'utiliz'+m.group(1)),
    (r'maximis(e|es|ed|ing)',      lambda m: 'maximiz'+m.group(1)),
    (r'minimis(e|es|ed|ing)',      lambda m: 'minimiz'+m.group(1)),
    (r'apologis(e|es|ed|ing)',     lambda m: 'apologiz'+m.group(1)),
    (r'equalis(er|ers)',           lambda m: 'equaliz'+m.group(1)),
    (r'behaviour(s|al)?',          lambda m: 'behavior'+(m.group(1) or '')),
    (r'flavour(s|ed)?',            lambda m: 'flavor'+(m.group(1) or '')),
    (r'honour(s|ed)?',             lambda m: 'honor'+(m.group(1) or '')),
    (r'neighbour(s|ing|hood)?',    lambda m: 'neighbor'+(m.group(1) or '')),
    (r'grey(s|ish)?',              lambda m: 'gray'+(m.group(1) or '')),
    (r'programme(s)?',             lambda m: 'program'+(m.group(1) or '')),
    (r'catalogue(s|d)?',           lambda m: 'catalog'+(m.group(1) or '')),
    (r'licence(s?)',               lambda m: 'license'+(m.group(1) or '')),
    (r'defence(s?)',               lambda m: 'defense'+(m.group(1) or '')),
    (r'offence(s?)',               lambda m: 'offense'+(m.group(1) or '')),
    (r'cancell(ed|ing)',           lambda m: 'cancel'+m.group(1)),
    (r'labell(ed|ing)',            lambda m: 'label'+m.group(1)),
    (r'travell(ed|ing|er|ers)',    lambda m: 'travel'+m.group(1)),
    (r'modell(ed|ing)',            lambda m: 'model'+m.group(1)),
    (r'theatre(s?)',               lambda m: 'theater'+(m.group(1) or '')),
    (r'whilst',                    lambda m: 'while'),
    (r'amongst',                   lambda m: 'among'),
    (r'manoeuvr(e|es|ing)',        lambda m: 'maneuver'+('' if m.group(1)=='e' else m.group(1))),
    (r'sceptic(al|ism)?',          lambda m: 'skeptic'+(m.group(1) or '')),
    (r'storey(s?)',                lambda m: 'story' if not m.group(1) else 'stories'),
]
BIG = re.compile(r'\b(' + '|'.join('(?:%s)' % p for p, _ in PAIRS) + r')\b', re.I)


def comment_mask(h):
    """True where a character sits inside a comment (block, line, or HTML)."""
    mask = bytearray(len(h))
    for m in re.finditer(r'/\*.*?\*/', h, re.S):
        mask[m.start():m.end()] = b'\x01' * (m.end() - m.start())
    for m in re.finditer(r'<!--.*?-->', h, re.S):
        mask[m.start():m.end()] = b'\x01' * (m.end() - m.start())
    # Line comments: require the // to open at line start or after whitespace/;/{/}
    # so protocol-relative URLs and https:// are not eaten.
    for m in re.finditer(r'(?m)(?:^|(?<=[\s;{}]))//[^\n]*', h):
        mask[m.start():m.end()] = b'\x01' * (m.end() - m.start())
    return mask


def classify(h, mask, start, end):
    if mask[start]:
        return 'COMMENT'
    before = h[start - 1] if start else ' '
    # Property access and declarations are code: `.centre`, `const centre =`
    if before == '.':
        return 'IDENT'
    line_start = h.rfind('\n', 0, start) + 1
    line_end = h.find('\n', end)
    line = h[line_start:line_end if line_end > 0 else len(h)]
    off = start - line_start
    if re.search(r'\b(?:const|let|var|function)\s+$', line[:off]):
        return 'IDENT'

    # A quoted token with no whitespace is either an identifier or a display
    # label, and CASE is what separates them. `'analyse'` and `'#mst-analyse'`
    # are wiring; `'ANALYSE'` is the text on the metro subtab and `'Favourites'`
    # is a tour step title. Both of those went to IDENT on the first pass purely
    # for being one word long, which is exactly the kind of miss that makes an
    # audit worse than no audit.
    for qm in re.finditer(r"""(['"`])(.*?)\1""", line):
        if qm.start(2) <= off < qm.end(2):
            tok = qm.group(2).strip()
            if ' ' not in tok:
                return 'IDENT' if tok == tok.lower() else 'COPY'
            break

    # Not inside a quoted string. That leaves two possibilities and they are
    # cleanly separable: an HTML text node (the ANALYSE on the metro subtab, the
    # colour-coded in a Survival Guide paragraph) or bare code (`const GREY =`,
    # `Math.abs(centre - midStep)`). Whichever of < and > came last decides it.
    lt, gt = h.rfind('<', 0, start), h.rfind('>', 0, start)
    return 'COPY' if gt > lt else 'IDENT'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    path = args[0] if args else 'Intonare.html'
    h = io.open(path, encoding='utf-8').read()
    mask = comment_mask(h)

    buckets = defaultdict(list)
    # Titles and API names are spelled the way their owners spell them.
    KEEP_NAMES = ('Daft Punk', 'Licence to Kill', 'Hapshash and the Coloured Coat',
                  'createAnalyser', 'AnalyserNode', 'userCancelled', 'Baduizm',
                  'The Grey Album')
    for m in BIG.finditer(h):
        _near = h[max(0, m.start() - 50):m.end() + 50]
        if any(k.lower() in _near.lower() for k in KEEP_NAMES):
            continue
        kind = classify(h, mask, m.start(), m.end())
        ln = h.count('\n', 0, m.start()) + 1
        ctx = re.sub(r'\s+', ' ', h[max(0, m.start() - 75):m.end() + 60])
        buckets[kind].append((ln, m.group(0), ctx, m.start(), m.end()))

    print('=' * 70)
    print('  BRITISH SPELLINGS BY CLASS')
    print('=' * 70)
    for k in ('COPY', 'IDENT', 'COMMENT'):
        print(f'  {k:9} {len(buckets[k]):5}')
    print(f'  {"TOTAL":9} {sum(len(v) for v in buckets.values()):5}')

    want = None
    for f in flags:
        if f == '--copy': want = 'COPY'
        elif f == '--ident': want = 'IDENT'
        elif f == '--comment': want = 'COMMENT'
    if want:
        print(f'\n----- {want} -----')
        counts = Counter(w.lower() for _, w, _, _, _ in buckets[want])
        for w, c in counts.most_common():
            print(f'  {w:16} {c}')
        print()
        for ln, w, ctx, _, _ in buckets[want]:
            print(f'  L{ln:<7} {w:14} ...{ctx}...')
    return buckets


if __name__ == '__main__':
    main()


# ── Guards against the sweep itself ──────────────────────────────────────────
# Two things have gone wrong doing this job, both silently, and neither is a
# British spelling. The audit now looks for its own wreckage.
#
# 1. MANGLED WORDS. A prefix rule turns "organist" into "organizt" and
#    "programmer" into "programr". Four of those shipped and sat in the app
#    until somebody read the sentence. Real English has no -izt, -izm or -iztic.
#
# 2. HALF-RENAMED IDENTIFIERS. A rename that protects some occurrences of a name
#    and not others leaves two spellings of one variable. `analyser` became
#    `analyzer` in forty-six places and stayed `analyser` in two, which broke the
#    tuner's microphone path and passed `node --check` cleanly, because an
#    undefined variable is a runtime fault and not a syntax one.
import re as _re
_src = open(__import__('sys').argv[1] if len(__import__('sys').argv) > 1 else 'Intonare.html',
            encoding='utf-8').read()
_KNOWN_Z = {'baduizm'}          # Erykah Badu spells it that way
_mangled = [m.group(0) for m in _re.finditer(r'\b\w*iz(?:t|ts|tic|tica|m|ms)\b', _src, _re.I)
            if m.group(0).lower() not in _KNOWN_Z]
_mangled += [m.group(0) for m in _re.finditer(r'\b\w*programr\w*\b', _src, _re.I)]
print()
print('=' * 70)
print('  SWEEP DAMAGE')
print('=' * 70)
print(f'  mangled words: {len(_mangled)}')
for w in sorted(set(_mangled)): print(f'    {w}')

_PAIRS_ID = [('analyser','analyzer'),('normalise','normalize'),('colour','color'),
             ('centre','center'),('synthesiser','synthesizer'),('organiser','organizer'),
             ('visualise','visualize'),('customise','customize')]
_split = []
for _br, _us in _PAIRS_ID:
    _a = len(_re.findall(r'\b' + _br + r'\b', _src))
    _b = len(_re.findall(r'\b' + _us + r'\b', _src))
    # createAnalyser is a Web Audio name and is not the variable
    if _br == 'analyser': _a -= 0
    if _a and _b: _split.append((_br, _a, _us, _b))
print(f'  names living under two spellings at once: {len(_split)}')
for _br, _a, _us, _b in _split:
    print(f'    {_br} x{_a}  and  {_us} x{_b}   <- one of these is unreachable')
if _mangled or _split:
    print('\n  A half-done sweep passes node --check. This is the only thing that sees it.')


# ── British idiom and grammar ────────────────────────────────────────────────
# Spelling was only half of it. These are spelled correctly in both dialects and
# an American writer would not use them. Six were found in shipping packs after
# the spelling audit reported the app clean: "put him in hospital", "nobody had
# got out of a bass", "the band have spent", "a full stop in the sound", "the
# trickiest of the lot", "a comma rather than a full stop".
_IDIOM = [
    (r'\bin hospital\b',                   'in the hospital'),
    (r'\bhad got\b|\bhave got\b|\bhas got\b', 'had gotten / have'),
    (r'\bat the weekend\b',                'on the weekend'),
    (r'\bdifferent to\b',                  'different from'),
    (r'\b(?:was|were)\s+(?:sat|stood)\b',   'was sitting / standing'),
    (r'\bstraight away\b',                 'right away'),
    (r'\bfull stop\b',                     'period'),
    (r'\bin future\b',                     'in the future'),
    (r'\bof the lot\b',                    'of them'),
    (r'\bhave a go\b|\bgive it a go\b',    'give it a try'),
    (r'\bmind you\b',                      'then again'),
    (r'\breckon\b',                        'figure'),
    (r'\bkeen on\b',                       'into'),
    (r'\bbloke\b|\bchap\b(?!-)',           'guy'),
    (r'\bdodgy\b|\bnaff\b|\bknackered\b|\bgutted\b|\bwhinge\b', 'US equivalent'),
    # "spot on" survives only as a standalone verdict; "its own spot on the neck"
    # is not the idiom, and "the 2nd of natural minor" is a scale degree.
    (r'\bat university\b',                 'in college'),
    (r'\bthe \d{1,2}(?:st|nd|rd|th) of (?:January|February|March|April|May|June|July|'
     r'August|September|October|November|December)\b', 'US date order'),
    (r'\bmaths\b',                         'math'),
    (r'\bpernickety\b',                    'persnickety'),
]
# A collective noun takes a singular verb in American English: "the band has",
# not "the band have". Compound subjects ("Morton and the Band were") are
# excluded, since those are correctly plural in both dialects.
# "two couples inside the band were" is correctly plural: the subject is the
# couples. Only fire when the collective noun is the subject of its own clause.
_COLL = (r'(?<!and )(?<!inside )(?<!within )\b(?:the|that|this|a)\s'
         r'(band|group|team|duo|trio|quartet|orchestra|committee|'
         r'company|label|crew|audience)\s+(were|have|do)\b')
_idiom_hits, _coll_hits = [], []
for _p, _f in _IDIOM:
    for _m in _re.finditer(_p, _src, _re.I):
        _l = _src.count('\n', 0, _m.start()) + 1
        _line = _src.split('\n')[_l - 1].strip()
        if _line.startswith('//') or _line.startswith('*'): continue
        _idiom_hits.append((_l, _m.group(0), _f))
for _m in _re.finditer(_COLL, _src, _re.I):
    _l = _src.count('\n', 0, _m.start()) + 1
    _line = _src.split('\n')[_l - 1].strip()
    if _line.startswith('//') or _line.startswith('*'): continue
    _coll_hits.append((_l, _m.group(0)))
print()
print('=' * 70)
print('  BRITISH IDIOM AND GRAMMAR  (spelled right in both, said only in one)')
print('=' * 70)
print(f'  idioms: {len(_idiom_hits)}')
for _l, _w, _f in _idiom_hits: print(f'    L{_l:<7} "{_w}" -> {_f}')
print(f'  collective noun taking a plural verb: {len(_coll_hits)}')
for _l, _w in _coll_hits: print(f'    L{_l:<7} "{_w}"')
