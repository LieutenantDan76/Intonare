"""Italian faults, in one tool, over either a draft or the installed file.

REPLACES intonare_italian_draft_check.py and intonare_italian_sweep.py. There
were two Italian checkers and they disagreed. On the guitar_technique pack the
sweep reported 16 drifts and the draft checker reported 4, because the draft
checker predated the metric-conversion and worded-decade calibrations and nobody
had ported them across. Every one of those 12 differences landed on Daniele as
triage, and there was no way to tell from either output which tool was right.

Now there is one program. It reads a draft JSON or an installed pack, and it
runs the same checks over both, so a pack that passes while you are writing it
passes once it is in the file.

    python3 intonare_italian_check.py draft.json
    python3 intonare_italian_check.py --pack bass
    python3 intonare_italian_check.py --pack all

Every calibration below exists because it fired on approved material once.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intonare_quiz_lib as lib

# ── What Italy does not translate ───────────────────────────────────────────
#
# Terms Italian players say in English. An identical option here is correct
# rather than untranslated, and every one of these was a false positive found on
# a real pack.
KEEP_EN = {
    'muting', 'fretting out', 'palm muting', 'hammer-on', 'pull-off',
    'bending', 'slide', 'raking', 'tremolo picking', 'sweep picking', 'legato',
    'tapping', 'power chord', 'flatwound', 'roundwound', 'halfwound',
    'tapewound', 'truss rod', 'action', 'sustain', 'feedback', 'chorus',
    'delay', 'reverb', 'fuzz', 'wah', 'buffer', 'pickup', 'hybrid picking',
    'economy picking', 'alternate picking', "chicken pickin'", 'gallop',
    'skank', 'clave', 'rasgueado', 'bossa nova', 'vibrato', 'in the pocket',
    'on the one', 'in the clave', 'four on the floor', 'slap', 'groove',
    'shuffle', 'swing', 'riff', 'loop', 'crossover', 'rockabilly', 'jam',
    'break', 'one drop', 'backbeat',
}

# Band, film and song names keep their English and legitimately carry "and" and
# "the": Rory Storm and the Hurricanes, The Long and Winding Road. Blanked out
# before looking for English in the prose. Up to two connectors between capitals,
# because a name can carry both.
NAME = r"\b[A-Z][\w\u2019']*(?:\s+(?:(?:and|the|of|in|my|is|it|a)\s+){0,2}[A-Z][\w\u2019']*)*"

ENG_LEAK = [' the ', ' and ', ' with ', ' from ', ' which ', ' after ',
            ' because ', ' their ', ' would ', ' about ']

# Plurals matter. \bpound\b never matched "pounds", so every converted figure
# was reported as drift.
IMPERIAL = re.compile(r'\b(pounds?|foot|feet|inch|inches|miles?|lbs?)\b', re.I)

# Things a spellchecker passes and a native reader trips on immediately.
# Deliberately does NOT test un'/un before masculine nouns: that needs the
# gender of the following word, and a naive pattern flagged un'ottava,
# un'acustica and un'anima, all correct.
IT_BAD = {
    r'\bQuale è\b': "Qual è",
    r"\bqual'è\b": "qual è, no apostrophe",
    r'\bpò\b': "po', apostrophe not accent",
    r"\be' ": 'è',
    r'\bnonostante che\b': 'nonostante',
    r'\bpiù meglio\b': 'meglio',
    r'\bda me stesso\b': 'da solo',
    r'\bfa piacere di\b': 'fa piacere',
    r'\bricordare le corde\b': 'rincordare. "ricordare" means to remember',
    r'\bricordato la chitarra\b': 'rincordato',
}

# "meta" without an accent is the rugby term, portare in meta, and is correct.
ACCENTLESS = (r'\b(perche|piu|gia|cosi|puo|citta|universita|liberta|verita|'
              r'poiche|finche|caffe|percio)\b')


def digits(t):
    """Digits normalized. Italian writes 0,042 for 0.042 and 8.000 for 8,000,
    so separators come out before comparing rather than being parsed, which is
    what broke the first version of this check.

    No word boundary at the end: "1.6mm" and "20-foot" have a letter straight
    after the digits, and requiring one truncated them to "1" and "20".
    """
    return {m.rstrip('.,').replace('.', '').replace(',', '').lstrip('0') or '0'
            for m in re.findall(r'\b\d[\d.,]*', t or '')}


def quotes(t):
    """Inch marks are units, not quotation, and they sit flush against the
    digits. Allowing a space made '1898 "Thorough School...' look like a
    measurement and ate the quote."""
    return len(re.findall(r'[\u201c\u201d"]', t or '')) // 2


def check(rows, label):
    err, warn, note = [], [], []
    done = [r for r in rows if r.get('q_it')]
    if not done:
        print(f'{label}: no Italian')
        return 0

    for i, r in enumerate(rows, 1):
        if not r.get('q_it'):
            warn.append(f'{i}: no Italian stem')
            continue
        en_q, en_o, ans, en_f = lib.view(r, 'en')
        it_q, it_o, _, it_f = lib.view(r, 'it')
        if 'ans' not in r:
            ans = 0

        # ── coverage ────────────────────────────────────────────────────────
        # opts_it must match opts in LENGTH. The answer index points into that
        # array, so an Italian array of a different length would silently mark
        # the wrong option correct.
        if len(r.get('opts_it') or []) != len(r.get('opts') or []):
            err.append(f'{i}: Italian option count differs from the English')
        if not r.get('fact_it'):
            err.append(f'{i}: no Italian blurb')

        # ── an option left in English ───────────────────────────────────────
        # Song and album titles are identical in Italian by rule, and so are
        # people, makes and places Italy does not translate. Only an option
        # reading like a phrase rather than a name counts.
        for k, (en, it) in enumerate(zip(r.get('opts') or [], r.get('opts_it') or [])):
            if en != it or en.lower() in KEEP_EN:
                continue
            if re.match(r"^[A-Z0-9\u00c0-\u00dd.'\"\u2026#@&%]", en):
                continue
            err.append(f'{i}: option {k} left in English: {en}')

        blob = it_q + ' ' + it_f + ' ' + ' '.join(it_o)
        if re.search(ACCENTLESS, blob):
            err.append(f'{i}: stripped accent')
        elif re.search(r'\b(la|una|alla|della|a)\s+meta\b', blob):
            err.append(f'{i}: "meta" wants an accent here')

        for pat, fix in IT_BAD.items():
            m = re.search(pat, blob)
            if m:
                err.append(f'{i}: "{m.group(0).strip()}" -> {fix}')

        # ── English leaking into Italian prose ──────────────────────────────
        prose = it_f
        for phrase in sorted(KEEP_EN, key=len, reverse=True):
            prose = re.sub(re.escape(phrase), ' ', prose, flags=re.I)
        # A title carried across untouched keeps its English function words, and
        # it should: "Welcome to the Jungle" is the name of the song in both
        # languages. Any run of three or more words that appears verbatim in the
        # English twin is that case, so it comes out before the scan. Three is
        # the floor because two words match by accident and three rarely do.
        _w = re.findall(r"[\w'\u2019]+", en_f)
        for _n in range(min(8, len(_w)), 2, -1):
            for _j in range(len(_w) - _n + 1):
                _run = ' '.join(_w[_j:_j + _n])
                if _run in prose:
                    prose = prose.replace(_run, ' ')
        stripped = ' ' + re.sub(NAME, ' ', prose) + ' '
        for w in ENG_LEAK:
            if w in stripped:
                err.append(f'{i}: English "{w.strip()}" in the Italian prose')
                break

        # ── drift between the twins ─────────────────────────────────────────
        # Six Beatles blurbs were silently translated from an older English
        # draft and nothing caught it. Digits are the tell. Blurbs whose English
        # carries imperial units are skipped, because the Italian converts them
        # on purpose: an Italian reader has no feel for pounds. Italian words
        # its decades and centuries, so "the 1980s" is "negli anni Ottanta" and
        # "the 1500s" is "nel Cinquecento", both correct rather than drift.
        if it_f and not IMPERIAL.search(en_f):
            en_txt = re.sub(r"\b(1[0-9]|20)?\d0s\b|\b\d0s\b", ' ', en_f)
            missing = digits(en_txt) - digits(it_f)
            if missing:
                note.append(f'{i}: figures in the English not the Italian '
                            f'{sorted(missing)}   {en_q[:44]}')

        if it_f and quotes(re.sub(r'\d[\u201d\u2033"]', '', en_f)) != quotes(it_f):
            note.append(f'{i}: quoted material differs   {en_q[:44]}')

        # ── the length tell, in Italian ─────────────────────────────────────
        # This is the one the draft gate could never see. In v0.189 livecheck
        # found 12 and half were Italian only, because every check in the draft
        # tools read English.
        gap, level = lib.length_tell(it_o, ans)
        if level == 'error':
            err.append(f'{i}: Italian answer {gap} chars longer than any '
                       f'distractor   {it_q[:44]}')
        elif level == 'warn':
            warn.append(f'{i}: Italian answer {gap} chars longer   {it_q[:44]}')

        # ── curly against straight quotes ───────────────────────────────────
        # Only visible in the installed file, because draft JSON normalizes
        # them. Three pairs of twins looked different on screen in v0.189.
        if ('\u2019' in en_q + en_f) and ("'" in it_q + it_f) and \
                ('\u2019' not in it_q + it_f):
            warn.append(f'{i}: English uses curly apostrophes, Italian straight')

    print(f'{label}: {len(done)} of {len(rows)} translated | '
          f'errors {len(err)} | warnings {len(warn)} | to read {len(note)}')
    for e in err:
        print('  ERR  ' + e)
    for w in warn:
        print('  warn ' + w)
    for n in note:
        print('  read ' + n)
    return len(err)


if __name__ == '__main__':
    bad = 0
    if '--pack' in sys.argv and sys.argv[sys.argv.index('--pack') + 1] == 'all':
        for pid in lib.ready_ids():
            r = lib.as_draft(lib.rows(pid))
            if any(x.get('q_it') for x in r):
                bad += check(r, pid)
    else:
        rows, label = lib.rows_from_argv(sys.argv)
        bad = check(rows, label)
    sys.exit(1 if bad else 0)
