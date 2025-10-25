#!/usr/bin/env pwsh
# Run Standalone Demo - Automated Script
# Kills old Python processes and runs fresh demo

Write-Host "`n╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       Distributed Sync System - Standalone Demo      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Step 1: Kill old Python processes
Write-Host "[1/3] Cleaning up old Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "      ✓ Cleanup complete`n" -ForegroundColor Green

# Step 2: Show menu
Write-Host "[2/3] Select demo type:" -ForegroundColor Yellow
Write-Host "      1 - Lock Manager" -ForegroundColor White
Write-Host "      2 - Queue System" -ForegroundColor White
Write-Host "      3 - Cache (MESI)`n" -ForegroundColor White

$choice = Read-Host "Enter choice (1-3)"

# Step 3: Run demo
Write-Host "`n[3/3] Starting demo..." -ForegroundColor Yellow
Write-Host "      Press Ctrl+C to exit when done`n" -ForegroundColor Gray

echo $choice | python benchmarks/demo_standalone.py
