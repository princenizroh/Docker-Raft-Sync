"""
Failure Detector Module
Implements failure detection for distributed nodes
"""

import asyncio
import time
import logging
import statistics
from typing import Dict, Set, Callable, Optional, List, Deque
from dataclasses import dataclass
from enum import Enum
from collections import deque

logger = logging.getLogger(__name__)


class NodeState(Enum):
    """Node states"""
    ALIVE = "alive"
    SUSPECTED = "suspected"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class NodeStatus:
    """Status information for a node"""
    node_id: str
    state: NodeState
    last_heartbeat: float
    missed_heartbeats: int = 0
    suspected_since: Optional[float] = None
    failed_since: Optional[float] = None
    last_interval: Optional[float] = None


class SlidingWindow:
    """Helper class for maintaining sliding window statistics"""
    def __init__(self, max_size: int = 100, min_samples: int = 10):
        self.max_size = max_size
        self.min_samples = min_samples
        self.values: Deque[float] = deque(maxlen=max_size)
        self._sum = 0
        self._sum_sq = 0
    
    def add(self, value: float):
        """Add a value to the window"""
        if len(self.values) >= self.max_size:
            old = self.values[0]
            self._sum -= old
            self._sum_sq -= old * old
        
        self.values.append(value)
        self._sum += value
        self._sum_sq += value * value
    
    def mean(self) -> Optional[float]:
        """Calculate mean of the window"""
        if len(self.values) < self.min_samples:
            return None
        return self._sum / len(self.values)
    
    def stddev(self) -> Optional[float]:
        """Calculate standard deviation of the window"""
        if len(self.values) < self.min_samples:
            return None
        n = len(self.values)
        variance = (self._sum_sq / n) - (self._sum / n) ** 2
        return max(0.001, (variance ** 0.5))  # Ensure minimum stddev to avoid division by zero


class FailureDetector:
    """
    Implements an adaptive failure detector using heartbeats
    Based on phi-accrual failure detector algorithm with improvements
    """
    
    def __init__(
        self,
        node_id: str,
        heartbeat_interval: float = 1.0,
        suspicion_threshold: int = 3,
        failure_threshold: int = 5,
        phi_threshold: float = 8.0,
        window_size: int = 100,
        min_samples: int = 10
    ):
        self.node_id = node_id
        self.heartbeat_interval = max(0.1, heartbeat_interval)  # Minimum 100ms
        self.suspicion_threshold = suspicion_threshold
        self.failure_threshold = failure_threshold
        self.phi_threshold = phi_threshold
        self.window_size = window_size
        self.min_samples = min_samples
        
        self.node_states: Dict[str, NodeStatus] = {}
        self.heartbeat_windows: Dict[str, SlidingWindow] = {}
        self.failure_callbacks: List[Callable] = []
        self.recovery_callbacks: List[Callable] = []
        
        self._running = False
        self._monitor_task: Optional[asyncio.Task] = None
        self._min_interval = heartbeat_interval * 0.1  # Minimum reasonable interval
    
    async def start(self):
        """Start failure detector"""
        self._running = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("Failure detector started")
    
    async def stop(self):
        """Stop failure detector"""
        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Failure detector stopped")
    
    def register_node(self, node_id: str):
        """Register a node for monitoring"""
        if node_id not in self.node_states:
            self.node_states[node_id] = NodeStatus(
                node_id=node_id,
                state=NodeState.UNKNOWN,
                last_heartbeat=time.time(),
                last_interval=None
            )
            self.heartbeat_windows[node_id] = SlidingWindow(
                max_size=self.window_size,
                min_samples=self.min_samples
            )
            logger.info(f"Registered node for monitoring: {node_id}")
    
    def unregister_node(self, node_id: str):
        """Unregister a node from monitoring"""
        if node_id in self.node_states:
            del self.node_states[node_id]
            del self.heartbeat_windows[node_id]
            logger.info(f"Unregistered node: {node_id}")
    
    def record_heartbeat(self, node_id: str):
        """Record a heartbeat from a node"""
        current_time = time.time()
        
        if node_id not in self.node_states:
            self.register_node(node_id)
            return
        
        status = self.node_states[node_id]
        window = self.heartbeat_windows[node_id]
        
        # Calculate and record interval
        if status.last_heartbeat is not None:
            interval = current_time - status.last_heartbeat
            # Filter out unreasonable intervals
            if interval >= self._min_interval:
                window.add(interval)
                status.last_interval = interval
        
        # Update status
        old_state = status.state
        status.last_heartbeat = current_time
        status.missed_heartbeats = 0
        status.state = NodeState.ALIVE
        status.suspected_since = None
        status.failed_since = None
        
        # Notify recovery if node was suspected or failed
        if old_state in [NodeState.SUSPECTED, NodeState.FAILED]:
            logger.info(f"Node recovered: {node_id}")
            self._notify_recovery(node_id)
    
    def get_node_state(self, node_id: str) -> NodeState:
        """Get current state of a node"""
        if node_id in self.node_states:
            return self.node_states[node_id].state
        return NodeState.UNKNOWN
    
    def get_alive_nodes(self) -> Set[str]:
        """Get set of alive nodes"""
        return {
            node_id for node_id, status in self.node_states.items()
            if status.state == NodeState.ALIVE
        }
    
    def get_suspected_nodes(self) -> Set[str]:
        """Get set of suspected nodes"""
        return {
            node_id for node_id, status in self.node_states.items()
            if status.state == NodeState.SUSPECTED
        }
    
    def get_failed_nodes(self) -> Set[str]:
        """Get set of failed nodes"""
        return {
            node_id for node_id, status in self.node_states.items()
            if status.state == NodeState.FAILED
        }
    
    def register_failure_callback(self, callback: Callable):
        """Register a callback for node failures"""
        self.failure_callbacks.append(callback)
    
    def register_recovery_callback(self, callback: Callable):
        """Register a callback for node recoveries"""
        self.recovery_callbacks.append(callback)
    
    def calculate_phi(self, node_id: str) -> float:
        """
        Calculate phi value for a node using improved phi-accrual algorithm
        Higher phi value indicates higher probability of failure
        """
        if node_id not in self.node_states or node_id not in self.heartbeat_windows:
            return 0.0
        
        status = self.node_states[node_id]
        window = self.heartbeat_windows[node_id]
        
        # Need enough samples for meaningful statistics
        mean = window.mean()
        stddev = window.stddev()
        if mean is None or stddev is None:
            return 0.0
        
        # Time since last heartbeat
        current_time = time.time()
        time_since_last = current_time - status.last_heartbeat
        
        # Early return if time is too short
        if time_since_last < self._min_interval:
            return 0.0
        
        # Calculate phi value with numerical stability checks
        try:
            # Normalize time difference
            z_score = (time_since_last - mean) / stddev
            
            # Use numerically stable approximation for large z-scores
            if z_score > 10:
                return z_score  # Linear approximation for very large delays
            
            import math
            # Calculate probability using normal distribution
            p = 0.5 * (1 + math.erf(-z_score / math.sqrt(2)))
            
            # Clamp probability to avoid log(0)
            p = max(1e-15, min(1.0, p))
            
            # Calculate phi
            phi = -math.log10(p)
            
            # Cap phi value for stability
            return min(phi, 50.0)  # Upper limit to avoid numerical issues
            
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            logger.warning(f"Error calculating phi for {node_id}: {e}")
            if time_since_last > self.heartbeat_interval * self.failure_threshold:
                return self.phi_threshold + 1  # Force failure state
            return 0.0
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self._running:
            try:
                current_time = time.time()
                
                for node_id, status in list(self.node_states.items()):
                    # Skip monitoring self
                    if node_id == self.node_id:
                        continue
                        
                    time_since_last = current_time - status.last_heartbeat
                    
                    # Calculate phi value
                    phi = self.calculate_phi(node_id)
                    
                    # Update state based on phi and time thresholds
                    if phi > self.phi_threshold:
                        # Node is failed
                        if status.state != NodeState.FAILED:
                            logger.warning(f"Node marked as FAILED: {node_id} (phi={phi:.2f})")
                            status.state = NodeState.FAILED
                            status.failed_since = current_time
                            self._notify_failure(node_id)
                    
                    elif time_since_last > (self.heartbeat_interval * self.suspicion_threshold):
                        # Node is suspected
                        if status.state == NodeState.ALIVE:
                            logger.warning(f"Node marked as SUSPECTED: {node_id} (phi={phi:.2f})")
                            status.state = NodeState.SUSPECTED
                            status.suspected_since = current_time
                    
                    # Update missed heartbeats counter
                    expected_heartbeats = int(time_since_last / self.heartbeat_interval)
                    status.missed_heartbeats = max(0, expected_heartbeats - 1)
                
                await asyncio.sleep(self.heartbeat_interval / 2)  # Monitor more frequently
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in failure detector monitor loop: {e}")
                await asyncio.sleep(self.heartbeat_interval)
    
    def _notify_failure(self, node_id: str):
        """Notify failure callbacks"""
        for callback in self.failure_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(node_id))
                else:
                    callback(node_id)
            except Exception as e:
                logger.error(f"Error in failure callback: {e}")
    
    def _notify_recovery(self, node_id: str):
        """Notify recovery callbacks"""
        for callback in self.recovery_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(node_id))
                else:
                    callback(node_id)
            except Exception as e:
                logger.error(f"Error in recovery callback: {e}")
    
    def get_cluster_health(self) -> Dict:
        """Get overall cluster health metrics"""
        total = len(self.node_states)
        if total == 0:
            return {
                'total_nodes': 0,
                'alive': 0,
                'suspected': 0, 
                'failed': 0,
                'health_percentage': 0
            }
        
        alive = len(self.get_alive_nodes())
        suspected = len(self.get_suspected_nodes())
        failed = len(self.get_failed_nodes())
        
        return {
            'total_nodes': total,
            'alive': alive,
            'suspected': suspected,
            'failed': failed,
            'health_percentage': (alive / total) * 100
        }
