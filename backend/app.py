from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import shutil
import uuid
import threading
from werkzeug.utils import secure_filename
from processor import process_pdfs, process_images_to_pdf
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename, mode):
    ext = filename.rsplit('.', 1)[1].lower()
    if mode == 'pdf':
        return ext in ALLOWED_EXTENSIONS['pdf']
    elif mode == 'image':
        return ext in ALLOWED_EXTENSIONS['image']
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No files selected'}), 400
    
    files = request.files.getlist('files')
    lang = request.form.get('lang', 'ben')
    mode = request.form.get('mode', 'pdf')
    
    if len(files) == 0 or all(file.filename == '' for file in files):
        return jsonify({'error': 'No files selected'}), 400

    session_id = str(uuid.uuid4())
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(upload_dir, exist_ok=True)

    for file in files:
        if file and allowed_file(file.filename, mode):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_dir, filename))

    return jsonify({
        'session_id': session_id,
        'lang': lang,
        'mode': mode
    })

@app.route('/process/<session_id>/<mode>/<lang>')
def process_files(session_id, mode, lang):
    input_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    output_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id, 'output')
    
    def processing_task():
        try:
            if mode == 'pdf':
                process_pdfs(input_dir, output_dir, lang=lang, session_id=session_id)
            elif mode == 'image':
                process_images_to_pdf(input_dir, output_dir, session_id=session_id)
        except Exception as e:
            print(f"Processing error: {str(e)}")

    thread = threading.Thread(target=processing_task)
    thread.start()
    
    return jsonify({'status': 'processing'})

@app.route('/progress/<session_id>')
def get_progress(session_id):
    session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    
    if not os.path.exists(session_dir):
        return jsonify({'error': 'Session not found'}), 404

    progress_file = os.path.join(session_dir, 'progress.txt')
    
    try:
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                current, total = map(int, f.read().split(','))
                progress = round((current / total) * 100, 1) if total > 0 else 0
                return jsonify({
                    'current': current,
                    'total': total,
                    'progress': progress
                })
        else:
            return jsonify({
                'current': 0,
                'total': 0,
                'progress': 0
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<session_id>')
def download_files(session_id):
    output_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id, 'output')
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id, 'output.zip')
    
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', output_dir)
    
    return send_from_directory(
        os.path.dirname(zip_path),
        'output.zip',
        as_attachment=True,
        mimetype='zip'
    )

@app.route('/cleanup/<session_id>', methods=['DELETE'])
def cleanup_session(session_id):
    session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
    return jsonify({'status': 'cleaned'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)