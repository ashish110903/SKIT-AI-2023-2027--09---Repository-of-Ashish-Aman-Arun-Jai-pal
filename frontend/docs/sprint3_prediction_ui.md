# Sprint 3: AI/ML Prediction & Risk Assessment Display

**Member:** Jai Pal (Frontend)  
**Dates:** 01/11/2026 – 25/11/2026  
**User Story:** "We will display the prediction result"  
**Details of Task:** "We will show the detected risk on the dashboard"  

---

## Objectives & Deliverables
1. **SVG Radial Risk Gauge**:
   - Engineered an animated circular gauge utilizing stroke-dasharray calculations to represent cloudburst risk percentage from `0.0%` to `100.0%`.
2. **Dynamic Risk Tier Badges**:
   - Level 0: Green (`NORMAL`, probability `< 35%`)
   - Level 1: Amber (`ELEVATED WATCH`, probability `35% – 74.9%`)
   - Level 2: Red (`CLOUDBURST WARNING`, probability `≥ 75%`, with animated pulse ring)
3. **Precursor Atmospheric Anomaly Checklist**:
   - Real-time indicator for pressure gradient drop rate (`ΔP/15m`), rainfall intensity acceleration, and vapor saturation.
