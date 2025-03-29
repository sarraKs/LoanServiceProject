import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI


@strawberry.type
class Query:
    hello: str = "CheckValidationService running"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def validate_check(self, check_amount: float, signature: bool, loan_amount: float) -> bool:
        return round(check_amount, 2) == round(loan_amount / 10, 2) and signature

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

