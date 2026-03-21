# ⚡ QUICK FIX: Database Not Loading on Easypanel

## The Problem
Your site https://khr-khr.epu6c6.easypanel.host/ is showing **hardcoded data** instead of **database data** because the Flask backend API is not running.

## The Fix

### Step 1: Update Environment Variables in Easypanel
Go to your app settings and add these environment variables:

```
FLASK_ENV=production
DATABASE_URL=postgresql://kishore:kishore*123@72.61.254.168:5432/khr_db
SECRET_KEY=kolan-hanmanth-reddy-2024-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=ranjith888999@gmail.com
MAIL_PASSWORD=(your app password)
MAIL_DEFAULT_SENDER=ranjith888999@gmail.com
GROQ_API_KEY=(your groq key)
```

### Step 2: Update Port Configuration
- **Exposed Port:** Change to **80** (not 5000)

### Step 3: Redeploy
1. Commit these updated files to your repository:
   ```bash
   git add Dockerfile docker-compose.yml EASYPANEL_DEPLOY.md
   git commit -m "Fix: Enable backend API for database access"
   git push
   ```

2. In Easypanel, click **"Rebuild"** or **"Deploy"**

### Step 4: Verify It's Working
After deployment completes (2-5 minutes), test:

1. **API Status:** https://khr-khr.epu6c6.easypanel.host/api/status
   - Should show: `{"status": "ok"}`

2. **Gallery API:** https://khr-khr.epu6c6.easypanel.host/api/gallery
   - Should return database JSON (not error)

3. **Main Site:** https://khr-khr.epu6c6.easypanel.host/
   - Gallery should now show database images
   - News should show database content
   - Community impacts should be from database

---

## Why This Happened

**Before:**
```
Easypanel → Only static files (HTML, CSS, JS)
JavaScript calls /api/* → 404 Not Found → Falls back to hardcoded data
```

**After:**
```
Easypanel → Nginx (Port 80) → Static files
                            → /api/* → Flask Backend (Port 5000) → Database ✅
```

---

## If Still Not Working

### Check 1: View Deployment Logs
Look for these messages:
- ✅ "Starting Flask backend..."
- ✅ "Booting worker with pid"
- ✅ "Starting Nginx..."

### Check 2: Test API Endpoint
```bash
curl https://khr-khr.epu6c6.easypanel.host/api/status
```

If you get 404 or 502, the backend isn't running. Check:
1. Environment variables are set
2. Port is set to 80
3. Build completed without errors

### Check 3: Database Connection
If API works but returns empty data:
1. Verify DATABASE_URL is correct
2. Check if database has data:
   ```bash
   # Run in backend directory
   python backend/seed_data.py
   python backend/seed_gallery.py
   ```

---

## Need More Help?
See full guide: [EASYPANEL_DEPLOY.md](./EASYPANEL_DEPLOY.md)
