from pydantic import BaseModel
from typing import List

class ReadingItem(BaseModel):
    timestamp: str
    rain_mm: float
    pressure_hpa: float
    humidity_pct: float
