@echo off
echo ==============================================
echo Zomato AI - Local Startup Script
echo ==============================================

echo [1/3] Setting up Python virtual environment...
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate
echo Installing backend dependencies...
pip install -r requirements.txt

echo [2/3] Building the frontend UI...
cd frontend
call npm install
call npm run build
cd ..

echo [3/3] Starting the FastAPI server...
echo ==============================================
echo Please open your browser and navigate to:
echo http://127.0.0.1:8000
echo ==============================================
python -m src.main --server
pause
