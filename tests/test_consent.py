"""
Tests for consent management.
"""

import pytest
from datetime import datetime, timedelta
from teacher_api.consent.manager import ConsentManager, ConsentScope, ConsentStatus


class TestConsentManagement:
    """Test consent functionality."""

    def test_grant_consent(self, consent_manager):
        """Should be able to grant consent."""
        grant = consent_manager.grant_consent(
            student_id="student_123",
            scope=ConsentScope.ACADEMIC_PATTERNS,
            granted_by="parent_456",
        )
        
        assert grant.status == ConsentStatus.GRANTED
        assert grant.student_id == "student_123"

    def test_check_consent_granted(self, consent_manager):
        """Should find granted consent."""
        consent_manager.grant_consent(
            student_id="student_123",
            scope=ConsentScope.BASIC_INFO,
            granted_by="parent_456",
        )
        
        has_consent = consent_manager.check_consent(
            "student_123",
            ConsentScope.BASIC_INFO,
        )
        
        assert has_consent is True

    def test_check_consent_not_granted(self, consent_manager):
        """Should return False for non-granted consent."""
        has_consent = consent_manager.check_consent(
            "student_123",
            ConsentScope.COLLABORATION,
        )
        
        assert has_consent is False

    def test_withdraw_consent(self, consent_manager):
        """Should be able to withdraw consent."""
        consent_manager.grant_consent(
            student_id="student_123",
            scope=ConsentScope.CLASSROOM_SIGNALS,
            granted_by="parent_456",
        )
        
        withdrawn = consent_manager.withdraw_consent(
            "student_123",
            ConsentScope.CLASSROOM_SIGNALS,
        )
        
        assert withdrawn is True
        
        # Should no longer have consent
        has_consent = consent_manager.check_consent(
            "student_123",
            ConsentScope.CLASSROOM_SIGNALS,
        )
        assert has_consent is False

    def test_consent_expiration(self, consent_manager):
        """Expired consent should not be valid."""
        # Grant consent that expires immediately
        consent_manager.grant_consent(
            student_id="student_123",
            scope=ConsentScope.SUPPORT_ROUTING,
            granted_by="parent_456",
            expires_at=datetime.utcnow() - timedelta(days=1),  # Already expired
        )
        
        has_consent = consent_manager.check_consent(
            "student_123",
            ConsentScope.SUPPORT_ROUTING,
        )
        
        assert has_consent is False

    def test_require_consent_enforces(self, consent_manager):
        """Should enforce consent requirement."""
        with pytest.raises(PermissionError, match="Consent required"):
            consent_manager.require_consent(
                "student_123",
                ConsentScope.ACADEMIC_PATTERNS,
            )

    def test_require_consent_allows_with_grant(self, consent_manager):
        """Should allow when consent granted."""
        consent_manager.grant_consent(
            student_id="student_123",
            scope=ConsentScope.ACADEMIC_PATTERNS,
            granted_by="parent_456",
        )
        
        # Should not raise
        consent_manager.require_consent(
            "student_123",
            ConsentScope.ACADEMIC_PATTERNS,
        )

    def test_get_consents(self, consent_manager):
        """Should retrieve all consents for student."""
        consent_manager.grant_consent(
            student_id="student_123",
            scope=ConsentScope.BASIC_INFO,
            granted_by="parent_456",
        )
        consent_manager.grant_consent(
            student_id="student_123",
            scope=ConsentScope.COLLABORATION,
            granted_by="parent_456",
        )
        
        consents = consent_manager.get_consents("student_123")
        
        assert len(consents) == 2
