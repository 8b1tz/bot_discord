from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Type(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String)
    wireds = relationship('Wired', back_populates='type')

    def __str__(self):
        return f'Type ID: {self.id}\nType NAME: {self.name}'


class Wired(Base):
    __tablename__ = "wired"
    name = Column(String, primary_key=True, nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey('types.id'))
    description = Column(String)

    type = relationship('Type', back_populates='wireds')

    def __str__(self):
        return f'Wired ID: {self.id}\nWired NAME: {self.name}\nType ID: {self.type_id}'