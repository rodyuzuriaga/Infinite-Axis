from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import glob
from PIL import Image
from rembg import remove
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)  # Para permitir requests desde el frontend

# Directory for generated images
GENERATED_DIR = 'generated'
os.makedirs(GENERATED_DIR, exist_ok=True)

def clean_generated_folder():
    """Delete all files in generated folder"""
    files = glob.glob(os.path.join(GENERATED_DIR, '*'))
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Error deleting {f}: {e}")
    return len(files)

print("Inicializando backend de Background Removal (rembg)...")

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
        # Clean old generated files before creating new one
        clean_generated_folder()
        
        file = request.files['image']
        
        # Read file content first for size calculation
        file_content = file.read()
        original_size_mb = len(file_content) / (1024 * 1024)
        
        # Read image and convert to PNG bytes
        input_image = Image.open(BytesIO(file_content)).convert('RGBA')
        
        # Get original dimensions
        original_width, original_height = input_image.size
        
        buf = BytesIO()
        input_image.save(buf, format='PNG')
        input_bytes = buf.getvalue()

        # Remove background using rembg
        result_bytes = remove(input_bytes)
        result_image = Image.open(BytesIO(result_bytes)).convert('RGBA')

        # Save to file for download
        filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(GENERATED_DIR, filename)
        result_image.save(output_path, format='PNG')

        # Convert result to base64 for preview
        output_buffer = BytesIO()
        result_image.save(output_buffer, format='PNG')
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return jsonify({
            'success': True,
            'image_url': f'/generated/{filename}',
            'image_data': f'data:image/png;base64,{output_base64}',
            'processed_prompt': 'background removal',
            'parameters': {
                'width': result_image.width,
                'height': result_image.height,
                'format': 'PNG',
                'original_size_mb': round(original_size_mb, 2)
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generated/<filename>')
def get_generated(filename):
    """Serve generated images for download"""
    return send_from_directory(GENERATED_DIR, filename)

@app.route('/clean', methods=['POST'])
def clean():
    """Clean all generated files"""
    try:
        deleted_count = clean_generated_folder()
        return jsonify({'success': True, 'deleted': deleted_count})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)