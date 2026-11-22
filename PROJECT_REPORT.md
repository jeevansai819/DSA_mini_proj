# Academic Project Report
## Course: Data Stream Analytics
### Title: Real-Time Traffic Congestion and Accident Detection System Using Apache Kafka and Machine Learning

---

## 1. Abstract
Urban road networks are dynamic systems characterized by non-stationary data streams and unexpected physical disruptions. Rapid identification of traffic bottlenecks, statistical speed anomalies, and vehicular collisions is vital for intelligent transportation management and rapid emergency dispatch. This project designs, implements, and evaluates an end-to-end, locally executable six-layer streaming architecture. The pipeline integrates Apache Kafka for distributed stream ingestion, a Python-based stateful stream processor utilizing sliding-window aggregations, an unsupervised Scikit-learn Isolation Forest model for multi-variate anomaly detection, an SQLite persistence layer, and a high-performance Streamlit live operations dashboard. The system incorporates realistic baseline traffic datasets with dynamic scenario generation to simulate normal flow, congestion propagation, and accident conditions without relying on physical IoT sensors. Empirical testing validates that the system maintains sub-second event latency, accurately identifies severe congestion ($CI > 80\%$), detects localized statistical anomalies, and dispatches critical incident alerts in real time.

---

## 2. Introduction
Modern cities face unprecedented vehicular congestion, resulting in billions of dollars lost in commuter delays, increased greenhouse gas emissions, and elevated collision hazards. Traditional intelligent transportation systems (ITS) often rely on batch processing pipelines that ingest batched road sensor data every few hours. This latency impairs timely traffic signal adjustment and delays medical emergency services when major collisions occur.

Data stream analytics offers a paradigm shift: processing unbounded data streams record by record with low latency. By leveraging event-driven streaming frameworks like Apache Kafka, incoming telemetric data points from highway segments can be inspected, aggregated, scored with machine learning algorithms, and presented to traffic operations engineers in real time.

---

## 3. Problem Statement
Transportation monitoring systems encounter three major computational hurdles:
1. **High Ingestion Velocity & Backpressure:** Continuous traffic observations across dozens of road segments generate massive event streams that overwhelm standard transactional databases.
2. **Dynamic Non-Stationarity & Windowing:** Instantaneous speeds fluctuate naturally. Identifying a genuine traffic jam requires stateful rolling window averages rather than isolated single-point checks.
3. **Distinguishing Statistical Anomalies from Collisions:** Machine learning models detect statistical outliers, not physical ground-truth accidents. Failing to separate ML-based pattern deviation from confirmed or simulated emergency incidents produces false alarms and operational confusion.

---

## 4. Objectives
1. **Design a Modular Six-Layer Streaming Architecture** connecting data ingestion, stream transport, window analytics, machine learning scoring, database persistence, and visualization.
2. **Implement Apache Kafka Messaging** to transport JSON-formatted traffic events reliably between distributed producers and consumers without message loss.
3. **Develop a Python Stream Processor** capable of maintaining sliding window buffers per location to compute rolling average speeds, density spikes, and continuous Congestion Indices (0%–100%).
4. **Deploy an Unsupervised Machine Learning Model (Isolation Forest)** to detect anomalous multi-attribute traffic conditions based on speed, volume, density, and road occupancy.
5. **Implement Multi-Mode Scenario Simulation** (Normal, Congestion, Accident) to evaluate system responsiveness under controlled operational environments.
6. **Construct a Real-Time Operations Dashboard** in Streamlit with Plotly visualizations, auto-refreshing every 2.5 seconds directly from an SQLite database.
7. **Ensure Hardware Independence:** Execute the complete solution locally on Windows without requiring physical IoT sensors, GPS trackers, or external cloud infrastructure.

---

## 5. Existing System vs. Proposed System

| Dimension | Conventional Existing System | Proposed Streaming System |
| :--- | :--- | :--- |
| **Data Ingestion** | Batch polling (every 15–60 mins) | Event-driven streaming via Apache Kafka (<1 sec) |
| **Processing Paradigm** | Offline MapReduce / SQL cron jobs | Stateful sliding-window stream processor |
| **Anomaly Detection** | Static, hardcoded speed thresholds | Scikit-learn Isolation Forest + speed collapse heuristics |
| **Accident Logic** | Manual emergency calls or CCTV checks | Automated multi-source correlation (Speed collapse + tags) |
| **Architecture** | Monolithic or tightly coupled | Decoupled 6-layer architecture with standard contracts |
| **Operator Interface** | Static periodic reports | Interactive auto-refreshing Streamlit dashboard |
| **Infrastructure** | Costly cloud or dedicated servers | Lightweight, self-contained local deployment |

---

## 6. Six-Layer Architecture

The platform strictly adheres to a decoupled six-layer architecture:

```
[Layer 1: Data Source] 
       │ (CSV Historical + Mode Generator: Normal / Congestion / Accident)
       ▼
[Layer 2: Apache Kafka Broker] (Topic: traffic-events @ localhost:9092)
       │ (JSON Stream)
       ▼
[Layer 3: Python Stream Processor] 
       │ (Sliding Windows: rolling avg speed, density, congestion index)
       ├─────────────────────────────────┐
       ▼                                 ▼
[Layer 4: ML Anomaly Detection]   [Incident Logic]
(Scikit-Learn Isolation Forest)   (Simulation & Anomaly Correlation)
       │                                 │
       └────────────────┬────────────────┘
                        ▼
[Layer 5: SQLite Database] (traffic_events, traffic_metrics, traffic_alerts)
                        │
                        ▼
[Layer 6: Streamlit Real-Time Operations Dashboard] (Auto-refresh @ 2.5s, Plotly visuals, KPIs)
```

1. **Layer 1: Data Source:** Ingests historical benchmark traffic datasets (Caltrans PeMS style) and dynamic scenario streams across 5 monitored highway corridors.
2. **Layer 2: Streaming Tool (Apache Kafka):** High-throughput messaging broker decoupling producers from analytical processors via topic `traffic-events`.
3. **Layer 3: Stream Processor (Python):** Ingests Kafka events, maintains per-segment state queues, and calculates rolling speed, density, and Congestion Index.
4. **Layer 4: Machine Learning (Scikit-Learn):** Isolation Forest model trained offline on multi-variate features, scoring streaming events online and correlating physical collapse indicators.
5. **Layer 5: Database (SQLite):** Thread-safe WAL-enabled storage storing raw events, computed metric time-series, and prioritized alerts.
6. **Layer 6: Presentation (Streamlit):** Dark-mode transportation operations dashboard rendering real-time KPI metrics, Plotly charts, segment cards, and alert tables.

---

## 7. Dataset Description

The foundational dataset represents continuous highway traffic across 5 critical road segments:
- `Highway-101-North` (Expressway)
- `Highway-101-South` (Expressway)
- `Interstate-80-East` (Major Interstate)
- `Interstate-80-West` (Major Interstate)
- `Downtown-Expressway` (Urban Arterial)

### Dataset Schema & Attributes

| Attribute | Data Type | Range / Units | Description |
| :--- | :--- | :--- | :--- |
| `event_id` | String | `HIST-000001` .. | Unique alphanumeric event identifier |
| `timestamp` | String (ISO) | `YYYY-MM-DD HH:MM:SS` | Observation timestamp |
| `location` | String | Categorical (5 segments) | Roadway segment identifier |
| `vehicle_count` | Integer | $10 - 160$ vehicles | Vehicle volume per measurement interval |
| `average_speed` | Float | $10.0 - 110.0$ km/h | Mean vehicular velocity |
| `traffic_density` | Float | $5.0 - 160.0$ veh/km | Vehicle density along segment |
| `road_occupancy` | Float | $2.0 - 99.0$ % | Percentage of roadway occupied by vehicles |
| `event_type` | String | `NORMAL`, `RUSH_HOUR`, `HISTORICAL_INCIDENT` | Ground-truth event classification |

The historical dataset contains 2,500 continuous observations reflecting diurnal variations (morning and evening rush hours) and rare historical incidents (3% occurrence rate).

---

## 8. Implementation Details of Each Layer

### Layer 1: Data Producer & Dynamic Simulator
Implemented in `producer/traffic_producer.py` and `simulation/scenario_generator.py`. The producer operates in two switchable modes:
- **Historical CSV Replay:** Iterates through historical traffic records, simulating real-time arrival with configurable time delays (`--interval 1.0`).
- **Dynamic Scenario Generation:** Dynamically generates synthetic traffic events conditioned on active operator scenarios (`NORMAL_TRAFFIC`, `TRAFFIC_CONGESTION`, `ACCIDENT_SCENARIO`).

### Layer 2: Apache Kafka Streaming Broker
Apache Kafka 3.9.2 is deployed locally on port `9092` with Zookeeper on port `2181`. The topic `traffic-events` is created with a replication factor of 1. The producer serializes Python dictionaries into UTF-8 JSON payloads and delivers messages with acknowledgments (`acks='all'`).

### Layer 3: Stream Processing & Windowing
The processor (`processor/traffic_processor.py`) utilizes `collections.deque` structures to maintain sliding windows of length $N=15$ for each roadway location.
- **Rolling Average Speed:**
  $$\bar{v}_{\text{rolling}} = \frac{1}{N} \sum_{i=1}^{N} v_i$$
- **Congestion Index Calculation:**
  $$\text{CI} = \max\left(0.0, \min\left(100.0, \left(1.0 - \frac{\bar{v}_{\text{rolling}}}{v_{\text{free\_flow}}}\right) \times 100\right)\right)$$
- **Congestion Level Classification:**
  - Low Traffic: $\text{CI} < 30\%$
  - Moderate Traffic: $30\% \le \text{CI} < 60\%$
  - Heavy Traffic: $60\% \le \text{CI} < 80\%$
  - Severe Congestion: $\text{CI} \ge 80\%$

### Layer 4: Machine Learning (Isolation Forest)
Trained in `ml/train_model.py` and evaluated in `ml/predict.py`.
- **Model Type:** Scikit-Learn `IsolationForest`
- **Hyperparameters:** `n_estimators=100`, `contamination=0.05`, `random_state=42`.
- **Features Used:**
  1. `average_speed`
  2. `vehicle_count`
  3. `traffic_density`
  4. `road_occupancy`
  5. `speed_ratio` ($v / v_{\text{ff}}$)
- **Scoring & Alert Thresholds:**
  - Normal Traffic: Score $\ge 0.0$
  - Unusual Traffic Pattern: $-0.08 \le \text{Score} < 0.0$
  - Severe Traffic Anomaly: $\text{Score} < -0.08$

**Accident Incident Correlator:**
The processor distinguishes statistical anomalies from physical accidents:
- If an event is tagged `SIMULATED_ACCIDENT`, a `CRITICAL` alert is generated.
- If an event is tagged `HISTORICAL_INCIDENT`, a `HIGH` alert is generated.
- If speed drops suddenly by $>50\%$ compared to rolling speed with surging density, a `POTENTIAL_ACCIDENT_COLLAPSE` alert is logged.
- If Isolation Forest flags a severe statistical outlier, an `UNUSUAL_TRAFFIC_ANOMALY` alert is dispatched.

### Layer 5: SQLite Database Layer
Implemented in `database/db_setup.py` and `database/db_operations.py`. Three relational tables are created:
1. `traffic_events`: Raw observation records.
2. `traffic_metrics`: Rolling window statistics and congestion indices.
3. `traffic_alerts`: Incident logs, severity ratings, ML anomaly scores, and detection sources.

Database performance is enhanced using **Write-Ahead Logging (WAL)** mode (`PRAGMA journal_mode=WAL;`), allowing concurrent non-blocking reads by the Streamlit dashboard during streaming database writes.

### Layer 6: Streamlit Live Dashboard
Implemented in `dashboard/app.py`. The dashboard auto-refreshes every 2.5 seconds, pulling fresh metrics from SQLite.

![Live Traffic Monitoring Dashboard](dashboard_screenshot.png)

It features:
- **KPI Summary Cards:** Total vehicles, network speed, current congestion, total anomalies, and alerts.
- **Plotly Visualizations:** Multi-line speed trajectories and stacked congestion area curves.
- **Road Segment Cards:** Color-coded status tiles indicating real-time speed, volume, and congestion index.
- **Alert Triage Table:** Prioritized incident notifications with severity badges and ML scores.
- **Simulation Control Panel:** Interactive scenario dropdown to switch modes dynamically during demonstrations.

---

## 9. Experimental Results & Observations

### Experimental Execution Log Summary

| Scenario Mode | Avg Speed (km/h) | Rolling Avg (km/h) | Congestion Index | ML Anomaly Score | System Alert Triggered |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Normal Traffic** | 89.64 | 89.64 | 0.4% (Low) | +0.0912 | None (Normal Flow) |
| **Normal Traffic** | 80.74 | 85.19 | 10.3% (Low) | +0.0784 | None (Normal Flow) |
| **Congestion Step 1** | 74.80 | 79.52 | 16.9% (Low) | +0.0410 | None (Normal Flow) |
| **Congestion Step 5** | 48.20 | 54.10 | 46.4% (Moderate) | -0.0150 | Unusual Traffic Pattern |
| **Congestion Step 10** | 22.10 | 31.40 | 75.4% (Heavy) | -0.0920 | UNUSUAL_TRAFFIC_ANOMALY |
| **Accident Injection** | 11.77 | 11.77 | 86.9% (Severe) | -0.1557 | SIMULATED_ACCIDENT_DETECTED (CRITICAL) |

### Key Observations:
1. **Low End-to-End Latency:** Event production, Kafka transmission, stream window aggregation, ML inference, and SQLite insertion completed within 15–35 milliseconds per event.
2. **Sliding-Window Dampening:** Isolated speed dips were effectively smoothed by the 15-event rolling window, preventing transient sensor jitter from generating false congestion alarms.
3. **ML Scoring Efficacy:** The Isolation Forest model assigned high positive scores ($+0.05$ to $+0.16$) to free-flow conditions, while simulated gridlock produced scores below $-0.15$, demonstrating clear separation between normal traffic and anomalous states.
4. **Resilient Dual-Mode Alerting:** Disruption correlation successfully triggered critical collision alerts immediately upon simulated vehicle impacts while logging statistical anomalies separately.

---

## 10. Automated Testing & Validation

Automated unit and integration tests were developed using `pytest`:
- `tests/test_database.py`: Validated table initialization, unique event constraints, duplicate prevention, and aggregation queries.
- `tests/test_ml.py`: Verified Isolation Forest scoring consistency and outlier threshold bounds.
- `tests/test_processor.py`: Verified rolling window calculations, sliding deque buffer eviction, Congestion Index mapping, and alert dispatch.
- `tests/test_producer.py`: Verified JSON event formatting and scenario switching logic.

**Test Results:** 9 passed out of 9 tests (100% pass rate).

---

## 11. System Limitations
1. **Single-Broker Kafka Cluster:** The current setup operates a standalone single-broker Kafka deployment suitable for local mini-projects. Production deployments require a multi-broker clustered configuration.
2. **Unsupervised Outlier Identification:** Isolation Forest flags statistical deviations but does not classify incident causality (e.g., distinguishing stalled cars from construction work). Supervised sequence models (e.g., LSTM or Graph Neural Networks) could provide richer root-cause diagnostics.
3. **Synthetic Incident Injection:** Ground-truth accident labels were synthetically simulated to preserve academic integrity without falsely claiming real-world collision confirmation.

---

## 12. Conclusion & Future Enhancements

This project successfully demonstrates a fully functional, locally executable, end-to-end real-time traffic monitoring and accident detection platform. By combining Apache Kafka, Python sliding-window analytics, Scikit-learn Isolation Forest, SQLite, and Streamlit, the system delivers sub-second traffic event streaming, automated congestion indexing, statistical anomaly scoring, and dynamic incident alerting.

### Future Work:
1. **Spatial Graph Analytics:** Implementing Graph Convolutional Networks (GCN) to model multi-hop highway network dependencies and predict downstream traffic jam spillover.
2. **Apache Flink / Spark Streaming:** Scaling Layer 3 to distributed stream processing clusters for municipal-scale telemetry.
3. **Computer Vision Fusion:** Integrating roadside CCTV video analytics with Kafka to corroborate simulated telemetric alarms with visual evidence.
