class SimpleScaler:
    def __init__(self):
        self.mean = 0.0
        self.std = 1.0
    def fit(self, vals):
        import statistics
        self.mean = statistics.mean(vals)
        self.std = statistics.stdev(vals) or 1.0
    def transform(self, vals):
        return [(v - self.mean) / self.std for v in vals]
