from flask import Blueprint, request, jsonify, render_template
from app.firebase.firebase_config import create_user, verify_firebase_token, get_user_by_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@auth_bp.route('/register/submit', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user_id = create_user(email, password)
    return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201
    # if user_id:
    # return jsonify({'error': 'Failed to create user'}), 400

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/login/submit', methods=['POST'])
def login():
    data = request.get_json()
    id_token = data.get('idToken')
    
    if not id_token:
        return jsonify({'error': 'ID token is required'}), 400
    
    uid, email = verify_firebase_token(id_token)
    if uid and email:
        return jsonify({
            'message': 'Login successful',
            'user': {
                'uid': uid,
                'email': email
            }
        }), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200