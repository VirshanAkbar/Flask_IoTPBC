from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_LOG_FILE = "./Blockchain_IoT/data_log.json"
LATEST_DATA_FILE = "./Blockchain_IoT/latest_data.json"

# Initialize files if they don't exist
if not os.path.exists(DATA_LOG_FILE):
    with open(DATA_LOG_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(LATEST_DATA_FILE):
    with open(LATEST_DATA_FILE, 'w') as f:
        json.dump({"temperature": None, "humidity": None, "timestamp": None}, f)


@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()
    if not data or 'temperature' not in data or 'humidity' not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_entry = {
        "temperature": data['temperature'],
        "humidity": data['humidity'],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Append to data_log.json
    with open(DATA_LOG_FILE, 'r+') as f:
        log = json.load(f)
        log.append(new_entry)
        f.seek(0)
        json.dump(log, f, indent=4)

    # Overwrite latest_data.json
    with open(LATEST_DATA_FILE, 'w') as f:
        json.dump(new_entry, f, indent=4)

    return jsonify({"status": "success", "data": new_entry}), 200


@app.route('/')
def index():
    # Load latest data for display
    with open(LATEST_DATA_FILE, 'r') as f:
        latest_data = json.load(f)
    return render_template("index.html", data=latest_data)


@app.route('/log')
def view_log():
    with open(DATA_LOG_FILE, 'r') as f:
        log = json.load(f)
    return jsonify(log)


@app.route('/latest')
def get_latest_data():
    with open(LATEST_DATA_FILE, 'r') as f:
        latest = json.load(f)
    return jsonify(latest)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=25113)
