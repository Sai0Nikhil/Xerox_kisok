-- Bittu Xerox Kiosk — Database Schema
-- SQLite3

CREATE TABLE IF NOT EXISTS jobs (
    id                  TEXT PRIMARY KEY,
    otp                 TEXT UNIQUE NOT NULL,
    status              TEXT NOT NULL DEFAULT 'uploaded',
    -- Status flow: uploaded → configured → payment_pending
    --              → paid → queued → printing → done
    --              → expired (auto, after 2 hours)

    -- File info
    original_filename   TEXT,
    file_type           TEXT,               -- pdf, docx, pptx, jpg, png
    converted_path      TEXT,               -- path in tmpfs after conversion
    total_pages         INTEGER DEFAULT 0,
    file_size_bytes     INTEGER DEFAULT 0,

    -- Print settings
    copies              INTEGER DEFAULT 1,
    duplex              INTEGER DEFAULT 0,  -- 0=single, 1=duplex
    logo_stamp          INTEGER DEFAULT 0,  -- 0=no, 1=yes (+₹1/page)
    page_range          TEXT,               -- "1-5,8,10-12" or NULL=all

    -- Pricing
    price_per_page      REAL DEFAULT 2.50,
    total_price         REAL DEFAULT 0.0,

    -- Payment
    payment_id          TEXT,               -- Razorpay order_id or UPI ref
    payment_method      TEXT DEFAULT 'upi', -- upi, razorpay
    payment_status      TEXT DEFAULT 'pending',
    paid_at             TEXT,               -- ISO 8601 timestamp

    -- Source
    source              TEXT DEFAULT 'qr',  -- qr, telegram, erp
    telegram_chat_id    INTEGER,
    telegram_message_id INTEGER,

    -- Express lane
    is_express          INTEGER DEFAULT 0,  -- 1 if total_pages <= 5

    -- Timestamps
    created_at          TEXT DEFAULT (datetime('now')),
    configured_at       TEXT,
    queued_at           TEXT,
    printing_started_at TEXT,
    printed_at          TEXT,
    expires_at          TEXT                 -- created_at + 2 hours
);

CREATE TABLE IF NOT EXISTS kiosk_stats (
    date                TEXT PRIMARY KEY,   -- YYYY-MM-DD
    pages_printed       INTEGER DEFAULT 0,
    revenue             REAL DEFAULT 0.0,
    jobs_completed      INTEGER DEFAULT 0,
    jobs_expired        INTEGER DEFAULT 0,
    paper_jams          INTEGER DEFAULT 0,
    avg_wait_secs       REAL DEFAULT 0.0,
    peak_queue_length   INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS energy_log (
    timestamp           TEXT PRIMARY KEY,   -- ISO 8601
    voltage             REAL,
    current_amps        REAL,
    power_watts         REAL,
    energy_kwh          REAL,
    power_tier          TEXT                -- active, light_sleep, deep_sleep, night
);

CREATE TABLE IF NOT EXISTS error_log (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp           TEXT DEFAULT (datetime('now')),
    error_type          TEXT,               -- paper_jam, payment_fail, file_error, overheat
    message             TEXT,
    job_id              TEXT,
    resolved            INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_jobs_otp ON jobs(otp);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_created ON jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
