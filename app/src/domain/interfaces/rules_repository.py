from abc import ABC, abstractmethod


class IRulesRepository(ABC):
    """Interface for rules definition data access operations."""
    
    @abstractmethod
    def get_fire_risk_rules(self) -> str:
        """Retrieve fire risk rule definitions as JSON string."""
        pass