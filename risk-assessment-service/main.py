from concurrent import futures
import grpc
import time
import random

import risk_pb2
import risk_pb2_grpc

class RiskAssessmentServicer(risk_pb2_grpc.RiskAssessmentServicer):

    def AssessCustomerRisk(self, request, context):
        # Simuler une logique de risque
        risk_level = random.choice(["low", "high"])
        print(f"Received risk check for customer {request.customer_id}, returning: {risk_level}")
        return risk_pb2.RiskResponse(
            customer_id=request.customer_id,
            risk_level=risk_level
        )
