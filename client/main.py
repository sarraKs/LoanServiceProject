from fastapi import FastAPI
from pydantic import BaseModel
import submit_loan
from contextlib import asynccontextmanager

app = FastAPI()

class Notification(BaseModel):
    customer_id: str
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan triggered: submitting initial loan")
    submit_loan.new_loan()
    yield
    print("App shutting down")

app = FastAPI(lifespan=lifespan)

# The client can receive a simple notification
@app.post("/notification")
def receive_notification(notif: Notification):
    print(f"Notification to customer {notif.customer_id}: {notif.message}")
    return {"status": "received"}

# The client can receive a notification to submit a check
@app.post("/request-check")
def receive_check_request(notif: Notification):
    submit_loan.validate_check(notif.customer_id, notif.message)
    return {"status": "received"}

#@app.on_event("startup")
#def send_initial_loan():
#    print("Client is starting, submitting initial loan...")
#    submit_loan.main()


