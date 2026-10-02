from fastapi import APIRouter, HTTPException
from backend.schemas import SensorTelemetrySchema

router = APIRouter(prefix='/api/telemetry', tags=['Sensors'])

@router.post('/ingest')
def ingest_telemetry(data: SensorTelemetrySchema):
    return {'status': 'accepted', 'station_id': data.station_id}
