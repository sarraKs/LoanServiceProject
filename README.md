# Loan service Application

### server : 

- receives a form submission for loan
- checks if the loan requested is higher than the maximum amount. if yes, decline and notify customer. Else,
- the "customer financial profile" activity is called from a partner service to determine the risk level of the customer. if risk level is "high" and the loan amount >= 20000, decline and notify customer. Else, 
- notify customer to submit check.  
- contact bank service to validate check. if check not validated, decline the loan and notify customer. Else, 
- request the loan amount from provider and send it to the customer's bank account. notify customer of approval.


### client : 
- calls CustomerService to register and create a new loan. 
- notification : loan declined if the loan amount is high than maximum firm capacity
- notification : loan declined if risk is high
- notification : asked to submit cashier check
- validateCheck : submit check (call CustomerService ?) for validation
- notification : loan declined if check not validated, approved if check validated


### A microservices architecture

- CustomerService (REST API) : Handles customer registration and loan application form submission.
- LoanVerificationService (SOAP API) : Checks whether the requested loan amount is lower than the firm's maximum limit. If the amount exceeds the limit, the loan is rejected (NotificationService is called).
- RiskAssessmentService (gRPC API) : Evaluates the customer's financial profile based on banking activity. Returns a risk level (Low, Medium, High). If the risk is High and the loan is >= 20000, the loan is rejected (NotificationService is called).
- CheckValidationService (GraphQL API) : Requests a cashier's check from the customer. Then, validates the check with a bank service. 
- BankService (SOAP API) : If the check is validated, it requests funds from a Loan Provider Service and adds them to the customer’s bank account. And, notifies the customer of the approval of the loan (NotificationService).
- NotificationService (REST API) : Notifies customers about loan approval or rejection via email/SMS.

### How to run the application 

- install the requirements : 
    
    pip install -r requirements.txt

- From within the customer-service/ folder, run:

    uvicorn main:app --reload











