from sqlalchemy import Column, Integer, String
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
