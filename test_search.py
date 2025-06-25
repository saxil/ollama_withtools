#!/usr/bin/env python3
"""
Test script to verify the search functionality
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from ollama_service import perform_search

def test_search():
    print("Testing search functionality...")
    
    # Test search
    query = "Salman Khan actor"
    print(f"Searching for: {query}")
    
    results = perform_search(query, num_results=3)
    
    if results:
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            if 'error' in result:
                print(f"Error: {result['error']}")
            else:
                print(f"\n{i}. {result['title']}")
                print(f"   URL: {result['url']}")
                print(f"   Snippet: {result['snippet']}")
    else:
        print("No results found")

if __name__ == "__main__":
    test_search()
