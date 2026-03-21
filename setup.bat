@echo off
REM Kolan Hanmanth Reddy Website - Setup Script for Windows

echo.
echo ============================================
echo Kolan Hanmanth Reddy - Website Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Python found!
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
cd backend
pip install -r requirements.txt
cd ..
echo Dependencies installed!
echo.

REM Initialize database
echo [5/5] Initializing database...
cd backend
python -c "from app import init_db; init_db()"
cd ..
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the website:
echo.
echo 1. Activate virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Start Flask backend:
echo    cd backend
echo    python app.py
echo.
echo 3. Open index.html in your browser
echo.
echo Admin Panel:
echo - Login at /admin/login.html
echo - Default username: khr
echo - Default password: khr@123
echo.
echo ============================================
echo.
pause
