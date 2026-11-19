"""
Cloudburst Early Warning & Alarm System - Hazard Detection & Alert Service
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from typing import Optional, Dict
from sqlalchemy.orm import Session
from backend.config import settings
from backend import crud

class AlertService:
    @staticmethod
    def evaluate_reading(db: Session, station_id: str, rain_rate: float, pressure_drop: float, humidity: float) -> Optional[Dict]:
        """
        Evaluates real-time sensor metrics against cloudburst precursor thresholds.
        Dispatches emergency alert if thresholds are breached.
        """
        # Critical Cloudburst Warning condition:
        # Torrential rain (>50 mm/h) AND rapid pressure plunge (<-3.5 hPa/h)
        if rain_rate >= settings.RAIN_RATE_WARNING_THRESHOLD and pressure_drop <= settings.PRESSURE_DROP_WARNING_THRESHOLD:
            desc = (
                f"CRITICAL WARNING: Cloudburst conditions at {station_id}. "
                f"Torrential rain ({rain_rate} mm/h) and rapid barometric plunge ({pressure_drop} hPa/h). "
                f"Immediate flash flood evacuation advisory!"
            )
            alert = crud.create_alert_record(db, station_id, "WARNING", desc, prob=94.5)
            return {
                "id": alert.id,
                "stationId": station_id,
                "level": "WARNING",
                "desc": desc,
                "probability": 94.5
            }
        
        # Elevated Watch condition:
        elif rain_rate >= settings.RAIN_RATE_WATCH_THRESHOLD or pressure_drop <= settings.PRESSURE_DROP_WATCH_THRESHOLD:
            desc = (
                f"ELEVATED WATCH: Rapid convective cloud buildup at {station_id}. "
                f"Rain rate: {rain_rate} mm/h, Pressure drop: {pressure_drop} hPa/h."
            )
            alert = crud.create_alert_record(db, station_id, "WATCH", desc, prob=52.0)
            return {
                "id": alert.id,
                "stationId": station_id,
                "level": "WATCH",
                "desc": desc,
                "probability": 52.0
            }
        
        return None

alert_service = AlertService()
