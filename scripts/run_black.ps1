<#
PowerShell helper to run Black using the project's .venv if available.
Run from workspace root (or call this script from anywhere):
  .\scripts\run_black.ps1
#>

$root = Split-Path -Parent $PSScriptRoot
$venv_activate = Join-Path $root ".venv\Scripts\Activate.ps1"

if (Test-Path $venv_activate) {
    Write-Host "Activating .venv..."
    & $venv_activate
} else {
    Write-Host ".venv not found, using system Python environment"
}

Write-Host "Running: black . (from $root)"
Push-Location $root
try {
    & black .
} catch {
    Write-Host "Error running black:" $_.Exception.Message -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}

Write-Host "Black finished." -ForegroundColor Green
