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
    return jsonify({'files': files})

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

@monitoring_routes.route('/details/<int:index>', methods=['GET'])
def get_comparison_details(index):
    try:
        # Get results from the previous check
        json_output_path = current_app.config['EMBEDDINGS_PATH']
        results = check_plagiarism_from_json(json_output_path)
        
        if index < 0 or index >= len(results):
            return jsonify({'error': 'Invalid index'}), 400
            
        result = results[index]
        file1 = result['file_1']
        file2 = result['file_2']
        
        # Read file contents
        uploads_folder = current_app.config['UPLOAD_FOLDER']
        with open(os.path.join(uploads_folder, file1), 'r', encoding='utf-8') as f:
            content_1 = f.read()
        with open(os.path.join(uploads_folder, file2), 'r', encoding='utf-8') as f:
            content_2 = f.read()
            
        # Analyze matching blocks (simplified for this example)
        # In a real app, this would use a more sophisticated algorithm
        lines1 = content_1.split('\n')
        lines2 = content_2.split('\n')
        matching_blocks = []
        
        # Simple string matching for demonstration
        # In a real application, you'd use a proper code comparison algorithm
        for i, line1 in enumerate(lines1):
            if line1.strip():  # Skip empty lines
                for j, line2 in enumerate(lines2):
                    if line1.strip() == line2.strip() and len(line1.strip()) > 5:
                        matching_blocks.append({
                            'start': i,
                            'length': 1,
                            'file1_line': i,
                            'file2_line': j
                        })
                        break
        
        return jsonify({
            'file_1': file1,
            'file_2': file2,
            'content_1': content_1,
            'content_2': content_2,
            'matching_blocks': matching_blocks,
            'similarity': result['similarity']
        })
        
    except Exception as e:
        print(f"Error in get_comparison_details: {str(e)}")
        return jsonify({'error': str(e)}), 500

@monitoring_routes.route('/file/<path:filename>', methods=['GET'])
def get_file_content(filename):
    try:
        uploads_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(uploads_folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return jsonify({'content': content})
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