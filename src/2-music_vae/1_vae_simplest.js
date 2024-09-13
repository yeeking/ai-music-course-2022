// This zcript is a minimal example to 
// sample from a music vae model 
// and print out the results

const mvae = require('@magenta/music/node/music_vae');
const model = new mvae.MusicVAE('http://127.0.0.1:8081/models/multitrack_chords/');
model.initialize()
// sample one 16 bar segment, conditioned with a cmajor chord
.then(() => model.sample(1, undefined, {chordProgression:['c']}))
// print it out - should show all the notes
.then((sample) => {console.log(sample[0])});
