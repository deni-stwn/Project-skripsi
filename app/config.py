import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'djaijsidjaisdi')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MODEL_PATH = os.path.join(os.getcwd(), 'app', 'model', 'siamese_model.h5')
    EMBEDDINGS_PATH = os.path.join(os.getcwd(), 'embeddings', 'embeddings.json')
    ACCOUNT_KEY_FIREBASE = os.path.join(os.getcwd(), 'crud-833c1-firebase-adminsdk-e01ya-b83fe59025.json')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  
