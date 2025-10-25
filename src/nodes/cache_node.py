"""
Distributed Cache with MESI Coherence Protocol
Implements cache coherence with LRU replacement policy
"""

import asyncio
import logging
import time
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from enum import Enum
from collections import OrderedDict

from .base_node import BaseNode
from ..utils.metrics import get_metrics

logger = logging.getLogger(__name__)


class MESIState(Enum):
    """MESI cache coherence protocol states"""
    MODIFIED = "modified"   
    EXCLUSIVE = "exclusive" 
    SHARED = "shared"     
    INVALID = "invalid"  


@dataclass
class CacheLine:
    """Cache line with MESI state"""
    key: str
    value: Any
    state: MESIState
    timestamp: float
    last_accessed: float
    version: int = 0
    
    def to_dict(self) -> dict:
        return {
            'key': self.key,
            'value': self.value,
            'state': self.state.value,
            'timestamp': self.timestamp,
            'last_accessed': self.last_accessed,
            'version': self.version
        }


class LRUCache:
    """LRU Cache implementation"""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict[str, CacheLine] = OrderedDict()
    
    def get(self, key: str) -> Optional[CacheLine]:
        """Get cache line and move to end (most recent)"""
        if key not in self.cache:
            return None
        
        self.cache.move_to_end(key)
        line = self.cache[key]
        line.last_accessed = time.time()
        return line
    
    def put(self, key: str, line: CacheLine):
        """Put cache line"""
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = line
        else:
            if len(self.cache) >= self.capacity:
                evicted_key, evicted_line = self.cache.popitem(last=False)
                logger.debug(f"Evicted cache line: {evicted_key}")
            
            self.cache[key] = line
    
    def remove(self, key: str):
        """Remove cache line"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache lines"""
        self.cache.clear()
    
    def __len__(self):
        return len(self.cache)
    
    def keys(self):
        return self.cache.keys()


class DistributedCache(BaseNode):
    """
    Distributed Cache with MESI coherence protocol
    """
    
    def __init__(
        self,
        node_id: str,
        host: str,
        port: int,
        cluster_nodes: list,
        cache_size_mb: int = 256,
        invalidation_timeout: int = 5000
    ):
        super().__init__(node_id, host, port, cluster_nodes)
        
        capacity = (cache_size_mb * 1024) // 1
        self.cache = LRUCache(capacity)
        self.invalidation_timeout = invalidation_timeout / 1000.0  
        
        self.metrics = get_metrics()
        
        self._setup_cache_handlers()
    
    def _setup_cache_handlers(self):
        """Setup cache-specific message handlers"""
        from ..communication.message_passing import MessageType
        
        self.message_passing.register_handler(
            MessageType.CACHE_GET.value,
            self._handle_cache_get
        )
        self.message_passing.register_handler(
            MessageType.CACHE_PUT.value,
            self._handle_cache_put
        )
        self.message_passing.register_handler(
            MessageType.CACHE_INVALIDATE.value,
            self._handle_cache_invalidate
        )
        self.message_passing.register_handler(
            MessageType.CACHE_UPDATE.value,
            self._handle_cache_update
        )
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        Implements MESI protocol for coherence
        """
        line = self.cache.get(key)
        
        if line is None or line.state == MESIState.INVALID:
            self.metrics.increment_counter('cache_misses')
            value = await self._fetch_from_cluster(key)
            
            if value is not None:
                new_line = CacheLine(
                    key=key,
                    value=value,
                    state=MESIState.SHARED,
                    timestamp=time.time(),
                    last_accessed=time.time()
                )
                self.cache.put(key, new_line)
            
            return value
        
        self.metrics.increment_counter('cache_hits')
        
        if line.state == MESIState.MODIFIED:
            return line.value
        elif line.state in [MESIState.EXCLUSIVE, MESIState.SHARED]:
            return line.value
        
        return None
    
    async def put(self, key: str, value: Any) -> bool:
        """
        Put value in cache
        Implements MESI protocol for coherence
        """
        await self._broadcast_invalidate(key)
        
        line = CacheLine(
            key=key,
            value=value,
            state=MESIState.MODIFIED,
            timestamp=time.time(),
            last_accessed=time.time(),
            version=self._get_version(key) + 1
        )
        
        self.cache.put(key, line)
        
        success = await self.submit_command('cache_put', {
            'key': key,
            'value': value,
            'version': line.version
        })
        
        if success:
            self.metrics.increment_counter('cache_puts')
        
        return success
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        await self._broadcast_invalidate(key)
        
        self.cache.remove(key)
        
        success = await self.submit_command('cache_delete', {'key': key})
        
        if success:
            self.metrics.increment_counter('cache_deletes')
        
        return success
    
    def _get_version(self, key: str) -> int:
        """Get current version of a cache line"""
        line = self.cache.get(key)
        return line.version if line else 0
    
    async def _fetch_from_cluster(self, key: str) -> Optional[Any]:
        """Fetch value from other nodes in cluster"""
        from ..communication.message_passing import Message, MessageType
        
        for node in self.message_passing.get_connected_nodes():
            message = Message(
                msg_type=MessageType.CACHE_GET.value,
                sender_id=self.node_id,
                receiver_id=node,
                payload={'key': key}
            )
            
            await self.message_passing.send_message(node, message)
        
        await asyncio.sleep(0.1)
        
        line = self.cache.get(key)
        if line and line.state != MESIState.INVALID:
            return line.value
        
        return None
    
    async def _broadcast_invalidate(self, key: str):
        """Broadcast cache invalidation to all nodes"""
        from ..communication.message_passing import Message, MessageType
        
        for node in self.message_passing.get_connected_nodes():
            message = Message(
                msg_type=MessageType.CACHE_INVALIDATE.value,
                sender_id=self.node_id,
                receiver_id=node,
                payload={'key': key}
            )
            
            await self.message_passing.send_message(node, message)
    
    async def _handle_cache_get(self, message):
        """Handle cache get request from another node"""
        key = message.payload.get('key')
        line = self.cache.get(key)
        
        if line and line.state != MESIState.INVALID:
            from ..communication.message_passing import Message, MessageType
            
            response = Message(
                msg_type=MessageType.CACHE_UPDATE.value,
                sender_id=self.node_id,
                receiver_id=message.sender_id,
                payload={
                    'key': key,
                    'value': line.value,
                    'version': line.version
                }
            )
            
            await self.message_passing.send_message(message.sender_id, response)
            
            if line.state == MESIState.EXCLUSIVE:
                line.state = MESIState.SHARED
    
    async def _handle_cache_put(self, message):
        """Handle cache put from another node"""
        key = message.payload.get('key')
        value = message.payload.get('value')
        version = message.payload.get('version', 0)
        
        line = self.cache.get(key)
        
        if line is None or version > line.version:
            new_line = CacheLine(
                key=key,
                value=value,
                state=MESIState.SHARED,
                timestamp=time.time(),
                last_accessed=time.time(),
                version=version
            )
            self.cache.put(key, new_line)
    
    async def _handle_cache_invalidate(self, message):
        """Handle cache invalidation"""
        key = message.payload.get('key')
        line = self.cache.get(key)
        
        if line:
            if line.state == MESIState.MODIFIED:
                logger.debug(f"Writing back modified cache line: {key}")
            
            line.state = MESIState.INVALID
            
            self.metrics.increment_counter('cache_invalidations')
    
    async def _handle_cache_update(self, message):
        """Handle cache update from another node"""
        key = message.payload.get('key')
        value = message.payload.get('value')
        version = message.payload.get('version', 0)
        
        line = self.cache.get(key)
        
        if line is None or version > line.version:
            new_line = CacheLine(
                key=key,
                value=value,
                state=MESIState.SHARED,
                timestamp=time.time(),
                last_accessed=time.time(),
                version=version
            )
            self.cache.put(key, new_line)
    
    async def process_committed_entry(self, log_entry):
        """Process committed cache commands"""
        command = log_entry.command
        data = log_entry.data
        
        if command == 'cache_put':
            key = data['key']
            value = data['value']
            version = data.get('version', 0)
            
            line = CacheLine(
                key=key,
                value=value,
                state=MESIState.SHARED,
                timestamp=time.time(),
                last_accessed=time.time(),
                version=version
            )
            self.cache.put(key, line)
        
        elif command == 'cache_delete':
            key = data['key']
            self.cache.remove(key)
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics"""
        total_lines = len(self.cache)
        
        states_count = {
            'modified': 0,
            'exclusive': 0,
            'shared': 0,
            'invalid': 0
        }
        
        # Fix: Create a snapshot of keys to avoid mutation during iteration
        for key in list(self.cache.keys()):
            line = self.cache.get(key)
            if line:
                states_count[line.state.value] += 1
        
        hit_rate = 0
        total_requests = self.metrics.get_counter('cache_hits') + self.metrics.get_counter('cache_misses')
        if total_requests > 0:
            hit_rate = (self.metrics.get_counter('cache_hits') / total_requests) * 100
        
        return {
            'total_lines': total_lines,
            'capacity': self.cache.capacity,
            'utilization_percent': (total_lines / self.cache.capacity) * 100,
            'states': states_count,
            'hit_rate_percent': hit_rate,
            'hits': self.metrics.get_counter('cache_hits'),
            'misses': self.metrics.get_counter('cache_misses'),
            'puts': self.metrics.get_counter('cache_puts'),
            'invalidations': self.metrics.get_counter('cache_invalidations')
        }


if __name__ == '__main__':
    import argparse
    
    async def main():
        parser = argparse.ArgumentParser(description='Run Distributed Cache')
        parser.add_argument('--node-id', required=True, help='Node ID')
        parser.add_argument('--host', default='0.0.0.0', help='Host address')
        parser.add_argument('--port', type=int, required=True, help='Port number')
        parser.add_argument('--cluster-nodes', required=True, help='Cluster nodes')
        
        args = parser.parse_args()
        cluster_nodes = args.cluster_nodes.split(',')
        
        cache = DistributedCache(
            node_id=args.node_id,
            host=args.host,
            port=args.port,
            cluster_nodes=cluster_nodes
        )
        
        try:
            await cache.start()
            
            while True:
                await asyncio.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            await cache.stop()
    
    asyncio.run(main())
