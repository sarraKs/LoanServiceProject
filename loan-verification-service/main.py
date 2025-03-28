# loan-verification-service/main.py
from spyne import Application, rpc, ServiceBase, Unicode, Float, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class LoanVerificationService(ServiceBase):
    
    @rpc(Unicode, Float, _returns=Boolean)
    def loan_amount_acceptation(ctx, customer_id, amount):
        MAX_LOAN_AMOUNT = 50000
        if amount <= MAX_LOAN_AMOUNT:
            return True
        return False

application = Application(
    [LoanVerificationService],
    tns='loan.verification.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8001, wsgi_app)
    print("SOAP Loan Verification Service running on http://localhost:8001")
    server.serve_forever()
