"""
Raft Consensus Algorithm Implementation
Implements leader election and log replication
"""

import asyncio
import random
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger(__name__)


class RaftState(Enum):
    """Raft node states"""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


@dataclass
class LogEntry:
    """Raft log entry"""
    term: int
    index: int
    command: str
    data: Any = None
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> dict:
        return {
            'term': self.term,
            'index': self.index,
            'command': self.command,
            'data': self.data,
            'timestamp': self.timestamp
        }


class RaftNode:
    """
    Implementation of Raft Consensus Algorithm
    Handles leader election and log replication
    """
    
    def __init__(
        self,
        node_id: str,
        cluster_nodes: List[str],
        election_timeout_min: int = 1500,  # 1.5s min
        election_timeout_max: int = 3000,  # 3s max
        heartbeat_interval: int = 500      # 500ms
    ):
        self.node_id = node_id
        # Filter out this node from cluster - handle both "nodeX" and "nodeX:host:port" formats
        self.cluster_nodes = [n for n in cluster_nodes if not n.startswith(f"{node_id}:") and n != node_id]
        self.election_timeout_min = election_timeout_min
        self.election_timeout_max = election_timeout_max
        self.heartbeat_interval = heartbeat_interval
        
        # Persistent state
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = []
        
        # Volatile state
        self.commit_index = -1
        self.last_applied = -1
        self.state = RaftState.FOLLOWER
        
        # Leader state
        self.next_index: Dict[str, int] = {}
        self.match_index: Dict[str, int] = {}
        
        # Timing
        self.last_heartbeat = time.time()
        self.election_timeout = self._random_election_timeout()
        
        # Tasks
        self._running = False
        self._election_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        
        # Callbacks
        self.message_sender = None
        self.state_change_callback = None
        self.commit_callback = None
        
        # Metrics
        self.votes_received: set = set()
        self.election_count = 0
    
    def _random_election_timeout(self) -> float:
        """Generate random election timeout with exponential backoff based on failed elections"""
        base_timeout = random.randint(self.election_timeout_min, self.election_timeout_max)
        if hasattr(self, 'election_count'):
            # Add exponential backoff based on election attempts
            backoff = min(3, self.election_count / 2)  # Cap at 3x
            base_timeout = int(base_timeout * (1 + backoff))
        return base_timeout / 1000.0
    
    async def start(self):
        """Start Raft node"""
        self._running = True
        self._election_task = asyncio.create_task(self._election_timer())
        logger.info(f"Raft node {self.node_id} started as {self.state.value}")
    
    async def stop(self):
        """Stop Raft node"""
        self._running = False
        
        if self._election_task:
            self._election_task.cancel()
            try:
                await self._election_task
            except asyncio.CancelledError:
                pass
        
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"Raft node {self.node_id} stopped")
    
    def set_message_sender(self, sender):
        """Set message sender callback"""
        self.message_sender = sender
    
    def set_state_change_callback(self, callback):
        """Set callback for state changes"""
        self.state_change_callback = callback
    
    def set_commit_callback(self, callback):
        """Set callback for committed entries"""
        self.commit_callback = callback
    
    async def _election_timer(self):
        """Election timer - triggers election if no heartbeat"""
        while self._running:
            try:
                await asyncio.sleep(0.1)  # Check every 100ms
                
                if self.state == RaftState.LEADER:
                    continue
                
                time_since_heartbeat = time.time() - self.last_heartbeat
                
                if time_since_heartbeat > self.election_timeout:
                    logger.info(f"Election timeout ({time_since_heartbeat:.2f}s > {self.election_timeout:.2f}s)")
                    await self._start_election()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in election timer: {e}")
    
    async def _start_election(self):
        """Start leader election"""
        # Don't start election if already leader
        if self.state == RaftState.LEADER:
            return

        # Safety check - only followers and candidates can start election
        if self.state not in [RaftState.FOLLOWER, RaftState.CANDIDATE]:
            return
            
        self.election_count += 1
        logger.info(f"Node {self.node_id} starting election (term {self.current_term + 1})")
        
        # Reset election timer with new timeout
        self.election_timeout = self._random_election_timeout()
        self.last_heartbeat = time.time()
        
        # Become candidate
        await self._transition_to_candidate()
        
        # Vote for self
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}
        
        # Initialize total nodes including self
        total_nodes = len(self.cluster_nodes) + 1
        
        # Check if already have majority (for standalone nodes)
        majority = (total_nodes // 2) + 1
        if len(self.votes_received) >= majority:
            logger.info(f"Node {self.node_id} won election immediately (standalone with {len(self.votes_received)} votes)")
            await self._transition_to_leader()
            return

        # Request votes from all other nodes in parallel
        vote_tasks = []
        for node in self.cluster_nodes:
            if self.message_sender:
                task = asyncio.create_task(
                    self.message_sender(node, {
                        'type': 'request_vote',
                        'term': self.current_term,
                        'candidate_id': self.node_id,
                        'last_log_index': len(self.log) - 1 if self.log else -1,
                        'last_log_term': self.log[-1].term if self.log else 0
                    })
                )
                vote_tasks.append(task)
                
        # Wait for responses with timeout
        try:
            await asyncio.wait_for(asyncio.gather(*vote_tasks, return_exceptions=True), timeout=1.0)
        except asyncio.TimeoutError:
            logger.warning(f"Vote request timeout for node {self.node_id} (term {self.current_term})")
        except Exception as e:
            logger.error(f"Error requesting votes: {e}")
            
        # Double check we have majority after gathering votes
        if len(self.votes_received) >= majority:
            logger.info(f"Node {self.node_id} confirmed majority with {len(self.votes_received)} votes")
            await self._transition_to_leader()
    
    async def handle_request_vote(self, message: dict):
        """Handle RequestVote RPC"""
        term = message['term']
        candidate_id = message['candidate_id']
        last_log_index = message['last_log_index']
        last_log_term = message['last_log_term']
        
        logger.debug(f"Node {self.node_id} received vote request from {candidate_id} (term {term})")
        
        # Reject immediately if lower term
        if term < self.current_term:
            logger.debug(f"Node {self.node_id} rejecting vote - lower term {term} < {self.current_term}")
            if self.message_sender:
                await self.message_sender(candidate_id, {
                    'type': 'vote_response',
                    'term': self.current_term,
                    'vote_granted': False
                })
            return
        
        # Update term if higher and become follower
        if term > self.current_term:
            logger.info(f"Node {self.node_id} updating term {self.current_term} -> {term}")
            await self._transition_to_follower(term)
        
        # Determine if we should grant vote
        vote_granted = False
        
        if self.voted_for is not None and self.voted_for != candidate_id:
            logger.debug(f"Node {self.node_id} rejecting vote - already voted for {self.voted_for}")
        else:
            # Check if candidate's log is at least as up-to-date as ours
            our_last_log_term = self.log[-1].term if self.log else 0
            our_last_log_index = len(self.log) - 1 if self.log else -1
            
            log_ok = (last_log_term > our_last_log_term) or \
                     (last_log_term == our_last_log_term and last_log_index >= our_last_log_index)
            
            if not log_ok:
                logger.debug(f"Node {self.node_id} rejecting vote - candidate log not up to date " + 
                           f"(last_term:{last_log_term} vs {our_last_log_term}, " +
                           f"last_idx:{last_log_index} vs {our_last_log_index})")
            else:
                # All conditions met - grant vote
                vote_granted = True
                self.voted_for = candidate_id
                logger.info(f"Node {self.node_id} granting vote to {candidate_id} (term {term})")
                
                # Reset election timer since we granted vote
                self.last_heartbeat = time.time()
                
                # Step down if we were leader or candidate
                if self.state != RaftState.FOLLOWER:
                    await self._transition_to_follower(term)
        
        # Send response
        if self.message_sender:
            response = {
                'type': 'vote_response',
                'term': self.current_term,
                'vote_granted': vote_granted,
                'sender_id': self.node_id  # Include sender for tracking
            }
            await self.message_sender(candidate_id, response)
            
        logger.debug(f"Vote request from {candidate_id}: {'granted' if vote_granted else 'rejected'} " +
                   f"(term:{term}, current_term:{self.current_term})")
    
    async def handle_vote_response(self, message: dict):
        """Handle RequestVote response"""
        term = message['term']
        vote_granted = message.get('vote_granted', False)
        sender = message.get('sender_id')

        logger.debug(f"Node {self.node_id} received vote response from {sender} " + 
                   f"(granted:{vote_granted}, term:{term})")

        # Validate sender
        if not sender:
            logger.warning("Received vote response without sender ID")
            return

        # Only process responses if still a candidate
        if self.state != RaftState.CANDIDATE:
            logger.debug(f"Ignoring vote from {sender} - no longer a candidate")
            return
            
        # Ignore old term responses
        if term < self.current_term:
            logger.debug(f"Ignoring vote from {sender} - old term {term} < {self.current_term}")
            return
            
        # Step down if response has higher term
        if term > self.current_term:
            logger.info(f"Discovered higher term from {sender} ({term} > {self.current_term})")
            await self._transition_to_follower(term)
            return
        
        # Process vote for current term
        if vote_granted and term == self.current_term:
            # Track vote
            self.votes_received.add(sender)
            logger.info(f"Received vote from {sender} ({len(self.votes_received)} total votes)")
            
            # Check for majority
            total_nodes = len(self.cluster_nodes) + 1  # Include self
            majority = (total_nodes // 2) + 1
            
            logger.debug(f"Have {len(self.votes_received)}/{total_nodes} votes, need {majority}")
            
            if len(self.votes_received) >= majority:
                logger.info(f"Node {self.node_id} won election with {len(self.votes_received)} votes")
                await self._transition_to_leader()
    
    async def _transition_to_candidate(self):
        """Transition to candidate state"""
        self.state = RaftState.CANDIDATE
        self.current_term += 1
        self.election_timeout = self._random_election_timeout()
        self.last_heartbeat = time.time()
        
        logger.info(f"Node {self.node_id} became CANDIDATE (term {self.current_term})")
        
        if self.state_change_callback:
            await self._safe_callback(self.state_change_callback, RaftState.CANDIDATE)
    
    async def _transition_to_follower(self, new_term=None):
        """
        Transition to follower state
        
        Args:
            new_term: Optional new term to update to
        """
        # Cancel heartbeat task if we were leader
        if self.state == RaftState.LEADER and self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
        
        # Update term if provided
        if new_term is not None:
            logger.info(f"Node {self.node_id} updating term {self.current_term} -> {new_term}")
            self.current_term = new_term
            self.voted_for = None  # Clear vote when term changes
        
        # Transition to follower
        self.state = RaftState.FOLLOWER
        self.election_timeout = self._random_election_timeout()
        
        logger.info(f"Node {self.node_id} became FOLLOWER (term {self.current_term})")
        
        if self.state_change_callback:
            await self._safe_callback(self.state_change_callback, RaftState.FOLLOWER)
    
    async def _transition_to_leader(self):
        """Transition to leader state"""
        # Safety checks
        if self.state != RaftState.CANDIDATE:
            logger.warning(f"Node {self.node_id} attempting to become leader while not a candidate")
            return
            
        # Double check we're still in a good state
        total_nodes = len(self.cluster_nodes) + 1
        majority = (total_nodes // 2) + 1
        if len(self.votes_received) < majority:
            logger.warning(f"Node {self.node_id} cannot become leader - lost majority " +
                         f"({len(self.votes_received)}/{total_nodes} votes)")
            return
            
        # Transition to leader
        self.state = RaftState.LEADER
        self.election_count = 0  # Reset election count
        self.voted_for = None  # Clear vote
        
        # Initialize leader state
        last_log_index = len(self.log) - 1 if self.log else -1
        for node in self.cluster_nodes:
            self.next_index[node] = last_log_index + 1
            self.match_index[node] = 0
            
        logger.info(f"Node {self.node_id} became LEADER for term {self.current_term}")
        
        # Cancel any existing heartbeat task
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            
        # Send immediate heartbeat to establish authority
        heartbeat_tasks = []
        for node in self.cluster_nodes:
            task = asyncio.create_task(self._send_append_entries(node))
            heartbeat_tasks.append(task)
            
        # Wait for initial heartbeats with timeout
        try:
            await asyncio.wait_for(asyncio.gather(*heartbeat_tasks), timeout=0.5)
        except asyncio.TimeoutError:
            logger.warning("Initial heartbeat timeout - proceeding anyway")
        except Exception as e:
            logger.error(f"Error sending initial heartbeats: {e}")
            
        # Start periodic heartbeat task
        self._heartbeat_task = asyncio.create_task(self._send_heartbeats())
        
        # Notify about state change
        if self.state_change_callback:
            await self._safe_callback(self.state_change_callback, RaftState.LEADER)
    
    async def _send_heartbeats(self):
        """Send periodic heartbeats as leader"""
        while self._running and self.state == RaftState.LEADER:
            try:
                # Send AppendEntries to all followers
                for node in self.cluster_nodes:
                    await self._send_append_entries(node)
                
                await asyncio.sleep(self.heartbeat_interval / 1000.0)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error sending heartbeats: {e}")
    
    async def _send_append_entries(self, node: str):
        """Send AppendEntries RPC to a follower"""
        if not self.message_sender:
            return
        
        prev_log_index = self.next_index.get(node, 0) - 1
        prev_log_term = self.log[prev_log_index].term if prev_log_index >= 0 and prev_log_index < len(self.log) else 0
        
        # Get entries to send
        entries = []
        next_idx = self.next_index.get(node, 0)
        if next_idx < len(self.log):
            entries = [e.to_dict() for e in self.log[next_idx:]]
        
        await self.message_sender(node, {
            'type': 'append_entries',
            'term': self.current_term,
            'leader_id': self.node_id,
            'prev_log_index': prev_log_index,
            'prev_log_term': prev_log_term,
            'entries': entries,
            'leader_commit': self.commit_index
        })
    
    async def handle_append_entries(self, message: dict):
        """Handle AppendEntries RPC"""
        term = message['term']
        leader_id = message['leader_id']
        prev_log_index = message['prev_log_index']
        prev_log_term = message['prev_log_term']
        entries = message['entries']
        leader_commit = message['leader_commit']
        
        # Update term if necessary
        if term > self.current_term:
            await self._update_term(term)
        
        # Reject if term is old
        if term < self.current_term:
            # Send failure response
            if self.message_sender:
                await self.message_sender(leader_id, {
                    'type': 'append_entries_response',
                    'term': self.current_term,
                    'success': False,
                    'match_index': 0
                })
            return
        
        # Reset election timer (we have a valid leader)
        self.last_heartbeat = time.time()
        
        # Become follower if we're not (and term is valid)
        if self.state != RaftState.FOLLOWER:
            await self._transition_to_follower()
        
        success = False
        
        if term < self.current_term:
            success = False
        elif prev_log_index >= 0 and \
             (prev_log_index >= len(self.log) or self.log[prev_log_index].term != prev_log_term):
            # Log doesn't contain entry at prev_log_index with matching term
            success = False
        else:
            # Append entries
            success = True
            
            # Delete conflicting entries and append new ones
            if entries:
                insert_index = prev_log_index + 1
                for i, entry_dict in enumerate(entries):
                    entry = LogEntry(**entry_dict)
                    actual_index = insert_index + i
                    
                    if actual_index < len(self.log):
                        if self.log[actual_index].term != entry.term:
                            # Delete this and all following entries
                            self.log = self.log[:actual_index]
                            self.log.append(entry)
                    else:
                        self.log.append(entry)
            
            # Update commit index
            if leader_commit > self.commit_index:
                self.commit_index = min(leader_commit, len(self.log) - 1 if self.log else 0)
                await self._apply_committed_entries()
        
        # Send response
        if self.message_sender:
            await self.message_sender(leader_id, {
                'type': 'append_entries_response',
                'term': self.current_term,
                'success': success,
                'match_index': len(self.log) - 1 if success and self.log else 0
            })
    
    async def handle_append_entries_response(self, message: dict):
        """Handle AppendEntries response"""
        if self.state != RaftState.LEADER:
            return
        
        term = message['term']
        success = message['success']
        sender = message.get('sender_id')
        match_index = message.get('match_index', 0)
        
        # Update term if necessary
        if term > self.current_term:
            await self._update_term(term)
            return
        
        if success:
            # Update next_index and match_index
            self.next_index[sender] = match_index + 1
            self.match_index[sender] = match_index
            
            # Check if we can commit
            await self._update_commit_index()
        else:
            # Decrement next_index and retry
            self.next_index[sender] = max(0, self.next_index.get(sender, 1) - 1)
    
    async def _update_commit_index(self):
        """Update commit index based on majority"""
        if self.state != RaftState.LEADER:
            return
        
        # Find highest N where majority has match_index >= N
        for n in range(len(self.log) - 1, self.commit_index, -1):
            if self.log[n].term == self.current_term:
                # Count nodes with match_index >= n
                count = 1  # Leader itself
                for node in self.cluster_nodes:
                    if self.match_index.get(node, 0) >= n:
                        count += 1
                
                majority = (len(self.cluster_nodes) + 1) // 2 + 1
                if count >= majority:
                    self.commit_index = n
                    await self._apply_committed_entries()
                    break
    
    async def _apply_committed_entries(self):
        """Apply committed log entries"""
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            entry = self.log[self.last_applied]
            
            logger.debug(f"Applying log entry {self.last_applied}: {entry.command}")
            
            if self.commit_callback:
                await self._safe_callback(self.commit_callback, entry)
    
    async def _update_term(self, new_term: int):
        """Update term and become follower"""
        self.current_term = new_term
        self.voted_for = None
        await self._transition_to_follower()
    
    async def append_log(self, command: str, data: Any = None) -> bool:
        """Append a new log entry (only leader)"""
        if self.state != RaftState.LEADER:
            return False
        
        entry = LogEntry(
            term=self.current_term,
            index=len(self.log),
            command=command,
            data=data
        )
        
        self.log.append(entry)
        logger.debug(f"Leader appended log entry {entry.index}: {command}")
        
        # Immediately replicate to followers
        for node in self.cluster_nodes:
            await self._send_append_entries(node)
        
        # For standalone nodes (no followers), immediately commit
        if len(self.cluster_nodes) == 0:
            logger.debug(f"Standalone node, immediately committing entry {entry.index}")
            self.commit_index = entry.index
            await self._apply_committed_entries()
        
        return True
    
    async def _safe_callback(self, callback, *args, **kwargs):
        """Safely execute callback"""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in callback: {e}")
    
    def is_leader(self) -> bool:
        """Check if this node is the leader"""
        return self.state == RaftState.LEADER
    
    def get_leader_id(self) -> Optional[str]:
        """Get current leader ID (if known)"""
        if self.state == RaftState.LEADER:
            return self.node_id
        return None
    
    def get_status(self) -> dict:
        """Get node status"""
        return {
            'node_id': self.node_id,
            'state': self.state.value,
            'term': self.current_term,
            'log_length': len(self.log),
            'commit_index': self.commit_index,
            'last_applied': self.last_applied,
            'voted_for': self.voted_for,
            'votes_received': len(self.votes_received) if hasattr(self, 'votes_received') else 0,
            'election_count': self.election_count
        }
