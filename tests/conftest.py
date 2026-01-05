"""Test configuration and fixtures."""

import pytest
from teacher_api.security.encryption import EncryptionService
from teacher_api.security.key_management import KeyManager
from teacher_api.provenance.audit_log import AuditLog
from teacher_api.consent.manager import ConsentManager


@pytest.fixture
def encryption_service():
    """Provide encryption service for tests."""
    return EncryptionService()


@pytest.fixture
def key_manager():
    """Provide key manager for tests."""
    return KeyManager()


@pytest.fixture
def audit_log():
    """Provide audit log for tests."""
    return AuditLog()


@pytest.fixture
def consent_manager():
    """Provide consent manager for tests."""
    return ConsentManager()
