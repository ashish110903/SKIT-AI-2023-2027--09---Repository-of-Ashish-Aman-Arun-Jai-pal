def calculate_pressure_drop(pressures: list) -> float:
    if not pressures: return 0.0
    return pressures[0] - min(pressures)
