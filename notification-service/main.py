from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class ChannelEnum(str, Enum):
    email = "email"
    sms = "sms"

class Notification(BaseModel):
    customer_id: str
    channel: ChannelEnum
    message: str

@app.post("/notify")
def notify(notification: Notification):
    # Simulate notification (email or SMS)
    print(f"Notification sent to {notification.customer_id} via {notification.channel.upper()}")
    print(f"Message: {notification.message}")
    
    return {
        "status": "sent",
        "to": notification.customer_id,
        "channel": notification.channel,
        "message": notification.message
    }

@app.get("/")
def root():
    return {"message": "NotificationService is running"}
