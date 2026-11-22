import time
from ml.cloudburst_predictor import predict_cloudburst
def benchmark():
    sample = [{'timestamp': '2026-11-18T10:00:00', 'rain_mm': 1.0, 'pressure_hpa': 1012.0, 'humidity_pct': 70.0}]
    t0 = time.time()
    for _ in range(100): predict_cloudburst(sample)
    elapsed = (time.time() - t0) / 100 * 1000
    print(f'Mean latency: {elapsed:.2f} ms')
if __name__ == '__main__': benchmark()
