from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_room_id: int):
        await websocket.accept()
        if chat_room_id not in self.active_connections:
            self.active_connections[chat_room_id] = []
        self.active_connections[chat_room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_room_id: int):
        self.active_connections[chat_room_id].remove(websocket)

    async def broadcast(self, message: str, chat_room_id: int):
        for connection in self.active_connections.get(chat_room_id, []):
            await connection.send_text(message)
