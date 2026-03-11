# Backend Server Starter
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Backend Server (FastAPI + Uvicorn)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendPath = Join-Path $ScriptDir "language_converter_backend"

# Change to backend directory and start server
Set-Location $BackendPath
uvicorn main:app --reload
