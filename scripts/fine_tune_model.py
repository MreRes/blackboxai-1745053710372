from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
import datasets
import json

def load_dataset_from_jsonl(file_path):
    texts = []
    labels = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            texts.append(item['prompt'])
            # For simplicity, map completion text to label index (customize as needed)
            labels.append(0)  # Placeholder label
    return texts, labels

def tokenize_function(examples, tokenizer):
    return tokenizer(examples, padding="max_length", truncation=True)

def main():
    model_name = "indobenchmark/indobert-base-p1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    texts, labels = load_dataset_from_jsonl('training_data.jsonl')

    dataset = datasets.Dataset.from_dict({'text': texts, 'label': labels})
    tokenized_dataset = dataset.map(lambda x: tokenizer(x['text'], padding="max_length", truncation=True), batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()
    trainer.save_model("./fine_tuned_model")

if __name__ == "__main__":
    main()
