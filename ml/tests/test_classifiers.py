from ml.models.decision_tree import SimpleDecisionTree
def test_dt():
    dt = SimpleDecisionTree()
    assert dt.predict(35.0, 5.0) == 'CRITICAL'
