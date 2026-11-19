# Sprint 6: AI/ML Model Backend Integration

**Member:** Ashish Sharma (Backend Lead & Team Lead)  
**Dates:** 26/12/2026 – 20/01/2027  
**User Story:** "We will integrate the backend with the ML model"  
**Details of Task:** "We will connect the prediction output with the backend system."  

---

## Deliverables & Inference Architecture

1. **ML Scoring Adapter (`services/ml_service.py`)**:
   - Ingests streaming telemetry attributes: rainfall rate, barometric pressure gradient, temperature, relative humidity.
   - Computes real-time non-linear logit probability score ($P \in [0.0\%, 100.0\%]$).
   - Classifies risk level into standard operational tiers (`NORMAL`, `WATCH`, `WARNING`).

2. **Prediction Status API (`routes/predict.py`)**:
   - `GET /api/v1/predict/status?station_id={id}`
   - Consumed directly by Jai Pal's frontend dashboard (`risk_gauge.js`) to drive the circular SVG risk needle and anomaly checklist.
