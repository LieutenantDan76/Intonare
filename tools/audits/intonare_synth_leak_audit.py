#!/usr/bin/env python3
"""
Intonare synth leak audit
=========================
Checks that every built-in synth voice unplugs its audio parts once a note ends.

Each note builds a small chain (oscillators, gains, filters). If the parts stay
connected after the note, the audio graph grows for the whole session and slower
phones start to crackle. This plays four short notes and one held note (then
stopped) on every voice in a real AudioContext, routed to a muted bus. The voices
that fade to silence by themselves (FADES_OUT) also get one note with no length
that is never stopped: it must end on its own when its decay is done. The other
voices hold a note with no length until the caller stops it, by design. The audit waits
for the longest natural decay and counts the parts that are still connected.

Needs: pip install playwright && playwright install chromium

Usage:
    python tools/audits/intonare_synth_leak_audit.py [Intonare.html]

About 15 seconds. Not in the ship check. Run it after any change to REF_TONES.
Exit code 0 = no voice leaves a part connected.
"""
import os, sys, pathlib
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html').resolve()
# The eleven simple voices, plus four that borrow the piano voice.
VOICES = ['sine', 'piano', 'flute', 'bell', 'marimba', 'xylophone', 'vibraphone', 'pad', 'guitar', 'brass', 'melodica',
          'grand_piano', 'honky_tonk', 'electric_piano', 'harpsichord']

# Voices whose sound dies away on its own, like a struck or plucked instrument.
FADES_OUT = ['bell', 'marimba', 'xylophone', 'guitar']

TEST = r"""async ([voices, fades]) => {
  const ctx = new AudioContext(); await ctx.resume();
  const owner = new Map(), conn = new Map();
  let current = null;
  const C = AudioNode.prototype.connect, D = AudioNode.prototype.disconnect;
  AudioNode.prototype.connect = function () { conn.set(this, (conn.get(this) || 0) + 1); return C.apply(this, arguments); };
  AudioNode.prototype.disconnect = function () {
    conn.set(this, arguments.length === 0 ? 0 : Math.max(0, (conn.get(this) || 0) - 1));
    return D.apply(this, arguments); };
  const P = BaseAudioContext.prototype, names = ['createOscillator', 'createGain', 'createBiquadFilter', 'createBufferSource'];
  const orig = {};
  names.forEach(n => { orig[n] = P[n]; P[n] = function () { const x = orig[n].apply(this, arguments); if (current) owner.set(x, current); return x; }; });
  const bus = orig.createGain.call(ctx); bus.gain.value = 0; bus.connect(ctx.destination);
  const t0 = ctx.currentTime + 0.05, held = [];
  for (const id of voices) {
    current = id;
    for (let i = 0; i < 4; i++) REF_TONES[id].synth(ctx, 220 * (1 + i / 4), t0 + i * 0.05, 0.4, bus, 0.5);
    held.push(REF_TONES[id].synth(ctx, 330, t0, null, bus, 0.5));
    if (fades.includes(id)) REF_TONES[id].synth(ctx, 165, t0, null, bus, 0.5);   // never stopped
    current = null;
  }
  setTimeout(() => held.forEach(h => { try { h.stop(); } catch (e) {} }), 500);
  await new Promise(r => setTimeout(r, 7000));   // longest natural decay (vibraphone) plus margin
  const res = {};
  for (const id of voices) res[id] = { parts: 0, connected: 0 };
  owner.forEach((id, node) => { res[id].parts++; if ((conn.get(node) || 0) > 0) res[id].connected++; });
  names.forEach(n => { P[n] = orig[n]; }); AudioNode.prototype.connect = C; AudioNode.prototype.disconnect = D;
  await ctx.close();
  return res; }"""

with sync_playwright() as p:
    kw = {'args': ['--no-sandbox', '--autoplay-policy=no-user-gesture-required']}
    if os.environ.get('INTONARE_CHROME'): kw['executable_path'] = os.environ['INTONARE_CHROME']
    b = p.chromium.launch(**kw)
    pg = b.new_page(); errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)[:200]))
    pg.goto(html.as_uri(), wait_until='load'); pg.wait_for_timeout(5000)
    res = pg.evaluate(TEST, [VOICES, FADES_OUT])
    b.close()

print('SYNTH LEAK AUDIT')
print('=' * 62)
bad = 0
for id in VOICES:
    r = res[id]
    flag = 'FAIL' if r['connected'] else 'ok  '
    if r['connected']: bad += 1
    print(f"  {flag}  {id:15} {r['parts']:3} parts, {r['connected']} still connected after the notes ended")
for e in errors: print('  PAGE ERROR', e)
print('=' * 62)
if bad or errors:
    print(f'  {bad} voice(s) leave parts connected. Do not ship.')
    sys.exit(1)
print(f'  All {len(VOICES)} voices unplug every part once their notes end.')
