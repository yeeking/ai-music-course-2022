from transformers import TFGPT2LMHeadModel
from transformers import pipeline

# assuming you are in the folder with the json and p5 files
model = TFGPT2LMHeadModel.from_pretrained('./euromodel/') 
# now make a pipeline - the pipeline API is very easy to use
generator = pipeline('text-generation', model=model, tokenizer='distilgpt2')
# and generate
res = generator("I like flowers ", max_length=30, num_return_sequences=5)
print(res)
