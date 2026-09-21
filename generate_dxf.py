import os

def create_kiosk_dxf():
    dxf_lines = [
        "0", "SECTION",
        "2", "HEADER",
        "9", "$ACADVER",
        "1", "AC1009",
        "0", "ENDSEC",
        "0", "SECTION",
        "2", "TABLES",
        "0", "TABLE",
        "2", "LAYER",
        "70", "6",
        # Layer 0
        "0", "LAYER", "2", "0", "70", "0", "62", "7", "6", "CONTINUOUS",
        # Layer OUTLINE (Green)
        "0", "LAYER", "2", "OUTLINE", "70", "0", "62", "3", "6", "CONTINUOUS",
        # Layer COMPONENTS (Cyan)
        "0", "LAYER", "2", "COMPONENTS", "70", "0", "62", "4", "6", "CONTINUOUS",
        # Layer DOORS_LOCKS (Red)
        "0", "LAYER", "2", "DOORS_LOCKS", "70", "0", "62", "1", "6", "CONTINUOUS",
        # Layer DIMENSIONS (Yellow)
        "0", "LAYER", "2", "DIMENSIONS", "70", "0", "62", "2", "6", "CONTINUOUS",
        # Layer LABELS (White)
        "0", "LAYER", "2", "LABELS", "70", "0", "62", "7", "6", "CONTINUOUS",
        "0", "ENDTAB",
        "0", "ENDSEC",
        "0", "SECTION",
        "2", "ENTITIES"
    ]

    def add_line(x1, y1, x2, y2, layer="OUTLINE"):
        dxf_lines.extend([
            "0", "LINE",
            "8", layer,
            "10", f"{float(x1):.2f}",
            "20", f"{float(y1):.2f}",
            "30", "0.00",
            "11", f"{float(x2):.2f}",
            "21", f"{float(y2):.2f}",
            "31", "0.00"
        ])

    def add_rect(x, y, w, h, layer="OUTLINE"):
        add_line(x, y, x + w, y, layer)
        add_line(x + w, y, x + w, y + h, layer)
        add_line(x + w, y + h, x, y + h, layer)
        add_line(x, y + h, x, y, layer)

    def add_text(x, y, text, height=20.0, layer="LABELS"):
        dxf_lines.extend([
            "0", "TEXT",
            "8", layer,
            "10", f"{float(x):.2f}",
            "20", f"{float(y):.2f}",
            "30", "0.00",
            "40", f"{float(height):.2f}",
            "1", str(text)
        ])

    # ==========================================
    # 1. FRONT ELEVATION VIEW (X: 0 to 600, Y: 0 to 1650)
    # ==========================================
    add_text(120, 1720, "1. FRONT ELEVATION VIEW (Scale 1:1 mm)", 28, "LABELS")
    add_rect(0, 0, 600, 1650, "OUTLINE")

    # Top Brand / Header Panel (Z = 1480 to 1650)
    add_rect(20, 1480, 560, 150, "COMPONENTS")
    add_text(130, 1570, "BITTU XEROX 24/7", 24, "LABELS")
    add_text(150, 1515, "SMART CAMPUS PRINTING", 14, "LABELS")

    # 14-inch Touchscreen (Z = 1200 to 1440, Center = 1320)
    add_rect(130, 1200, 340, 240, "COMPONENTS")
    add_text(170, 1310, "14\" FHD TOUCHSCREEN", 18, "LABELS")
    # Camera & PIR Sensor & Speaker grill
    add_line(270, 1455, 330, 1455, "COMPONENTS")
    add_text(240, 1460, "[CAMERA & PIR SENSOR]", 11, "LABELS")

    # Ergonomic Sloped User Console (Z = 850 to 1150)
    add_rect(30, 860, 540, 290, "OUTLINE")
    # Metal PIN Pad
    add_rect(60, 920, 110, 150, "COMPONENTS")
    add_text(75, 985, "METAL KEYPAD", 13, "LABELS")
    # Physical Action Buttons
    add_rect(190, 1010, 60, 55, "COMPONENTS")
    add_text(198, 1030, "START", 11, "LABELS")
    add_rect(190, 930, 60, 55, "COMPONENTS")
    add_text(198, 950, "CANCEL", 11, "LABELS")
    # Smartphone Staging Dock & QR Code Scanner zone
    add_rect(280, 900, 260, 220, "COMPONENTS")
    add_text(300, 1040, "SMARTPHONE DOCK", 14, "LABELS")
    add_text(300, 990, "DYNAMIC UPI QR / NFC TAP", 12, "LABELS")
    add_text(300, 940, "DIRECT FAST-WIFI / UPLOAD", 11, "LABELS")

    # Flatbed Scanner Access Hatch (Z = 730 to 840)
    add_rect(40, 740, 520, 100, "COMPONENTS")
    add_text(150, 785, "CANON LiDE SCANNER HATCH", 16, "LABELS")

    # Finished Document Output Chute (Z = 530 to 640)
    add_rect(90, 540, 420, 80, "COMPONENTS")
    add_text(140, 575, "OUTPUT RETRIEVAL TRAY (A4)", 16, "LABELS")

    # Front Service Door (Z = 40 to 500)
    add_rect(25, 40, 550, 480, "DOORS_LOCKS")
    add_rect(285, 490, 30, 15, "DOORS_LOCKS")
    add_text(260, 510, "CAM LOCK", 11, "LABELS")

    # Louver Cooling Vents (Base)
    for vy in [90, 130, 170, 210]:
        add_line(70, vy, 210, vy, "COMPONENTS")
        add_line(240, vy, 370, vy, "COMPONENTS")
        add_line(400, vy, 530, vy, "COMPONENTS")
    add_text(170, 240, "POSITIVE PRESSURE AIR INTAKE", 13, "LABELS")

    # Front Dimensions
    add_line(-60, 0, -60, 1650, "DIMENSIONS")
    add_line(-75, 0, -45, 0, "DIMENSIONS")
    add_line(-75, 1650, -45, 1650, "DIMENSIONS")
    add_text(-200, 800, "TOTAL H = 1650 mm", 20, "DIMENSIONS")

    add_line(0, -60, 600, -60, "DIMENSIONS")
    add_line(0, -75, 0, -45, "DIMENSIONS")
    add_line(600, -75, 600, -45, "DIMENSIONS")
    add_text(220, -100, "WIDTH = 600 mm", 20, "DIMENSIONS")

    # ==========================================
    # 2. SIDE SECTION & ELEVATION VIEW (X: 850 to 1450, Y: 0 to 1650)
    # ==========================================
    add_text(920, 1720, "2. SIDE SECTION PROFILE VIEW (Depth: 600 mm)", 28, "LABELS")
    # Outer contour with ergonomic slope
    add_line(850, 0, 1450, 0, "OUTLINE")      # Base floor
    add_line(1450, 0, 1450, 1650, "OUTLINE")  # Rear vertical wall
    add_line(1450, 1650, 850, 1650, "OUTLINE") # Roof
    add_line(850, 1650, 850, 1180, "OUTLINE") # Upper front
    add_line(850, 1180, 800, 880, "OUTLINE")  # Ergonomic forward tilt console
    add_line(800, 880, 850, 840, "OUTLINE")   # Console return
    add_line(850, 840, 850, 0, "OUTLINE")     # Lower front wall

    # Internal Component Shelves
    add_line(860, 1170, 1430, 1170, "COMPONENTS") # Upper Logic & Display Shelf
    add_line(860, 730, 1430, 730, "COMPONENTS")   # Scanner Bay Shelf
    add_line(860, 500, 1430, 500, "COMPONENTS")   # Heavy-Duty Printer Shelf
    add_line(860, 230, 1430, 230, "COMPONENTS")   # Paper Stock Shelf
    add_line(860, 30, 1430, 30, "COMPONENTS")     # Heavy Power Base Shelf

    # Side View Hardware Placements
    # Logic: Raspberry Pi 5 & 12V Power Distribution
    add_rect(1100, 1200, 200, 80, "COMPONENTS")
    add_text(1110, 1235, "PI 5 + POWER CONTROLLER", 12, "LABELS")

    # Dual 120mm Exhaust Fans (Top Rear Chimney)
    add_rect(1340, 1470, 90, 150, "COMPONENTS")
    add_text(1310, 1635, "EXHAUST CHIMNEY", 12, "LABELS")

    # Canon LiDE Scanner (Z = 740 to 810)
    add_rect(880, 740, 480, 70, "COMPONENTS")
    add_text(980, 770, "CANON LiDE SCANNER (Z=740)", 13, "LABELS")

    # Brother Laser Printer (Z = 510 to 720)
    add_rect(880, 510, 500, 210, "COMPONENTS")
    add_text(940, 600, "BROTHER HL-L2321D LASER PRINTER", 14, "LABELS")

    # Paper Stock Reservoir (Z = 240 to 480)
    add_rect(880, 240, 320, 220, "COMPONENTS")
    add_text(900, 340, "1500 SHEETS A4 STORAGE", 13, "LABELS")

    # Paper Waste Shredder / Drop Bin
    add_rect(1220, 240, 190, 220, "COMPONENTS")
    add_text(1230, 330, "WASTE BIN", 12, "LABELS")

    # 600VA-1000VA Heavy UPS (Z = 40 to 220)
    add_rect(880, 40, 250, 180, "COMPONENTS")
    add_text(910, 120, "600VA ONLINE UPS", 13, "LABELS")

    # AC Inlet + MCB Breaker + Modbus Energy Meter
    add_rect(1200, 40, 210, 120, "COMPONENTS")
    add_text(1210, 90, "AC MCB & METER", 12, "LABELS")

    # Side Dimensions
    add_line(850, -60, 1450, -60, "DIMENSIONS")
    add_line(850, -75, 850, -45, "DIMENSIONS")
    add_line(1450, -75, 1450, -45, "DIMENSIONS")
    add_text(1080, -100, "DEPTH = 600 mm", 20, "DIMENSIONS")

    # ==========================================
    # 3. TOP PLAN VIEW (X: 0 to 600, Y: -800 to -200)
    # ==========================================
    add_text(120, -150, "3. TOP PLAN VIEW (Roof & Airflow Layout)", 28, "LABELS")
    add_rect(0, -800, 600, 600, "OUTLINE")
    # Dual 120mm Exhaust Fan cutouts
    add_rect(80, -400, 160, 160, "COMPONENTS")
    add_text(95, -330, "FAN 1 (120mm)", 14, "LABELS")
    add_rect(360, -400, 160, 160, "COMPONENTS")
    add_text(375, -330, "FAN 2 (120mm)", 14, "LABELS")
    # External IEC Power socket & Antenna port
    add_rect(240, -785, 120, 35, "DOORS_LOCKS")
    add_text(250, -765, "IEC AC INLET", 11, "LABELS")

    # Close DXF Structure
    dxf_lines.extend(["0", "ENDSEC", "0", "EOF"])

    output_path = os.path.join(os.getcwd(), "kiosk_cad_blueprint.dxf")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(dxf_lines))
    print(f"AutoCAD DXF generated successfully at: {output_path}")

if __name__ == "__main__":
    create_kiosk_dxf()
