@echo off
setlocal
cd /d "%~dp0"

echo [StratumWeb] Starting Backend Pipeline...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Virtual Environment Setup
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

:: Install Dependencies
echo [INFO] Ensuring dependencies are up-to-date...
venv\Scripts\python -m pip install -r requirements.txt --quiet

:: Run Application
echo [INFO] Launching StratumWeb Backend...
venv\Scripts\python main.py

if %errorlevel% neq 0 (
    echo [ERROR] Backend failed to start.
    pause
)
endlocal
