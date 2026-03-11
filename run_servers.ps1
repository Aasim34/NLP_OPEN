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
$pythonInstalled = $false
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonInstalled = $true
        Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
    }
}
catch {
    $pythonInstalled = $false
}

if (-not $pythonInstalled) {
    Write-Host "  ✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    Write-Host "    Download: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
$nodeInstalled = $false
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $nodeInstalled = $true
        Write-Host "  ✓ Node.js found: $nodeVersion" -ForegroundColor Green
    }
}
catch {
    $nodeInstalled = $false
}

if (-not $nodeInstalled) {
    Write-Host "  ✗ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    Write-Host "    Download: https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# ==============================================================================
# Check Backend Dependencies
# ==============================================================================

Write-Host ""
Write-Host "[2/5] Checking backend dependencies..." -ForegroundColor Yellow

if (-not (Test-Path $BackendPath)) {
    Write-Host "  ✗ Backend directory not found: $BackendPath" -ForegroundColor Red
    exit 1
}

# Check if uvicorn is installed
$uvicornInstalled = $false
try {
    python -c "import uvicorn" 2>$null
    if ($LASTEXITCODE -eq 0) {
        $uvicornInstalled = $true
    }
}
catch {
    $uvicornInstalled = $false
}

if ($uvicornInstalled) {
    Write-Host "  ✓ Backend dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "  ✗ Backend dependencies missing" -ForegroundColor Red
    Write-Host "    Installing dependencies..." -ForegroundColor Yellow
    
    Push-Location $BackendPath
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    ✗ Failed to install backend dependencies" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    Write-Host "  ✓ Backend dependencies installed successfully" -ForegroundColor Green
}

# ==============================================================================
# Check Frontend Dependencies
# ==============================================================================

Write-Host ""
Write-Host "[3/5] Checking frontend dependencies..." -ForegroundColor Yellow

if (-not (Test-Path $FrontendPath)) {
    Write-Host "  ✗ Frontend directory not found: $FrontendPath" -ForegroundColor Red
    exit 1
}

$nodeModulesPath = Join-Path $FrontendPath "node_modules"
if (-not (Test-Path $nodeModulesPath)) {
    Write-Host "  ✗ Frontend dependencies missing" -ForegroundColor Red
    Write-Host "    Installing dependencies..." -ForegroundColor Yellow
    
    Push-Location $FrontendPath
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    ✗ Failed to install frontend dependencies" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    Write-Host "  ✓ Frontend dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "  ✓ Frontend dependencies installed" -ForegroundColor Green
}

# ==============================================================================
# Start Backend Server
# ==============================================================================

Write-Host ""
Write-Host "[4/5] Starting backend server..." -ForegroundColor Yellow

# Start backend in a new PowerShell window
$backendCommand = "cd '$BackendPath'; Write-Host ''; Write-Host '================================================' -ForegroundColor Cyan; Write-Host '  Backend Server (FastAPI + Uvicorn)' -ForegroundColor Cyan; Write-Host '================================================' -ForegroundColor Cyan; Write-Host ''; Write-Host 'Starting server at: http://127.0.0.1:8000' -ForegroundColor Green; Write-Host 'API Docs: http://127.0.0.1:8000/docs' -ForegroundColor Green; Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow; Write-Host ''; uvicorn main:app --reload"

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand

Write-Host "  ✓ Backend server starting in new window..." -ForegroundColor Green
Write-Host "    URL: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "    Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan

# Wait for backend to start
Write-Host "    Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# ==============================================================================
# Start Frontend Server
# ==============================================================================

Write-Host ""
Write-Host "[5/5] Starting frontend server..." -ForegroundColor Yellow

# Start frontend in a new PowerShell window
$frontendCommand = "cd '$FrontendPath'; Write-Host ''; Write-Host '================================================' -ForegroundColor Cyan; Write-Host '  Frontend Server (Vite + React)' -ForegroundColor Cyan; Write-Host '================================================' -ForegroundColor Cyan; Write-Host ''; Write-Host 'Starting server at: http://localhost:5173' -ForegroundColor Green; Write-Host 'Press Ctrl+C to stop' -ForegroundColor Yellow; Write-Host ''; npm run dev"

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand

Write-Host "  ✓ Frontend server starting in new window..." -ForegroundColor Green
Write-Host "    URL: http://localhost:5173" -ForegroundColor Cyan

# ==============================================================================
# Success Message
# ==============================================================================

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "  🚀 Both servers are starting!" -ForegroundColor Green
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

# ==============================================================================
# Wait for User Input
# ==============================================================================

Write-Host "Press Enter to open the application in your browser..." -ForegroundColor Yellow
Read-Host

# Open browser
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Application opened in your default browser!" -ForegroundColor Green
Write-Host "You can close this window now." -ForegroundColor Gray
Write-Host ""
