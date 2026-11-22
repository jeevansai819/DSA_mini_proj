"""
SQLite Database Schema and Initialization for Traffic Monitoring System.
"""
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATABASE_PATH

def init_database(db_path=DATABASE_PATH, drop_tables=False):
    """Initializes tables and indexes for traffic analytics."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable WAL mode for concurrent read/write performance
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    
    if drop_tables:
        cursor.execute("DROP TABLE IF EXISTS traffic_alerts;")
        cursor.execute("DROP TABLE IF EXISTS traffic_metrics;")
        cursor.execute("DROP TABLE IF EXISTS traffic_events;")
        
    # 1. traffic_events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_events (
        event_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        location TEXT NOT NULL,
        vehicle_count INTEGER NOT NULL,
        average_speed REAL NOT NULL,
        traffic_density REAL NOT NULL,
        road_occupancy REAL NOT NULL,
        event_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. traffic_metrics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_metrics (
        metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        location TEXT NOT NULL,
        rolling_average_speed REAL NOT NULL,
        current_vehicle_count INTEGER NOT NULL,
        congestion_level TEXT NOT NULL,
        congestion_index REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 3. traffic_alerts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_alerts (
        alert_id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        location TEXT NOT NULL,
        alert_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        description TEXT NOT NULL,
        anomaly_score REAL,
        incident_source TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Create indexes for optimal dashboard query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_ts_loc ON traffic_events(timestamp, location);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_ts_loc ON traffic_metrics(timestamp, location);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_ts ON traffic_alerts(timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_severity ON traffic_alerts(severity);")
    
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {db_path}")

if __name__ == "__main__":
    init_database()
