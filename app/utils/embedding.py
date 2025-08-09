import os
import json
import datetime
from pathlib import Path
import numpy as np
from flask import current_app

# Lazy globals
_tokenizer = None
_model = None

def _initialize_model():
    """Lazy load transformers/torch & model hanya saat dibutuhkan."""
    global _tokenizer, _model
    if _tokenizer is not None and _model is not None:
        return
    try:
        from transformers import RobertaTokenizer, RobertaModel
        import torch
        # irit CPU
        try:
            torch.set_num_threads(1)
        except Exception:
            pass

        _tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        _model = RobertaModel.from_pretrained("microsoft/codebert-base")
        _model.eval()  # CPU default
    except Exception as e:
        raise RuntimeError(f"Failed to initialize model: {e}")

def _iter_python_files(root_dir: str):
    """Iterasi semua .py (rekursif), skip AppleDouble (._) & hidden (.)"""
    for p in Path(root_dir).rglob("*.py"):
        name = p.name
        if name.startswith("._") or name.startswith("."):
            continue
        yield p

def _read_text_robust(path: Path) -> str:
    """Baca file dengan fallback encoding; terakhir pakai ignore."""
    data = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")

def get_embedding_from_code(code_string: str):
    try:
        _initialize_model()

        if not code_string or not isinstance(code_string, str):
            raise ValueError("Invalid code input")

        import torch

        inputs = _tokenizer(
            code_string,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512,
        )

        with torch.no_grad():
            outputs = _model(**inputs)
            vec = outputs.last_hidden_state[:, 0, :].squeeze().numpy()

        norm = np.linalg.norm(vec)
        if norm == 0:
            raise ValueError("Zero embedding detected")
        return (vec / norm).tolist()

    except Exception as e:
        current_app.logger.error(f"Embedding error: {e}")
        raise

def extract_and_save_embeddings(
    folder_path: str,
    output_json_path: str,
    user_id: str | None = None,
    max_files: int = 50,   # <-- batasi default untuk hindari timeout/OOM
):
    """
    Extract code embeddings from Python files and save them to a JSON file.
    """
    user_context = f"for user {user_id}" if user_id else ""
    try:
        current_app.logger.info(f"Extracting embeddings {user_context} from {folder_path}")

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        files = sorted(_iter_python_files(folder_path), key=lambda p: p.name)
        files = list(files)
        if not files:
            raise ValueError(f"No Python files found in the folder {user_context}")

        # terapkan batas file agar request tidak terlalu berat
        if max_files and max_files > 0:
            files = files[:max_files]

        current_app.logger.info(f"Processing {len(files)} Python files {user_context} (capped by max_files={max_files})")

        embeddings_dict: dict[str, dict] = {}

        for p in files:
            try:
                code = _read_text_robust(p)
                emb = get_embedding_from_code(code)
                if emb is not None:
                    embeddings_dict[p.name] = {
                        "embedding": emb,
                        "file_path": str(p),
                        "file_name": p.name,
                    }
            except MemoryError as me:
                current_app.logger.error(f"MemoryError on {p.name} {user_context}: {me}")
                break
            except Exception as e:
                current_app.logger.error(f"Failed to process {p.name} {user_context}: {e}")
                continue

        if not embeddings_dict:
            raise ValueError(f"No valid embeddings generated {user_context}")

        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        output_data = {
            "metadata": {
                "user_id": user_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "file_count": len(embeddings_dict),
            },
            "embeddings": embeddings_dict,
        }
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        current_app.logger.info(f"Successfully saved {len(embeddings_dict)} embeddings to {output_json_path}")
        return embeddings_dict

    except Exception as e:
        current_app.logger.error(f"Embedding extraction failed {user_context}: {e}")
        raise
