"""
Layer 3 & Layer 4: Python Stream Processor with ML Integration and Database Persistence.
Consumes events from Apache Kafka topic 'traffic-events', computes sliding window statistics,
scores anomalies using Isolation Forest, correlates accident indicators, and writes to SQLite.
"""
import os
import sys
import json
import time
import argparse
from collections import deque
from typing import Dict, Any, List, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_CONSUMER_GROUP,
    FREE_FLOW_SPEED_KMH, SLIDING_WINDOW_SIZE, CONGESTION_LEVELS, DATABASE_PATH
)
from database.db_operations import (
    insert_traffic_event, insert_traffic_metric, insert_traffic_alert
)
from ml.predict import TrafficAnomalyDetector

try:
    from kafka import KafkaConsumer
    from kafka.errors import NoBrokersAvailable
except ImportError:
    from kafka_python_ng import KafkaConsumer
    from kafka_python_ng.errors import NoBrokersAvailable

class LocationTrafficState:
    """Maintains state and sliding window buffers per location."""
    
    def __init__(self, location: str, window_size: int = SLIDING_WINDOW_SIZE):
        self.location = location
        self.window_size = window_size
        self.recent_speeds = deque(maxlen=window_size)
        self.recent_counts = deque(maxlen=window_size)
        self.recent_densities = deque(maxlen=window_size)
        self.recent_occupancies = deque(maxlen=window_size)
        self.max_vehicle_count = 0
        self.total_events_processed = 0
        self.total_anomalies_detected = 0
        
    def update(self, speed: float, count: int, density: float, occupancy: float):
        """Adds observation to sliding window."""
        self.recent_speeds.append(speed)
        self.recent_counts.append(count)
        self.recent_densities.append(density)
        self.recent_occupancies.append(occupancy)
        self.max_vehicle_count = max(self.max_vehicle_count, count)
        self.total_events_processed += 1
        
    @property
    def rolling_avg_speed(self) -> float:
        return sum(self.recent_speeds) / len(self.recent_speeds) if self.recent_speeds else 0.0
        
    @property
    def rolling_avg_density(self) -> float:
        return sum(self.recent_densities) / len(self.recent_densities) if self.recent_densities else 0.0
        
    @property
    def current_speed(self) -> float:
        return self.recent_speeds[-1] if self.recent_speeds else 0.0

class TrafficStreamProcessor:
    """Core stream analytics engine."""
    
    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS, db_path: str = DATABASE_PATH):
        self.bootstrap_servers = bootstrap_servers
        self.db_path = db_path
        self.location_states: Dict[str, LocationTrafficState] = {}
        self.anomaly_detector = TrafficAnomalyDetector()
        self.total_processed = 0
        self.total_alerts = 0
        
    def get_or_create_state(self, location: str) -> LocationTrafficState:
        if location not in self.location_states:
            self.location_states[location] = LocationTrafficState(location)
        return self.location_states[location]
        
    def calculate_congestion(self, rolling_speed: float) -> tuple[str, float]:
        """
        Calculates Congestion Index (0.0 to 100.0) and classifications:
        - Low traffic (<30%)
        - Moderate traffic (30-60%)
        - Heavy traffic (60-80%)
        - Severe congestion (>80%)
        """
        raw_index = (1.0 - (rolling_speed / FREE_FLOW_SPEED_KMH)) * 100.0
        congestion_index = max(0.0, min(100.0, round(raw_index, 2)))
        
        if congestion_index < CONGESTION_LEVELS["LOW"][1]:
            level = "Low traffic"
        elif congestion_index < CONGESTION_LEVELS["MODERATE"][1]:
            level = "Moderate traffic"
        elif congestion_index < CONGESTION_LEVELS["HEAVY"][1]:
            level = "Heavy traffic"
        else:
            level = "Severe congestion"
            
        return level, congestion_index

    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Processes an incoming event through windowing, ML scoring, and incident logic."""
        self.total_processed += 1
        location = event["location"]
        speed = float(event["average_speed"])
        count = int(event["vehicle_count"])
        density = float(event["traffic_density"])
        occupancy = float(event["road_occupancy"])
        timestamp = event["timestamp"]
        event_type = event.get("event_type", "NORMAL")
        
        state = self.get_or_create_state(location)
        prev_rolling_speed = state.rolling_avg_speed
        
        # 1. Update sliding window buffer
        state.update(speed, count, density, occupancy)
        curr_rolling_speed = round(state.rolling_avg_speed, 2)
        
        # 2. Congestion computation
        congestion_level, congestion_index = self.calculate_congestion(curr_rolling_speed)
        
        # 3. Machine Learning Anomaly Detection
        ml_class, ml_score = self.anomaly_detector.predict_event(event)
        
        # 4. Check for sudden speed collapse or incident indicators
        is_sudden_speed_drop = (
            len(state.recent_speeds) >= 3 and 
            prev_rolling_speed > 45.0 and 
            speed < (prev_rolling_speed * 0.50)
        )
        
        # 5. Persist raw event to SQLite
        insert_traffic_event(event, self.db_path)
        
        # 6. Persist metrics to SQLite
        metric_record = {
            "timestamp": timestamp,
            "location": location,
            "rolling_average_speed": curr_rolling_speed,
            "current_vehicle_count": count,
            "congestion_level": congestion_level,
            "congestion_index": congestion_index
        }
        insert_traffic_metric(metric_record, self.db_path)
        
        # 7. Alert Generation & Correlation
        alert_generated = None
        
        # Scenario A: Explicit Simulated Accident Event
        if event_type == "SIMULATED_ACCIDENT":
            self.total_alerts += 1
            alert_generated = {
                "alert_id": f"ALT-ACC-{self.total_alerts:06d}",
                "timestamp": timestamp,
                "location": location,
                "alert_type": "SIMULATED_ACCIDENT_DETECTED",
                "severity": "CRITICAL",
                "description": f"Simulated vehicle collision/incident verified at {location}. Severe speed collapse to {speed} km/h.",
                "anomaly_score": ml_score,
                "incident_source": "SIMULATED_SCENARIO"
            }
            insert_traffic_alert(alert_generated, self.db_path)
            
        # Scenario B: Historical Incident Label
        elif event_type == "HISTORICAL_INCIDENT":
            self.total_alerts += 1
            alert_generated = {
                "alert_id": f"ALT-HIST-{self.total_alerts:06d}",
                "timestamp": timestamp,
                "location": location,
                "alert_type": "HISTORICAL_INCIDENT_FLAG",
                "severity": "HIGH",
                "description": f"Historical road incident recorded at {location}. Speed: {speed} km/h, Occupancy: {occupancy}%.",
                "anomaly_score": ml_score,
                "incident_source": "HISTORICAL_DATASET"
            }
            insert_traffic_alert(alert_generated, self.db_path)
            
        # Scenario C: Sudden Physical Traffic Collapse (Potential Accident / Bottleneck)
        elif is_sudden_speed_drop:
            self.total_alerts += 1
            alert_generated = {
                "alert_id": f"ALT-COL-{self.total_alerts:06d}",
                "timestamp": timestamp,
                "location": location,
                "alert_type": "POTENTIAL_ACCIDENT_COLLAPSE",
                "severity": "CRITICAL",
                "description": f"Sudden >50% speed collapse from {prev_rolling_speed:.1f} km/h to {speed:.1f} km/h with surging density.",
                "anomaly_score": ml_score,
                "incident_source": "STREAM_HEURISTIC_CORRELATION"
            }
            insert_traffic_alert(alert_generated, self.db_path)
            
        # Scenario D: Machine Learning Outlier Alert (Severe Anomaly)
        elif ml_class == "Severe traffic anomaly":
            state.total_anomalies_detected += 1
            self.total_alerts += 1
            alert_generated = {
                "alert_id": f"ALT-ML-{self.total_alerts:06d}",
                "timestamp": timestamp,
                "location": location,
                "alert_type": "UNUSUAL_TRAFFIC_ANOMALY",
                "severity": "HIGH" if congestion_index > 70 else "MEDIUM",
                "description": f"Isolation Forest flagged statistically severe pattern (Score: {ml_score:.4f}).",
                "anomaly_score": ml_score,
                "incident_source": "ML_ISOLATION_FOREST"
            }
            insert_traffic_alert(alert_generated, self.db_path)
            
        return {
            "metric": metric_record,
            "ml_class": ml_class,
            "ml_score": ml_score,
            "alert": alert_generated
        }

    def start_consuming(self, max_messages: Optional[int] = None):
        """Main Kafka consumer loop."""
        print(f"Connecting to Kafka topic '{KAFKA_TOPIC}' on {self.bootstrap_servers}...")
        
        while True:
            try:
                consumer = KafkaConsumer(
                    KAFKA_TOPIC,
                    bootstrap_servers=self.bootstrap_servers,
                    auto_offset_reset="earliest",
                    enable_auto_commit=True,
                    group_id=KAFKA_CONSUMER_GROUP,
                    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
                    request_timeout_ms=15000
                )
                print(f"Connected to Kafka broker. Listening for events on topic '{KAFKA_TOPIC}'...")
                break
            except NoBrokersAvailable:
                print("Waiting for Kafka broker to be available on localhost:9092. Retrying in 3s...")
                time.sleep(3.0)
            except Exception as e:
                print(f"Error connecting to Kafka: {e}. Retrying in 3s...")
                time.sleep(3.0)
                
        count = 0
        try:
            while True:
                msg_pack = consumer.poll(timeout_ms=1000)
                if not msg_pack:
                    time.sleep(0.1)
                    continue
                for tp, messages in msg_pack.items():
                    for message in messages:
                        event = message.value
                        res = self.process_event(event)
                        count += 1
                        
                        alert_info = f" [ALERT: {res['alert']['alert_type']}]" if res['alert'] else ""
                        print(
                            f"Processed #{count:05d} | {event['location'][:16]:16} | "
                            f"Spd: {event['average_speed']:5.1f} km/h | RollSpd: {res['metric']['rolling_average_speed']:5.1f} | "
                            f"Cong: {res['metric']['congestion_level']:16} (CI: {res['metric']['congestion_index']:4.1f}%) | "
                            f"ML: {res['ml_class'][:16]:16}{alert_info}"
                        )
                        
                        if max_messages and count >= max_messages:
                            print(f"Reached {max_messages} messages limit. Exiting consumer.")
                            return
                        
        except KeyboardInterrupt:
            print("\nStream processor stopped by user.")
        finally:
            consumer.close()
            print("Kafka consumer closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-Time Traffic Stream Processor")
    parser.add_argument("--limit", type=int, default=None, help="Max messages to consume")
    args = parser.parse_args()
    
    processor = TrafficStreamProcessor()
    processor.start_consuming(max_messages=args.limit)
