from dependency_injector import containers, providers
from ..domain.interfaces.greeting_repository import IGreetingRepository
from ..domain.interfaces.greeting_service import IGreetingService
from ..infrastructure.repositories.in_memory_greeting_repository import InMemoryGreetingRepository
from ..application.services.greeting_service import GreetingService


class Container(containers.DeclarativeContainer):
    """Dependency injection container."""
    
    # Configuration
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.controllers.greeting_controller"
        ]
    )
    
    # Repositories
    greeting_repository = providers.Singleton(InMemoryGreetingRepository)
    
    # Services  
    greeting_service = providers.Factory(
        GreetingService,
        greeting_repository=greeting_repository
    )