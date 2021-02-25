from flask import send_from_directory, request
from werkzeug import secure_filename
from peers.server import app
import os.path

@app.route('/uploads/<filename>', methods=['post'])
def upload_image(image_name='image'):
    image = request.files[image_name]
    if image:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/students/uploads/<filename>')
@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
