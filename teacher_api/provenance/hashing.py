"""
Cryptographic hashing utilities for data integrity and provenance.

Uses SHA-256 for general hashing and BLAKE2 for high-performance scenarios.
"""

from hashlib import sha256, blake2b
from typing import Any
import json


def hash_data(data: bytes) -> str:
    """
    Hash raw bytes using SHA-256.
    
    Args:
        data: Raw bytes to hash
        
    Returns:
        Hex-encoded hash
    """
    return sha256(data).hexdigest()


def hash_object(obj: Any) -> str:
    """
    Hash a Python object (dict, list, etc.) deterministically.
    
    Args:
        obj: Object to hash
        
    Returns:
        Hex-encoded hash
        
    Note:
        Object is serialized to JSON with sorted keys for determinism.
    """
    serialized = json.dumps(obj, sort_keys=True, separators=(',', ':'))
    return sha256(serialized.encode('utf-8')).hexdigest()


def hash_file_content(content: bytes) -> str:
    """
    Hash file content using BLAKE2b (faster for large files).
    
    Args:
        content: File content as bytes
        
    Returns:
        Hex-encoded BLAKE2b hash
    """
    return blake2b(content).hexdigest()


def verify_hash(data: bytes, expected_hash: str, algorithm: str = "sha256") -> bool:
    """
    Verify that data matches the expected hash.
    
    Args:
        data: Data to verify
        expected_hash: Expected hash value
        algorithm: Hash algorithm ("sha256" or "blake2b")
        
    Returns:
        True if hash matches, False otherwise
    """
    if algorithm == "sha256":
        computed = sha256(data).hexdigest()
    elif algorithm == "blake2b":
        computed = blake2b(data).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    return computed == expected_hash
