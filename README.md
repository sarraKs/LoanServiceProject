# Loan service Application

### server : 
- customerLoanRequest (REST) : creates a new loan request with the form information. check if the loan requested is higher than the maximum amount. if yes, cancel and notify customer. else, call : 
- checkRisk (SOAP) : the "customer financial profile" activity is called from a partner service to determine the risk level of the customer. if risk level is "high" and the loan amount >= 20000, cancel and notify customer. else, notify customer to submit check.  
- validateCheck (gRPC): contact bank service to validate check. if check not validated, cancel the loan and notify customer. else, call : 
- requestLoanAmount : request the loan amount from provider and send it to the customer's bank account. notify customer of approval.


### client : 
- calls newLoanRequest to create a new loan. notification : loan cancelled if the loan amount is very high
- notification : loan cancelled if risk is high
- notification : asked to submit check
- validateCheck : submit check for validation
- notification : declined if check not validated, approved if check validated


### A microservices architecture

- CustomerService (REST API) : Handles customer loan application form submission.
- LoanVerificationService (SOAP API) : Checks whether the requested loan amount is lower than the firm's maximum limit. If the amount exceeds the limit, the loan is rejected (NotificationService is called).
- RiskAssessmentService (gRPC API) : Evaluates the customer's financial profile based on banking activity. Returns a risk level (Low, Medium, High). If the risk is High and the loan is >= 20000, the loan is rejected (NotificationService is called).
- CheckValidationService (GraphQL API) : Requests a cashier's check from the customer. Then, validates the check with a bank service. 
- BankService (SOAP API) : If the check is validated, it requests funds from a Loan Provider Service and adds them to the customer’s bank account. And, notifies the customer of the approval of the loan (NotificationService).
- NotificationService (REST API) : Notifies customers about loan approval or rejection via email/SMS.










