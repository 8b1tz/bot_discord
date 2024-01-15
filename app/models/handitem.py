from database import Base
from sqlalchemy import Column, Integer, String


class Handitem(Base):
    __tablename__ = "handitem"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __str__(self):
        return f'Handitem ID: {self.id}\nHanditem NAME: {self.name}'
