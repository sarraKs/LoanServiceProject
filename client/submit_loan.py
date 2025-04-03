import time
import requests


API_SUBMIT_LOAN = "http://customer-service:8000/apply-loan"
API_VALIDATE_CHECK = "http://customer-service:8000/validate-check"

# This is the code of the client. You can modify the customer_id and loan info to have different responses from the application

def validate_check(customer_id: str, message: str):
    
    print(f"Notification to customer {customer_id}: {message}")

    # Each customer submits a different check_amount

    check_amount = 100.0 #default
    check_signature = True #default

    if (customer_id == "94"): # For this customer, the check should be valid
        check_amount = 150.0
        check_signature = True
    elif (customer_id == "96"): # For this customer, the check should be declined
        check_amount = 2300.0
        check_signature = True

    print(f"Submitting check of {check_amount} for validation...")
    
    check_data = {
        "customer_id": customer_id,
        "check_amount": check_amount,
        "signature": check_signature
    }

    requests.post(API_VALIDATE_CHECK, json=check_data)


# We coded 4 example customers to be able to see all the different scenarios

if __name__ == "__main__":
   
    
    # This customer submits a loan request that will be approved
    customer_id = "94"
    loan_amount = 1500.0

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

    print(f"Customer {customer_id} submitting a new loan request...")
    requests.post(API_SUBMIT_LOAN, json=loan_data)

    # Wait 8 seconds between two customer scenarios to have a clean client prompt
    time.sleep(8)

    # This customer submits a loan request with a very high amount. It will be declined
    customer_id = "95"
    loan_amount = 55000.0

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

    print(f"Customer {customer_id} submitting a new loan request...")
    requests.post(API_SUBMIT_LOAN, json=loan_data)

    # Wait 8 seconds between two customer scenarios to have a clean client prompt
    time.sleep(8)

    # This customer submits a loan request but the customer's profile has a high risk, and the amount exceeds 20000. I will be declined
    customer_id = "97" # All customers with an ID impair have a high risk profile
    loan_amount =25000.0

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

    print(f"Customer {customer_id} submitting a new loan request...")
    requests.post(API_SUBMIT_LOAN, json=loan_data)

    # Wait 8 seconds between two customer scenarios to have a clean client prompt
    time.sleep(8)

    # This customer submits a loan request but the cashier's check has a wrong amount. I will be declined
    customer_id = "96"
    loan_amount =25000.0

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

    print(f"Customer {customer_id} submitting a new loan request...")
    requests.post(API_SUBMIT_LOAN, json=loan_data)
