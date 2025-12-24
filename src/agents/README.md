# Agents Module

## WHY
The agents module enables the creation and management of autonomous AI agents that can communicate, process information, and execute tasks. This module is essential for building agent-based applications that require inter-agent communication and coordination.

## WHAT
This module contains:

- **agent.py**: Main agent class definition that provides the core agent functionality, lifecycle management, and task execution capabilities
- **agent_communication.py**: Communication protocol handlers (e.g., NATS, message queues) for enabling agents to send and receive messages, coordinate tasks, and share information

## HOW
Create and use agents in your application:

```python
from src.agents.agent import Agent
from src.agents.agent_communication import AgentCommunicator

# Create an agent instance
agent = Agent(agent_id="agent-1", capabilities=["task_execution", "data_processing"])

# Set up communication
communicator = AgentCommunicator(protocol="nats")
agent.set_communicator(communicator)

# Start the agent
agent.start()
```

Agents can be configured with specific capabilities, communication protocols, and event handlers to suit your application's needs.

