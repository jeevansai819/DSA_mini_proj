<#
.SYNOPSIS
    Master Pipeline Launcher for Real-Time Traffic Congestion & Accident Detection System.
.DESCRIPTION
    Integrates and launches the complete 6-layer streaming analytics platform:
    1. Checks environment (Java, Python, Kafka).
    2. Ensures database and ML model are initialized.
    3. Launches Zookeeper, Kafka broker, Stream Processor, Producer, and Streamlit Dashboard.
#>

$ErrorActionPreference = "Stop"
$ProjectDir = $PSScriptRoot
Set-Location $ProjectDir

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " REAL-TIME TRAFFIC CONGESTION & ACCIDENT DETECTION SYSTEM" -ForegroundColor Cyan
Write-Host " Six-Layer Streaming Architecture (Kafka • Python • ML • SQLite • UI)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Environment Verification
Write-Host "`n[Step 1/6] Verifying Environment..." -ForegroundColor Yellow

$PythonExe = "$ProjectDir\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "Error: Virtual environment not found at $PythonExe." -ForegroundColor Red
    Write-Host "Please run: C:\Users\Dell\AppData\Local\Programs\Python\Python311\python.exe -m venv .venv" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] Python Environment: $PythonExe" -ForegroundColor Green

$KafkaHome = "C:\kafka"
if (-not (Test-Path $KafkaHome)) {
    Write-Host "Error: Apache Kafka directory not found at $KafkaHome." -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] Apache Kafka Home: $KafkaHome" -ForegroundColor Green

# 2. Database Initialization
Write-Host "`n[Step 2/6] Initializing SQLite Database..." -ForegroundColor Yellow
& $PythonExe "$ProjectDir\database\db_setup.py"
Write-Host "  [OK] Database initialized at database/traffic_analytics.db" -ForegroundColor Green

# 3. Model Verification / Training
Write-Host "`n[Step 3/6] Verifying Isolation Forest ML Model..." -ForegroundColor Yellow
$ModelFile = "$ProjectDir\models\isolation_forest.pkl"
if (-not (Test-Path $ModelFile)) {
    Write-Host "  Model artifact missing. Initiating training pipeline..." -ForegroundColor Yellow
    & $PythonExe "$ProjectDir\ml\train_model.py"
}
Write-Host "  [OK] Machine Learning Model verified at models/isolation_forest.pkl" -ForegroundColor Green

# 4. Kafka & Zookeeper Verification
Write-Host "`n[Step 4/6] Checking Apache Kafka & Zookeeper Services..." -ForegroundColor Yellow

function Test-Port($Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $client.Connect("127.0.0.1", $Port)
        $connected = $client.Connected
        $client.Close()
        return $connected
    } catch {
        return $false
    }
}

if (-not (Test-Port 2181)) {
    Write-Host "  Starting Zookeeper on port 2181..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Zookeeper Service Window' -ForegroundColor Yellow; cmd.exe /c '$KafkaHome\bin\windows\zookeeper-server-start.bat $KafkaHome\config\zookeeper.properties'"
    Start-Sleep -Seconds 6
} else {
    Write-Host "  [OK] Zookeeper already running on port 2181." -ForegroundColor Green
}

if (-not (Test-Port 9092)) {
    Write-Host "  Starting Kafka Broker on port 9092..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Kafka Broker Service Window' -ForegroundColor Yellow; cmd.exe /c '$KafkaHome\bin\windows\kafka-server-start.bat $KafkaHome\config\server.properties'"
    Start-Sleep -Seconds 8
} else {
    Write-Host "  [OK] Kafka Broker already running on port 9092." -ForegroundColor Green
}

# Create topic
Write-Host "  Checking Kafka topic 'traffic-events'..." -ForegroundColor Yellow
& $PythonExe "$ProjectDir\scripts\create_topic.py"
Write-Host "  [OK] Topic 'traffic-events' is ready." -ForegroundColor Green

# 5. Launch Stream Processor
Write-Host "`n[Step 5/6] Launching Python Stream Processor..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Traffic Stream Processor (Layer 3 & 4)' -ForegroundColor Cyan; cd '$ProjectDir'; & '$PythonExe' 'processor/traffic_processor.py'"
Start-Sleep -Seconds 3
Write-Host "  [OK] Stream processor running in dedicated window." -ForegroundColor Green

# 6. Launch Producer & Dashboard
Write-Host "`n[Step 6/6] Launching Producer & Streamlit Live Dashboard..." -ForegroundColor Yellow

# Launch Traffic Producer
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Traffic Event Producer (Layer 1 & 2)' -ForegroundColor Cyan; cd '$ProjectDir'; & '$PythonExe' 'producer/traffic_producer.py' --interval 1.0"

# Launch Streamlit
Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host 'Streamlit Traffic Operations Dashboard (Layer 6)' -ForegroundColor Cyan; cd '$ProjectDir'; & '$PythonExe' -m streamlit run 'dashboard/app.py' --server.port 8501"

Write-Host "`n======================================================================" -ForegroundColor Green
Write-Host " ALL SERVICES LAUNCHED SUCCESSFULLY!" -ForegroundColor Green
Write-Host " - Kafka Broker      : localhost:9092 (Topic: traffic-events)" -ForegroundColor Cyan
Write-Host " - Stream Processor  : Ingesting, scoring & windowing" -ForegroundColor Cyan
Write-Host " - Streamlit Web UI  : http://localhost:8501" -ForegroundColor Cyan
Write-Host " - Event Producer    : Streaming live traffic observations" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "To switch modes, use the interactive dropdown in the Streamlit sidebar" -ForegroundColor Yellow
Write-Host "or stop all services anytime with: .\scripts\stop_all.ps1`n" -ForegroundColor Yellow
