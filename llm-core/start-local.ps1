# PowerShell script to start the server locally
# Usage: .\start-local.ps1

Write-Host "🔧 llm-core Local Development Server" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Cyan

# Check if we're in the correct directory
if (-not (Test-Path "app\main.py")) {
    Write-Host "❌ Error: Run this script from the llm-core project root" -ForegroundColor Red
    exit 1
}

# Load environment variables if .env file exists
if (Test-Path ".env") {
    Write-Host "📋 Loading environment variables from .env..." -ForegroundColor Green
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#][^=]+)=(.+)$") {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
} else {
    Write-Host "⚠️  .env file not found, using default values" -ForegroundColor Yellow
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Blue
try {
    python -m pip install -r requirements.txt
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Error installing dependencies: $_" -ForegroundColor Red
    exit 1
}

# Get configurations
$host_addr = if ($env:HOST) { $env:HOST } else { "127.0.0.1" }
$port = if ($env:PORT) { $env:PORT } else { "8001" }
$log_level = if ($env:LOG_LEVEL) { $env:LOG_LEVEL } else { "info" }
$debug = if ($env:DEBUG) { $env:DEBUG.ToLower() -eq "true" } else { $true }

Write-Host "🚀 Starting server on http://$host_addr`:$port" -ForegroundColor Green
Write-Host "📄 API documentation available at http://$host_addr`:$port/docs" -ForegroundColor Green
Write-Host "🔄 Auto-reload: $(if ($debug) { 'Enabled' } else { 'Disabled' })" -ForegroundColor Green
Write-Host "📝 Log level: $log_level" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

# Build the command
$cmd = @("python", "-m", "uvicorn", "app.main:app", "--host", $host_addr, "--port", $port, "--log-level", $log_level)
if ($debug) {
    $cmd += "--reload"
}

# Start the server
try {
    & $cmd[0] $cmd[1..($cmd.Length-1)]
} catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
}