# Source Code Directory

## WHY
This directory contains the core source code for the Metadata Python SDK. It is organized into logical modules that handle different aspects of the SDK's functionality, making the codebase maintainable, scalable, and easy to understand.

## WHAT
The `src/` directory is the main package directory containing all SDK modules:

- **core/**: Core components and utilities that form the foundation of the SDK
- **agents/**: Agent-related functionality using Agno framework for autonomous AI agents
- **ai_gateway/**: AI Gateway components using LiteLLM for unified access to multiple AI models
- **database/**: PostgreSQL database integration module
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
from src.database.sql_db import PostgreSQLDatabase
```

Each module is designed to be imported independently, allowing you to use only the components you need for your specific use case.

## Libraries
The SDK modules use various Python standard libraries and packages:

- **Standard Library**: typing, dataclasses, datetime, asyncio, threading, enum, logging, os, pathlib, json, base64, abc, concurrent.futures
- **Third-party**: 
  - **litellm**: Unified AI gateway for multiple providers
  - **agno**: Agent framework for autonomous AI agents
  - **psycopg2-binary**: PostgreSQL database adapter
  - Dependencies are managed in `requirements.txt`, `requirements-dev.txt`, and `requirements-test.txt`

## Project Configuration
The SDK uses modern Python packaging and development tools:

- **pyproject.toml**: Project metadata, build system, and tool configurations (black, isort, mypy, pytest)
- **setup.py**: Package installation script with version management from `src/__version__.py`
- **MANIFEST.in**: Specifies non-Python files to include in distribution
- **.gitignore**: Version control ignore patterns
- **.gitattributes**: Line ending and file type handling
- **.coveragerc**: Test coverage configuration
- **.env.example**: Environment variable template (copy to .env for local development)

## Functions and Classes
Each module in the `src/` directory contains its own set of functions and classes. For detailed information about specific functions and classes, refer to the README.md file in each module directory:

- **core/**: Data models, concurrency utilities, event handlers, and utility functions
- **agents/**: Agent classes using Agno framework and communication handlers
- **ai_gateway/**: AI Gateway interface using LiteLLM, prompt management, and I/O processing
- **database/**: PostgreSQL database implementation with connection pooling
- **codecs/**: Encoding/decoding codecs and utilities
- **api/**: API communication, authentication, and request/response handling
- **config/**: Configuration management and logging setup
- **tests/**: Unit test classes for all SDK components

