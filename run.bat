@echo off
echo ============================================
echo YouTube Channel Downloader
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Run the downloader in interactive mode
python main.py --interactive

pause
