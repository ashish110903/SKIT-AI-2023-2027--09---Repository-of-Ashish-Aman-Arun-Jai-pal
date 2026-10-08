def calc_30m_volume(rain_rates: list) -> float:
    return sum(rain_rates[:3]) * 0.5
