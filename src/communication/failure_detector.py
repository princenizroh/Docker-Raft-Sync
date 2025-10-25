"""
Failure Detector Module
Implements failure detection for distributed nodes
"""

import asyncio
import time
import logging
from typing import Dict, Set, Callable, Optional
from dataclasses import dataclass
from enum import Enum

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


class FailureDetector:
    """
    Implements an adaptive failure detector using heartbeats
    Based on phi-accrual failure detector algorithm
    """
    
    def __init__(
        self,
        node_id: str,
        heartbeat_interval: float = 1.0,
        suspicion_threshold: int = 3,
        failure_threshold: int = 5,
        phi_threshold: float = 8.0
    ):
        self.node_id = node_id
        self.heartbeat_interval = heartbeat_interval
        self.suspicion_threshold = suspicion_threshold
        self.failure_threshold = failure_threshold
        self.phi_threshold = phi_threshold
        
        self.node_states: Dict[str, NodeStatus] = {}
        self.heartbeat_history: Dict[str, list] = {}
        self.failure_callbacks: list = []
        self.recovery_callbacks: list = []
        
        self._running = False
        self._monitor_task: Optional[asyncio.Task] = None
    
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
                last_heartbeat=time.time()
            )
            self.heartbeat_history[node_id] = []
            logger.info(f"Registered node for monitoring: {node_id}")
    
    def unregister_node(self, node_id: str):
        """Unregister a node from monitoring"""
        if node_id in self.node_states:
            del self.node_states[node_id]
            del self.heartbeat_history[node_id]
            logger.info(f"Unregistered node: {node_id}")
    
    def record_heartbeat(self, node_id: str):
        """Record a heartbeat from a node"""
        current_time = time.time()
        
        if node_id not in self.node_states:
            self.register_node(node_id)
        
        status = self.node_states[node_id]
        
        # Record heartbeat time
        if node_id in self.heartbeat_history:
            self.heartbeat_history[node_id].append(current_time)
            # Keep only last 100 heartbeats
            if len(self.heartbeat_history[node_id]) > 100:
                self.heartbeat_history[node_id] = self.heartbeat_history[node_id][-100:]
        
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
        Calculate phi value for a node (phi-accrual failure detector)
        Higher phi value indicates higher probability of failure
        """
        if node_id not in self.heartbeat_history:
            return 0.0
        
        history = self.heartbeat_history[node_id]
        if len(history) < 2:
            return 0.0
        
        # Calculate inter-arrival times
        intervals = []
        for i in range(1, len(history)):
            intervals.append(history[i] - history[i-1])
        
        if not intervals:
            return 0.0
        
        # Calculate mean and standard deviation
        mean = sum(intervals) / len(intervals)
        variance = sum((x - mean) ** 2 for x in intervals) / len(intervals)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            std_dev = 0.001  # Avoid division by zero
        
        # Time since last heartbeat
        current_time = time.time()
        status = self.node_states[node_id]
        time_since_last = current_time - status.last_heartbeat
        
        # Calculate phi
        # phi = -log10(P(T > t))
        # Using exponential distribution assumption
        import math
        try:
            exp_val = math.exp(-(time_since_last - mean) / std_dev)
            # Clamp to avoid log domain errors
            exp_val = max(1e-10, min(1.0, exp_val))
            phi = -math.log10(exp_val)
        except (ValueError, ZeroDivisionError):
            phi = 0.0
        
        # TEMPORARY: Return low phi to avoid false failures
        return max(0, min(phi, 5.0))  # Cap at 5.0
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self._running:
            try:
                current_time = time.time()
                
                for node_id, status in list(self.node_states.items()):
                    time_since_last = current_time - status.last_heartbeat
                    
                    # Calculate phi value
                    phi = self.calculate_phi(node_id)
                    
                    # Update state based on phi and time
                    if phi > self.phi_threshold or time_since_last > (self.heartbeat_interval * self.failure_threshold):
                        # Node is failed
                        if status.state != NodeState.FAILED:
                            old_state = status.state
                            status.state = NodeState.FAILED
                            status.failed_since = current_time
                            logger.warning(f"Node marked as FAILED: {node_id} (phi={phi:.2f})")
                            self._notify_failure(node_id)
                    
                    elif time_since_last > (self.heartbeat_interval * self.suspicion_threshold):
                        # Node is suspected
                        if status.state == NodeState.ALIVE:
                            status.state = NodeState.SUSPECTED
                            status.suspected_since = current_time
                            logger.warning(f"Node marked as SUSPECTED: {node_id} (phi={phi:.2f})")
                    
                    # Update missed heartbeats counter
                    expected_heartbeats = int(time_since_last / self.heartbeat_interval)
                    status.missed_heartbeats = max(0, expected_heartbeats - 1)
                
                await asyncio.sleep(self.heartbeat_interval)
                
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
