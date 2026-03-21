# 🚀 EASYPANEL DEPLOYMENT GUIDE

## Current Issue Analysis

Your deployment is failing because:
1. **Flask backend is not running** - API requests return 404
2. **Nginx is serving files directly** - not proxying to Flask app
3. **Missing production server** - Flask dev server not suitable for production

## Fix for EasyPanel Deployment

### Step 1: Update EasyPanel Configuration

In your EasyPanel dashboard, configure:

**Build Command:**
```bash
pip install -r backend/requirements.txt
```

**Start Command:**
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile - backend.app:app
```

**Port:** `5000` (or use environment variable `$PORT`)

### Step 2: Set Environment Variables

Add these in EasyPanel Environment Variables section:

```
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://kishore:kishore*123@72.61.254.168:5432/khr_db
SECRET_KEY=kolan-hanmanth-reddy-2024-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=ranjith888999@gmail.com
MAIL_PASSWORD=your-gmail-app-password-here
MAIL_DEFAULT_SENDER=ranjith888999@gmail.com
GROQ_API_KEY=your-groq-api-key-here
ADMIN_USERNAME=khr
ADMIN_PASSWORD=khr@123
```

### Step 3: Nginx Configuration (if using Nginx)

If EasyPanel uses Nginx, add this configuration:

```nginx
location /api/ {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location / {
    root /app;
    try_files $uri $uri/ /index.html;
}
```

### Step 4: Health Check Endpoint

Use this for health checks:
```
/api/status
```

---

## Alternative: Using Docker

If EasyPanel supports Docker, upload these files:

1. **Dockerfile** ✅ (already created)
2. **docker-compose.yml** ✅ (already created)
3. **.dockerignore** ✅ (already created)

Then in EasyPanel:
- **Deployment Type:** Docker
- **Dockerfile:** `./Dockerfile`
- **Port:** 5000

---

## Quick Fix Commands

### Rebuild and Deploy:
```bash
# Commit new deployment files
git add .
git commit -m "Add production deployment configuration"
git push origin main
```

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
