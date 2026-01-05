"""
Tests for security components.
"""

import pytest
from teacher_api.security.encryption import EncryptionService, derive_key_from_password
from teacher_api.security.key_management import KeyManager
from cryptography.exceptions import InvalidTag


class TestEncryption:
    """Test encryption functionality."""

    def test_encrypt_decrypt_roundtrip(self, encryption_service):
        """Data should survive encryption and decryption."""
        plaintext = b"sensitive student data"
        key = encryption_service.generate_key()
        
        nonce, ciphertext = encryption_service.encrypt(plaintext, key)
        decrypted = encryption_service.decrypt(nonce, ciphertext, key)
        
        assert decrypted == plaintext

    def test_encryption_with_authenticated_data(self, encryption_service):
        """Authenticated encryption should protect associated data."""
        plaintext = b"secret message"
        associated_data = b"metadata"
        key = encryption_service.generate_key()
        
        nonce, ciphertext = encryption_service.encrypt(plaintext, key, associated_data)
        decrypted = encryption_service.decrypt(nonce, ciphertext, key, associated_data)
        
        assert decrypted == plaintext

    def test_tamper_detection(self, encryption_service):
        """Tampering should be detected."""
        plaintext = b"important data"
        key = encryption_service.generate_key()
        
        nonce, ciphertext = encryption_service.encrypt(plaintext, key)
        
        # Tamper with ciphertext
        tampered = bytes([b ^ 1 for b in ciphertext])
        
        with pytest.raises(InvalidTag):
            encryption_service.decrypt(nonce, tampered, key)

    def test_key_derivation_deterministic(self):
        """Same password and salt should produce same key."""
        password = "strong_password"
        salt = b"unique_salt_12345678"
        
        key1 = derive_key_from_password(password, salt)
        key2 = derive_key_from_password(password, salt)
        
        assert key1 == key2

    def test_key_derivation_different_salts(self):
        """Different salts should produce different keys."""
        password = "strong_password"
        salt1 = b"salt_1_1234567890123"
        salt2 = b"salt_2_1234567890123"
        
        key1 = derive_key_from_password(password, salt1)
        key2 = derive_key_from_password(password, salt2)
        
        assert key1 != key2


class TestKeyManagement:
    """Test key management and rotation."""

    def test_generate_key(self, key_manager):
        """Should generate valid keys."""
        key_id = key_manager.generate_key()
        
        assert key_id is not None
        assert len(key_id) > 0

    def test_get_active_key(self, key_manager):
        """Should retrieve active key."""
        key_id = key_manager.generate_key()
        active_id, active_key = key_manager.get_active_key()
        
        assert active_id == key_id
        assert len(active_key) == 32  # 256 bits

    def test_key_rotation(self, key_manager):
        """Key rotation should work correctly."""
        key_id_1 = key_manager.generate_key()
        key_id_2 = key_manager.generate_key()
        
        # Second key should be active
        active_id, _ = key_manager.get_active_key()
        assert active_id == key_id_2
        
        # First key should be deactivated
        metadata = key_manager.list_keys()
        assert metadata[key_id_1].is_active is False
        assert metadata[key_id_2].is_active is True

    def test_old_keys_remain_accessible(self, key_manager):
        """Old keys should remain accessible for decryption."""
        key_id_1 = key_manager.generate_key()
        key_1 = key_manager.get_key(key_id_1)
        
        key_manager.generate_key()  # Rotate
        
        # Old key should still be retrievable
        old_key = key_manager.get_key(key_id_1)
        assert old_key == key_1
