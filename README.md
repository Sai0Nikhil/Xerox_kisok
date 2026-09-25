# Bittu Xerox Kiosk — 24/7 Smart Campus Printing & Scanning System
**Autonomous, Zero-Clerk Privacy Self-Service Document Hub for University Campuses & Hostels**

---

## 📁 Repository Structure

```text
c:\zerox_kisok\
├── cad/                              # 3D CAD Models & 2D AutoCAD Blueprints
│   ├── kiosk_model.scad              # 3D Parametric OpenSCAD Assembly (15.6" Screen + Rear Vents)
│   ├── kiosk_cad_blueprint.dxf       # 1:1 Metric 2D Orthographic CAD Blueprint (AutoCAD / DXF)
│   └── generate_dxf.py               # Parametric Python script to regenerate/adjust DXF drawings
│
├── docs/                             # Proposals, Pitch Decks & Engineering Specs
│   ├── CAMPUS_INCUBATION_PITCH_DECK.md # Complete Pitch Deck & Proposal for HOD / Incubation E-Cell
│   ├── AUTOCAD_DESIGN_SPEC.md        # Mechanical, Ergonomic & Electrical Architectural Specs
│   ├── PROJECT_EXECUTION_ROADMAP.md  # 5-Phase Campus Deployment & Execution Plan
│   ├── Bittu_Xerox_Kiosk_Proposal.docx # Original Project Proposal Document
│   └── proposal_extracted.md         # Markdown Transcript of Proposal
│
├── procurement/                      # Procurement Budget & Vendor Sourcing
│   ├── BITTU_Xerox_Kiosk_Procurement_BOM.xlsx # 100% Itemized Bill of Materials (BOM)
│   └── excel_bom_extracted.md        # Markdown summary of Procurement BOM & Vijayawada Buying Plan
│
└── assets/                           # Reference Imagery & Visual Assets
    └── reference_images/             # Original OpenSCAD render screenshots (Figures 1 to 6)
```

---

## 🚀 Quick Start Guide

### 1. View 3D CAD Model in OpenSCAD
1. Open **OpenSCAD**.
2. Open [`cad/kiosk_model.scad`](file:///c:/zerox_kisok/cad/kiosk_model.scad).
3. Press **`F5`** (Preview) or **`F6`** (Render).
   * Toggle `view_mode = "side_by_side";` (default) to inspect the internal frame on the left and the finished enclosure on the right.
   * Toggle `view_mode = "assembled";` for the full combined unit.

### 2. View 2D Blueprint in AutoCAD / Web Viewer
1. Open [`cad/kiosk_cad_blueprint.dxf`](file:///c:/zerox_kisok/cad/kiosk_cad_blueprint.dxf) in **AutoCAD**, **QCAD**, or drag-and-drop into [Autodesk Viewer (viewer.autodesk.com)](https://viewer.autodesk.com/).
2. Contains Front Elevation, Side Section, Top Plan View, and exact layer annotations.

### 3. Review Pitch Deck & Incubation Ask
* Read [`docs/CAMPUS_INCUBATION_PITCH_DECK.md`](file:///c:/zerox_kisok/docs/CAMPUS_INCUBATION_PITCH_DECK.md) for the 52% gross margin economics, student privacy rationale, and the incubation grant ask.

---

## ⚙️ Core Technical Specifications

| Parameter | Specification | Purpose / Standard |
| :--- | :--- | :--- |
| **Total Height ($H$)** | **1,650 mm (5.4 ft)** | Eye-level viewing for 5th percentile female to 95th percentile male |
| **Total Width ($W$)** | **600 mm (2.0 ft)** | Fits compact hostel lobby corridors |
| **Total Depth ($D$)** | **600 mm (2.0 ft)** | Low center-of-gravity stabilization (heavy UPS at bottom) |
| **Display** | **15.6" Full HD Capacitive Touchscreen** | Touch-first intuitive student interface |
| **Laser Printer** | **Brother HL-L2321D** | High-speed monochrome auto-duplex printing |
| **Flatbed Scanner** | **Canon CanoScan LiDE 300** | USB-powered instant photocopy / scanning |
| **Power Backup** | **600VA Line-Interactive UPS** | Clean power backup during generator changeovers |
| **Controller** | **Raspberry Pi 5 (2GB) + Active Cooler** | Linux-based CUPS & SANE local orchestrator |
| **Total Budget** | **~₹48,400 (Under ₹50k Goal)** | 70% cheaper than commercial market franchises |
