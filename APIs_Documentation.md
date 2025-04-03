# Loan Microservices System — Full API Documentation

This project is a complete loan approval system composed of several microservices communicating over REST, gRPC, SOAP, and GraphQL.

---

## Microservices Overview

| Service                | Port   | Description                                      |
|------------------------|--------|--------------------------------------------------|
| customer-service       | 8000   | REST service: Orchestrates loan applications and logic         |
| loan-verification      | 8001   | SOAP service: verifies max loan amount           |
| check-validation       | 8002   | GraphQL service: validates check info            |
| notification-service   | 8003   | Sends notifications to client                    |
| bank-service           | 8004   | Deposits loan to bank account                    |
| client-service         | 8005   | Client simulation to send loan requests          |
| risk-assessment        | 50051  | gRPC: Assesses customer risk                     |

---

## 1. customer-service

**POST** `/apply-loan`  
_Submits a new loan application_

### Request body

```json
{
  "customer_id": "122",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "55522",
  "address": "86 Example Street",
  "loan_type": "personal",
  "loan_amount": 25000.0,
  "loan_description": "Buy a car"
}
```

### Responses

- **200 OK**  
- Loan accepted, waiting for check validation.
 ```json
{
  "message": "Loan request successfully processed",
  "customer_id": "134",
  "risk_level": "low",
  "loan_amount": 25000.0,
  "loan_type": "personal",
  "status": "pending check validation"
}
```

- **400 Bad Request**  
  - "Loan amount exceeds allowed limit."
  - "Customer already exists".

---

**POST** `/validate-check`  
_Validates the cashier's check submitted by the customer._

### Request body

```json
{
  "customer_id": "122",
  "check_amount": 2500.0,
  "signature": true
}
```

###  Responses

- **200 OK**  
  `{ "check_valid": true | false }`



