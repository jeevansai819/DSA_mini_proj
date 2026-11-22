"""
Unit tests for Machine Learning Anomaly Detection.
"""
import pytest
from ml.predict import TrafficAnomalyDetector

def test_ml_normal_prediction():
    detector = TrafficAnomalyDetector()
    normal_event = {
        "average_speed": 82.0,
        "vehicle_count": 50,
        "traffic_density": 28.0,
        "road_occupancy": 20.0
    }
    classification, score = detector.predict_event(normal_event)
    assert classification in ["Normal traffic", "Unusual traffic pattern"]
    assert isinstance(score, float)

def test_ml_severe_anomaly_prediction():
    detector = TrafficAnomalyDetector()
    extreme_anomaly = {
        "average_speed": 12.0,
        "vehicle_count": 180,
        "traffic_density": 160.0,
        "road_occupancy": 95.0
    }
    classification, score = detector.predict_event(extreme_anomaly)
    # Extreme gridlock / breakdown should have low score
    assert score < 0.0
    assert classification in ["Unusual traffic pattern", "Severe traffic anomaly"]
