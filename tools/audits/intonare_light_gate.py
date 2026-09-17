#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
intonare_light_gate.py — definitive light-mode leftover scanner (v1)

Stops the hex-hunt loop. Static by default; optional live walk with Playwright
when installed (`pip install playwright` && `playwright install chromium`).

What it finds
  NEON      Dark-stage accent hexes still painted outside keep-dark / intentional
            light ink overrides (the #5ee2ff / #6ef0ff class of leftovers).
  WASH      Near-white / near-black at tiny alpha (dark-mode glass that vanishes
            or muddies on light grounds).
  ROLE      Content surfaces that alias page stage (--bg-0 / --bg) as text ground
            without a body.light remap (Survival Guide class of bug).
  LIVE      Optional: open each Tools screen in light, sample visible text vs
            ancestor background, report WCAG AA fails (<4.5:1 body, <3:1 large).

Usage (repo root):
  python tools/audits/intonare_light_gate.py
  python tools/audits/intonare_light_gate.py Intonare.html
  python tools/audits/intonare_light_gate.py --live http://127.0.0.1:8899/Intonare.html
  set INTONARE_HTML=...  (same as other audits)

Exit 0 always for v1 (report, do not block ship yet). Print ranked fix list.
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_HTML = Path(os.environ.get("INTONARE_HTML", str(ROOT / "Intonare.html")))
REPORT_PATH = ROOT / "tools" / "prototypes" / "light-mode" / "GATE_LAST.md"

# Dark-stage accents that read as neon chalk on light mint/sage/cream.
NEON_HEX = {
    "5ee2ff", "6ef0ff", "7aafff", "b6f25b", "34d399", "06b6d4",
    "ffd166", "ffa07a", "ff8aae", "b8a3ff", "60a5fa", "4ade80",
    "a3e635", "22d3ee", "2dd4bf", "f472b6", "c084fc", "a78bfa",
    "67e8f9", "86efac", "fde047", "fb923c",
}

# RGB forms of the worst offenders (inline styles / JS).
NEON_RGB = [
    (94, 226, 255),   # #5ee2ff
    (110, 240, 255),  # #6ef0ff
    (122, 175, 255),  # #7aafff
    (182, 242, 91),   # #b6f25b
    (52, 211, 153),   # #34d399
]

TOOLS_LIVE = [
    ("piano", "toolPiano"),
    ("tonal", "toolTonal"),
    ("theremin", "toolTheremin"),
    ("guitarchords", "toolGuitarChords"),
    ("chords", "toolChords"),
    ("progression", "toolProgression"),
    ("drumkit", "toolDrumkit"),
    ("rhythmcards", "toolRhythmCards"),
    ("cof", "toolCof"),
    ("intervalref", "toolIntervalRef"),
    ("vocalrange", "toolVocalRange"),
    ("scales", "exScales"),
    ("survivalguide", "toolSurvivalGuide"),
    ("volume", "toolVolume"),
    ("transpose", "toolTranspose"),
]

HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
RGB_RE = re.compile(
    r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})"
    r"(?:\s*,\s*(0?\.\d+|1(?:\.0+)?|\d*\.?\d+))?\s*\)",
    re.I,
)


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def snippet(text: str, idx: int, radius: int = 70) -> str:
    a = max(0, idx - radius)
    b = min(len(text), idx + radius)
    s = text[a:b].replace("\n", " ")
    return re.sub(r"\s+", " ", s).strip()


def expand_hex(h: str) -> str:
    h = h.lower()
    if len(h) == 3:
        return "".join(c * 2 for c in h)
    return h


def classify_context(text: str, idx: int) -> str:
    """
    Bucket a neon hit so dark theme tokens are not treated as light bugs.

      dark-token  --accent:#5ee2ff in :root / theme blocks (expected; body.light redefines)
      keep-dark   intentional dark island
      body.light  already under a light override (may still be wrong neon ink)
      draw/js     canvas / fillStyle / setProperty
      leak        component CSS paint that still applies on light unless overridden
    """
    window = text[max(0, idx - 1600) : idx]
    low = window.lower()
    left = text[max(0, idx - 100) : idx]
    head = text[max(0, idx - 80) : idx + 40]

    if "keep-dark" in low:
        return "keep-dark"

    # Custom property: --accent: #5ee2ff  or  --grad: linear-gradient(..., #5ee2ff
    if re.search(r"--[\w-]+\s*:\s*[^;{]*$", left):
        return "dark-token"
    if "@property" in low[-200:]:
        return "dark-token"

    brace = window.rfind("{")
    if brace >= 0:
        sel_chunk = window[max(0, brace - 240) : brace]
        sel_chunk = re.sub(r"/\*.*?\*/", " ", sel_chunk, flags=re.S)
        sel_line = sel_chunk.strip().split("\n")[-1].strip().lower()
        if "body.light" in sel_line or sel_line.startswith("html.light"):
            return "body.light"
        if "keep-dark" in sel_line:
            return "keep-dark"

    if any(k in head for k in ("fillStyle", "strokeStyle", "setProperty", "ctx.")):
        return "draw/js"
    if re.search(r"""['"]fill['"]\s*:|fill\s*=\s*['"]#|stroke\s*=\s*['"]#""", head):
        return "draw/js"

    return "leak"


def selector_for_hit(text: str, idx: int) -> str:
    window = text[max(0, idx - 1600) : idx]
    brace = window.rfind("{")
    if brace < 0:
        return ""
    sel_chunk = window[max(0, brace - 280) : brace]
    sel_chunk = re.sub(r"/\*.*?\*/", " ", sel_chunk, flags=re.S)
    return sel_chunk.strip().split("\n")[-1].strip()


def has_light_override(text: str, selector: str) -> bool:
    """True if body.light mentions a key id/class from this selector."""
    if not selector:
        return False
    keys = re.findall(r"#[A-Za-z][\w-]+|\.[A-Za-z][\w-]+", selector)
    for key in reversed(keys[-4:]):
        if len(key) < 4:
            continue
        if re.search(rf"body\.light[^{{]*{re.escape(key)}", text):
            return True
    return False


def scan_neon(text: str) -> list[dict]:
    hits = []
    for m in HEX_RE.finditer(text):
        hx = expand_hex(m.group(1))
        if hx not in NEON_HEX:
            continue
        ctx = classify_context(text, m.start())
        sel = selector_for_hit(text, m.start()) if ctx == "leak" else ""
        if ctx == "leak" and has_light_override(text, sel):
            ctx = "leak-ok"
        hits.append({
            "kind": "NEON",
            "token": f"#{hx}",
            "line": line_of(text, m.start()),
            "ctx": ctx,
            "sel": sel[:80],
            "snip": snippet(text, m.start()),
        })
    for m in RGB_RE.finditer(text):
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if (r, g, b) not in NEON_RGB:
            continue
        ctx = classify_context(text, m.start())
        sel = selector_for_hit(text, m.start()) if ctx == "leak" else ""
        if ctx == "leak" and has_light_override(text, sel):
            ctx = "leak-ok"
        hits.append({
            "kind": "NEON",
            "token": f"rgb({r},{g},{b})",
            "line": line_of(text, m.start()),
            "ctx": ctx,
            "sel": sel[:80],
            "snip": snippet(text, m.start()),
        })
    return hits


def scan_wash(text: str) -> list[dict]:
    """Dark-mode glass: white or black at tiny alpha on light = vanish or mud."""
    hits = []
    for m in RGB_RE.finditer(text):
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a = m.group(4)
        if a is None:
            continue
        alpha = float(a)
        near_white = r >= 240 and g >= 240 and b >= 240
        near_black = r <= 20 and g <= 20 and b <= 20
        if near_white and 0 < alpha <= 0.08:
            ctx = classify_context(text, m.start())
            if ctx == "keep-dark":
                continue
            hits.append({
                "kind": "WASH",
                "token": m.group(0)[:48],
                "line": line_of(text, m.start()),
                "ctx": ctx,
                "snip": snippet(text, m.start()),
            })
        if near_black and 0.45 <= alpha <= 0.85:
            ctx = classify_context(text, m.start())
            if ctx in ("keep-dark", "body.light"):
                continue
            sn = snippet(text, m.start()).lower()
            if not any(k in sn for k in ("overlay", "scrim", "backdrop", "modal", "sheet")):
                continue
            hits.append({
                "kind": "WASH",
                "token": m.group(0)[:48],
                "line": line_of(text, m.start()),
                "ctx": ctx,
                "snip": snippet(text, m.start()),
            })
    return hits


def scan_role(text: str) -> list[dict]:
    """Modules that map content --bg to page stage without a light remap."""
    hits = []
    for m in re.finditer(
        r"(#tool[A-Za-z0-9_-]+|#ex[A-Za-z0-9_-]+)\s*\{[^}]{0,400}--bg\s*:\s*var\(--bg-0\)",
        text,
    ):
        sel = m.group(1)
        light = re.search(
            rf"body\.light\s+{re.escape(sel)}\s*\{{[^}}]{{0,500}}--bg\s*:",
            text,
        )
        if light:
            continue
        hits.append({
            "kind": "ROLE",
            "token": f"{sel} --bg→--bg-0",
            "line": line_of(text, m.start()),
            "ctx": "base",
            "snip": snippet(text, m.start(), 90),
        })
    return hits


def rank_neon(hits: list[dict]) -> list:
    """Rank open neon: skip keep-dark, dark-token, and leaks that already have light overrides."""
    buckets = collections.Counter()
    examples = collections.defaultdict(list)
    for h in hits:
        if h["ctx"] in ("keep-dark", "dark-token", "leak-ok"):
            continue
        key = (h["token"], h["ctx"])
        buckets[key] += 1
        if len(examples[key]) < 3:
            examples[key].append(h)
    out = []
    for (token, ctx), n in buckets.items():
        sev = 5 if ctx == "draw/js" else 4 if ctx == "leak" else 1
        out.append({
            "kind": "NEON",
            "token": token,
            "ctx": ctx,
            "count": n,
            "severity": sev * n,
            "examples": examples[(token, ctx)],
        })
    out.sort(key=lambda x: -x["severity"])
    return out


def write_report(path: Path, sections: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Light mode gate — last run",
        "",
        "Generated by `tools/audits/intonare_light_gate.py`.",
        "Fix top NEON `leak` / `draw/js` rows first. Then ROLE. Then LIVE AA fails.",
        "Skipped: dark-token, keep-dark, leak-ok (already has a body.light twin).",
        "",
    ]
    neon = sections.get("neon_ranked", [])
    lines.append(f"## NEON leftovers (ranked) — {len(neon)} groups")
    lines.append("")
    if not neon:
        lines.append("_None outside keep-dark._")
    else:
        lines.append("| score | count | ctx | token | example line |")
        lines.append("|------:|------:|-----|-------|-------------|")
        for row in neon[:40]:
            ex = row["examples"][0]
            lines.append(
                f"| {row['severity']} | {row['count']} | `{row['ctx']}` | `{row['token']}` | L{ex['line']} |"
            )
        lines.append("")
        lines.append("### Top snips")
        lines.append("")
        for row in neon[:12]:
            lines.append(f"**{row['token']}** (`{row['ctx']}` ×{row['count']})")
            for ex in row["examples"][:2]:
                lines.append(f"- L{ex['line']}: `{ex['snip'][:120]}`")
            lines.append("")

    wash = sections.get("wash", [])
    lines.append(f"## WASH (tiny white / heavy dark scrim) — {len(wash)} hits")
    lines.append("")
    for h in wash[:25]:
        lines.append(f"- L{h['line']} `{h['ctx']}` `{h['token']}` — {h['snip'][:100]}")
    if len(wash) > 25:
        lines.append(f"- … {len(wash) - 25} more")
    lines.append("")

    role = sections.get("role", [])
    lines.append(f"## ROLE (stage used as content ground) — {len(role)} hits")
    lines.append("")
    for h in role:
        lines.append(f"- L{h['line']} `{h['token']}` — {h['snip'][:100]}")
    if not role:
        lines.append("_None detected by alias heuristic._")
    lines.append("")

    live = sections.get("live")
    if live is None:
        lines.append("## LIVE AA walk")
        lines.append("")
        lines.append("_Skipped. Pass `--live http://127.0.0.1:8899/Intonare.html` with Playwright installed._")
    else:
        lines.append(f"## LIVE AA walk — {live.get('screens', 0)} screens, {live.get('fails', 0)} fails")
        lines.append("")
        if live.get("error"):
            lines.append(f"**Error:** {live['error']}")
        by_tool = collections.Counter(r.get("tool", "?") for r in live.get("rows", []))
        if by_tool:
            lines.append("### Fails by tool")
            lines.append("")
            for tool, n in by_tool.most_common():
                lines.append(f"- `{tool}`: {n}")
            lines.append("")
            lines.append(
                "_Note: keep-dark islands (piano skins, theremin Moog, tuner glass) can "
                "legitimately fail AA on dark fills. Triage those last._"
            )
            lines.append("")
        lines.append("### Worst samples")
        lines.append("")
        for row in live.get("rows", [])[:60]:
            txt = (row.get("text") or "").replace("\n", " ")[:60]
            lines.append(
                f"- `{row.get('tool', '?')}` {row.get('ratio', 0):.2f}:1 — {txt!r} "
                f"fg={row.get('fg', '')} bg={row.get('bg', '')}"
            )
        if live.get("fails", 0) > 60:
            lines.append(f"- … {live['fails'] - 60} more")
    lines.append("")
    lines.append("## Next actions")
    lines.append("")
    lines.append("1. Burn top NEON `leak` / `draw/js` groups (add `body.light` ink or gate draw).")
    lines.append("2. Ignore `dark-token` (theme vars redefined under body.light) and `keep-dark`.")
    lines.append("3. Fix any ROLE hits (remap `--bg` to surface/panel under `body.light`).")
    lines.append("4. Re-run gate; then LIVE walk; then your screenshot board only.")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def rel_lum(rgb):
    def f(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast_ratio(fg, bg):
    L1, L2 = rel_lum(fg), rel_lum(bg)
    lighter, darker = max(L1, L2), min(L1, L2)
    return (lighter + 0.05) / (darker + 0.05)


def parse_css_color(s: str):
    if not s or s in ("transparent", "inherit"):
        return None
    m = re.match(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)", s)
    if m:
        return (int(float(m.group(1))), int(float(m.group(2))), int(float(m.group(3))))
    m = re.match(r"#([0-9a-fA-F]{6})", s)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return None


def run_live(url: str) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "error": "Playwright not installed. pip install playwright && playwright install chromium",
            "screens": 0,
            "fails": 0,
            "rows": [],
        }

    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        page.evaluate(
            """() => {
              document.documentElement.classList.add('light-root');
              document.body.classList.add('light', 'theme-tools', 'is-pro', 'lnch-settled');
              document.body.classList.remove('lnch-open');
              try { localStorage.setItem('intonare-appearance', 'light'); } catch (e) {}
              try { if (typeof tryUnlockCode === 'function') tryUnlockCode('INTONARE_AMICI'); } catch (e) {}
            }"""
        )
        page.wait_for_timeout(400)
        # Dismiss launcher if present
        page.evaluate(
            """() => {
              document.querySelectorAll('.lnch-grid, .lnch-panel, .lnch-root').forEach(el => {
                el.style.display = 'none';
              });
              const btn = [...document.querySelectorAll('.mode-btn')].find(b => /TOOLS/i.test(b.textContent||''));
              if (btn) btn.click();
            }"""
        )
        page.wait_for_timeout(300)

        probe = """(tool) => {
          const root = document.body;
          const fails = [];
          const parse = (s) => {
            if (!s || s === 'transparent') return null;
            const m = s.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
            if (m) return [+m[1], +m[2], +m[3]];
            return null;
          };
          const lum = ([r,g,b]) => {
            const f = c => { c/=255; return c<=0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
            return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b);
          };
          const ratio = (fg, bg) => {
            const L1 = lum(fg), L2 = lum(bg);
            const a = Math.max(L1,L2), b = Math.min(L1,L2);
            return (a+0.05)/(b+0.05);
          };
          const bgOf = (el) => {
            let n = el;
            while (n && n !== document.documentElement) {
              const cs = getComputedStyle(n);
              const bg = parse(cs.backgroundColor);
              if (bg && cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent') {
                // ignore fully transparent
                const a = cs.backgroundColor.includes('rgba') ?
                  +cs.backgroundColor.split(',')[3] : 1;
                if (isNaN(a) || a > 0.15) return bg;
              }
              n = n.parentElement;
            }
            return parse(getComputedStyle(document.body).backgroundColor) || [167,167,216];
          };
          const nodes = document.querySelectorAll(
            'button, a, label, p, span, h1, h2, h3, h4, li, td, th, .chip, .stp-name, .mode-btn, .pg-heading, .pg-body, .pg-subhead'
          );
          let checked = 0;
          for (const el of nodes) {
            if (checked > 400) break;
            const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.2) continue;
            const r = el.getBoundingClientRect();
            if (r.width < 4 || r.height < 4) continue;
            const text = (el.innerText || el.textContent || '').trim().replace(/\\s+/g,' ');
            if (text.length < 1 || text.length > 80) continue;
            const fg = parse(cs.color);
            if (!fg) continue;
            const bg = bgOf(el);
            const rat = ratio(fg, bg);
            const fs = parseFloat(cs.fontSize) || 12;
            const large = fs >= 18 || (fs >= 14 && (cs.fontWeight === '700' || +cs.fontWeight >= 700));
            const need = large ? 3.0 : 4.5;
            checked++;
            if (rat < need) {
              fails.push({
                tool, ratio: +rat.toFixed(2), need, text: text.slice(0,72),
                fg: cs.color, bg: `rgb(${bg.join(',')})`, fs
              });
            }
          }
          return fails.slice(0, 40);
        }"""

        for tool, _dom in TOOLS_LIVE:
            try:
                page.evaluate(
                    """(name) => {
                      if (typeof enterTool === 'function') enterTool(name);
                      else if (typeof enterExercise === 'function' && name === 'scales') enterExercise('scales');
                    }""",
                    tool,
                )
                page.wait_for_timeout(350)
                batch = page.evaluate(probe, tool)
                for item in batch:
                    rows.append(item)
            except Exception as e:
                rows.append({
                    "tool": tool,
                    "ratio": 0,
                    "text": f"ERROR {e}",
                    "fg": "",
                    "bg": "",
                })
        browser.close()

    return {
        "screens": len(TOOLS_LIVE),
        "fails": len(rows),
        "rows": sorted(rows, key=lambda r: (r.get("ratio", 0), r.get("tool", ""))),
        "error": None,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Intonare light-mode gate")
    ap.add_argument("html", nargs="?", default=str(DEFAULT_HTML))
    ap.add_argument("--live", metavar="URL", help="Playwright walk of Tools screens")
    ap.add_argument("--report", default=str(REPORT_PATH))
    args = ap.parse_args()

    html_path = Path(args.html)
    if not html_path.is_file():
        print(f"FAIL: missing {html_path}", file=sys.stderr)
        return 2

    text = html_path.read_text(encoding="utf-8")
    print(f"Scanning {html_path} ({len(text):,} chars)…")

    neon_hits = scan_neon(text)
    wash_hits = scan_wash(text)
    role_hits = scan_role(text)
    neon_ranked = rank_neon(neon_hits)

    keep = sum(1 for h in neon_hits if h["ctx"] == "keep-dark")
    tokens = sum(1 for h in neon_hits if h["ctx"] == "dark-token")
    overridden = sum(1 for h in neon_hits if h["ctx"] == "leak-ok")
    actionable = sum(r["count"] for r in neon_ranked)

    print()
    print("=== LIGHT GATE (static) ===")
    print(f"NEON hits total:        {len(neon_hits)}")
    print(f"  dark-token (skip):    {tokens}")
    print(f"  keep-dark (skip):     {keep}")
    print(f"  leak w/ light override (skip): {overridden}")
    print(f"NEON still open:        {actionable} across {len(neon_ranked)} groups")
    print(f"WASH hits:              {len(wash_hits)}")
    print(f"ROLE hits:              {len(role_hits)}")
    print()
    print("--- Top open NEON leaks / draw (fix these) ---")
    for row in neon_ranked[:20]:
        ex = row["examples"][0]
        sel = ex.get("sel") or ""
        print(
            f"  [{row['severity']:4d}] ×{row['count']:<3} {row['ctx']:<10} {row['token']:<18} "
            f"L{ex['line']}  {sel[:40]}"
        )

    live = None
    if args.live:
        print()
        print(f"=== LIVE walk {args.live} ===")
        live = run_live(args.live)

    report = Path(args.report)
    write_report(
        report,
        {
            "neon_ranked": neon_ranked,
            "wash": wash_hits,
            "role": role_hits,
            "live": live,
        },
    )

    if args.live:
        if live.get("error"):
            print(f"LIVE skipped: {live['error']}")
        else:
            print(f"LIVE fails: {live['fails']} across {live['screens']} screens")
            for row in live.get("rows", [])[:20]:
                line = (
                    f"  {row.get('ratio', 0):4.2f}  {row.get('tool', '?'):<14} "
                    f"{(row.get('text') or '')[:50]}"
                )
                print(line.encode("ascii", "replace").decode("ascii"))

    print()
    print(f"Report: {report}")
    print("Next: burn top NEON leak/draw rows, re-run, then screenshot board.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
