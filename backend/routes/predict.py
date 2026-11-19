"""
Cloudburst Early Warning & Alarm System - AI/ML Prediction Router
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.ml_service import ml_service
from backend import crud

router = APIRouter(prefix="/predict", tags=["AI/ML Prediction"])

@router.get("/status", response_model=dict)
def get_prediction_status(
    station_id: str = Query("STN-01", description="Station Identifier"),
    db: Session = Depends(get_db)
):
    """
    Feeds live telemetry from DB into the ML inference pipeline 
    and returns real-time cloudburst risk probability for the Frontend Risk Gauge.
    """
    latest = crud.get_latest_reading(db, station_id)
    if latest:
        return ml_service.predict_risk(
            rain_rate=latest.rainfall_rate,
            pressure_drop=latest.pressure_drop_rate,
            temp=latest.temperature,
            humidity=latest.humidity
        )
    
    # Default baseline nominal prediction
    return ml_service.predict_risk(
        rain_rate=0.5,
        pressure_drop=-0.1,
        temp=21.0,
        humidity=68.0
    )
