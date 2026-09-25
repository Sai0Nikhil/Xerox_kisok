# AutoCAD Design & Architectural Blueprint: 24/7 Smart Xerox Kiosk

## 1. Project Overview & Physical Envelope
The **Bittu Xerox Kiosk** is an autonomous 24/7 self-service document printing, scanning, and copying kiosk specifically designed for Indian university campuses and hostel common areas (such as KL University).

| Dimension | Metric (mm) | Imperial (ft / in) | Notes |
| :--- | :--- | :--- | :--- |
| **Total Height ($H$)** | **1,650 mm** | 5.41 ft (65.0 in) | Ergonomic eye-level visibility |
| **Total Width ($W$)** | **600 mm** | 1.97 ft (23.6 in) | Compact footprint, fits any hostel lobby corridor |
| **Total Depth ($D$)** | **600 mm** | 1.97 ft (23.6 in) | Front sloped console extends +50mm at interaction zone |
| **Footprint Area** | **0.36 m²** | ~3.88 sq ft | High revenue per sq.ft |
| **Chassis Material** | 1.6mm–2.0mm CRCA Sheet Metal / 12mm Marine Ply / MDF with HPL | Powder-coated KLU Forest Green (#1B4D3E) + Warm Gold Trim |

---

## 2. Vertical Stacking & Hardware Architecture ($Z$-Axis from 0 to 1650 mm)

```
 +---------------------------------------------------------+  Z = 1650 mm (Top Roof)
 |  BRAND HEADER / LED BACKLIT ACRYLIC CANOPY               |
 |  [ DUAL 120mm PWM EXHAUST FANS (Rear Chimney) ]         |  Z = 1480 - 1650 mm
 +---------------------------------------------------------+
 |  14-INCH FHD CAPACITIVE TOUCHSCREEN                     |  Z = 1200 - 1440 mm
 |  [ Wide-Angle Security Cam + PIR Motion Wake Sensor ]   |  (Center: 1320 mm - Eye Level)
 +---------------------------------------------------------+
 |  ERGONOMIC SLOPED USER CONSOLE (Tilted 38.7°)           |  Z = 850 - 1150 mm
 |  - Metal Vandal-Proof Keypad (Left)                     |
 |  - Start (Green) & Cancel (Red) Buttons                 |
 |  - Smartphone Staging Rest & Dynamic UPI QR Display     |
 +---------------------------------------------------------+
 |  CANON LiDE FLATBED SCANNER BAY (Spring-Assisted Lid)   |  Z = 730 - 840 mm
 +---------------------------------------------------------+
 |  FINISHED DOCUMENT RETRIEVAL TRAY (Sloped Chute + LED)  |  Z = 530 - 640 mm
 +---------------------------------------------------------+
 |  BROTHER HL-L2321D HEAVY-DUTY LASER PRINTER COMPARTMENT |  Z = 500 - 720 mm (Internal)
 +---------------------------------------------------------+
 |  BULK PAPER STORAGE SHELF (1,500 Sheets A4) + WASTE BIN |  Z = 230 - 480 mm
 +---------------------------------------------------------+
 |  BASE POWER & ELECTRICAL MANAGEMENT                     |  Z = 0 - 230 mm
 |  - 600VA - 1000VA Online UPS Battery Backup             |
 |  - AC MCB Breaker + Modbus Energy Meter + Surge Board   |
 |  - Dual Intake Cooling Louvers (Positive Pressure)      |
 +---------------------------------------------------------+  Z = 0 mm (Floor Anchor Plates)
```

---

## 3. Ergonomics & Campus / Hostel Specific Design Features

1. **Anti-Glare Viewing Hood & Angle**:
   - The 14" display is mounted at $Z = 1320\text{ mm}$ (center) with a subtle $8^\circ$ backward tilt and upper sun/light visor hood to eliminate glare from bright hostel corridor tube lights.
2. **Smartphone Resting Ledge**:
   - Students frequently handle documents, phones, and IDs simultaneously. A dedicated 15° angled non-slip silicone/acrylic phone rest next to the QR code reader allows hands-free scanning and UPI payment.
3. **24/7 Night Ambience & Accessibility**:
   - Soft downward-facing 4000K warm LED strip illuminates the document retrieval chute and scanner bed without disturbing sleeping hostelers in quiet corridors.
   - Status RGB Ring:
     - 🟢 **Solid Green**: Ready for instant print/scan.
     - 🟡 **Pulsing Amber**: Printing / Processing document.
     - 🔴 **Red**: Low paper / Hopper empty / Door open.
4. **Thermal Management in Indian Summers**:
   - Positive-pressure ventilation: Cool air enters through bottom filtered intake louvers ($Z = 100\text{ mm}$); hot air from the laser fuser ($>180^\circ\text{C}$) rises naturally through a rear vertical chimney and is extracted by dual 120mm ball-bearing fans at the top roof ($Z = 1550\text{ mm}$).
5. **Physical Security & Anti-Vandalism**:
   - Tubular cam key-alike locks on front and rear access doors.
   - Anti-tamper vibration/tilt sensor integrated into the Raspberry Pi GPIO to trigger alerts if tilted or forced.
   - Heavy UPS (12 kg) positioned at the bottom base ($Z=0-200\text{ mm}$) to lower center of gravity and prevent tipping.

---

## 4. AutoCAD Drafting & Layer Organization Standard

When working in AutoCAD, organize the geometry into the following layers:

| Layer Name | Color | Linetype | Description |
| :--- | :--- | :--- | :--- |
| `0_FRAME_OUTLINE` | Green (3) | Continuous (0.50 mm) | Outer enclosure profile, bent sheet metal edges |
| `0_INTERNAL_SHELVES`| Cyan (4) | Continuous (0.35 mm) | Internal MDF/steel partition shelves & brackets |
| `0_HARDWARE_PARTS` | Magenta (6)| Continuous (0.25 mm) | Printer, scanner, display, UPS, Pi 5, fan solid models |
| `0_DOORS_LOCKS` | Red (1) | Continuous (0.35 mm) | Hinged maintenance panels, cam locks, piano hinges |
| `0_AIRFLOW_VENTS` | Blue (5) | Continuous (0.18 mm) | Louvers, fan cutouts, chimney ducting |
| `0_DIMENSIONS` | Yellow (2)| Continuous (0.18 mm) | Linear, angular, and datum elevation dimensions |
| `0_ANNOTATIONS` | White (7) | Continuous (0.25 mm) | Component tags, callouts, and notes |

---

## 5. AutoCAD Ready Files Generated

1. **DXF Blueprint**: [`kiosk_cad_blueprint.dxf`](file:///c:/zerox_kisok/kiosk_cad_blueprint.dxf)
   - Contains 1:1 scale Front Elevation, Side Profile Elevation with section cutaways, and Top Plan View.
   - Import directly into AutoCAD using `OPEN` -> select `.dxf` or `DXFIN`.
2. **Parametric Script**: [`generate_dxf.py`](file:///c:/zerox_kisok/generate_dxf.py)
   - Python generator to programmatically modify any kiosk dimension or cut-out size.
