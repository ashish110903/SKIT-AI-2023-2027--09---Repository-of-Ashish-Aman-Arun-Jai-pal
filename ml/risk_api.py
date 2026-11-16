"""
ml/risk_api.py
Aman Sharma - AI/ML | SKIT/AI/2023-2027/09
Sprint 4: REST API wrapper for cloudburst risk prediction

Exposes predict_cloudburst() as a FastAPI endpoint
so the backend and frontend can query it in real-time.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from ml.cloudburst_predictor import predict_cloudburst

app = FastAPI(title="CloudBurst Risk API", version="1.0")

class SensorReading(BaseModel):
    timestamp:    str
    rain_mm:      float
    pressure_hpa: float
    humidity_pct: float

class PredictionResponse(BaseModel):
    risk_level:    str
    rainfall_rate: float
    pressure_drop: bool
    alert:         str

@app.post("/predict", response_model=PredictionResponse, tags=["prediction"])
def predict(readings: List[SensorReading]):
    """
    Accept a list of sensor readings and return a cloudburst risk prediction.
    """
    if not readings:
        raise HTTPException(status_code=400, detail="No sensor readings provided.")
    payload = [r.dict() for r in readings]
    result  = predict_cloudburst(payload)
    return PredictionResponse(**result)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "model": "cloudburst_predictor_v1"}