# Sprint 2: Backend Structure & Core Service Design

**Member:** Ashish Sharma (Backend Lead & Team Lead)  
**Dates:** 05/10/2026 – 25/10/2026  
**User Story:** "We will design the backend structure for the project"  
**Details of Task:** "We will prepare the backend structure for receiving and managing sensor data."  

---

## Deliverables & Architecture

1. **Modular Directory Structure**:
   ```
   backend/
   ├── config.py         # Environmental configurations & hazard thresholds
   ├── database.py       # SQLAlchemy ORM session & database engine
   ├── models.py         # Database entities (SensorReading, Station, AlertLog)
   ├── schemas.py        # Pydantic data validation contracts
   ├── crud.py           # Database transaction repositories
   ├── main.py           # FastAPI server & route orchestration
   ├── routes/           # REST API endpoints (sensors, alerts, predict)
   ├── services/         # Alert threshold & ML scoring engines
   ├── tests/            # Pytest automated testing suite
   └── docs/             # Technical specifications & sprint logs
   ```

2. **CORS & Multi-Client Support**:
   - Integrated CORS middleware allowing secure bi-directional telemetry exchanges with the frontend dashboard.
   - Built health check endpoints for gateway connectivity probes.
