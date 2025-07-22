from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = 'todos.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(load_data())

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    todos = load_data()
    todos.append(data)
    save_data(todos)
    return jsonify({'message': 'Todo added'}), 201

@app.route('/todos/<int:index>', methods=['DELETE'])
def delete_todo(index):
    todos = load_data()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_data(todos)
        return jsonify({'message': 'Deleted'}), 200
    return jsonify({'error': 'Index out of range'}), 404

if __name__ == '__main__':
    app.run(debug=True)