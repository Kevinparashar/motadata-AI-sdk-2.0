# Metadata Python SDK

> A comprehensive Python SDK for building AI-powered applications with agent-based architectures, multi-model AI integration, and seamless database connectivity.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Module Documentation](#module-documentation)
- [Libraries](#libraries)
- [Functions and Classes](#functions-and-classes)
- [Contributing](#contributing)
- [License](#license)

## Overview

### What is This SDK?

The **Metadata Python SDK** is a powerful toolkit designed to simplify the development of AI-powered applications. It provides a unified interface for:

- 🤖 **AI Agents**: Create and manage autonomous AI agents that can communicate and coordinate tasks
- 🧠 **AI Models**: Integrate with multiple AI providers (OpenAI, Anthropic, etc.) through a single interface
- 💾 **Databases**: Work with SQL, NoSQL, and vector databases using consistent APIs
- 🔐 **Authentication**: Handle OAuth2, JWT, and API key authentication seamlessly
- 📡 **API Communication**: Make HTTP requests and WebSocket connections with built-in error handling
- ⚙️ **Configuration**: Manage settings and logging across your application

### Why Use This SDK?

Instead of writing boilerplate code for each AI provider, database, or API integration, this SDK provides:

- **Unified Interface**: Switch between different providers without changing your code
- **Built-in Best Practices**: Error handling, retries, and connection pooling included
- **Type Safety**: Full type hints for better IDE support and fewer bugs
- **Modular Design**: Use only what you need - import specific modules as required
- **Well Documented**: Every module has detailed README files explaining usage

## Features

✨ **Key Capabilities:**

- 🎯 **Agent Management**: Create, start, stop, and coordinate multiple AI agents
- 🔄 **Multi-Model Support**: Easily switch between OpenAI, Anthropic, and other AI providers
- 📊 **Database Abstraction**: Work with PostgreSQL, MySQL, MongoDB, Cassandra, FAISS, Pinecone, and more
- 🔒 **Security First**: Built-in authentication and secure credential management
- 🚀 **Async Support**: Full asyncio support for high-performance applications
- 📝 **Prompt Management**: Template-based prompt system for consistent AI interactions
- 🧪 **Well Tested**: Comprehensive unit tests for all components

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd motadata-ai-sdk

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### 2. Your First AI Agent

```python
from src.agents.agent import Agent
from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.model_integration import ModelIntegrationFactory

# Create an AI agent
agent = Agent(
    agent_id="my-first-agent",
    capabilities=["task_execution", "data_processing"]
)

# Set up AI gateway
gateway = AIGateway(provider="openai", api_key="your-api-key")
model_integration = ModelIntegrationFactory.create("openai", "your-api-key")
gateway.set_model_integration(model_integration)

# Start the agent
agent.start()

# Use the agent to process tasks
result = agent.execute_task({
    "type": "analyze",
    "data": "Your data here"
})
```

### 3. Connect to a Database

```python
from src.database.sql_db import SQLDatabase

# Connect to PostgreSQL
db = SQLDatabase(connection_string="postgresql://user:pass@localhost/dbname")
db.connect()

# Execute queries
results = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
```

## Installation

### Requirements

- Python 3.7 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd motadata-ai-sdk

# Install the package
pip install -r requirements.txt

# Or install in editable mode for development
pip install -e .
```

### Verify Installation

```python
# Test that the SDK is installed correctly
python -c "from src.core.data_structures import RequestModel; print('SDK installed successfully!')"
```

## Project Structure

```
motadata-ai-sdk/
│
├── src/                          # Main source code
│   ├── core/                     # Core utilities and data structures
│   │   ├── data_structures.py   # Request/Response models
│   │   ├── concurrency.py       # Async and threading utilities
│   │   ├── event_handler.py     # Event system
│   │   └── utils.py             # Helper functions
│   │
│   ├── agents/                   # AI Agent functionality
│   │   ├── agent.py             # Main Agent class
│   │   └── agent_communication.py # Agent messaging
│   │
│   ├── ai_gateway/              # AI Model Integration
│   │   ├── gateway.py           # Main gateway interface
│   │   ├── model_integration.py # Provider implementations
│   │   ├── prompt_manager.py    # Prompt templates
│   │   └── input_output.py     # Data preprocessing
│   │
│   ├── database/                # Database integrations
│   │   ├── sql_db.py           # SQL databases
│   │   ├── no_sql_db.py        # NoSQL databases
│   │   └── vector_db.py        # Vector databases
│   │
│   ├── codecs/                  # Encoding/Decoding
│   │   ├── custom_codec.py     # Codec implementations
│   │   └── codec_utils.py      # Codec utilities
│   │
│   ├── api/                     # API Communication
│   │   ├── api_communicator.py # HTTP/WebSocket
│   │   ├── api_methods.py      # Request helpers
│   │   └── authentication.py   # Auth handlers
│   │
│   ├── config/                  # Configuration
│   │   ├── settings.py        # Settings management
│   │   └── logging.py         # Logging setup
│   │
│   └── tests/                   # Unit tests
│       ├── test_agents.py
│       ├── test_ai_gateway.py
│       ├── test_database.py
│       ├── test_codecs.py
│       └── test_api.py
│
├── README.md                     # This file
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
└── LICENSE                      # License information
```

**💡 Tip**: Each module has its own `README.md` file with detailed documentation. Check them out for module-specific usage!

## Usage Examples

### Example 1: AI-Powered Text Analysis

```python
from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.model_integration import ModelIntegrationFactory
from src.ai_gateway.prompt_manager import PromptManager

# Initialize AI Gateway
gateway = AIGateway(provider="openai", api_key="your-key")
model = ModelIntegrationFactory.create("openai", "your-key")
gateway.set_model_integration(model)

# Use prompt manager
prompt_mgr = PromptManager()
template = prompt_mgr.get_template("classification")

# Generate AI response
response = gateway.generate(
    prompt=template.render(text="Your text to classify"),
    model="gpt-3.5-turbo"
)
print(response)
```

### Example 2: Multi-Agent System

```python
from src.agents.agent import Agent
from src.agents.agent_communication import AgentCommunicator

# Create multiple agents
agent1 = Agent(agent_id="agent-1", capabilities=["data_collection"])
agent2 = Agent(agent_id="agent-2", capabilities=["data_analysis"])

# Set up communication
communicator = AgentCommunicator(protocol="nats")
communicator.connect()

agent1.set_communicator(communicator)
agent2.set_communicator(communicator)

# Agents can now communicate
agent1.send_message("agent-2", {"task": "analyze", "data": "..."})
```

### Example 3: Database Operations

```python
from src.database.sql_db import PostgreSQLDatabase
from src.database.vector_db import PineconeDatabase

# SQL Database
sql_db = PostgreSQLDatabase(connection_string="postgresql://...")
sql_db.connect()
users = sql_db.execute_query("SELECT * FROM users")

# Vector Database for AI embeddings
vector_db = PineconeDatabase(
    api_key="your-key",
    environment="us-west1",
    index_name="embeddings"
)
vector_db.connect()
vector_db.upsert(vectors=[[0.1, 0.2, ...]], ids=["doc1"])
similar = vector_db.search(query_vector=[0.1, 0.2, ...], top_k=5)
```

### Example 4: API Communication with Authentication

```python
from src.api.api_communicator import APICommunicator
from src.api.authentication import OAuth2Authenticator

# Set up authentication
auth = OAuth2Authenticator(
    client_id="your-client-id",
    client_secret="your-secret",
    token_url="https://api.example.com/oauth/token"
)

# Create API client
api = APICommunicator(base_url="https://api.example.com")
api.set_auth(auth.get_access_token())

# Make authenticated requests
response = api.get("/users")
data = api.post("/users", data={"name": "John"})
```

## Module Documentation

Each module in the SDK has comprehensive documentation. Here's where to find what you need:

| Module | Purpose | Documentation |
|--------|---------|--------------|
| **core/** | Foundation utilities | [`src/core/README.md`](src/core/README.md) |
| **agents/** | AI Agent management | [`src/agents/README.md`](src/agents/README.md) |
| **ai_gateway/** | AI model integration | [`src/ai_gateway/README.md`](src/ai_gateway/README.md) |
| **database/** | Database connections | [`src/database/README.md`](src/database/README.md) |
| **codecs/** | Data encoding/decoding | [`src/codecs/README.md`](src/codecs/README.md) |
| **api/** | API communication | [`src/api/README.md`](src/api/README.md) |
| **config/** | Configuration & logging | [`src/config/README.md`](src/config/README.md) |
| **tests/** | Unit tests | [`src/tests/README.md`](src/tests/README.md) |

**📚 Each README includes:**
- **WHY**: Purpose and use cases
- **WHAT**: Files and components
- **HOW**: Usage examples
- **Libraries**: Dependencies used
- **Functions and Classes**: Complete API reference

## Libraries

The SDK is built using Python's standard library and is designed to be lightweight. Here are the key libraries used:

### Python Standard Library

| Library | Purpose |
|---------|---------|
| `typing` | Type hints for better code documentation and IDE support |
| `dataclasses` | Data class decorators for structured data models |
| `datetime` | Date and time handling for timestamps |
| `asyncio` | Asynchronous programming support |
| `threading` | Thread synchronization and parallel execution |
| `enum` | Enumeration support for event types |
| `logging` | Logging framework for application logging |
| `os` | Operating system interface for environment variables |
| `pathlib` | Object-oriented filesystem paths |
| `json` | JSON encoding and decoding |
| `base64` | Base64 encoding and decoding |
| `abc` | Abstract base classes for interfaces |
| `concurrent.futures` | Thread pool execution |
| `unittest` | Unit testing framework |

### Third-party Libraries

Currently, the SDK uses only Python standard library. Third-party dependencies will be added to `requirements.txt` as needed.

## Functions and Classes

The SDK is organized into modules, each containing specific functions and classes. Here's a quick reference:

### Core Module (`src/core/`)

**Data Models:**
- `RequestModel` - Base request model for API requests
- `ResponseModel` - Base response model for API responses
- `ConfigModel` - Configuration data model

**Concurrency:**
- `AsyncExecutor` - Async executor for running async functions
- `ThreadPool` - Thread pool for parallel execution
- `ThreadSafeCounter` - Thread-safe counter with lock protection

**Events:**
- `EventHandler` - Base event handler for managing events
- `EventEmitter` - Event emitter for asynchronous event handling
- `EventType` - Event type enumeration

**Exceptions:**
- `SDKError` - Base exception for all SDK errors (replaces generic `Exception`)
- `ValidationError` - Input validation errors (replaces `ValueError`, `TypeError`)
- `APIError` - API request errors with status codes and response data
- `DatabaseError` - Database operation errors
- `AuthenticationError` - Authentication failures
- `ConnectionError` - Connection failures (replaces built-in `ConnectionError`)
- `ConfigurationError` - Configuration errors (replaces `FileNotFoundError`, `ValueError` for config)
- `CodecError` - Encoding/decoding errors
- `AgentError` - Agent operation errors
- `ModelError` - AI model operation errors
- All exceptions include detailed error messages and optional `details` dictionary for debugging

**Validators:**
- `validate_string()` - Validate and sanitize string input with length constraints
- `validate_dict()` - Validate dictionary input with required keys checking
- `validate_list()` - Validate list input with item count constraints
- `validate_int()` - Validate integer input with range checking
- `validate_bool()` - Validate boolean input
- `validate_url()` - Validate URL format
- `validate_email()` - Validate email format
- `validate_uuid()` - Validate UUID format

**Note:** All public methods across the SDK now include comprehensive input validation using these validators, ensuring type safety and preventing invalid data from causing runtime errors.

**Utilities:**
- `setup_logger()` - Setup and configure a logger
- `validate_config()` - Validate configuration dictionary
- `get_env_var()` - Get environment variable with optional default
- `ensure_dir()` - Ensure directory exists, create if it doesn't
- `merge_dicts()` - Merge multiple dictionaries

### Agents Module (`src/agents/`)

- `Agent` - Main agent class with lifecycle management
- `AgentCommunicator` - Base communicator for agent-to-agent communication
- `NATSCommunicator` - NATS-specific communicator implementation

### AI Gateway Module (`src/ai_gateway/`)

- `AIGateway` - Main gateway interface for AI model interactions
- `ModelProvider` - Abstract base class for model providers
- `OpenAIProvider` - OpenAI model provider implementation
- `AnthropicProvider` - Anthropic (Claude) model provider implementation
- `ModelIntegrationFactory` - Factory for creating model integrations
- `PromptManager` - Manager for prompts and templates
- `PromptTemplate` - Prompt template class
- `preprocess_input()` - Preprocess input data for AI model
- `postprocess_output()` - Postprocess AI model output
- `normalize_text()` - Normalize text input
- `chunk_text()` - Split text into chunks with overlap
- `format_messages()` - Format messages for chat API

### Database Module (`src/database/`)

**SQL Databases:**
- `SQLDatabase` - SQL database connection and operations
- `PostgreSQLDatabase` - PostgreSQL-specific implementation
- `MySQLDatabase` - MySQL-specific implementation

**NoSQL Databases:**
- `NoSQLDatabase` - Base NoSQL database connection and operations
- `MongoDBDatabase` - MongoDB-specific implementation
- `CassandraDatabase` - Cassandra-specific implementation

**Vector Databases:**
- `VectorDatabase` - Base vector database for similarity search
- `FAISSDatabase` - FAISS vector database implementation
- `PineconeDatabase` - Pinecone vector database implementation

### Codecs Module (`src/codecs/`)

- `Codec` - Abstract base class for codecs
- `JSONCodec` - JSON encoding/decoding codec
- `Base64Codec` - Base64 encoding/decoding codec
- `BinaryCodec` - Binary encoding/decoding codec
- `CustomCodec` - Custom codec with configurable encoding/decoding
- `register_codec()` - Register a custom codec
- `get_codec()` - Get a codec instance by name
- `list_codecs()` - List all registered codecs
- `validate_encoded_data()` - Validate that data can be decoded
- `encode_with_format()` - Quick encode function
- `decode_with_format()` - Quick decode function

### API Module (`src/api/`)

- `APICommunicator` - Base API communicator for HTTP and WebSocket
- `WebSocketCommunicator` - WebSocket communicator for real-time communication
- `Authenticator` - Base authenticator class
- `OAuth2Authenticator` - OAuth2 authentication
- `JWTAuthenticator` - JWT token authentication
- `APIKeyAuthenticator` - API key authentication
- `encode_data()` - Encode data for API transmission
- `decode_data()` - Decode data from API response
- `send_request()` - Send an HTTP request with authentication
- `prepare_request_data()` - Prepare data for API request
- `parse_response()` - Parse API response into structured format

### Config Module (`src/config/`)

- `Settings` - Configuration settings manager
- `LoggerMixin` - Mixin class to add logging capability to any class
- `load_config()` - Load configuration from file or environment
- `setup_logger()` - Setup and configure a logger
- `get_logger()` - Get a logger instance by name
- `configure_logging()` - Configure root logger for the SDK

### Tests Module (`src/tests/`)

Comprehensive unit tests for all SDK components:
- `TestAgent`, `TestAgentCommunicator` - Agent functionality tests
- `TestAIGateway`, `TestPromptManager` - AI Gateway tests
- `TestSQLDatabase`, `TestNoSQLDatabase`, `TestVectorDatabase` - Database tests
- `TestJSONCodec`, `TestBase64Codec`, `TestCustomCodec` - Codec tests
- `TestAPICommunicator`, `TestOAuth2Authenticator`, `TestJWTAuthenticator`, `TestAPIKeyAuthenticator` - API tests

**Test Infrastructure:**
- `conftest.py` - Shared pytest fixtures (sample_agent_config, sample_task, etc.)
- `.coveragerc` - Test coverage configuration
- `requirements-test.txt` - Test-specific dependencies

**📖 For detailed API documentation**, refer to the README.md files in each module directory.

## Input Validation and Error Handling

**Comprehensive Input Validation:** All public methods across the SDK now include input validation to ensure:
- Type safety (correct data types for all parameters)
- Range checking (string lengths, list sizes, numeric ranges)
- Required fields (dictionary keys, list items)
- Format validation (URLs, emails, UUIDs)

**Custom Exception Hierarchy:** The SDK uses a custom exception hierarchy instead of built-in Python exceptions:
- All exceptions inherit from `SDKError` for consistent error handling
- Specific exception types for different error categories (ValidationError, APIError, DatabaseError, etc.)
- Detailed error messages with optional `details` dictionary for debugging
- Better error context (field names, values, status codes, etc.)

This ensures better error handling, easier debugging, and more predictable behavior throughout the SDK.

## Project Configuration

The SDK includes standard configuration files following industry best practices:

### Core Configuration Files
- **pyproject.toml** - Modern Python project configuration (PEP 621) with tool settings for black, isort, mypy, and pytest
- **setup.py** - Package installation script with version management from `src/__version__.py`
- **MANIFEST.in** - Specifies non-Python files to include in package distribution
- **.gitignore** - Version control ignore patterns for Python projects
- **.gitattributes** - Line ending and file type handling for cross-platform compatibility

### Dependency Management
- **requirements.txt** - Production dependencies
- **requirements-dev.txt** - Development dependencies (linting, formatting, testing tools)
- **requirements-test.txt** - Test-specific dependencies (pytest, coverage, etc.)

### Testing & Quality
- **.coveragerc** - Test coverage configuration with exclusions and reporting options
- **conftest.py** - Shared pytest fixtures for all tests

### Environment Configuration
- **.env.example** - Environment variable template (copy to `.env` for local development)

## Version Management

The SDK version is centrally managed in `src/__version__.py`:
```python
from src import __version__
print(__version__)  # "0.1.0"
```

This ensures a single source of truth for version information across the project.

## Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? Open an issue with details
2. **Suggest Features**: Have an idea? Share it in an issue
3. **Submit Pull Requests**: Fix bugs or add features
4. **Improve Documentation**: Help make the docs better

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd motadata-ai-sdk

# Install in development mode
pip install -e .

# Run tests
pytest src/tests/

# Run tests with coverage
pytest src/tests/ --cov=src --cov-report=html
```

## License

See [LICENSE](LICENSE) file for license information.

---

**Need Help?** Check the module-specific README files in each directory, or open an issue for support.

