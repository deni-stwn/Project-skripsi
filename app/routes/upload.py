from flask import Blueprint, request, jsonify, current_app
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(save_path)
    return jsonify({'message': f'{file.filename} uploaded successfully'}), 200
