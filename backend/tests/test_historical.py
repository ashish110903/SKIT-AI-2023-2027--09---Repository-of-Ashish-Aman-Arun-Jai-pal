from backend.utils.exporter import export_telemetry_to_csv
def test_csv_export():
    csv_data = export_telemetry_to_csv([{'timestamp': '2026-10-25', 'station_id': 'ST-1', 'rainfall_mm': 10.0, 'pressure_hpa': 1005.0, 'temperature_c': 20.0, 'humidity_pct': 80.0}])
    assert 'ST-1' in csv_data
