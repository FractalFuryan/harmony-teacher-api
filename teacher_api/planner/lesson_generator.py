"""
Lesson plan generation and management.

All generated plans are DRAFTS that require teacher review.
Teachers can edit, approve, or reject any generated content.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Any, Optional
from uuid import uuid4


class LessonStatus(Enum):
    """Status of a lesson plan."""
    
    DRAFT = "draft"
    TEACHER_REVIEW = "teacher_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_USE = "in_use"
    COMPLETED = "completed"


@dataclass
class LessonObjective:
    """A learning objective for a lesson."""
    
    description: str
    bloom_level: str  # e.g., "understand", "apply", "analyze"
    success_criteria: List[str]


@dataclass
class LessonActivity:
    """An activity within a lesson."""
    
    title: str
    duration_minutes: int
    description: str
    materials: List[str]
    differentiation_notes: str = ""


@dataclass
class LessonPlan:
    """A complete lesson plan."""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    subject: str = ""
    grade_level: str = ""
    duration_minutes: int = 60
    objectives: List[LessonObjective] = field(default_factory=list)
    activities: List[LessonActivity] = field(default_factory=list)
    materials: List[str] = field(default_factory=list)
    standards_alignment: List[str] = field(default_factory=list)
    differentiation_strategies: Dict[str, str] = field(default_factory=dict)
    assessment_methods: List[str] = field(default_factory=list)
    homework_assignment: str = ""
    notes: str = ""
    
    # Metadata
    status: LessonStatus = LessonStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""  # Teacher ID
    last_modified_at: datetime = field(default_factory=datetime.utcnow)
    modified_by: str = ""
    scheduled_date: Optional[date] = None
    
    # Audit trail
    requires_teacher_approval: bool = True
    ai_generated: bool = True
    teacher_edits: List[Dict[str, Any]] = field(default_factory=list)

    def mark_edited_by_teacher(self, teacher_id: str, changes: Dict[str, Any]) -> None:
        """
        Record teacher edit.
        
        Args:
            teacher_id: Teacher making the edit
            changes: Description of changes made
        """
        self.teacher_edits.append({
            'timestamp': datetime.utcnow(),
            'teacher_id': teacher_id,
            'changes': changes,
        })
        self.last_modified_at = datetime.utcnow()
        self.modified_by = teacher_id

    def approve(self, teacher_id: str) -> None:
        """
        Teacher approves the lesson plan.
        
        Args:
            teacher_id: Approving teacher
        """
        self.status = LessonStatus.APPROVED
        self.last_modified_at = datetime.utcnow()
        self.modified_by = teacher_id

    def reject(self, teacher_id: str, reason: str) -> None:
        """
        Teacher rejects the lesson plan.
        
        Args:
            teacher_id: Rejecting teacher
            reason: Reason for rejection
        """
        self.status = LessonStatus.REJECTED
        self.notes += f"\n\nRejected by {teacher_id}: {reason}"
        self.last_modified_at = datetime.utcnow()
        self.modified_by = teacher_id


class LessonGenerator:
    """Generates lesson plan drafts."""

    def generate_draft(
        self,
        subject: str,
        grade_level: str,
        topic: str,
        duration_minutes: int = 60,
        standards: Optional[List[str]] = None,
    ) -> LessonPlan:
        """
        Generate a lesson plan draft.
        
        Args:
            subject: Subject area
            grade_level: Target grade level
            topic: Lesson topic
            duration_minutes: Lesson duration
            standards: Educational standards to align with
            
        Returns:
            A DRAFT lesson plan requiring teacher review
            
        Note:
            This is a stub. In production, this would call an LLM
            with careful prompting to generate appropriate content.
        """
        plan = LessonPlan(
            title=f"{topic} - {grade_level} {subject}",
            subject=subject,
            grade_level=grade_level,
            duration_minutes=duration_minutes,
            standards_alignment=standards or [],
            status=LessonStatus.DRAFT,
            ai_generated=True,
            requires_teacher_approval=True,
        )
        
        # In production: LLM generates objectives, activities, etc.
        # For now, stub structure
        plan.objectives.append(LessonObjective(
            description=f"Students will understand {topic}",
            bloom_level="understand",
            success_criteria=["Can explain key concepts", "Can provide examples"],
        ))
        
        plan.activities.append(LessonActivity(
            title="Introduction",
            duration_minutes=10,
            description="Introduce topic and activate prior knowledge",
            materials=["Whiteboard", "Markers"],
        ))
        
        return plan

    def suggest_differentiation(
        self,
        plan: LessonPlan,
        student_needs: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Suggest differentiation strategies.
        
        Args:
            plan: The lesson plan
            student_needs: Aggregated classroom needs (not individual students)
            
        Returns:
            Differentiation suggestions by category
            
        Note:
            Operates on classroom-level patterns, not individual profiles.
        """
        suggestions = {
            "support": "Provide graphic organizers and sentence starters",
            "challenge": "Offer extension activities for advanced learners",
            "engagement": "Include multiple modalities (visual, auditory, kinesthetic)",
        }
        
        return suggestions
