from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from backend.database import Base

class HazardAlert(Base):
    __tablename__ = 'hazard_alerts'
    id = Column(Integer, primary_key=True)
    severity = Column(String(20)) # LOW, MODERATE, HIGH, CRITICAL
    rainfall_rate = Column(Float)
    message = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
