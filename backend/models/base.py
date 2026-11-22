from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from backend.database import Base

class TimestampMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
