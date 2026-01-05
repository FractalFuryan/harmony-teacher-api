"""
Key management and rotation utilities.

Keys are versioned and rotated on a schedule.
Old keys are retained for decryption but not used for new encryption.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict
import secrets


@dataclass
class KeyMetadata:
    """Metadata for a cryptographic key."""
    
    key_id: str
    created_at: datetime
    expires_at: datetime
    is_active: bool
    purpose: str  # "encryption", "signing", etc.


class KeyManager:
    """Manages cryptographic key lifecycle and rotation."""

    def __init__(self, rotation_days: int = 90) -> None:
        """
        Initialize key manager.
        
        Args:
            rotation_days: Days before key rotation
        """
        self.rotation_days = rotation_days
        self._keys: Dict[str, bytes] = {}
        self._metadata: Dict[str, KeyMetadata] = {}
        self._active_key_id: str | None = None

    def generate_key(self, purpose: str = "encryption") -> str:
        """
        Generate and register a new key.
        
        Args:
            purpose: Purpose of the key
            
        Returns:
            Key ID
        """
        key_id = secrets.token_urlsafe(16)
        key = secrets.token_bytes(32)  # 256-bit key
        
        now = datetime.utcnow()
        metadata = KeyMetadata(
            key_id=key_id,
            created_at=now,
            expires_at=now + timedelta(days=self.rotation_days),
            is_active=True,
            purpose=purpose,
        )
        
        self._keys[key_id] = key
        self._metadata[key_id] = metadata
        
        # Deactivate previous active key if exists
        if self._active_key_id:
            self._metadata[self._active_key_id].is_active = False
        
        self._active_key_id = key_id
        return key_id

    def get_active_key(self) -> tuple[str, bytes]:
        """
        Get the currently active key.
        
        Returns:
            Tuple of (key_id, key)
            
        Raises:
            ValueError: If no active key exists
        """
        if not self._active_key_id:
            raise ValueError("No active key. Generate one first.")
        
        return self._active_key_id, self._keys[self._active_key_id]

    def get_key(self, key_id: str) -> bytes:
        """
        Get a specific key by ID (for decryption of old data).
        
        Args:
            key_id: The key identifier
            
        Returns:
            The key bytes
            
        Raises:
            KeyError: If key not found
        """
        return self._keys[key_id]

    def rotate_if_needed(self) -> bool:
        """
        Check if rotation is needed and perform it.
        
        Returns:
            True if rotation occurred
        """
        if not self._active_key_id:
            return False
        
        metadata = self._metadata[self._active_key_id]
        if datetime.utcnow() >= metadata.expires_at:
            self.generate_key(purpose=metadata.purpose)
            return True
        
        return False

    def list_keys(self) -> Dict[str, KeyMetadata]:
        """List all keys with their metadata."""
        return self._metadata.copy()
