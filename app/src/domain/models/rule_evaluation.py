from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


@dataclass
class RuleEvaluationRequest:
    """Domain model representing a rules evaluation request."""
    
    observations: Union[Dict[str, Any], List[Dict[str, Any]]]
    version: Optional[str] = None
    request_id: Optional[str] = None


@dataclass
class RuleEvaluationResult:
    """Domain model representing a rules evaluation result."""
    
    result: Union[Dict[str, Any], List[Dict[str, Any]]]
    performance: str
    timestamp: datetime
    api_version: str
    request_id: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()