from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# File path to store mute status
mute_status_file = 'mute_status.txt'

# Function to read mute status from the file
def read_mute_status():
    try:
        with open(mute_status_file, 'r') as file:
            return file.read().strip().lower() == 'true'
    except FileNotFoundError:
        return False

# Function to write mute status to the file
def write_mute_status(status):
    with open(mute_status_file, 'w') as file:
        file.write('true' if status else 'false')

# Example endpoint to toggle mute status
@app.route('/mute-state', methods=['GET'])
def get_mute_state():
    mute_status = read_mute_status()
    return jsonify({'mute_status': mute_status})

@app.route('/toggle-mute', methods=['POST'])
def toggle_mute():
    mute_status = not read_mute_status()
    write_mute_status(mute_status)
    return jsonify({'mute_status': mute_status})

@app.route("/")
def index():
    return "Hello World!"

