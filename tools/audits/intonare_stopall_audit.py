#!/usr/bin/env python3
"""
intonare_stopall_audit.py — guard against stopAllAudio() drifting again.

stopAllAudio() is a hand-maintained list of every "make it quiet" function in
the app. It has now drifted twice: once between exitTool/exitExercise keeping
two rival lists with different holes, and once where 43 stop-style functions
existed that the list had never heard of — including every drone, which rings
indefinitely by design and so leaked through every exit.

This audit diffs the functions DEFINED in the file against the ones the list
CALLS, and fails on anything new that isn't explicitly classified. When a new
stop function is added, it must be either wired into stopAllAudio or named in
EXEMPT below with a reason. Silence is no longer an option.

Usage: python3 intonare_stopall_audit.py [path/to/Intonare.html]
"""
import re, sys

# Functions that intentionally must NOT be in stopAllAudio, with the reason.
EXEMPT = {
    # Mic teardown — stopAllAudio fires on every module exit and on
    # backgrounding; killing the stream there would break tuner resume.
    'stopMic': 'mic stream teardown, would break tuner resume',
    '_nativeMicStop': 'native mic teardown, same reason',
    'vrStopDetect': 'mic detection loop, not output audio',
    # Per-note / per-voice stops — called by their module's own stop.
    '_organStopNote': 'per-note, covered by _organStopAll',
    '_riffStopVoice': 'per-voice, covered by riffStop',
    '_riffRhodesStopVoice': 'per-voice, covered by riffStop',
    'rhodesStopNote': 'per-note, covered by stopAllRhodesDrones',
    'stopRef': 'per-note, covered by stopAllRef',
    '_ivPeekStop': 'per-peek, covered by ivStop',
    '_bowedRenderDstop': 'render helper, not audio',
    # Animation / timer / UI stops — no audio.
    'rlpStopAnim': 'animation only',
    'rlpStopBoot': 'boot animation only',
    'rrSurvStopTimer': 'timer only',
    'rcStopTapTimers': 'timers only',
    'stopRamp': 'parameter ramp helper',
    '_stopInertia': 'scroll inertia, not audio',
    'progStopSyncSource': 'internal sync source, covered by progStop',
    'rtDistractStop': 'covered directly in list',
    'rtFinishStop': 'navigation, not audio',
    'rtNextStop': 'navigation, not audio',
    'rtRetryStop': 'navigation, not audio',
    'didiStop': 'no call sites; dormant',
    'stopAllAudio': 'the function itself',
    'thmnStopDemo': 'covered directly in list',
    'fluteTrillStopPulse': 'pulse helper, covered by fluteTrillStop',
    'stopAllSounds': 'covered directly in list',
    'sgStopCadence': 'covered via stopAllSounds',
    'diadleStopDrone': 'covered directly in list',
    'bowedScaleStop': 'covered directly in list',
    'tonaleStopCompare': 'covered directly in list',
    'tonaleStopWave': 'covered directly in list',
    'rcStopPlayback': 'covered directly in list',
    'rcdStop': 'covered directly in list',
    'fluteTrillAudioStop': 'covered directly in list',
    'tpStopAudio': 'covered directly in list',
    'mqAmbStop': 'covered directly in list',
    'hpStop': 'covered directly in list',
    'riffStop': 'covered directly in list',
    '_bowedStopAll': 'covered directly in list',
    '_organStopAll': 'covered directly in list',
    'stopAllRef': 'covered directly in list',
    'stopAllPianoDrones': 'covered directly in list',
    'stopAllRhodesDrones': 'covered directly in list',
}

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'Intonare.html'
    h = open(path, encoding='utf-8').read()

    m = re.search(r'function stopAllAudio\(\) \{(.*?)\n\}', h, re.DOTALL)
    if not m:
        print("  ✗ stopAllAudio() not found")
        return 1
    body = m.group(1)
    listed = set(re.findall(r"'([A-Za-z_][A-Za-z0-9_]*)'", body))
    listed |= set(re.findall(r"typeof (\w+) === 'function'", body))

    defined = set(re.findall(r'\nfunction (\w*[Ss]top[A-Za-z0-9_]*)\s*\(', h))
    unclassified = sorted(d for d in defined if d not in listed and d not in EXEMPT)

    print("=" * 70)
    print("  STOP-ALL AUDIT")
    print("=" * 70)
    print(f"  stop-style functions defined : {len(defined)}")
    print(f"  called by stopAllAudio       : {len(defined & listed)}")
    print(f"  explicitly exempt            : {len(defined & set(EXEMPT))}")
    print()

    if unclassified:
        print(f"  ✗ {len(unclassified)} stop function(s) neither wired in nor exempt:")
        for u in unclassified:
            print(f"      {u}")
        print()
        print("  Wire it into stopAllAudio(), or add it to EXEMPT with a reason.")
        print("=" * 70)
        return 1

    print("  ✓ Every stop function is either wired into stopAllAudio or")
    print("    explicitly exempt with a stated reason.")
    print("=" * 70)
    return 0

if __name__ == '__main__':
    sys.exit(main())
