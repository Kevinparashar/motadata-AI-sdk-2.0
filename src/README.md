# Source Code Directory

## WHY
This directory contains the core source code for the Metadata Python SDK. It is organized into logical modules that handle different aspects of the SDK's functionality, making the codebase maintainable, scalable, and easy to understand.

## WHAT
The `src/` directory is the main package directory containing all SDK modules:

- **core/**: Core components and utilities that form the foundation of the SDK
- **agents/**: Agent-related functionality for autonomous AI agents
- **ai_gateway/**: AI Gateway components for integrating with various AI models
- **database/**: Database integration modules for SQL, NoSQL, and vector databases
- **codecs/**: Custom encoding and decoding logic for data transformation
- **api/**: API communication and authentication mechanisms
- **config/**: Configuration management and logging setup
- **tests/**: Unit tests for all SDK components

## HOW
To use the SDK, import modules from the `src` package:

```python
from src.core.data_structures import DataModel
from src.agents.agent import Agent
from src.ai_gateway.gateway import AIGateway
from src.database.sql_db import SQLDatabase
```

Each module is designed to be imported independently, allowing you to use only the components you need for your specific use case.

