from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
import redis
import json
import threading
import asyncio
from . import models, schemas, crud
from .database import engine, get_db
from .websocket_manager import ConnectionManager

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
manager = ConnectionManager()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/chat_rooms/", response_model=schemas.ChatRoomResponse)
def create_chat_room(chat_room: schemas.ChatRoomCreate, db: Session = Depends(get_db)):
    db_chat_room = crud.create_chat_room(db=db, chat_room=chat_room)
    threading.Thread(target=redis_subscriber, args=(db_chat_room.id,)).start()
    return db_chat_room

@app.post("/messages/", response_model=schemas.MessageResponse)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)

@app.get("/messages/{chat_room_id}", response_model=List[schemas.MessageResponse])
def read_messages(chat_room_id: int, db: Session = Depends(get_db)):
    return crud.get_messages(db=db, chat_room_id=chat_room_id)

@app.websocket("/ws/{chat_room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, chat_room_id: int, client_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket, chat_room_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = {"chat_room_id": chat_room_id, "client_id": client_id, "message": data}
            redis_client.publish(f"chat_channel_{chat_room_id}", json.dumps(message))
            db_message = models.Message(content=data, user_id=client_id, chat_room_id=chat_room_id)
            db.add(db_message)
            db.commit()
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_room_id)
        await manager.broadcast(f"Client {client_id} left the chat", chat_room_id)

def redis_subscriber(chat_room_id: int):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"chat_channel_{chat_room_id}")
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            client_id = data['client_id']
            msg = data['message']
            asyncio.run(manager.broadcast(f"Client {client_id} says: {msg}", chat_room_id))
