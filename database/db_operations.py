"""
Database Operations for SQLite storage and retrieval.
"""
import sqlite3
from typing import Dict, List, Any, Optional
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATABASE_PATH

def get_connection(db_path=DATABASE_PATH):
    """Establishes an SQLite connection with Row factory and WAL mode."""
    conn = sqlite3.connect(db_path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def insert_traffic_event(event: Dict[str, Any], db_path=DATABASE_PATH) -> bool:
    """Inserts a single raw/preprocessed traffic event, ignoring duplicates."""
    query = """
    INSERT OR IGNORE INTO traffic_events 
    (event_id, timestamp, location, vehicle_count, average_speed, traffic_density, road_occupancy, event_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                event["event_id"],
                event["timestamp"],
                event["location"],
                int(event["vehicle_count"]),
                float(event["average_speed"]),
                float(event["traffic_density"]),
                float(event["road_occupancy"]),
                event.get("event_type", "NORMAL")
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error inserting traffic event: {e}")
        return False

def insert_traffic_metric(metric: Dict[str, Any], db_path=DATABASE_PATH) -> bool:
    """Inserts computed rolling stream metrics."""
    query = """
    INSERT INTO traffic_metrics 
    (timestamp, location, rolling_average_speed, current_vehicle_count, congestion_level, congestion_index)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                metric["timestamp"],
                metric["location"],
                float(metric["rolling_average_speed"]),
                int(metric["current_vehicle_count"]),
                metric["congestion_level"],
                float(metric["congestion_index"])
            ))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error inserting traffic metric: {e}")
        return False

def insert_traffic_alert(alert: Dict[str, Any], db_path=DATABASE_PATH) -> bool:
    """Inserts an incident or anomaly alert, ignoring duplicates."""
    query = """
    INSERT OR IGNORE INTO traffic_alerts 
    (alert_id, timestamp, location, alert_type, severity, description, anomaly_score, incident_source)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                alert["alert_id"],
                alert["timestamp"],
                alert["location"],
                alert["alert_type"],
                alert["severity"],
                alert["description"],
                alert.get("anomaly_score"),
                alert["incident_source"]
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error inserting traffic alert: {e}")
        return False

def get_kpi_metrics(db_path=DATABASE_PATH) -> Dict[str, Any]:
    """Retrieves high-level summary KPIs for the dashboard."""
    result = {
        "total_vehicles": 0,
        "avg_speed": 0.0,
        "current_congestion": "LOW",
        "total_anomalies": 0,
        "total_alerts": 0,
        "locations_monitored": 0,
        "last_event_time": "N/A"
    }
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            
            # Total events & vehicles
            cursor.execute("SELECT COUNT(*), SUM(vehicle_count), AVG(average_speed), MAX(timestamp) FROM traffic_events;")
            row = cursor.fetchone()
            if row and row[0] > 0:
                result["total_vehicles"] = row[1] or 0
                result["avg_speed"] = round(row[2] or 0.0, 1)
                result["last_event_time"] = row[3] or "N/A"
                
            # Distinct locations monitored
            cursor.execute("SELECT COUNT(DISTINCT location) FROM traffic_events;")
            loc_row = cursor.fetchone()
            result["locations_monitored"] = loc_row[0] if loc_row else 0
            
            # Alerts summary
            cursor.execute("SELECT COUNT(*) FROM traffic_alerts;")
            alerts_count = cursor.fetchone()
            result["total_alerts"] = alerts_count[0] if alerts_count else 0
            
            cursor.execute("SELECT COUNT(*) FROM traffic_alerts WHERE incident_source = 'ML_ISOLATION_FOREST';")
            anom_count = cursor.fetchone()
            result["total_anomalies"] = anom_count[0] if anom_count else 0
            
            # Latest overall congestion level
            cursor.execute("SELECT congestion_level FROM traffic_metrics ORDER BY metric_id DESC LIMIT 1;")
            cong_row = cursor.fetchone()
            if cong_row:
                result["current_congestion"] = cong_row[0]
                
    except Exception as e:
        print(f"Error fetching KPI metrics: {e}")
        
    return result

def get_recent_metrics(limit: int = 100, db_path=DATABASE_PATH) -> List[Dict[str, Any]]:
    """Retrieves recent traffic metrics ordered chronologically for time series charts."""
    query = """
    SELECT timestamp, location, rolling_average_speed, current_vehicle_count, congestion_level, congestion_index
    FROM traffic_metrics
    ORDER BY metric_id DESC
    LIMIT ?;
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in reversed(rows)]
    except Exception as e:
        print(f"Error fetching recent metrics: {e}")
        return []

def get_location_latest_status(db_path=DATABASE_PATH) -> List[Dict[str, Any]]:
    """Retrieves the latest traffic status for each monitored location."""
    query = """
    SELECT m.location, m.timestamp, m.rolling_average_speed, m.current_vehicle_count, 
           m.congestion_level, m.congestion_index, e.traffic_density, e.road_occupancy
    FROM traffic_metrics m
    INNER JOIN (
        SELECT location, MAX(metric_id) as max_id
        FROM traffic_metrics
        GROUP BY location
    ) latest ON m.metric_id = latest.max_id
    LEFT JOIN traffic_events e ON m.location = e.location AND m.timestamp = e.timestamp
    ORDER BY m.congestion_index DESC;
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(r) for r in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching location status: {e}")
        return []

def get_recent_alerts(limit: int = 50, db_path=DATABASE_PATH) -> List[Dict[str, Any]]:
    """Retrieves recent incident and anomaly alerts."""
    query = """
    SELECT alert_id, timestamp, location, alert_type, severity, description, anomaly_score, incident_source
    FROM traffic_alerts
    ORDER BY created_at DESC
    LIMIT ?;
    """
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            return [dict(r) for r in cursor.fetchall()]
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []
