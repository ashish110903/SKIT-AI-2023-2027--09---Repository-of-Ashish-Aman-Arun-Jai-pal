from pydantic import BaseModel
from enum import Enum

class AlertSeverity(str, Enum):
    LOW = 'LOW'
    MODERATE = 'MODERATE'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

class AlertCreate(BaseModel):
    severity: AlertSeverity
    rainfall_rate: float
    message: str
