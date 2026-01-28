# 🎯 END-TO-END TESTING GUIDE - Catalyst AI Backend

## ✅ AGENT INTEGRATION COMPLETE!

Your actual LangGraph agents are now integrated! The system will:
- Use **REAL agents** if you have Azure OpenAI & Brave API keys configured
- Use **MOCK agents** if keys are not configured (for testing the workflow)

---

## 🚀 QUICK START - Test in 5 Minutes!

### **Option 1: Test with Mock Agents (No API Keys Needed)**

This is perfect for testing the complete workflow without needing API keys!

1. **Start the server** (if not already running)
2. **Open Swagger UI:** http://localhost:8000/docs
3. **Follow the test steps below**

### **Option 2: Test with Real Agents (Requires API Keys)**

To use your actual agents, you need to configure:

**Required:**
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- `AZURE_OPENAI_KEY` - Your Azure OpenAI API key
- `BRAVE_API_KEY` - Your Brave Search API key (free at brave.com/search/api)

**Optional (for publishing):**
- LinkedIn, Meta, Medium tokens

**Update `.env` file with your keys, then restart the server.**

---

## 📋 COMPLETE END-TO-END TEST WORKFLOW

### **STEP 1: Authenticate** ✅

#### 1.1 Create Account
```
POST /auth/signup

Body:
{
  "email": "demo@catalyst.ai",
  "password": "demo123456"
}
```

#### 1.2 Login
```
Click "Authorize" button (🔓 top right)
username: demo@catalyst.ai
password: demo123456
Click "Authorize"
```

✅ **Expected:** Green checkmark appears

---

### **STEP 2: Create a Project** ✅

```
POST /projects

Form Data:
- product_name: "iPhone 15 Pro Max"
- brand_name: "Apple"
- price: "$1,199"
- description: "The ultimate iPhone with titanium design, A17 Pro chip, and advanced camera system"
- campaign_goal: "product launch"
- target_audience: "tech enthusiasts, professionals, early adopters aged 25-45"
- brand_persona: "innovative, premium, user-friendly, cutting-edge"
- image: [upload a product image - optional]
```

✅ **Expected Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "product_name": "iPhone 15 Pro Max",
  "status": "created",
  ...
}
```

**📋 COPY THE PROJECT ID!**

---

### **STEP 3: Start the Agent Workflow** 🚀

This is where the magic happens!

```
POST /jobs/start/{project_id}

Paste your project ID from STEP 2
```

✅ **Expected Response:**
```json
{
  "message": "Workflow started",
  "project_id": "550e8400-...",
  "status": "success",
  "jobs": {
    "vision_analysis": "job-uuid-1",
    "market_research": "job-uuid-2",
    "content_generation": "job-uuid-3",
    "image_generation": null
  }
}
```

**What's happening behind the scenes:**
1. 🔍 **Vision Analysis** - Analyzing product features
2. 📊 **Market Research** - Researching competitors and trends
3. ✍️ **Content Generation** - Creating LinkedIn, Meta, Blog posts
4. 🎨 **Image Generation** - Creating marketing images (optional)

---

### **STEP 4: Check Workflow Status** ✅

```
GET /jobs/project/{project_id}/status

Paste your project ID
```

✅ **Expected Response:**
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
      "type": "MARKET_RESEARCH",
      "status": "completed",
      ...
    },
    {
      "type": "CONTENT_GENERATION",
      "status": "completed",
      ...
    }
  ]
}
```

---

### **STEP 5: Get Generated Content** 🎉

```
GET /projects/{project_id}/assets

Paste your project ID
```

✅ **Expected Response:**
```json
{
  "assets": [
    {
      "id": "...",
      "asset_type": "linkedin_post",
      "content": "{\"title\":\"Introducing iPhone 15 Pro Max\",\"content\":\"We're excited to announce...\",\"hashtags\":[\"#Innovation\",\"#Technology\"]}",
      "created_at": "2026-01-26T..."
    },
    {
      "asset_type": "meta_post",
      "content": "{\"caption\":\"🚀 Check out iPhone 15 Pro Max!...\",\"hashtags\":[...]}",
      ...
    },
    {
      "asset_type": "blog_post",
      "content": "{\"title\":\"...\",\"content\":\"# iPhone 15 Pro Max\\n\\n...\",\"seo_keywords\":[...]}",
      ...
    }
  ]
}
```

**🎉 SUCCESS! You now have:**
- ✅ LinkedIn post with title, content, hashtags
- ✅ Meta (Facebook/Instagram) post with caption, hashtags
- ✅ Blog post with title, content, SEO keywords

---

### **STEP 6: View Individual Job Details** ✅

```
GET /jobs/{job_id}

Use a job ID from STEP 4
```

This shows detailed input/output for each agent step.

---

### **STEP 7: Get Project Details** ✅

```
GET /projects/{project_id}

Paste your project ID
```

✅ **Expected Response:**
```json
{
  "id": "...",
  "product_name": "iPhone 15 Pro Max",
  "status": "completed",
  "jobs_count": 3,
  "assets_count": 3,
  "latest_job_status": "completed",
  ...
}
```

---

## 🎯 TESTING CHECKLIST

- [ ] Server is running
- [ ] Swagger UI loads
- [ ] Created user account
- [ ] Logged in successfully
- [ ] Created a project
- [ ] Started workflow
- [ ] All jobs completed successfully
- [ ] Generated assets retrieved
- [ ] LinkedIn post looks good
- [ ] Meta post looks good
- [ ] Blog post looks good

---

## 🔧 Configuration Status

### **Current Setup:**

**✅ Working with Mock Agents:**
- No API keys required
- Tests complete workflow
- Generates sample content

**🔑 To Use Real Agents:**

Edit `.env` and add:
```bash
# Required for real agents
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_key_here
BRAVE_API_KEY=your_brave_key_here

# Set to false to use real agents
USE_MOCK_AGENTS=false
```

Then restart the server.

---

## 📊 What Each Agent Does

### **1. Vision Analysis Agent**
**Input:** Product image + description
**Output:**
- Product name and category
- Primary colors
- Material
- Key features
- Target demographic
- Visual style
- Selling points

### **2. Market Research Agent**
**Input:** Product name + brand + vision data
**Output:**
- Competitor analysis
- Market trends
- Customer pain points
- Pricing insights
- Review summaries

### **3. Content Generation Agent**
**Input:** Vision data + market data + campaign goals
**Output:**
- LinkedIn post (title, content, hashtags)
- Meta post (caption, hashtags)
- Blog post (title, content, SEO keywords)

### **4. Image Generation Agent** (Optional)
**Input:** Product data + market data
**Output:**
- Social media images
- Blog header images
- Marketing graphics

---

## 🐛 Troubleshooting

### Issue: "Workflow failed"
**Check:**
1. Look at job error messages in workflow status
2. Check if API keys are configured (if using real agents)
3. Verify image path is valid (if uploaded)

### Issue: "No assets generated"
**Solution:**
1. Check if content generation job completed
2. Verify workflow status shows "completed"
3. Check job output_payload for generated content

### Issue: Agents using mocks instead of real APIs
**Solution:**
1. Check `.env` has correct API keys
2. Set `USE_MOCK_AGENTS=false`
3. Restart the server

---

## 🎉 SUCCESS CRITERIA

After completing the test, you should have:

✅ **Project created** with product details
✅ **Workflow completed** with all jobs successful
✅ **3+ assets generated:**
   - LinkedIn post
   - Meta (Facebook/Instagram) post
   - Blog post
✅ **Content is relevant** to your product
✅ **All API endpoints working**

---

## 🚀 Next Steps

### **1. Configure Real Agents**
Add your API keys to `.env` to use actual AI-powered content generation.

### **2. Test with Different Products**
Try various product types:
- Electronics
- Fashion
- Food & Beverage
- Services
- B2B products

### **3. Customize Content**
Experiment with different:
- Campaign goals
- Target audiences
- Brand personas

### **4. Build Frontend**
Create a React/Next.js UI to:
- Upload product images
- Monitor workflow progress
- Display generated content
- Edit and publish content

### **5. Add Publishing**
Configure social media tokens to auto-publish:
- LinkedIn
- Facebook
- Instagram
- Medium

---

## 📞 Quick Reference

| Endpoint | Purpose |
|----------|---------|
| POST /auth/signup | Create account |
| POST /auth/login | Get auth token |
| POST /projects | Create project |
| POST /jobs/start/{id} | Start workflow |
| GET /jobs/project/{id}/status | Check progress |
| GET /projects/{id}/assets | Get results |

---

## 💡 Pro Tips

1. **Start with mock agents** to test the workflow
2. **Use descriptive product details** for better content
3. **Specify clear campaign goals** for targeted content
4. **Define target audience** for personalized messaging
5. **Set brand persona** for consistent voice

---

**🎉 READY TO TEST!**

Open Swagger UI and follow the steps above. The complete workflow should take less than 5 minutes!

**Questions or issues?** Check the troubleshooting section or review the job error messages.

---

**Last Updated:** 2026-01-26
**Status:** 🟢 READY FOR END-TO-END TESTING
