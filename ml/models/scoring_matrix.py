class HazardScoreMatrix:
    WEIGHT_RAIN = 0.45
    WEIGHT_PRESSURE = 0.35
    WEIGHT_HUMIDITY = 0.20
    @classmethod
    def calculate(cls, r, p, h):
        return (min(r/50.0, 1.0)*cls.WEIGHT_RAIN) + (min(p/10.0, 1.0)*cls.WEIGHT_PRESSURE) + (min(h/100.0, 1.0)*cls.WEIGHT_HUMIDITY)
