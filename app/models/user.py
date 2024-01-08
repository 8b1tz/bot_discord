from database import Base
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        relationship)


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True, auto_increment=True)
    username = Column(String)
    reg_date = Column(DateTime)
    achievement_points = Column(Integer)
    image_id = Column(String)
    gender = Column(String(1))
    friends = relationship(
        "User",
        secondary="friendship",
        primaryjoin=id == ForeignKey("friendship.user_id"),
        secondaryjoin=id == ForeignKey("friendship.friend_id")
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
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id"), primary_key=True)


class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    users = relationship("User", secondary="user_room")


class UserRoom(Base):
    __tablename__ = "user_room"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"), primary_key=True)


class Badge(Base):
    __tablename__ = "badge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    users = relationship("User", secondary="user_badge")


class UserBadge(Base):
    __tablename__ = "user_badge"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    badge_id = Column(Integer, ForeignKey("badge.id"), primary_key=True)


class Friendship(Base):
    __tablename__ = "friendship"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    friend_id = Column(Integer, ForeignKey("user.id"), primary_key=True)