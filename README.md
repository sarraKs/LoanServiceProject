# use cases :

### server : 
- newLoanRequest (REST ?) : creates a new loan request with the form information. check if the loan requested is higher than the maximum amount. if yes, cancel and notify customer. else, call : 
- checkRisk (SOAP ?) : the "customer financial profile" activity is called from a partner service to determine the risk level of the customer. if risk level is "high" and the loan amount >= 20000, cancel and notify customer. else, notify customer to submit check.  
- validateCheck : contact bank service to validate check. if check not validated, cancel the loan and notify customer. else, call : 
- requestLoanAmount : request the loan amount from provider and send it to the customer's bank account. notify customer of approval.


### client : 
- calls newLoanRequest to create a new loan. notification : loan cancelled if the loan amount is very high
- notification : loan cancelled if risk is high
- notification : asked to submit check
- validateCheck : submit check for validation
- notification : declined if check not validated, approved if check validated














