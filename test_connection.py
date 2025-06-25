#!/usr/bin/env python3

import socket
import ssl

def test_smtp_connection():
    print("Testing SMTP connections...")
    
    # Test port 587 (STARTTLS)
    print("\n1. Testing SMTP port 587 (STARTTLS):")
    try:
        with socket.create_connection(('smtp.gmail.com', 587), timeout=10) as sock:
            print("   ✅ Connection successful")
            response = sock.recv(1024).decode()
            print(f"   Server response: {response.strip()}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    # Test port 465 (SSL)
    print("\n2. Testing SMTP port 465 (SSL):")
    try:
        context = ssl.create_default_context()
        with socket.create_connection(('smtp.gmail.com', 465), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname='smtp.gmail.com') as ssock:
                print("   ✅ SSL connection successful")
                response = ssock.recv(1024).decode()
                print(f"   Server response: {response.strip()}")
    except Exception as e:
        print(f"   ❌ SSL connection failed: {e}")

if __name__ == "__main__":
    test_smtp_connection()
