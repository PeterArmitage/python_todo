from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

TASKS_FILE = 'tasks.json'

tasks = []

def load_tasks():
    return tasks

def save_tasks(new_tasks):
    global tasks
    tasks = new_tasks
@app.route('/')
def home():
    return "Todo API is running!"

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        return jsonify(load_tasks())
    elif request.method == 'POST':
        tasks = load_tasks()
        new_task = request.json
        tasks.append(new_task)
        save_tasks(tasks)
        return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id] = request.json
        save_tasks(tasks)
        return jsonify(tasks[task_id])
    return jsonify({"error": "Task not found"}), 404

@app.route('/export', methods=['GET'])
def export_completed():
    tasks = load_tasks()
    completed_tasks = [task for task in tasks if task['completed']]
    if not completed_tasks:
        return jsonify({"message": "No completed tasks to export."})
    
    filename = f"completed_tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write("Completed Tasks:\n\n")
        for task in completed_tasks:
            f.write(f"- {task['text']}\n")
    
    return jsonify({"message": f"Completed tasks exported to {filename}"})

if __name__ == '__main__':
    app.run(debug=True)