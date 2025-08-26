from abc import ABC, abstractmethod
from ..models.rule_evaluation import RuleEvaluationRequest, RuleEvaluationResult


class IRulesService(ABC):
    """Interface for rules engine business logic operations."""
    
    @abstractmethod
    def evaluate_fire_risk(self, request: RuleEvaluationRequest) -> RuleEvaluationResult:
        """Evaluate fire risk rules against provided observations."""
        pass