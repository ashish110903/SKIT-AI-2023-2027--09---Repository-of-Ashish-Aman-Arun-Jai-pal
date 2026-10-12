from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from backend.database import Base

class TelemetryRecord(Base):
    __tablename__ = 'telemetry_records'
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String(50), index=True)
    rainfall_mm = Column(Float)
    pressure_hpa = Column(Float)
    temperature_c = Column(Float)
    humidity_pct = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
