#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from ollama_service import classify_task, generate_chat_response, compose_and_send_email, perform_search

def test_ai_functions():
    """Test all AI functions without Telegram bot"""
    
    print("🧪 Testing AI Functions\n")
    
    # Test 1: Chat classification
    print("1. Testing Classification:")
    test_inputs = [
        "hi",
        "hello how are you",
        "search for python tutorials", 
        "send email to john@example.com about meeting tomorrow"
    ]
    
    for inp in test_inputs:
        classification = classify_task(inp)
        print(f"   '{inp}' → {classification}")
    
    # Test 2: Chat response
    print("\n2. Testing Chat Response:")
    try:
        response = generate_chat_response("Tell me a joke")
        print(f"   Chat response: {response[:100]}...")
    except Exception as e:
        print(f"   ❌ Chat failed: {e}")
    
    # Test 3: Email composition
    print("\n3. Testing Email Composition:")
    try:
        email_task = "send email to sahilchanna14@gmail.com with subject 'Test from AI' and tell them about our new AI system"
        result = compose_and_send_email(email_task)
        print(f"   Email result: Success={result['success']}")
        if 'details' in result:
            details = result['details']
            print(f"   To: {details.get('recipient', 'N/A')}")
            print(f"   Subject: {details.get('subject', 'N/A')}")
            print(f"   Body: {details.get('body', 'N/A')[:50]}...")
    except Exception as e:
        print(f"   ❌ Email failed: {e}")
    
    # Test 4: Search
    print("\n4. Testing Search:")
    try:
        search_results = perform_search("Python programming tutorial", num_results=2)
        if search_results and 'error' not in search_results[0]:
            print(f"   Search found {len(search_results)} results")
            for i, result in enumerate(search_results, 1):
                print(f"   {i}. {result['title'][:50]}...")
                print(f"      {result['url']}")
        else:
            error_msg = search_results[0].get('error', 'Unknown error') if search_results else 'No results'
            print(f"   ❌ Search failed: {error_msg}")
    except Exception as e:
        print(f"   ❌ Search failed: {e}")
    
    print("\n✅ AI Function testing complete!")

if __name__ == "__main__":
    test_ai_functions()
