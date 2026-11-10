from backend.services.ml_client import ml_client
from backend.services.alert_dispatcher import alert_dispatcher

async def process_incoming_batch(batch: list):
    result = await ml_client.predict_risk(batch)
    if result.get('risk_level') in ('HIGH', 'CRITICAL'):
        alert_dispatcher.broadcast(result['risk_level'], result.get('alert', 'Warning'))
    return result
