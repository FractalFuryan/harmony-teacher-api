"""
Audit logging with cryptographic chaining.

Each log entry is hashed and linked to the previous entry,
creating a tamper-evident chain.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
from hashlib import sha256
import json


@dataclass
class AuditEntry:
    """A single audit log entry."""
    
    timestamp: datetime
    actor: str  # Who performed the action
    action: str  # What was done
    resource: str  # What was affected
    details: Dict[str, Any]
    previous_hash: str
    entry_hash: str = field(init=False)

    def __post_init__(self) -> None:
        """Calculate the hash of this entry."""
        self.entry_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute SHA-256 hash of entry content."""
        content = {
            'timestamp': self.timestamp.isoformat(),
            'actor': self.actor,
            'action': self.action,
            'resource': self.resource,
            'details': self.details,
            'previous_hash': self.previous_hash,
        }
        content_str = json.dumps(content, sort_keys=True)
        return sha256(content_str.encode('utf-8')).hexdigest()

    def verify(self) -> bool:
        """Verify the integrity of this entry."""
        return self.entry_hash == self._compute_hash()


class AuditLog:
    """Tamper-evident audit log with cryptographic chaining."""

    def __init__(self) -> None:
        """Initialize the audit log."""
        self._entries: List[AuditEntry] = []
        self._genesis_hash = sha256(b"HARMONY_TEACHER_API_GENESIS").hexdigest()

    def log(
        self,
        actor: str,
        action: str,
        resource: str,
        details: Dict[str, Any] | None = None,
    ) -> AuditEntry:
        """
        Add a new entry to the audit log.
        
        Args:
            actor: Identity of the actor (user ID, service name, etc.)
            action: Action performed (e.g., "read", "update", "delete")
            resource: Resource affected (e.g., "lesson_plan:123")
            details: Additional context
            
        Returns:
            The created audit entry
        """
        previous_hash = (
            self._entries[-1].entry_hash if self._entries else self._genesis_hash
        )
        
        entry = AuditEntry(
            timestamp=datetime.utcnow(),
            actor=actor,
            action=action,
            resource=resource,
            details=details or {},
            previous_hash=previous_hash,
        )
        
        self._entries.append(entry)
        return entry

    def verify_chain(self) -> bool:
        """
        Verify the integrity of the entire audit chain.
        
        Returns:
            True if the chain is intact, False if tampering detected
        """
        if not self._entries:
            return True
        
        # Verify first entry links to genesis
        if self._entries[0].previous_hash != self._genesis_hash:
            return False
        
        # Verify each entry
        for i, entry in enumerate(self._entries):
            if not entry.verify():
                return False
            
            # Verify chain linkage
            if i > 0 and entry.previous_hash != self._entries[i - 1].entry_hash:
                return False
        
        return True

    def get_entries(
        self,
        actor: str | None = None,
        resource: str | None = None,
        action: str | None = None,
    ) -> List[AuditEntry]:
        """
        Query audit entries with filters.
        
        Args:
            actor: Filter by actor
            resource: Filter by resource
            action: Filter by action
            
        Returns:
            Matching audit entries
        """
        results = self._entries
        
        if actor:
            results = [e for e in results if e.actor == actor]
        if resource:
            results = [e for e in results if e.resource == resource]
        if action:
            results = [e for e in results if e.action == action]
        
        return results

    def get_all_entries(self) -> List[AuditEntry]:
        """Get all audit entries."""
        return self._entries.copy()
