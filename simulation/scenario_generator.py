"""
Traffic Scenario Generator.
Supports three dynamic demonstration modes:
- Mode 1: NORMAL_TRAFFIC
- Mode 2: TRAFFIC_CONGESTION
- Mode 3: ACCIDENT_SCENARIO
"""
import os
import sys
import json
import random
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import LOCATIONS, BASE_DIR

MODE_STATE_FILE = BASE_DIR / "simulation" / "active_scenario.json"

class ScenarioGenerator:
    """Generates continuous streaming traffic events conditioned on active scenario mode."""
    
    def __init__(self):
        self.state_file = MODE_STATE_FILE
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.state_file.exists():
            self.set_mode("NORMAL_TRAFFIC")
            
        self.event_counter = 0
        self.location_index = 0
        self.accident_location = "Highway-101-North"
        self.congestion_step = 0
        
    def set_mode(self, mode_name: str, target_location: str = "Highway-101-North"):
        """Updates the active scenario configuration."""
        valid_modes = ["NORMAL_TRAFFIC", "TRAFFIC_CONGESTION", "ACCIDENT_SCENARIO"]
        if mode_name not in valid_modes:
            mode_name = "NORMAL_TRAFFIC"
            
        state = {
            "mode": mode_name,
            "target_location": target_location,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)
            
    def get_current_mode(self) -> Dict[str, str]:
        """Reads the currently configured scenario mode."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"mode": "NORMAL_TRAFFIC", "target_location": "Highway-101-North"}
        
    def generate_event(self) -> Dict[str, Any]:
        """Generates the next synthetic/real-time streaming event."""
        self.event_counter += 1
        curr_loc = LOCATIONS[self.location_index % len(LOCATIONS)]
        self.location_index += 1
        
        mode_info = self.get_current_mode()
        active_mode = mode_info.get("mode", "NORMAL_TRAFFIC")
        target_loc = mode_info.get("target_location", "Highway-101-North")
        
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if active_mode == "ACCIDENT_SCENARIO" and curr_loc == target_loc:
            # Mode 3: Accident scenario at target segment
            speed = round(random.uniform(10.0, 22.0), 2)
            vehicle_count = random.randint(110, 160)
            density = round(random.uniform(95.0, 145.0), 2)
            occupancy = round(random.uniform(75.0, 94.0), 2)
            event_type = "SIMULATED_ACCIDENT"
            
        elif active_mode == "TRAFFIC_CONGESTION":
            # Mode 2: Traffic congestion scenario
            self.congestion_step += 1
            # Progressive degradation of traffic flow
            speed = round(max(15.0, 85.0 - (self.congestion_step % 20) * 3.2 + random.uniform(-3, 3)), 2)
            vehicle_count = min(150, 45 + (self.congestion_step % 20) * 5 + random.randint(-5, 5))
            density = round(min(130.0, 30.0 + (self.congestion_step % 20) * 4.5 + random.uniform(-2, 2)), 2)
            occupancy = round(min(90.0, 20.0 + (self.congestion_step % 20) * 3.5 + random.uniform(-2, 2)), 2)
            event_type = "SIMULATED_CONGESTION"
            
        else:
            # Mode 1: Normal traffic conditions with smooth natural variance
            speed = round(random.uniform(72.0, 94.0), 2)
            vehicle_count = random.randint(35, 75)
            density = round(random.uniform(22.0, 45.0), 2)
            occupancy = round(random.uniform(15.0, 32.0), 2)
            event_type = "NORMAL"
            
        event = {
            "event_id": f"LIVE-{self.event_counter:07d}",
            "timestamp": timestamp_str,
            "location": curr_loc,
            "vehicle_count": vehicle_count,
            "average_speed": speed,
            "traffic_density": density,
            "road_occupancy": occupancy,
            "event_type": event_type,
            "simulation_mode": active_mode
        }
        return event

if __name__ == "__main__":
    gen = ScenarioGenerator()
    print("Testing Scenario Generator across modes:")
    for mode in ["NORMAL_TRAFFIC", "TRAFFIC_CONGESTION", "ACCIDENT_SCENARIO"]:
        gen.set_mode(mode)
        print(f"\nMode: {mode}")
        for _ in range(3):
            print(" ", gen.generate_event())
    gen.set_mode("NORMAL_TRAFFIC")
