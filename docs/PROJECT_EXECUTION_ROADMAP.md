# Master Execution Roadmap: Bittu Xerox Kiosk
**From Concept to 24/7 Campus Deployment**

---

## Phase 1: Presentation & Campus Approvals (Week 1)
**Goal**: Secure permission for a pilot location in a hostel lobby and apply for seed funding from the Incubation Cell / E-Cell.

### Key Actions:
1. **Prepare the Demo**:
   - Run the local server (`python -m uvicorn server:app --port 8000`) on your laptop.
   - Open the Kiosk UI (`/kiosk`) on fullscreen and the Admin Dashboard (`/admin`) on your phone/tablet.
2. **Schedule Meetings**:
   - **Meeting 1: Incubation / E-Cell Director**: Present [`CAMPUS_INCUBATION_PITCH_DECK.md`](file:///c:/zerox_kisok/CAMPUS_INCUBATION_PITCH_DECK.md) highlighting the 52% gross margin and ₹50k low-CAPEX model.
   - **Meeting 2: Chief Warden / Hostel Administrator**: Explain the 24/7 convenience for late-night student emergencies and zero need for extra personnel.
3. **Outcomes to Secure**:
   - Written permission for 0.36 m² floor space in 1 hostel lobby + 1 standard 5A/16A electrical socket.
   - Prototype seed grant (₹50,000) or self-funded pilot approval.

---

## Phase 2: AutoCAD Finalization & Cabinet Fabrication (Weeks 2–3)
**Goal**: Produce the physical enclosure with precise CNC cutting, internal shelving, and ventilation.

### Key Actions:
1. **Open & Review CAD Blueprint**:
   - Open [`kiosk_cad_blueprint.dxf`](file:///c:/zerox_kisok/kiosk_cad_blueprint.dxf) in AutoCAD.
   - Verify mounting hole cutouts for your specific 14" screen and Brother printer dimensions.
2. **Fabrication Method Selection**:
   - **Option A (Fast & Low Cost)**: 12mm CNC Marine Plywood / MDF + High-Pressure Laminate (HPL) finish. Total chassis cost: ~₹5,000–₹6,500.
   - **Option B (Industrial & Heavy Duty)**: 1.6mm–2.0mm CRCA Sheet Metal (Laser cut & CNC bent) + Powder coat. Total chassis cost: ~₹12,000–₹15,000.
3. **Send Cut-List to Workshop**:
   - Export 2D flat panel profiles from AutoCAD to the local laser/CNC cutting shop.
   - Apply powder coating / paint finish (KLU Forest Green `#1B4D3E` with gold branding vinyl).

---

## Phase 3: Hardware Procurement & Chassis Assembly (Week 3)
**Goal**: Assemble all electrical, computing, and printing hardware inside the cabinet.

### Bill of Materials (BOM) Checklist:
| Component | Recommended Model | Est. Cost (₹) |
| :--- | :--- | :--- |
| **Computing Unit** | Raspberry Pi 5 (4GB/8GB) or Intel N100 Mini PC | ₹6,500 – ₹9,000 |
| **Display** | 14-inch Full HD Capacitive Touchscreen (HDMI + USB) | ₹5,500 – ₹6,500 |
| **Printer** | Brother HL-L2321D Laser Printer (Auto-Duplex) | ₹12,500 |
| **Scanner** | Canon CanoScan LiDE 300 Flatbed Scanner | ₹4,500 |
| **Power Backup** | 600VA / 1000VA Line-Interactive UPS | ₹3,200 – ₹4,500 |
| **Cooling** | Dual 120mm PWM 12V High-CFM Ball-Bearing Fans | ₹800 |
| **Security & Misc** | Tubular Cam Locks (Key-alike), IEC AC inlet, Surge board | ₹1,500 |
| **Consumables Float**| 5 Reams 75 GSM A4 Paper + 2 High-Yield Toner Cartridges | ₹4,000 |
| **Total Build Cost** | | **~₹45,000 – ₹50,000** |

---

## Phase 4: Software Setup & Production Deployment (Week 4)
**Goal**: Configure the kiosk to run autonomously on boot without keyboard/mouse.

### Key Actions:
1. **Operating System Setup**:
   - Install Raspberry Pi OS / Ubuntu Linux.
   - Configure CUPS for Brother printer drivers (`sudo apt install cups`) and SANE for Canon flatbed scanner.
2. **Auto-Start Kiosk on Boot**:
   - Set up systemd service to start `server.py` on power-on.
   - Configure Chromium browser to launch in fullscreen kiosk mode:
     ```bash
     chromium-browser --kiosk --noerrdialogs --disable-infobars --check-for-update-interval=31536000 http://localhost:8000/kiosk
     ```
3. **Payment & WhatsApp Integration**:
   - Link your production Merchant UPI VPA / QR webhook or Razorpay automated payment gateway.
   - Connect the WhatsApp Business Cloud API / Twilio to auto-receive PDFs and return 4-digit PINs.

---

## Phase 5: Pilot Launch & Scaling (Month 2 onwards)
**Goal**: Launch 1 unit in Hostel Block 4, validate unit economics, and expand.

### Operational Routine:
1. **Daily Check via Phone (`/admin`)**:
   - Check paper level tray (refill every 400–500 pages).
   - Review daily revenue, uptime, and temperature gauges.
2. **Expansion Milestones**:
   - **Month 1**: 1 Pilot Kiosk (Break-even tracking).
   - **Month 3**: Deploy 3 additional kiosks in Girls Hostel, Main Academic Block, and Library Corridor.
