package com.lieutenantdan.intonare;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * IntonareMic — PHASE 0 (pipeline proof only).
 *
 * This does NOTHING but prove that a custom native plugin written by us can:
 *   1. compile inside the Android project,
 *   2. be auto-discovered + registered by Capacitor 8,
 *   3. survive a full `go.bat` run (cap sync + native-file restore),
 *   4. be called from the WebView JS and return a value.
 *
 * No audio code yet — that's Phase 1+. Keep this tiny until the round trip works
 * on a real device. Capacitor 8 auto-registers any @CapacitorPlugin-annotated
 * class in the app package, so MainActivity.java needs NO changes.
 */
@CapacitorPlugin(name = "IntonareMic")
public class IntonareMicPlugin extends Plugin {

    @PluginMethod
    public void ping(PluginCall call) {
        JSObject ret = new JSObject();
        ret.put("ok", true);
        ret.put("msg", "native alive");
        // Echo back anything JS sent, so we prove data crosses both directions.
        ret.put("echo", call.getString("from", "(none)"));
        call.resolve(ret);
    }
}
