#!/usr/bin/env python3

import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

print(f"Testing SMTP connection...")
print(f"Email: {email_address}")
print(f"Password configured: {'Yes' if email_password else 'No'}")

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    print("✅ Connected to SMTP server")
    
    server.ehlo()
    print("✅ EHLO successful")
    
    server.starttls()
    print("✅ STARTTLS successful")
    
    server.ehlo()
    print("✅ Second EHLO successful")
    
    server.login(email_address, email_password)
    print("✅ Login successful")
    
    server.quit()
    print("✅ Connection closed successfully")
    
    print("\n🎉 All tests passed! Email configuration is working.")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\n💡 Troubleshooting tips:")
    print("1. Make sure you're using an App Password, not your regular Gmail password")
    print("2. Enable 2-Factor Authentication on your Gmail account")
    print("3. Generate an App Password in your Google Account settings")
    print("4. Make sure 'Less secure app access' is enabled (if using regular password)")
