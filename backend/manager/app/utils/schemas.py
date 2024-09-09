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