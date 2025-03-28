from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
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

@app.post("/apply-loan")
def apply_loan(request: LoanRequest):
    db = SessionLocal()

    exists = db.query(CustomerLoanRequest).filter_by(customer_id=request.customer_id).first()
    if exists:
        db.close()
        raise HTTPException(status_code=400, detail="Customer already exists")

    new_request = CustomerLoanRequest(**request.dict())

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    db.close()

    return {"message": "Loan request received", "customer_id": request.customer_id}
