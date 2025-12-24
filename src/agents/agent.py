"""
Main agent class definition
"""
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from ..core.event_handler import EventEmitter, EventType


class Agent:
    """Main agent class for autonomous AI agents"""
    
    def __init__(
        self,
        agent_id: str,
        capabilities: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.agent_id = agent_id
        self.capabilities = capabilities or []
        self.config = config or {}
        self.status = "idle"
        self.created_at = datetime.now()
        self.event_emitter = EventEmitter()
        self._communicator = None
    
    def set_communicator(self, communicator):
        """Set the communication handler for the agent"""
        self._communicator = communicator
    
    def start(self) -> None:
        """Start the agent"""
        self.status = "running"
        self.event_emitter.emit("agent_started", self.agent_id)
    
    def stop(self) -> None:
        """Stop the agent"""
        self.status = "stopped"
        self.event_emitter.emit("agent_stopped", self.agent_id)
    
    def execute_task(self, task: Dict[str, Any]) -> Any:
        """Execute a task"""
        self.status = "processing"
        self.event_emitter.emit("task_started", task)
        
        try:
            result = self._process_task(task)
            self.status = "idle"
            self.event_emitter.emit("task_completed", task, result)
            return result
        except Exception as e:
            self.status = "error"
            self.event_emitter.emit("task_error", task, str(e))
            raise
    
    def _process_task(self, task: Dict[str, Any]) -> Any:
        """Internal method to process a task"""
        # Override in subclasses
        return {"status": "completed", "task": task}
    
    def on(self, event: str, handler: Callable) -> None:
        """Register an event handler"""
        self.event_emitter.on(event, handler)
    
    def send_message(self, recipient: str, message: Dict[str, Any]) -> None:
        """Send a message to another agent"""
        if self._communicator:
            self._communicator.send(recipient, message)
        else:
            raise ValueError("No communicator set for agent")
    
    def receive_message(self, sender: str, message: Dict[str, Any]) -> None:
        """Receive a message from another agent"""
        self.event_emitter.emit("message_received", sender, message)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "capabilities": self.capabilities,
            "created_at": self.created_at.isoformat()
        }
