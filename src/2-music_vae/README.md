# How to run musicvae js scripts

## Install the node.js

If you are running this in the Coursera lab environment, you can skip this step as we have installed node.js for you already. 

If you are running this on your own system, you will need node.js installed. Google onde.js installer and follow the instructions. 

## Install the node packages

If you are running this in the Coursera lab, you can skip this step as we installed the node packages for you.

If you are running on your own machine, you need to 

Open the terminal and enter the folder called 2-music_vae (it containins a file called package.json)

Run this command:

```
npm install 
```

This should install all the extra packages you need to run the javascripts in the folder. 

## Serve the models directory with a local web server on port 8080

You need to do this step for Coursera labs and a local install. 

The scripts have to download the music vae models from a web server.
They expect the following address to serve a folder containing a model:

http://127.0.0.1:8081/models/multitrack_chords/

Handily, one of the node packages installed is a mini web server called http-server. 

To run http-server: 

```
./node_modules/http-server/bin/http-server -p 8081 &
```

in the top level directory which contains the models folder. 

You should see some output like this:

```
Available on:
  http://127.0.0.1:8081
  http://10.100.8.168:8081
Hit CTRL-C to stop the server
```

## Get more models

You can download more models from here: 

https://github.com/magenta/magenta-js/blob/master/music/checkpoints/README.md#table

## Run a script

Now you are ready to run a script - type node then the name of the script you want to run:

```
node 1_vae_simplest.js
```

## Render a midi file to a wav

Some of the scripts output a midi file. E.g.:

```
node 3_vae_to_phrase_midi.js
```
This will output a file called phrase.mid. If you want to be able to hear the music, you need to render the midi file to audio.

You can do this with the fluidsynth program. Check the fluidsynth download page:

https://github.com/FluidSynth/fluidsynth/wiki/Download

You install fluidsynth as follows:

```
# mac
brew install fluidsynth # assuming you have homebrew installed
# linux/ apt
sudo apt install fluidsynth
# windows
choco install fluidsynth # assuming you have choclatey installed
```
Once you have fluidsynth, this command will render MIDI to WAV with fluidsynth:

```
fluidsynth -F <wav_file> <midi_file>
```

You can then play the wav file in an audio player like VLC. You can also load the MIDI files into your DAW if you have one. 
