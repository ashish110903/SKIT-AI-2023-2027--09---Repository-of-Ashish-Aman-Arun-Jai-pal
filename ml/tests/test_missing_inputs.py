from ml.cloudburst_predictor import predict_cloudburst
def test_fallback_on_missing():
    # partial sensor packet
    r = predict_cloudburst([{'timestamp': '2026-11-19T10:00:00', 'rain_mm': 0.0, 'pressure_hpa': 1012.0}])
    assert r['risk_level'] == 'LOW'
if __name__ == '__main__': test_fallback_on_missing(); print('Missing input fallback verified.')
