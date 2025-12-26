"""
Config settings (URLs, credentials)
"""
from typing import Dict, Any, Optional
import os
import json
from pathlib import Path
from ..core.utils import get_env_var, validate_config
from ..core.validators import validate_string, validate_dict
from ..core.exceptions import ConfigurationError, ValidationError
import logging


class Settings:
    """Configuration settings manager"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or {}
        self._load_from_env()
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables"""
        env_mappings = {
            "API_BASE_URL": "api.base_url",
            "API_KEY": "api.key",
            "API_TIMEOUT": "api.timeout",
            "DB_CONNECTION_STRING": "database.connection_string",
            "LOG_LEVEL": "logging.level",
        }
        
        for env_key, config_key in env_mappings.items():
            value = get_env_var(env_key)
            if value:
                self.set(config_key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def update(self, config: Dict[str, Any]) -> None:
        """Update configuration with a dictionary"""
        self._config.update(config)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return self._config.copy()
    
    @classmethod
    def from_file(cls, file_path: str) -> 'Settings':
        """Load settings from a JSON or YAML file
        
        Args:
            file_path: Path to configuration file
        
        Returns:
            Settings instance
        
        Raises:
            ValidationError: If file_path is invalid
            ConfigurationError: If file not found or format unsupported
        """
        file_path = validate_string(file_path, "file_path", min_length=1)
        path = Path(file_path)
        if not path.exists():
            raise ConfigurationError(f"Config file not found: {file_path}")
        
        try:
            with open(path, 'r') as f:
                if path.suffix == '.json':
                    config = json.load(f)
                    if not isinstance(config, dict):
                        raise ConfigurationError("Config file must contain a JSON object")
                else:
                    # YAML loading would go here if yaml library is available
                    raise ConfigurationError(
                        f"Unsupported config file format: {path.suffix}",
                        details={"supported_formats": [".json"]}
                    )
            
            return cls(config=config)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file: {str(e)}", details={"file": file_path})
        except Exception as e:
            raise ConfigurationError(f"Failed to load config file: {str(e)}", details={"file": file_path})
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Create settings from environment variables"""
        return cls()
    
    def save_to_file(self, file_path: str) -> None:
        """Save settings to a file
        
        Args:
            file_path: Path to save configuration file
        
        Raises:
            ValidationError: If file_path is invalid
            ConfigurationError: If file format is unsupported or save fails
        """
        file_path = validate_string(file_path, "file_path", min_length=1)
        path = Path(file_path)
        try:
            with open(path, 'w') as f:
                if path.suffix == '.json':
                    json.dump(self._config, f, indent=2)
                else:
                    raise ConfigurationError(
                        f"Unsupported config file format: {path.suffix}",
                        details={"supported_formats": [".json"]}
                    )
        except Exception as e:
            raise ConfigurationError(f"Failed to save config file: {str(e)}", details={"file": file_path})


def load_config(file_path: Optional[str] = None) -> Settings:
    """Load configuration from file or environment"""
    if file_path:
        return Settings.from_file(file_path)
    else:
        return Settings.from_env()
