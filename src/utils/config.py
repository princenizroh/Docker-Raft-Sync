"""
Configuration Management Module
Handles loading and managing system configuration from environment variables
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class NodeConfig:
    """Configuration for a single node"""
    node_id: str = field(default_factory=lambda: os.getenv('NODE_ID', 'node-1'))
    host: str = field(default_factory=lambda: os.getenv('NODE_HOST', '0.0.0.0'))
    port: int = field(default_factory=lambda: int(os.getenv('NODE_PORT', '5000')))
    cluster_port: int = field(default_factory=lambda: int(os.getenv('NODE_CLUSTER_PORT', '5001')))


@dataclass
class ClusterConfig:
    """Configuration for cluster nodes"""
    nodes: List[str] = field(default_factory=lambda: [
        node.strip() for node in os.getenv('CLUSTER_NODES', 'node-1:localhost:5000').split(',')
    ])
    min_cluster_size: int = field(default_factory=lambda: int(os.getenv('MIN_CLUSTER_SIZE', '3')))


@dataclass
class RedisConfig:
    """Redis configuration"""
    host: str = field(default_factory=lambda: os.getenv('REDIS_HOST', 'localhost'))
    port: int = field(default_factory=lambda: int(os.getenv('REDIS_PORT', '6379')))
    db: int = field(default_factory=lambda: int(os.getenv('REDIS_DB', '0')))
    password: Optional[str] = field(default_factory=lambda: os.getenv('REDIS_PASSWORD', None))


@dataclass
class RaftConfig:
    """Raft consensus algorithm configuration"""
    election_timeout_min: int = field(default_factory=lambda: int(os.getenv('RAFT_ELECTION_TIMEOUT_MIN', '150')))
    election_timeout_max: int = field(default_factory=lambda: int(os.getenv('RAFT_ELECTION_TIMEOUT_MAX', '300')))
    heartbeat_interval: int = field(default_factory=lambda: int(os.getenv('RAFT_HEARTBEAT_INTERVAL', '50')))


@dataclass
class QueueConfig:
    """Distributed queue configuration"""
    partition_count: int = field(default_factory=lambda: int(os.getenv('QUEUE_PARTITION_COUNT', '16')))
    replication_factor: int = field(default_factory=lambda: int(os.getenv('QUEUE_REPLICATION_FACTOR', '2')))
    persistence_path: str = field(default_factory=lambda: os.getenv('QUEUE_PERSISTENCE_PATH', './data/queue'))


@dataclass
class CacheConfig:
    """Distributed cache configuration"""
    size_mb: int = field(default_factory=lambda: int(os.getenv('CACHE_SIZE_MB', '256')))
    protocol: str = field(default_factory=lambda: os.getenv('CACHE_PROTOCOL', 'MESI'))
    replacement_policy: str = field(default_factory=lambda: os.getenv('CACHE_REPLACEMENT_POLICY', 'LRU'))
    invalidation_timeout: int = field(default_factory=lambda: int(os.getenv('CACHE_INVALIDATION_TIMEOUT', '5000')))


@dataclass
class LockConfig:
    """Distributed lock configuration"""
    lock_timeout: int = field(default_factory=lambda: int(os.getenv('LOCK_TIMEOUT', '30000')))
    deadlock_detection_interval: int = field(default_factory=lambda: int(os.getenv('DEADLOCK_DETECTION_INTERVAL', '10000')))


@dataclass
class MonitoringConfig:
    """Monitoring and metrics configuration"""
    prometheus_port: int = field(default_factory=lambda: int(os.getenv('PROMETHEUS_PORT', '9090')))
    metrics_enabled: bool = field(default_factory=lambda: os.getenv('METRICS_ENABLED', 'true').lower() == 'true')
    log_level: str = field(default_factory=lambda: os.getenv('LOG_LEVEL', 'INFO'))


@dataclass
class PerformanceConfig:
    """Performance-related configuration"""
    max_concurrent_requests: int = field(default_factory=lambda: int(os.getenv('MAX_CONCURRENT_REQUESTS', '1000')))
    message_batch_size: int = field(default_factory=lambda: int(os.getenv('MESSAGE_BATCH_SIZE', '100')))
    network_buffer_size: int = field(default_factory=lambda: int(os.getenv('NETWORK_BUFFER_SIZE', '65536')))


@dataclass
class APIConfig:
    """API Server configuration"""
    enable_http_api: bool = field(default_factory=lambda: os.getenv('ENABLE_HTTP_API', 'false').lower() == 'true')
    api_host: str = field(default_factory=lambda: os.getenv('API_HOST', '0.0.0.0'))
    api_port: int = field(default_factory=lambda: int(os.getenv('API_PORT', '6000')))

@dataclass
class DevelopmentConfig:
    """Development and debugging configuration"""
    debug_mode: bool = field(default_factory=lambda: os.getenv('DEBUG_MODE', 'false').lower() == 'true')
    enable_tracing: bool = field(default_factory=lambda: os.getenv('ENABLE_TRACING', 'false').lower() == 'true')


@dataclass
class SystemConfig:
    """Complete system configuration"""
    node: NodeConfig = field(default_factory=NodeConfig)
    cluster: ClusterConfig = field(default_factory=ClusterConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    raft: RaftConfig = field(default_factory=RaftConfig)
    queue: QueueConfig = field(default_factory=QueueConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    lock: LockConfig = field(default_factory=LockConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    development: DevelopmentConfig = field(default_factory=DevelopmentConfig)
    api: APIConfig = field(default_factory=APIConfig)


# Global configuration instance
config = SystemConfig()


def reload_config():
    """Reload configuration from environment"""
    global config
    load_dotenv(override=True)
    config = SystemConfig()
    return config


def get_config() -> SystemConfig:
    """Get current system configuration"""
    return config
