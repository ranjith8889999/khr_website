@echo off
echo ========================================
echo Stopping all Python processes...
echo ========================================
taskkill /F /IM python.exe /T
timeout /t 2

echo.
echo ========================================
echo Starting KHR Website Backend...
echo ========================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Backend starting on http://localhost:5000
echo Press Ctrl+C to stop the server
python backend\app.py
pause
