from ml.models.anomaly_detector import AnomalyDetector
def test_anomaly_score():
    ad = AnomalyDetector()
    assert ad.anomaly_score(50, 10) == 1.0
