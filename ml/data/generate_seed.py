from ml.data.synthetic_generator import generate_synthetic_record
import csv

def build_seed_dataset():
    with open('ml/data/seed_weather.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['rain_mm', 'pressure_hpa', 'humidity_pct', 'label'])
        w.writeheader()
        for _ in range(450): w.writerow(generate_synthetic_record(False))
        for _ in range(50): w.writerow(generate_synthetic_record(True))

if __name__ == '__main__': build_seed_dataset()
