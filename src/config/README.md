# Configuration Module

## WHY
The config module centralizes configuration management and logging setup for the entire SDK. It ensures consistent configuration handling, environment-based settings, and proper logging across all SDK components.

## WHAT
This module contains:

- **settings.py**: Configuration settings management including URLs, credentials, API endpoints, feature flags, and environment-specific configurations. Supports loading from files, environment variables, and command-line arguments
- **logging.py**: Custom logging configuration with support for multiple log levels, output formats, log rotation, and integration with standard logging frameworks

## HOW
Configure the SDK using the config module:

```python
from src.config.settings import Settings, load_config
from src.config.logging import setup_logger, get_logger

# Load configuration
config = load_config(config_file="config.yaml")
# Or use environment variables
config = Settings.from_env()

# Access settings
api_url = config.get("api.base_url")
api_key = config.get("api.key")

# Set up logging
setup_logger(level="INFO", format="json", output_file="sdk.log")
logger = get_logger(__name__)
logger.info("SDK initialized")
```

Configuration can be loaded from YAML files, JSON files, environment variables, or passed programmatically. The logging system integrates seamlessly with Python's standard logging module.

