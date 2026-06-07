@echo off
setlocal
cd /d "%~dp0"
echo [StratumWeb] Running Bulletproof Backend Fix...

:: 1. Force kill existing Python instances to release DB locks
echo [1/4] Cleaning existing processes...
taskkill /F /IM python.exe /T >nul 2>&1

:: 2. Ensure Virtual Env
if not exist venv (
    echo [2/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/4] Virtual environment exists.
)

:: 3. Reinstall requirements just in case
echo [3/4] Validating dependencies...
venv\Scripts\python -m pip install -r requirements.txt --quiet

:: 4. Start fresh
echo [4/4] Starting StratumWeb Lead Engine...
echo --------------------------------------------------
echo ACCESS DASHBOARD AT: http://localhost:8000/admin?pass=stratum_admin
echo --------------------------------------------------
venv\Scripts\python main.py

pause
endlocal
