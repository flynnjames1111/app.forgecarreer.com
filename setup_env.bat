@echo off
echo Setting up ResumeAI Python Environment...

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

REM Install dependencies
pip install --upgrade pip
pip install -r backend\requirements.txt

echo.
echo Environment setup complete! 
echo To activate the environment in the future, run: venv\Scripts\activate
pause
