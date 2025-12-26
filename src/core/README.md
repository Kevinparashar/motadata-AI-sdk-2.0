# Core Components

## WHY

The core module provides fundamental building blocks and utilities that are used throughout the SDK. These components establish the foundation for data structures, concurrency handling, event management, and common utilities that other modules depend on.

## WHAT

This module contains:

- **data_structures.py**: Core data models and structures used across the SDK (e.g., request/response models, configuration objects)
- **concurrency.py**: Concurrency utilities for handling asyncio operations, threading, and parallel processing
- **event_handler.py**: Event handling logic for managing SDK events, callbacks, and asynchronous notifications
- **utils.py**: Helper functions for logging, configuration parsing, validation, and other common operations
- **exceptions.py**: Custom exception classes for better error handling and debugging
- **validators.py**: Input validation utilities for sanitizing and validating user input

## HOW

Import and use core components in your code:

```python
from src.core.data_structures import RequestModel, ResponseModel
from src.core.concurrency import AsyncExecutor, ThreadPool
from src.core.event_handler import EventHandler, EventEmitter
from src.core.utils import setup_logger, validate_config
from src.core.exceptions import ValidationError, APIError, SDKError
from src.core.validators import validate_string, validate_dict, validate_list

# Using custom exceptions
try:
    validate_config(config, ["api_key", "api_url"])
except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"Missing field: {e.field}")

# Using validators
validated_string = validate_string(
    user_input,
    field_name="username",
    min_length=3,
    max_length=20
)
```

These components are typically used internally by other SDK modules, but can also be used directly in your application code when needed.

## Input Validation and Error Handling

**All public methods across the SDK now include comprehensive input validation** using the validators module. This ensures:

- **Type Safety**: All inputs are validated for correct types before processing
- **Range Checking**: String lengths, list sizes, and numeric ranges are validated
- **Required Fields**: Required dictionary keys and list items are checked
- **Custom Exceptions**: All validation failures raise `ValidationError` with detailed field and value information

**Custom Exception Hierarchy**: The SDK uses a custom exception hierarchy instead of built-in Python exceptions:

- **SDKError**: Base exception for all SDK errors (replaces generic `Exception`)
- **ValidationError**: Input validation failures (replaces `ValueError`, `TypeError`)
- **ConnectionError**: Connection failures (replaces built-in `ConnectionError`)
- **ConfigurationError**: Configuration issues (replaces `FileNotFoundError`, `ValueError` for config)
- **APIError**: API request failures (includes status codes and response data)
- **DatabaseError**: Database operation failures
- **CodecError**: Encoding/decoding failures
- **AgentError**: Agent operation failures
- **ModelError**: AI model operation failures
- **AuthenticationError**: Authentication failures

All exceptions include detailed error messages and optional `details` dictionary for debugging.

## Version Management

The SDK version is managed in `src/__version__.py`:

```python
from src import __version__
print(__version__)  # "0.1.0"
```

## Libraries

This module uses the following Python standard libraries and packages:

- **typing**: Type hints for function parameters and return types (Dict, Any, Optional, List, Callable, Coroutine)
- **dataclasses**: Data class decorators for creating structured data models
- **datetime**: Date and time handling for timestamps
- **asyncio**: Asynchronous programming support
- **concurrent.futures**: Thread pool execution (ThreadPoolExecutor, Executor)
- **threading**: Thread synchronization primitives (Thread, Lock)
- **enum**: Enumeration support for event types
- **logging**: Logging framework for application logging
- **os**: Operating system interface for environment variables
- **pathlib**: Object-oriented filesystem paths

## Configuration Files

This module works with the following project configuration:

- **pyproject.toml**: Project metadata and tool configurations (black, isort, mypy, pytest)
- **.coveragerc**: Test coverage configuration
- **requirements.txt**: Production dependencies
- **requirements-dev.txt**: Development dependencies (linting, formatting, testing tools)
- **requirements-test.txt**: Test-specific dependencies

## Functions and Classes

### data_structures.py

- **RequestModel** (class): Base request model for API requests with method, URL, headers, params, data, and timestamp
- **ResponseModel** (class): Base response model for API responses with status_code, data, headers, timestamp, and error
- **ConfigModel** (class): Configuration data model with api_url, api_key, timeout, retry_count, and settings

### concurrency.py

- **AsyncExecutor** (class): Async executor for running async functions with event loop management
  - `execute()`: Execute a function asynchronously
  - `run()`: Run a coroutine in the event loop
  - `shutdown()`: Shutdown the executor
- **ThreadPool** (class): Thread pool for parallel execution
  - `submit()`: Submit a task to the thread pool
  - `map()`: Map function over iterable in parallel
  - `shutdown()`: Shutdown the thread pool
- **ThreadSafeCounter** (class): Thread-safe counter with lock protection
  - `increment()`: Increment the counter
  - `decrement()`: Decrement the counter
  - `value` (property): Get the current value

### event_handler.py

- **EventType** (enum): Event type enumeration (INFO, WARNING, ERROR, SUCCESS, CUSTOM)
- **EventHandler** (class): Base event handler for managing events
  - `on()`: Register an event handler
  - `off()`: Unregister an event handler
  - `emit()`: Emit an event
  - `once()`: Register a one-time event handler
- **EventEmitter** (class): Event emitter for asynchronous event handling
  - `on()`: Register an event handler
  - `off()`: Unregister an event handler
  - `emit()`: Emit an event
  - `once()`: Register a one-time event handler

### utils.py

- **setup_logger()**: Setup and configure a logger with custom format and output
- **validate_config()**: Validate configuration dictionary for required keys (raises ValidationError)
- **get_env_var()**: Get environment variable with optional default
- **ensure_dir()**: Ensure directory exists, create if it doesn't
- **merge_dicts()**: Merge multiple dictionaries into one

### exceptions.py

- **SDKError** (class): Base exception for all SDK errors with message and details support
- **ConfigurationError** (class): Raised when there's a configuration error
- **AuthenticationError** (class): Raised when authentication fails
- **ConnectionError** (class): Raised when connection to external service fails
- **ValidationError** (class): Raised when input validation fails (includes field and value info)
- **APIError** (class): Raised when API request fails (includes status_code and response)
- **DatabaseError** (class): Raised when database operation fails
- **CodecError** (class): Raised when encoding/decoding fails
- **AgentError** (class): Raised when agent operation fails
- **ModelError** (class): Raised when AI model operation fails
- **EventHandlerError** (class): Raised when event handler operation fails

### validators.py

- **validate_string()**: Validate and sanitize string input with length constraints
- **validate_dict()**: Validate dictionary input with required keys checking
- **validate_list()**: Validate list input with item count constraints
- **validate_int()**: Validate integer input with range checking
- **validate_bool()**: Validate boolean input
- **validate_url()**: Validate URL format
- **validate_email()**: Validate email format
- **validate_uuid()**: Validate UUID format
