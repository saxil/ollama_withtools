from services.email_service import send_email_smtp
from services.search_service import google_search
from services.telegram_service import TelegramBot
from services.ollama_service import classify_task, generate_chat_response,extract_email_details

# Configure your SMTP and Telegram credentials here
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "lucifer.ai.288@gmail.com"
SMTP_PASS = "mfbjcjevynjezpaz"
SENDER_EMAIL = SMTP_USER

TELEGRAM_TOKEN = "7834559734:AAHs3dNqnDSFCMRVy8uzPLHreTo0GAO2mJQ"

def process_task(task):
    classification = classify_task(task)
    
    if "EMAIL" in classification:
        details = extract_email_details(task)
        if details and all(k in details for k in ("recipient", "subject", "body")):
            success, msg = send_email_smtp(
                SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS,
                SENDER_EMAIL, details['recipient'], details['subject'], details['body']
            )
            return msg  # Return success/failure message, NOT the email content
        else:
            return "❌ Failed to extract email details from your message."
    
    elif "SEARCH" in classification:
        results = google_search(task, num_results=3)
        return "Top search results:\n" + "\n".join(results)
    
    else:
        return generate_chat_response(task)

def main():
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.start(process_task)

if __name__ == "__main__":
    main()
