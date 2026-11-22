"""
Unit tests for Database Operations.
"""
import os
import pytest
import sqlite3
import tempfile
from database.db_setup import init_database
from database.db_operations import (
    insert_traffic_event, insert_traffic_metric, insert_traffic_alert,
    get_kpi_metrics, get_recent_metrics, get_recent_alerts
)

@pytest.fixture
def temp_db():
    import gc
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_database(path, drop_tables=True)
    yield path
    gc.collect()
    try:
        if os.path.exists(path):
            os.remove(path)
    except PermissionError:
        pass

def test_insert_and_retrieve_event(temp_db):
    event = {
        "event_id": "TEST-001",
        "timestamp": "2026-11-21 10:00:00",
        "location": "Highway-101-North",
        "vehicle_count": 55,
        "average_speed": 78.5,
        "traffic_density": 32.0,
        "road_occupancy": 22.0,
        "event_type": "NORMAL"
    }
    inserted = insert_traffic_event(event, temp_db)
    assert inserted is True
    
    # Inserting duplicate should not fail or duplicate
    assert insert_traffic_event(event, temp_db) is False

def test_insert_metric_and_kpi(temp_db):
    event = {
        "event_id": "TEST-002",
        "timestamp": "2026-11-21 10:01:00",
        "location": "Highway-101-North",
        "vehicle_count": 80,
        "average_speed": 65.0,
        "traffic_density": 45.0,
        "road_occupancy": 35.0,
        "event_type": "NORMAL"
    }
    insert_traffic_event(event, temp_db)
    
    metric = {
        "timestamp": "2026-11-21 10:01:00",
        "location": "Highway-101-North",
        "rolling_average_speed": 71.75,
        "current_vehicle_count": 80,
        "congestion_level": "Low traffic",
        "congestion_index": 20.28
    }
    assert insert_traffic_metric(metric, temp_db) is True
    
    kpis = get_kpi_metrics(temp_db)
    assert kpis["total_vehicles"] == 80
    assert kpis["locations_monitored"] == 1
    assert kpis["current_congestion"] == "Low traffic"

def test_insert_alert(temp_db):
    alert = {
        "alert_id": "ALT-TEST-001",
        "timestamp": "2026-11-21 10:02:00",
        "location": "Highway-101-North",
        "alert_type": "SIMULATED_ACCIDENT_DETECTED",
        "severity": "CRITICAL",
        "description": "Simulated vehicle collision test",
        "anomaly_score": -0.12,
        "incident_source": "SIMULATED_SCENARIO"
    }
    assert insert_traffic_alert(alert, temp_db) is True
    alerts = get_recent_alerts(10, temp_db)
    assert len(alerts) == 1
    assert alerts[0]["alert_id"] == "ALT-TEST-001"
