from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# 회사 CRUD
class CompanyBase(BaseModel):
    name: str
    is_active: int

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True



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
    owner_id: int
    name: str
    address: str
    introduction: str

class AccommodationCreate(AccommodationBase):
    pass

class AccommodationUpdate(AccommodationBase):
    pass

class Accommodation(AccommodationBase):
    id: int
    date: datetime
    score: Optional[float] = None
    loveCount: Optional[int] = None

    class Config:
        from_attributes = True
        
   
