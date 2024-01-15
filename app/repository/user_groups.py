from database import SessionLocal, dec_session_local
from models import Group, User, UserGroup


@dec_session_local
def get_groups_by_username(db: SessionLocal, username: str):
    user = db.query(User).filter(User.username == username).first()

    if user:
        groups = db.query(Group).join(UserGroup).filter(UserGroup.user_id == username).all()
        return groups
    return None