package com.lieutenantdan.intonare;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.media.audiofx.AcousticEchoCanceler;
import android.media.audiofx.NoiseSuppressor;
import android.media.audiofx.AutomaticGainControl;
import android.util.Base64;

/**
 * IntonareMic — native microphone capture + per-mode audio processing.
 *
 * PHASE 0 (done): plugin compiles, registers, round-trips JS <-> native (ping()).
 *
 * PHASE 1a (done): AudioRecord capture on a background thread, RMS pushed to JS
 *   as a continuous "micLevel" event. Proven on-device.
 *
 * PHASE 1b (this): per-mode audio processing via the platform AudioEffect APIs,
 *   gated on flags passed from JS to start():
 *     - aec : AcousticEchoCanceler  — cancels the app's own speaker output from
 *             the mic input. ON for reference-and-match surfaces (the mic must
 *             hear the player, not the app): tonal drone, interval sing-back,
 *             sing-the-note, piano reference-match, metronome (cancels click
 *             self-trigger). OFF for raw-signal surfaces: tuner, tools pitch
 *             readout, volume meter, vocal-range (sings freely, no reference).
 *     - ns  : NoiseSuppressor        — speech-tuned; eats sustained musical tones,
 *             so OFF by default everywhere. Exposed only so the metronome's
 *             transient onset detection can be A/B-tested with it later in a
 *             noisy room; do NOT enable for any pitch surface.
 *     - agc : AutomaticGainControl   — pumps levels, defeating the detector's RMS
 *             silence gate and the volume meter. Harmful on every surface; OFF
 *             everywhere. Exposed only for completeness / future measurement.
 *
 *   Each effect attaches to the AudioRecord's audio SESSION ID (valid only after
 *   the recorder is constructed) and is released BEFORE the recorder. A device
 *   may not support a given effect (isAvailable() == false); start() reports back
 *   what was ACTUALLY applied, so JS sees the truth, not just the request.
 *
 * NOT YET:
 *   1c — stream PCM buffers to the existing, proven JS YIN detector.
 *   1d — (only if on-device measurement shows latency/jank on weak phones) port
 *        the JS detectPitch to native, JS version as the test oracle.
 */
@CapacitorPlugin(name = "IntonareMic")
public class IntonareMicPlugin extends Plugin {

    // ── Capture config ───────────────────────────────────────────────────────
    // 44100 Hz mono 16-bit PCM: universally supported, matches the JS detector.
    // VOICE_COMMUNICATION is the source that COOPERATES with AcousticEchoCanceler
    // — AEC is designed around the voice-comms capture path. VOICE_RECOGNITION
    // (used in 1a) is the least-processed source but does NOT reliably pair with
    // platform AEC. Since AEC is now per-mode, we pick the source per request:
    //   aec ON  -> VOICE_COMMUNICATION (AEC works against the comms path)
    //   aec OFF -> VOICE_RECOGNITION   (least DSP colouring on the raw signal)
    private static final int SAMPLE_RATE = 44100;
    private static final int CHANNEL = AudioFormat.CHANNEL_IN_MONO;
    private static final int ENCODING = AudioFormat.ENCODING_PCM_16BIT;
    private static final int SOURCE_RAW = MediaRecorder.AudioSource.VOICE_RECOGNITION;
    private static final int SOURCE_AEC = MediaRecorder.AudioSource.VOICE_COMMUNICATION;

    private AudioRecord recorder;
    private Thread captureThread;
    private volatile boolean capturing = false;

    // Effects held so we can release them in stopCapture (before the recorder).
    private AcousticEchoCanceler aec;
    private NoiseSuppressor ns;
    private AutomaticGainControl agc;

    @PluginMethod
    public void ping(PluginCall call) {
        JSObject ret = new JSObject();
        ret.put("ok", true);
        ret.put("msg", "native alive");
        ret.put("echo", call.getString("from", "(none)"));
        call.resolve(ret);
    }

    @PluginMethod
    public void start(PluginCall call) {
        if (capturing) {
            JSObject ret = new JSObject();
            ret.put("started", true);
            ret.put("alreadyRunning", true);
            call.resolve(ret);
            return;
        }

        // Processing flags from JS. All default false (raw signal) so a caller
        // that passes nothing gets the safest, least-coloured capture.
        boolean wantAec = Boolean.TRUE.equals(call.getBoolean("aec", false));
        boolean wantNs  = Boolean.TRUE.equals(call.getBoolean("ns", false));
        boolean wantAgc = Boolean.TRUE.equals(call.getBoolean("agc", false));
        // When true, each captured frame is also emitted as base64 int16 PCM via
        // the "micFrame" event, so JS can run the existing detector on the NATIVE
        // audio (the real test of capture + AEC). Off by default so the cheap
        // level-meter path doesn't ship frames it doesn't need.
        boolean sendPcm = Boolean.TRUE.equals(call.getBoolean("sendPcm", false));

        int source = wantAec ? SOURCE_AEC : SOURCE_RAW;

        int minBuf = AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL, ENCODING);
        if (minBuf == AudioRecord.ERROR || minBuf == AudioRecord.ERROR_BAD_VALUE) {
            call.reject("AudioRecord.getMinBufferSize failed for this device config");
            return;
        }
        int frameSamples = 2048;
        int frameBytes = frameSamples * 2;
        int bufBytes = Math.max(minBuf, frameBytes * 2);

        try {
            recorder = new AudioRecord(source, SAMPLE_RATE, CHANNEL, ENCODING, bufBytes);
        } catch (Exception e) {
            recorder = null;
            call.reject("AudioRecord construction threw: " + e.getMessage());
            return;
        }
        if (recorder.getState() != AudioRecord.STATE_INITIALIZED) {
            try { recorder.release(); } catch (Exception ignored) {}
            recorder = null;
            call.reject("AudioRecord failed to initialize (mic permission? in-use by another app?)");
            return;
        }

        // ── Attach requested effects to this recorder's audio session ──
        // Each is best-effort: a device may not support it (isAvailable() false),
        // or creation may fail; we record what ACTUALLY applied and report it.
        int sessionId = recorder.getAudioSessionId();
        boolean aecApplied = false, nsApplied = false, agcApplied = false;
        // Diagnostics: distinguish "device reports no AEC" from "create/enable failed".
        boolean aecAvailable = AcousticEchoCanceler.isAvailable();
        String aecNote = "";

        if (wantAec && aecAvailable) {
            try {
                aec = AcousticEchoCanceler.create(sessionId);
                if (aec != null) { aec.setEnabled(true); aecApplied = aec.getEnabled(); aecNote = "created+enabled=" + aecApplied; }
                else { aecNote = "create() returned null"; }
            } catch (Exception e) { aec = null; aecNote = "exception: " + e.getMessage(); }
        } else if (wantAec) {
            aecNote = "isAvailable()=false on this device";
        }
        if (wantNs && NoiseSuppressor.isAvailable()) {
            try {
                ns = NoiseSuppressor.create(sessionId);
                if (ns != null) { ns.setEnabled(true); nsApplied = ns.getEnabled(); }
            } catch (Exception e) { ns = null; }
        }
        if (wantAgc && AutomaticGainControl.isAvailable()) {
            try {
                agc = AutomaticGainControl.create(sessionId);
                if (agc != null) { agc.setEnabled(true); agcApplied = agc.getEnabled(); }
            } catch (Exception e) { agc = null; }
        }

        capturing = true;
        try {
            recorder.startRecording();
        } catch (Exception e) {
            capturing = false;
            releaseEffects();
            try { recorder.release(); } catch (Exception ignored) {}
            recorder = null;
            call.reject("startRecording threw: " + e.getMessage());
            return;
        }

        final int readSamples = frameSamples;
        final boolean emitPcm = sendPcm;
        captureThread = new Thread(new Runnable() {
            @Override public void run() {
                short[] buf = new short[readSamples];
                byte[] bytes = emitPcm ? new byte[readSamples * 2] : null;
                while (capturing) {
                    int n = recorder.read(buf, 0, readSamples);
                    if (n <= 0) {
                        if (n < 0) break;
                        continue;
                    }
                    double sumSq = 0;
                    for (int i = 0; i < n; i++) {
                        double s = buf[i] / 32768.0;
                        sumSq += s * s;
                    }
                    double rms = Math.sqrt(sumSq / n);

                    JSObject ev = new JSObject();
                    ev.put("rms", rms);
                    ev.put("samples", n);
                    notifyListeners("micLevel", ev);

                    if (emitPcm) {
                        // Little-endian int16 -> bytes -> base64. The bridge can't
                        // carry a Float array cleanly; base64 int16 is compact and
                        // JS decodes it back to Float32 for the detector.
                        for (int i = 0; i < n; i++) {
                            short s = buf[i];
                            bytes[i * 2]     = (byte) (s & 0xff);
                            bytes[i * 2 + 1] = (byte) ((s >> 8) & 0xff);
                        }
                        String b64 = Base64.encodeToString(bytes, 0, n * 2, Base64.NO_WRAP);
                        JSObject fr = new JSObject();
                        fr.put("pcm", b64);
                        fr.put("samples", n);
                        fr.put("sampleRate", SAMPLE_RATE);
                        notifyListeners("micFrame", fr);
                    }
                }
            }
        }, "IntonareMicCapture");
        captureThread.start();

        JSObject ret = new JSObject();
        ret.put("started", true);
        ret.put("sampleRate", SAMPLE_RATE);
        ret.put("frameSamples", frameSamples);
        ret.put("source", wantAec ? "voice_communication" : "voice_recognition");
        ret.put("sendPcm", sendPcm);
        // requested vs. actually-applied, so JS can tell when a device silently
        // lacks an effect (e.g. AEC requested but unavailable on this hardware).
        ret.put("aecRequested", wantAec); ret.put("aecApplied", aecApplied);
        ret.put("aecAvailable", aecAvailable); ret.put("aecNote", aecNote);
        ret.put("nsRequested", wantNs);   ret.put("nsApplied", nsApplied);
        ret.put("agcRequested", wantAgc); ret.put("agcApplied", agcApplied);
        call.resolve(ret);
    }

    @PluginMethod
    public void stop(PluginCall call) {
        stopCapture();
        JSObject ret = new JSObject();
        ret.put("stopped", true);
        call.resolve(ret);
    }

    private void releaseEffects() {
        if (aec != null) { try { aec.release(); } catch (Exception ignored) {} aec = null; }
        if (ns  != null) { try { ns.release();  } catch (Exception ignored) {} ns  = null; }
        if (agc != null) { try { agc.release(); } catch (Exception ignored) {} agc = null; }
    }

    // Clean teardown: stop the read loop, join the thread, then release effects
    // BEFORE the recorder (effects are bound to the recorder's session), then
    // stop + release the recorder. Order matters at every step.
    private void stopCapture() {
        capturing = false;
        Thread t = captureThread;
        captureThread = null;
        if (t != null) {
            try { t.join(500); } catch (InterruptedException ignored) {}
        }
        releaseEffects();
        if (recorder != null) {
            try {
                if (recorder.getRecordingState() == AudioRecord.RECORDSTATE_RECORDING) {
                    recorder.stop();
                }
            } catch (Exception ignored) {}
            try { recorder.release(); } catch (Exception ignored) {}
            recorder = null;
        }
    }

    @Override
    protected void handleOnDestroy() {
        stopCapture();
        super.handleOnDestroy();
    }
}
