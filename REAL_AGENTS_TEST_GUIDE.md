# 🚀 Real Agents Testing Guide - Step by Step

## ✅ Prerequisites Confirmed
- ✅ Server is running on `http://localhost:8000`
- ✅ Real agents enabled (`USE_MOCK_AGENTS=false`)
- ✅ Azure OpenAI configured (GPT-4o)
- ✅ Brave Search API configured
- ✅ Bytez API configured for image generation
- ✅ LinkedIn credentials configured

---

## 📋 Step-by-Step Testing Instructions

### **Step 1: Open Swagger UI**
1. Open your browser
2. Navigate to: **`http://localhost:8000/docs`**
3. You should see the FastAPI Swagger documentation interface

---

### **Step 2: Create a New User Account**

1. **Locate the Auth Section** in Swagger UI
2. **Find `POST /auth/signup`** endpoint
3. Click **"Try it out"**
4. Fill in the request body with a **NEW email** (not previously used):

```json
{
  "email": "testuser@example.com",
  "password": "TestPassword123!",
  "full_name": "Test User"
}
```

5. Click **"Execute"**
6. **Expected Response:** `201 Created` with user details

> ⚠️ **Note:** If you get "Email already registered", use a different email address.

---

### **Step 3: Login and Get Access Token**

#### **Option A: Using Swagger's Authorize Button (Recommended)**
1. Click the **green "Authorize" button** at the top right of Swagger UI
2. In the popup:
   - **Username:** `testuser@example.com` (your email)
   - **Password:** `TestPassword123!` (your password)
   - Leave other fields empty
3. Click **"Authorize"**
4. Click **"Close"**
5. You're now authenticated! 🎉

#### **Option B: Manual Login**
1. Find `POST /auth/login` endpoint
2. Click **"Try it out"**
3. Fill in the form data:
   - **username:** `testuser@example.com`
   - **password:** `TestPassword123!`
4. Click **"Execute"**
5. Copy the `access_token` from the response
6. Click the **"Authorize" button** and paste the token in the format: `Bearer <your_token>`

---

### **Step 4: Create a Marketing Project**

1. **Find `POST /projects`** endpoint
2. Click **"Try it out"**
3. Fill in the project details:

```json
{
  "name": "Nike Air Max Campaign",
  "description": "Launch campaign for new Nike Air Max sneakers targeting fitness enthusiasts",
  "campaign_goal": "Increase brand awareness and drive online sales for the new Air Max collection",
  "target_audience": "Fitness enthusiasts, sneaker collectors, and active lifestyle millennials aged 25-40",
  "brand_persona": "Energetic, innovative, and performance-driven. We inspire athletes to push their limits."
}
```

4. **For the image field:**
   - Click **"Choose File"** and upload a product image (e.g., a sneaker photo)
   - OR leave it empty if you don't have an image

5. Click **"Execute"**
6. **Expected Response:** `201 Created` with project details
7. **📝 IMPORTANT:** Copy the `project_id` from the response (e.g., `1`)

---

### **Step 5: Start the AI Agent Workflow** 🤖

This is where the magic happens! The system will run 4 AI agents sequentially:

1. **Find `POST /jobs/start/{project_id}`** endpoint
2. Click **"Try it out"**
3. Enter your **project_id** from Step 4 (e.g., `1`)
4. Click **"Execute"**
5. **Expected Response:** `200 OK` with a message like:
```json
{
  "message": "Agent workflow started for project 1",
  "jobs_created": 4
}
```

#### **What's Happening Behind the Scenes:**
- 🔍 **Vision Analyzer Agent**: Analyzing your product image using Azure OpenAI GPT-4o Vision
- 📊 **Market Research Agent**: Searching Brave for market trends, competitors, and customer reviews
- ✍️ **Content Writer Agent**: Generating LinkedIn posts, Meta posts, and blog content
- 🎨 **Image Generator Agent**: Creating marketing visuals using Bytez API

> ⏱️ **Processing Time:** This will take **2-5 minutes** as real AI agents are working!

---

### **Step 6: Monitor Job Progress**

While the agents are working, you can check their status:

1. **Find `GET /jobs/project/{project_id}/status`** endpoint
2. Click **"Try it out"**
3. Enter your **project_id** (e.g., `1`)
4. Click **"Execute"**

**You'll see the status of each job:**
```json
{
  "project_id": 1,
  "total_jobs": 4,
  "completed": 2,
  "running": 1,
  "pending": 1,
  "failed": 0,
  "jobs": [
    {
      "job_id": 1,
      "agent_type": "VISION_ANALYSIS",
      "status": "completed",
      "started_at": "2026-01-27T06:10:00",
      "completed_at": "2026-01-27T06:10:15"
    },
    {
      "job_id": 2,
      "agent_type": "MARKET_RESEARCH",
      "status": "running",
      "started_at": "2026-01-27T06:10:15"
    },
    ...
  ]
}
```

**Keep refreshing this endpoint** until all jobs show `"status": "completed"`

---

### **Step 7: View Generated Marketing Assets** 🎉

Once all jobs are completed:

1. **Find `GET /projects/{project_id}/assets`** endpoint
2. Click **"Try it out"**
3. Enter your **project_id** (e.g., `1`)
4. Click **"Execute"**

**You'll see AI-generated marketing content:**
```json
[
  {
    "id": 1,
    "asset_type": "LINKEDIN_POST",
    "content": "🚀 Introducing the all-new Nike Air Max...",
    "created_at": "2026-01-27T06:12:30"
  },
  {
    "id": 2,
    "asset_type": "META_POST",
    "content": "Step into greatness with Nike Air Max...",
    "created_at": "2026-01-27T06:12:30"
  },
  {
    "id": 3,
    "asset_type": "BLOG_POST",
    "content": "# The Evolution of Performance: Nike Air Max 2024...",
    "created_at": "2026-01-27T06:12:30"
  }
]
```

---

## 🔍 What Each Agent Does (Real Implementation)

### 1. **Vision Analyzer Agent** (`VISION_ANALYSIS`)
- **Technology:** Azure OpenAI GPT-4o with Vision
- **Input:** Product image + project description
- **Output:** Detailed visual analysis including:
  - Product features and design elements
  - Color palette and aesthetics
  - Target audience insights from visual cues
  - Emotional appeal and brand positioning

### 2. **Market Research Agent** (`MARKET_RESEARCH`)
- **Technology:** Brave Search API + Azure OpenAI
- **Input:** Product name, campaign goal, target audience
- **Output:** Comprehensive market intelligence:
  - Industry trends and market size
  - Competitor analysis
  - Customer reviews and sentiment
  - Pricing strategies
  - Market opportunities

### 3. **Content Writer Agent** (`CONTENT_GENERATION`)
- **Technology:** Azure OpenAI GPT-4o
- **Input:** Vision analysis + Market research + Brand persona
- **Output:** Three types of marketing content:
  - **LinkedIn Post:** Professional, B2B-focused
  - **Meta Post:** Engaging, visual-first for Instagram/Facebook
  - **Blog Post:** Long-form, SEO-optimized article

### 4. **Image Generator Agent** (`IMAGE_GENERATION`) - Optional
- **Technology:** Bytez API
- **Input:** Content themes and visual requirements
- **Output:** AI-generated marketing images

---

## 🧪 Additional Testing Scenarios

### **Test 2: Different Product Category**
Try creating a project for a different product:
```json
{
  "name": "Organic Skincare Launch",
  "description": "New line of organic, vegan skincare products",
  "campaign_goal": "Build brand trust and drive e-commerce sales",
  "target_audience": "Health-conscious women aged 30-50 interested in clean beauty",
  "brand_persona": "Natural, transparent, and science-backed. We believe beauty starts with healthy skin."
}
```

### **Test 3: Check Individual Job Details**
1. Use `GET /jobs/{job_id}` to see detailed output from each agent
2. Check `output_payload` for the raw agent results

### **Test 4: Retry Failed Jobs**
If any job fails:
1. Use `POST /jobs/{job_id}/retry` to retry that specific job
2. Check the `error_message` field to understand what went wrong

---

## 🐛 Troubleshooting

### **Issue: Jobs stuck in "running" status**
- **Cause:** API rate limits or network issues
- **Solution:** Wait 2-3 minutes and check status again, or use retry endpoint

### **Issue: "401 Unauthorized" errors**
- **Cause:** Token expired or not authenticated
- **Solution:** Re-authenticate using the "Authorize" button

### **Issue: No assets generated**
- **Cause:** Content generation job failed
- **Solution:** Check job status for error messages, verify Azure OpenAI credentials in `.env`

### **Issue: Vision analysis fails**
- **Cause:** No image uploaded or invalid image format
- **Solution:** Upload a valid image (JPG, PNG) or the agent will work without image analysis

---

## 📊 Expected Timeline

| Agent | Typical Duration | What to Expect |
|-------|-----------------|----------------|
| Vision Analysis | 10-20 seconds | Fast, uses GPT-4o Vision |
| Market Research | 30-60 seconds | Brave Search + AI analysis |
| Content Generation | 30-45 seconds | Generates 3 content pieces |
| Image Generation | 20-40 seconds | Optional, creates visuals |
| **Total** | **2-3 minutes** | Full workflow completion |

---

## ✅ Success Criteria

You've successfully tested the system when:
- ✅ User signup and login work
- ✅ Project creation succeeds with all marketing fields
- ✅ All 4 jobs complete with "completed" status
- ✅ Assets endpoint returns AI-generated LinkedIn, Meta, and Blog posts
- ✅ Content is relevant to your product and target audience
- ✅ No jobs show "failed" status

---

## 🎯 Next Steps After Testing

1. **Review Content Quality:** Check if the AI-generated content matches your brand voice
2. **Test Multiple Products:** Try different product categories to see agent versatility
3. **API Integration:** Use the REST API endpoints in your frontend application
4. **Publishing:** Implement LinkedIn/Meta publishing features (optional)
5. **Analytics:** Track which content performs best

---

## 🔗 Quick Reference URLs

- **Swagger UI:** http://localhost:8000/docs
- **API Root:** http://localhost:8000/
- **Health Check:** http://localhost:8000/

---

## 💡 Pro Tips

1. **Use descriptive project names** - helps identify campaigns later
2. **Be specific with target audience** - better AI-generated content
3. **Define clear campaign goals** - agents optimize for your objectives
4. **Upload high-quality images** - better vision analysis results
5. **Check job status regularly** - don't wait too long between checks

---

**Happy Testing! 🚀**

If you encounter any issues, check the server logs or the job `error_message` field for details.
