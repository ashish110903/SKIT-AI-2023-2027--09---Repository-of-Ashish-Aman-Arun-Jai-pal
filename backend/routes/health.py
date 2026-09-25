from fastapi import APIRouter
from backend.schemas.health_check import SystemHealthResponse

router = APIRouter(prefix='/api/health', tags=['Health'])

@router.get('', response_model=SystemHealthResponse)
def get_health():
    return SystemHealthResponse(status='healthy', uptime_seconds=1200.0, active_stations=4, queue_backlog=0)
