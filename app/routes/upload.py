from flask import Blueprint, request, jsonify, current_app, render_template, session
import os
import zipfile
import shutil
from werkzeug.utils import secure_filename
import firebase_admin.auth as auth

upload_routes = Blueprint('upload', __name__)

def get_user_id():
    """Get current user ID from session or token"""
    # Check if user is authenticated
    token = request.cookies.get('token') or request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not token:
        return None
        
    try:
        # Verify the Firebase token
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

def get_user_upload_folder():
    """Get the upload folder specific to the current user"""
    user_id = get_user_id()
    
    if not user_id:
        return None
    
    # Use the helper from Config
    from app.config import Config
    return Config.get_user_folder(user_id)

@upload_routes.route('/', methods=['GET'])
def upload_page():
    # Get user-specific upload folder
    user_folder = get_user_upload_folder()
    
    if not user_folder:
        # User not authenticated, redirect to login
        return render_template('upload.html', files=[], error="Please log in to upload files")
    
    files = [f for f in os.listdir(user_folder) if f.endswith('.py')]
    return render_template('upload.html', files=files)

@upload_routes.route('/', methods=['POST'])
def upload_file():
    # Get user-specific upload folder
    user_folder = get_user_upload_folder()
    
    if not user_folder:
        return jsonify({'error': 'Authentication required'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension == '.zip':
        return handle_zip_upload(file, user_folder)
    elif file_extension == '.py':
        return handle_python_file_upload(file, filename, user_folder)
    else:
        return jsonify({'error': 'Only Python (.py) or ZIP files are allowed'}), 400

def handle_zip_upload(file, upload_folder):
    temp_zip_path = os.path.join(upload_folder, 'temp.zip')
    temp_extract_dir = os.path.join(upload_folder, 'temp_extract')
    python_files_count = 0

    try:
        file.save(temp_zip_path)
        os.makedirs(temp_extract_dir, exist_ok=True)
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)

        python_files_count = move_python_files_from_dir(temp_extract_dir, upload_folder)

        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)
        if os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)

        if python_files_count == 0:
            return jsonify({'error': 'No Python files found in the ZIP archive'}), 400

        return jsonify({
            'message': f'ZIP file processed successfully. {python_files_count} Python files extracted.',
            'files_count': python_files_count
        }), 200

    except zipfile.BadZipFile:
        return jsonify({'error': 'Invalid ZIP file'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing ZIP: {str(e)}'}), 500

def move_python_files_from_dir(src_dir, dest_dir):
    python_files_count = 0
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.py'):
                python_files_count += 1
                original_name = os.path.join(root, f)
                dest_name = os.path.join(dest_dir, f)
                counter = 1
                while os.path.exists(dest_name):
                    name_parts = os.path.splitext(f)
                    dest_name = os.path.join(
                        dest_dir,
                        f"{name_parts[0]}_{counter}{name_parts[1]}"
                    )
                    counter += 1
                shutil.copy2(original_name, dest_name)
    return python_files_count

def handle_python_file_upload(file, filename, upload_folder):
    save_path = os.path.join(upload_folder, filename)
    counter = 1
    while os.path.exists(save_path):
        name_parts = os.path.splitext(filename)
        save_path = os.path.join(
            upload_folder,
            f"{name_parts[0]}_{counter}{name_parts[1]}"
        )
        counter += 1
    file.save(save_path)
    return jsonify({'message': f'{os.path.basename(save_path)} uploaded successfully'}), 200