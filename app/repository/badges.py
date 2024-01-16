from database import SessionLocal, dec_session_local
from models import Badge


@dec_session_local
def get_badge_by_id(db: SessionLocal, badge_id: str) -> Badge:
    return db.query(Badge).filter(Badge.id == badge_id).first()


@dec_session_local
def insert_badge(db: SessionLocal, badge: Badge) -> Badge:
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge
