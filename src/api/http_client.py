"""
HTTP API Client for connecting to nodes running in Docker containers
"""

import aiohttp
import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

class HTTPAPIClient:
    """Client for connecting to nodes running in Docker containers"""
    
    def __init__(self, node_id: str, host: str, port: int, cluster_nodes: List[str]):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.cluster_nodes = cluster_nodes
        self.session: Optional[aiohttp.ClientSession] = None
        self.running = False
    
    async def start(self):
        """Start client connection"""
        self.session = aiohttp.ClientSession()
        self.running = True
        logger.info(f"Connected to Docker container {self.node_id} at {self.host}:{self.port}")
    
    async def stop(self):
        """Stop client connection"""
        if self.session:
            await self.session.close()
        self.running = False
        logger.info(f"Disconnected from Docker container {self.node_id}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get node status"""
        if not self.session:
            return {"status": "disconnected"}
            
        try:
            url = f"http://{self.host}:{self.port}/status"
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"status": "error", "code": resp.status}
        except Exception as e:
            logger.error(f"Error getting status from {self.node_id}: {e}")
            return {"status": "error", "message": str(e)}
    
    @property
    def raft(self):
        """Access to Raft properties"""
        return RaftProxy(self)


class RaftProxy:
    """Proxy class to mimic Raft node properties"""
    
    def __init__(self, client: HTTPAPIClient):
        self.client = client
        self.state = "unknown"
        self.current_term = 0