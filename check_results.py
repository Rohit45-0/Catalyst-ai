import requests
import json

BASE_URL = "http://127.0.0.1:8001"

# Login
print("Logging in...")
r = requests.post(f"{BASE_URL}/auth/login",
    data={"username": "testuser123@example.com", "password": "TestPass123!"})
token = r.json()["access_token"]
print(f"✅ Logged in\n")

# Get the latest project
project_id = "3ab987b8-1057-4d9b-9eab-e1233d4d6ca7"

# Check status to see the actual response format
print("Checking job status...")
r = requests.get(f"{BASE_URL}/jobs/project/{project_id}/status",
    headers={"Authorization": f"Bearer {token}"})

print(f"Status Code: {r.status_code}")
print(f"\nActual Response:")
print(json.dumps(r.json(), indent=2))

# Get assets
print("\n" + "="*70)
print("Getting generated assets...")
print("="*70)
r = requests.get(f"{BASE_URL}/projects/{project_id}/assets",
    headers={"Authorization": f"Bearer {token}"})

if r.status_code == 200:
    assets = r.json()
    print(f"\n✅ Found {len(assets)} assets!\n")
    
    for i, asset in enumerate(assets, 1):
        print(f"\n{'='*70}")
        print(f"ASSET {i}")
        print(f"{'='*70}")
        
        # Handle both dict and string formats
        if isinstance(asset, dict):
            asset_type = asset.get('asset_type', 'Unknown')
            content = asset.get('content', 'No content')
            print(f"Type: {asset_type}")
            print(f"\nContent:")
        else:
            # Asset is a string
            content = str(asset)
            print(f"Content:")
        
        if len(content) > 1000:
            print(content[:1000] + "\n\n... (truncated)")
        else:
            print(content)
else:
    print(f"❌ Failed to get assets: {r.status_code}")
    print(r.text)
