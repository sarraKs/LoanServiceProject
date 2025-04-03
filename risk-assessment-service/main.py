from concurrent import futures
import grpc
import time
import random
import sys

sys.path.append('./generated')  # chemin des fichiers générés
import risk_pb2
import risk_pb2_grpc

class RiskAssessmentServicer(risk_pb2_grpc.RiskAssessmentServicer):
    # Les clients avec un ID pair ont un risque faible, les autres ont un risque élevé
    def AssessCustomerRisk(self, request, context):
        digits = ''.join(filter(str.isdigit, request.customer_id))
        risk_level = "high"
        if digits:
            last_digit = int(digits[-1])
            if last_digit % 2 == 0:
                risk_level = "low"

        print(f"Received risk check for customer {request.customer_id}, returning: {risk_level}")
        return risk_pb2.RiskResponse(
            customer_id=request.customer_id,
            risk_level=risk_level
        )

# La fonction serve() doit être en dehors de la classe
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    risk_pb2_grpc.add_RiskAssessmentServicer_to_server(RiskAssessmentServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC RiskAssessmentService running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
