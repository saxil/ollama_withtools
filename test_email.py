#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from email_service import send_email_with_env_config
from dotenv import load_dotenv

load_dotenv()

# Test email sending
print("Testing email functionality...")

# Get email credentials from environment
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

print(f"Email address: {email_address}")
print(f"Password configured: {'Yes' if email_password else 'No'}")

# Test sending email using the dedicated email service
success, message = send_email_with_env_config(
    recipient="sahilchanna14@gmail.com",
    subject="Test Email from Neon Nexus AI",
    body="This is a test email to verify the email functionality is working correctly."
)

print(f"Email result: Success={success}, Message={message}")
