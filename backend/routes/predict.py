from fastapi import APIRouter
from backend.services.ml_client import ml_client

router = APIRouter(prefix='/api/predict', tags=['Prediction'])

@router.post('')
async def trigger_prediction(readings: list):
    return await ml_client.predict_risk(readings)
