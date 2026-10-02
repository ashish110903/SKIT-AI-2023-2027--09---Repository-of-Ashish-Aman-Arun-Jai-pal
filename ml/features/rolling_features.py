def compute_rolling_rain(readings: list, window_mins: int = 60) -> float:
    return sum(float(r.get('rain_mm', 0)) for r in readings)
