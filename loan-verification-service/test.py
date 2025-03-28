from zeep import Client

client = Client("http://localhost:8001/?wsdl")

customer_id = "27"
amount = 550

result = client.service.loan_amount_acceptation(customer_id, float(amount))

print("Résultat SOAP :", result)
