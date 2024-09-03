from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_chat_room(db: Session, chat_room: schemas.ChatRoomCreate):
    db_chat_room = models.ChatRoom(user1_id=chat_room.user1_id, user2_id=chat_room.user2_id)
    db.add(db_chat_room)
    db.commit()
    db.refresh(db_chat_room)
    return db_chat_room

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(content=message.content, user_id=message.user_id, chat_room_id=message.chat_room_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, chat_room_id: int):
    return db.query(models.Message).filter(models.Message.chat_room_id == chat_room_id).all()

