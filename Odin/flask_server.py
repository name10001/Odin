from flask import *
from flask_socketio import SocketIO
from os import urandom

app = Flask(__name__)
socket_io = SocketIO(app)
app.secret_key = urandom(16)
