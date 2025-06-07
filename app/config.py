import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'djaijsidjaisdi')
    MODEL_PATH = os.path.join(os.getcwd(), 'app', 'model', 'siamese_model.h5')
    ACCOUNT_KEY_FIREBASE = os.path.join(os.getcwd(), 'crud-833c1-firebase-adminsdk-e01ya-b83fe59025.json')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  
    
    # Base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Upload folder - parent folder for all user uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # Embeddings folder - parent folder for all user embeddings
    EMBEDDINGS_FOLDER = os.path.join(BASE_DIR, 'embeddings')
    
    # Ensure directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)
    
    @staticmethod
    def get_user_folder(user_id):
        """Get user-specific upload folder path"""
        if not user_id:
            return None
        user_folder = os.path.join(Config.UPLOAD_FOLDER, f"user_{user_id}")
        os.makedirs(user_folder, exist_ok=True)
        return user_folder
    
    @staticmethod
    def get_user_embeddings_path(user_id):
        """Get user-specific embeddings JSON file path"""
        if not user_id:
            return None
        return os.path.join(Config.EMBEDDINGS_FOLDER, f"embeddings_{user_id}.json")