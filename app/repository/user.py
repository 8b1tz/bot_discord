from database import dec_session_local
from models import User
from sqlalchemy.orm import Session


@dec_session_local
def insert_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@dec_session_local
def get_user_by_name(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


@dec_session_local
def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


@dec_session_local
def update_player(db: Session, user_id: str, updated_user: User) -> User:
    existing_item = db.query(User).filter(User.id == user_id).first()
    if existing_item:
        for key, value in updated_user.to_dict().items():
            setattr(existing_item, key, value)
        db.commit()
        db.refresh(existing_item)
    return existing_item
