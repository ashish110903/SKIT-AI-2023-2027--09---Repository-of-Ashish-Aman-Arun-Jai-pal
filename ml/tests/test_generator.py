from ml.data.synthetic_generator import generate_synthetic_record
def test_cloudburst_record():
    r = generate_synthetic_record(True)
    assert r['label'] == 'CRITICAL'
    assert r['rain_mm'] >= 30.0
