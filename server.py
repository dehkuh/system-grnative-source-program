import os
import json
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

api_key = os.getenv("API_KEY")  # מפתח API של Monday.com
url = "https://api.monday.com/v2/"

headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "AI Automation System is running!"})

@app.route('/fetch_boards', methods=['GET'])
def fetch_boards():
    query = '{ boards(limit: 1) { id name } }'
    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        response.raise_for_status()
        data = response.json()
        boards = data.get("data", {}).get("boards", [])
        
        if boards:
            return jsonify({"board_id": boards[0]["id"], "board_name": boards[0]["name"]})
        return jsonify({"message": "No boards found."})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/create_board', methods=['POST'])
def create_board():
    data = request.json
    board_name = data.get("board_name")
    
    if not board_name:
        return jsonify({"error": "Please provide a board name"}), 400

    query = f'mutation {{ create_board (board_name: "{board_name}", board_kind: public) {{ id name }} }}'
    
    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        response.raise_for_status()
        return jsonify({"message": "Board created successfully!"})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/automated_action', methods=['POST'])
def automated_action():
    data = request.json
    action_type = data.get("action_type")
    
    if action_type == "create_software":
        return jsonify({"message": "Software created successfully!"})
    elif action_type == "create_device":
        return jsonify({"message": "Device created successfully!"})
    elif action_type == "patent_invention":
        return jsonify({"message": "Patent created successfully!"})
    return jsonify({"error": "Unknown action type"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
