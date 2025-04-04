import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import grpc
import sys
import requests
import os
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from customer_model import Base, CustomerLoanRequest, LoanTypeEnum
from gql import gql, Client 
from gql.transport.requests import RequestsHTTPTransport
from zeep import Client as ZeepClient

# gRPC path
sys.path.append('./grpc')
import risk_pb2
import risk_pb2_grpc

app = FastAPI()

# ---------------------- Configuration ----------------------

DB_USER = os.getenv("DB_USER", "user1")
DB_PASS = os.getenv("DB_PASS", "password1")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "loans_db")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
NOTIFY_URL = "http://notification-service:8003/notify"
NOTIFY_REQUEST_CHECK_URL = "http://notification-service:8003/request-check"

# ---------------------- DB Setup ----------------------

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# ---------------------- Models ----------------------

class LoanRequest(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: str
    loan_type: LoanTypeEnum
    loan_amount: float
    loan_description: str | None = None

class CheckInput(BaseModel):
    customer_id: str
    check_amount: float
    signature: bool

# ---------------------- Utils ----------------------

def send_notification(customer_id: str, message: str):
    try:
        requests.post(NOTIFY_URL, json={
            "customer_id": customer_id,
            "message": message
        })
        #print("Notification sent")
    except Exception as e:
        print("Failed to notify customer:", e)

def send_notification_check_request(customer_id: str, message: str):
    try:
        requests.post(NOTIFY_REQUEST_CHECK_URL, json={
            "customer_id": customer_id,
            "message": message
        })
        #print("Notification sent")
    except Exception as e:
        print("Failed to notify customer:", e)


def check_loan_amount(customer_id: str, amount: float) -> bool:
    try:
        wsdl_url = "http://loan-verification-service:8001/?wsdl"
        client = ZeepClient(wsdl=wsdl_url)
        result = client.service.loan_amount_acceptation(customer_id, float(amount))
        print("Loan amount verification (SOAP result):", result)
        return result
    except Exception as e:
        print("SOAP Error:", e)
        return False

def get_customer_risk(customer_id: str) -> str:
    try:
        channel = grpc.insecure_channel('risk-assessment-service:50051')
        stub = risk_pb2_grpc.RiskAssessmentStub(channel)
        request = risk_pb2.RiskRequest(customer_id=customer_id)
        response = stub.AssessCustomerRisk(request)
        return response.risk_level
    except Exception as e:
        print("gRPC Error:", e)
        return "high"

# ---------------------- Routes ----------------------

@app.get("/")
def root():
    return {"message": "CustomerService with PostgreSQL is running"}

@app.post("/apply-loan")
def apply_loan(request: LoanRequest):
    db = SessionLocal()

    exists = db.query(CustomerLoanRequest).filter_by(customer_id=request.customer_id).first()
    if exists:
        send_notification(request.customer_id, f"From customer-service: Customer {request.customer_id} already exists. You already submitted a loan request.")
        db.close()
        raise HTTPException(status_code=400, detail="Customer already exists")

    new_request = CustomerLoanRequest(**request.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    print(f"loan request received from customer {request.customer_id}.")

    # 1. Notify customer : loan request submitted
    send_notification(request.customer_id, f"From customer-service: Loan request of {request.loan_amount} submitted and being processed.")

    # 2. Loan amount check (using SOAP) : 
    soap_result = check_loan_amount(request.customer_id, request.loan_amount)
    if not soap_result:
        # 3. Notify customer if loan declined
        send_notification(request.customer_id, "From customer-service: Loan declined: amount exceeds the firm's limit.")
        db.close()
        raise HTTPException(status_code=400, detail="Loan amount exceeds allowed limit")

    #print(f"SOAP check passed for {request.customer_id}")

    # 4. Risk check (using gRPC) :
    risk = get_customer_risk(request.customer_id)
    print(f"Risk level check (gRPC result): {risk}")
    if risk == "high" and request.loan_amount >= 20000.0:
        # 5. Notify customer if loan declined
        send_notification(request.customer_id, "From customer-service: Loan declined: high risk profile detected.")
        db.close()
        raise HTTPException(status_code=400, detail="Loan declined due to high risk")

    # 6. Notify customer to submit a cashier check
    requested_check_amount = request.loan_amount / 10
    send_notification_check_request(request.customer_id, f"From customer-service: First checks passed. Please submit a cashier's check of {requested_check_amount:.2f} for loan processing.")

    db.close()
    return {
        "message": "Loan request successfully processed",
        "customer_id": request.customer_id,
        "risk_level": risk,
        "loan_amount": request.loan_amount,
        "loan_type": request.loan_type,
        "status": "pending check validation"
    }

@app.post("/validate-check")
def validate_check(data: CheckInput):
    db = SessionLocal()
    # Verify that the customer who submitted the check, exists (submitted a loan previously)
    loan = db.query(CustomerLoanRequest).filter_by(customer_id=data.customer_id).first()
    db.close()
    if not loan:
        raise HTTPException(status_code=404, detail="Customer not found")

    # 7. Check validation (using graphQL) : 
    transport = RequestsHTTPTransport(url="http://check-validation-service:8002/graphql", verify=False)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql("""
    mutation ValidateCheck($checkAmount: Float!, $signature: Boolean!, $loanAmount: Float!) {
        validateCheck(checkAmount: $checkAmount, signature: $signature, loanAmount: $loanAmount)
    }
    """)

    result = client.execute(query, variable_values={
        "checkAmount": data.check_amount,
        "signature": data.signature,
        "loanAmount": loan.loan_amount
    })
    
    check_valid = result["validateCheck"]
    print(f"Check validation (Graphql result): {check_valid}")

    # If the check is valid, wait 3 seconds, then
    # 8. Notify customer : loan approved

    if check_valid:
        time.sleep(3)
        send_notification(data.customer_id, "From customer-service: Loan approved. Congratulations !")
    else:
        send_notification(data.customer_id, "From customer-service: Loan declined due to invalid check.")

    return {"check_valid": check_valid}

   
