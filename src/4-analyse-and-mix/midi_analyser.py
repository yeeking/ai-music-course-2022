### Prints some descriptive information about a MIDI file

import mido # might need to run pip3 install mido
import os 

# load the instrument file
ins_file = 'instrument_list.txt'
print('Loading instrument file', ins_file)
assert os.path.exists(ins_file), 'Tried to load ' + ins_file + ' but it does not exist'

with open(ins_file) as f:
    data = f.read()
data = data.split('\n')
ins_dict = {}
for ins in data:
    parts = ins.split(' ')
    # the program number is the first part of the line
    # note that we convert it to an int type
    ins_key = parts[0]
    # create the name by joining the rest of the 
    # parts together
    ins_name = " ".join(parts[1:])
    ins_dict[int(ins_key)] = ins_name
# program zero means no change
ins_dict[0] = "No change"



filename = 'song.mid'
assert os.path.exists(filename), 'Tried to load midi file '+filename+' but it does not exist'
print('analysing', filename)

mf = mido.MidiFile('song.mid')
for m in mf:
    if m.type == 'program_change':
        chan = m.channel
        ins = ins_dict[m.program]
        print("Chan", chan, ins)
