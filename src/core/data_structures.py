"""
Core data models & structures
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RequestModel:
    """Base request model for API requests"""
    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    data: Optional[Any] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ResponseModel:
    """Base response model for API responses"""
    status_code: int
    data: Any
    headers: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None


@dataclass
class ConfigModel:
    """Configuration data model"""
    api_url: str
    api_key: Optional[str] = None
    timeout: int = 30
    retry_count: int = 3
    settings: Dict[str, Any] = field(default_factory=dict)
