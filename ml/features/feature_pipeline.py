from ml.features.rolling_features import compute_rolling_rain
from ml.features.pressure_gradient import compute_dp_dt

def extract_features(readings: list) -> dict:
    if not readings: return {}
    rain_sum = compute_rolling_rain(readings)
    return {'rain_sum': rain_sum, 'reading_count': len(readings)}
