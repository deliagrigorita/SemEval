from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  

max_sequence_length = tokenizer.model_max_length
print(f"Lungimea maximă a secvenței pentru model: {max_sequence_length}")
