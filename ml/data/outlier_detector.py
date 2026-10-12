def filter_outliers_zscore(vals: list, threshold: float = 3.0) -> list:
    import statistics
    m = statistics.mean(vals)
    s = statistics.stdev(vals) or 1.0
    return [v for v in vals if abs((v - m) / s) < threshold]
