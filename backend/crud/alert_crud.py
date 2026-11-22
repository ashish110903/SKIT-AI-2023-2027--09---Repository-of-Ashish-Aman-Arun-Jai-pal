from sqlalchemy.orm import Session
from backend.models.alert import HazardAlert

def create_alert(db: Session, severity: str, rain_rate: float, msg: str):
    alert = HazardAlert(severity=severity, rainfall_rate=rain_rate, message=msg)
    db.add(alert)
    db.commit()
    return alert
