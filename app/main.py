from database import Base, engine
from models import (Badge, Enable, Friendship, Group, Handitem, Room, User,
                    UserBadge, UserGroup, UserRoom)

Base.metadata.create_all(bind=engine, tables=[Enable.__table__, Handitem.__table__, User.__table__, UserRoom.__table__, UserBadge.__table__, UserGroup.__table__, Friendship.__table__,
                                              Room.__table__, Badge.__table__, Group.__table__])
