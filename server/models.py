from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Temperature(Base):
    __tablename__ = 'temperature'

    id = Column(Integer, primary_key=True, index=True)
    tem = Column(Integer)


class AlertNum(Base):
    __tablename__ = 'alertNum'

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer)
