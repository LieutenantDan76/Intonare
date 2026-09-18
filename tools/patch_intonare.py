#!/usr/bin/env python3
"""
Bytes-safe Intonare.html patcher
================================
The Windows failure mode: Path.read_text() turns CRLF into \\n in memory,
then write_bytes(text.encode()) writes LF-only and silently drops ~140 KB.
Editors can also truncate. This helper never does either.

Usage (from repo root):
    python tools/patch_intonare.py --old "unique old" --new "replacement"
    python tools/patch_intonare.py --pair tools/_pair.json   # list of {old,new}

Each old string must match exactly once (after the same newline style as the
file). Exit non-zero on ambiguity, missing match, or post-write integrity fail.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as `python tools/patch_intonare.py` from repo root.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "audits"))
from intonare_html_integrity import MAX_SHRINK_VS_HEAD, check  # noqa: E402


def _to_file_newlines(s: str, data: bytes) -> bytes:
    """Encode patch text using the file's dominant newline."""
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    body = s.replace("\r\n", "\n").replace("\r", "\n")
    if crlf >= lf:
        return body.replace("\n", "\r\n").encode("utf-8")
    return body.encode("utf-8")


def apply_pairs(path: Path, pairs: list[tuple[str, str]]) -> None:
    data = path.read_bytes()
    size0 = len(data)

    for i, (old, new) in enumerate(pairs, 1):
        ob = _to_file_newlines(old, data)
        nb = _to_file_newlines(new, data)
        n = data.count(ob)
        if n != 1:
            raise SystemExit(
                f"pair {i}: expected exactly 1 match, got {n}. "
                f"old starts: {old[:80]!r}"
            )
        data = data.replace(ob, nb, 1)

    size1 = len(data)
    if size1 + MAX_SHRINK_VS_HEAD < size0:
        raise SystemExit(
            f"refusing write: size would drop {size0 - size1:,} bytes "
            f"({size0:,} → {size1:,}). Not writing."
        )
    if not data.rstrip().endswith(b"</html>"):
        raise SystemExit("refusing write: result would not end with </html>")

    path.write_bytes(data)

    errs = check(path)
    if errs:
        raise SystemExit(
            "wrote file but integrity check failed:\n  - "
            + "\n  - ".join(errs)
            + "\nRestore: git checkout -- Intonare.html"
        )

    print(f"OK: patched {path.name}  {size0:,} -> {size1:,}  (delta {size1 - size0:+,})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--file",
        default=str(ROOT / "Intonare.html"),
        help="path to Intonare.html",
    )
    ap.add_argument("--old", help="exact old string (use with --new)")
    ap.add_argument("--new", help="exact new string (use with --old)")
    ap.add_argument(
        "--pair",
        help="JSON file: [{\"old\":\"...\",\"new\":\"...\"}, ...]",
    )
    args = ap.parse_args()
    path = Path(args.file)

    pairs: list[tuple[str, str]] = []
    if args.pair:
        raw = json.loads(Path(args.pair).read_text(encoding="utf-8"))
        for row in raw:
            pairs.append((row["old"], row["new"]))
    elif args.old is not None and args.new is not None:
        pairs.append((args.old, args.new))
    else:
        ap.error("provide --old/--new or --pair")

    apply_pairs(path, pairs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
