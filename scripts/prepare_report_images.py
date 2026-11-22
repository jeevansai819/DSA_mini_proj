"""
Generates cropped figures from dashboard_screenshot.png and draws the System Architecture diagram.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def generate_report_images():
    output_dir = "report_images"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Architecture Diagram
    w, h = 800, 950
    arch_img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(arch_img)
    
    # Try system fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 22)
        font_sub = ImageFont.truetype("arial.ttf", 12)
        font_box_title = ImageFont.truetype("arialbd.ttf", 15)
        font_box_text = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_box_title = ImageFont.load_default()
        font_box_text = ImageFont.load_default()
        
    # Title
    draw.text((w/2, 35), "System Architecture", fill=(15, 23, 42), font=font_title, anchor="mm")
    draw.text((w/2, 60), "The following diagram shows the end-to-end flow of data in the", fill=(71, 85, 105), font=font_sub, anchor="mm")
    draw.text((w/2, 78), "Real-Time Traffic Congestion and Accident Detection System.", fill=(71, 85, 105), font=font_sub, anchor="mm")
    
    layers = [
        ("1. Data Source", "Python Producer (Simulated & Historical Data)\n• Vehicle Count   • Average Speed\n• Traffic Density   • Road Occupancy",
         "Generates time-stamped\ntraffic events for 5 highway\ncorridors (Highway-101-N/S,\nInterstate-80-E/W, Downtown)",
         (219, 234, 254), (59, 130, 246)),
         
        ("2. Streaming Platform", "Apache Kafka\n(traffic-events topic on localhost:9092)",
         "Transports events through\nthe Kafka topic using a\nproducer/consumer model.",
         (243, 232, 255), (168, 85, 247)),
         
        ("3. Stream Processor", "Python Consumer & Sliding Window Engine\n• In-memory deques (N=15)\n• Calculates rolling average speed & density\n• Prepares features for ML model",
         "Processes incoming events,\ncomputes Congestion Index,\nand sliding window metrics.",
         (220, 252, 231), (34, 197, 94)),
         
        ("4. Machine Learning", "Isolation Forest + Collision Heuristics\n(models/isolation_forest.pkl)\nContamination: 0.05, n_estimators: 100",
         "Detects anomalies using:\n• Isolation Forest model (ML)\n• Speed collapse heuristic\n• Multi-source alert triage",
         (254, 243, 199), (245, 158, 11)),
         
        ("5. Database", "SQLite Analytical Storage\n(traffic_analytics.db)\nTables: traffic_events, traffic_metrics, traffic_alerts",
         "Stores processed events,\ncomputed rolling metrics,\nand prioritized incident alerts.",
         (224, 242, 254), (14, 165, 233)),
         
        ("6. Visualization", "Streamlit Operations Center\n(http://localhost:8501)\nKPI Cards • Speed Curves • Congestion Area",
         "Displays roadway status,\nreal-time speed telemetry,\ncongestion index and alerts\n(with 2.5-second auto-refresh).",
         (254, 226, 226), (239, 68, 68))
    ]
    
    y = 110
    box_w = 420
    desc_w = 260
    box_h = 95
    spacing = 135
    
    for i, (ltitle, lmain, lside, bg_col, border_col) in enumerate(layers):
        # Left main box
        draw.rounded_rectangle([(40, y), (40 + box_w, y + box_h)], radius=8, fill=bg_col, outline=border_col, width=2)
        draw.text((55, y + 12), ltitle, fill=(15, 23, 42), font=font_box_title)
        draw.text((55, y + 36), lmain, fill=(51, 65, 85), font=font_box_text)
        
        # Right description box
        draw.rounded_rectangle([(480, y), (480 + desc_w, y + box_h)], radius=8, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
        draw.text((495, y + 16), lside, fill=(71, 85, 105), font=font_box_text)
        
        # Arrow down (except last)
        if i < len(layers) - 1:
            arrow_x = 40 + box_w / 2
            arrow_y1 = y + box_h + 4
            arrow_y2 = y + spacing - 8
            draw.line([(arrow_x, arrow_y1), (arrow_x, arrow_y2)], fill=(100, 116, 139), width=2)
            draw.polygon([(arrow_x - 5, arrow_y2 - 6), (arrow_x + 5, arrow_y2 - 6), (arrow_x, arrow_y2)], fill=(100, 116, 139))
            
        y += spacing
        
    arch_path = os.path.join(output_dir, "architecture_diagram.png")
    arch_img.save(arch_path)
    print(f"Saved architecture diagram to {arch_path}")
    
    # 2. Crop figures from dashboard_screenshot.png
    screenshot_src = "dashboard_screenshot.png"
    if os.path.exists(screenshot_src):
        img = Image.open(screenshot_src)
        W, H = img.size
        
        # Figure 1: KPI cards & Corridor status (top portion)
        # Usually from top 10% to 50%
        fig1 = img.crop((int(W * 0.16), int(H * 0.05), int(W * 0.98), int(H * 0.38)))
        fig1_path = os.path.join(output_dir, "figure1_kpis.png")
        fig1.save(fig1_path)
        print(f"Saved Figure 1 to {fig1_path}")
        
        # Figure 2: The Plotly charts (middle portion)
        fig2 = img.crop((int(W * 0.16), int(H * 0.37), int(W * 0.98), int(H * 0.69)))
        fig2_path = os.path.join(output_dir, "figure2_charts.png")
        fig2.save(fig2_path)
        print(f"Saved Figure 2 to {fig2_path}")
        
        # Figure 3: Corridor cards and Alert table (bottom portion)
        fig3 = img.crop((int(W * 0.16), int(H * 0.68), int(W * 0.98), int(H * 0.98)))
        fig3_path = os.path.join(output_dir, "figure3_alerts.png")
        fig3.save(fig3_path)
        print(f"Saved Figure 3 to {fig3_path}")

if __name__ == "__main__":
    generate_report_images()
