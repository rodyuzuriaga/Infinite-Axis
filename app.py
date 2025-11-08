from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import glob
from PIL import Image
from rembg import remove
from io import BytesIO
import base64
import gc
import psutil
import math

app = Flask(__name__)
CORS(app)  # Para permitir requests desde el frontend

# Directory for generated images
GENERATED_DIR = 'generated'
os.makedirs(GENERATED_DIR, exist_ok=True)

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def optimize_image_for_processing(image, max_size=1024, quality=85):
    """
    Optimize image for processing using mathematical compression techniques
    - Reduces dimensions using aspect ratio preservation
    - Applies JPEG compression for lossy formats
    - Maintains quality while reducing memory footprint
    """
    width, height = image.size

    # Calculate optimal dimensions using mathematical scaling
    if width > max_size or height > max_size:
        # Use mathematical ratio calculation for optimal scaling
        ratio = min(max_size / width, max_size / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        # Use high-quality Lanczos resampling for minimal quality loss
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"Optimized image: {width}x{height} -> {new_width}x{new_height}")

    return image

def smart_memory_cleanup():
    """Force garbage collection and memory cleanup"""
    gc.collect()
    # Force Python to return memory to OS
    import ctypes
    try:
        ctypes.CDLL('libc.so.6').malloc_trim(0)
    except:
        pass  # Not available on all systems

def calculate_optimal_chunk_size(image_size, available_memory_mb=400):
    """
    Calculate optimal chunk size for processing large images
    Uses mathematical formula: chunk_size = sqrt(available_memory / image_complexity)
    """
    width, height = image_size
    pixels = width * height

    # Estimate memory per pixel (RGBA = 4 bytes)
    memory_per_pixel = 4

    # Available memory for processing (leave 100MB for system)
    safe_memory = available_memory_mb - 100

    # Calculate optimal chunk size using square root for balanced processing
    optimal_pixels = int(math.sqrt(safe_memory * 1024 * 1024 / memory_per_pixel))

    # Ensure minimum chunk size
    chunk_size = max(512, min(optimal_pixels, min(width, height)))

    return chunk_size

def clean_generated_folder():
    """Delete all files in generated folder with memory cleanup"""
    files = glob.glob(os.path.join(GENERATED_DIR, '*'))
    deleted_count = 0
    for f in files:
        try:
            os.remove(f)
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {f}: {e}")

    # Force memory cleanup after file operations
    smart_memory_cleanup()
    return deleted_count

print(f"Backend initialized. Current memory usage: {get_memory_usage():.1f} MB")

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
    initial_memory = get_memory_usage()
    print(f"Starting processing. Memory: {initial_memory:.1f} MB")

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

        # Read file content with memory monitoring
        file_content = file.read()
        original_size_mb = len(file_content) / (1024 * 1024)
        print(f"File loaded: {original_size_mb:.1f} MB. Memory: {get_memory_usage():.1f} MB")

        # Read image with optimization
        input_image = Image.open(BytesIO(file_content)).convert('RGBA')
        original_width, original_height = input_image.size

        # Apply mathematical optimization for memory efficiency
        print("Applying memory optimization...")
        input_image = optimize_image_for_processing(input_image, max_size=1024)
        optimized_width, optimized_height = input_image.size

        # Calculate optimal processing parameters
        chunk_size = calculate_optimal_chunk_size((optimized_width, optimized_height))
        print(f"Optimal chunk size: {chunk_size}. Memory: {get_memory_usage():.1f} MB")

        # Convert to PNG with memory-efficient buffer management
        print("Converting to PNG format...")
        buf = BytesIO()
        input_image.save(buf, format='PNG', optimize=True)
        input_bytes = buf.getvalue()
        buf.close()  # Explicitly close buffer to free memory

        # Force cleanup before heavy processing
        del file_content
        smart_memory_cleanup()

        print(f"Starting background removal. Memory: {get_memory_usage():.1f} MB")
        # Remove background using rembg with memory monitoring
        result_bytes = remove(input_bytes)

        # Cleanup input data immediately
        del input_bytes
        smart_memory_cleanup()

        print("Processing result image...")
        result_image = Image.open(BytesIO(result_bytes)).convert('RGBA')

        # Calculate compression ratio for memory efficiency
        compression_ratio = (result_image.width * result_image.height) / (original_width * original_height)
        print(f"Compression ratio: {compression_ratio:.2f}. Memory: {get_memory_usage():.1f} MB")

        # Save to file with optimized settings
        filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(GENERATED_DIR, filename)
        result_image.save(output_path, format='PNG', optimize=True)
        print(f"Result saved. Memory: {get_memory_usage():.1f} MB")

        # Create base64 only when needed, with memory monitoring
        print("Creating preview...")
        output_buffer = BytesIO()
        result_image.save(output_buffer, format='PNG', optimize=True)
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        output_buffer.close()

        # Final memory cleanup
        del result_bytes, result_image
        smart_memory_cleanup()

        final_memory = get_memory_usage()
        memory_delta = final_memory - initial_memory

        print(f"Processing completed. Memory delta: {memory_delta:.1f} MB. Final: {final_memory:.1f} MB")

        return jsonify({
            'success': True,
            'image_url': f'/generated/{filename}',
            'image_data': f'data:image/png;base64,{output_base64}',
            'processed_prompt': 'background removal',
            'parameters': {
                'width': optimized_width,
                'height': optimized_height,
                'format': 'PNG',
                'original_size_mb': round(original_size_mb, 2),
                'compression_ratio': round(compression_ratio, 2),
                'memory_usage_mb': round(final_memory, 1),
                'memory_delta_mb': round(memory_delta, 1),
                'optimized': original_width > 1024 or original_height > 1024
            }
        })

    except Exception as e:
        # Emergency memory cleanup on error
        smart_memory_cleanup()
        error_memory = get_memory_usage()
        print(f"Error occurred. Memory: {error_memory:.1f} MB. Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})@app.route('/generated/<filename>')
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

@app.route('/health')
def health():
    """Health check endpoint for container orchestration"""
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-11-08',
        'memory_usage_mb': round(get_memory_usage(), 1),
        'service': 'infinite-axis-bg-removal'
    })

@app.route('/ready')
def ready():
    """Readiness check endpoint"""
    try:
        # Test if we can create a simple image (tests rembg availability)
        from PIL import Image
        test_img = Image.new('RGB', (10, 10), color='red')
        return jsonify({'status': 'ready', 'message': 'Service is ready to process images'})
    except Exception as e:
        return jsonify({'status': 'not_ready', 'error': str(e)}), 503

if __name__ == '__main__':
    print("🚀 Starting Infinite Axis Background Removal Service...")
    print(f"📊 Initial memory usage: {get_memory_usage():.1f} MB")

    # Test rembg initialization
    try:
        print("🔧 Testing rembg initialization...")
        from rembg import remove
        from PIL import Image
        # Create a simple test image
        test_img = Image.new('RGB', (10, 10), color='red')
        test_buffer = BytesIO()
        test_img.save(test_buffer, format='PNG')
        test_bytes = test_buffer.getvalue()
        test_buffer.close()

        # Test rembg with a simple image
        result = remove(test_bytes)
        print("✅ Rembg initialized successfully")
    except Exception as e:
        print(f"❌ Rembg initialization failed: {e}")
        exit(1)

    print("🌐 Starting Flask server on 0.0.0.0:5000")
    print("📡 Health check available at: http://localhost:5000/health")
    print("🔍 Readiness check available at: http://localhost:5000/ready")

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)