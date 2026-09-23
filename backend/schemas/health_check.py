from pydantic import BaseModel

class SystemHealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    active_stations: int
    queue_backlog: int
