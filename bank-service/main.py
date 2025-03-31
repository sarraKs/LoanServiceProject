from fastapi import FastAPI

app = FastAPI()

@app.get("/provide-loan")
def provide_loan(loan_amount: float):
    print(f"Loan amount {loan_amount} added to customer bank account.")
    return {"message": f"Loan amount {loan_amount} added to customer bank account"}
