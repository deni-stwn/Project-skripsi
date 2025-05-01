from flask import Blueprint, jsonify
import os
from app.utils.embedding import get_embeddings_from_folder
from app.utils.compare import check_plagiarism

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/files', methods=['GET'])
def list_uploaded_files():
    folder = os.path.join(os.getcwd(), 'uploads')
    files = os.listdir(folder)
    return jsonify({'uploaded_files': files})

@monitoring_bp.route('/check', methods=['POST'])
def check():
    embeddings, file_names = get_embeddings_from_folder('uploads')
    results = check_plagiarism(embeddings, file_names)
    return jsonify({'plagiarism_results': results})
