from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from myapp.models import User
from flask.ext.socketio import SocketIO
app = Flask(__name__)
UPLOAD_FOLDER = '/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config')
socketio = SocketIO(app)
import myapp.views,  models
from myapp import database
database.init_db()

