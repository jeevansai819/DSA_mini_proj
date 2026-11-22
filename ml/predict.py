"""
Inference module for Traffic Anomaly Detection using Isolation Forest.
Provides scoring and classification of incoming streaming traffic events.
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Any, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import MODEL_PATH, FREE_FLOW_SPEED_KMH

class TrafficAnomalyDetector:
    """Online anomaly detector leveraging the pre-trained Isolation Forest artifact."""
    
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.feature_columns = None
        self.threshold_normal = 0.0
        self.threshold_unusual = -0.08
        self.is_loaded = False
        self.load_model()
        
    def load_model(self):
        """Loads the serialized model artifact from disk."""
        if not os.path.exists(self.model_path):
            print(f"Warning: Model artifact not found at {self.model_path}. Anomaly scoring will use fallback heuristic.")
            self.is_loaded = False
            return
            
        try:
            artifact = joblib.load(self.model_path)
            self.model = artifact["model"]
            self.feature_columns = artifact["feature_columns"]
            self.threshold_normal = artifact.get("threshold_normal", 0.0)
            self.threshold_unusual = artifact.get("threshold_unusual", -0.08)
            self.is_loaded = True
            print(f"Loaded Isolation Forest model from {self.model_path}")
        except Exception as e:
            print(f"Error loading model from {self.model_path}: {e}")
            self.is_loaded = False
            
    def predict_event(self, event: Dict[str, Any]) -> Tuple[str, float]:
        """
        Scores a single incoming traffic event.
        Returns:
            classification: 'Normal traffic', 'Unusual traffic pattern', or 'Severe traffic anomaly'
            score: Isolation Forest anomaly score (normalized float; lower indicates higher anomaly)
        """
        if not self.is_loaded:
            # Fallback heuristic if model file is not yet generated
            return self._heuristic_fallback(event)
            
        try:
            speed = float(event.get("average_speed", 60.0))
            count = float(event.get("vehicle_count", 50))
            density = float(event.get("traffic_density", 30.0))
            occupancy = float(event.get("road_occupancy", 25.0))
            speed_ratio = speed / FREE_FLOW_SPEED_KMH
            
            # Construct DataFrame matching training feature columns
            feature_data = pd.DataFrame([{
                "average_speed": speed,
                "vehicle_count": count,
                "traffic_density": density,
                "road_occupancy": occupancy,
                "speed_ratio": speed_ratio
            }])[self.feature_columns]
            
            # Isolation Forest decision_function: positive = inlier, negative = outlier
            raw_score = float(self.model.decision_function(feature_data)[0])
            score = round(raw_score, 4)
            
            if score >= self.threshold_normal:
                classification = "Normal traffic"
            elif score >= self.threshold_unusual:
                classification = "Unusual traffic pattern"
            else:
                classification = "Severe traffic anomaly"
                
            return classification, score
            
        except Exception as e:
            print(f"Error scoring event: {e}")
            return "Normal traffic", 0.0
            
    def _heuristic_fallback(self, event: Dict[str, Any]) -> Tuple[str, float]:
        speed = float(event.get("average_speed", 60.0))
        density = float(event.get("traffic_density", 30.0))
        if speed < 25.0 and density > 80.0:
            return "Severe traffic anomaly", -0.15
        elif speed < 40.0:
            return "Unusual traffic pattern", -0.05
        return "Normal traffic", 0.05
