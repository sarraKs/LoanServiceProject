from fastapi import FastAPI
from pydantic import BaseModel
import requests
import submit_loan


# We created a fastAPI server for the clients to receive notifications from the application

app = FastAPI()

API_SUBMIT_LOAN = "http://customer-service:8000/apply-loan"
API_VALIDATE_CHECK = "http://customer-service:8000/validate-check"

class Notification(BaseModel):
    customer_id: str
    message: str


# The client can receive a simple notification
@app.post("/notification")
def receive_notification(notif: Notification):
    print(f"Notification to customer {notif.customer_id}: {notif.message}")
    return {"status": "received"}

# The client can receive a notification to submit a check
@app.post("/request-check")
def receive_check_request(notif: Notification):
    #validate_check(notif.customer_id, notif.message)
    submit_loan.validate_check(notif.customer_id, notif.message)
    return {"status": "received"}




