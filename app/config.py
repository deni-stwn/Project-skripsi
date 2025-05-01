import os

class Config:
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MODEL_PATH = os.path.join(os.getcwd(), 'app', 'model', 'siamese_model.h5')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
