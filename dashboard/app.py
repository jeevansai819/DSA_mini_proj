"""
Layer 6: Streamlit Real-Time Intelligent Traffic Monitoring & Analytics Dashboard.
Fetches fresh real-time metrics, anomalies, and incident alerts directly from SQLite.
Features Plotly interactive charts, live KPI indicators, and interactive scenario controls.
"""
import os
import sys
import time
import socket
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import (
    DATABASE_PATH, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, LOCATIONS
)
from database.db_operations import (
    get_kpi_metrics, get_recent_metrics, get_location_latest_status, get_recent_alerts, get_connection
)
from simulation.scenario_generator import ScenarioGenerator

# Page Configuration
st.set_page_config(
    page_title="IntelliTraffic AI - Real-Time Traffic & Accident Analytics",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Operations Center Aesthetic
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        color: #f8fafc;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .badge-critical {
        background-color: #ef4444;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-high {
        background-color: #f97316;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-normal {
        background-color: #10b981;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .status-pill {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .pill-green { background-color: #22c55e; }
    .pill-red { background-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

def check_kafka_broker_online(bootstrap_servers: str) -> bool:
    """Checks if Kafka port 9092 is listening."""
    try:
        host, port = bootstrap_servers.split(":")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        res = sock.connect_ex((host, int(port)))
        sock.close()
        return res == 0
    except Exception:
        return False

# Initialize scenario controller
scenario_gen = ScenarioGenerator()
current_mode_info = scenario_gen.get_current_mode()

# --- SIDEBAR: Simulation Controls & Pipeline Health ---
st.sidebar.image("https://img.icons8.com/fluency/96/traffic-light.png", width=64)
st.sidebar.title("Traffic Ops Center")
st.sidebar.caption("Intelligent Transportation Analytics Engine")

st.sidebar.markdown("---")
st.sidebar.subheader("🎮 Simulation Control Mode")
selected_mode = st.sidebar.selectbox(
    "Active Demonstration Mode",
    ["NORMAL_TRAFFIC", "TRAFFIC_CONGESTION", "ACCIDENT_SCENARIO"],
    index=["NORMAL_TRAFFIC", "TRAFFIC_CONGESTION", "ACCIDENT_SCENARIO"].index(
        current_mode_info.get("mode", "NORMAL_TRAFFIC")
    )
)

selected_target_loc = "Highway-101-North"
if selected_mode == "ACCIDENT_SCENARIO":
    selected_target_loc = st.sidebar.selectbox(
        "Accident Target Roadway",
        LOCATIONS,
        index=LOCATIONS.index(current_mode_info.get("target_location", "Highway-101-North"))
    )

if st.sidebar.button("Apply Scenario Mode", type="primary"):
    scenario_gen.set_mode(selected_mode, selected_target_loc)
    st.sidebar.success(f"Mode applied: {selected_mode}")
    time.sleep(0.5)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🔌 Pipeline Health")

kafka_online = check_kafka_broker_online(KAFKA_BOOTSTRAP_SERVERS)
if kafka_online:
    st.sidebar.markdown('<span class="status-pill pill-green"></span> **Kafka Broker:** `ONLINE (9092)`', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="status-pill pill-red"></span> **Kafka Broker:** `OFFLINE`', unsafe_allow_html=True)

db_exists = os.path.exists(DATABASE_PATH)
if db_exists:
    st.sidebar.markdown('<span class="status-pill pill-green"></span> **SQLite Database:** `CONNECTED`', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="status-pill pill-red"></span> **SQLite Database:** `NOT FOUND`', unsafe_allow_html=True)

st.sidebar.markdown(f"**Kafka Topic:** `{KAFKA_TOPIC}`")
st.sidebar.markdown("---")
auto_refresh = st.sidebar.checkbox("Auto-refresh (2.5s)", value=True)
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", min_value=1.0, max_value=10.0, value=2.5, step=0.5)

# --- MAIN CONTENT ---
st.title("🚦 Real-Time Traffic Congestion & Accident Detection System")
st.caption("Six-Layer Streaming Architecture | Apache Kafka • Python Windowing • Scikit-Learn Isolation Forest • SQLite")

# Retrieve latest data from SQLite
kpis = get_kpi_metrics(DATABASE_PATH)
metrics_list = get_recent_metrics(limit=120, db_path=DATABASE_PATH)
location_status = get_location_latest_status(DATABASE_PATH)
alerts_list = get_recent_alerts(limit=50, db_path=DATABASE_PATH)

# Section A: Dashboard Overview KPI Cards
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Vehicles Monitored</div>
        <div class="metric-value">{kpis['total_vehicles']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Network Speed</div>
        <div class="metric-value">{kpis['avg_speed']} <span style="font-size: 1rem; color: #94a3b8;">km/h</span></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    cong_color = "#10b981"
    if kpis['current_congestion'] == "Moderate traffic":
        cong_color = "#f59e0b"
    elif kpis['current_congestion'] in ["Heavy traffic", "Severe congestion"]:
        cong_color = "#ef4444"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Congestion State</div>
        <div class="metric-value" style="color: {cong_color}; font-size: 1.4rem;">{kpis['current_congestion']}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">ML Anomalies</div>
        <div class="metric-value" style="color: #a855f7;">{kpis['total_anomalies']}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    alert_color = "#ef4444" if kpis['total_alerts'] > 0 else "#38bdf8"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Incident Alerts</div>
        <div class="metric-value" style="color: {alert_color};">{kpis['total_alerts']}</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Road Segments</div>
        <div class="metric-value">{kpis['locations_monitored']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section B & C: Live Traffic & Congestion Charts
col_left, col_right = st.columns([7, 5])

if metrics_list:
    df_metrics = pd.DataFrame(metrics_list)
    
    with col_left:
        st.subheader("📈 Live Traffic Speed & Rolling Trend")
        fig_speed = px.line(
            df_metrics,
            x="timestamp",
            y="rolling_average_speed",
            color="location",
            labels={"rolling_average_speed": "Speed (km/h)", "timestamp": "Time", "location": "Segment"},
            template="plotly_dark"
        )
        fig_speed.update_layout(
            margin=dict(l=15, r=15, t=35, b=15),
            xaxis=dict(title=None),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title=None
            ),
            height=370
        )
        st.plotly_chart(fig_speed, use_container_width=True)

    with col_right:
        st.subheader("⚠️ Congestion Index Dynamics (%)")
        fig_cong = px.area(
            df_metrics,
            x="timestamp",
            y="congestion_index",
            color="location",
            labels={"congestion_index": "Congestion Index %", "timestamp": "Time", "location": "Segment"},
            template="plotly_dark"
        )
        fig_cong.update_layout(
            margin=dict(l=15, r=15, t=35, b=15),
            xaxis=dict(title=None),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title=None
            ),
            height=370
        )
        st.plotly_chart(fig_cong, use_container_width=True)

else:
    st.info("Awaiting live stream data from Apache Kafka. Start producer and processor to view real-time curves.")

# Section E: Road Segment Status Cards
st.subheader("🛣️ Segment-Wise Real-Time Conditions")
if location_status:
    cols = st.columns(len(location_status))
    for i, loc in enumerate(location_status):
        ci = loc.get("congestion_index", 0.0)
        card_border = "#10b981" if ci < 30 else ("#f59e0b" if ci < 60 else "#ef4444")
        with cols[i]:
            st.markdown(f"""
            <div style="border-left: 5px solid {card_border}; background: #1e293b; padding: 12px; border-radius: 6px; margin-bottom: 12px;">
                <div style="font-weight: bold; font-size: 0.95rem; color: #f8fafc;">{loc['location']}</div>
                <div style="color: #94a3b8; font-size: 0.8rem;">Status: <b style="color:{card_border}">{loc['congestion_level']}</b></div>
                <div style="margin-top: 6px; font-size: 0.85rem;">
                    🚗 Count: <b>{loc['current_vehicle_count']}</b> veh<br>
                    ⚡ Speed: <b>{loc['rolling_average_speed']}</b> km/h<br>
                    📊 Index: <b>{ci}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.write("No location stream observations recorded yet.")

# Section D: Accident & Anomaly Alert Log
st.subheader("🚨 Incident & Anomaly Detection Log")
if alerts_list:
    df_alerts = pd.DataFrame(alerts_list)
    
    # Render with custom styled dataframe
    def style_severity(val):
        color = '#ef4444' if val == 'CRITICAL' else ('#f97316' if val == 'HIGH' else '#3b82f6')
        return f'color: {color}; font-weight: bold;'

    st.dataframe(
        df_alerts[["timestamp", "location", "alert_type", "severity", "incident_source", "anomaly_score", "description"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("✅ Normal Flow: No critical accidents or severe statistical anomalies detected in current window.")

# Section F: Footer Pipeline Status
st.markdown("---")
foot_col1, foot_col2, foot_col3 = st.columns(3)
with foot_col1:
    st.caption(f"🕒 **Last Database Event:** {kpis['last_event_time']}")
with foot_col2:
    st.caption(f"⚙️ **Active Simulation Mode:** `{current_mode_info.get('mode', 'NORMAL_TRAFFIC')}`")
with foot_col3:
    st.caption(f"📡 **Host:** Localhost • Stream: `Kafka 3.9.2`")

# Auto-refresh loop
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
