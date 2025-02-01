from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# Agent orchestration routes
@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get list of available agents"""
    try:
        agents = [
            {"id": 1, "name": "Assistant", "type": "default"},
            {"id": 2, "name": "Code Assistant", "type": "coder"},
            {"id": 3, "name": "Product Manager", "type": "pm"}
        ]
        return jsonify({"agents": agents})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def start_chat():
    """Start or continue a chat session"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        agent_id = data.get('agent_id')
        
        # TODO: Implement actual agent chat logic
        response = {
            "message": f"Agent {agent_id} received: {message}",
            "agent_id": agent_id
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get list of running tasks"""
    try:
        tasks = [
            {"id": 1, "name": "Code Review", "status": "running"},
            {"id": 2, "name": "Documentation", "status": "completed"}
        ]
        return jsonify({"tasks": tasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        task_name = data.get('name', '')
        # TODO: Implement actual task creation logic
        new_task = {
            "id": 3,
            "name": task_name,
            "status": "created"
        }
        return jsonify(new_task)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/filesystem', methods=['GET'])
def list_files():
    """List files in workspace"""
    try:
        # TODO: Implement actual filesystem operations
        files = [
            {"name": "main.py", "type": "file"},
            {"name": "data", "type": "directory"}
        ]
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)