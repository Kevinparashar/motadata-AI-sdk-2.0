# Configuration Module

## WHY

The config module centralizes configuration management and logging setup for the entire SDK. It ensures consistent configuration handling, environment-based settings, and proper logging across all SDK components.

## WHAT

This module contains:

- **settings.py**: Configuration settings management including URLs, credentials, API endpoints, feature flags, and environment-specific configurations. Supports loading from files, environment variables, and command-line arguments
- **logging.py**: Custom logging configuration with support for multiple log levels, output formats, log rotation, and integration with standard logging frameworks
- **observability.py**: Comprehensive observability module providing metrics collection, distributed tracing, performance monitoring, health checks, and integration with monitoring tools (Prometheus, Datadog, Jaeger, etc.)

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

# Set up observability
from src.config.observability import Observability, get_observability

# Initialize observability
obs = Observability(
    service_name="my-service",
    enable_metrics=True,
    enable_tracing=True,
    enable_performance_monitoring=True,
    enable_health_checks=True
)

# Use metrics
counter = obs.metrics.get_or_create_counter("requests_total", description="Total requests")
counter.inc()

# Use tracing
with obs.tracer.span("api_request", tags={"method": "GET", "endpoint": "/users"}):
    # Your code here
    pass

# Monitor performance
with obs.performance_monitor.measure("database_query"):
    # Your database operation
    pass

# Health checks
from src.config.observability import HealthCheck
health_check = HealthCheck("database", lambda: db.is_connected())
obs.health_checker.register(health_check)
```

Configuration can be loaded from YAML files, JSON files, environment variables, or passed programmatically. The logging system integrates seamlessly with Python's standard logging module. The observability module provides comprehensive monitoring capabilities for production deployments.

## Input Validation and Error Handling

**All public methods in the config module include comprehensive input validation:**

- **Settings.from_file()**: Validates `file_path` (string, non-empty), checks file exists, validates JSON format (must be object), and handles JSON decode errors
- **Settings.save_to_file()**: Validates `file_path` (string, non-empty) and file format (must be .json)

**Custom Exceptions Used:**

- `ValidationError`: Invalid input parameters (replaces `ValueError`, `TypeError`)
- `ConfigurationError`: Configuration and file loading errors (replaces `FileNotFoundError`, `ValueError`, `json.JSONDecodeError`)

All methods raise appropriate custom exceptions with detailed error messages and context information for debugging.

## Observability Features

The observability module provides comprehensive monitoring capabilities:

### 1. Metrics Collection

- **Counters**: Track total counts (e.g., requests_total, errors_total)
- **Gauges**: Track current values (e.g., active_connections, queue_size)
- **Histograms**: Track value distributions (e.g., request_duration, response_size)
- **Labels**: Support for multi-dimensional metrics with labels

### 2. Distributed Tracing

- **Trace Spans**: Create spans for operations across services
- **Parent-Child Relationships**: Track span hierarchies
- **Tags and Logs**: Add contextual information to spans
- **Trace IDs**: Unique identifiers for request traces

### 3. Performance Monitoring

- **Latency Tracking**: Measure operation durations with percentiles (p50, p95, p99)
- **Throughput Monitoring**: Track operation rates per second
- **Operation Timing**: Context managers for easy measurement

### 4. Health Checks

- **Component Health**: Check health of individual components (database, API, etc.)
- **Timeout Support**: Configurable timeouts for health checks
- **Status Reporting**: Get health status of all registered checks

### 5. Integration Ready

- **Prometheus**: Metrics can be exported in Prometheus format
- **Datadog**: Integration hooks for Datadog APM
- **Jaeger**: Trace format compatible with Jaeger
- **Custom Adapters**: Extensible architecture for other monitoring tools

### Usage Examples

#### Metrics Example

```python
from src.config.observability import get_observability

obs = get_observability()

# Counter metric
requests_counter = obs.metrics.get_or_create_counter(
    "http_requests_total",
    description="Total HTTP requests",
    labels={"method": "GET", "status": "200"}
)
requests_counter.inc()

# Gauge metric
active_connections = obs.metrics.get_or_create_gauge(
    "active_connections",
    description="Number of active connections"
)
active_connections.set(42)

# Histogram metric
request_duration = obs.metrics.get_or_create_histogram(
    "http_request_duration_seconds",
    description="HTTP request duration",
    labels={"method": "GET"}
)
request_duration.observe(0.123)  # Record 123ms
```

#### Tracing Example

```python
# Start a trace span
with obs.tracer.span("api_request", tags={"method": "GET", "endpoint": "/users"}):
    # Nested span
    with obs.tracer.span("database_query", tags={"query": "SELECT * FROM users"}):
        # Your code here
        results = db.execute_query("SELECT * FROM users")

    # Add tags and logs to active span
    span = obs.tracer.get_active_span()
    if span:
        span.add_tag("result_count", len(results))
        span.add_log("Query completed successfully", level="info")
```

#### Performance Monitoring Example

```python
# Measure operation latency
with obs.performance_monitor.measure("database_query"):
    results = db.execute_query("SELECT * FROM users")

# Get latency statistics
stats = obs.performance_monitor.get_latency_stats("database_query")
print(f"Mean latency: {stats['mean']}s")
print(f"P95 latency: {stats['p95']}s")

# Record throughput
obs.performance_monitor.record_throughput("api_requests", count=100)
throughput = obs.performance_monitor.get_throughput_stats("api_requests")
print(f"Requests per second: {throughput['rate_per_second']}")
```

#### Health Checks Example

```python
from src.config.observability import HealthCheck

# Create health check
def check_database():
    return db.is_connected()

db_health = HealthCheck("database", check_database, timeout=5.0)
obs.health_checker.register(db_health)

# Run all health checks
status = obs.health_checker.run_all()
print(f"Overall status: {status['status']}")
for check_name, check_result in status['checks'].items():
    print(f"{check_name}: {check_result['status']}")
```

#### Full Status Example

```python
# Get complete observability status
status = obs.get_full_status()
print(f"Service: {status['service_name']}")
print(f"Metrics: {status['metrics']}")
print(f"Traces: {status['tracing']}")
print(f"Performance: {status['performance']}")
print(f"Health: {status['health']}")
```

## Libraries

This module uses the following Python standard libraries and packages:

- **typing**: Type hints (Dict, Any, Optional, List, Callable)
- **os**: Operating system interface for environment variables
- **json**: JSON encoding and decoding for configuration file parsing
- **pathlib**: Object-oriented filesystem paths for configuration file management
- **logging**: Logging framework for application logging
- **sys**: System-specific parameters and functions for logging output
- **time**: Time-related functions for performance monitoring and tracing
- **threading**: Thread synchronization for thread-safe operations
- **uuid**: UUID generation for trace and span IDs
- **datetime**: Date and time handling for timestamps
- **collections**: defaultdict and deque for efficient data structures
- **contextlib**: Context managers for resource management
- **src.core.utils**: get_env_var and validate_config from core module
- **src.core.validators**: Input validation utilities
- **src.core.exceptions**: Custom exception classes
- **src.core.event_handler**: EventEmitter for observability events

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

### observability.py

- **Observability** (class): Main observability class integrating all observability features
  - `__init__()`: Initialize observability with service name and feature flags
  - `metrics` (property): MetricsRegistry instance for metrics collection
  - `tracer` (property): Tracer instance for distributed tracing
  - `performance_monitor` (property): PerformanceMonitor instance for performance tracking
  - `health_checker` (property): HealthChecker instance for health checks
  - `get_metrics_summary()`: Get summary of all metrics
  - `get_traces_summary()`: Get summary of all traces
  - `get_performance_summary()`: Get summary of performance metrics
  - `get_health_status()`: Get health status
  - `get_full_status()`: Get complete observability status

- **MetricsRegistry** (class): Registry for managing metrics
  - `register_counter()`: Register a counter metric
  - `register_gauge()`: Register a gauge metric
  - `register_histogram()`: Register a histogram metric
  - `get_metric()`: Get a metric by name and labels
  - `get_or_create_counter()`: Get existing counter or create new one
  - `get_or_create_gauge()`: Get existing gauge or create new one
  - `get_or_create_histogram()`: Get existing histogram or create new one
  - `get_all_metrics()`: Get all registered metrics
  - `clear()`: Clear all metrics

- **Counter** (class): Counter metric - increments only
  - `inc()`: Increment counter by value
  - `get()`: Get current counter value
  - `reset()`: Reset counter to zero

- **Gauge** (class): Gauge metric - can increase or decrease
  - `inc()`: Increment gauge by value
  - `dec()`: Decrement gauge by value
  - `set()`: Set gauge to specific value
  - `get()`: Get current gauge value

- **Histogram** (class): Histogram metric - tracks distribution of values
  - `observe()`: Record an observation
  - `get()`: Get histogram statistics (count, sum, mean, min, max, percentiles, buckets)

- **Tracer** (class): Distributed tracing system
  - `start_span()`: Start a new trace span
  - `get_active_span()`: Get the active span for current thread
  - `finish_span()`: Finish a span
  - `span()`: Context manager for creating spans
  - `get_spans_by_trace_id()`: Get all spans for a trace
  - `get_all_spans()`: Get all spans

- **TraceSpan** (class): Represents a span in a distributed trace
  - `add_tag()`: Add a tag to the span
  - `add_log()`: Add a log entry to the span
  - `finish()`: Finish the span
  - `to_dict()`: Convert span to dictionary

- **PerformanceMonitor** (class): Performance monitoring for latency, throughput, and resource usage
  - `start_operation()`: Start timing an operation
  - `end_operation()`: End timing an operation and return duration
  - `measure()`: Context manager for measuring operation duration
  - `record_throughput()`: Record throughput for an operation
  - `get_latency_stats()`: Get latency statistics for an operation (mean, min, max, p50, p95, p99)
  - `get_throughput_stats()`: Get throughput statistics for an operation

- **HealthCheck** (class): Health check for system components
  - `__init__()`: Initialize health check with name, check function, and timeout
  - `run()`: Run the health check
  - `get_status()`: Get last health check status

- **HealthChecker** (class): Registry for health checks
  - `register()`: Register a health check
  - `unregister()`: Unregister a health check
  - `run_all()`: Run all health checks
  - `get_status()`: Get status of all health checks

- **get_observability()**: Get or create global observability instance
- **set_observability()**: Set global observability instance
