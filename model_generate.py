import argparse

from transformers import AutoTokenizer, GPT2LMHeadModel

parser = argparse.ArgumentParser(
    prog='model_generate.py',
    description='Generate output from a trained model',
)
parser.add_argument('sentence')
args = parser.parse_args()

local_model_path = 'gpt2-ger-digitec'

tokenizer = AutoTokenizer.from_pretrained("anonymous-german-nlp/german-gpt2")
model = GPT2LMHeadModel.from_pretrained(local_model_path)

input_text = args.sentence

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

input_ids = tokenizer.encode(input_text, return_tensors='pt')

output = model.generate(input_ids, max_length=50, num_return_sequences=1, pad_token_id=tokenizer.pad_token_id, do_sample=True)

response = tokenizer.decode(output[0], skip_special_tokens=True)

print(response)

