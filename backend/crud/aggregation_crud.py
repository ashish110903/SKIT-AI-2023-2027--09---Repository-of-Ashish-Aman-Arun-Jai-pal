from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import TelemetryRecord

def get_hourly_rainfall(db: Session, station_id: str):
    return db.query(func.sum(TelemetryRecord.rainfall_mm)).filter(TelemetryRecord.station_id == station_id).scalar() or 0.0
