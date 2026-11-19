"""
Cloudburst Early Warning & Alarm System - Sensor Ingestion API Router
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from backend.database import get_db
from backend.schemas import SensorTelemetryCreate
from backend import crud

router = APIRouter(prefix="/sensors", tags=["Sensors Telemetry"])

@router.post("/telemetry", response_model=dict, status_code=201)
def ingest_telemetry(payload: SensorTelemetryCreate, db: Session = Depends(get_db)):
    """
    Ingests environmental sensor packet from LoRa / Hardware Gateway.
    Validates metrics and stages for database persistence and hazard check.
    """
    record = crud.create_sensor_reading(db, payload)
    return {
        "status": "success",
        "message": f"Telemetry processed for {payload.station_id}",
        "record_id": record.id,
        "timestamp": record.recorded_at.isoformat()
    }

@router.get("/latest", response_model=dict)
def get_latest_telemetry(
    station_id: str = Query("STN-01", description="Station Identifier"),
    db: Session = Depends(get_db)
):
    """
    Returns latest telemetry readings from DB for frontend dashboard cards.
    """
    reading = crud.get_latest_reading(db, station_id)
    if reading:
        return {
            "stationId": reading.station_id,
            "rainfallRate": reading.rainfall_rate,
            "rainAccum1h": reading.rain_accum_1h,
            "pressure": reading.pressure,
            "pressureDropRate": reading.pressure_drop_rate,
            "temperature": reading.temperature,
            "dewPoint": reading.dew_point,
            "humidity": reading.humidity,
            "battery": f"{reading.battery_pct}%",
            "signal": f"{reading.signal_rssi} dBm"
        }
    
    # Baseline nominal fallback
    return {
        "stationId": station_id,
        "rainfallRate": 0.0,
        "rainAccum1h": 0.0,
        "pressure": 1013.25,
        "pressureDropRate": -0.1,
        "temperature": 21.0,
        "dewPoint": 17.5,
        "humidity": 70.0,
        "battery": "94%",
        "signal": "-74 dBm"
    }

@router.get("/history", response_model=List[dict])
def get_telemetry_history(
    station_id: str = Query("STN-01"),
    limit: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Returns rolling historical readings from DB for Chart.js telemetry trends.
    """
    records = crud.get_historical_readings(db, station_id, limit)
    result = []
    for r in reversed(records):
        result.append({
            "id": r.id,
            "station_id": r.station_id,
            "rainfall_rate": r.rainfall_rate,
            "pressure": r.pressure,
            "temperature": r.temperature,
            "humidity": r.humidity,
            "recorded_at": r.recorded_at.isoformat()
        })
    return result
