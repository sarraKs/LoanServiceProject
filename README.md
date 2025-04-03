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
- BankService (REST API) : Provides Loan and adds them to the customer’s bank account. And, notifies the customer of the approval of the loan (NotificationService).
- NotificationService (REST API) : Notifies customers about loan approval or rejection via email/SMS.

### How to run the application 

- install docker compose in your machine.

- clone this repository and go to the project folder. 

- create a docker network : 

    `docker network create loan-net`

- run the microservices application : 

    `docker compose -f docker-compose.yml up --build`

- run the client service in another terminal : 

    `docker compose -f client/docker-compose-client.yml up --build`

- Alternative (run the two client parts in different terminals): 

    ```
    run the app : docker compose -f docker-compose.yml up --build 
    run the client fastapi main.py : docker compose -f client/docker-compose-client.yml up --build 
    run the client submit_loan.py to start the scenario : docker exec -it client_service python submit_loan.py
    ```

### Q&A 

- To install the requirements of a microservice: 
    
    `pip install -r requirements.txt`

- To run only the customer-service in local :

    ```
    cd customer-service 
    uvicorn main:app --reload
    ```

- To run the client : 

    ```
    cd client
    python main.py
    ```

- To confirm data in postgres database :

    `docker exec -it loan_postgres psql -U user1 -d loans_db`

- In the following database prompt : loans_db=#

    `SELECT * FROM loan_requests;`

- To quit database :

    `\q`











