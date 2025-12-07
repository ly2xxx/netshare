@echo off
REM Launcher script for Holiday Greeting QR Code Generator (Windows)

echo.
echo 🎄 Starting Holiday Greeting QR Code Generator...
echo.

REM Check if streamlit is installed
where streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Streamlit is not installed.
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "app.py" (
    echo ❌ app.py not found. Please run this script from the streamlit directory.
    pause
    exit /b 1
)

echo ✅ All checks passed!
echo 🚀 Launching application...
echo.

REM Run streamlit
streamlit run app.py

pause
