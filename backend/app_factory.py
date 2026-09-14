from fastapi import FastAPI
from backend.config import config

def create_app():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    return app
