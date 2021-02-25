from flask import Flask
from flaskext.markdown import Markdown
import os.path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads/')
app.secret_key='asjdfkla;jdsfklajsdkl;fjiaoweruowufvbwehogayfz'
Markdown(app)


import peers.views
