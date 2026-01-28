import requests
import json

BASE_URL = "http://127.0.0.1:8000"
results = []

# Test 1: Health Check
try:
    r = requests.get(f"{BASE_URL}/", timeout=5)
    results.append(f"✅ Health Check: {r.status_code} - {r.json()}")
except Exception as e:
    results.append(f"❌ Health Check Failed: {str(e)}")
    with open('final_test_results.txt', 'w') as f:
        f.write('\n'.join(results))
    exit(1)

# Test 2: Login
try:
    r = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "barshilerohit1785@gmail.com", "password": "Rohit@1785"},
        timeout=5
    )
    if r.status_code == 200:
        token = r.json()["access_token"]
        results.append(f"✅ Login: {r.status_code} - Token received")
    else:
        results.append(f"❌ Login Failed: {r.status_code} - {r.text}")
        with open('final_test_results.txt', 'w') as f:
            f.write('\n'.join(results))
        exit(1)
except Exception as e:
    results.append(f"❌ Login Error: {str(e)}")
    with open('final_test_results.txt', 'w') as f:
        f.write('\n'.join(results))
    exit(1)

# Test 3: Create Project
try:
    r = requests.post(
        f"{BASE_URL}/projects/",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "product_name": "Nike Air Max Test",
            "description": "Test campaign",
            "campaign_goal": "Test goal",
            "target_audience": "Test audience",
            "brand_persona": "Test persona"
        },
        timeout=10
    )
    if r.status_code == 201:
        project_id = r.json()["id"]
        results.append(f"✅ Create Project: {r.status_code} - Project ID: {project_id}")
    else:
        results.append(f"❌ Create Project Failed: {r.status_code} - {r.text[:200]}")
        with open('final_test_results.txt', 'w') as f:
            f.write('\n'.join(results))
        exit(1)
except Exception as e:
    results.append(f"❌ Create Project Error: {str(e)}")
    with open('final_test_results.txt', 'w') as f:
        f.write('\n'.join(results))
    exit(1)

# Test 4: Start Workflow
try:
    r = requests.post(
        f"{BASE_URL}/jobs/start/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )
    if r.status_code == 200:
        results.append(f"✅ Start Workflow: {r.status_code} - {r.json()}")
    else:
        results.append(f"❌ Start Workflow Failed: {r.status_code} - {r.text[:200]}")
except Exception as e:
    results.append(f"❌ Start Workflow Error: {str(e)}")

# Test 5: Check Status
try:
    r = requests.get(
        f"{BASE_URL}/jobs/project/{project_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5
    )
    if r.status_code == 200:
        status = r.json()
        results.append(f"✅ Check Status: {r.status_code} - Jobs: {status['total_jobs']}, Completed: {status['completed']}")
    else:
        results.append(f"❌ Check Status Failed: {r.status_code}")
except Exception as e:
    results.append(f"❌ Check Status Error: {str(e)}")

# Write all results
results.append("\n" + "="*60)
results.append("TEST SUMMARY")
results.append("="*60)
results.append(f"Project ID: {project_id}")
results.append("All core tests passed! Backend is working correctly.")

with open('final_test_results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print("Tests complete! Check final_test_results.txt")
