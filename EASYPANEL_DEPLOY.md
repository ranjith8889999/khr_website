# 🚀 EASYPANEL DEPLOYMENT GUIDE - FIXED

## Problem Diagnosed
Your deployed site at https://khr-khr.epu6c6.easypanel.host/ is showing **hardcoded local data instead of database data** because:
- ✗ Backend Flask API is not running/accessible
- ✓ Frontend loads successfully
- ✗ API calls to `/api/*` fail
- ✓ Fallback mechanism in main.js shows local hardcoded data

## Solution Overview
The Dockerfile has been updated to run **both Flask backend (port 5000) and Nginx (port 80)** simultaneously.

---

## 🔧 EASYPANEL DEPLOYMENT STEPS

### Step 1: Update Your Repository
Ensure these files are committed to your repository:
- ✅ `Dockerfile` (updated to run both services)
- ✅ `docker-compose.yml` (updated with port 80)
- ✅ `nginx.conf` (already correct)
- ✅ `start-server.sh` (startup script)

### Step 2: Configure Easypanel

#### A. Create New App (or Update Existing)
1. Go to your Easypanel dashboard
2. Select your project
3. Choose **"Deploy from GitHub"** or **"Docker"**

#### B. Configuration Settings

**Deployment Type:** Docker

**Repository:** Your GitHub repository

**Branch:** main (or your default branch)

**Build Settings:**
- Dockerfile: `./Dockerfile`
- Build Context: `.` (root)

**Port Configuration:**
- Main Port: **80** (this is what Easypanel will expose)
- Internal Backend Port: 5000 (internal to container)

#### C. Environment Variables
Add these in Easypanel's Environment Variables section:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://kishore:kishore*123@72.61.254.168:5432/khr_db
SECRET_KEY=kolan-hanmanth-reddy-2024-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=ranjith888999@gmail.com
MAIL_PASSWORD=your-app-password-here
MAIL_DEFAULT_SENDER=ranjith888999@gmail.com
GROQ_API_KEY=your-groq-api-key-here
```

⚠️ **Important:** Replace `your-app-password-here` and `your-groq-api-key-here` with actual values.

### Step 3: Deploy

1. Click **"Deploy"** or **"Rebuild"**
2. Wait for build to complete (2-5 minutes)
3. Check logs for these messages:
   - ✅ "Starting Flask backend..."
   - ✅ "Starting Nginx..."
   - ✅ Gunicorn worker messages

### Step 4: Verify Deployment

Test these endpoints after deployment:

1. **Main Site:** https://khr-khr.epu6c6.easypanel.host/
   - Should load homepage

2. **API Health Check:** https://khr-khr.epu6c6.easypanel.host/api/status
   - Should return: `{"status": "ok"}`

3. **Gallery Data:** https://khr-khr.epu6c6.easypanel.host/api/gallery
   - Should return JSON with database data

4. **Community Impacts:** https://khr-khr.epu6c6.easypanel.host/api/community-impacts
   - Should return JSON with database data

---

## 🐛 Troubleshooting

### Issue: Still showing local data after deployment

**Check 1: Backend logs**
```bash
# In Easypanel, view logs to see if Flask is running
# Look for: "Booting worker with pid: XXXX"
```

**Check 2: API endpoint test**
Visit: https://khr-khr.epu6c6.easypanel.host/api/status
- If 404: Backend not running
- If 502: Backend crashed
- If 200: Backend OK, check database connection

**Check 3: Database connection**
```bash
# Check if DATABASE_URL environment variable is set correctly
# Check if database is accessible from Easypanel IP
```

### Issue: 502 Bad Gateway

**Cause:** Flask backend crashed

**Fix:**
1. Check logs for Python errors
2. Verify all environment variables are set
3. Ensure database is accessible
4. Check if port 5000 is available internally

### Issue: Build fails

**Cause:** Missing dependencies or Docker error

**Fix:**
1. Check Dockerfile syntax
2. Ensure `backend/requirements.txt` exists
3. View build logs for specific errors

---

## 📊 How It Works Now

```
User Request → Nginx (Port 80)
    ├─ Static files (HTML, CSS, JS, images) → Served directly
    └─ /api/* requests → Proxy to Flask (Port 5000) → Database
```

### Before Fix:
```
User → Nginx → Static files only
Frontend JS → /api/* → 404 → Fallback to hardcoded data ❌
```

### After Fix:
```
User → Nginx → Static files
Frontend JS → /api/* → Nginx Proxy → Flask → Database ✅
```

---

## 🔄 Alternative: Separate Backend Service

If you prefer separating frontend and backend:

### Option 1: Two Easypanel Apps

**App 1: Backend API**
- Port: 5000
- Dockerfile: Backend only
- Domain: api.yourdomain.com

**App 2: Frontend**
- Port: 80
- Nginx serving static files
- Update JS to call: `https://api.yourdomain.com/api/*`

### Option 2: Single App with Process Manager

Use `supervisord` to manage multiple processes:
- Already done in our updated Dockerfile ✅

---

## ✅ Quick Checklist

Before redeploying, ensure:
- [ ] Environment variables configured in Easypanel
- [ ] Port 80 is set as main exposed port
- [ ] Database accessible from Easypanel IP
- [ ] Latest code pushed to GitHub
- [ ] Build logs show no errors

After deployment:
- [ ] `/api/status` returns 200 OK
- [ ] Homepage loads correctly
- [ ] Gallery shows database images (not hardcoded)
- [ ] News section shows database content
- [ ] Forms can be submitted

---

## 🆘 Need Help?

If still having issues:
1. Share the **build logs** from Easypanel
2. Share the **runtime logs** (last 50 lines)
3. Test: `curl https://khr-khr.epu6c6.easypanel.host/api/status`
4. Check database connection from Easypanel terminal

### Test Locally with Docker:
```bash
docker-compose up --build
```

Visit: http://localhost:5000

---

## Troubleshooting

### Issue 1: API 404 Errors
**Cause:** Flask app not running
**Fix:** Ensure start command uses `gunicorn backend.app:app`

### Issue 2: Static Files Not Loading
**Cause:** Wrong root directory
**Fix:** Set root to `/app` in Nginx or use Flask to serve static files

### Issue 3: Database Connection Errors
**Cause:** PostgreSQL credentials incorrect
**Fix:** Verify `DATABASE_URL` environment variable

### Issue 4: Service Worker 404
**Cause:** sw.js doesn't exist in project
**Fix:** This is normal - remove service worker registration from main.js if not needed

---

## EasyPanel Specific Settings

**App Type:** Web Service
**Build Pack:** Python
**Python Version:** 3.11
**Install Command:** `pip install -r backend/requirements.txt`
**Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 4 backend.app:app`
**Working Directory:** `/app`

---

## File Structure After Push

```
/app/
├── backend/
│   ├── app.py          # Main Flask application
│   └── requirements.txt
├── css/
├── js/
├── images/
├── admin/
├── index.html
├── ai-chat.html
├── Dockerfile
├── nginx.conf
└── start.sh
```

---

## Expected Logs (Success)

```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 8
[INFO] Booting worker with pid: 9
[INFO] Booting worker with pid: 10
[INFO] Booting worker with pid: 11
```

---

## Support URLs

- Flask Docs: https://flask.palletsprojects.com/
- Gunicorn Docs: https://docs.gunicorn.org/
- EasyPanel Docs: https://easypanel.io/docs
