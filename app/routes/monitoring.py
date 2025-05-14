from flask import Blueprint, jsonify, render_template, request, current_app
import os
import shutil
from app.utils.embedding import extract_and_save_embeddings
from app.utils.compare import check_plagiarism_from_json

monitoring_routes = Blueprint('monitoring', __name__)

@monitoring_routes.route('/', methods=['GET'])
def monitoring_page():
    # lempar file ke halaman monitoring
    folder = current_app.config['UPLOAD_FOLDER']
    files = [f for f in os.listdir(folder) if f.endswith('.py')]
    return render_template('monitoring.html', files=files)

@monitoring_routes.route('/files', methods=['GET'])
def list_uploaded_files():
    folder = current_app.config['UPLOAD_FOLDER']
    files = [f for f in os.listdir(folder) if f.endswith('.py')]
    return jsonify({'uploaded_files': files})

@monitoring_routes.route('/check', methods=['POST'])
def check():
    try:
        uploads_folder = current_app.config['UPLOAD_FOLDER']
        json_output_path = current_app.config['EMBEDDINGS_PATH']
        print(f"Uploads folder: {uploads_folder}")
        print(f"JSON output path: {json_output_path}")

        extract_and_save_embeddings(uploads_folder, json_output_path)

        results = check_plagiarism_from_json(json_output_path)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@monitoring_routes.route('/reset', methods=['POST'])
def reset():
    try:
        # Hapus semua file di folder uploads
        uploads_folder = current_app.config['UPLOAD_FOLDER']
        if os.path.exists(uploads_folder):
            shutil.rmtree(uploads_folder)
            os.makedirs(uploads_folder)  # Buat ulang folder kosong

        # Hapus file JSON embeddings
        json_output_path = current_app.config['EMBEDDINGS_PATH']
        if os.path.exists(json_output_path):
            os.remove(json_output_path)

        return jsonify({'message': 'Uploads folder and embeddings have been reset.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500