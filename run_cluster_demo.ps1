#!/usr/bin/env pwsh
# Run Cluster Demo - Automated Script
# Manages cluster and demo in two processes

Write-Host "`n╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        Distributed Sync System - Cluster Demo        ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Step 1: Kill old Python processes
Write-Host "[1/5] Cleaning up old Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "      ✓ Cleanup complete`n" -ForegroundColor Green

# Step 2: Start cluster in background
Write-Host "[2/5] Starting 3-node cluster..." -ForegroundColor Yellow
$cluster = Start-Process python -ArgumentList "benchmarks/start_cluster.py" -PassThru -WindowStyle Minimized
Start-Sleep -Seconds 8
Write-Host "      ✓ Cluster running (PID: $($cluster.Id))`n" -ForegroundColor Green

# Step 3: Show menu
Write-Host "[3/5] Select demo type:" -ForegroundColor Yellow
Write-Host "      1 - Lock Manager" -ForegroundColor White
Write-Host "      2 - Queue System" -ForegroundColor White
Write-Host "      3 - Cache (MESI)`n" -ForegroundColor White

$choice = Read-Host "Enter choice (1-3)"

# Step 4: Run demo
Write-Host "`n[4/5] Starting demo (connecting to cluster)..." -ForegroundColor Yellow
Write-Host "      Press Ctrl+C to exit when done`n" -ForegroundColor Gray

try {
    echo $choice | python benchmarks/demo_cluster.py
}
finally {
    # Step 5: Cleanup
    Write-Host "`n[5/5] Cleaning up..." -ForegroundColor Yellow
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "      ✓ All processes stopped`n" -ForegroundColor Green
}
