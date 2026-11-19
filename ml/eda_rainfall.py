"""
ml/eda_rainfall.py
Aman Sharma - AI/ML | SKIT/AI/2023-2027/09
Sprint 2: Exploratory Data Analysis - Rainfall & Atmospheric Data
"""
import statistics

SAMPLE_DATA = [
    {"date": "2026-10-01", "rain_mm": 0.0,  "pressure_hpa": 1013.0, "humidity_pct": 55},
    {"date": "2026-10-02", "rain_mm": 2.5,  "pressure_hpa": 1010.0, "humidity_pct": 68},
    {"date": "2026-10-03", "rain_mm": 18.0, "pressure_hpa": 1004.5, "humidity_pct": 88},
    {"date": "2026-10-04", "rain_mm": 45.0, "pressure_hpa": 998.0,  "humidity_pct": 96},
    {"date": "2026-10-05", "rain_mm": 3.0,  "pressure_hpa": 1009.0, "humidity_pct": 72},
]

def describe(values: list, label: str):
    print(f"\n--- {label} ---")
    print(f"  Count : {len(values)}")
    print(f"  Mean  : {statistics.mean(values):.2f}")
    print(f"  Median: {statistics.median(values):.2f}")
    print(f"  Stdev : {statistics.stdev(values):.2f}")
    print(f"  Min   : {min(values):.2f}")
    print(f"  Max   : {max(values):.2f}")

def correlation(xs, ys):
    """Pearson correlation coefficient."""
    n = len(xs)
    mx, my = sum(xs)/n, sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    den = (sum((x-mx)**2 for x in xs) * sum((y-my)**2 for y in ys)) ** 0.5
    return round(num/den, 4) if den else 0.0

if __name__ == "__main__":
    rain     = [d["rain_mm"]      for d in SAMPLE_DATA]
    pressure = [d["pressure_hpa"] for d in SAMPLE_DATA]
    humidity = [d["humidity_pct"] for d in SAMPLE_DATA]

    describe(rain,     "Rainfall (mm)")
    describe(pressure, "Pressure (hPa)")
    describe(humidity, "Humidity (%)")

    print(f"\nCorrelation: Rain vs Pressure = {correlation(rain, pressure)}")
    print(f"Correlation: Rain vs Humidity  = {correlation(rain, humidity)}")