import os
import json
from transformers import RobertaTokenizer, RobertaModel
import torch
import numpy as np

_tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
_model = RobertaModel.from_pretrained("microsoft/codebert-base")
_model.eval()


def get_embedding_from_code(code_string):
    try:
        inputs = _tokenizer(
            code_string,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512  # Batasi panjang token untuk menghindari error
        )

        # Nonaktifkan gradien untuk efisiensi
        with torch.no_grad():
            outputs = _model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :]  # CLS token

        # Normalisasi embedding
        embedding = embedding.squeeze().numpy()
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Norm of the embedding is zero, cannot normalize.")
        embedding = embedding / norm

        return embedding.tolist()
    except Exception as e:
        print(f"Error saat memproses embedding: {e}")
        return None  # Kembalikan None jika terjadi error
    
def extract_and_save_embeddings(folder_path, output_json_path):
    embeddings_dict = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.py'):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    
                    try:
                        # Proses membaca file dan menghitung embedding
                        embedding = get_embedding_from_code(code)
                        embeddings_dict[file_name] = embedding
                    except Exception as e:
                        print(f"Gagal memproses {file_name}: {e}")

            except Exception as e:
                print(f"Gagal memproses {file_name}: {e}")

    # Simpan semua embedding ke file JSON
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as out_file:
        json.dump(embeddings_dict, out_file, indent=2)
    print(f"✅ Embeddings berhasil disimpan ke {output_json_path}")
