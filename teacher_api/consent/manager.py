"""
Consent management and enforcement.

All student data access must pass through consent gates.
Default policy: DENY unless explicitly granted.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class ConsentScope(Enum):
    """Types of data that can be consented to."""
    
    BASIC_INFO = "basic_info"  # Name, grade level
    ACADEMIC_PATTERNS = "academic_patterns"  # Learning patterns (anonymized)
    CLASSROOM_SIGNALS = "classroom_signals"  # Aggregated classroom data
    COLLABORATION = "collaboration"  # Cross-teacher coordination
    SUPPORT_ROUTING = "support_routing"  # Referrals to counselors


class ConsentStatus(Enum):
    """Status of a consent grant."""
    
    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"


@dataclass
class ConsentGrant:
    """A record of consent."""
    
    student_id: str
    scope: ConsentScope
    status: ConsentStatus
    granted_at: datetime
    granted_by: str  # Parent/guardian ID
    expires_at: Optional[datetime]
    withdrawn_at: Optional[datetime] = None


class ConsentManager:
    """Manages student data consent."""

    def __init__(self) -> None:
        """Initialize consent manager."""
        self._grants: Dict[str, List[ConsentGrant]] = {}

    def grant_consent(
        self,
        student_id: str,
        scope: ConsentScope,
        granted_by: str,
        expires_at: Optional[datetime] = None,
    ) -> ConsentGrant:
        """
        Record a consent grant.
        
        Args:
            student_id: Student identifier
            scope: What is being consented to
            granted_by: Who granted consent (parent/guardian)
            expires_at: Optional expiration
            
        Returns:
            The consent grant record
        """
        grant = ConsentGrant(
            student_id=student_id,
            scope=scope,
            status=ConsentStatus.GRANTED,
            granted_at=datetime.utcnow(),
            granted_by=granted_by,
            expires_at=expires_at,
        )
        
        if student_id not in self._grants:
            self._grants[student_id] = []
        
        self._grants[student_id].append(grant)
        return grant

    def check_consent(self, student_id: str, scope: ConsentScope) -> bool:
        """
        Check if valid consent exists for a scope.
        
        Args:
            student_id: Student identifier
            scope: Requested scope
            
        Returns:
            True if valid consent exists
        """
        if student_id not in self._grants:
            return False
        
        now = datetime.utcnow()
        
        for grant in self._grants[student_id]:
            if grant.scope != scope:
                continue
            
            if grant.status != ConsentStatus.GRANTED:
                continue
            
            if grant.expires_at and grant.expires_at < now:
                grant.status = ConsentStatus.EXPIRED
                continue
            
            return True
        
        return False

    def withdraw_consent(
        self,
        student_id: str,
        scope: ConsentScope,
    ) -> bool:
        """
        Withdraw consent for a scope.
        
        Args:
            student_id: Student identifier
            scope: Scope to withdraw
            
        Returns:
            True if consent was found and withdrawn
        """
        if student_id not in self._grants:
            return False
        
        withdrawn = False
        for grant in self._grants[student_id]:
            if grant.scope == scope and grant.status == ConsentStatus.GRANTED:
                grant.status = ConsentStatus.WITHDRAWN
                grant.withdrawn_at = datetime.utcnow()
                withdrawn = True
        
        return withdrawn

    def get_consents(self, student_id: str) -> List[ConsentGrant]:
        """
        Get all consent grants for a student.
        
        Args:
            student_id: Student identifier
            
        Returns:
            List of consent grants
        """
        return self._grants.get(student_id, []).copy()

    def require_consent(self, student_id: str, scope: ConsentScope) -> None:
        """
        Enforce consent requirement.
        
        Args:
            student_id: Student identifier
            scope: Required scope
            
        Raises:
            PermissionError: If consent not granted
        """
        if not self.check_consent(student_id, scope):
            raise PermissionError(
                f"Consent required: {scope.value} for student {student_id}. "
                "Access denied by default."
            )
