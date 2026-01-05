"""
Encryption utilities for secure data handling.

All encryption uses modern, audited algorithms (AES-256-GCM).
Keys are never logged or transmitted in plaintext.
"""

from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import secrets


class EncryptionService:
    """Handles encryption/decryption with authenticated encryption (AEAD)."""

    def __init__(self, key_size: int = 256) -> None:
        """
        Initialize encryption service.
        
        Args:
            key_size: Key size in bits (256 recommended)
        """
        self.key_size = key_size // 8  # Convert to bytes

    def generate_key(self) -> bytes:
        """Generate a cryptographically secure random key."""
        return AESGCM.generate_key(bit_length=self.key_size * 8)

    def encrypt(self, plaintext: bytes, key: bytes, associated_data: bytes | None = None) -> Tuple[bytes, bytes]:
        """
        Encrypt data with authenticated encryption.
        
        Args:
            plaintext: Data to encrypt
            key: Encryption key
            associated_data: Additional authenticated data (not encrypted but authenticated)
            
        Returns:
            Tuple of (nonce, ciphertext)
        """
        aesgcm = AESGCM(key)
        nonce = secrets.token_bytes(12)  # 96-bit nonce
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
        return nonce, ciphertext

    def decrypt(
        self, 
        nonce: bytes, 
        ciphertext: bytes, 
        key: bytes, 
        associated_data: bytes | None = None
    ) -> bytes:
        """
        Decrypt authenticated encrypted data.
        
        Args:
            nonce: The nonce used during encryption
            ciphertext: Encrypted data
            key: Decryption key
            associated_data: Associated authenticated data
            
        Returns:
            Decrypted plaintext
            
        Raises:
            cryptography.exceptions.InvalidTag: If authentication fails
        """
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, associated_data)


def derive_key_from_password(password: str, salt: bytes, iterations: int = 480000) -> bytes:
    """
    Derive encryption key from password using PBKDF2.
    
    Args:
        password: User password
        salt: Cryptographic salt (must be unique per password)
        iterations: Number of iterations (higher = more secure but slower)
        
    Returns:
        Derived 256-bit key
    """
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode('utf-8'))
