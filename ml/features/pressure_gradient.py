def compute_dp_dt(p_start: float, p_end: float, dt_hours: float) -> float:
    if dt_hours <= 0: return 0.0
    return (p_end - p_start) / dt_hours
