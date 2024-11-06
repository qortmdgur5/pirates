from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class SimpleResponse(BaseModel):
    msg: str
    
## admim (관리자 사용 API)
class AdminAccomodations(BaseModel):
    id: int
    name: str
    address: str
    number: str
    date: str
    
class AdminAccomodation(BaseModel):
    data: List[AdminAccomodations]
    totalCount: int
  
class AdminOwners(BaseModel):
    id: int
    name: str
    username: str
    phoneNumber: str
    isAuth: bool 

class AdminOwner(BaseModel):
    data: List[AdminOwners]
    totalCount: int


## owner (사장님 사용 API)
class OwnerAccomodationsWithoutDates(BaseModel):
    id: int
    name: str
    address: str
    number: str
    introduction: str
    score: Optional[float] = None
    loveCount: Optional[int] = None
    
class OwnerAccomodationsWithoutDate(BaseModel):
    data: List[OwnerAccomodationsWithoutDates] 
    totalCount: int  
    
class OwnerAccomodationsPost(BaseModel):
    id: int
    name: str
    address: str
    number: Optional[str] = None
    introduction: str

class OwnerAccomodationsPut(BaseModel):
    name: str
    address: str
    number: str
    introduction: str    


class OwnerManagers(BaseModel):
    id: int
    name: str
    username: str
    phoneNumber: str
    date: str   
    isAuth: bool 

class OwnerManager(BaseModel):
    data: List[OwnerManagers]    
    totalCount: int  
    

## owner , manager(사장님 And 매니저 사용 API)
class managerParties(BaseModel):
    id: int
    partyDate: str
    number: int
    partyOpen: bool
    partyTime: str
    participant: int

class managerParty(BaseModel):
    data: List[managerParties]    
    totalCount: int  
 
class managerPartiesPost(BaseModel):
    id: int
    partyDate: str
    number: int
    partyOpen: bool
    partyTime: str
       
class managerPartyUpdate(BaseModel):
    partyDate: str
    number: int
    partyOpen: bool
    partyTime: str
    
class managerParticipant(BaseModel):
    id: int
    name: str
    phone: str
    age: int
    gender: str
    mbti: str
    region: str

class managerParticipants(BaseModel):
    data: List[managerParticipant]    
    totalCount: int  
    
class managerParticipantPost(BaseModel):
    id: int
    name: str
    phone: str
    age: int
    gender: bool
    mbti: str
    region: str

class managerPartyOn(BaseModel):
    partyOn: bool
