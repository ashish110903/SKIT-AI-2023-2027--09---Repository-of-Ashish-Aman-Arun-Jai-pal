from sqlalchemy import Column, String, Float, Boolean
from backend.database import Base

class WeatherStation(Base):
    __tablename__ = 'weather_stations'
    station_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    is_active = Column(Boolean, default=True)
