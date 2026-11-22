def determine_alert_stage(risk_level: str) -> str:
    stages = {'LOW': 'NO_ALERT', 'MODERATE': 'ADVISORY', 'HIGH': 'WATCH', 'CRITICAL': 'WARNING'}
    return stages.get(risk_level, 'NO_ALERT')
