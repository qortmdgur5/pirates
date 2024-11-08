from sqlalchemy import Column, Index, Integer, String, DateTime, Float, Time, func, Boolean, Text, ForeignKey
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
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255))


class Owner(Base):
    __tablename__ = "Owner"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
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
    name = Column(String(255))
    address = Column(String(255))
    introduction =Column(String(255))
    date = Column(DateTime, default=func.now())
    score = Column(Float, nullable=True)
    loveCount = Column(Integer, nullable=True)
    number = Column(String(100))
    directory = Column(String(255))
    owner = relationship("Owner", back_populates="accomodations")
    reviews = relationship("Review", back_populates="accomodation")
    party = relationship("Party", back_populates="partys")

class Review(Base):
    __tablename__ = "Review"

    id = Column(Integer, primary_key=True, index=True)
    accomodation_id = Column(Integer, ForeignKey('Accomodation.id'))
    user_id = Column(Integer)
    contents = Column(Text)
    score = Column(Float)
    accomodation = relationship("Accomodation", back_populates="reviews") 

class Party(Base):
    __tablename__ = "Party"

    id = Column(Integer, primary_key=True, index=True)
    accomodation_id = Column(Integer, ForeignKey('Accomodation.id'))
    partyDate = Column(DateTime, default=func.now())
    partyOpen = Column(Integer)
    partyTime = Column(Time, default=func.now())
    number = Column(Integer)
    partyOn = Column(Integer)
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