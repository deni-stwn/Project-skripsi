import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from itertools import combinations
from flask import current_app

@tf.keras.utils.register_keras_serializable()
def euclidean_distance(vects):
    diff = tf.abs(vects[0] - vects[1])
    return tf.reduce_sum(diff, axis=1, keepdims=True) / tf.cast(tf.shape(vects[0])[-1], tf.float32)

def load_embeddings(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both old and new format (with metadata)
    if "embeddings" in data:
        # New format with metadata
        embeddings_data = data["embeddings"]
    else:
        # Old format without metadata
        embeddings_data = data
    
    file_names = list(embeddings_data.keys())
    embeddings = []
    
    for f in file_names:
        if isinstance(embeddings_data[f], dict) and "embedding" in embeddings_data[f]:
            # New format where each file has a dict with "embedding" key
            embeddings.append(np.array(embeddings_data[f]["embedding"]))
        else:
            # Old format where each file maps directly to its embedding
            embeddings.append(np.array(embeddings_data[f]))
    
    return embeddings, file_names

def check_plagiarism_from_json(json_path):
    try:
        # Load model with custom configuration
        model = tf.keras.models.load_model(
            current_app.config['MODEL_PATH'],
            custom_objects={
                'euclidean_distance': euclidean_distance,
                'InputLayer': tf.keras.layers.InputLayer
            },
            compile=False,
            safe_mode=False
        )

        embeddings, file_names = load_embeddings(json_path)
        
        results = []
        for i, j in combinations(range(len(file_names)), 2):
            emb1 = np.expand_dims(embeddings[i], axis=0)
            emb2 = np.expand_dims(embeddings[j], axis=0)
            
            # Make prediction
            pred = model.predict(
                [emb1, emb2], 
                verbose=0,
                batch_size=1
            )[0][0]
            
            similarity_score = float(pred * 100)
            results.append({
                'file_1': file_names[i],
                'file_2': file_names[j],
                'similarity': similarity_score
            })

        results = sorted(results, key=lambda x: float(x['similarity']), reverse=True)
        return results
        
    except Exception as e:
        current_app.logger.error(f"Plagiarism check failed: {str(e)}")
        raise RuntimeError(f"Failed to check plagiarism: {str(e)}")