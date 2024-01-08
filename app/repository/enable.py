from database import SessionLocal, dec_session_local
from models import Enable


@dec_session_local
def get_enable_by_id(db: SessionLocal, enable_id: str) -> Enable:
    return db.query(Enable).filter(Enable.id == enable_id).first()


@dec_session_local
def get_enable_by_name(db: SessionLocal, enable_name: str) -> Enable:
    return db.query(Enable).filter(Enable.name == enable_name).first()


@dec_session_local
def get_all_enables(db: SessionLocal) -> Enable:
    return db.query(Enable).all()


@dec_session_local
def insert_enable(db: SessionLocal, enable: Enable) -> Enable:
    db.add(enable)
    db.commit()
    db.refresh(enable)
    return enable


@dec_session_local
def update_enable(db: SessionLocal, id: str, update_enable: Enable) -> Enable:
    existing_item = db.query(Enable).filter(Enable.id == id).first()
    if existing_item:
        for key, value in update_enable.to_dict().items():
            setattr(existing_item, key, value)
        db.commit()
        db.refresh(existing_item)
    return existing_item
