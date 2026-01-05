"""
Tests for ethical constraint enforcement.

These tests ensure that ethical violations are IMPOSSIBLE by construction.
"""

import pytest
from teacher_api.ethics.constraints import (
    EthicsGuard,
    ConstraintViolation,
    ProhibitedOutputType,
)


class TestEthicsGuard:
    """Test suite for ethical constraint enforcement."""

    def test_blocks_diagnostic_labels(self):
        """CRITICAL: Diagnostic labels must be blocked."""
        output = {
            "output_type": ProhibitedOutputType.DIAGNOSTIC_LABEL.value,
            "content": "Student assessment",
        }
        
        with pytest.raises(ConstraintViolation) as exc_info:
            EthicsGuard.validate_output(output)
        
        assert "diagnostic_label" in str(exc_info.value).lower()

    def test_blocks_emotional_classification(self):
        """CRITICAL: Emotional classification must be blocked."""
        output = {
            "output_type": ProhibitedOutputType.EMOTIONAL_CLASSIFICATION.value,
            "content": "Mood analysis",
        }
        
        with pytest.raises(ConstraintViolation) as exc_info:
            EthicsGuard.validate_output(output)
        
        assert "emotional_classification" in str(exc_info.value).lower()

    def test_blocks_automated_grades_without_review(self):
        """CRITICAL: Automated grades without review must be blocked."""
        output = {
            "grade": "A",
            "score": 95,
            "requires_teacher_review": False,  # VIOLATION
        }
        
        with pytest.raises(ConstraintViolation) as exc_info:
            EthicsGuard.validate_output(output)
        
        assert "requires_teacher_review" in str(exc_info.value).lower()

    def test_allows_grades_with_review_flag(self):
        """Grades are OK if they require teacher review."""
        output = {
            "grade": "B",
            "score": 85,
            "requires_teacher_review": True,  # CORRECT
        }
        
        # Should not raise
        EthicsGuard.validate_output(output)

    def test_blocks_prohibited_diagnostic_terms(self):
        """CRITICAL: Diagnostic terminology must be detected."""
        output = {
            "content": "Student shows symptoms of ADHD",
        }
        
        with pytest.raises(ConstraintViolation) as exc_info:
            EthicsGuard.validate_output(output)
        
        assert "prohibited" in str(exc_info.value).lower()

    def test_blocks_prohibited_emotional_terms(self):
        """CRITICAL: Emotional classification terms must be detected."""
        output = {
            "content": "Student appears depressed and anxious",
        }
        
        with pytest.raises(ConstraintViolation) as exc_info:
            EthicsGuard.validate_output(output)
        
        assert "prohibited" in str(exc_info.value).lower()

    def test_allows_descriptive_language(self):
        """Descriptive, non-diagnostic language should be allowed."""
        output = {
            "content": "Student participation has decreased this week",
            "suggestion": "Consider checking in",
        }
        
        # Should not raise
        EthicsGuard.validate_output(output)

    def test_finds_prohibited_terms_in_nested_data(self):
        """Prohibited terms in nested structures must be detected."""
        output = {
            "data": {
                "analysis": {
                    "notes": "Shows symptoms consistent with disorder",
                }
            }
        }
        
        with pytest.raises(ConstraintViolation):
            EthicsGuard.validate_output(output)


class TestNonGoalEnforcement:
    """Ensure hard non-goals are enforced."""

    def test_no_student_profiling(self):
        """CRITICAL: Longitudinal student profiling must be blocked."""
        output = {
            "output_type": ProhibitedOutputType.LONGITUDINAL_PROFILE.value,
        }
        
        with pytest.raises(ConstraintViolation):
            EthicsGuard.validate_output(output)

    def test_no_predictive_outcomes(self):
        """CRITICAL: Predictive outcomes must be blocked."""
        output = {
            "output_type": ProhibitedOutputType.PREDICTIVE_OUTCOME.value,
        }
        
        with pytest.raises(ConstraintViolation):
            EthicsGuard.validate_output(output)

    def test_all_outputs_require_teacher_judgment(self):
        """All sensitive outputs must require teacher judgment."""
        # This is enforced in specific modules (grading, support, etc.)
        # Test here as integration check
        from teacher_api.support.awareness_flags import AwarenessFlag, FlagType, FlagSeverity
        from datetime import datetime
        
        flag = AwarenessFlag(
            flag_id="test",
            flag_type=FlagType.PARTICIPATION_CHANGE,
            severity=FlagSeverity.ATTENTION,
            description="Test flag",
            suggested_action="Test action",
            context="Test",
            detected_at=datetime.utcnow(),
            student_id="test_student",
        )
        
        assert flag.requires_teacher_judgment is True
        assert flag.is_diagnostic is False

    def test_awareness_flags_cannot_be_diagnostic(self):
        """Awareness flags must not be diagnostic."""
        from teacher_api.support.awareness_flags import AwarenessFlag, FlagType, FlagSeverity
        from datetime import datetime
        
        with pytest.raises(ValueError, match="cannot be diagnostic"):
            AwarenessFlag(
                flag_id="test",
                flag_type=FlagType.PARTICIPATION_CHANGE,
                severity=FlagSeverity.ATTENTION,
                description="Test",
                suggested_action="Test",
                context="Test",
                detected_at=datetime.utcnow(),
                student_id="test",
                is_diagnostic=True,  # VIOLATION
            )

    def test_feedback_must_require_review(self):
        """Feedback drafts must require teacher review."""
        from teacher_api.grading.feedback_drafts import FeedbackDraft
        
        with pytest.raises(ValueError, match="require teacher review"):
            FeedbackDraft(
                student_work_id="test",
                requires_teacher_review=False,  # VIOLATION
            )
