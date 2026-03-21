@echo off
echo ========================================
echo STEP 1: Stopping Wrong Python Processes
echo ========================================
taskkill /F /IM python.exe /T 2>nul
echo Done!
timeout /t 2

echo.
echo ========================================  
echo STEP 2: Installing Missing Packages
echo ========================================
call .venv\Scripts\activate.bat
python -m pip install Flask-Mail==0.9.1 groq==0.4.2 psycopg2-binary==2.9.9 gunicorn==21.2.0
echo Done!
timeout /t 2

echo.
echo ========================================
echo STEP 3: Starting KHR Backend Server  
echo ========================================
echo.
echo Server will start on: http://localhost:5000
echo.
echo IMPORTANT:
echo  1. Keep this window OPEN
echo  2. Open browser to: http://localhost:5000/
echo  3. DO NOT open index.html directly as a file
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.
python backend\app.py
pause
