from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
from tqdm import tqdm
import threading
import os
import json
from PIL import Image
import numpy as np
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ploter-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Foldery
IMAGES_FOLDER = 'images'
INSTRUCTION_FOLDER = 'instructions'
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(INSTRUCTION_FOLDER, exist_ok=True)

# Dane

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/images')
def get_images():
    """Zwróć listę dostępnych obrazów"""
    images = [f for f in os.listdir(IMAGES_FOLDER) if f.endswith(('.png'))]
    app.logger.info(f'Obrazy ===> {images}')
    return jsonify({'instructions': images})

@app.route('/api/instructions')
def get_instructions():
    """Zwróć listę dostępnych obrazów"""
    instructions = [f for f in os.listdir(INSTRUCTION_FOLDER) if f.endswith(('.json'))]
    app.logger.info(f'Instrukcje ===> {instructions}')
    return jsonify({'instructions': instructions})

# Ustawienie folderu zapisu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Tworzy folder jeśli nie istnieje

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/save_image', methods=['POST'])
def save_image():
    # Sprawdzenie czy plik jest w żądaniu
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Brak pliku w żądaniu'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'Nie wybrano pliku'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        images = [f for f in os.listdir(IMAGES_FOLDER) if f.endswith(('.png'))]

        if filename in images:
            return jsonify({'success': False, 'message': f'Plik o tej nazwie już istnieje'}), 500

        try:
            file.save(save_path)
            # Zwracamy sukces (można też zwrócić np. URL do obrazka)
            return jsonify({
                'success': True,
                'message': f'Zapisano: {filename}',
                'filename': filename
            })
        except Exception as e:
            return jsonify({'success': False, 'message': f'Błąd zapisu: {str(e)}'}), 500

    return jsonify({'success': False, 'message': 'Niedozwolony typ pliku'}), 400

@app.route('/api/run-plotter', methods=['POST'])
def run_plotter():
    """Uruchom Ploter z obrazem"""
    data = request.json
    app.logger.info(f'data : {data}')
    instruction_name = data['instruction_filename']
    app.logger.info(f'Image name : {instruction_name}')
    try:
        os.system(f'python src/plot.py instructions/{instruction_name}')
        return jsonify({'success': True})
        socketio.emit('done', {
            'result': 'Ok',
        })
    except Exception as e:
        socketio.emit('done', {
            'result': f'Błąd: {str(e)}',
        })

@app.route('/api/make-instruction', methods=['POST'])
def make_instruction():
    """Przetwórz obraz z tqdm"""
    data = request.json
    app.logger.info(f'data : {data}')
    imagename = data['image_filename']
    app.logger.info(f'Image name : {imagename}')
    try:
        os.system(f'python ./src/get_instructon.py images/{imagename}')
        return jsonify({'success': True})
        socketio.emit('done', {
            'result': 'Ok',
        })
    except Exception as e:
        socketio.emit('done', {
            'result': f'Błąd: {str(e)}',
        })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

