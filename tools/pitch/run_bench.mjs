/**
 * Pitch regression bench for Intonare.
 *
 *   node tools/pitch/gen_corpus.mjs
 *   node tools/pitch/run_bench.mjs
 *   node tools/pitch/run_bench.mjs --write-baseline
 *
 * Exit 1 if any clip fails its cents/dropout gates, or if app detector
 * knobs drifted from the offline port pins.
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { detectPitch, centsError } from './yin_fft.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const CORPUS = path.join(__dirname, 'corpus');
const BASELINE_PATH = path.join(__dirname, 'baselines', 'synth_baseline.json');
const writeBaseline = process.argv.includes('--write-baseline');

const FRAME = 4096;
const HOP = 2048;

/** Pins: offline port must match live Intonare.html detector knobs. */
const APP_PINS = [
  { label: 'YIN dip accept', re: /if \(yin\[tau\] < 0\.10\)/ },
  { label: 'YIN clarity reject', re: /yin\[tau\] >= 0\.18/ },
  { label: 'FFT size 8192', re: /const _FFT_SIZE = 8192/ },
  { label: 'native RMS floor', re: /_nativeMicActive \? 0\.00012/ },
  { label: 'web RMS floor', re: /: 0\.0004\)/ },
];

function readWavMono(filePath) {
  const buf = fs.readFileSync(filePath);
  if (buf.toString('ascii', 0, 4) !== 'RIFF') throw new Error('not RIFF: ' + filePath);
  const sr = buf.readUInt32LE(24);
  const bits = buf.readUInt16LE(34);
  const ch = buf.readUInt16LE(22);
  if (bits !== 16 || ch !== 1) throw new Error('need 16-bit mono: ' + filePath);
  let dataOff = 12;
  while (dataOff < buf.length - 8) {
    const id = buf.toString('ascii', dataOff, dataOff + 4);
    const sz = buf.readUInt32LE(dataOff + 4);
    if (id === 'data') {
      const start = dataOff + 8;
      const n = Math.floor(sz / 2);
      const samples = new Float32Array(n);
      for (let i = 0; i < n; i++) samples[i] = buf.readInt16LE(start + i * 2) / 32768;
      return { sr, samples };
    }
    dataOff += 8 + sz + (sz % 2);
  }
  throw new Error('no data chunk: ' + filePath);
}

function median(arr) {
  if (!arr.length) return null;
  const s = [...arr].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

function analyzeClip(clip, wav) {
  const { sr, samples } = wav;
  const floorMode = clip.floorMode || 'web';
  const hzList = [];
  let dropouts = 0;
  let frames = 0;
  for (let i = 0; i + FRAME <= samples.length; i += HOP) {
    const frame = samples.subarray(i, i + FRAME);
    const hz = detectPitch(frame, sr, floorMode);
    frames++;
    if (!(hz > 0)) {
      dropouts++;
      continue;
    }
    hzList.push(hz);
  }
  const dropoutPct = frames ? (100 * dropouts) / frames : 100;
  const medHz = median(hzList);
  let medCents = null;
  let maxAbsCents = null;
  if (clip.expectedHz != null && hzList.length) {
    const cents = hzList.map((h) => Math.abs(centsError(h, clip.expectedHz)));
    medCents = median(cents);
    maxAbsCents = Math.max(...cents);
  }
  return {
    id: clip.file,
    tag: clip.tag,
    note: clip.note,
    frames,
    hits: hzList.length,
    dropoutPct: +dropoutPct.toFixed(1),
    medianHz: medHz != null ? +medHz.toFixed(3) : null,
    medianAbsCents: medCents != null ? +medCents.toFixed(2) : null,
    maxAbsCents: maxAbsCents != null ? +maxAbsCents.toFixed(2) : null,
  };
}

function gateClip(clip, result) {
  const fails = [];
  if (clip.expectDropout) {
    if (result.dropoutPct < (clip.minDropoutPct ?? 95)) {
      fails.push(`expected silence dropout >= ${clip.minDropoutPct ?? 95}%, got ${result.dropoutPct}%`);
    }
    return fails;
  }
  if (result.medianAbsCents == null) {
    fails.push('no pitch detections');
    return fails;
  }
  if (clip.maxMedianCents != null && result.medianAbsCents > clip.maxMedianCents) {
    fails.push(`median |cents| ${result.medianAbsCents} > ${clip.maxMedianCents}`);
  }
  if (clip.maxDropoutPct != null && result.dropoutPct > clip.maxDropoutPct) {
    fails.push(`dropout ${result.dropoutPct}% > ${clip.maxDropoutPct}%`);
  }
  return fails;
}

function pinApp() {
  const htmlPath = path.join(ROOT, 'Intonare.html');
  if (!fs.existsSync(htmlPath)) {
    return [{ ok: false, label: 'Intonare.html missing' }];
  }
  const text = fs.readFileSync(htmlPath, 'utf8');
  return APP_PINS.map((p) => ({
    ok: p.re.test(text),
    label: p.label,
  }));
}

function main() {
  const manifestPath = path.join(CORPUS, 'manifest.json');
  if (!fs.existsSync(manifestPath)) {
    console.error('No corpus. Run: node tools/pitch/gen_corpus.mjs');
    process.exit(2);
  }
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

  console.log('── App detector pins ──');
  const pins = pinApp();
  let pinFail = 0;
  for (const p of pins) {
    console.log((p.ok ? '  OK  ' : ' FAIL ') + p.label);
    if (!p.ok) pinFail++;
  }

  console.log('\n── Corpus ──');
  const results = [];
  let clipFail = 0;
  for (const clip of manifest.clips) {
    const wavPath = path.join(CORPUS, clip.file);
    if (!fs.existsSync(wavPath)) {
      console.log(` FAIL ${clip.file}  (missing file)`);
      clipFail++;
      continue;
    }
    const wav = readWavMono(wavPath);
    const result = analyzeClip(clip, wav);
    const fails = gateClip(clip, result);
    results.push({ ...result, pass: fails.length === 0, fails });
    const status = fails.length ? 'FAIL' : ' OK ';
    const cents =
      result.medianAbsCents != null ? `${result.medianAbsCents}¢` : '—';
    console.log(
      ` ${status} ${clip.note.padEnd(8)} ${clip.tag.padEnd(7)} ` +
        `med=${cents.padStart(7)}  drop=${String(result.dropoutPct).padStart(5)}%  ` +
        `hz=${result.medianHz ?? '—'}`
    );
    if (fails.length) {
      for (const f of fails) console.log('       ' + f);
      clipFail++;
    }
  }

  const summary = {
    generatedAt: new Date().toISOString(),
    frame: FRAME,
    hop: HOP,
    clipCount: results.length,
    passCount: results.filter((r) => r.pass).length,
    pinFail,
    clipFail,
    results,
  };

  if (writeBaseline) {
    fs.mkdirSync(path.dirname(BASELINE_PATH), { recursive: true });
    fs.writeFileSync(BASELINE_PATH, JSON.stringify(summary, null, 2) + '\n');
    console.log('\nWrote baseline → tools/pitch/baselines/synth_baseline.json');
  } else if (fs.existsSync(BASELINE_PATH)) {
    const base = JSON.parse(fs.readFileSync(BASELINE_PATH, 'utf8'));
    console.log('\n── Vs baseline ──');
    let regFail = 0;
    for (const r of results) {
      const b = (base.results || []).find((x) => x.id === r.id);
      if (!b || b.medianAbsCents == null || r.medianAbsCents == null) continue;
      const delta = r.medianAbsCents - b.medianAbsCents;
      if (delta > 1.0) {
        console.log(` REG  ${r.id}  median cents worsened ${b.medianAbsCents} → ${r.medianAbsCents}`);
        regFail++;
      }
    }
    if (!regFail) console.log('  OK  no median-cents regression > 1¢ vs baseline');
    summary.regFail = regFail;
    clipFail += regFail;
  }

  console.log(
    `\nDone. pins_fail=${pinFail} clips_fail=${clipFail} ` +
      `pass=${summary.passCount}/${summary.clipCount}`
  );
  process.exit(pinFail || clipFail ? 1 : 0);
}

main();
