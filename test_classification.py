#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

from ollama_service import classify_task

# Test various inputs
test_inputs = [
    "hi",
    "hello",
    "how are you?",
    "search for python tutorials",
    "find information about AI",
    "send email to john@example.com",
    "compose email to sarah with subject meeting",
    "what's the weather like?",
    "tell me a joke"
]

print("Testing classification logic:")
print("=" * 50)

for test_input in test_inputs:
    classification = classify_task(test_input)
    print(f"Input: '{test_input}' -> Classification: {classification}")

print("\n" + "=" * 50)
print("Classification complete.")
