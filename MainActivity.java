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
    private static final float SPLASH_VOLUME = 0.55f; // hard playback multiplier (0..1)
    private MediaPlayer splashPlayer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Sticky immersive: hide status + nav bars. "Sticky" = a reveal swipe
        // shows them transiently, then Android auto-hides again on its own.
        hideSystemBars();

        // Expose a tiny JS bridge: the in-app settings toggle persists the mute
        // preference, and the splash sequence calls playSplashSound() at the exact
        // instant the animation clock starts (so audio + visual stay locked even
        // though the WebView waits for viewport stabilisation before animating).
        getBridge().getWebView().addJavascriptInterface(new SplashSoundBridge(), "IntonareNative");

        // Prepare the launch sound now (decodes ahead) so the JS trigger can start it
        // with no prepare latency. Playback itself is fired by the bridge, not here.
        prepareSplashSound();

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
    // prepareSplashSound() decodes the clip ahead of time in onCreate. The actual
    // start is triggered from JS (window.IntonareNative.playSplashSound) at the exact
    // frame the splash animation begins, so the sound lines up with the visual.
    private boolean splashPlayed = false;

    private void prepareSplashSound() {
        try {
            SharedPreferences prefs = getSharedPreferences(PREFS, Context.MODE_PRIVATE);
            // Default ON: only skip if explicitly set to "0".
            if ("0".equals(prefs.getString(KEY_SPLASH_SOUND, "1"))) return;

            splashPlayer = MediaPlayer.create(this, R.raw.intonare_splash);
            if (splashPlayer == null) return; // resource missing — fail silent
            splashPlayer.setAudioAttributes(
                new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            );
            // Hard playback-level multiplier. Independent of the clip's internal gain
            // and not subject to sonification loudness compensation — this is the
            // reliable lever for how loud the launch sound actually is on device.
            try { splashPlayer.setVolume(SPLASH_VOLUME, SPLASH_VOLUME); } catch (Exception ignored) {}
            // Release as soon as it finishes so it never lingers.
            splashPlayer.setOnCompletionListener(mp -> releaseSplashPlayer());
            // Prime: seek to 0 so the eventual start() resumes instantly with no
            // first-frame buffering latency on top of the JS bridge hop.
            try { splashPlayer.seekTo(0); } catch (Exception ignored) {}
        } catch (Exception e) {
            releaseSplashPlayer();
        }
    }

    // JS-callable: window.IntonareNative.playSplashSound()
    private void startSplashSound() {
        if (splashPlayed) return;          // never fire twice (e.g. resume)
        if (splashPlayer == null) return;  // muted or unprepared
        splashPlayed = true;
        try {
            splashPlayer.start();
        } catch (Exception e) {
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
        // Only stop if the sound has actually started playing. On first launch the
        // permission dialog fires an onPause BEFORE the splash triggers playback —
        // releasing here would destroy the primed player and the sound would never
        // play. So we leave a not-yet-started player alone and let it fire on resume.
        if (splashPlayed) releaseSplashPlayer();
    }

    @Override
    public void onDestroy() {
        releaseSplashPlayer();
        super.onDestroy();
    }

    // JS-callable bridge: toggle persists the mute pref; playSplashSound() starts
    // the prepared clip at the exact moment the splash animation begins.
    public class SplashSoundBridge {
        @JavascriptInterface
        public void setSplashSound(boolean on) {
            getSharedPreferences(PREFS, Context.MODE_PRIVATE)
                .edit()
                .putString(KEY_SPLASH_SOUND, on ? "1" : "0")
                .apply();
        }

        @JavascriptInterface
        public void playSplashSound() {
            runOnUiThread(MainActivity.this::startSplashSound);
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
