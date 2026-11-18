"""
ml/tests/test_predictor.py
Aman Sharma - AI/ML | SKIT/AI/2023-2027/09
Sprint 4: Unit tests for cloudburst_predictor.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from ml.cloudburst_predictor import compute_rainfall_rate, detect_pressure_drop, predict_cloudburst

def make_readings(rain_values, pressure_values, humidity_last=70.0):
    base_time = "2026-11-01T10:{}:00"
    return [
        {"timestamp": base_time.format(str(i*10).zfill(2)),
         "rain_mm": rain_values[i],
         "pressure_hpa": pressure_values[i],
         "humidity_pct": humidity_last}
        for i in range(len(rain_values))
    ]

def test_low_risk():
    readings = make_readings([0, 1, 2], [1013, 1012, 1012], 60)
    result = predict_cloudburst(readings)
    assert result["risk_level"] == "LOW", f"Expected LOW, got {result['risk_level']}"
    print("PASS: test_low_risk")

def test_critical_risk():
    readings = make_readings([0, 10, 25, 40], [1012, 1007, 1003, 998], 96)
    result = predict_cloudburst(readings)
    assert result["risk_level"] in ("HIGH", "CRITICAL"), f"Expected HIGH/CRITICAL, got {result['risk_level']}"
    print("PASS: test_critical_risk")

def test_empty_input():
    result = predict_cloudburst([])
    assert result["risk_level"] == "LOW"
    print("PASS: test_empty_input")

def test_pressure_drop_detected():
    readings = make_readings([0, 0, 1], [1013, 1007, 1006], 65)
    assert detect_pressure_drop(readings) == True
    print("PASS: test_pressure_drop_detected")

if __name__ == "__main__":
    test_low_risk()
    test_critical_risk()
    test_empty_input()
    test_pressure_drop_detected()
    print("\nAll tests passed.")