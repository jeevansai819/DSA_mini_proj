# PowerShell helper to start Streamlit Dashboard
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Launching Streamlit Traffic Dashboard" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Set-Location $ProjectDir
& "$ProjectDir\.venv\Scripts\python.exe" -m streamlit run "$ProjectDir\dashboard\app.py" --server.port 8501 --server.headless false
