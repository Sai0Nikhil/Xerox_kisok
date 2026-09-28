# 🛠️ Bittu Xerox Kiosk — Developer Guide

> **Share this with your building team.** Everything they need to start coding.

---

## Quick Context (30-second read)

We're building an **autonomous 24/7 self-service printing kiosk** for university hostels. Students send documents via **Telegram bot** or **QR code upload**, pay via **UPI**, enter a **4-digit PIN** at the kiosk, and collect printed pages. No clerk. No queue.

**Tech stack:** Python 3.11 + FastAPI + SQLite + CUPS + python-telegram-bot + Chromium PWA  
**Hardware:** Raspberry Pi 5 + Brother HL-L2321D printer + 15.6" touchscreen  
**Target:** Pi runs Linux. Develop on any OS, deploy on Pi.

---

## Project Structure

```
c:\zerox_kisok\
├── software/
│   ├── backend/                    # 🔧 FastAPI Backend (Module 1)
│   │   ├── main.py                 # App entry point + CORS + lifespan
│   │   ├── config.py               # Settings (env vars, paths)
│   │   ├── models.py               # Pydantic models (Job, Payment)
│   │   ├── database.py             # SQLite connection + helpers
│   │   ├── schema.sql              # Table definitions
│   │   ├── routes/
│   │   │   ├── jobs.py             # POST /jobs, GET /jobs/{otp}
│   │   │   ├── payments.py         # POST /payments/webhook
│   │   │   ├── kiosk.py            # POST /kiosk/verify-otp
│   │   │   ├── upload.py           # POST /upload (QR web upload)
│   │   │   └── admin.py            # GET /admin/dashboard
│   │   ├── services/
│   │   │   ├── printer.py          # CUPS integration + Express Lane
│   │   │   ├── converter.py        # .docx/.pptx → PDF (LibreOffice)
│   │   │   ├── payment_service.py  # UPI QR generation + verification
│   │   │   ├── otp_service.py      # 4-digit OTP gen + validation
│   │   │   ├── stamper.py          # University logo watermark
│   │   │   └── file_validator.py   # File type/size validation
│   │   └── requirements.txt
│   │
│   ├── bot/                        # 🤖 Telegram Bot (Module 2)
│   │   ├── bot.py                  # Entry point
│   │   ├── handlers/
│   │   │   ├── start.py            # /start command
│   │   │   ├── upload.py           # File upload handler
│   │   │   ├── configure.py        # Print options inline keyboard
│   │   │   ├── payment.py          # Payment flow in chat
│   │   │   └── status.py           # Job status check
│   │   ├── keyboards.py            # Inline keyboard builders
│   │   ├── api_client.py           # Talks to FastAPI backend
│   │   └── requirements.txt
│   │
│   ├── kiosk-ui/                   # 🖥️ Kiosk Touchscreen UI (Module 3)
│   │   ├── index.html              # Main page
│   │   ├── css/
│   │   │   └── styles.css          # Dark theme, touch-friendly
│   │   ├── js/
│   │   │   ├── app.js              # Main logic
│   │   │   ├── otp.js              # OTP entry numpad
│   │   │   ├── status.js           # Job status + queue position
│   │   │   ├── qr.js               # QR code display for uploads
│   │   │   └── payment.js          # UPI QR display for payment
│   │   └── assets/
│   │       └── logo.png
│   │
│   ├── power/                      # 🔋 Power Manager (Module 4)
│   │   ├── power_manager.py        # PIR-driven 3-tier sleep daemon
│   │   └── requirements.txt
│   │
│   └── scripts/                    # 📜 DevOps Scripts
│       ├── setup-dev.sh            # Dev environment setup
│       ├── setup-bittu-os.sh       # Pi OS hardening
│       ├── run-all.sh              # Start all services locally
│       └── deploy.sh               # Deploy to Pi
│
├── cad/                            # 3D models (OpenSCAD)
├── docs/                           # All documentation
├── procurement/                    # BOM Excel
└── assets/                         # Reference images
```

---

## Database Schema

```sql
-- schema.sql

CREATE TABLE IF NOT EXISTS jobs (
    id          TEXT PRIMARY KEY,        -- UUID
    otp         TEXT UNIQUE NOT NULL,    -- 4-digit PIN
    status      TEXT NOT NULL DEFAULT 'uploaded',
                -- uploaded → configured → payment_pending 
                -- → paid → queued → printing → done → expired
    
    -- File info
    original_filename   TEXT,
    file_type          TEXT,             -- pdf, docx, pptx, jpg
    converted_path     TEXT,             -- path to converted PDF in tmpfs
    total_pages        INTEGER DEFAULT 0,
    
    -- Print settings
    copies         INTEGER DEFAULT 1,
    duplex         BOOLEAN DEFAULT 0,
    logo_stamp     BOOLEAN DEFAULT 0,
    page_range     TEXT,                 -- e.g., "1-5,8,10-12" or NULL=all
    
    -- Pricing
    price_per_page REAL DEFAULT 2.50,
    total_price    REAL DEFAULT 0.0,
    
    -- Payment
    payment_id     TEXT,                 -- Razorpay order_id
    payment_status TEXT DEFAULT 'pending', -- pending, captured, failed
    paid_at        TIMESTAMP,
    
    -- Source
    source         TEXT DEFAULT 'qr',    -- qr, telegram, erp
    telegram_chat_id  INTEGER,
    
    -- Timestamps
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at     TIMESTAMP,            -- 2 hours from creation
    printed_at     TIMESTAMP,
    
    -- Express lane
    is_express     BOOLEAN DEFAULT 0     -- true if total_pages <= 5
);

CREATE TABLE IF NOT EXISTS kiosk_stats (
    date           TEXT PRIMARY KEY,      -- YYYY-MM-DD
    pages_printed  INTEGER DEFAULT 0,
    revenue        REAL DEFAULT 0.0,
    jobs_completed INTEGER DEFAULT 0,
    paper_jams     INTEGER DEFAULT 0,
    avg_wait_secs  REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS energy_log (
    timestamp      TIMESTAMP PRIMARY KEY,
    voltage        REAL,
    current_amps   REAL,
    power_watts    REAL,
    energy_kwh     REAL
);

CREATE INDEX idx_jobs_otp ON jobs(otp);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created ON jobs(created_at);
```

---

## API Endpoints (Contracts)

### Backend API (FastAPI — port 8000)

```
POST /api/upload
  Body: multipart/form-data { file, source: "qr"|"telegram" }
  Response: { job_id, otp, pages, file_type }
  Notes: Validates file, converts to PDF if needed, stores in tmpfs

POST /api/jobs/{job_id}/configure
  Body: { copies, duplex, logo_stamp, page_range }
  Response: { job_id, total_pages, total_price }

POST /api/jobs/{job_id}/pay
  Response: { upi_qr_url, razorpay_order_id, amount }

POST /api/payments/webhook
  Body: Razorpay webhook payload
  Response: 200 OK
  Notes: Verifies signature, updates job status to "paid"

POST /api/kiosk/verify-otp
  Body: { otp: "7429" }
  Response: { job_id, filename, pages, status } or 404
  Notes: Rate-limited to 3 attempts/minute

POST /api/kiosk/print/{job_id}
  Response: { status: "queued", position: 3 }
  Notes: Adds to Express/Bulk queue based on page count

GET /api/kiosk/queue-status
  Response: { current_job, queue_length, estimated_wait_secs }

GET /api/admin/dashboard
  Response: { today_pages, today_revenue, active_jobs, toner_level, paper_est }

GET /api/health
  Response: { status: "ok", version: "1.0.0", uptime_secs, cpu_temp }
```

### Telegram Bot Commands

```
/start          → Welcome message + instructions
Send a file     → Triggers upload → config keyboard → payment → OTP
/status {otp}   → Check job status
/help           → Usage guide
/cancel         → Cancel current operation
```

---

## Module Ownership & Task Board

### 👤 Person A — Backend Core
**Skills needed:** Python, FastAPI, SQLite  
**Estimated:** 40-50 hours

| Task | Priority | Hours | Description |
|------|----------|-------|-------------|
| Project setup + FastAPI skeleton | P0 | 2 | `main.py`, config, CORS, lifespan |
| Database setup + schema | P0 | 2 | SQLite connection, create tables |
| File upload endpoint | P0 | 4 | Accept file, validate, store in tmpfs |
| File conversion service | P0 | 6 | LibreOffice headless: .docx/.pptx/.jpg → PDF |
| OTP service | P0 | 2 | Generate unique 4-digit PIN, TTL, rate-limit |
| Job configuration endpoint | P1 | 3 | Accept print settings, calculate price |
| Payment integration | P1 | 8 | UPI QR generation + Razorpay webhook + polling |
| OTP verification endpoint | P0 | 2 | Verify PIN, return job, rate-limit |
| Admin dashboard API | P2 | 4 | Stats aggregation queries |
| Logo stamp service | P2 | 4 | PyPDF2 overlay university watermark |
| File validator | P1 | 3 | Type check, size limit, page count |
| Job expiry cleanup | P1 | 2 | Background task: expire jobs after 2 hours |

---

### 👤 Person B — Telegram Bot
**Skills needed:** Python, python-telegram-bot library  
**Estimated:** 25-30 hours

| Task | Priority | Hours | Description |
|------|----------|-------|-------------|
| Bot setup + /start handler | P0 | 2 | @BotFather, token, basic bot |
| File upload handler | P0 | 4 | Receive doc/PDF/image, send to backend API |
| Print config keyboard | P0 | 5 | Inline keyboard: copies, duplex, logo, pages |
| Payment flow | P1 | 5 | Show price → send UPI link → wait for confirmation |
| OTP delivery | P0 | 1 | Send 4-digit PIN after payment |
| Status check handler | P1 | 2 | /status command |
| Error handling | P1 | 3 | File too large, unsupported format, payment failed |
| Conversation state machine | P1 | 4 | ConversationHandler for multi-step flow |
| API client module | P0 | 2 | HTTP client for talking to backend |

---

### 👤 Person C — Kiosk UI (Frontend)
**Skills needed:** HTML, CSS, JavaScript (no frameworks needed)  
**Estimated:** 25-30 hours

| Task | Priority | Hours | Description |
|------|----------|-------|-------------|
| Welcome/idle screen | P0 | 3 | Dark theme, animated Bittu branding, "Tap to start" |
| QR code display | P0 | 3 | Generate QR linking to upload page, refresh periodically |
| OTP entry numpad | P0 | 5 | Big touch-friendly 0-9 numpad, 4 digit fields |
| Job confirmation screen | P0 | 3 | Show filename, pages, price, "Print" button |
| UPI payment QR screen | P1 | 3 | Display Razorpay QR, "Waiting for payment..." |
| Printing status screen | P0 | 3 | Progress bar, "Printing page 5 of 12...", Express Lane notice |
| Queue position display | P1 | 2 | "You are #3. Est. wait: 24 sec" |
| Done / collect screen | P0 | 1 | "Collect your pages! Returning to home in 10s..." |
| Error screens | P1 | 2 | Paper jam, payment failed, file error |
| Touch-friendly CSS | P0 | 3 | Big buttons (min 48px), high contrast, no hover states |
| Web upload page | P1 | 4 | Mobile page for QR upload (file picker + submit) |

---

### 👤 Person D (or shared) — Printer + Hardware Integration
**Skills needed:** Python, Linux, CUPS, GPIO  
**Estimated:** 20-25 hours

| Task | Priority | Hours | Description |
|------|----------|-------|-------------|
| CUPS setup + test print | P0 | 3 | Install driver, configure printer, test from Python |
| Print service (pycups) | P0 | 5 | Send PDF to CUPS, monitor job status, handle errors |
| Express Lane scheduler | P1 | 8 | Chunk splitting, express queue, preemption logic |
| PIR power manager | P2 | 4 | GPIO interrupt, 3-tier sleep, display on/off |
| Paper jam detection | P2 | 2 | Monitor CUPS job status for errors, send alert |
| Heartbeat reporter | P2 | 2 | POST status every 5 min to central server |

---

## How to Split the Work

### If 2 people:
```
You:       Backend + Printer (Person A + D)
Friend:    Telegram Bot + Kiosk UI (Person B + C)
```

### If 3 people:
```
Person 1:  Backend core (Person A)
Person 2:  Telegram Bot (Person B)
Person 3:  Kiosk UI + Printer integration (Person C + D)
```

### If 4 people: 
```
One person per module. Ship in 2-3 weeks.
```

---

## Dev Setup (5 minutes)

```bash
# 1. Clone the repo
git clone <repo_url>
cd zerox_kisok/software

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate          # Linux/Mac
# or: venv\Scripts\activate       # Windows

# 3. Install backend deps
pip install -r backend/requirements.txt

# 4. Install bot deps
pip install -r bot/requirements.txt

# 5. Create .env file
cp .env.example .env
# Edit: TELEGRAM_BOT_TOKEN, RAZORPAY_KEY, etc.

# 6. Initialize database
python -c "import backend.database; backend.database.init()"

# 7. Run backend
uvicorn backend.main:app --reload --port 8000

# 8. Run bot (separate terminal)
python -m bot.bot

# 9. Open kiosk UI
# Open browser: http://localhost:8000
```

### Required dependencies
```
# backend/requirements.txt
fastapi==0.115.0
uvicorn[standard]==0.30.0
python-multipart==0.0.9
aiofiles==24.1.0
pydantic==2.9.0
PyPDF2==3.0.1
reportlab==4.2.0
Pillow==10.4.0
qrcode[pil]==7.4
httpx==0.27.0
jinja2==3.1.4

# bot/requirements.txt
python-telegram-bot==21.5
httpx==0.27.0

# Only on Pi (not needed for dev):
# pycups
# RPi.GPIO
```

---

## Communication Contracts Between Modules

```
┌───────────┐     HTTP/REST      ┌───────────┐
│ Telegram  │ ──────────────────►│  FastAPI   │
│ Bot       │ POST /api/upload   │  Backend   │
│ (bot.py)  │ POST /api/jobs/... │ (main.py)  │
└───────────┘                    └─────┬──────┘
                                       │
┌───────────┐     HTTP/REST            │ Python import
│ Kiosk UI  │ ──────────────────►      │
│ (browser) │ POST /api/kiosk/...      ▼
└───────────┘                    ┌───────────┐
                                 │  Printer   │
                                 │  Service   │
                                 │ (CUPS)     │
                                 └───────────┘
```

**Rule:** Bot and UI NEVER talk to each other. Both talk to Backend only. Backend talks to Printer service internally.

---

## First Sprint Goal (Week 1)

> A person can upload a PDF via a web form on the kiosk screen, see the page count + price, and get a fake "Printed!" confirmation.

No Telegram. No payment. No real printer. Just the **happy path** through the backend → UI → fake print. This proves the architecture works, then we plug in real modules one by one.
