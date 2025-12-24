# Metadata Python SDK

## WHY
This SDK provides a comprehensive Python interface for interacting with the Metadata AI platform. It enables developers to build AI-powered applications with agent-based architectures, integrate with multiple AI models, manage database connections, and handle API communications seamlessly. The SDK abstracts away the complexities of AI model integration, database management, and communication protocols, allowing developers to focus on building their applications.

## WHAT
This repository contains the complete source code and documentation for the Metadata Python SDK:

- **src/**: Main source code directory containing all SDK modules
  - **core/**: Core components and utilities (data structures, concurrency, event handling, utils)
  - **agents/**: Agent-related functionality for autonomous AI agents
  - **ai_gateway/**: AI Gateway components for model integration
  - **database/**: Database integrations (SQL, NoSQL, Vector DB)
  - **codecs/**: Custom encoding and decoding logic
  - **api/**: API communication and authentication
  - **config/**: Configuration management and logging
  - **tests/**: Unit tests for all SDK components
- **requirements.txt**: Python package dependencies
- **setup.py**: Python setup file for package installation
- **LICENSE**: License information for the SDK

## HOW
### Installation
Install the SDK using pip:

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### Basic Usage
Import and use SDK components:

```python
from src.agents.agent import Agent
from src.ai_gateway.gateway import AIGateway
from src.database.sql_db import SQLDatabase
from src.api.api_communicator import APICommunicator

# Initialize components
agent = Agent(agent_id="my-agent")
gateway = AIGateway(provider="openai", api_key="your-key")
db = SQLDatabase(connection_string="postgresql://...")
api = APICommunicator(base_url="https://api.example.com")
```

### Getting Started
1. Review the README.md files in each module directory for specific usage instructions
2. Check `src/config/README.md` for configuration setup
3. Explore `src/tests/` for usage examples in test files
4. Refer to individual module documentation for detailed API references

For detailed information about each module, see the README.md files in their respective directories.

