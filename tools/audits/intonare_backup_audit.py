#!/usr/bin/env python3
"""
Intonare Backup Coverage Audit
==============================
Asserts that every key Intonare persists is classified for backup.

Why this exists: a backup feature fails silently. Add a localStorage key next
year, forget to add it to a list, and nothing breaks; users just quietly lose
that data when they change phones, and nobody finds out for months. This walks
the file for every persisted key and every progState field, and fails if any of
them is not accounted for in one of the BACKUP_* lists.

It does NOT check that the classification is *correct* (that is a judgement
call, recorded in BACKUP_LEDGER.md). It checks that a decision was made.

Usage:
    python3 intonare_backup_audit.py Intonare.html

Exit 0 = every key classified. Non-zero = something is unclassified.
"""

import re
import sys
import argparse

# Keys written through a const identifier rather than a literal. A grep for
# quoted strings never sees these, which is exactly how intonare_dk_saves
# (saved drum patterns) nearly ended up absent from every backup.
CONST_KEYS = ['PROG_STORAGE_KEY', 'APPEARANCE_KEY', 'DARK_DEPTH_KEY',
              'DK_CUSTOM_KEY', 'DK_SAVES_KEY', 'LIGHT_BRIGHT_KEY']


def js_list(text, name):
    """Pull a flat JS array of string literals out of the file by name."""
    m = re.search(r'const\s+' + name + r'\s*=\s*\[(.*?)\]', text, re.S)
    if not m:
        return None
    body = m.group(1)
    lits = re.findall(r"'([^']*)'", body)
    # Entries can also be const identifiers (PROG_STORAGE_KEY); hand those back
    # with a marker so the caller can resolve them to their literal values.
    idents = re.findall(r'(?<![\'\w])([A-Z_][A-Z0-9_]{2,})(?![\'\w])', body)
    return lits + ['@' + i for i in idents]


def run(path):
    text = open(path, encoding='utf-8').read()
    vm = re.search(r'INTONARE_VERSION:\s*([0-9.]+)', text)
    print(f"\n{'='*70}\n  INTONARE BACKUP COVERAGE — v{vm.group(1) if vm else '??'}\n{'='*70}")

    lists = {}
    for name in ('BACKUP_KEYS_PROGRESS', 'BACKUP_KEYS_SETTINGS', 'BACKUP_KEYS_SKIP',
                 'BACKUP_PREFIX_TAKE', 'BACKUP_PREFIX_SKIP', 'BACKUP_PROG_EXCLUDE'):
        got = js_list(text, name)
        if got is None:
            print(f"  \u2717 {name} is missing from the file entirely.")
            return 2
        lists[name] = got

    # Resolve const-referenced key names to their literal values.
    const_vals = {}
    for c in CONST_KEYS:
        m = re.search(r"const\s+" + c + r"\s*=\s*'([^']*)'", text)
        if m:
            const_vals[c] = m.group(1)

    # Every persisted key: literals plus resolved consts.
    literals = set(re.findall(r"localStorage\.(?:setItem|getItem|removeItem)\('([^']*)'", text))
    referenced = set(re.findall(r"localStorage\.(?:setItem|getItem|removeItem)\(([A-Z_][A-Z0-9_]*)", text))
    for r in referenced:
        if r in const_vals:
            literals.add(const_vals[r])
        else:
            print(f"  \u26a0  localStorage key via unresolved const {r}; add it to CONST_KEYS.")

    # Resolve any '@IDENT' entries the lists carried.
    for name, vals in lists.items():
        out = []
        for v in vals:
            if v.startswith('@'):
                if v[1:] in const_vals:
                    out.append(const_vals[v[1:]])
                else:
                    print(f"  \u26a0  {name} references unknown const {v[1:]}.")
            else:
                out.append(v)
        lists[name] = out

    prefixes = set(lists['BACKUP_PREFIX_TAKE']) | set(lists['BACKUP_PREFIX_SKIP'])
    classified = (set(lists['BACKUP_KEYS_PROGRESS']) | set(lists['BACKUP_KEYS_SETTINGS'])
                  | set(lists['BACKUP_KEYS_SKIP']))

    unclassified = []
    for k in sorted(literals):
        if k in classified:
            continue
        if k in prefixes:            # the prefix itself, e.g. 'pref_'
            continue
        if any(k.startswith(p) for p in prefixes):
            continue
        unclassified.append(k)

    print(f"\n  KEYS")
    print(f"    persisted        {len(literals)}")
    print(f"    progress         {len(lists['BACKUP_KEYS_PROGRESS'])}")
    print(f"    settings         {len(lists['BACKUP_KEYS_SETTINGS'])}")
    print(f"    skipped          {len(lists['BACKUP_KEYS_SKIP'])}")
    print(f"    prefix families  {len(prefixes)}  ({', '.join(sorted(prefixes))})")

    # progState fields must each be exported or explicitly excluded. The default
    # object is the source of truth for what fields exist.
    m = re.search(r'const PROG_DEFAULTS = \{(.*?)\n\};', text, re.S)
    fields = re.findall(r'^\s{2}([A-Za-z_][A-Za-z0-9_]*)\s*:', m.group(1), re.M) if m else []
    excluded = set(lists['BACKUP_PROG_EXCLUDE'])
    print(f"\n  progState")
    print(f"    fields           {len(fields)}")
    print(f"    excluded         {len(excluded)}  ({', '.join(sorted(excluded))})")

    missing_exclude = [e for e in excluded if e not in fields]

    # The reset keep-list is the other consumer of the same field names; a typo
    # there is silent (the field just is not preserved), so check it too.
    keep = js_list(text, 'PROG_KEEP_ON_RESET') or []
    missing_keep = [k for k in keep if k not in fields]
    print(f"    kept on reset    {len(keep)}")

    # The entitlement guard is the one that matters most; assert it by name.
    hard = []
    if 'hasPro' not in excluded:
        hard.append("hasPro is NOT excluded — a hand-edited backup would grant Pro.")
    if 'tapOffsetMs' not in excluded:
        hard.append("tapOffsetMs is NOT excluded — device calibration would travel.")
    if keep and 'hasPro' not in keep:
        hard.append("hasPro is NOT in PROG_KEEP_ON_RESET — reset would revoke a purchase.")

    print(f"\n{'='*70}")
    ok = True
    if unclassified:
        ok = False
        print(f"  \u26a0  {len(unclassified)} persisted key(s) not classified for backup:")
        for k in unclassified:
            print(f"     \u2717 {k}")
        print("     Add each to BACKUP_KEYS_PROGRESS, _SETTINGS or _SKIP.")
    if missing_keep:
        ok = False
        print(f"  \u26a0  PROG_KEEP_ON_RESET names field(s) PROG_DEFAULTS does not have:")
        for k in missing_keep:
            print(f"     \u2717 {k}  (it will not be preserved across a reset)")
    if missing_exclude:
        ok = False
        print(f"  \u26a0  BACKUP_PROG_EXCLUDE names field(s) progState does not have:")
        for e in missing_exclude:
            print(f"     \u2717 {e}  (renamed or removed? the exclusion is now a no-op)")
    for msg in hard:
        ok = False
        print(f"  \u2717 {msg}")

    if ok:
        print(f"  \u2713 All {len(literals)} persisted keys and {len(fields)} progState fields classified.")
    print(f"{'='*70}\n")
    return 0 if ok else 1


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Intonare backup coverage audit')
    p.add_argument('filepath', help='Path to Intonare.html')
    sys.exit(run(p.parse_args().filepath))
