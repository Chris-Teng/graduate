from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
from .database import Base


class Temperature(Base):
    __tablename__ = 'temperature'

    id = Column(Integer, primary_key=True, index=True)
    tem = Column(Integer)


class AlertNum(Base):
    __tablename__ = 'alertNum'

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer)

class securityStatus(Base):
    __tablename__ = "securitystatus"

    id = Column(Integer, primary_key=True, index=True)
    someone = Column(Boolean)
    onfire = Column(Boolean)

class faceRecord(Base):
    __tablename__ = "faceRecord"

    id = Column(Integer, primary_key=True, index=True)
    face = Column(String)
    time = Column(String)