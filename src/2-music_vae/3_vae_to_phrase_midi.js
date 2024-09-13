/**
 * This script generates a midi file
 * which contains a phrase of multi-instrument music
 * and writes it to phrase.mid
 */


const mvae = require('@magenta/music/node/music_vae');
const mm = require('@magenta/music/node/core')
const fs = require('fs')
const model = new mvae.MusicVAE('http://127.0.0.1:8081/models/multitrack_chords/');

const STEPS_PER_QTR = 32
const chord = 'C'

/** write the sent raw midi data, retrieved from 
 *  mm.sequenceProtoToMidi to filename
 */
function writeMidiToDisk(rawMidi, filename='music.mid')
{
  const res = fs.createWriteStream(filename).write(Buffer.from(rawMidi)); 
  console.log("writeMidiToDisk: " + filename + " : " + res);
}

// functions on MusicVAE
// decode(z: tf.Tensor2D, temperature?: number, controlArgs?: MusicVAEControlArgs, stepsPerQuarter?: number, qpm?: number): Promise<INoteSequence[]>;
// sample(numSamples: number, temperature?: number, controlArgs?: MusicVAEControlArgs, stepsPerQuarter?: number, qpm?: number): Promise<INoteSequence[]>;
// https://magenta.github.io/magenta-js/music/classes/_music_vae_model_.musicvae.html#sample

model
  .initialize()
  .then(() => {
 // 1 is the number of latent vectors (well, distributions) to sample
 // undefined is the temperature which is something like how crazy the output is
 // chordProgression is a single chord to condition with
    return model.sample(1, undefined, {chordProgression:[chord]}, STEPS_PER_QTR);
  }) 
  // call then on the promise received from model.sample
  .then((samples) => {
      // convert to midi
        const midi = mm.sequenceProtoToMidi(samples[0]);
        writeMidiToDisk(midi, "phrase.mid");
  });
