import re
import json

from sklearn.model_selection import train_test_split

with open('reviews.json', encoding='utf8') as f:
    data = json.load(f)

def build_text_files(data_json, dest_path):
    f = open(dest_path, 'w', encoding='utf8')
    data = ''
    for product in data_json:
        if product is None:
            continue

        product_info = product['product_info']
        summary = str(product_info['brand_name']).strip() + " "
        summary += str(product_info['name']).strip() + " "
        summary += str(product_info['description']).strip() + " "
        summary += str(product_info['price']).strip() + " "
        summary += str(product_info['rating']).strip() + " "

        for review in product['reviews']:
            summary += str(review['rating']).strip() + " "
            summary += str(review['title']).strip() + " "
            summary += str(review['description']).strip() + " "

            for pro in review['pros']:
                summary += str(pro).strip() + " "

            for con in review['cons']:
                summary += str(con).strip() + " "

        summary = re.sub(r"\s", " ", summary)
        data += summary + "  "
    f.write(data)


train, test = train_test_split(data, test_size=0.15)

train_path = 'train_dataset.txt'
test_path = 'test_dataset.txt'
pretrained_model = 'anonymous-german-nlp/german-gpt2'

build_text_files(train, train_path)
build_text_files(test, test_path)

print("Train dataset length: " + str(len(train)))
print("Test dataset length: " + str(len(test)))

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(pretrained_model)

from transformers import TextDataset, DataCollatorForLanguageModeling


def load_dataset(train_path, test_path, tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=128)

    test_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=test_path,
        block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset, test_dataset, data_collator


train_dataset, test_dataset, data_collator = load_dataset(train_path, test_path, tokenizer)

from transformers import Trainer, TrainingArguments, AutoModelWithLMHead

model = AutoModelWithLMHead.from_pretrained(pretrained_model).to('cuda')

training_args = TrainingArguments(
    output_dir="gpt2-ger-digitec",  # The output directory
    overwrite_output_dir=True,  # overwrite the content of the output directory
    num_train_epochs=1000,  # number of training epochs
    per_device_train_batch_size=32,  # batch size for training
    per_device_eval_batch_size=64,  # batch size for evaluation
    eval_steps=400,  # Number of update steps between two evaluations.
    save_steps=800,  # after # steps model is saved
    warmup_steps=500,  # number of warmup steps for learning rate scheduler
    prediction_loss_only=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train(resume_from_checkpoint=True)

trainer.save_model()
