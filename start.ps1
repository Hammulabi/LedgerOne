$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location "$RootDir\backend"
if (-Not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\Activate.ps1"
pip install -r requirements.txt
python scripts/init_db.py

$backend = Start-Process -PassThru python -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Set-Location $RootDir
$frontend = Start-Process -PassThru python -ArgumentList "-m http.server 8080 --directory frontend"

Write-Host "Backend: http://127.0.0.1:8000"
Write-Host "Frontend: http://127.0.0.1:8080"
Write-Host "Press Enter to stop both services"
[void][System.Console]::ReadLine()

Stop-Process -Id $backend.Id,$frontend.Id
