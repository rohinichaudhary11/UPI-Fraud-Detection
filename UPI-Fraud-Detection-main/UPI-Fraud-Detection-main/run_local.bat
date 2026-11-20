@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3.11 --version >nul 2>&1
  if errorlevel 1 (
    echo Python 3.11 is required. Install Python 3.11, then run this file again.
    echo Setup details: LOCAL_SETUP.md
    pause
    exit /b 1
  )
  echo Creating the project environment...
  py -3.11 -m venv .venv
  if errorlevel 1 goto setup_failed
  echo Installing project dependencies...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto setup_failed
)
set "OPEN_BROWSER=1"
".venv\Scripts\python.exe" app.py
exit /b %errorlevel%

:setup_failed
echo Setup did not finish. See LOCAL_SETUP.md for troubleshooting.
pause
