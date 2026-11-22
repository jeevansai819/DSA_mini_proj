# PowerShell helper to start Zookeeper and Kafka
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent $ScriptDir
$KafkaHome = "C:\kafka"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Starting Apache Kafka & Zookeeper" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Start Zookeeper in background window
Write-Host "[1/2] Launching Zookeeper on localhost:2181..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Starting Zookeeper...' -ForegroundColor Yellow; cmd.exe /c '$KafkaHome\bin\windows\zookeeper-server-start.bat $KafkaHome\config\zookeeper.properties'"

Start-Sleep -Seconds 5

# 2. Start Kafka broker in background window
Write-Host "[2/2] Launching Kafka Broker on localhost:9092..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Starting Kafka Broker...' -ForegroundColor Yellow; cmd.exe /c '$KafkaHome\bin\windows\kafka-server-start.bat $KafkaHome\config\server.properties'"

Start-Sleep -Seconds 7

# 3. Create topic
Write-Host "Initializing Kafka topic 'traffic-events'..." -ForegroundColor Green
& "$ProjectDir\.venv\Scripts\python.exe" "$ProjectDir\scripts\create_topic.py"

Write-Host "Apache Kafka broker is ready." -ForegroundColor Green
