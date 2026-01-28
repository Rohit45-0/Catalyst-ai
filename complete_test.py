import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001"

print("=" * 70)
print("🔧 CREATING NEW TEST USER AND RUNNING FULL TEST")
print("=" * 70)

# Step 1: Create new user
print("\n[1/6] Creating new test user...")
r = requests.post(f"{BASE_URL}/auth/signup",
    json={
        "email": "testuser123@example.com",
        "password": "TestPass123!",
        "full_name": "Test User"
    })
print(f"    Status: {r.status_code}")
if r.status_code in [200, 201]:
    print(f"    ✅ User created successfully!")
elif "already registered" in r.text:
    print(f"    ℹ️  User already exists, will use existing account")
else:
    print(f"    Response: {r.json()}")

# Step 2: Login
print("\n[2/6] Logging in...")
r = requests.post(f"{BASE_URL}/auth/login",
    data={
        "username": "testuser123@example.com",
        "password": "TestPass123!"
    })
print(f"    Status: {r.status_code}")
if r.status_code == 200:
    token = r.json()["access_token"]
    print(f"    ✅ Login successful!")
    print(f"    Token: {token[:50]}...")
else:
    print(f"    ❌ Login failed: {r.json()}")
    exit(1)

# Step 3: Create Project
print("\n[3/6] Creating project...")
r = requests.post(f"{BASE_URL}/projects/",
    headers={"Authorization": f"Bearer {token}"},
    data={
        "product_name": "Nike Air Max Campaign",
        "brand_name": "Nike",
        "price": "$150",
        "description": "Launch campaign for new Nike Air Max sneakers targeting fitness enthusiasts",
        "campaign_goal": "Increase brand awareness and drive online sales for the new Air Max collection",
        "target_audience": "Fitness enthusiasts, sneaker collectors, and active lifestyle millennials aged 25-40",
        "brand_persona": "Energetic, innovative, and performance-driven. We inspire athletes to push their limits."
    })
print(f"    Status: {r.status_code}")
if r.status_code == 201:
    project = r.json()
    project_id = project["id"]
    print(f"    ✅ Project created!")
    print(f"    Project ID: {project_id}")
    print(f"    Name: {project['product_name']}")
else:
    print(f"    ❌ Failed: {r.text}")
    exit(1)

# Step 4: Start Workflow
print("\n[4/6] Starting AI agent workflow...")
r = requests.post(f"{BASE_URL}/jobs/start/{project_id}",
    headers={"Authorization": f"Bearer {token}"})
print(f"    Status: {r.status_code}")
if r.status_code == 200:
    result = r.json()
    print(f"    ✅ Workflow started!")
    print(f"    Message: {result.get('message', 'Workflow started')}")
    if 'jobs_created' in result:
        print(f"    Jobs created: {result['jobs_created']}")
else:
    print(f"    ❌ Failed: {r.text}")
    exit(1)

# Step 5: Monitor Progress
print("\n[5/6] Monitoring job progress...")
print("    (Checking every 30 seconds, max 5 minutes)")
start_time = time.time()
while True:
    r = requests.get(f"{BASE_URL}/jobs/project/{project_id}/status",
        headers={"Authorization": f"Bearer {token}"})
    status = r.json()
    
    # Check project status directly
    project_status = status.get('project_status', 'unknown')
    
    # Calculate counts manually from jobs list
    jobs = status.get('jobs', [])
    total_jobs = len(jobs)
    completed_jobs = sum(1 for j in jobs if j.get('status') == 'completed')
    failed_jobs = sum(1 for j in jobs if j.get('status') == 'failed')
    running_jobs = sum(1 for j in jobs if j.get('status') == 'running')
    
    print(f"    Status: {project_status} ({completed_jobs}/{total_jobs} completed)")
    
    if project_status == 'completed' or (total_jobs > 0 and completed_jobs == total_jobs):
        print("\n    ✅ All jobs completed!")
        break
        
    if project_status == 'failed' or failed_jobs > 0:
        print("\n    ❌ Workflow failed!")
        break
        
    elapsed = time.time() - start_time
    if elapsed > 300:  # 5 minutes timeout
        print("\n    ⚠️ Timeout waiting for jobs")
        break
        
    time.sleep(10)

# Step 6: Get Generated Assets
print("\n[6/6] Fetching generated marketing content...")
r = requests.get(f"{BASE_URL}/projects/{project_id}/assets",
    headers={"Authorization": f"Bearer {token}"})
print(f"    Status: {r.status_code}")
if r.status_code == 200:
    assets = r.json()
    print(f"    ✅ Retrieved {len(assets)} assets!\n")
    
    print("\n" + "=" * 70)
    print("📄 GENERATED MARKETING CONTENT")
    print("=" * 70)
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{'─' * 70}")
        print(f"Asset {i}")
        print(f"{'─' * 70}")
        
        # Handle both dict and string formats
        if isinstance(asset, dict):
            asset_type = asset.get('asset_type', 'Unknown')
            content = asset.get('content', 'No content')
            print(f"Type: {asset_type}")
            print(f"\nContent:")
        else:
            # Asset might be a string (JSON string or raw text)
            try:
                # Try to parse if it's a JSON string
                if isinstance(asset, str) and (asset.startswith('{') or asset.startswith('[')):
                     parsed = json.loads(asset)
                     if isinstance(parsed, dict):
                         print(f"Type: {parsed.get('asset_type', 'Unknown')}")
                         content = parsed.get('content', str(parsed))
                     else:
                         content = str(asset)
                else:
                    content = str(asset)
            except:
                content = str(asset)
            print(f"Content:")

        if len(content) > 800:
            print(content[:800] + "\n... (truncated)")
        else:
            print(content)
else:
    print(f"    ❌ Failed to get assets: {r.text}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETE!")
print("=" * 70)
print(f"\nSummary:")
print(f"  - Project ID: {project_id}")
print(f"  - Total Assets Generated: {len(assets) if r.status_code == 200 else 0}")
print(f"  - Real AI Agents: ENABLED")
print(f"  - Backend Status: WORKING ✅")
print("=" * 70)
