"""
Distributed Synchronization System
Main package initialization
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .nodes import base_node, lock_manager, queue_node, cache_node
from .consensus import raft
from .communication import message_passing, failure_detector
from .utils import config, metrics

__all__ = [
    'base_node',
    'lock_manager',
    'queue_node',
    'cache_node',
    'raft',
    'message_passing',
    'failure_detector',
    'config',
    'metrics',
]
