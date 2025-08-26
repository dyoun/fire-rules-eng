from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.greeting import Greeting


class IGreetingRepository(ABC):
    """Interface for greeting data access operations."""
    
    @abstractmethod
    def get_by_id(self, greeting_id: str) -> Optional[Greeting]:
        """Retrieve a greeting by its ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Greeting]:
        """Retrieve all greetings."""
        pass
    
    @abstractmethod
    def save(self, greeting: Greeting) -> Greeting:
        """Save a greeting and return it with generated ID if applicable."""
        pass