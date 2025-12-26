"""
Helper functions (logging, configurations)
"""
import logging
import os
from typing import Dict, Any, Optional, List
from pathlib import Path
from .exceptions import ValidationError


def setup_logger(
    name: str = "sdk",
    level: str = "INFO",
    format: str = "standard",
    output_file: Optional[str] = None
) -> logging.Logger:
    """Setup and configure a logger"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatter
    if format == "json":
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if output_file:
        file_handler = logging.FileHandler(output_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def validate_config(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """Validate configuration dictionary
    
    Args:
        config: Configuration dictionary to validate
        required_keys: List of required keys that must be present in config
    
    Returns:
        True if validation passes
    
    Raises:
        ValidationError: If required keys are missing from config
    
    Example:
        >>> config = {"api_key": "test", "api_url": "https://api.com"}
        >>> validate_config(config, ["api_key", "api_url"])
        True
        >>> validate_config(config, ["api_key", "missing"])
        ValidationError: Missing required configuration keys: ['missing']
    """
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValidationError(
            f"Missing required configuration keys: {missing_keys}",
            details={"missing_keys": missing_keys, "config_keys": list(config.keys())}
        )
    return True


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with optional default"""
    return os.getenv(key, default)


def ensure_dir(path: str) -> Path:
    """Ensure directory exists, create if it doesn't"""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result
