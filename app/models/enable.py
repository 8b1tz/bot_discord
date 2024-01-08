from database import Base
from sqlalchemy import Column, Integer, String


class Enable(Base):
    __tablename__ = "enable"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
