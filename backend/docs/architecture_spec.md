# Sprint 1: Cloudburst Parameter Analysis & Backend Architecture

**Member:** Ashish Sharma (Backend Lead & Team Lead)  
**Dates:** 21/09/2026 – 05/10/2026  
**User Story:** "We will analyze cloudburst conditions and identify parameters"  
**Details of Task:** "We will study the problem and finalize the required sensor communication method and software components."  

---

## 1. Cloudburst Conditions & Parameter Identification

A cloudburst is an extreme meteorological phenomenon characterized by intense rainfall (> 100 mm/hour over a localized area of ~20–30 sq km), often accompanied by rapid convective updrafts and flash floods in mountainous terrains.

Through our analysis, the key environmental parameters required for early detection are:
1. **Precipitation Intensity ($R$)**: Measured in mm/hr via tipping bucket rain gauge. Spikes $> 50$ mm/hr signal high convective storm cells.
2. **Barometric Pressure Gradient ($\Delta P / \Delta t$)**: Sudden drops exceeding $-2.5$ to $-4.0$ hPa within 15–30 minutes indicate severe mesoscale convective system (MCS) formation.
3. **Relative Humidity ($RH$)**: Saturated air mass ($RH > 90\%$) with rapid moisture convergence.
4. **Ambient Temperature ($T$) & Dew Point ($T_d$)**: Small depression ($T - T_d < 1.5^\circ\text{C}$) confirming low cloud condensation level.

---

## 2. Sensor Communication Protocol (LoRa to Backend Gateway)

In remote hilly terrains with intermittent cellular coverage, edge stations communicate over LoRa (868/433 MHz). The base station gateway receives raw LoRa packets and relays JSON payloads over HTTP/REST to the central FastAPI backend:

```json
{
  "station_id": "STN-01",
  "timestamp": "2026-10-02T10:30:00Z",
  "rainfall_rate": 14.5,
  "rain_accum_1h": 8.2,
  "pressure": 1008.4,
  "pressure_drop_rate": -1.8,
  "temperature": 18.2,
  "humidity": 88.5,
  "battery_pct": 94,
  "signal_rssi": -76
}
```

---

## 3. Backend Software Component Architecture

```
[LoRa Edge Nodes] ──(LoRa RF)──> [Gateway Station] ──(HTTP POST)──> [FastAPI Server]
                                                                        │
                   ┌────────────────────────┬───────────────────────────┤
                   ▼                        ▼                           ▼
          [Sensor Ingestion API]    [Database Engine]           [Alert & ML Engine]
          - Validation (Pydantic)   - SQLAlchemy ORM            - Threshold Evaluation
          - Ingestion Endpoints     - SQLite / PostgreSQL       - ML Model Scoring
                                    - Time-series readings      - Emergency Siren Dispatches
```
