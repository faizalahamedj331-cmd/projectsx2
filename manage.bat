@echo off
REM Wrapper manage.bat placed at repository root to forward commands
REM to the actual Django project manage.bat located in projectsx2-main\projectsx2-main

pushd "%~dp0projectsx2-main\projectsx2-main"
call manage.bat %*
set RC=%ERRORLEVEL%
popd
exit /b %RC%
