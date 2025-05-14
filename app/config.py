import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MODEL_PATH = os.path.join(os.getcwd(), 'app', 'model', 'siamese_model.h5')
    EMBEDDINGS_PATH = os.path.join(os.getcwd(), 'embeddings', 'embeddings.json')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  
