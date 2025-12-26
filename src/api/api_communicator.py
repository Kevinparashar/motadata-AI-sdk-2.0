"""
API communication methods (HTTP, WebSocket)
"""
from typing import Dict, Any, Optional, List
import threading
from ..core.data_structures import RequestModel, ResponseModel
from ..core.validators import validate_string, validate_dict
from ..core.exceptions import APIError, ValidationError, ConnectionError as SDKConnectionError
import logging


class APICommunicator:
    """Base API communicator for HTTP and WebSocket"""
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None
    ):
        # Validate inputs
        self.base_url = validate_string(base_url, "base_url", min_length=1).rstrip('/')
        if timeout <= 0:
            raise ValidationError("timeout must be positive", field="timeout", value=timeout)
        self.timeout = timeout
        if headers is not None:
            self.default_headers = validate_dict(headers, "headers", required_keys=None)
        else:
            self.default_headers = {}
        self._auth_token = None
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
    
    def set_auth(self, token: str) -> None:
        """Set authentication token
        
        Args:
            token: Authentication token string
        
        Raises:
            ValidationError: If token is invalid
        """
        token = validate_string(token, "token", min_length=1)
        with self._lock:
            self._auth_token = token
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a GET request
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Additional headers
        
        Returns:
            ResponseModel with response data
        
        Raises:
            ValidationError: If endpoint is invalid
            APIError: If request fails
        """
        endpoint = validate_string(endpoint, "endpoint", min_length=1, allow_empty=True)
        if params is not None:
            params = validate_dict(params, "params", required_keys=None)
        if headers is not None:
            headers = validate_dict(headers, "headers", required_keys=None)
        return self._make_request("GET", endpoint, params=params, headers=headers)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a POST request
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers
        
        Returns:
            ResponseModel with response data
        
        Raises:
            ValidationError: If endpoint is invalid
            APIError: If request fails
        """
        endpoint = validate_string(endpoint, "endpoint", min_length=1, allow_empty=True)
        if headers is not None:
            headers = validate_dict(headers, "headers", required_keys=None)
        return self._make_request("POST", endpoint, data=data, headers=headers)
    
    def put(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a PUT request
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            headers: Additional headers
        
        Returns:
            ResponseModel with response data
        
        Raises:
            ValidationError: If endpoint is invalid
            APIError: If request fails
        """
        endpoint = validate_string(endpoint, "endpoint", min_length=1, allow_empty=True)
        if headers is not None:
            headers = validate_dict(headers, "headers", required_keys=None)
        return self._make_request("PUT", endpoint, data=data, headers=headers)
    
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a DELETE request
        
        Args:
            endpoint: API endpoint path
            headers: Additional headers
        
        Returns:
            ResponseModel with response data
        
        Raises:
            ValidationError: If endpoint is invalid
            APIError: If request fails
        """
        endpoint = validate_string(endpoint, "endpoint", min_length=1, allow_empty=True)
        if headers is not None:
            headers = validate_dict(headers, "headers", required_keys=None)
        return self._make_request("DELETE", endpoint, headers=headers)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Internal method to make HTTP requests
        
        Raises:
            APIError: If request fails
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            request_headers = {**self.default_headers}
            
            if self._auth_token:
                request_headers["Authorization"] = f"Bearer {self._auth_token}"
            
            if headers:
                request_headers.update(headers)
            
            # Actual HTTP request would be made here
            # This is a placeholder implementation
            return ResponseModel(
                status_code=200,
                data={"message": "Request successful"},
                headers=request_headers
            )
        except Exception as e:
            error_msg = f"API request failed: {method} {endpoint}"
            self._logger.error(error_msg, exc_info=True)
            raise APIError(error_msg, details={"method": method, "endpoint": endpoint, "error": str(e)})


class WebSocketCommunicator:
    """WebSocket communicator for real-time communication"""
    
    def __init__(self, url: str):
        self.url = validate_string(url, "url", min_length=1)
        self._connected = False
        self._socket = None
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
    
    def connect(self) -> None:
        """Connect to WebSocket server
        
        Raises:
            SDKConnectionError: If connection fails
        """
        try:
            # WebSocket connection logic would go here
            self._connected = True
        except Exception as e:
            error_msg = f"Failed to connect to WebSocket: {self.url}"
            self._logger.error(error_msg, exc_info=True)
            raise SDKConnectionError(error_msg, details={"url": self.url, "error": str(e)})
    
    def disconnect(self) -> None:
        """Disconnect from WebSocket server"""
        with self._lock:
            if self._socket:
                self._socket = None
            self._connected = False
    
    def send(self, message: Dict[str, Any]) -> None:
        """Send a message through WebSocket
        
        Args:
            message: Message dictionary to send
        
        Raises:
            ValidationError: If message is invalid
            SDKConnectionError: If not connected to WebSocket
        """
        message = validate_dict(message, "message", required_keys=None)
        if not self._connected:
            raise SDKConnectionError("Not connected to WebSocket")
        # WebSocket send logic would go here
        pass
    
    def receive(self) -> Dict[str, Any]:
        """Receive a message from WebSocket
        
        Returns:
            Received message dictionary
        
        Raises:
            SDKConnectionError: If not connected to WebSocket
        """
        if not self._connected:
            raise SDKConnectionError("Not connected to WebSocket")
        # WebSocket receive logic would go here
        return {}
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to WebSocket"""
        return self._connected
