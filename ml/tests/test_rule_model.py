from ml.models.rule_based_model import rule_based_predict
def test_rules():
    assert rule_based_predict(40.0, 6.0, 95.0) == 'CRITICAL'
    assert rule_based_predict(2.0, 1.0, 60.0) == 'LOW'
