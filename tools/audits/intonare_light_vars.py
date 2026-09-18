# -*- coding: utf-8 -*-
"""
Broad light-mode visual audit — not just blooms.

Buckets:
  A) Theme tokens: body.light.theme-* must declare core ramp vars
  B) JS style writers: color/background/fill/stroke/border/filter/shadow
     without a nearby light gate
  C) Hardcoded near-black / neon hex in CSS rules that are NOT under
     body.light / keep-dark / @keyframes-only contexts (heuristic)
  D) setProperty of color-ish custom props

Read-only report.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

text = Path("Intonare.html").read_bytes().decode("utf-8")
lines = text.splitlines()

CORE_TOKENS = [
    "--bg-0", "--bg-1", "--surface", "--surface-2", "--panel",
    "--border", "--border-soft", "--accent", "--tab-accent",
    "--accent-fill", "--text", "--text-dim", "--muted",
]

print("=" * 60)
print("A) THEME TOKEN COVERAGE (body.light.theme-*)")
print("=" * 60)
for theme in ("tuner", "metro", "tools", "train"):
    # find ramp block with --bg-0
    key = f"body.light.theme-{theme}"
    idx = 0
    block = ""
    while True:
        i = text.find(key, idx)
        if i < 0:
            break
        snip = text[i : i + 1200]
        if "--bg-0" in snip:
            block = snip
            break
        idx = i + 1
    missing = [t for t in CORE_TOKENS if t not in block]
    print(f"  theme-{theme}: {'PASS' if not missing else 'MISSING ' + ','.join(missing)}")

print()
print("=" * 60)
print("B) JS INLINE STYLE WRITERS (ungated heuristic)")
print("=" * 60)
# style.PROP = ... where PROP is visual
js_pat = re.compile(
    r"""\.style\.(color|background|backgroundColor|fill|stroke|borderColor|border|opacity|filter|boxShadow|textShadow|outline)\s*="""
)
setprop_pat = re.compile(r"""\.style\.setProperty\(\s*['\"]([^'\"]+)['\"]""")

ungated = []
gated_n = 0
for i, line in enumerate(lines, 1):
    m = js_pat.search(line) or setprop_pat.search(line)
    if not m:
        continue
    # skip clears
    if re.search(r"""=\s*(''|\"\"|'none'|\"none\")""", line):
        continue
    window = "\n".join(lines[max(0, i - 18) : min(len(lines), i + 2)])
    gated = bool(
        re.search(r"contains\(['\"]light['\"]\)", window)
        or re.search(r"\b(_dl|_dbLight|_wLight|_lt|_prL|_pianoLight|_sgL|_msL|_rrL|_cofLight|_tpLight|_stLight|_phLight|_nkLight)\b", window)
        or re.search(r"\bisDark\b|\blight\s*\?|_prL\b", window)
    )
    if gated:
        gated_n += 1
        continue
    prop = m.group(1) if m.lastindex else "?"
    # skip pure layout transforms
    ungated.append((i, prop, line.strip()[:120]))

# Summarize by prop
by_prop = defaultdict(list)
for i, prop, s in ungated:
    by_prop[prop].append((i, s))

print(f"  gated-ish writes (approx): {gated_n}")
print(f"  ungated visual writes: {len(ungated)}")
for prop in sorted(by_prop, key=lambda p: -len(by_prop[p])):
    items = by_prop[prop]
    print(f"\n  .{prop}  ({len(items)})")
    for i, s in items[:12]:
        print(f"    L{i}: {s}")
    if len(items) > 12:
        print(f"    ... +{len(items)-12} more")

print()
print("=" * 60)
print("C) HARDCODED DARK / NEON IN GLOBAL CSS (sample)")
print("=" * 60)
# Heuristic: lines with near-black or classic neon that are NOT body.light / keep-dark
DARK_HEX = re.compile(
    r"#0[0-9a-fA-F]{5}|#1[0-2][0-9a-fA-F]{4}|rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\.[5-9]"
)
NEON = re.compile(
    r"#5ee2ff|#b6f25b|#b8a3ff|#ffa07a|#34d399|rgba\(\s*182\s*,\s*242\s*,\s*91|rgba\(\s*52\s*,\s*211\s*,\s*153|rgba\(\s*94\s*,\s*226\s*,\s*255",
    re.I,
)

dark_hits = []
neon_hits = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped or stripped.startswith("/*") or stripped.startswith("*"):
        continue
    # skip body.light lines and keep-dark blocks (weak)
    prev = "\n".join(lines[max(0, i - 25) : i])
    if "body.light" in line or "body.light" in prev[-200:]:
        continue
    if ".keep-dark" in prev or "keep-dark" in line:
        continue
    if DARK_HEX.search(line) and ("background" in line or "color:" in line or "fill:" in line or "stroke:" in line):
        dark_hits.append((i, stripped[:110]))
    if NEON.search(line) and ("box-shadow" in line or "text-shadow" in line or "filter:" in line or "drop-shadow" in line):
        neon_hits.append((i, stripped[:110]))

print(f"  near-black paints (not obviously light-scoped): {len(dark_hits)}")
for i, s in dark_hits[:25]:
    print(f"    L{i}: {s}")
if len(dark_hits) > 25:
    print(f"    ... +{len(dark_hits)-25} more")

print(f"\n  neon emission on non-light lines: {len(neon_hits)}")
for i, s in neon_hits[:20]:
    print(f"    L{i}: {s}")
if len(neon_hits) > 20:
    print(f"    ... +{len(neon_hits)-20} more")

print()
print("=" * 60)
print("D) setProperty color-ish custom props")
print("=" * 60)
for i, line in enumerate(lines, 1):
    m = re.search(r"setProperty\(\s*['\"](--[^'\"]+)['\"]", line)
    if not m:
        continue
    name = m.group(1)
    if any(k in name for k in ("color", "glow", "bg", "accent", "theme", "fill", "stroke", "tg", "tc", "shadow")):
        window = "\n".join(lines[max(0, i - 10) : i + 1])
        gated = "light" in window.lower()
        flag = "gated?" if gated else "CHECK"
        print(f"  {flag} L{i}: {name}  |  {line.strip()[:90]}")

print()
print("DONE — this is coverage of writers/tokens, not a pixel QA of every screen.")
