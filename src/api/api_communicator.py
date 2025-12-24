"""
API communication methods (HTTP, WebSocket)
"""
from typing import Dict, Any, Optional, List
import threading
from ..core.data_structures import RequestModel, ResponseModel


class APICommunicator:
    """Base API communicator for HTTP and WebSocket"""
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.default_headers = headers or {}
        self._auth_token = None
        self._lock = threading.Lock()
    
    def set_auth(self, token: str) -> None:
        """Set authentication token"""
        with self._lock:
            self._auth_token = token
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a GET request"""
        return self._make_request("GET", endpoint, params=params, headers=headers)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a POST request"""
        return self._make_request("POST", endpoint, data=data, headers=headers)
    
    def put(
        self,
        endpoint: str,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a PUT request"""
        return self._make_request("PUT", endpoint, data=data, headers=headers)
    
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Make a DELETE request"""
        return self._make_request("DELETE", endpoint, headers=headers)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> ResponseModel:
        """Internal method to make HTTP requests"""
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


class WebSocketCommunicator:
    """WebSocket communicator for real-time communication"""
    
    def __init__(self, url: str):
        self.url = url
        self._connected = False
        self._socket = None
        self._lock = threading.Lock()
    
    def connect(self) -> None:
        """Connect to WebSocket server"""
        # WebSocket connection logic would go here
        self._connected = True
    
    def disconnect(self) -> None:
        """Disconnect from WebSocket server"""
        with self._lock:
            if self._socket:
                self._socket = None
            self._connected = False
    
    def send(self, message: Dict[str, Any]) -> None:
        """Send a message through WebSocket"""
        if not self._connected:
            raise ConnectionError("Not connected to WebSocket")
        # WebSocket send logic would go here
        pass
    
    def receive(self) -> Dict[str, Any]:
        """Receive a message from WebSocket"""
        if not self._connected:
            raise ConnectionError("Not connected to WebSocket")
        # WebSocket receive logic would go here
        return {}
    
    @property
    def is_connected(self) -> bool:
        """Check if connected to WebSocket"""
        return self._connected
