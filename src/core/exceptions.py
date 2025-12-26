"""
Custom exception classes for the SDK
"""
from typing import Optional, Dict, Any


class SDKError(Exception):
    """Base exception for all SDK errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(SDKError):
    """Raised when there's a configuration error"""
    pass


class AuthenticationError(SDKError):
    """Raised when authentication fails"""
    pass


class ConnectionError(SDKError):
    """Raised when connection to external service fails"""
    pass


class ValidationError(SDKError):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = str(value)
        super().__init__(message, details)
        self.field = field
        self.value = value


class APIError(SDKError):
    """Raised when API request fails"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None
    ):
        details = {}
        if status_code:
            details["status_code"] = status_code
        if response:
            details["response"] = response
        super().__init__(message, details)
        self.status_code = status_code
        self.response = response


class DatabaseError(SDKError):
    """Raised when database operation fails"""
    pass


class CodecError(SDKError):
    """Raised when encoding/decoding fails"""
    pass


class AgentError(SDKError):
    """Raised when agent operation fails"""
    pass


class ModelError(SDKError):
    """Raised when AI model operation fails"""
    pass


class EventHandlerError(SDKError):
    """Raised when event handler operation fails"""
    pass

