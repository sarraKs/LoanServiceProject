import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
import requests

BANK_SERVICE_URL = "http://bank-service:8004/provide-loan"

@strawberry.type
class Query:
    hello: str = "CheckValidationService running"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def validate_check(self, check_amount: float, signature: bool, loan_amount: float) -> bool:
        
        is_valid = round(check_amount, 2) == round(loan_amount / 10, 2) and signature

        if is_valid:
            try:
                response = requests.get(f"{BANK_SERVICE_URL}?loan_amount={loan_amount}")
                print("BankService response:", response.json())
            except Exception as e:
                print("Error calling BankService:", e)

        return is_valid
    

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

