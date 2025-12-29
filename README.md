# Metadata Python SDK

> A comprehensive Python SDK for building AI-powered applications with agent-based architectures, multi-model AI integration, and seamless database connectivity.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Execution Flow](#execution-flow)
- [Module Documentation](#module-documentation)
- [Libraries](#libraries)
- [Functions and Classes](#functions-and-classes)
- [Contributing](#contributing)
- [License](#license)

## Overview

### What is This SDK?

The **Metadata Python SDK** is a powerful toolkit designed to simplify the development of AI-powered applications. It provides a unified interface for:

- 🤖 **AI Agents**: Create and manage autonomous AI agents using Agno framework that can communicate and coordinate tasks
- 🧠 **AI Models**: Integrate with multiple AI providers through LiteLLM unified interface (OpenAI, Anthropic, Gemini, etc.)
- 💾 **Databases**: Work with PostgreSQL database using consistent APIs
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

- 🎯 **Agent Management**: Create, start, stop, and coordinate multiple AI agents using Agno framework
- 🔄 **Multi-Model Support**: Easily switch between AI providers (OpenAI, Anthropic, Gemini, etc.) through LiteLLM
- 📊 **PostgreSQL Integration**: Work with PostgreSQL database using optimized connection pooling and transactions
- 🔒 **Security First**: Built-in authentication and secure credential management
- 🚀 **Async Support**: Full asyncio support for high-performance applications
- 📝 **Prompt Management**: Template-based prompt system for consistent AI interactions
- 🧪 **Well Tested**: Comprehensive unit tests for all components

## Quick Start

### 1. Installation

**Prerequisites:**
- Python 3.8.1 or higher
- [UV](https://github.com/astral-sh/uv) package manager (fast Python package installer)

**Install UV:**
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or using pip
pip install uv
```

**Setup the project:**
```bash
# Clone the repository
git clone <repository-url>
cd motadata-ai-sdk

# Install dependencies and create virtual environment (UV will handle this automatically)
uv sync

# Or install with development dependencies
uv sync --extra dev

# Or install with test dependencies
uv sync --extra test

# Or install with both dev and test dependencies
uv sync --all-extras
```

**Using UV commands:**
```bash
# Run commands in the UV environment
uv run python your_script.py

# Run tests
uv run pytest

# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade
```

### 2. Your First AI Agent

```python
from src.agents.agent import Agent
from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.model_integration import ModelIntegrationFactory
from agno import LLM

# Set up LiteLLM AI gateway
gateway = AIGateway(provider="litellm", api_key="your-api-key")
model_integration = ModelIntegrationFactory.create("litellm", api_key="your-api-key")
gateway.set_model_integration(model_integration)

# Create LLM instance for Agno
llm = LLM(model="gpt-4", api_key="your-api-key")

# Create an AI agent using Agno framework
agent = Agent(
    agent_id="my-first-agent",
    capabilities=["task_execution", "data_processing"],
    llm=llm
)

# Start the agent
agent.start()

# Use the agent to process tasks
result = agent.execute_task({
    "type": "analyze",
    "data": {"prompt": "Your task prompt here"}
})
```

### 3. Connect to a Database

```python
from src.database.sql_db import PostgreSQLDatabase

# Connect to PostgreSQL
db = PostgreSQLDatabase(connection_string="postgresql://user:pass@localhost/dbname")
db.connect()

# Execute queries
results = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
```

## Installation

### Requirements

- Python 3.8.1 or higher
- [UV](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd motadata-ai-sdk

# Install dependencies and create virtual environment (UV handles this automatically)
uv sync

# Or install with development dependencies
uv sync --extra dev

# Or install with all extras (dev + test)
uv sync --all-extras
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
│   │   ├── sql_db.py           # PostgreSQL database
│   │   ├── no_sql_db.py        # NoSQL databases (optional)
│   │   └── vector_db.py        # Vector databases (optional)
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
├── pyproject.toml               # Project configuration and dependencies (UV)
├── uv.lock                      # UV lock file (dependency versions)
├── requirements.txt             # Legacy pip dependencies (use pyproject.toml)
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

# Initialize AI Gateway with LiteLLM
gateway = AIGateway(provider="litellm", api_key="your-key")
model = ModelIntegrationFactory.create("litellm", api_key="your-key")
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

### Example 2: Multi-Agent System with Agno

```python
from src.agents.agent import Agent
from src.agents.agent_communication import AgentCommunicator
from agno import LLM

# Create LLM for agents
llm = LLM(model="gpt-4", api_key="your-api-key")

# Create multiple agents using Agno framework
agent1 = Agent(agent_id="agent-1", capabilities=["data_collection"], llm=llm)
agent2 = Agent(agent_id="agent-2", capabilities=["data_analysis"], llm=llm)

# Set up communication
communicator = AgentCommunicator(protocol="nats")
communicator.connect()

agent1.set_communicator(communicator)
agent2.set_communicator(communicator)

# Agents can now communicate
agent1.send_message("agent-2", {"task": "analyze", "data": "..."})
```

### Example 3: PostgreSQL Database Operations

```python
from src.database.sql_db import PostgreSQLDatabase

# PostgreSQL Database
db = PostgreSQLDatabase(connection_string="postgresql://user:pass@localhost/dbname")
db.connect()

# Execute queries
users = db.execute_query("SELECT * FROM users WHERE status = %s", ("active",))

# Execute updates
db.execute_update("INSERT INTO users (name, email) VALUES (%s, %s)", ("John", "john@example.com"))

# Transactions
db.execute_transaction([
    ("INSERT INTO users (name) VALUES (%s)", ("Alice",)),
    ("UPDATE users SET status = %s WHERE name = %s", ("active", "Alice"))
])
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

## Execution Flow

This section explains step-by-step how the SDK processes user input and executes operations. Understanding the execution flow helps you debug issues, optimize performance, and extend the SDK functionality.

### Flow 1: Agent Task Execution Flow

When a user executes a task through an Agent, here's the complete step-by-step execution flow:

**Step 1: User Input**
- User calls `agent.execute_task(task)` with a task dictionary
- Example input: `{"type": "analyze", "data": {"prompt": "Analyze this data..."}}`

**Step 2: Input Validation**
- SDK validates the task structure using `validate_dict()` from `core.validators`
- Checks for required keys: `"type"` and `"data"`
- Validates that `"type"` is a non-empty string
- If validation fails, raises `ValidationError` with detailed field information

**Step 3: Agent State Management**
- Agent status changes from `"idle"` to `"processing"`
- Event emitter emits `"task_started"` event with task information
- Observability module records metrics (task counter incremented, trace span started)

**Step 4: Task Processing (Agno Framework)**
- If Agno agent is initialized (LLM provided), task is processed through Agno framework
- Agno extracts prompt from task data
- Agno agent uses LLM to process the task intelligently
- If Agno is not available, falls back to default task processing

**Step 5: AI Gateway Integration (if needed)**
- If task requires AI processing, Agent may call AI Gateway
- AI Gateway uses LiteLLM to make API calls to OpenAI/Anthropic/Gemini
- LiteLLM handles provider-specific API formatting and authentication
- Response is received and processed

**Step 6: Database Operations (if needed)**
- If task requires data storage/retrieval, Agent may interact with PostgreSQL
- Connection pool (psycopg2) provides database connection
- Query is executed with parameterized inputs for security
- Results are returned to Agent

**Step 7: Response Processing**
- Agent processes the results from AI Gateway and/or Database
- Response is formatted according to task type
- Agent status changes from `"processing"` to `"idle"`

**Step 8: Event Emission & Observability**
- Event emitter emits `"task_completed"` event with task and result
- Observability module records:
  - Performance metrics (latency, throughput)
  - Trace span is finished with duration
  - Success counter is incremented

**Step 9: Return to User**
- Final result is returned to the user
- If any error occurred, appropriate exception is raised (AgentError, ValidationError, etc.)

**Error Handling Throughout:**
- Any validation error → `ValidationError` with field details
- Any agent operation error → `AgentError` with context
- Any connection error → `ConnectionError` with connection details
- All errors are logged and metrics are recorded

---

### Flow 2: AI Gateway Request Flow (LiteLLM)

When a user makes an AI request through the AI Gateway, here's the execution flow:

**Step 1: User Input**
- User calls `gateway.generate(prompt, model)` or `gateway.chat(messages, model)`
- Example: `gateway.generate("Explain quantum computing", model="gpt-4")`

**Step 2: Input Validation**
- SDK validates `prompt` (string, 1-100000 characters)
- SDK validates `model` (string, 1-100 characters, optional)
- SDK validates gateway configuration
- If validation fails, raises `ValidationError`

**Step 3: Input Preprocessing**
- Input is preprocessed using `preprocess_input()` from `input_output.py`
- Text is normalized (whitespace, newlines handled)
- Large text is chunked if necessary
- Data is formatted for the AI model

**Step 4: LiteLLM Provider Initialization**
- LiteLLMProvider checks if LiteLLM is installed
- API key is retrieved from environment or provided parameter
- LiteLLM provider is configured with API key and base URL

**Step 5: Model Selection**
- If model is not specified, default model is used (e.g., "gpt-3.5-turbo")
- Model availability is checked against LiteLLM's model list
- If model is invalid, raises `ModelError`

**Step 6: API Request Preparation**
- Request is formatted according to provider requirements (OpenAI/Anthropic/Gemini format)
- Messages are structured with roles (user, assistant, system)
- Request parameters are set (temperature, max_tokens, etc.)

**Step 7: LiteLLM API Call**
- LiteLLM makes unified API call to the selected provider
- Handles provider-specific authentication automatically
- Manages rate limiting and retries
- Tracks token usage and costs

**Step 8: Response Processing**
- Raw API response is received from the provider
- Response is parsed and structured
- Usage information (tokens, costs) is extracted
- Response is postprocessed using `postprocess_output()`

**Step 9: Output Formatting**
- Response is formatted into SDK's standard format
- Includes: text content, model used, provider, usage statistics
- Response is wrapped in ResponseModel structure

**Step 10: Return to User**
- Formatted response is returned to the user
- If API call failed, raises `APIError` with status code and error details

---

### Flow 3: PostgreSQL Database Operation Flow

When a user executes a database query, here's the execution flow:

**Step 1: User Input**
- User calls `db.execute_query(query, params)` or `db.execute_update(query, params)`
- Example: `db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))`

**Step 2: Input Validation**
- SDK validates `query` (string, 1-10000 characters, non-empty)
- SDK validates `params` (tuple, if provided)
- Validates connection string format (must start with "postgresql://" or "postgres://")
- If validation fails, raises `ValidationError`

**Step 3: Connection Check**
- SDK checks if database connection exists
- If not connected, raises `ConnectionError`
- Connection pool (psycopg2) is checked for available connections

**Step 4: Connection Acquisition**
- Connection is acquired from the connection pool
- If pool is exhausted, waits for available connection (with timeout)
- Connection is validated (ping test)

**Step 5: Query Preparation**
- Query string is validated for SQL injection risks (parameterized queries enforced)
- Parameters are bound to query placeholders
- Query is prepared for execution

**Step 6: Transaction Management (if applicable)**
- If `execute_transaction()` is called, transaction is started
- Multiple queries are executed within the same transaction
- Transaction is committed if all queries succeed
- Transaction is rolled back if any query fails

**Step 7: Query Execution**
- Query is executed on PostgreSQL server via psycopg2
- Execution is monitored for performance (latency tracking)
- Query results are fetched from database

**Step 8: Result Processing**
- Results are converted from database format to Python dictionaries
- Column names are preserved
- Data types are maintained (strings, integers, dates, etc.)

**Step 9: Connection Release**
- Connection is returned to the connection pool
- Connection is marked as available for reuse
- Pool statistics are updated

**Step 10: Observability & Logging**
- Query execution time is recorded in performance monitor
- Success/failure metrics are updated
- Query is logged (with sensitive data redacted)
- Trace span is finished

**Step 11: Return to User**
- Query results are returned to the user
- If query failed, raises `DatabaseError` with query details (truncated for security)

---

### Flow 4: API Communication Flow

When a user makes an external API request, here's the execution flow:

**Step 1: User Input**
- User calls `api.get(endpoint)` or `api.post(endpoint, data)`
- Example: `api.get("/users", params={"status": "active"})`

**Step 2: Input Validation**
- SDK validates `endpoint` (string, non-empty)
- SDK validates `params` or `data` (dict, if provided)
- SDK validates headers (dict, if provided)
- If validation fails, raises `ValidationError`

**Step 3: Authentication**
- If authentication is required, authenticator is called
- OAuth2: Token is retrieved or refreshed
- JWT: Token is generated or validated
- API Key: Key is retrieved from configuration
- Token is added to request headers

**Step 4: Request Preparation**
- Base URL and endpoint are combined
- Request data is encoded using codecs (JSON, Base64, etc.)
- Headers are merged (default + custom + auth)
- Request timeout is set

**Step 5: HTTP Request Execution**
- HTTP request is made using requests library
- Request method (GET, POST, PUT, DELETE) is validated
- Request is sent to external API
- Response is awaited

**Step 6: Response Processing**
- HTTP response is received
- Status code is checked
- Response body is decoded using codecs
- Response headers are extracted

**Step 7: Error Handling**
- If status code indicates error (4xx, 5xx), raises `APIError`
- Error includes: status code, response data, error message
- Retry logic may be triggered (if configured)

**Step 8: Response Formatting**
- Response is wrapped in `ResponseModel` structure
- Includes: status_code, data, headers, timestamp
- Response is logged (with sensitive data redacted)

**Step 9: Observability**
- API call metrics are recorded (request count, latency)
- Trace span is created for distributed tracing
- Success/failure counters are updated

**Step 10: Return to User**
- Formatted response is returned to the user
- If request failed, raises `APIError` with detailed error information

---

### Flow 5: Complete End-to-End Example Flow

Here's a complete flow when a user performs a complex operation involving multiple SDK components:

**Scenario**: User wants to analyze data using an AI agent, store results in database, and send notification via API.

**Step 1: User Initiates Operation**
```python
result = agent.execute_task({
    "type": "analyze_and_store",
    "data": {
        "prompt": "Analyze sales data",
        "store_in_db": True,
        "notify": True
    }
})
```

**Step 2: Agent Receives and Validates Input**
- Agent validates task structure (type, data keys)
- Agent status changes to "processing"
- Event "task_started" is emitted

**Step 3: Agent Processes Task via Agno**
- Agno agent extracts prompt from task data
- Agno uses LLM (via LiteLLM) to analyze the prompt
- AI Gateway is called internally

**Step 4: AI Gateway Processes Request**
- LiteLLM formats request for OpenAI/Anthropic
- API call is made to AI provider
- Response is received and processed
- Analysis result is generated

**Step 5: Database Storage (if requested)**
- Agent checks if `store_in_db` is True
- PostgreSQL connection is acquired from pool
- Analysis result is inserted into database
- Transaction is committed
- Connection is released

**Step 6: API Notification (if requested)**
- Agent checks if `notify` is True
- API Communicator sends notification via external API
- Authentication token is retrieved
- HTTP POST request is made
- Notification is sent

**Step 7: Result Aggregation**
- Agent combines results from:
  - AI analysis result
  - Database storage confirmation
  - API notification status
- Final result is formatted

**Step 8: Observability & Events**
- All operations are traced (distributed tracing)
- Metrics are recorded (latency, success rates)
- Event "task_completed" is emitted
- Performance statistics are updated

**Step 9: Return to User**
- Complete result is returned:
```python
{
    "status": "completed",
    "analysis": "AI analysis result...",
    "database_id": "12345",
    "notification_sent": True,
    "duration": 2.5  # seconds
}
```

**Error Handling:**
- If any step fails, appropriate exception is raised
- Partial results are logged
- Rollback is performed (database transaction, if applicable)
- Error is propagated to user with context

---

### Key Execution Principles

1. **Validation First**: All inputs are validated before processing begins
2. **Error Handling**: Errors are caught, logged, and converted to SDK exceptions
3. **Observability**: All operations are monitored, traced, and measured
4. **Resource Management**: Connections, threads, and resources are properly managed
5. **Type Safety**: Type hints ensure correct data types throughout the flow
6. **Thread Safety**: All operations are thread-safe for concurrent use
7. **Event-Driven**: Important events are emitted for external listeners
8. **Modular Design**: Each component can be used independently or together

Understanding these execution flows helps you:
- Debug issues by tracing through the steps
- Optimize performance by identifying bottlenecks
- Extend functionality by adding custom steps
- Monitor operations using observability metrics

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

| Library | Purpose |
|---------|---------|
| **litellm** | Unified AI gateway for accessing multiple AI providers (OpenAI, Anthropic, Gemini, etc.) |
| **agno** | Agent framework for building autonomous AI agents |
| **psycopg2-binary** | PostgreSQL database adapter with connection pooling |
| **requests** | HTTP library for API communication |
| **pydantic** | Data validation and settings management |
| **python-dotenv** | Environment variable management |

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

- `Agent` - Main agent class integrating with Agno framework for intelligent task processing
- `AgentCommunicator` - Base communicator for agent-to-agent communication
- `NATSCommunicator` - NATS-specific communicator implementation

### AI Gateway Module (`src/ai_gateway/`)

- `AIGateway` - Main gateway interface for AI model interactions
- `ModelProvider` - Abstract base class for model providers
- `LiteLLMProvider` - LiteLLM provider implementation (unified interface for OpenAI, Anthropic, Gemini, etc.)
- `ModelIntegrationFactory` - Factory for creating LiteLLM model integrations
- `PromptManager` - Manager for prompts and templates
- `PromptTemplate` - Prompt template class
- `preprocess_input()` - Preprocess input data for AI model
- `postprocess_output()` - Postprocess AI model output
- `normalize_text()` - Normalize text input
- `chunk_text()` - Split text into chunks with overlap
- `format_messages()` - Format messages for chat API

### Database Module (`src/database/`)

**PostgreSQL Database (Primary):**
- `PostgreSQLDatabase` - PostgreSQL database connection and operations with connection pooling (psycopg2)
- `SQLDatabase` - Alias for PostgreSQLDatabase (backward compatibility)

**NoSQL Databases (Optional):**
- `NoSQLDatabase` - Base NoSQL database connection and operations
- `MongoDBDatabase` - MongoDB-specific implementation
- `CassandraDatabase` - Cassandra-specific implementation

**Vector Databases (Optional):**
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
- **pyproject.toml** - Project configuration and dependencies (UV format)
- **uv.lock** - Locked dependency versions (managed by UV)
- **requirements.txt** - Legacy pip dependencies (kept for compatibility, use pyproject.toml)
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

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies with development extras
uv sync --all-extras

# Run tests
uv run pytest src/tests/

# Run tests with coverage
uv run pytest src/tests/ --cov=src --cov-report=html
pytest src/tests/ --cov=src --cov-report=html
```

## License

See [LICENSE](LICENSE) file for license information.

---

**Need Help?** Check the module-specific README files in each directory, or open an issue for support.

