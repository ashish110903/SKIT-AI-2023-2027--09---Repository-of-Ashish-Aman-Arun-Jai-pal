# Cloudburst Early Warning & Alarm System - Frontend Dashboard

**Author:** Jai Pal (Frontend Lead & User Interface Developer)  
**Project ID:** SKIT/AI/2023-2027/09 | **Branch:** CSE (AI), Section A  
**Role:** Dashboard and User Interface Development  
**Session:** 2026–2027  

---

## Overview

The Frontend Monitoring Dashboard is a real-time, mission-critical web application designed to monitor distributed environmental sensors (Rainfall rate, Atmospheric Pressure, Temperature, Relative Humidity) across hilly terrains prone to cloudburst disasters.

The interface serves emergency response authorities, meteorological station operators, and local administrative teams by providing:
1. **Real-Time Sensor Telemetry**: Multi-station telemetry visualization with continuous updates.
2. **AI/ML Cloudburst Risk Gauge**: Instant visual indicator of localized cloudburst risk derived from trained predictive models.
3. **Emergency Warning & Audio Alarm**: High-visibility warning banners, modal alerts, and audible sirens.
4. **Poor-Connectivity Resilience**: Offline-first cached local operations with automatic backend sync when connectivity is restored.

---

## Sprints Roadmap (Form-2 Alignment)

| Sprint | Date Range | Sprint Objective | Status |
|---|---|---|---|
| **Sprint 1** | 25/09/2026 – 10/10/2026 | Design monitoring dashboard layout, wireframes & component skeleton | Completed |
| **Sprint 2** | 10/10/2026 – 30/10/2026 | Display real-time sensor data (Rainfall, Pressure, Temp, Humidity charts) | Completed |
| **Sprint 3** | 01/11/2026 – 25/11/2026 | Display AI/ML prediction results and risk gauge | Completed |
| **Sprint 4** | 25/11/2026 – 20/12/2026 | Warning notification UI, modal & audible emergency siren system | Completed |
| **Sprint 5** | 20/12/2026 – 20/01/2027 | Full integration with FastAPI backend & live data ingestion | Completed |
| **Sprint 6** | 25/01/2027 – 15/02/2027 | End-to-end dashboard testing, simulation suite & validation | Completed |

---

## Technology Stack

- **Markup & Layout:** Semantic HTML5, CSS Grid, Flexbox
- **Styling:** Custom CSS3 with Modern Theme (Dark/Light mode support, High-contrast warning states)
- **Data Visualization:** Chart.js 4.x (Time-series multi-sensor charts)
- **Audio Synthesis:** Web Audio API (Client-side zero-dependency emergency siren generator)
- **API Integration:** Async Fetch API, Server-Sent Events / Polling Engine with offline fallback
- **Testing:** Custom In-Browser Test Suite & Simulation Control Panel

---

## How to Run

1. Open `index.html` directly in any modern web browser (Chrome, Edge, Firefox).
2. Alternatively, serve via Python's built-in HTTP server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
3. Access the dashboard at `http://localhost:3000`.
