# Cloudburst Early Warning & Alarm System - Backend Server

**Author:** Ashish Sharma (Backend Lead & Team Lead)  
**Project ID:** SKIT/AI/2023-2027/09 | **Branch:** CSE (AI), Section A  
**Role:** Server, Database & Data Management  
**Session:** 2026–2027  

---

## Overview

The Backend Server is the central intelligence and data ingestion backbone of the **Cloudburst Early Warning & Alarm System**. Built with **FastAPI** and **SQLAlchemy**, it processes high-frequency telemetry transmitted by distributed mountain sensor stations (via LoRa Gateway / HTTP), manages time-series storage, runs automated hazard threshold detection, and integrates with AI/ML predictive models for real-time risk assessment.

---

## Core Capabilities

1. **Sensor Ingestion Engine**: High-throughput REST API validating incoming telemetry packets (Rainfall rate, Atmospheric pressure, Temperature, Humidity).
2. **Relational Time-Series Database**: SQLite/PostgreSQL layer managing sensor readings, station metadata, and emergency incident logs.
3. **Automated Alert & Alarm Service**: Threshold rule engine detecting cloudburst precursors (steep barometric pressure plunge, torrential rainfall spikes) and dispatching warnings.
4. **AI/ML Inference Integration**: Real-time scoring adapter predicting flash flood and cloudburst probabilities for the frontend monitoring dashboard.
5. **Comprehensive Testing**: Pytest test suite validating data ingestion, database transactions, alert dispatching, and prediction APIs.

---

## Sprints Roadmap (Form-2 Alignment)

| Sprint | Date Range | Sprint Objective | Status |
|---|---|---|---|
| **Sprint 1** | 21/09/2026 – 05/10/2026 | Analyze cloudburst conditions, parameters & finalize architecture | Completed |
| **Sprint 2** | 05/10/2026 – 25/10/2026 | Design backend project structure, FastAPI app skeleton & config | Completed |
| **Sprint 3** | 26/10/2026 – 15/11/2026 | Develop sensor data ingestion REST APIs & validation schemas | Completed |
| **Sprint 4** | 16/11/2026 – 30/11/2026 | Database integration with SQLAlchemy ORM & CRUD repositories | Completed |
| **Sprint 5** | 30/11/2026 – 25/12/2026 | Connect backend with automated alert & early warning system | Completed |
| **Sprint 6** | 26/12/2026 – 20/01/2027 | Integrate backend with AI/ML prediction pipeline | Completed |
| **Sprint 7** | 20/01/2027 – 15/02/2027 | End-to-end backend data flow testing & test suites | Completed |

---

## How to Run

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Start the FastAPI development server:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Interactive API documentation (Swagger UI):
   Visit `http://localhost:8000/docs`.
