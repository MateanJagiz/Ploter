from flask import Flask, render_template, request, jsonify, send_from_directory
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

@app.route('/api/save-image', methods=['POST'])
def save_image():
    """Zapisz wrzucony obraz"""
    data = request.json
    app.logger.info(f'data ===========> {data}')
    try:
        # Zdekoduj base64 z binary string
        name = data['name']
        binary = data['binary']
        width = data['width']
        height = data['height']
        imagepath = os.path.join(IMAGES_FOLDER, name.replace('.', '_') + '.png')
        print(imagepath)
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False})

@app.route('/api/run-plotter', methods=['POST'])
def run_plotter():
    """Uruchom Ploter z obrazem"""
    data = request.json
    app.logger.info(f'data : {data}')
    instruction = data['instruction_filename']
    return jsonify({'success': True})

@app.route('/api/make-instruction', methods=['POST'])
def make_instruction(image_data):
    """Przetwórz obraz z tqdm"""
    data = request.json
    app.logger.info(f'data : {data}')
    image_path = data['image_path']
    try:
        os.system(f'./src/get_instructon.py {image_path}')
        socketio.emit('done', {
            'result': 'Ok',
        })
    except Exception as e:
        socketio.emit('done', {
            'result': f'Błąd: {str(e)}',
        })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

