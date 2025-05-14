# app/utils/compare.py
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.saving import register_keras_serializable
import tensorflow.keras.backend as K
from itertools import combinations
from flask import current_app

@register_keras_serializable()
def euclidean_distance(vects):
    diff = K.abs(vects[0] - vects[1])
    return K.sum(diff, axis=1, keepdims=True) / K.int_shape(vects[0])[-1]

def load_embeddings(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    file_names = list(data.keys())
    embeddings = [np.array(data[f]) for f in file_names]
    return embeddings, file_names

def check_plagiarism_from_json(json_path):
    model = load_model(
        current_app.config['MODEL_PATH'],
        custom_objects={'euclidean_distance': euclidean_distance},
        compile=False
    )
    embeddings, file_names = load_embeddings(json_path)

    results = []
    for i, j in combinations(range(len(file_names)), 2):
        emb1 = np.expand_dims(embeddings[i], axis=0)
        emb2 = np.expand_dims(embeddings[j], axis=0)
        pred = model.predict([emb1, emb2], verbose=0)[0][0]
        similarity_score = pred * 100  
        results.append({
            'file_1': file_names[i],
            'file_2': file_names[j],
            'similarity': f"{similarity_score:.2f}%"  
        })

    results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    return results