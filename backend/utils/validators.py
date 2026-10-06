def validate_sensor_reading(rain: float, pressure: float, temp: float, hum: float) -> bool:
    if rain < 0.0 or rain > 300.0: return False
    if pressure < 850.0 or pressure > 1080.0: return False
    if hum < 0.0 or hum > 100.0: return False
    return True
