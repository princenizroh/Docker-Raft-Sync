"""
Message Passing Module
Handles inter-node communication using async networking
"""

import asyncio
import json
import logging
import time
from typing import Dict, Callable, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Types of messages in the system"""
    # Raft messages
    REQUEST_VOTE = "request_vote"
    VOTE_RESPONSE = "vote_response"
    APPEND_ENTRIES = "append_entries"
    APPEND_ENTRIES_RESPONSE = "append_entries_response"
    
    # Lock messages
    LOCK_REQUEST = "lock_request"
    LOCK_RESPONSE = "lock_response"
    LOCK_RELEASE = "lock_release"
    DEADLOCK_DETECT = "deadlock_detect"
    
    # Queue messages
    ENQUEUE = "enqueue"
    DEQUEUE = "dequeue"
    QUEUE_SYNC = "queue_sync"
    
    # Cache messages
    CACHE_GET = "cache_get"
    CACHE_PUT = "cache_put"
    CACHE_INVALIDATE = "cache_invalidate"
    CACHE_UPDATE = "cache_update"
    
    # General
    HEARTBEAT = "heartbeat"
    PING = "ping"
    PONG = "pong"
    ERROR = "error"


@dataclass
class Message:
    """Base message structure"""
    msg_type: str
    sender_id: str
    receiver_id: str
    term: int = 0
    payload: Dict[str, Any] = None
    timestamp: float = None
    message_id: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.message_id is None:
            self.message_id = f"{self.sender_id}_{self.timestamp}_{id(self)}"
        if self.payload is None:
            self.payload = {}
    
    def to_json(self) -> str:
        """Serialize message to JSON"""
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, data: str) -> 'Message':
        """Deserialize message from JSON"""
        return cls(**json.loads(data))


class MessagePassing:
    """
    Handles message passing between nodes using asyncio
    """
    
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.server: Optional[asyncio.Server] = None
        self.connections: Dict[str, asyncio.StreamWriter] = {}
        self.handlers: Dict[str, Callable] = {}
        self.running = False
        self._message_queue = asyncio.Queue()
        self._lock = asyncio.Lock()
    
    async def start(self):
        """Start message passing server"""
        self.running = True
        self.server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port
        )
        logger.info(f"Message passing server started on {self.host}:{self.port}")
        
        # Start message processor
        asyncio.create_task(self._process_messages())
    
    async def stop(self):
        """Stop message passing server"""
        self.running = False
        
        # Close all connections - Fix: Create a snapshot to avoid mutation during iteration
        for writer in list(self.connections.values()):
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass  # Ignore errors during cleanup
        
        # Close server
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        logger.info("Message passing server stopped")
    
    def register_handler(self, msg_type: str, handler: Callable):
        """Register a message handler"""
        self.handlers[msg_type] = handler
        logger.debug(f"Registered handler for {msg_type}")
    
    async def send_message(self, target_node: str, message: Message) -> bool:
        """Send a message to a target node"""
        try:
            # Get or create connection
            writer = await self._get_connection(target_node)
            if not writer:
                logger.error(f"Failed to connect to {target_node}")
                return False
            
            # Send message
            data = message.to_json() + "\n"
            writer.write(data.encode())
            await writer.drain()
            
            logger.debug(f"Sent {message.msg_type} to {target_node}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message to {target_node}: {e}")
            # Remove failed connection
            if target_node in self.connections:
                del self.connections[target_node]
            return False
    
    async def broadcast_message(self, message: Message, exclude_self: bool = True):
        """Broadcast a message to all known nodes"""
        tasks = []
        for node_id in self.connections.keys():
            if exclude_self and node_id == self.node_id:
                continue
            tasks.append(self.send_message(node_id, message))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            success_count = sum(1 for r in results if r is True)
            logger.debug(f"Broadcast sent to {success_count}/{len(tasks)} nodes")
    
    async def _get_connection(self, target_node: str) -> Optional[asyncio.StreamWriter]:
        """Get or create connection to target node"""
        async with self._lock:
            if target_node in self.connections:
                return self.connections[target_node]
            
            # Parse target node address
            # Expected format: "node-id:host:port"
            try:
                _, host, port = target_node.split(':')
                port = int(port)
                
                reader, writer = await asyncio.open_connection(host, port)
                self.connections[target_node] = writer
                
                # Start listening to this connection
                asyncio.create_task(self._handle_connection(reader, target_node))
                
                logger.info(f"Connected to {target_node}")
                return writer
                
            except Exception as e:
                logger.error(f"Failed to connect to {target_node}: {e}")
                return None
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connection"""
        addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {addr}")
        
        try:
            # Read first message to identify the node
            data = await reader.readline()
            if data:
                message = Message.from_json(data.decode().strip())
                sender_id = message.sender_id
                
                async with self._lock:
                    self.connections[sender_id] = writer
                
                # Process the first message
                await self._message_queue.put(message)
                
                # Continue handling this connection
                await self._handle_connection(reader, sender_id)
                
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def _handle_connection(self, reader: asyncio.StreamReader, node_id: str):
        """Handle messages from a specific connection"""
        try:
            while self.running:
                data = await reader.readline()
                if not data:
                    break
                
                try:
                    message = Message.from_json(data.decode().strip())
                    await self._message_queue.put(message)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode message from {node_id}: {e}")
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in connection handler for {node_id}: {e}")
        finally:
            # Remove connection
            async with self._lock:
                if node_id in self.connections:
                    del self.connections[node_id]
            logger.info(f"Connection closed: {node_id}")
    
    async def _process_messages(self):
        """Process messages from the queue"""
        while self.running:
            try:
                message = await asyncio.wait_for(
                    self._message_queue.get(),
                    timeout=1.0
                )
                
                # Find and call handler
                handler = self.handlers.get(message.msg_type)
                if handler:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(message)
                        else:
                            handler(message)
                    except Exception as e:
                        logger.error(f"Error in handler for {message.msg_type}: {e}")
                else:
                    logger.warning(f"No handler for message type: {message.msg_type}")
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    def get_connected_nodes(self) -> list:
        """Get list of connected nodes"""
        return list(self.connections.keys())
    
    def is_connected(self, node_id: str) -> bool:
        """Check if connected to a specific node"""
        return node_id in self.connections
