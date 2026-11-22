from ml.eda.pressure_analysis import calculate_pressure_drop
def test_drop():
    assert calculate_pressure_drop([1012, 1008, 1004]) == 8.0
