"""
NATS or other messaging protocol handler
"""
from typing import Dict, Any, Optional, Callable, List
import threading
from ..core.validators import validate_string, validate_dict
from ..core.exceptions import ConnectionError as SDKConnectionError, ValidationError
import logging


class AgentCommunicator:
    """Base communicator for agent-to-agent communication"""
    
    def __init__(self, protocol: str = "nats", config: Optional[Dict[str, Any]] = None):
        self.protocol = validate_string(protocol, "protocol", min_length=1, max_length=50)
        if config is not None:
            self.config = validate_dict(config, "config", required_keys=None)
        else:
            self.config = {}
        self._connected = False
        self._message_handlers: Dict[str, Callable] = {}
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
    
    def connect(self) -> None:
        """Connect to the messaging system"""
        self._connected = True
    
    def disconnect(self) -> None:
        """Disconnect from the messaging system"""
        self._connected = False
    
    def send(self, recipient: str, message: Dict[str, Any]) -> None:
        """Send a message to a recipient
        
        Args:
            recipient: Recipient identifier
            message: Message dictionary to send
        
        Raises:
            ValidationError: If recipient or message is invalid
            SDKConnectionError: If not connected to messaging system
        """
        recipient = validate_string(recipient, "recipient", min_length=1)
        message = validate_dict(message, "message", required_keys=None)
        
        if not self._connected:
            raise SDKConnectionError("Not connected to messaging system")
        # Implementation depends on protocol
        pass
    
    def subscribe(self, topic: str, handler: Callable) -> None:
        """Subscribe to a topic
        
        Args:
            topic: Topic name to subscribe to
            handler: Callable function to handle messages
        
        Raises:
            ValidationError: If topic or handler is invalid
        """
        topic = validate_string(topic, "topic", min_length=1)
        if not callable(handler):
            raise ValidationError("handler must be callable", field="handler", value=type(handler).__name__)
        with self._lock:
            self._message_handlers[topic] = handler
    
    def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from a topic
        
        Args:
            topic: Topic name to unsubscribe from
        
        Raises:
            ValidationError: If topic is invalid
        """
        topic = validate_string(topic, "topic", min_length=1)
        with self._lock:
            if topic in self._message_handlers:
                del self._message_handlers[topic]
    
    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to a topic
        
        Args:
            topic: Topic name to publish to
            message: Message dictionary to publish
        
        Raises:
            ValidationError: If topic or message is invalid
            SDKConnectionError: If not connected to messaging system
        """
        topic = validate_string(topic, "topic", min_length=1)
        message = validate_dict(message, "message", required_keys=None)
        
        if not self._connected:
            raise SDKConnectionError("Not connected to messaging system")
        # Implementation depends on protocol
        pass
    
    @property
    def is_connected(self) -> bool:
        """Check if connected"""
        return self._connected


class NATSCommunicator(AgentCommunicator):
    """NATS-specific communicator"""
    
    def __init__(self, servers: Optional[List[str]] = None, **kwargs):
        super().__init__(protocol="nats", config=kwargs)
        if servers is not None:
            self.servers = validate_list(servers, "servers", min_items=1, allow_empty=False)
            # Validate each server is a string
            for i, server in enumerate(self.servers):
                validate_string(server, f"servers[{i}]", min_length=1)
        else:
            self.servers = ["nats://localhost:4222"]
    
    def connect(self) -> None:
        """Connect to NATS server"""
        # NATS connection logic would go here
        self._connected = True
    
    def send(self, recipient: str, message: Dict[str, Any]) -> None:
        """Send message via NATS
        
        Args:
            recipient: Recipient identifier
            message: Message dictionary to send
        
        Raises:
            ValidationError: If recipient or message is invalid
            SDKConnectionError: If not connected to NATS
        """
        recipient = validate_string(recipient, "recipient", min_length=1)
        message = validate_dict(message, "message", required_keys=None)
        
        if not self._connected:
            raise SDKConnectionError("Not connected to NATS")
        # NATS publish logic would go here
        pass
