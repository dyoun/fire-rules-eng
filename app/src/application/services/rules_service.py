import json
import os
import zen
from datetime import datetime
from ...domain.interfaces.rules_service import IRulesService
from ...domain.models.rule_evaluation import RuleEvaluationRequest, RuleEvaluationResult


class RulesService(IRulesService):
    """Service implementation for rules engine operations."""
    
    def __init__(self, rules_file_path: str = None):
        self.engine = zen.ZenEngine()
        # Default to src/rules/fire-risk.json relative to the service file location
        if rules_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.rules_file_path = os.path.join(current_dir, '..', '..', 'rules', 'fire-risk.json')
        else:
            self.rules_file_path = rules_file_path
    
    def evaluate_fire_risk(self, request: RuleEvaluationRequest) -> RuleEvaluationResult:
        """Evaluate fire risk rules against provided observations."""
        try:
            # Load rule definition from file
            if not os.path.exists(self.rules_file_path):
                raise FileNotFoundError(f"Rules file not found: {self.rules_file_path}")
            
            with open(self.rules_file_path, 'r') as f:
                rule_json = f.read()
            
            # Create decision from rule definition
            decision = self.engine.create_decision(rule_json)
            
            # Evaluate against observations
            result = decision.evaluate(request.observations)
            
            return RuleEvaluationResult(
                result=result.get('result', {}),
                performance=result.get('performance', ''),
                timestamp=datetime.utcnow(),
                request_id=request.request_id
            )
        except Exception as e:
            raise RuntimeError(f"Failed to evaluate rules: {str(e)}") from e