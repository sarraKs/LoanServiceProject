import requests

# URL of the customer-service API
API_URL = "http://localhost:8000/apply-loan"

# Example loan application data
loan_data = {
    "customer_id": "001",
    "first_name": "Yakine",
    "last_name": "Klabi",
    "email": "yakineklabi@example.com",
    "phone": "55500000",
    "address": "42 Example Street",
    "loan_type": "personal",
    "loan_amount": 10000,
    "loan_description": "start a small business"
}

# Send POST request to customer-service
response = requests.post(API_URL, json=loan_data)

# Show response
print("Status Code:", response.status_code)
print("Response:", response.json())
