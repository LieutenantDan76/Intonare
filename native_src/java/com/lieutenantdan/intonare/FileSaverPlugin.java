package com.lieutenantdan.intonare;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;

import androidx.activity.result.ActivityResult;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.ActivityCallback;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

/**
 * A real "Save as..." dialog on Android.
 *
 * WHY THIS EXISTS
 * ---------------
 * Android has no API for silently writing a non-media file somewhere the person
 * can find it. Capacitor's Filesystem plugin can only reach app-scoped storage,
 * which is invisible in a file manager AND deleted when the app is uninstalled —
 * the worst possible place for a backup, because it disappears at exactly the
 * moment it is needed. The share sheet works but only offers apps that accept the
 * file; it has no guaranteed "save to this phone" target.
 *
 * The Storage Access Framework is the sanctioned answer: ACTION_CREATE_DOCUMENT
 * shows the system file picker, the person chooses the folder and filename, and
 * the app writes through the returned URI. No storage permission is required,
 * because the person granted access by picking the location themselves. Nothing
 * in the Capacitor ecosystem wraps it, hence this file.
 *
 * INSTALL
 * -------
 * 1. Drop this file in android/app/src/main/java/com/lieutenantdan/intonare/
 * 2. Register it in MainActivity.java:
 *
 *        import com.getcapacitor.BridgeActivity;
 *        public class MainActivity extends BridgeActivity {
 *            @Override
 *            public void onCreate(android.os.Bundle savedInstanceState) {
 *                registerPlugin(FileSaverPlugin.class);
 *                super.onCreate(savedInstanceState);
 *            }
 *        }
 *
 *    registerPlugin MUST come before super.onCreate, or the bridge starts
 *    without it and the JS side sees no plugin.
 * 3. npx cap sync android
 *
 * If the package name ever changes, the `package` line at the top of this file
 * has to change with it.
 */
@CapacitorPlugin(name = "FileSaver")
public class FileSaverPlugin extends Plugin {

    /**
     * Opens the system save dialog.
     *
     * @param call  filename  suggested name, e.g. "intonare-backup-2026-08-18.json"
     *              data      the file contents as a string
     *              mimeType  optional, defaults to application/json
     *
     * Resolves { saved: true, uri: "content://..." } once written,
     * or { saved: false } if the person backed out of the picker.
     * Rejects only on a genuine write failure.
     */
    @PluginMethod
    public void save(PluginCall call) {
        String filename = call.getString("filename", "backup.json");
        String mimeType = call.getString("mimeType", "application/json");

        if (call.getString("data") == null) {
            call.reject("No data provided");
            return;
        }

        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(mimeType);
        intent.putExtra(Intent.EXTRA_TITLE, filename);

        // The call is saved so its data survives the trip through the picker;
        // startActivityForResult hands it back to the callback below.
        startActivityForResult(call, intent, "saveResult");
    }

    @ActivityCallback
    private void saveResult(PluginCall call, ActivityResult result) {
        if (call == null) return;

        // Backing out of the picker is a normal choice, not a failure. Resolving
        // with saved:false lets the JS side stay quiet instead of showing an
        // error for something the person did on purpose.
        if (result.getResultCode() != Activity.RESULT_OK || result.getData() == null) {
            JSObject cancelled = new JSObject();
            cancelled.put("saved", false);
            call.resolve(cancelled);
            return;
        }

        Uri uri = result.getData().getData();
        if (uri == null) {
            JSObject cancelled = new JSObject();
            cancelled.put("saved", false);
            call.resolve(cancelled);
            return;
        }

        try {
            String data = call.getString("data", "");
            OutputStream out = getContext().getContentResolver().openOutputStream(uri, "wt");
            if (out == null) {
                call.reject("Could not open the chosen file for writing");
                return;
            }
            try {
                out.write(data.getBytes(StandardCharsets.UTF_8));
                out.flush();
            } finally {
                out.close();
            }

            JSObject ok = new JSObject();
            ok.put("saved", true);
            ok.put("uri", uri.toString());
            call.resolve(ok);
        } catch (Exception e) {
            call.reject("Could not write the file: " + e.getMessage(), e);
        }
    }
}
