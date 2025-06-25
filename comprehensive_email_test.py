#!/usr/bin/env python3

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

print(f"Testing multiple SMTP methods...")
print(f"Email: {email_address}")
print(f"Password configured: {'Yes' if email_password else 'No'}")

def test_method_1_starttls():
    print("\n🔧 Method 1: SMTP with STARTTLS (Port 587)")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debug output
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email_address, email_password)
        
        # Send test email
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = "sahilchanna14@gmail.com"
        msg['Subject'] = "Test Email - Method 1 (STARTTLS)"
        msg.attach(MIMEText("This is a test email using STARTTLS method.", 'plain'))
        
        server.sendmail(email_address, "sahilchanna14@gmail.com", msg.as_string())
        server.quit()
        
        print("✅ Method 1 successful!")
        return True
        
    except Exception as e:
        print(f"❌ Method 1 failed: {str(e)}")
        return False

def test_method_2_ssl():
    print("\n🔧 Method 2: SMTP_SSL (Port 465)")
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        server.set_debuglevel(1)  # Enable debug output
        server.ehlo()
        server.login(email_address, email_password)
        
        # Send test email
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = "sahilchanna14@gmail.com"
        msg['Subject'] = "Test Email - Method 2 (SSL)"
        msg.attach(MIMEText("This is a test email using SSL method.", 'plain'))
        
        server.sendmail(email_address, "sahilchanna14@gmail.com", msg.as_string())
        server.quit()
        
        print("✅ Method 2 successful!")
        return True
        
    except Exception as e:
        print(f"❌ Method 2 failed: {str(e)}")
        return False

def test_method_3_basic():
    print("\n🔧 Method 3: Basic SMTP (Port 25)")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 25)
        server.set_debuglevel(1)  # Enable debug output
        server.ehlo()
        server.login(email_address, email_password)
        
        # Send test email
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = "sahilchanna14@gmail.com"
        msg['Subject'] = "Test Email - Method 3 (Basic)"
        msg.attach(MIMEText("This is a test email using basic SMTP method.", 'plain'))
        
        server.sendmail(email_address, "sahilchanna14@gmail.com", msg.as_string())
        server.quit()
        
        print("✅ Method 3 successful!")
        return True
        
    except Exception as e:
        print(f"❌ Method 3 failed: {str(e)}")
        return False

# Test all methods
methods = [test_method_1_starttls, test_method_2_ssl, test_method_3_basic]
success = False

for method in methods:
    if method():
        success = True
        break

if not success:
    print("\n❌ All methods failed!")
    print("\n💡 Troubleshooting suggestions:")
    print("1. The app password might be expired - generate a new one")
    print("2. Check if 2FA is enabled on the Gmail account")
    print("3. Try using a different email provider (Outlook, Yahoo)")
    print("4. Check if your ISP is blocking SMTP ports")
    print("5. Try from a different network connection")
else:
    print("\n🎉 Email sending is working!")
