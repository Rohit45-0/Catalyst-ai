# 🧪 Manual Testing Guide - Using Python Requests

Since Swagger UI has issues with OAuth2 + multipart/form-data, let's test the backend directly using Python.

## ✅ Server Status
- Server should be running on: `http://localhost:8000`
- Check by opening: http://localhost:8000/docs in your browser

---

## 📝 Step-by-Step Testing with Python

### **Step 1: Open Python Interactive Shell**
```bash
python
```

### **Step 2: Import requests and set base URL**
```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
```

### **Step 3: Login and Get Token**
```python
# Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": "barshilerohit1785@gmail.com",
        "password": "Rohit@1785"
    }
)

print(f"Login Status: {login_response.status_code}")
print(json.dumps(login_response.json(), indent=2))

# Save the token
token = login_response.json()["access_token"]
print(f"\nToken: {token[:50]}...")
```

**Expected Output:**
```
Login Status: 200
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

### **Step 4: Create a Project**
```python
# Create project with authentication
project_response = requests.post(
    f"{BASE_URL}/projects/",
    headers={"Authorization": f"Bearer {token}"},
    data={
        "product_name": "Nike Air Max Campaign",
        "brand_name": "Nike",
        "price": "$150",
        "description": "Launch campaign for new Nike Air Max sneakers",
        "campaign_goal": "Increase brand awareness and drive online sales",
        "target_audience": "Fitness enthusiasts aged 25-40",
        "brand_persona": "Energetic, innovative, performance-driven"
    }
)

print(f"\nProject Creation Status: {project_response.status_code}")
print(json.dumps(project_response.json(), indent=2))

# Save project ID
project_id = project_response.json()["id"]
print(f"\nProject ID: {project_id}")
```

**Expected Output:**
```
Project Creation Status: 201
{
  "id": 1,
  "product_name": "Nike Air Max Campaign",
  ...
}
```

### **Step 5: Start Agent Workflow**
```python
# Start the AI agent workflow
workflow_response = requests.post(
    f"{BASE_URL}/jobs/start/{project_id}",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"\nWorkflow Start Status: {workflow_response.status_code}")
print(json.dumps(workflow_response.json(), indent=2))
```

**Expected Output:**
```
Workflow Start Status: 200
{
  "message": "Agent workflow started for project 1",
  "jobs_created": 4
}
```

### **Step 6: Check Workflow Status**
```python
# Check job status
status_response = requests.get(
    f"{BASE_URL}/jobs/project/{project_id}/status",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"\nStatus Check: {status_response.status_code}")
print(json.dumps(status_response.json(), indent=2))
```

**Expected Output:**
```
Status Check: 200
{
  "project_id": 1,
  "total_jobs": 4,
  "completed": 0,
  "running": 1,
  "pending": 3,
  ...
}
```

### **Step 7: Wait and Check Assets (After 2-5 minutes)**
```python
import time

# Wait for jobs to complete (check every 30 seconds)
for i in range(10):  # Check up to 10 times (5 minutes)
    time.sleep(30)
    status = requests.get(
        f"{BASE_URL}/jobs/project/{project_id}/status",
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    
    print(f"\nCheck {i+1}: Completed={status['completed']}/{status['total_jobs']}")
    
    if status['completed'] == status['total_jobs']:
        print("✅ All jobs completed!")
        break

# Get generated assets
assets_response = requests.get(
    f"{BASE_URL}/projects/{project_id}/assets",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"\nAssets Status: {assets_response.status_code}")
print(json.dumps(assets_response.json(), indent=2))
```

---

## 🎯 What Each Test Verifies

| Test | What It Checks | Success Criteria |
|------|---------------|------------------|
| Login | Authentication works | Status 200, returns token |
| Create Project | Project creation + auth | Status 201, returns project with ID |
| Start Workflow | Agent orchestration | Status 200, creates 4 jobs |
| Check Status | Job monitoring | Status 200, shows job progress |
| Get Assets | Content generation | Status 200, returns AI-generated content |

---

## ✅ Success Indicators

You'll know everything is working when:

1. **Login** returns `200` with an `access_token`
2. **Create Project** returns `201` with a project `id`
3. **Start Workflow** returns `200` with `"jobs_created": 4`
4. **Check Status** shows jobs progressing: `pending` → `running` → `completed`
5. **Get Assets** returns AI-generated LinkedIn posts, Meta posts, and blog content

---

## 🐛 Troubleshooting

### If Login Fails (401):
- Check password is correct: `Rohit@1785`
- Verify email: `barshilerohit1785@gmail.com`

### If Project Creation Fails (401):
- Token might be expired, login again
- Make sure you're using the token from the login response

### If Project Creation Fails (422):
- Check the error message in the response
- Verify all required fields are provided

### If Workflow Fails to Start:
- Check server logs for errors
- Verify `.env` has all API keys configured

---

## 📊 Expected Timeline

- **Login**: Instant
- **Create Project**: 1-2 seconds
- **Start Workflow**: 1-2 seconds
- **Jobs Complete**: 2-5 minutes total
  - Vision Analysis: 10-20 seconds
  - Market Research: 30-60 seconds
  - Content Generation: 30-45 seconds
  - Image Generation: 20-40 seconds

---

## 💡 Pro Tip

Run all commands in a Python interactive session so you can:
- See immediate results
- Reuse the `token` and `project_id` variables
- Easily retry commands if needed

---

**Ready to test!** Open a Python shell and follow the steps above. 🚀
