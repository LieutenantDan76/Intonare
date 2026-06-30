package com.lieutenantdan.intonare;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;

/**
 * IntonareMic — native microphone capture.
 *
 * PHASE 0 (done): proved a custom plugin compiles, registers, and round-trips
 *   JS <-> native via ping().
 *
 * PHASE 1a (this): native AudioRecord capture on a background thread. Reads PCM,
 *   computes RMS level per buffer, and pushes it to JS as a continuous "micLevel"
 *   event. No pitch detection, no echo cancellation yet — this only proves the
 *   native mic opens, audio flows, the capture thread behaves, and teardown is
 *   clean. The push-event channel built here is the SAME channel that will later
 *   carry real audio buffers / detection results, so this plumbing is permanent,
 *   not scaffolding.
 *
 * Permission: RECORD_AUDIO is requested at launch in MainActivity, so start()
 *   assumes it's granted and fails gracefully (reject) if AudioRecord can't init.
 *
 * NOT YET (later phases):
 *   1b — AcousticEchoCanceler on the AudioRecord session (kills speaker bleed on
 *        reference-tone modes; the real payoff).
 *   1c — stream PCM buffers to the existing, proven JS YIN detector.
 *   1d — (only if on-device measurement shows latency/jank on weak phones) port
 *        the JS detectPitch to native, JS version as the test oracle.
 */
@CapacitorPlugin(name = "IntonareMic")
public class IntonareMicPlugin extends Plugin {

    // ── Capture config ───────────────────────────────────────────────────────
    // 44100 Hz mono 16-bit PCM: universally supported, and matches what the JS
    // detection path already assumes. VOICE_RECOGNITION is the least-processed
    // audio source that's reliable across devices (UNPROCESSED isn't guaranteed;
    // MIC/DEFAULT apply more device DSP that colours sustained musical tones).
    private static final int SAMPLE_RATE = 44100;
    private static final int CHANNEL = AudioFormat.CHANNEL_IN_MONO;
    private static final int ENCODING = AudioFormat.ENCODING_PCM_16BIT;
    private static final int AUDIO_SOURCE = MediaRecorder.AudioSource.VOICE_RECOGNITION;

    private AudioRecord recorder;
    private Thread captureThread;
    // volatile: the capture thread reads this every loop; stop() writes it from
    // the bridge thread. Without volatile the thread could cache a stale value
    // and never exit. This flag + join() is the clean-teardown contract.
    private volatile boolean capturing = false;

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
            // Already running — idempotent success rather than erroring.
            JSObject ret = new JSObject();
            ret.put("started", true);
            ret.put("alreadyRunning", true);
            call.resolve(ret);
            return;
        }

        int minBuf = AudioRecord.getMinBufferSize(SAMPLE_RATE, CHANNEL, ENCODING);
        if (minBuf == AudioRecord.ERROR || minBuf == AudioRecord.ERROR_BAD_VALUE) {
            call.reject("AudioRecord.getMinBufferSize failed for this device config");
            return;
        }
        // Read in ~2048-sample frames (close to the JS detector's working size),
        // but never below the device minimum. Bigger of the two wins.
        int frameSamples = 2048;
        int frameBytes = frameSamples * 2; // 16-bit = 2 bytes/sample
        int bufBytes = Math.max(minBuf, frameBytes * 2); // double-buffer headroom

        try {
            recorder = new AudioRecord(AUDIO_SOURCE, SAMPLE_RATE, CHANNEL, ENCODING, bufBytes);
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

        capturing = true;
        try {
            recorder.startRecording();
        } catch (Exception e) {
            capturing = false;
            try { recorder.release(); } catch (Exception ignored) {}
            recorder = null;
            call.reject("startRecording threw: " + e.getMessage());
            return;
        }

        final int readSamples = frameSamples;
        captureThread = new Thread(new Runnable() {
            @Override public void run() {
                short[] buf = new short[readSamples];
                while (capturing) {
                    int n = recorder.read(buf, 0, readSamples);
                    if (n <= 0) {
                        // ERROR_INVALID_OPERATION (-3) / ERROR_BAD_VALUE (-2) etc.
                        // Don't spin hot on a broken read; bail the loop.
                        if (n < 0) break;
                        continue;
                    }
                    // RMS over the frame, normalised to 0..1 (shorts are -32768..32767).
                    double sumSq = 0;
                    for (int i = 0; i < n; i++) {
                        double s = buf[i] / 32768.0;
                        sumSq += s * s;
                    }
                    double rms = Math.sqrt(sumSq / n);

                    JSObject ev = new JSObject();
                    ev.put("rms", rms);
                    ev.put("samples", n);
                    // Continuous push: same channel that will later carry real
                    // buffers / detection results.
                    notifyListeners("micLevel", ev);
                }
            }
        }, "IntonareMicCapture");
        captureThread.start();

        JSObject ret = new JSObject();
        ret.put("started", true);
        ret.put("sampleRate", SAMPLE_RATE);
        ret.put("frameSamples", frameSamples);
        call.resolve(ret);
    }

    @PluginMethod
    public void stop(PluginCall call) {
        stopCapture();
        JSObject ret = new JSObject();
        ret.put("stopped", true);
        call.resolve(ret);
    }

    // Clean teardown: flip the flag so the thread exits its loop, wait for it to
    // finish (so we never release the recorder out from under a live read()),
    // then stop + release. Order matters: join BEFORE release.
    private void stopCapture() {
        capturing = false;
        Thread t = captureThread;
        captureThread = null;
        if (t != null) {
            try { t.join(500); } catch (InterruptedException ignored) {}
        }
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

    // If the activity/plugin is torn down while capturing, don't leak the mic.
    @Override
    protected void handleOnDestroy() {
        stopCapture();
        super.handleOnDestroy();
    }
}
