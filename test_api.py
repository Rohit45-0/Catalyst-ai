"""
Test script to verify the backend API works correctly with curl-like requests.
This bypasses Swagger UI to test the actual endpoints.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_login():
    """Test login endpoint"""
    print("=" * 60)
    print("TEST 1: Login")
    print("=" * 60)
    
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "barshilerohit1785@gmail.com",
        "password": "Rohit@1785"
    }
    
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"\n✅ Login successful!")
        print(f"Token: {token[:50]}...")
        return token
    else:
        print(f"\n❌ Login failed!")
        return None

def test_create_project(token):
    """Test project creation with authentication"""
    print("\n" + "=" * 60)
    print("TEST 2: Create Project")
    print("=" * 60)
    
    url = f"{BASE_URL}/projects/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "product_name": "Nike Air Max Campaign",
        "brand_name": "Nike",
        "price": "$150",
        "description": "Launch campaign for new Nike Air Max sneakers targeting fitness enthusiasts",
        "campaign_goal": "Increase brand awareness and drive online sales for the new Air Max collection",
        "target_audience": "Fitness enthusiasts, sneaker collectors, and active lifestyle millennials aged 25-40",
        "brand_persona": "Energetic, innovative, and performance-driven. We inspire athletes to push their limits."
    }
    
    response = requests.post(url, headers=headers, data=data)
    print(f"Status Code: {response.status_code}")
    
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    if response.status_code == 201:
        project_id = response.json()["id"]
        print(f"\n✅ Project created successfully!")
        print(f"Project ID: {project_id}")
        return project_id
    else:
        print(f"\n❌ Project creation failed!")
        return None

def test_start_workflow(token, project_id):
    """Test starting the agent workflow"""
    print("\n" + "=" * 60)
    print("TEST 3: Start Agent Workflow")
    print("=" * 60)
    
    url = f"{BASE_URL}/jobs/start/{project_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print(f"\n✅ Workflow started successfully!")
        return True
    else:
        print(f"\n❌ Workflow start failed!")
        return False

def test_check_status(token, project_id):
    """Test checking workflow status"""
    print("\n" + "=" * 60)
    print("TEST 4: Check Workflow Status")
    print("=" * 60)
    
    url = f"{BASE_URL}/jobs/project/{project_id}/status"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print(f"\n✅ Status check successful!")
        return True
    else:
        print(f"\n❌ Status check failed!")
        return False

if __name__ == "__main__":
    print("\n🚀 Starting Backend API Tests\n")
    
    # Test 1: Login
    token = test_login()
    if not token:
        print("\n❌ Cannot proceed without valid token. Exiting.")
        exit(1)
    
    # Test 2: Create Project
    project_id = test_create_project(token)
    if not project_id:
        print("\n❌ Cannot proceed without project. Exiting.")
        exit(1)
    
    # Test 3: Start Workflow
    workflow_started = test_start_workflow(token, project_id)
    
    # Test 4: Check Status
    if workflow_started:
        test_check_status(token, project_id)
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60)
    print(f"\nProject ID: {project_id}")
    print(f"You can now check assets at: {BASE_URL}/projects/{project_id}/assets")
    print("\nNote: Agent workflow takes 2-5 minutes to complete.")
    print("Check status periodically using TEST 4 endpoint.")
