## Mixes together two WAV files. Figures out which one is the longest and goeds from there.

import librosa as lr
import soundfile as sf 
import numpy as np

# load
singing,sr = lr.load('output.wav', sr=44100)
backing,sr = lr.load('song.wav', sr=44100)

# pad
diff = len(backing) - len(singing)
if diff < 0: # singing is longer
    backing = np.pad(backing, pad_width=(np.abs(diff), 0), mode='constant')
if diff > 0: # backing is longer
    singing = np.pad(singing, pad_width=(np.abs(diff), 0), mode='constant')

# normalise
singing = singing / np.max(singing) * 0.5
backing = backing / np.max(backing) * 0.5

# mix and save
mix = singing + backing
sf.write(file='mix.wav', data=mix,samplerate=44100)
