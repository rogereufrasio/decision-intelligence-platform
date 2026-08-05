$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$backend = $null
$frontend = $null

try {
    $backend = Start-Process powershell -WindowStyle Hidden -PassThru -WorkingDirectory "$repositoryRoot\backend" -ArgumentList "-NoProfile", "-Command", "uv run uvicorn src.main:app --host 127.0.0.1 --port 8000"
    $frontend = Start-Process powershell -WindowStyle Hidden -PassThru -WorkingDirectory "$repositoryRoot\frontend" -ArgumentList "-NoProfile", "-Command", "npm run dev -- --host 127.0.0.1"
    Write-Host "Backend: http://127.0.0.1:8000"
    Write-Host "Frontend: http://127.0.0.1:5173"
    Write-Host "Pressione Ctrl+C para encerrar."
    while (-not $backend.HasExited -and -not $frontend.HasExited) {
        Start-Sleep -Seconds 1
    }
} finally {
    if ($backend -and -not $backend.HasExited) { Stop-Process -Id $backend.Id }
    if ($frontend -and -not $frontend.HasExited) { Stop-Process -Id $frontend.Id }
}
