from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Para permitir requests desde el frontend

# Directorio para imágenes generadas (simulado)
GENERATED_DIR = 'generated'
os.makedirs(GENERATED_DIR, exist_ok=True)

# Simular modelo cargado (sin cargar realmente para probar frontend)
print("Simulando carga de modelo... (solo para frontend)")
pipe = None  # No cargar modelo
print("Modelo simulado listo")

@app.route('/')
def index():
    return send_from_directory('.', 'front.html')

@app.route('/front.html')
def front_html():
    return send_from_directory('.', 'front.html')

@app.route('/App.html')
def app_html():
    return send_from_directory('.', 'App.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get form data
        file = request.files['image']
        prompt = request.form['prompt']
        
        # Get camera parameters
        rotate = float(request.form.get('rotate', 0))
        forward = float(request.form.get('forward', 0))
        vertical = float(request.form.get('vertical', 0))
        wide_angle = request.form.get('wide_angle', 'false') == 'true'
        
        # Get advanced settings
        seed = int(request.form.get('seed', 42))
        guidance_scale = float(request.form.get('guidance_scale', 7.5))
        steps = int(request.form.get('steps', 20))
        height = int(request.form.get('height', 512))
        width = int(request.form.get('width', 512))

        # Read image
        image = Image.open(file.stream).convert("RGB")

        # Simulate generation based on camera parameters
        edited_image = image.copy()
        
        # Apply rotation
        if rotate != 0:
            edited_image = edited_image.rotate(-rotate, expand=False, fillcolor=(255, 255, 255))
        
        # Apply forward (zoom)
        if forward > 0:
            width_img, height_img = edited_image.size
            zoom_factor = 1 + (forward / 10)
            new_size = (int(width_img * zoom_factor), int(height_img * zoom_factor))
            edited_image = edited_image.resize(new_size, Image.LANCZOS)
            # Crop center
            left = (new_size[0] - width_img) // 2
            top = (new_size[1] - height_img) // 2
            edited_image = edited_image.crop((left, top, left + width_img, top + height_img))
        
        # Apply vertical angle (simulate with vertical shift and perspective)
        if vertical != 0:
            if vertical > 0:
                # Bird view - rotate slightly
                edited_image = edited_image.rotate(-10, expand=False, fillcolor=(255, 255, 255))
            else:
                # Worm view - rotate opposite
                edited_image = edited_image.rotate(10, expand=False, fillcolor=(255, 255, 255))
        
        # Apply wide angle
        if wide_angle:
            width_img, height_img = edited_image.size
            new_size = (int(width_img * 0.8), int(height_img * 0.8))
            resized = edited_image.resize(new_size, Image.LANCZOS)
            # Create new image with padding
            new_image = Image.new('RGB', (width_img, height_img), (240, 240, 240))
            x = (width_img - new_size[0]) // 2
            y = (height_img - new_size[1]) // 2
            new_image.paste(resized, (x, y))
            edited_image = new_image
        
        # Resize to requested dimensions
        if edited_image.size != (width, height):
            edited_image = edited_image.resize((width, height), Image.LANCZOS)

        # Save generated image
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join(GENERATED_DIR, filename)
        edited_image.save(filepath)

        # Return URL
        return jsonify({
            'success': True, 
            'image_url': f'/generated/{filename}',
            'processed_prompt': prompt,
            'parameters': {
                'rotate': rotate,
                'forward': forward,
                'vertical': vertical,
                'wide_angle': wide_angle,
                'seed': seed,
                'guidance_scale': guidance_scale,
                'steps': steps,
                'dimensions': f'{width}x{height}'
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generated/<filename>')
def get_generated(filename):
    return send_from_directory(GENERATED_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)