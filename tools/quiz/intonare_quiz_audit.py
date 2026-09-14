#!/usr/bin/env python3
"""
INTONARE QUIZ AUDIT — v2.0
===========================
Flags questions where the correct answer is significantly longer than the wrong answers.
Detects length giveaways that let players bypass reading the question.

Usage:
    python3 intonare_quiz_audit.py [path/to/Intonare.html]

Output:
    Prints a per-pack summary and writes quiz_audit_report.txt.

Thresholds:
    CRITICAL  >2.5x  — fix before shipping
    WARN      >1.8x  — fix if easy

─────────────────────────────────────────────────────────────
QUESTION WRITING GUIDE
─────────────────────────────────────────────────────────────

THE CORE PROBLEM
The most common failure mode is a length giveaway: the correct answer
is a full explanation while wrong answers are lazy two-word labels.
Players learn to pick the longest option without reading the question.

  Bad:   ✓ "The commercial songwriting hub on 28th Street, New York..."
         ✗ "A Nashville street"
         ✗ "A type of piano music"

  Good:  ✓ "The commercial songwriting hub on 28th Street, New York..."
         ✗ "The district in Nashville around Music Row where country publishing..."
         ✗ "A style of syncopated ragtime piano named after the bright, percussive..."

RULES FOR WRONG ANSWERS
  1. Be specific, not vague. "A type of jazz" is not a wrong answer.
  2. Match the correct answer's length roughly — all four within ~1.5x.
  3. Make them plausible. Partial knowledge might genuinely believe them.
  4. No single noun-phrase answers: "A Nashville street", "A jazz club".
  5. Don't make wrong answers accidentally correct.
  6. Avoid overlapping answers — if two mean the same thing, consolidate.

RULES FOR CORRECT ANSWERS
  1. Trim where you can. Core claim in the option; full detail goes in fact.
  2. Don't pad. Correct ≠ longest.
  3. Avoid em-dashes in option text — display trims at em-dashes.

THE FACT FIELD
  Every question should have a fact (shown after answering):
  - Adds context beyond the correct answer — don't just repeat it
  - One or two sentences is fine
  - Can disambiguate the wrong answers

FORMAT REFERENCE
  {
    q: "Question text here?",
    opts: ["Option A", "Option B", "Option C — correct one", "Option D"],
    ans: 2,      // 0-indexed position of correct answer in opts[]
    fact: "Context or detail shown after the player answers."
  }

  Rules:
  - q ends with ?, no trailing space
  - opts always exactly 4 options
  - ans is integer 0–3
  - fact is required; empty string "" is acceptable but try
  - Use double quotes; escape internals with \\" and \\'
  - No trailing comma after the last question in a pack's array

DIFFICULTY TIERS (by array position)
  Easy    First 12 questions — most accessible, well-known facts
  Medium  All questions
  Hard    From index 18

  Put famous Hendrix / Beatles facts at the front, not the back.

ADDING A NEW PACK
  1. Add pack object to const PACKS with name, emoji, color, desc, questions
  2. Add colour entry to MQ_PACK_COLORS
  3. Add pack id and display name to PACK_IDS / PACK_NAMES below
  4. Run this audit — target zero criticals

─────────────────────────────────────────────────────────────
"""

import re
import os
import sys

HTML_PATH   = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'Intonare.html')
REPORT_PATH = os.path.join(os.path.dirname(os.path.abspath(HTML_PATH)), 'quiz_audit_report.txt')

PACK_IDS = [
    'guitar_gods', 'beatles', 'jazz_legends', 'rock_metal',
    'theory_fundamentals', 'studio_recording', 'gear_equipment', 'music_history',
    'guitar_technique', 'bass', 'drums', 'keys', 'vocals',
    'fifties', 'sixties', 'seventies', 'eighties', 'nineties', 'noughties'
]

PACK_NAMES = {
    'guitar_gods':         'Guitar Gods',
    'beatles':             'Beatles',
    'jazz_legends':        'Jazz Legends',
    'rock_metal':          'Rock & Metal',
    'theory_fundamentals': 'Theory Fundamentals',
    'studio_recording':    'Studio & Recording',
    'gear_equipment':      'Gear & Equipment',
    'music_history':       'Music History',
    'guitar_technique':    'Guitar Technique',
    'bass':                'Bass',
    'drums':               'Drums',
    'keys':                'Keys',
    'vocals':              'Vocals',
    'fifties':             '1950s',
    'sixties':             '1960s',
    'seventies':           '1970s',
    'eighties':            '1980s',
    'nineties':            '1990s',
    'noughties':           '2000s',
}


def trim_opt(text):
    """Mirror the app's display trimming logic."""
    for dash in [' \u2014 ', ' \u2013 ']:
        d = text.find(dash)
        if d > 0:
            text = text[:d]
    if len(text) > 60:
        breaks = [text.rfind(', ', 0, 60), text.rfind(' (', 0, 60), text.rfind(': ', 0, 60)]
        cut = max(breaks)
        if cut > 20:
            text = text[:cut]
    return text.strip()


def parse_questions(block):
    """Brace-matched parser: robust to commas/brackets inside strings."""
    questions = []
    i = 0
    while True:
        i = block.find('{q:"', i)
        if i == -1:
            break
        depth = 0; j = i
        while j < len(block):
            c = block[j]
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    j += 1; break
            j += 1
        obj = block[i:j]
        i = j
        qm = re.search(r'q:"((?:[^"\\]|\\.)*)"', obj)
        # Whitespace-tolerant. The Bass pack writes "opts:[...], opts_it:[...],
        # ans:0" and this parser silently reported BASS (0Q) for 106 questions,
        # which is worse than an error because it reads as a pass.
        om = re.search(r'\bopts\s*:\s*\[(.*?)\]\s*,\s*(?:opts_it|ans)\s*:', obj, re.S)
        am = re.search(r'\bans\s*:\s*(\d+)', obj)
        fm = re.search(r'fact:"((?:[^"\\]|\\.)*)"', obj)
        if not (qm and om and am):
            continue
        def unesc(s):
            return s.replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
        q_text = unesc(qm.group(1))
        opts = [unesc(o) for o in re.findall(r'"((?:[^"\\]|\\.)*)"', om.group(1))]
        ans = int(am.group(1))
        fact = unesc(fm.group(1)) if fm else ''
        if opts and ans < len(opts):
            questions.append({'q': q_text, 'opts': opts, 'ans': ans, 'fact': fact})
    return questions


def audit():
    with open(HTML_PATH) as f:
        content = f.read()

    packs_start = content.find('const PACKS = {')
    packs_end   = content.find('\nconst MQ_PACK_COLORS', packs_start)
    if packs_start < 0 or packs_end < 0:
        print("ERROR: Could not find PACKS block in Intonare.html")
        return

    packs_js = content[packs_start:packs_end]

    lines = [
        'INTONARE QUIZ AUDIT REPORT',
        '=' * 62,
        '',
        'CRITICAL (>2.5x): correct answer is a dead giveaway — fix before shipping',
        'WARN     (>1.8x): noticeably longer — fix if easy',
        '',
        'Format: #N [ratio]  Q text',
        '        ✓ (trimmed_len)  displayed correct answer',
        '        ✗ (trimmed_len)  displayed wrong answer',
        '',
    ]

    total_crit = total_warn = total_q = 0

    for pid in PACK_IDS:
        p_start = packs_js.find(f'{pid}:')
        p_end   = packs_js.find('\n},\n\n', p_start)
        if p_end < 0: p_end = len(packs_js)
        block = packs_js[p_start:p_end]
        qs    = parse_questions(block)
        total_q += len(qs)

        crits, warns = [], []
        for i, q in enumerate(qs):
            ct    = len(q['opts'][q['ans']])
            wts   = [len(q['opts'][j]) for j in range(len(q['opts'])) if j != q['ans']]
            avg_w = sum(wts) / len(wts) if wts else 0
            if avg_w == 0: continue
            # MEASURE THE RAW OPTION, NOT THE TRIMMED ONE. This is why the audit
            # reported "no criticals — good to ship" while giveaways were being found
            # by hand. It was scoring what the app DISPLAYS, and the app's trimmer cuts
            # long options to ~60 chars. So a 151-char correct answer against 26/32/40
            # char distractors — a 4.6x giveaway — was trimmed to 32 chars before being
            # measured, scored ~1.0x, and passed. The trimmer was hiding the exact fault
            # this script exists to catch.
            ratio = ct / avg_w
            entry = {'n': i + 1, 'q': q, 'ratio': ratio, 'ct': ct}
            if ratio >= 2.5:   crits.append(entry)
            elif ratio >= 1.8: warns.append(entry)

        total_crit += len(crits)
        total_warn += len(warns)
        name = PACK_NAMES.get(pid, pid)

        if not crits and not warns:
            lines.append(f'━━ {name.upper()} ({len(qs)}Q) — clean ✓')
            lines.append('')
            continue

        lines.append(f'━━ {name.upper()} ({len(qs)}Q) ━━')
        for label, entries, prefix in [('⛔ CRITICAL', crits, '  '), ('⚠ WARN', warns, '  ')]:
            if not entries: continue
            lines.append(f'  {label} ({len(entries)}):')
            for e in sorted(entries, key=lambda x: -x['ratio']):
                q = e['q']
                lines.append(f"    #{e['n']:02d} [{e['ratio']:.1f}x]  {q['q'][:75]}")
                lines.append(f"         ✓ ({e['ct']}c)  {trim_opt(q['opts'][q['ans']])[:75]}")
                for j, w in enumerate(q['opts']):
                    if j != q['ans']:
                        lines.append(f"         ✗ ({len(trim_opt(w))}c)  {trim_opt(w)[:75]}")
                lines.append('')

    lines.insert(8, f'Total questions: {total_q}   CRITICAL: {total_crit}   WARN: {total_warn}   Clean: {total_q - total_crit - total_warn}')

    report = '\n'.join(lines)
    with open(REPORT_PATH, 'w') as f:
        f.write(report)

    print(f'\nIntonare Quiz Audit')
    print(f'{"=" * 40}')
    print(f'Questions:  {total_q}')
    print(f'Critical:   {total_crit}  (fix before shipping)')
    print(f'Warn:       {total_warn}  (fix if easy)')
    print(f'Clean:      {total_q - total_crit - total_warn}')
    print()

    for pid in PACK_IDS:
        p_start = packs_js.find(f'{pid}:')
        p_end   = packs_js.find('\n},\n\n', p_start)
        if p_end < 0: p_end = len(packs_js)
        qs = parse_questions(packs_js[p_start:p_end])
        c = w = 0
        for q in qs:
            ct    = len(q['opts'][q['ans']])
            wts   = [len(q['opts'][j]) for j in range(len(q['opts'])) if j != q['ans']]
            avg_w = sum(wts) / len(wts) if wts else 0
            if avg_w == 0: continue
            r = ct / avg_w
            if r >= 2.5:   c += 1
            elif r >= 1.8: w += 1
        status = '✓' if c == 0 and w == 0 else ('⛔' if c > 0 else '⚠')
        print(f'  {status}  {PACK_NAMES.get(pid, pid):<22} crit:{c:2d}  warn:{w:2d}')

    print(f'\nFull report written to: {REPORT_PATH}')
    if total_crit == 0: print('No criticals — good to ship.')
    else: print(f'{total_crit} critical issue(s) need fixing before shipping.')


if __name__ == '__main__':
    audit()
