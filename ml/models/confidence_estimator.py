def estimate_confidence(score: int) -> float:
    mapping = {4: 0.96, 3: 0.88, 2: 0.75, 1: 0.65, 0: 0.99}
    return mapping.get(score, 0.80)
