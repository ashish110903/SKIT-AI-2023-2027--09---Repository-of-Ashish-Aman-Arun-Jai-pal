"""
ml/feature_engineering.py
Aman Sharma - AI/ML | SKIT/AI/2023-2027/09
Sprint 3: Feature Engineering for Cloudburst Prediction Model
"""
from datetime import datetime

def compute_features(readings: list[dict]) -> dict:
    """
    Derive ML features from raw sensor readings.

    Input fields per reading:
        timestamp    - ISO 8601 string
        rain_mm      - rainfall accumulation
        pressure_hpa - atmospheric pressure
        humidity_pct - relative humidity

    Returns a feature dict ready for model input.
    """
    if not readings:
        return {}

    rain_values     = [r["rain_mm"]      for r in readings]
    pressure_values = [r["pressure_hpa"] for r in readings]
    humidity_values = [r["humidity_pct"] for r in readings]

    n = len(readings)

    # Rolling rainfall statistics
    rain_mean  = sum(rain_values) / n
    rain_max   = max(rain_values)
    rain_std   = (sum((x - rain_mean)**2 for x in rain_values) / n) ** 0.5

    # Pressure trend (drop = negative = danger)
    pressure_trend = pressure_values[-1] - pressure_values[0]
    pressure_min   = min(pressure_values)

    # Humidity spike
    humidity_max  = max(humidity_values)
    humidity_mean = sum(humidity_values) / n

    # Time window duration in hours
    t0 = datetime.fromisoformat(readings[0]["timestamp"])
    t1 = datetime.fromisoformat(readings[-1]["timestamp"])
    duration_hr = max((t1 - t0).total_seconds() / 3600.0, 0.001)

    # Rainfall rate (mm/hr)
    rainfall_rate = sum(rain_values) / duration_hr

    # Composite risk index (heuristic, later replaced by trained model)
    risk_index = (
        min(rainfall_rate / 30.0, 1.0) * 0.4 +
        min(abs(min(pressure_trend, 0)) / 10.0, 1.0) * 0.4 +
        min(humidity_max / 100.0, 1.0) * 0.2
    )

    return {
        "rain_mean_mm"    : round(rain_mean, 3),
        "rain_max_mm"     : round(rain_max, 3),
        "rain_std_mm"     : round(rain_std, 3),
        "rainfall_rate"   : round(rainfall_rate, 3),
        "pressure_trend"  : round(pressure_trend, 3),
        "pressure_min_hpa": round(pressure_min, 3),
        "humidity_max_pct": round(humidity_max, 3),
        "humidity_mean_pct": round(humidity_mean, 3),
        "duration_hr"     : round(duration_hr, 3),
        "risk_index"      : round(risk_index, 4),
    }

if __name__ == "__main__":
    sample = [
        {"timestamp": "2026-11-01T08:00:00", "rain_mm": 1.0,  "pressure_hpa": 1012.0, "humidity_pct": 70},
        {"timestamp": "2026-11-01T08:10:00", "rain_mm": 4.0,  "pressure_hpa": 1008.5, "humidity_pct": 83},
        {"timestamp": "2026-11-01T08:20:00", "rain_mm": 11.0, "pressure_hpa": 1004.0, "humidity_pct": 92},
        {"timestamp": "2026-11-01T08:30:00", "rain_mm": 22.0, "pressure_hpa": 1000.5, "humidity_pct": 97},
    ]
    features = compute_features(sample)
    print("=== Extracted Features ===")
    for k, v in features.items():
        print(f"  {k:25s}: {v}")