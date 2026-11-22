import csv

def load_csv_data(filepath: str) -> list:
    records = []
    with open(filepath, 'r') as f:
        r = csv.DictReader(f)
        for row in r: records.append(row)
    return records
