# Loan service Application

### server : 

- receives a form submission for loan request
- checks if the loan amount requested is higher than the firm's maximum amount. if yes, decline and notify customer. Else,
- the "customer financial profile" activity is called from a partner service to determine the risk level of the customer. if risk level is "high" and the loan amount >= 20000, decline and notify customer. Else, 
- notify customer to submit check.  
- validate the check. if check not validated, decline the loan and notify customer. Else, 
- request the loan amount from bank and send it to the customer's bank account. notify customer of approval.


### client : 

- calls CustomerService to register and create a new loan. 
- notification : loan declined if the loan amount is higher than maximum firm capacity
- notification : loan declined if risk is high
- notification : asked to submit cashier check, with checkAmount equal to loanAmount/10
- validateCheck : submit check to CustomerService for validation
- notification : loan declined if check not validated, approved if check validated


### A microservices architecture

- CustomerService (REST API) : Handles customer loan application form submission.
- LoanVerificationService (SOAP API) : Checks whether the requested loan amount is lower than the firm's maximum limit. If the amount exceeds the limit, the loan is rejected (NotificationService is called).
- RiskAssessmentService (gRPC API) : Evaluates the customer's financial profile based on banking activity. Returns a risk level (Low, Medium, High). If the risk is High and the loan is >= 20000, the loan is rejected (NotificationService is called).
- CheckValidationService (GraphQL API) : Receives customer's check and validates the check (checkAmount is equal to loanAmount/10 and signature is equal to True). If the check is validated, call BankService. Else the loan is rejected.
- BankService (REST API) : Provides Loan and adds them to the customer’s bank account. And, notifies the customer of the approval of the loan (NotificationService).
- NotificationService (REST API) : Notifies customers about loan approval or rejection.

### Project structure 

- client : Contains a fastAPI server (main.py), a python client (submit_loan.py), docker-compose-client.yml file to deploy the message fastAPI server.
- customer-service : Contains a client model (client_model.py) to communicate with database and a fastAPI server (main.py).
- loan-verification-service : Contains a SOAP webservice (main.py).
- notification-service : Contains a fastAPI server (main.py).
- risk-assessment-service : Contains a gRPC webservice (main.py).
- check-validation-service : Contains a graphQL webservice (main.py).
- bank-service : Contains a fastAPI server (main.py).
- docker-compose.yml : file to deploy the microservices application. 
- APIs_Documentation.md : documentation of the APIs used.

### Remarks 

- The CustomerService is the only microservice with which the client communicates. 
- The risk level determination (Low, Medium, High) is simplified for this version of the application. All customers with an odd ID (impair) have a "high" risk level. And customers with an even ID (pair) have a "low" risk level.
- The client is composed of two parts : 
    - main.py : a fastAPI messages server that receives notifications of all customers from the application and prints them.
    - submit-loan.py : a python client that can send POST requests to the application.  
- The notificationService sends POST requests to the clients message server "ClientService". 
- We use a Postgres database to store the loan and customer information. You need to run the application with a different customer_id each time, because a loan request cannot be submitted by an already existing customer_id.
- We coded four different customers in the client code to be able to run the four different scenarios. You need to modify the IDs to be able to run the scenario another time, then rebuild the client messages server. 

### How to run the application 

- install docker compose in your machine.

- clone this repository and go to the project folder. 

- create a docker network : 

    `docker network create loan-net`

- run the microservices application : 

    `docker compose -f docker-compose.yml up --build`

- run the "client messages server" in another terminal : 

    `docker compose -f client/docker-compose-client.yml up --build`

- run the client python file to start the scenario : 

    `docker exec -it client_service python submit_loan.py`
    
- You can modify the following customer variables in submit_loan.py and rebuild the "client messages server" to run different scenarios : 

    - customer_id
    - loan_amount
    - check_amount
    - check_signature

### Q&A 

- To install the requirements of a microservice: 
    
    `pip install -r requirements.txt`

- To run only the customer-service in local :

    ```
    cd customer-service 
    uvicorn main:app --reload
    ```

- To verify data existence in postgres database :

    `docker exec -it loan_postgres psql -U user1 -d loans_db`

- In the following database prompt : loans_db=#

    `SELECT * FROM loan_requests;`

- To quit database :

    `\q`











