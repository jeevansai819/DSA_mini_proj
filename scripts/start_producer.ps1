# PowerShell helper to start Traffic Event Producer
param (
    [string]$Mode = "NORMAL_TRAFFIC",
    [string]$Source = "scenario",
    [float]$Interval = 1.0
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Starting Traffic Event Producer ($Mode)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Set-Location $ProjectDir
& "$ProjectDir\.venv\Scripts\python.exe" "$ProjectDir\producer\traffic_producer.py" --mode $Mode --source $Source --interval $Interval
