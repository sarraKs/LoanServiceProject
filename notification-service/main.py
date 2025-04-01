from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

CLIENT_NOTIFICATION_URL = "http://client-service:8005/notification"
CLIENT_CHECK_REQUEST_URL = "http://client-service:8005/request-check"

class Notification(BaseModel):
    customer_id: str
    message: str

@app.post("/notify")
def send_notification(notification: Notification):
    try:
        response = requests.post(CLIENT_NOTIFICATION_URL, json={
            "customer_id": notification.customer_id,
            "message": notification.message
        })
        #print(f"client_response: {response.json()}")
        return {"status": "sent", "client_response": response.json()}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
    
@app.post("/request-check")
def send_notification_check_request(notification: Notification):
    try:
        response = requests.post(CLIENT_CHECK_REQUEST_URL, json={
            "customer_id": notification.customer_id,
            "message": notification.message
        })
        return {"status": "sent", "client_response": response.json()}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
