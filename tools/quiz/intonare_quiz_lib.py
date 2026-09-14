"""Shared loader and shared thresholds for every quiz tool.

Written after three tools died at once. Each carried its own hardcoded list of
twenty pack keys, and deleting gear_equipment in v0.196.0 killed all three with
the same AttributeError. A tool that carries a copy of the file's contents goes
stale the moment the file changes, and a broken audit looks exactly like a
passing one.

Two jobs:

1. ONE way to read PACKS. Keys are discovered from the file, never listed here.
   Parsing goes through node, because the rows are JS object literals and every
   regex written against them has under-counted a bilingual pack at some point:
   guitar_gods reported 52 questions while holding 90.

2. ONE threshold per fault class. The answer-length tell had three different
   numbers in three tools (2.0x in the draft check, 12 chars in the pack audit,
   1.6x in the v0.189 padding pass), so a pack could clear the draft, get
   padded, and still fail at ship. Same fault, three verdicts, all landing on
   Daniele.

The numbers below are MEASURED against the approved packs, not chosen. Where a
measurement is quoted, it was taken with this library on the shipped file.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import hashlib

HTML = os.environ.get(
    'INTONARE_HTML',
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), 'Intonare.html'))



# ── Thresholds, measured ─────────────────────────────────────────────────────
#
# ANSWER FINDABLE BY LENGTH. Measured over 561 questions in both languages
# across the six authored packs:
#
#     rule            gods  beatles  bass  70s  theory  technique
#     gap > 12           1        1     0    0       3         11
#     gap > 15           0        0     0    0       1          3
#     ratio > 1.6        0        0     3    2       1          0
#
# gap > 15 is clean on the four packs Daniele read question by question, so it
# is the error. 13 to 15 is a reading list rather than a fault.
#
# The ratio rule is DROPPED. Every one of its hits was a name or a term whose
# length is inherent and cannot be padded away: "four on the floor" against
# "a shuffle", "Quattro" against "Uno / Due / Tre", "The Complete Book of
# Running" against "Aerobics". A check that fires on material nobody can fix
# teaches you to ignore the output.
LEN_GAP_ERROR = 15
LEN_GAP_WARN = 12

# Subject cap: 2 for a decades pack where variety is the point, 3 for a subject
# pack where returning to Hendrix three times is the design.
CAP_DECADES = 2
CAP_SUBJECT = 3

DECADE_PACKS = {'fifties', 'sixties', 'seventies', 'eighties', 'nineties', 'noughties'}

# Blurb word count, measured from shipped guitar_gods: 28 to 58, median 39.
# Read as a range for the pack being written, not as one number for all packs;
# Beatles runs 43 because it tells stories, guitar_technique runs 28 because one
# idea per blurb is enough there.
BLURB_WORDS_LOW = 18
BLURB_WORDS_HIGH = 60

# RUN-ON CEILING, measured over 870 English and 867 Italian sentences in the six
# authored packs. The old check used 45 words for both languages, which fires on
# approved material in both: the English ceiling is 48 and the Italian is 53.
# The first thing the bilingual version flagged was the Angus Young blurb out of
# QUIZ_VOICE.md, in Italian, at 44 words. That is the gold standard failing its
# own check.
#
#            p90  p95  p99  max
#     EN      39   41   45   48
#     IT      39   42   48   53
#
# Italian is only 5 to 10 percent longer at the tail, so it needs its own number
# rather than a shared one. Set at the approved maximum, so a hit means the
# sentence is longer than anything that has ever shipped.
RUNON_WORDS = {'en': 48, 'it': 53}
RUNON_COMMAS = 5      # both languages; max on approved material is 5
RUNON_JOINERS = {'en': 6, 'it': 7}


# ── Reading the file ─────────────────────────────────────────────────────────

_NODE_EXTRACT = r'''
const fs = require('fs');
const h = fs.readFileSync(process.argv[2], 'utf8');
const i = h.indexOf('const PACKS');
if (i < 0) { console.error('no const PACKS in file'); process.exit(2); }
let j = h.indexOf('{', i), d = 0, k = j;
for (;;) {
  const c = h[k];
  if (c === '{') d++;
  else if (c === '}') { d--; if (d === 0) break; }
  k++;
}
const PACKS = eval('(' + h.slice(j, k + 1) + ')');
const ready = (h.match(/MQ_PACK_READY\s*=\s*\[([\s\S]*?)\]/) || [, ''])[1]
  .split(',').map(s => s.trim().replace(/^['"]|['"]$/g, '')).filter(Boolean);
const out = { ready: ready, order: Object.keys(PACKS), packs: {} };
for (const key of Object.keys(PACKS)) {
  const p = PACKS[key];
  out.packs[key] = {
    name: p.name || key, group: p.group || '',
    questions: Array.isArray(p.questions) ? p.questions : []
  };
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
'''

_cache = {}


def load(path=None):
    """Return {'ready': [...], 'order': [...], 'packs': {id: {...}}}.

    Cached per (path, mtime, size) so a gate running eight checks reads the
    10MB file once.
    """
    path = path or HTML
    if not os.path.exists(path):
        sys.exit(f'{path} not found. Copy Intonare.html there, or set INTONARE_HTML.')
    st = os.stat(path)
    key = (path, st.st_mtime, st.st_size)
    if key in _cache:
        return _cache[key]
    with tempfile.TemporaryDirectory() as td:
        js = os.path.join(td, 'x.js')
        out = os.path.join(td, 'out.json')
        open(js, 'w').write(_NODE_EXTRACT)
        r = subprocess.run(['node', js, path, out], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit('could not parse PACKS with node: ' + (r.stderr.strip() or 'unknown'))
        data = json.load(open(out, encoding='utf-8'))
    _cache[key] = data
    return data


def pack_ids(path=None, ready_only=False):
    d = load(path)
    ids = d['order']
    if ready_only:
        ids = [k for k in ids if k in d['ready']]
    return ids


def ready_ids(path=None):
    return load(path)['ready']


def rows(pack_id, path=None):
    """Shipped rows for one pack, exactly as they sit in the file.

    The answer is at opts[ans]. Draft JSON puts the answer at opts[0] instead;
    use as_draft() to convert, and never assume one shape.
    """
    d = load(path)
    if pack_id not in d['packs']:
        sys.exit(f'no pack "{pack_id}". Packs: ' + ', '.join(d['order']))
    return d['packs'][pack_id]['questions']


def pack_name(pack_id, path=None):
    return load(path)['packs'].get(pack_id, {}).get('name', pack_id)


# ── Row shapes ───────────────────────────────────────────────────────────────

def as_draft(shipped):
    """Shipped rows (answer at opts[ans]) to draft rows (answer at opts[0])."""
    out = []
    for r in shipped:
        a = r.get('ans', 0)
        o = list(r.get('opts') or [])
        oi = list(r.get('opts_it') or [])
        if o and 0 <= a < len(o):
            o = [o[a]] + [x for n, x in enumerate(o) if n != a]
        if oi and 0 <= a < len(oi):
            oi = [oi[a]] + [x for n, x in enumerate(oi) if n != a]
        row = dict(r)
        row['opts'] = o
        if oi:
            row['opts_it'] = oi
        row.pop('ans', None)
        out.append(row)
    return out


def answer_index(row):
    """Works for both shapes. Draft rows have no ans and put it first."""
    return row.get('ans', 0)


def view(row, lang='en'):
    """One language's side of a row, as (stem, options, answer index, blurb).

    This exists because the draft structural check and the blurb check had ZERO
    references to q_it, opts_it or fact_it. Every check they ran was English
    only, so every Italian fault survived the draft gate and was found either by
    livecheck at ship or by Daniele. In v0.189 that was 12 answer-length tells,
    half of them Italian, plus 16 drifts against the draft checker's 4.
    """
    if lang == 'it':
        q = row.get('q_it') or row.get('q', '')
        o = row.get('opts_it') or row.get('opts') or []
        f = row.get('fact_it') or ''
    else:
        q = row.get('q', '')
        o = row.get('opts') or []
        f = row.get('fact') or ''
    return q, list(o), answer_index(row), f


def has_italian(rows_):
    return any(r.get('q_it') for r in rows_)


def langs(rows_):
    return ('en', 'it') if has_italian(rows_) else ('en',)


def load_rows(arg, path=None):
    """Rows from EITHER a draft JSON file OR a pack id in Intonare.html.

    This is the fix for the thing that generated most of the triage. The draft
    tools and the ship tools were separate programs reading separate inputs, so
    they disagreed constantly: the draft check used a 2.0x length rule on
    English only, the pack audit used 12 characters on both languages, and the
    padding pass used 1.6x. A pack could clear the draft, get padded, and still
    fail at ship, three verdicts on one fault.

    Every checker takes this instead, so the draft gate and the ship gate run
    the same code over the same shapes. A pack that passes in draft passes
    installed, or the tool is wrong in both places at once, which is the only
    honest kind of wrong.

        python3 <check>.py draft.json
        python3 <check>.py --pack bass
    """
    if arg and not arg.endswith('.json') and os.path.exists(arg) is False:
        # bare pack id
        return as_draft(rows(arg, path))
    if not os.path.exists(arg):
        sys.exit(arg + ' not found')
    import json as _json
    return _json.load(open(arg, encoding='utf-8'))


def rows_from_argv(argv, default='draft.json'):
    """Read the usual command line: a JSON path, or --pack <id>.

    Returns (rows, label). Shipped rows come back in DRAFT shape, answer first,
    so a checker never has to care which side it is looking at.
    """
    if '--pack' in argv:
        pid = argv[argv.index('--pack') + 1]
        return as_draft(rows(pid)), pid
    args = [a for a in argv[1:] if not a.startswith('-')]
    p = args[0] if args else default
    if not os.path.exists(p):
        sys.exit(f'{p} not found. Pass a draft JSON, or --pack <id> to read '
                 f'the installed pack.')
    import json as _json
    return _json.load(open(p, encoding='utf-8')), os.path.basename(p)


# ── Word lists, per language ─────────────────────────────────────────────────
#
# The lexical checks all need to know which words carry meaning. Running the
# English list over Italian is how the pair check went from 12 pairs to 60 on
# the same pack: "quale", "della" and "parte" counted as content words, so every
# stem matched every other stem.

STOP_EN = {
    'which', 'what', 'who', 'whose', 'where', 'when', 'why', 'how', 'that',
    'this', 'these', 'those', 'from', 'with', 'they', 'their', 'them', 'there',
    'here', 'have', 'has', 'had', 'been', 'being', 'were', 'was', 'are', 'is',
    'does', 'did', 'do', 'the', 'and', 'but', 'for', 'not', 'you', 'your',
    'his', 'her', 'its', 'one', 'two', 'more', 'most', 'than', 'then', 'also',
    'about', 'after', 'before', 'into', 'over', 'under', 'only', 'just',
    'song', 'album', 'band', 'record', 'called', 'name', 'named', 'first',
    'like', 'make', 'made', 'take', 'took', 'come', 'came', 'give', 'gave',
    'play', 'played', 'plays', 'thing', 'things', 'some', 'each', 'other',
    'would', 'could', 'should', 'will', 'can', 'may', 'much', 'many', 'both',
}

STOP_IT = {
    'quale', 'quali', 'cosa', 'come', 'dove', 'quando', 'perche', 'perché',
    'chi', 'che', 'della', 'dello', 'delle', 'degli', 'dei', 'del', 'nella',
    'nello', 'nelle', 'negli', 'nei', 'nel', 'alla', 'allo', 'alle', 'agli',
    'sulla', 'sullo', 'sulle', 'sugli', 'sui', 'sul', 'dalla', 'dallo',
    'dalle', 'dagli', 'dai', 'dal', 'con', 'per', 'tra', 'fra', 'una', 'uno',
    'gli', 'gli', 'gli', 'suo', 'sua', 'suoi', 'sue', 'loro', 'gli', 'gli',
    'era', 'erano', 'sono', 'essere', 'stato', 'stata', 'aveva', 'avere',
    'hanno', 'viene', 'venne', 'fece', 'fatto', 'fare', 'dice', 'detto',
    'piu', 'più', 'meno', 'molto', 'anche', 'ancora', 'sempre', 'mai',
    'solo', 'soltanto', 'dopo', 'prima', 'sopra', 'sotto', 'senza',
    'canzone', 'brano', 'album', 'disco', 'gruppo', 'nome', 'chiamato',
    'chiama', 'suona', 'suonava', 'suonato', 'primo', 'prima', 'questo',
    'questa', 'questi', 'queste', 'quello', 'quella', 'altri', 'altre',
    'altro', 'altra', 'ogni', 'tutti', 'tutte', 'tutto', 'tutta', 'due',
}


def stop(lang):
    return STOP_IT if lang == 'it' else STOP_EN


def content_words(text, lang='en', minlen=4):
    """Meaningful words, lowercased, with the right stop list for the language."""
    pat = r"[a-z\u00e0-\u00ff']{%d,}" % minlen
    return {w for w in re.findall(pat, (text or '').lower())} - stop(lang)


# ── Stem freeze ──────────────────────────────────────────────────────────────
#
# The omega read keeps finding the same fault: a stem was rewritten and its
# options and blurb were not looked at underneath it. On the Bass pack that was
# three questions whose options had stopped answering their own stems, and every
# audit passed them. That is bookkeeping, not taste, so it can be a gate that
# never cries wolf.
#
# A row carries "sq", the hash of the stem as it stood when the options and the
# blurb were last approved. Change the stem and the hash stops matching.

def stem_hash(row):
    """Both languages, so an Italian-only edit also marks the row stale."""
    raw = (row.get('q') or '') + '\x00' + (row.get('q_it') or '')
    return hashlib.sha1(' '.join(raw.split()).encode('utf-8')).hexdigest()[:10]


def stale_rows(rows_):
    """Rows whose stem moved since the options and blurb were approved.

    Returns (stale, unsealed). A row with no sq has never been sealed, which is
    normal while a tier is still being written and is a fault at ship.
    """
    stale, unsealed = [], []
    for i, r in enumerate(rows_, 1):
        if not r.get('sq'):
            unsealed.append(i)
        elif r['sq'] != stem_hash(r):
            stale.append(i)
    return stale, unsealed


def seal(rows_):
    """Stamp every row's current stem. Run only after reading the row whole."""
    for r in rows_:
        r['sq'] = stem_hash(r)
    return rows_


# ── Small shared helpers ─────────────────────────────────────────────────────

def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text or '') if s.strip()]


def length_tell(opts, ans_i):
    """The one answer-length rule. Returns (gap, level) with level in
    '', 'warn', 'error'."""
    if not opts or len(opts) < 2 or not (0 <= ans_i < len(opts)):
        return 0, ''
    a = len(opts[ans_i])
    rest = max(len(o) for n, o in enumerate(opts) if n != ans_i)
    gap = a - rest
    if gap > LEN_GAP_ERROR:
        return gap, 'error'
    if gap > LEN_GAP_WARN:
        return gap, 'warn'
    return gap, ''


def cap_for(pack_id):
    return CAP_DECADES if pack_id in DECADE_PACKS else CAP_SUBJECT


_JOINERS = {'en': r'\b(and|then|but|so|which|while)\b',
            'it': r'\b(e|poi|ma|quindi|che|mentre)\b'}


def runon(sentence, lang='en'):
    """True when a sentence is longer than anything in the approved packs.

    Commas inside a LIST are not clause joins. "A bass is tuned E, A, D and G"
    is three commas and one clause, so a run of short comma-separated items is
    collapsed before counting.
    """
    s2 = re.sub(r'(?:[^,]{1,22},\s+){2,}[^,]{1,22}\s+(and|e)\s+[^,]{1,22}',
                'LIST', sentence)
    return (len(sentence.split()) > RUNON_WORDS.get(lang, 48)
            or s2.count(',') > RUNON_COMMAS
            or len(re.findall(_JOINERS.get(lang, _JOINERS['en']), sentence, re.I))
            > RUNON_JOINERS.get(lang, 6))


if __name__ == '__main__':
    d = load()
    print(f"{len(d['order'])} packs, {len(d['ready'])} ready   [{HTML}]")
    print(f"{'pack':24}{'n':>5}{'it':>5}{'d1/d2/d3':>12}  ready")
    for k in d['order']:
        qs = d['packs'][k]['questions']
        it = sum(1 for q in qs if q.get('q_it'))
        t = [sum(1 for q in qs if q.get('d') == n) for n in (1, 2, 3)]
        tier = f'{t[0]}/{t[1]}/{t[2]}'
        print(f"{k:24}{len(qs):5}{it:5}{tier:>12}  {'yes' if k in d['ready'] else ''}")
