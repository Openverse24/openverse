from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app, origins=["https://moritzjenny.github.io"])

# File path to store mute status
mute_status_file = 'mute_status.txt'

# File path to store last clicked button and introduction text
last_clicked_file = 'last_clicked.txt'

# File path to store the introduction counter
introduction_counter_file = 'introduction.txt'

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

# Function to read the last clicked button and introduction text from the file
def read_last_clicked():
    try:
        with open(last_clicked_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return '{"last_clicked": "None", "introduction_text": ""}'

# Function to write the last clicked button and introduction text to the file
def write_last_clicked(option, introduction_text):
    data = {
        'last_clicked': option,
        'introduction_text': introduction_text
    }
    with open(last_clicked_file, 'w') as file:
        file.write(json.dumps(data))

# Function to read the introduction counter file
def read_introduction():
    try:
        with open(introduction_counter_file, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

# Function to write the introduction counter file
def write_introduction(counter):
    with open(introduction_counter_file, 'w') as file:
        file.write(str(counter))

# Example endpoint to toggle mute status
@app.route('/mute-state', methods=['GET'])
def get_mute_state():
    mute_status = read_mute_status()
    return jsonify({'mute_status': mute_status})

# Example endpoint to get the currently set option
@app.route('/get-option', methods=['GET'])
def get_option():
    option_data = json.loads(read_last_clicked())
    return jsonify(option_data)

# New endpoint to get the current counter value
@app.route('/get-introduction-count', methods=['GET'])
def get_introduction_count():
    # Read the current counter value
    current_counter = read_introduction()

    return jsonify({'counter': current_counter})

# Example endpoint to toggle mute status
@app.route('/toggle-mute', methods=['POST'])
def toggle_mute():
    mute_status = not read_mute_status()
    write_mute_status(mute_status)
    return jsonify({'mute_status': mute_status})

# Example endpoint to center the scene
@app.route('/center-scene', methods=['POST'])
def center_scene():
    # Implement the action for centering the scene if needed
    return jsonify({'success': True})

# Example endpoint to set chat, robot, or johan
@app.route('/set-option', methods=['POST'])
def set_option():
    option = request.json.get('option')

    # Read introduction text from the request
    introduction_text = request.json.get('introductionText', '')

    # Update last clicked button and introduction text in the file
    write_last_clicked(option, introduction_text)

    return jsonify({'success': True, 'last_clicked': option, 'introduction_text': introduction_text})


# New endpoint to increment the counter
@app.route('/introduction', methods=['POST'])
def introduction():
    # Read the current counter value
    current_counter = read_introduction()

    # Increment the counter
    new_counter = current_counter + 1

    # Write the new counter value to the file
    write_introduction(new_counter)

    return jsonify({'counter': new_counter})

@app.route("/")
def index():
    return "Co-Cre-AI-Tion Backend :) "
