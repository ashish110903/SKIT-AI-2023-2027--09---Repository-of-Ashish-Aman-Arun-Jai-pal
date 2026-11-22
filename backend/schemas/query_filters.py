from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HistoryFilter(BaseModel):
    station_ids: Optional[List[str]] = None
    start_time: datetime
    end_time: datetime
