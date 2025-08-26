import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application configuration settings."""
    
    # Flask settings
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    host: str = os.getenv('HOST', '0.0.0.0')
    port: int = int(os.getenv('PORT', '5000'))
    
    # API settings
    api_version: str = os.getenv('API_VERSION', 'v1')
    
    @classmethod
    def load(cls) -> 'Settings':
        """Load settings from environment variables."""
        return cls()