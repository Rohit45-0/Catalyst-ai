import requests
import json

# Test 1: Health check
try:
    r = requests.get('http://127.0.0.1:8000/')
    with open('test_results.txt', 'w') as f:
        f.write(f"Health Check: {r.status_code} - {r.json()}\n\n")
except Exception as e:
    with open('test_results.txt', 'w') as f:
        f.write(f"Health Check FAILED: {e}\n\n")

# Test 2: Login
try:
    r = requests.post('http://127.0.0.1:8000/auth/login', data={
        'username': 'barshilerohit1785@gmail.com',
        'password': 'Rohit@1785'
    })
    with open('test_results.txt', 'a') as f:
        f.write(f"Login: {r.status_code}\n")
        f.write(f"{json.dumps(r.json(), indent=2)}\n\n")
    
    if r.status_code == 200:
        token = r.json()['access_token']
        
        # Test 3: Create project
        r2 = requests.post('http://127.0.0.1:8000/projects/', 
            headers={'Authorization': f'Bearer {token}'},
            data={
                'product_name': 'Nike Air Max Campaign',
                'description': 'Test campaign'
            })
        with open('test_results.txt', 'a') as f:
            f.write(f"Create Project: {r2.status_code}\n")
            f.write(f"{r2.text}\n")
except Exception as e:
    with open('test_results.txt', 'a') as f:
        f.write(f"Test FAILED: {e}\n")

print("Tests complete. Check test_results.txt")
