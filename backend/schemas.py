"""
Cloudburst Early Warning & Alarm System - Pydantic Validation Schemas
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SensorTelemetryCreate(BaseModel):
    station_id: str = Field(..., example="STN-01")
    rainfall_rate: float = Field(..., ge=0.0, description="Rainfall intensity in mm/hr", example=12.4)
    rain_accum_1h: Optional[float] = Field(0.0, ge=0.0, description="1-hour accumulated rain in mm", example=6.8)
    pressure: float = Field(..., ge=800.0, le=1100.0, description="Atmospheric pressure in hPa", example=1011.5)
    pressure_drop_rate: Optional[float] = Field(0.0, description="15-min drop rate in hPa/hr", example=-1.2)
    temperature: float = Field(..., ge=-20.0, le=55.0, description="Ambient temperature in °C", example=19.4)
    dew_point: Optional[float] = Field(None, description="Dew point in °C", example=17.2)
    humidity: float = Field(..., ge=0.0, le=100.0, description="Relative humidity in %", example=85.0)
    battery_pct: Optional[int] = Field(95, ge=0, le=100, example=94)
    signal_rssi: Optional[int] = Field(-75, example=-76)

class SensorTelemetryResponse(SensorTelemetryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ActiveAlertResponse(BaseModel):
    id: int
    station_id: str
    level: str
    description: str
    created_at: datetime
    is_active: bool

class PredictionResponse(BaseModel):
    station_id: str
    probability: float
    risk_level: str
    factors: dict
