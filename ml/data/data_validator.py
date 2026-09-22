def check_record_integrity(row: dict) -> bool:
    try:
        rain = float(row['rain_mm'])
        pres = float(row['pressure_hpa'])
        return rain >= 0.0 and 800.0 <= pres <= 1100.0
    except Exception:
        return False
