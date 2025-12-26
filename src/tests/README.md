# Tests Module

## WHY
The tests module contains comprehensive unit tests for all SDK components. Having a robust test suite ensures code quality, prevents regressions, and provides documentation through examples of how each component should be used.

## WHAT
This module contains:

- **test_agents.py**: Unit tests for agent functionality, agent communication, lifecycle management, and agent coordination scenarios
- **test_ai_gateway.py**: Unit tests for AI Gateway integration, model interactions, prompt management, and input/output processing
- **test_database.py**: Unit tests for database integrations including SQL, NoSQL, and vector database operations, connection handling, and query execution
- **test_codecs.py**: Unit tests for codec functionality, encoding/decoding operations, format validation, and codec registry
- **test_api.py**: Unit tests for API communication, authentication mechanisms, request/response handling, and error scenarios

## HOW
Run the test suite:

```bash
# Install test dependencies first
pip install -r requirements-test.txt

# Run all tests
pytest src/tests/

# Run specific test file
pytest src/tests/test_agents.py

# Run with coverage (configured in .coveragerc)
pytest src/tests/ --cov=src --cov-report=html --cov-report=term-missing

# Run specific test
pytest src/tests/test_agents.py::TestAgent::test_agent_creation

# Run tests with markers
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

Tests use the pytest framework and include:
- Unit tests for individual components
- Integration tests for module interactions
- Mock objects for external dependencies
- Shared fixtures in `conftest.py` for common test data and setup

Each test file focuses on a specific module and tests both happy paths and error scenarios.

## Test Fixtures
The `conftest.py` file provides shared fixtures:
- **sample_agent_config**: Sample agent configuration dictionary
- **sample_task**: Sample task dictionary for testing
- **sample_api_config**: Sample API configuration dictionary
- **sample_db_config**: Sample database configuration dictionary

Usage:
```python
def test_agent_with_fixture(sample_agent_config):
    agent = Agent(**sample_agent_config)
    assert agent.agent_id == "test-agent"
```

## Libraries
This module uses the following Python standard libraries and packages:

- **unittest**: Python's built-in unit testing framework
- **pytest**: Third-party testing framework (recommended for running tests)
- **pytest-cov**: Test coverage plugin for pytest
- **pytest-mock**: Mocking utilities for pytest
- **pytest-asyncio**: Async test support
- **coverage**: Code coverage measurement tool
- **src.agents**: Agent and AgentCommunicator classes for testing
- **src.ai_gateway**: AIGateway and PromptManager classes for testing
- **src.database**: SQLDatabase, NoSQLDatabase, and VectorDatabase classes for testing
- **src.codecs**: Codec classes for testing
- **src.api**: APICommunicator and authentication classes for testing

## Configuration Files
- **conftest.py**: Shared pytest fixtures for all tests
- **.coveragerc**: Coverage configuration file
- **requirements-test.txt**: Test-specific dependencies
- **pyproject.toml**: Pytest configuration in [tool.pytest.ini_options]

## Functions and Classes

### test_agents.py
- **TestAgent** (class): Test cases for Agent class
  - `setUp()`: Set up test fixtures
  - `test_agent_creation()`: Test agent creation
  - `test_agent_start_stop()`: Test agent start and stop
  - `test_agent_execute_task()`: Test task execution
- **TestAgentCommunicator** (class): Test cases for AgentCommunicator
  - `setUp()`: Set up test fixtures
  - `test_communicator_creation()`: Test communicator creation

### test_ai_gateway.py
- **TestAIGateway** (class): Test cases for AIGateway
  - `setUp()`: Set up test fixtures
  - `test_gateway_creation()`: Test gateway creation
- **TestPromptManager** (class): Test cases for PromptManager
  - `setUp()`: Set up test fixtures
  - `test_prompt_manager_creation()`: Test prompt manager creation
  - `test_get_template()`: Test getting a template
  - `test_list_templates()`: Test listing templates

### test_database.py
- **TestSQLDatabase** (class): Test cases for SQLDatabase
  - `setUp()`: Set up test fixtures
  - `test_database_creation()`: Test database creation
- **TestNoSQLDatabase** (class): Test cases for NoSQLDatabase
  - `setUp()`: Set up test fixtures
  - `test_database_creation()`: Test database creation
- **TestVectorDatabase** (class): Test cases for VectorDatabase
  - `setUp()`: Set up test fixtures
  - `test_database_creation()`: Test database creation

### test_codecs.py
- **TestJSONCodec** (class): Test cases for JSONCodec
  - `setUp()`: Set up test fixtures
  - `test_encode_decode()`: Test encoding and decoding
- **TestBase64Codec** (class): Test cases for Base64Codec
  - `setUp()`: Set up test fixtures
  - `test_encode_decode()`: Test encoding and decoding
- **TestCustomCodec** (class): Test cases for CustomCodec
  - `test_codec_creation()`: Test custom codec creation
  - `test_get_codec()`: Test getting codec from registry
  - `test_list_codecs()`: Test listing codecs

### test_api.py
- **TestAPICommunicator** (class): Test cases for APICommunicator
  - `setUp()`: Set up test fixtures
  - `test_communicator_creation()`: Test communicator creation
  - `test_set_auth()`: Test setting authentication
- **TestOAuth2Authenticator** (class): Test cases for OAuth2Authenticator
  - `setUp()`: Set up test fixtures
  - `test_authenticator_creation()`: Test authenticator creation
- **TestJWTAuthenticator** (class): Test cases for JWTAuthenticator
  - `setUp()`: Set up test fixtures
  - `test_authenticator_creation()`: Test authenticator creation
- **TestAPIKeyAuthenticator** (class): Test cases for APIKeyAuthenticator
  - `setUp()`: Set up test fixtures
  - `test_authenticator_creation()`: Test authenticator creation
  - `test_get_access_token()`: Test getting access token

