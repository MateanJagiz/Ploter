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
UPLOAD_FOLDER = 'images'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Dane
tasks = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/images')
def get_images():
    """Zwróć listę dostępnych obrazów"""
    images = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return jsonify({'images': images})

@app.route('/api/save-image', methods=['POST'])
def save_image():
    """Zapisz wrzucony obraz"""
    data = request.json
    try:
        # Zdekoduj base64 z binary string
        name = data['name']
        binary = data['binary']
        width = data['width']
        height = data['height']
        
        # Zapisz metadane
        meta_file = os.path.join(UPLOAD_FOLDER, name.replace('.', '_') + '.json')
        with open(meta_file, 'w') as f:
            json.dump({
                'name': name,
                'width': width,
                'height': height,
                'binary': binary[:1000]  # Zapisz pierwsze 1000 znaków
            }, f)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/run-plotter', methods=['POST'])
def run_plotter():
    """Uruchom Ploter z obrazem"""
    data = request.json
    image_name = data['image']
    instructions = data['instructions']
    task_id = len(tasks)
    
    # Uruchom w wątku
    thread = threading.Thread(target=process_image, args=(task_id, image_name, instructions))
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id})

def process_image(task_id, image_name, instructions):
    """Przetwórz obraz z tqdm"""
    image_path = os.path.join(UPLOAD_FOLDER, image_name)
    
    try:
        # Wczytaj obraz
        img = Image.open(image_path).convert('L')  # Konwertuj na grayscale
        img_array = np.array(img)
        
        steps = 5  # Liczba kroków przetwarzania
        
        # Utwórz pbar z opisem
        pbar = tqdm(total=100, desc=f"Ploter: {image_name}", unit='%')
        tasks[task_id] = pbar
        
        # Krok 1: Wczytaj (20%)
        socketio.emit('progress', {
            'percent': 20,
            'eta': '--',
            'step': 'Wczytywanie',
            'status': 'Wczytywanie obrazu...'
        })
        pbar.update(20)
        time.sleep(0.5)
        
        # Krok 2: Konwertuj (40%)
        binary_array = np.where(img_array > 127, ord('-'), ord('0'))
        socketio.emit('progress', {
            'percent': 40,
            'eta': '~5s',
            'step': 'Konwersja',
            'status': 'Konwersja na tablicę binarną...'
        })
        pbar.update(20)
        time.sleep(0.5)
        
        # Krok 3: Przetwarzaj (70%)
        result = binary_array.tobytes().decode('latin-1')
        socketio.emit('progress', {
            'percent': 70,
            'eta': '~2s',
            'step': 'Przetwarzanie',
            'status': 'Przetwarzanie instrukcji...'
        })
        pbar.update(30)
        time.sleep(0.3)
        
        # Krok 4: Zapisuj (100%)
        output_file = os.path.join(OUTPUT_FOLDER, image_name.replace('.', '_') + '_result.txt')
        with open(output_file, 'w') as f:
            f.write(result[:5000])  # Zapisz pierwsze 5000 znaków
        
        socketio.emit('progress', {
            'percent': 100,
            'eta': '0s',
            'step': 'Gotowe',
            'status': 'Ukończono!'
        })
        pbar.update(10)
        pbar.close()
        
        # Emituj "done"
        socketio.emit('done', {
            'result': 'Tablica zapisana do ' + output_file,
            'task_id': task_id
        })
        
    except Exception as e:
        socketio.emit('done', {
            'result': f'Błąd: {str(e)}',
            'task_id': task_id
        })
        if task_id in tasks:
            tasks[task_id].close()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

