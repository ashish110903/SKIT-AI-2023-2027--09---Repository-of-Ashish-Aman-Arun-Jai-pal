from sqlalchemy import Index
from backend.models import TelemetryRecord
Index('ix_station_time', TelemetryRecord.station_id, TelemetryRecord.timestamp)
