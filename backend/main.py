from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import api_router

app = FastAPI(title='Cloudburst Early Warning System')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
app.include_router(api_router)

@app.get('/')
def root():
    return {'system': 'Cloudburst Early Warning API', 'status': 'online'}
