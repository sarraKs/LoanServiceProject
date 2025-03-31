import requests

# === Configuration ===
BASE_URL = "http://localhost:8000"
NOTIF_URL = "http://localhost:8003/notify"

API_SUBMIT_LOAN = f"{BASE_URL}/apply-loan"
API_VALIDATE_CHECK = f"{BASE_URL}/validate-check"

# === Example customer input ===
customer_id = "54"
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

def send_notification(customer_id, message, channel="email"):
    payload = {
        "customer_id": customer_id,
        "channel": channel,
        "message": message
    }
    try:
        res = requests.post(NOTIF_URL, json=payload)
        if res.status_code == 200:
            print(f"NOTIFICATION → {message}")
        else:
            print(f"Failed to notify: {res.text}")
    except Exception as e:
        print(f"Notification error: {e}")


# === STEP 1 — Submit loan ===
print("Submitting loan request...")
#send_notification(customer_id, "Submitting loan request...")

loan_submit_response = requests.post(API_SUBMIT_LOAN, json=loan_data)
print("Loan submit Response Status:", loan_submit_response)
print("Loan submit Response:", loan_submit_response.json())

"""
if loan_submit_response.status_code != 200:
    #send_notification(customer_id, "Loan declined ")
    print(" Loan rejected. Process stopped.")
    exit()

loan_response = response.json()
send_notification(customer_id, "Loan request approved (pre-check)")
print("Loan approved for next step.")
"""


# === STEP 2 — Notification to submit check ===
"""
required_check_amount = loan_amount / 10
check_message = f"Please submit a cashier's check of {required_check_amount:.2f} €"
send_notification(customer_id, check_message)
print(f"{check_message}")
time.sleep(1.5)"

"""

# === STEP 3 — Validate check ===
check_amount = 5500.0
print("Submitting check for validation...")
check_data = {
    "customer_id": customer_id,
    "check_amount": check_amount,
    "signature": True
}

check_validation_response = requests.post(API_VALIDATE_CHECK, json=check_data)
print("Check Validation Response Status:", check_validation_response.status_code)
print("Check Validation Response:", check_validation_response.json())

"""
if check_validation_response.status_code != 200:
    send_notification(customer_id, "Check validation failed ")
    print(" Check validation error. Process stopped.")
    exit()

if check_validation_response.get("check_valid"):
    send_notification(customer_id, "Loan approved Funds will be transferred.")
    print(" Loan fully approved and check validated.")
else:
    send_notification(customer_id, "Loan rejected : invalid check.")
    print(" Loan rejected due to check.")
"""