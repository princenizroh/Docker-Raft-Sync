"""
Base Node Implementation
Integrates Raft consensus, message passing, and failure detection
"""

import asyncio
import logging
import sys
from typing import Optional, Dict, Any
from dataclasses import dataclass

from ..communication.message_passing import MessagePassing, Message, MessageType
from ..communication.failure_detector import FailureDetector, NodeState
from ..consensus.raft import RaftNode, RaftState
from ..utils.config import get_config
from ..utils.metrics import get_metrics, PerformanceTimer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseNode:
    """
    Base distributed node that combines all core components
    """
    
    def __init__(self, node_id: str, host: str, port: int, cluster_nodes: list):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.cluster_nodes = cluster_nodes
        
        # Initialize components
        self.message_passing = MessagePassing(node_id, host, port)
        self.failure_detector = FailureDetector(
            node_id=node_id,
            heartbeat_interval=1.0,
            suspicion_threshold=3,
            failure_threshold=5
        )
        self.raft = RaftNode(
            node_id=node_id,
            cluster_nodes=cluster_nodes,
            election_timeout_min=150,
            election_timeout_max=300,
            heartbeat_interval=50
        )
        
        # State
        self.running = False
        self.metrics = get_metrics()
        
        # Setup callbacks and handlers
        self._setup_message_handlers()
        self._setup_raft_callbacks()
        self._setup_failure_callbacks()
        
        logger.info(f"BaseNode {node_id} initialized on {host}:{port}")
    
    def _setup_message_handlers(self):
        """Register message handlers"""
        # Raft message handlers
        self.message_passing.register_handler(
            MessageType.REQUEST_VOTE.value,
            self._handle_request_vote
        )
        self.message_passing.register_handler(
            MessageType.VOTE_RESPONSE.value,
            self._handle_vote_response
        )
        self.message_passing.register_handler(
            MessageType.APPEND_ENTRIES.value,
            self._handle_append_entries
        )
        self.message_passing.register_handler(
            MessageType.APPEND_ENTRIES_RESPONSE.value,
            self._handle_append_entries_response
        )
        
        # Heartbeat handlers
        self.message_passing.register_handler(
            MessageType.HEARTBEAT.value,
            self._handle_heartbeat
        )
        self.message_passing.register_handler(
            MessageType.PING.value,
            self._handle_ping
        )
    
    def _setup_raft_callbacks(self):
        """Setup Raft callbacks"""
        self.raft.set_message_sender(self._send_raft_message)
        self.raft.set_state_change_callback(self._on_raft_state_change)
        self.raft.set_commit_callback(self._on_log_commit)
    
    def _setup_failure_callbacks(self):
        """Setup failure detector callbacks"""
        self.failure_detector.register_failure_callback(self._on_node_failure)
        self.failure_detector.register_recovery_callback(self._on_node_recovery)
        
        # Register all cluster nodes
        for node in self.cluster_nodes:
            if node != self.node_id:
                self.failure_detector.register_node(node)
    
    async def start(self):
        """Start the node"""
        logger.info(f"Starting node {self.node_id}...")
        self.running = True
        
        # Start components
        await self.message_passing.start()
        await self.failure_detector.start()
        await self.raft.start()
        
        # Start heartbeat sender
        asyncio.create_task(self._heartbeat_sender())
        
        # Connect to cluster nodes
        await self._connect_to_cluster()
        
        self.metrics.increment_counter('node_starts')
        logger.info(f"Node {self.node_id} started successfully")
    
    async def stop(self):
        """Stop the node"""
        logger.info(f"Stopping node {self.node_id}...")
        self.running = False
        
        # Stop components
        await self.raft.stop()
        await self.failure_detector.stop()
        await self.message_passing.stop()
        
        logger.info(f"Node {self.node_id} stopped")
    
    async def _connect_to_cluster(self):
        """Connect to other nodes in the cluster"""
        logger.info("Connecting to cluster nodes...")
        
        for node_addr in self.cluster_nodes:
            if node_addr != f"{self.node_id}:{self.host}:{self.port}":
                # Send initial ping
                message = Message(
                    msg_type=MessageType.PING.value,
                    sender_id=self.node_id,
                    receiver_id=node_addr
                )
                await self.message_passing.send_message(node_addr, message)
    
    async def _heartbeat_sender(self):
        """Send periodic heartbeats"""
        while self.running:
            try:
                # Send heartbeat to all connected nodes
                for node in self.message_passing.get_connected_nodes():
                    message = Message(
                        msg_type=MessageType.HEARTBEAT.value,
                        sender_id=self.node_id,
                        receiver_id=node,
                        term=self.raft.current_term
                    )
                    await self.message_passing.send_message(node, message)
                
                await asyncio.sleep(1.0)
                
            except Exception as e:
                logger.error(f"Error in heartbeat sender: {e}")
                await asyncio.sleep(1.0)
    
    # Raft message handlers
    async def _handle_request_vote(self, message: Message):
        """Handle RequestVote message"""
        with PerformanceTimer(self.metrics, 'request_vote_handling_time'):
            await self.raft.handle_request_vote({
                **message.payload,
                'term': message.term,
                'sender_id': message.sender_id
            })
    
    async def _handle_vote_response(self, message: Message):
        """Handle VoteResponse message"""
        await self.raft.handle_vote_response({
            **message.payload,
            'term': message.term,
            'sender_id': message.sender_id
        })
    
    async def _handle_append_entries(self, message: Message):
        """Handle AppendEntries message"""
        with PerformanceTimer(self.metrics, 'append_entries_handling_time'):
            await self.raft.handle_append_entries({
                **message.payload,
                'term': message.term
            })
    
    async def _handle_append_entries_response(self, message: Message):
        """Handle AppendEntries response"""
        await self.raft.handle_append_entries_response({
            **message.payload,
            'term': message.term,
            'sender_id': message.sender_id
        })
    
    async def _handle_heartbeat(self, message: Message):
        """Handle heartbeat message"""
        self.failure_detector.record_heartbeat(message.sender_id)
        self.metrics.increment_counter('heartbeats_received')
    
    async def _handle_ping(self, message: Message):
        """Handle ping message"""
        # Send pong response
        pong = Message(
            msg_type=MessageType.PONG.value,
            sender_id=self.node_id,
            receiver_id=message.sender_id
        )
        await self.message_passing.send_message(message.sender_id, pong)
    
    # Raft callbacks
    async def _send_raft_message(self, target_node: str, payload: dict):
        """Send Raft message to target node"""
        msg_type = payload.get('type', 'unknown')
        
        # Map Raft message types to our message types
        type_mapping = {
            'request_vote': MessageType.REQUEST_VOTE.value,
            'vote_response': MessageType.VOTE_RESPONSE.value,
            'append_entries': MessageType.APPEND_ENTRIES.value,
            'append_entries_response': MessageType.APPEND_ENTRIES_RESPONSE.value
        }
        
        message = Message(
            msg_type=type_mapping.get(msg_type, msg_type),
            sender_id=self.node_id,
            receiver_id=target_node,
            term=payload.get('term', self.raft.current_term),
            payload=payload
        )
        
        await self.message_passing.send_message(target_node, message)
        self.metrics.increment_counter(f'raft_messages_sent_{msg_type}')
    
    async def _on_raft_state_change(self, new_state: RaftState):
        """Handle Raft state change"""
        logger.info(f"Raft state changed to: {new_state.value}")
        self.metrics.increment_counter(f'raft_state_change_{new_state.value}')
        
        if new_state == RaftState.LEADER:
            logger.info(f"Node {self.node_id} is now the LEADER")
            self.metrics.set_gauge('is_leader', 1)
        else:
            self.metrics.set_gauge('is_leader', 0)
    
    async def _on_log_commit(self, log_entry):
        """Handle committed log entry"""
        logger.info(f"Log entry committed: {log_entry.command}")
        self.metrics.increment_counter('log_entries_committed')
        
        # Subclasses can override this to handle specific commands
        await self.process_committed_entry(log_entry)
    
    async def process_committed_entry(self, log_entry):
        """Process a committed log entry (to be overridden by subclasses)"""
        pass
    
    # Failure detector callbacks
    def _on_node_failure(self, node_id: str):
        """Handle node failure"""
        logger.warning(f"Node failed: {node_id}")
        self.metrics.increment_counter('node_failures_detected')
    
    def _on_node_recovery(self, node_id: str):
        """Handle node recovery"""
        logger.info(f"Node recovered: {node_id}")
        self.metrics.increment_counter('node_recoveries_detected')
    
    # Public API
    async def submit_command(self, command: str, data: Any = None) -> bool:
        """Submit a command to be replicated (redirects to leader if not leader)"""
        if self.raft.is_leader():
            logger.info(f"Submitting command to Raft: {command}")
            result = await self.raft.append_log(command, data)
            logger.info(f"Raft append_log result: {result}")
            return result
        else:
            logger.info("Not leader, cannot submit command")
            return False
    
    def is_leader(self) -> bool:
        """Check if this node is the leader"""
        return self.raft.is_leader()
    
    def get_status(self) -> dict:
        """Get comprehensive node status"""
        return {
            'node_id': self.node_id,
            'host': self.host,
            'port': self.port,
            'running': self.running,
            'raft': self.raft.get_status(),
            'connected_nodes': self.message_passing.get_connected_nodes(),
            'cluster_health': self.failure_detector.get_cluster_health(),
            'metrics': self.metrics.get_all_metrics()
        }


async def main():
    """Main entry point for running a node"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run a distributed node')
    parser.add_argument('--node-id', required=True, help='Node ID')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    parser.add_argument('--cluster-nodes', required=True, help='Comma-separated list of cluster nodes (id:host:port)')
    
    args = parser.parse_args()
    
    cluster_nodes = args.cluster_nodes.split(',')
    
    node = BaseNode(
        node_id=args.node_id,
        host=args.host,
        port=args.port,
        cluster_nodes=cluster_nodes
    )
    
    try:
        await node.start()
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
            # Print status every 10 seconds
            if int(asyncio.get_event_loop().time()) % 10 == 0:
                status = node.get_status()
                logger.info(f"Status: {status['raft']}")
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await node.stop()


if __name__ == '__main__':
    asyncio.run(main())
