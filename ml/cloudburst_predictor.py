"""
ml/cloudburst_predictor.py
Aman Sharma - AI/ML | SKIT/AI/2023-2027/09
Sprint 4: Prediction & Detection - Updated with tuned thresholds

Rainfall anomaly detection model using sensor data.
Thresholds tuned via model_trainer.py grid search.
"""
import numpy as np
from datetime import datetime

RAINFALL_ANOMALY_THRESHOLD_MM = 28.0
PRESSURE_DROP_THRESHOLD_HPA   = 5.0
HUMIDITY_HIGH_THRESHOLD        = 88.0

def compute_rainfall_rate(readings: list[dict]) -> float:
    if len(readings) < 2:
        return 0.0
    t0 = datetime.fromisoformat(readings[0]["timestamp"])
    t1 = datetime.fromisoformat(readings[-1]["timestamp"])
    duration_hr = (t1 - t0).total_seconds() / 3600.0
    if duration_hr == 0:
        return 0.0
    return sum(r["rain_mm"] for r in readings) / duration_hr

def detect_pressure_drop(readings: list[dict]) -> bool:
    if len(readings) < 2:
        return False
    pressures = [r["pressure_hpa"] for r in readings]
    return (pressures[0] - min(pressures)) >= PRESSURE_DROP_THRESHOLD_HPA

def predict_cloudburst(sensor_readings: list[dict]) -> dict:
    if not sensor_readings:
        return {"risk_level": "LOW", "rainfall_rate": 0.0, "pressure_drop": False, "alert": "No data received."}
    rainfall_rate = compute_rainfall_rate(sensor_readings)
    pressure_drop = detect_pressure_drop(sensor_readings)
    humidity = sensor_readings[-1].get("humidity_pct", 0.0)
    score = 0
    if rainfall_rate >= RAINFALL_ANOMALY_THRESHOLD_MM: score += 2
    if pressure_drop:                                  score += 2
    if humidity >= HUMIDITY_HIGH_THRESHOLD:            score += 1
    if score >= 4:   risk_level, alert = "CRITICAL", f"CRITICAL: Cloudburst imminent! Rain={rainfall_rate:.1f}mm/hr, PressureDrop={pressure_drop}, Humidity={humidity:.0f}%"
    elif score == 3: risk_level, alert = "HIGH",     f"HIGH RISK: Dangerous conditions. Rain={rainfall_rate:.1f}mm/hr"
    elif score == 2: risk_level, alert = "MODERATE", f"MODERATE: Monitor closely. Rain={rainfall_rate:.1f}mm/hr"
    else:            risk_level, alert = "LOW",      "LOW: Conditions normal."
    return {"risk_level": risk_level, "rainfall_rate": round(rainfall_rate, 2), "pressure_drop": pressure_drop, "alert": alert}

if __name__ == "__main__":
    sample = [
        {"timestamp": "2026-11-01T14:00:00", "rain_mm": 0.0,  "pressure_hpa": 1012.0, "humidity_pct": 70.0},
        {"timestamp": "2026-11-01T14:10:00", "rain_mm": 5.0,  "pressure_hpa": 1009.0, "humidity_pct": 82.0},
        {"timestamp": "2026-11-01T14:20:00", "rain_mm": 12.0, "pressure_hpa": 1006.5, "humidity_pct": 91.0},
        {"timestamp": "2026-11-01T14:30:00", "rain_mm": 18.0, "pressure_hpa": 1004.0, "humidity_pct": 95.0},
    ]
    result = predict_cloudburst(sample)
    print("=== Cloudburst Prediction ===")
    for k, v in result.items():
        print(f"  {k}: {v}")