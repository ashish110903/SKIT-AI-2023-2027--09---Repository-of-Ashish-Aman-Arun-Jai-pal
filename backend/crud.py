"""
Cloudburst Early Warning & Alarm System - CRUD Database Repositories
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from sqlalchemy.orm import Session
from datetime import datetime
from backend.models import SensorReading, Station, AlertRecord
from backend.schemas import SensorTelemetryCreate

def create_sensor_reading(db: Session, data: SensorTelemetryCreate) -> SensorReading:
    """Inserts a new sensor telemetry reading into the database."""
    # Ensure station exists
    station = db.query(Station).filter(Station.id == data.station_id).first()
    if not station:
        station = Station(
            id=data.station_id,
            name=f"Station-{data.station_id}",
            altitude_m=2000.0,
            latitude=30.45,
            longitude=78.06
        )
        db.add(station)
        db.commit()

    reading = SensorReading(
        station_id=data.station_id,
        rainfall_rate=data.rainfall_rate,
        rain_accum_1h=data.rain_accum_1h or 0.0,
        pressure=data.pressure,
        pressure_drop_rate=data.pressure_drop_rate or 0.0,
        temperature=data.temperature,
        dew_point=data.dew_point or (data.temperature - 2.5),
        humidity=data.humidity,
        battery_pct=data.battery_pct or 95,
        signal_rssi=data.signal_rssi or -75,
        recorded_at=datetime.utcnow()
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

def get_latest_reading(db: Session, station_id: str) -> SensorReading:
    """Retrieves the most recent sensor measurement for a given station."""
    return db.query(SensorReading)\
             .filter(SensorReading.station_id == station_id)\
             .order_by(SensorReading.recorded_at.desc())\
             .first()

def get_historical_readings(db: Session, station_id: str, limit: int = 12):
    """Retrieves rolling history buffer of sensor measurements."""
    return db.query(SensorReading)\
             .filter(SensorReading.station_id == station_id)\
             .order_by(SensorReading.recorded_at.desc())\
             .limit(limit)\
             .all()

def create_alert_record(db: Session, station_id: str, severity: str, desc: str, prob: float = 0.0) -> AlertRecord:
    """Records an automated hazard alert in database."""
    alert = AlertRecord(
        station_id=station_id,
        severity=severity,
        description=desc,
        probability=prob,
        acknowledged=False,
        created_at=datetime.utcnow()
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def get_active_alerts(db: Session):
    """Retrieves all unacknowledged active alerts."""
    return db.query(AlertRecord)\
             .filter(AlertRecord.acknowledged == False)\
             .order_by(AlertRecord.created_at.desc())\
             .all()
