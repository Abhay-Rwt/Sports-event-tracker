# App package initialization
from flask import Flask
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

socketio = SocketIO()

def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    
    socketio.init_app(app)
    
    return app 