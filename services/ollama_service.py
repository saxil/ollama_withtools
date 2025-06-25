import ollama
import re, json
import requests
from googlesearch import search
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def classify_task(task):
    # Simple rule-based classification first
    task_lower = task.lower()
    
    # Email keywords
    email_keywords = ['email', 'send email', 'compose email', 'write email', 'mail to', '@', 'send to', 'compose']
    
    # Search keywords  
    search_keywords = ['search', 'find', 'look for', 'search for', 'google', 'lookup', 'find information']
    
    # Check for email patterns
    if any(keyword in task_lower for keyword in email_keywords) or '@' in task:
        return 'EMAIL'
    
    # Check for search patterns
    if any(keyword in task_lower for keyword in search_keywords):
        return 'SEARCH'
    
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
    except:
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
        
        # Get search results from Google (fix the parameter issue)
        search_urls = list(search(query, num_results=num_results, stop=num_results, pause=2))
        
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

def send_email(recipient, subject, body, sender_email=None, sender_password=None):
    """
    Send an email using SMTP
    """
    try:
        # Email configuration - you'll need to set these
        if not sender_email:
            sender_email = os.getenv('EMAIL_ADDRESS', 'your-email@gmail.com')
        if not sender_password:
            sender_password = os.getenv('EMAIL_PASSWORD', 'your-app-password')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        
        return {
            'success': True,
            'message': f'Email sent successfully to {recipient}'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to send email: {str(e)}'
        }

def compose_and_send_email(task):
    """
    Extract email details and send the email
    """
    # First extract the email details
    email_details = extract_email_details(task)
    
    if not email_details:
        return {
            'success': False,
            'error': 'Could not extract email details from your request'
        }
    
    # Send the email
    result = send_email(
        recipient=email_details['recipient'],
        subject=email_details['subject'],
        body=email_details['body']
    )
    
    if result['success']:
        return {
            'success': True,
            'details': email_details,
            'message': result['message']
        }
    else:
        return {
            'success': False,
            'details': email_details,
            'error': result['error']
        }
