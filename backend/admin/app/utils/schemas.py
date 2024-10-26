from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

## 새롭게 
class AdminAccomodations(BaseModel):
    id: int
    name: str
    address: str
    phoneNumber: str
    date: datetime

class AdminAccomodation(BaseModel):
    accomodations: List[AdminAccomodations]

class AdminOwners(BaseModel):
    id: int
    name: str
    username: str
    phoneNumber: str
    isAuth: bool 

class AdminOwner(BaseModel):
    owners: List[AdminOwners]



# 관리자 CRUD
class AdminBase(BaseModel):
    username: str
    role: str

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(AdminBase):
    pass



class Admin(AdminBase):
    id: int

    class Config:
        from_attributes = True
        
        
        
# 사장 CRUD        
class OwnerBase(BaseModel):
    username: str
    password: str
    

class OwnerCreate(OwnerBase):
    pass

class OwnerUpdate(OwnerBase):
    pass

class Owner(OwnerBase):
    id: int
    date: datetime
    role: Optional[str] = None

    class Config:
        from_attributes = True     
 
 
 
 
# 사장 권한 U
class OwnerRole(BaseModel):
    role: str
 
 
 
# 숙소 CRUD  
class AccommodationBase(BaseModel):
    name: str
    address: str
    introduction: str

class AccommodationCreate(AccommodationBase):
    owner_id: int

class AccommodationUpdate(AccommodationBase):
    pass

class Accommodation(AccommodationBase):
    id: int
    date: datetime
    score: Optional[float] = None
    loveCount: Optional[int] = None

    class Config:
        from_attributes = True
        
   
