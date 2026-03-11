# Frontend Server Starter
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Frontend Server (Vite + React)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: http://localhost:5173" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$FrontendPath = Join-Path $ScriptDir "Frontend"

# Change to frontend directory and start server
Set-Location $FrontendPath
npm run dev
