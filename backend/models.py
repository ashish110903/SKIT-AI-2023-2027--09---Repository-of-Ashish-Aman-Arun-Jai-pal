"""
Cloudburst Early Warning & Alarm System - SQLAlchemy Database Models
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    altitude_m = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    readings = relationship("SensorReading", back_populates="station")
    alerts = relationship("AlertRecord", back_populates="station")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(String(32), ForeignKey("stations.id"), index=True)
    rainfall_rate = Column(Float, nullable=False)
    rain_accum_1h = Column(Float, default=0.0)
    pressure = Column(Float, nullable=False)
    pressure_drop_rate = Column(Float, default=0.0)
    temperature = Column(Float, nullable=False)
    dew_point = Column(Float, nullable=True)
    humidity = Column(Float, nullable=False)
    battery_pct = Column(Integer, default=100)
    signal_rssi = Column(Integer, default=-75)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)

    station = relationship("Station", back_populates="readings")

class AlertRecord(Base):
    __tablename__ = "alert_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_id = Column(String(32), ForeignKey("stations.id"), index=True)
    severity = Column(String(32), nullable=False) # WATCH, WARNING, CRITICAL
    description = Column(String(512), nullable=False)
    probability = Column(Float, default=0.0)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    station = relationship("Station", back_populates="alerts")
