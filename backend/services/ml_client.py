class MLPredictionClient:
    async def predict_risk(self, sensor_readings: list) -> dict:
        from ml.cloudburst_predictor import predict_cloudburst
        return predict_cloudburst(sensor_readings)

ml_client = MLPredictionClient()
