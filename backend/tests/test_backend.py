"""
Cloudburst Early Warning & Alarm System - Complete Backend Integration Test Suite
Sprint 7: Test the complete backend (hardware -> backend -> DB -> ML -> frontend)
Author: Ashish Sharma (Backend Lead & Team Lead)
Project ID: SKIT/AI/2023-2027/09
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.ml_service import ml_service

client = TestClient(app)

def test_root_and_health_endpoints():
    """Verify backend server connectivity and health check."""
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "author" in res_root.json()

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

def test_telemetry_ingestion_and_db_flow():
    """Verify hardware sensor data ingestion and database retrieval."""
    payload = {
        "station_id": "STN-TEST-01",
        "rainfall_rate": 24.5,
        "rain_accum_1h": 12.0,
        "pressure": 1009.2,
        "pressure_drop_rate": -1.5,
        "temperature": 18.0,
        "dew_point": 16.5,
        "humidity": 88.0,
        "battery_pct": 92,
        "signal_rssi": -78
    }

    # 1. Post telemetry packet
    post_res = client.post("/api/v1/sensors/telemetry", json=payload)
    assert post_res.status_code == 201
    assert post_res.json()["status"] == "success"

    # 2. Retrieve latest reading
    get_res = client.get("/api/v1/sensors/latest?station_id=STN-TEST-01")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["rainfallRate"] == 24.5
    assert data["pressure"] == 1009.2

def test_ml_prediction_risk_scoring():
    """Verify ML model scoring adapter on normal vs extreme cloudburst metrics."""
    # Test nominal conditions
    nominal = ml_service.predict_risk(rain_rate=1.0, pressure_drop=-0.2, temp=20.0, humidity=65.0)
    assert nominal["risk_level"] == "NORMAL"
    assert nominal["probability"] < 35.0

    # Test extreme cloudburst conditions (severe drop & torrential rain)
    extreme = ml_service.predict_risk(rain_rate=75.0, pressure_drop=-4.8, temp=15.0, humidity=98.0)
    assert extreme["risk_level"] == "WARNING"
    assert extreme["probability"] >= 75.0

def test_prediction_api_endpoint():
    """Verify live prediction endpoint consumed by Frontend Risk Gauge."""
    res = client.get("/api/v1/predict/status?station_id=STN-TEST-01")
    assert res.status_code == 200
    data = res.json()
    assert "probability" in data
    assert "risk_level" in data
    assert "factors" in data

def test_alert_system_flow():
    """Verify hazard alert retrieval and operator acknowledgment."""
    # 1. Query active alerts
    res_alerts = client.get("/api/v1/alerts/active")
    assert res_alerts.status_code == 200
    assert isinstance(res_alerts.json(), list)
