from datetime import date, time, datetime
from pydantic import BaseModel

# 로그인 
class UserCreate(BaseModel):
    email: str
    password: str

class UserInDB(UserCreate):
    hashed_password: str

class UserResponse(BaseModel):
    email: str
    is_active: bool

    class Config:
        from_attributes = True
        
     
# 파티방 관리     
class PartyBase(BaseModel):
    accommodation_id: int
    partyDate: date
    partyOpen: int
    partyTime: time
    number: int
    partyOn: int
    
class Party(PartyBase):
    id: int

    class Config:
        from_attributes = True
        
# 파티방 명단       
class ParticipantBase(BaseModel):
    party_id: int
    name: str
    phone: str
    mbti: str
    age: int
    region: str
    gender: int
    
class Participant(ParticipantBase):
    id: int

    class Config:
        from_attributes = True
        
        
        
        
    

# # 조 관리
# class PartyTeam(BaseModel):
#     id: int
#     totalNumber: int
#     teamNumber: int
    
#     class Config:
#         from_attributes = True
        
        
# class PartyUserInfoBase(BaseModel):
#     user_id: int
#     team: int
#     partyOn: int

    
# class PartyUserInfo(PartyUserInfoBase):
#     id: int

#     class Config:
#         from_attributes = True
        






# 매니저 관리
class ManagerBase(BaseModel):
    owner_id: int
    username: str
    password: str
    role: str

class ManagerCreate(ManagerBase):
    pass
  
class Manager(ManagerBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True





#  프로그램 관리