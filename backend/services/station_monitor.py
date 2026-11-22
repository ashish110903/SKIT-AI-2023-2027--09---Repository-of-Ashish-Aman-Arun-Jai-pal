import time
def is_station_alive(last_seen_ts: float, timeout_sec: float = 900) -> bool:
    return (time.time() - last_seen_ts) < timeout_sec
