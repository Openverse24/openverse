from flask import Flask, jsonify

app = Flask(__name__)

# Your mute status variable
is_muted = False

@app.route("/")
def index():
    return "Hello this is the new version!"

@app.route('/mute-status', methods=['GET'])
def get_mute_status():
    return jsonify({'isMuted': is_muted})

@app.route('/toggle-mute', methods=['POST'])
def toggle_mute():
    global is_muted
    is_muted = not is_muted
    return jsonify({'isMuted': is_muted})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

