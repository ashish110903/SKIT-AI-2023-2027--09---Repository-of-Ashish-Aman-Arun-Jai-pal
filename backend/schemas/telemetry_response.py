from pydantic import BaseModel

class IngestionResponse(BaseModel):
    success: bool
    station_id: str
    records_processed: int
