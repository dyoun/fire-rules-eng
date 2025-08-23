from datetime import datetime
from typing import List
from ...domain.interfaces.greeting_service import IGreetingService
from ...domain.interfaces.greeting_repository import IGreetingRepository
from ...domain.models.greeting import Greeting


class GreetingService(IGreetingService):
    """Service implementing greeting business logic."""
    
    def __init__(self, greeting_repository: IGreetingRepository):
        self._greeting_repository = greeting_repository
    
    def create_hello_world_greeting(self) -> Greeting:
        """Create a standard 'Hello World' greeting."""
        greeting = Greeting(
            message="Hello World!",
            timestamp=datetime.utcnow()
        )
        return self._greeting_repository.save(greeting)
    
    def create_custom_greeting(self, message: str) -> Greeting:
        """Create a custom greeting with provided message."""
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        greeting = Greeting(
            message=message.strip(),
            timestamp=datetime.utcnow()
        )
        return self._greeting_repository.save(greeting)
    
    def get_all_greetings(self) -> List[Greeting]:
        """Retrieve all stored greetings."""
        return self._greeting_repository.get_all()