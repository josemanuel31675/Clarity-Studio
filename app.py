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

    width = request.form.get('width', type=int)
    height = request.form.get('height', type=int)
    remove_bg = request.form.get('remove_bg') == 'true'

    try:
        # Open image directly from stream
        input_image = file.read()
        img = Image.open(io.BytesIO(input_image))
        
        # 1. Remove background if requested
        if remove_bg:
            print("Iniciando remoción de fondo con IA...")
            # We use rembg. remove() handles the conversion and processing
            try:
                # Specify a local home for the model to avoid permission issues
                os.environ['U2NET_HOME'] = os.path.join(os.getcwd(), '.u2net')
                output_data = remove(input_image)
                img = Image.open(io.BytesIO(output_data))
                print("Fondo removido exitosamente.")
            except Exception as e_rembg:
                print(f"Error específico en rembg: {str(e_rembg)}")
                return jsonify({'error': 'Error al procesar la IA de fondo. El servidor podría estar saturado.'}), 500

        # Convert to RGBA for transparency support in output
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 2. Resize if dimensions are provided
        if width and height:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        elif width or height:
            # Maintain aspect ratio logic
            w, h = img.size
            if width:
                h = int(h * (width / w))
                w = width
            else:
                w = int(w * (height / h))
                h = height
            img = img.resize((w, h), Image.Resampling.LANCZOS)

        # Save result to a buffer
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='clarity_logo.png')

    except Exception as e:
        print(f"Error general de procesamiento: {str(e)}")
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
