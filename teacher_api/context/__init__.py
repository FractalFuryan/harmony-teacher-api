"""
Context memory with classroom-scoped retention.

Adapted from Tutor API with key differences:
- Scoped to classrooms, not individuals
- Shorter retention windows
- No longitudinal student identity persistence
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict


@dataclass
class ContextEntry:
    """A single context memory entry."""
    
    entry_id: str
    scope: str  # "classroom:ID" not "student:ID"
    context_type: str
    data: Dict[str, Any]
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None


class ContextMemory:
    """Manages ephemeral classroom-scoped context."""

    def __init__(self, default_retention_days: int = 30) -> None:
        """
        Initialize context memory.
        
        Args:
            default_retention_days: Default retention period (max 90 days)
        """
        if default_retention_days > 90:
            raise ValueError("Maximum retention is 90 days for privacy")
        
        self.default_retention_days = default_retention_days
        self._entries: Dict[str, ContextEntry] = {}
        self._scope_index: Dict[str, List[str]] = defaultdict(list)

    def store(
        self,
        scope: str,
        context_type: str,
        data: Dict[str, Any],
        retention_days: Optional[int] = None,
    ) -> str:
        """
        Store context data.
        
        Args:
            scope: Scope identifier (e.g., "classroom:5th_math")
            context_type: Type of context
            data: Context data
            retention_days: Custom retention period
            
        Returns:
            Entry ID
        """
        retention = retention_days or self.default_retention_days
        if retention > 90:
            raise ValueError("Maximum retention is 90 days")
        
        entry_id = f"{scope}:{context_type}:{datetime.utcnow().timestamp()}"
        
        entry = ContextEntry(
            entry_id=entry_id,
            scope=scope,
            context_type=context_type,
            data=data,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=retention),
        )
        
        self._entries[entry_id] = entry
        self._scope_index[scope].append(entry_id)
        
        return entry_id

    def retrieve(
        self,
        scope: str,
        context_type: Optional[str] = None,
    ) -> List[ContextEntry]:
        """
        Retrieve context entries for a scope.
        
        Args:
            scope: Scope to retrieve
            context_type: Optional filter by type
            
        Returns:
            List of context entries
        """
        self._cleanup_expired()
        
        entry_ids = self._scope_index.get(scope, [])
        entries = []
        
        for entry_id in entry_ids:
            if entry_id not in self._entries:
                continue
            
            entry = self._entries[entry_id]
            
            if context_type and entry.context_type != context_type:
                continue
            
            # Update access tracking
            entry.access_count += 1
            entry.last_accessed = datetime.utcnow()
            
            entries.append(entry)
        
        return entries

    def delete(self, entry_id: str) -> bool:
        """
        Delete a context entry.
        
        Args:
            entry_id: Entry to delete
            
        Returns:
            True if deleted, False if not found
        """
        if entry_id not in self._entries:
            return False
        
        entry = self._entries[entry_id]
        self._scope_index[entry.scope].remove(entry_id)
        del self._entries[entry_id]
        
        return True

    def delete_scope(self, scope: str) -> int:
        """
        Delete all entries for a scope.
        
        Args:
            scope: Scope to delete
            
        Returns:
            Number of entries deleted
        """
        entry_ids = self._scope_index.get(scope, []).copy()
        
        for entry_id in entry_ids:
            self.delete(entry_id)
        
        return len(entry_ids)

    def _cleanup_expired(self) -> int:
        """
        Remove expired entries.
        
        Returns:
            Number of entries cleaned up
        """
        now = datetime.utcnow()
        expired_ids = [
            entry_id
            for entry_id, entry in self._entries.items()
            if entry.expires_at < now
        ]
        
        for entry_id in expired_ids:
            self.delete(entry_id)
        
        return len(expired_ids)

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        self._cleanup_expired()
        
        return {
            "total_entries": len(self._entries),
            "scopes": len(self._scope_index),
            "oldest_entry": min(
                (e.created_at for e in self._entries.values()),
                default=None
            ),
            "newest_entry": max(
                (e.created_at for e in self._entries.values()),
                default=None
            ),
        }
