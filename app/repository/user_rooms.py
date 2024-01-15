from database import SessionLocal, dec_session_local
from models import Room, User, UserRoom


@dec_session_local
def get_rooms_by_username(db: SessionLocal, username: str):
    user = db.query(User).filter(User.username == username).first()

    if user:
        rooms = db.query(Room).join(UserRoom).filter(UserRoom.user_id == username).all()
        return rooms
    return None