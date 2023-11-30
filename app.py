from flask import Flask, jsonify, request

app = Flask(__name__)

# Example endpoint to toggle mute status
mute_status = False

@app.route('/mute-state', methods=['GET'])
def get_mute_state():
    return jsonify({'mute_status': mute_status})

@app.route('/toggle-mute', methods=['POST'])
def toggle_mute():
    global mute_status
    mute_status = not mute_status
    return jsonify({'mute_status': mute_status})

@app.route("/")
def index():
    return "Hello World!"