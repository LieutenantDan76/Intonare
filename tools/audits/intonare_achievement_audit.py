#!/usr/bin/env python3
"""
intonare_achievement_audit.py: every achievement must be earnable.

Why this exists: achievements failed in four different ways, and none of them
threw an error.
  1. The unlock read a stat nothing wrote (Tempo Guess never fed I Have You Now).
  2. The unlock compared a float with === (a "0ms" on screen is 0.3 in the code).
  3. The flag was set but nobody asked "did this unlock anything?" afterward, so
     the toast waited for some unrelated save.
  4. The unlock was reachable only through a code path that does not exist.

What this checks:
  A. TABLE   Every achievement has a passing state and a just-short state below,
             and every row here names a real achievement. A new achievement with
             no row fails the gate, so nothing ships untested.
  B. EVAL    The real check() functions run in node. The passing state must
             unlock, the just-short state must not, and an empty save must not.
  C. FIELDS  name, name_it, cond, cond_it, rarity, cat, desc and an icon exist.
  D. WRITERS Every stat or flag a check reads is written somewhere outside the
             achievement table.
  E. PROMPT  A flag the app sets by hand must be followed by checkAchievements().
  F. FLOATS  No === or == against a number on a millisecond, cents or seconds stat.

What it cannot see: a writer that exists but is never reached. Great Ears had
one of those. Row B proves the check is satisfiable, not that a player can get
there. Walk new achievements through once on a device.

Usage (repo root):  python tools/audits/intonare_achievement_audit.py [Intonare.html]
"""
import json, os, re, subprocess, sys, tempfile

PATH = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('INTONARE_HTML', 'Intonare.html')

def streak(n): return {"streak": {"count": n}}
def hist(**kw): return {"history": {"2026-01-01": kw}}
def st(**kw): return {"stats": kw}

# id: (state that must unlock, state one step short that must not)
CASES = {
 'first_light':       ({"sessionsCompleted": 1}, {"sessionsCompleted": 0}),
 'three_days':        (streak(3), streak(2)),
 'week_strong':       (streak(7), streak(6)),
 'creature_of_habit': (streak(21), streak(20)),
 'committed':         (streak(50), streak(49)),
 'zelda':             (streak(100), streak(99)),
 'great_ears':        (st(interval={"perfectSession": True}), st(interval={"correct": 10, "total": 10})),
 'i_have_you':        (st(tempo={"bestMs": 0.3}), st(tempo={"bestMs": 0.8})),
 'clean_summit':      (st(relpitch={"ch": {"best": 200000, "bestMult": 2}}), st(relpitch={"ch": {"best": 200000, "bestMult": 1.75}})),
 'chord_scholar':     (st(chords={"streak": 30}), st(chords={"streak": 29})),
 'perfect_pitch':     (st(singsing={"streak": 30}), st(singsing={"streak": 29})),
 'flawless':          (st(anyPerfect=True), st()),
 'curious':           (hist(**{"m%d" % i: 5 for i in range(10)}), hist(**{"m%d" % i: 5 for i in range(9)})),
 'explorer':          (st(**{k: {"x": 1} for k in ['interval','chords','singsing','tempo','tempoguess','poly','chordle']}),
                       st(**{k: {"x": 1} for k in ['interval','chords','singsing','tempo','tempoguess','poly']})),
 'rhythm_curious':    ({"summitReached": True}, {}),
 'apprentice':        ({"level": 5}, {"level": 4}),
 'practitioner':      ({"level": 10}, {"level": 9}),
 'musician':          ({"level": 20}, {"level": 19}),
 'master':            ({"level": 30}, {"level": 29}),
 'maestro':           ({"level": 50}, {"level": 49}),
 'adventurer':        ({"rt_parchment_done": True}, {}),
 'night_owl':         ({"nightOwl": True}, {}),
 'full_house':        ({"allPresetsLoaded": True}, {}),
 'dedicated':         ({"totalPracticeSec": 36000}, {"totalPracticeSec": 35999, "history": {"d": {"a": 100}}}),
 'more_cowbell':      ({"cowbellUsed": True}, {}),
 'hard_days_night':   ({"hardDaysNight": True}, {}),
 'everything_right_place': ({"everythingRightPlace": True}, {}),
 'first_chord':       (st(chordle={"correct": 1}), st(chordle={"correct": 0})),
 'harmonic_ear':      (st(chordle={"firstTry": 1}), st(chordle={"firstTry": 0})),
 'giant_steps':       (st(chordle={"vhardSolved": 5}), st(chordle={"vhardSolved": 4})),
 'deaf_composer':     (st(chordle={"solvedNoPlay": True}), st(chordle={"solvedNoPlay": False})),
 'crikey':            ({"didgeridooUsed": True}, {}),
 'addicted':          (hist(a=21600), hist(a=21599)),
 'the_summit':        ({"hardcoreSummit": True}, {}),
 'know_it_all':       ({"mqDailyPerfect": True}, {}),
 'last_standing':     ({"mqBestSurvival": 20}, {"mqBestSurvival": 19}),
 'trivia_night':      ({"mqTotalCorrect": 500}, {"mqTotalCorrect": 499}),
 'golden_ear':        ({"tonalePerfect": True}, {}),
 'completionist':     ("@all-non-secret", "@all-but-one"),
 'daily_grind':       ({"dailyChallengeStreak": {"count": 7}}, {"dailyChallengeStreak": {"count": 6}}),
}
# More than one way in. Each of these must unlock, on its own.
ALSO_UNLOCKS = {
 'i_have_you': [st(tempoguess={"bestDelta": 0})],
 'flawless':   [{"mqDailyPerfect": True}, {"tonalePerfect": True}],
}
ALSO_STAYS_LOCKED = {
 'i_have_you': [st(tempoguess={"bestDelta": 1})],
}
# Flags set by hand in the app. checkAchievements() must follow within a few lines,
# or the unlock waits for some unrelated save. nightOwl is set inside progUpdate,
# which runs the check itself on the next line.
PROMPT_EXEMPT = {'nightOwl'}
FLOAT_LEAVES = re.compile(r'(Ms|Cents|Sec)$')

def main():
    html = open(PATH, encoding='utf-8').read()
    errs, warns = [], []
    a = html.find('const ACHIEVEMENTS = [')
    b = html.find('\n];', a) + 3
    if a < 0:
        print('FAIL: ACHIEVEMENTS not found'); return 2
    table = html[a:b]
    h0 = html.find('function _achTotalTime(s)')
    h1 = html.find('// SVG icons per category')
    helpers = html[h0:h1]
    i0 = html.find('const ACH_ICONS = {')
    i1 = html.find('\n};', i0)
    icons = set(re.findall(r'^\s{2}([a-z_0-9]+):`', html[i0:i1], re.M))

    js = helpers + '\n' + table + '''
const CASES = %s, ALSO = %s, STAY = %s;
const out = [];
const nonSecret = ACHIEVEMENTS.filter(a => a.id !== 'completionist' && a.cat !== 'secrets');
function state(v, id){
  if (v === '@all-non-secret') { const m = {}; nonSecret.forEach(a => m[a.id] = {unlockedAt:'x'}); return {achievements: m}; }
  if (v === '@all-but-one')    { const m = {}; nonSecret.slice(1).forEach(a => m[a.id] = {unlockedAt:'x'}); return {achievements: m}; }
  return v;
}
function run(a, s){ try { return !!a.check(s); } catch (e) { return 'THREW ' + e.message; } }
ACHIEVEMENTS.forEach(a => {
  const c = CASES[a.id];
  const r = { id: a.id, src: String(a.check), cat: a.cat, miss: [] };
  ['name','name_it','cond','cond_it','rarity','cat','desc'].forEach(k => { if (!a[k]) r.miss.push(k); });
  r.empty = run(a, {});
  if (c) {
    r.pass = run(a, state(c[0])); r.fail = run(a, state(c[1]));
    r.also = (ALSO[a.id] || []).map(s => run(a, s));
    r.stay = (STAY[a.id] || []).map(s => run(a, s));
  }
  out.push(r);
});
console.log(JSON.stringify(out));
''' % (json.dumps(CASES), json.dumps(ALSO_UNLOCKS), json.dumps(ALSO_STAYS_LOCKED))
    tmp = os.path.join(tempfile.mkdtemp(), 'ach.js')
    open(tmp, 'w', encoding='utf-8').write(js)
    r = subprocess.run(['node', tmp], capture_output=True, text=True)
    if r.returncode:
        print('FAIL: node could not evaluate the achievement table'); print(r.stderr[:1500]); return 2
    res = json.loads(r.stdout)
    ids = [x['id'] for x in res]

    # A. table coverage
    for i in ids:
        if i not in CASES: errs.append(f'{i}: no row in CASES. Add a passing and a just-short state.')
    for i in CASES:
        if i not in ids: errs.append(f'{i}: in CASES but not in ACHIEVEMENTS (removed or renamed?)')
    if len(set(ids)) != len(ids): errs.append('duplicate achievement ids')

    outside = html[:a] + html[b:]
    lines = html.split('\n')
    for x in res:
        i = x['id']
        # B. eval
        if x['empty'] is not False: errs.append(f'{i}: an empty save gave {x["empty"]!r}, expected False')
        if 'pass' in x:
            if x['pass'] is not True: errs.append(f'{i}: the passing state did NOT unlock ({x["pass"]!r})')
            if x['fail'] is not False: errs.append(f'{i}: the just-short state unlocked or threw ({x["fail"]!r})')
            for k, v in enumerate(x['also']):
                if v is not True: errs.append(f'{i}: alternate route {k+1} did not unlock ({v!r})')
            for k, v in enumerate(x['stay']):
                if v is not False: errs.append(f'{i}: should-stay-locked state {k+1} unlocked ({v!r})')
        # C. fields
        if x['miss']: errs.append(f'{i}: missing {", ".join(x["miss"])}')
        if i not in icons: errs.append(f'{i}: no icon in ACH_ICONS')
        # D. writers
        src = x['src']
        keys = set(re.findall(r's\.(?:stats\?\.)?([A-Za-z_]\w*)', src))
        keys |= set(re.findall(r'\?\.([A-Za-z_]\w*)', src))
        keys |= set(re.findall(r'\.([A-Za-z_]\w*)\s*(?:\|\||>=|===|\)|;|,|\})', src))
        keys -= {'stats', 'check', 'count', 'length', 'every', 'some', 'has', 'add', 'size', 'max', 'min', 'keys', 'values',
                 'includes', 'forEach', 'ch', 'achievements', 'history', 'level', 'streak', 'Math', 'Object', 'Set'}
        for k in sorted(keys):
            if not re.search(r'(?<![\w.])%s\s*[:=](?!=)|\.%s\s*=(?!=)' % (k, k), outside):
                errs.append(f'{i}: reads "{k}" but nothing writes it')
        # F. float equality
        for m in re.finditer(r'([A-Za-z_]\w*)\s*(===|==)\s*-?\d', src):
            if FLOAT_LEAVES.search(m.group(1)):
                errs.append(f'{i}: exact compare on "{m.group(1)}", which is a float. Use a threshold.')

    # E. prompt check after hand-set flags
    flags = set()
    for x in res:
        for m in re.finditer(r'!!\(?\s*s\.([A-Za-z_]\w*)\s*\)?\s*(?:$|[,}\)])', x['src']):
            flags.add(m.group(1))
    for f in sorted(flags - PROMPT_EXEMPT):
        for n, ln in enumerate(lines):
            if re.search(r'progState\.%s\s*=\s*true' % f, ln):
                # The migration inside checkAchievements() itself needs no extra call.
                if any('function checkAchievements' in l for l in lines[max(0, n - 14):n]):
                    continue
                win = '\n'.join(lines[n:n + 14])
                if 'checkAchievements' not in win and 'progUpdate(' not in win:
                    warns.append(f'line {n+1}: progState.{f} is set with no checkAchievements() close behind it')

    print('=' * 70)
    print(f'  ACHIEVEMENT AUDIT: {len(ids)} achievements, {len(CASES)} test rows')
    print('=' * 70)
    for w in warns: print('  ! ' + w)
    for e in errs:  print('  x ' + e)
    if errs or warns:
        print(f'\n  {len(errs)} error(s), {len(warns)} warning(s). Do not ship.')
        print('=' * 70); return 1
    print(f'  ok  all {len(ids)} unlock on their passing state, stay locked when one step short,')
    print('      have names, Italian text, an icon, and a writer for every stat they read.')
    print('=' * 70); return 0

if __name__ == '__main__':
    sys.exit(main())
