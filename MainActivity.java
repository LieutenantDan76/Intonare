package com.lieutenantdan.intonare;

import android.Manifest;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.BridgeWebChromeClient;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends BridgeActivity {

    private static final int MIC_PERMISSION_CODE = 1001;

    // Splash sound: stored in SharedPreferences so this native layer can read the
    // user's mute choice (the WebView's localStorage isn't visible to Java). The JS
    // toggle writes it via the "Android" bridge below.
    private static final String PREFS = "intonare_prefs";
    private static final String KEY_SPLASH_SOUND = "splashSound"; // "1" on (default), "0" muted
    private MediaPlayer splashPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Sticky immersive: hide status + nav bars. "Sticky" = a reveal swipe
        // shows them transiently, then Android auto-hides again on its own.
        hideSystemBars();

        // Expose a tiny JS bridge so the in-app settings toggle can persist the
        // splash-sound preference where this native code can read it next launch.
        getBridge().getWebView().addJavascriptInterface(new SplashSoundBridge(), "IntonareNative");

        // Play the launch sound (unless muted). Fires immediately on cold start,
        // no user gesture required — this is the whole point of doing it natively.
        playSplashSound();

        // Grant WebView mic requests
        getBridge().getWebView().setWebChromeClient(
            new BridgeWebChromeClient(getBridge()) {
                @Override
                public void onPermissionRequest(PermissionRequest request) {
                    runOnUiThread(() -> request.grant(request.getResources()));
                }
            }
        );

        // Request mic permission natively if not already granted
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                new String[]{ Manifest.permission.RECORD_AUDIO },
                MIC_PERMISSION_CODE);
        }
    }

    // ── Splash sound ────────────────────────────────────────────────────────
    private void playSplashSound() {
        try {
            SharedPreferences prefs = getSharedPreferences(PREFS, Context.MODE_PRIVATE);
            // Default ON: only skip if explicitly set to "0".
            if ("0".equals(prefs.getString(KEY_SPLASH_SOUND, "1"))) return;

            splashPlayer = MediaPlayer.create(this, R.raw.intonare_splash);
            if (splashPlayer == null) return; // resource missing — fail silent
            splashPlayer.setAudioAttributes(
                new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .build()
            );
            // Release as soon as it finishes so it never lingers.
            splashPlayer.setOnCompletionListener(mp -> releaseSplashPlayer());
            splashPlayer.start();
        } catch (Exception e) {
            // Never let a launch sound crash the app.
            releaseSplashPlayer();
        }
    }

    private void releaseSplashPlayer() {
        if (splashPlayer != null) {
            try { splashPlayer.release(); } catch (Exception ignored) {}
            splashPlayer = null;
        }
    }

    @Override
    public void onPause() {
        super.onPause();
        // Stop the tail if the user backgrounds the app mid-sound.
        releaseSplashPlayer();
    }

    @Override
    public void onDestroy() {
        releaseSplashPlayer();
        super.onDestroy();
    }

    // JS-callable: window.IntonareNative.setSplashSound(true/false)
    public class SplashSoundBridge {
        @JavascriptInterface
        public void setSplashSound(boolean on) {
            getSharedPreferences(PREFS, Context.MODE_PRIVATE)
                .edit()
                .putString(KEY_SPLASH_SOUND, on ? "1" : "0")
                .apply();
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        // Re-assert immersive whenever the window regains focus. This fires after
        // a bar reveal, a permission dialog, or returning from background — the
        // hook the WebView/JS layer can't see, which is why JS-only hiding fails.
        if (hasFocus) hideSystemBars();
    }

    private void hideSystemBars() {
        View decorView = getWindow().getDecorView();
        decorView.setSystemUiVisibility(
              View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            | View.SYSTEM_UI_FLAG_FULLSCREEN            // status bar
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION       // nav bar
            | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
        );
    }
}
