# Sprint 3: Sensor Telemetry Ingestion APIs

**Member:** Ashish Sharma (Backend Lead & Team Lead)  
**Dates:** 26/10/2026 – 15/11/2026  
**User Story:** "We will develop API's for sensor data"  
**Details of Task:** "We will develop API's to recieve and process data from the hardware system."  

---

## Deliverables & API Contracts

1. **Ingestion Endpoint**: `POST /api/v1/sensors/telemetry`
   - Accepts JSON payload from LoRa receiver/gateway.
   - Pydantic schema validation for sensor ranges (e.g., pressure between 800–1100 hPa, humidity 0–100%).
   - Response: `201 Created` with acknowledgment ID.

2. **Dashboard Query Endpoints**:
   - `GET /api/v1/sensors/latest?station_id={id}`: Supplies real-time telemetry to Jai Pal's frontend KPI cards.
   - `GET /api/v1/sensors/history?station_id={id}&limit=12`: Supplies time-series data buffer to Chart.js.
