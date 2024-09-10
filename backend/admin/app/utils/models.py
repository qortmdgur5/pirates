from sqlalchemy import Column, Integer, String, DateTime, Float, func
from ..db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    is_active = Column(Integer, index=True)


class Admin(Base):
    __tablename__ = "Admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    password = Column(String(255), index=True)
    role = Column(String(255), index=True)


class Owner(Base):
    __tablename__ = "Owner"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    password = Column(String(255), index=True)
    role = Column(String(255), index=True, nullable=True)
    date = Column(DateTime, default=func.now(), index=True)
    

class Accommodation(Base):
    __tablename__ = "Accommodation"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255), index=True)
    introduction =Column(String(255), index=True)
    date = Column(DateTime, default=func.now(), index=True)
    score = Column(Float, index=True, nullable=True)
    loveCount = Column(Integer, index=True, nullable=True)
  