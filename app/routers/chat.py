from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter()

# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message_to_user(self, message: str, user_id: int):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)
        else:
            # Optionally log that the user was not connected
            print(f"User {user_id} is not connected.")

    async def broadcast(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)

manager = ConnectionManager()

# WebSocket endpoint for chat
@router.websocket("/ws/chat/{sender_id}/{receiver_id}")
async def chat_endpoint(websocket: WebSocket, sender_id: int, receiver_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    await manager.connect(websocket, sender_id)  # Store the sender's connection
    try:
        while True:
            data = await websocket.receive_text()
            # Save the message to the database
            chat_message = await save_message_to_db(sender_id, receiver_id, data, db)

            # Send the message to the receiver
            await manager.send_message_to_user(data, receiver_id)

            # Acknowledge the message sent to sender
            await websocket.send_text(f"Message sent to {receiver_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(sender_id)  # Remove the sender's connection on disconnect
        print(f"User {sender_id} disconnected.")

async def save_message_to_db(sender_id: int, receiver_id: int, content: str, db: Session):
    chat_message = models.ChatMessage(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message

# New endpoint to retrieve message history
@router.get("/messages/{user_id}")
async def get_message_history(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.ChatMessage).filter(
        (models.ChatMessage.sender_id == user_id) | (models.ChatMessage.receiver_id == user_id)
    ).all()
    return messages

# Endpoint to check user presence
@router.get("/users/online")
async def get_online_users():
    return list(manager.active_connections.keys())  # Return list of connected user IDs

