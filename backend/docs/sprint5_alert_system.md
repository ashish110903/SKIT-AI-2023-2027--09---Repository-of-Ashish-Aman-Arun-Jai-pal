# Sprint 5: Automated Alert & Emergency Alarm System

**Member:** Ashish Sharma (Backend Lead & Team Lead)  
**Dates:** 30/11/2026 – 25/12/2026  
**User Story:** "We will connect the backend with the alert system."  
**Details of Task:** "We will send warning information from the backend to the frontend and alert alert"  

---

## Deliverables & Alert Pipeline

1. **Hazard Threshold Service (`services/alert_service.py`)**:
   - Compares streaming parameters against meteorological risk thresholds:
     - `WARNING`: Rain rate $\ge 50$ mm/hr AND Pressure drop $\le -3.5$ hPa/hr.
     - `WATCH`: Rain rate $\ge 20$ mm/hr OR Pressure drop $\le -2.0$ hPa/hr.
   - Automatically records triggered alerts into `alert_records` table.

2. **Alert Endpoints (`routes/alerts.py`)**:
   - `GET /api/v1/alerts/active`: Polled by Jai Pal's frontend `api.js` to trigger the audio siren and flashing modal.
   - `POST /api/v1/alerts/{id}/ack`: Records operator acknowledgement when "Silence Siren / Acknowledge" is clicked.
