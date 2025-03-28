from sqlalchemy import Column, String, Float, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class LoanTypeEnum(enum.Enum):
    personal = "personal"
    commercial = "commercial"

class CustomerLoanRequest(Base):
    __tablename__ = "loan_requests"

    customer_id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    loan_type = Column(Enum(LoanTypeEnum), nullable=False)
    loan_amount = Column(Float, nullable=False)
    loan_description = Column(Text, nullable=True)
