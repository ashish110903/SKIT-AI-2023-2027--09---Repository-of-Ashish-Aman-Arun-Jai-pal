# Sprint 4: Emergency Warning & Alarm UI System

**Member:** Jai Pal (Frontend)  
**Dates:** 25/11/2026 – 20/12/2026  
**User Story:** "We will display warning notification"  
**Details of Task:** "We will create interface for showing emergency"  

---

## Objectives & Deliverables
1. **Critical Emergency Warning Modal**:
   - Full-screen high-priority alert pop-up triggered when cloudburst probability reaches emergency thresholds.
   - Highlights node location, trigger timestamp, and recommended standard operating procedures (SOP).
2. **Persistent Sticky Warning Banner**:
   - Red alert banner displaying current station advisory and silence controls.
3. **Web Audio API Emergency Siren Synthesizer**:
   - Fully zero-dependency client-side alarm synthesizer (`AudioContext` + `OscillatorNode`) producing a two-tone emergency siren.
   - Operates completely offline without requiring audio files or external CDNs.
4. **Early Warning Log Table**:
   - Historical drawer recording timestamped warning alerts, operator acknowledgements, and advisory status.
