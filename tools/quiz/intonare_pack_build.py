"""Put a drafted pack into a copy of Intonare.html, then read it back and prove
it landed.

The spec's own discipline is "read every edit back out of the shipped file
before reporting it done", and it is there because three separate fixes silently
failed in one session and were nearly reported as complete: two on whitespace
inside an option array, one because the answer-spread step had rotated the
options since the string was written. A fourth appended a comma next to an
existing one and left a sparse array hole, so the pack counted 91 while the
filters saw 90.

`assert count == 1` catches a miss. It does not catch a script that asserts on
one substitution, applies it, then throws on the next and writes nothing.

So this does not trust itself. After writing, it parses the written file back
through the same loader the audits use and compares every field of every row
against the draft JSON. A mismatch is an error and, on --install, nothing is
written to the real file at all.

    python3 intonare_pack_build.py draft.json --pack bass
        -> %TEMP%/intonare_draft.html (or --out path), for HTML tools via INTONARE_HTML

    python3 intonare_pack_build.py draft.json --pack bass --install
        -> writes the repo Intonare.html (lib.HTML), but only if the round trip is clean

Rows are written in house style: one line each, double-quoted, in the field
order the file already uses.
"""
import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intonare_quiz_lib as lib

FIELD_ORDER = ['q', 'q_it', 'opts', 'opts_it', 'ans', 'd', 'loc', 'vis',
               'also', 'fact', 'fact_it']

# Build bookkeeping, not app data. sq is the stem seal and lives in the draft
# JSON, which is the archive. Shipping it would put roughly 2KB of dead bytes in
# front of every user for no runtime purpose.
STRIP = {'sq'}


def js(v):
    """A JS literal. JSON escaping is valid JS escaping, and accented characters
    go through literally because the file already carries them that way."""
    s = json.dumps(v, ensure_ascii=False)
    # A closing tag inside a string would end the <script> block early.
    return s.replace('</', '<\\/')


def row_source(r, indent='    '):
    parts = []
    for k in FIELD_ORDER:
        if k in STRIP or k not in r or r[k] is None:
            continue
        parts.append(f'{k}:{js(r[k])}')
    for k in r:
        if k in FIELD_ORDER or k in STRIP:
            continue
        parts.append(f'{k}:{js(r[k])}')
    return indent + '{' + ', '.join(parts) + '}'


def find_questions_array(h, pack_id):
    """Return (start, end) of the contents inside `questions:[ ... ]`.

    Walks brackets while skipping over string literals, because an option
    reading "[sic]" or a blurb carrying a bracket would otherwise close the
    array early. Never runs a DOTALL regex over the 10MB file: a pattern
    starting [^/\\n]* rescans from every position and does not finish.
    """
    i = h.index('const PACKS')
    m = re.compile(r'\n\s{0,4}' + re.escape(pack_id) + r':\s*\{').search(h, i)
    if not m:
        sys.exit(f'no pack "{pack_id}" in PACKS')
    q = h.index('questions:', m.end())
    start = h.index('[', q) + 1
    depth, k, quote, esc = 1, start, None, False
    while depth:
        c = h[k]
        if quote:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == quote:
                quote = None
        elif c in '"\'':
            quote = c
        elif c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                break
        k += 1
    return start, k


def normalize(r):
    """Compare on content, not on shape. Draft rows put the answer at opts[0];
    installed rows put it at opts[ans]. Both are converted to a single form so
    the round trip is not comparing a rotation with itself."""
    out = {}
    for k, v in r.items():
        if k in STRIP:
            continue
        out[k] = v
    if 'ans' not in out:
        out['ans'] = 0
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args or '--pack' not in sys.argv:
        sys.exit(__doc__.strip().splitlines()[0] + '\n\n'
                 '  python3 intonare_pack_build.py draft.json --pack <id> [--install]')
    src = args[0]
    pack_id = sys.argv[sys.argv.index('--pack') + 1]
    install = '--install' in sys.argv
    if install:
        out = lib.HTML
    elif '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
    else:
        out = os.path.join(tempfile.gettempdir(), 'intonare_draft.html')

    draft = json.load(open(src, encoding='utf-8'))
    if not draft:
        sys.exit('no rows in ' + src)

    # Draft shape (answer first) becomes shipped shape (answer at ans). Doing
    # this here and nowhere else means the answer index is written once.
    shipped = []
    for r in draft:
        row = dict(r)
        if 'ans' not in row:
            row['ans'] = 0
        shipped.append(row)

    h = open(lib.HTML, encoding='utf-8').read()
    a, b = find_questions_array(h, pack_id)
    body = '\n' + ',\n'.join(row_source(r) for r in shipped) + '\n  '
    written = h[:a] + body + h[b:]

    if install:
        shutil.copy(lib.HTML, lib.HTML + '.bak')
    open(out, 'w', encoding='utf-8').write(written)

    # ── the round trip ──────────────────────────────────────────────────────
    back = lib.rows(pack_id, out)
    bad = []
    if len(back) != len(shipped):
        bad.append(f'row count: wrote {len(shipped)}, read back {len(back)}')
    for i, (want, got) in enumerate(zip(shipped, back), 1):
        w, g = normalize(want), normalize(got)
        for k in set(w) | set(g):
            if w.get(k) != g.get(k):
                bad.append(f'{i}: field "{k}" differs\n'
                           f'      wrote: {w.get(k)!r}\n'
                           f'      read:  {g.get(k)!r}')

    print(f'{pack_id}: {len(shipped)} rows -> {out}')
    if bad:
        print(f'  ROUND TRIP FAILED, {len(bad)} difference(s):')
        for x in bad[:20]:
            print('    ' + x)
        if install:
            shutil.move(lib.HTML + '.bak', lib.HTML)
            print('  the real file was restored and nothing was installed.')
        sys.exit(1)

    print('  round trip clean: every field read back exactly as written.')
    if install:
        os.remove(lib.HTML + '.bak')
        print('  installed. Run the ship gate before bumping the version.')
    else:
        print(f'  now run the HTML tools against it:\n'
              f'    INTONARE_HTML={out} python3 intonare_pack_faults.py {pack_id}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
