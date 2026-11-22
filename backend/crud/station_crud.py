from sqlalchemy.orm import Session
from backend.models.station import WeatherStation

def register_station(db: Session, st_id: str, name: str, lat: float, lon: float):
    st = WeatherStation(station_id=st_id, name=name, latitude=lat, longitude=lon)
    db.add(st)
    db.commit()
    return st
