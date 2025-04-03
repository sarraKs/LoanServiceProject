from fastapi import FastAPI
from pydantic import BaseModel
import requests
import submit_loan
#from contextlib import asynccontextmanager

app = FastAPI()

API_SUBMIT_LOAN = "http://customer-service:8000/apply-loan"
API_VALIDATE_CHECK = "http://customer-service:8000/validate-check"

class Notification(BaseModel):
    customer_id: str
    message: str

"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan triggered: submitting initial loan")
    submit_loan.new_loan()
    yield
    print("App shutting down")

"""
#app = FastAPI(lifespan=lifespan)

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

"""
@app.on_event("startup")
def send_initial_loan():
    print("Client is starting, submitting initial loan...")
    new_loan()
    #submit_loan.new_loan()
"""

"""
def validate_check(customer_id: str, message: str):
    
    print(f"Notification to customer {customer_id}: {message}")
    check_amount = 5500.0
    print(f"Submitting check of {check_amount} for validation...")

    check_data = {
        "customer_id": customer_id,
        "check_amount": check_amount,
        "signature": True
    }
    requests.post(API_VALIDATE_CHECK, json=check_data)


def new_loan():
    # === Example customer input ===
    customer_id = "65"
    loan_amount = 5500.0

    loan_data = {
        "customer_id": customer_id,
        "first_name": "Johnny",
        "last_name": "Hd",
        "email": "johnny@example.com",
        "phone": "55522",
        "address": "86 Example Street",
        "loan_type": "commercial",
        "loan_amount": loan_amount,
        "loan_description": "buy something"
    }
    print("Submitting loan request...")
    requests.post(API_SUBMIT_LOAN, json=loan_data)

"""



