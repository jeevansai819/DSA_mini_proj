"""
Configuration settings for Real-Time Traffic Congestion and Accident Detection System.
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"
DATABASE_DIR = BASE_DIR / "database"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# Database Configuration
DATABASE_PATH = str(DATABASE_DIR / "traffic_analytics.db")

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "traffic-events")
KAFKA_CONSUMER_GROUP = "traffic-stream-processor-group"
KAFKA_HOME = os.getenv("KAFKA_HOME", "C:\\kafka")

# Machine Learning Model Configuration
MODEL_PATH = str(MODELS_DIR / "isolation_forest.pkl")
ML_CONTAMINATION = 0.05
ML_N_ESTIMATORS = 100
ML_RANDOM_STATE = 42

# Traffic Monitoring Locations
LOCATIONS = [
    "Highway-101-North",
    "Highway-101-South",
    "Interstate-80-East",
    "Interstate-80-West",
    "Downtown-Expressway"
]

# Baseline Traffic Parameters
FREE_FLOW_SPEED_KMH = 90.0  # Speed in km/h under ideal conditions
ROAD_CAPACITY_VPH = 150.0   # Max normal vehicles per interval per segment
JAM_DENSITY_VPK = 180.0     # Vehicles per kilometer representing full gridlock

# Stream Windowing Configuration
SLIDING_WINDOW_SIZE = 15    # Number of recent events for location sliding window
ROLLING_SHORT_WINDOW = 5    # Immediate short window

# Congestion Thresholds (Congestion Index = 0.0 to 100.0)
# Congestion Index = (1.0 - (current_speed / free_flow_speed)) * 100
CONGESTION_LEVELS = {
    "LOW": (0.0, 30.0),
    "MODERATE": (30.0, 60.0),
    "HEAVY": (60.0, 80.0),
    "SEVERE": (80.0, 100.0)
}

# Producer Settings
DEFAULT_PRODUCER_INTERVAL_SEC = 1.0  # Delay between events
RAW_DATASET_FILE = str(RAW_DATA_DIR / "traffic_historical_data.csv")
