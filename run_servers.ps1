# ==============================================================================
# Indian Code-Mixed Language Converter - Server Launcher
# ==============================================================================
# This script starts both the FastAPI backend and React frontend servers
# in separate terminal windows.
#
# Usage:
#   .\run_servers.ps1
#
# Requirements:
#   - Python 3.11+ with backend dependencies installed
#   - Node.js 18+ with frontend dependencies installed
# ==============================================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Indian Code-Mixed Language Converter - Server Launcher" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory (project root)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Define paths
$BackendPath = Join-Path $ProjectRoot "language_converter_backend"
$FrontendPath = Join-Path $ProjectRoot "Frontend"

# ==============================================================================
# Check Prerequisites
# ==============================================================================

Write-Host "[1/5] Checking prerequisites..." -ForegroundColor Yellow

# Check if Python is installed
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  X Python not found. Please install Python 3.11+" -ForegroundColor Red
    Write-Host "    Download: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host "  OK Python found: $pythonCheck" -ForegroundColor Green

# Check if Node.js is installed
$nodeCheck = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  X Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    Write-Host "    Download: https://nodejs.org/" -ForegroundColor Red
    exit 1
}
Write-Host "  OK Node.js found: $nodeCheck" -ForegroundColor Green

# ==============================================================================
# Check Backend Dependencies
# ==============================================================================

Write-Host ""
Write-Host "[2/5] Checking backend dependencies..." -ForegroundColor Yellow

if (-not (Test-Path $BackendPath)) {
    Write-Host "  X Backend directory not found: $BackendPath" -ForegroundColor Red
    exit 1
}

# Check if uvicorn is installed
python -c "import uvicorn" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK Backend dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "  X Backend dependencies missing" -ForegroundColor Red
    Write-Host "    Installing dependencies..." -ForegroundColor Yellow
    
    Push-Location $BackendPath
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    X Failed to install backend dependencies" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    Write-Host "  OK Backend dependencies installed successfully" -ForegroundColor Green
}

# ==============================================================================
# Check Frontend Dependencies
# ==============================================================================

Write-Host ""
Write-Host "[3/5] Checking frontend dependencies..." -ForegroundColor Yellow

if (-not (Test-Path $FrontendPath)) {
    Write-Host "  X Frontend directory not found: $FrontendPath" -ForegroundColor Red
    exit 1
}

$nodeModulesPath = Join-Path $FrontendPath "node_modules"
if (-not (Test-Path $nodeModulesPath)) {
    Write-Host "  X Frontend dependencies missing" -ForegroundColor Red
    Write-Host "    Installing dependencies..." -ForegroundColor Yellow
    
    Push-Location $FrontendPath
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    X Failed to install frontend dependencies" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    Write-Host "  OK Frontend dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "  OK Frontend dependencies installed" -ForegroundColor Green
}

# ==============================================================================
# Start Backend Server
# ==============================================================================

Write-Host ""
Write-Host "[4/5] Starting backend server..." -ForegroundColor Yellow

# Start backend script in new window
$backendScript = Join-Path $ProjectRoot "start_backend.ps1"
Start-Process powershell -ArgumentList "-NoExit","-ExecutionPolicy","Bypass","-File",$backendScript

Write-Host "  OK Backend server starting in new window..." -ForegroundColor Green
Write-Host "     URL: http://127.0.0.1:8000" -ForegroundColor Cyan

# Wait for backend to start
Write-Host "     Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

# ==============================================================================
# Start Frontend Server
# ==============================================================================

Write-Host ""
Write-Host "[5/5] Starting frontend server..." -ForegroundColor Yellow

# Start frontend script in new window
$frontendScript = Join-Path $ProjectRoot "start_frontend.ps1"
Start-Process powershell -ArgumentList "-NoExit","-ExecutionPolicy","Bypass","-File",$frontendScript

Write-Host "  OK Frontend server starting in new window..." -ForegroundColor Green
Write-Host "     URL: http://localhost:5173" -ForegroundColor Cyan

# ==============================================================================
# Verify Servers Started
# ==============================================================================

Write-Host ""
Write-Host "Waiting for servers to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Check if backend is running
$backendConn = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($backendConn) {
    Write-Host "  OK Backend verified running on port 8000" -ForegroundColor Green
}
else {
    Write-Host "  ! Backend may not have started. Check the backend window." -ForegroundColor Yellow
}

# Check if frontend is running
$frontendConn = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
if ($frontendConn) {
    Write-Host "  OK Frontend verified running on port 5173" -ForegroundColor Green
}
else {
    Write-Host "  ! Frontend may not have started. Check the frontend window." -ForegroundColor Yellow
}

# ==============================================================================
# Success Message
# ==============================================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  Servers are ready!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend (API):      http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Frontend (UI):      http://localhost:5173" -ForegroundColor Cyan
Write-Host "API Documentation:  http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open your browser and navigate to:" -ForegroundColor Yellow
Write-Host "  http://localhost:5173" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host ""
Write-Host "To stop the servers:" -ForegroundColor Yellow
Write-Host "  - Press Ctrl+C in each server window" -ForegroundColor White
Write-Host "  - Or close the PowerShell windows" -ForegroundColor White
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# Open browser
Start-Process "http://localhost:5173"

Write-Host "Application opened in your default browser!" -ForegroundColor Green
Write-Host "You can close this window now. The servers are running in separate windows." -ForegroundColor Cyan
Write-Host ""
