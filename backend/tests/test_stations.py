from backend.crud.station_crud import register_station
from backend.database import SessionLocal, Base, engine

def test_register():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    assert db is not None
    db.close()
