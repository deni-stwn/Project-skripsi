from flask import Blueprint, request, jsonify, current_app, render_template
import os
import zipfile
import shutil
from werkzeug.utils import secure_filename

upload_routes = Blueprint('upload', __name__)

@upload_routes.route('/', methods=['GET'])
def upload_page():
    folder = current_app.config['UPLOAD_FOLDER']
    files = [f for f in os.listdir(folder) if f.endswith('.py')]
    return render_template('upload.html' , files=files)

@upload_routes.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    filename = secure_filename(file.filename)
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension == '.zip':
        return handle_zip_upload(file)
    elif file_extension == '.py':
        return handle_python_file_upload(file, filename)
    else:
        return jsonify({'error': 'Only Python (.py) or ZIP files are allowed'}), 400

def handle_zip_upload(file):
    upload_folder = current_app.config['UPLOAD_FOLDER']
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

def handle_python_file_upload(file, filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
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