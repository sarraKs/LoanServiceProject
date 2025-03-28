from concurrent import futures
import grpc
import time
import random
import sys

sys.path.append('./generated') #chemin des fichiers générés
import risk_pb2
import risk_pb2_grpc

class RiskAssessmentServicer(risk_pb2_grpc.RiskAssessmentServicer):

    def AssessCustomerRisk(self, request, context):
        # Extraire les chiffres de l'ID client
        digits = ''.join(filter(str.isdigit, request.customer_id))

        # Par défaut : risque élevé
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
