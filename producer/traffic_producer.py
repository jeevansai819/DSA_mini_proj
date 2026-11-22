"""
Layer 1 & Layer 2: Kafka Traffic Data Producer.
Streams traffic events to Apache Kafka topic 'traffic-events' in JSON format.
Supports historical CSV replay and live scenario generation (Normal, Congestion, Accident).
"""
import os
import sys
import time
import json
import argparse
from datetime import datetime
import pandas as pd
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, DEFAULT_PRODUCER_INTERVAL_SEC, RAW_DATASET_FILE
)
from simulation.scenario_generator import ScenarioGenerator

try:
    from kafka import KafkaProducer
    from kafka.errors import NoBrokersAvailable, KafkaError
except ImportError:
    # Alternative import if named kafka_python_ng
    from kafka_python_ng import KafkaProducer
    from kafka_python_ng.errors import NoBrokersAvailable, KafkaError

def create_kafka_producer(bootstrap_servers: str, max_retries: int = 5, retry_interval: float = 3.0) -> Optional[KafkaProducer]:
    """Establishes connection to Kafka broker with graceful retry."""
    print(f"Connecting to Kafka broker at {bootstrap_servers}...")
    for attempt in range(1, max_retries + 1):
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                acks="all",
                retries=3,
                request_timeout_ms=10000
            )
            print("Successfully connected to Apache Kafka broker.")
            return producer
        except NoBrokersAvailable:
            print(f"Broker not available (attempt {attempt}/{max_retries}). Retrying in {retry_interval}s...")
            time.sleep(retry_interval)
        except Exception as e:
            print(f"Failed to connect to Kafka: {e}. Retrying in {retry_interval}s...")
            time.sleep(retry_interval)
            
    print("Error: Could not connect to Kafka broker. Please ensure Kafka is running on localhost:9092.")
    return None

def run_producer(
    source: str = "scenario",
    interval: float = DEFAULT_PRODUCER_INTERVAL_SEC,
    mode: str = "NORMAL_TRAFFIC",
    max_events: Optional[int] = None
):
    """
    Main producer streaming loop.
    source: 'scenario' (dynamic live generator) or 'csv' (historical replay)
    """
    scenario_gen = ScenarioGenerator()
    if mode:
        scenario_gen.set_mode(mode)
        
    producer = create_kafka_producer(KAFKA_BOOTSTRAP_SERVERS)
    if producer is None:
        sys.exit(1)
        
    print("\n" + "="*60)
    print(" TRAFFIC STREAMING PRODUCER RUNNING")
    print(f" - Target Kafka Topic : {KAFKA_TOPIC}")
    print(f" - Event Source        : {source.upper()}")
    print(f" - Emission Interval   : {interval} seconds")
    print(f" - Initial Mode        : {mode}")
    print("="*60 + "\n")
    
    events_sent = 0
    
    try:
        if source == "csv":
            if not os.path.exists(RAW_DATASET_FILE):
                raise FileNotFoundError(f"Historical dataset not found at {RAW_DATASET_FILE}")
            df = pd.read_csv(RAW_DATASET_FILE)
            
            while True:
                for idx, row in df.iterrows():
                    # Handle missing or invalid values
                    speed = float(row.get("average_speed", 60.0))
                    density = float(row.get("traffic_density", 30.0))
                    occupancy = float(row.get("road_occupancy", 25.0))
                    count = int(row.get("vehicle_count", 50))
                    
                    event = {
                        "event_id": f"CSV-{idx+1:06d}",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "location": str(row.get("location", "Highway-101-North")),
                        "vehicle_count": count,
                        "average_speed": speed,
                        "traffic_density": density,
                        "road_occupancy": occupancy,
                        "event_type": str(row.get("event_type", "NORMAL")),
                        "simulation_mode": "CSV_REPLAY"
                    }
                    
                    producer.send(KAFKA_TOPIC, key=event["location"], value=event)
                    producer.flush()
                    events_sent += 1
                    print(f"[{event['timestamp']}] Sent CSV Event #{events_sent}: {event['location']} | Spd: {event['average_speed']} km/h | Veh: {event['vehicle_count']}")
                    
                    if max_events and events_sent >= max_events:
                        print(f"Reached max events limit ({max_events}). Stopping.")
                        return
                    time.sleep(interval)
        else:
            # Dynamic Scenario Generation Mode
            while True:
                event = scenario_gen.generate_event()
                
                producer.send(KAFKA_TOPIC, key=event["location"], value=event)
                producer.flush()
                events_sent += 1
                
                alert_tag = f" *** [{event['event_type']}] ***" if event['event_type'] != "NORMAL" else ""
                print(f"[{event['timestamp']}] Sent Event #{events_sent}: {event['location']} | Spd: {event['average_speed']} km/h | Dens: {event['traffic_density']} | Mode: {event['simulation_mode']}{alert_tag}")
                
                if max_events and events_sent >= max_events:
                    print(f"Reached max events limit ({max_events}). Stopping.")
                    return
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print("\nProducer stopped by user (Ctrl+C).")
    finally:
        if producer:
            producer.close()
            print("Kafka producer closed gracefully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Traffic Event Producer")
    parser.add_argument("--source", type=str, default="scenario", choices=["scenario", "csv"], help="Event data source")
    parser.add_argument("--interval", type=float, default=DEFAULT_PRODUCER_INTERVAL_SEC, help="Delay between events in seconds")
    parser.add_argument("--mode", type=str, default="NORMAL_TRAFFIC", choices=["NORMAL_TRAFFIC", "TRAFFIC_CONGESTION", "ACCIDENT_SCENARIO"], help="Scenario mode")
    parser.add_argument("--limit", type=int, default=None, help="Max events to send")
    
    args = parser.parse_args()
    run_producer(source=args.source, interval=args.interval, mode=args.mode, max_events=args.limit)
