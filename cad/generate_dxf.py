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
        "70", "8",
        # Layer 0
        "0", "LAYER", "2", "0", "70", "0", "62", "7", "6", "CONTINUOUS",
        # Layer 0_MDF_STRUCTURE (Green)
        "0", "LAYER", "2", "0_MDF_STRUCTURE", "70", "0", "62", "3", "6", "CONTINUOUS",
        # Layer 0_BOM_HARDWARE (Cyan)
        "0", "LAYER", "2", "0_BOM_HARDWARE", "70", "0", "62", "4", "6", "CONTINUOUS",
        # Layer 0_ELECTRICAL (Red)
        "0", "LAYER", "2", "0_ELECTRICAL", "70", "0", "62", "1", "6", "CONTINUOUS",
        # Layer 0_3D_PRINTED_PARTS (Magenta)
        "0", "LAYER", "2", "0_3D_PRINTED_PARTS", "70", "0", "62", "6", "6", "CONTINUOUS",
        # Layer 0_ACRYLIC_FASCIA (Blue)
        "0", "LAYER", "2", "0_ACRYLIC_FASCIA", "70", "0", "62", "5", "6", "CONTINUOUS",
        # Layer 0_DIMENSIONS (Yellow)
        "0", "LAYER", "2", "0_DIMENSIONS", "70", "0", "62", "2", "6", "CONTINUOUS",
        # Layer 0_BOM_TAGS (White)
        "0", "LAYER", "2", "0_BOM_TAGS", "70", "0", "62", "7", "6", "CONTINUOUS",
        "0", "ENDTAB",
        "0", "ENDSEC",
        "0", "SECTION",
        "2", "ENTITIES"
    ]

    def add_line(x1, y1, x2, y2, layer="0_MDF_STRUCTURE"):
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

    def add_rect(x, y, w, h, layer="0_MDF_STRUCTURE"):
        add_line(x, y, x + w, y, layer)
        add_line(x + w, y, x + w, y + h, layer)
        add_line(x + w, y + h, x, y + h, layer)
        add_line(x, y + h, x, y, layer)

    def add_text(x, y, text, height=18.0, layer="0_BOM_TAGS"):
        dxf_lines.extend([
            "0", "TEXT",
            "8", layer,
            "10", f"{float(x):.2f}",
            "20", f"{float(y):.2f}",
            "30", "0.00",
            "40", f"{float(height):.2f}",
            "1", str(text)
        ])

    # 1. FRONT ELEVATION VIEW (X: 0 to 600, Y: 0 to 1650)
    add_text(100, 1720, "1. FRONT ELEVATION VIEW (Scale 1:1 mm)", 26, "0_BOM_TAGS")
    add_rect(0, 0, 600, 1650, "0_MDF_STRUCTURE")

    # Clean Solid Top Marquee Canopy (Z = 1350 to 1650) - NO FRONT MESH!
    add_rect(12, 1350, 576, 300, "0_MDF_STRUCTURE")
    add_rect(40, 1450, 520, 170, "0_ACRYLIC_FASCIA")
    add_text(150, 1550, "BITTU XEROX 24/7", 26, "0_BOM_TAGS")
    add_text(170, 1490, "SMART CAMPUS PRINTING HUB", 14, "0_BOM_TAGS")

    # BIG 15.6" FULL HD TOUCHSCREEN (Z = 1040 to 1300, 420mm W x 260mm H)
    add_rect(90, 1040, 420, 260, "0_BOM_HARDWARE")
    add_rect(85, 1035, 430, 270, "0_3D_PRINTED_PARTS")
    add_text(130, 1160, "BIG 15.6\" FHD TOUCHSCREEN DISPLAY", 16, "0_BOM_TAGS")

    # Sloped Smartphone Staging Dock (Z = 830 to 1020)
    add_rect(20, 830, 560, 190, "0_MDF_STRUCTURE")
    add_rect(140, 850, 320, 150, "0_ACRYLIC_FASCIA")
    add_text(170, 920, "SMARTPHONE STAGING DOCK (UPI / QR)", 12, "0_BOM_TAGS")

    # Canon LiDE 300 Scanner Bay (Z = 760 to 830)
    add_rect(60, 760, 480, 50, "0_BOM_HARDWARE")
    add_text(180, 780, "CANON LiDE 300 SCANNER", 14, "0_BOM_TAGS")

    # Document Output Retrieval Chute (Z = 530 to 600)
    add_rect(70, 530, 460, 65, "0_ACRYLIC_FASCIA")
    add_text(160, 560, "PRINT RETRIEVAL CHUTE (A4 DUPLEX)", 14, "0_BOM_TAGS")

    # Brother HL-L2321D Laser Printer (Z = 510 to 740)
    add_rect(50, 520, 500, 210, "0_BOM_HARDWARE")
    add_text(140, 640, "BROTHER HL-L2321D LASER PRINTER", 14, "0_BOM_TAGS")

    # Paper Reserve Shelf (Z = 250 to 420)
    add_rect(50, 260, 260, 145, "0_BOM_HARDWARE")
    add_text(65, 330, "1,500 SHEETS A4 PAPER RESERVE", 12, "0_BOM_TAGS")

    # Waste / Recycle Bin (Right)
    add_rect(350, 36, 180, 444, "0_BOM_HARDWARE")
    add_text(370, 240, "COLLECTION BIN", 12, "0_BOM_TAGS")

    # 600VA UPS Battery (Z = 36 to 216)
    add_rect(50, 36, 160, 180, "0_ELECTRICAL")
    add_text(60, 120, "600VA UPS POWER", 12, "0_BOM_TAGS")

    # Dimensions
    add_line(-60, 0, -60, 1650, "0_DIMENSIONS")
    add_line(-75, 0, -45, 0, "0_DIMENSIONS")
    add_line(-75, 1650, -45, 1650, "0_DIMENSIONS")
    add_text(-220, 800, "TOTAL H = 1650 mm", 20, "0_DIMENSIONS")

    add_line(0, -60, 600, -60, "0_DIMENSIONS")
    add_line(0, -75, 0, -45, "0_DIMENSIONS")
    add_line(600, -75, 600, -45, "0_DIMENSIONS")
    add_text(220, -100, "WIDTH = 600 mm", 20, "0_DIMENSIONS")

    # 2. SIDE SECTION VIEW (X: 850 to 1450, Y: 0 to 1650)
    add_text(950, 1720, "2. SIDE SECTION VIEW (Depth: 600 mm)", 26, "0_BOM_TAGS")
    add_line(850, 0, 1450, 0, "0_MDF_STRUCTURE")
    add_line(1450, 0, 1450, 1650, "0_MDF_STRUCTURE")
    add_line(1450, 1650, 850, 1650, "0_MDF_STRUCTURE")
    add_line(850, 1650, 850, 1180, "0_MDF_STRUCTURE")
    add_line(850, 1180, 790, 880, "0_MDF_STRUCTURE")
    add_line(790, 880, 850, 820, "0_MDF_STRUCTURE")
    add_line(850, 820, 850, 0, "0_MDF_STRUCTURE")

    # Rear Exhaust Chimney Vents in Side View
    add_rect(1430, 1420, 15, 180, "0_BOM_HARDWARE")
    add_text(1280, 1520, "REAR EXHAUST VENTS", 11, "0_BOM_TAGS")

    # Close DXF
    dxf_lines.extend(["0", "ENDSEC", "0", "EOF"])

    output_path = os.path.join(os.getcwd(), "kiosk_cad_blueprint.dxf")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(dxf_lines))
    print("AutoCAD DXF updated with 15.6 inch screen and rear vents!")

if __name__ == "__main__":
    create_kiosk_dxf()
