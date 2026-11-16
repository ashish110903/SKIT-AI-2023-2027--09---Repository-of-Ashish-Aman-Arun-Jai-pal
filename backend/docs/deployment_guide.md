# Production Deployment Guide

- Run Uvicorn: `uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4`
- Systemd service file: `/etc/systemd/system/cloudburst.service`
