"""
Comprehensive observability module for metrics, tracing, monitoring, and health checks
"""
import time
import threading
import uuid
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from collections import defaultdict, deque
from contextlib import contextmanager
import logging

from ..core.validators import validate_string, validate_dict, validate_list, validate_int
from ..core.exceptions import ValidationError, ConfigurationError
from ..core.event_handler import EventEmitter


class MetricType:
    """Metric type enumeration"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class Metric:
    """Base class for metrics"""
    
    def __init__(self, name: str, metric_type: str, description: str = "", labels: Optional[Dict[str, str]] = None):
        self.name = validate_string(name, "name", min_length=1, max_length=200)
        self.metric_type = validate_string(metric_type, "metric_type", min_length=1)
        if metric_type not in [MetricType.COUNTER, MetricType.GAUGE, MetricType.HISTOGRAM, MetricType.SUMMARY]:
            raise ValidationError(
                f"Invalid metric type: {metric_type}",
                field="metric_type",
                value=metric_type
            )
        self.description = description
        self.labels = labels or {}
        self._lock = threading.Lock()
        self._created_at = datetime.now()
    
    def get_labels_key(self) -> str:
        """Get a string representation of labels for indexing"""
        if not self.labels:
            return ""
        return ",".join(f"{k}={v}" for k, v in sorted(self.labels.items()))


class Counter(Metric):
    """Counter metric - increments only"""
    
    def __init__(self, name: str, description: str = "", labels: Optional[Dict[str, str]] = None):
        super().__init__(name, MetricType.COUNTER, description, labels)
        self._value = 0.0
    
    def inc(self, value: float = 1.0) -> None:
        """Increment counter by value"""
        if value < 0:
            raise ValidationError("Counter cannot be decremented", field="value", value=value)
        with self._lock:
            self._value += value
    
    def get(self) -> float:
        """Get current counter value"""
        with self._lock:
            return self._value
    
    def reset(self) -> None:
        """Reset counter to zero"""
        with self._lock:
            self._value = 0.0


class Gauge(Metric):
    """Gauge metric - can increase or decrease"""
    
    def __init__(self, name: str, description: str = "", labels: Optional[Dict[str, str]] = None):
        super().__init__(name, MetricType.GAUGE, description, labels)
        self._value = 0.0
    
    def inc(self, value: float = 1.0) -> None:
        """Increment gauge by value"""
        with self._lock:
            self._value += value
    
    def dec(self, value: float = 1.0) -> None:
        """Decrement gauge by value"""
        with self._lock:
            self._value -= value
    
    def set(self, value: float) -> None:
        """Set gauge to specific value"""
        with self._lock:
            self._value = value
    
    def get(self) -> float:
        """Get current gauge value"""
        with self._lock:
            return self._value


class Histogram(Metric):
    """Histogram metric - tracks distribution of values"""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        labels: Optional[Dict[str, str]] = None,
        buckets: Optional[List[float]] = None
    ):
        super().__init__(name, MetricType.HISTOGRAM, description, labels)
        # Default buckets for common use cases
        self.buckets = buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        self._observations = deque(maxlen=10000)  # Keep last 10k observations
        self._sum = 0.0
        self._count = 0
    
    def observe(self, value: float) -> None:
        """Record an observation"""
        if value < 0:
            raise ValidationError("Histogram value cannot be negative", field="value", value=value)
        with self._lock:
            self._observations.append(value)
            self._sum += value
            self._count += 1
    
    def get(self) -> Dict[str, Any]:
        """Get histogram statistics"""
        with self._lock:
            observations = list(self._observations)
            if not observations:
                return {
                    "count": 0,
                    "sum": 0.0,
                    "mean": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "buckets": {str(bucket): 0 for bucket in self.buckets}
                }
            
            sorted_obs = sorted(observations)
            buckets_count = {str(bucket): 0 for bucket in self.buckets}
            
            for obs in observations:
                for bucket in self.buckets:
                    if obs <= bucket:
                        buckets_count[str(bucket)] += 1
                        break
            
            return {
                "count": self._count,
                "sum": self._sum,
                "mean": self._sum / self._count if self._count > 0 else 0.0,
                "min": sorted_obs[0],
                "max": sorted_obs[-1],
                "p50": sorted_obs[len(sorted_obs) // 2] if sorted_obs else 0.0,
                "p95": sorted_obs[int(len(sorted_obs) * 0.95)] if sorted_obs else 0.0,
                "p99": sorted_obs[int(len(sorted_obs) * 0.99)] if sorted_obs else 0.0,
                "buckets": buckets_count
            }


class MetricsRegistry:
    """Registry for managing metrics"""
    
    def __init__(self):
        self._metrics: Dict[str, Dict[str, Metric]] = defaultdict(dict)
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
    
    def register_counter(
        self,
        name: str,
        description: str = "",
        labels: Optional[Dict[str, str]] = None
    ) -> Counter:
        """Register a counter metric"""
        counter = Counter(name, description, labels)
        labels_key = counter.get_labels_key()
        with self._lock:
            self._metrics[name][labels_key] = counter
        return counter
    
    def register_gauge(
        self,
        name: str,
        description: str = "",
        labels: Optional[Dict[str, str]] = None
    ) -> Gauge:
        """Register a gauge metric"""
        gauge = Gauge(name, description, labels)
        labels_key = gauge.get_labels_key()
        with self._lock:
            self._metrics[name][labels_key] = gauge
        return gauge
    
    def register_histogram(
        self,
        name: str,
        description: str = "",
        labels: Optional[Dict[str, str]] = None,
        buckets: Optional[List[float]] = None
    ) -> Histogram:
        """Register a histogram metric"""
        histogram = Histogram(name, description, labels, buckets)
        labels_key = histogram.get_labels_key()
        with self._lock:
            self._metrics[name][labels_key] = histogram
        return histogram
    
    def get_metric(self, name: str, labels: Optional[Dict[str, str]] = None) -> Optional[Metric]:
        """Get a metric by name and labels"""
        name = validate_string(name, "name", min_length=1)
        labels_key = Counter("", MetricType.COUNTER, "", labels or {}).get_labels_key()
        with self._lock:
            return self._metrics.get(name, {}).get(labels_key)
    
    def get_or_create_counter(
        self,
        name: str,
        description: str = "",
        labels: Optional[Dict[str, str]] = None
    ) -> Counter:
        """Get existing counter or create new one"""
        metric = self.get_metric(name, labels)
        if metric and isinstance(metric, Counter):
            return metric
        return self.register_counter(name, description, labels)
    
    def get_or_create_gauge(
        self,
        name: str,
        description: str = "",
        labels: Optional[Dict[str, str]] = None
    ) -> Gauge:
        """Get existing gauge or create new one"""
        metric = self.get_metric(name, labels)
        if metric and isinstance(metric, Gauge):
            return metric
        return self.register_gauge(name, description, labels)
    
    def get_or_create_histogram(
        self,
        name: str,
        description: str = "",
        labels: Optional[Dict[str, str]] = None,
        buckets: Optional[List[float]] = None
    ) -> Histogram:
        """Get existing histogram or create new one"""
        metric = self.get_metric(name, labels)
        if metric and isinstance(metric, Histogram):
            return metric
        return self.register_histogram(name, description, labels, buckets)
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Metric]]:
        """Get all registered metrics"""
        with self._lock:
            return dict(self._metrics)
    
    def clear(self) -> None:
        """Clear all metrics"""
        with self._lock:
            self._metrics.clear()


class TraceSpan:
    """Represents a span in a distributed trace"""
    
    def __init__(
        self,
        trace_id: str,
        span_id: str,
        parent_span_id: Optional[str] = None,
        operation_name: str = "",
        tags: Optional[Dict[str, Any]] = None
    ):
        self.trace_id = validate_string(trace_id, "trace_id", min_length=1)
        self.span_id = validate_string(span_id, "span_id", min_length=1)
        self.parent_span_id = parent_span_id
        self.operation_name = validate_string(operation_name, "operation_name", min_length=1, allow_empty=True)
        self.tags = tags or {}
        self.logs: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.duration: Optional[float] = None
        self._lock = threading.Lock()
    
    def add_tag(self, key: str, value: Any) -> None:
        """Add a tag to the span"""
        key = validate_string(key, "key", min_length=1)
        with self._lock:
            self.tags[key] = value
    
    def add_log(self, message: str, level: str = "info", fields: Optional[Dict[str, Any]] = None) -> None:
        """Add a log entry to the span"""
        message = validate_string(message, "message", min_length=1, allow_empty=True)
        with self._lock:
            self.logs.append({
                "timestamp": time.time(),
                "message": message,
                "level": level,
                "fields": fields or {}
            })
    
    def finish(self) -> None:
        """Finish the span"""
        with self._lock:
            self.end_time = time.time()
            self.duration = self.end_time - self.start_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary"""
        with self._lock:
            return {
                "trace_id": self.trace_id,
                "span_id": self.span_id,
                "parent_span_id": self.parent_span_id,
                "operation_name": self.operation_name,
                "tags": self.tags,
                "logs": self.logs,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.duration
            }


class Tracer:
    """Distributed tracing system"""
    
    def __init__(self, service_name: str):
        self.service_name = validate_string(service_name, "service_name", min_length=1)
        self._spans: Dict[str, TraceSpan] = {}
        self._active_spans: Dict[str, str] = {}  # thread_id -> span_id
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
    
    def start_span(
        self,
        operation_name: str,
        parent_span_id: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> TraceSpan:
        """Start a new span"""
        operation_name = validate_string(operation_name, "operation_name", min_length=1)
        
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        
        span_id = str(uuid.uuid4())
        span = TraceSpan(trace_id, span_id, parent_span_id, operation_name, tags)
        
        with self._lock:
            self._spans[span_id] = span
            thread_id = threading.current_thread().ident
            if thread_id:
                self._active_spans[str(thread_id)] = span_id
        
        return span
    
    def get_active_span(self) -> Optional[TraceSpan]:
        """Get the active span for current thread"""
        thread_id = str(threading.current_thread().ident)
        with self._lock:
            span_id = self._active_spans.get(thread_id)
            if span_id:
                return self._spans.get(span_id)
        return None
    
    def finish_span(self, span: TraceSpan) -> None:
        """Finish a span"""
        span.finish()
        thread_id = str(threading.current_thread().ident)
        with self._lock:
            if thread_id in self._active_spans:
                del self._active_spans[thread_id]
    
    @contextmanager
    def span(self, operation_name: str, tags: Optional[Dict[str, Any]] = None):
        """Context manager for creating spans"""
        active_span = self.get_active_span()
        parent_span_id = active_span.span_id if active_span else None
        trace_id = active_span.trace_id if active_span else None
        
        span = self.start_span(operation_name, parent_span_id, tags, trace_id)
        try:
            yield span
        finally:
            self.finish_span(span)
    
    def get_spans_by_trace_id(self, trace_id: str) -> List[TraceSpan]:
        """Get all spans for a trace"""
        trace_id = validate_string(trace_id, "trace_id", min_length=1)
        with self._lock:
            return [span for span in self._spans.values() if span.trace_id == trace_id]
    
    def get_all_spans(self) -> List[TraceSpan]:
        """Get all spans"""
        with self._lock:
            return list(self._spans.values())


class PerformanceMonitor:
    """Performance monitoring for latency, throughput, and resource usage"""
    
    def __init__(self):
        self._latencies: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self._throughput: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self._start_times: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
    
    def start_operation(self, operation_name: str) -> None:
        """Start timing an operation"""
        operation_name = validate_string(operation_name, "operation_name", min_length=1)
        with self._lock:
            self._start_times[operation_name] = time.time()
    
    def end_operation(self, operation_name: str) -> float:
        """End timing an operation and return duration"""
        operation_name = validate_string(operation_name, "operation_name", min_length=1)
        with self._lock:
            if operation_name not in self._start_times:
                self._logger.warning(f"Operation {operation_name} was not started")
                return 0.0
            
            duration = time.time() - self._start_times[operation_name]
            del self._start_times[operation_name]
            self._latencies[operation_name].append(duration)
            return duration
    
    @contextmanager
    def measure(self, operation_name: str):
        """Context manager for measuring operation duration"""
        self.start_operation(operation_name)
        try:
            yield
        finally:
            self.end_operation(operation_name)
    
    def record_throughput(self, operation_name: str, count: int = 1) -> None:
        """Record throughput for an operation"""
        operation_name = validate_string(operation_name, "operation_name", min_length=1)
        validate_int(count, "count", min_value=1)
        with self._lock:
            self._throughput[operation_name].append({
                "timestamp": time.time(),
                "count": count
            })
    
    def get_latency_stats(self, operation_name: str) -> Dict[str, float]:
        """Get latency statistics for an operation"""
        operation_name = validate_string(operation_name, "operation_name", min_length=1)
        with self._lock:
            latencies = list(self._latencies.get(operation_name, []))
            if not latencies:
                return {
                    "count": 0,
                    "mean": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "p50": 0.0,
                    "p95": 0.0,
                    "p99": 0.0
                }
            
            sorted_latencies = sorted(latencies)
            return {
                "count": len(latencies),
                "mean": sum(latencies) / len(latencies),
                "min": sorted_latencies[0],
                "max": sorted_latencies[-1],
                "p50": sorted_latencies[len(sorted_latencies) // 2],
                "p95": sorted_latencies[int(len(sorted_latencies) * 0.95)],
                "p99": sorted_latencies[int(len(sorted_latencies) * 0.99)]
            }
    
    def get_throughput_stats(self, operation_name: str, window_seconds: int = 60) -> Dict[str, Any]:
        """Get throughput statistics for an operation"""
        operation_name = validate_string(operation_name, "operation_name", min_length=1)
        validate_int(window_seconds, "window_seconds", min_value=1)
        
        cutoff_time = time.time() - window_seconds
        with self._lock:
            throughput_data = [
                entry for entry in self._throughput.get(operation_name, [])
                if entry["timestamp"] >= cutoff_time
            ]
            
            if not throughput_data:
                return {
                    "count": 0,
                    "total": 0,
                    "rate_per_second": 0.0
                }
            
            total = sum(entry["count"] for entry in throughput_data)
            return {
                "count": len(throughput_data),
                "total": total,
                "rate_per_second": total / window_seconds if window_seconds > 0 else 0.0
            }


class HealthCheck:
    """Health check for system components"""
    
    def __init__(self, name: str, check_func: Callable[[], bool], timeout: float = 5.0):
        self.name = validate_string(name, "name", min_length=1, max_length=100)
        if not callable(check_func):
            raise ValidationError("check_func must be callable", field="check_func")
        self.check_func = check_func
        if timeout <= 0:
            raise ValidationError("timeout must be positive", field="timeout", value=timeout)
        self.timeout = timeout
        self._last_check: Optional[datetime] = None
        self._last_result: Optional[bool] = None
        self._last_error: Optional[str] = None
    
    def run(self) -> Dict[str, Any]:
        """Run the health check"""
        start_time = time.time()
        try:
            result = self.check_func()
            duration = time.time() - start_time
            self._last_check = datetime.now()
            self._last_result = result
            self._last_error = None
            
            return {
                "name": self.name,
                "status": "healthy" if result else "unhealthy",
                "duration": duration,
                "timestamp": self._last_check.isoformat()
            }
        except Exception as e:
            duration = time.time() - start_time
            self._last_check = datetime.now()
            self._last_result = False
            self._last_error = str(e)
            
            return {
                "name": self.name,
                "status": "unhealthy",
                "error": str(e),
                "duration": duration,
                "timestamp": self._last_check.isoformat()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get last health check status"""
        return {
            "name": self.name,
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "last_result": self._last_result,
            "last_error": self._last_error
        }


class HealthChecker:
    """Registry for health checks"""
    
    def __init__(self):
        self._checks: Dict[str, HealthCheck] = {}
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)
    
    def register(self, health_check: HealthCheck) -> None:
        """Register a health check"""
        if not isinstance(health_check, HealthCheck):
            raise ValidationError("health_check must be a HealthCheck instance", field="health_check")
        with self._lock:
            self._checks[health_check.name] = health_check
    
    def unregister(self, name: str) -> None:
        """Unregister a health check"""
        name = validate_string(name, "name", min_length=1)
        with self._lock:
            if name in self._checks:
                del self._checks[name]
    
    def run_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        with self._lock:
            checks = dict(self._checks)
        
        results = {}
        overall_healthy = True
        
        for name, check in checks.items():
            result = check.run()
            results[name] = result
            if result["status"] != "healthy":
                overall_healthy = False
        
        return {
            "status": "healthy" if overall_healthy else "unhealthy",
            "checks": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all health checks"""
        with self._lock:
            checks = dict(self._checks)
        
        return {
            "checks": {name: check.get_status() for name, check in checks.items()},
            "timestamp": datetime.now().isoformat()
        }


class Observability:
    """Main observability class that integrates all observability features"""
    
    def __init__(
        self,
        service_name: str = "sdk",
        enable_metrics: bool = True,
        enable_tracing: bool = True,
        enable_performance_monitoring: bool = True,
        enable_health_checks: bool = True
    ):
        self.service_name = validate_string(service_name, "service_name", min_length=1)
        self._logger = logging.getLogger(__name__)
        
        # Initialize components
        self.metrics = MetricsRegistry() if enable_metrics else None
        self.tracer = Tracer(service_name) if enable_tracing else None
        self.performance_monitor = PerformanceMonitor() if enable_performance_monitoring else None
        self.health_checker = HealthChecker() if enable_health_checks else None
        
        # Event emitter for observability events
        self.event_emitter = EventEmitter()
        
        # Integration adapters
        self._prometheus_adapter = None
        self._datadog_adapter = None
        self._jaeger_adapter = None
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        if not self.metrics:
            return {"error": "Metrics not enabled"}
        
        all_metrics = self.metrics.get_all_metrics()
        summary = {}
        
        for metric_name, metric_instances in all_metrics.items():
            summary[metric_name] = {}
            for labels_key, metric in metric_instances.items():
                if isinstance(metric, Counter):
                    summary[metric_name][labels_key or "default"] = metric.get()
                elif isinstance(metric, Gauge):
                    summary[metric_name][labels_key or "default"] = metric.get()
                elif isinstance(metric, Histogram):
                    summary[metric_name][labels_key or "default"] = metric.get()
        
        return summary
    
    def get_traces_summary(self) -> Dict[str, Any]:
        """Get summary of all traces"""
        if not self.tracer:
            return {"error": "Tracing not enabled"}
        
        all_spans = self.tracer.get_all_spans()
        trace_ids = set(span.trace_id for span in all_spans)
        
        return {
            "total_spans": len(all_spans),
            "total_traces": len(trace_ids),
            "finished_spans": len([s for s in all_spans if s.end_time is not None]),
            "active_spans": len([s for s in all_spans if s.end_time is None])
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of performance metrics"""
        if not self.performance_monitor:
            return {"error": "Performance monitoring not enabled"}
        
        # Get latency stats for all operations
        latency_stats = {}
        if self.performance_monitor._latencies:
            for operation_name in self.performance_monitor._latencies.keys():
                latency_stats[operation_name] = self.performance_monitor.get_latency_stats(operation_name)
        
        # Get throughput stats for all operations
        throughput_stats = {}
        if self.performance_monitor._throughput:
            for operation_name in self.performance_monitor._throughput.keys():
                throughput_stats[operation_name] = self.performance_monitor.get_throughput_stats(operation_name)
        
        return {
            "latency": latency_stats,
            "throughput": throughput_stats
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status"""
        if not self.health_checker:
            return {"error": "Health checks not enabled"}
        
        return self.health_checker.get_status()
    
    def get_full_status(self) -> Dict[str, Any]:
        """Get complete observability status"""
        return {
            "service_name": self.service_name,
            "timestamp": datetime.now().isoformat(),
            "metrics": self.get_metrics_summary(),
            "tracing": self.get_traces_summary(),
            "performance": self.get_performance_summary(),
            "health": self.get_health_status()
        }


# Global observability instance
_global_observability: Optional[Observability] = None


def get_observability() -> Observability:
    """Get or create global observability instance"""
    global _global_observability
    if _global_observability is None:
        _global_observability = Observability()
    return _global_observability


def set_observability(observability: Observability) -> None:
    """Set global observability instance"""
    global _global_observability
    if not isinstance(observability, Observability):
        raise ValidationError("observability must be an Observability instance", field="observability")
    _global_observability = observability

