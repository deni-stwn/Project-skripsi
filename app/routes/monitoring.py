from flask import Blueprint, jsonify, render_template, request, current_app
import os
from pathlib import Path
from app.utils.embedding import extract_and_save_embeddings
from app.routes.upload import get_user_id, get_user_upload_folder

monitoring_routes = Blueprint('monitoring', __name__)

def _list_py_files(user_folder: str) -> list[str]:
    """List hanya .py, skip AppleDouble (._*) & hidden (.*)"""
    p = Path(user_folder)
    files = []
    for f in p.iterdir():
        if not f.is_file():
            continue
        name = f.name
        if name.startswith("._") or name.startswith("."):
            continue
        if name.endswith(".py"):
            files.append(name)
    return sorted(files)

@monitoring_routes.route('/', methods=['GET'])
def monitoring_page():
    user_folder = get_user_upload_folder()
    if not user_folder:
        return render_template('monitoring.html', files=[])
    return render_template('monitoring.html', files=_list_py_files(user_folder))

@monitoring_routes.route('/files', methods=['GET'])
def list_uploaded_files():
    user_folder = get_user_upload_folder()
    if not user_folder:
        return jsonify({'files': []})
    return jsonify({'files': _list_py_files(user_folder)})

@monitoring_routes.route('/check', methods=['POST'])
def check():
    # LAZY-IMPORT agar TensorFlow baru ke-load saat endpoint ini dipakai
    from app.utils.compare import check_plagiarism_from_json

    user_id = get_user_id()
    user_folder = get_user_upload_folder()
    if not user_folder or not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    # optional: batasi jumlah file per-run via query (?max_files=50)
    try:
        max_files = int(request.args.get('max_files', '50'))
        if max_files <= 0:
            max_files = 50
    except Exception:
        max_files = 50

    try:
        embeddings_dir = current_app.config['EMBEDDINGS_FOLDER']
        os.makedirs(embeddings_dir, exist_ok=True)
        json_output_path = os.path.join(embeddings_dir, f"embeddings_{user_id}.json")

        current_app.logger.info(f"User folder: {user_folder}")
        current_app.logger.info(f"JSON output path: {json_output_path} (max_files={max_files})")

        extract_and_save_embeddings(
            folder_path=user_folder,
            output_json_path=json_output_path,
            user_id=user_id,
            max_files=max_files,          # <-- batasi
        )

        results = check_plagiarism_from_json(json_output_path)
        return jsonify({'results': results})
    except Exception as e:
        current_app.logger.exception("Error in /monitoring/check")
        return jsonify({'error': str(e)}), 500

@monitoring_routes.route('/details/<int:index>', methods=['GET'])
def get_comparison_details(index):
    # LAZY-IMPORT supaya TF tidak ke-load di route lain
    from app.utils.compare import check_plagiarism_from_json

    user_folder = get_user_upload_folder()
    user_id = get_user_id()
    if not user_folder or not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    try:
        embeddings_dir = current_app.config['EMBEDDINGS_FOLDER']
        json_output_path = os.path.join(embeddings_dir, f"embeddings_{user_id}.json")
        results = check_plagiarism_from_json(json_output_path)

        if index < 0 or index >= len(results):
            return jsonify({'error': 'Invalid index'}), 400

        result = results[index]
        file1 = result['file_1']
        file2 = result['file_2']

        def read_file_with_fallback(filepath: str) -> str:
            encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
            for enc in encodings:
                try:
                    with open(filepath, 'r', encoding=enc) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            # terakhir: pakai replacement
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()

        content_1 = read_file_with_fallback(os.path.join(user_folder, file1))
        content_2 = read_file_with_fallback(os.path.join(user_folder, file2))

        matching_blocks = analyze_matching_blocks(content_1, content_2)

        return jsonify({
            'file_1': file1,
            'file_2': file2,
            'content_1': content_1,
            'content_2': content_2,
            'matching_blocks': matching_blocks,
            'similarity': result.get('similarity'),
        })
    except Exception as e:
        current_app.logger.exception("Error in get_comparison_details")
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

        encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return jsonify({'content': f.read()})
            except UnicodeDecodeError:
                continue
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return jsonify({'content': f.read()})
    except Exception as e:
        current_app.logger.exception("Error in get_file_content")
        return jsonify({'error': str(e)}), 500

@monitoring_routes.route('/reset', methods=['POST'])
def reset():
    user_folder = get_user_upload_folder()
    user_id = get_user_id()
    if not user_folder or not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    try:
        clean_macos_metadata_files(user_folder)
        for file in Path(user_folder).iterdir():
            if file.is_file():
                try:
                    file.unlink()
                except Exception as e:
                    current_app.logger.warning(f"Failed to delete {file}: {e}")

        embeddings_dir = current_app.config['EMBEDDINGS_FOLDER']
        json_output_path = os.path.join(embeddings_dir, f"embeddings_{user_id}.json")
        if os.path.exists(json_output_path):
            os.remove(json_output_path)

        return jsonify({'message': 'Your files and embeddings have been reset.'}), 200
    except Exception as e:
        current_app.logger.exception("Error in reset")
        return jsonify({'error': str(e)}), 500

def clean_macos_metadata_files(folder_path: str):
    """Remove macOS AppleDouble files (._*)"""
    for filename in os.listdir(folder_path):
        if filename.startswith('._'):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                current_app.logger.warning(f"Failed to remove metadata file {filename}: {e}")

def analyze_matching_blocks(content_1: str, content_2: str):
    """Sederhana: cocokkan baris persis (diabaikan spasi & komentar)"""
    lines1 = content_1.splitlines()
    lines2 = content_2.splitlines()
    matching = []
    for i, l1 in enumerate(lines1):
        s1 = l1.strip()
        if not s1 or s1.startswith('#'):
            continue
        for j, l2 in enumerate(lines2):
            s2 = l2.strip()
            if s2 and s1 == s2 and len(s1) > 5:
                matching.append({
                    'file1_line': i,
                    'file2_line': j,
                    'length': 1,
                    'content': s1
                })
    return matching
