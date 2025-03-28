from fastapi import FastAPI
from starlette.graphql import GraphQLApp
import graphene

class ValidateCheck(graphene.Mutation):
    class Arguments:
        check_amount = graphene.String(required=True)
        signature = graphene.Boolean(required=True)
        loan_amount = graphene.Float(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, check_amount, signature, loan_amount):
        try:
            valid = float(check_amount) == loan_amount / 10 and signature
        except ValueError:
            valid = False
        return ValidateCheck(ok=valid)

class Mutation(graphene.ObjectType):
    validate_check = ValidateCheck.Field()

schema = graphene.Schema(mutation=Mutation)

app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=schema))
