package chechRiskService;

public class RiskEvaluator {
	
	public String checkRisk(String customerId) {
		
        // on retourne "high" pour les ID impairs et "low" pour les ID pairs
		
        int id = Integer.parseInt(customerId);
        if (id % 2 == 1) {
            return "high";
        } else {
            return "low";
        }
    }

}
