def clean_telemetry_batch(records: list) -> list:
    seen = set()
    clean = []
    for r in records:
        key = (r.get('station_id'), r.get('timestamp'))
        if key not in seen:
            seen.add(key)
            clean.append(r)
    return clean
