from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import ast
import json
from apscheduler.schedulers.background import BackgroundScheduler






app = Flask(__name__)
CORS(app, origins=["https://moritzjenny.github.io", "https://openverse24.github.io", "*"])

# File path to store mute status
mute_status_file = 'mute_status.txt'

# File path to store last clicked button and introduction text
last_clicked_file = 'last_clicked.txt'

# File path to store the introduction counter
introduction_counter_file = 'introduction.txt'

# File that stores recent id's
recent_users = 'recent_users.txt'

temp_recent_users = []

def add_temp_recent_users(user_id):
    global temp_recent_users
    if not user_id in temp_recent_users:
        temp_recent_users.append(user_id)


# Function to read mute status from the file
def read_mute_status():
    try:
        with open(mute_status_file, 'r') as file:
            return file.read().strip().lower()
    except FileNotFoundError:
        return True

# Function to write mute status to the file
def write_mute_status(status, user_id):
    try:
        complete_file = json.loads(read_mute_status())
    except TypeError:
        complete_file = {}
    complete_file[str(user_id)] = ('true' if status else 'false')
    with open(mute_status_file, 'w') as file:
        file.write(json.dumps(complete_file))

# Function to read the last clicked button and introduction text from the file
def read_last_clicked():
    try:
        with open(last_clicked_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return '{"last_clicked": "None", "introduction_text": ""}'

# Function to write the last clicked button and introduction text to the file
def write_last_clicked(option, introduction_text, user_id):
    data = {
        'last_clicked': option,
        'introduction_text': introduction_text
    }
    complete_file = json.loads(read_last_clicked())
    complete_file[user_id] = data
    with open(last_clicked_file, 'w') as file:
        file.write(json.dumps(complete_file))

# Function to read the introduction counter file
def read_introduction():
    try:
        with open(introduction_counter_file, 'r') as file:
            return str(file.read().strip())
    except FileNotFoundError:
        return "{}"

def read_active_users():
    try:
        with open(recent_users, 'r') as file:
            return (file.read().strip())
    except FileNotFoundError:
        return 0

# Function to write the introduction counter file
def write_introduction(user_id):
    introduction_counter_data = json.loads(read_introduction())
    current_count = 0
    try:
        current_count = introduction_counter_data[str(user_id)]
    except KeyError:
        current_count = 0
    introduction_counter_data[str(user_id)] = current_count + 1
    with open(introduction_counter_file, 'w') as file:
        file.write(json.dumps(introduction_counter_data))
        return current_count + 1
    return 0

# Example endpoint to toggle mute status
@app.route('/mute-state/<string:user_id>', methods=['GET'])
def get_mute_state(user_id):
    try:
        data = json.loads(read_mute_status())
    except TypeError:
        data = {}

    try:
        mute_status = data[str(user_id)]
    except KeyError:
        mute_status = "true"
        write_mute_status("true", user_id)
    return jsonify({'mute_status': mute_status})

# Example endpoint to get the currently set option
@app.route('/get-option/<int:user_id>', methods=['GET'])
def get_option(user_id):
    option_data = json.loads(read_last_clicked())
    add_temp_recent_users(user_id)
    try:
        user_data = option_data[str(user_id)]
    except KeyError:
        user_data = {"introduction_text":"","last_clicked":"None"}
    return jsonify(user_data)

# New endpoint to get the current counter value
@app.route('/get-introduction-count/<string:user_id>', methods=['GET'])
def get_introduction_count(user_id):
    # Read the current counter value
    data = json.loads(read_introduction())
    try:
        current_counter = data[str(user_id)]
    except KeyError:
        current_counter = 0
    return jsonify({'counter': current_counter})


# Get all active user ID's
@app.route('/get-all-active-users', methods=['GET'])
def get_all_active_users():
    # Read the current counter value
    current_users = temp_recent_users

    return jsonify({'users': current_users})

# Example endpoint to toggle mute status
@app.route('/toggle-mute/<int:user_id>', methods=['POST'])
def toggle_mute(user_id):
    try:
        mute_status = json.loads(read_mute_status())[str(user_id)] != "true"
    except KeyError:
        mute_status = True
    write_mute_status(mute_status, user_id)
    return jsonify({'mute_status': mute_status})

# Example endpoint to center the scene
@app.route('/center-scene', methods=['POST'])
def center_scene():
    # Implement the action for centering the scene if needed
    return jsonify({'success': True})

# Example endpoint to set chat, robot, or johan
@app.route('/set-option/<int:user_id>', methods=['POST'])
def set_option(user_id):
    option = request.json.get('option')

    # Read introduction text from the request
    introduction_text = request.json.get('introductionText')

    # Update last clicked button and introduction text in the file
    write_last_clicked(option, introduction_text, user_id)

    return jsonify({'last_clicked': option, 'introduction_text': introduction_text})


# New endpoint to increment the counter
@app.route('/introduction/<int:user_id>', methods=['POST'])
def introduction(user_id):
    # Write the new counter value to the file
    new_counter = write_introduction(user_id)

    return jsonify({'counter': new_counter})

@app.route("/")
def index():
    return "Hello, this is the Co-Cre-AI-Tion Backend :) "

def scheduled_task():
    global temp_recent_users
    all_recent_users = []
    try:
        # Try to open the file for reading
        with open(recent_users, 'r') as file:
            content = file.read()
            all_recent_users = ast.literal_eval(content)
            old_recent_users = []
            for user in all_recent_users:
                if user not in temp_recent_users:
                    old_recent_users.append(user)
    except FileNotFoundError:
        # If the file doesn't exist, create it
        with open(recent_users, 'w') as file:
            file.write("")
            print(f"File created with initial content.")

    with open(recent_users, 'w') as file:
        file.write(str(temp_recent_users))

    temp_recent_users = []

    for user in old_recent_users:

        # Remove mute status
        try:
            complete_file = json.loads(read_mute_status())
            complete_file.pop(str(user))
        except TypeError:
            complete_file = {}
        except KeyError:
            pass
        with open(mute_status_file, 'w') as file:
            file.write(json.dumps(complete_file))

        # Remove last clicked entry
        complete_file = json.loads(read_last_clicked())
        try:
            complete_file.pop(str(user))
        except KeyError:
            pass
        with open(last_clicked_file, 'w') as file:
            file.write(json.dumps(complete_file))

        # Remove introduction count entry
        introduction_counter_data = json.loads(read_introduction())
        try:
            introduction_counter_data.pop(str(user))
        except KeyError:
            pass
        with open(introduction_counter_file, 'w') as file:
            file.write(json.dumps(introduction_counter_data))


# Create a scheduler instance
scheduler = BackgroundScheduler()

# Add the scheduled task to the scheduler
scheduler.add_job(scheduled_task, 'interval', minutes=1)

# Start the scheduler when the Flask app starts
scheduler.start()
scheduled_task()
