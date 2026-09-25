# SHEET: BITTU BOM

Category | Component | Exact Search / Model | Qty | Current Reference Price (₹) | Budget (₹) | Buy From | Local Vijayawada Target | Purchased? | Actual Price (₹) | Notes
Core Computer | Raspberry Pi | Raspberry Pi 5 2GB | 1 | 8000 | 8000 | Online / electronics dealer | Compare local vs online |  |  | Main controller
Core Computer | Active Cooler | Raspberry Pi 5 Active Cooler | 1 | 600 | 600 | Online / electronics dealer | Ask Pi retailer |  |  | Cooling
Core Computer | Power Supply | Raspberry Pi 27W USB-C PSU | 1 | 1300 | 1300 | Online / electronics dealer | Ask Pi retailer |  |  | Official/reliable PSU preferred
Core Computer | Storage | 64/128GB A2 MicroSD | 1 | 700 | 700 | Online / computer shop | ₹600–900 |  |  | 
UI | Touchscreen | 7-inch HDMI capacitive 1024×600 | 1 | 4300 | 4300 | Online / robotics shop | ₹4,000–4,500 |  |  | Generic HDMI preferred
Printing | Laser Printer | Brother HL-L2321D | 1 | 12199 | 12200 | Brother dealer / computer shop | ₹10,500–12,000 |  |  | Monochrome laser
Printing | Toner | Compatible / genuine Brother toner | 1 | 1500 | 1500 | Printer dealer | Quote with printer |  |  | Consumable
Scanning | Scanner | Canon LiDE 300 | 1 | 5000 | 5000 | Printer/computer dealer | ₹4,500–5,500 |  |  | Epson V39II is alternative
Presence | PIR Sensor | HC-SR501 | 2 | 75 | 150 | Electronics shop / online | ₹50–100 each |  |  | Wake/idle detection
Energy | Energy Meter | Single-phase RS485 Modbus DIN-rail energy meter | 1 | 2000 | 2000 | Electrical dealer / online | ₹1,500–2,500 |  |  | Mains installation by qualified electrician
Energy | RS485 Adapter | USB to RS485 adapter | 1 | 300 | 300 | Electronics shop / online | ₹200–500 |  |  | Pi ↔ energy meter
Connectivity | USB Hub | 4-port USB 2.0/3.0 hub | 1 | 400 | 400 | Computer shop / online | ₹300–500 |  |  | 
Controls | Push Buttons | 22mm illuminated push button | 2 | 200 | 400 | Electronics shop | ₹150–250 each |  |  | Green START, red CANCEL
Controls | Buzzer | 5V active buzzer module | 1 | 100 | 100 | Electronics shop | ₹50–100 |  |  | 
Audio | Speaker | Small USB speaker | 1 | 500 | 500 | Computer/mobile shop | ₹300–500 |  |  | Voice prompts
Power | UPS | 600VA UPS | 1 | 2700 | 2700 | UPS dealer | ₹2,500–3,000 |  |  | Back up Pi/touchscreen etc.; printer UPS strategy separate
Body | Main panels | 12mm MDF sheets | 1 | 1500 | 1500 | Local fabrication/material shop | ₹1,000–1,500 |  |  | Main enclosure
Body | Front panels | 3mm acrylic | 1 | 800 | 800 | Local acrylic/laser cutting shop | ₹500–800 |  |  | Front/bezel elements
Body | 3D printed parts | PLA/PETG filament + prints | 1 | 1000 | 1000 | KLU lab / local 3D printing | ₹500–1,000 |  |  | Brackets, bezel, mounts
Body | Fasteners | M3/M4 screws, nuts, standoffs | 1 | 800 | 800 | NTR Complex / hardware shop | ₹500–800 |  |  | 
Body | Hinges / brackets | Cabinet hinges + L brackets | 1 | 300 | 300 | Hardware shop | ₹200–400 |  |  | Service door
Body | Cable management | Cable ties, clips, heat-shrink | 1 | 300 | 300 | Electronics/hardware shop | ₹200–300 |  |  | 
Power | Extension board | AC extension/surge protection | 1 | 500 | 500 | Electrical shop | ₹400–700 |  |  | 
Consumables | A4 paper | 75/80 GSM, 500-sheet ream | 3 | 350 | 1050 | Stationery shop | ₹300–400/ream |  |  | Reserve paper shelf
Misc | Cables | USB A-B, HDMI, USB-C, Ethernet etc. | 1 | 1000 | 1000 | Computer shop | ₹800–1,200 |  |  | Allow spare cables
Safety | Electrical protection | Fuse/MCB/terminal hardware | 1 | 500 | 500 | Electrical dealer | ₹300–700 |  |  | Qualified electrician for mains
TOTAL |  |  |  |  | None |  |  |  |  | 


# SHEET: Vijayawada Buying Plan

Area / Dealer Type | Suggested Place / Dealer | What to Ask For | Notes
Governorpet / NTR Complex | Krishna Computer Peripherals | Pi accessories, cables, electronics | Compare local vs online
Governorpet / NTR Complex | Navkar Computers Accessories | Cables, small electronics, computer accessories | Price-check Pi accessories and cables
Mogalrajapuram / Governorpet | Baid Electronics | Brother printer + scanner quote | Ask for HL-L2321D cash/GST price
Governorpet / Labbipet | CK Computers / Computer shops | Printer, scanner, UPS, cables | Get bundle quote
Auto Nagar / Kanuru | Laser/CNC/MDF fabrication shops | MDF/acrylic cutting, enclosure panels | Use final CAD dimensions
Local electrical dealer | UPS / energy meter | 600VA UPS, RS485 Modbus DIN-rail meter | Qualified electrician for mains wiring


# SHEET: Software & Features

Module | Technology / Component | Purpose | Status / Dependency
Kiosk UI | React + TypeScript | Touchscreen interface | Build
Backend | Python + FastAPI | APIs, jobs, orchestration | Build
Database | SQLite | Users, jobs, payments, logs, energy | Build
Printing | CUPS | Linux print management | Build on Pi
Scanning | SANE | Scanner integration | Build on Pi
ERP Connector | HTTPS REST API | Hall tickets, letters, certificates etc. | Depends on authorized KLU API/access
OTP | SMS OTP provider | User authentication | Provider selection
Payments | UPI + payment gateway/webhook | Payment verification | Merchant/gateway setup
Energy | Modbus RTU over RS485 | Read V/A/W/kWh | Hardware + electrician
Idle/Wake | PIR + software state machine | Dim/sleep when idle | Build
Admin Dashboard | React + FastAPI | Device health, jobs, revenue, energy | Build
CAD | OpenSCAD | Parametric kiosk body | Finalize after hardware dimensions


