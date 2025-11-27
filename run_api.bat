@echo off
REM Script to run the FastAPI application
REM This script activates the virtual environment and starts the uvicorn server

echo.
echo ================================================
echo 🚀 Starting FastAPI Logging Service...
echo ================================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start the uvicorn server
echo 📡 Running on http://localhost:8000
echo 📚 API docs available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
