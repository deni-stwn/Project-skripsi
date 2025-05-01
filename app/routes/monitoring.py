from flask import Blueprint, render_template, current_app
import os
from app.services.plagiarism import check_plagiarism

monitor_bp = Blueprint("monitor", __name__)

@monitor_bp.route('/', methods=['GET'])
def monitor():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template('monitor.html', files=files)

@monitor_bp.route('/check', methods=['POST'])
def check():
    result = check_plagiarism()
    return render_template('monitor.html', result=result)
