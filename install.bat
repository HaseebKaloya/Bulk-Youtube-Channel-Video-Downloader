@echo off
echo ============================================
echo YouTube Channel Downloader - Installation
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [OK] pip found
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing required packages...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install requirements
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ============================================
echo Installation completed successfully!
echo ============================================
echo.
echo IMPORTANT: Make sure FFmpeg is installed
echo.
echo To install FFmpeg:
echo 1. Download from: https://ffmpeg.org/download.html
echo 2. Extract and add bin folder to PATH
echo.
echo OR use Chocolatey:
echo    choco install ffmpeg
echo.
echo To verify FFmpeg installation, run:
echo    ffmpeg -version
echo.
echo ============================================
echo You can now run the downloader:
echo    python main.py --interactive
echo ============================================
echo.
pause
