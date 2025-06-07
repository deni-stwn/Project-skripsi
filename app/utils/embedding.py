import os
import json
import datetime
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

def extract_and_save_embeddings(folder_path, output_json_path, user_id=None):
    """
    Extract code embeddings from Python files and save them to a JSON file.
    
    Args:
        folder_path: Path to folder containing Python files
        output_json_path: Path to save the JSON embeddings
        user_id: Optional user ID for logging purposes
    """
    try:
        user_context = f"for user {user_id}" if user_id else ""
        current_app.logger.info(f"Extracting embeddings {user_context} from {folder_path}")
        
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        embeddings_dict = {}
        python_files = [f for f in os.listdir(folder_path) if f.endswith('.py')]
        
        if not python_files:
            raise ValueError(f"No Python files found in the folder {user_context}")

        current_app.logger.info(f"Processing {len(python_files)} Python files {user_context}")
        
        for file_name in python_files:
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                embedding = get_embedding_from_code(code)
                if embedding is not None:
                    embeddings_dict[file_name] = {
                        "embedding": embedding,
                        "file_path": file_path,
                        "file_name": file_name
                    }
            except Exception as e:
                current_app.logger.error(f"Failed to process {file_name} {user_context}: {str(e)}")
                continue

        if not embeddings_dict:
            raise ValueError(f"No valid embeddings generated {user_context}")

        # Create directory structure, without error if exists
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        
        # Save embeddings with metadata
        with open(output_json_path, 'w', encoding='utf-8') as out_file:
            output_data = {
                "metadata": {
                    "user_id": user_id,
                    "timestamp": str(datetime.datetime.now()),
                    "file_count": len(embeddings_dict)
                },
                "embeddings": embeddings_dict
            }
            json.dump(output_data, out_file, indent=2)
        
        current_app.logger.info(f"Successfully saved {len(embeddings_dict)} embeddings to {output_json_path}")
        return embeddings_dict
    except Exception as e:
        current_app.logger.error(f"Embedding extraction failed {user_context}: {str(e)}")
        raise