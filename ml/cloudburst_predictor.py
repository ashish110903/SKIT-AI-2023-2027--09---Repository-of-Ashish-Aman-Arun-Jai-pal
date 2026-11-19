"""
ml/cloudburst_predictor.py
Aman Sharma - AI/ML: Cloud Burst Early Warning System
SKIT/AI/2023-2027/09

Rainfall anomaly detection model using sensor data.
Sprint 4: Prediction & Detection
"""

import numpy as np
from datetime import datetime


# --- Thresholds (tunable) ---
RAINFALL_ANOMALY_THRESHOLD_MM = 30.0   # mm/hr considered anomalous
PRESSURE_DROP_THRESHOLD_HPA   = 5.0    # hPa sudden drop (danger sign)
HUMIDITY_HIGH_THRESHOLD        = 90.0  # % relative humidity


def compute_rainfall_rate(readings: list[dict]) -> float:
    """
    Compute average rainfall rate (mm/hr) from a list of sensor readings.

    Args:
        readings: List of dicts with keys 'timestamp' (ISO str) and 'rain_mm'.
    Returns:
        Rainfall rate in mm/hr.
    """
    if len(readings) < 2:
        return 0.0

    t0 = datetime.fromisoformat(readings[0]["timestamp"])
    t1 = datetime.fromisoformat(readings[-1]["timestamp"])
    duration_hr = (t1 - t0).total_seconds() / 3600.0

    if duration_hr == 0:
        return 0.0

    total_rain = sum(r["rain_mm"] for r in readings)
    return total_rain / duration_hr


def detect_pressure_drop(readings: list[dict]) -> bool:
    """
    Detect a sudden drop in atmospheric pressure (early storm indicator).

    Args:
        readings: List of dicts with keys 'timestamp' and 'pressure_hpa'.
    Returns:
        True if a dangerous pressure drop is detected.
    """
    if len(readings) < 2:
        return False

    pressures = [r["pressure_hpa"] for r in readings]
    drop = pressures[0] - min(pressures)
    return drop >= PRESSURE_DROP_THRESHOLD_HPA


def predict_cloudburst(sensor_readings: list[dict]) -> dict:
    """
    Main prediction function for cloudburst risk.

    Args:
        sensor_readings: List of dicts with sensor data:
            - timestamp    : ISO 8601 string
            - rain_mm      : accumulated rainfall (mm)
            - pressure_hpa : atmospheric pressure (hPa)
            - humidity_pct : relative humidity (%)

    Returns:
        dict with:
            - risk_level   : "LOW" | "MODERATE" | "HIGH" | "CRITICAL"
            - rainfall_rate: computed mm/hr
            - pressure_drop: bool
            - alert        : human-readable alert message
    """
    if not sensor_readings:
        return {"risk_level": "LOW", "rainfall_rate": 0.0,
                "pressure_drop": False, "alert": "No data received."}

    rainfall_rate = compute_rainfall_rate(sensor_readings)
    pressure_drop = detect_pressure_drop(sensor_readings)
    latest = sensor_readings[-1]
    humidity = latest.get("humidity_pct", 0.0)

    # Scoring: accumulate risk points
    score = 0
    if rainfall_rate >= RAINFALL_ANOMALY_THRESHOLD_MM:
        score += 2
    if pressure_drop:
        score += 2
    if humidity >= HUMIDITY_HIGH_THRESHOLD:
        score += 1

    if score >= 4:
        risk_level = "CRITICAL"
        alert = (f"CRITICAL: Cloudburst imminent! "
                 f"Rainfall={rainfall_rate:.1f} mm/hr, "
                 f"Pressure drop={pressure_drop}, "
                 f"Humidity={humidity:.0f}%")
    elif score == 3:
        risk_level = "HIGH"
        alert = (f"HIGH RISK: Dangerous conditions detected. "
                 f"Rainfall={rainfall_rate:.1f} mm/hr")
    elif score == 2:
        risk_level = "MODERATE"
        alert = (f"MODERATE: Monitor closely. "
                 f"Rainfall={rainfall_rate:.1f} mm/hr")
    else:
        risk_level = "LOW"
        alert = "LOW: Conditions normal."

    return {
        "risk_level": risk_level,
        "rainfall_rate": round(rainfall_rate, 2),
        "pressure_drop": pressure_drop,
        "alert": alert,
    }


# --- Quick test ---
if __name__ == "__main__":
    sample_readings = [
        {"timestamp": "2026-09-15T14:00:00", "rain_mm": 0.0,  "pressure_hpa": 1012.0, "humidity_pct": 70.0},
        {"timestamp": "2026-09-15T14:10:00", "rain_mm": 5.0,  "pressure_hpa": 1009.0, "humidity_pct": 82.0},
        {"timestamp": "2026-09-15T14:20:00", "rain_mm": 12.0, "pressure_hpa": 1006.5, "humidity_pct": 91.0},
        {"timestamp": "2026-09-15T14:30:00", "rain_mm": 18.0, "pressure_hpa": 1004.0, "humidity_pct": 95.0},
    ]

    result = predict_cloudburst(sample_readings)
    print("=== Cloudburst Prediction Result ===")
    for k, v in result.items():
        print(f"  {k}: {v}")