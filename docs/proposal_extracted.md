Project Proposal: Xerox Kiosk
A 24/7 Smart Self-Service Printing Kiosk

1. Executive Summary & Market Opportunity

KL University’s Vaddeswaram/Vijayawada campus houses over 15,000+ students and faculty. Currently, this massive population relies on a single campus photocopy shop to print hall tickets, lab records, and assignments. This setup presents critical pain points:

Restricted Hours: The shop is open only from 9:20 AM to 5:30 PM (overlapping with class hours). Hostelers and late-night studiers have no access to printing.

Monopoly Pricing: Printouts are charged at high rates (up to ₹3 to ₹5 per page).

Poor User Experience: Students routinely wait in lines for 20-30 minutes, sharing private files via WhatsApp or email with a clerk.

The Bittu Xerox Kiosk is an autonomous, self-contained, 24/7 self-service machine that scans, copies (Xerox), and prints documents instantly via UPI payment.

Figure 1: Fully assembled Bittu Xerox Kiosk in KLU Forest Green.

2. User Flow & 'Zero-Clerk Privacy' Persona Story

To understand the impact of the kiosk, we compare the student experience of printing sensitive documents (e.g., Aadhaar cards, resumes, internship letters, academic grades) under the old model versus our self-service model.

• Goal: Print an internship offer letter and an Aadhaar card copy for submission.
• Pain Point: The document contains sensitive personal details (phone, address, photo, signature).

The Old Way (High Risk & High Friction)

1. WhatsApp/Email Share: The clerk tells the student to send the files to their personal phone WhatsApp or email them to a generic address.

2. Public Cache: The clerk downloads the files onto a shared public desktop, exposing them to the downloads folder.

3. Privacy Risk: Personal files remain stored on the public PC long after printout, visible to other students.

The Bittu Xerox Way (Zero-Clerk Privacy)

1. Secure Connection: Student scans the on-screen QR with their phone to connect to the local Pi 5.

2. Direct Upload: Files are sent directly to the local memory over encrypted HTTPS. No WhatsApp, no public emails.

3. Easy Verification: Student verifies the pages on the 14-inch touchscreen interface.

4. Quick UPI Pay: Student scans the dynamic UPI QR code on the display to make the transaction.

5. Secure Disposal: Kiosk prints the page and instantly runs a secure file deletion command, wiping the document.(It never stores) 

Key Security & Marketing Buzzwords

Zero-Clerk Privacy: Complete confidentiality. No human eyes or hands touch your documents. Resumes and Aadhaar numbers remain 100% private.

Encrypted Sandbox Link: SSL-secured web page gateway (upload.bittuxerox.in) routes files directly to volatile memory.

Instant Endpoint Data Wiping: FastAPI backend automatically executes file shredding commands upon printing completion.

3. Technical Cabinet Architecture & Hardware

The kiosk enclosure is engineered for public university environments, ensuring physical security, efficient cooling, and easy maintenance.

Cabinet Envelope: Height: 1.65 m (5.5 ft), Width: 0.60 m (2 ft), Depth: 0.60 m (2 ft).

Structural Material: Constructed from 12mm MDF panels reinforced with pine-wood joint support cleats.

Ergonomic Sloped Shelf: Tilted at 38.66 degrees (Z = 800 mm to 1000 mm) to house user controls at natural height.

Service Access: Key-alike chrome cylinder cam locks secure both the front lower door (Z = 780 mm) and the rear access door.

Figure 2: Interior layout showing component placement, support cleats, and cabling.

Internal Compartments & Separation

Top Upper Section (Z = 1000 to 1350 mm): Houses the 14-inch Full HD display, USB speakers, and dual 120mm exhaust fans.

Middle Console Shelf (Z = 800 to 1000 mm): Integrates the 12-key metal numeric PIN pad, Start/Cancel buttons, and dual HC-SR501 PIR motion sensors.

Scanner Bay (Z = 760 mm): Houses the Canon LiDE flatbed scanner, aligned with a side service hatch for document placement.

Printer Compartment (Z = 510 mm): Holds the Brother HL-L2321D laser printer with 3D-printed corner locator brackets for slot alignment.

Lower Compartment (Z = 24 to 510 mm): Left side houses the waste bin. Right side houses the 600VA UPS, AC energy meter, and paper storage shelf (Z = 250 mm) holding 1,000 backup sheets.

Figure 3: Front and side profile of the cabinet with ventilation grilles and key cam locks.

4. Electrical & Wiring Layout

The electrical harness is split inside the cabinet to prevent interference and ensure safety:
• High-Voltage Mains Power (Right-Aligned): AC power comes through an external IEC C14 inlet at the bottom right. It goes directly to the 600VA UPS. The UPS feeds the surge-protected power strip, supplying AC power to the Brother Printer and the Raspberry Pi 5.
• Low-Voltage Data Cables (Left-Aligned): HDMI, USB data, and GPIO wires run along the left cleats.
• Thermal Management: Dual 120mm exhaust fans pull hot air out of the cabinet's top-rear ventilation grilles, powered directly by the Pi 5's 12V rail.

Figure 4: Side-by-side view showing the external shell (left) and internal structure (right).

5. Software Architecture & Flow

The system runs autonomously on Raspberry Pi OS (Linux), utilizing a split frontend/backend stack:
1. Frontend UI (Tailwind CSS + HTML5): Running locally in Chromium fullscreen kiosk mode. Shows steps to select services, choose B&W/Color/Duplex, preview documents, and displays the dynamic payment QR code.
2. Backend Engine (FastAPI + Python): Directs the order state machine.
3. Scan-to-Copy Workflow: SANE library pulls image data from Canon flatbed scanner. Python image processing converts the raw scan to a high-contrast B&W document. CUPS print server outputs the document directly via the Brother printer.
4. Modbus Energy Logging: Measures total kWh consumption and operating costs in real time.

Figure 5: Interior focus on the Raspberry Pi 5, active cooler, and USB hubs.

6. Business Model & Unit Economics

Kiosk CAPEX Setup Cost

Unit Economics (Per B&W Page)

ROI & Payback Scenarios (25 Active Days/Month)

Conservative (200 pages/day): Daily profit: ₹260. Monthly profit: ₹6,500. Payback: ~7.7 months (230 Days).

Realistic (450 pages/day): Daily profit: ₹585. Monthly profit: ₹14,625. Payback: ~3.4 months (102 Days).

High-Volume Exam Season (900 pages/day): Daily profit: ₹1,170. Monthly profit: ₹29,250. Payback: ~1.7 months (51 Days).

7. Competitive Analysis vs. Commercial Franchises

Figure 6: Detail view of rear service access, exhaust fans, and security locks.

Category | Components | Cost
Electronics | Raspberry Pi 5, 14" Touchscreen, Speakers, Meter, Sensors | ₹12,100
Printing & Scan | Brother HL-L2321D Laser Printer & Canon Flatbed Scanner | ₹17,000
Power | 600VA UPS Battery Backup & Surge Extension Board | ₹3,700
Structure | Custom MDF Enclosure, Acrylic panels, Locks, Cleats, Screws | ₹5,100
Cables & Cooling | Cable Harness, Dual 120mm Fans, USB Hub | ₹1,600
Labor & Buffer | CNC cutting labor, paint finish, transportation | ₹6,500
Initial Stock Float | Starting paper reams (5) + compatible toner cartridges (2) | ₹4,000
Total CAPEX Setup | One-time build cost per kiosk | ₹50,000
Expense Item | Details / Assumptions | Cost / Page
A4 Paper | Ream of 500 sheets at ₹250 | ₹0.50
Toner Ink | Compatible cartridge at ₹600 for 2,600 pages | ₹0.23
Electricity | 500W printing, 5W idle. KLU tariff category | ₹0.02
Maintenance Buffer | Wear-and-tear, drum replacement, system upgrades | ₹0.25
KLU Royalty Share | 10% royalty/rent share back to University | ₹0.20
Total Cost / Page | Total cost to produce 1 printout | ₹1.20
Selling Price | Rate charged to student | ₹2.50
Net Profit / Page | Net margin per printed page (52% margin) | ₹1.30
Feature | Qwikprint MINI | Qwikprint PRO | Bittu Xerox Kiosk
Price (CAPEX) | ₹1.65 Lakh (₹1.4L + GST) | ₹3.49 Lakh (₹2.96L + GST) | ₹50,000 (All inclusive)
Revenue Cut | Requires royalty share | Requires royalty share | 100% profit retained
Interface Display | Standard small screen | Standard small screen | 14-inch Full HD Display
Paper Capacity | 750 sheets | 1,950 sheets | 1,250 sheets total
Xerox Option | Standard flatbed | Heavy-duty scanner | Canon LiDE Flatbed Scanner
Software System | Locked proprietary OS | Locked proprietary OS | Open Python Code (No fees)
