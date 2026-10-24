# Sprint 2: Real-Time Sensor Telemetry Display

**Member:** Jai Pal (Frontend)  
**Dates:** 10/10/2026 – 30/10/2026  
**User Story:** "We will display sensor data on the dashboard"  
**Details of Task:** "We will display rainfall, pressure and other sensor readings."  

---

## Objectives & Deliverables
1. **Multi-Sensor Visualization**: Integrated Chart.js 4.x for dynamic rolling charts tracking:
   - Rainfall Intensity (`mm/h`) with a cumulative 1-hour total.
   - Atmospheric Barometric Pressure (`hPa`) with a rolling 15-minute rate of change (`ΔP/Δt`).
   - Ambient Temperature (`°C`) and Relative Humidity (`%`).
2. **Station Telemetry Cards**:
   - High-contrast KPI metric cards featuring live value formatting, tabular numeric rendering, and threshold status badges (e.g., `STABLE`, `RAPID PLUNGE`, `TORRENTIAL`).
3. **Filtering Controls**:
   - Tab toggles allowing operators to isolate individual sensor curves (All Sensors vs. Rainfall vs. Pressure Drop) for granular analysis during severe weather events.
