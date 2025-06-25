#!/usr/bin/env python3
"""
Setup script for Neon Nexus AI
Helps configure email and other services
"""

import os
import getpass

def setup_email():
    print("🔧 Email Configuration Setup")
    print("=" * 40)
    
    print("\nFor Gmail users:")
    print("1. Enable 2-factor authentication on your Google account")
    print("2. Go to Google Account settings > Security > App passwords")
    print("3. Generate a new app password")
    print("4. Use that app password (not your regular password)")
    
    email = input("\nEnter your email address: ").strip()
    password = getpass.getpass("Enter your app password: ").strip()
    
    # Create .env file
    env_content = f"""# Email Configuration
EMAIL_ADDRESS={email}
EMAIL_PASSWORD={password}

# SMTP Configuration (Gmail default)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Email configuration saved to .env file")
    print("🚀 You can now send emails through the chat interface!")

def main():
    print("🌟 Welcome to Neon Nexus AI Setup!")
    print("=" * 50)
    
    print("\nAvailable setup options:")
    print("1. Configure Email Service")
    print("2. Exit")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == '1':
        setup_email()
    elif choice == '2':
        print("👋 Setup cancelled")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
