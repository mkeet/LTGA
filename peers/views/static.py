from peers.server import app
from flask import send_from_directory
import os.path

@app.route('/students/static/<path:filename>')
def custom_static(filename):
        dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/')
        print dir
        return send_from_directory(dir, filename)
