import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'djaijsidjaisdi')
    
    # Base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Model path with fallback
    MODEL_PATH = os.environ.get('MODEL_PATH') or os.path.join(BASE_DIR, 'app', 'model', 'best_model.h5')
    
    # Firebase key path with fallback
    ACCOUNT_KEY_FIREBASE = os.environ.get('FIREBASE_KEY_PATH') or os.path.join(BASE_DIR, 'crud-833c1-firebase-adminsdk-e01ya-b83fe59025.json')
    
    # File upload settings
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))  # 10MB default
    
    # Upload folder - parent folder for all user uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads')
    
    # Embeddings folder - parent folder for all user embeddings
    EMBEDDINGS_FOLDER = os.environ.get('EMBEDDINGS_FOLDER') or os.path.join(BASE_DIR, 'embeddings')
    
    # Firebase disable flag for testing
    DISABLE_FIREBASE = os.environ.get('DISABLE_FIREBASE', 'false').lower() == 'true'
    
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