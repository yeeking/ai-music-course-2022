## Works out how long a MIDI file is in seconds

import mido 
import os 

filename = 'song.mid'
print('analysing', filename)
assert os.path.exists(filename), 'Tried to load midi file '+filename+' but it does not exist'
mf = mido.MidiFile(filename)

elapsed = 0

for m in mf:
    elapsed = elapsed + m.time
print('total_elapsed_time', elapsed)
