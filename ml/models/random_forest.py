class SimpleEnsemble:
    def predict(self, r, p, h):
        votes = ['CRITICAL' if r > 28 and p > 4.5 else 'LOW']
        return votes[0]
