#!/usr/bin/env python3
"""
intonare_groove_audit.py

Audits GROOVE_PRESETS in Intonare.html for structure, duplicates, and - the
point of the thing - whether each groove has a real source behind it.

Usage:  python3 intonare_groove_audit.py [path/to/Intonare.html] [> GROOVE_AUDIT.txt]

WHY THIS EXISTS
    The previous version of this script only read comments sitting ABOVE the
    `id:` line, so any groove documented below its id read as undocumented. That
    inflated the unverified count from 8 to 20 and sent a whole session chasing
    grooves that were already fine. This version reads the entire object.

STATUS CLASSES
    SOURCED    comment contains at least one http(s) URL. A real citation.
    CONFLICT   comment contains a conflict marker. Sources disagree; a judgement
               call was made and is reversible. Read the comment before touching.
    FLAGGED    comment contains a warning marker but no URL. Known-unresolved.
    DESCRIBED  comment exists but cites nothing. Someone's assertion, not proof.
    NONE       no comment at all.

    CONSTRUCTED      an invented teaching cell, not a transcription of anything.
                     Cannot ever have a citation; what CAN be true of it is that
                     its comment describes its own notes, and that is checked.
    BY-CONSTRUCTION  derived from another entry by a rule stated in the comment
                     (e.g. a 2-3 clave is its 3-2 parent with halves swapped).
                     The parent carries the citation; duplicating it here would
                     be noise.

    SOURCED, CONFLICT, CONSTRUCTED and BY-CONSTRUCTION all count as done. The last
    two are done in a different sense from the first two and the ledger says which.
    DESCRIBED is not done; it reads like documentation and isn't.
"""

import os
import re
import sys
from collections import defaultdict

WARN = "\u26a0"                 # the warning triangle used in the file's comments
CONFLICT_HINT = "SOURCES GENUINELY CONFLICT"
CONSTRUCTED_HINT = "CONSTRUCTED, not transcribed"
BYCONSTRUCTION_HINT = "VERIFIED BY CONSTRUCTION"


# ---------------------------------------------------------------- parsing ----

def load_presets(path):
    html = open(path, encoding="utf-8").read()
    start = html.find("const GROOVE_PRESETS = [")
    if start < 0:
        sys.exit("GROOVE_PRESETS not found; has the constant been renamed?")
    end = html.find("\n];", start)
    block = html[start:end]

    presets, cursor = [], 0
    while True:
        obj_start = block.find("\n  {\n", cursor)
        if obj_start < 0:
            break
        obj_end = block.find("\n  },", obj_start + 1)
        if obj_end < 0:
            break
        raw = block[obj_start:obj_end + 5]
        cursor = obj_end + 1

        def field(name):
            m = re.search(r"%s:\s*'((?:[^'\\]|\\.)*)'" % name, raw)
            return m.group(1).replace("\\'", "'") if m else None

        pid = field("id")
        if not pid or pid == "custom":
            continue

        steps_at = raw.find("steps: [")
        if steps_at < 0:
            continue
        steps = [int(x) for x in raw[steps_at + 8:raw.find("]", steps_at)].split(",")]

        beats_m = re.search(r"beats:\s*(\d+)", raw)
        comment = [ln.strip()[3:].strip()
                   for ln in raw.split("\n") if ln.strip().startswith("//")]

        presets.append({
            "id": pid,
            "name": field("name") or pid,
            "cat": field("cat") or "?",
            "origin": field("origin") or "",
            "beats": int(beats_m.group(1)) if beats_m else 4,
            "steps": steps,
            "comment": comment,
        })
    return presets


def status_of(p):
    body = " ".join(p["comment"])
    if not body:
        return "NONE"
    if CONFLICT_HINT in body:
        return "CONFLICT"
    # Order matters: a constructed cell can never have a citation, so it must be
    # classified before the URL test rather than after it, or a constructed entry
    # that happens to reference a source in passing would read as SOURCED.
    if CONSTRUCTED_HINT in body:
        return "CONSTRUCTED"
    if BYCONSTRUCTION_HINT in body:
        return "BY-CONSTRUCTION"
    if re.search(r"https?://", body):
        return "SOURCED"
    if WARN in body:
        return "FLAGGED"
    return "DESCRIBED"


def first_url(p):
    m = re.search(r"https?://\S+", " ".join(p["comment"]))
    return m.group(0).rstrip(".,") if m else ""


# ------------------------------------------------------------- rendering ----

TICKS = ["", "e", "&", "a"]


def beat_language(p):
    """Render onsets as musicians count them: 1, 1e, 2&, 3a ... (w) = weak."""
    steps, beats = p["steps"], p["beats"]
    if beats == 0 or len(steps) % beats:
        return ["(cannot render: %d steps do not divide into %d beats)"
                % (len(steps), beats)]
    per = len(steps) // beats
    out = []
    for i, v in enumerate(steps):
        if not v:
            continue
        beat, sub = divmod(i, per)
        if per == 4:
            label = "%d%s" % (beat + 1, TICKS[sub])
        elif per == 2:
            label = "%d%s" % (beat + 1, "&" if sub else "")
        elif per == 1:
            label = str(beat + 1)
        else:
            label = "%d.%d" % (beat + 1, sub)
        out.append(label + ("(w)" if v == 1 else ""))
    return out


def onsets(p):
    return [i for i, v in enumerate(p["steps"]) if v]


# ------------------------------------------------------------------ main ----

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'Intonare.html')
    presets = load_presets(path)
    ver = re.search(r"INTONARE_VERSION: ([\d.]+)", open(path, encoding="utf-8").read(2000))

    print("GROOVE AUDIT - %d grooves in %s" % (len(presets), path))
    if ver:
        print("build v%s" % ver.group(1))
    print()

    # 1. structure ------------------------------------------------------------
    bad = [p for p in presets if p["beats"] == 0 or len(p["steps"]) % p["beats"]]
    print("1. STRUCTURE")
    if bad:
        for p in bad:
            print("   !! %-22s %d steps do not divide into %d beats"
                  % (p["name"], len(p["steps"]), p["beats"]))
    else:
        print("   %d/%d divide evenly into their beats" % (len(presets), len(presets)))
    print()

    # 2. source ledger --------------------------------------------------------
    by_status = defaultdict(list)
    for p in presets:
        by_status[status_of(p)].append(p)

    done = (len(by_status["SOURCED"]) + len(by_status["CONFLICT"])
            + len(by_status["CONSTRUCTED"]) + len(by_status["BY-CONSTRUCTION"]))
    print("2. SOURCE LEDGER  -  %d/%d vetted" % (done, len(presets)))
    print()
    for label, blurb in [
        ("SOURCED",         "citation present, considered done"),
        ("CONFLICT",        "sources disagree; judgement call, reversible"),
        ("CONSTRUCTED",     "teaching cell, not a transcription; claim checked against notes"),
        ("BY-CONSTRUCTION", "derived from another entry by a stated rule; parent carries the citation"),
        ("FLAGGED",         "known unresolved, reason written in the file"),
        ("DESCRIBED",       "comment asserts something but cites nothing - NOT done"),
        ("NONE",            "no comment at all - NOT done"),
    ]:
        group = by_status[label]
        print("   %s (%d)  %s" % (label, len(group), blurb))
        for p in sorted(group, key=lambda x: x["name"]):
            line = "      %-22s %s" % (p["name"], p["origin"])
            print(line)
            if label in ("SOURCED", "CONFLICT") and first_url(p):
                print("         %s" % first_url(p))
        print()

    # 3. duplicates -----------------------------------------------------------
    print("3. DUPLICATE PATTERNS  -  different names, identical steps")
    seen = defaultdict(list)
    for p in presets:
        seen[tuple(p["steps"])].append(p)
    dups = [g for g in seen.values() if len(g) > 1]
    if not dups:
        print("   none")
    for group in dups:
        names = [p["name"] for p in group]
        documented = any("deliberately identical" in " ".join(p["comment"])
                         or "same as the son clave" in " ".join(p["comment"])
                         for p in group)
        print("   %s %s" % ("ok" if documented else "!!", names))
        print("      %s" % list(group[0]["steps"]))
        if not documented:
            print("      Unsourced duplicate: at least one of the pair is wrong.")
    print()

    # 3b. shared onsets, different weights ------------------------------------
    print("3b. SHARED ONSETS  -  same hits, different accents. Check these are meant.")
    on = defaultdict(list)
    for p in presets:
        on[(p["beats"], tuple(onsets(p)))].append(p["name"])
    shared = [v for v in on.values() if len(v) > 1]
    if not shared:
        print("   none")
    for names in shared:
        print("   %s" % names)
    print()

    # 4. beat language --------------------------------------------------------
    print("4. EVERY PATTERN IN BEAT LANGUAGE  (S = accent, w = weak)")
    print("   Give this section to someone who plays the style. No code required.")
    print()
    for p in sorted(presets, key=lambda x: (x["cat"], x["name"])):
        per = len(p["steps"]) // p["beats"] if p["beats"] else 0
        print("   %s  [%s]  %s" % (p["name"], p["cat"], p["origin"]))
        print("      %d beats, %d steps (%d per beat)  -  %s"
              % (p["beats"], len(p["steps"]), per, status_of(p)))
        print("      plays: %s" % ", ".join(beat_language(p)))
        url = first_url(p)
        if url:
            print("      source: %s" % url)
        print()


if __name__ == "__main__":
    main()
