
import argparse
import os
import yaml
import torch
import numpy as np
import re
from string import punctuation

import sys
sys.path.insert(1, './diffsinger')


from utils.model import get_model_step, get_vocoder
from utils.tools import to_device, synth_samples

from g2p_en import G2p
from text import text_to_sequence

# try GPU and fallback on CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# note to pitch control map
# for the LJSpeech model
note_to_pitch = {
'A':0.875,
'A#':1,
'B':1.125, 
'C':1.25, 
'C#':1.375,  
'D':1.5, 
'D#':1.625,
'E':1.9, 
'F':2.1,
'F#':0.5, 
'G':0.625, 
'G#':0.75}


def read_lexicon(lex_path):
    lexicon = {}
    with open(lex_path) as f:
        for line in f:
            temp = re.split(r"\s+", line.strip("\n"))
            word = temp[0]
            phones = temp[1:]
            if word.lower() not in lexicon:
                lexicon[word.lower()] = phones
    return lexicon


def preprocess_english(text, preprocess_config):
    text = text.rstrip(punctuation)
    lexicon = read_lexicon(preprocess_config["path"]["lexicon_path"])

    g2p = G2p()
    phones = []
    words = re.split(r"([,;.\-\?\!\s+])", text)
    for w in words:
        if w.lower() in lexicon:
            phones += lexicon[w.lower()]
        else:
            phones += list(filter(lambda p: p != " ", g2p(w)))
    phones = "{" + "}{".join(phones) + "}"
    phones = re.sub(r"\{[^\w\s]?\}", "{sp}", phones)
    phones = phones.replace("}{", " ")

    print("Raw Text Sequence: {}".format(text))
    print("Phoneme Sequence: {}".format(phones))
    sequence = np.array(
        text_to_sequence(
            phones, preprocess_config["preprocessing"]["text"]["text_cleaners"]
        )
    )

    return np.array(sequence), phones

def load_models():
    # assert the model is where it should be
    preproc_path = "config/LJSpeech/preprocess.yaml"
    model_path = "config/LJSpeech/model.yaml"
    train_path = "config/LJSpeech/train.yaml"

    assert os.path.exists(preproc_path), "model preproc not found" + preproc_path
    assert os.path.exists(model_path), "model not found " + model_path
    assert os.path.exists(train_path), "model train not found" + train_path

     # Read Config
    preprocess_config = yaml.load(open(preproc_path, "r"), Loader=yaml.FullLoader)
    model_config = yaml.load(open(model_path, "r"), Loader=yaml.FullLoader)
    train_config = yaml.load(open(train_path, "r"), Loader=yaml.FullLoader)
    configs = (preprocess_config, model_config, train_config)


    # Get model
    model = get_model_step(160000, configs, device, train=False)
    # Load vocoder
    vocoder = get_vocoder(model_config, device)
    return configs, model, vocoder

def prepare_batch_data(lyrics, preprocess_config):
    #ids = raw_texts = [args.lyrics[:100]]
    ids = raw_texts = [lyrics]
    speakers = np.array([0]) # zero is the default speaker id
    texts, phones = preprocess_english(lyrics, preprocess_config)
    print("phones: ", phones)
    print("sequence: ", texts)
    texts = np.array([texts])
    text_lens = np.array([len(texts[0])])
    # prepare data for the call to 'to_model'
    run_data =(ids, raw_texts, speakers, texts, text_lens, max(text_lens))
    return run_data, phones

def synthesize(model, step, configs, vocoder, run_data, 
        filename, 
        global_pitch=1, 
        energy=1, 
        duration=1, 
        notes=['c']
        ):
    preprocess_config, model_config, train_config = configs

    run_data = to_device(run_data, device)
    # get p_targets from the notes
    p_targets = np.array([note_to_pitch[n] for n in notes])
    p_targets = torch.tensor(p_targets, device=device)
    with torch.no_grad():
        # Forward
        output = model(
            *(run_data[2:]),
            p_targets=p_targets, #None, 
            p_control=global_pitch,
            e_control=energy,
            d_control=duration
        )
        wav_file, wav_len = synth_samples(
            run_data,
            output,
            vocoder,
            model_config,
            preprocess_config,
            path='./', 
            filename=filename   
        )
        return wav_file, wav_len



if __name__ == "__main__":    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--lyrics",
        default="Daisy ... daisy ... give me your answer do. ",
        type=str,
        help="the lyrics you want to sing",
    )

    parser.add_argument(
        '--notes', 
        default="G,G,E,E,C,C,G,G,A,B,C,A,A,C,G,G",
        help='comma separated list of notes e.g. C,D,G', 
        type=lambda s: [str(item).upper() for item in s.split(',')], 
    )
    parser.add_argument(
        "--dur",
        default=8, 
        type=float,
        help="duration in seconds",
    )
    
    args = parser.parse_args()

    configs, model, vocoder = load_models()
 
    run_data, phones = prepare_batch_data(args.lyrics, configs[0])

    wav_file, wav_len = synthesize(model, 160000, 
        configs, 
        vocoder, run_data, 
        filename='output', # it will add .wav
        global_pitch=1, 
        energy=1, 
        duration=1,
        notes=args.notes
    )

    print("Sang ", len(phones), "in", wav_len, "per phone: ", float(wav_len) / len(phones))
    print("Wrote file",wav_file, "Singing ", args.lyrics, " with notes ", args.notes, "in time", args.dur, 'actual time ', wav_len)

    # now we do another synthesis using the scale to ensure it has a certain
    # length
    wav_file, wav_len = synthesize(model, 160000, configs, 
        vocoder, run_data, 
        filename='output', # it will add .wav
        global_pitch=1, 
        energy=1, 
        duration=args.dur / float(wav_len), 
        notes=args.notes
    )

    print('You asked for dur of ', args.dur, 'I got', wav_len)
