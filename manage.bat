@echo off

:: Activate Virtual Environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: Check if the command is 'runserver'
if "%1"=="runserver" (
    echo ==================================================
    echo  Starting Project Tracker (Full Stack)
    echo ==================================================
    echo 1. Starting React Frontend in a new window...
    start "React Frontend" cmd /k "cd project_tracker/frontend && npm run dev"
    
    echo 2. Starting Django Backend...
    cd project_tracker
    python manage.py runserver
) else (
    :: Forward all other commands (migrate, createsuperuser, etc.) to actual manage.py
    cd project_tracker
    python manage.py %*
)
