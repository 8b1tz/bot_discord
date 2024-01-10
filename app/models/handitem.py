from database import Base
from sqlalchemy import Column, Integer, String


class Handitem(Base):
    __tablename__ = "handitem"
    id = Column(Integer, primary_key=True)
    name = Column(String)
