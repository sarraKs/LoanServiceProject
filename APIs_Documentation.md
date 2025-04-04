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

## 1. customer-service (REST service)

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
  - `Loan amount exceeds allowed limit.`
  - `Customer already exists.`

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

## 2. check-validation-service (GraphQL service)

### **GraphQL Endpoint**: `/graphql`

#### Mutation: `validateCheck`

_Validates the cashier's check and calls the bank service if successful._

#### Request (GraphQL)

```graphql
mutation {
  validateCheck(checkAmount: 2500.0, signature: true, loanAmount: 25000.0)
}
```

#### Response

```json
{
  "data": {
    "validateCheck": true
  }
}
```

> A valid check will trigger a GET request to the bank-service.

---
## 3. loan-verification-service (SOAP service)

### **SOAP Endpoint**: `http://localhost:8001/?wsdl`

SOAP method used to verify if the loan amount is acceptable.

#### Method: `loan_amount_acceptation(customer_id: string, amount: float) -> bool`

- Returns `true` if `amount <= 50000.0`
- Else returns `false`

---
## 4. risk-assessment-service (gRPC service)

### **gRPC Port**: `50051`

Determines customer risk based on the last digit of the `customer_id`.

#### Request

```proto
message RiskRequest {
  string customer_id = 1;
}
```

#### Response

```proto
message RiskResponse {
  string customer_id = 1;
  string risk_level = 2; // "low" or "high"
}
```

- Even-numbered IDs → low risk
- Odd-numbered IDs → high risk

---
## 5. notification-service 

### **POST** `/notify`

_For general notifications (loan approved, declined, etc.)_

```json
{
  "customer_id": "122",
  "message": "Your loan has been approved"
}
```

### **POST** `/request-check`

_Used to ask a customer to submit a cashier's check._

```json
{
  "customer_id": "122",
  "message": "Please submit a check of 2500.00"
}
```
---
## 6. bank-service

### **GET** `/provide-loan?loan_amount=<amount>`

Simulates transferring the loan amount to the customer’s account.

#### Example

```
GET /provide-loan?loan_amount=25000.0
```

#### Response

```json
{
  "message": "Loan amount 25000.0 added to customer bank account"
}
```
---

## Test Scenarios (client.py)

| Customer ID | Description                                        |
|-------------|----------------------------------------------------|
| `94`        | Valid loan, low risk, valid check → **Approved**   |
| `95`        | Loan amount too high → **Declined**                |
| `96`        | Valid amount, but check is invalid → **Declined**  |
| `97`        | High risk profile & high loan amount → **Declined**|


