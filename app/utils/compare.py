import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
import itertools
from flask import current_app

def check_plagiarism(embeddings, file_names, threshold=0.85):
    model = load_model(current_app.config['MODEL_PATH'])
    # model = load_model('app/model/siamese_model.h5')
    results = []

    for (i, j) in itertools.combinations(range(len(embeddings)), 2):
        e1, e2 = embeddings[i], embeddings[j]
        pred = model.predict([np.expand_dims(e1, axis=0), np.expand_dims(e2, axis=0)])
        similarity = pred[0][0]
        if similarity > threshold:
            results.append({
                'file_1': file_names[i],
                'file_2': file_names[j],
                'similarity': float(similarity)
            })
    return results
