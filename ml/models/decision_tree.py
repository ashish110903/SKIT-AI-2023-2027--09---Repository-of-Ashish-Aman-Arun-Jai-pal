class SimpleDecisionTree:
    def predict(self, r, p):
        if r > 30.0:
            return 'CRITICAL' if p > 4.5 else 'HIGH'
        return 'LOW'
