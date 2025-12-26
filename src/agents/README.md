# Agents Module

## WHY
The agents module enables the creation and management of autonomous AI agents using the Agno framework. Agno provides a powerful agent framework for building intelligent, autonomous agents that can communicate, process information, and execute tasks. This module integrates Agno with the SDK's infrastructure for seamless agent management.

## WHAT
This module contains:

- **agent.py**: Main agent class definition integrating with Agno framework, providing core agent functionality, lifecycle management, and task execution capabilities
- **agent_communication.py**: Communication protocol handlers (e.g., NATS, message queues) for enabling agents to send and receive messages, coordinate tasks, and share information

## HOW
Create and use agents with Agno framework in your application:

```python
from src.agents.agent import Agent
from src.agents.agent_communication import AgentCommunicator
from src.core.exceptions import AgentError, ValidationError, ConnectionError
from agno import LLM

# Create LLM instance for Agno agent
llm = LLM(model="gpt-4", api_key="your-api-key")

# Create an agent instance using Agno framework (with automatic input validation)
agent = Agent(
    agent_id="agent-1",
    capabilities=["task_execution", "data_processing"],
    llm=llm
)

# Set up communication
communicator = AgentCommunicator(protocol="nats")
agent.set_communicator(communicator)

# Start the agent
agent.start()

# Execute tasks with validation (Agno will process the task)
try:
    result = agent.execute_task({
        "type": "process_data",
        "data": {"prompt": "Analyze this data: example"}
    })
except ValidationError as e:
    print(f"Invalid task: {e.message}, field: {e.field}")
except AgentError as e:
    print(f"Agent error: {e.message}")
```

Agents use the Agno framework for intelligent task processing, with SDK infrastructure for communication, validation, and event handling.

## Input Validation and Error Handling

**All public methods in the agents module include comprehensive input validation:**

- **Agent.__init__()**: Validates `agent_id` (string, 1-100 chars), `capabilities` (list), `config` (dict), and initializes Agno agent if LLM is provided
- **Agent.execute_task()**: Validates task structure (must have "type" and "data" keys)
- **Agent.send_message()**: Validates recipient (string) and message (dict)
- **Agent.receive_message()**: Validates sender (string) and message (dict)
- **Agent.on()**: Validates event name (string) and handler (callable)
- **AgentCommunicator.send()**: Validates recipient and message
- **AgentCommunicator.subscribe()**: Validates topic (string) and handler (callable)
- **NATSCommunicator.__init__()**: Validates servers list (non-empty, all strings)

**Custom Exceptions Used:**
- `ValidationError`: Invalid input parameters (replaces `ValueError`, `TypeError`)
- `AgentError`: Agent operation failures (replaces generic `Exception`)
- `ConnectionError`: Communication failures (replaces built-in `ConnectionError`)

All methods raise appropriate custom exceptions with detailed error messages and context.

## Libraries
This module uses the following Python standard libraries and packages:

- **typing**: Type hints (List, Dict, Any, Optional, Callable)
- **datetime**: Date and time handling for agent timestamps
- **threading**: Thread synchronization primitives (Lock) for thread-safe operations
- **agno**: Agent framework for building autonomous AI agents
- **src.core.event_handler**: EventEmitter and EventType from core module for event handling

## Functions and Classes

### agent.py
- **Agent** (class): Main agent class integrating with Agno framework for autonomous AI agents
  - `__init__()`: Initialize agent with agent_id, capabilities, config, and optional LLM for Agno
  - `set_communicator()`: Set the communication handler for the agent
  - `start()`: Start the agent
  - `stop()`: Stop the agent
  - `execute_task()`: Execute a task (uses Agno if LLM is provided)
  - `_process_task()`: Internal method to process a task using Agno framework
  - `on()`: Register an event handler
  - `send_message()`: Send a message to another agent
  - `receive_message()`: Receive a message from another agent
  - `get_status()`: Get agent status information

### agent_communication.py
- **AgentCommunicator** (class): Base communicator for agent-to-agent communication
  - `__init__()`: Initialize communicator with protocol and config
  - `connect()`: Connect to the messaging system
  - `disconnect()`: Disconnect from the messaging system
  - `send()`: Send a message to a recipient
  - `subscribe()`: Subscribe to a topic
  - `unsubscribe()`: Unsubscribe from a topic
  - `publish()`: Publish a message to a topic
  - `is_connected` (property): Check if connected to messaging system
- **NATSCommunicator** (class): NATS-specific communicator implementation
  - `__init__()`: Initialize NATS communicator with servers
  - `connect()`: Connect to NATS server
  - `send()`: Send message via NATS

