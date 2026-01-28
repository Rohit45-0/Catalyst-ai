import requests
import sys

try:
    # Test root endpoint
    response = requests.get('http://localhost:8000/')
    print(f"✅ Server is running!")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test docs endpoint
    docs_response = requests.get('http://localhost:8000/docs')
    print(f"✅ Swagger UI is accessible!")
    print(f"Docs Status Code: {docs_response.status_code}")
    print()
    
    # Test OpenAPI schema
    openapi_response = requests.get('http://localhost:8000/openapi.json')
    openapi_data = openapi_response.json()
    print(f"✅ OpenAPI Schema loaded!")
    print(f"API Title: {openapi_data.get('info', {}).get('title')}")
    print(f"API Version: {openapi_data.get('info', {}).get('version')}")
    print()
    
    # List all endpoints
    print("📋 Available Endpoints:")
    for path, methods in openapi_data.get('paths', {}).items():
        for method in methods.keys():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                print(f"  {method.upper():6} {path}")
    
    sys.exit(0)
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Cannot connect to server!")
    print("Make sure the server is running on http://localhost:8000")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
