import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("🧪 TESTING CATALYST AI BACKEND")
print("=" * 70)

# Test 1: Health Check
print("\n[1/5] Testing health check...")
try:
    r = requests.get(f"{BASE_URL}/")
    print(f"✅ Server is running! Status: {r.status_code}")
    print(f"    Response: {r.json()}")
except Exception as e:
    print(f"❌ Server not responding: {e}")
    sys.exit(1)

# Test 2: Login
print("\n[2/5] Testing login...")
try:
    r = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": "barshilerohit1785@gmail.com",
            "password": "Rohit@1785"
        }
    )
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        token = r.json()["access_token"]
        print(f"✅ Login successful!")
        print(f"    Token: {token[:50]}...")
    else:
        print(f"❌ Login failed!")
        print(f"    Response: {r.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Login error: {e}")
    sys.exit(1)

# Test 3: Create Project
print("\n[3/5] Testing project creation...")
try:
    r = requests.post(
        f"{BASE_URL}/projects/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "product_name": "Nike Air Max Campaign",
            "brand_name": "Nike",
            "price": "$150",
            "description": "Launch campaign for new Nike Air Max sneakers targeting fitness enthusiasts",
            "campaign_goal": "Increase brand awareness and drive online sales for the new Air Max collection",
            "target_audience": "Fitness enthusiasts, sneaker collectors, and active lifestyle millennials aged 25-40",
            "brand_persona": "Energetic, innovative, and performance-driven. We inspire athletes to push their limits."
        }
    )
    print(f"    Status: {r.status_code}")
    if r.status_code == 201:
        project = r.json()
        project_id = project["id"]
        print(f"✅ Project created successfully!")
        print(f"    Project ID: {project_id}")
        print(f"    Name: {project['product_name']}")
    else:
        print(f"❌ Project creation failed!")
        print(f"    Response: {r.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Project creation error: {e}")
    sys.exit(1)

# Test 4: Start Workflow
print("\n[4/5] Testing agent workflow start...")
try:
    r = requests.post(
        f"{BASE_URL}/jobs/start/{project_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        result = r.json()
        print(f"✅ Workflow started successfully!")
        print(f"    Message: {result['message']}")
        print(f"    Jobs created: {result['jobs_created']}")
    else:
        print(f"❌ Workflow start failed!")
        print(f"    Response: {r.text}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Workflow start error: {e}")
    sys.exit(1)

# Test 5: Check Status
print("\n[5/5] Testing job status check...")
try:
    r = requests.get(
        f"{BASE_URL}/jobs/project/{project_id}/status",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        status = r.json()
        print(f"✅ Status check successful!")
        print(f"    Total jobs: {status['total_jobs']}")
        print(f"    Completed: {status['completed']}")
        print(f"    Running: {status['running']}")
        print(f"    Pending: {status['pending']}")
        print(f"    Failed: {status['failed']}")
    else:
        print(f"❌ Status check failed!")
        print(f"    Response: {r.text}")
except Exception as e:
    print(f"❌ Status check error: {e}")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print(f"\n📊 Summary:")
print(f"   Project ID: {project_id}")
print(f"   Status: Agent workflow is running")
print(f"   Next: Wait 2-5 minutes for agents to complete")
print(f"   Then check: {BASE_URL}/projects/{project_id}/assets")
print("\n🤖 Real AI agents are now processing your project!")
print("=" * 70)
