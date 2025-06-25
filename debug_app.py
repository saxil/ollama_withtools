#!/usr/bin/env python3
"""
Debug version of Flask app to diagnose issues
"""
from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        print(f"DEBUG: Received message: '{user_message}'")
        
        # Simple classification for debugging
        user_message_lower = user_message.lower()
        
        if any(keyword in user_message_lower for keyword in ['email', 'send email', '@']):
            task_type = 'EMAIL'
            response = "📧 **Email Classification Test** - This would handle email requests"
        elif any(keyword in user_message_lower for keyword in ['search', 'find', 'look for']):
            task_type = 'SEARCH'
            response = "🔍 **Search Classification Test** - This would perform real search"
        else:
            task_type = 'CHAT'
            response = f"💬 **Chat Response** - Hello! You said: '{user_message}'. This is working correctly now!"
        
        print(f"DEBUG: Classified as: {task_type}")
        
        return jsonify({
            'response': response,
            'task_type': task_type
        })
    
    except Exception as e:
        print(f"DEBUG: Error occurred: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting debug Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
