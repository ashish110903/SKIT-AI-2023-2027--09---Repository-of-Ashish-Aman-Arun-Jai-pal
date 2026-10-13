from sqlalchemy.orm import Session
from backend.models import TelemetryRecord

def create_telemetry_record(db: Session, station_id: str, rain: float, pres: float, temp: float, hum: float):
    record = TelemetryRecord(station_id=station_id, rainfall_mm=rain, pressure_hpa=pres, temperature_c=temp, humidity_pct=hum)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
