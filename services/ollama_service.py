import ollama
import re, json
import requests
from googlesearch import search
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def classify_task(task):
    # Simple rule-based classification first
    task_lower = task.lower().strip()
    
    # Email keywords - need to be specific to avoid false matches
    email_keywords = ['send email', 'compose email', 'write email', 'mail to', 'send to', 'email to']
    
    # Search keywords - need to be specific to avoid false matches
    search_keywords = ['search for', 'find information', 'look for', 'google', 'lookup', 'search']
    
    # Check for email patterns
    if any(keyword in task_lower for keyword in email_keywords) or '@' in task:
        return 'EMAIL'
    
    # Check for search patterns - be more specific
    if any(keyword in task_lower for keyword in search_keywords):
        return 'SEARCH'
    
    # For simple greetings and conversational inputs, return CHAT immediately
    chat_keywords = ['hi', 'hello', 'hey', 'how are you', 'what\'s up', 'good morning', 'good afternoon', 'good evening']
    if any(keyword in task_lower for keyword in chat_keywords) or len(task_lower) <= 3:
        return 'CHAT'
    
    # For everything else, use AI classification as backup
    try:
        response = ollama.chat(
            model='Jarvis',
            messages=[{'role': 'user', 'content': f"Classify this task into exactly one category: {task}. Respond with only: EMAIL, SEARCH, or CHAT"}]
        )
        classification = response['message']['content'].upper().strip()
        
        # Ensure it's one of our valid options
        if classification in ['EMAIL', 'SEARCH', 'CHAT']:
            return classification
        else:
            return 'CHAT'  # Default to chat
    except Exception as e:
        return 'CHAT'  # Default fallback

def extract_email_details(task):
    prompt = f"""
    Extract email details from the following request and return them in JSON format:
    
    Request: {task}
    
    Please extract:
    - recipient: email address or name of the recipient
    - subject: email subject line
    - body: email message content
    
    Return only valid JSON in this format:
    {{
        "recipient": "email or name",
        "subject": "subject line",
        "body": "email content"
    }}
    """

    response = ollama.chat(
        model='Jarvis',
        messages=[{'role': 'user', 'content': prompt}]
    )
    text = response['message']['content']

    # Extract JSON substring using regex
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if not json_match:
        return None

    json_str = json_match.group()
    try:
        details = json.loads(json_str)
        # Validate keys exist
        if all(k in details for k in ("recipient", "subject", "body")):
            return details
    except json.JSONDecodeError:
        return None

    return None

def generate_chat_response(task):
    response = ollama.chat(
        model='Jarvis',
        messages=[{'role': 'user', 'content': task}]
    )
    return response['message']['content']

def perform_search(query, num_results=5):
    """
    Perform a Google search and return results with summaries
    """
    try:
        search_results = []
        
        # Get search results from Google (remove pause parameter)
        search_urls = list(search(query, num_results=num_results))
        
        for i, url in enumerate(search_urls[:num_results]):
            try:
                # Try to get page title and snippet
                response = requests.get(url, timeout=5, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                # Extract title from HTML (simple approach)
                title_start = response.text.find('<title>')
                title_end = response.text.find('</title>')
                title = "No title"
                if title_start != -1 and title_end != -1:
                    title = response.text[title_start + 7:title_end].strip()
                
                search_results.append({
                    'title': title,
                    'url': url,
                    'snippet': f"Search result {i+1} for '{query}'"
                })
                
            except Exception as e:
                # If we can't fetch the page, still include the URL
                search_results.append({
                    'title': f"Search Result {i+1}",
                    'url': url,
                    'snippet': f"Result {i+1} for '{query}'"
                })
        
        return search_results
        
    except Exception as e:
        return [{'error': f"Search failed: {str(e)}"}]

def compose_and_send_email(task):
    """
    Extract email details and send the email using the dedicated email service
    """
    from email_service import send_email_with_env_config
    
    # First extract the email details
    email_details = extract_email_details(task)
    
    if not email_details:
        return {
            'success': False,
            'error': 'Could not extract email details from your request'
        }
    
    # Send the email using the dedicated email service
    success, message = send_email_with_env_config(
        recipient=email_details['recipient'],
        subject=email_details['subject'],
        body=email_details['body']
    )
    
    if success:
        return {
            'success': True,
            'details': email_details,
            'message': message
        }
    else:
        return {
            'success': False,
            'details': email_details,
            'error': message
        }
