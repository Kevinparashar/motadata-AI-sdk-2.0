"""
Custom logging configuration
"""
import logging
import sys
from typing import Optional
from pathlib import Path
from ..core.utils import setup_logger as core_setup_logger


def setup_logger(
    name: str = "sdk",
    level: str = "INFO",
    format: str = "standard",
    output_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """Setup and configure a logger with custom settings"""
    return core_setup_logger(name, level, format, output_file)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)


def configure_logging(
    level: str = "INFO",
    format: str = "standard",
    log_file: Optional[str] = None
) -> None:
    """Configure root logger for the SDK"""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
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
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


class LoggerMixin:
    """Mixin class to add logging capability to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return logging.getLogger(self.__class__.__name__)
