"""
Cloudburst Early Warning & Alarm System - FastAPI Application Entry Point
Author: Ashish Sharma (Backend Lead & Team Lead)
Project ID: SKIT/AI/2023-2027/09
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes.sensors import router as sensor_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for real-time mountain sensor data ingestion, hazard detection & AI/ML cloudburst risk scoring.",
    version="1.0.0"
)

# Enable CORS for Frontend Dashboard (Jai Pal)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(sensor_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "author": "Ashish Sharma (Backend Lead)",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "api_version": "v1"
    }
