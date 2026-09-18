from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SensorTelemetrySchema(BaseModel):
    station_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    rainfall_mm: float = Field(ge=0.0)
    pressure_hpa: float = Field(ge=800.0, le=1100.0)
    temperature_c: float
    humidity_pct: float = Field(ge=0.0, le=100.0)
