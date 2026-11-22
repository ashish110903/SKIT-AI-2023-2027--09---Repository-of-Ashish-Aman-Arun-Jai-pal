import csv
import io

def export_telemetry_to_csv(records: list) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(['timestamp', 'station_id', 'rainfall_mm', 'pressure_hpa', 'temperature_c', 'humidity_pct'])
    for r in records:
        writer.writerow([r.get('timestamp'), r.get('station_id'), r.get('rainfall_mm'), r.get('pressure_hpa'), r.get('temperature_c'), r.get('humidity_pct')])
    return out.getvalue()
