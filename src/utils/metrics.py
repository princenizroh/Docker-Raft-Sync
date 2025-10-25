"""
Metrics Collection Module
Provides performance monitoring and metrics collection capabilities
"""

import time
import psutil
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from threading import Lock
import logging

logger = logging.getLogger(__name__)


@dataclass
class MetricValue:
    """Single metric value with timestamp"""
    value: float
    timestamp: float = field(default_factory=time.time)


class MetricsCollector:
    """
    Collects and manages system metrics
    """
    
    def __init__(self):
        self._metrics: Dict[str, List[MetricValue]] = defaultdict(list)
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = defaultdict(float)
        self._lock = Lock()
        self._start_time = time.time()
    
    def record_metric(self, name: str, value: float):
        """Record a metric value"""
        with self._lock:
            self._metrics[name].append(MetricValue(value=value))
            # Keep only last 1000 values
            if len(self._metrics[name]) > 1000:
                self._metrics[name] = self._metrics[name][-1000:]
    
    def increment_counter(self, name: str, value: int = 1):
        """Increment a counter"""
        with self._lock:
            self._counters[name] += value
    
    def set_gauge(self, name: str, value: float):
        """Set a gauge value"""
        with self._lock:
            self._gauges[name] = value
    
    def get_counter(self, name: str) -> int:
        """Get counter value"""
        with self._lock:
            return self._counters.get(name, 0)
    
    def get_gauge(self, name: str) -> float:
        """Get gauge value"""
        with self._lock:
            return self._gauges.get(name, 0.0)
    
    def get_metric_stats(self, name: str) -> Optional[Dict]:
        """Get statistics for a metric"""
        with self._lock:
            if name not in self._metrics or not self._metrics[name]:
                return None
            
            values = [m.value for m in self._metrics[name]]
            return {
                'count': len(values),
                'sum': sum(values),
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values),
                'latest': values[-1]
            }
    
    def get_all_metrics(self) -> Dict:
        """Get all metrics"""
        with self._lock:
            return {
                'counters': dict(self._counters),
                'gauges': dict(self._gauges),
                'metrics': {
                    name: self.get_metric_stats(name) 
                    for name in self._metrics.keys()
                },
                'system': self.get_system_metrics(),
                'uptime': time.time() - self._start_time
            }
    
    def get_system_metrics(self) -> Dict:
        """Get system-level metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage_percent': psutil.disk_usage('/').percent,
                'network_connections': len(psutil.net_connections()),
            }
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return {}
    
    def reset(self):
        """Reset all metrics"""
        with self._lock:
            self._metrics.clear()
            self._counters.clear()
            self._gauges.clear()
            self._start_time = time.time()


class PerformanceTimer:
    """Context manager for timing operations"""
    
    def __init__(self, metrics_collector: MetricsCollector, metric_name: str):
        self.metrics = metrics_collector
        self.metric_name = metric_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (time.time() - self.start_time) * 1000  # Convert to ms
        self.metrics.record_metric(self.metric_name, duration)


# Global metrics instance
_global_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Get global metrics collector"""
    return _global_metrics


def record_latency(operation: str):
    """Decorator to record operation latency"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = (time.time() - start) * 1000
                _global_metrics.record_metric(f"{operation}_latency_ms", duration)
        
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = (time.time() - start) * 1000
                _global_metrics.record_metric(f"{operation}_latency_ms", duration)
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator
