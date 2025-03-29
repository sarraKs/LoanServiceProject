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
- notification : loan declined if the loan amount is higher than maximum firm capacity
- notification : loan declined if risk is high
- notification : asked to submit cashier check, with checkAmount equal to loanAmount/10
- validateCheck : submit check (call CustomerService ?) for validation
- notification : loan declined if check not validated, approved if check validated


### A microservices architecture

- CustomerService (REST API) : Handles customer registration and loan application form submission.
- LoanVerificationService (SOAP API) : Checks whether the requested loan amount is lower than the firm's maximum limit. If the amount exceeds the limit, the loan is rejected (NotificationService is called).
- RiskAssessmentService (gRPC API) : Evaluates the customer's financial profile based on banking activity. Returns a risk level (Low, Medium, High). If the risk is High and the loan is >= 20000, the loan is rejected (NotificationService is called).
- CheckValidationService (GraphQL API) : Receives customer's check and validates the check (checkAmount is equal to loanAmount/10 and signature is equal to True). If the check is validated, call BankService. Else the loan is rejected.
- BankService (SOAP API) : Provides Loan and adds them to the customer’s bank account. And, notifies the customer of the approval of the loan (NotificationService).
- NotificationService (REST API) : Notifies customers about loan approval or rejection via email/SMS.

### How to run the application 

- install the requirements : 
    
    pip install -r requirements.txt

- From within the customer-service folder, run:

    uvicorn main:app --reload

- From within the client folder, run : 

    python main.py

- To confirm data in db :

    docker exec -it loan_postgres psql -U user1 -d loans_db

- in the following prompt : loans_db=#

    SELECT * FROM loan_requests;

- to quit database :

    \q


- Steps to run the app : 

    -  Launch the soap service : 
        - cd loan-verification-service
        - python3 main.py
    - Launch the GRPC service : 
        - cd risk-assessment-service
        - python3 main.py
    - Launch the customer service : 









