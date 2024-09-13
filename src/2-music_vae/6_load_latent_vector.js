/**
 * This script generates a midi file
 * which contains a complete song fragment
 * by concatenating chord conditioned sequences together
 */

const mvae = require('@magenta/music/node/music_vae');
const mm = require('@magenta/music/node/core')
const tf = require('@tensorflow/tfjs')
const fs = require('fs')
const model = new mvae.MusicVAE('http://127.0.0.1:8081/models/multitrack_chords/');

const STEPS_PER_QTR = 32 // higher means faster music
// the chord sequence for the song
let chords = ["C", "G", "E", "D", "C"];
// this will eventually contain the parts of the song
let song = [];


/**
 * callback that receives each output from model
 */
function receivePhrase(phrase, chord)
{
  console.log("receive phrase " + chord);
  song.push(phrase);
  if (song.length == chords.length)
  {
    receiveSong(song);
  }  
}

function receiveSong(song)
{
  console.log("Receiving song. It has " +song.length+ " parts. Contcatenating.");
  // put the phrases together
  const songCat = concatenateSequences(song); 
  // chordSeqs = seqs;
  // concatSeqs = chordSeqs.map(s => concatenateSequences(s));
  const mergedSeq = mm.sequences.mergeInstruments(songCat);
  const progSeq = mm.sequences.unquantizeSequence(mergedSeq);
  progSeq.ticksPerQuarter = STEPS_PER_QTR;
  const midi = mm.sequenceProtoToMidi(progSeq);
  writeMidiToDisk(midi, 'song.mid');
}

/** this complete function is taken from the interpolation musicvae demo */ 
function concatenateSequences(seqs) {
  const seq = mm.sequences.clone(seqs[0]);
  let numSteps = seqs[0].totalQuantizedSteps;
  for (let i=1; i<seqs.length; i++) {
    const s = mm.sequences.clone(seqs[i]);
    s.notes.forEach(note => {
      note.quantizedStartStep += numSteps;
      note.quantizedEndStep += numSteps;
      seq.notes.push(note);
    });
    numSteps += s.totalQuantizedSteps;
  }
  seq.totalQuantizedSteps = numSteps;
  return seq;
}

/** write the sent raw midi data, retrieved from 
 *  mm.sequenceProtoToMidi to filename
 */
 function writeMidiToDisk(rawMidi, filename='music.mid')
 {
   const res = fs.createWriteStream(filename).write(Buffer.from(rawMidi)); 
   console.log("writeMidiToDisk: " + filename + " : " + res);
 }
 



model
  .initialize()
  // .then(() => {
  //   // generate a 256D sample to use as our latent vector
  //   const z = tf.randomNormal([1, 256]);
  //   return z.data()
  // })
  .then(() => {  
    fs.promises.readFile("sample.txt", 'ascii')
    .then((filedata) => {
      //console.log(filedata);
      let sample = [];
      filedata.split(',').map((item) => {sample.push(+(item) + (0.25 * Math.random()))})
 //    filedata.split(',').map((item) => {sample.push(+(item) )})
 
 sample.pop()
      console.log(sample[1])
    // convert the latent vector z into a form where we can 
    // use it to sample from the mvae model
    // note that we re-use the latent vector, but
    // with different chord conditioning 
    const z = tf.tensor2d(sample, [1, 256]);
    for (let i=0;i<chords.length;i++)
    {
      model.decode(z, undefined, {chordProgression:[chords[i]]}, STEPS_PER_QTR)
      .then((phrase) => 
      {
        console.log("Processing model output "+phrase.length);
        receivePhrase(phrase[0], chords[i]);
      }
      );
    }
    console.log("End of loop");
    })
  })

