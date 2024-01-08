from database import SessionLocal, dec_session_local
from models import Handitem


@dec_session_local
def get_handitem_by_id(db: SessionLocal, handitem_id: str) -> Handitem:
    return db.query(Handitem).filter(Handitem.id == handitem_id).first()


@dec_session_local
def get_handitem_by_name(db: SessionLocal, handitem_name: str) -> Handitem:
    return db.query(Handitem).filter(Handitem.name == handitem_name).first()


@dec_session_local
def get_all_handitens(db: SessionLocal) -> Handitem:
    return db.query(Handitem).all()


@dec_session_local
def insert_handitem(db: SessionLocal, handitem: Handitem) -> Handitem:
    db.add(handitem)
    db.commit()
    db.refresh(handitem)
    return handitem


@dec_session_local
def update_handitem(
    db: SessionLocal,
    id: str,
    update_handitem: Handitem
) -> Handitem:
    existing_item = db.query(Handitem).filter(Handitem.id == id).first()
    if existing_item:
        for key, value in update_handitem.to_dict().items():
            setattr(existing_item, key, value)
        db.commit()
        db.refresh(existing_item)
    return existing_item
