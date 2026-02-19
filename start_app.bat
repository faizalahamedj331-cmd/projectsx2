@echo off
echo ==========================================
echo       Project Tracker - Startup Script
echo ==========================================
echo.

:: Check for venv and activate
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Virtual environment not found in .venv. Assuming global python or manual activation.
)

:: Start Backend
echo Starting Django Backend (Port 8000)...
start "Django Backend" cmd /k "cd project_tracker && python manage.py runserver"

:: Start Frontend
echo Starting React Frontend (Port 5173)...
start "React Frontend" cmd /k "cd project_tracker/frontend && npm run dev"

echo.
echo ==========================================
echo Servers are launching in separate windows.
echo.
echo Backend URL: http://127.0.0.1:8000/
echo Frontend URL: http://localhost:5173/
echo.
echo You can close this window now.
echo ==========================================
pause
