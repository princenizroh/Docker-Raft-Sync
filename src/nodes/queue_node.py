"""
Distributed Queue System
Implements distributed queue with consistent hashing and persistence
"""

import asyncio
import hashlib
import json
import logging
import os
import pickle
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from collections import deque, defaultdict
import time

from .base_node import BaseNode
from ..utils.metrics import get_metrics

logger = logging.getLogger(__name__)


@dataclass
class QueueMessage:
    """Queue message structure"""
    message_id: str
    data: Any
    timestamp: float = field(default_factory=time.time)
    partition: int = 0
    retry_count: int = 0
    delivered: bool = False
    
    def to_dict(self) -> dict:
        return {
            'message_id': self.message_id,
            'data': self.data,
            'timestamp': self.timestamp,
            'partition': self.partition,
            'retry_count': self.retry_count,
            'delivered': self.delivered
        }


class ConsistentHash:
    """Consistent hashing implementation"""
    
    def __init__(self, nodes: List[str], virtual_nodes: int = 100):
        self.nodes = nodes
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}
        self._build_ring()
    
    def _build_ring(self):
        """Build the hash ring"""
        for node in self.nodes:
            for i in range(self.virtual_nodes):
                key = f"{node}:{i}"
                hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
                self.ring[hash_value] = node
    
    def get_node(self, key: str) -> str:
        """Get node for a given key"""
        if not self.ring:
            return None
        
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        
        # Find the first node with hash >= key hash
        for ring_hash in sorted(self.ring.keys()):
            if ring_hash >= hash_value:
                return self.ring[ring_hash]
        
        # Wrap around to first node
        return self.ring[min(self.ring.keys())]
    
    def add_node(self, node: str):
        """Add a node to the ring"""
        if node not in self.nodes:
            self.nodes.append(node)
            for i in range(self.virtual_nodes):
                key = f"{node}:{i}"
                hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
                self.ring[hash_value] = node
    
    def remove_node(self, node: str):
        """Remove a node from the ring"""
        if node in self.nodes:
            self.nodes.remove(node)
            # Remove all virtual nodes
            keys_to_remove = [k for k, v in self.ring.items() if v == node]
            for key in keys_to_remove:
                del self.ring[key]


class DistributedQueue(BaseNode):
    """
    Distributed Queue System with consistent hashing
    Provides at-least-once delivery guarantee
    """
    
    def __init__(
        self,
        node_id: str,
        host: str,
        port: int,
        cluster_nodes: list,
        partition_count: int = 16,
        replication_factor: int = 2,
        persistence_path: str = './data/queue'
    ):
        super().__init__(node_id, host, port, cluster_nodes)
        
        self.partition_count = partition_count
        self.replication_factor = replication_factor
        self.persistence_path = persistence_path
        
        # Queue storage
        self.queues: Dict[int, deque] = defaultdict(deque)
        self.message_index: Dict[str, QueueMessage] = {}
        self.consumer_offsets: Dict[str, Dict[int, int]] = defaultdict(dict)
        
        # Consistent hashing
        # If no cluster nodes, use self as the only node
        if cluster_nodes:
            self.consistent_hash = ConsistentHash(cluster_nodes)
        else:
            self.consistent_hash = ConsistentHash([f"{node_id}:{host}:{port}"])
        
        # Metrics
        self.metrics = get_metrics()
        
        # Ensure persistence directory exists
        os.makedirs(persistence_path, exist_ok=True)
        
        # Background tasks
        self._persistence_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start distributed queue"""
        await super().start()
        
        # Load persisted data
        await self._load_persisted_data()
        
        # Start background tasks
        self._persistence_task = asyncio.create_task(self._periodic_persistence())
        
        logger.info("Distributed Queue started")
    
    async def stop(self):
        """Stop distributed queue"""
        # Persist data before stopping
        await self._persist_data()
        
        if self._persistence_task:
            self._persistence_task.cancel()
            try:
                await self._persistence_task
            except asyncio.CancelledError:
                pass
        
        await super().stop()
        logger.info("Distributed Queue stopped")
    
    def _get_partition(self, key: str) -> int:
        """Get partition for a key"""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_value % self.partition_count
    
    def _is_partition_owner(self, partition: int) -> bool:
        """Check if this node owns a partition"""
        partition_key = f"partition_{partition}"
        owner = self.consistent_hash.get_node(partition_key)
        return owner == f"{self.node_id}:{self.host}:{self.port}"
    
    async def enqueue(self, queue_name: str, data: Any, message_id: Optional[str] = None) -> bool:
        """
        Enqueue a message
        Returns True if successful
        """
        if message_id is None:
            message_id = f"{self.node_id}_{time.time()}_{id(data)}"
        
        partition = self._get_partition(queue_name)
        
        message = QueueMessage(
            message_id=message_id,
            data=data,
            partition=partition
        )
        
        # Submit through Raft for replication
        success = await self.submit_command('enqueue', {
            'queue_name': queue_name,
            'message': message.to_dict()
        })
        
        if success:
            self.metrics.increment_counter('messages_enqueued')
            logger.debug(f"Message enqueued: {message_id} to {queue_name}")
        
        return success
    
    async def dequeue(self, queue_name: str, consumer_id: str) -> Optional[QueueMessage]:
        """
        Dequeue a message
        Returns message if available, None otherwise
        """
        partition = self._get_partition(queue_name)
        
        if not self._is_partition_owner(partition):
            logger.warning(f"Not owner of partition {partition}")
            return None
        
        if partition not in self.queues or not self.queues[partition]:
            return None
        
        # Get message
        message = self.queues[partition].popleft()
        
        # Update consumer offset
        self.consumer_offsets[consumer_id][partition] = \
            self.consumer_offsets[consumer_id].get(partition, 0) + 1
        
        # Mark as delivered (at-least-once)
        message.delivered = True
        
        # Submit through Raft
        await self.submit_command('mark_delivered', {
            'message_id': message.message_id,
            'consumer_id': consumer_id
        })
        
        self.metrics.increment_counter('messages_dequeued')
        logger.debug(f"Message dequeued: {message.message_id} by {consumer_id}")
        
        return message
    
    async def acknowledge(self, message_id: str, consumer_id: str) -> bool:
        """Acknowledge message delivery"""
        success = await self.submit_command('acknowledge', {
            'message_id': message_id,
            'consumer_id': consumer_id
        })
        
        if success:
            self.metrics.increment_counter('messages_acknowledged')
        
        return success
    
    async def process_committed_entry(self, log_entry):
        """Process committed queue commands"""
        command = log_entry.command
        data = log_entry.data
        
        if command == 'enqueue':
            await self._process_enqueue(data)
        elif command == 'mark_delivered':
            await self._process_mark_delivered(data)
        elif command == 'acknowledge':
            await self._process_acknowledge(data)
    
    async def _process_enqueue(self, data: dict):
        """Process enqueue command"""
        queue_name = data['queue_name']
        message_dict = data['message']
        
        message = QueueMessage(**message_dict)
        partition = message.partition
        
        # Add to queue
        self.queues[partition].append(message)
        self.message_index[message.message_id] = message
        
        logger.debug(f"Processed enqueue: {message.message_id}")
    
    async def _process_mark_delivered(self, data: dict):
        """Process mark delivered command"""
        message_id = data['message_id']
        
        if message_id in self.message_index:
            self.message_index[message_id].delivered = True
    
    async def _process_acknowledge(self, data: dict):
        """Process acknowledge command"""
        message_id = data['message_id']
        
        # Remove from index after acknowledgment
        if message_id in self.message_index:
            del self.message_index[message_id]
    
    async def _periodic_persistence(self):
        """Periodically persist queue data"""
        while self.running:
            try:
                await asyncio.sleep(10.0)  # Persist every 10 seconds
                await self._persist_data()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in periodic persistence: {e}")
    
    async def _persist_data(self):
        """Persist queue data to disk"""
        try:
            data = {
                'queues': {
                    partition: list(queue)
                    for partition, queue in self.queues.items()
                },
                'message_index': {
                    msg_id: msg.to_dict()
                    for msg_id, msg in self.message_index.items()
                },
                'consumer_offsets': dict(self.consumer_offsets)
            }
            
            persistence_file = os.path.join(
                self.persistence_path,
                f"{self.node_id}_queue.pkl"
            )
            
            with open(persistence_file, 'wb') as f:
                pickle.dump(data, f)
            
            logger.debug("Queue data persisted")
            
        except Exception as e:
            logger.error(f"Error persisting data: {e}")
    
    async def _load_persisted_data(self):
        """Load persisted queue data"""
        try:
            persistence_file = os.path.join(
                self.persistence_path,
                f"{self.node_id}_queue.pkl"
            )
            
            if not os.path.exists(persistence_file):
                logger.info("No persisted data found")
                return
            
            with open(persistence_file, 'rb') as f:
                data = pickle.load(f)
            
            # Restore queues
            for partition, messages in data.get('queues', {}).items():
                self.queues[int(partition)] = deque(
                    QueueMessage(**msg) if isinstance(msg, dict) else msg
                    for msg in messages
                )
            
            # Restore message index
            for msg_id, msg_dict in data.get('message_index', {}).items():
                self.message_index[msg_id] = QueueMessage(**msg_dict)
            
            # Restore consumer offsets
            self.consumer_offsets = defaultdict(
                dict,
                data.get('consumer_offsets', {})
            )
            
            logger.info("Queue data loaded from persistence")
            
        except Exception as e:
            logger.error(f"Error loading persisted data: {e}")
    
    def get_queue_stats(self) -> dict:
        """Get queue statistics"""
        total_messages = sum(len(q) for q in self.queues.values())
        
        return {
            'total_messages': total_messages,
            'partitions': len(self.queues),
            'messages_by_partition': {
                partition: len(queue)
                for partition, queue in self.queues.items()
            },
            'total_consumers': len(self.consumer_offsets),
            'messages_in_index': len(self.message_index)
        }


if __name__ == '__main__':
    import argparse
    
    async def main():
        parser = argparse.ArgumentParser(description='Run Distributed Queue')
        parser.add_argument('--node-id', required=True, help='Node ID')
        parser.add_argument('--host', default='0.0.0.0', help='Host address')
        parser.add_argument('--port', type=int, required=True, help='Port number')
        parser.add_argument('--cluster-nodes', required=True, help='Cluster nodes')
        
        args = parser.parse_args()
        cluster_nodes = args.cluster_nodes.split(',')
        
        queue = DistributedQueue(
            node_id=args.node_id,
            host=args.host,
            port=args.port,
            cluster_nodes=cluster_nodes
        )
        
        try:
            await queue.start()
            
            while True:
                await asyncio.sleep(1)
        
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            await queue.stop()
    
    asyncio.run(main())
