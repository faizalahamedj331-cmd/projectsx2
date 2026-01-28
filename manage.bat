@echo off
REM manage.bat - wrapper to run Django manage.py using the project's venv Python
REM Usage: manage.bat runserver  or manage.bat migrate

setlocal
set "ROOT=%~dp0"
set "VENV_PY=%ROOT%project_tracker\venv\Scripts\python.exe"
if exist "%VENV_PY%" (
    "%VENV_PY%" "%ROOT%project_tracker\manage.py" %*
) else (
    REM Fall back to system python if venv python not found
    python "%ROOT%project_tracker\manage.py" %*
)
endlocal
