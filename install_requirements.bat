@echo off
REM Install Python dependencies for Keydrop Bot

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+ and ensure it is in your PATH.
    pause
    exit /b 1
)

python -m pip install --upgrade pip

REM Install libraries required by the backend (FastAPI + Playwright)
python -m pip install -r bot_keydrop\backend\requirements.txt

REM Install Playwright browsers
python -m playwright install

echo.
echo All requirements installed!
pause
