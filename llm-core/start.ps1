# Simple PowerShell script to start the server
# Usage: .\start.ps1

Write-Host "Starting llm-core server..." -ForegroundColor Green

# Check if we're in the correct directory
if (!(Test-Path "app\main.py")) {
    Write-Host "Error: Run this script from the llm-core project root" -ForegroundColor Red
    exit 1
}

# Use the Python script to start the server
python run_local.py