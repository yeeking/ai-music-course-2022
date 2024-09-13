// this script generates a random sample 
// in latent space (256 vector) and 
// writes it to disk as sample.txt

const tf = require('@tensorflow/tfjs')
fs = require('fs');


const z = tf.randomNormal([1, 256]);

z.data()
.then((data) => {
  let out = "";
  data.map((val)=>{out += val + ","} )
  fs.writeFile("sample.txt", out, 'ascii', () => 
  {
    console.log("file written");
  });
})
