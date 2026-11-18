from fastapi import APIRouter
router = APIRouter(prefix='/api/stats', tags=['Stats'])
@router.get('')
def get_stats():
    return {'telemetry_ingested': 14850, 'active_nodes': 4, 'alerts_triggered': 1}
