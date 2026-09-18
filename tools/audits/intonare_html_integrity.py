#!/usr/bin/env python3
"""
Intonare.html integrity gate
============================
Catches the "rogue editor" failure mode: a tool reports success but the
file silently shrinks (truncate) or has its CRLF line endings stripped to
LF (Windows read_text → write_text / write_bytes of a text-decoded string).

Either one leaves the app looking half-broken. Cursor rules already say
stop-and-restore; this script makes ship_check fail hard so a bad copy
cannot ride out as "green."

Usage:
    python tools/audits/intonare_html_integrity.py [Intonare.html]

Exit 0 = ok. Non-zero = do not ship; restore from git and re-patch.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Floor: real file is ~12.2 MB. Truncate disasters land ~8 MB. CRLF→LF alone
# drops ~140 KB and still clears a soft floor, so we also compare to HEAD.
MIN_BYTES = 11_000_000
# A small intentional patch is hundreds of bytes to a few KB. CRLF→LF is
# ~130–150 KB. Truncate is megabytes. Fail if working tree is this much
# smaller than HEAD for Intonare.html.
MAX_SHRINK_VS_HEAD = 80_000
# Brace balance can drift a few counts across edits; huge imbalance means
# a half-written CSS/JS block.
MAX_BRACE_IMBALANCE = 20


def _git_head_size(repo: Path, rel: str) -> int | None:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo), "show", f"HEAD:{rel}"],
            capture_output=True,
            check=False,
        )
        if r.returncode != 0:
            return None
        return len(r.stdout)
    except OSError:
        return None


def check(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing file: {path}"]

    data = path.read_bytes()
    size = len(data)

    if size < MIN_BYTES:
        errors.append(
            f"size {size:,} bytes is under floor {MIN_BYTES:,} "
            f"(likely truncate; restore Intonare.html from git)"
        )

    if not data.rstrip().endswith(b"</html>"):
        errors.append("file does not end with </html> (truncated or corrupt write)")

    crlf = data.count(b"\r\n")
    lf_only = data.count(b"\n") - crlf
    head_size = _git_head_size(path.parent, path.name)
    if head_size is not None and size + MAX_SHRINK_VS_HEAD < head_size:
        drop = head_size - size
        hint = ""
        if crlf < 1000 and lf_only > 50_000:
            hint = (
                " (looks like CRLF→LF rewrite: use tools/patch_intonare.py, "
                "not read_text/write_text)"
            )
        elif drop > 500_000:
            hint = " (looks like truncate)"
        errors.append(
            f"size dropped {drop:,} bytes vs HEAD ({head_size:,} → {size:,})"
            f"{hint}. Restore: git checkout -- Intonare.html"
        )

    brace = data.count(b"{") - data.count(b"}")
    if abs(brace) > MAX_BRACE_IMBALANCE:
        errors.append(
            f"brace imbalance {{ vs }} = {brace} "
            f"(limit ±{MAX_BRACE_IMBALANCE}); likely a half-eaten CSS/JS edit"
        )

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "html",
        nargs="?",
        default="Intonare.html",
        help="path to Intonare.html (default: ./Intonare.html)",
    )
    args = ap.parse_args()
    path = Path(args.html)
    if not path.is_absolute():
        path = Path.cwd() / path

    errs = check(path)
    if errs:
        print(f"FAIL: {path}")
        for e in errs:
            print(f"  - {e}")
        print(
            "\nDo not ship. Restore the file, then re-apply with "
            "tools/patch_intonare.py (bytes-safe)."
        )
        return 1

    data = path.read_bytes()
    crlf = data.count(b"\r\n")
    brace = data.count(b"{") - data.count(b"}")
    print(
        f"OK: {path.name}  size={len(data):,}  crlf={crlf}  "
        f"ends=</html>  brace_diff={brace}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
