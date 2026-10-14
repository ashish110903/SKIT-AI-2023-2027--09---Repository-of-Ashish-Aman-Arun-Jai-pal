from backend.database import SessionLocal, Base, engine

def test_db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    assert db is not None
    db.close()
