"""Blurb checks, implementing what QUIZ_SPEC records rather than what feels right.

The two rules most easily got backwards:
  - Fragments are WRONG. The approved voice is one long flowing sentence and one
    short one. The early draft assumed clipped prose and Daniele's rewrites went
    the other way.
  - Two sentences of NEARLY EQUAL LENGTH is the actual failure. Measured SD of
    3.0 across 100 bad blurbs; the approved ones are long-then-short.
"""
import json,sys,re,os,statistics,collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intonare_quiz_lib as lib

# ── Language ─────────────────────────────────────────────────────────────────
# This whole file used to read F(r) and nothing else, so the Italian blurbs
# went through the draft gate unread. Every check that is not about English
# itself now runs on whichever side you ask for.
#
#     python3 intonare_blurb_draft_check.py draft.json           # English
#     python3 intonare_blurb_draft_check.py draft.json --lang it # Italian
#
# The English-only sections (British spelling, British vocabulary, British
# prose, the register targets taken from Daniele's edits) are skipped on the
# Italian pass rather than mistranslated into nonsense.
_args=[a for a in sys.argv[1:] if not a.startswith('-')]
LANG='it' if '--lang' in sys.argv and sys.argv[sys.argv.index('--lang')+1]=='it' else 'en'
EN = LANG=='en'
rows=json.load(open(_args[0] if _args else 'draft.json',encoding='utf-8'))

def F(x):  return (x.get('fact') if EN else x.get('fact_it')) or ''
def Q(x):  return (x.get('q') if EN else (x.get('q_it') or x.get('q'))) or ''
def O(x):
    o = x.get('opts') if EN else (x.get('opts_it') or x.get('opts'))
    return list(o or [])
def A(x):
    o = O(x)
    i = x.get('ans', 0) if 'ans' in x else 0
    return o[i] if o and 0 <= i < len(o) else ''

rows=[r for r in rows if F(r)]
if not rows:
    sys.exit(f'no {LANG} blurbs in this draft')
TICS=['most of what','most of the reason','which is why','is where','comes from',
      'turns up','built on','built around','whole point','runs on','is all about',
      'to this day','ever since','and that is']
EMPTY=['the rest is history','and the rest is history','never looked back',
       'the rest, as they say','a legend was born','history was made','changed everything forever']
BR=['honour','colour','favourite','behaviour','centre','theatre','realise','recognise',
    'organise','analyse','popularise','specialise','minimise','maximise','emphasise','criticise','memorise','apologise','summarise','travelling','cancelled','practise','licence','metre','grey',
    'programme','towards','amongst','whilst','learnt','spelt','defence','jewellery','per cent','favour','flavour','labour','neighbour','endeavour','armour','rumour','humour','harbour','vapour','odour','saviour','haemorrhage','aeroplane','moustache',
    'pyjamas','sceptical','aluminium','cheque','kerb','tyre','plough','draught']
# Italian twins. Repetition is measured per pack and the point is the same in
# either language: every instance reads fine alone, which is why no per-question
# check has ever caught one.
TICS_IT=['gran parte di','ed e per questo','e da qui che','viene da','salta fuori',
         'costruito su','tutto il senso','va avanti','e tutto incentrato',
         'ancora oggi','da allora','ed e cosi che']
EMPTY_IT=['e il resto e storia','non si e piu voltato indietro',
          'era nata una leggenda','ha fatto la storia',
          'e cambiato tutto per sempre']
err=[];warn=[];tic=collections.Counter()
for r in rows:
    f=F(r); q=Q(r)[:44]
    # Name the subject first, never a pronoun. Italian drops the subject
    # pronoun far more often than English, so an Italian blurb usually opens on
    # the noun already; what stands in for the fault there is a bare
    # demonstrative.
    _PRON = (r'^(He|She|It|They|His|Her|Their|This|That)\b' if EN
             else r'^(Lui|Lei|Loro|Esso|Essa|Questo|Questa|Questi|Queste|'
                  r'Quello|Quella|Il suo|La sua)\b')
    if re.match(_PRON,f):
        err.append(f'opens with a pronoun: {q}')
    s=[x.strip() for x in re.split(r'(?<=[.!?])\s+',f) if x.strip()]
    w=[len(x.split()) for x in s]
    # NOT a per-blurb rule. Measured against guitar_gods, 17 of its 43
    # two-sentence blurbs run a ratio under 1.8, and the lowest is 0.45 with the
    # SECOND sentence longer. A threshold here rejects 40% of the shipped pack
    # and rejected two of Daniele's own rewrites. The spec's "SD of 3.0" was a
    # property of the whole pack, not of one blurb: it is measured below.
    pass
    pass
    tot=len(f.split())
    # Recalibrated. 26 came from Beatles, which is a pack of stories about
    # people and can afford the room. An information-heavy pack runs shorter:
    # Daniele's own model blurb for this pack is 27 words carrying one idea,
    # and the first draft here averaged 36 trying to fit three. Under 14 is
    # usually a fragment; anything above that is a judgement, not a fault.
    if tot<14: warn.append(f'very short ({tot} words): {q}')
    # Raised from 58. Two of Daniele's own rewrites came in at 64, both because
    # he had swapped a summary for the actual quote and the numbers. Specifics
    # cost words and are worth them; the shipped pack's 58 was a description of
    # thinner writing, not a ceiling.
    if tot>68: warn.append(f'long ({tot} words): {q}')
    for e in (EMPTY if EN else EMPTY_IT):
        if e in f.lower(): err.append(f'empty closer "{e}": {q}')
    if EN:
        # Checked FIELD BY FIELD, not as one blob. Joining them put the first
        # option straight after the blurb's closing period, so a title sitting
        # in that slot read as sentence-initial and lost its proper-noun
        # exemption: "Rumours" was reported as a British spelling of "rumors"
        # on the shipped Seventies pack.
        #
        # A title keeps its own spelling. "Rumours" is the album and "Hapshash
        # and the Coloured Coat" is the band, and both fired here on approved
        # material. In prose, a capital that is not sentence-initial is a proper
        # noun. In an OPTION, any capital is: an option is a noun phrase, and a
        # British spelling that matters there is lowercase, as "Slides between
        # two neighbouring pitches" is.
        def _brit(text, is_option):
            out = []
            for b in BR:
                for _m in re.finditer(r'\b' + b + r'(s|d|ing|ed|ly|ite|ites)?\b',
                                      text, re.I):
                    if _m.group(0)[0].isupper():
                        if is_option:
                            continue
                        _before = text[:_m.start()].rstrip()
                        if _before and not _before.endswith(('.', '!', '?')):
                            continue
                    out.append(b)
                    break
            return out
        for b in _brit(f, False) + _brit(Q(r), False):
            err.append(f'British "{b}": {q}')
        for _o in O(r):
            for b in _brit(_o, True):
                err.append(f'British "{b}" in an option: {q}')
    if '\u2014' in f: err.append(f'em-dash: {q}')
    # NOT a warning. The rules say to name the subject first, so a blurb about
    # the Mellotron opening with "The Mellotron" is obeying them. Fired on 8 of
    # 90 correct blurbs before it was demoted. What matters is whether the
    # sentence ADDS anything, and no check can see that; read them instead.
    if A(r).lower() in ' '.join(s[:1]).lower():
        pass
    for t in (TICS if EN else TICS_IT):
        if t in f.lower(): tic[t]+=1
# A blurb can hand over another question's answer. Two did: one named Peter
# Blake in a blurb about the Sgt. Pepper sleeve, and one said outright that Mal
# Evans counted the bars on A Day in the Life. Both are separate questions.
# Most hits are incidental ("Liverpool" in a blurb is not the airport question),
# so this reports rather than errors: read each one.
_leak=[]
for r in rows:
    for o in rows:
        if o is r: continue
        a=A(o)
        if len(a)>8 and a.lower() in F(r).lower():
            _leak.append((a,Q(r)[:40],Q(o)[:40]))
print(f'{len(rows)} blurbs | errors {len(err)} | warnings {len(warn)} | answer mentions {len(_leak)}')
for e in err: print('  ERR  '+e)
for w in warn: print('  warn '+w)
if rows:
    W=[len(F(r).split()) for r in rows]
    print(f'  words: median {statistics.median(W):.0f}, range {min(W)}-{max(W)}  (guitar_gods: 39, 28-58)')
    _all=[len(x.split()) for r in rows for x in re.split(r'(?<=[.!?])\s+',F(r)) if x.strip()]
    _sd=statistics.pstdev(_all)
    print(f'  sentence-length SD across the pack: {_sd:.1f}  (guitar_gods 11.0; flat prose measured 3.0)')
    if _sd < 7: print('  WARN the pack reads flat: vary how long the sentences run')
    rate=sum(tic.values())/len(rows)
    print(f'  repeated constructions: {sum(tic.values())} = {rate:.2f}/blurb (warn at 0.08)')
    for t,n in tic.most_common(6): print(f'     {t} x{n}')

# ── Run-on check ─────────────────────────────────────────────────────────────
# Absorbing every closing fact into the sentence above fixes one sameness and
# creates a worse one. Measured against guitar_gods, per SENTENCE:
#     words    median 29, 90th 40, max 45
#     commas   median 1,  90th 2,  max 3
#     connectives (and/then/but/so/which/while)  median 1, 90th 3, max 4
# A sentence past those is not carrying the reader, it is dragging them.
#
# The fix is rarely to cut a fact. It is to move the SPLIT to where the thought
# actually turns, and let the second sentence pick the thread up with a
# connective: "...cleared one at a time by EMI's lawyers. They wrote to every
# living person on it, though Gandhi was taken out at the last minute."
#
# RECALIBRATED, per language. The old numbers were 45 words for both, and the
# first thing the bilingual run flagged was the Angus Young blurb out of
# QUIZ_VOICE.md, in Italian, at 44 words. That is the gold standard failing its
# own check. Measured over 870 English and 867 Italian sentences in the six
# authored packs, the ceilings are 48 words English and 53 Italian; Italian is
# only 5 to 10 percent longer at the tail, so it needs its own number rather
# than a shared one. lib.RUNON_* holds them.
_JOIN = (r'\b(and|then|but|so|which|while)\b' if EN
         else r'\b(e|poi|ma|quindi|che|mentre)\b')
_ro=[]
for r in rows:
    for s in lib.sentences(F(r)):
        if not lib.runon(s, LANG): continue
        w=len(s.split()); c=s.count(','); k=len(re.findall(_JOIN,s,re.I))
        why=[]
        if w>lib.RUNON_WORDS[LANG]: why.append(f'{w} words')
        if c>lib.RUNON_COMMAS:      why.append(f'{c} commas')
        if k>lib.RUNON_JOINERS[LANG]: why.append(f'{k} connectives')
        _ro.append((', '.join(why), Q(r)[:40], s[:88]))
print(f'  run-on risk: {len(_ro)} sentence(s) past the shipped ceiling')
for why,q,s in _ro: print(f'    [{why}] {q}\n      {s}...')

# ── One thread, not a life ───────────────────────────────────────────────────
# The fault Daniele kept correcting by hand, finally measured. guitar_gods runs
# a MEDIAN OF 0 sequence markers and only 2% of its blurbs narrate two or more
# steps in time. A first draft of this pack ran a median of 1 and 13%.
#
# The difference is not length or facts. It is that the approved blurbs follow
# ONE thread, or state a thing and its consequence, while the draft walked
# through a life: sold a painting, bought a bass, joined a band, stayed in
# Hamburg, went to art school, died there. Six steps, no story.
#
# His corrections all cut the clause belonging to a DIFFERENT thread:
#   cut  "spent seven years scoring their ideas for orchestras"  (Martin's age
#        and being called sir are one thread; his arranging is another)
#   cut  "had his own following in Liverpool"  (the sacking is the thread)
# Narrowed after measuring. The first version counted before/after/until, which
# are usually just prepositions ("the day before a session") and put the
# approved pack over the line too. These are the markers that actually say "and
# then the next thing happened", which is the biography habit being hunted.
_SEQ = (r'\bthen\b|\blater\b|\bafterward\b|\beventually\b|\bwent on to\b|'
        r'\bby which time\b|\bended up\b' if EN else
        r'\bpoi\b|\bin seguito\b|\bpi\u00f9 tardi\b|\balla fine\b|'
        r'\bfin\u00ec per\b|\bsuccessivamente\b|\bda l\u00ec\b')
_seq=[(len(re.findall(_SEQ,F(r),re.I)), Q(r)[:40], F(r)[:80]) for r in rows]
_multi=[x for x in _seq if x[0]>=2]
_med=statistics.median([x[0] for x in _seq])
print(f'  sequence markers: median {_med:.0f} (guitar_gods 0) | '
      f'{100*len(_multi)/len(rows):.0f}% narrate 2+ steps (guitar_gods 2%)')
for n,q,f in _multi:
    print(f'    [{n} steps] {q}\n      {f}...')

# ── Register, learned from a real edit pass ──────────────────────────────────
# 26 edited blurbs, measured mine against his. The rhythm was already identical:
# median 2 sentences, 24 words each. Every structural rule I derived was aimed
# at the wrong axis. What actually changed was register and specificity.
#
#                          mine   his
#   contractions              5    11
#   exclamation marks         1     5
#   quoted words / lyrics     4    14
#   "only" / "just"           0     3
#   "which" as a joiner       6     3
#
# He also replaced summary with the thing itself: the actual Scrambled Eggs
# lyric instead of "Portugal gave him the real words", Harrison's own sentence
# about the chord instead of "a mathematician ran a Fourier transform".
_reg = {
  'contractions': len(re.findall(r"\b\w+['\u2019](s|ll|re|ve|t)\b", ' '.join(F(r) for r in rows))),
  'exclamations': sum(1 for r in rows if '!' in F(r)),
  'quoted':       len(re.findall(r'["\u201c\u201d]', ' '.join(F(r) for r in rows))) // 2,
  'which-joins':  len(re.findall(r'\bwhich\b', ' '.join(F(r) for r in rows))),
}
_per = {k: v / max(len(rows), 1) for k, v in _reg.items()}
# The targets are Daniele's numbers from an English edit pass. Italian
# contracts differently (l', dell', un') and has no twin for "which" as a
# joiner, so the Italian side reports the measurement without a target rather
# than scoring itself against a number that does not apply to it.
if EN:
    print(f"  register per blurb: contractions {_per['contractions']:.2f} (his 0.42) | "
          f"exclamations {_per['exclamations']:.2f} (his 0.19) | "
          f"quoted {_per['quoted']:.2f} (his 0.54) | "
          f"which {_per['which-joins']:.2f} (his 0.12)")
else:
    print(f"  register per blurb: exclamations {_per['exclamations']:.2f} | "
          f"quoted {_per['quoted']:.2f}   (no English targets apply)")

# ── British VOCABULARY, which no spelling check sees ──────────────────────────
# "zebra crossing" is spelled the same on both sides of the Atlantic and is
# still the wrong word. He changed it to crosswalk.
_BRV = {'zebra crossing':'crosswalk','coach':'bus','lorry':'truck','queue':'line',
        'autumn':'fall','posh':'expensive/upmarket','mate':'friend','fortnight':'two weeks',
        'storeys':'stories','cinema':'movie theater','holiday':'vacation','motorway':'highway',
        'petrol':'gas','trousers':'pants','biscuit':'cookie','rubbish':'garbage','bloke':'guy',
        'chemist':'drugstore','torch':'flashlight','pram':'stroller'}
# "flat" needs an article or it fires on "lay flat on his back" and "a flat fee"
_BRV_ART = {'flat':'apartment'}
# MUSIC terminology, which is the half of this the original list missed entirely.
# The list above is general-life words: it would catch a pram in a music quiz,
# which will never happen, while "semitone" went past it two hundred times. A
# spelling audit cannot help here either, because these are spelled the same in
# both dialects; only the word choice differs. US theory teaching says half step,
# whole step and measure, and every American textbook and the AP course
# description follow that.
_BRV_MUS = {
    'stave':'staff', 'staves':'staff',
    'quaver':'eighth note', 'crotchet':'quarter note', 'minim':'half note',
    'semibreve':'whole note', 'semiquaver':'sixteenth note',
    'demisemiquaver':'thirty-second note', 'breve':'double whole note',
    'leading note':'leading tone',
    'perfect cadence':'authentic cadence',
    'imperfect cadence':'half cadence',
    'interrupted cadence':'deceptive cadence',
    'tonic sol-fa':'solfege',
}
# "bar" only counts when it is a measure of music. Unguarded it fires on the
# toolbar, the progress bar and the timer bar, which outnumber the musical ones.
_BRV_BAR = (r'\b(?:a|the|per|each|one|two|three|four|eight|sixteen|first|last|next|'
            r'previous|whole|half|same|opening|closing|final)\s+bars?\b'
            r'|\bbars?\s+(?:of|in|later|long|before|after|earlier)\b')
_bv=[]
for r in (rows if EN else []):
    for w,us in _BRV.items():
        if re.search(r'\b'+w+r'\b', F(r)+' '+Q(r), re.I):
            _bv.append((w, us, Q(r)[:38]))
    for w,us in _BRV_ART.items():
        if re.search(r'\b(?:a|the|his|her|their)\s+'+w+r'\b(?!\s*(?:fee|rate|session))', F(r)+' '+Q(r), re.I):
            _bv.append((w, us, Q(r)[:38]))
    for w,us in _BRV_MUS.items():
        if re.search(r'\b'+w+r'\b', F(r)+' '+Q(r), re.I):
            _bv.append((w, us, Q(r)[:38]))
print(f'  British vocabulary: {len(_bv)} (spelling checks do not see these)')
for w,us,q in _bv: print(f'    {w} -> {us}   in: {q}')

# ── Omega leak pass ──────────────────────────────────────────────────────────
# Reports every blurb that names another question's answer, with the shared
# words, so the pair can be read. A tighter rule requiring two shared subject
# words found NOTHING and missed two real leaks, because "drums" in the question
# and "drumming" in the blurb are not the same string. This one is a reading
# aid, not a verdict: expect roughly fifteen hits on a ninety-question pack and
# expect most of them to be harmless.
# The stop list has to match the language, or every Italian stem matches every
# other one: running the English list over Italian took the leaning-pair count
# from 12 to 60 on the same pack, because "quale", "della" and "parte" counted
# as content words.
def _kw(q): return lib.content_words(q, LANG)
_om=[]
for _i,_r in enumerate(rows,1):
    for _j,_o in enumerate(rows,1):
        if _i==_j: continue
        _a=A(_o)
        if len(_a)<8: continue
        if re.search(r'\b'+re.escape(_a)+r'\b',F(_r),re.I):
            _sh=sorted(_kw(Q(_o)) & lib.content_words(F(_r), LANG))
            _om.append((_i,_j,_a,_sh))
print(f'  omega leak pass: {len(_om)} blurb/question pairs to read')
for _i,_j,_a,_sh in _om:
    print(f"    blurb {_i} names \"{_a}\" (answer to {_j}){'  shared: '+', '.join(_sh) if _sh else ''}")

# ── Question contradicting its own blurb ─────────────────────────────────────
# Question 38 asked about an engineer "at just twenty years old" and its blurb
# said nineteen. Nothing else catches that: both are grammatical, neither is a
# duplicate, and the fault only appears when the two are read together.
_NUM={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,
 'eleven':11,'twelve':12,'thirteen':13,'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,
 'nineteen':19,'twenty':20,'thirty':30,'forty':40,'fifty':50}
def _nums(t):
    out=set(int(x.replace(',','')) for x in re.findall(r'\b\d[\d,]*\b',t))
    for w,v in _NUM.items():
        if re.search(r'\b'+w+r'\b',t,re.I): out.add(v)
    return out
_mm=[]
for r in rows:
    for a in _nums(Q(r)):
        for b in _nums(F(r)):
            if a!=b and abs(a-b)<=2 and a>2: _mm.append((a,b,Q(r)[:46]))
print(f'  near-miss numbers between question and blurb: {len(_mm)} (read them; most are fine)')
for a,b,q in _mm: print(f'    question {a} / blurb {b}   {q}')

# ── British PROSE, which is neither spelling nor vocabulary ──────────────────
# "colour" is a spelling. "zebra crossing" is a vocabulary item. "rather than",
# "on the grounds that", "in the twenties" and "far more" are none of those:
# they are how a British writer builds a sentence, and they pass every other
# check in this file.
_BRIT_PROSE = {
 r'\brather than\b': 'instead of',
 r'\broughly\b': 'about',
 r'\bon the grounds that\b': 'because',
 r'\bfar (more|harder|less|better|worse)\b': 'much / way',
 r'\breckon(s|ed|ing)?\b': 'figure / think',
 r'\bin the (twenties|thirties|forties|fifties|sixties|seventies|eighties|nineties)\b': 'use digits',
 r'\bwhole reason\b': 'the reason',
 r'\bnowadays\b': 'these days',
 r'\bplenty of\b': 'a lot of',
 r'\bhaving a\b': 'often British sequencing',
 r'\bshan\u2019?t\b': 'not American',
 r'\bfortnight\b': 'two weeks',
}
_bp = []
for r in (rows if EN else []):
    for p_, note in _BRIT_PROSE.items():
        m = re.search(p_, F(r), re.I)
        if m: _bp.append((m.group(0), note, Q(r)[:40]))
print(f'  British prose habits: {len(_bp)}')
for w, note, q in _bp: print(f'    "{w}" -> {note}   in: {q}')

# ── Does the blurb carry a FACT, or just an observation? ─────────────────────
# The Guitar easy tier came back with 33 of 40 rewritten, and a large part of
# it was blurbs that made a general remark instead of stating something. A
# did-you-know needs a name, a number or a date; "most beginners press too hard"
# is not one, and neither is "factories ship guitars set high".
_NOTNAME = {'The','A','An','That','This','It','Take','Play','Tune','Most','Some','Every',
            'Nothing','Beginners','Guitarists','Teachers','Session','Classical','Metal',
            'Cheap','Standard','Which','Live','Folk','Palm','Barre','Studio','Wood','Frets',
            'Action','Stage','Calluses','Nuts','Twelve','Three','Big','Ten','Lifting','Factories'}
_GENERAL = [r'\bmost (beginners|players|people|of them)\b', r'\bnobody\b',
            r'\balmost (nobody|every|all)\b', r'\bplayers (learn|find|say)\b',
            r'\bteachers (usually |often )?say\b', r'\bit is why\b']
# English only: _NOTNAME is a list of English sentence openers, and Italian
# capitalises far less, so an Italian blurb legitimately carries fewer capitals
# and would be flagged for writing correct Italian.
_noFact = []
for r in (rows if EN else []):
    names = [w for w in re.findall(r"\b[A-Z][a-z']+\b", F(r)) if w not in _NOTNAME]
    nums  = re.search(r'\b\d', F(r))
    if not names and not nums: _noFact.append(Q(r)[:44])
_gen = [(re.search(p_, F(r), re.I).group(0), Q(r)[:40])
        for r in (rows if EN else []) for p_ in _GENERAL if re.search(p_, F(r), re.I)]
print(f'  blurbs with no name, number or date: {len(_noFact)} of {len(rows)}')
for q in _noFact: print('    ' + q)
if _gen:
    print(f'  generalisations standing in for a fact: {len(_gen)}')
    for w, q in _gen: print(f'    "{w}"   in: {q}')

# ── An answer restated in another form ──────────────────────────────────────
# Blurb 102 said "a 25.5-inch scale" while question 41's answer is "25.5
# inches". The omega leak pass compares whole option strings, so it never
# matched. Numbers and model names leak just as badly in a different wrapper.
_TOKEN = re.compile(r'\b\d[\d.,]*\b|\b[A-Z][\w-]{3,}\b')
_restated = []
for i, a in enumerate(rows, 1):
    for j, b in enumerate(rows, 1):
        if i == j: continue
        toks = set(_TOKEN.findall(A(b)))
        if not toks: continue
        hit = [x for x in toks if re.search(r'\b' + re.escape(x), F(a))]
        if hit and len(hit) == len(toks):
            _restated.append((i, j, ', '.join(sorted(toks))))
print(f'  answers restated inside another blurb: {len(_restated)}')
for i, j, t_ in _restated: print(f'    blurb {i} carries "{t_}" — the answer to {j}')
