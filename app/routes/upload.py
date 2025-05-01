from flask import Blueprint, request, render_template, redirect, flash
import os
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)
UPLOAD_FOLDER = 'uploads'

@upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.py'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash("✅ File berhasil diupload!", "success")
            return redirect('/upload')
        else:
            flash("❌ Hanya file Python (.py) yang diperbolehkan", "danger")
    return render_template('upload.html')
