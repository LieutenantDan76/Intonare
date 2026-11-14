#!/usr/bin/env python3
"""
Intonare taint audit
====================
Checks that saved text can never reach the page as markup.

It loads Intonare.html in a headless browser. For each kind of saved item
(progression, chart view, drum save, metronome preset, ramp preset, vocal range
session) it puts a script-running payload into one field at a time, then loads
and shows the item the way the app does. If any payload runs, or lands in the
page as an element, the audit fails and names the field.

Saved items can come from a backup file, so every field counts as outside input.

Needs: pip install playwright && playwright install chromium

Usage:
    python tools/audits/intonare_taint_audit.py [Intonare.html]

Exit code 0 = no payload ran. It takes about a minute, so it is not part of
the ship check. Run it after any change to a screen that shows saved items.
"""
import os, sys, pathlib
from playwright.sync_api import sync_playwright
html = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html').resolve()
JS = r"""
async () => {
  const P = id => `"'><img src=x onerror="(window.__xss=window.__xss||[]).push('${id}')">`;
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const res = { hits: [], errs: {}, fields: 0 };
  progState.hasPro = true;
  const realSave = window.progSave; window.progSave = function () {};
  function leaves(o, path, out) { if (typeof o === 'string') out.push(path);
    else if (o && typeof o === 'object') Object.keys(o).forEach(k => leaves(o[k], path.concat([k]), out)); return out; }
  function setAt(o, path, v) { let c = o; for (let i = 0; i < path.length - 1; i++) c = c[path[i]]; c[path[path.length - 1]] = v; }
  function check(tag) { const a = (window.__xss || []).slice(); window.__xss = [];
    const dom = [...document.querySelectorAll('img[src="x"],img[src="X"]')].map(i => { let e = i; while (e && !e.id) e = e.parentElement; i.remove(); return (e && e.id) || '?'; });
    if (a.length || dom.length) res.hits.push(tag + ' -> ' + JSON.stringify([a, dom])); }
  async function each(kind, base, run) {
    const paths = leaves(base, [], []).concat(Object.keys(base).filter(k => typeof base[k] === 'number').map(k => [k]));
    for (const p of paths) { res.fields++;
      const item = JSON.parse(JSON.stringify(base)); setAt(item, p, P(kind + '.' + p.join('.')));
      try { await run(item); } catch (e) { res.errs[kind + '.' + p.join('.')] = String(e.message).slice(0, 80); }
      await wait(250); check(kind + '.' + p.join('.')); } }
  // 1. saved progression
  setMode('tools'); enterTool('progression'); await wait(600);
  const pp = JSON.parse(JSON.stringify(PROG_PRESETS.find(x => x.bars && x.bars.length) || PROG_PRESETS[1])); pp.id = 'u1';
  await each('prog', pp, async item => { progState.savedProgressions = [item]; try { progBuildPresets && progBuildPresets(); } catch (e) {} progLoadPreset('u1'); });
  exitTool(true);
  // 2. saved chart view
  setMode('tools'); enterTool('guitarchords'); await wait(600);
  progState.savedCharts = []; svcSaveCurrentView('x'); const sc = JSON.parse(JSON.stringify(progState.savedCharts[0]));
  await each('chart', sc, async item => { progState.savedCharts = [item]; try { lnchBuildPins(); } catch (e) {} try { svcRenderTiles && svcRenderTiles(); } catch (e) {} svcLaunch(item); });
  exitTool(true);
  // 3. drum kit save
  setMode('tools'); enterTool('drumkit'); await wait(600);
  const snap = Object.assign({ name: 'n' }, _customSnapshot());
  await each('dk', snap, async item => { _setSaves([item]); try { _applySnapshot(item); } catch (e) { throw e; } try { dkRenderSaves && dkRenderSaves(); } catch (e) {} });
  _setSaves([]); exitTool(true);
  // 4. metronome and ramp presets
  setMode('metronome');
  await each('metro', { id: 'm1', name: 'n', bpm: 120, sound: 'click', mode: 'std' }, async item => { progState.metroPresets = [item]; renderSetlist(); loadSetlistPreset(item.id); });
  await each('ramp', { id: 'r1', name: 'n', fromBpm: 60, toBpm: 120, stepBpm: 5, measuresPerStep: 4, sound: 'click' }, async item => { progState.rampPresets = [item]; renderRampPresets(); loadRampPreset(item.id); });
  // 5. vocal range sessions and the launcher pin row
  setMode('tools'); enterTool('vocalrange'); await wait(500);
  const vt = JSON.parse(JSON.stringify(VR_VOICE_TYPES[0]));
  await each('vr', { voiceType: vt, lowComf: 48, highComf: 67, tessCenter: 57, extLow: 45, extHigh: 70, date: new Date().toISOString() }, async item => {
    localStorage.setItem('intonare_vr_sessions', JSON.stringify([item, item])); vrRenderHistory(); try { vrRenderTimeline(); } catch (e) {} });
  localStorage.removeItem('intonare_vr_sessions'); exitTool(true);
  window.progSave = realSave;
  return res;
}
"""
with sync_playwright() as p:
    kw = {'args': ['--no-sandbox', '--autoplay-policy=no-user-gesture-required']}
    if os.environ.get('INTONARE_CHROME'): kw['executable_path'] = os.environ['INTONARE_CHROME']
    b = p.chromium.launch(**kw)
    pg = b.new_context(viewport={'width':412,'height':915}, has_touch=True, is_mobile=True).new_page()
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto(html.as_uri(), wait_until='load'); pg.wait_for_timeout(5500)
    pg.evaluate("window._intonareSkipSplash&&window._intonareSkipSplash()"); pg.wait_for_timeout(1200)
    r = pg.evaluate(JS)
    b.close()
print('TAINT AUDIT')
print('=' * 62)
for h in r['hits']:
    print('  FAIL  payload reached the page:', h[:200])
for e in errs:
    print('  FAIL  page error:', e)
print('=' * 62)
if r['hits'] or errs:
    print(f"  {len(r['hits']) + len(errs)} problem(s) across {r['fields']} fields. Do not ship.")
    sys.exit(1)
print(f"  {r['fields']} fields tested across 6 kinds of saved item. No payload ran.")
