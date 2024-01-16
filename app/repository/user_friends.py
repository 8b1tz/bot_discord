from database import SessionLocal, dec_session_local
from models import User


@dec_session_local
def get_friends(db: SessionLocal, username: str):
    user = db.query(User).filter_by(username=username).first()

    if user:
        friends = user.friendships
        return friends
    else:
        return None