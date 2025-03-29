import requests

# URLs for the customer-service API
API_URL_SUBMIT_LOAN = "http://localhost:8000/apply-loan"
API_URL_VALIDATE_CHECK = "http://localhost:8000/validate-check"

# Example loan data to submit
loan_data = {
    "customer_id": "008",
    "first_name": "Amelie",
    "last_name": "Mre",
    "email": "amelie@example.com",
    "phone": "5552444",
    "address": "86 Example Street",
    "loan_type": "personal",
    "loan_amount": 15000.0,
    "loan_description": "i just want a loan"
}

# Submit loan request
response = requests.post(API_URL_SUBMIT_LOAN, json=loan_data)

print("Submit Loan Status Code:", response.status_code)
try:
    print("Submit Loan Response:", response.json())
except Exception:
    print("Submit Loan Response Error: Could not decode JSON")

# SHOULD RECEIVE NOTIFICATION HERE TO SUBMIT A CHECK 
# THE VALIDATE CHECK REQUEST SHOULD ONLY BE MADE IF THIS NOTIFICATION ARRIVES 

# Example check data to submit and validate
check_data = {
    "customer_id": "008",
    "check_amount": 1500.0,
    "signature": True,
}

# Validate the check
response2 = requests.post(API_URL_VALIDATE_CHECK, json=check_data)

print("Validate Check Status Code:", response2.status_code)
try:
    print("Validate Check Response:", response2.json())
except Exception:
    print("Validate Check Response Error: Could not decode JSON")
