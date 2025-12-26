"""
Agno agent framework integration
"""
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from ..core.event_handler import EventEmitter, EventType
from ..core.validators import validate_string, validate_dict, validate_list
from ..core.exceptions import AgentError, ValidationError, ConnectionError as SDKConnectionError, SDKError
import logging

try:
    from agno import Agent as AgnoAgent, LLM, Prompt, Run
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False
    logging.warning("Agno not installed. Install with: pip install agno")


class Agent:
    """Agent class integrating with Agno framework for autonomous AI agents"""
    
    def __init__(
        self,
        agent_id: str,
        capabilities: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
        llm: Optional[Any] = None
    ):
        # Validate inputs
        self.agent_id = validate_string(agent_id, "agent_id", min_length=1, max_length=100)
        if capabilities is not None:
            self.capabilities = validate_list(capabilities, "capabilities", allow_empty=True)
        else:
            self.capabilities = []
        if config is not None:
            self.config = validate_dict(config, "config", required_keys=None)
        else:
            self.config = {}
        self.status = "idle"
        self.created_at = datetime.now()
        self.event_emitter = EventEmitter()
        self._communicator = None
        self._logger = logging.getLogger(__name__)
        
        # Initialize Agno agent if available
        self._agno_agent: Optional[Any] = None
        if AGNO_AVAILABLE and llm is not None:
            try:
                self._agno_agent = AgnoAgent(
                    name=self.agent_id,
                    llm=llm,
                    description=f"Agent with capabilities: {', '.join(self.capabilities)}",
                    **self.config
                )
                self._logger.info(f"Agno agent initialized: {self.agent_id}")
            except Exception as e:
                self._logger.warning(f"Failed to initialize Agno agent: {str(e)}")
        elif not AGNO_AVAILABLE:
            self._logger.warning("Agno framework not available. Install with: pip install agno")
    
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
        """Execute a task
        
        Args:
            task: Dictionary containing task information with required keys:
                - type: Task type identifier (string)
                - data: Task data payload (any)
        
        Returns:
            Task execution result
        
        Raises:
            ValidationError: If task structure is invalid
            AgentError: If task execution fails
        """
        # Validate task structure
        task = validate_dict(task, "task", required_keys=["type", "data"])
        validate_string(task["type"], "task.type", min_length=1)
        
        self.status = "processing"
        self.event_emitter.emit("task_started", task)
        
        try:
            result = self._process_task(task)
            self.status = "idle"
            self.event_emitter.emit("task_completed", task, result)
            return result
        except ValidationError:
            self.status = "error"
            self._logger.error(f"Validation error in task execution: {task.get('type', 'unknown')}")
            raise
        except AgentError:
            self.status = "error"
            raise
        except Exception as e:
            self.status = "error"
            error_msg = f"Unexpected error in task execution: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            self.event_emitter.emit("task_error", task, str(e))
            raise AgentError(error_msg, details={"task": task.get("type", "unknown"), "original_error": str(e)})
    
    def _process_task(self, task: Dict[str, Any]) -> Any:
        """Internal method to process a task using Agno framework if available"""
        if self._agno_agent is not None:
            try:
                # Use Agno agent to process the task
                prompt = task.get("data", {}).get("prompt", str(task.get("data", "")))
                if isinstance(prompt, dict):
                    prompt = str(prompt)
                
                run = self._agno_agent.run(prompt=prompt)
                return {
                    "status": "completed",
                    "task": task,
                    "result": run.content if hasattr(run, 'content') else str(run),
                    "agent": "agno"
                }
            except Exception as e:
                self._logger.error(f"Agno task processing failed: {str(e)}", exc_info=True)
                # Fallback to default processing
                return {"status": "completed", "task": task, "error": str(e)}
        
        # Default processing if Agno is not available
        return {"status": "completed", "task": task}
    
    def on(self, event: str, handler: Callable) -> None:
        """Register an event handler
        
        Args:
            event: Event name to listen for
            handler: Callable function to handle the event
        
        Raises:
            ValidationError: If event name or handler is invalid
        """
        validate_string(event, "event", min_length=1)
        if not callable(handler):
            raise ValidationError("handler must be callable", field="handler", value=type(handler).__name__)
        self.event_emitter.on(event, handler)
    
    def send_message(self, recipient: str, message: Dict[str, Any]) -> None:
        """Send a message to another agent
        
        Args:
            recipient: Recipient agent ID
            message: Message dictionary to send
        
        Raises:
            ValidationError: If recipient or message is invalid
            AgentError: If no communicator is set or sending fails
        """
        recipient = validate_string(recipient, "recipient", min_length=1)
        message = validate_dict(message, "message", required_keys=None)
        
        if not self._communicator:
            raise AgentError("No communicator set for agent. Call set_communicator() first.")
        try:
            self._communicator.send(recipient, message)
        except SDKConnectionError as e:
            raise AgentError(f"Failed to send message: {str(e)}", details={"recipient": recipient})
    
    def receive_message(self, sender: str, message: Dict[str, Any]) -> None:
        """Receive a message from another agent
        
        Args:
            sender: Sender agent ID
            message: Received message dictionary
        
        Raises:
            ValidationError: If sender or message is invalid
        """
        sender = validate_string(sender, "sender", min_length=1)
        message = validate_dict(message, "message", required_keys=None)
        self.event_emitter.emit("message_received", sender, message)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "capabilities": self.capabilities,
            "created_at": self.created_at.isoformat()
        }
