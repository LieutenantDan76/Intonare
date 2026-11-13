#!/usr/bin/env python3
"""
Intonare boot smoke test
========================
Loads Intonare.html in a headless browser, opens every mode, tool and exercise,
switches language and theme, and fails if anything throws or logs an error.

Why this exists: the other gates read the file as text. They cannot see a
ReferenceError that only happens when a screen opens. The 1.0.5 lint pass found
four of those (a name used outside the closure that owned it). This catches the
same class at run time.

Pro is switched on in memory only, so locked modules open. Nothing is written
to the file. Audio and the mic are not tested; that still needs a phone.

Needs: pip install playwright && playwright install chromium

Usage:
    python tools/audits/intonare_boot_smoke.py [Intonare.html]

Exit code 0 = every screen opened with no error. Non-zero = see the list.

Maintenance: when a tool or exercise is added, add its id to TOOLS or EXS.
A wrong id fails loudly ("did not open"), so a stale list cannot pass.
"""
import os, re, sys, pathlib
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html').resolve()
TOOLS = ['piano', 'tonal', 'theremin', 'guitarchords', 'chords', 'progression', 'drumkit', 'rhythmcards',
         'cof', 'intervalref', 'scales', 'survivalguide', 'transpose', 'vocalrange', 'volume']
EXS = ['chordle', 'chords', 'diadle', 'interval', 'notationcards', 'poly', 'relpitch', 'rhythmread',
       'roadtrip', 'singsing', 'staffread', 'tempo', 'tempoguess', 'tonale']
MODES = ['tuner', 'metronome', 'practice', 'tools']
# Local asset fetches fail from file:// and are not app errors.
NOISE = ('CORS policy', 'ERR_FAILED', 'ERR_FILE_NOT_FOUND')
# Paths that broke before. Each one throws if the fix is gone.
PROBES = [
    ('interval peek opens the reference with a return pill',
     "setMode('practice');enterExercise('interval');_ivPeekSem=4;ivPeekOpenFull();"
     "var pl=document.getElementById('sgReturnPill');if(!pl)throw new Error('no return pill');"
     "if(currentTool!=='intervalref')throw new Error('reference did not open')"),
    ('the return pill goes back to the exercise',
     "document.getElementById('sgReturnPill').click();await new Promise(r=>setTimeout(r,500));"
     "if(currentExercise!=='interval')throw new Error('did not return to the exercise');exitExercise()"),
    ('backup share fallback runs', "setMode('tuner');_backupShareFallback('x.json','{}')"),
    ('Sight Singing voice button saves',
     "setMode('practice');enterExercise('singsing');ssCycleVoice();"
     "var ok=localStorage.getItem('ss_voice')===ssVoice;exitExercise();if(!ok)throw new Error('ss_voice not saved')"),
    ('Survival Guide follows a language switch',
     "setLang('en');setMode('tools');enterTool('survivalguide');await new Promise(r=>setTimeout(r,600));"
     "var a=document.getElementById('toolSurvivalGuide').innerText.slice(0,400);setLang('it');"
     "await new Promise(r=>setTimeout(r,600));var b=document.getElementById('toolSurvivalGuide').innerText.slice(0,400);"
     "setLang('en');exitTool(true);if(a===b)throw new Error('guide text did not change')"),
    ('note displays refresh', "refreshAllNoteDisplays()"),
    # A fake trivia server answers with an <img onerror> in every field. If any of
    # it runs or renders as an element, online text is reaching the page as HTML.
    ('online quiz: start a round from a hostile reply', 'window.__xss=0;var P=\'<img src=x onerror="window.__xss=(window.__xss||0)+1">\';var mk=function(i){return {category:encodeURIComponent(\'Music \'+P),type:\'multiple\',difficulty:\'easy\',question:encodeURIComponent(\'Which band wrote song number \'+i+\'? \'+P),correct_answer:encodeURIComponent(\'The Beatles \'+i+\' \'+P),incorrect_answers:[encodeURIComponent(\'Queen \'+i+\' \'+P),encodeURIComponent(\'Rush \'+i+\' \'+P),encodeURIComponent(\'Muse \'+i+\' \'+P)]}};var rs=[];for(var i=0;i<50;i++)rs.push(mk(i));window.__realFetch=window.fetch;window.fetch=function(u){if(String(u).indexOf(\'opentdb\')>=0)return Promise.resolve({json:function(){return Promise.resolve({response_code:0,results:rs})}});return window.__realFetch.apply(this,arguments)};setMode(\'tools\');mqOpen();progState.mqMusicOn=false;MQ.qCount=10;mqRunOnlineFetch(MQ_ONLINE_CATS[0].id,\'quick\');await new Promise(r=>setTimeout(r,1800));if(!MQ.questions||!MQ.questions.length)throw new Error(\'no online questions dealt\')'),
    ('online quiz: answer every question', "for(var k=0;k<10;k++){var b=document.querySelector('.mq2-opt')||document.querySelector('.mq-ans-btn');if(!b)break;b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));b.click();await new Promise(r=>setTimeout(r,900));var nx=document.getElementById('mq2Next')||document.querySelector('.mq2-next,.mq-next-btn');if(nx)nx.click();await new Promise(r=>setTimeout(r,500))}"),
    ('online quiz: nothing injected ran, review included', 'try{mqShowMissReview()}catch(e){};await new Promise(r=>setTimeout(r,600));window.fetch=window.__realFetch;var im=document.querySelectorAll(\'#mqPanel img[src="x"]\').length;if(window.__xss||im)throw new Error(\'injected HTML ran or rendered\');if(!MQ.misses||!MQ.misses.length)throw new Error(\'test did not reach the review\')'),
]

log = []
cur = ['boot']


def norm(s):
    return re.sub(r'\d{3,}', 'N', s)[:300]


with sync_playwright() as p:
    kw = {'args': ['--no-sandbox', '--autoplay-policy=no-user-gesture-required',
                   '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream']}
    chrome = os.environ.get('INTONARE_CHROME')
    if chrome:
        kw['executable_path'] = chrome
    b = p.chromium.launch(**kw)
    ctx = b.new_context(viewport={'width': 412, 'height': 915}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: log.append((cur[0], 'page error', norm(str(e)))))
    pg.on('console', lambda m: log.append((cur[0], 'console error', norm(m.text)))
          if m.type == 'error' and not any(n in m.text for n in NOISE) else None)
    pg.goto(html.as_uri(), wait_until='load')
    pg.wait_for_timeout(6000)

    def step(name, js, wait=500):
        cur[0] = name
        try:
            r = pg.evaluate('(async()=>{try{' + js + ';return "ok"}catch(e){return "THROW "+(e&&e.message)}})()')
            if r != 'ok':
                log.append((name, 'throw', norm(r)))
        except Exception as e:
            log.append((name, 'eval failed', norm(str(e))))
        pg.wait_for_timeout(wait)

    step('skip splash', 'if(window._intonareSkipSplash)window._intonareSkipSplash()', 1500)
    step('test Pro (memory only)', 'progState.hasPro=true', 100)
    for m in MODES:
        step('mode ' + m, f"setMode('{m}')")
    for t in TOOLS:
        step('tool ' + t, f"setMode('tools');enterTool('{t}');if(currentTool!=='{t}')throw new Error('did not open')", 900)
        step('tool ' + t + ' exit', 'exitTool(true)', 250)
    for e in EXS:
        step('exercise ' + e, f"setMode('practice');enterExercise('{e}');if(currentExercise!=='{e}')throw new Error('did not open')", 900)
        step('exercise ' + e + ' exit', 'exitExercise()', 250)
    for lang in ('it', 'en'):
        step('language ' + lang, f"setLang('{lang}')", 900)
    step('light theme', "document.body.classList.contains('light')||(typeof toggleTheme==='function'&&toggleTheme())", 600)
    for m in MODES:
        step('light, mode ' + m, f"setMode('{m}')", 300)
    for name, js in PROBES:
        step('probe: ' + name, js, 600)
    cur[0] = 'end'
    pg.wait_for_timeout(500)
    b.close()

seen = {}
for k in log:
    seen[k] = seen.get(k, 0) + 1
steps = 2 + len(MODES) * 2 + len(TOOLS) * 2 + len(EXS) * 2 + 3 + len(PROBES)
print('BOOT SMOKE TEST')
print('=' * 62)
for (where, kind, msg), n in seen.items():
    print(f'  FAIL  [{where}] {kind} x{n}: {msg[:200]}')
print('=' * 62)
if seen:
    print(f'  {len(seen)} problem(s) across {steps} steps. Do not ship.')
    sys.exit(1)
print(f'  All {steps} steps ran clean: {len(MODES)} modes, {len(TOOLS)} tools, {len(EXS)} exercises, {len(PROBES)} probes.')
