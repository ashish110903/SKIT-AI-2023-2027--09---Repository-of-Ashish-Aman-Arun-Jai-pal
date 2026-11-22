def ensemble_vote(rule_risk: str, ml_risk: str) -> str:
    order = ['LOW', 'MODERATE', 'HIGH', 'CRITICAL']
    # Conservative fail-safe: take highest detected risk level
    return order[max(order.index(rule_risk), order.index(ml_risk))]
