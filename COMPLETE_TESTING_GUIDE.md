# 🧪 Complete Testing Guide - Catalyst AI Backend

## 🎯 Quick Test Workflow

Follow this step-by-step guide to test the complete system!

---

## ✅ Prerequisites

1. **Server Running:** http://localhost:8000
2. **Swagger UI Open:** http://localhost:8000/docs
3. **Authenticated:** Click "Authorize" and login

---

## 📝 Test Sequence

### **TEST 1: Authentication** ✅

#### 1.1 Create Account
```
POST /auth/signup
{
  "email": "demo@catalyst.ai",
  "password": "demo123456"
}
```
**Expected:** 201 Created

#### 1.2 Login
```
Click "Authorize" button
username: demo@catalyst.ai
password: demo123456
Click "Authorize"
```
**Expected:** Green checkmark ✅

#### 1.3 Get Current User
```
GET /auth/me
```
**Expected:** Your user data

---

### **TEST 2: Create Project** ✅

```
POST /projects

Form Data:
- product_name: "iPhone 15 Pro Max"
- brand_name: "Apple"
- price: "$1,199"
- description: "The most advanced iPhone ever with titanium design and A17 Pro chip"
- campaign_goal: "product launch"
- target_audience: "tech enthusiasts, professionals, early adopters"
- brand_persona: "innovative, premium, user-friendly"
- image: [upload a product image if you have one]
```

**Expected Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "...",
  "product_name": "iPhone 15 Pro Max",
  "brand_name": "Apple",
  "price": "$1,199",
  "description": "...",
  "campaign_goal": "product launch",
  "target_audience": "tech enthusiasts, professionals, early adopters",
  "brand_persona": "innovative, premium, user-friendly",
  "image_path": "uploads/xyz.jpg",
  "status": "created",
  "created_at": "2026-01-26T..."
}
```

**📋 COPY THE PROJECT ID!** You'll need it for the next steps.

---

### **TEST 3: List Projects** ✅

```
GET /projects
```

**Expected:** Array of your projects

---

### **TEST 4: Get Project Details** ✅

```
GET /projects/{project_id}

Paste the project ID from TEST 2
```

**Expected Response:**
```json
{
  "id": "...",
  "product_name": "iPhone 15 Pro Max",
  ...
  "jobs_count": 0,
  "assets_count": 0,
  "latest_job_status": null
}
```

---

### **TEST 5: Start Agent Workflow** ✅

```
POST /jobs/start/{project_id}

Paste the project ID from TEST 2
```

**Expected Response:**
```json
{
  "message": "Workflow started",
  "project_id": "...",
  "status": "success",
  "jobs": {
    "vision_analysis": "job-uuid-1",
    "market_research": "job-uuid-2",
    "content_generation": "job-uuid-3",
    "image_generation": null
  }
}
```

---

### **TEST 6: Check Workflow Status** ✅

```
GET /jobs/project/{project_id}/status

Paste the project ID
```

**Expected Response:**
```json
{
  "project_status": "completed",
  "jobs": [
    {
      "id": "...",
      "type": "VISION_ANALYSIS",
      "status": "completed",
      "started_at": "2026-01-26T...",
      "completed_at": "2026-01-26T...",
      "error": null
    },
    {
      "id": "...",
      "type": "MARKET_RESEARCH",
      "status": "completed",
      ...
    },
    {
      "id": "...",
      "type": "CONTENT_GENERATION",
      "status": "completed",
      ...
    }
  ]
}
```

---

### **TEST 7: Get Generated Assets** ✅

```
GET /projects/{project_id}/assets

Paste the project ID
```

**Expected Response:**
```json
{
  "assets": [
    {
      "id": "...",
      "project_id": "...",
      "asset_type": "linkedin_post",
      "content": "{\"title\":\"Introducing iPhone 15 Pro Max\",\"content\":\"...\",\"hashtags\":[...]}",
      "file_url": null,
      "created_at": "2026-01-26T..."
    },
    {
      "id": "...",
      "asset_type": "meta_post",
      "content": "{\"caption\":\"🚀 Check out iPhone 15 Pro Max!\",\"hashtags\":[...]}",
      ...
    },
    {
      "id": "...",
      "asset_type": "blog_post",
      "content": "{\"title\":\"...\",\"content\":\"...\",\"seo_keywords\":[...]}",
      ...
    }
  ]
}
```

---

### **TEST 8: Get Project Jobs** ✅

```
GET /projects/{project_id}/jobs

Paste the project ID
```

**Expected:** List of all jobs for the project

---

### **TEST 9: Get Specific Job** ✅

```
GET /jobs/{job_id}

Use a job ID from TEST 6
```

**Expected:** Detailed job information with input/output payloads

---

### **TEST 10: Update Project** ✅

```
PUT /projects/{project_id}

Body:
{
  "campaign_goal": "brand awareness and product launch",
  "status": "completed"
}
```

**Expected:** Updated project data

---

### **TEST 11: Delete Project** ⚠️

```
DELETE /projects/{project_id}

⚠️ WARNING: This will delete the project and all related jobs/assets!
```

**Expected:** 204 No Content

---

## 🎯 Success Criteria

After completing all tests, you should have:

- ✅ Created a user account
- ✅ Logged in successfully
- ✅ Created a project with product details
- ✅ Started the agent workflow
- ✅ Monitored job progress
- ✅ Retrieved generated content (LinkedIn, Meta, Blog posts)
- ✅ Updated project information
- ✅ (Optional) Deleted a project

---

## 📊 Expected Data Flow

```
1. Create Project
   ↓
   Status: "created"
   Jobs: 0
   Assets: 0

2. Start Workflow
   ↓
   Status: "processing"
   Jobs: 3-4 (pending/running)
   Assets: 0

3. Workflow Completes
   ↓
   Status: "completed"
   Jobs: 3-4 (all completed)
   Assets: 3+ (LinkedIn, Meta, Blog posts)

4. Retrieve Assets
   ↓
   Get generated marketing content
```

---

## 🐛 Troubleshooting

### Issue: "Unauthorized" errors
**Solution:** Click "Authorize" button and login again

### Issue: "Project not found"
**Solution:** Make sure you're using the correct project ID

### Issue: Workflow status shows "failed"
**Solution:** Check the job details for error messages

### Issue: No assets generated
**Solution:** Check if workflow completed successfully

---

## 📝 Test Data Examples

### Example 1: Tech Product
```
product_name: "MacBook Pro M3"
brand_name: "Apple"
price: "$1,999"
campaign_goal: "product launch"
target_audience: "creative professionals, developers"
brand_persona: "innovative, powerful, professional"
```

### Example 2: Fashion Product
```
product_name: "Premium Leather Jacket"
brand_name: "StyleCo"
price: "$299"
campaign_goal: "seasonal campaign"
target_audience: "fashion-conscious millennials"
brand_persona: "trendy, quality-focused, sustainable"
```

### Example 3: Food Product
```
product_name: "Organic Energy Bars"
brand_name: "NutriBoost"
price: "$24.99 (12-pack)"
campaign_goal: "brand awareness"
target_audience: "health-conscious consumers, athletes"
brand_persona: "healthy, energetic, natural"
```

---

## ✅ Testing Checklist

- [ ] Server is running
- [ ] Swagger UI loads
- [ ] Can create account
- [ ] Can login
- [ ] Can create project
- [ ] Can start workflow
- [ ] Workflow completes successfully
- [ ] Jobs show correct statuses
- [ ] Assets are generated
- [ ] Can retrieve assets
- [ ] Can update project
- [ ] Can delete project

---

## 🚀 Next Steps After Testing

Once testing is complete:

1. **Integrate Real Agents**
   - Replace mock implementations in orchestrator
   - Add your LangGraph agents

2. **Add Environment Variables**
   - Azure OpenAI keys
   - Brave Search API key
   - Social media credentials

3. **Build Frontend**
   - Create React/Next.js UI
   - Connect to backend APIs
   - Display generated content

4. **Deploy**
   - Set up production database
   - Deploy backend to cloud
   - Configure domain and SSL

---

## 📞 Quick Reference

| What | Where |
|------|-------|
| Swagger UI | http://localhost:8000/docs |
| API Docs | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/ |

---

**Happy Testing!** 🎉

If everything works, you're ready to integrate your actual agents!
