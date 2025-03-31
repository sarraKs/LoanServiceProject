import requests

# === Configuration ===
API_SUBMIT_LOAN = "http://customer-service:8000/apply-loan"
API_VALIDATE_CHECK = "http://customer-service:8000/validate-check"


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


def main():
    # === Example customer input ===
    customer_id = "56"
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

    # === STEP 1 — Submit loan ===
    print("Submitting loan request...")

    requests.post(API_SUBMIT_LOAN, json=loan_data)
    