#!/usr/bin/env python3
"""
Search audit (1.0.5): loads the real Intonare.html in headless Chromium and checks
  1. every top-level module has main tags (folders may not, Utilities has none by design);
  2. every tag used anywhere is a known concept, and every concept has English AND Italian words;
  3. every query in tools/audits/search_queries.json returns what it must.

Usage (from repo root):  python tools/audits/intonare_search_audit.py [Intonare.html]
Needs: pip install playwright && playwright install chromium
Exit 0 = green. The expectations are the source of truth for what Search should find;
change them on purpose, with a reason, never to make a failure go away.
"""
import fnmatch, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
HTML = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Intonare.html"
QUERIES = Path(__file__).with_name("search_queries.json")


def hit(ids, pat):
    return any(fnmatch.fnmatch(i, pat) for i in ids)


def main() -> int:
    from playwright.sync_api import sync_playwright
    fails = []
    queries = json.loads(QUERIES.read_text(encoding="utf-8"))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 420, "height": 860})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(HTML.resolve().as_uri(), wait_until="domcontentloaded", timeout=120000)
        pg.wait_for_function("typeof window._hvsSearch === 'function' && typeof window._hvsMeta === 'function'", timeout=120000)

        # 1 + 2: tags
        meta = pg.evaluate("window._hvsMeta()")
        for tag, words in meta["concept"].items():
            parts = [w.strip() for w in words.split("|")]
            if len(parts) != 2 or not parts[0] or not parts[1]:
                fails.append(f"concept '{tag}' needs English words | Italian words")
            if tag not in meta["names"]:
                fails.append(f"concept '{tag}' has no display name")
        known = set(meta["concept"])
        items = pg.evaluate("window._hvsIndex().map(x => ({id: x.id, top: x.top, kind: x.kind, mt: x.mt, rt: x.rt}))")
        for it in items:
            for t in it["mt"] + it["rt"]:
                if t not in known:
                    fails.append(f"{it['id']}: unknown tag '{t}'")
            if it["top"] and not it["mt"] and it["id"] != "folder:utilities":
                fails.append(f"{it['id']}: top-level module with no main tags (add a line to TAGS)")
        fav = pg.evaluate("Object.keys(FAV_META)")
        have = {i["id"] for i in items}
        for k in fav:
            if k not in have:
                fails.append(f"{k}: in FAV_META but not in the search index")

        # 3: queries
        cur_lang = None
        for q in queries:
            lang = q.get("lang", "en")
            if lang != cur_lang:
                pg.evaluate(f"progState.lang = '{lang}'")
                cur_lang = lang
            res = pg.evaluate("q => window._hvsSearch(q, 14).map(x => x.id)", q["q"])
            tag = f"[{lang}] '{q['q']}'"
            if q.get("none"):
                if res:
                    fails.append(f"{tag}: expected nothing, got {res[:4]}")
                continue
            if "first" in q and (not res or res[0] != q["first"]):
                fails.append(f"{tag}: expected {q['first']} first, got {res[:4]}")
            if "top" in q:
                n, ids = q["top"]
                miss = [i for i in ids if i not in res[:n]]
                if miss:
                    fails.append(f"{tag}: expected {miss} in top {n}, got {res[:n]}")
            if "topany" in q:
                n, pats = q["topany"]
                if not any(hit(res[:n], pt) for pt in pats):
                    fails.append(f"{tag}: expected one of {pats} in top {n}, got {res[:n]}")
            if "absent" in q:
                bad = [i for i in q["absent"] if i in res]
                if bad:
                    fails.append(f"{tag}: {bad} must not appear, got {res}")
            if "order" in q:
                a, b2 = q["order"]
                pa = [res.index(i) for i in a if i in res]
                pb = [res.index(i) for i in b2 if i in res]
                if not pa or (pb and max(pa) > min(pb)):
                    fails.append(f"{tag}: every {a[:3]}... must come before {b2}; got {res}")
        pg.evaluate("progState.lang = 'en'")
        b.close()
        for e in errs:
            fails.append(f"page error: {e[:200]}")
    if fails:
        print(f"SEARCH AUDIT FAILED ({len(fails)})")
        for f in fails:
            print("  -", f)
        return 1
    print(f"SEARCH AUDIT OK: {len(queries)} queries, tags and Italian twins checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
