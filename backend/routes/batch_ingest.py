from fastapi import APIRouter
router = APIRouter(prefix='/api/telemetry/batch', tags=['Telemetry'])
@router.post('')
def ingest_batch(packets: list):
    return {'status': 'success', 'accepted_count': len(packets)}
