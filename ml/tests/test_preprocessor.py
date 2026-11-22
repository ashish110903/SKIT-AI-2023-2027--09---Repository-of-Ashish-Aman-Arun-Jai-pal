from ml.data.preprocessor import SimpleScaler
def test_scaler():
    s = SimpleScaler()
    s.fit([10, 20, 30])
    t = s.transform([20])
    assert round(t[0], 2) == 0.0
