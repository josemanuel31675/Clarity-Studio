import os
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Get parameters
    width = request.form.get('width', type=int)
    height = request.form.get('height', type=int)
    remove_bg = request.form.get('remove_bg') == 'true'

    try:
        # Open image
        img = Image.open(file.stream)
        
        # Convert to RGBA if we are removing background
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 1. Remove background if requested
        if remove_bg:
            # We use rembg for high-quality background removal
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            output_data = remove(img_byte_arr.getvalue())
            img = Image.open(io.BytesIO(output_data))

        # 2. Resize if dimensions are provided
        if width and height:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        elif width:
            # Maintain aspect ratio if only width is provided
            w_percent = (width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((width, h_size), Image.Resampling.LANCZOS)
        elif height:
            # Maintain aspect ratio if only height is provided
            h_percent = (height / float(img.size[1]))
            w_size = int((float(img.size[0]) * float(h_percent)))
            img = img.resize((w_size, height), Image.Resampling.LANCZOS)

        # Save result to a buffer
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='processed_logo.png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
