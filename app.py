import os

from   flask import Flask, request, jsonify, render_template
from   werkzeug.utils import secure_filename

from   utils import save_uploaded_file, extract_document

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'documents/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Home route to display upload and query forms
@app.route('/')
def index():
    return render_template('index.html')


# Route to upload a document
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        return jsonify({"message": f"File {filename} uploaded successfully.", "path": file_path}), 201
    else:
        return jsonify({"error": "Invalid file type. Only PDFs are allowed."}), 400

# Route to extract text from an uploaded document
@app.route('/extract', methods=['POST'])
def extract_text():
    data = request.json
    print(data.get("query"))
    sim_index = extract_document(
        data.get("query"),
        app.config["UPLOAD_FOLDER"]
    )

    return jsonify(sim_index), 200

# Route to list all files in the storage
@app.route('list', methods=["GET"])
def list_files():
    try:
        files = os.listdir(app.config["UPLOAD_FOLDER"])
        pdf_files = [f for f in files if allowed_file(f)]
        return jsonify({"documents": pdf_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
