from datetime import datetime

RAINFALL_ANOMALY_THRESHOLD_MM = 28.0
PRESSURE_DROP_THRESHOLD_HPA = 5.0
HUMIDITY_HIGH_THRESHOLD = 88.0

def compute_rainfall_rate(readings: list) -> float:
    if len(readings) < 2: return 0.0
    t0 = datetime.fromisoformat(readings[0]['timestamp'])
    t1 = datetime.fromisoformat(readings[-1]['timestamp'])
    duration_hr = max((t1 - t0).total_seconds() / 3600.0, 0.001)
    return sum(float(r['rain_mm']) for r in readings) / duration_hr

def detect_pressure_drop(readings: list) -> bool:
    if len(readings) < 2: return False
    pressures = [float(r['pressure_hpa']) for r in readings]
    return (pressures[0] - min(pressures)) >= PRESSURE_DROP_THRESHOLD_HPA

def predict_cloudburst(readings: list) -> dict:
    if not readings:
        return {'risk_level': 'LOW', 'rainfall_rate': 0.0, 'pressure_drop': False, 'alert': 'No data received.'}
    rate = compute_rainfall_rate(readings)
    drop = detect_pressure_drop(readings)
    humidity = float(readings[-1].get('humidity_pct', 0.0))
    score = 0
    if rate >= RAINFALL_ANOMALY_THRESHOLD_MM: score += 2
    if drop: score += 2
    if humidity >= HUMIDITY_HIGH_THRESHOLD: score += 1
    if score >= 4:
        risk, alert = 'CRITICAL', f'CRITICAL: Cloudburst imminent! Rain={rate:.1f}mm/hr'
    elif score == 3:
        risk, alert = 'HIGH', f'HIGH RISK: Heavy downpour. Rain={rate:.1f}mm/hr'
    elif score == 2:
        risk, alert = 'MODERATE', f'MODERATE: Rain={rate:.1f}mm/hr'
    else:
        risk, alert = 'LOW', 'LOW: Conditions normal.'
    return {'risk_level': risk, 'rainfall_rate': round(rate, 2), 'pressure_drop': drop, 'alert': alert}
