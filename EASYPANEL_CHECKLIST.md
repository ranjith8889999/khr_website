# 🚨 CRITICAL: Easypanel Configuration Checklist

## The Problem
Your API endpoints return **404 Not Found** because Flask backend isn't accessible.
- ❌ API calls like `/api/community-impacts/all` fail
- ❌ Admin panel can't load database data
- ✅ Static files load (HTML/CSS/JS)

## Root Cause
**The Flask backend container is either:**
1. Not starting properly
2. Not exposed on the correct port
3. Environment variables missing
4. Build failing silently

---

## ✅ EXACT EASYPANEL CONFIGURATION

### Step 1: App Settings

**Source:**
- Repository: Your GitHub repo
- Branch: `fix/dockerfix` ← CRITICAL!
- Build Context: `/` (root)

**Build:**
- Build Method: `Dockerfile`
- Dockerfile Path: `./Dockerfile`

**Networking:**
- **Port: 5000** ← MUST BE 5000 (not 80, not 3000)
- Protocol: HTTP

### Step 2: Environment Variables

Click "Environment" tab and add **ALL** these:

```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://kishore:kishore*123@72.61.254.168:5432/khr_db
SECRET_KEY=kolan-hanmanth-reddy-2024-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=ranjith888999@gmail.com
MAIL_PASSWORD=<your-gmail-app-password>
MAIL_DEFAULT_SENDER=ranjith888999@gmail.com
GROQ_API_KEY=<your-groq-api-key>
```

**IMPORTANT:** Replace:
- `<your-gmail-app-password>` with actual Gmail app password
- `<your-groq-api-key>` with actual Groq API key

### Step 3: Domain Settings

**Custom Domain:**
- Domain: `khr-khr.epu6c6.easypanel.host` (already configured)
- Make sure it points to port 5000

---

## 🔄 Deploy Steps

1. **Save all configuration above**
2. Click **"Rebuild"** button
3. **Wait 3-5 minutes** for build to complete
4. **Watch the logs** during build:
   - Look for: `Successfully built`
   - Look for: `Starting gunicorn`
   - NO errors about missing files

---

## 🧪 Testing After Deployment

### Test 1: Health Check
Open in browser:
```
https://khr-khr.epu6c6.easypanel.host/api/status
```
**Expected:** `{"status": "ok"}`
**If 404:** Backend not running - check logs

### Test 2: Community Impacts API
Open in browser:
```
https://khr-khr.epu6c6.easypanel.host/api/community-impacts/all
```
**Expected:** JSON array with data
**If 404:** Backend not running
**If []:** Database connection issue

### Test 3: Admin Panel Database
1. Go to: https://khr-khr.epu6c6.easypanel.host/admin/
2. Login (username: khr, password: khr@123)
3. Check if data loads from database

---

## 🔍 Troubleshooting

### Issue: Still Getting 404

**Check 1: View Recent Logs**
In Easypanel:
1. Go to your app
2. Click "Logs" tab
3. Look for errors during startup

**Expected logs:**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 7
```

**Bad signs:**
```
Error: ... (any Python error)
ModuleNotFoundError: ...
Database connection failed: ...
```

**Check 2: Verify Port**
- Easypanel port MUST be **5000**
- NOT 80, NOT 3000, NOT 8000

**Check 3: Check Build Logs**
Look for:
```
✅ Successfully built
✅ Successfully tagged
✅ Container started
```

**Check 4: Test Direct Connection**
In Easypanel, try opening a console and run:
```bash
curl http://localhost:5000/api/status
```
If this works but external URL doesn't, it's a routing issue.

### Issue: Build Fails

**Common causes:**
1. `requirements.txt` missing dependencies
2. Database not accessible from Easypanel IP
3. Out of memory during build

**Fix:**
- Check build logs for specific error
- Ensure all Python packages are in `backend/requirements.txt`

### Issue: Database Connection Error

**Check:**
1. Database `72.61.254.168:5432` is accessible from internet
2. Firewall allows Easypanel IPs
3. Credentials in `DATABASE_URL` are correct

**Test locally:**
```bash
psql "postgresql://kishore:kishore*123@72.61.254.168:5432/khr_db"
```

---

## 📋 Pre-Deployment Checklist

Before clicking Rebuild, verify:

- [ ] Branch is `fix/dockerfix`
- [ ] Port is `5000`
- [ ] All environment variables are set
- [ ] `DATABASE_URL` is correct
- [ ] `GROQ_API_KEY` is set
- [ ] `MAIL_PASSWORD` is Gmail app password (not regular password)
- [ ] Dockerfile path is `./Dockerfile`

---

## 🆘 If Still Not Working

**Collect this information:**

1. **Build logs** (last 50 lines)
2. **Runtime logs** (last 50 lines)
3. Screenshot of Easypanel port configuration
4. Result of: `curl https://khr-khr.epu6c6.easypanel.host/api/status`

Then we can diagnose the exact issue.

---

## 📝 What Changed in This Fix

**Before:**
- Tried to run Nginx + Flask together
- Multiple processes caused conflicts
- Port mapping was confusing (80 vs 5000)

**After:**
- **Simple:** Just Flask with gunicorn
- **Clean:** One process, one port (5000)
- **Compatible:** Works with Easypanel's built-in reverse proxy

Easypanel handles the reverse proxy automatically, so we don't need Nginx inside the container.
