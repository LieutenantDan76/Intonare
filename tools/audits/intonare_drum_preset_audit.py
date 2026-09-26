#!/usr/bin/env python3
"""
intonare_drum_preset_audit.py

Structural audit of the DRUMKIT presets (PRESET_CATS).
Checks what a machine can prove: step counts against meter and subdivision,
track ids, value ranges, kit ids, BPM range, name twins, duplicates, and the
globalSub upscale interaction.

Musical accuracy (is this really a Purdie Shuffle?) is NOT checked here.
That is a listening and sourcing job.

Usage: python3 intonare_drum_preset_audit.py [path/to/Intonare.html]
"""
import json
import re
import subprocess
import sys
import tempfile
import os

DEFAULT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'Intonare.html')


VALID_KITS = {"standard", "brush", "electronic", "jazz", "latin"}
BPM_MIN, BPM_MAX = 40, 300
VALID_VALUES = {0, 1, 2, 3}   # 0 off, 1 ghost, 2 hit, 3 flam
VALID_SUBS = {1, 2, 3, 4, 6, 8}

META_KEYS = {"name", "nameIt", "ts", "dk_bpm", "kit", "swing",
             "globalSub", "trackSub", "barCount",
             # nudge: { track: { step: fraction } } per-step timing offsets
             # (loadPreset copies it into dk_nudges). Checked separately below.
             "nudge"}


def extract_block(src, marker, endmark):
    i = src.find(marker)
    if i < 0:
        return None
    j = src.find(endmark, i)
    if j < 0:
        return None
    return src[i:j + len(endmark)]


def loadpreset_still_upscales(src):
    """True if loadPreset() still calls _upscalePatterns() on preset load.

    That call is for the SUB button, not for loading. A preset writes its rows
    at its own globalSub, so upscaling on load multiplies every index and drops
    the tail.
    """
    i = src.find("function loadPreset(")
    if i < 0:
        return False
    j = src.find("\nfunction ", i + 10)
    body = src[i:j if j > 0 else len(src)]
    for line in body.splitlines():
        bare = line.split("//")[0]
        if "_upscalePatterns()" in bare:
            return True
    return False


def load(path):
    src = open(path, encoding="utf-8").read()
    tracks = extract_block(src, "const TRACK_GROUPS = [", "\n];")
    sigs = extract_block(src, "const TIME_SIGS = {", "\n};")
    cats = extract_block(src, "const PRESET_CATS = [", "\n];")
    if not (tracks and sigs and cats):
        print("FAIL: could not find TRACK_GROUPS / TIME_SIGS / PRESET_CATS")
        sys.exit(2)

    js = (tracks + "\n" + sigs + "\n" + cats + "\n"
          + "const TRACKS = TRACK_GROUPS.flatMap(g => g.tracks);\n"
          + "console.log(JSON.stringify({tracks:TRACKS.map(t=>t.id),"
            "sigs:TIME_SIGS, cats:PRESET_CATS}));\n")
    with tempfile.NamedTemporaryFile("w", suffix=".mjs", delete=False,
                                     encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    try:
        out = subprocess.run(["node", tmp], capture_output=True, text=True)
        if out.returncode != 0:
            print("FAIL: node could not evaluate the preset block")
            print(out.stderr[:2000])
            sys.exit(2)
        data = json.loads(out.stdout)
        data["upscales_on_load"] = loadpreset_still_upscales(src)
        # Every drumPreset a progression preset names has to resolve. Preset
        # names are the join key and nothing enforces it, so renaming one in
        # PRESET_CATS silently breaks whatever PROG_PRESETS pointed at it.
        data["prog_refs"] = sorted(set(
            m.group(1).replace("\\'", "'")
            for m in re.finditer(r"drumPreset:\s*'((?:[^'\\]|\\.)*)'", src)))
        return data
    finally:
        os.unlink(tmp)


def steps_per_bar(sig, sub):
    """Mirrors _trackSteps(): native sub uses ts.steps, otherwise beats * sub."""
    if sub == sig["sub"]:
        return sig["steps"]
    return sig["beats"] * sub


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    data = load(path)
    track_ids = set(data["tracks"])
    sigs = {int(k): v for k, v in data["sigs"].items()}

    errors, warnings, notes = [], [], []
    seen_names = {}
    total = 0
    it_missing = []

    for cat in data["cats"]:
        if cat.get("isCustom"):
            continue
        clabel = cat["label"]
        for p in cat["presets"]:
            total += 1
            name = p.get("name", "<unnamed>")
            tag = f"[{clabel}] {name}"

            if name in seen_names:
                errors.append(f"{tag}: duplicate name, also in {seen_names[name]}")
            seen_names[name] = clabel

            if not p.get("nameIt"):
                it_missing.append(tag)

            ts = p.get("ts")
            if ts not in sigs:
                errors.append(f"{tag}: ts {ts} has no TIME_SIGS entry")
                continue
            sig = sigs[ts]

            kit = p.get("kit")
            if kit not in VALID_KITS:
                errors.append(f"{tag}: kit '{kit}' is not a real kit id")

            bpm = p.get("dk_bpm")
            if not isinstance(bpm, int):
                errors.append(f"{tag}: dk_bpm missing or not a number")
            elif not (BPM_MIN <= bpm <= BPM_MAX):
                errors.append(f"{tag}: dk_bpm {bpm} is outside the "
                              f"{BPM_MIN}-{BPM_MAX} slider range")

            swing = p.get("swing", 0)
            if not (0 <= swing <= 100):
                errors.append(f"{tag}: swing {swing} is outside 0-100")

            gsub = p.get("globalSub", 4)
            if gsub not in VALID_SUBS:
                errors.append(f"{tag}: globalSub {gsub} is not a real "
                              f"subdivision value")

            bars = p.get("barCount", 1)
            if not isinstance(bars, int) or bars < 1:
                errors.append(f"{tag}: barCount {bars} is not valid")
                bars = 1

            tsub = p.get("trackSub", {})
            for tid, s in tsub.items():
                if tid not in track_ids:
                    errors.append(f"{tag}: trackSub names unknown track '{tid}'")
                if s not in VALID_SUBS:
                    errors.append(f"{tag}: trackSub['{tid}'] = {s} is not a "
                                  f"real subdivision value")
                if tid not in p:
                    warnings.append(f"{tag}: trackSub['{tid}'] set but the "
                                    f"track has no pattern")

            # Swing on a compound meter at native resolution reaches the
            # scheduler (isCompoundNative), but it stretches EVEN step indices
            # and shrinks odd ones. In a meter grouped in threes that alternates
            # across the groups instead of inside them, so the pulse limps.
            if swing and gsub == 1 and sig["sub"] == 3:
                warnings.append(
                    f"{tag}: swing {swing}% on a compound native grid. The "
                    f"scheduler applies it, but it lengthens even steps and "
                    f"shortens odd ones, so whole beats alternate long and "
                    f"short. {sig['label']} is already compound; the shuffle is "
                    f"in the meter")
            elif swing and gsub != 4:
                warnings.append(f"{tag}: swing {swing}% is set but globalSub "
                                f"is {gsub}; swing is only eligible on a 16th "
                                f"grid or a compound native grid, so this value "
                                f"never applies")

            # the upscale trap
            if gsub > 4 and data["upscales_on_load"]:
                for tid in p:
                    if tid in META_KEYS:
                        continue
                    if tid in tsub:
                        continue
                    errors.append(
                        f"{tag}: globalSub {gsub} makes loadPreset call "
                        f"_upscalePatterns on '{tid}', which multiplies every "
                        f"step index by {gsub // 4}; the written data is "
                        f"stretched and the tail is dropped")
                    break

            # nudge: every track must exist, every step must be on the grid,
            # every offset must be a fraction of a step (0 < x < 1).
            nud = p.get("nudge", {})
            if nud and not isinstance(nud, dict):
                errors.append(f"{tag}: nudge is not an object")
                nud = {}
            for tid, steps in nud.items():
                if tid not in track_ids:
                    errors.append(f"{tag}: nudge names unknown track '{tid}'")
                    continue
                if not isinstance(steps, dict):
                    errors.append(f"{tag}: nudge['{tid}'] is not an object")
                    continue
                arr = p.get(tid)
                for st, off in steps.items():
                    try:
                        si, fv = int(st), float(off)
                    except (TypeError, ValueError):
                        errors.append(f"{tag}: nudge['{tid}'][{st}] is not numeric")
                        continue
                    if not (0 < fv < 1):
                        errors.append(f"{tag}: nudge['{tid}'][{si}] = {fv} is not a fraction of a step")
                    if isinstance(arr, list) and not (0 <= si < len(arr)):
                        errors.append(f"{tag}: nudge['{tid}'][{si}] is off the end of the pattern")
                    elif isinstance(arr, list) and not arr[si]:
                        warnings.append(f"{tag}: nudge['{tid}'][{si}] moves a step that has no hit")

            # per-track pattern lengths
            voices = 0
            for tid, arr in p.items():
                if tid in META_KEYS:
                    continue
                if tid not in track_ids:
                    errors.append(f"{tag}: unknown track '{tid}'")
                    continue
                if not isinstance(arr, list):
                    errors.append(f"{tag}: '{tid}' is not an array")
                    continue
                voices += 1
                sub = tsub.get(tid, gsub)
                want = steps_per_bar(sig, sub) * bars
                if len(arr) != want:
                    errors.append(
                        f"{tag}: '{tid}' has {len(arr)} steps, meter "
                        f"{sig['label']} at sub {sub} over {bars} bar(s) "
                        f"needs {want}")
                bad = sorted({v for v in arr if v not in VALID_VALUES})
                if bad:
                    errors.append(f"{tag}: '{tid}' has values {bad}; only "
                                  f"0/1/2/3 are valid")
                if not any(arr):
                    warnings.append(f"{tag}: '{tid}' is an empty row")

            # --- 3+2+3 miscount signature -------------------------------
            # A tresillo is 3+3+2, so a half-bar figure opens 0, 3, 6. Several
            # rows in this file opened 0, 3, 5 instead, and the same wrong array
            # had been copied into four presets. Catch the shape, not the array.
            for tid, arr in p.items():
                if tid in META_KEYS or not isinstance(arr, list):
                    continue
                if tsub.get(tid, gsub) != 4 or sig["label"] != "4/4":
                    continue
                on = [i for i, v in enumerate(arr[:16]) if v > 0]
                if on[:3] == [0, 3, 5]:
                    errors.append(
                        f"{tag}: '{tid}' opens 0, 3, 5. That is 3+2+3; a "
                        f"tresillo is 3+3+2 and opens 0, 3, 6. This exact "
                        f"miscount produced every broken clave in this file")

            # --- triplet grid against 16th grid --------------------------
            # If a preset puts any track on triplets, every other track has to
            # land on triplet positions too, because each track runs its own
            # clock. A 16th-grid hit only coincides with the triplet grid when
            # its index divides by 4; anywhere else is a 4-against-3 polyrhythm.
            # This is what made the Purdie Shuffle not a shuffle.
            trip = [t for t, v in tsub.items() if v in (3, 6)]
            if trip:
                for tid, arr in p.items():
                    if tid in META_KEYS or not isinstance(arr, list):
                        continue
                    sub = tsub.get(tid, gsub)
                    if sub in (3, 6) or sub == 0:
                        continue
                    per = steps_per_bar(sig, sub)
                    off = [i % per for i, v in enumerate(arr) if v > 0
                           and (i % per) * 3 % sub != 0]
                    if off:
                        warnings.append(
                            f"{tag}: '{tid}' is on a sub-{sub} grid while "
                            f"{trip} run triplets, and its hits at "
                            f"{sorted(set(off))[:6]} fall between triplet "
                            f"positions. Each track has its own clock, so that "
                            f"sounds as 4 against 3, not as swing")

            if voices == 0:
                errors.append(f"{tag}: no pattern rows at all")
            if voices == 1:
                notes.append(f"{tag}: single voice only")

    for ref in data.get("prog_refs", []):
        if ref not in seen_names:
            errors.append(f"PROG_PRESETS names drumPreset '{ref}', which no "
                          f"preset in PRESET_CATS provides")

    print("=" * 62)
    print(f"DRUM PRESET STRUCTURAL AUDIT — {total} presets, "
          f"{len(data.get('prog_refs', []))} progression links")
    print("=" * 62)
    for label, items in (("ERROR", errors), ("WARN", warnings),
                         ("NOTE", notes)):
        if items:
            print(f"\n{label} ({len(items)})")
            for s in items:
                print(f"  {label[0]}: {s}")
    if it_missing:
        print(f"\nMISSING nameIt ({len(it_missing)})")
        for s in it_missing:
            print(f"  -: {s}")
    print()
    if errors:
        print(f"RESULT: FAIL — {len(errors)} error(s), "
              f"{len(warnings)} warning(s)")
        return 1
    print(f"RESULT: PASS — 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
