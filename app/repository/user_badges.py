from database import SessionLocal, dec_session_local
from models import Badge, User, UserBadge


@dec_session_local
def get_badges_by_username(db: SessionLocal, username: str):
    user = db.query(User).filter(User.username == username).first()

    if user:
        badges = db.query(Badge).join(UserBadge).filter(UserBadge.user_id == username).all()
        return badges
    return None