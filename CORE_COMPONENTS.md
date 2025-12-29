# Core Components

This document provides a high-level overview of the core components in the Metadata Python SDK with one-line explanations.

## Table of Contents

- [Agents](#agents)
- [AI Gateway](#ai-gateway)
- [Database](#database)
- [API](#api)
- [Codecs](#codecs)
- [Config](#config)
- [Core Foundation](#core-foundation)

---

## Agents

**Module**: `src/agents/`

- **Agent** - Main agent class integrating with Agno framework for creating and managing autonomous AI agents.
- **AgentCommunicator** - Base communicator for enabling agents to send and receive messages, coordinate tasks, and share information.
- **NATSCommunicator** - NATS-specific communicator implementation for message queuing and agent coordination.

**Purpose**: Enables creation and management of autonomous AI agents that can communicate, process information, and execute tasks using the Agno framework.

---

## AI Gateway

**Module**: `src/ai_gateway/`

- **AIGateway** - Main gateway interface providing a unified API for interacting with multiple AI models and services.
- **ModelProvider** - Abstract base class for model providers defining the interface for AI model interactions.
- **LiteLLMProvider** - LiteLLM provider integration offering unified access to multiple AI providers (OpenAI, Anthropic, Gemini, etc.).
- **ModelIntegrationFactory** - Factory for creating and managing LiteLLM model integrations.
- **PromptManager** - Manager for handling prompt templates, fine-tuning configurations, and dynamic prompt generation.
- **PromptTemplate** - Prompt template class for managing reusable prompt templates with variable substitution.
- **preprocess_input()** - Preprocess input data for AI model compatibility (supports str, dict, list formats).
- **postprocess_output()** - Postprocess AI model output for application use with JSON parsing support.
- **normalize_text()** - Normalize text input by stripping whitespace and replacing special characters.
- **chunk_text()** - Split text into chunks with overlap for processing large text inputs.
- **format_messages()** - Format messages for chat API with optional system prompt support.

**Purpose**: Provides a unified interface for interacting with various AI models, abstracting away provider-specific complexities and allowing seamless switching between models.

---

## Database

**Module**: `src/database/`

- **PostgreSQLDatabase** - PostgreSQL database integration with optimized connection pooling, transaction handling, and query execution.
- **NoSQLDatabase** - Base NoSQL database integration for document and key-value stores like MongoDB, Cassandra, and Redis.
- **MongoDBDatabase** - MongoDB-specific database implementation for document storage.
- **CassandraDatabase** - Cassandra-specific database implementation for distributed NoSQL storage.
- **VectorDatabase** - Base vector database integration for similarity search and embeddings storage.
- **FAISSDatabase** - FAISS vector database implementation with index save/load capabilities.
- **PineconeDatabase** - Pinecone vector database implementation with index creation and management.

**Purpose**: Provides database integration capabilities for PostgreSQL (primary), NoSQL databases, and vector databases with optimized connection management.

---

## API

**Module**: `src/api/`

- **APICommunicator** - Core API communication methods for HTTP requests (GET, POST, PUT, DELETE) and WebSocket connections.
- **WebSocketCommunicator** - WebSocket communicator for real-time bidirectional communication.
- **Authenticator** - Abstract base class for authentication mechanisms defining the authentication interface.
- **OAuth2Authenticator** - OAuth2 authentication mechanism with token refresh support.
- **JWTAuthenticator** - JWT token authentication with encoding and decoding capabilities.
- **APIKeyAuthenticator** - API key authentication for simple key-based authentication.
- **encode_data()** - Encode data for API transmission in various formats (JSON, base64, etc.).
- **decode_data()** - Decode data from API response into Python objects.
- **send_request()** - Send an HTTP request with authentication and error handling.
- **prepare_request_data()** - Prepare and format data for API request transmission.
- **parse_response()** - Parse API response into structured format for application use.

**Purpose**: Handles all external API communication, authentication, and request/response management with built-in error handling and retries.

---

## Codecs

**Module**: `src/codecs/`

- **Codec** - Abstract base class for codecs with encode and decode methods.
- **JSONCodec** - JSON encoding/decoding codec for structured data serialization.
- **Base64Codec** - Base64 encoding/decoding codec for binary data transformation.
- **BinaryCodec** - Binary encoding/decoding codec for raw binary data handling.
- **CustomCodec** - Custom codec with configurable encoding/decoding formats.
- **register_codec()** - Register a custom codec in the codec registry for reuse.
- **get_codec()** - Get a codec instance by name from the registry.
- **list_codecs()** - List all registered codecs in the registry.
- **validate_encoded_data()** - Validate that data can be decoded with the given codec.
- **encode_with_format()** - Quick encode function with format specification.
- **decode_with_format()** - Quick decode function with format specification.

**Purpose**: Provides custom encoding and decoding functionality for transforming data between different formats and protocols.

---

## Config

**Module**: `src/config/`

- **Settings** - Configuration settings manager supporting loading from files, environment variables, and command-line arguments.
- **load_config()** - Load configuration from file or environment variables.
- **setup_logger()** - Setup and configure a logger with custom settings (name, level, format, output_file, console).
- **get_logger()** - Get a logger instance by name for application logging.
- **configure_logging()** - Configure root logger for the SDK with standard settings.
- **LoggerMixin** - Mixin class to add logging capability to any class.

### Observability

- **Observability** - Main observability class integrating all observability features (metrics, tracing, monitoring, health checks).
- **MetricsRegistry** - Registry for managing metrics (counters, gauges, histograms) with label support.
- **Counter** - Counter metric that increments only for tracking totals (e.g., requests_total, errors_total).
- **Gauge** - Gauge metric that can increase or decrease for tracking current values (e.g., active_connections, queue_size).
- **Histogram** - Histogram metric that tracks distribution of values with percentiles (e.g., request_duration, response_size).
- **Tracer** - Distributed tracing system for request tracing across services with span management.
- **TraceSpan** - Represents a span in a distributed trace with tags, logs, and parent-child relationships.
- **PerformanceMonitor** - Performance monitoring for latency tracking, throughput monitoring, and resource usage.
- **HealthCheck** - Health check for system components with timeout support and status reporting.
- **HealthChecker** - Registry for health checks with status reporting and timeout management.
- **get_observability()** - Get or create global observability instance.
- **set_observability()** - Set global observability instance.

**Purpose**: Centralizes configuration management, logging setup, and observability features for the entire SDK.

---

## Core Foundation

**Module**: `src/core/`

### Data Structures

- **RequestModel** - Base request model for API requests with method, URL, headers, params, data, and timestamp.
- **ResponseModel** - Base response model for API responses with status_code, data, headers, timestamp, and error.
- **ConfigModel** - Configuration data model with api_url, api_key, timeout, retry_count, and settings.

### Concurrency

- **AsyncExecutor** - Async executor for running async functions with event loop management.
- **ThreadPool** - Thread pool for parallel execution of tasks with submit and map methods.
- **ThreadSafeCounter** - Thread-safe counter with lock protection for concurrent operations.

### Event Handler

- **EventType** - Event type enumeration (INFO, WARNING, ERROR, SUCCESS, CUSTOM).
- **EventHandler** - Base event handler for managing events with on, off, emit, and once methods.
- **EventEmitter** - Event emitter for asynchronous event handling across the SDK.

### Exceptions

- **SDKError** - Base exception for all SDK errors with message and details support.
- **ValidationError** - Input validation failures with field and value information.
- **APIError** - API request failures with status codes and response data.
- **DatabaseError** - Database operation failures with detailed error context.
- **ConnectionError** - Connection failures to external services.
- **ConfigurationError** - Configuration issues and file loading errors.
- **CodecError** - Encoding/decoding failures in codec operations.
- **AgentError** - Agent operation failures in agent lifecycle management.
- **ModelError** - AI model operation failures in model interactions.
- **AuthenticationError** - Authentication failures in API and service authentication.
- **EventHandlerError** - Event handler operation failures in event management.

### Validators

- **validate_string()** - Validate and sanitize string input with length constraints.
- **validate_dict()** - Validate dictionary input with required keys checking.
- **validate_list()** - Validate list input with item count constraints.
- **validate_int()** - Validate integer input with range checking.
- **validate_bool()** - Validate boolean input type and value.
- **validate_url()** - Validate URL format and structure.
- **validate_email()** - Validate email format and structure.
- **validate_uuid()** - Validate UUID format and structure.

### Utils

- **setup_logger()** - Setup and configure a logger with custom format and output.
- **validate_config()** - Validate configuration dictionary for required keys.
- **get_env_var()** - Get environment variable with optional default value.
- **ensure_dir()** - Ensure directory exists, create if it doesn't.
- **merge_dicts()** - Merge multiple dictionaries into one.

**Purpose**: Provides fundamental building blocks and utilities that form the foundation for all other SDK modules.

---

## Technology Stack

- **LiteLLM** - Unified AI gateway for multiple AI providers (OpenAI, Anthropic, Gemini, etc.)
- **Agno** - Agent framework for building autonomous AI agents
- **PostgreSQL** - Primary relational database with psycopg2 adapter
- **UV** - Fast Python package manager and dependency resolver
- **Python 3.8.1+** - Programming language and runtime environment

---

## Architecture Flow

```
Application Layer
    ↓
Agents → AI Gateway → Database → API → Codecs
    ↓
Core Foundation (Data Structures, Concurrency, Events, Exceptions, Validators, Utils)
    ↓
Config (Settings, Logging, Observability)
    ↓
External Services (LiteLLM, PostgreSQL, External APIs, Monitoring Tools)
```

---

## Version

Current SDK version: **0.1.0**

Version is managed in `src/__version__.py` as a single source of truth.
