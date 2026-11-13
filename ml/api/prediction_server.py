from fastapi import FastAPI
from ml.cloudburst_predictor import predict_cloudburst

app = FastAPI(title='Cloudburst Prediction Service')
@app.post('/predict')
def predict(payload: list):
    return predict_cloudburst(payload)
