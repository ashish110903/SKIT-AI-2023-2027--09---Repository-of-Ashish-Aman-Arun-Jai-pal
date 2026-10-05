def detect_humidity_spike(h_list: list) -> bool:
    return len(h_list) > 1 and (h_list[-1] - h_list[0]) >= 15.0
