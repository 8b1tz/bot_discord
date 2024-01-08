from database import SessionLocal, dec_session_local
from models import Enable


@dec_session_local
def get_enable_by_id(db: SessionLocal, enable_id: str) -> Enable:
    return db.query(Enable).filter(Enable.id == enable_id).first()


@dec_session_local
def insert_enable(db: SessionLocal, enable: Enable) -> dict:
    pass