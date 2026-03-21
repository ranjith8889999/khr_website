# ⚠️ CRITICAL: Your Backend Is Not Running Correctly

## Current Problem

You have the **WRONG Flask application** running on port 5000. It's serving a "Police RAG System" instead of the KHR website backend.

---

## Quick Fix (3 Steps)

### Step 1: Stop All Python Processes

**Option A - PowerShell:**
```powershell
Get-Process python | Stop-Process -Force
```

**Option B - Task Manager:**
- Press `Ctrl+Shift+Esc`
- Find all `python.exe` processes
- Right-click → End Task

---

### Step 2: Start the CORRECT Backend

**Open a NEW PowerShell terminal:**
```powershell
cd C:\Users\Ranjit\Desktop\khr\khr1
.\.venv\Scripts\Activate.ps1
python backend\app.py
```

**You should see:**
```
 * Serving Flask app 'backend.app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**OR use the batch file:**
```cmd
start_backend.bat
```

---

### Step 3: Access Website Through Flask Server

**DO NOT open `index.html` directly as a file!**

Instead, open in browser:
```
http://localhost:5000/
```

Or:
```
http://localhost:5000/index.html
```

---

## How to Verify It's Working

### Test 1: Root Page
```
http://localhost:5000/
```
Should show: **Kolan Hanmanth Reddy** website (not Police RAG)

### Test 2: API Status
```
http://localhost:5000/api/status
```
Should return: `{"status": "ok"}`

### Test 3: Gallery API
```
http://localhost:5000/api/gallery
```
Should return JSON data

---

## Why This Happened

You likely:
1. Have multiple Python projects in different folders
2. Started a different Flask app accidentally
3. That app is occupying port 5000
4. Your KHR backend can't start

---

## Common Mistakes to Avoid

### ❌ DON'T DO THIS:
- Double-clicking `index.html` (opens as `file:///`)
- Running `python app.py` (looking for wrong file)
- Starting server in wrong directory

### ✅ DO THIS:
- Always activate virtual environment first
- Run `python backend/app.py` from project root
- Access via `http://localhost:5000/`
- Keep terminal open to see logs

---

## Expected Backend Logs

When KHR backend starts correctly:
```
==================================================
EMAIL CONFIGURATION:
MAIL_SERVER: smtp.gmail.com
MAIL_PORT: 587
MAIL_USE_TLS: True
MAIL_USERNAME: ranjith888999@gmail.com
==================================================
 * Serving Flask app 'backend.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

When form is submitted:
```
INFO: Complaint submitted - Ref: CPL-20260321-XXXX
✓ Complaint confirmation email sent to user@email.com
```

---

## Troubleshooting

### Port Already in Use?
```powershell
# Kill process on port 5000
$port = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($port) { Stop-Process -Id $port.OwningProcess -Force }
```

### Can't Activate Virtual Environment?
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Backend Won't Start?
Check if requirements are installed:
```powershell
pip list | Select-String "Flask|SQLAlchemy|psycopg2"
```

---

## Quick Test Script

Save as `test_backend.ps1`:
```powershell
# Test if correct backend is running
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/status" -ErrorAction SilentlyContinue
if ($response.StatusCode -eq 200) {
    Write-Host "✅ Backend is running!" -ForegroundColor Green
} else {
    Write-Host "❌ Backend not responding!" -ForegroundColor Red
}
```

---

## Summary

**Current State:** ❌ Wrong Flask app running  
**Required Action:** Stop all Python processes, start correct backend  
**Access Method:** http://localhost:5000/ (not file://)  
**Success Indicator:** Forms work, emails send, data loads from database
