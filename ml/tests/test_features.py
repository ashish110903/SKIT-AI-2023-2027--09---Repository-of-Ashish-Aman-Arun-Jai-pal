from ml.features.rolling_features import compute_rolling_rain
def test_rolling():
    assert compute_rolling_rain([{'rain_mm': 5}, {'rain_mm': 10}]) == 15
