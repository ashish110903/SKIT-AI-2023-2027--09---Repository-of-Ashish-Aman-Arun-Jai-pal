"""
Cloudburst Early Warning & Alarm System - Sensor Ingestion API Router
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from backend.schemas import SensorTelemetryCreate, SensorTelemetryResponse

router = APIRouter(prefix="/sensors", tags=["Sensors Telemetry"])

# In-memory buffer for fast prototyping and edge caching
telemetry_buffer = {}

@router.post("/telemetry", response_model=dict, status_code=201)
def ingest_telemetry(payload: SensorTelemetryCreate):
    """
    Ingests environmental sensor packet from LoRa / Hardware Gateway.
    Validates metrics and stages for database persistence and hazard check.
    """
    record = payload.model_dump()
    record["id"] = len(telemetry_buffer.get(payload.station_id, [])) + 1
    record["created_at"] = datetime.utcnow()
    
    if payload.station_id not in telemetry_buffer:
        telemetry_buffer[payload.station_id] = []
    
    telemetry_buffer[payload.station_id].append(record)
    
    return {
        "status": "success",
        "message": f"Telemetry processed for {payload.station_id}",
        "record_id": record["id"],
        "timestamp": record["created_at"].isoformat()
    }

@router.get("/latest", response_model=dict)
def get_latest_telemetry(station_id: str = Query("STN-01", description="Station Identifier")):
    """
    Returns latest telemetry readings for the frontend dashboard cards.
    """
    station_records = telemetry_buffer.get(station_id, [])
    if station_records:
        latest = station_records[-1]
        return {
            "stationId": latest["station_id"],
            "rainfallRate": latest["rainfall_rate"],
            "rainAccum1h": latest.get("rain_accum_1h", latest["rainfall_rate"] * 0.7),
            "pressure": latest["pressure"],
            "pressureDropRate": latest.get("pressure_drop_rate", -0.2),
            "temperature": latest["temperature"],
            "dewPoint": latest.get("dew_point", latest["temperature"] - 2.5),
            "humidity": latest["humidity"],
            "battery": f"{latest.get('battery_pct', 92)}%",
            "signal": f"{latest.get('signal_rssi', -75)} dBm"
        }
    
    # Baseline nominal fallback if no packet received yet
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
    limit: int = Query(12, ge=1, le=100)
):
    """
    Returns rolling historical readings for Chart.js telemetry trends.
    """
    records = telemetry_buffer.get(station_id, [])
    return records[-limit:] if records else []
