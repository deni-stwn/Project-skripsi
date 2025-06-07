from flask import Blueprint, jsonify, render_template, request, current_app
import os
from app.utils.embedding import extract_and_save_embeddings
from app.utils.compare import check_plagiarism_from_json
from app.routes.upload import get_user_id, get_user_upload_folder
from app.config import Config

monitoring_routes = Blueprint('monitoring', __name__)

@monitoring_routes.route('/', methods=['GET'])
def monitoring_page():
    user_folder = get_user_upload_folder()
    
    if not user_folder:
        # User not authenticated
        return render_template('monitoring.html', files=[])
    
    files = [f for f in os.listdir(user_folder) if f.endswith('.py')]
    return render_template('monitoring.html', files=files)

@monitoring_routes.route('/files', methods=['GET'])
def list_uploaded_files():
    user_folder = get_user_upload_folder()
    
    if not user_folder:
        return jsonify({'files': []})
    
    files = [f for f in os.listdir(user_folder) if f.endswith('.py')]
    return jsonify({'files': files})

@monitoring_routes.route('/check', methods=['POST'])
def check():
    user_id = get_user_id()
    user_folder = get_user_upload_folder()
    
    if not user_folder or not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get the correct embeddings path (from EMBEDDINGS_FOLDER, not EMBEDDINGS_PATH)
        json_output_path = os.path.join(current_app.config['EMBEDDINGS_FOLDER'], f"embeddings_{user_id}.json")
        
        print(f"User folder: {user_folder}")
        print(f"JSON output path: {json_output_path}")

        extract_and_save_embeddings(user_folder, json_output_path, user_id=user_id)

        results = check_plagiarism_from_json(json_output_path)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@monitoring_routes.route('/details/<int:index>', methods=['GET'])
def get_comparison_details(index):
    user_folder = get_user_upload_folder()
    user_id = get_user_id()
    
    if not user_folder or not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Fix: Use EMBEDDINGS_FOLDER instead of EMBEDDINGS_PATH
        json_output_path = os.path.join(current_app.config['EMBEDDINGS_FOLDER'], f"embeddings_{user_id}.json")
        results = check_plagiarism_from_json(json_output_path)
        
        if index < 0 or index >= len(results):
            return jsonify({'error': 'Invalid index'}), 400
            
        result = results[index]
        file1 = result['file_1']
        file2 = result['file_2']
        
        # Read file contents
        with open(os.path.join(user_folder, file1), 'r', encoding='utf-8') as f:
            content_1 = f.read()
        with open(os.path.join(user_folder, file2), 'r', encoding='utf-8') as f:
            content_2 = f.read()
            
        # Analyze matching blocks
        matching_blocks = analyze_matching_blocks(content_1, content_2)
            
        return jsonify({
            'file_1': file1,
            'file_2': file2,
            'content_1': content_1,
            'content_2': content_2,
            'matching_blocks': matching_blocks,
            'similarity': result['similarity']
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in get_comparison_details: {str(e)}")
        return jsonify({'error': str(e)}), 500

@monitoring_routes.route('/file/<path:filename>', methods=['GET'])
def get_file_content(filename):
    user_folder = get_user_upload_folder()
    
    if not user_folder:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        file_path = os.path.join(user_folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@monitoring_routes.route('/reset', methods=['POST'])
def reset():
    user_folder = get_user_upload_folder()
    user_id = get_user_id()
    
    if not user_folder or not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Delete all files in user's upload folder
        for file in os.listdir(user_folder):
            file_path = os.path.join(user_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Fix: Use EMBEDDINGS_FOLDER instead of EMBEDDINGS_PATH
        json_output_path = os.path.join(current_app.config['EMBEDDINGS_FOLDER'], f"embeddings_{user_id}.json")
        if os.path.exists(json_output_path):
            os.remove(json_output_path)

        return jsonify({'message': 'Your files and embeddings have been reset.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def analyze_matching_blocks(content_1, content_2):
    """Find matching blocks between two code contents"""
    lines1 = content_1.split('\n')
    lines2 = content_2.split('\n')
    matching_blocks = []
    
    # Simple line-by-line matching for demonstration
    for i, line1 in enumerate(lines1):
        line1_stripped = line1.strip()
        if not line1_stripped or line1_stripped.startswith('#'):
            continue  # Skip empty lines and comments
            
        for j, line2 in enumerate(lines2):
            line2_stripped = line2.strip()
            if line2_stripped and line1_stripped == line2_stripped and len(line1_stripped) > 5:
                matching_blocks.append({
                    'file1_line': i,  
                    'file2_line': j,
                    'length': 1,
                    'content': line1_stripped
                })
    
    return matching_blocks