# Core Components

## WHY
The core module provides fundamental building blocks and utilities that are used throughout the SDK. These components establish the foundation for data structures, concurrency handling, event management, and common utilities that other modules depend on.

## WHAT
This module contains:

- **data_structures.py**: Core data models and structures used across the SDK (e.g., request/response models, configuration objects)
- **concurrency.py**: Concurrency utilities for handling asyncio operations, threading, and parallel processing
- **event_handler.py**: Event handling logic for managing SDK events, callbacks, and asynchronous notifications
- **utils.py**: Helper functions for logging, configuration parsing, validation, and other common operations

## HOW
Import and use core components in your code:

```python
from src.core.data_structures import RequestModel, ResponseModel
from src.core.concurrency import AsyncExecutor, ThreadPool
from src.core.event_handler import EventHandler, EventEmitter
from src.core.utils import setup_logger, validate_config
```

These components are typically used internally by other SDK modules, but can also be used directly in your application code when needed.

