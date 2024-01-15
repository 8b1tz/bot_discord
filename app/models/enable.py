from database import Base
from sqlalchemy import Column, Integer, String


class Enable(Base):
    __tablename__ = "enable"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String)

    def __str__(self):
        return f'Enable ID: {self.id}\nEnable NAME: {self.name}'