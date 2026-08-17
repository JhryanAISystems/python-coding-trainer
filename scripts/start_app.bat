@echo off
setlocal
set "ROOT=%~dp0.."

REM --- Backend ---
cd /d "%ROOT%\backend"
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Installing backend dependencies...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)
start "Python Coding Trainer - Backend" cmd /k "cd /d "%ROOT%\backend" && .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM --- Frontend ---
cd /d "%ROOT%\frontend"
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)
start "Python Coding Trainer - Frontend" cmd /k "cd /d "%ROOT%\frontend" && npm run dev"

REM --- Open the app once the frontend is ready ---
timeout /t 6 /nobreak >nul
start "" "http://localhost:5173"

endlocal
