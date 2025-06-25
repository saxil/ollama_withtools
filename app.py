from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from ollama_service import classify_task, extract_email_details, generate_chat_response, perform_search, compose_and_send_email

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
        
        # Classify the task first
        task_type = classify_task(user_message)
        
        if 'EMAIL' in task_type:
            # Try to compose and send email
            email_result = compose_and_send_email(user_message)
            
            if email_result['success']:
                details = email_result['details']
                response = f"""📧 **Email Sent Successfully!**
                
**To:** {details.get('recipient', 'N/A')}
**Subject:** {details.get('subject', 'N/A')}
**Body:** {details.get('body', 'N/A')}

✅ {email_result['message']}

Your email has been sent successfully!"""
            else:
                if 'details' in email_result:
                    details = email_result['details']
                    response = f"""📧 **Email Composed but Not Sent**
                    
**To:** {details.get('recipient', 'N/A')}
**Subject:** {details.get('subject', 'N/A')}
**Body:** {details.get('body', 'N/A')}

❌ **Error:** {email_result['error']}

*Note: To enable email sending, please configure your email credentials in environment variables.*"""
                else:
                    response = f"❌ **Email Error:** {email_result['error']}\n\nPlease provide the recipient, subject, and message content clearly."
        
        elif 'SEARCH' in task_type:
            # Perform actual search
            search_results = perform_search(user_message, num_results=3)
            
            if search_results and 'error' not in search_results[0]:
                response = f"🔍 **Search Results for '{user_message}':**\n\n"
                
                for i, result in enumerate(search_results, 1):
                    response += f"**{i}. {result['title']}**\n"
                    response += f"🌐 {result['url']}\n"
                    response += f"📝 {result['snippet']}\n\n"
                
                response += "Click on any link above to visit the website for more details."
            else:
                error_msg = search_results[0].get('error', 'Unknown error') if search_results else 'No results found'
                response = f"🔍 **Search Error**\n\nSorry, I couldn't perform the search for '{user_message}'. Error: {error_msg}"
        
        else:
            # Generate chat response
            response = generate_chat_response(user_message)
        
        return jsonify({
            'response': response,
            'task_type': task_type
        })
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
