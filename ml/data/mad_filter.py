import statistics
def mad_filter(data: list, thresh: float = 3.5) -> list:
    med = statistics.median(data)
    devs = [abs(x - med) for x in data]
    mad = statistics.median(devs) or 1.0
    return [x for x in data if (abs(x - med) / mad) < thresh]
