import argparse

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

parser = argparse.ArgumentParser(
    prog='model_generate.py',
    description='Generate output from a trained model',
)
parser.add_argument('sentence')
args = parser.parse_args()

dig = pipeline('text-generation', model='gpt2-ger-digitec', tokenizer='anonymous-german-nlp/german-gpt2')
result = dig(args.sentence)[0]['generated_text']
print(result)
