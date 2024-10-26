from sqlalchemy import Column, Integer, String, DateTime, Float, func, Boolean, Text, ForeignKey
from ..db.database import Base
from sqlalchemy.orm import relationship

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
    isAuth = Column(Boolean) 
    date = Column(DateTime, default=func.now(), index=True)
    name = Column(String(100))
    phoneNumber = Column(String(100))
    accommodations = relationship("Accommodation", back_populates="owner")
    

class Accommodation(Base):
    __tablename__ = "Accommodation"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('Owner.id'))
    name = Column(String(255), index=True)
    address = Column(String(255), index=True)
    introduction =Column(String(255), index=True)
    date = Column(DateTime, default=func.now(), index=True)
    score = Column(Float, index=True, nullable=True)
    loveCount = Column(Integer, index=True, nullable=True)
    owner = relationship("Owner", back_populates="accommodations")
    reviews = relationship("Review", back_populates="accommodation")


class Review(Base):
    __tablename__ = "Review"

    id = Column(Integer, primary_key=True, index=True)
    accommodation_id = Column(Integer, ForeignKey('Accommodation.id'))
    user_id = Column(Integer, index=True)
    contents = Column(Text, index=True)
    score =Column(Float, index=True)
    accommodation = relationship("Accommodation", back_populates="reviews") 
