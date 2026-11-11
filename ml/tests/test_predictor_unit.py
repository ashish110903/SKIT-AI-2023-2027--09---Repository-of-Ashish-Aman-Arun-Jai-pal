from ml.cloudburst_predictor import predict_cloudburst
def test_cloudburst_smoke():
    res = predict_cloudburst([])
    assert res['risk_level'] == 'LOW'
