"""
Generates the complete 11-page Academic Project Report PDF matching the exact template format.
Uses ReportLab to render page borders, headers/footers, styled tables, headings, code blocks, and figures.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that adds an outer page border and running footer to every page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations()
            super().showPage()
        super().save()

    def draw_page_decorations(self):
        self.saveState()
        # Page border: 28pt from edges
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(1.0)
        # letter is 612 x 792 pt
        self.rect(26, 26, 560, 740)
        
        # Running footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawCentredString(306, 36, "Data Stream Analytics Mini-Project")
        self.restoreState()

def build_pdf_report(filename="PROJECT_REPORT.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=44,
        rightMargin=44,
        topMargin=46,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Color palette matching template
    NAVY = colors.HexColor("#1A365D")
    SLATE = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#475569")
    BORDER_COL = colors.HexColor("#CBD5E1")

    # Custom styles
    style_cover_super = ParagraphStyle('CoverSuper', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY, alignment=1, spaceAfter=80)
    style_cover_h1 = ParagraphStyle('CoverH1', fontName='Helvetica-Bold', fontSize=26, textColor=colors.black, alignment=1, spaceAfter=22)
    style_cover_title = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=18, textColor=NAVY, alignment=1, spaceAfter=14, leading=24)
    style_cover_sub = ParagraphStyle('CoverSub', fontName='Helvetica', fontSize=13, textColor=colors.HexColor("#2B6CB0"), alignment=1, spaceAfter=16)
    style_cover_repo = ParagraphStyle('CoverRepo', fontName='Helvetica', fontSize=9.5, textColor=colors.HexColor("#2B6CB0"), alignment=1, spaceAfter=140)
    style_cover_meta = ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=12, textColor=SLATE, alignment=1, spaceAfter=6, leading=18)

    style_abstract_h1 = ParagraphStyle('AbstractH1', fontName='Helvetica-Bold', fontSize=20, textColor=NAVY, alignment=1, spaceAfter=28)
    style_abstract_body = ParagraphStyle('AbstractBody', fontName='Helvetica', fontSize=11, textColor=SLATE, leading=17, spaceAfter=12, alignment=4)

    style_h1 = ParagraphStyle('SectionH1', fontName='Helvetica-Bold', fontSize=14, textColor=NAVY, spaceBefore=12, spaceAfter=6, leading=18)
    style_h2 = ParagraphStyle('SectionH2', fontName='Helvetica-Bold', fontSize=11.5, textColor=NAVY, spaceBefore=10, spaceAfter=4, leading=16)
    style_h3 = ParagraphStyle('SectionH3', fontName='Helvetica-Bold', fontSize=10.5, textColor=SLATE, spaceBefore=8, spaceAfter=3, leading=14)
    style_body = ParagraphStyle('BodyTextCustom', fontName='Helvetica', fontSize=9.5, textColor=SLATE, leading=13.5, spaceAfter=6)
    style_bullet = ParagraphStyle('BulletCustom', fontName='Helvetica', fontSize=9.5, textColor=SLATE, leading=13.5, leftIndent=14, firstLineIndent=-8, spaceAfter=3)
    style_caption = ParagraphStyle('CaptionCustom', fontName='Helvetica-Oblique', fontSize=8.5, textColor=TEXT_MUTED, alignment=1, spaceBefore=3, spaceAfter=8)
    style_term_h = ParagraphStyle('TermH', fontName='Helvetica-Bold', fontSize=10.5, textColor=NAVY, spaceBefore=7, spaceAfter=2)
    style_code = ParagraphStyle('CodeCustom', fontName='Courier', fontSize=8.5, textColor=SLATE, leading=11, leftIndent=12, spaceAfter=2)

    story = []

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROJECT REPORT", style_cover_h1))
    story.append(Spacer(1, 10))
    story.append(Paragraph("REAL-TIME TRAFFIC CONGESTION AND ACCIDENT DETECTION SYSTEM", style_cover_title))
    story.append(Paragraph("A Data Stream Analytics Mini-Project", style_cover_sub))
    story.append(Paragraph("GitHub Repository: https://github.com/26yashu/real-time-traffic-congestion", style_cover_repo))
    
    story.append(Paragraph("Submitted to: <b>Shahad P</b>", style_cover_meta))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Submitted by: <b>Gandlaparthi Yaswanthi</b>", style_cover_meta))
    story.append(Paragraph("USN: <b>23BTRCL187</b>", style_cover_meta))
    story.append(Paragraph("Department: <b>CSE-AIML(D)</b>", style_cover_meta))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ABSTRACT
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Abstract", style_abstract_h1))
    abstract_text = (
        "This project demonstrates an end-to-end streaming analytics pipeline for monitoring real-time highway "
        "traffic conditions and detecting congestion and accident anomalies. A Python data producer generates time-stamped "
        "traffic events for vehicle count, average vehicle speed, traffic density and road occupancy based on historical "
        "roadway benchmarks. Apache Kafka transports the events, a Python stream processor evaluates incoming readings using "
        "a sliding-window aggregation and an Isolation Forest machine learning model for anomaly scoring, and SQLite stores "
        "processed readings, traffic metrics and incident alerts. A Streamlit dashboard presents roadway status, speed trends, "
        "congestion index dynamics and detected anomaly alerts with automatic refresh. This is an educational prototype using "
        "simulated traffic and historical data; its alerts are an intelligent monitoring prototype for data stream analytics."
    )
    story.append(Paragraph(abstract_text, style_abstract_body))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: INTRODUCTION, OBJECTIVES, SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("1. Introduction", style_h1))
    intro_text = (
        "Urban highway networks may experience abnormal conditions such as severe congestion, sudden speed collapses, "
        "abnormal density spikes or potential accident disruptions. Streaming analytics can process sensor readings continuously "
        "and display unusual values as they arrive. This project demonstrates that workflow with historical and simulated "
        "traffic data and a local software stack. The dashboard includes five example corridors: Highway-101-North, "
        "Highway-101-South, Interstate-80-East, Interstate-80-West, and Downtown-Expressway."
    )
    story.append(Paragraph(intro_text, style_body))

    story.append(Paragraph("2. Objectives", style_h1))
    objectives = [
        "Generate time-stamped traffic sensor events using Python.",
        "Transport events through an Apache Kafka topic.",
        "Apply sliding-window calculations and Isolation Forest anomaly scoring to incoming readings.",
        "Store events, metrics and anomaly flags in SQLite.",
        "Display roadway corridor status, telemetry trends and anomaly records in a refreshing dashboard.",
        "Demonstrate the complete flow from data source to visualization."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", style_bullet))

    story.append(Paragraph("3. System Architecture", style_h1))
    story.append(Paragraph("The system follows six connected layers:", style_body))

    arch_box_data = [
        [Paragraph("<b>1. Data source</b><br/>Python producer generates simulated and historical vehicle count, speed, density and occupancy readings.", style_body)],
        [Paragraph("<b>2. Streaming platform</b><br/>Apache Kafka topic: traffic-events.", style_body)],
        [Paragraph("<b>3. Stream processor</b><br/>Python consumer reads events and computes a rolling speed and density average.", style_body)],
        [Paragraph("<b>4. Machine learning</b><br/>Isolation Forest anomaly scoring using five traffic features.", style_body)],
        [Paragraph("<b>5. Database</b><br/>SQLite database traffic_analytics.db; tables traffic_events, traffic_metrics, traffic_alerts.", style_body)],
        [Paragraph("<b>6. Visualization</b><br/>Streamlit dashboard at http://localhost:8501 with KPIs, charts and anomaly alerts.", style_body)],
    ]
    t_arch_box = Table(arch_box_data, colWidths=[520])
    t_arch_box.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_arch_box)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ARCHITECTURE DIAGRAM & TECHNOLOGIES
    # =========================================================================
    story.append(Paragraph("Figure: End-to-end architecture and data flow", style_h2))
    arch_img_path = "report_images/architecture_diagram.png"
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=490, height=390))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Technologies Used", style_h1))
    tech_data_p4 = [
        [Paragraph("<b>Technology</b>", style_body), Paragraph("<b>Purpose</b>", style_body)],
        [Paragraph("<b>Python</b>", style_body), Paragraph("Traffic event generation, stream processing and model integration", style_body)],
        [Paragraph("<b>Apache Kafka</b>", style_body), Paragraph("Event streaming and producer/consumer messaging", style_body)],
        [Paragraph("<b>scikit-learn / Isolation Forest</b>", style_body), Paragraph("Unsupervised anomaly detection", style_body)]
    ]
    t_tech_p4 = Table(tech_data_p4, colWidths=[200, 320])
    t_tech_p4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2C59")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech_p4)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TECHNOLOGIES (CONT) & IMPLEMENTATION
    # =========================================================================
    tech_data_p5 = [
        [Paragraph("<b>SQLite</b>", style_body), Paragraph("Persistent storage of traffic readings, metrics and anomaly alerts", style_body)],
        [Paragraph("<b>Streamlit</b>", style_body), Paragraph("Interactive dashboard and periodic refresh", style_body)],
        [Paragraph("<b>Pandas / joblib</b>", style_body), Paragraph("Feature preparation and model persistence", style_body)]
    ]
    t_tech_p5 = Table(tech_data_p5, colWidths=[200, 320])
    t_tech_p5.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech_p5)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Implementation", style_h1))
    story.append(Paragraph("5.1 Traffic data generation", style_h2))
    story.append(Paragraph(
        "The producer emits events with a roadway identifier and telemetric measurements. Normal readings are "
        "generated around baseline values, while selected events simulate high vehicle volume, sudden speed reduction, "
        "high density or incident disruptions.", style_body
    ))
    story.append(Paragraph("Traffic fields and their purpose", style_h3))

    fields_data = [
        [Paragraph("<b>Field</b>", style_body), Paragraph("<b>Meaning / unit</b>", style_body), Paragraph("<b>Monitoring purpose</b>", style_body)],
        [Paragraph("location", style_body), Paragraph("Roadway corridor identifier (e.g., Highway-101-North)", style_body), Paragraph("Associates each event with a roadway segment", style_body)],
        [Paragraph("vehicle_count", style_body), Paragraph("Vehicle count per interval (vehicles)", style_body), Paragraph("Measures traffic volume and queue buildup", style_body)],
        [Paragraph("average_speed", style_body), Paragraph("Average vehicle speed (km/h)", style_body), Paragraph("Identifies sudden deceleration and speed collapse", style_body)],
        [Paragraph("traffic_density", style_body), Paragraph("Traffic density (veh/km)", style_body), Paragraph("Quantifies spatial concentration of vehicles", style_body)],
        [Paragraph("road_occupancy", style_body), Paragraph("Road occupancy (%)", style_body), Paragraph("Indicates lane blockage and physical road saturation", style_body)]
    ]
    t_fields = Table(fields_data, colWidths=[110, 200, 210])
    t_fields.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#DCE6F1")),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_fields)
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.2 Kafka streaming", style_h2))
    story.append(Paragraph(
        "The producer publishes JSON events to traffic-events. The processor consumes events from this topic, "
        "separating event generation from downstream processing.", style_body
    ))

    story.append(Paragraph("5.3 Stream processing and anomaly detection", style_h2))
    story.append(Paragraph(
        "The processor prepares the incoming traffic features and scores each reading with the trained Isolation Forest "
        "model. The producer also injects simulated incident examples to demonstrate abnormal conditions. In the "
        "processor code, anomaly flags are based on the model prediction combined with explicit speed collapse "
        "heuristics for accident triage.", style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: MODEL TRAINING, DATABASE, DASHBOARD, SCREENSHOTS INTRO
    # =========================================================================
    story.append(Paragraph("5.3.1 Model training and live scoring", style_h2))
    story.append(Paragraph(
        "The project separates model training from live stream processing. The training script (train_model.py) generates "
        "2,500 synthetic normal-operation records using a fixed random seed (42), then trains an Isolation Forest with "
        "100 trees (n_estimators=100), contamination=0.05 and random_state=42. The five model features are average_speed, "
        "vehicle_count, traffic_density, road_occupancy and speed_ratio. The trained estimator is saved as isolation_forest.pkl. "
        "During streaming, predict.py uses the same features and classifies incoming readings into Normal traffic (score >= 0.0), "
        "Unusual traffic pattern (-0.08 <= score < 0.0), and Severe traffic anomaly (score < -0.08).", style_body
    ))
    story.append(Paragraph(
        "The processor computes a rolling average over the most recent 15 speed readings for display and context. The producer "
        "injects simulated scenarios (Normal Traffic, Traffic Congestion, and Accident Scenario). These demonstrate "
        "abnormal conditions across three distinct operational regimes. No precision, recall or accuracy is fabricated because "
        "no independent labeled real-world collision dataset was claimed.", style_body
    ))

    story.append(Paragraph("5.4 Database storage", style_h2))
    story.append(Paragraph(
        "Processed events are stored in the SQLite traffic_analytics.db database in the traffic_events, traffic_metrics, "
        "and traffic_alerts tables with Write-Ahead Logging (WAL) concurrency.", style_body
    ))

    story.append(Paragraph("5.5 Dashboard", style_h2))
    story.append(Paragraph(
        "The Streamlit interface displays service-status indicators, roadway corridor cards, latest-value KPIs, telemetry "
        "charts, speed versus rolling average, congestion index dynamics, and a detected anomaly table. The dashboard "
        "utilizes a 2.5-second automatic refresh.", style_body
    ))

    story.append(Paragraph("6. Dashboard Screenshots", style_h1))
    story.append(Paragraph(
        "The following screenshots were supplied from the project dashboard and are included as visual evidence of the "
        "interface and displayed telemetry.", style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: FIGURES 1 & 2
    # =========================================================================
    story.append(Paragraph("Figure 1. Roadway corridor status and latest KPIs", style_h2))
    fig1_path = "report_images/figure1_kpis.png"
    if os.path.exists(fig1_path):
        story.append(Image(fig1_path, width=520, height=170))
    story.append(Paragraph(
        "Figure 1: Roadway status for Highway-101-North, Highway-101-South, Interstate-80-East, Interstate-80-West and "
        "Downtown-Expressway, latest traffic metrics, anomaly count and telemetry section.", style_caption
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Figure 2. Real-time traffic telemetry and congestion dynamics", style_h2))
    fig2_path = "report_images/figure2_charts.png"
    if os.path.exists(fig2_path):
        story.append(Image(fig2_path, width=520, height=220))
    story.append(Paragraph(
        "Figure 2: Average speed and congestion index dynamics, including rolling average speed and corridor congestion percentage.", style_caption
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: FIGURE 3 & RESULTS
    # =========================================================================
    story.append(Paragraph("Figure 3. Detected anomaly and accident alerts", style_h2))
    fig3_path = "report_images/figure3_alerts.png"
    if os.path.exists(fig3_path):
        story.append(Image(fig3_path, width=520, height=150))
    story.append(Paragraph(
        "Figure 3: Anomaly alert table showing timestamps, roadway identifiers, alert types, severity levels and flagged events.", style_caption
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("7. Verification and Results", style_h1))
    story.append(Paragraph(
        "The following results are taken from the verification output supplied by the project setup tool. "
        "They are reported test evidence, not an independent audit of the computer.", style_body
    ))

    res_table_data = [
        [Paragraph("<b>Check</b>", style_body), Paragraph("<b>Status</b>", style_body), Paragraph("<b>Reported evidence</b>", style_body)],
        [Paragraph("<b>Dashboard availability</b>", style_body), Paragraph("PASS (reported)", style_body), Paragraph("HTTP 200 at localhost:8501; dashboard UI reportedly loaded.", style_body)],
        [Paragraph("<b>Automatic updates</b>", style_body), Paragraph("PASS (reported)", style_body), Paragraph("Readings reportedly changed across refreshes; refresh interval set to 2.5 seconds.", style_body)],
        [Paragraph("<b>SQLite persistence</b>", style_body), Paragraph("PASS (reported)", style_body), Paragraph("Row count increased from 15 to 25 during observation; WAL mode enabled.", style_body)],
        [Paragraph("<b>Anomaly & accident alerts</b>", style_body), Paragraph("PASS (reported)", style_body), Paragraph("Speed collapse (<15 km/h) and accident collision examples reportedly flagged in SQLite.", style_body)],
        [Paragraph("<b>Producer/processor logs</b>", style_body), Paragraph("PASS (reported)", style_body), Paragraph("Verification output reported no recurring errors during its observation period.", style_body)],
    ]
    t_res = Table(res_table_data, colWidths=[150, 110, 260])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2C59")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COL),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_res)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: LIMITATIONS, FUTURE ENHANCEMENTS, HOW TO RUN
    # =========================================================================
    story.append(Paragraph(
        "The anomaly count displayed in the screenshots can vary with the selected time window and database query; "
        "it should not be interpreted as a fixed total.", style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("8. Limitations", style_h1))
    limits = [
        "Traffic readings are simulated rather than collected from physical highway loop sensors or CCTV cameras.",
        "Results depend on synthetic training data and Isolation Forest settings. Simulated fault and accident values are injected by the producer.",
        "A flagged reading indicates a model-identified outlier; it does not prove that an accident has occurred without correlation.",
        "The prototype has not been validated for safety-critical emergency response systems.",
        "Operation depends on Kafka, Python processes, SQLite and Streamlit remaining available."
    ]
    for lim in limits:
        story.append(Paragraph(f"• {lim}", style_bullet))

    story.append(Paragraph("9. Future Enhancements", style_h1))
    enhancements = [
        "Connect real sensors or open municipal traffic IoT gateways.",
        "Evaluate model precision and recall using larger labeled traffic incident benchmarks.",
        "Add automated emergency notifications and incident acknowledgement workflows.",
        "Implement spatial Graph Neural Networks (GNN) to model multi-corridor congestion spillover.",
        "Add service health checks, structured logging and reproducible containerized deployment."
    ]
    for enh in enhancements:
        story.append(Paragraph(f"• {enh}", style_bullet))

    story.append(Paragraph("10. How to Run the Project", style_h1))
    story.append(Paragraph("Prerequisites and one-time setup", style_h2))
    story.append(Paragraph(
        "Use Windows with a supported Python installation, a running local Kafka broker and SQLite. "
        "From the project folder, create and activate a virtual environment, then install dependencies:", style_body
    ))
    story.append(Paragraph("py -3.11 -m venv .venv", style_code))
    story.append(Paragraph(".venv\\Scripts\\activate", style_code))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: RUN INSTRUCTIONS (TERMINALS)
    # =========================================================================
    story.append(Paragraph("python -m pip install -r requirements.txt", style_code))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Before starting the pipeline, initialize database/traffic_analytics.db with python database/db_setup.py, "
        "confirm that Kafka is reachable at the configured address (localhost:9092) and that topic traffic-events exists, "
        "then train the model once with python ml/train_model.py so models/isolation_forest.pkl is available. "
        "Use the Kafka startup command and storage configuration appropriate to the Kafka version already installed. "
        "Alternatively, run the master PowerShell script .\\run_pipeline.ps1 to start all services automatically.", style_body
    ))
    story.append(Paragraph(
        "To run components manually in separate terminals, follow these steps:", style_body
    ))

    story.append(Paragraph("Terminal 1 — Kafka broker", style_term_h))
    story.append(Paragraph("cd C:\\kafka", style_code))
    story.append(Paragraph(".\\bin\\windows\\zookeeper-server-start.bat .\\config\\zookeeper.properties", style_code))
    story.append(Paragraph(".\\bin\\windows\\kafka-server-start.bat .\\config\\server.properties", style_code))

    story.append(Paragraph("Terminal 2 — Stream processor", style_term_h))
    story.append(Paragraph("In a new PowerShell terminal, change to the project folder, activate the virtual environment, then run:", style_body))
    story.append(Paragraph("cd C:\\Users\\Dell\\Downloads\\Real_Time_Traffic_Congestion", style_code))
    story.append(Paragraph(".\\.venv\\Scripts\\Activate.ps1", style_code))
    story.append(Paragraph("python processor/traffic_processor.py", style_code))

    story.append(Paragraph("Terminal 3 — Traffic producer", style_term_h))
    story.append(Paragraph("In a separate PowerShell terminal, change to the project folder, activate the virtual environment, then run:", style_body))
    story.append(Paragraph("cd C:\\Users\\Dell\\Downloads\\Real_Time_Traffic_Congestion", style_code))
    story.append(Paragraph(".\\.venv\\Scripts\\Activate.ps1", style_code))
    story.append(Paragraph("python producer/traffic_producer.py", style_code))

    story.append(Paragraph("Terminal 4 — Dashboard", style_term_h))
    story.append(Paragraph("In a separate PowerShell terminal, change to the project folder, activate the virtual environment, then run:", style_body))
    story.append(Paragraph("cd C:\\Users\\Dell\\Downloads\\Real_Time_Traffic_Congestion", style_code))
    story.append(Paragraph(".\\.venv\\Scripts\\Activate.ps1", style_code))
    story.append(Paragraph("streamlit run dashboard/app.py --server.port 8501", style_code))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CONCLUSION, REFERENCES, REPOSITORY
    # =========================================================================
    story.append(Paragraph("Open http://localhost:8501 in a browser.", style_body))
    story.append(Spacer(1, 10))

    story.append(Paragraph("11. Conclusion", style_h1))
    story.append(Paragraph(
        "This project demonstrates the main components of a real-time stream analytics system: generating traffic "
        "events, transporting them through Kafka, applying sliding-window calculations and Isolation Forest anomaly "
        "detection, persisting results in SQLite and visualizing the stream in an auto-refreshing dashboard. "
        "The screenshots illustrate the roadway corridor overview, sensor telemetry and anomaly alert table. "
        "The prototype can be extended with real highway loop detectors, formal model evaluation and secure deployment.", style_body
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("References", style_h1))
    refs = [
        "Apache Kafka documentation — event streaming and producer/consumer concepts. https://kafka.apache.org/documentation/",
        "scikit-learn documentation — Isolation Forest estimator. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html",
        "SQLite documentation — relational database engine. https://www.sqlite.org/docs.html",
        "Streamlit documentation — interactive Python data applications. https://docs.streamlit.io/"
    ]
    for ref in refs:
        story.append(Paragraph(f"• {ref}", style_bullet))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Project Repository", style_h1))
    story.append(Paragraph("Source code, setup instructions, and project files are available at:", style_body))
    story.append(Paragraph("https://github.com/26yashu/real-time-traffic-congestion", style_bullet))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated 11-page PDF Report: {filename}")

if __name__ == "__main__":
    build_pdf_report()
