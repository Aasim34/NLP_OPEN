"""
Test script for optimized Hindi conversion pipeline
Tests natural Hindi replacements and improved translation
"""

import requests
import json

# Test cases
test_cases = [
    {
        "name": "Natural Hindi - rest lena",
        "input": "tumhe thoda rest lena chahiye",
        "expected_hindi_contains": "आराम",
        "expected_english_contains": "rest"
    },
    {
        "name": "Natural Hindi - meeting office",
        "input": "kal meeting hai office me",
        "expected_hindi_contains": "बैठक",
        "expected_english_contains": "meeting"
    },
    {
        "name": "Natural Hindi - exam preparation",
        "input": "kal exam hai tayari kar lena",
        "expected_hindi_contains": "परीक्षा",
        "expected_english_contains": "exam"
    },
    {
        "name": "Original test case",
        "input": "hello bhai kaise ho",
        "expected_hindi_contains": "भाई",
        "expected_english_contains": "brother"
    },
]

API_URL = "http://127.0.0.1:8000/convert"

print("\n" + "="*80)
print("TESTING OPTIMIZED PIPELINE")
print("="*80 + "\n")

for i, test in enumerate(test_cases, 1):
    print(f"Test {i}: {test['name']}")
    print(f"Input: {test['input']}")
    print("-" * 80)
    
    try:
        response = requests.post(API_URL, json={"text": test["input"]})
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✓ Hindi:    {data['hindi']}")
            print(f"✓ Finglish: {data['finglish']}")
            print(f"✓ English:  {data['english']}")
            
            # Verify expectations
            if test['expected_hindi_contains'] in data['hindi']:
                print(f"  ✓ Hindi contains '{test['expected_hindi_contains']}'")
            else:
                print(f"  ✗ Hindi missing '{test['expected_hindi_contains']}'")
            
        else:
            print(f"✗ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n")

print("="*80)
print("Testing complete!")
print("="*80 + "\n")
