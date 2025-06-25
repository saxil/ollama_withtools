#!/usr/bin/env python3
"""
Test script to verify the ollama service functions
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from ollama_service import classify_task, perform_search

def test_classification():
    print("Testing task classification...")
    
    # Test cases
    test_cases = [
        "hi",
        "hello",
        "how are you",
        "search about salman khan",
        "find information about python",
        "send email to john@example.com",
        "compose email"
    ]
    
    for task in test_cases:
        try:
            classification = classify_task(task)
            print(f"'{task}' -> {classification}")
        except Exception as e:
            print(f"'{task}' -> ERROR: {e}")

def test_search():
    print("\nTesting search functionality...")
    
    try:
        results = perform_search("python programming", num_results=2)
        print(f"Search results: {len(results)} found")
        for i, result in enumerate(results[:2], 1):
            if 'error' in result:
                print(f"  {i}. ERROR: {result['error']}")
            else:
                print(f"  {i}. {result['title'][:50]}...")
    except Exception as e:
        print(f"Search ERROR: {e}")

if __name__ == "__main__":
    test_classification()
    test_search()
