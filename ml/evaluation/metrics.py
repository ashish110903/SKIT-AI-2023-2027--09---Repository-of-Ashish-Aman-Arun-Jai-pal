def compute_f1_score(tp, fp, fn):
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return 2 * (prec * rec) / (prec + rec) if (prec + rec) else 0.0
