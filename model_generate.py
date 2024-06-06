import argparse

from transformers import AutoTokenizer, AutoModelForCausalLM

parser = argparse.ArgumentParser(
    prog='model_generate.py',
    description='Generate output from a trained model',
)
parser.add_argument('sentence')
args = parser.parse_args()

local_model_path = 'gpt2-ger-digitec'

tokenizer = AutoTokenizer.from_pretrained("anonymous-german-nlp/german-gpt2")
model = AutoModelForCausalLM.from_pretrained(local_model_path)

input_text = args.sentence

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

input_ids = tokenizer(input_text, return_tensors='pt')

outputs = model.generate(
    **input_ids,
    pad_token_id=tokenizer.pad_token_id,
    num_beams=5,
    max_new_tokens=50,
    do_sample=True,
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)
