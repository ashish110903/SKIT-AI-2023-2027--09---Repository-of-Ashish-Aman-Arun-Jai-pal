def f_beta_score(precision: float, recall: float, beta: float = 2.0) -> float:
    # Beta=2 prioritizes recall (minimizing missed cloudburst disasters)
    num = (1 + beta**2) * (precision * recall)
    den = (beta**2 * precision) + recall
    return num / den if den else 0.0
