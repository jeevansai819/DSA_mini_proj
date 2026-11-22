"""
Generates the Microsoft Word (.docx) version matching the 11-page template format.
Includes Cover page, Abstract, Section 1 through 11, Tables, Figures, Code Blocks, and References.
"""
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_docx_report(output_path="Real_Time_Traffic_Congestion_Project_Report.docx"):
    doc = Document()
    
    # 0.8 inch margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
        # Running footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f_r = f_p.add_run("Data Stream Analytics Mini-Project")
        f_r.font.size = Pt(8.5)
        f_r.font.color.rgb = RGBColor(100, 116, 139)

    def set_cell_background(cell, fill_hex):
        shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(26, 54, 93)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(26, 54, 93)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_code(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.25)
        r = p.add_run(text)
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(8)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.italic = True
        r.font.color.rgb = RGBColor(100, 116, 139)
        return p

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    for _ in range(4):
        doc.add_paragraph()
    
    p_main = doc.add_paragraph()
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_main = p_main.add_run("PROJECT REPORT")
    r_main.font.name = "Arial"
    r_main.font.size = Pt(26)
    r_main.font.bold = True
    
    doc.add_paragraph()
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("REAL-TIME TRAFFIC CONGESTION AND ACCIDENT DETECTION SYSTEM")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(26, 54, 93)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("A Data Stream Analytics Mini-Project")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(43, 108, 176)
    
    p_repo = doc.add_paragraph()
    p_repo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_repo = p_repo.add_run("GitHub Repository: https://github.com/26yashu/real-time-traffic-congestion")
    r_repo.font.name = "Calibri"
    r_repo.font.size = Pt(10)
    r_repo.font.color.rgb = RGBColor(43, 108, 176)
    
    for _ in range(6):
        doc.add_paragraph()
        
    meta_lines = [
        ("Submitted to: ", "Shahad P"),
        ("Submitted by: ", "Gandlaparthi Yaswanthi"),
        ("USN: ", "23BTRCL187"),
        ("Department: ", "CSE-AIML(D)")
    ]
    for lbl, val in meta_lines:
        p_m = doc.add_paragraph()
        p_m.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_m.paragraph_format.space_after = Pt(3)
        r_lbl = p_m.add_run(lbl)
        r_lbl.font.size = Pt(12)
        r_val = p_m.add_run(val)
        r_val.font.size = Pt(12)
        r_val.font.bold = True
        
    doc.add_page_break()

    # =========================================================================
    # PAGE 2: ABSTRACT
    # =========================================================================
    for _ in range(3):
        doc.add_paragraph()
        
    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_abs_h = p_abs_h.add_run("Abstract")
    r_abs_h.font.name = "Arial"
    r_abs_h.font.size = Pt(20)
    r_abs_h.font.bold = True
    r_abs_h.font.color.rgb = RGBColor(26, 54, 93)
    
    doc.add_paragraph()
    
    add_p(
        "This project demonstrates an end-to-end streaming analytics pipeline for monitoring real-time highway "
        "traffic conditions and detecting congestion and accident anomalies. A Python data producer generates time-stamped "
        "traffic events for vehicle count, average vehicle speed, traffic density and road occupancy based on historical "
        "roadway benchmarks. Apache Kafka transports the events, a Python stream processor evaluates incoming readings using "
        "a sliding-window aggregation and an Isolation Forest machine learning model for anomaly scoring, and SQLite stores "
        "processed readings, traffic metrics and incident alerts. A Streamlit dashboard presents roadway status, speed trends, "
        "congestion index dynamics and detected anomaly alerts with automatic refresh. This is an educational prototype using "
        "simulated traffic and historical data; its alerts are an intelligent monitoring prototype for data stream analytics."
    )
    doc.add_page_break()

    # =========================================================================
    # PAGE 3: INTRODUCTION, OBJECTIVES, SYSTEM ARCHITECTURE
    # =========================================================================
    add_h1("1. Introduction")
    add_p(
        "Urban highway networks may experience abnormal conditions such as severe congestion, sudden speed collapses, "
        "abnormal density spikes or potential accident disruptions. Streaming analytics can process sensor readings continuously "
        "and display unusual values as they arrive. This project demonstrates that workflow with historical and simulated "
        "traffic data and a local software stack. The dashboard includes five example corridors: Highway-101-North, "
        "Highway-101-South, Interstate-80-East, Interstate-80-West, and Downtown-Expressway."
    )

    add_h1("2. Objectives")
    objectives = [
        "Generate time-stamped traffic sensor events using Python.",
        "Transport events through an Apache Kafka topic.",
        "Apply sliding-window calculations and Isolation Forest anomaly scoring to incoming readings.",
        "Store events, metrics and anomaly flags in SQLite.",
        "Display roadway corridor status, telemetry trends and anomaly records in a refreshing dashboard.",
        "Demonstrate the complete flow from data source to visualization."
    ]
    for obj in objectives:
        add_bullet(obj)

    add_h1("3. System Architecture")
    add_p("The system follows six connected layers:")
    
    t_arch = doc.add_table(rows=6, cols=1)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_layers = [
        ("1. Data source", "Python producer generates simulated and historical vehicle count, speed, density and occupancy readings."),
        ("2. Streaming platform", "Apache Kafka topic: traffic-events."),
        ("3. Stream processor", "Python consumer reads events and computes a rolling speed and density average."),
        ("4. Machine learning", "Isolation Forest anomaly scoring using five traffic features."),
        ("5. Database", "SQLite database traffic_analytics.db; tables traffic_events, traffic_metrics, traffic_alerts."),
        ("6. Visualization", "Streamlit dashboard at http://localhost:8501 with KPIs, charts and anomaly alerts.")
    ]
    for idx, (lt, ld) in enumerate(arch_layers):
        cell = t_arch.cell(idx, 0)
        cell.width = Inches(6.8)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(lt + "\n")
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r2 = p.add_run(ld)
        r2.font.size = Pt(9.5)
    doc.add_page_break()

    # =========================================================================
    # PAGE 4: ARCHITECTURE DIAGRAM & TECHNOLOGIES
    # =========================================================================
    add_h2("Figure: End-to-end architecture and data flow")
    arch_img_path = "report_images/architecture_diagram.png"
    if os.path.exists(arch_img_path):
        doc.add_picture(arch_img_path, width=Inches(6.2))
        
    add_h1("4. Technologies Used")
    tech_table_p4 = doc.add_table(rows=4, cols=2)
    tech_table_p4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_p4_data = [
        ("Technology", "Purpose"),
        ("Python", "Traffic event generation, stream processing and model integration"),
        ("Apache Kafka", "Event streaming and producer/consumer messaging"),
        ("scikit-learn / Isolation Forest", "Unsupervised anomaly detection")
    ]
    for ridx, (tech, purp) in enumerate(t_p4_data):
        c0 = tech_table_p4.cell(ridx, 0)
        c1 = tech_table_p4.cell(ridx, 1)
        c0.width = Inches(2.6)
        c1.width = Inches(4.2)
        if ridx == 0:
            set_cell_background(c0, "0F2C59")
            set_cell_background(c1, "0F2C59")
            r0 = c0.paragraphs[0].add_run(tech)
            r1 = c1.paragraphs[0].add_run(purp)
            r0.font.bold = True
            r1.font.bold = True
            r0.font.color.rgb = RGBColor(255, 255, 255)
            r1.font.color.rgb = RGBColor(255, 255, 255)
        else:
            c0.paragraphs[0].add_run(tech).font.bold = True
            c1.paragraphs[0].add_run(purp)
    doc.add_page_break()

    # =========================================================================
    # PAGE 5: TECHNOLOGIES (CONT) & IMPLEMENTATION
    # =========================================================================
    tech_table_p5 = doc.add_table(rows=3, cols=2)
    tech_table_p5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_p5_data = [
        ("SQLite", "Persistent storage of traffic readings, metrics and anomaly alerts"),
        ("Streamlit", "Interactive dashboard and periodic refresh"),
        ("Pandas / joblib", "Feature preparation and model persistence")
    ]
    for ridx, (tech, purp) in enumerate(t_p5_data):
        c0 = tech_table_p5.cell(ridx, 0)
        c1 = tech_table_p5.cell(ridx, 1)
        c0.width = Inches(2.6)
        c1.width = Inches(4.2)
        c0.paragraphs[0].add_run(tech).font.bold = True
        c1.paragraphs[0].add_run(purp)
        
    add_h1("5. Implementation")
    add_h2("5.1 Traffic data generation")
    add_p(
        "The producer emits events with a roadway identifier and telemetric measurements. Normal readings are "
        "generated around baseline values, while selected events simulate high vehicle volume, sudden speed reduction, "
        "high density or incident disruptions."
    )
    add_h3("Traffic fields and their purpose")
    
    fields_table = doc.add_table(rows=6, cols=3)
    fields_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    f_data = [
        ("Field", "Meaning / unit", "Monitoring purpose"),
        ("location", "Roadway corridor identifier (e.g., Highway-101-North)", "Associates each event with a roadway segment"),
        ("vehicle_count", "Vehicle count per interval (vehicles)", "Measures traffic volume and queue buildup"),
        ("average_speed", "Average vehicle speed (km/h)", "Identifies sudden deceleration and speed collapse"),
        ("traffic_density", "Traffic density (veh/km)", "Quantifies spatial concentration of vehicles"),
        ("road_occupancy", "Road occupancy (%)", "Indicates lane blockage and physical road saturation")
    ]
    for ridx, (fld, mean, purp) in enumerate(f_data):
        c0 = fields_table.cell(ridx, 0)
        c1 = fields_table.cell(ridx, 1)
        c2 = fields_table.cell(ridx, 2)
        c0.width = Inches(1.5)
        c1.width = Inches(2.6)
        c2.width = Inches(2.7)
        if ridx == 0:
            set_cell_background(c0, "DCE6F1")
            set_cell_background(c1, "DCE6F1")
            set_cell_background(c2, "DCE6F1")
            c0.paragraphs[0].add_run(fld).font.bold = True
            c1.paragraphs[0].add_run(mean).font.bold = True
            c2.paragraphs[0].add_run(purp).font.bold = True
        else:
            c0.paragraphs[0].add_run(fld).font.bold = True
            c1.paragraphs[0].add_run(mean)
            c2.paragraphs[0].add_run(purp)

    add_h2("5.2 Kafka streaming")
    add_p("The producer publishes JSON events to traffic-events. The processor consumes events from this topic, separating event generation from downstream processing.")

    add_h2("5.3 Stream processing and anomaly detection")
    add_p("The processor prepares the incoming traffic features and scores each reading with the trained Isolation Forest model. The producer also injects simulated incident examples to demonstrate abnormal conditions. In the processor code, anomaly flags are based on the model prediction combined with explicit speed collapse heuristics for accident triage.")
    doc.add_page_break()

    # =========================================================================
    # PAGE 6: MODEL TRAINING, DATABASE, DASHBOARD, SCREENSHOTS INTRO
    # =========================================================================
    add_h2("5.3.1 Model training and live scoring")
    add_p(
        "The project separates model training from live stream processing. The training script (train_model.py) generates "
        "2,500 synthetic normal-operation records using a fixed random seed (42), then trains an Isolation Forest with "
        "100 trees (n_estimators=100), contamination=0.05 and random_state=42. The five model features are average_speed, "
        "vehicle_count, traffic_density, road_occupancy and speed_ratio. The trained estimator is saved as isolation_forest.pkl. "
        "During streaming, predict.py uses the same features and classifies incoming readings into Normal traffic (score >= 0.0), "
        "Unusual traffic pattern (-0.08 <= score < 0.0), and Severe traffic anomaly (score < -0.08)."
    )
    add_p(
        "The processor computes a rolling average over the most recent 15 speed readings for display and context. The producer "
        "injects simulated scenarios (Normal Traffic, Traffic Congestion, and Accident Scenario). These demonstrate "
        "abnormal conditions across three distinct operational regimes. No precision, recall or accuracy is fabricated because "
        "no independent labeled real-world collision dataset was claimed."
    )
    add_h2("5.4 Database storage")
    add_p("Processed events are stored in the SQLite traffic_analytics.db database in the traffic_events, traffic_metrics, and traffic_alerts tables with Write-Ahead Logging (WAL) concurrency.")

    add_h2("5.5 Dashboard")
    add_p("The Streamlit interface displays service-status indicators, roadway corridor cards, latest-value KPIs, telemetry charts, speed versus rolling average, congestion index dynamics, and a detected anomaly table. The dashboard utilizes a 2.5-second automatic refresh.")

    add_h1("6. Dashboard Screenshots")
    add_p("The following screenshots were supplied from the project dashboard and are included as visual evidence of the interface and displayed telemetry.")
    doc.add_page_break()

    # =========================================================================
    # PAGE 7: FIGURES 1 & 2
    # =========================================================================
    add_h2("Figure 1. Roadway corridor status and latest KPIs")
    fig1_path = "report_images/figure1_kpis.png"
    if os.path.exists(fig1_path):
        doc.add_picture(fig1_path, width=Inches(6.4))
    add_caption("Figure 1: Roadway status for Highway-101-North, Highway-101-South, Interstate-80-East, Interstate-80-West and Downtown-Expressway, latest traffic metrics, anomaly count and telemetry section.")

    add_h2("Figure 2. Real-time traffic telemetry and congestion dynamics")
    fig2_path = "report_images/figure2_charts.png"
    if os.path.exists(fig2_path):
        doc.add_picture(fig2_path, width=Inches(6.4))
    add_caption("Figure 2: Average speed and congestion index dynamics, including rolling average speed and corridor congestion percentage.")
    doc.add_page_break()

    # =========================================================================
    # PAGE 8: FIGURE 3 & RESULTS
    # =========================================================================
    add_h2("Figure 3. Detected anomaly and accident alerts")
    fig3_path = "report_images/figure3_alerts.png"
    if os.path.exists(fig3_path):
        doc.add_picture(fig3_path, width=Inches(6.4))
    add_caption("Figure 3: Anomaly alert table showing timestamps, roadway identifiers, alert types, severity levels and flagged events.")

    add_h1("7. Verification and Results")
    add_p("The following results are taken from the verification output supplied by the project setup tool. They are reported test evidence, not an independent audit of the computer.")

    res_table = doc.add_table(rows=6, cols=3)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_data = [
        ("Check", "Status", "Reported evidence"),
        ("Dashboard availability", "PASS (reported)", "HTTP 200 at localhost:8501; dashboard UI reportedly loaded."),
        ("Automatic updates", "PASS (reported)", "Readings reportedly changed across refreshes; refresh interval set to 2.5 seconds."),
        ("SQLite persistence", "PASS (reported)", "Row count increased from 15 to 25 during observation; WAL mode enabled."),
        ("Anomaly & accident alerts", "PASS (reported)", "Speed collapse (<15 km/h) and accident collision examples reportedly flagged in SQLite."),
        ("Producer/processor logs", "PASS (reported)", "Verification output reported no recurring errors during its observation period.")
    ]
    for ridx, (chk, st, ev) in enumerate(r_data):
        c0 = res_table.cell(ridx, 0)
        c1 = res_table.cell(ridx, 1)
        c2 = res_table.cell(ridx, 2)
        c0.width = Inches(2.0)
        c1.width = Inches(1.5)
        c2.width = Inches(3.3)
        if ridx == 0:
            set_cell_background(c0, "0F2C59")
            set_cell_background(c1, "0F2C59")
            set_cell_background(c2, "0F2C59")
            for c, txt in [(c0, chk), (c1, st), (c2, ev)]:
                r = c.paragraphs[0].add_run(txt)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
        else:
            c0.paragraphs[0].add_run(chk).font.bold = True
            c1.paragraphs[0].add_run(st)
            c2.paragraphs[0].add_run(ev)
    doc.add_page_break()

    # =========================================================================
    # PAGE 9: LIMITATIONS, FUTURE ENHANCEMENTS, HOW TO RUN
    # =========================================================================
    add_p("The anomaly count displayed in the screenshots can vary with the selected time window and database query; it should not be interpreted as a fixed total.")
    
    add_h1("8. Limitations")
    limits = [
        "Traffic readings are simulated rather than collected from physical highway loop sensors or CCTV cameras.",
        "Results depend on synthetic training data and Isolation Forest settings. Simulated fault and accident values are injected by the producer.",
        "A flagged reading indicates a model-identified outlier; it does not prove that an accident has occurred without correlation.",
        "The prototype has not been validated for safety-critical emergency response systems.",
        "Operation depends on Kafka, Python processes, SQLite and Streamlit remaining available."
    ]
    for lim in limits:
        add_bullet(lim)

    add_h1("9. Future Enhancements")
    enhancements = [
        "Connect real sensors or open municipal traffic IoT gateways.",
        "Evaluate model precision and recall using larger labeled traffic incident benchmarks.",
        "Add automated emergency notifications and incident acknowledgement workflows.",
        "Implement spatial Graph Neural Networks (GNN) to model multi-corridor congestion spillover.",
        "Add service health checks, structured logging and reproducible containerized deployment."
    ]
    for enh in enhancements:
        add_bullet(enh)

    add_h1("10. How to Run the Project")
    add_h2("Prerequisites and one-time setup")
    add_p("Use Windows with a supported Python installation, a running local Kafka broker and SQLite. From the project folder, create and activate a virtual environment, then install dependencies:")
    add_code("py -3.11 -m venv .venv")
    add_code(".venv\\Scripts\\activate")
    doc.add_page_break()

    # =========================================================================
    # PAGE 10: RUN INSTRUCTIONS (TERMINALS)
    # =========================================================================
    add_code("python -m pip install -r requirements.txt")
    add_p(
        "Before starting the pipeline, initialize database/traffic_analytics.db with python database/db_setup.py, "
        "confirm that Kafka is reachable at the configured address (localhost:9092) and that topic traffic-events exists, "
        "then train the model once with python ml/train_model.py so models/isolation_forest.pkl is available. "
        "Use the Kafka startup command and storage configuration appropriate to the Kafka version already installed. "
        "Alternatively, run the master PowerShell script .\\run_pipeline.ps1 to start all services automatically."
    )
    add_p("To run components manually in separate terminals, follow these steps:")

    add_h2("Terminal 1 — Kafka broker")
    add_code("cd C:\\kafka")
    add_code(".\\bin\\windows\\zookeeper-server-start.bat .\\config\\zookeeper.properties")
    add_code(".\\bin\\windows\\kafka-server-start.bat .\\config\\server.properties")

    add_h2("Terminal 2 — Stream processor")
    add_p("In a new PowerShell terminal, change to the project folder, activate the virtual environment, then run:")
    add_code("cd C:\\Users\\Dell\\Downloads\\Real_Time_Traffic_Congestion")
    add_code(".\\.venv\\Scripts\\Activate.ps1")
    add_code("python processor/traffic_processor.py")

    add_h2("Terminal 3 — Traffic producer")
    add_p("In a separate PowerShell terminal, change to the project folder, activate the virtual environment, then run:")
    add_code("cd C:\\Users\\Dell\\Downloads\\Real_Time_Traffic_Congestion")
    add_code(".\\.venv\\Scripts\\Activate.ps1")
    add_code("python producer/traffic_producer.py")

    add_h2("Terminal 4 — Dashboard")
    add_p("In a separate PowerShell terminal, change to the project folder, activate the virtual environment, then run:")
    add_code("cd C:\\Users\\Dell\\Downloads\\Real_Time_Traffic_Congestion")
    add_code(".\\.venv\\Scripts\\Activate.ps1")
    add_code("streamlit run dashboard/app.py --server.port 8501")
    doc.add_page_break()

    # =========================================================================
    # PAGE 11: CONCLUSION, REFERENCES, REPOSITORY
    # =========================================================================
    add_p("Open http://localhost:8501 in a browser.")

    add_h1("11. Conclusion")
    add_p(
        "This project demonstrates the main components of a real-time stream analytics system: generating traffic "
        "events, transporting them through Kafka, applying sliding-window calculations and Isolation Forest anomaly "
        "detection, persisting results in SQLite and visualizing the stream in an auto-refreshing dashboard. "
        "The screenshots illustrate the roadway corridor overview, sensor telemetry and anomaly alert table. "
        "The prototype can be extended with real highway loop detectors, formal model evaluation and secure deployment."
    )

    add_h1("References")
    refs = [
        "Apache Kafka documentation — event streaming and producer/consumer concepts. https://kafka.apache.org/documentation/",
        "scikit-learn documentation — Isolation Forest estimator. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html",
        "SQLite documentation — relational database engine. https://www.sqlite.org/docs.html",
        "Streamlit documentation — interactive Python data applications. https://docs.streamlit.io/"
    ]
    for ref in refs:
        add_bullet(ref)

    add_h1("Project Repository")
    add_p("Source code, setup instructions, and project files are available at:")
    add_bullet("https://github.com/26yashu/real-time-traffic-congestion")

    doc.save(output_path)
    print(f"Generated Word (.docx) matching template: {output_path}")

if __name__ == "__main__":
    create_docx_report()
