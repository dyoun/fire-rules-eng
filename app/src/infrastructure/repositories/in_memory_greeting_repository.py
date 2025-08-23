from typing import Dict, List, Optional
import uuid
from ...domain.interfaces.greeting_repository import IGreetingRepository
from ...domain.models.greeting import Greeting


class InMemoryGreetingRepository(IGreetingRepository):
    """In-memory implementation of the greeting repository."""
    
    def __init__(self):
        self._greetings: Dict[str, Greeting] = {}
    
    def get_by_id(self, greeting_id: str) -> Optional[Greeting]:
        """Retrieve a greeting by its ID."""
        return self._greetings.get(greeting_id)
    
    def get_all(self) -> List[Greeting]:
        """Retrieve all greetings."""
        return list(self._greetings.values())
    
    def save(self, greeting: Greeting) -> Greeting:
        """Save a greeting and return it with generated ID if applicable."""
        if greeting.id is None:
            greeting.id = str(uuid.uuid4())
        
        self._greetings[greeting.id] = greeting
        return greeting