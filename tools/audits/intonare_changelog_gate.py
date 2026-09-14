#!/usr/bin/env python3
"""
intonare_changelog_gate.py — ship gate for CHANGELOG.md

Two failures this catches, both of which happened for real:

  1. NEWEST AT TOP. The file's own header says so. Entries were appended to the
     BOTTOM for nine consecutive versions, so the top of the file still advertised
     a version from before the session started. Nobody reading it would have known.

  2. TOP ENTRY MATCHES THE SHIPPED VERSION. A version bump in Intonare.html with no
     matching changelog entry means the log silently falls behind the build.

Usage:
    python3 intonare_changelog_gate.py [Intonare.html] [CHANGELOG.md]

Exits non-zero on failure, so it can sit in the ship gate next to the sentinel.
"""

import re
import sys
from pathlib import Path


def parse_versions(changelog_text):
    """Return [(version_tuple, raw_string, line_no)] in the order they appear."""
    out = []
    for i, line in enumerate(changelog_text.splitlines(), 1):
        m = re.match(r'^## v(\d+(?:\.\d+)*)', line)
        if m:
            raw = m.group(1)
            out.append((tuple(int(x) for x in raw.split('.')), raw, i))
    return out


def main():
    html_path = Path(sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html')
    log_path = Path(sys.argv[2] if len(sys.argv) > 2 else 'CHANGELOG.md')

    if not html_path.exists():
        print(f"  ✗ {html_path} not found")
        return 1
    if not log_path.exists():
        print(f"  ✗ {log_path} not found")
        return 1

    html = html_path.read_text(encoding='utf-8', errors='replace')
    log = log_path.read_text(encoding='utf-8', errors='replace')

    print("=" * 70)
    print("  CHANGELOG GATE")
    print("=" * 70)

    fails = 0

    # ── the version being shipped ──────────────────────────────────────────
    m = re.search(r"const INTONARE_VERSION = '([\d.]+)'", html)
    if not m:
        print("  ✗ could not read INTONARE_VERSION const from the HTML")
        return 1
    shipped = m.group(1)

    # the HTML comment on line 4 must agree with the const (the two-spot bump)
    m2 = re.search(r'<!-- INTONARE_VERSION: ([\d.]+) -->', html)
    if not m2:
        print("  ✗ could not read the INTONARE_VERSION HTML comment")
        fails += 1
    elif m2.group(1) != shipped:
        print(f"  ✗ version mismatch INSIDE the HTML: "
              f"comment says {m2.group(1)}, const says {shipped}")
        fails += 1
    else:
        print(f"  ✓ HTML version stamps agree: v{shipped}")

    # ── entries ────────────────────────────────────────────────────────────
    versions = parse_versions(log)
    if not versions:
        print("  ✗ no '## vX.Y.Z' entries found in the changelog")
        return 1
    print(f"  · {len(versions)} entries found")

    # 1. NEWEST AT TOP — the file's header says so; enforce it.
    ordered = sorted(versions, key=lambda v: v[0], reverse=True)
    if [v[1] for v in versions] != [v[1] for v in ordered]:
        print("  ✗ ENTRIES ARE NOT NEWEST-FIRST. The header says 'newest at top'.")
        # Report only the ACTUAL inversions (an entry newer than the one above it),
        # not every downstream entry the shift knocked out of position — one
        # misplaced entry otherwise reports as fifty-seven failures.
        for i in range(1, len(versions)):
            prev_v, prev_raw, _ = versions[i - 1]
            cur_v, cur_raw, cur_line = versions[i]
            if cur_v > prev_v:
                print(f"      line {cur_line}: v{cur_raw} sits BELOW v{prev_raw} "
                      f"— it is newer and belongs above it")
        print("    Prepend new entries; do NOT append them to the bottom.")
        fails += 1
    else:
        print("  ✓ entries are newest-first")

    # 2. duplicates
    seen = {}
    for tup, raw, line in versions:
        seen.setdefault(raw, []).append(line)
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    if dupes:
        for raw, lines in dupes.items():
            print(f"  ✗ v{raw} appears {len(lines)}x (lines {lines})")
        fails += 1
    else:
        print("  ✓ no duplicate version entries")

    # 3. the top entry must be the version being shipped
    top_raw = versions[0][1]
    if top_raw != shipped:
        print(f"  ✗ TOP ENTRY IS v{top_raw} BUT THE BUILD IS v{shipped}")
        print("    Every ship needs a changelog entry, prepended, before it goes out.")
        fails += 1
    else:
        print(f"  ✓ top entry matches the shipped build (v{shipped})")

    print("=" * 70)
    if fails:
        print(f"  ✗ CHANGELOG GATE FAILED ({fails} problem"
              f"{'s' if fails != 1 else ''}). Do not ship.")
        return 1
    print("  ✓ CHANGELOG GATE PASSED.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
