import functools
import os

from   flask import (
    Blueprint, flash, g, 
    redirect, render_template, request, 
    session, url_for, jsonify,
    send_from_directory
)
from   werkzeug.utils import secure_filename

from   utils import extract_document, save_uploaded_file


bp = Blueprint('documents', __name__, url_prefix='/documents')
UPLOAD_FOLDER = 'documents/'


# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

@bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = save_uploaded_file(file, UPLOAD_FOLDER)
        return jsonify({"message": f"File {filename} uploaded successfully.", "path": file_path}), 201
    else:
        return jsonify({"error": "Invalid file type. Only PDFs are allowed."}), 400
    

@bp.route('/', methods=['GET', 'POST'])
def list_documents():
    if request.method == 'GET':
        return render_template('upload.html')
    try:
        files = os.listdir(UPLOAD_FOLDER)
        pdf_files = [f for f in files if allowed_file(f)]
        return jsonify({"documents": pdf_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Route to download a file
@bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    print("downloading...")
    try:
        # Serve the file from the upload folder
        return send_from_directory(
            UPLOAD_FOLDER, filename, as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404


# Route to remove a file
@bp.route('/remove/<filename>', methods=['DELETE'])
def remove_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path) and allowed_file(filename):
            os.remove(file_path)
            return jsonify(
                {"message": f"File {filename} removed successfully."}
            ), 200
        else:
            return jsonify(
                {"error": "File not found or invalid file type."}
            ), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500