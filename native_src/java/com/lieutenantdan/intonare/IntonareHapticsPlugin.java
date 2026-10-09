package com.lieutenantdan.intonare;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.Build;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.os.VibratorManager;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * IntonareHaptics: custom haptic patterns on Android.
 *
 * WHY THIS EXISTS
 * Capacitor's Haptics plugin fires fixed presets. Every multi-tap feel in the app was
 * a chain of those presets with a JS timer between them, so spacing wobbled with
 * bridge and main-thread load. This takes the whole pattern in one call and hands it
 * to the vibrator as ONE effect, which the system times on its own.
 *
 * THE CONTRACT WITH JS (same on iOS, see IntonareHapticsPlugin.swift)
 *   isSupported()            -> { supported, amplitudeControl, primitives, sdk }
 *   play({ events: [...] })  -> { ok, mode }
 *   cancel()                 -> { ok: true }
 * Each event: { t: ms from now, i: intensity 0..1, s: sharpness 0..1, d: ms }.
 * d == 0 is a single tap. d > 0 is a sustained buzz of that length.
 *
 * HOW A PATTERN BECOMES AN EFFECT
 *   1. All taps and the phone supports the tick/click/thud primitives (API 30+):
 *      a composition. Primitives are crisp on phones with a proper linear motor
 *      (Pixel, Samsung flagships) and far better than a timed pulse.
 *   2. Otherwise, API 26+: a waveform with per-step amplitude. A tap becomes a
 *      10 to 24 ms pulse (sharper means shorter).
 *   3. API 24 and 25: an on/off pattern, no strength control.
 * Any exception while building or playing resolves ok:false, and JS drops back to
 * the old Capacitor taps. A cheap phone with a weak motor will still feel weak. No
 * software changes that.
 */
@CapacitorPlugin(name = "IntonareHaptics")
public class IntonareHapticsPlugin extends Plugin {

    private static final int MAX_EVENTS = 64;
    private static final long MAX_SPAN_MS = 4000;

    private Vibrator vibrator;

    private Vibrator vib() {
        if (vibrator != null) return vibrator;
        try {
            Context ctx = getContext();
            if (Build.VERSION.SDK_INT >= 31) {
                VibratorManager vm = (VibratorManager) ctx.getSystemService(Context.VIBRATOR_MANAGER_SERVICE);
                if (vm != null) vibrator = vm.getDefaultVibrator();
            } else {
                vibrator = (Vibrator) ctx.getSystemService(Context.VIBRATOR_SERVICE);
            }
        } catch (Exception ignored) {
            vibrator = null;
        }
        return vibrator;
    }

    /** One parsed event. */
    private static final class Ev {
        long t;       // ms from now
        float i;      // intensity 0..1
        float s;      // sharpness 0..1
        long d;       // ms, 0 = tap
    }

    private static float clamp01(double v) {
        if (Double.isNaN(v)) return 0f;
        return (float) Math.max(0.0, Math.min(1.0, v));
    }

    @SuppressLint("NewApi")
    private static boolean primitivesOk(Vibrator v) {
        if (Build.VERSION.SDK_INT < 30) return false;
        try {
            return v.areAllPrimitivesSupported(
                    VibrationEffect.Composition.PRIMITIVE_TICK,
                    VibrationEffect.Composition.PRIMITIVE_CLICK,
                    VibrationEffect.Composition.PRIMITIVE_THUD);
        } catch (Exception e) {
            return false;
        }
    }

    // When the last effect should be over (uptime ms), so a new one knows to cancel it.
    private volatile long lastEndAt = 0;

    @PluginMethod
    public void isSupported(PluginCall call) {
        Vibrator v = vib();
        JSObject ret = new JSObject();
        boolean has = false;
        boolean amp = false;
        try {
            has = v != null && v.hasVibrator();
            amp = has && Build.VERSION.SDK_INT >= 26 && v.hasAmplitudeControl();
        } catch (Exception ignored) {}
        ret.put("supported", has);
        ret.put("amplitudeControl", amp);
        ret.put("primitives", has && primitivesOk(v));
        ret.put("sdk", Build.VERSION.SDK_INT);
        call.resolve(ret);
    }

    @PluginMethod
    public void cancel(PluginCall call) {
        try {
            Vibrator v = vib();
            if (v != null) v.cancel();
        } catch (Exception ignored) {}
        JSObject ret = new JSObject();
        ret.put("ok", true);
        call.resolve(ret);
    }

    @SuppressLint("NewApi")
    @PluginMethod
    public void play(PluginCall call) {
        JSObject ret = new JSObject();
        try {
            Vibrator v = vib();
            if (v == null || !v.hasVibrator()) {
                ret.put("ok", false);
                ret.put("error", "unsupported");
                call.resolve(ret);
                return;
            }

            JSArray arr = call.getArray("events");
            if (arr == null || arr.length() == 0) {
                ret.put("ok", false);
                ret.put("error", "no events");
                call.resolve(ret);
                return;
            }

            // 0 soft, 1 normal, 2 strong. Strong swaps the thin tick for a click. On the
            // waveform route Normal and Strong also hold each short tap longer where the
            // pattern leaves room (see tapMs), since a motor barely spins up in 10 ms.
            final int level = call.getInt("strength", 1);
            // Test aid from Settings: "wave" or "prim" forces one route, anything else is auto.
            final String route = call.getString("route", "auto");
            List<Ev> evs = new ArrayList<>();
            int n = Math.min(arr.length(), MAX_EVENTS);
            boolean anySustained = false;
            for (int k = 0; k < n; k++) {
                JSONObject o = arr.getJSONObject(k);
                Ev e = new Ev();
                e.t = Math.max(0, Math.min(MAX_SPAN_MS, Math.round(o.optDouble("t", 0))));
                e.i = clamp01(o.optDouble("i", 0.5));
                e.s = clamp01(o.optDouble("s", 0.5));
                e.d = Math.max(0, Math.min(MAX_SPAN_MS, Math.round(o.optDouble("d", 0))));
                if (e.d > 0) anySustained = true;
                evs.add(e);
            }
            Collections.sort(evs, new Comparator<Ev>() {
                @Override public int compare(Ev a, Ev b) { return Long.compare(a.t, b.t); }
            });

            // A new effect replaces the old one, but a half played composition can leave a
            // bump when a waveform takes over (and the reverse). If the last effect is
            // still running, stop it cleanly first.
            long nowMs = android.os.SystemClock.uptimeMillis();
            if (nowMs < lastEndAt) {
                try { v.cancel(); } catch (Exception ignored) {}
            }
            long span = 0;
            for (Ev e : evs) span = Math.max(span, e.t + Math.max(e.d, 40));
            lastEndAt = nowMs + span + 60;

            String mode;
            // Primitives run ~20 to 40 ms each and blur into one buzz when events sit
            // closer than that, so a tight pattern takes the waveform path instead.
            long minGap = Long.MAX_VALUE;
            for (int k = 1; k < evs.size(); k++) {
                minGap = Math.min(minGap, evs.get(k).t - evs.get(k - 1).t);
            }
            boolean wantPrims = "prim".equals(route) || (!"wave".equals(route) && !anySustained && minGap >= 70);
            if (wantPrims && primitivesOk(v) && playComposition(v, evs, level)) {
                mode = "primitives";
            } else if (Build.VERSION.SDK_INT >= 26) {
                playWaveform(v, evs, level);
                mode = "waveform";
            } else {
                playLegacy(v, evs);
                mode = "legacy";
            }
            ret.put("ok", true);
            ret.put("mode", mode);
            call.resolve(ret);
        } catch (Exception e) {
            ret.put("ok", false);
            ret.put("error", String.valueOf(e));
            call.resolve(ret);
        }
    }

    // ── 1. Composition (API 30+) ────────────────────────────────────────────

    @SuppressLint("NewApi")
    private boolean playComposition(Vibrator v, List<Ev> evs, int level) {
        try {
            VibrationEffect.Composition comp = VibrationEffect.startComposition();
            long prevT = 0;
            boolean first = true;
            for (Ev e : evs) {
                int prim;
                if (e.s >= 0.66f && level < 2) prim = VibrationEffect.Composition.PRIMITIVE_TICK;
                else if (e.s >= 0.33f) prim = VibrationEffect.Composition.PRIMITIVE_CLICK;
                else prim = VibrationEffect.Composition.PRIMITIVE_THUD;
                // The delay is measured from the END of the previous primitive. They
                // run roughly 20 ms, so take that off the gap between start times.
                int delay = first ? (int) e.t : (int) Math.max(0, e.t - prevT - 20);
                // Primitive scale is the phone's own curve and runs well below the same number
                // on the waveform route (which also has a 48/255 floor). Lift it to match.
                float scale = Math.min(1f, 0.15f + e.i * 0.95f);
                comp.addPrimitive(prim, scale, delay);
                prevT = e.t;
                first = false;
            }
            v.vibrate(comp.compose());
            return true;
        } catch (Exception ex) {
            return false;
        }
    }

    // ── 2. Waveform with amplitude (API 26+) ────────────────────────────────

    @SuppressLint("NewApi")
    private void playWaveform(Vibrator v, List<Ev> evs, int level) {
        List<Long> timings = new ArrayList<>();
        List<Integer> amps = new ArrayList<>();
        long cursor = 0;
        for (int k = 0; k < evs.size(); k++) {
            Ev e = evs.get(k);
            long nextGap = (k + 1 < evs.size()) ? evs.get(k + 1).t - e.t : Long.MAX_VALUE;
            long dur = e.d > 0 ? e.d : tapMs(e.s, level, nextGap);
            long start = Math.max(e.t, cursor);
            long gap = start - cursor;
            // An off step only where there is a real gap. Back-to-back events (the
            // swells and fades JS builds from short steps) run straight into each
            // other with no zero-length steps between them.
            if (timings.isEmpty()) {
                if (start > 0) { timings.add(start); amps.add(0); }
            } else if (gap > 0) {
                timings.add(gap);
                amps.add(0);
            }
            timings.add(dur);
            amps.add(ampFor(e.i));
            cursor = start + dur;
        }
        long[] t = new long[timings.size()];
        int[] a = new int[amps.size()];
        for (int k = 0; k < t.length; k++) { t[k] = timings.get(k); a[k] = amps.get(k); }
        v.vibrate(VibrationEffect.createWaveform(t, a, -1));
    }

    // Quiet kept after a stretched tap, so two hits never run together.
    private static final long GUARD_MS = 14;

    /**
     * How long a short tap runs on the waveform route.
     *
     * A motor needs 10 to 20 ms to reach full strength, so a 10 ms tap never gets there, and
     * past full drive the only way to hit harder is to hold the pulse longer. Normal and
     * Strong stretch each tap, but only into the quiet AFTER it: the pulse ends at least
     * GUARD_MS before the next one starts. Where a pattern is tight (the detent's click then
     * thud) the tap stretches less or not at all, so the rhythm and the gaps a feel was
     * written with are never changed, and the dynamics (loud versus quiet hits) stay as
     * written. Soft is not stretched.
     */
    static long tapMs(float sharp, int level, long nextGapMs) {
        long base = Math.round(10 + (1.0f - sharp) * 14);
        long bonus = level >= 2 ? 14 : (level == 1 ? 4 : 0);
        long room = nextGapMs == Long.MAX_VALUE ? bonus : nextGapMs - base - GUARD_MS;
        return Math.min(40, base + Math.max(0, Math.min(bonus, room)));
    }

    // Motors do not move below a certain drive level, so a quiet step either does
    // nothing or just whines. Below ~8% the step is off. Above that it is raised to a
    // floor the motor can really show, so a soft tap is still felt.
    private static int ampFor(float i) {
        int a = Math.round(i * 255f);
        if (a < 20) return 0;
        return Math.max(48, Math.min(255, a));
    }

    // ── 3. On/off pattern (API 24, 25) ──────────────────────────────────────

    @SuppressWarnings("deprecation")
    private void playLegacy(Vibrator v, List<Ev> evs) {
        List<Long> timings = new ArrayList<>();
        long cursor = 0;
        for (Ev e : evs) {
            long dur = e.d > 0 ? e.d : Math.round(10 + (1.0f - e.s) * 14);
            long start = Math.max(e.t, cursor);
            timings.add(timings.isEmpty() ? start : start - cursor);
            timings.add(dur);
            cursor = start + dur;
        }
        long[] t = new long[timings.size()];
        for (int k = 0; k < t.length; k++) t[k] = timings.get(k);
        v.vibrate(t, -1);
    }
}
