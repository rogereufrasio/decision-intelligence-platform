$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$backend = $null
$frontend = $null

function Stop-ProcessTree([int]$ProcessId) {
    Get-CimInstance Win32_Process -Filter "ParentProcessId = $ProcessId" -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-ProcessTree $_.ProcessId }
    Stop-Process -Id $ProcessId -ErrorAction SilentlyContinue
}

try {
    $backend = Start-Process uv -WindowStyle Hidden -PassThru -WorkingDirectory "$repositoryRoot\backend" -ArgumentList "run", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"
    $frontend = Start-Process npm -WindowStyle Hidden -PassThru -WorkingDirectory "$repositoryRoot\frontend" -ArgumentList "run", "dev", "--", "--host", "127.0.0.1"
    Write-Host "Backend: http://127.0.0.1:8000"
    Write-Host "Frontend: http://127.0.0.1:5173"
    Write-Host "Pressione Ctrl+C para encerrar."
    while (-not $backend.HasExited -and -not $frontend.HasExited) {
        Start-Sleep -Seconds 1
    }
} finally {
    if ($backend -and -not $backend.HasExited) { Stop-ProcessTree $backend.Id }
    if ($frontend -and -not $frontend.HasExited) { Stop-ProcessTree $frontend.Id }
}
