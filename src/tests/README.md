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
# Run all tests
pytest src/tests/

# Run specific test file
pytest src/tests/test_agents.py

# Run with coverage
pytest src/tests/ --cov=src --cov-report=html

# Run specific test
pytest src/tests/test_agents.py::test_agent_creation
```

Tests use the pytest framework and include:
- Unit tests for individual components
- Integration tests for module interactions
- Mock objects for external dependencies
- Fixtures for common test data and setup

Each test file focuses on a specific module and tests both happy paths and error scenarios.

