from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['CONTRACT_FOLDER'] = '../contracts'

from app import routes