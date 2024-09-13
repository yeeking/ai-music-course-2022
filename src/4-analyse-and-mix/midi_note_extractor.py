## Extracts a molody from a file called song.mid

import mido 
import os 

num_to_note = { 0:'C', 1:'C#', 2:'D',3:'D#',
    4:'E', 5:'F', 6:'F#', 7:'G', 8:'G#',
    9:'A', 10:'A#',11:'B'
}

filename = 'song.mid'
print('analysing', filename)
assert os.path.exists(filename), 'Tried to load midi file '+filename+' but it does not exist'
mf = mido.MidiFile(filename)

notes = ""
for m in mf:
    if m.type == 'note_on' and m.channel == 2:
        note = num_to_note[m.note % 12] 
        notes = notes + note + ","
print(notes)
