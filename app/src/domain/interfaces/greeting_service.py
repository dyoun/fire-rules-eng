from abc import ABC, abstractmethod
from typing import List
from ..models.greeting import Greeting


class IGreetingService(ABC):
    """Interface for greeting business logic operations."""
    
    @abstractmethod
    def create_hello_world_greeting(self) -> Greeting:
        """Create a standard 'Hello World' greeting."""
        pass
    
    @abstractmethod
    def create_custom_greeting(self, message: str) -> Greeting:
        """Create a custom greeting with provided message."""
        pass
    
    @abstractmethod
    def get_all_greetings(self) -> List[Greeting]:
        """Retrieve all stored greetings."""
        pass