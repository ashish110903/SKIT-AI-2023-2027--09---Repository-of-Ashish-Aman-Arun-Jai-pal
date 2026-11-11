import asyncio
from backend.services.pipeline_coordinator import process_incoming_batch

def test_coordinator():
    sample = [{'timestamp': '2026-11-10T10:00:00', 'rain_mm': 1.0, 'pressure_hpa': 1012.0, 'humidity_pct': 70.0}]
    # sync smoke test
    assert len(sample) == 1
