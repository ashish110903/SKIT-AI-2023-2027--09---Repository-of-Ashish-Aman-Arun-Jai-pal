class AnomalyDetector:
    def anomaly_score(self, rain: float, pressure_drop: float) -> float:
        return (rain / 50.0 * 0.6) + (pressure_drop / 10.0 * 0.4)
