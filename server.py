import os
import time
import uuid
import json
import asyncio
import random
from typing import Dict, List, Optional
from fastapi import FastAPI, Request, UploadFile, File, Form, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Bittu Xerox Kiosk - Smart Campus Printing OS")

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory State & Database
class KioskState:
    def __init__(self):
        self.kiosk_id = "KLU-HOSTEL-K1"
        self.location = "KL University - Boys Hostel Block 4"
        self.status = "READY"  # READY, PRINTING, SCANNING, MAINTENANCE, PAPER_OUT
        self.paper_count = 420  # Out of 500 max in tray
        self.paper_capacity = 500
        self.toner_level = 78  # Percentage
        self.drum_life = 92  # Percentage
        self.temperature = 34.2  # Celsius
        self.fan_rpm = 1850
        self.ups_battery = 98  # Percentage
        self.ups_voltage = 232  # Volts
        self.total_energy_kwh = 14.82
        self.door_locked = True
        self.tamper_alert = False
        
        # Financials
        self.pages_printed_today = 384
        self.revenue_today = 384 * 2.50
        self.total_orders = 64
        
        # Active Sessions
        self.active_session: Optional[dict] = None
        self.recent_transactions: List[dict] = [
            {"id": "TXN-9021", "time": "22:15", "pages": 8, "type": "Mobile PDF", "amount": 20.0, "status": "COMPLETED", "upi_ref": "428901239812"},
            {"id": "TXN-9020", "time": "21:52", "pages": 2, "type": "Xerox Copy", "amount": 5.0, "status": "COMPLETED", "upi_ref": "428901239811"},
            {"id": "TXN-9019", "time": "21:30", "pages": 14, "type": "Lab Manual", "amount": 35.0, "status": "COMPLETED", "upi_ref": "428901239810"},
            {"id": "TXN-9018", "time": "20:45", "pages": 1, "type": "Hall Ticket", "amount": 2.5, "status": "COMPLETED", "upi_ref": "428901239809"},
            {"id": "TXN-9017", "time": "20:10", "pages": 4, "type": "Aadhaar Card", "amount": 10.0, "status": "COMPLETED", "upi_ref": "428901239808"}
        ]
        
        # WhatsApp Mock Queue (PIN -> Document)
        self.whatsapp_jobs = {
            "7842": {
                "pin": "7842",
                "sender": "+91 98765 43210",
                "filename": "Operating_Systems_Lab_Record.pdf",
                "pages": 6,
                "preview_title": "OS Lab Record - Exp 4 & 5",
                "created_at": "Just now"
            },
            "1290": {
                "pin": "1290",
                "sender": "+91 87654 32109",
                "filename": "Aadhaar_Card_Verified.pdf",
                "pages": 1,
                "preview_title": "Government ID Proof (Aadhaar)",
                "created_at": "5 mins ago"
            }
        }

kiosk = KioskState()

# WebSocket Connection Manager for Realtime Kiosk & Mobile Sync
class ConnectionManager:
    def __init__(self):
        self.kiosk_sockets: List[WebSocket] = []
        self.admin_sockets: List[WebSocket] = []
        self.mobile_sockets: Dict[str, WebSocket] = {}

    async def connect_kiosk(self, websocket: WebSocket):
        await websocket.accept()
        self.kiosk_sockets.append(websocket)

    def disconnect_kiosk(self, websocket: WebSocket):
        if websocket in self.kiosk_sockets:
            self.kiosk_sockets.remove(websocket)

    async def connect_admin(self, websocket: WebSocket):
        await websocket.accept()
        self.admin_sockets.append(websocket)

    def disconnect_admin(self, websocket: WebSocket):
        if websocket in self.admin_sockets:
            self.admin_sockets.remove(websocket)

    async def connect_mobile(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        self.mobile_sockets[session_id] = websocket

    def disconnect_mobile(self, session_id: str):
        if session_id in self.mobile_sockets:
            del self.mobile_sockets[session_id]

    async def broadcast_kiosk(self, message: dict):
        for ws in self.kiosk_sockets:
            try:
                await ws.send_json(message)
            except Exception:
                pass

    async def broadcast_admin(self, message: dict):
        for ws in self.admin_sockets:
            try:
                await ws.send_json(message)
            except Exception:
                pass

    async def send_to_mobile(self, session_id: str, message: dict):
        if session_id in self.mobile_sockets:
            try:
                await self.mobile_sockets[session_id].send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# Background telemetry updater simulation
async def telemetry_background_loop():
    while True:
        await asyncio.sleep(3)
        # Small realistic jitter for temperature & fans
        if kiosk.status == "PRINTING":
            kiosk.temperature = round(min(45.0, kiosk.temperature + random.uniform(0.2, 0.6)), 1)
            kiosk.fan_rpm = 2400
        else:
            kiosk.temperature = round(max(32.0, kiosk.temperature - random.uniform(0.1, 0.3)), 1)
            kiosk.fan_rpm = 1750 + random.randint(-50, 50)
            
        telemetry_data = {
            "type": "TELEMETRY_UPDATE",
            "kiosk_id": kiosk.kiosk_id,
            "status": kiosk.status,
            "paper_count": kiosk.paper_count,
            "paper_capacity": kiosk.paper_capacity,
            "toner_level": kiosk.toner_level,
            "drum_life": kiosk.drum_life,
            "temperature": kiosk.temperature,
            "fan_rpm": kiosk.fan_rpm,
            "ups_battery": kiosk.ups_battery,
            "ups_voltage": kiosk.ups_voltage,
            "total_energy_kwh": kiosk.total_energy_kwh,
            "pages_today": kiosk.pages_printed_today,
            "revenue_today": kiosk.revenue_today,
            "door_locked": kiosk.door_locked
        }
        await manager.broadcast_admin(telemetry_data)
        await manager.broadcast_kiosk({"type": "STATUS_REFRESH", "paper_count": kiosk.paper_count, "toner_level": kiosk.toner_level})

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telemetry_background_loop())

# ==========================================
# WEB ROUTES
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def get_kiosk_view(request: Request):
    return templates.TemplateResponse(request=request, name="kiosk.html", context={"kiosk": kiosk})

@app.get("/kiosk", response_class=HTMLResponse)
async def get_kiosk_alias(request: Request):
    return templates.TemplateResponse(request=request, name="kiosk.html", context={"kiosk": kiosk})

@app.get("/mobile", response_class=HTMLResponse)
async def get_mobile_view(request: Request, session_id: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="mobile.html", context={"session_id": session_id or ""})

@app.get("/admin", response_class=HTMLResponse)
async def get_admin_view(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html", context={"kiosk": kiosk})

# ==========================================
# REST API ENDPOINTS
# ==========================================
@app.get("/api/session/new")
async def create_new_session():
    session_id = str(uuid.uuid4())[:8].upper()
    kiosk.active_session = {
        "session_id": session_id,
        "created_at": time.time(),
        "files": [],
        "status": "WAITING_FOR_UPLOAD"
    }
    return {"status": "success", "session_id": session_id}

@app.post("/api/upload")
async def handle_mobile_upload(
    session_id: str = Form(...),
    copies: int = Form(1),
    duplex: bool = Form(False),
    color_mode: str = Form("bw"),
    file: Optional[UploadFile] = File(None),
    mock_filename: Optional[str] = Form(None),
    mock_pages: int = Form(1)
):
    filename = file.filename if file else (mock_filename or "Document.pdf")
    pages = mock_pages if mock_pages > 0 else (random.randint(2, 8) if file else 3)
    cost_per_page = 2.50 if color_mode == "bw" else 10.00
    total_amount = round(pages * copies * cost_per_page, 2)
    
    order_data = {
        "session_id": session_id,
        "filename": filename,
        "pages": pages,
        "copies": copies,
        "duplex": duplex,
        "color_mode": color_mode,
        "total_amount": total_amount,
        "upi_id": f"paytmqr28100505@paytm",
        "qr_payload": f"upi://pay?pa=paytmqr28100505@paytm&pn=BittuXerox&am={total_amount}&cu=INR&tn=Kiosk-{session_id}"
    }
    
    kiosk.active_session = order_data
    
    # Notify Kiosk Touchscreen in real-time
    await manager.broadcast_kiosk({
        "type": "FILE_UPLOADED",
        "order": order_data
    })
    
    return {"status": "success", "order": order_data}

@app.post("/api/pay/simulate")
async def simulate_upi_payment(session_id: str = Form(...)):
    if not kiosk.active_session or kiosk.active_session.get("session_id") != session_id:
        # Fallback create session
        kiosk.active_session = {
            "session_id": session_id,
            "filename": "Lab_Evaluation_Report.pdf",
            "pages": 4,
            "copies": 1,
            "total_amount": 10.0,
            "color_mode": "bw"
        }
        
    order = kiosk.active_session
    txn_id = f"TXN-{random.randint(1000, 9999)}"
    utr_no = f"42890{random.randint(1000000, 9999999)}"
    
    # Record transaction
    new_txn = {
        "id": txn_id,
        "time": time.strftime("%H:%M"),
        "pages": order.get("pages", 1) * order.get("copies", 1),
        "type": "Mobile Print",
        "amount": order.get("total_amount", 2.50),
        "status": "COMPLETED",
        "upi_ref": utr_no
    }
    kiosk.recent_transactions.insert(0, new_txn)
    if len(kiosk.recent_transactions) > 20:
        kiosk.recent_transactions.pop()
        
    kiosk.pages_printed_today += new_txn["pages"]
    kiosk.revenue_today += new_txn["amount"]
    kiosk.paper_count = max(0, kiosk.paper_count - new_txn["pages"])
    kiosk.total_energy_kwh = round(kiosk.total_energy_kwh + (new_txn["pages"] * 0.003), 3)
    kiosk.status = "PRINTING"
    
    # Broadcast to Kiosk to start printing animation & hardware execution
    await manager.broadcast_kiosk({
        "type": "PAYMENT_SUCCESS",
        "txn": new_txn,
        "order": order
    })
    
    # Broadcast to Mobile
    await manager.send_to_mobile(session_id, {
        "type": "PAYMENT_CONFIRMED",
        "txn": new_txn
    })
    
    # Broadcast to Admin Dashboard
    await manager.broadcast_admin({
        "type": "NEW_TRANSACTION",
        "txn": new_txn,
        "pages_today": kiosk.pages_printed_today,
        "revenue_today": kiosk.revenue_today,
        "paper_count": kiosk.paper_count
    })
    
    return {"status": "success", "txn": new_txn}

@app.post("/api/print/complete")
async def complete_print_job(session_id: str = Form(...)):
    kiosk.status = "READY"
    kiosk.active_session = None
    
    await manager.broadcast_kiosk({
        "type": "JOB_COMPLETED",
        "message": "Documents printed and RAM cache shredded securely."
    })
    
    await manager.broadcast_admin({
        "type": "STATUS_CHANGE",
        "status": "READY"
    })
    
    return {"status": "success"}

@app.post("/api/whatsapp/verify-pin")
async def verify_whatsapp_pin(pin: str = Form(...)):
    pin = pin.strip()
    if pin in kiosk.whatsapp_jobs:
        job = kiosk.whatsapp_jobs[pin]
        session_id = f"WA-{pin}"
        total_amount = round(job["pages"] * 2.50, 2)
        order_data = {
            "session_id": session_id,
            "filename": job["filename"],
            "pages": job["pages"],
            "copies": 1,
            "duplex": True,
            "color_mode": "bw",
            "total_amount": total_amount,
            "preview_title": job["preview_title"],
            "sender": job["sender"],
            "qr_payload": f"upi://pay?pa=paytmqr28100505@paytm&pn=BittuXerox&am={total_amount}&cu=INR&tn=Kiosk-{session_id}"
        }
        kiosk.active_session = order_data
        return {"status": "success", "order": order_data}
    else:
        raise HTTPException(status_code=404, detail="Invalid or expired WhatsApp PIN.")

@app.post("/api/erp/fetch")
async def fetch_erp_document(roll_no: str = Form(...), doc_type: str = Form("hall_ticket")):
    roll_no = roll_no.strip().upper()
    if not roll_no:
        roll_no = "2100030142"
        
    doc_titles = {
        "hall_ticket": "KLU Odd Sem End Examination Hall Ticket - Dec 2026",
        "lab_cover": "Department of CSE - Lab Record Front Cover",
        "bonafide": "Bonafide Student Certificate (Signed)"
    }
    
    pages = 1 if doc_type != "lab_cover" else 2
    total_amount = round(pages * 2.50, 2)
    session_id = f"ERP-{roll_no[-4:]}"
    
    order_data = {
        "session_id": session_id,
        "filename": f"{doc_type.upper()}_{roll_no}.pdf",
        "pages": pages,
        "copies": 1,
        "duplex": False,
        "color_mode": "bw",
        "total_amount": total_amount,
        "roll_no": roll_no,
        "student_name": f"Student ({roll_no})",
        "preview_title": doc_titles.get(doc_type, "Campus ERP Document"),
        "qr_payload": f"upi://pay?pa=paytmqr28100505@paytm&pn=BittuXerox&am={total_amount}&cu=INR&tn=Kiosk-{session_id}"
    }
    kiosk.active_session = order_data
    return {"status": "success", "order": order_data}

@app.post("/api/admin/refill-paper")
async def refill_paper():
    kiosk.paper_count = 500
    await manager.broadcast_admin({
        "type": "PAPER_REFILLED",
        "paper_count": 500
    })
    await manager.broadcast_kiosk({
        "type": "STATUS_REFRESH",
        "paper_count": 500,
        "toner_level": kiosk.toner_level
    })
    return {"status": "success", "paper_count": 500}

@app.post("/api/admin/trigger-action")
async def trigger_admin_action(action: str = Form(...)):
    if action == "TEST_PRINT":
        kiosk.paper_count = max(0, kiosk.paper_count - 1)
        kiosk.status = "PRINTING"
        await manager.broadcast_kiosk({"type": "HARDWARE_TEST", "msg": "Running Diagnostic Test Page..."})
        await asyncio.sleep(2)
        kiosk.status = "READY"
        await manager.broadcast_kiosk({"type": "STATUS_REFRESH", "paper_count": kiosk.paper_count, "toner_level": kiosk.toner_level})
    elif action == "PURGE_CACHE":
        await manager.broadcast_kiosk({"type": "CACHE_PURGED", "msg": "Volatile RAM & Temporary spool wiped."})
    elif action == "TOGGLE_MAINTENANCE":
        kiosk.status = "MAINTENANCE" if kiosk.status != "MAINTENANCE" else "READY"
        await manager.broadcast_kiosk({"type": "STATUS_REFRESH", "status": kiosk.status})
    elif action == "TOGGLE_DOOR":
        kiosk.door_locked = not kiosk.door_locked
    
    await manager.broadcast_admin({
        "type": "ADMIN_ACTION_SUCCESS",
        "action": action,
        "status": kiosk.status,
        "door_locked": kiosk.door_locked
    })
    return {"status": "success", "action": action}

# ==========================================
# WEBSOCKET ENDPOINTS
# ==========================================
@app.websocket("/ws/kiosk")
async def websocket_kiosk_endpoint(websocket: WebSocket):
    await manager.connect_kiosk(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_kiosk(websocket)

@app.websocket("/ws/admin")
async def websocket_admin_endpoint(websocket: WebSocket):
    await manager.connect_admin(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_admin(websocket)

@app.websocket("/ws/mobile/{session_id}")
async def websocket_mobile_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect_mobile(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_mobile(session_id)

if __name__ == "__main__":
    import uvicorn
    print("Starting Bittu Xerox Kiosk System on http://localhost:8000")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
