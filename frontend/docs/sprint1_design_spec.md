# Sprint 1: Dashboard Interface Design Specification

**Member:** Jai Pal (Frontend)  
**Dates:** 25/09/2026 – 10/10/2026  
**User Story:** "We will design the monitoring dashboard"  
**Details of Task:** "We will create the basic dashboard interface for the project"  

---

## 1. Problem Statement & UX Objectives
Cloudburst phenomena in hilly regions are sudden, localized, and devastating. Traditional weather portals are often too complex, overloaded, or sluggish for rapid evacuation decision-making. 

The primary UX objectives for this monitoring dashboard are:
1. **Sub-second Comprehension**: Operators must assess the danger level across all monitored stations within 3 seconds of looking at the screen.
2. **Terrain-Aware Spatial Grouping**: Hill stations are grouped by ridge/valley geography (e.g., Station 1: Mussoorie Ridge, Station 2: Kedarnath Valley, Station 3: Shimla Foothills).
3. **High-Contrast Warning States**: Clear visual hierarchy transitioning from tranquil teal/slate in normal conditions to pulsating scarlet/amber during emergency alerts.
4. **Resilience to Poor Connectivity**: The interface must visibly report link health (LoRa Gateway / Cellular backhaul status) without freezing.

---

## 2. Information Architecture & Layout Structure

The layout is structured into 4 primary viewports:

```
+--------------------------------------------------------------------------------+
|  LOGO & TITLE   |  STATION STATUS  |  NETWORK STATUS  |  SYSTEM CLOCK (IST)   |
+--------------------------------------------------------------------------------+
|  [Mussoorie Ridge]  [Kedarnath Valley]  [Shimla Peak]  [Nainital Slopes]       |
+--------------------------------------------------------------------------------+
|  KPI CARDS:                                                                    |
|  [Rainfall Rate]   [Barometric Pressure]   [Temperature]   [Humidity]          |
+--------------------------------------------------------------------------------+
|  TELEMETRY TREND CHARTS              |  AI/ML PREDICTION & RISK ASSESSMENT     |
|  - Rainfall Intensity (mm/h)         |  - Real-Time Risk Gauge (0-100%)        |
|  - Atmospheric Pressure Trend (hPa)  |  - Risk Tier: NORMAL / WATCH / WARNING  |
|  - Temp & Humidity Correlation       |  - Anomaly Checklist                    |
+--------------------------------------------------------------------------------+
|  EMERGENCY ACTION BANNER & ACTIVE ALERTS LOG                                   |
+--------------------------------------------------------------------------------+
```

---

## 3. Component Hierarchy
- **Header**: Branding, live digital clock, online/offline badge, emergency siren toggle.
- **Station Selector**: Horizontal pill navigation to switch between remote mountain monitoring nodes.
- **Metric Cards (KPIs)**:
  - `Rainfall Rate (mm/h)` with 1-hr delta.
  - `Barometric Pressure (hPa)` with 15-min rate of drop indicator (`ΔP/Δt`).
  - `Ambient Temperature (°C)`.
  - `Relative Humidity (%)`.
- **Visualization Hub**:
  - Main multi-sensor chart container.
  - Circular Risk Gauge container.
- **Alert Drawer**: Historical log of dispatched warnings.

---

## 4. Typography & Color Tokens
- **Backgrounds**: Slate-900 (`#0f172a`), Slate-800 (`#1e293b`), Slate-950 (`#020617`).
- **Accent**: Cyan-500 (`#06b6d4`), Indigo-500 (`#6366f1`).
- **Severity Colors**:
  - Normal: Emerald-500 (`#10b981`)
  - Elevated Watch: Amber-500 (`#f59e0b`)
  - High Warning: Rose-600 (`#e11d48`)
- **Typography**: Inter / System UI sans-serif for optimal legibility under field operations.
