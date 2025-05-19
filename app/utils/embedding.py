import os
import json
from transformers import RobertaTokenizer, RobertaModel
import torch
import numpy as np
from flask import current_app

# Initialize tokenizer and model globally
_tokenizer = None
_model = None

def initialize_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        try:
            _tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
            _model = RobertaModel.from_pretrained("microsoft/codebert-base")
            _model.eval()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize model: {str(e)}")

def get_embedding_from_code(code_string):
    try:
        initialize_model()
        
        # Validate input
        if not code_string or not isinstance(code_string, str):
            raise ValueError("Invalid code input")

        inputs = _tokenizer(
            code_string,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = _model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :]

        # Convert to numpy and normalize
        embedding = embedding.squeeze().numpy()
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Zero embedding detected")
        normalized_embedding = embedding / norm

        return normalized_embedding.tolist()
    except Exception as e:
        current_app.logger.error(f"Embedding error: {str(e)}")
        raise

def extract_and_save_embeddings(folder_path, output_json_path):
    try:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        embeddings_dict = {}
        python_files = [f for f in os.listdir(folder_path) if f.endswith('.py')]
        
        if not python_files:
            raise ValueError("No Python files found in the specified folder")

        for file_name in python_files:
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                embedding = get_embedding_from_code(code)
                if embedding is not None:
                    embeddings_dict[file_name] = embedding
            except Exception as e:
                current_app.logger.error(f"Failed to process {file_name}: {str(e)}")
                continue

        if not embeddings_dict:
            raise ValueError("No valid embeddings generated")

        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, 'w', encoding='utf-8') as out_file:
            json.dump(embeddings_dict, out_file, indent=2)
        
        return embeddings_dict
    except Exception as e:
        current_app.logger.error(f"Embedding extraction failed: {str(e)}")
        raise