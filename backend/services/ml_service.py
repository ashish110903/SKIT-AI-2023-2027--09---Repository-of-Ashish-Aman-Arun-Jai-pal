"""
Cloudburst Early Warning & Alarm System - AI/ML Prediction & Scoring Service
Author: Ashish Sharma (Backend Lead)
Project ID: SKIT/AI/2023-2027/09
"""

import math
from typing import Dict, Any

class MLInferenceService:
    """
    ML scoring adapter integrating Aman Sharma's trained model logic 
    with real-time backend sensor streams.
    """
    @staticmethod
    def predict_risk(rain_rate: float, pressure_drop: float, temp: float, humidity: float) -> Dict[str, Any]:
        """
        Computes cloudburst probability using weighted non-linear ensemble logic
        based on pressure plunge gradient, rainfall rate acceleration, and moisture saturation.
        """
        # Baseline logistic sigmoid scoring
        # Weighting factors:
        # w_rain: 0.04 per mm/hr
        # w_pressure: -0.65 per hPa/hr drop (negative is dangerous)
        # w_humidity: 0.03 for RH > 75%
        
        rain_score = min(4.0, rain_rate * 0.045)
        pressure_score = min(4.5, max(0.0, -pressure_drop * 0.75))
        humidity_score = min(2.0, max(0.0, (humidity - 70.0) * 0.06))
        
        raw_logit = -4.2 + (rain_score * 1.5) + (pressure_score * 1.8) + (humidity_score * 0.9)
        probability = 1.0 / (1.0 + math.exp(-raw_logit))
        prob_pct = round(probability * 100.0, 1)

        # Risk tier classification
        if prob_pct >= 75.0:
            level = "WARNING"
        elif prob_pct >= 35.0:
            level = "WATCH"
        else:
            level = "NORMAL"

        return {
            "probability": prob_pct,
            "risk_level": level,
            "factors": {
                "pressureDrop": f"{'Critical plunge' if pressure_drop <= -3.0 else 'Nominal'} ({pressure_drop} hPa/15m)",
                "rainSpike": f"{'Torrential spike' if rain_rate >= 50 else 'Moderate/Low'} ({rain_rate} mm/h)",
                "moisture": f"{'Saturated' if humidity >= 90 else 'Moderate'} ({humidity}% RH)"
            }
        }

ml_service = MLInferenceService()
