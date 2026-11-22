import random

def generate_synthetic_record(is_cloudburst=False):
    if is_cloudburst:
        return {'rain_mm': random.uniform(30.0, 75.0), 'pressure_hpa': random.uniform(985.0, 1002.0), 'humidity_pct': random.uniform(90.0, 99.0), 'label': 'CRITICAL'}
    return {'rain_mm': random.uniform(0.0, 8.0), 'pressure_hpa': random.uniform(1008.0, 1018.0), 'humidity_pct': random.uniform(45.0, 75.0), 'label': 'LOW'}
