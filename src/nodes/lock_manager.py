"""
Distributed Lock Manager
Implements distributed locking with deadlock detection
"""

import asyncio
import time
import logging
from typing import Dict, Set, Optional, List
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict

from .base_node import BaseNode
from ..utils.metrics import get_metrics

logger = logging.getLogger(__name__)


class LockType(Enum):
    """Types of locks"""
    SHARED = "shared"
    EXCLUSIVE = "exclusive"


class LockStatus(Enum):
    """Lock status"""
    GRANTED = "granted"
    WAITING = "waiting"
    DENIED = "denied"


@dataclass
class LockRequest:
    """Lock request information"""
    resource_id: str
    requester_id: str
    lock_type: LockType
    timestamp: float
    timeout: float
    status: LockStatus = LockStatus.WAITING


@dataclass
class Lock:
    """Lock information"""
    resource_id: str
    holders: Set[str]
    lock_type: Optional[LockType]
    waiters: List[LockRequest]
    
    def __init__(self, resource_id: str):
        self.resource_id = resource_id
        self.holders = set()
        self.lock_type = None
        self.waiters = []


class DistributedLockManager(BaseNode):
    """
    Distributed Lock Manager with deadlock detection
    Extends BaseNode to use Raft consensus for lock coordination
    """
    
    def __init__(self, node_id: str, host: str, port: int, cluster_nodes: list):
        super().__init__(node_id, host, port, cluster_nodes)
        
        self.locks: Dict[str, Lock] = {}
        self.held_locks: Dict[str, Set[str]] = defaultdict(set)  
        self.wait_for_graph: Dict[str, Set[str]] = defaultdict(set) 
        
        self.default_lock_timeout = 30.0 
        self.deadlock_detection_interval = 10.0  
        
        self.metrics = get_metrics()
        
        self._deadlock_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start lock manager"""
        await super().start()
        self._deadlock_task = asyncio.create_task(self._deadlock_detector())
        logger.info("Distributed Lock Manager started")
    
    async def stop(self):
        """Stop lock manager"""
        if self._deadlock_task:
            self._deadlock_task.cancel()
            try:
                await self._deadlock_task
            except asyncio.CancelledError:
                pass
        await super().stop()
        logger.info("Distributed Lock Manager stopped")
    
    async def acquire_lock(
        self,
        resource_id: str,
        requester_id: str,
        lock_type: LockType = LockType.EXCLUSIVE,
        timeout: float = None
    ) -> bool:
        """
        Acquire a lock on a resource
        Returns True if lock acquired, False otherwise
        """
        if timeout is None:
            timeout = self.default_lock_timeout
        
        request = LockRequest(
            resource_id=resource_id,
            requester_id=requester_id,
            lock_type=lock_type,
            timestamp=time.time(),
            timeout=timeout
        )
        
        # Convert to dict and serialize enums
        request_dict = request.__dict__.copy()
        request_dict['lock_type'] = lock_type.value  # Serialize enum
        request_dict['status'] = request.status.value  # Serialize enum status
        
        success = await self.submit_command('acquire_lock', request_dict)
        
        if not success:
            logger.warning(f"Failed to submit lock request for {resource_id}")
            return False
        
        logger.info(f"Lock request submitted for {resource_id} by {requester_id}, waiting...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._is_lock_held(requester_id, resource_id):
                self.metrics.increment_counter('locks_acquired')
                logger.info(f"Lock acquired: {resource_id} by {requester_id}")
                return True
            await asyncio.sleep(0.1)
        
        await self.submit_command('cancel_lock_request', {
            'resource_id': resource_id,
            'requester_id': requester_id
        })
        
        self.metrics.increment_counter('lock_timeouts')
        logger.warning(f"Lock acquisition timeout: {resource_id} by {requester_id}")
        return False
    
    async def release_lock(self, resource_id: str, holder_id: str) -> bool:
        """Release a lock on a resource"""
        success = await self.submit_command('release_lock', {
            'resource_id': resource_id,
            'holder_id': holder_id
        })
        
        if success:
            self.metrics.increment_counter('locks_released')
            logger.info(f"Lock released: {resource_id} by {holder_id}")
        
        return success
    
    async def process_committed_entry(self, log_entry):
        """Process committed lock commands"""
        command = log_entry.command
        data = log_entry.data
        
        if command == 'acquire_lock':
            await self._process_acquire_lock(data)
        elif command == 'release_lock':
            await self._process_release_lock(data)
        elif command == 'cancel_lock_request':
            await self._process_cancel_request(data)
    
    async def _process_acquire_lock(self, request_data: dict):
        """Process lock acquisition request"""
        resource_id = request_data['resource_id']
        requester_id = request_data['requester_id']
        lock_type = LockType(request_data['lock_type'])
        status = LockStatus(request_data['status'])  # Deserialize status enum
        
        logger.info(f"Processing lock request: {resource_id} by {requester_id} (type: {lock_type.value})")
        
        if resource_id not in self.locks:
            self.locks[resource_id] = Lock(resource_id)
        
        lock = self.locks[resource_id]
        request = LockRequest(**request_data)
        request.lock_type = lock_type
        request.status = status  # Set deserialized status
       
        can_grant = self._can_grant_lock(lock, lock_type)
        
        logger.info(f"Can grant lock {resource_id}? {can_grant}")
        
        if can_grant:
            lock.holders.add(requester_id)
            lock.lock_type = lock_type
            self.held_locks[requester_id].add(resource_id)
            request.status = LockStatus.GRANTED
            
            if requester_id in self.wait_for_graph:
                del self.wait_for_graph[requester_id]
            
            logger.debug(f"Lock granted: {resource_id} to {requester_id} ({lock_type.value})")
        else:
            lock.waiters.append(request)
            
            self.wait_for_graph[requester_id] = set(lock.holders)
            
            logger.debug(f"Lock request queued: {resource_id} by {requester_id}")
    
    async def _process_release_lock(self, release_data: dict):
        """Process lock release"""
        resource_id = release_data['resource_id']
        holder_id = release_data['holder_id']
        
        if resource_id not in self.locks:
            logger.warning(f"Attempted to release non-existent lock: {resource_id}")
            return
        
        lock = self.locks[resource_id]
        
        if holder_id not in lock.holders:
            logger.warning(f"Attempted to release lock not held: {resource_id} by {holder_id}")
            return
        
        lock.holders.remove(holder_id)
        self.held_locks[holder_id].discard(resource_id)
        
        if not lock.holders:
            lock.lock_type = None
        
        await self._grant_waiting_locks(lock)
        
        if not lock.holders and not lock.waiters:
            del self.locks[resource_id]
        
        logger.debug(f"Lock released: {resource_id} by {holder_id}")
    
    async def _process_cancel_request(self, cancel_data: dict):
        """Process lock request cancellation"""
        resource_id = cancel_data['resource_id']
        requester_id = cancel_data['requester_id']
        
        if resource_id in self.locks:
            lock = self.locks[resource_id]
            lock.waiters = [w for w in lock.waiters if w.requester_id != requester_id]
            
            if requester_id in self.wait_for_graph:
                del self.wait_for_graph[requester_id]
    
    def _can_grant_lock(self, lock: Lock, lock_type: LockType) -> bool:
        """Check if a lock can be granted"""
        if not lock.holders:
            return True
        
        if lock_type == LockType.SHARED and lock.lock_type == LockType.SHARED:
            return True
        
        return False
    
    async def _grant_waiting_locks(self, lock: Lock):
        """Try to grant locks to waiting requests"""
        granted = []
        
        for request in lock.waiters[:]:
            if time.time() - request.timestamp > request.timeout:
                lock.waiters.remove(request)
                if request.requester_id in self.wait_for_graph:
                    del self.wait_for_graph[request.requester_id]
                continue
            
            if self._can_grant_lock(lock, request.lock_type):
                lock.holders.add(request.requester_id)
                lock.lock_type = request.lock_type
                self.held_locks[request.requester_id].add(lock.resource_id)
                request.status = LockStatus.GRANTED
                granted.append(request)
                
                if request.requester_id in self.wait_for_graph:
                    del self.wait_for_graph[request.requester_id]
                
                logger.debug(f"Granted waiting lock: {lock.resource_id} to {request.requester_id}")
                
                if request.lock_type == LockType.EXCLUSIVE:
                    break
        
        for request in granted:
            if request in lock.waiters:
                lock.waiters.remove(request)
    
    def _is_lock_held(self, holder_id: str, resource_id: str) -> bool:
        """Check if a lock is held by a client"""
        return resource_id in self.held_locks.get(holder_id, set())
    
    async def _deadlock_detector(self):
        """Periodic deadlock detection"""
        while self.running:
            try:
                await asyncio.sleep(self.deadlock_detection_interval)
                
                deadlocks = self._detect_deadlocks()
                
                if deadlocks:
                    self.metrics.increment_counter('deadlocks_detected')
                    logger.warning(f"Deadlocks detected: {deadlocks}")
                    
                    await self._resolve_deadlocks(deadlocks)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in deadlock detector: {e}")
    
    def _detect_deadlocks(self) -> List[List[str]]:
        """
        Detect deadlocks using cycle detection in wait-for graph
        Returns list of cycles (deadlocks)
        """
        deadlocks = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> bool:
            """DFS to detect cycles"""
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.wait_for_graph.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor, path.copy()):
                        return True
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in deadlocks:
                        deadlocks.append(cycle)
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in self.wait_for_graph.keys():
            if node not in visited:
                dfs(node, [])
        
        return deadlocks
    
    async def _resolve_deadlocks(self, deadlocks: List[List[str]]):
        """Resolve deadlocks by aborting transactions"""
        for cycle in deadlocks:
            if not cycle:
                continue

            youngest = cycle[0]
            youngest_time = float('inf')
            
            for client_id in cycle:
                for resource_id in self.held_locks.get(client_id, set()):
                    if resource_id in self.locks:
                        lock = self.locks[resource_id]
                        for holder in lock.holders:
                            if holder == client_id:
                                if resource_id in self.locks:
                                    youngest = client_id
                                    break
            
            logger.warning(f"Resolving deadlock by aborting {youngest}")
            
            for resource_id in list(self.held_locks.get(youngest, set())):
                await self.release_lock(resource_id, youngest)
    
    def get_lock_status(self, resource_id: str) -> Optional[dict]:
        """Get status of a specific lock"""
        if resource_id not in self.locks:
            return None
        
        lock = self.locks[resource_id]
        return {
            'resource_id': resource_id,
            'holders': list(lock.holders),
            'lock_type': lock.lock_type.value if lock.lock_type else None,
            'waiters': len(lock.waiters),
            'waiter_details': [
                {
                    'requester': w.requester_id,
                    'type': w.lock_type.value,
                    'status': w.status.value
                }
                for w in lock.waiters
            ]
        }
    
    def get_all_locks(self) -> Dict[str, dict]:
        """Get status of all locks"""
        return {
            resource_id: self.get_lock_status(resource_id)
            for resource_id in self.locks.keys()
        }
    
    def get_client_locks(self, client_id: str) -> Set[str]:
        """Get all locks held by a client"""
        return self.held_locks.get(client_id, set())


if __name__ == '__main__':
    import argparse
    
    async def main():
        parser = argparse.ArgumentParser(description='Run Distributed Lock Manager')
        parser.add_argument('--node-id', required=True, help='Node ID')
        parser.add_argument('--host', default='0.0.0.0', help='Host address')
        parser.add_argument('--port', type=int, required=True, help='Port number')
        parser.add_argument('--cluster-nodes', required=True, help='Cluster nodes')
        
        args = parser.parse_args()
        cluster_nodes = args.cluster_nodes.split(',')
        
        lock_manager = DistributedLockManager(
            node_id=args.node_id,
            host=args.host,
            port=args.port,
            cluster_nodes=cluster_nodes
        )
        
        try:
            await lock_manager.start()
            
            while True:
                await asyncio.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            await lock_manager.stop()
    
    asyncio.run(main())
