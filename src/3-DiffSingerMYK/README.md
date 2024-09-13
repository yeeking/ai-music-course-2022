# Diffsinger notes + lyrics to singing voice audio system

This folder contains files that allow you to render a list of notes and some lyrics into a singing 'performance'. 

The code is a modified version of Keon Lee's version of the Diffsinger system. Here is Keon Lee's repo:

https://github.com/keonlee9420/DiffSinger

```
@misc{lee2021diffsinger,
  author = {Lee, Keon},
  title = {DiffSinger},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/keonlee9420/DiffSinger}}
}
```

Here is the citation for the original Diffsinger paper:

```
@misc{liu2022diffsingersingingvoicesynthesis,
      title={DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism}, 
      author={Jinglin Liu and Chengxi Li and Yi Ren and Feiyang Chen and Zhou Zhao},
      year={2022},
      eprint={2105.02446},
      archivePrefix={arXiv},
      primaryClass={eess.AS},
      url={https://arxiv.org/abs/2105.02446}, 
}
```

## How to run it 

Assuming you have created a virtualenv and installed the packages from ../requirements.txt, e.g. by doing this:

```
python3 -m venv ~/Python/ai-music-course
source ~/Python/ai-music-course/bin/activate
pip install -r ../requirements.txt
```

You then need to install some bits from nltk:

```
python
  >>> import nltk
  >>> nltk.download('averaged_perceptron_tagger_eng')
# (quit python)
cd diffsinger
python sing.py # use default melody,  lyrics and duration
```
A file 'output.wav' should appear in the folder. 

Then you can try specifying the lyrics and notes

```
python sing.py --lyrics "do ray me fa so la ti do" --notes C,D,E,F,G,A,B --dur 5
```

