from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://moritzjenny.github.io"])

# File path to store mute status
mute_status_file = 'mute_status.txt'

# File path to store last clicked button
last_clicked_file = 'last_clicked.txt'

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

# Function to read the last clicked button from the file
def read_last_clicked():
    try:
        with open(last_clicked_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return 'None'

# Function to write the last clicked button to the file
def write_last_clicked(button):
    with open(last_clicked_file, 'w') as file:
        file.write(button)

# Example endpoint to toggle mute status
@app.route('/mute-state', methods=['GET'])
def get_mute_state():
    mute_status = read_mute_status()
    return jsonify({'mute_status': mute_status})

# Example endpoint to get the currently set option
@app.route('/get-option', methods=['GET'])
def get_option():
    option = read_last_clicked()
    return jsonify({'last_clicked': option})


# Example endpoint to center the scene
@app.route('/center-scene', methods=['POST'])
def center_scene():
    # Implement the action for centering the scene if needed
    return jsonify({'success': True})

# Example endpoint to set chat, robot, or johan
@app.route('/set-option', methods=['POST'])
def set_option():
    option = request.json.get('option')

    # Update last clicked button
    write_last_clicked(option)



    return jsonify({'success': True, 'last_clicked': option})

@app.route("/")
def index():
    return "Co-Cre-AI-Tion Backend :) "
