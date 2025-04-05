import os
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO

# Import modules from the app package
from app.utils.sports_api import get_sports_data
from app.utils.chatbot import process_message

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sports/events', methods=['GET'])
def get_events():
    sport_type = request.args.get('type', 'all')
    events = get_sports_data(sport_type)
    return jsonify(events)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = process_message(message)
    return jsonify({'response': response})

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Use 0.0.0.0 to make the app publicly available
    socketio.run(app, host='0.0.0.0', port=port, debug=True) 