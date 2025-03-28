from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import grpc
import sys
sys.path.append("./risk-assessment-service/generated")  # chemin vers les fichiers générés
import risk_pb2
import risk_pb2_grpc
from zeep import Client
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from customer_model import Base, CustomerLoanRequest, LoanTypeEnum
import os

app = FastAPI()

# PostgreSQL database setup
DB_USER = os.getenv("DB_USER", "user1")
DB_PASS = os.getenv("DB_PASS", "password1")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "loans_db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

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

@app.get("/")
def root():
    return {"message": "CustomerService with PostgreSQL is running"}

# ---------- Endpoint REST ----------

@app.post("/apply-loan")
def apply_loan(request: LoanRequest):
    db = SessionLocal()

    exists = db.query(CustomerLoanRequest).filter_by(customer_id=request.customer_id).first()
    if exists:
        db.close()
        raise HTTPException(status_code=400, detail="Customer already exists")
    
    # Appel SOAP pour vérifier le montant
    if not check_loan_amount(request.customer_id, request.loan_amount):
        db.close()
        raise HTTPException(status_code=400, detail="Loan amount exceeds allowed limit")

    # Appel GRPC pour vérifier le risque 
    risk_level = get_customer_risk(request.customer_id)
    if risk_level == "high" and request.loan_amount >= 20000:
        db.close()
        raise HTTPException(status_code=400, detail="Loan rejected due to high risk")
    
    new_request = CustomerLoanRequest(**request.dict())

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    db.close()

    return {"message": "Loan request received", "customer_id": request.customer_id, "risk_level":risk_level}

#-----------------------SOAP client ------------------
def check_loan_amount(customer_id: str, amount: float) -> bool:
    try:
        wsdl_url = "http://localhost:8001/?wsdl"  # SOAP service WSDL
        client = Client(wsdl=wsdl_url)
        return client.service.loan_amount_acceptation(customer_id, amount)
    except Exception as e:
        print("SOAP Error:", e)
        return False  # on rejette si le service échoue


#-----------------------GRPC Client--------------------
def get_customer_risk(customer_id: str) -> str:
    try:
        channel = grpc.insecure_channel('localhost:50051')  # Port de ton service gRPC
        stub = risk_pb2_grpc.RiskAssessmentStub(channel)
        request = risk_pb2.RiskRequest(customer_id=customer_id)
        response = stub.AssessCustomerRisk(request)
        return response.risk_level  # "low" ou "high"
    except Exception as e:
        print("gRPC Error:", e)
        return "high"  # par défaut on rejette si le service échoue

   
