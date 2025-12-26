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

## Input Validation and Error Handling

**All public methods in the config module include comprehensive input validation:**

- **Settings.from_file()**: Validates `file_path` (string, non-empty), checks file exists, validates JSON format (must be object), and handles JSON decode errors
- **Settings.save_to_file()**: Validates `file_path` (string, non-empty) and file format (must be .json)

**Custom Exceptions Used:**
- `ValidationError`: Invalid input parameters (replaces `ValueError`, `TypeError`)
- `ConfigurationError`: Configuration and file loading errors (replaces `FileNotFoundError`, `ValueError`, `json.JSONDecodeError`)

All methods raise appropriate custom exceptions with detailed error messages and context information for debugging.

## Libraries
This module uses the following Python standard libraries and packages:

- **typing**: Type hints (Dict, Any, Optional)
- **os**: Operating system interface for environment variables
- **json**: JSON encoding and decoding for configuration file parsing
- **pathlib**: Object-oriented filesystem paths for configuration file management
- **logging**: Logging framework for application logging
- **sys**: System-specific parameters and functions for logging output
- **src.core.utils**: get_env_var and validate_config from core module

## Functions and Classes

### settings.py
- **Settings** (class): Configuration settings manager
  - `__init__()`: Initialize settings with optional config dictionary
  - `_load_from_env()`: Load configuration from environment variables
  - `get()`: Get a configuration value by key (supports dot notation)
  - `set()`: Set a configuration value by key (supports dot notation)
  - `update()`: Update configuration with a dictionary
  - `to_dict()`: Convert settings to dictionary
  - `from_file()`: Class method to load settings from a JSON or YAML file
  - `from_env()`: Class method to create settings from environment variables
  - `save_to_file()`: Save settings to a file
- **load_config()**: Load configuration from file or environment

### logging.py
- **setup_logger()**: Setup and configure a logger with custom settings (name, level, format, output_file, console)
- **get_logger()**: Get a logger instance by name
- **configure_logging()**: Configure root logger for the SDK
- **LoggerMixin** (class): Mixin class to add logging capability to any class
  - `logger` (property): Get logger for this class

