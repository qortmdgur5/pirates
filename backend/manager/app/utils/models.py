from sqlalchemy import Column, Integer, String, Date, Time
from ..db.database import Base

# 회원가입, 로그인 나중에, 테이블 다 바꿔야 함
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)

class Party(Base):
    __tablename__ = 'Party'
    id = Column(Integer, primary_key=True, index=True)
    accommodation_id = Column(Integer, index=True, nullable=False)
    partyDate = Column(Date, index=True)
    partyOpen = Column(Integer, index=True)
    partyTime = Column(Time, index=True)
    number = Column(Integer, index=True)
    partyOn = Column(Integer, index=True)
    
    
class Participant(Base):
    __tablename__ = 'Participant'
    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, index=True, nullable=False)
    name = Column(String(255), index=True)
    phone = Column(String(255), index=True)
    mbti = Column(String(255), index=True)
    age = Column(Integer, index=True)
    region = Column(String(255), index=True)
    gender = Column(Integer, index=True)