# Sprint 5: Backend API Integration & Poor-Connectivity Resilience

**Member:** Jai Pal (Frontend)  
**Dates:** 20/12/2026 – 20/01/2027  
**User Story:** "We will connect the dashboard with backend"  
**Details of Task:** "We will fetch and display real-time data from the backend"  

---

## Objectives & Deliverables
1. **Asynchronous REST API Integration**:
   - Built modular `api.js` client interacting with Ashish Sharma's FastAPI server:
     - `GET /api/v1/sensors/latest?station_id={id}`
     - `GET /api/v1/predict/status?station_id={id}`
     - `GET /api/v1/alerts/active`
2. **Resilience to Poor Mountain Connectivity**:
   - Built-in abort controllers with automatic timeout protection (4000ms).
   - If connectivity to the central server is intermittent, the dashboard automatically transitions into local offline cache mode, displaying the active LoRa buffer without freezing the user interface.
3. **Live Polling Engine**:
   - Automated 5-second polling loop refreshing sensor cards, charts, and risk predictions dynamically.
