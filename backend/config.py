"""
Cloudburst Early Warning & Alarm System - Configuration
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Cloudburst Early Warning & Alarm System"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cloudburst.db")
    
    # Mountain Meteorological Hazard Thresholds
    RAIN_RATE_WATCH_THRESHOLD: float = 20.0       # mm/hr
    RAIN_RATE_WARNING_THRESHOLD: float = 50.0     # mm/hr
    PRESSURE_DROP_WATCH_THRESHOLD: float = -2.0   # hPa/hr
    PRESSURE_DROP_WARNING_THRESHOLD: float = -3.5 # hPa/hr
    HUMIDITY_SATURATION_THRESHOLD: float = 90.0   # %
    
    # Pre-configured Mountain Sensor Nodes
    MONITORED_STATIONS: dict = {
        "STN-01": {"name": "Mussoorie Ridge", "altitude_m": 2005, "lat": 30.4598, "lon": 78.0644},
        "STN-02": {"name": "Kedarnath Valley", "altitude_m": 3583, "lat": 30.7346, "lon": 79.0669},
        "STN-03": {"name": "Shimla Peak", "altitude_m": 2276, "lat": 31.1048, "lon": 77.1734},
        "STN-04": {"name": "Nainital Slopes", "altitude_m": 2084, "lat": 29.3919, "lon": 79.4542}
    }

settings = Settings()
