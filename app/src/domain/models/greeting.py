from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Greeting:
    """Domain model representing a greeting message."""
    
    message: str
    timestamp: datetime
    id: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()