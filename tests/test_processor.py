"""
Unit tests for Stream Processor window calculations and alerts.
"""
import pytest
import tempfile
import os
from processor.traffic_processor import TrafficStreamProcessor, LocationTrafficState
from database.db_setup import init_database

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

def test_sliding_window_state():
    state = LocationTrafficState("Highway-101-North", window_size=5)
    speeds = [80.0, 70.0, 60.0, 50.0, 40.0]
    for s in speeds:
        state.update(speed=s, count=50, density=30.0, occupancy=20.0)
    assert state.rolling_avg_speed == 60.0
    assert len(state.recent_speeds) == 5
    
    # Adding 6th element drops the oldest (80.0)
    state.update(speed=30.0, count=60, density=40.0, occupancy=25.0)
    assert len(state.recent_speeds) == 5
    assert state.rolling_avg_speed == (70.0 + 60.0 + 50.0 + 40.0 + 30.0) / 5

def test_congestion_calculation(temp_db):
    processor = TrafficStreamProcessor(db_path=temp_db)
    # Speed 90 km/h (free flow) -> Congestion Index ~0% -> Low traffic
    level, ci = processor.calculate_congestion(90.0)
    assert level == "Low traffic"
    assert ci == 0.0
    
    # Speed 18 km/h -> Congestion Index 80% -> Severe congestion
    level, ci = processor.calculate_congestion(18.0)
    assert level == "Severe congestion"
    assert ci == 80.0

def test_process_accident_event(temp_db):
    processor = TrafficStreamProcessor(db_path=temp_db)
    accident_event = {
        "event_id": "TEST-ACC-01",
        "timestamp": "2026-11-21 12:00:00",
        "location": "Downtown-Expressway",
        "vehicle_count": 130,
        "average_speed": 15.0,
        "traffic_density": 110.0,
        "road_occupancy": 85.0,
        "event_type": "SIMULATED_ACCIDENT"
    }
    result = processor.process_event(accident_event)
    assert result["alert"] is not None
    assert result["alert"]["alert_type"] == "SIMULATED_ACCIDENT_DETECTED"
    assert result["alert"]["severity"] == "CRITICAL"
