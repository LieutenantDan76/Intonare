/**
 * Intonare FFT-YIN — offline port of Intonare.html detectPitch.
 * Keep thresholds in sync with the app; run_bench.mjs pins the live file.
 *
 * Floor modes match the app branches:
 *   native  → 0.00012
 *   agc     → 0.00015
 *   web     → 0.0004   (default for offline synth)
 */

const FFT_SIZE = 8192;
const fWr = new Float64Array(FFT_SIZE);
const fWi = new Float64Array(FFT_SIZE);
const fFr = new Float64Array(FFT_SIZE);
const fFi = new Float64Array(FFT_SIZE);
const fCr = new Float64Array(FFT_SIZE);
const fCi = new Float64Array(FFT_SIZE);
const fPs = new Float64Array(4097);
const fYin = new Float32Array(2048);

const FLOORS = { native: 0.00012, agc: 0.00015, web: 0.0004 };

function fftInPlace(re, im) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      let t = re[i]; re[i] = re[j]; re[j] = t;
      t = im[i]; im[i] = im[j]; im[j] = t;
    }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = -2 * Math.PI / len;
    const wr = Math.cos(ang), wi = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let cr = 1, ci = 0;
      const half = len >> 1;
      for (let k = 0; k < half; k++) {
        const ur = re[i + k], ui = im[i + k];
        const vr = re[i + k + half] * cr - im[i + k + half] * ci;
        const vi = re[i + k + half] * ci + im[i + k + half] * cr;
        re[i + k] = ur + vr; im[i + k] = ui + vi;
        re[i + k + half] = ur - vr; im[i + k + half] = ui - vi;
        const ncr = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = ncr;
      }
    }
  }
}

/**
 * @param {Float32Array|Float64Array|number[]} buf  length 4096 preferred
 * @param {number} sr
 * @param {'web'|'native'|'agc'|number} [floorMode='web']
 * @returns {number} Hz or -1
 */
export function detectPitch(buf, sr, floorMode = 'web') {
  const N = buf.length;
  const H = Math.floor(N / 2);
  let rms = 0;
  for (let i = 0; i < N; i++) rms += buf[i] * buf[i];
  rms = Math.sqrt(rms / N);

  const floor = typeof floorMode === 'number'
    ? floorMode
    : (FLOORS[floorMode] ?? FLOORS.web);
  if (rms < floor) return -1;

  if (N > 4096) {
    throw new Error('detectPitch offline port expects N <= 4096 (app ring size)');
  }

  fWr.fill(0); fWi.fill(0); fFr.fill(0); fFi.fill(0);
  for (let i = 0; i < H; i++) fWr[i] = buf[i];
  for (let i = 0; i < N; i++) fFr[i] = buf[i];
  fftInPlace(fWr, fWi);
  fftInPlace(fFr, fFi);
  for (let i = 0; i < FFT_SIZE; i++) {
    const a = fWr[i], b = -fWi[i], c = fFr[i], d = fFi[i];
    fCr[i] = a * c - b * d;
    fCi[i] = a * d + b * c;
  }
  for (let i = 0; i < FFT_SIZE; i++) fCi[i] = -fCi[i];
  fftInPlace(fCr, fCi);
  for (let i = 0; i < FFT_SIZE; i++) fCr[i] /= FFT_SIZE;

  fPs[0] = 0;
  for (let i = 0; i < N; i++) fPs[i + 1] = fPs[i] + buf[i] * buf[i];
  const term1 = fPs[H];

  const yin = fYin;
  for (let tau = 0; tau < H; tau++) {
    const v = term1 + (fPs[tau + H] - fPs[tau]) - 2 * fCr[tau];
    yin[tau] = v > 0 ? v : 0;
  }

  yin[0] = 1;
  let running = 0;
  for (let tau = 1; tau < H; tau++) {
    running += yin[tau];
    yin[tau] *= running > 0 ? tau / running : 1;
  }
  let tau = 2;
  while (tau < H) {
    if (yin[tau] < 0.10) {
      while (tau + 1 < H && yin[tau + 1] < yin[tau]) tau++;
      break;
    }
    tau++;
  }
  if (tau === H || yin[tau] >= 0.18) return -1;
  if (tau > 0 && tau < H - 1) {
    const s0 = yin[tau - 1], s1 = yin[tau], s2 = yin[tau + 1];
    const den = 2 * (2 * s1 - s2 - s0);
    if (Math.abs(den) > 1e-12) tau += (s2 - s0) / den;
  }
  return sr / tau;
}

export function centsError(hz, expectedHz) {
  if (!(hz > 0) || !(expectedHz > 0)) return null;
  return 1200 * Math.log2(hz / expectedHz);
}

export { FLOORS, FFT_SIZE };
