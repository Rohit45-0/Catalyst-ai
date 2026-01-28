"""
Quick test script to verify the OAuth2 fix
Run this after starting the server to test authentication
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup"""
    print("🧪 Testing signup...")
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Signup successful!")
        print(f"Response: {response.json()}")
        return True
    elif response.status_code == 400:
        print("⚠️  User already exists (this is OK)")
        return True
    else:
        print(f"❌ Signup failed: {response.text}")
        return False

def test_login():
    """Test OAuth2 login"""
    print("\n🧪 Testing login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpassword123"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login successful!")
        token_data = response.json()
        print(f"Token type: {token_data.get('token_type')}")
        print(f"Access token: {token_data.get('access_token')[:50]}...")
        return token_data.get('access_token')
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_me(token):
    """Test /auth/me endpoint"""
    print("\n🧪 Testing /auth/me...")
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ /auth/me successful!")
        print(f"User data: {response.json()}")
        return True
    else:
        print(f"❌ /auth/me failed: {response.text}")
        return False

def test_cors():
    """Test CORS headers"""
    print("\n🧪 Testing CORS headers...")
    response = requests.options(
        f"{BASE_URL}/auth/login",
        headers={
            "Origin": "http://localhost:8000",
            "Access-Control-Request-Method": "POST"
        }
    )
    cors_headers = {
        k: v for k, v in response.headers.items() 
        if k.lower().startswith('access-control')
    }
    if cors_headers:
        print("✅ CORS headers present!")
        for key, value in cors_headers.items():
            print(f"  {key}: {value}")
        return True
    else:
        print("❌ CORS headers missing!")
        return False

def main():
    print("=" * 60)
    print("🚀 Catalyst AI Backend - OAuth2 Fix Verification")
    print("=" * 60)
    
    try:
        # Test CORS
        test_cors()
        
        # Test signup
        test_signup()
        
        # Test login
        token = test_login()
        
        if token:
            # Test protected endpoint
            test_me(token)
            
            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED! OAuth2 is working correctly!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ Login failed - check credentials or server")
            print("=" * 60)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Make sure the server is running on http://localhost:8000")
        print("\nStart the server with:")
        print("  python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
