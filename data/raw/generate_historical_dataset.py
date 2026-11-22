"""
Generates a realistic historical traffic dataset for model training and baseline replay.
Features based on real-world highway traffic metrics (e.g., Caltrans PeMS benchmarks):
- timestamp
- location
- vehicle_count (vehicles/interval)
- average_speed (km/h)
- traffic_density (veh/km)
- road_occupancy (0.0 to 100.0 %)
- event_type (NORMAL, RUSH_HOUR, HISTORICAL_INCIDENT)
"""
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import LOCATIONS, RAW_DATASET_FILE, FREE_FLOW_SPEED_KMH

def generate_historical_data(n_samples=2500, random_seed=42):
    np.random.seed(random_seed)
    
    records = []
    base_time = datetime(2026, 11, 15, 6, 0, 0)
    
    for i in range(n_samples):
        # Time progression across 5 days with 5-minute steps per location
        curr_time = base_time + timedelta(minutes=(i // len(LOCATIONS)) * 5)
        loc = LOCATIONS[i % len(LOCATIONS)]
        
        hour = curr_time.hour
        is_rush_hour = (7 <= hour <= 9) or (17 <= hour <= 19)
        is_night = (23 <= hour or hour <= 5)
        
        # Decide regime: normal, rush-hour peak, or rare historical incident (e.g. stalled vehicle)
        incident_roll = np.random.rand()
        
        if incident_roll < 0.03:  # 3% rare incident in historical data
            event_type = "HISTORICAL_INCIDENT"
            speed = np.random.uniform(15.0, 32.0)
            vehicle_count = int(np.random.uniform(95, 145))
            density = np.random.uniform(90.0, 140.0)
            occupancy = np.random.uniform(65.0, 92.0)
        elif is_rush_hour:
            event_type = "RUSH_HOUR"
            speed = np.random.uniform(38.0, 62.0)
            vehicle_count = int(np.random.uniform(75, 125))
            density = np.random.uniform(50.0, 85.0)
            occupancy = np.random.uniform(35.0, 65.0)
        elif is_night:
            event_type = "NORMAL"
            speed = np.random.uniform(85.0, 105.0)
            vehicle_count = int(np.random.uniform(10, 35))
            density = np.random.uniform(8.0, 22.0)
            occupancy = np.random.uniform(5.0, 18.0)
        else:
            event_type = "NORMAL"
            speed = np.random.uniform(72.0, 95.0)
            vehicle_count = int(np.random.uniform(40, 80))
            density = np.random.uniform(25.0, 48.0)
            occupancy = np.random.uniform(18.0, 36.0)
            
        # Add small natural Gaussian noise
        speed = max(10.0, min(120.0, speed + np.random.normal(0, 2.0)))
        density = max(5.0, min(180.0, density + np.random.normal(0, 1.5)))
        occupancy = max(2.0, min(99.0, occupancy + np.random.normal(0, 1.0)))
        
        records.append({
            "event_id": f"HIST-{i+1:06d}",
            "timestamp": curr_time.strftime("%Y-%m-%d %H:%M:%S"),
            "location": loc,
            "vehicle_count": vehicle_count,
            "average_speed": round(speed, 2),
            "traffic_density": round(density, 2),
            "road_occupancy": round(occupancy, 2),
            "event_type": event_type
        })
        
    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(RAW_DATASET_FILE), exist_ok=True)
    df.to_csv(RAW_DATASET_FILE, index=False)
    print(f"Generated {len(df)} historical traffic records to {RAW_DATASET_FILE}")
    print(df.head())
    print("Class distribution:")
    print(df["event_type"].value_counts())
    return df

if __name__ == "__main__":
    generate_historical_data()
