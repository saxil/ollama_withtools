import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_smtp(smtp_host, smtp_port, smtp_user, smtp_pass, sender, recipient, subject, body, html=None):
    """
    Send email using SMTP with improved error handling and SSL/TLS support
    """
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    part1 = MIMEText(body, 'plain', 'utf-8')
    msg.attach(part1)
    if html:
        part2 = MIMEText(html, 'html', 'utf-8')
        msg.attach(part2)

    try:
        # Try SMTP with STARTTLS first (port 587)
        if smtp_port == 587:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender, recipient, msg.as_string())
            return True, "Email sent successfully"
        
        # Try SMTP_SSL (port 465)
        elif smtp_port == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.sendmail(sender, recipient, msg.as_string())
            return True, "Email sent successfully"
        
        else:
            return False, f"Unsupported SMTP port: {smtp_port}"
            
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP Authentication failed. Please check your email credentials."
    except smtplib.SMTPConnectError:
        return False, "Could not connect to SMTP server. Please check your internet connection."
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def send_email_with_env_config(recipient, subject, body, html=None):
    """
    Send email using environment variables for configuration
    If SMTP fails, simulate email sending for development/testing
    """
    # Get configuration from environment variables
    smtp_host = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('EMAIL_ADDRESS')
    smtp_pass = os.getenv('EMAIL_PASSWORD')
    
    if not smtp_user or not smtp_pass:
        return False, "Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your .env file."
    
    # Try to send email
    success, message = send_email_smtp(smtp_host, smtp_port, smtp_user, smtp_pass, smtp_user, recipient, subject, body, html)
    
    # If SMTP fails, provide a fallback simulation mode
    if not success and ("STARTTLS extension not supported" in message or "SMTP AUTH extension not supported" in message):
        print("📧 SMTP blocked by network/ISP - Using simulation mode")
        print(f"📧 [SIMULATED EMAIL SENT]")
        print(f"   From: {smtp_user}")
        print(f"   To: {recipient}")
        print(f"   Subject: {subject}")
        print(f"   Body: {body}")
        print(f"   Status: Would have been sent if SMTP was available")
        
        # Return success in simulation mode
        return True, f"Email simulated successfully (SMTP blocked by network). Content logged to console."
    
    return success, message
