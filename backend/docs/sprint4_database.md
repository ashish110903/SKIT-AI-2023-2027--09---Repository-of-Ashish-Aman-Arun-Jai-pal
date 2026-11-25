# Sprint 4: Database Integration & Storage Architecture

**Member:** Ashish Sharma (Backend Lead & Team Lead)  
**Dates:** 16/11/2026 – 30/11/2026  
**User Story:** "We will connect the backend with the database"  
**Details of Task:** "We will store and manage sensor data in the database"  

---

## Deliverables & Data Models

1. **SQLAlchemy ORM Layer (`database.py`, `models.py`)**:
   - `stations`: Hardware node registry (ID, coordinates, altitude, health status).
   - `sensor_readings`: Time-series sensor measurements (rainfall, pressure, temperature, humidity, LoRa signal).
   - `alert_records`: Audit log of triggered hazard warnings and operator acknowledgments.

2. **Repository Operations (`crud.py`)**:
   - `create_sensor_reading`: Atomically saves new packets.
   - `get_latest_reading`: High-speed indexed query for real-time dashboard status.
   - `get_historical_readings`: Fetches rolling chronological window for charting.
