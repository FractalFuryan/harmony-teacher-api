"""
Tests for audit logging and provenance.
"""

import pytest
from teacher_api.provenance.audit_log import AuditLog
from teacher_api.provenance.hashing import hash_data, hash_object, verify_hash


class TestAuditLog:
    """Test audit logging functionality."""

    def test_log_entry(self, audit_log):
        """Should create audit log entries."""
        entry = audit_log.log(
            actor="teacher_123",
            action="read",
            resource="lesson_plan:456",
            details={"reason": "review"},
        )
        
        assert entry.actor == "teacher_123"
        assert entry.action == "read"
        assert entry.resource == "lesson_plan:456"

    def test_audit_chain_integrity(self, audit_log):
        """Audit chain should maintain integrity."""
        audit_log.log("user1", "create", "resource1")
        audit_log.log("user2", "update", "resource1")
        audit_log.log("user3", "delete", "resource2")
        
        assert audit_log.verify_chain() is True

    def test_tamper_detection(self, audit_log):
        """Should detect tampering."""
        audit_log.log("user1", "action1", "resource1")
        entry = audit_log.log("user2", "action2", "resource2")
        
        # Tamper with entry
        entry.action = "modified_action"
        
        # Verification should fail
        assert audit_log.verify_chain() is False

    def test_query_by_actor(self, audit_log):
        """Should filter entries by actor."""
        audit_log.log("teacher_1", "read", "resource1")
        audit_log.log("teacher_2", "write", "resource2")
        audit_log.log("teacher_1", "update", "resource3")
        
        entries = audit_log.get_entries(actor="teacher_1")
        
        assert len(entries) == 2
        assert all(e.actor == "teacher_1" for e in entries)

    def test_query_by_resource(self, audit_log):
        """Should filter entries by resource."""
        audit_log.log("user1", "create", "lesson_plan:123")
        audit_log.log("user2", "read", "lesson_plan:123")
        audit_log.log("user3", "update", "lesson_plan:456")
        
        entries = audit_log.get_entries(resource="lesson_plan:123")
        
        assert len(entries) == 2

    def test_genesis_hash_linkage(self, audit_log):
        """First entry should link to genesis hash."""
        entry = audit_log.log("user", "action", "resource")
        
        assert entry.previous_hash == audit_log._genesis_hash


class TestHashing:
    """Test hashing utilities."""

    def test_hash_data_deterministic(self):
        """Same data should produce same hash."""
        data = b"test data"
        hash1 = hash_data(data)
        hash2 = hash_data(data)
        
        assert hash1 == hash2

    def test_hash_data_different(self):
        """Different data should produce different hashes."""
        hash1 = hash_data(b"data1")
        hash2 = hash_data(b"data2")
        
        assert hash1 != hash2

    def test_hash_object_deterministic(self):
        """Same object should produce same hash."""
        obj = {"key": "value", "number": 123}
        hash1 = hash_object(obj)
        hash2 = hash_object(obj)
        
        assert hash1 == hash2

    def test_hash_object_key_order_independent(self):
        """Key order shouldn't affect hash."""
        obj1 = {"a": 1, "b": 2}
        obj2 = {"b": 2, "a": 1}
        
        assert hash_object(obj1) == hash_object(obj2)

    def test_verify_hash_success(self):
        """Should verify correct hash."""
        data = b"test data"
        expected_hash = hash_data(data)
        
        assert verify_hash(data, expected_hash) is True

    def test_verify_hash_failure(self):
        """Should detect incorrect hash."""
        data = b"test data"
        wrong_hash = hash_data(b"different data")
        
        assert verify_hash(data, wrong_hash) is False
