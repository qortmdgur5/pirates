from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    is_active: bool = True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True