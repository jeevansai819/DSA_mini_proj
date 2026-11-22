"""
Machine Learning Training Pipeline: Isolation Forest for Traffic Anomaly Detection.
Trains an Isolation Forest model on historical traffic attributes to establish baseline normal behavior
and isolate statistical anomalies in vehicle count, speed, density, and occupancy.
"""
import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    RAW_DATASET_FILE, MODEL_PATH, ML_CONTAMINATION, ML_N_ESTIMATORS, ML_RANDOM_STATE, FREE_FLOW_SPEED_KMH
)

FEATURE_COLUMNS = [
    "average_speed",
    "vehicle_count",
    "traffic_density",
    "road_occupancy",
    "speed_ratio"
]

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses and extracts engineering features for the model."""
    df_clean = df.copy()
    
    # Handle missing values
    for col in ["average_speed", "vehicle_count", "traffic_density", "road_occupancy"]:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            
    # Speed ratio compared to free-flow baseline
    df_clean["speed_ratio"] = df_clean["average_speed"] / FREE_FLOW_SPEED_KMH
    
    return df_clean[FEATURE_COLUMNS]

def train_isolation_forest():
    """Trains and serializes the Isolation Forest pipeline."""
    if not os.path.exists(RAW_DATASET_FILE):
        raise FileNotFoundError(f"Training dataset not found: {RAW_DATASET_FILE}")
        
    print(f"Loading training data from {RAW_DATASET_FILE}...")
    df = pd.read_csv(RAW_DATASET_FILE)
    print(f"Total historical records: {len(df)}")
    
    # Filter predominantly normal/rush hour for baseline learning
    X = prepare_features(df)
    
    print("Training features shape:", X.shape)
    print(X.describe())
    
    # Pipeline with StandardScaler and Isolation Forest
    model = IsolationForest(
        n_estimators=ML_N_ESTIMATORS,
        contamination=ML_CONTAMINATION,
        random_state=ML_RANDOM_STATE,
        n_jobs=-1
    )
    
    model.fit(X)
    
    # Evaluate model predictions on training set
    predictions = model.predict(X) # 1 for inlier (normal), -1 for outlier (anomaly)
    scores = model.decision_function(X) # Higher = more normal, lower/negative = more anomalous
    
    anomalies_detected = (predictions == -1).sum()
    print(f"\nModel Training Complete:")
    print(f"  - Contamination rate: {ML_CONTAMINATION * 100:.1f}%")
    print(f"  - Detected outliers in training set: {anomalies_detected} ({anomalies_detected / len(X) * 100:.2f}%)")
    print(f"  - Anomaly score min: {scores.min():.4f}, median: {np.median(scores):.4f}, max: {scores.max():.4f}")
    
    # Package model metadata and fitted model
    artifact = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "free_flow_speed": FREE_FLOW_SPEED_KMH,
        "threshold_normal": 0.0,      # score >= 0.0 -> Normal
        "threshold_unusual": -0.08,   # 0.0 > score >= -0.08 -> Unusual
        # score < -0.08 -> Severe anomaly
        "trained_at": pd.Timestamp.now().isoformat(),
        "n_training_samples": len(X)
    }
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    print(f"Model saved successfully to {MODEL_PATH}")
    return artifact

if __name__ == "__main__":
    train_isolation_forest()
