# !pip install tensorflow ipython transformers

# simple example of text continuation
from transformers import pipeline, set_seed
generator = pipeline('text-generation', model='distilgpt2')
res = generator("I like flowers ", max_length=30, num_return_sequences=5)
print(res)
