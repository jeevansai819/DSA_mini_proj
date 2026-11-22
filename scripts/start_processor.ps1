# PowerShell helper to start Traffic Stream Processor
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Starting Python Traffic Stream Processor" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Set-Location $ProjectDir
& "$ProjectDir\.venv\Scripts\python.exe" "$ProjectDir\processor\traffic_processor.py"
