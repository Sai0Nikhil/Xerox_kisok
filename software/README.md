# Bittu Xerox Kiosk — Software

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# 2. Install dependencies
pip install -r backend/requirements.txt
pip install -r bot/requirements.txt

# 3. Configure
copy .env.example .env
# Edit .env with your tokens

# 4. Initialize database
python -c "from backend.database import init_db; init_db()"

# 5. Run backend
uvicorn backend.main:app --reload --port 8000

# 6. Run bot (separate terminal)
python -m bot.bot

# 7. Open UI
# Browser → http://localhost:8000
```

## Architecture

```
Student → Telegram Bot ──HTTP──→ FastAPI Backend ──→ CUPS → Printer
Student → QR Upload ────HTTP──→ FastAPI Backend ──→ CUPS → Printer
Student → ERP (Phase 2) ─────→ FastAPI Backend ──→ CUPS → Printer
```

## Modules

| Module | Directory | Owner | Status |
|--------|-----------|-------|--------|
| Backend API | `backend/` | TBD | 🔴 Not started |
| Telegram Bot | `bot/` | TBD | 🔴 Not started |
| Kiosk UI | `kiosk-ui/` | TBD | 🔴 Not started |
| Power Manager | `power/` | TBD | 🔴 Not started |

## Sprint 1 Goal (Week 1)

Upload a PDF via web form → see page count + price → fake "Printed!" confirmation.

No Telegram. No payment. No real printer. Just prove the pipeline works.

## Full Developer Guide

See `docs/DEVELOPER_GUIDE.md` for complete API contracts, database schema, task board, and team splitting guide.
