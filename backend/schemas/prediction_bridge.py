def adapt_telemetry_to_ml(records: list) -> list:
    return [{'timestamp': r.get('timestamp', ''), 'rain_mm': r.get('rainfall_mm', 0.0), 'pressure_hpa': r.get('pressure_hpa', 1013.0), 'humidity_pct': r.get('humidity_pct', 70.0)} for r in records]
