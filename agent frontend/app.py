"""Simple Flask web server for Agent Micheal dashboard."""
from flask import Flask, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

# Path to messages file from agent_micheal
MESSAGES_FILE = r"c:\Users\Admin\OneDrive\Desktop\agent micheal\agent_micheal\messages.json"

@app.route('/')
def dashboard():
    """Serve the dashboard."""
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/api/status')
def get_status():
    """Get channel status."""
    return jsonify({
        'email': {'status': 'online', 'last_check': datetime.now().isoformat()},
        'telegram': {'status': 'offline', 'reason': 'Not configured'},
        'whatsapp': {'status': 'offline', 'reason': 'Not configured'},
        'linkedin': {'status': 'offline', 'reason': 'Stub implementation'},
        'instagram': {'status': 'offline', 'reason': 'Stub implementation'}
    })

@app.route('/api/messages')
def get_messages():
    """Get recent messages."""
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r') as f:
                messages = json.load(f)
            # Return last 10 messages, sorted by time
            return jsonify(sorted(messages, key=lambda x: x.get('received_at', ''), reverse=True)[:10])
        else:
            return jsonify([])
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)