from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    username = Column(String, primary_key=True, nullable=False, unique=True)
    reg_date = Column(DateTime)
    achievement_points = Column(Integer)
    image_id = Column(String)
    gender = Column(String(1))

    # Relacionamentos
    friendships = relationship(
        'Friendship',
        back_populates='user_id',
        cascade="all, delete-orphan"
    )
    groups = relationship("Group", secondary="user_group")
    rooms = relationship("Room", secondary="user_room")
    badges = relationship("Badge", secondary="user_badge")


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    users = relationship("User", secondary="user_group")


class UserGroup(Base):
    __tablename__ = "user_group"
    user_id = Column(String, ForeignKey("user.username"), primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id"), primary_key=True)


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    users = relationship("User", secondary="user_room")


class UserRoom(Base):
    __tablename__ = "user_room"
    user_id = Column(String, ForeignKey("user.username"), primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"), primary_key=True) 


class Badge(Base):
    __tablename__ = "badge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    users = relationship("User", secondary="user_badge")


class UserBadge(Base):
    __tablename__ = "user_badge"
    user_id = Column(String, ForeignKey("user.username"), primary_key=True)  
    badge_id = Column(Integer, ForeignKey("badge.id"), primary_key=True)


class Friendship(Base):
    __tablename__ = "friendship"
    user_id = Column(String, ForeignKey('user.username'), primary_key=True)
    friend_id = Column(String, ForeignKey('user.username'), primary_key=True)

    friends = relationship("User", back_populates="username")