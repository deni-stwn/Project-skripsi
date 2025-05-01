import os
from transformers import RobertaTokenizer, RobertaModel
import torch

tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")
model.eval()

def get_embedding_from_code(code_string):
    inputs = tokenizer(code_string, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :]
    return embedding.squeeze().numpy()

def get_embeddings_from_folder(folder_path):
    embeddings = []
    file_names = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.py'):
            path = os.path.join(folder_path, file_name)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    code = f.read()
                emb = get_embedding_from_code(code)
                embeddings.append(emb)
                file_names.append(file_name)
            except Exception as e:
                print(f"Gagal memproses {file_name}: {e}")
    return embeddings, file_names
