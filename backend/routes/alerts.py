"""
Cloudburst Early Warning & Alarm System - Alerts & Notifications Router
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import AlertRecord
from backend import crud

router = APIRouter(prefix="/alerts", tags=["Emergency Alerts & Alarms"])

@router.get("/active", response_model=List[dict])
def get_active_alerts(db: Session = Depends(get_db)):
    """
    Returns currently active hazard alerts for the frontend emergency banner & siren.
    """
    alerts = crud.get_active_alerts(db)
    return [
        {
            "id": a.id,
            "stationId": a.station_id,
            "level": a.severity,
            "desc": a.description,
            "probability": a.probability,
            "time": a.created_at.isoformat()
        }
        for a in alerts
    ]

@router.post("/{alert_id}/ack", response_model=dict)
def acknowledge_alert(
    alert_id: int = Path(..., description="Alert Record ID"),
    db: Session = Depends(get_db)
):
    """
    Allows emergency operators to acknowledge an active alert and mute sirens.
    """
    alert = db.query(AlertRecord).filter(AlertRecord.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert record not found")
    
    alert.acknowledged = True
    db.commit()
    
    return {
        "status": "success",
        "message": f"Alert {alert_id} acknowledged by operator",
        "alert_id": alert_id
    }
