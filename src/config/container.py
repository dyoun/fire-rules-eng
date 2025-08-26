from dependency_injector import containers, providers
from ..domain.interfaces.greeting_repository import IGreetingRepository
from ..domain.interfaces.greeting_service import IGreetingService
from ..domain.interfaces.rules_service import IRulesService
from ..infrastructure.repositories.in_memory_greeting_repository import InMemoryGreetingRepository
from ..application.services.greeting_service import GreetingService
from ..application.services.rules_service import RulesService


class Container(containers.DeclarativeContainer):
    """Dependency injection container."""
    
    # Configuration
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.controllers.greeting_controller",
            "src.presentation.controllers.rules_controller"
        ]
    )
    
    # Repositories
    greeting_repository = providers.Singleton(InMemoryGreetingRepository)
    
    # Services  
    greeting_service = providers.Factory(
        GreetingService,
        greeting_repository=greeting_repository
    )
    
    rules_service = providers.Factory(RulesService)