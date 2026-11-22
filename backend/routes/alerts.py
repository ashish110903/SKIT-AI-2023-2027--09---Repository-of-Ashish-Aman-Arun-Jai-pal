from fastapi import APIRouter
from backend.services.alert_dispatcher import alert_dispatcher

router = APIRouter(prefix='/api/alerts', tags=['Alerts'])

@router.get('/active')
def get_active_alerts():
    return [{'severity': 'LOW', 'message': 'All sensors normal'}]
