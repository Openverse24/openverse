from flask import Flask, jsonify
from threading import Lock

app = Flask(__name__)

# Example endpoint to toggle mute status
mute_status = False
mute_status_lock = Lock()

@app.route('/mute-state', methods=['GET'])
def get_mute_state():
    with mute_status_lock:
        return jsonify({'mute_status': mute_status})

@app.route('/toggle-mute', methods=['POST'])
def toggle_mute():
    global mute_status
    with mute_status_lock:
        mute_status = not mute_status
        return jsonify({'mute_status': mute_status})

@app.route("/")
def index():
    return "Hello World!"
