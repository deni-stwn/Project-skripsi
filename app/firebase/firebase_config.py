import firebase_admin
from firebase_admin import credentials, auth
from app.config import Config

cred = credentials.Certificate(Config.ACCOUNT_KEY_FIREBASE)
firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid'], decoded_token['email']
    except Exception as e:
        print("Token verification failed:", str(e))
        return None, None

def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            email_verified=False
        )
        return user.uid
    except Exception as e:
        print("User creation failed:", str(e))
        return None

def get_user_by_email(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception as e:
        print("Get user failed:", str(e))
        return None