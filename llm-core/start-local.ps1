# ==============================================
# llm-core - Avvio ambiente locale (development)
# Uso:  .\start-local.ps1
# ==============================================

$ErrorActionPreference = "Stop"

Write-Host "🔧 llm-core - Local Development Server" -ForegroundColor Cyan
Write-Host ("=" * 50) -ForegroundColor Cyan

function Load-EnvFile {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path $Path)) {
        Write-Host "❌ Env file '$Path' non trovato" -ForegroundColor Red
        exit 1
    }

    Write-Host "📋 Carico variabili da $Path" -ForegroundColor Green

    Get-Content $Path | ForEach-Object {
        if ($_ -match '^\s*$' -or $_ -match '^\s*#') { return }

        if ($_ -match '^\s*([^#=]+?)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
}

# 1) Controllo cartella
if (-not (Test-Path "app\main.py")) {
    Write-Host "❌ Error: esegui questo script dalla root del progetto llm-core" -ForegroundColor Red
    exit 1
}

# 2) Carica env locale
$envFile = ".env.local"
Load-EnvFile -Path $envFile

# 3) Installa dipendenze (se vuoi, puoi rimuoverlo dopo la prima volta)
Write-Host "📦 Installazione dipendenze (requirements.txt)..." -ForegroundColor Blue
python -m pip install -r requirements.txt

# 4) Leggi alcune info per log
$host_addr = if ($env:HOST) { $env:HOST } else { "127.0.0.1" }
$port      = if ($env:PORT) { $env:PORT } else { "8001" }
$log_level = if ($env:LOG_LEVEL) { $env:LOG_LEVEL } else { "info" }
$debug     = if ($env:DEBUG) { $env:DEBUG.ToLower() -eq "true" } else { $true }

Write-Host "🚀 Avvio server su http://$host_addr`:$port" -ForegroundColor Green
Write-Host "📄 Docs: http://$host_addr`:$port/docs" -ForegroundColor Green
Write-Host "🔄 Auto-reload: $(if ($debug) { 'Enabled' } else { 'Disabled' })" -ForegroundColor Green
Write-Host "📝 Log level: $log_level" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

# 5) Avvia uvicorn (come nel tuo main.py / run_local.py)
$cmd = @(
    "python", "-m", "uvicorn",
    "app.main:app",
    "--host", $host_addr,
    "--port", $port,
    "--log-level", $log_level
)

if ($debug) {
    $cmd += "--reload"
}

try {
    & $cmd[0] $cmd[1..($cmd.Length-1)]
} catch {
    Write-Host "❌ Errore nell'avvio del server: $_" -ForegroundColor Red
}