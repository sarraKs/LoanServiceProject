import grpc
import sys
sys.path.append('./generated')

import risk_pb2
import risk_pb2_grpc

def test_risk_service(customer_id):
    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = risk_pb2_grpc.RiskAssessmentStub(channel)
        request = risk_pb2.RiskRequest(customer_id=customer_id)
        response = stub.AssessCustomerRisk(request)
        print(f"✔️ Risk level for customer '{customer_id}': {response.risk_level}")
    except Exception as e:
        print(f"❌ Error during gRPC call: {e}")

if __name__ == "__main__":
    test_risk_service("15")
    test_risk_service("2")
