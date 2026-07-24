# Adapted performance MIDI

These are the twenty-one piano performance sequences used by Performance mode in
[Intonare](https://lieutenantdan76.github.io/Intonare/). They are adaptations of MIDI
recordings by **Bernd Krüger**, published at **[piano-midi.de](https://www.piano-midi.de)**
under the [Creative Commons Attribution-ShareAlike 3.0 Germany](https://creativecommons.org/licenses/by-sa/3.0/de/deed.en)
licence.

That licence is ShareAlike, so the adapted files are published here under the same terms.
This folder exists so anyone can take them, hear exactly what the app plays, and reuse them.

## Attribution

Original recordings: **Bernd Krüger**, piano-midi.de, licensed CC BY-SA 3.0 DE.
Adapted files in this folder: **© Bernd Krüger, adapted for Intonare**, licensed CC BY-SA
3.0 DE. The underlying compositions are all public domain; the licence covers Krüger's
performances, not the music itself.

## What was changed

Krüger's recordings were converted into the compact note-list format the app uses, and these
files are exported straight back out of that format. Everything audible is his: the note
choices, the timing, the dynamics, the pedalling. The changes are structural.

- **Tempo map flattened.** The originals carry expressive tempo in a tempo map. Here every file
  sits at a fixed 120 BPM, 480 ticks per quarter, with the rubato baked into the absolute note
  positions instead. Playback is identical; the bar lines just no longer line up with the score.
- **Tracks merged.** Left and right hand are collapsed into a single track on channel 1, so the
  hand split is gone.
- **Velocities round-tripped.** They are stored in the app as a 0 to 1 float and converted back
  to 0 to 127, so a velocity may land a step either side of the original.
- **Pedal reduced to on and off.** Sustain is CC64 at 0 or 127. Half-pedalling, if the original
  had any, is not preserved.
- **No trimming.** Every file is the complete performance.

Seven of these pieces also appear in the app with a Rhodes voice. Those use the same note data
with the sustain pedal removed, so they are not published separately.

## Files

21 files, 423 KB total.

| File | Work | Composer | Length | Notes |
|---|---|---|---|---|
| [`fuer_elise.mid`](fuer_elise.mid) | Für Elise (WoO 59) | Beethoven | 2:46 | 1,041 |
| [`moonlight.mid`](moonlight.mid) | Piano Sonata No. 14 "Moonlight", I. Adagio sostenuto | Beethoven | 6:07 | 1,144 |
| [`moonlight_2.mid`](moonlight_2.mid) | Piano Sonata No. 14 "Moonlight", II. Allegretto | Beethoven | 2:04 | 898 |
| [`moonlight_3.mid`](moonlight_3.mid) | Piano Sonata No. 14 "Moonlight", III. Presto agitato | Beethoven | 6:50 | 6,538 |
| [`waldstein_1.mid`](waldstein_1.mid) | Piano Sonata No. 21 "Waldstein", I. Allegro con brio | Beethoven | 10:18 | 8,576 |
| [`prelude_c.mid`](prelude_c.mid) | Prelude in C major, BWV 846 (WTC I) | J. S. Bach | 3:46 | 1,284 |
| [`clair_de_lune.mid`](clair_de_lune.mid) | Clair de lune (Suite bergamasque, L. 75) | Debussy | 4:09 | 1,491 |
| [`prelude_em.mid`](prelude_em.mid) | Prélude in E minor, Op. 28 No. 4 | Chopin | 1:42 | 604 |
| [`raindrop.mid`](raindrop.mid) | Prélude in D-flat major "Raindrop", Op. 28 No. 15 | Chopin | 4:32 | 1,518 |
| [`fantaisie_impromptu.mid`](fantaisie_impromptu.mid) | Fantaisie-Impromptu in C-sharp minor, Op. 66 | Chopin | 4:34 | 3,050 |
| [`barcarolle.mid`](barcarolle.mid) | The Seasons, June: Barcarolle, Op. 37a | Tchaikovsky | 3:55 | 1,502 |
| [`troika.mid`](troika.mid) | The Seasons, November: Troika, Op. 37a | Tchaikovsky | 2:57 | 1,852 |
| [`alla_turca.mid`](alla_turca.mid) | Piano Sonata No. 11, K. 331, III. Rondo alla turca | Mozart | 3:10 | 2,819 |
| [`sonata_facile.mid`](sonata_facile.mid) | Piano Sonata No. 16 "Sonata facile", K. 545, I | Mozart | 4:21 | 2,714 |
| [`to_spring.mid`](to_spring.mid) | To Spring, Op. 43 No. 6 | Grieg | 2:36 | 1,626 |
| [`butterfly.mid`](butterfly.mid) | Butterfly, Op. 43 No. 1 | Grieg | 1:38 | 937 |
| [`wedding_day.mid`](wedding_day.mid) | Wedding Day at Troldhaugen, Op. 65 No. 6 | Grieg | 5:30 | 3,842 |
| [`traumerei.mid`](traumerei.mid) | Kinderszenen, Träumerei, Op. 15 No. 7 | Schumann | 2:17 | 456 |
| [`prelude_csharp.mid`](prelude_csharp.mid) | Prélude in C-sharp minor, Op. 3 No. 2 | Rachmaninoff | 4:09 | 1,725 |
| [`prelude_op23.mid`](prelude_op23.mid) | Prélude in G minor, Op. 23 No. 5 | Rachmaninoff | 3:17 | 3,861 |
| [`liebestraum.mid`](liebestraum.mid) | Liebestraum No. 3, S. 541 | Liszt | 4:09 | 1,888 |

## Reuse

Take them. Under CC BY-SA 3.0 DE you need to credit Bernd Krüger and piano-midi.de, note that
the files were adapted, and licence anything you build from them under the same licence.
