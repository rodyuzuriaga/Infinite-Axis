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

        # Validate file type
        if not file or not file.filename:
            return jsonify({'success': False, 'error': 'No file uploaded'})

        allowed_extensions = {'png', 'jpg', 'jpeg'}
        file_extension = file.filename.lower().split('.')[-1]
        if file_extension not in allowed_extensions:
            return jsonify({'success': False, 'error': 'Only PNG, JPG, and JPEG files are allowed'})

        # Read file content first for size calculation
        file_content = file.read()
        original_size_mb = len(file_content) / (1024 * 1024)

        # Read image and convert to PNG bytes
        input_image = Image.open(BytesIO(file_content)).convert('RGBA')

        # Get original dimensions
        original_width, original_height = input_image.size

        # Handle large images - resize if too big (max 2048x2048 to prevent memory issues)
        max_size = 2048
        if original_width > max_size or original_height > max_size:
            print(f"🔄 Resizing large image ({original_width}x{original_height})...")
            # Calculate new dimensions maintaining aspect ratio
            ratio = min(max_size / original_width, max_size / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            input_image = input_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"✅ Image resized to {new_width}x{new_height}")

        print("🔄 Converting image to PNG format...")
        buf = BytesIO()
        input_image.save(buf, format='PNG')
        input_bytes = buf.getvalue()
        print("✅ Image converted to PNG")

        print("🤖 Starting background removal with rembg...")
        # Remove background using rembg
        result_bytes = remove(input_bytes)
        print("✅ Background removal completed")

        print("🔄 Processing result image...")
        result_image = Image.open(BytesIO(result_bytes)).convert('RGBA')

        # Save to file for download
        filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(GENERATED_DIR, filename)
        result_image.save(output_path, format='PNG')
        print(f"💾 Result saved as {filename}")

        # Convert result to base64 for preview
        print("🔄 Converting to base64 for preview...")
        output_buffer = BytesIO()
        result_image.save(output_buffer, format='PNG')
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        print("✅ Base64 conversion completed")

        return jsonify({
            'success': True,
            'image_url': f'/generated/{filename}',
            'image_data': f'data:image/png;base64,{output_base64}',
            'processed_prompt': 'background removal',
            'parameters': {
                'width': result_image.width,
                'height': result_image.height,
                'format': 'PNG',
                'original_size_mb': round(original_size_mb, 2),
                'resized': original_width > max_size or original_height > max_size
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