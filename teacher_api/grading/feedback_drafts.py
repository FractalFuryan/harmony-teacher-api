"""
Rubric helpers and feedback draft generation.

All outputs are SUGGESTIONS only. Teacher has final authority.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class FeedbackTone(Enum):
    """Tone for feedback generation."""
    
    ENCOURAGING = "encouraging"
    CONSTRUCTIVE = "constructive"
    DIRECT = "direct"


@dataclass
class RubricCriterion:
    """A single criterion in a rubric."""
    
    name: str
    description: str
    max_points: int
    levels: Dict[int, str]  # points -> description


@dataclass
class Rubric:
    """A grading rubric."""
    
    title: str
    criteria: List[RubricCriterion]
    total_points: int
    
    def calculate_total(self) -> int:
        """Calculate total possible points."""
        return sum(c.max_points for c in self.criteria)


@dataclass
class FeedbackDraft:
    """A draft of feedback for a student assignment."""
    
    student_work_id: str
    suggested_comments: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    areas_for_growth: List[str] = field(default_factory=list)
    
    # Critical flags
    is_draft: bool = True
    requires_teacher_review: bool = True
    teacher_approved: bool = False
    
    def __post_init__(self) -> None:
        """Enforce that this is always a draft."""
        if not self.requires_teacher_review:
            raise ValueError("Feedback must always require teacher review")


class FeedbackAssistant:
    """Assists with feedback generation."""

    def draft_feedback(
        self,
        student_work: str,
        rubric: Optional[Rubric] = None,
        tone: FeedbackTone = FeedbackTone.CONSTRUCTIVE,
    ) -> FeedbackDraft:
        """
        Generate a DRAFT of feedback.
        
        Args:
            student_work: The student's work (text)
            rubric: Optional rubric to guide feedback
            tone: Desired tone
            
        Returns:
            A draft requiring teacher review
            
        Note:
            This is a stub. In production, LLM generates suggestions.
        """
        draft = FeedbackDraft(
            student_work_id="stub_id",
            is_draft=True,
            requires_teacher_review=True,
            teacher_approved=False,
        )
        
        # Stub suggestions
        draft.strengths.append("Clear organization and structure")
        draft.areas_for_growth.append("Consider adding more specific examples")
        draft.suggested_comments.append(
            "Good effort! Your main ideas are well-developed. "
            "To strengthen this further, try adding concrete examples."
        )
        
        return draft

    def suggest_rubric_scores(
        self,
        student_work: str,
        rubric: Rubric,
    ) -> Dict[str, Dict[str, any]]:
        """
        Suggest rubric scores ONLY as a starting point.
        
        Args:
            student_work: Student's work
            rubric: The rubric
            
        Returns:
            Suggested scores with metadata
            
        Warning:
            These are SUGGESTIONS only. Teacher must review and approve.
        """
        suggestions = {
            "scores": {},
            "requires_teacher_review": True,
            "is_final": False,
            "note": "These are AI suggestions only. Teacher review required before use.",
        }
        
        # In production: LLM suggests scores based on rubric
        for criterion in rubric.criteria:
            suggestions["scores"][criterion.name] = {
                "suggested_points": criterion.max_points // 2,  # Stub
                "max_points": criterion.max_points,
                "confidence": "low",  # Always mark as low confidence
                "reasoning": "Stub reasoning - teacher review needed",
            }
        
        return suggestions


class GradingSafeguards:
    """Enforces grading safety rules."""

    @staticmethod
    def validate_grading_output(output: Dict) -> None:
        """
        Ensure grading output follows safety rules.
        
        Args:
            output: Grading output to validate
            
        Raises:
            ValueError: If output violates safety rules
        """
        # Must require teacher review
        if not output.get("requires_teacher_review", False):
            raise ValueError("All grading outputs must require teacher review")
        
        # Cannot be marked as final
        if output.get("is_final", False):
            raise ValueError("AI cannot generate final grades")
        
        # Must be marked as draft/suggestion
        if not output.get("is_draft", True):
            raise ValueError("All AI grading must be marked as draft")

    @staticmethod
    def block_automated_grade_submission() -> None:
        """
        Architectural safeguard: grades cannot be auto-submitted.
        
        This is a marker function. In production, the API would have
        no endpoint for automated grade submission.
        """
        raise NotImplementedError(
            "Automated grade submission is prohibited by design. "
            "All grades must go through teacher review and manual approval."
        )
