# PowerShell helper to cleanly stop all running traffic processes
Write-Host "Stopping all Traffic Pipeline processes..." -ForegroundColor Yellow

# Stop Python and Streamlit instances associated with the project
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*Real_Time_Traffic_Congestion*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process streamlit -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Stop Kafka and Zookeeper batch instances
Write-Host "Stopping Kafka Broker..." -ForegroundColor Yellow
cmd.exe /c "C:\kafka\bin\windows\kafka-server-stop.bat"
Start-Sleep -Seconds 2

Write-Host "Stopping Zookeeper..." -ForegroundColor Yellow
cmd.exe /c "C:\kafka\bin\windows\zookeeper-server-stop.bat"

Write-Host "All traffic pipeline services stopped." -ForegroundColor Green
