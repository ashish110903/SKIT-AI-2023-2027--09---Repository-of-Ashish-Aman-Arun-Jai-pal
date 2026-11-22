def rule_based_predict(rain_rate: float, pressure_drop: float, humidity: float) -> str:
    score = 0
    if rain_rate >= 28.0: score += 2
    if pressure_drop >= 5.0: score += 2
    if humidity >= 88.0: score += 1
    if score >= 4: return 'CRITICAL'
    if score == 3: return 'HIGH'
    if score == 2: return 'MODERATE'
    return 'LOW'
