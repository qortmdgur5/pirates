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
    owner_id = Column(Integer, ForeignKey('Owner.id', ondelete="CASCADE"))
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
    accomodation_id = Column(Integer, ForeignKey('Accomodation.id', ondelete="CASCADE"))
    user_id = Column(Integer)
    contents = Column(Text)
    score = Column(Float)
    
    accomodation = relationship("Accomodation", back_populates="reviews") 

class Party(Base):
    __tablename__ = "Party"

    id = Column(Integer, primary_key=True, index=True)
    accomodation_id = Column(Integer, ForeignKey('Accomodation.id', ondelete="CASCADE"))
    partyDate = Column(DateTime, default=func.now())
    partyOpen = Column(Integer)
    partyTime = Column(Time, default=func.now())
    number = Column(Integer)
    partyOn = Column(Integer)
    team = Column(Integer)
    matchStartTime = Column(DateTime, nullable=False)
    
    partys = relationship("Accomodation", back_populates="party") 
    participant = relationship("Participant", back_populates="participants", cascade="all, delete-orphan") 
    users = relationship("User", back_populates="party", cascade="all, delete-orphan") 
    chatRooms = relationship("ChatRoom", back_populates="party", cascade="all, delete-orphan")
    userMatch = relationship("UserMatch", back_populates="party", cascade="all, delete-orphan")
    
class Manager(Base):
    __tablename__ = "Manager"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('Owner.id', ondelete="CASCADE"))
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
    party_id = Column(Integer, ForeignKey('Party.id', ondelete="CASCADE"))
    name = Column(String(255))
    phone = Column(String(255))
    mbti = Column(String(255))
    age = Column(Integer)
    region = Column(String(255))
    gender = Column(Boolean)
    
    participants = relationship("Party", back_populates="participant") 

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey('Party.id', ondelete="CASCADE"))
    username = Column(String(255))
    provider = Column(String(255))
    provider_id = Column(String(255))
    date = Column(DateTime, default=func.now())
    nickname = Column(String(255))
    role = Column(String(50))

    party = relationship("Party", back_populates="users")  
    userInfo = relationship("UserInfo", back_populates="user") 
    partyUserInfo = relationship("PartyUserInfo", back_populates="user") 
    chat = relationship("Chat", back_populates="user") 
    chatReadStatus = relationship("ChatReadStatus", back_populates="user") 

class UserInfo(Base):
    __tablename__ = "UserInfo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"))
    name = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255))
    gender = Column(Boolean)
    job = Column(String(255))
    age = Column(Integer)
    mbti = Column(String(255))
    region = Column(String(255))
    
    user = relationship("User", back_populates="userInfo")

class PartyUserInfo(Base):
    __tablename__ = "PartyUserInfo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"))
    team = Column(Integer)
    partyOn = Column(Boolean)

    user = relationship("User", back_populates="partyUserInfo")

class Chat(Base):
    __tablename__ = "Chat"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"))
    contents = Column(Text)
    date = Column(DateTime, default=func.now())
    chatRoom_id = Column(Integer, ForeignKey('ChatRoom.id', ondelete="CASCADE"))

    user = relationship("User", back_populates="chat")
    chatRooms = relationship("ChatRoom", back_populates="chat")


class ChatReadStatus(Base):
    __tablename__ = "ChatReadStatus"

    id = Column(Integer, primary_key=True, index=True)
    chatRoom_id = Column(Integer, ForeignKey('ChatRoom.id', ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"))
    lastReadChat_id = Column(Integer)
    date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="chatReadStatus")
    chatRooms = relationship("ChatRoom", back_populates="chatReadStatus")


class ChatRoom(Base):
    __tablename__ = "ChatRoom"

    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey('Party.id', ondelete="CASCADE"))
    user_id_1 = Column(Integer)
    user_id_2 = Column(Integer)

    party = relationship("Party", back_populates="chatRooms")
    chat = relationship("Chat", back_populates="chatRooms")
    chatReadStatus = relationship("ChatReadStatus", back_populates="chatRooms")
    
class UserMatch(Base):
    __tablename__ = "UserMatch"
    
    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey('Party.id', ondelete="CASCADE"))
    user_id_1 = Column(Integer)
    user_id_2 = Column(Integer)
    date = Column(DateTime, default=func.now())
    
    party = relationship("Party", back_populates="userMatch")
    
    