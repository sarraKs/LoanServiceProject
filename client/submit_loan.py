import requests

# === Configuration ===
API_SUBMIT_LOAN = "http://customer-service:8000/apply-loan"
API_VALIDATE_CHECK = "http://customer-service:8000/validate-check"


def validate_check(customer_id: str, message: str):
    
    print(f"Notification to customer {customer_id}: {message}")

    check_amount = 2500.0
    check_signature = True
    print(f"Submitting check of {check_amount} for validation...")
    
    check_data = {
        "customer_id": customer_id,
        "check_amount": check_amount,
        "signature": check_signature
    }

    requests.post(API_VALIDATE_CHECK, json=check_data)


#def main():
if __name__ == "__main__":
    # === Example customer input ===
    customer_id = "77"
    loan_amount = 25000.0

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
    print(f"Customer {customer_id} submitting a new loan request...")

    requests.post(API_SUBMIT_LOAN, json=loan_data)
