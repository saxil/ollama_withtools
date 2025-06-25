from services.telegram_service import TelegramBot
from services.ollama_service import classify_task, generate_chat_response, compose_and_send_email, perform_search

# Configure your Telegram credentials here
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

def process_task(task):
    classification = classify_task(task)
    print(f"[DEBUG] Task: '{task}' -> Classification: {classification}")
    
    if "EMAIL" in classification:
        email_result = compose_and_send_email(task)
        
        if email_result['success']:
            details = email_result['details']
            return f"📧 Email sent successfully!\nTo: {details.get('recipient', 'N/A')}\nSubject: {details.get('subject', 'N/A')}\nBody: {details.get('body', 'N/A')}"
        else:
            if 'details' in email_result:
                details = email_result['details']
                return f"📧 Email composed but not sent:\nTo: {details.get('recipient', 'N/A')}\nSubject: {details.get('subject', 'N/A')}\nBody: {details.get('body', 'N/A')}\n\nError: {email_result['error']}"
            else:
                return f"❌ Email Error: {email_result['error']}"
    
    elif "SEARCH" in classification:
        search_results = perform_search(task, num_results=3)
        
        if search_results and 'error' not in search_results[0]:
            response = f"🔍 Search Results for '{task}':\n\n"
            for i, result in enumerate(search_results, 1):
                response += f"{i}. {result['title']}\n{result['url']}\n{result['snippet']}\n\n"
            return response
        else:
            error_msg = search_results[0].get('error', 'Unknown error') if search_results else 'No results found'
            return f"🔍 Search Error: {error_msg}"
    
    else:
        return generate_chat_response(task)

def main():
    if not TELEGRAM_TOKEN:
        print("❌ Error: TELEGRAM_TOKEN not found in environment variables.")
        print("Please check your .env file and make sure TELEGRAM_TOKEN is set.")
        return
    
    print("🤖 Starting Neon Nexus AI Bot...")
    print("📱 Telegram Bot is running. Send messages to interact!")
    
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.start(process_task)

if __name__ == "__main__":
    main()
