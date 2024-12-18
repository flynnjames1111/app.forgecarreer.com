@echo off
echo Setting up ResumeAI with Gemini AI...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r backend\requirements.txt

REM Run the application
cd backend
python app.py

pause
