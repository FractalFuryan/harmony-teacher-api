"""
Hard ethical constraints enforced at runtime.

These constraints cannot be bypassed - they are structural safeguards.
"""

from enum import Enum
from typing import Any, Dict, List
from dataclasses import dataclass


class ProhibitedOutputType(Enum):
    """Types of outputs that are strictly forbidden."""
    
    DIAGNOSTIC_LABEL = "diagnostic_label"
    EMOTIONAL_CLASSIFICATION = "emotional_classification"
    AUTOMATED_GRADE = "automated_grade"
    STUDENT_SCORE = "student_score"
    LONGITUDINAL_PROFILE = "longitudinal_profile"
    PREDICTIVE_OUTCOME = "predictive_outcome"


@dataclass
class ConstraintViolation(Exception):
    """Raised when an ethical constraint is violated."""
    
    constraint: str
    details: str
    
    def __str__(self) -> str:
        return f"Ethical constraint violated: {self.constraint} - {self.details}"


class EthicsGuard:
    """Enforces ethical constraints on all outputs."""

    # Prohibited terms that indicate diagnostic/classification attempts
    PROHIBITED_TERMS = {
        # Diagnostic terms
        "adhd", "autism", "disorder", "syndrome", "condition",
        "diagnosis", "diagnosed", "symptom",
        
        # Emotional classification
        "depressed", "anxious", "disturbed", "troubled",
        
        # Scoring/grading terms when used automatically
        "final_grade", "score", "points", "percentage",
        
        # Profiling terms
        "risk_level", "trajectory", "prediction", "likelihood",
    }

    @staticmethod
    def validate_output(output: Dict[str, Any], context: str = "") -> None:
        """
        Validate that output doesn't violate ethical constraints.
        
        Args:
            output: The output to validate
            context: Additional context about the operation
            
        Raises:
            ConstraintViolation: If output violates constraints
        """
        # Check for prohibited output types
        if "output_type" in output:
            try:
                output_type = ProhibitedOutputType(output["output_type"])
                raise ConstraintViolation(
                    constraint="prohibited_output_type",
                    details=f"Output type '{output_type.value}' is strictly forbidden. Context: {context}"
                )
            except ValueError:
                # Not a prohibited type, continue
                pass
        
        # Check for automated grading without review flag
        if "grade" in output or "score" in output:
            if not output.get("requires_teacher_review", False):
                raise ConstraintViolation(
                    constraint="automated_grading",
                    details="Grades/scores must require teacher review. Set requires_teacher_review=True."
                )
        
        # Scan text content for prohibited terms
        text_content = EthicsGuard._extract_text(output)
        violations = EthicsGuard._find_prohibited_terms(text_content)
        
        if violations:
            raise ConstraintViolation(
                constraint="prohibited_language",
                details=f"Prohibited terms found: {', '.join(violations)}. Context: {context}"
            )

    @staticmethod
    def _extract_text(obj: Any) -> str:
        """Recursively extract all text from an object."""
        if isinstance(obj, str):
            return obj.lower()
        elif isinstance(obj, dict):
            return " ".join(EthicsGuard._extract_text(v) for v in obj.values())
        elif isinstance(obj, list):
            return " ".join(EthicsGuard._extract_text(item) for item in obj)
        else:
            return str(obj).lower()

    @staticmethod
    def _find_prohibited_terms(text: str) -> List[str]:
        """Find prohibited terms in text."""
        words = set(text.split())
        return [term for term in EthicsGuard.PROHIBITED_TERMS if term in words]

    @staticmethod
    def require_teacher_override(operation: str) -> None:
        """
        Mark that an operation requires explicit teacher override.
        
        Args:
            operation: Description of the operation
            
        Note:
            This is a marker function. In production, this would integrate
            with the UI to require explicit teacher confirmation.
        """
        # In production, this would trigger UI confirmation flow
        pass

    @staticmethod
    def enforce_consent_gate(student_id: str, data_type: str) -> bool:
        """
        Check if consent exists for accessing student data.
        
        Args:
            student_id: Student identifier
            data_type: Type of data being accessed
            
        Returns:
            True if consent exists (stub - integrate with consent module)
        """
        # Stub - will integrate with consent module
        return True
