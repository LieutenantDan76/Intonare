/**
 * Generate synthetic mono WAVs for the pitch regression corpus.
 * Run from repo root:  node tools/pitch/gen_corpus.mjs
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, 'corpus', 'synth');
const SR = 44100;
const DUR = 1.0; // seconds

function midiToHz(m) {
  return 440 * Math.pow(2, (m - 69) / 12);
}

function writeWav(filePath, samples, sampleRate) {
  const n = samples.length;
  const dataSize = n * 2;
  const buf = Buffer.alloc(44 + dataSize);
  buf.write('RIFF', 0);
  buf.writeUInt32LE(36 + dataSize, 4);
  buf.write('WAVE', 8);
  buf.write('fmt ', 12);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20); // PCM
  buf.writeUInt16LE(1, 22); // mono
  buf.writeUInt32LE(sampleRate, 24);
  buf.writeUInt32LE(sampleRate * 2, 28);
  buf.writeUInt16LE(2, 32);
  buf.writeUInt16LE(16, 34);
  buf.write('data', 36);
  buf.writeUInt32LE(dataSize, 40);
  for (let i = 0; i < n; i++) {
    let s = Math.max(-1, Math.min(1, samples[i]));
    buf.writeInt16LE((s * 32767) | 0, 44 + i * 2);
  }
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, buf);
}

function makeTone({ hz, amp = 0.25, harmonics = [1], noise = 0, cents = 0 }) {
  const f0 = hz * Math.pow(2, cents / 1200);
  const n = Math.floor(SR * DUR);
  const out = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    let s = 0;
    let wsum = 0;
    for (let h = 0; h < harmonics.length; h++) {
      const w = harmonics[h];
      s += w * Math.sin(2 * Math.PI * f0 * (h + 1) * t);
      wsum += w;
    }
    s = (s / wsum) * amp;
    if (noise > 0) s += (Math.random() * 2 - 1) * noise;
    out[i] = s;
  }
  return out;
}

const NOTES = [
  { id: 'E2', hz: midiToHz(40) },
  { id: 'A2', hz: midiToHz(45) },
  { id: 'E3', hz: midiToHz(52) },
  { id: 'A3', hz: midiToHz(57) },
  { id: 'E4', hz: midiToHz(64) },
  { id: 'A4', hz: 440 },
  { id: 'C5', hz: midiToHz(72) },
];

const clips = [];

for (const note of NOTES) {
  const pure = `pure_${note.id}.wav`;
  writeWav(path.join(OUT, pure), makeTone({ hz: note.hz, amp: 0.3, harmonics: [1] }), SR);
  clips.push({
    file: `synth/${pure}`,
    expectedHz: note.hz,
    tag: 'pure',
    note: note.id,
    maxMedianCents: 2,
    maxDropoutPct: 5,
  });

  const rich = `rich_${note.id}.wav`;
  writeWav(
    path.join(OUT, rich),
    makeTone({ hz: note.hz, amp: 0.28, harmonics: [1, 0.55, 0.35, 0.2, 0.12] }),
    SR
  );
  clips.push({
    file: `synth/${rich}`,
    expectedHz: note.hz,
    tag: 'rich',
    note: note.id,
    maxMedianCents: 3,
    maxDropoutPct: 8,
  });
}

// Quiet A4 — near web floor but still audible to detector
{
  const f = 'quiet_A4.wav';
  writeWav(path.join(OUT, f), makeTone({ hz: 440, amp: 0.0025, harmonics: [1] }), SR);
  clips.push({
    file: `synth/${f}`,
    expectedHz: 440,
    tag: 'quiet',
    note: 'A4',
    floorMode: 'native', // web floor would drop this; native is the stress case
    maxMedianCents: 5,
    maxDropoutPct: 40,
  });
}

// Noisy A4
{
  const f = 'noisy_A4.wav';
  writeWav(
    path.join(OUT, f),
    makeTone({ hz: 440, amp: 0.25, harmonics: [1, 0.4, 0.2], noise: 0.04 }),
    SR
  );
  clips.push({
    file: `synth/${f}`,
    expectedHz: 440,
    tag: 'noisy',
    note: 'A4',
    maxMedianCents: 8,
    maxDropoutPct: 25,
  });
}

// Detuned targets (detector should report the actual pitch, not snap to A4)
{
  const sharp = 'sharp_A4_p12c.wav';
  writeWav(path.join(OUT, sharp), makeTone({ hz: 440, amp: 0.3, cents: 12 }), SR);
  clips.push({
    file: `synth/${sharp}`,
    expectedHz: 440 * Math.pow(2, 12 / 1200),
    tag: 'detune',
    note: 'A4+12c',
    maxMedianCents: 2,
    maxDropoutPct: 5,
  });
  const flat = 'flat_A4_m15c.wav';
  writeWav(path.join(OUT, flat), makeTone({ hz: 440, amp: 0.3, cents: -15 }), SR);
  clips.push({
    file: `synth/${flat}`,
    expectedHz: 440 * Math.pow(2, -15 / 1200),
    tag: 'detune',
    note: 'A4-15c',
    maxMedianCents: 2,
    maxDropoutPct: 5,
  });
}

// Silence — must drop out
{
  const f = 'silence.wav';
  writeWav(path.join(OUT, f), new Float32Array(Math.floor(SR * DUR)), SR);
  clips.push({
    file: `synth/${f}`,
    expectedHz: null,
    tag: 'silence',
    note: '—',
    expectDropout: true,
    minDropoutPct: 95,
  });
}

const manifest = {
  version: 1,
  sampleRate: SR,
  frameSize: 4096,
  hop: 2048,
  description:
    'Synthetic pitch corpus for Intonare FFT-YIN. Replace/add real phone recordings under corpus/live/ later.',
  clips,
};

fs.writeFileSync(
  path.join(__dirname, 'corpus', 'manifest.json'),
  JSON.stringify(manifest, null, 2) + '\n'
);

console.log(`Wrote ${clips.length} clips → ${OUT}`);
console.log('Manifest → tools/pitch/corpus/manifest.json');
