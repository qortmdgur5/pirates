from sqlalchemy import Column, Integer, String, DateTime, Float, Time, func, Boolean, Text, ForeignKey
from ..db.database import Base
from sqlalchemy.orm import relationship

class ErrorLog(Base):
    __tablename__ = "ErrorLogs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    
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
    role = Column(String(50)) 
    date = Column(DateTime, default=func.now())
    name = Column(String(100))
    phoneNumber = Column(String(100))
    accomodations = relationship("Accomodation", back_populates="owner")
    manager = relationship("Manager", back_populates="managers")
    

class Accomodation(Base):
    __tablename__ = "Accomodation"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('Owner.id'))
    name = Column(String(255), index=True)
    address = Column(String(255), index=True)
    introduction =Column(String(255), index=True)
    date = Column(DateTime, default=func.now())
    score = Column(Float, index=True, nullable=True)
    loveCount = Column(Integer, index=True, nullable=True)
    number = Column(String(100))
    owner = relationship("Owner", back_populates="accomodations")
    reviews = relationship("Review", back_populates="accomodation")
    party = relationship("Party", back_populates="partys")

class Review(Base):
    __tablename__ = "Review"

    id = Column(Integer, primary_key=True, index=True)
    accomodation_id = Column(Integer, ForeignKey('Accomodation.id'))
    user_id = Column(Integer, index=True)
    contents = Column(Text, index=True)
    score = Column(Float, index=True)
    accomodation = relationship("Accomodation", back_populates="reviews") 

class Party(Base):
    __tablename__ = "Party"

    id = Column(Integer, primary_key=True, index=True)
    accomodation_id = Column(Integer, ForeignKey('Accomodation.id'))
    partyDate = Column(DateTime, default=func.now())
    partyOpen = Column(Integer, index=True)
    partyTime = Column(Time, default=func.now())
    number = Column(Integer, index=True)
    partyOn = Column(Integer, index=True)
    partys = relationship("Accomodation", back_populates="party") 
    participant = relationship("Participant", back_populates="participants") 
    
class Manager(Base):
    __tablename__ = "Manager"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('Owner.id'))
    username = Column(String(255))
    password = Column(String(255))
    role =Column(String(255))
    date = Column(DateTime, default=func.now())
    name = Column(String(100))
    phoneNumber =Column(String(100))
    managers = relationship("Owner", back_populates="manager")

class Participant(Base):
    __tablename__ = "Participant"
    
    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey('Party.id'))
    name = Column(String(255))
    phone = Column(String(255))
    mbti = Column(String(255))
    age = Column(Integer)
    region = Column(String(255))
    gender = Column(Boolean)
    participants = relationship("Party", back_populates="participant") 