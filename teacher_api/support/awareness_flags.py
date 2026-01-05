"""
Pattern detection for teacher awareness.

Detects deviations that may warrant teacher attention.
NEVER diagnostic, NEVER prescriptive.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional


class FlagSeverity(Enum):
    """Urgency level for teacher awareness."""
    
    INFO = "info"  # FYI only
    ATTENTION = "attention"  # May want to check in
    PRIORITY = "priority"  # Recommend check-in soon


class FlagType(Enum):
    """Types of patterns that can be flagged."""
    
    PARTICIPATION_CHANGE = "participation_change"
    PATTERN_SHIFT = "pattern_shift"
    ENGAGEMENT_DEVIATION = "engagement_deviation"
    COLLABORATION_CONCERN = "collaboration_concern"


@dataclass
class AwarenessFlag:
    """A flag for teacher awareness."""
    
    flag_id: str
    flag_type: FlagType
    severity: FlagSeverity
    description: str  # Descriptive, not diagnostic
    suggested_action: str  # "Consider..." not "Student has..."
    context: str
    detected_at: datetime
    student_id: str  # Hashed/anonymized in some contexts
    
    # Critical metadata
    is_diagnostic: bool = False  # Must always be False
    requires_teacher_judgment: bool = True  # Must always be True
    visible_to_student: bool = False  # Default: teacher-only

    def __post_init__(self) -> None:
        """Enforce safety constraints."""
        if self.is_diagnostic:
            raise ValueError("Flags cannot be diagnostic")
        if not self.requires_teacher_judgment:
            raise ValueError("Flags must require teacher judgment")


class PatternDetector:
    """Detects patterns that may warrant teacher attention."""

    def detect_participation_changes(
        self,
        student_id: str,
        recent_data: List[dict],
        baseline_data: List[dict],
    ) -> Optional[AwarenessFlag]:
        """
        Detect significant changes in participation.
        
        Args:
            student_id: Student identifier
            recent_data: Recent participation data
            baseline_data: Baseline for comparison
            
        Returns:
            Awareness flag if significant change detected, None otherwise
            
        Note:
            This is descriptive pattern detection, not diagnosis.
        """
        # Stub logic - in production, use statistical methods
        if len(recent_data) < 3:
            return None
        
        # Example: detect sustained decrease
        recent_avg = sum(d.get('participation_score', 0) for d in recent_data) / len(recent_data)
        baseline_avg = sum(d.get('participation_score', 0) for d in baseline_data) / len(baseline_data)
        
        if recent_avg < baseline_avg * 0.5:  # 50% decrease
            return AwarenessFlag(
                flag_id=f"flag_{student_id}_{datetime.utcnow().timestamp()}",
                flag_type=FlagType.PARTICIPATION_CHANGE,
                severity=FlagSeverity.ATTENTION,
                description="Participation pattern has decreased compared to baseline",
                suggested_action="Consider checking in with student about recent participation",
                context=f"Recent average: {recent_avg:.1f}, Baseline: {baseline_avg:.1f}",
                detected_at=datetime.utcnow(),
                student_id=student_id,
                is_diagnostic=False,
                requires_teacher_judgment=True,
                visible_to_student=False,
            )
        
        return None

    def detect_engagement_patterns(
        self,
        classroom_data: dict,
        timeframe_days: int = 7,
    ) -> List[AwarenessFlag]:
        """
        Detect classroom-wide engagement patterns.
        
        Args:
            classroom_data: Aggregated classroom data
            timeframe_days: Lookback period
            
        Returns:
            List of awareness flags for teacher
            
        Note:
            Operates on classroom aggregates, not individual profiles.
        """
        flags = []
        
        # Stub - in production, analyze patterns
        # This would look at classroom-level trends
        
        return flags


class SupportRouter:
    """Routes awareness to appropriate support personnel."""

    def suggest_routing(
        self,
        flag: AwarenessFlag,
        available_resources: List[str],
    ) -> dict:
        """
        Suggest appropriate support resources.
        
        Args:
            flag: The awareness flag
            available_resources: Available support personnel/resources
            
        Returns:
            Routing suggestion for teacher to review
            
        Note:
            Teacher makes final decision on all referrals.
        """
        suggestion = {
            "flag_id": flag.flag_id,
            "suggested_resource": "school_counselor",  # Stub
            "reason": "Pattern suggests emotional/social support may help",
            "urgency": flag.severity.value,
            "requires_teacher_approval": True,
            "teacher_note": "Teacher should review context before making referral",
        }
        
        return suggestion
