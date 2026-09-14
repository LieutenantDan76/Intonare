"""Seal a draft: stamp each row's stem so a later edit to it cannot go unnoticed.

The omega read keeps finding the same fault, and it is not a matter of taste.
On the Bass pack, three questions had options that had stopped answering their
own stems: "The fretless solo does what in its second half?" was rewritten to
"How did the engineers make it?" and the options were left reading "repeats the
first half backwards". Every audit passed. The question was nonsense.

Two more were caught the same way in later packs. The rule that falls out of it
is in QUIZ_VOICE.md: **when a stem changes, its options and its blurb are
stale.** That is bookkeeping, so it can be a gate that never cries wolf, unlike
the three taste detectors that were built and thrown away.

How it works. Sealing writes `sq` into each row, a short hash of the English and
Italian stems together. `intonare_draft_check.py` recomputes it and errors on
any row where the stem has moved since. Change a stem afterward and the row
fails until somebody reads the whole question again and re-seals it.

    python3 intonare_pack_seal.py draft.json            # seal rows you have read
    python3 intonare_pack_seal.py draft.json --status   # what is sealed, stale, new
    python3 intonare_pack_seal.py draft.json --rows 1-24

Seal a tier once you have read it, not while you are still writing it. Sealing
everything at the end defeats the point: the seal is a record that somebody read
the row whole, and a blanket stamp records nothing.

`sq` never reaches Intonare.html. The builder strips it, because it is build
bookkeeping and the draft JSON is where it belongs.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intonare_quiz_lib as lib


def parse_rows(spec, n):
    """1-24, or 3,7,9, or 1-10,15."""
    out = set()
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-')
            out |= set(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return {i for i in out if 1 <= i <= n}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    if not args:
        print(__doc__)
        return 0
    path = args[0]
    if not os.path.exists(path):
        sys.exit(path + ' not found')
    rows = json.load(open(path, encoding='utf-8'))

    stale, unsealed = lib.stale_rows(rows)
    sealed = len(rows) - len(unsealed)

    if '--status' in sys.argv or len(sys.argv) == 2:
        print(f'{path}: {len(rows)} rows')
        print(f'  sealed and holding  {sealed - len(stale)}')
        print(f'  STEM CHANGED        {len(stale)}'
              + (f'   rows {stale}' if stale else ''))
        print(f'  never sealed        {len(unsealed)}'
              + (f'   rows {unsealed}' if len(unsealed) <= 30 else ''))
        if stale:
            print()
            print('  A changed stem means the options and the blurb are stale.')
            print('  Read the whole question again, fix what no longer follows,')
            print('  then re-seal just those rows:')
            print(f'    python3 intonare_pack_seal.py {path} --rows '
                  + ','.join(str(i) for i in stale))
            for i in stale:
                print(f'\n  [{i}] {rows[i-1].get("q","")}')
                for o in rows[i-1].get('opts') or []:
                    print(f'        - {o}')
                if rows[i-1].get('fact'):
                    print(f'        blurb: {rows[i-1]["fact"][:90]}')
        return 1 if stale else 0

    which = (parse_rows(sys.argv[sys.argv.index('--rows') + 1], len(rows))
             if '--rows' in sys.argv else set(range(1, len(rows) + 1)))

    changed = []
    for i, r in enumerate(rows, 1):
        if i not in which:
            continue
        h = lib.stem_hash(r)
        if r.get('sq') != h:
            changed.append(i)
            r['sq'] = h

    json.dump(rows, open(path, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'{path}: sealed {len(changed)} row(s) of {len(which)} selected')
    if changed and len(changed) <= 40:
        print('  ' + ', '.join(str(i) for i in changed))
    if len(which) == len(rows) and len(changed) > 30:
        print('\n  You sealed most of the pack in one go. That is fine after an')
        print('  omega read and meaningless before one: the seal records that')
        print('  somebody read the row whole.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
