# ==============================================
# llm-core - Avvio ambiente produzione
# Uso:  .\start-production.ps1
# ==============================================

$ErrorActionPreference = "Stop"

Write-Host "🏭 llm-core - Production Server" -ForegroundColor Cyan
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

# 2) Carica env di produzione
$envFile = ".env.production"
Load-EnvFile -Path $envFile

# 3) (Opzionale) installa dipendenze - in produzione spesso lo fai solo in fase deploy
Write-Host "📦 Controllo dipendenze..." -ForegroundColor Blue
python -m pip install -r requirements.txt

# 4) Leggi configurazione
$host_addr = if ($env:HOST) { $env:HOST } else { "0.0.0.0" }
$port      = if ($env:PORT) { $env:PORT } else { "8001" }
$log_level = if ($env:LOG_LEVEL) { $env:LOG_LEVEL } else { "info" }

Write-Host "🚀 Avvio server PRODUZIONE su http://$host_addr`:$port" -ForegroundColor Green
Write-Host "📝 Log level: $log_level" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Cyan

# 5) Avvia uvicorn SENZA reload
$cmd = @(
    "python", "-m", "uvicorn",
    "app.main:app",
    "--host", $host_addr,
    "--port", $port,
    "--log-level", $log_level
)

try {
    & $cmd[0] $cmd[1..($cmd.Length-1)]
} catch {
    Write-Host "❌ Errore nell'avvio del server: $_" -ForegroundColor Red
}