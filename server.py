import os
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO

# Import modules from the app package
from app.utils.sports_api import get_sports_data
from app.utils.chatbot import process_query

application = Flask(__name__)
socketio = SocketIO(application, cors_allowed_origins="*", async_mode='threading')

# Routes
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/api/sports/events', methods=['GET'])
def get_events():
    sport_type = request.args.get('type', 'all')
    events = get_sports_data(sport_type)
    return jsonify(events)

@application.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = process_query(message)
    return jsonify({'response': response})

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# This is the variable that Gunicorn will look for
app = application

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Use 0.0.0.0 to make the app publicly available
    socketio.run(application, host='0.0.0.0', port=port, debug=True) 