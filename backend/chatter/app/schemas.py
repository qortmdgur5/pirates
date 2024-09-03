from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class ChatRoomCreate(BaseModel):
    user1_id: int
    user2_id: int

class ChatRoomResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    content: str
    user_id: int
    chat_room_id: int

class MessageResponse(BaseModel):
    id: int
    content: str
    timestamp: datetime
    user_id: int
    chat_room_id: int

    class Config:
        orm_mode = True
