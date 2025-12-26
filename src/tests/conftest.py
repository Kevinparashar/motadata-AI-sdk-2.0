"""
Pytest configuration and shared fixtures
"""
import pytest
from typing import Dict, Any


@pytest.fixture
def sample_agent_config() -> Dict[str, Any]:
    """Sample agent configuration for testing"""
    return {
        "agent_id": "test-agent",
        "capabilities": ["test"],
        "config": {"test": True}
    }


@pytest.fixture
def sample_task() -> Dict[str, Any]:
    """Sample task dictionary for testing"""
    return {
        "type": "test",
        "data": "test_data",
        "metadata": {"test": True}
    }


@pytest.fixture
def sample_api_config() -> Dict[str, Any]:
    """Sample API configuration for testing"""
    return {
        "base_url": "https://api.test.com",
        "timeout": 30,
        "headers": {"Content-Type": "application/json"}
    }


@pytest.fixture
def sample_db_config() -> Dict[str, Any]:
    """Sample database configuration for testing"""
    return {
        "connection_string": "sqlite:///:memory:",
        "database_name": "test_db"
    }

