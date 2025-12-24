"""
Event handling logic
"""
from typing import Callable, Dict, List, Any, Optional
from enum import Enum
import threading


class EventType(Enum):
    """Event type enumeration"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    CUSTOM = "custom"


class EventHandler:
    """Base event handler for managing events"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def on(self, event: str, handler: Callable) -> None:
        """Register an event handler"""
        with self._lock:
            if event not in self._handlers:
                self._handlers[event] = []
            self._handlers[event].append(handler)
    
    def off(self, event: str, handler: Optional[Callable] = None) -> None:
        """Unregister an event handler"""
        with self._lock:
            if event in self._handlers:
                if handler is None:
                    self._handlers[event].clear()
                elif handler in self._handlers[event]:
                    self._handlers[event].remove(handler)
    
    def emit(self, event: str, *args, **kwargs) -> None:
        """Emit an event"""
        with self._lock:
            handlers = self._handlers.get(event, [])
        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(f"Error in event handler for {event}: {e}")
    
    def once(self, event: str, handler: Callable) -> None:
        """Register a one-time event handler"""
        def wrapper(*args, **kwargs):
            handler(*args, **kwargs)
            self.off(event, wrapper)
        self.on(event, wrapper)


class EventEmitter:
    """Event emitter for asynchronous event handling"""
    
    def __init__(self):
        self.handler = EventHandler()
    
    def on(self, event: str, handler: Callable) -> None:
        """Register an event handler"""
        self.handler.on(event, handler)
    
    def off(self, event: str, handler: Optional[Callable] = None) -> None:
        """Unregister an event handler"""
        self.handler.off(event, handler)
    
    def emit(self, event: str, *args, **kwargs) -> None:
        """Emit an event"""
        self.handler.emit(event, *args, **kwargs)
    
    def once(self, event: str, handler: Callable) -> None:
        """Register a one-time event handler"""
        self.handler.once(event, handler)
