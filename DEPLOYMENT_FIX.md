# 🔧 QUICK FIX FOR EASYPANEL DEPLOYMENT

## Problem Summary
Your API endpoints are returning 404 because the Flask backend isn't running. Nginx is trying to serve API requests as static files.

---

## ⚡ IMMEDIATE FIX (3 Steps)

### Step 1: Update Start Command in EasyPanel

Go to your EasyPanel dashboard → Your App → Settings

**Change Start Command to:**
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 backend.app:app
```

### Step 2: Add Missing Environment Variable

In EasyPanel Environment Variables section, add:

**Variable Name:** `GROQ_API_KEY`  
**Value:** `<your-groq-api-key-from-env-file>`

### Step 3: Redeploy

1. Pull latest code from GitHub (has deployment configs)
2. Click **Rebuild** or **Restart** in EasyPanel
3. Wait for deployment to complete

---

## ✅ Verify It Works

After redeployment, check these URLs:

1. **Homepage:** https://khr-khr.epu6c6.easypanel.host/
2. **API Status:** https://khr-khr.epu6c6.easypanel.host/api/status
3. **Gallery API:** https://khr-khr.epu6c6.easypanel.host/api/gallery

If `/api/status` returns data, your backend is working! ✅

---

## 📋 Complete EasyPanel Configuration

### Build Settings:
- **Framework:** Python
- **Python Version:** 3.11
- **Root Directory:** `/`
- **Build Command:** `pip install -r backend/requirements.txt`

### Deployment Settings:
- **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 backend.app:app`
- **Port:** `5000` (or use variable `$PORT`)
- **Working Directory:** `/app`

### Environment Variables (all required):
```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://kishore:kishore*123@72.61.254.168:5432/khr_db
SECRET_KEY=kolan-hanmanth-reddy-2024-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=ranjith888999@gmail.com
MAIL_PASSWORD=<your-actual-password>
MAIL_DEFAULT_SENDER=ranjith888999@gmail.com
GROQ_API_KEY=<your-actual-api-key>
ADMIN_USERNAME=khr
ADMIN_PASSWORD=khr@123
```

---

## 🐛 Troubleshooting

### Issue: Still getting 404 on API endpoints
**Solution:** Check logs to ensure gunicorn started:
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
```

### Issue: Database errors
**Solution:** Verify PostgreSQL is accessible from EasyPanel servers

### Issue: 500 Internal Server Error
**Solution:** Check application logs for Python errors

---

## 📚 Additional Resources

- Full deployment guide: [EASYPANEL_DEPLOY.md](EASYPANEL_DEPLOY.md)
- Docker deployment: [Dockerfile](Dockerfile)
- Alternative platforms: [railway.json](railway.json), [render.yaml](render.yaml)

---

## 🆘 Still Having Issues?

1. Check EasyPanel logs for errors
2. Verify all environment variables are set
3. Ensure port configuration matches
4. Check if database is accessible
5. Review nginx configuration if using reverse proxy

**Expected successful log:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
