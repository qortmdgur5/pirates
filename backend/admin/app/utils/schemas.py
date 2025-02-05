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
    team: int
    matchStartTime: Optional[str]

class managerParty(BaseModel):
    data: List[managerParties]    
    totalCount: int  
 
class managerPartiesPost(BaseModel):
    id: int
    partyDate: str
    number: int
    partyOpen: bool
    partyTime: str
    team: int
       
class managerPartyUpdate(BaseModel):
    partyDate: str
    number: int
    partyOpen: bool
    partyTime: str
    team: int
    
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
    
    
class signupOwner(BaseModel):
    username: str
    password: str
    name: str
    phoneNumber: str
    
class signupManager(BaseModel):
    username: str
    password: str
    name: str
    phoneNumber: str
    owner_id: int
    
class loginResponse(BaseModel):
    access_token: str
    token_type: str

class managerPartyUserInfoData(BaseModel):
    id: int
    team: int

class managerPartyUserInfoDatas(BaseModel):
    data: List[managerPartyUserInfoData] 

## user
class userLoginResponse(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[bool] = None
    job: Optional[str] = None
    age: Optional[int] = None
    mbti: Optional[str] = None   
    region: Optional[str] = None

class userLoginResponses(BaseModel):
    userInfo: List[userLoginResponse] = []   
    id: int  
    party_id: int

class userSignupResponse(BaseModel):
    user_id: int
    name: str
    phone: str
    email: str
    gender: bool
    job: Optional[str] = None
    age: Optional[int] = None
    mbti: Optional[str] = None
    region: Optional[str] = None

class userPartyRequest(BaseModel):
    qr: Optional[str] = None
    party_id: Optional[int] = None

class userPartyResponses(BaseModel):
    name: Optional[str] = None
    introduction: Optional[str] = None
    address: Optional[str] = None
    number: Optional[str] = None
    phoneNumber: Optional[str] = None
    score: Optional[float] = None
    loveCount: Optional[int] = None   
    party_id: Optional[int] = None
    party_on: bool
    matchStartTime: Optional[datetime] = None

class userPartyResponse(BaseModel):
    data: List[userPartyResponses]
    totalCount: int

class userPartyInfoResponses(BaseModel):
    id: int
    name: str
    gender: bool
    team: int 

class userPartyInfoResponse(BaseModel):
    data: List[userPartyInfoResponses]
    totalCount: int
    
class userPartyInfoChatExistResponses(BaseModel):
    id: int
    chatRoom_id: int

class userPartyInfoChatExistResponse(BaseModel):
    data: List[userPartyInfoChatExistResponses]
    totalCount: int
    
    
class UserLoginResponse(BaseModel):
    msg: str
    user: str

class userChatRoomRequest(BaseModel):
    user_id_1: int
    user_id_2: int
    party_id: int

class userChatRoomsRequest(BaseModel):
    user_id: int
    party_id: int

class userChatContentsRequest(BaseModel):
    chatRoom_id: int
    lastChat_id: Optional[int] = None

class chatCreateRequest(BaseModel):
    user_id: int
    contents: str
    chatRoom_id: int
    
    
class lastReadChatRequest(BaseModel):
    chatRoom_id: int
    user_id: int
    lastReadChat_id: Optional[int] = None
    
class userMatchSelectResponses(BaseModel):
    user_id: int
    phone: str
    team: int
    
class userMatchSelectResponse(BaseModel):
    data: Optional[dict] = None  
    totalCount: int