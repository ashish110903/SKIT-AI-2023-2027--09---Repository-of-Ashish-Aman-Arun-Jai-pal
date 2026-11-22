import statistics

def analyze_rain_distribution(values: list) -> dict:
    return {'mean': statistics.mean(values), 'median': statistics.median(values), 'stdev': statistics.stdev(values)}
