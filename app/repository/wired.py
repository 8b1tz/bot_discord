from database import SessionLocal, dec_session_local
from models import Wired


@dec_session_local
def get_wired_by_type(db: SessionLocal, wired_type: str) -> Wired:
    return db.query(Wired).filter(Wired.type == wired_type).first()


@dec_session_local
def get_wired_by_name(db: SessionLocal, wired_name: str) -> Wired:
    return db.query(Wired).filter(Wired.name == wired_name).first()


@dec_session_local
def get_all_wireds(db: SessionLocal) -> Wired:
    return db.query(Wired).all()


@dec_session_local
def insert_wired(db: SessionLocal, wired: Wired) -> Wired:
    db.add(wired)
    db.commit()
    db.refresh(wired)
    return wired


@dec_session_local
def update_wired(db: SessionLocal, id: str, update_wired: Wired) -> Wired:
    existing_item = db.query(Wired).filter(Wired.id == id).first()
    if existing_item:
        for key, value in update_wired.to_dict().items():
            setattr(existing_item, key, value)
        db.commit()
        db.refresh(existing_item)
    return existing_item
