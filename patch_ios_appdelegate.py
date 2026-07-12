#!/usr/bin/env python3
"""
patch_ios_appdelegate.py

Injects Intonare's AVAudioSession configuration into the AppDelegate.swift that
`npx cap add ios` generates.

WHY THIS EXISTS
---------------
When WKWebView calls getUserMedia, iOS switches the audio session to
playAndRecord. That category routes OUTPUT through the earpiece receiver rather
than the loudspeaker, because the OS assumes an app that records and plays at
the same time is a phone call. Every sound Intonare makes goes quiet the moment
the microphone is touched.

WebKit exposes no way to change this. There is no JS API, no AudioContext
property, nothing. It cannot be fixed in the web layer at any price.
AVAudioSession is the only lever, and it is native-only.

WHY IT IS A CI STEP AND NOT A COMMITTED FILE
--------------------------------------------
ios/ is regenerated on every build (see codemagic.yaml). A committed
AppDelegate.swift would be deleted by the next `cap add ios`. This mirrors what
go.bat [4b]-[4c2] does on Android, where MainActivity.java and
IntonareMicPlugin.java are restored from native_src/ after `cap sync` overwrites
them.

WHY IT APPENDS RATHER THAN ADDING A NEW FILE
--------------------------------------------
Xcode tracks source files in project.pbxproj. A new .swift file would have to be
registered there to compile, and editing pbxproj with a script is exactly the
kind of thing that breaks silently six months later. AppDelegate.swift is
already in the project, so appending to it needs no pbxproj surgery.

Run from the repo root, after `npx cap add ios` and before `npx cap sync ios`.
"""

import re
import sys
import os

APPDELEGATE = "ios/App/App/AppDelegate.swift"
AUDIO_SWIFT = "native_src/ios/IntonareAudioSession.swift"
MARKER = "IntonareAudioSession.configure()"


def fail(msg):
    print(f"FATAL: {msg}")
    sys.exit(1)


def main():
    if not os.path.isfile(APPDELEGATE):
        fail(f"{APPDELEGATE} not found. `cap add ios` may have changed its layout.")

    if not os.path.isfile(AUDIO_SWIFT):
        fail(f"{AUDIO_SWIFT} not found.")

    src = open(APPDELEGATE).read()

    print("--- AppDelegate.swift as generated ---")
    print(src)
    print("--------------------------------------")

    if MARKER in src:
        print("Already patched; nothing to do.")
        return

    # 1. AVFoundation import. The appended code needs it, and Capacitor's
    #    generated AppDelegate does not import it.
    if not re.search(r'^import AVFoundation\s*$', src, re.M):
        # Put it directly after the UIKit import, which is always present.
        src, n = re.subn(
            r'^(import UIKit\s*)$',
            r'\1\nimport AVFoundation',
            src,
            count=1,
            flags=re.M,
        )
        if n == 0:
            fail("could not find `import UIKit` to anchor the AVFoundation import")

    # 2. Call configure() at the top of didFinishLaunchingWithOptions. Capacitor's
    #    AppDelegate always has this method; anchoring on its opening brace is
    #    stable across Capacitor versions in a way that anchoring on the body is
    #    not.
    pattern = re.compile(
        r'(func\s+application\s*\(\s*_\s+application:\s*UIApplication\s*,\s*'
        r'didFinishLaunchingWithOptions[^{]*\{)',
        re.S,
    )

    m = pattern.search(src)
    if not m:
        fail(
            "could not find didFinishLaunchingWithOptions in AppDelegate.swift. "
            "Capacitor may have changed the generated template; the AppDelegate "
            "printed above shows what it actually wrote."
        )

    src = (
        src[: m.end()]
        + "\n        // Route audio to the loudspeaker rather than the earpiece.\n"
        + "        // See native_src/ios/IntonareAudioSession.swift for why.\n"
        + f"        {MARKER}\n"
        + src[m.end():]
    )

    # 3. Append the audio session code itself. It is a standalone enum, so it
    #    cannot collide with anything Capacitor generated.
    audio = open(AUDIO_SWIFT).read()

    # Strip its own import lines; they would be duplicates at file scope.
    audio = re.sub(r'^import\s+\w+\s*$', '', audio, flags=re.M)

    src = src.rstrip() + "\n\n" + audio.strip() + "\n"

    open(APPDELEGATE, 'w').write(src)

    print("--- AppDelegate.swift after patch ---")
    print(src)
    print("-------------------------------------")

    # 4. Verify. A silent no-op here would ship a quiet app with a green build.
    check = open(APPDELEGATE).read()
    if MARKER not in check:
        fail("configure() call was not injected")
    if 'import AVFoundation' not in check:
        fail("AVFoundation import was not added")
    if 'enum IntonareAudioSession' not in check:
        fail("IntonareAudioSession was not appended")

    print("OK: AppDelegate patched.")


if __name__ == "__main__":
    main()
