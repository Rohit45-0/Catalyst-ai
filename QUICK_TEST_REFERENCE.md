# 🚀 Quick Testing Reference Card

## 📍 URLs
- **Swagger UI:** http://localhost:8000/docs
- **API Base:** http://localhost:8000

---

## ✅ 3-Step Testing Process

### 1️⃣ SIGNUP
```
Endpoint: POST /auth/signup
Body: {
  "email": "test@example.com",
  "password": "testpassword123"
}
Expected: 201 Created
```

### 2️⃣ LOGIN
```
Method: Click "Authorize" button in Swagger UI
Username: test@example.com
Password: testpassword123
Expected: Green checkmark ✅
```

### 3️⃣ TEST PROTECTED ENDPOINT
```
Endpoint: GET /auth/me
Auth: Automatic (after Step 2)
Expected: 200 OK with user data
```

---

## 🎯 Test Credentials

**Email:** test@example.com
**Password:** testpassword123

---

## 🔧 Automated Testing

Run the automated test script:
```bash
python test_oauth_fix.py
```

---

## ✨ Success Indicators

✅ Server running on port 8000
✅ Swagger UI loads
✅ Can create new user (201)
✅ Can login and get token (200)
✅ Can access /auth/me (200)
✅ OAuth2 "Authorize" works
✅ No "Failed to fetch" errors

---

## ❌ Common Errors (Expected!)

| Error | Meaning | Solution |
|-------|---------|----------|
| 400 Email already registered | User exists | Use different email or login |
| 401 Unauthorized | Wrong password | Check credentials |
| 401 on /auth/me | Not logged in | Click "Authorize" first |

---

## 🎨 Swagger UI Tips

1. **Authorize Button** (🔓) - Top right corner
2. **Try it out** - Click before testing endpoint
3. **Execute** - Runs the request
4. **Response** - Shows result below
5. **Clear** - Reset the form

---

## 📊 Testing Checklist

- [ ] Start server: `python -m uvicorn app.main:app --reload`
- [ ] Open Swagger: http://localhost:8000/docs
- [ ] Test signup
- [ ] Test login via Authorize button
- [ ] Test /auth/me endpoint
- [ ] Verify all responses are correct

---

## 🔐 Current Status

✅ **CORS Error:** FIXED
✅ **Dependencies:** INSTALLED
✅ **Server:** RUNNING
✅ **Authentication:** WORKING
✅ **OAuth2:** FUNCTIONAL

---

## 📞 Quick Commands

```bash
# Start server
python -m uvicorn app.main:app --reload

# Run automated tests
python test_oauth_fix.py

# Check server health
curl http://localhost:8000/
```

---

**Ready to test!** 🎉
Open http://localhost:8000/docs and follow the 3-step process above.
