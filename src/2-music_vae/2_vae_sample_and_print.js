// This script samples from the model
// and demonstrates the contents
// of the data structure that comes back

const mvae = require('@magenta/music/node/music_vae');
const model = new mvae.MusicVAE('http://127.0.0.1:8081/models/multitrack_chords/');
// functions on MusicVAE
//   decode(z: tf.Tensor2D, temperature?: number, controlArgs?: MusicVAEControlArgs, stepsPerQuarter?: number, qpm?: number): Promise<INoteSequence[]>;
//   sample(numSamples: number, temperature?: number, controlArgs?: MusicVAEControlArgs, stepsPerQuarter?: number, qpm?: number): Promise<INoteSequence[]>;
// https://magenta.github.io/magenta-js/music/classes/_music_vae_model_.musicvae.html#sample

model
  .initialize()
 // 1 is the number of latent vectors (well, distributions) to sample
 // undefined is the temperature which is something like how crazy the output is
 // chordProgression is a single chord to condition with
 .then(() => model.sample(1, undefined, {chordProgression:['c']}))
  .then((samples) => {
      for (let samp = 0; samp < samples.length; samp++)
      {
        for (let ins = 0; ins < 10; ins++)
        {
            console.log("Frame"+samp+"Notes for instrument: " + ins)
            samples[samp]['notes'].map((x) => {
                if (x['instrument'] == ins) 
                    console.log("p:"+x['pitch'] + " start: "+x['quantizedStartStep'])
                })
        }
    }
  });
