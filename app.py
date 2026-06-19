"""
Web Application for AI Data Analyst Agent
Flask-based web interface with beautiful chat UI.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from agent import DataAnalystAgent

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global agent instance
agent = None


def get_agent():
    """Get or create the agent instance."""
    global agent
    if agent is None:
        agent = DataAnalystAgent()
    return agent


@app.route('/')
def index():
    """Serve the main page."""
    return send_from_directory('.', 'index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        a = get_agent()
        summary = a.load_data(filepath)
        return jsonify({'summary': summary, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/load-sample', methods=['POST'])
def load_sample():
    """Load the built-in sample dataset."""
    sample_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'sales_data.csv')
    if not os.path.exists(sample_path):
        return jsonify({'error': 'Sample data not found'}), 404

    try:
        a = get_agent()
        summary = a.load_data(sample_path)
        return jsonify({'summary': summary, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle user questions."""
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'Empty question'}), 400

    try:
        a = get_agent()
        result = a.ask(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print('\n🚀 AI Data Analyst Agent - Web Interface')
    print('   Open http://localhost:5000 in your browser\n')
    app.run(debug=True, port=5000)
