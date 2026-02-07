#!/usr/bin/env python3
"""
Simple test script for the Overleaf MCP API.
Tests both local and remote deployments.
"""

import sys
import requests
import json

def test_api(base_url: str, api_key: str = None):
    """Test the API endpoints."""
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    print(f"Testing API at: {base_url}\n")
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Projects configured: {data.get('projects_configured')}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print()
    
    # Test 2: List projects
    print("2. Testing list projects...")
    try:
        response = requests.get(f"{base_url}/projects")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ List projects passed")
            print(f"   Result preview: {data.get('result', '')[:100]}...")
        else:
            print(f"   ✗ List projects failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 3: List files (requires auth if API_KEY is set)
    print("3. Testing list files...")
    try:
        payload = {"arguments": {}}
        response = requests.post(
            f"{base_url}/files/list",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ List files passed")
            print(f"   Result preview: {data.get('result', '')[:100]}...")
        elif response.status_code == 401:
            print(f"   ⚠ Authentication required (this is expected if API_KEY is set)")
        else:
            print(f"   ✗ List files failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    
    # Test 4: Read file (if we know a file exists)
    print("4. Testing read file (main.tex)...")
    try:
        payload = {"arguments": {"file_path": "main.tex"}}
        response = requests.post(
            f"{base_url}/files/read",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Read file passed")
            result = data.get('result', '')
            if len(result) > 100:
                print(f"   Content preview: {result[:100]}...")
            else:
                print(f"   Content: {result}")
        elif response.status_code == 401:
            print(f"   ⚠ Authentication required")
        else:
            print(f"   ⚠ File might not exist or other error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print()
    print("=" * 60)
    print("Testing complete!")
    print()
    print("Next steps:")
    print("- If tests passed: Your API is working!")
    print("- If auth errors: Set API_KEY environment variable")
    print("- If file errors: Check your Overleaf project configuration")
    print()
    
    return True


if __name__ == "__main__":
    # Default to localhost
    base_url = "http://localhost:8000"
    api_key = None
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    if len(sys.argv) > 2:
        api_key = sys.argv[2]
    
    # Check for API key in environment
    import os
    if not api_key:
        api_key = os.environ.get("API_KEY")
    
    print("=" * 60)
    print("Overleaf MCP API Test Script")
    print("=" * 60)
    print()
    
    if api_key:
        print(f"Using API key: {api_key[:10]}...")
    else:
        print("No API key provided (testing public endpoints only)")
    
    print()
    
    test_api(base_url, api_key)
