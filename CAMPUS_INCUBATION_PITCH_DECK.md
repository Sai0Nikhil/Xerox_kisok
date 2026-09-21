# Pitch Deck & Incubation Proposal: Bittu Xerox Kiosk
**Autonomous 24/7 Smart Self-Service Printing & Document Kiosk for Universities**

---

## Slide 1: Title & Executive Summary
- **Project Name**: Bittu Xerox Kiosk (Smart Campus Printing System)
- **Tagline**: *"Zero Queues. Zero Human Leakage. 24/7 Instant Printing for Hostels & Colleges."*
- **Presented by**: [Your Name / Team Name]
- **Target Location**: KL University Hostels, Academic Blocks & Library Corridors

---

## Slide 2: The Core Problem on Campus
1. **Restricted Shop Timings**: Campus photocopy shops operate strictly from 9:30 AM – 5:30 PM (matching lecture hours). Hostelers needing prints at 11 PM or 7 AM before an 8 AM lab evaluation have zero access.
2. **Extreme Privacy Risk (Data Leakage)**: Students share sensitive documents (Aadhaar cards, resumes, medical records, mark sheets) via WhatsApp/Email to the shop clerk's personal phone and shared public PC.
3. **Severe Peak-Hour Queues**: During exam weeks, assignment deadlines, and lab submissions, students waste 20–45 minutes standing in line.
4. **Monopoly & Irregular Pricing**: Students are often charged ₹3 to ₹5 per page without standard receipts.

---

## Slide 3: The Solution — Bittu Xerox Kiosk
An unattended, IoT-enabled, secure self-service printing, scanning, and copying kiosk built inside a rugged, compact 0.36 m² cabinet.

- **24/7 Accessibility**: Active in hostel lobbies day and night.
- **Zero-Clerk Privacy**: Direct encrypted HTTPS upload; files are processed in volatile RAM and shredded immediately after printing.
- **Instant UPI Payment**: Dynamic QR code on screen generated per order.
- **Affordable & Transparent**: ₹2.00 – ₹2.50 per page with real-time digital billing.

---

## Slide 4: High-Value Features & Innovations

### A. Document Upload & Print Workflow
1. **QR & Web Upload**: Scan the screen QR on mobile -> Upload PDF/DOCX/Images directly via browser without installing an app.
2. **WhatsApp Bot Integration**: Send document to a dedicated WhatsApp business number -> Get a 4-digit PIN -> Punch PIN on kiosk to print in 10 seconds.
3. **ERP / Hall Ticket Auto-Pull**: Integration with college ERP to print semester hall tickets or lab manuals with one-click student ID login.
4. **Canon LiDE Flatbed Scanner**: Instant photocopy / Aadhaar copy mode without needing a smartphone.

### B. Campus Smart Hardware Features
1. **Battery Backup (600VA–1000VA UPS)**: Uninterrupted printing even during campus power fluctuations or generator changeovers.
2. **Positive-Pressure Thermal Chimney**: Prevents printer overheating during heavy exam-time volume.
3. **PIR Wake Sensor & Corridors Night Mode**: Soft LED downlight wakes up automatically when a student approaches, remaining unobtrusive in hostel halls.
4. **Paper Out & Toner Telemetry**: IoT dashboard notifies kiosk admin via Telegram/WhatsApp when paper drops below 100 sheets.

---

## Slide 5: Market Opportunity & Unit Economics (KLU Context)

### Total Addressable Market (KL University)
- **Student & Faculty Strength**: 15,000+
- **Hostel Residents**: 6,000+
- **Average Prints per Student / Month**: 15–20 pages (Lab reports, assignments, hall tickets, resumes)
- **Campus Monthly Print Volume**: >2,00,000 pages

### Unit Economics per Page (Black & White)
| Cost Component | Cost per Page |
| :--- | :--- |
| Paper (75 GSM) | ₹0.50 |
| Toner Cartridge | ₹0.23 |
| Power Consumption (500W run / 5W idle) | ₹0.02 |
| Maintenance & Drum Replacement Buffer | ₹0.25 |
| University Royalty / Floor Electricity Share (10%) | ₹0.20 |
| **Total Production Cost** | **₹1.20** |
| **Selling Price to Student** | **₹2.50** |
| **Net Profit Margin per Page** | **₹1.30 (52% Margin)** |

### Financial Projections (Single Kiosk in Boys/Girls Hostel)
- **Conservative (250 pages/day)**: Monthly Net Profit = **₹8,125** | Payback: **~6.1 months**
- **Moderate (500 pages/day)**: Monthly Net Profit = **₹16,250** | Payback: **~3.1 months**
- **Exam Season (1,000 pages/day)**: Monthly Net Profit = **₹32,500** | Payback: **~1.5 months**
- **Initial Setup CAPEX**: **₹50,000** (Full hardware, chassis & initial stock)

---

## Slide 6: Competitive Advantage vs. Commercial Franchises
| Parameter | Commercial Franchise (e.g. Qwikprint) | Bittu Xerox Kiosk |
| :--- | :--- | :--- |
| **Initial Investment** | ₹1.65 Lakh – ₹3.50 Lakh | **₹50,000 (70% Lower)** |
| **Software Licensing** | Monthly proprietary fee + % revenue cut | **100% In-house Open Python/FastAPI (Zero fees)** |
| **Custom Campus Integration** | Not possible | **Full Student ERP & WhatsApp Bot Support** |
| **Maintenance & Spares** | Dependent on third-party vendor | **Standard off-the-shelf components (Brother & Canon)** |

---

## Slide 7: Safety, Privacy & Operational Reliability
1. **Zero Data Retention Policy**: Documents never touch persistent storage; memory is wiped automatically upon print termination.
2. **Anti-Paper Jam Protection**: Optimized short-path gravity output chute with smooth Teflon guides.
3. **Physical Security**: Dual cam locks, internal steel anchors to floor, tamper-detection accelerometer.

---

## Slide 8: The Ask from Incubation Cell / HOD
1. **Pilot Location Grant**: Permission to place 1 Pilot Unit in a primary hostel lobby (0.36 m² space + 1 standard 5A/16A socket).
2. **Incubation / Seed Grant**: ₹50,000 – ₹1,00,000 for building the production chassis and deployment of 2 pilot kiosks.
3. **Mentorship & Campus Integration**: Support for linking student authentication/ERP for seamless one-tap campus logins.
