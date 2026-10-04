import io,sys
p=sys.argv[1]
s=io.open(p,encoding='utf-8',newline='').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:60])
    s=s.replace(old,new)

# constants
rep('STORYBOARD   = "ios/App/App/Base.lproj/Main.storyboard"',
    'STORYBOARD   = "ios/App/App/Base.lproj/Main.storyboard"\nSCENEDELEGATE = "ios/App/App/SceneDelegate.swift"')

rep('print("[Intonare] IntonarePlugin and IntonareMicPlugin registered.")',
    'print("[Intonare] IntonarePlugin, IntonareMicPlugin and IntonareHapticsPlugin registered.")')

# quick actions block
i=s.index('QUICK_ACTIONS = """')
j=s.index('def fail(msg):')
new_qa='''QUICK_ACTIONS = """
// Handles a home screen long-press item. The item's userInfo carries an intonare://
// link (set in Info.plist by codemagic.yaml). Posting it as Capacitor's open-URL
// notification makes it arrive in JS as appUrlOpen, the same path a shared daily
// result takes. Capacitor 8.5 uses scenes, so a cold start must wait until the
// bridge has loaded its plugins (capacitorViewDidAppear) or the event is lost.
enum IntonareQuickAction {
    static func handle(_ item: UIApplicationShortcutItem, cold: Bool) {
        guard let link = item.userInfo?["url"] as? String,
              let url = URL(string: link) else { return }
        func post() {
            NotificationCenter.default.post(name: .capacitorOpenURL, object: [
                "url": url,
                "options": [String: Any]()
            ])
        }
        if cold {
            var token: NSObjectProtocol?
            token = NotificationCenter.default.addObserver(forName: .capacitorViewDidAppear, object: nil, queue: .main) { _ in
                if let t = token { NotificationCenter.default.removeObserver(t) }
                post()
            }
        } else {
            post()
        }
    }
}

// Older, non-scene template. Harmless when scenes are in use: iOS then calls the
// scene method instead.
extension AppDelegate {
    func application(_ application: UIApplication,
                     performActionFor shortcutItem: UIApplicationShortcutItem,
                     completionHandler: @escaping (Bool) -> Void) {
        IntonareQuickAction.handle(shortcutItem, cold: false)
        completionHandler(true)
    }
}
"""

SCENE_METHOD = """
    // Home screen long-press item chosen while the app is already running.
    func windowScene(_ windowScene: UIWindowScene,
                     performActionFor shortcutItem: UIApplicationShortcutItem,
                     completionHandler: @escaping (Bool) -> Void) {
        IntonareQuickAction.handle(shortcutItem, cold: false)
        completionHandler(true)
    }
"""

SCENE_COLD = """
        // Home screen long-press item that launched the app from cold.
        if let item = connectionOptions.shortcutItem {
            IntonareQuickAction.handle(item, cold: true)
        }
"""


'''
s=s[:i]+new_qa+s[j:]

# step 5: storyboard vs scene
rep('''    # 5. Point the storyboard at IntonareViewController.''',
'''    # 5a. Capacitor 8.5 template: SceneDelegate builds the view controller in code and
    #     the storyboard is unused. Swap the class there, add quick actions, done.
    if os.path.isfile(SCENEDELEGATE):
        sc = open(SCENEDELEGATE).read()
        if sc.count("CAPBridgeViewController()") != 1:
            print(sc)
            fail("SceneDelegate.swift does not contain exactly one CAPBridgeViewController(); "
                 "the file printed above shows what cap add ios wrote.")
        sc = sc.replace("CAPBridgeViewController()", "IntonareViewController()")
        anchor = "SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)"
        if sc.count(anchor) != 1:
            print(sc)
            fail("SceneDelegate.swift: willConnectTo anchor not found exactly once.")
        sc = sc.replace(anchor, anchor + "\\n" + SCENE_COLD.rstrip("\\n"))
        k = sc.rstrip().rfind("}")
        if k < 0:
            fail("SceneDelegate.swift: no closing brace.")
        sc = sc[:k].rstrip() + "\\n" + SCENE_METHOD.rstrip("\\n") + "\\n}\\n"
        open(SCENEDELEGATE, "w").write(sc)
        scene_ok = open(SCENEDELEGATE).read()
        for need in ("IntonareViewController()", "IntonareQuickAction.handle(item, cold: true)",
                     "performActionFor shortcutItem"):
            if need not in scene_ok:
                fail("SceneDelegate patch is missing: " + need)
        if "CAPBridgeViewController()" in scene_ok:
            fail("SceneDelegate still creates CAPBridgeViewController")
        verify_tail()
        print("--- SceneDelegate.swift after patch ---")
        print(scene_ok)
        print("OK: AppDelegate + plugins appended; SceneDelegate patched (scene template).")
        return

    # 5. Point the storyboard at IntonareViewController (older, storyboard template).''')
open(p,'w',encoding='utf-8',newline='').write(s)

s=io.open(p,encoding='utf-8',newline='').read()
vt='''def verify_tail():
    check = open(APPDELEGATE).read()
    for need in ("import AVFoundation", "import Capacitor", "import CoreHaptics",
                 "enum IntonareAudioSession", "class IntonarePlugin",
                 "class IntonareMicPlugin", "class IntonareHapticsPlugin",
                 "registerPluginInstance(IntonarePlugin())",
                 "registerPluginInstance(IntonareMicPlugin())",
                 "registerPluginInstance(IntonareHapticsPlugin())",
                 "enum IntonareQuickAction", MARKER, VC_MARKER):
        if need not in check:
            fail("AppDelegate.swift is missing: " + need)


def main():'''
assert s.count('def main():')==1
s=s.replace('def main():',vt)
io.open(p,'w',encoding='utf-8',newline='').write(s)
