#!/usr/bin/env python3
"""
Intonare language switch audit
==============================
Finds text that keeps the old language after the user changes language.

For every main tab, tool, exercise, folder, Settings and Progress, it:
  1. opens the screen in language A and reads every visible text node,
  2. switches to language B without leaving the screen and reads again,
  3. starts the app fresh in language B, opens the screen, and reads again.

A text is stale when it sits in the same place in all three reads, the switch
left it unchanged, and a fresh open in language B draws something else there. Random content
is pinned with a seeded Math.random that is reset before every open, and tours
are closed after every open, so both opens draw the same thing.

Needs: pip install playwright && playwright install chromium

Usage:
    python tools/audits/intonare_lang_switch_audit.py [Intonare.html] [en it]

Runs both directions by default (en to it, then it to en). Takes several
minutes, so it is not part of the ship check. Run it after any change to text
that a screen draws from code. Exit code 0 = nothing stale.
"""
import os, sys, pathlib
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html').resolve()
PAIRS = [(sys.argv[2], sys.argv[3])] if len(sys.argv) > 3 else [('en', 'it'), ('it', 'en')]

TOOLS = ['piano', 'tonal', 'theremin', 'guitarchords', 'chords', 'progression', 'drumkit', 'rhythmcards', 'cof',
         'intervalref', 'scales', 'survivalguide', 'transpose', 'vocalrange', 'volume', 'musicquiz']
EXERCISES = ['chordle', 'chords', 'diadle', 'interval', 'notationcards', 'poly', 'relpitch', 'rhythmread',
             'roadtrip', 'singsing', 'staffread', 'tempo', 'tempoguess', 'tonale']
TRAIN_FOLDERS = [('enterEarTraining', 'exitEarTraining'), ('enterRhythm', 'exitRhythm'),
                 ('enterGames', 'exitGames'), ('enterReading', 'exitReading')]
TOOL_FOLDERS = ['pitch', 'harmony', 'rhythm', 'reference', 'utilities']

SEED = """window.__seed = function (n) { let a = n >>> 0;
  Math.random = function () { a = (a + 0x6D2B79F5) >>> 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };"""

# Each visible text node, keyed by where it sits: the nearest element id plus the
# child positions below it. Comparing by place means a panel that is simply not
# open the second time is skipped, instead of counted as stale.
SNAP = """(() => { const out = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const key = el => { const parts = []; let e = el;
    while (e && e !== document.body) { if (e.id) { parts.push('#' + e.id); break; }
      const par = e.parentElement; parts.push(e.tagName + ':' + (par ? [...par.children].indexOf(e) : 0)); e = par; }
    return parts.reverse().join('>'); };
  while (w.nextNode()) { const n = w.currentNode, p = n.parentElement; if (!p) continue;
    if (p.tagName === 'SCRIPT' || p.tagName === 'STYLE') continue;
    const s = n.textContent.replace(/\\s+/g, ' ').trim(); if (s.length < 3 || !/[A-Za-zÀ-ú]{3}/.test(s)) continue;
    if (!p.getClientRects().length) continue; const cs = getComputedStyle(p);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const k = key(p); out[k] = (out[k] ? out[k] + ' ' : '') + s.slice(0, 80); }
  return out; })()"""

def screens():
    out = [('tab ' + m, f"setMode('{m}')", '') for m in ['tuner', 'metronome', 'practice', 'tools']]
    out += [('folder ' + f, f"setMode('practice');{f}()", x + '()') for f, x in TRAIN_FOLDERS]
    out += [('tool folder ' + f, f"setMode('tools');enterToolFolder('{f}')", 'exitToolFolder()') for f in TOOL_FOLDERS]
    out += [('tool ' + t, f"setMode('tools');enterTool('{t}')", 'exitTool(true)') for t in TOOLS]
    out += [('exercise ' + e, f"setMode('practice');enterExercise('{e}')", 'exitExercise()') for e in EXERCISES]
    out += [('settings', 'openSettings()', 'closeSettings()'),
            ('progress', 'openProgress()', "document.getElementById('progressModal').classList.remove('active','open')")]
    return out

def boot(p, lang=None):
    kw = {'args': ['--no-sandbox', '--autoplay-policy=no-user-gesture-required',
                   '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream']}
    if os.environ.get('INTONARE_CHROME'): kw['executable_path'] = os.environ['INTONARE_CHROME']
    br = p.chromium.launch(**kw)
    pg = br.new_context(viewport={'width': 412, 'height': 915}, has_touch=True, is_mobile=True).new_page()
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)[:160]))
    pg.goto(html.as_uri(), wait_until='load'); pg.wait_for_timeout(5500)
    if lang:   # start the app the way a user does who chose this language before
        pg.evaluate(f"progState.lang = '{lang}'; progSave();")
        pg.reload(wait_until='load'); pg.wait_for_timeout(5500)
    pg.evaluate("window._intonareSkipSplash && window._intonareSkipSplash();"
                "progState.hasPro = true; window.progSave = function () {};" + SEED)
    pg.wait_for_timeout(1000)
    return br, pg, errors

def walk(a, b):
    """Pass 1 switches a -> b on each screen. Pass 2 starts the app fresh in b and
    reads each screen once. Text is stale when the switch left it unchanged and the
    fresh start draws something else in the same place. A fresh start also redraws
    things that live outside one screen, like the launcher and the header."""
    stale, r1s, r2s, r3s = {}, {}, {}, {}
    with sync_playwright() as p:
        def run(pg, js, wait=700):
            try: pg.evaluate('(() => { try { ' + js + ' } catch (e) {} })()')
            except Exception: pass
            pg.wait_for_timeout(wait)
        def open_screen(pg, enter):
            run(pg, '__seed(7); ' + enter, 1100)
            run(pg, 'try { endTour(); } catch (e) {}', 300)
        br, pg, errors = boot(p)
        for name, enter, leave in screens():
            run(pg, f"setLang('{a}')", 500); open_screen(pg, enter); r1s[name] = pg.evaluate(SNAP)
            run(pg, f"setLang('{b}')", 1300); r2s[name] = pg.evaluate(SNAP)
            if leave: run(pg, leave, 300)
        leaks = pg.evaluate('JSON.stringify(typeof _RELABEL_LEAKS !== "undefined" ? _RELABEL_LEAKS : [])')
        br.close()
        br, pg, errors2 = boot(p, b)
        for name, enter, leave in screens():
            open_screen(pg, enter); r3s[name] = pg.evaluate(SNAP)
            if leave: run(pg, leave, 300)
        br.close()
    for name in r1s:
        r1, r2, r3 = r1s[name], r2s[name], r3s.get(name, {})
        s = sorted(r1[k] for k in r1 if k in r2 and k in r3 and r1[k] == r2[k] != r3[k])
        if s: stale[name] = s
    return stale, leaks, errors + errors2

failed = False
print('LANGUAGE SWITCH AUDIT')
for a, b in PAIRS:
    print('=' * 62); print(f'  {a} -> {b}')
    stale, leaks, errors = walk(a, b)
    for name, lines in stale.items():
        print(f'  STALE  {name}')
        for s in lines[:12]: print(f'           {s}')
        if len(lines) > 12: print(f'           ... and {len(lines) - 12} more')
    if leaks != '[]':
        print('  RELABELER SWITCHED OFF (it added nodes on a second run):', leaks)
    for e in errors[:5]: print('  PAGE ERROR', e)
    n = sum(len(v) for v in stale.values())
    print(f'  {n} stale line(s) on {len(stale)} screen(s)')
    failed = failed or bool(stale) or leaks != '[]' or bool(errors)
print('=' * 62)
print('  FAIL' if failed else '  PASS: every screen follows a language switch.')
sys.exit(1 if failed else 0)
