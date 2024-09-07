from pydantic import BaseModel

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