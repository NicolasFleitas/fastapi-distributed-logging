# Script to run the FastAPI application
# This script activates the virtual environment and starts the uvicorn server

Write-Host "🚀 Starting FastAPI Logging Service..." -ForegroundColor Green

# Activate virtual environment
& "$PSScriptRoot\.venv\Scripts\Activate.ps1"

# Start the uvicorn server
Write-Host "📡 Running on http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API docs available at http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "" 
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Gray

uvicorn main:app --reload --host 0.0.0.0 --port 8000
