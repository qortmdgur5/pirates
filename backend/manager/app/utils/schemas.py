from datetime import date, time
from pydantic import BaseModel

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