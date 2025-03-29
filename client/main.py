import requests

# URL of the customer-service API
API_URL_SUBMIT_LOAN = "http://localhost:8000/apply-loan"
API_URL_VALIDATE_CHECK = "http://localhost:8000/validate-check"

# Example loan application data
loan_data = {
    "customer_id": "003",
    "first_name": "Ines",
    "last_name": "Ks",
    "email": "saraks@example.com",
    "phone": "55504558",
    "address": "48 Example Street",
    "loan_type": "commercial",
    "loan_amount": 5000.0,
    "loan_description": "buy a tv"
}

# Send POST request to customer-service to submit a loan
response = requests.post(API_URL_SUBMIT_LOAN, json=loan_data)

# Show response
print("Status Code:", response.status_code)
print("Response:", response.json())

# TODO : Should receive a notification a submit a check

check_data = {
    "customer_id": "003",
    "check_amount": 500.0,
    "signature": True,
}

# Send POST request to customer-service to validate check
response2 = requests.post(API_URL_VALIDATE_CHECK, json=check_data)

# Show response
print("Response2 Status Code:", response2.status_code)
print("Response2:", response2.json())